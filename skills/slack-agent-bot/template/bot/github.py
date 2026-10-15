"""A GitHub issue per code change: the durable record, independent of Slack
retention and of this box. Optional (BOT_OPEN_ISSUES). Uses the `gh` CLI that
is already logged in on the host; failures degrade the record, never the job."""

import json
import logging
import subprocess
from typing import Optional

from . import config

log = logging.getLogger("bot.github")
MARKER = "bot-request-id:"


def _gh(*args: str) -> str:
    r = subprocess.run(["gh", *args], capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:300])
    return r.stdout.strip()


def ensure_issue(request: dict, brief: dict) -> Optional[str]:
    if not config.OPEN_ISSUES:
        return None
    rid = request["request_id"]
    try:
        found = json.loads(_gh("issue", "list", "--repo", config.REPO_SLUG, "--state", "all",
                               "--search", f'"{MARKER} {rid}"', "--json", "url,body") or "[]")
        for issue in found:
            if f"{MARKER} {rid}" in (issue.get("body") or ""):
                return issue["url"]
    except (RuntimeError, ValueError) as exc:
        log.warning("issue search failed: %s", exc)

    c = brief["classification"]
    text = brief.get("resolved_request") or request["slack"]["message"]
    title = " ".join(text.split())
    title = title if len(title) <= 70 else title[:67] + "..."
    steps = "\n".join(f"- {s}" for s in brief.get("plan") or []) or "_none_"
    body = (f"### Request (from Slack)\n\n> {text.strip()}\n\n"
            f"Requested by Slack user `{request['slack'].get('user_id')}`. "
            f"{request['slack'].get('permalink') or ''}\n\n"
            f"### Brief\n\n{c['task_type']}, {c.get('scope')} scope, {c.get('risk')} risk, "
            f"**{c.get('execution_mode')}**\n\n{steps}\n\n{brief.get('reasoning_summary', '')}\n\n"
            f"---\n<sub>Opened by the Slack bot. {MARKER} {rid}</sub>")
    try:
        url = _gh("issue", "create", "--repo", config.REPO_SLUG,
                  "--title", f"[{c['task_type']}] {title}", "--body", body)
        return url.splitlines()[-1].strip()
    except RuntimeError as exc:
        log.warning("could not open issue: %s", exc)
        return None


def comment(issue_url: Optional[str], text: str) -> None:
    if not issue_url:
        return
    try:
        _gh("issue", "comment", issue_url, "--body", text)
    except RuntimeError as exc:
        log.warning("could not comment on %s: %s", issue_url, exc)
