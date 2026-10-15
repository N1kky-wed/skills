# Operating the bot

Everything here runs on the server as the bot user, from the bot's directory (e.g. `~/slack-agent-bot`).

## Daily commands

```bash
bin/botctl status                 # in flight + last 15
bin/botctl show C0123-1712345678.123456
bin/botctl stop C0123-1712345678.123456     # kill + polite "stopped" in the thread
bin/botctl clean C0123-1712345678.123456    # delete everything the bot posted for it
bin/botctl rerun C0123-1712345678.123456    # run it again here (service keeps running)
bin/botctl say 1712345678.123456 "back in 5, deploying"
bin/past search invoice           # what has the bot done about invoices before
journalctl -u slack-agent-bot -f  # live log; grep the request id
journalctl -u slack-agent-bot --since "1 hour ago" | grep C0123-1712345678
```

The request id is `<channel>-<message ts>`. The message ts is the number at the end of a Slack permalink (`p1712345678123456` → `1712345678.123456`).

## Restarting safely

A restart kills every running job.

1. Run `bin/botctl status`. If anything is in flight, wait, or tell its thread.
2. Run `sudo systemctl restart slack-agent-bot`.
3. On start-up, every request still marked in flight is set to FAILED, and its thread gets "i got restarted in the middle of this one, tag me again".

Changes to `.env`, the code or the unit need a restart. Changes to `context.md` and `voice.md` don't: they are read for every prompt.

## Stopping a job

Run `bin/botctl stop <id>`. It sets CANCELLED first, so the pipeline stays quiet instead of posting "failed". Then it kills the CLI pid and posts the polite stop line, using the requester's nickname if they have one. If the job was still in triage (no pid yet), it finishes triage and then notices the cancel. To remove the job's earlier messages too, run `botctl clean <id>`.

Follow-ups people sent to a stopped job don't run on their own. Tell them to tag the bot again.

## Common failures

| Symptom | Likely cause | Fix |
|---|---|---|
| Bot never reacts | not in the channel; wrong `BOT_CHANNEL_ID`; Socket Mode off; app token missing `connections:write` | `doctor.py`, then the app settings |
| Reacts to a tag in a thread but not to a file upload with a tag | an old version filtered the `file_share` subtype | current `app.is_human` lets it through |
| "this one failed: claude CLI exited 1: … login" | Claude auth expired on the box | `claude` interactively once, or refresh `CLAUDE_CODE_OAUTH_TOKEN` |
| "this one failed: claude CLI exited 143" | the job was killed (stop, restart, OOM) | `journalctl -k` for OOM; otherwise expected |
| "workspace: setup command failed" | `SETUP_COMMAND` broke (lockfile drift, missing toolchain) | run it by hand in `work/` or `repo/` |
| "shipping failed: … protected branch" | DIRECT_PUSH on a protected branch with no bypass | normally falls back to a PR; check the bypass setting |
| "reported success but there is no commit" | the agent edited but didn't commit, or worked outside its worktree | read the run in `botctl show`; usually a prompt or timeout issue |
| Replies are walls of text | voice too loose | tighten `voice.md`; the prompts already cap length |
| Attachments pasted instead of attached | the bot lacks `files:write` | add the scope, reinstall the app |
| Thread context missing | `channels:history` / `groups:history` missing | add the scope, reinstall |
| Two jobs for one message | (should be impossible) | check that two services aren't running with the same tokens: `systemctl list-units \| grep bot` |

## Costs

Each request is one triage run (cheap model, seconds), plus one plan run for code changes, plus one implementer run. Look at `cost_usd` in `botctl show <id>` (in `triage_result._meta` and `run_result._meta`). Long data jobs dominate the bill. Keep `IMPLEMENTER_TIMEOUT_SECONDS` sane, and use `PROGRESS_MODEL=haiku` or leave it empty.

## Housekeeping

- `out/` keeps every file the bot produced, so `past` can point at prior work. Prune old directories now and then.
- `state/bot.db` grows slowly. Back it up with the server.
- Branches the bot kept (unpushed failed attempts) can be listed with `git -C repo branch --list 'bot/*'`.
