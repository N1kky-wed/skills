"""One request, all the way through: Slack message in, outcome back in the thread.

  triage    fast, read-only. Says the first thing: an answer, a question, or a
            specific ack. Decides what kind of work it is.
  plan      code changes only. Read-only pass over a freshly fast-forwarded
            checkout; writes the brief and picks DIRECT_PUSH or PR.
  implement one `claude -p` in a private worktree, streamed, with progress
            lines in the thread and follow-ups fed in through a file.
  verify    the agent's report is checked against git before it is believed.
  ship      this code, not the agent, pushes or opens the PR, and decides
            which one the requester is allowed.

Rule the module is built around: nothing is reported done unless the artefact
proving it exists.
"""

import logging
import traceback

from . import (agents, attachments, config, followups, github, gitops, phrases,
               prompts, slack_io, state)

log = logging.getLogger("bot.pipeline")


def _one_line(text: str, limit: int = 300) -> str:
    text = " ".join(str(text).split())
    return text if len(text) <= limit else text[:limit - 1] + "…"


def _deliver_files(thread_ts: str, out_dir, request_id: str) -> None:
    for path in sorted(p for p in out_dir.iterdir() if p.is_file() and p.stat().st_size > 0):
        if slack_io.upload(thread_ts, str(path)):
            continue
        body = path.read_text(errors="replace")[:3500]
        slack_io.post(thread_ts, f"{path.name} (couldn't attach it, pasting instead):\n```\n{body}\n```",
                      request_id)


def operation_brief(t: dict) -> dict:
    return {"classification": {"task_type": t["task_type"], "scope": "small", "risk": "low",
                               "priority": t.get("priority", "normal"), "confidence": 1.0,
                               "execution_mode": "REPORT"},
            "plan": [], "resolved_request": t["resolved_request"],
            "reasoning_summary": t.get("reasoning_summary", "")}


def _validate_triage(obj: dict, original: str) -> dict:
    if obj.get("request_kind") not in prompts.REQUEST_KINDS:
        raise agents.AgentError(f"bad request_kind {obj.get('request_kind')!r}")
    if not (obj.get("message") or "").strip():
        raise agents.AgentError("triage returned no message")
    if obj["request_kind"] == "actionable" and obj.get("task_type") not in prompts.TASK_TYPES:
        raise agents.AgentError(f"bad task_type {obj.get('task_type')!r}")
    if obj.get("priority") not in prompts.PRIORITIES:
        obj["priority"] = "normal"
    obj["resolved_request"] = (obj.get("resolved_request") or "").strip() or original
    return obj


def _validate_plan(obj: dict) -> dict:
    c = obj.get("classification") or {}
    problems = []
    if c.get("task_type") not in prompts.CODE_TYPES:
        problems.append(f"task_type {c.get('task_type')!r}")
    if c.get("execution_mode") not in ("DIRECT_PUSH", "PR"):
        problems.append(f"execution_mode {c.get('execution_mode')!r}")
    if not isinstance(obj.get("plan"), list):
        problems.append("plan is not a list")
    if problems:
        raise agents.AgentError("plan failed validation: " + "; ".join(problems))
    c.setdefault("priority", "normal")
    return obj


def recover(store: state.Store) -> None:
    """On startup: nothing is running after a restart, so any request still
    marked in flight was cut off. Say so in its thread instead of going quiet."""
    for row in store.inflight():
        store.update(row["request_id"], status=state.FAILED, error="interrupted by a restart")
        thread = row.get("thread_ts") or row["message_ts"]
        slack_io.post(thread, "i got restarted in the middle of this one, tag me again and i'll redo it",
                      row["request_id"])
        log.warning("[%s] marked failed: interrupted by a restart", row["request_id"])


def process(request: dict, store: state.Store) -> None:
    rid = request["request_id"]
    slack = request["slack"]
    user = slack.get("user_id")
    thread_ts = slack.get("thread_ts") or slack["message_ts"]
    issue_url = None

    def say(text: str) -> None:
        slack_io.post(thread_ts, text, rid)

    def cancelled() -> bool:
        return store.status(rid) == state.CANCELLED

    def fail(status: str, reason: str) -> None:
        if cancelled():
            log.info("[%s] stopped by operator", rid)
            return
        log.error("[%s] %s: %s", rid, status, reason)
        store.update(rid, status=status, error=_one_line(reason, 2000))
        lead = "couldn't do this one" if status == state.BLOCKED else "this one failed"
        say(f"{lead}: {_one_line(reason)}")
        github.comment(issue_url, f"**{status}**\n\n```\n{_one_line(reason, 1500)}\n```")

    try:
        # ── triage ──────────────────────────────────────────────────────────
        store.update(rid, status=state.TRIAGING)
        history = [r for r in store.thread_history(thread_ts) if r["request_id"] != rid]
        request["thread"] = slack_io.read_thread(slack["thread_ts"]) if slack.get("thread_ts") else []
        files = list(slack.get("files") or [])
        seen = {f.get("id") for f in files}
        for m in request["thread"]:  # a screenshot one message up is usually the subject
            for f in m.get("files") or []:
                if f.get("id") not in seen:
                    seen.add(f.get("id"))
                    files.append(f)
        request["attachments"] = attachments.fetch(files, rid)

        try:
            t = _validate_triage(agents.run_json(
                prompts.triage(request, history), config.TRIAGE_MODEL,
                config.READ_ONLY_TOOLS + config.MCP_READ_TOOLS, config.READ_ONLY_DENY,
                config.TRIAGE_TIMEOUT_SECONDS, config.REPO_PATH, config.read_env(),
                key="request_kind"), slack["message"])
        except agents.AgentError as exc:
            return fail(state.FAILED, f"triage: {exc}")
        store.update(rid, triage_result=t)
        if cancelled():
            return
        log.info("[%s] %s/%s: %s", rid, t["request_kind"], t.get("task_type"), _one_line(t["message"], 120))
        slack_io.post_long(thread_ts, t["message"], rid)

        if t["request_kind"] == "unclear":
            return store.update(rid, status=state.AWAITING_REPLY, error=None)
        if t["request_kind"] != "actionable":
            return store.update(rid, status=state.COMPLETED, error=None)

        writes_allowed = config.can_write(user)
        task = t["task_type"]

        # ── plan ────────────────────────────────────────────────────────────
        if task in prompts.OPERATION_TYPES:
            if task == "action" and not writes_allowed:
                store.update(rid, status=state.COMPLETED, error="requester may not change data")
                return say(f"i can look things up for anyone, but changing live data only runs when "
                           f"<@{config.OWNER_USER_ID}> asks. tag them if this needs doing")
            brief = operation_brief(t)
        else:
            try:
                repo_state = gitops.refresh()
                brief = _validate_plan(agents.run_json(
                    prompts.plan(request, t, repo_state), config.PLAN_MODEL,
                    config.READ_ONLY_TOOLS + config.MCP_READ_TOOLS, config.READ_ONLY_DENY,
                    config.PLAN_TIMEOUT_SECONDS, config.REPO_PATH, config.read_env(),
                    key="classification"))
            except (agents.AgentError, gitops.GitError) as exc:
                return fail(state.FAILED, f"planning: {exc}")
            brief["resolved_request"] = t["resolved_request"]
            store.update(rid, plan_result=brief)
            if cancelled():
                return
            if brief.get("blockers"):
                return fail(state.BLOCKED, "; ".join(map(str, brief["blockers"])))
            if not brief.get("plan"):
                store.update(rid, status=state.COMPLETED, error=None)
                return say(f"nothing to change here. {_one_line(brief.get('reasoning_summary', ''))}")
            c = brief["classification"]
            if config.FORCE_PR or not writes_allowed:
                c["execution_mode"] = "PR"
            store.update(rid, status=state.PLANNED)
            issue_url = github.ensure_issue(request, brief)
            store.update(rid, issue_url=issue_url)
            ships = "a PR" if c["execution_mode"] == "PR" else f"a push to {config.DEFAULT_BRANCH}"
            say(f"{c['task_type']}, {c.get('scope')} scope, {c.get('risk')} risk, will ship as {ships}"
                + (f". issue: {issue_url}" if issue_url else ""))

        # ── implement ───────────────────────────────────────────────────────
        run_and_ship(request, brief, store, writes_allowed, say, fail, issue_url)

    except Exception as exc:  # noqa: BLE001 - a worker must never die silently
        log.error("[%s] unhandled:\n%s", rid, traceback.format_exc())
        fail(state.FAILED, f"unexpected error: {exc.__class__.__name__}: {exc}")
    finally:
        attachments.discard(rid)


def run_and_ship(request, brief, store, writes_allowed, say, fail, issue_url) -> None:
    rid = request["request_id"]
    thread_ts = request["slack"].get("thread_ts") or request["slack"]["message_ts"]
    c = brief["classification"]
    task = c["task_type"]
    is_code = task in prompts.CODE_TYPES
    branch = gitops.branch_for(rid, task)
    out_dir = config.OUT_ROOT / config.safe_id(rid)
    out_dir.mkdir(parents=True, exist_ok=True)
    # Write credentials only for a data action by someone allowed to write.
    env = config.implementer_env(writes_allowed and task == "action")
    tools = config.IMPLEMENTER_TOOLS + config.MCP_READ_TOOLS + (config.MCP_WRITE_TOOLS if writes_allowed else [])
    deny = config.IMPLEMENTER_DENY + ([] if writes_allowed else config.MCP_WRITE_TOOLS)

    request["followups"] = store.followups(rid)
    store.update(rid, status=state.EXECUTING, branch=branch if is_code else None)
    try:
        worktree, base = gitops.create_worktree(rid, branch, env)
    except gitops.GitError as exc:
        return fail(state.FAILED, f"workspace: {exc}")
    followups.exclude_from_git(config.REPO_PATH)
    followups.write(worktree, request["followups"])

    progress = phrases.Progress()
    on_progress = lambda minutes: say(config.with_name(progress.line(minutes), request["slack"].get("user_id")))  # noqa: E731
    env["BOT_OUT_DIR"] = str(out_dir)

    def run(prompt: str, resume=None) -> dict:
        cmd = agents.command(prompt, config.IMPLEMENTER_MODEL, tools, deny,
                             output="stream-json", resume=resume)
        s = agents.Streamed(cmd, worktree, env, on_start=lambda pid: store.update(rid, pid=pid))
        s.wait(config.IMPLEMENTER_TIMEOUT_SECONDS, on_progress, config.PROGRESS_INTERVAL_SECONDS)
        report = s.report("status")
        if report is None:
            raise agents.AgentError("the agent finished without its JSON report")
        return report

    try:
        prompt = prompts.implement(request, brief, branch, writes_allowed, str(out_dir), issue_url)
        try:
            report = run(prompt)
        except agents.AgentError as exc:
            produced = [p for p in out_dir.iterdir() if p.is_file() and p.stat().st_size > 0]
            if is_code or not produced or store.status(rid) == state.CANCELLED:
                return fail(state.FAILED, str(exc))
            report = {"status": "success", "summary": "finished, the file is attached "
                      "(its final report was malformed)"}
        store.update(rid, run_result=report)
        if report.get("status") != "success":
            status = state.BLOCKED if report.get("status") == "blocked" else state.FAILED
            return fail(status, report.get("error") or report.get("summary") or "no detail given")

        # ── operations: the summary is the product ──────────────────────────
        if not is_code:
            if gitops.verify(worktree, base)["committed"]:
                log.warning("[%s] operation made a commit; discarded with the worktree", rid)
            answer = (report.get("summary") or "").strip()
            if not answer:
                return fail(state.FAILED, "reported success but gave no answer")
            slack_io.post_long(thread_ts, answer, rid)
            _deliver_files(thread_ts, out_dir, rid)
            return store.update(rid, status=state.COMPLETED, error=None)

        # ── code: verify, then ship ─────────────────────────────────────────
        seen = gitops.verify(worktree, base)
        if not seen["committed"]:
            return fail(state.FAILED, "reported success but there is no commit on the branch")

        mode = c["execution_mode"]
        if writes_allowed and not config.FORCE_PR and report.get("execution_mode") in ("PR", "DIRECT_PUSH"):
            mode = report["execution_mode"]    # the agent may downgrade to PR, or confirm
        title = report.get("pr_title") or f"{task}: {brief['resolved_request'][:60]}"
        body = (report.get("pr_body") or report.get("summary") or "") + \
               (f"\n\nCloses {issue_url}" if issue_url else "")

        shipped = _ship(worktree, branch, mode, title, body)
        if not shipped["ok"] and shipped.get("stage") == "push" and not shipped.get("fallback"):
            # A pre-push hook said no. Give the same agent one go at fixing it.
            say("the push hook flagged something, fixing it")
            try:
                fix = run(f"The bot tried to push your commit and the push was rejected:\n\n```\n"
                          f"{shipped['output'][-2500:]}\n```\n\nFix the cause, run the checks, commit "
                          "again, and reply with the same JSON report as before.",
                          resume=(report.get("_meta") or {}).get("session_id"))
            except agents.AgentError as exc:
                return fail(state.FAILED, f"push rejected and the fix run failed: {exc}")
            if fix.get("status") != "success":
                return fail(state.FAILED, f"push rejected: {fix.get('error') or shipped['output'][-300:]}")
            report.update({k: v for k, v in fix.items() if k != "_meta"})
            seen = gitops.verify(worktree, base)
            shipped = _ship(worktree, branch, mode, title, body)
        if not shipped["ok"]:
            return fail(state.FAILED, f"shipping failed: {shipped.get('output', '')[-400:]}")

        files = len(seen["changed_files"])
        summary = _one_line(report.get("summary") or "", 600)
        if shipped.get("pr_url"):
            store.update(rid, status=state.PR_CREATED, pull_request_url=shipped["pr_url"],
                         commit_sha=seen["head"], error=None)
            say(f"opened a PR: {shipped['pr_url']}\n{files} file{'s' * (files != 1)} changed.\n\n{summary}")
        else:
            store.update(rid, status=state.PUSHED, commit_sha=shipped["commit"], error=None)
            say(f"pushed {shipped['commit'][:10]} to {config.DEFAULT_BRANCH}, "
                f"{files} file{'s' * (files != 1)} changed.\n\n{summary}")
        tests = ", ".join((report.get("tests") or {}).get("commands") or []) or "none reported"
        github.comment(issue_url, f"**Shipped** {shipped.get('pr_url') or shipped.get('commit')}\n\n"
                                  f"Checks run: {tests}\n\n{report.get('summary', '')}")
    finally:
        gitops.remove_worktree(worktree, branch)


def _ship(worktree, branch: str, mode: str, title: str, body: str) -> dict:
    if mode == "DIRECT_PUSH":
        pushed = gitops.push_direct(worktree)
        if pushed["ok"] or not pushed.get("fallback"):
            return pushed
        log.info("direct push not possible (%s); opening a PR instead", pushed.get("output", "")[:120])
    return gitops.open_pr(worktree, branch, title, body)
