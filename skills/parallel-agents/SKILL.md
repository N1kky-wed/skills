---
name: parallel-agents
description: A method for getting substantial software work done through parallel background agents in any git repo. Split work by area, give each agent a self-contained brief and an isolated worktree, let builders open PRs and checkers (QA, security) only report, then integrate yourself (combine with main → full test suite → review → merge → the project's safe deploy → live check). Use this whenever a request is bigger than a quick one-file edit — a feature, several fixes at once (e.g. a batch of bug reports or screenshots), a QA or security pass, an overnight or "keep going until I stop you" job — or when the user asks for agents, parallel work or workflows, even if they don't name this skill.
---

# Parallel agents

Agents build and check in isolation; you, the coordinator, integrate, verify and ship. Agents never merge or deploy. That stays with you, so one person sees the whole picture before anything reaches users. This loop has shipped dozens of PRs in a day without breaking production. Most of its value is in the brief and in the integration step.

## 0. Load the project profile first

Every project differs in how you test, preview and ship, and in what counts as production. Those facts live in a **project profile**:
1. Look for `.claude/agent-profile.md` in the repo root. Also check for a project-specific skill or memory entry (e.g. `<project>-agents`).
2. If there's none, build one with `references/project-profile.md`. Derive what you can from the repo (README, CI config, test layout, deploy scripts, docker files). Ask the user only about things you can't infer *and* that matter for safety: which tests touch real systems, how deploys happen, and what must never be touched. Save it to `.claude/agent-profile.md` (or memory if the repo shouldn't hold it) and tell the user in one line.

Everything below says "per the profile" wherever a project-specific fact is needed.

## 1. Decide the shape of the work

- **Small (one file, a few lines):** do it yourself in a worktree: change, test, check, PR, merge, ship. Spawning an agent costs more than it saves.
- **Bigger, or several independent asks:** one agent per *area*, chosen so their files overlap as little as possible (e.g. UI shell vs. notifications vs. scheduling, or per package/service). When two agents must touch the same file, tell each to keep its edits inside its own functions. Then merge their PRs one at a time and re-test after each merge.
- **Checking rather than building:** QA or security agents **only report** (no code, no PRs). Give their findings to a fix agent, or to the builder already working in those files (via SendMessage), so ownership stays clear.
- **Research or root-causing an incident:** look at real data yourself first: logs, metrics, the affected records. Delegate only the bounded investigation or the fix.
- Launch independent agents **in one message** so they run concurrently, in the background. Keep talking to the user while they work. Prefer a handful of well-briefed agents over many thin ones.

## 2. Write the brief

Each agent starts with no context, so the brief must stand alone. Use `references/brief-template.md`. The parts that matter most, and why:

- **The user's words, verbatim** (typos included), plus any quoted reports. Agents treat only the latest message as "the request", and paraphrase loses intent.
- **What already shipped and where:** PR numbers and files, so they build on current main and don't redo or undo work.
- **Coordination:** the files they own, the files a parallel agent owns, and the branch names of work in flight.
- **Isolation:** a fresh worktree from the main branch, plus their own scratch data and ports, so parallel previews can't clobber each other.
- **Safety rules:** the generic ones from §5, plus the profile's production boundaries.
- **Verification:** the profile's test command (never the suites it marks as touching real systems), a real run of the changed behaviour (browser, CLI, API) with evidence the agent has actually looked at, and before/after numbers for performance work.
- **End state:** an open PR with a specific body, *not merged*, and a report in a set shape.

### Run tasks in the background, always

The user wants the conversation free while work happens, so nothing slow runs in the foreground: not by you, and not by the agents you brief.
- **Agents:** always launch them in the background (the default for the Agent tool), never wait on one in the foreground.
- **Your own commands:** anything that can take more than a few seconds runs with `run_in_background: true`. That covers test suites, `integrate.sh`, builds, deploys, media processing, long greps and installs. Then keep talking to the user. You're notified when it exits, so don't poll it or sleep-wait. If you need several notifications from one job, use a Monitor with a filter that also matches failures.
- **Briefs:** put this rule in every brief. Agents start their previews, test suites and browser checks in the background, and stop them by PID when done.
- **Gates:** a background step that gates the next one (tests → push, tests → merge) must check the real exit status. Write the output to a file, take `$?` from the test command itself, then `tail` the file; `cmd | tail && git push` pushes even when the tests fail, because the pipeline's status is `tail`'s.

## 3. While agents run

- Don't duplicate their work, and don't read their transcripts. You'll get a notification when each one finishes; don't predict its results before then.
- Pass new user asks for an area to the agent already working there (SendMessage), rather than starting a competing agent.
- If an agent stops because a command was blocked, that's a question for the user (§5), not a task for you to finish.

## 4. Integrate and ship (you)

For each finished PR:
1. **Combine with current main and test everything.** Run `scripts/integrate.sh <branch> [more…]`. It creates a scratch worktree from the main branch, merges the branches, stops on conflicts, and runs the profile's test command. Configure it via the env vars at its top, or a `.claude/agent-profile.env`. Run it in the background.
2. **Conflicts:** resolve them in the scratch worktree, keeping both sides' intent. Put the same resolution on the PR branch (merge main into it, then copy the resolved files from the scratch commit) and confirm the two trees are identical (`git diff HEAD <scratch sha>` is empty). What you merge must be exactly what you tested.
3. **Review the risky parts yourself:** auth and permissions, input validation, anything touching user data, money, or production config. Be extra careful when an automated check on the agent's work was skipped or timed out.
4. **Check user-facing changes yourself:** for UI or behaviour changes, do a short real run on the combined code (the profile's preview), not just tests.
5. **Merge** with the project's convention (`gh pr merge …`). Run `gh` from inside the repo; outside it, the merge silently doesn't happen.
6. **Ship** only via the profile's safe deploy path, then run the profile's live check. If the profile says deploys are zero-downtime, don't hold them for user activity.
7. **Prod steps** the PR lists (cron, web server, env/config): back up the live file first, apply, validate (`nginx -t`, `logrotate -d`, a dry run), then reload.
8. **Record it:** add a dated line to the project memory with what shipped, the commit, and any config changed.

## 5. Safety rules

These are general lessons. Each one came from a real near-miss.

- **Blocked means stop.** If the permission system refuses an action, yours or an agent's, say what was blocked and why it's needed, then wait. Don't find another route, and don't redo an agent's blocked action in your own session; that launders the permission. An approval covers the exact command the user saw, so retry it unchanged.
- **Previews must not touch production.** Check every shared service a preview talks to: databases, media servers, queues, recorders writing to shared folders, email/push/calendar senders. Point them at stubs or throwaway copies, switch off side effects (recording, sending) in the preview's own data, and use unique IDs so nothing collides with real records. If a preview *needs* a production secret, ask the user.
- **Tests that touch real systems are off-limits** unless the user asks. The profile lists them, and agents must exclude them explicitly; don't rely on a glob.
- **Production data changes:** read-only queries first, then back up the affected rows or files with a timestamp, then a narrow change with guards (state/owner conditions), then verify. Files owned by service users may need elevated rights; only remove what you've confirmed is junk.
- **Secrets:** back up config before editing, append rather than rewrite, and never print secret values (redirect to files, grep key names only).
- **Outward-facing actions** (emails, pushes, calendar invites, posts, permission grants) happen only when the user asked. Use the project's audit trail if it has one.
- **Worktree and harness hygiene:**
  - Never use bare `git stash`: the stash stack is shared across worktrees.
  - Kill processes by PID, never with `pkill -f` on a pattern that also matches your own shell.
  - Don't name scratch scripts after standard-library modules.
  - Clean up worktrees, servers and containers you started.

## 6. Talking to the user

- Lead with the outcome in plain words ("live", "fixed", "blocked — need your OK"), then what changed, how it was verified (what was real vs. simulated), and anything they need to decide. Match their vocabulary and keep jargon out.
- The user doesn't see agent reports. Relay what matters, including mistakes an agent made and how they were handled.
- **Incidents:** look at real data first. Separate the platform from individual users' conditions, say honestly whether a recent change could be the cause, and offer a reversible mitigation (a kill switch, a revert) before a deeper fix.
- **Long or overnight jobs:** keep a queue of next rounds (polish, performance, QA sweep, security review, fix the findings), and say what's running and what's next each time something lands.
