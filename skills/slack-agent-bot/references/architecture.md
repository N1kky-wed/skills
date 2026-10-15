# Architecture

## Process model

There is one long-running Python process: `app.py`, run by systemd.

- **Socket Mode listener (Bolt).** It receives `message` events over a websocket. No public URL, TLS or inbound port is needed, so a VPS behind a firewall is fine.
- **N worker threads** (`BOT_WORKERS`, default 2). Each takes one request at a time and runs `pipeline.process`. Runs wait on the model, not the CPU, so the real limit is your Claude plan's rate limit.
- **Agents are subprocesses.** Every phase is `claude -p …` with its own tool allowlist, its own environment and its own working directory.

State lives in SQLite (`state/bot.db`): one file, no daemon, and it survives restarts.

## Request lifecycle

```
RECEIVED ─▶ TRIAGING ─┬─▶ COMPLETED          (answered / conversational / refused)
                      ├─▶ AWAITING_REPLY     (asked one question; the reply re-enters)
                      └─▶ PLANNED ─▶ EXECUTING ─┬─▶ PUSHED | PR_CREATED
                         (code only)            ├─▶ COMPLETED   (lookup/action answered)
                                                ├─▶ FAILED | BLOCKED
                                                └─▶ CANCELLED   (botctl stop)
ATTACHED   a message folded into a job already running in its thread
```

## The phases

**1. Listener** (`app.py`). It accepts only:

- the configured channel;
- a human (no `bot_id`), with subtype empty, `thread_broadcast` or `file_share`;
- either a tag, or an untagged reply in a thread the bot is active in, from the person it was talking to, within `FOLLOW_UP_WINDOW_SECONDS`.

It then:

1. claims the request id (exactly one execution);
2. answers greetings and thanks from a table, without spending a model call;
3. folds a message into a running job in the same thread as a follow-up;
4. otherwise queues the request and returns, all inside Slack's 3-second ack window.

If no worker picks the request up within `QUEUE_ACK_AFTER_SECONDS`, the bot says it's queued.

**2. Triage** (`prompts.triage`, read-only, `TRIAGE_MODEL`). It sees the message, the whole Slack thread (fetched with the bot token, from this channel only), every file attached anywhere in the thread, the bot's own history in the thread, and `context.md`. It returns `request_kind`, `task_type`, `priority`, `message` and `resolved_request`, and `message` is posted immediately.

- **answered:** it answered with its own read tools (a code question, a quick `dbq` count). Done.
- **unclear:** one question; the reply re-enters as a follow-up.
- **conversational:** a short reply. Done.
- **actionable:** one of
  - `bug | feature | refactor | docs | chore`: code;
  - `lookup`: answer or file, changes nothing;
  - `action`: changes live data, and only for write-allowed people.

`resolved_request` is the self-contained restatement every later phase works from. It folds in the thread and any answers, because later phases do not see the thread.

**3. Plan** (code only, read-only, `PLAN_MODEL`).

1. Fast-forward the canonical checkout (`./repo`, ff-only, never resolves anything).
2. The analyst reads the repo and writes a brief: steps, files, tests and constraints. It picks `DIRECT_PUSH` for small, low-risk, confident work, otherwise `PR`.
3. Blockers become BLOCKED; an empty plan means "nothing to change".
4. If the requester can't write, or `BOT_FORCE_PR` is set, the mode becomes PR.
5. A GitHub issue is opened as the durable record (optional).

**4. Implement** (`IMPLEMENTER_MODEL`, write-capable, isolated).

1. `git worktree add -B bot/<type>-<ts> work/<id> origin/<default>`, then `SETUP_COMMAND`, and the base SHA is recorded.
2. The prompt carries the brief, the request, the follow-ups so far and `context.md`.
3. `.bot/followups.md` in the worktree is rewritten whenever a new follow-up lands. The prompt says to re-read it before each step and before finishing.
4. The run streams (`--output-format stream-json`). Every `PROGRESS_INTERVAL_SECONDS` a progress line is posted, and the CLI's pid is stored so `botctl stop` can kill it.
5. For lookups and actions, files written to `$BOT_OUT_DIR` are attached to the thread, or pasted if `files:write` is missing.

**5. Verify and ship** (Python, `pipeline.run_and_ship` and `gitops`).

1. `verify()` compares HEAD with the recorded base SHA. No new commit means FAILED, whatever the report says.
2. DIRECT_PUSH: fetch, rebase onto the newest default, then `git push origin HEAD:<default>`, then confirm that the remote contains the commit. A conflict or branch protection falls back to a PR.
3. PR: `git push -u origin <branch>`, then `gh pr create` with the agent's `pr_title` and `pr_body`.
4. If a **pre-push hook** rejects the push, the hook output goes back to the same agent session (`--resume <session_id>`) once. It fixes, commits again, and the bot ships again.
5. The worktree is removed. Its branch is kept only if it holds commits no remote has.

## Why the agent doesn't push

The first version let the implementer push, guarded by deny rules such as `Bash(git push origin main:*)`. Prefix rules are a speed bump, not a wall: `git push -u origin x:main`, `git -C . push`, `bash -c` and refspec tricks all slip past one rule or another. Moving shipping into Python makes the permission check ordinary code (`config.can_write`) and makes verification simple, because nothing reaches the remote that Python didn't send. Keep GitHub branch protection on as the final wall.

## Data on disk

| Path | What | Lifetime |
|---|---|---|
| `.env` | all secrets and settings (0600) | permanent |
| `state/bot.db` | requests, follow-ups, posted message ts | permanent; `past` reads it |
| `repo/` | canonical checkout, ff-only | permanent |
| `work/<id>/` | one worktree per running job | deleted when the job ends |
| `out/<id>/` | files a job produced for the thread | kept (prior-work lookup) |
| `in/<id>/` | files people attached | deleted when the job ends |
