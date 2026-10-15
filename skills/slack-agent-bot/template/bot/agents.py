"""Running the Claude Code CLI headlessly (`claude -p`).

Two shapes:
  run_json()  short runs (triage, plan): wait, parse the JSON object it returns.
  Streamed    long runs (implementer): follow the event stream so progress can
              be posted, the pid can be recorded for `botctl stop`, and the
              final report can be recovered even if the agent said one more
              sentence after its JSON.
"""

import json
import logging
import re
import subprocess
import threading
import time
from pathlib import Path
from typing import Callable, Optional

from . import config

log = logging.getLogger("bot.agents")


class AgentError(RuntimeError):
    pass


def command(prompt: str, model: str, allowed: list[str], denied: list[str],
            output: str = "json", resume: Optional[str] = None) -> list[str]:
    cmd = [config.CLAUDE_BIN, "-p", prompt, "--model", model, "--output-format", output]
    if output == "stream-json":
        cmd.append("--verbose")
    if resume:
        cmd += ["--resume", resume]
    cmd += ["--allowedTools", *allowed, "--disallowedTools", *denied]
    if config.MCP_CONFIG and any(t.startswith("mcp__") for t in allowed):
        cmd += ["--mcp-config", config.MCP_CONFIG]
    return cmd


def find_json(text: str, key: Optional[str] = None) -> Optional[dict]:
    """The last JSON object in `text` (optionally one carrying `key`)."""
    fenced = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    for block in reversed(fenced):
        try:
            obj = json.loads(block)
            if isinstance(obj, dict) and (key is None or key in obj):
                return obj
        except json.JSONDecodeError:
            pass
    idx = len(text)
    while True:
        idx = text.rfind("{", 0, idx)
        if idx == -1:
            return None
        end = len(text)
        while True:
            end = text.rfind("}", idx, end)
            if end == -1:
                break
            try:
                obj = json.loads(text[idx:end + 1])
            except json.JSONDecodeError:
                continue
            if isinstance(obj, dict) and (key is None or key in obj):
                return obj
            break


def _envelope(stdout: str) -> dict:
    for candidate in (stdout, *reversed(stdout.splitlines())):
        candidate = candidate.strip()
        if candidate.startswith("{"):
            try:
                obj = json.loads(candidate)
            except json.JSONDecodeError:
                continue
            if isinstance(obj, dict) and "result" in obj:
                return obj
    raise AgentError("no result envelope in CLI output")


def run_json(prompt: str, model: str, allowed: list[str], denied: list[str],
             timeout: int, cwd: Path, env: dict, key: str) -> dict:
    """One short headless run. Returns the JSON object the model replied with."""
    try:
        r = subprocess.run(command(prompt, model, allowed, denied), cwd=str(cwd),
                           capture_output=True, text=True, timeout=timeout, env=env)
    except subprocess.TimeoutExpired as exc:
        raise AgentError(f"timed out after {timeout}s") from exc
    if r.returncode != 0:
        raise AgentError(f"claude CLI exited {r.returncode}: {(r.stderr or r.stdout).strip()[:400]}")
    env_obj = _envelope(r.stdout)
    if env_obj.get("is_error"):
        raise AgentError(f"model error: {str(env_obj.get('result'))[:400]}")
    obj = find_json(env_obj.get("result") or "", key)
    if obj is None:
        raise AgentError("reply contained no JSON object")
    obj["_meta"] = {"model": model, "cost_usd": env_obj.get("total_cost_usd"),
                    "session_id": env_obj.get("session_id")}
    return obj


def describe_tool(name: str, inp: dict) -> str:
    """One short line about a tool call, for the journal."""
    inp = inp or {}
    if name == "Bash":
        return (inp.get("description") or inp.get("command") or "running a command")[:80]
    if name in ("Read", "Edit", "Write", "MultiEdit"):
        return f"{name.lower()} {(inp.get('file_path') or '').rsplit('/', 1)[-1]}"
    if name in ("Grep", "Glob"):
        return f"searching {inp.get('pattern', '')[:40]}"
    return name.split("__")[-1]


class Streamed:
    """A long run whose events are followed as they happen."""

    def __init__(self, cmd: list[str], cwd: Path, env: dict,
                 on_start: Optional[Callable[[int], None]] = None) -> None:
        self.started = time.time()
        self.steps = 0
        self.recent: list[str] = []
        self.texts: list[str] = []
        self.envelope: Optional[dict] = None
        self._lock = threading.Lock()
        self.proc = subprocess.Popen(cmd, cwd=str(cwd), env=env, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, text=True)
        if on_start:
            on_start(self.proc.pid)
        self._reader = threading.Thread(target=self._read, daemon=True)
        self._reader.start()

    def _read(self) -> None:
        for line in self.proc.stdout:  # type: ignore[union-attr]
            line = line.strip()
            if not line.startswith("{"):
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") == "assistant":
                for part in (event.get("message") or {}).get("content") or []:
                    with self._lock:
                        if part.get("type") == "text" and part.get("text", "").strip():
                            self.texts = (self.texts + [part["text"]])[-12:]
                        elif part.get("type") == "tool_use":
                            self.steps += 1
                            self.recent = (self.recent + [describe_tool(part.get("name", ""), part.get("input"))])[-4:]
            elif event.get("type") == "result":
                self.envelope = event

    def wait(self, timeout: int, on_progress: Optional[Callable[[int], None]] = None,
             interval: int = 600) -> dict:
        """Wait for the run; call on_progress(minutes) every `interval` seconds."""
        stop = threading.Event()

        def ticker() -> None:
            while not stop.wait(interval):
                if self.proc.poll() is not None:
                    return
                try:
                    on_progress(int((time.time() - self.started) // 60))  # type: ignore[misc]
                except Exception:  # noqa: BLE001
                    log.exception("progress callback failed")

        if on_progress:
            threading.Thread(target=ticker, daemon=True).start()
        try:
            self.proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            self.proc.kill()
            self.proc.wait()
            raise AgentError(f"timed out after {timeout // 60} min "
                             f"({self.steps} steps; last: {', '.join(self.recent[-2:]) or 'n/a'})") from exc
        finally:
            stop.set()
            self._reader.join(timeout=10)
            err = ""
            if self.proc.stderr:
                err = self.proc.stderr.read().strip() if self.proc.returncode else ""
                self.proc.stderr.close()
            if self.proc.stdout:
                self.proc.stdout.close()
        if self.proc.returncode != 0:
            raise AgentError(f"claude CLI exited {self.proc.returncode}: {err[:400]}")
        if self.envelope is None:
            raise AgentError("no result event in CLI output")
        if self.envelope.get("is_error"):
            raise AgentError(f"model error: {str(self.envelope.get('result'))[:400]}")
        return self.envelope

    def report(self, key: str = "status") -> Optional[dict]:
        """The agent's structured report. The CLI's `result` is only its LAST
        message, so if it said one more sentence after the JSON, look back."""
        for text in [(self.envelope or {}).get("result") or ""] + list(reversed(self.texts)):
            obj = find_json(text, key)
            if obj is not None:
                obj["_meta"] = {"session_id": (self.envelope or {}).get("session_id"),
                                "cost_usd": (self.envelope or {}).get("total_cost_usd"),
                                "turns": (self.envelope or {}).get("num_turns")}
                return obj
        return None
