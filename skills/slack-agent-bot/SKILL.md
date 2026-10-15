---
name: slack-agent-bot
description: Build, deploy and run a Slack bot that turns messages in a channel into real work done by Claude Code on a GitHub repo, hosted on your own VPS. People tag the bot; it answers questions, looks things up, writes code in an isolated git worktree, runs the tests, and ships a commit or PR, with follow-ups, progress lines, file attachments, per-person write permissions and secret scoping. Ships a tested Python template, a Slack app manifest, a systemd unit, an installer and an ops CLI. Use this whenever someone wants a "Claude in Slack" engineering or ops bot, a Slack-to-Claude-Code pipeline, a bot that opens PRs from Slack messages, or wants to set up, harden, debug, extend or operate one on a server, even if they don't name this skill.
---

# Slack agent bot

A team tags `@bot` in one Slack channel. The bot replies in the thread within
seconds, then does the work with headless Claude Code (`claude -p`) on a VPS
and reports back. The outcome is an answer, a file, a pushed commit or a PR.
`template/` is a complete, tested implementation. Copy it, configure it and run it.
Change its code only to extend it.

```
Slack channel ──@bot──▶ app.py (Socket Mode)  filter · claim (idempotent) · queue
                           │
                           ▼  worker thread (bot/pipeline.py)
   triage   read-only, fast    answer now | ask one question | ack + classify
   plan     read-only, code    fresh checkout → brief + DIRECT_PUSH or PR
   implement  write, isolated  own git worktree, streamed, progress lines,
                               follow-ups fed in via .bot/followups.md
   verify   python, not model  is there really a commit? (git, not the report)
   ship     python, not model  push / open PR per the requester's rights
                           │
                           ▼
   thread: answer, files, "pushed abc123" / "opened a PR: …"   + GitHub issue
```

## The rules that make it safe to leave running

Never weaken these while customising. `references/security.md` explains why each one exists.

1. **Idempotent claim.** The request id is `channel-ts`, and an INSERT claims it. Slack re-delivers events, and a re-delivery must never run a job twice.
2. **Read-only phases are read-only because of tool allowlists, not prompts.** Triage and plan get `Read/Grep/Glob`, read-only git/gh, and a `dbq` wrapper. Their deny list names `Write`, `Edit`, `git commit` and `git push`.
3. **The agent commits but never ships.** `git push` and `gh pr create/merge` are denied to it. The bot's own Python checks the commit exists, then pushes or opens the PR. Python decides who may land on the default branch (`WRITE_ALLOWED_USER_IDS`); everyone else gets a PR.
4. **Secrets are scoped.** `.env` is never loaded into `os.environ`. Each phase gets an allowlist of keys: read credentials for everyone, write credentials only for a data `action` by a write-allowed person.
5. **Slack text is untrusted data.** It is fenced in the prompt, and nothing in it can grant a tool.
6. **Nothing is reported done without the artefact.** No commit means the job failed, whatever the agent said.
7. **Terse, human replies.** One specific ack, sparse progress lines and the outcome. No walls of text in a shared channel.

## Setting one up

Work through these steps with the user. Ask only for what you cannot find yourself: which channel, which repo, who may push, and server access.

1. **Inputs.** You need the Slack workspace and channel, the GitHub repo, the people allowed to push or change data (Slack user ids), and a VPS with SSH access. Ubuntu 22.04+ with 2 vCPU and 4 GB is plenty for 2 workers.
2. **Slack app.** Create it from `template/slack-manifest.yaml`. Make an app-level token with `connections:write` (`xapp-`), install the app to get the bot token (`xoxb-`), and `/invite` the bot into the channel. See `references/slack-app.md`.
3. **Server prep.** Follow `references/vps-setup.md`:
   - Create a dedicated user and install Node, the Claude Code CLI and `gh`.
   - Log Claude in (`claude` once, or `claude setup-token` for a long-lived token).
   - Run `gh auth login` with an account or GitHub App that can push.
   - Set a git identity.
4. **Install.** Run `bash scripts/install.sh ~/slack-agent-bot` from this skill's directory on the server. It copies the template, builds the venv, clones the repo to `./repo` once `REPO_SLUG` is set, and renders the systemd unit. Re-running it is safe and upgrades in place.
5. **Configure.**
   - Fill in `.env` from `.env.example` and `chmod 600` it. Never paste tokens into a Claude chat; the user types them into the file on the server.
   - Write `context.md`: what the product is, where data lives, and things the bot must never do.
   - Optionally edit `voice.md`, the persona.
   - Set `SETUP_COMMAND` so tests can run in a fresh worktree (e.g. `pnpm install --frozen-lockfile --prefer-offline`).
6. **Doctor.** Run `.venv/bin/python doctor.py`. It checks tokens, scopes, channel membership, headless `claude`, `gh` permissions and the checkout. Fix every `XX` before going on.
7. **Dry run.** Set `BOT_DRY_RUN=true`, run `.venv/bin/python app.py` and tag the bot. The log should show `DRY RUN …`. Then set it back to `false`.
8. **Start.** Copy the unit to `/etc/systemd/system/`, then run `systemctl enable --now slack-agent-bot` and `journalctl -u slack-agent-bot -f`.
9. **First week.** Keep `BOT_FORCE_PR=true` so every change is reviewed. Turn it off once the bot has earned direct pushes for small, low-risk work.
10. **Hand over.** Show the user `bin/botctl` (below) and `references/operations.md`.

Verify each step by doing it: tag the bot with a question, a lookup and a tiny code change, and watch each reach its outcome. Run the template's tests on the server with `.venv/bin/python -m unittest discover -s tests`. They use a fake `claude` and a local git remote, and need no network.

## Running it

- `bin/botctl status`: what's in flight, and the recent requests.
- `bin/botctl stop <id>`: kill a running job and say so politely in its thread.
- `bin/botctl clean <id>`: delete every message the bot posted for a job.
- `bin/botctl rerun <id>`: run a request again, out of process, without restarting.
- `bin/botctl say <thread_ts> "text"`: speak as the bot in a thread.
- **Restart** with `sudo systemctl restart slack-agent-bot`. A restart kills running jobs, so check `botctl status` first. On the way up the bot tells each cut-off thread to re-tag.
- **Logs:** `journalctl -u slack-agent-bot -f`. Each line carries `[request_id]`.

## Customising

Prefer configuration over code.

- **Project knowledge:** `context.md`. **Persona:** `voice.md`. **Nicknames:** `ADDRESS_AS` in `.env`.
- **Databases:** map names to read-only URLs in `bin/dbq`, and list the URL keys in `READ_ENV_KEYS`. Write URLs go in `WRITE_ENV_KEYS`.
- **MCP servers** (internal APIs): set `MCP_CONFIG` to a file outside the repo, `MCP_READ_TOOLS` and `MCP_WRITE_TOOLS`. Write tools only reach write-allowed requesters.
- **Bigger changes** (a "heartbeat" that reads the channel and chimes in, several channels, scheduled jobs, new task types): see `references/extending.md`.

When debugging or changing the bot, read `references/lessons.md` first. Every rule there cost a real incident.

## Files

- `template/`: the bot. `app.py` (listener), `bot/` (config, state, pipeline, prompts, agents, gitops, slack_io, followups, attachments, github, phrases), `botctl.py`, `doctor.py`, `bin/` (botctl, dbq, past), `.env.example`, `context.md`, `voice.md`, `slack-manifest.yaml`, `systemd/`, `tests/`.
- `scripts/install.sh`: the idempotent VPS installer.
- `references/`: `architecture.md`, `security.md`, `slack-app.md`, `vps-setup.md`, `operations.md`, `lessons.md`, `extending.md`.
