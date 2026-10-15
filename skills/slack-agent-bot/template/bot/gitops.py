"""Git: the canonical checkout, per-request worktrees, verification, shipping.

The canonical checkout (REPO_PATH) is read-only analysis territory: it is only
ever fast-forwarded. Each request that needs to write gets its own worktree, so
concurrent jobs cannot collide. Agents commit; only this module pushes, and
only after it has seen the commit with its own eyes.
"""

import logging
import shutil
import subprocess
from pathlib import Path
from typing import Optional

from . import config

log = logging.getLogger("bot.git")


class GitError(RuntimeError):
    pass


def git(*args: str, cwd: Optional[Path] = None, timeout: int = 300,
        check: bool = False) -> subprocess.CompletedProcess:
    r = subprocess.run(["git", *args], cwd=str(cwd or config.REPO_PATH),
                       capture_output=True, text=True, timeout=timeout)
    if check and r.returncode != 0:
        raise GitError(f"git {' '.join(args[:3])} failed: {(r.stderr or r.stdout).strip()[:400]}")
    return r


def refresh() -> dict:
    """Fast-forward the canonical checkout. Never merges, rebases or discards:
    anything unexpected there is reported, not resolved."""
    if not (config.REPO_PATH / ".git").exists():
        raise GitError(f"{config.REPO_PATH} is not a git checkout")
    git("fetch", "--all", "--prune", check=True)
    branch = config.DEFAULT_BRANCH
    dirty = git("status", "--porcelain", "--untracked-files=no").stdout.strip()
    if dirty:
        log.warning("canonical checkout has tracked changes; not fast-forwarding")
    else:
        if git("rev-parse", "--abbrev-ref", "HEAD").stdout.strip() != branch:
            git("checkout", branch, check=True)
        git("merge", "--ff-only", f"origin/{branch}", check=True)
    return {"default_branch": branch,
            "head": git("rev-parse", "HEAD").stdout.strip(),
            "subject": git("log", "-1", "--pretty=%s").stdout.strip(),
            "dirty": bool(dirty)}


def branch_for(request_id: str, task_type: str) -> str:
    return f"bot/{task_type}-{request_id.split('-')[-1].replace('.', '')}"


def create_worktree(request_id: str, branch: str, env: dict) -> tuple[Path, str]:
    """A private checkout on a new branch from the current remote default.
    Returns (path, base_sha). base_sha is captured now because it is the only
    moment it is knowable: after a direct push origin/main has moved."""
    config.WORK_ROOT.mkdir(parents=True, exist_ok=True)
    path = config.WORK_ROOT / config.safe_id(request_id)
    if path.exists():
        remove_worktree(path, branch)
    git("fetch", "--all", "--prune", check=True)
    git("worktree", "add", "-B", branch, str(path), f"origin/{config.DEFAULT_BRANCH}", check=True)
    if config.SETUP_COMMAND:
        r = subprocess.run(config.SETUP_COMMAND, shell=True, cwd=str(path), env=env,
                           capture_output=True, text=True, timeout=config.SETUP_TIMEOUT_SECONDS)
        if r.returncode != 0:
            remove_worktree(path, branch)
            raise GitError(f"setup command failed: {(r.stderr or r.stdout).strip()[-400:]}")
    base = git("rev-parse", "HEAD", cwd=path).stdout.strip()
    return path, base


def remove_worktree(path: Path, branch: Optional[str] = None) -> None:
    """Tear a worktree down. Its branch goes too, unless it carries commits no
    remote has: that is the only copy of a failed attempt someone may want."""
    git("worktree", "remove", "--force", str(path), timeout=120)
    if path.exists():
        shutil.rmtree(path, ignore_errors=True)
    git("worktree", "prune", timeout=60)
    if not branch:
        return
    head = git("rev-parse", "--verify", branch).stdout.strip()
    if head and not git("branch", "-r", "--contains", head).stdout.strip() \
            and git("rev-list", "--count", f"origin/{config.DEFAULT_BRANCH}..{branch}").stdout.strip() not in ("", "0"):
        log.warning("keeping local branch %s: it has commits no remote has", branch)
        return
    git("branch", "-D", branch)


def verify(worktree: Path, base_sha: str) -> dict:
    """What actually happened, whatever the agent reported."""
    head = git("rev-parse", "HEAD", cwd=worktree).stdout.strip()
    changed: list[str] = []
    if head and head != base_sha:
        changed = [l for l in git("diff", "--name-only", f"{base_sha}..{head}", cwd=worktree)
                   .stdout.splitlines() if l]
    dirty = git("status", "--porcelain", "--untracked-files=no", cwd=worktree).stdout.strip()
    return {"head": head, "committed": bool(head and head != base_sha),
            "changed_files": changed, "uncommitted_changes": bool(dirty)}


def _gh(*args: str, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(["gh", *args], cwd=str(cwd), capture_output=True, text=True, timeout=180)


def open_pr(worktree: Path, branch: str, title: str, body: str) -> dict:
    push = git("push", "-u", "origin", branch, cwd=worktree, timeout=1800)
    if push.returncode != 0:
        return {"ok": False, "stage": "push", "output": (push.stderr or push.stdout)[-3000:]}
    pr = _gh("pr", "create", "--repo", config.REPO_SLUG, "--base", config.DEFAULT_BRANCH,
             "--head", branch, "--title", title[:250], "--body", body, cwd=worktree)
    if pr.returncode != 0:
        existing = _gh("pr", "view", branch, "--repo", config.REPO_SLUG, "--json", "url",
                       "--jq", ".url", cwd=worktree)
        if existing.returncode == 0 and existing.stdout.strip():
            return {"ok": True, "pr_url": existing.stdout.strip()}
        return {"ok": False, "stage": "pr", "output": (pr.stderr or pr.stdout)[-1500:]}
    return {"ok": True, "pr_url": pr.stdout.strip().splitlines()[-1]}


def push_direct(worktree: Path) -> dict:
    """Rebase onto the newest default branch and push to it. Any trouble
    (conflict, branch protection) returns ok=False with fallback=True so the
    caller opens a PR instead."""
    default = config.DEFAULT_BRANCH
    git("fetch", "origin", default, cwd=worktree, check=True)
    rebase = git("rebase", f"origin/{default}", cwd=worktree)
    if rebase.returncode != 0:
        git("rebase", "--abort", cwd=worktree)
        return {"ok": False, "fallback": True, "output": "rebase onto the newest default branch conflicted"}
    push = git("push", "origin", f"HEAD:{default}", cwd=worktree, timeout=1800)
    if push.returncode != 0:
        out = (push.stderr or push.stdout)[-3000:]
        protected = any(s in out.lower() for s in ("protected branch", "gh006", "required status", "review"))
        return {"ok": False, "fallback": protected, "stage": "push", "output": out}
    head = git("rev-parse", "HEAD", cwd=worktree).stdout.strip()
    git("fetch", "origin", default, cwd=worktree)
    on_remote = bool(git("branch", "-r", "--contains", head, cwd=worktree).stdout.strip())
    return {"ok": on_remote, "commit": head,
            "output": "" if on_remote else "push reported success but the commit is not on the remote"}
