"""Check that everything the bot needs is in place. Prints no secret values.

    .venv/bin/python doctor.py
"""

import os
import shutil
import stat
import subprocess
import sys

from bot import config

ok = True


def check(label: str, passed: bool, hint: str = "") -> None:
    global ok
    ok &= passed
    print(f"  {'ok ' if passed else 'XX '} {label}" + ("" if passed else f"\n      -> {hint}"))


print("config")
env_file = config.ROOT / ".env"
check(".env exists", env_file.exists(), "cp .env.example .env and fill it in")
if env_file.exists():
    check(".env is private (0600)", stat.S_IMODE(env_file.stat().st_mode) & 0o077 == 0, "chmod 600 .env")
for name in config.missing():
    check(f"{name} set", False, "set it in .env (still empty or a placeholder)")

print("slack")
try:
    from slack_sdk import WebClient
    c = WebClient(token=config.SLACK_BOT_TOKEN)
    me = c.auth_test()
    check(f"bot token works (bot user {me['user_id']})", True)
    check("BOT_USER_ID matches the token's bot user", me["user_id"] == config.BOT_USER_ID,
          f"set BOT_USER_ID={me['user_id']}")
    scopes = set((me.headers.get("x-oauth-scopes") or "").split(","))
    for s in ("chat:write", "channels:history", "groups:history", "files:read", "files:write"):
        check(f"scope {s}", s in scopes, "add it in the app's OAuth & Permissions, then reinstall")
    try:
        info = c.conversations_info(channel=config.CHANNEL_ID)["channel"]
        check(f"channel #{info.get('name')} visible", True)
        check("bot is a member of the channel", bool(info.get("is_member")), "/invite the bot there")
    except Exception as exc:  # noqa: BLE001
        check("channel visible", False, f"{exc.__class__.__name__}: is BOT_CHANNEL_ID right and the bot invited?")
except Exception as exc:  # noqa: BLE001
    check("bot token works", False, f"{exc.__class__.__name__}")
check("app token looks like xapp-", config.SLACK_APP_TOKEN.startswith("xapp-"),
      "Basic Information -> App-Level Tokens (connections:write)")

print("tools")
claude = shutil.which(config.CLAUDE_BIN)
check(f"claude CLI on PATH ({claude})", bool(claude), "npm i -g @anthropic-ai/claude-code, then `claude` once to log in")
if claude:
    r = subprocess.run([config.CLAUDE_BIN, "-p", "reply with the word ok", "--model",
                        config.TRIAGE_MODEL, "--allowedTools", ""],
                       capture_output=True, text=True, timeout=120, env=config.scoped_env([]))
    check("claude answers headlessly", r.returncode == 0 and "ok" in r.stdout.lower(),
          (r.stderr or r.stdout).strip()[:200] or "run `claude` interactively once to log in")
check("git on PATH", bool(shutil.which("git")), "apt install git")
gh = shutil.which("gh")
check("gh on PATH", bool(gh), "install GitHub CLI, then `gh auth login`")
if gh:
    r = subprocess.run(["gh", "repo", "view", config.REPO_SLUG, "--json", "viewerPermission",
                        "--jq", ".viewerPermission"], capture_output=True, text=True, timeout=60)
    perm = r.stdout.strip()
    check(f"gh can see {config.REPO_SLUG} (permission {perm or '?'})",
          perm in ("WRITE", "MAINTAIN", "ADMIN"), "gh auth login with an account that can push")

print("repository")
check(f"checkout at {config.REPO_PATH}", (config.REPO_PATH / ".git").exists(),
      f"git clone https://github.com/{config.REPO_SLUG} {config.REPO_PATH}")
if (config.REPO_PATH / ".git").exists():
    r = subprocess.run(["git", "fetch", "--dry-run"], cwd=config.REPO_PATH, capture_output=True, text=True, timeout=60)
    check("git can reach the remote", r.returncode == 0, r.stderr.strip()[:200])
for p in (config.STATE_DB.parent, config.WORK_ROOT, config.OUT_ROOT, config.IN_ROOT):
    p.mkdir(parents=True, exist_ok=True)
    check(f"{p} writable", os.access(p, os.W_OK), f"chown the bot user {p}")

print("\nall good" if ok else "\nfix the XX lines above")
sys.exit(0 if ok else 1)
