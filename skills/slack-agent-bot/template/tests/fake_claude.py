#!/usr/bin/env python3
"""A stand-in for the `claude` CLI, for tests. No network, no cost.

Reads `scenario.json` next to itself:
  {"triage": {...}, "plan": {...}, "impl": "commit|file|bad_then_fix|sleep|noreport"}
and answers each phase the way the real CLI's -p mode does.
"""

import json
import os
import pathlib
import subprocess
import sys
import time

here = pathlib.Path(__file__).resolve().parent
scenario = json.loads((here / "scenario.json").read_text())
args = sys.argv[1:]
prompt = args[args.index("-p") + 1]
fmt = args[args.index("--output-format") + 1] if "--output-format" in args else "text"
(here / "calls.log").open("a").write(json.dumps({"argv": args[:1] + args[2:], "cwd": os.getcwd()}) + "\n")


def envelope(obj: dict) -> None:
    print(json.dumps({"type": "result", "is_error": False, "session_id": "s1",
                      "result": "here you go\n```json\n" + json.dumps(obj) + "\n```"}))


def git(*a: str) -> None:
    subprocess.run(["git", *a], check=True, capture_output=True)


if "first responder" in prompt:
    envelope(scenario["triage"])
elif "planning analyst" in prompt:
    envelope(scenario["plan"])
else:
    impl = scenario.get("impl", "commit")
    report = {"status": "success", "summary": "done, added hello.txt",
              "tests": {"passed": True, "commands": ["true"]},
              "pr_title": "feat: add hello", "pr_body": "adds hello.txt", "error": None}
    if "push was rejected" in prompt:
        git("rm", "-q", "bad.txt")
        git("commit", "-qm", "fix: drop bad file")
    elif impl == "commit":
        pathlib.Path("hello.txt").write_text("hello\n")
        git("add", "hello.txt")
        git("commit", "-qm", "feat: add hello")
    elif impl == "bad_then_fix":
        pathlib.Path("bad.txt").write_text("nope\n")
        git("add", "bad.txt")
        git("commit", "-qm", "feat: add bad")
    elif impl == "file":
        pathlib.Path(os.environ["BOT_OUT_DIR"], "report.csv").write_text("a,b\n1,2\n")
        report["summary"] = "42 rows, csv attached"
        report["env_seen"] = sorted(k for k in os.environ if k.startswith("DB_"))
        report["summary"] += " env=" + ",".join(report["env_seen"])
    elif impl == "sleep":
        time.sleep(60)
    events = [
        {"type": "assistant", "message": {"content": [
            {"type": "tool_use", "name": "Bash", "input": {"description": "Running tests"}}]}},
        {"type": "assistant", "message": {"content": [{"type": "text", "text": json.dumps(report)}]}},
    ]
    if impl != "noreport":
        # one more sentence after the JSON: the bot must still find the report
        events.append({"type": "assistant", "message": {"content": [{"type": "text", "text": "all done!"}]}})
    else:
        events = events[:1]
    for e in events:
        print(json.dumps(e), flush=True)
    print(json.dumps({"type": "result", "is_error": False, "session_id": "s1",
                      "result": "all done!", "num_turns": 3}), flush=True)
