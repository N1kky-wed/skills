"""Messages that arrive in a thread while its job is still running.

They amend the running job instead of starting new ones ("pull 30" then "make
it 50" must not become two jobs). A `claude -p` process cannot be spoken to
once started, so two channels reach it:

  1. the prompt lists the follow-ups that had arrived when it was rendered;
  2. `.bot/followups.md` in the job's worktree is rewritten on every new one,
     and the prompt tells the agent to re-read it before each major step and
     before finishing. `.bot/` is in the repo's info/exclude so it can never
     be committed.
"""

import datetime
import logging
from pathlib import Path

from . import config

log = logging.getLogger("bot.followups")

RELATIVE = Path(".bot") / "followups.md"


def worktree_for(request_id: str) -> Path:
    return config.WORK_ROOT / config.safe_id(request_id)


def _stamp(ts: str) -> str:
    try:
        return datetime.datetime.fromtimestamp(float(ts)).strftime("%H:%M:%S")
    except (TypeError, ValueError):
        return str(ts)


def render(rows: list[dict]) -> str:
    if not rows:
        return "# Follow-ups\n\n_none so far_\n"
    out = ["# Follow-ups", "", "Later messages from the thread, oldest first. Each one "
           "amends the request. Honour them all before you finish.", ""]
    for r in rows:
        out += [f"## {_stamp(r['message_ts'])}", "", (r.get("text") or "").strip(), ""]
    return "\n".join(out)


def write(worktree: Path, rows: list[dict]) -> bool:
    if not worktree.is_dir():
        return False
    target = worktree / RELATIVE
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(".tmp")
    tmp.write_text(render(rows), encoding="utf-8")
    tmp.replace(target)
    return True


def exclude_from_git(repo: Path) -> None:
    info = repo / ".git" / "info"
    try:
        info.mkdir(parents=True, exist_ok=True)
        exclude = info / "exclude"
        existing = exclude.read_text() if exclude.exists() else ""
        if ".bot/" not in existing.splitlines():
            with exclude.open("a") as fh:
                fh.write(("" if not existing or existing.endswith("\n") else "\n") + ".bot/\n")
    except OSError as exc:
        log.warning("could not exclude .bot/: %s", exc)


def attach(store, running_id: str, event: dict) -> int:
    store.add_followup(running_id, event["ts"], event.get("user"),
                       (event.get("text") or "").replace(config.MENTION_TOKEN, "").strip())
    rows = store.followups(running_id)
    write(worktree_for(running_id), rows)
    return len(rows)


def prompt_section(rows: list[dict] | None) -> str:
    listed = "\n".join(f"  - {_stamp(r['message_ts'])}: {(r.get('text') or '').strip()}"
                       for r in rows or []) or "  _none yet_"
    return f"""# Follow-ups from the thread

The requester may send more messages while you work. They amend this request.
The ones that had arrived when this prompt was written are below; every later
one is appended to `{RELATIVE.as_posix()}` in your working directory. **Read
that file before each major step and again before you finish.** If one changes
the scope after you did the work, redo the affected part. Never commit it.

Already in hand:
{listed}"""
