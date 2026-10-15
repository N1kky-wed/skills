# Security model

The bot reads text from anyone in a channel and runs an agent with shell access
on a server that holds credentials. Assume someone will try to talk it into
something. The controls below enforce limits mechanically; none of them rely
on the model behaving.

## Threats and controls

| Threat | Control | Where |
|---|---|---|
| Prompt injection in a message, a thread or an attachment | Fenced as untrusted data in every prompt. Tools come from allowlists, so text can't grant a tool. | `prompts.UNTRUSTED`, `config.*_TOOLS` |
| Anyone in the channel landing code on main | Agents cannot push (denied). Python ships, and only `WRITE_ALLOWED_USER_IDS` get DIRECT_PUSH; everyone else gets a PR. | `pipeline.run_and_ship`, `config.can_write` |
| Anyone changing live data | `action` is refused before any run unless the requester is write-allowed. Write credentials (`WRITE_ENV_KEYS`) and MCP write tools exist only in that run. | `pipeline.process`, `config.implementer_env` |
| An agent reading every secret on the box | `.env` is never put in `os.environ`. Each subprocess env is built up from an allowlist (`scoped_env`). | `config.py` |
| Data sent out through a URL | Triage and plan have `WebSearch` but no `WebFetch`, and Bash only under read-only prefixes. Only the implementer can fetch. | `config.READ_ONLY_TOOLS` |
| Private content leaking into a public channel, issue or PR | The bot reads Slack only through its own token, only in its channel. Agents get no Slack MCP tools. The prompt says that everything written is public. | `slack_io.read_thread`, `prompts.PRIVACY` |
| Double execution | Idempotent claim on `channel-ts`. The handler acks in under 3 s. | `state.claim`, `app.handle` |
| The bot triggering itself | Messages with a `bot_id` are dropped. | `app.is_human` |
| A false "done" | Commits are verified against git, and pushes are confirmed on the remote. | `gitops.verify`, `gitops.push_direct` |
| Bypassing the repo's checks | `--no-verify` is impossible because the agent never pushes. Hooks run on the bot's push, and a failure goes back to the agent. | `gitops`, `pipeline` |
| Destructive git on shared history | `git reset --hard origin`, `git remote`, `gh api` and deleting the default branch are denied. Pushes are never forced. | `config.IMPLEMENTER_DENY` |

## Limits, stated honestly

- **The implementer has `Bash`.** It can read anything the bot's Unix user can read, including `~/.claude` (Claude credentials) and `~/.config/gh` (the GitHub token). Contain this:
  - Run the bot as a **dedicated Unix user** that owns nothing else.
  - Give `gh` a **fine-grained token or a GitHub App** scoped to the one repo (contents and pull requests: read/write; nothing else).
  - Turn on **branch protection** on the default branch. Require PRs and checks, and allow the bot's identity to bypass only if you want DIRECT_PUSH at all.
  - Never put production admin credentials in `.env`. Use read-only roles for `READ_ENV_KEYS` and a narrowly-scoped role for `WRITE_ENV_KEYS`.
- **Deny rules are prefix matches.** They stop accidents and casual attempts. GitHub permissions, branch protection and database roles are the walls.
- **Model credentials** (`CLAUDE_CODE_OAUTH_TOKEN` or `ANTHROPIC_API_KEY`) necessarily reach every agent. Set a spend limit on the account.

## Rules for whoever operates or edits the bot

- Never paste a token into a Claude chat, an issue or a commit. The person types secrets into `.env` on the server.
- Keep `.env` at mode 0600 and out of git. `.env.example` holds placeholders only.
- A new credential goes in `.env`, and then into exactly one of `READ_ENV_KEYS`, `IMPLEMENTER_ENV_KEYS` or `WRITE_ENV_KEYS`. Never widen the base env.
- A new MCP tool goes in `MCP_READ_TOOLS` only if it truly can't change anything.
- Don't give any phase Slack MCP tools that run as a person. They can read that person's DMs, and the agent's output is public.
- Keep the bot's channel focused. Everyone in it can make the bot spend money and read whatever its read credentials can.

## Pre-launch checklist

- [ ] Dedicated Unix user; `.env` is 0600.
- [ ] `gh` uses a token or app scoped to this repo only.
- [ ] Branch protection is on for the default branch.
- [ ] `WRITE_ALLOWED_USER_IDS` lists only the people who should land code and data.
- [ ] Read-only database roles in `READ_ENV_KEYS`; write roles only in `WRITE_ENV_KEYS`.
- [ ] `BOT_FORCE_PR=true` for the first week.
- [ ] A spend limit on the Claude account.
- [ ] `doctor.py` passes; the tests pass on the server.
