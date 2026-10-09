# Agent brief template

Copy, then fill in the `<…>` parts from the user's request and the project profile. Keep every section: the agent knows nothing beyond what's here.

---

<One-line goal> in <project name> (<one-line description of the stack>; repo <owner/repo>; <live URL or "not deployed">; production lives at <path/host from the profile> — do NOT modify production files, data, config or services, and do not deploy). Your job ends at an OPEN pull request (not merged).

User's ask, verbatim:
"<paste exactly, typos included>"
<Quoted reports / screenshot descriptions, with file paths the agent can open.>

Context — already done (read the main branch first): <PRs/commits + one line each + key files>.
<Facts you already established: data findings, measurements, root-cause evidence, decisions the user made.>

Coordination: <other agents in flight, their branches, and the files they own — "do NOT edit X; keep shared-file edits small and localized">.

Your scope:
1. <item — what and why; constraints; decisions already made>
2. <…>
<Decisions you want the agent to make and justify: thresholds, defaults, privacy rules, trade-offs.>

Read first: <the most relevant files/functions/docs>.

Verification:
- Tests: <the profile's test command>. Do NOT run <the profile's list of tests that touch real systems>. All must pass. Add tests for <…>.
- Real run: <the profile's preview recipe>, with YOUR OWN data dir/DB copy and ports <unique numbers>. Before any run that talks to shared services: <the profile's side-effect switches, e.g. disable recording/sending, unique IDs, stub endpoints>. Capture evidence (screenshots, output, numbers) and look at it yourself before reporting. Stop anything you started, by PID.
- Run everything slow in the background (test suites, previews, browser checks, builds) and take exit status from the command itself, not from a `| tail`. Never block on a foreground wait.
- If any command is blocked by the permission system, STOP and report what and why. Don't work around it.

Worktree: `git -C <repo> fetch -q && git -C <repo> worktree add -b <type>/<short-name> <worktree path> origin/<main>`. Never use bare `git stash` (it's shared across worktrees).
Commit and PR: <the profile's conventions: message format, sign-off/co-author line, pre-commit checks>. Push, then open a PR to <main>. The body quotes the user's ask and covers design and decisions, tests, what was verified for real vs. simulated, risks, and prod steps. Do NOT merge.

Report: PR URL; what changed and why; decisions; verification (real vs. simulated); measurements; prod steps needed (describe, don't apply); risks; next ideas.

---

## Variants

**Report-only QA agent.** Replace the job line with "FIND and REPORT problems with evidence — do NOT change code or open PRs; never act on production." Use a detached worktree (`worktree add --detach …`) and remove it at the end. List recent fixes to re-verify, and the devices, roles and states to cover. Report: prioritized issues (severity, exact steps, environment, expected vs. actual, evidence path, errors, likely file/function), what works, coverage and gaps.

**Security review agent.** Report-only. Against production, at most plain unauthenticated reads of public URLs; all active testing goes against a local copy. Scope: the PRs/files to review. Look for authz/IDOR, CSRF, info leaks, injection/XSS, SSRF, open redirects, token handling and replay, cache issues, DoS bounds, secrets in logs. Report: findings ranked critical → info, each with location, a concrete scenario (reproduced locally where possible), impact and a specific fix, plus what was checked and found sound. No working exploit code against live systems.

**Fix agent from findings.** Paste the findings with their evidence paths. Require "reproduce each issue first, fix, then show before/after", plus a regression test per finding.

**Investigation agent.** Scope a question rather than a change ("why does X happen; measure Y"). Require evidence with sources (file:line, log lines, numbers), and a recommendation with alternatives. No changes unless the brief allows a PR.
