# Extending the bot

Change configuration before code. When you do change code, keep the rules in
SKILL.md intact, add a test in `tests/test_bot.py` (the fake `claude` makes
that cheap), and run the suite.

## Give it your data

- **Read-only database.** Add a line to `bin/dbq` (`analytics) url="${ANALYTICS_READ_URL:-}" ;;`). Put the URL in `.env`, add its key to `READ_ENV_KEYS`, and describe the tables and an example query in `context.md`. Triage can then answer counts on its own.
- **Write access for data fixes.** Use a narrowly-granted role. Add its key to `WRITE_ENV_KEYS`. It appears only in an `action` run by a write-allowed person. The prompt already makes the agent run the equivalent SELECT and use a transaction.
- **Internal APIs through MCP.** Write a `mcp.json` outside the repo (`claude --mcp-config` format, with bearer tokens from `.env` interpolated by you or stored in the file at 0600). Then set `MCP_CONFIG`, `MCP_READ_TOOLS` and `MCP_WRITE_TOOLS`. List tools by exact name. Generate the list from the server's `tools/list`, not by hand: hand lists miss tools.
- **Metered third-party APIs** (scrapers, enrichment). Put the key in `IMPLEMENTER_ENV_KEYS`. Say in `context.md` which endpoints work, which are broken or rate-limited, and that calls cost money.

## New task types

`prompts.TASK_TYPES` drives triage. To add, say, `report` (writes a long document):

1. Add it to `OPERATION_TYPES` (produces an answer) or `CODE_TYPES` (produces a commit).
2. Describe it in the triage prompt's "Decide what this is" list.
3. If it needs different rules, branch on `task` in `prompts.implement`.
4. Add a fake-claude scenario and a test.

## Heartbeat: a bot that reads the room

The original bot had an optional heartbeat thread. Every 15 minutes it read the channel's last 12 hours, judged each new message once (recorded in a `seen_messages` table so nothing is judged twice), and mostly stayed silent. Now and then it answered an unasked question that it could answer read-only.

If you build one:

- Default to **silence**. A bot that talks unprompted is tiring.
- An unprompted run gets **no write tools at all**: no MCP writes, no actions, no code. At most, it offers: "i could take a run at that, tag me".
- Skip a beat while real jobs are running, so it doesn't queue behind them on the rate limit.
- Beat on start-up, then sleep. Sleeping first opens a 15-minute blind spot after every deploy.
- Retry an empty channel read (see `lessons.md`).
- Make it switchable (`BOT_HEARTBEAT=false` by default) and wake it with `SIGUSR1` for testing.

## More channels

`CHANNEL_ID` is a single value on purpose: one channel, one audience, one set of permissions. For several, run one service per channel, each with its own `.env`, state and repo checkout. That keeps permissions and context from bleeding across. A shared multi-channel bot needs the channel in every Slack call and per-channel config, which is a real refactor.

## Several repos

Same advice: one instance per repo. Repos have different setup commands, conventions and reviewers.

## Scheduled work

Use a systemd timer or cron that posts a tagged message into the channel as a person (or calls `botctl say` and then `rerun`), rather than a scheduler inside the bot. Scheduled jobs then go through the same claim, permissions and logging as everything else.

## Delivering files outside Slack

Large outputs can go to object storage or a static file server instead of a Slack upload. Have the agent write to `$BOT_OUT_DIR` as usual, then extend `pipeline._deliver_files` to copy each file and post a link. Links are usually unauthenticated, so say so in the thread when the file names real people.
