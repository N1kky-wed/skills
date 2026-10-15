# Lessons from running one of these in production

Every rule below cost a real incident in the bot this template came from.
Read it before changing the bot, and add to it when something new bites.

## Slack

- **Ack in under 3 seconds, or the job runs twice.** Slack re-delivers unacknowledged events. The handler only filters, claims and queues; the work happens on worker threads. The claim (INSERT on `channel-ts`) makes the re-delivery a no-op.
- **The bot must never trigger itself.** Drop anything with a `bot_id` or `app_id`. The bot's own posts are `message` events too.
- **A tag on a message with a file has subtype `file_share`.** Filtering on "no subtype" silently ignored every screenshot-plus-question.
- **`app_mention` and `message` both fire for a tag.** Handle one and no-op the other.
- **People point at other messages.** "why did that happen" refers to a message one up the thread, usually someone else's. Fetch the whole thread and give it to triage, along with files attached anywhere in it, not just on the tagged message.
- **App posts keep their content in Block Kit.** `text` is only the headline. Walk the `blocks` and `attachments` too.
- **Untagged replies count only from the person the bot is talking to, and only for a while.** Otherwise the bot butts into every conversation in a thread it once touched.
- **`conversations.history` sometimes returns ok and empty for a window with messages in it,** especially when called back to back (throttling with no 429). Retry once before believing the silence. This matters if you add a heartbeat.

## Conversation

- **The first reply must be specific and fast.** "on it, adding the retry to the webhook handler" beats "on it" followed by silence. Triage exists mostly to produce that line.
- **Greetings and thanks never reach a model.** Running triage on "thanks" and replying "okok on it" reads as broken.
- **Messages sent while a job runs are amendments, not new jobs.** "pull 30" then "make it 50" became two jobs, each producing its own list. Fold them in: the prompt lists the ones so far, and a file in the worktree gets the later ones.
- **Long answers are split, never cut.** Cutting at a fixed length lost the end of exactly the explanation someone asked for.
- **Terse in a shared channel.** The outcome and one line of why. Details go in the issue or PR, or in `botctl show`.
- **Never promise a rerun.** After a failure, nothing reruns unless someone asks. Say that.
- **Progress lines are signs of life, not logs.** No file names, no step counts. One every 10 minutes at most. A pool of lines repeats within a week; a cheap model writing fresh ones (with the pool as fallback) doesn't.
- **No em dashes.** A prompt asks, and `slack_io._house_style` enforces it. Models ignore style rules a few percent of the time, so anything that must be true goes in code.
- **Nicknames and warmth per person** (`ADDRESS_AS`) are cheap and people notice. Keep them in config, applied to canned lines too, not only to model output.

## Agents and the CLI

- **The tool allowlist is the security boundary; the prompt is not.** A read-only phase must not hold `Write`, `Edit` or push. Name them in the deny list as well, so a later allowlist edit can't hand them over by accident.
- **`psql "$URL" …` is refused under a `Bash(psql:*)` prefix rule** because of the variable expansion. A tiny wrapper (`bin/dbq name "sql"`) with nothing to expand works, and it can force `BEGIN READ ONLY` too.
- **An MCP tool on the allowlist does nothing without `--mcp-config`.** A run that "lost its connection" had the tool names but no config.
- **`result` in the CLI envelope is only the agent's LAST message.** If something gave it one more turn after it wrote its JSON (a background monitor firing, say), `result` is "all done!" and the JSON is one message back. Stream the events and search backwards for the report.
- **Never trust the report; check git.** Agents have said "pushed abc123" about commits that didn't exist.
- **Record the base SHA when the worktree is made.** Comparing against `origin/main` afterwards says "nothing committed" about a direct push, which moved `origin/main` onto the new commit.
- **Worktrees don't share `node_modules` or venvs.** Without `SETUP_COMMAND` the agent can't run a test, and the pre-push hook rejects every push.
- **Ff-only refresh of the canonical checkout must ignore untracked files.** Tools that drop logs into the repo left it permanently "dirty" and stuck on an old commit.
- **A triage timeout of 2 minutes was too short** once triage could answer small lookups itself. Give it about 5.
- **Long data jobs legitimately take hours.** Set the implementer timeout for the longest real job, and stream progress so hours aren't silent.
- **Keep secrets out of `os.environ`.** Load `.env` into a private dict and build each subprocess env from an allowlist. Adding a key to `.env` must never widen what an agent sees.
- **Don't give agents Slack tools that act as a person.** They can read that person's DMs, and anything they read can end up in a public thread, issue or commit.

## Git and shipping

- **The agent commits; the bot pushes.** Deny rules on push refspecs leak (`-u origin x:main`, `-C`, `bash -c`). Shipping from Python makes the permission check plain code.
- **Pre-push hooks are the repo's quality gate.** Never `--no-verify`. On rejection, hand the hook output back to the same agent session (`--resume`) once.
- **Direct push: fetch, rebase, push, then confirm the remote has the commit.** Fall back to a PR on a conflict or branch protection.
- **Remove each worktree and its branch afterwards,** except a branch with unpushed commits. That is the only copy of a failed attempt.
- **Keep the bot's own scratch files out of git** with `.git/info/exclude` (shared by every worktree), not with the repo's `.gitignore`.

## Operations

- **A restart kills running jobs, and it used to do so silently.** Check what's in flight first. On boot, the bot now tells each cut-off thread to re-tag.
- **Stopping a job must be quiet and kind.** Mark it cancelled before killing it, so the pipeline doesn't post "this one failed: exited 143". Then post one polite line, and delete the job's earlier messages if asked.
- **A rerun shouldn't need a restart.** `botctl rerun` runs the pipeline out of process against the same state.
- **Log every request with its id,** e.g. `[C0123-1712345678.123456]`. It's what makes `journalctl | grep` useful.
- **Paid APIs bill even on 429.** If agents call metered APIs, tell them in `context.md` which ones are rate-limited or broken, so they don't retry into a bill.
