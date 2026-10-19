# skills

Personal [Claude Code](https://claude.com/claude-code) skills.

## parallel-agents

A method for getting substantial software work done through parallel background agents in any git repo:
split work by area, give each agent a self-contained brief and an isolated worktree, let builders open PRs
and checkers (QA, security) only report, then integrate yourself (combine with main → full test suite →
review → merge → the project's safe deploy → live check).

- `skills/parallel-agents/SKILL.md` — the method
- `skills/parallel-agents/references/brief-template.md` — agent brief (+ QA, security, fix, investigation variants)
- `skills/parallel-agents/references/project-profile.md` — per-project profile template and how to build one
- `skills/parallel-agents/scripts/integrate.sh` — merge PR branches onto main in a scratch worktree and run the tests

### Install

```bash
git clone git@github.com:N1kky-wed/skills.git
mkdir -p ~/.claude/skills && cp -r skills/skills/parallel-agents ~/.claude/skills/
```

Each project then gets a short profile (`.claude/agent-profile.md` in the repo); the skill builds it the first time it's used.

## mahoraga

A design + research + asset pipeline for building, redesigning or pitching websites, landing pages and app UI,
distilled from real sites. It runs a loop (research in the browser pane → direction from a pinned or ten-reference
pick → assets → build → verify → ship) and keeps every design correction in `references/taste.md` so it is never
made twice.

- `skills/mahoraga/SKILL.md` — the loop
- `skills/mahoraga/references/` — taste rules, research, direction, assets, motion, app UI, build/verify/deploy, past projects
- `skills/mahoraga/scripts/` — Python tools: site/reference capture, Dribbble pulls, palette, Gemini images, video loops, tour, site checks
- `skills/mahoraga/assets/` — Next.js templates (motion, film, page shell, browser window) and example DESIGN.md files

### Install

```bash
cp -r skills/skills/mahoraga ~/.claude/skills/
```

Image and video scripts read `GEMINI_API_KEY` from the environment, or from the .env file named by `--env` or
`$MAHORAGA_ENV`. Machine-specific setup (key file, git identity, Vercel scope, where past projects live) goes in
`~/.claude/skills/mahoraga/local.md`, started from `local.example.md`; it is git-ignored and never pushed.

## switchboard

A method for organising and building systems and agents across whatever MCP servers and connectors you have, and for
handing parts of the work to the AI agents in your Slack workspace. It builds a map of your tools and Slack agents
(read-only), maps a goal onto them, messages agents only in a private agent channel or their DM (never where people
work), reads their replies from the thread, and runs the build with parallel agents.

- `skills/switchboard/SKILL.md` — the method

### Install

```bash
cp -r skills/skills/switchboard ~/.claude/skills/
```

The first time it runs it saves a `switchboard-map.md` of your servers and Slack agents and keeps it current.

## slack-agent-bot

A Slack bot that turns messages in a channel into real work done by Claude Code on a GitHub repo, running on your
own VPS. People tag it; it answers, looks things up, or writes code in an isolated worktree, runs the tests, and the
bot (not the agent) ships a commit or PR, with per-person write rights, scoped secrets, follow-ups, progress lines and
file attachments.

- `skills/slack-agent-bot/SKILL.md` — architecture, safety rules, setup steps, operations
- `skills/slack-agent-bot/template/` — the tested bot: listener, pipeline, prompts, ops CLI (`botctl`), `doctor.py`,
  Slack manifest, systemd unit, tests with a fake `claude`
- `skills/slack-agent-bot/scripts/install.sh` — idempotent VPS installer
- `skills/slack-agent-bot/references/` — architecture, security, Slack app, VPS setup, operations, lessons, extending

### Install

```bash
cp -r skills/skills/slack-agent-bot ~/.claude/skills/
```

Then ask Claude to set up a Slack bot. On the server: `bash skills/slack-agent-bot/scripts/install.sh ~/slack-agent-bot`.
Tokens go in that directory's `.env` on the server (0600), never into a chat.

## before-after

Before-and-after screenshots of a change to any web app. It photographs the same routes at the same viewports
(desktop and phone) on two versions, a base ref and a branch in their own throwaway worktrees with their own dev
servers, or two URLs such as production and a preview deploy. Each screen goes side by side under a caption,
printed to a PDF, with the PNGs kept.

- `skills/before-after/SKILL.md` — picking the two versions, running the app, signing in, writing shots, limits
- `skills/before-after/scripts/before-after.mjs` — capture, layout, PDF and pair PNGs (Node + Playwright)
- `skills/before-after/examples/8x-linkedin-local-stack.mjs` — a worked config: a Next.js monorepo on a local
  stack, with a minted session and a database reset between sides

### Install

```bash
cp -r skills/skills/before-after ~/.claude/skills/
cd ~/.claude/skills/before-after/scripts && pnpm install   # Playwright, for repos without their own
```

Then ask Claude for a before and after of a PR or a change.
