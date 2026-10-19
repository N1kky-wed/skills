---
name: before-after
description: Before-and-after screenshots of a change to a web app, in any repo and any stack. It photographs the same routes at the same viewports (desktop and phone) on two versions — a base ref and a branch, each in its own throwaway worktree with its own dev server, or two URLs such as production and a preview deploy — then lays each screen out side by side with a caption, prints a PDF and keeps the PNGs. Use it whenever the user asks for a before and after, screenshots of a change or a PR, "show me what changed", visual proof for a review, Slack or a client, or a PDF of a UI fix, even if they don't say "before-after".
---

# Before and after

One script does the whole job: `scripts/before-after.mjs <config.mjs>`. Your work is the config: which two versions, how the app runs, how to sign in, which screens, and what each caption says. The script never touches the user's working tree. A ref gets its own `git worktree` in the temp folder, an install from the shared store and a dev server on its own port, and is removed afterwards. The two sides run one after the other, so only one dev server and one browser are up at a time.

## 1. Pick the two versions

| The ask | before | after |
|---|---|---|
| A PR, open or merged | `{ ref: "<merge-sha>^" }` or `{ ref: "origin/main" }` | `{ ref: "<merge-sha>" }` or `{ ref: "<pr-branch>" }` |
| Uncommitted work in this checkout | `{ ref: "HEAD" }` | `{ worktree: true }` (runs here, as it is) |
| Live site vs a preview deploy | `{ url: "https://site.com" }` | `{ url: "https://pr-123.preview.app" }` |
| A fix already live | `{ ref: "<sha-before-the-fix>" }` | `{ url: "https://site.com" }` |

Merged PR: `gh pr view <n> --json mergeCommit` gives the sha; `<sha>^` is main just before it. Sides can mix (a ref and a URL).

## 2. Find out how the app runs

Read before asking. In order: the project's own before/after or screenshot tooling (search for `before-after`, `screens`, `shots`, `walkthrough`), a project memory or `.claude/` profile, the README's "run locally" section, then `package.json` scripts and the lockfile. Things to settle:

- **Where the app lives** (`app.cwd`), for a monorepo such as `apps/web`.
- **Install**: detected from the lockfile when omitted (pnpm, an npm repo through `pnpm import`, yarn, bun). Set `app.install` for anything else, `null` to skip.
- **Start**: detected as `pnpm run dev --port {port}` when omitted. Set `app.start` when the port flag differs (`-p`, `PORT` only) or for non-JS stacks: `python -m uv run manage.py runserver {port}`, `bundle exec rails s -p {port}`, `go run . --addr :{port}`. `PORT` is always set too.
- **Env**: untracked files the app needs go in `app.copy` (copied from the main checkout into each worktree). Extra variables go in `app.env` or `app.envFile`; `{root}` in a value is that side's checkout. **If the env file names a production database or API, don't run against it.** Use the project's local stack or seeded dev database, or compare two deployed URLs instead.
- **Ready**: `app.ready` is a path polled until it answers below 500 (default `/`). Pick a public page when `/` redirects to a login.

## 3. Sign in

The script has no login form step. Give it a session one of these ways:
- `auth.command`: a command run for each pass that prints a cookie as JSON: a Playwright cookie array, one `{ name, value }`, or `{ cookieName, cookieValue }`. Use this when the project can mint a session for a seeded account (most local stacks, Supabase, NextAuth with a dev secret).
- `auth.storageState`: a Playwright storage-state file saved from a dev or test login.
- `auth.cookies`: literal cookies, for a dev-only session.

Real OAuth (Google, LinkedIn, GitHub) on a production URL can't be scripted. Ask the user for a test account on a local or staging build, or photograph the public pages only.

## 4. Write the shots

Each shot is one screen. It runs at every viewport unless it names some. Captions are the point of the document, so write them for someone who never saw the code: what the screen is, what was wrong, and what is right now.

```js
// before-after.config.mjs: keep it in the scratchpad, or in the repo if the team will reuse it.
export default {
  name: "pr-283-saved-topics",          // file names and the PDF's name
  title: "Saved topics show as picked",
  lede: "One line under the title: the PR, where to look.",
  before: { ref: "45e002fb^" },
  after: { ref: "45e002fb" },
  app: { cwd: "apps/web", copy: ["apps/web/.env.local"], ready: "/login", env: {}, ports: [3101, 3102] },
  auth: { command: "node scripts/mint-session.mjs maya@test.dev" },
  viewports: [                          // default: desktop 1280x800 and phone 390x844 @2x
    { name: "desktop", width: 1280, height: 800 },
    { name: "phone", width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true },
  ],
  reset: async ({ label }) => {},       // or a shell command; runs before each side, for flows that write
  prepare: async (page, { label, viewport }) => {}, // after every navigation: cookie bars, first-run notices
  shots: [
    {
      id: "profile-topics",
      path: "/employee/app/profile",
      say: "Profile settings, right after saving two typed topics",  // the screen's heading
      beforeWords: "The typed topics stay in the box.",               // under each side
      afterWords: "They move into the picked chips.",
      act: async (page, { label, viewport }) => {},  // clicks and typing before the shutter
      only: "after",            // optional: the screen is new ("before" = it was removed)
      viewports: ["desktop"],   // optional: only some sizes
      fullPage: false,          // optional: the whole scroll height
      settle: 1200,             // optional: ms to wait before the shot
    },
  ],
};
```

Write `act` with role and text locators (`getByRole`, `getByPlaceholder`, `getByText`) and wait for the result on screen. A fixed sleep photographs spinners. When an act fails in one pass only (a control the change added), that shot should say `only: "after"`.

## 5. Run it, then look

```bash
node ~/.claude/skills/before-after/scripts/before-after.mjs <config.mjs> [--out <dir>] [--keep]
```

Run it in the background: an install plus two dev-server compiles takes minutes. It prints where it wrote:
- `<name>.pdf`: A4 landscape, one screen per page, before and after side by side under the caption.
- `pairs/<viewport>-<id>.png`: each page of the PDF as an image, for Slack or a PR comment.
- `shots/<side>-<viewport>-<id>.png`: the raw screenshots.
- `index.html`: the page the PDF was printed from.

`--keep` keeps the worktrees for a rerun. Exit code 1 means a shot failed: the report is still written, with the failure named at the top. **Open the pairs before sending anything.** Check that the two sides differ where the change is, that neither is a login page, a spinner or an error overlay, and that the caption matches what is on screen. Fix the config and rerun rather than explaining a bad picture.

Playwright comes from the project when it has one, otherwise from this skill (`cd ~/.claude/skills/before-after/scripts && pnpm install`, once). `PLAYWRIGHT_CHROMIUM` points it at a specific browser.

## 6. Deliver

Attach the PDF and say in one line what it shows. Add the pair PNGs when the user will paste them somewhere. Put the PDF in the PR description or a comment only when the user asked for that.

## What it can't do

- **Real OAuth or SSO logins** on production, and anything behind 2FA or a CAPTCHA. Use a minted session, a storage state, or public pages.
- **Native mobile or desktop apps.** "Phone" means a phone-sized mobile browser.
- **Old commits that no longer build or install**, such as a lockfile that has drifted or a removed dependency. Compare against a deployed URL instead.
- **Data it doesn't own.** Each side shows whatever its database holds at that moment. Use `reset` or seeded fixtures for flows that write, and never point a local run at production data.
- **Third-party calls** (payments, email, AI) run for real unless the project stubs them. Stub them or skip those screens.
- **Animations and live data** can differ between the two sides by timing alone. Wait for the settled state, or freeze it in `prepare`.

## Project notes

Per-project setup goes in `examples/`, one worked config each:
- `examples/8x-linkedin-local-stack.mjs`: 8x business. It runs on the local stack (Postgres, PostgREST and the gateway already up), starts the app with the env block `up.sh` prints using keys minted from the harness secret, plants a minted session for a seeded account, and resets the account before each side. Never start it against `.env.local` alone, because that file names production. The repo's own `apps/web/scripts/local-stack/before-after.mjs` (which stashes uncommitted work) is the older, single-repo version of this skill.
