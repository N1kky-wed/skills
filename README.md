# skills

Personal [Claude Code](https://claude.com/claude-code) skills. They hold no machine-specific paths: scripts work
relative to the folder you run them from (or folders you name with environment variables), and anything that belongs
to one machine goes in a git-ignored `local.md`.

## Install

Clone once, then copy the skills you want into your personal skills folder (`~/.claude/skills`), or into a project's
`.claude/skills` to share them with that repo.

macOS / Linux:

```bash
git clone https://github.com/N1kky-wed/skills.git
mkdir -p ~/.claude/skills
cp -r skills/skills/parallel-agents skills/skills/mahoraga ~/.claude/skills/
```

Windows (PowerShell):

```powershell
git clone https://github.com/N1kky-wed/skills.git
New-Item -ItemType Directory -Force "$HOME\.claude\skills" | Out-Null
Copy-Item -Recurse -Force skills\skills\parallel-agents, skills\skills\mahoraga "$HOME\.claude\skills\"
```

## parallel-agents

A method for getting substantial software work done through parallel background agents in any git repo:
split work by area, give each agent a self-contained brief and an isolated worktree, let builders open PRs
and checkers (QA, security) only report, then integrate yourself (combine with main → full test suite →
review → merge → the project's safe deploy → live check).

- `skills/parallel-agents/SKILL.md` — the method
- `skills/parallel-agents/references/brief-template.md` — agent brief (+ QA, security, fix, investigation variants)
- `skills/parallel-agents/references/project-profile.md` — per-project profile template and how to build one
- `skills/parallel-agents/scripts/integrate.sh` — merge PR branches onto main in a scratch worktree and run the tests
  (bash; on Windows it runs in Git Bash)

Needs only git and bash. Each project then gets a short profile (`.claude/agent-profile.md` in the repo); the skill
builds it the first time it's used.

## mahoraga

A design + research + asset pipeline for building, redesigning or pitching websites, landing pages and app UI,
distilled from real sites. It runs a loop (research in the browser pane → direction from a pinned or ten-reference
pick → assets → build → verify → ship) and keeps every design correction in `references/taste.md` so it is never
made twice.

- `skills/mahoraga/SKILL.md` — the loop
- `skills/mahoraga/references/` — taste rules, research, direction, assets, motion, app UI, build/verify/deploy, past projects
- `skills/mahoraga/scripts/` — Python tools: site/reference capture, Dribbble pulls, palette, Gemini images, video loops, tour, site checks
- `skills/mahoraga/assets/` — Next.js templates (motion, film, page shell, browser window) and example DESIGN.md files

### Setup

Python 3.10 or newer (`python3` on macOS/Linux if `python` is missing; on Windows the path is
`$HOME\.claude\skills\mahoraga\scripts\requirements.txt`):

```bash
python -m pip install -r ~/.claude/skills/mahoraga/scripts/requirements.txt
python -m playwright install chromium
```

Video work also wants ffmpeg on PATH (`brew install ffmpeg`, `sudo apt install ffmpeg`, `winget install ffmpeg`);
without it the scripts fall back to the `imageio-ffmpeg` binary from pip.

### Gemini API key (required for image and video generation)

`scripts/gemini_image.py`, the borrowed `gen_*.py` and `grade_portraits.py` scripts, and any Veo or Omni video call
the Gemini API, and **they will not run without a `GEMINI_API_KEY`**. Everything else (site capture, Dribbble pulls,
palette, video encoding, site checks) needs no key.

1. Create a key at https://aistudio.google.com/apikey. Calls are billed to the key's Google project, and some image
   and video models need billing turned on there.
2. Make it available in any one of these ways:
   - An environment variable:
     - macOS / Linux: `export GEMINI_API_KEY="your-key"` (add the line to `~/.zshrc` or `~/.bashrc` to keep it)
     - Windows PowerShell: `$env:GEMINI_API_KEY="your-key"` for this session, or `setx GEMINI_API_KEY "your-key"`
       to keep it for new terminals
   - A `.env` file holding the line `GEMINI_API_KEY=your-key`, either in the folder you run the scripts from, or
     anywhere with `MAHORAGA_ENV` pointing at it (`gemini_image.py` also takes `--env path/to/.env`).
3. Check it: `python ~/.claude/skills/mahoraga/scripts/gemini_key.py` says where the key was found (it never prints
   the key).

Without a key the scripts stop before calling anything and print these steps. Never commit the key; `.env` files are
git-ignored here.

### Machine-specific setup (optional)

Which .env holds the key, the git identity, the Vercel scope and where past projects live go in
`~/.claude/skills/mahoraga/local.md`, started from `local.example.md`. It is git-ignored and never pushed; without
it the skill asks for what it needs.
