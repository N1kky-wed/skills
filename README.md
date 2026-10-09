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
