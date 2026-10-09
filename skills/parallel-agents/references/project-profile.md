# Project profile

A short, factual file that tells the coordinator and every agent how this particular project is tested, previewed and shipped, and what counts as production. Save it as `.claude/agent-profile.md` in the repo, or in the project's memory if it holds host-specific details that shouldn't be committed. Keep it under ~80 lines, and update it whenever you learn something the hard way.

## Template

```markdown
# Agent profile: <project>

## Basics
- Repo / main branch: <owner/repo>, <main>
- Stack: <languages, frameworks, services>
- Live at: <URL / hosts>; production checkout or deploy target: <path or "CI only">

## Tests
- Run all safe tests: <command, incl. env vars / virtualenv / working dir>
- NEVER run (they touch real systems): <files/markers/targets>
- Per-file run: <command pattern>
- Syntax/lint quick checks: <e.g. node --check, tsc --noEmit, ruff>

## Preview (real run without production)
- How to start: <script/command; port range agents may use; data dir/DB copy>
- Shared services a preview may touch, and how to neutralise each: <db, media server, queue, email/push, storage> → <stub / flag / unique IDs>
- Gotchas: <auth cookies, seed data, cached assets, anything that bit before>

## Ship
- Merge convention: <gh pr merge --merge / squash; who may merge>
- Deploy: <command>. Zero-downtime? <yes/no>. Safe during user activity? <yes/no>
- Live check after deploy: <command/URL>
- Prod config locations + backup habit: <cron, nginx, env file, ...>

## Conventions
- Commit message format, sign-off/co-author lines, pre-commit checks: <...>
- PR body requirements: <...>

## Production boundaries (things agents must never touch)
- <paths, databases, buckets, services, accounts>

## Lessons learned
- <dated one-liners: what went wrong and the rule it produced>
```

## Building one for a new project

Derive before asking:
- **Tests:** CI config (`.github/workflows`, `Makefile`, `package.json` scripts, `pyproject`/`pytest.ini`, `tests/README`). Look for tests that need credentials, hit URLs, or write data: names like e2e/live/integration/smoke/load, env vars like `*_URL`/`*_KEY`, or network calls in fixtures. Treat anything doubtful as "never run" until the user confirms.
- **Preview:** README "development" sections, docker-compose, dev scripts, seed/fixture scripts.
- **Ship:** deploy scripts, CI deploy jobs, Procfile/systemd units, infra docs.
- **Boundaries:** paths the deploy writes to, production env files, shared services named in config.

Then ask the user only what's still unknown *and* safety-relevant. Usually that's: "Which tests touch real systems?", "How do you deploy, and is it safe during use?", and "Anything agents must never touch?". Write the profile, show it in a few lines, and proceed.
