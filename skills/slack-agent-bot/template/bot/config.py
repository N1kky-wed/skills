"""All configuration, in one place.

Every value comes from `.env` next to the code (mode 0600). The file is read
into a private dict and NEVER loaded into os.environ: every agent is a
subprocess, subprocesses inherit the environment, and an agent reading
untrusted Slack text must not be one `env` away from every secret on the box.
Each phase gets an explicit allowlist instead (see `scoped_env`).
"""

import json
import os
from pathlib import Path

from dotenv import dotenv_values

ROOT = Path(os.environ.get("BOT_ROOT") or Path(__file__).resolve().parent.parent)

_SECRETS: dict[str, str] = {
    k: v for k, v in dotenv_values(ROOT / ".env").items() if v is not None
}


def _get(name: str, default: str = "") -> str:
    """A value from .env, with the process environment as an override."""
    return os.environ.get(name) or _SECRETS.get(name) or default


def _list(name: str, default: str = "") -> list[str]:
    return [x.strip() for x in _get(name, default).split(",") if x.strip()]


def _flag(name: str, default: str = "false") -> bool:
    return _get(name, default).lower() in ("1", "true", "yes", "on")


# ── Slack ───────────────────────────────────────────────────────────────────
SLACK_BOT_TOKEN = _get("SLACK_BOT_TOKEN")      # xoxb-...
SLACK_APP_TOKEN = _get("SLACK_APP_TOKEN")      # xapp-... (Socket Mode)
CHANNEL_ID = _get("BOT_CHANNEL_ID")            # the one channel the bot works in
BOT_USER_ID = _get("BOT_USER_ID")              # the bot's own user id (U...)
MENTION_TOKEN = f"<@{BOT_USER_ID}>"

# The person who runs the bot. Named in "ask <owner>" replies.
OWNER_USER_ID = _get("OWNER_USER_ID")

# Anyone in the channel can ask questions, look things up, or get a PR opened.
# Only these users can cause anything to land without review: a direct push,
# or an `action` that changes live data. Enforced by withholding credentials
# and denying tools, not by asking the model nicely.
WRITE_ALLOWED_USER_IDS = set(_list("WRITE_ALLOWED_USER_IDS", OWNER_USER_ID))


def can_write(user_id: str | None) -> bool:
    return bool(user_id) and user_id in WRITE_ALLOWED_USER_IDS


# Optional nicknames: {"U123": "boss"}. The bot uses the name in every reply to
# that person and is extra warm with them.
try:
    ADDRESS_AS: dict[str, str] = json.loads(_get("ADDRESS_AS", "{}"))
except ValueError:
    ADDRESS_AS = {}


def address_note(user_id: str | None) -> str:
    name = ADDRESS_AS.get(user_id or "")
    if not name:
        return ""
    return (f'This request is from {user_id}. Address them as "{name}" in every '
            f'message you write back, and be especially warm and respectful with '
            f'them. Still short: warmth is in the tone, not the length.')


def with_name(text: str, user_id: str | None) -> str:
    """A canned line with the requester's nickname worked in."""
    name = ADDRESS_AS.get(user_id or "")
    return f"{text.rstrip(' .!')}, {name}" if name else text


# ── Behaviour ───────────────────────────────────────────────────────────────
WORKERS = int(_get("BOT_WORKERS", "2"))
QUEUE_ACK_AFTER_SECONDS = int(_get("QUEUE_ACK_AFTER_SECONDS", "20"))
# After the bot has spoken in a thread, an untagged reply from the same person
# counts as a follow-up for this long.
FOLLOW_UP_WINDOW_SECONDS = int(_get("FOLLOW_UP_WINDOW_SECONDS", str(48 * 3600)))
FORCE_PR = _flag("BOT_FORCE_PR")          # every code change ships as a PR
DRY_RUN = _flag("BOT_DRY_RUN")            # log matching messages, do nothing else
OPEN_ISSUES = _flag("BOT_OPEN_ISSUES", "true")  # a GitHub issue per code change
PROGRESS_INTERVAL_SECONDS = int(_get("PROGRESS_INTERVAL_SECONDS", "600"))

# ── Repository ──────────────────────────────────────────────────────────────
REPO_SLUG = _get("REPO_SLUG")                              # owner/name
REPO_PATH = Path(_get("REPO_PATH", str(ROOT / "repo")))    # canonical checkout
DEFAULT_BRANCH = _get("DEFAULT_BRANCH", "main")
# Run once in each fresh worktree so tests can run, e.g.
# "pnpm install --frozen-lockfile --prefer-offline" or "pip install -e .[dev]".
SETUP_COMMAND = _get("SETUP_COMMAND")
SETUP_TIMEOUT_SECONDS = int(_get("SETUP_TIMEOUT_SECONDS", "900"))

# ── Claude ──────────────────────────────────────────────────────────────────
CLAUDE_BIN = _get("CLAUDE_BIN", "claude")
TRIAGE_MODEL = _get("TRIAGE_MODEL", "sonnet")
PLAN_MODEL = _get("PLAN_MODEL", "opus")
IMPLEMENTER_MODEL = _get("IMPLEMENTER_MODEL", "opus")
# Cheap model for fresh progress lines. Empty = use the canned pool only.
PROGRESS_MODEL = _get("PROGRESS_MODEL", "")
TRIAGE_TIMEOUT_SECONDS = int(_get("TRIAGE_TIMEOUT_SECONDS", "300"))
PLAN_TIMEOUT_SECONDS = int(_get("PLAN_TIMEOUT_SECONDS", "900"))
IMPLEMENTER_TIMEOUT_SECONDS = int(_get("IMPLEMENTER_TIMEOUT_SECONDS", str(3 * 3600)))

# Optional MCP servers (a claude --mcp-config file kept OUTSIDE the repo).
MCP_CONFIG = _get("MCP_CONFIG")
# Fully-qualified MCP tool names (mcp__server__tool). READ tools go to every
# phase; WRITE tools only to runs a person asked for (never the triage pass of
# a heartbeat-style unprompted run, never a requester who cannot write).
MCP_READ_TOOLS = _list("MCP_READ_TOOLS")
MCP_WRITE_TOOLS = _list("MCP_WRITE_TOOLS")

# ── Tool grants ─────────────────────────────────────────────────────────────
# The allowlist is the enforcement, not the prompt. Triage and planning read;
# they cannot edit, commit or push whatever the Slack message says.
READ_ONLY_TOOLS = [
    "Read", "Grep", "Glob",
    "Bash(git log:*)", "Bash(git diff:*)", "Bash(git show:*)", "Bash(git status:*)",
    "Bash(git ls-files:*)", "Bash(git blame:*)", "Bash(git branch:*)",
    "Bash(ls:*)", "Bash(cat:*)", "Bash(head:*)", "Bash(tail:*)", "Bash(wc:*)",
    "Bash(find:*)", "Bash(rg:*)", "Bash(grep:*)", "Bash(jq:*)",
    "Bash(gh issue list:*)", "Bash(gh issue view:*)", "Bash(gh pr list:*)",
    "Bash(gh pr view:*)", "Bash(gh pr checks:*)", "Bash(gh run list:*)",
    "Bash(gh run view:*)",
    "Bash(dbq:*)",     # read-only database helper in bin/, if you wire one up
    "Bash(past:*)",    # what the bot has done before
    # Search only. No WebFetch: a phase that reads untrusted text and holds
    # read credentials must not be able to send a URL anywhere, since a URL
    # can carry data out.
    "WebSearch",
] + _list("EXTRA_READ_TOOLS")

READ_ONLY_DENY = [
    "Write", "Edit", "MultiEdit", "NotebookEdit",
    "Bash(git commit:*)", "Bash(git push:*)", "Bash(git checkout:*)",
    "Bash(git merge:*)", "Bash(git rebase:*)", "Bash(git reset:*)", "Bash(rm:*)",
]

IMPLEMENTER_TOOLS = [
    "Read", "Write", "Edit", "MultiEdit", "Glob", "Grep", "Bash",
    "Agent", "TodoWrite", "WebSearch", "WebFetch",
] + _list("EXTRA_IMPLEMENTER_TOOLS")

# The agent commits; it never ships. Pushing, opening and merging PRs is done
# by the bot's own code after it has checked the commit (see shipping.py), so
# who-may-land-what is decided by Python, not by a prefix rule a creative
# command line can slip past. Keep GitHub branch protection on as well.
IMPLEMENTER_DENY = [
    "Bash(git push:*)", "Bash(gh pr create:*)", "Bash(gh pr merge:*)",
    "Bash(gh api:*)", "Bash(git reset --hard origin:*)", "Bash(git remote:*)",
    f"Bash(git branch -D {DEFAULT_BRANCH}:*)",
] + _list("EXTRA_IMPLEMENTER_DENY")

# ── What each phase may see from .env ───────────────────────────────────────
_BASE_ENV_KEYS = ("PATH", "HOME", "LANG", "LC_ALL", "TERM", "TMPDIR", "USER", "SHELL")
# How the claude CLI itself authenticates, when not via `claude` login in
# ~/.claude: a long-lived token from `claude setup-token`, or an API key.
_CLAUDE_AUTH_KEYS = ("CLAUDE_CODE_OAUTH_TOKEN", "ANTHROPIC_API_KEY")
# Read-only credentials (a read-only DB URL, a read-only API key).
READ_ENV_KEYS = _list("READ_ENV_KEYS")
# What the implementer additionally needs to build/test (e.g. NEXT_PUBLIC_ vars).
IMPLEMENTER_ENV_KEYS = _list("IMPLEMENTER_ENV_KEYS")
# Write credentials. Only for a write-allowed requester.
WRITE_ENV_KEYS = _list("WRITE_ENV_KEYS")


def scoped_env(keys: list[str]) -> dict[str, str]:
    """A minimal environment, built UP from an allowlist, so adding a secret to
    .env never widens what an agent can see."""
    env = {k: os.environ[k] for k in _BASE_ENV_KEYS if k in os.environ}
    env["PATH"] = f"{ROOT / 'bin'}:{env.get('PATH', '/usr/bin:/bin')}"
    env["COREPACK_ENABLE_DOWNLOAD_PROMPT"] = "0"
    for name in (*_CLAUDE_AUTH_KEYS, *keys):
        value = _get(name)
        if value:
            env[name] = value
    return env


def read_env() -> dict[str, str]:
    return scoped_env(READ_ENV_KEYS)


def implementer_env(writes_allowed: bool) -> dict[str, str]:
    keys = READ_ENV_KEYS + IMPLEMENTER_ENV_KEYS + (WRITE_ENV_KEYS if writes_allowed else [])
    return scoped_env(keys)


# ── Local paths ─────────────────────────────────────────────────────────────
STATE_DB = Path(_get("BOT_STATE_DB", str(ROOT / "state" / "bot.db")))
WORK_ROOT = Path(_get("BOT_WORK_ROOT", str(ROOT / "work")))   # one worktree per request
OUT_ROOT = Path(_get("BOT_OUT_ROOT", str(ROOT / "out")))      # files to attach to the thread
IN_ROOT = Path(_get("BOT_IN_ROOT", str(ROOT / "in")))         # files people attached

# Plain-text files that shape the prompts. Edit them, no code change needed.
VOICE_FILE = Path(_get("VOICE_FILE", str(ROOT / "voice.md")))
CONTEXT_FILE = Path(_get("CONTEXT_FILE", str(ROOT / "context.md")))


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8").strip()
    except OSError:
        return ""


def voice() -> str:
    return _read(VOICE_FILE)


def context() -> str:
    return _read(CONTEXT_FILE)


def safe_id(request_id: str) -> str:
    return request_id.replace(".", "_")


def missing() -> list[str]:
    """Required settings that are not set."""
    need = {
        "SLACK_BOT_TOKEN": SLACK_BOT_TOKEN, "SLACK_APP_TOKEN": SLACK_APP_TOKEN,
        "BOT_CHANNEL_ID": CHANNEL_ID, "BOT_USER_ID": BOT_USER_ID,
        "OWNER_USER_ID": OWNER_USER_ID, "REPO_SLUG": REPO_SLUG,
    }
    placeholder = ("...", "0123456789", "your-org/")
    return [k for k, v in need.items() if not v or any(p in v for p in placeholder)]


def redacted_summary() -> dict:
    """Presence, never value. Safe to log."""
    mark = lambda v: f"set({len(v)} chars)" if v else "MISSING"  # noqa: E731
    return {
        "SLACK_BOT_TOKEN": mark(SLACK_BOT_TOKEN), "SLACK_APP_TOKEN": mark(SLACK_APP_TOKEN),
        "channel": CHANNEL_ID, "repo": REPO_SLUG, "repo_path": str(REPO_PATH),
        "models": [TRIAGE_MODEL, PLAN_MODEL, IMPLEMENTER_MODEL],
        "write_allowed": sorted(WRITE_ALLOWED_USER_IDS),
        "force_pr": FORCE_PR, "dry_run": DRY_RUN, "mcp": bool(MCP_CONFIG),
    }
