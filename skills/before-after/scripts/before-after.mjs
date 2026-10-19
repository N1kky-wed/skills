#!/usr/bin/env node
/**
 * The same screens, photographed on two versions of a web app, laid out side by
 * side with a caption per screen, printed to a PDF, PNGs kept.
 *
 *   node before-after.mjs <config.mjs> [--out <dir>] [--keep]
 *
 * A side is either a URL that already serves that version (production, a
 * preview deploy) or a git ref. A ref gets its own throwaway worktree, an
 * install and a dev server on its own port, so your working tree is never
 * stashed or switched. The two sides run one after the other, never together.
 *
 * The config format is in ../SKILL.md. Exit code 1 means a shot failed; the
 * report is still written, with the failure in it.
 */
import { execFileSync, execSync, spawn } from "node:child_process";
import { copyFileSync, existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { createRequire } from "node:module";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const WIN = process.platform === "win32";

const DEFAULT_VIEWPORTS = [
  { name: "desktop", width: 1280, height: 800 },
  { name: "phone", width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true },
];

/* ----------------------------------------------------------------- args */

const args = process.argv.slice(2);
const flag = (name) => {
  const i = args.indexOf(name);
  if (i < 0) return null;
  const v = args[i + 1];
  args.splice(i, v && !v.startsWith("--") ? 2 : 1);
  return v && !v.startsWith("--") ? v : true;
};
const outFlag = flag("--out");
const keep = Boolean(flag("--keep"));
const configPath = args[0];
if (!configPath) {
  console.error("usage: node before-after.mjs <config.mjs> [--out <dir>] [--keep]");
  process.exit(2);
}
const configFile = resolve(configPath);
const cfg = (await import(pathToFileURL(configFile).href)).default;
if (!cfg?.shots?.length) throw new Error("the config has no shots");
if (!cfg.before || !cfg.after) throw new Error("the config needs both `before` and `after`");

const sh = (cmd, cwd, env) =>
  execSync(cmd, { cwd, env: { ...process.env, ...env }, stdio: "inherit" });
const git = (cwd, ...a) => execFileSync("git", a, { cwd, encoding: "utf8" }).trim();

const REPO = resolve(
  cfg.repo ? resolve(dirname(configFile), cfg.repo) : git(process.cwd(), "rev-parse", "--show-toplevel"),
);
const name = cfg.name ?? "before-after";
const stamp = new Date().toISOString().slice(0, 16).replace(/[:T]/g, "-");
const OUT = resolve(outFlag && outFlag !== true ? outFlag : join(tmpdir(), "before-after", `${name}-${stamp}`));
mkdirSync(join(OUT, "shots"), { recursive: true });
mkdirSync(join(OUT, "pairs"), { recursive: true });

const viewports = cfg.viewports ?? DEFAULT_VIEWPORTS;

/* ----------------------------------------------------------- playwright */

/**
 * Playwright from the project if it has one, else from this skill's own
 * scripts folder (`pnpm install` there once). A pnpm workspace keeps it under
 * the app package, so the app's folder is asked too.
 */
async function playwright() {
  const roots = [
    cfg.playwrightFrom && resolve(REPO, cfg.playwrightFrom),
    cfg.app?.cwd && resolve(REPO, cfg.app.cwd),
    process.cwd(),
    REPO,
    HERE,
  ].filter(Boolean);
  for (const root of roots) {
    try {
      const at = createRequire(join(root, "noop.js")).resolve("playwright");
      const mod = await import(pathToFileURL(at).href);
      return mod.chromium ? mod : mod.default;
    } catch {
      /* next root */
    }
  }
  throw new Error(`playwright is not installed here. Run: cd "${HERE}" && pnpm install`);
}
const { chromium } = await playwright();
const launchOptions = process.env.PLAYWRIGHT_CHROMIUM
  ? { executablePath: process.env.PLAYWRIGHT_CHROMIUM }
  : {};

/* ------------------------------------------------------ running the app */

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function waitFor(url, timeoutMs, server) {
  const until = Date.now() + timeoutMs;
  while (Date.now() < until) {
    if (server?.exitCode != null) throw new Error(`the server exited (${server.exitCode}) before answering`);
    try {
      const res = await fetch(url, { redirect: "manual" });
      if (res.status < 500) return;
    } catch {
      /* not up yet */
    }
    await sleep(1000);
  }
  throw new Error(`${url} never answered`);
}

/** What installs dependencies at a checkout, from its lockfile. */
function detectInstall(root) {
  if (existsSync(join(root, "pnpm-lock.yaml"))) return "pnpm install --frozen-lockfile";
  // npm-deployed repos keep their lockfile; pnpm imports it and links from the shared store.
  if (existsSync(join(root, "package-lock.json")))
    return "pnpm import && pnpm install --config.node-linker=hoisted";
  if (existsSync(join(root, "yarn.lock"))) return "yarn install --frozen-lockfile";
  if (existsSync(join(root, "bun.lockb")) || existsSync(join(root, "bun.lock"))) return "bun install";
  if (existsSync(join(root, "package.json"))) return "pnpm install";
  return null;
}

/** What starts the dev server, from the app's package.json. */
function detectStart(appDir) {
  const pkgFile = join(appDir, "package.json");
  if (!existsSync(pkgFile)) {
    throw new Error(`no package.json in ${appDir}: set app.start in the config`);
  }
  const scripts = JSON.parse(readFileSync(pkgFile, "utf8")).scripts ?? {};
  const script = ["dev", "start", "serve"].find((s) => scripts[s]);
  if (!script) throw new Error(`no dev/start script in ${pkgFile}: set app.start in the config`);
  return `pnpm run ${script} --port {port}`;
}

function kill(child) {
  if (!child || child.exitCode != null) return;
  try {
    if (WIN) execFileSync("taskkill", ["/pid", String(child.pid), "/T", "/F"], { stdio: "ignore" });
    else process.kill(-child.pid, "SIGTERM");
  } catch {
    /* already gone */
  }
}

/** One side made servable: a URL as given, or a ref checked out and started. */
async function bringUp(side, label, port) {
  if (side.url) return { base: side.url.replace(/\/$/, ""), what: side.url, down: async () => {} };

  const app = cfg.app ?? {};
  let root = REPO;
  let worktree = null;
  let what;
  if (side.worktree) {
    what = `the working tree on ${git(REPO, "log", "-1", "--format=%h %s")}`;
  } else {
    if (!side.ref) throw new Error(`${label} needs url, ref or worktree`);
    const sha = git(REPO, "rev-parse", "--verify", `${side.ref}^{commit}`);
    what = `${side.ref} (${git(REPO, "log", "-1", "--format=%h %s", sha)})`;
    worktree = join(tmpdir(), "before-after-wt", `${name}-${label}-${sha.slice(0, 8)}`);
    if (!existsSync(worktree)) {
      console.log(`  ${label}: worktree at ${sha.slice(0, 8)}`);
      git(REPO, "-c", "core.longpaths=true", "worktree", "add", "--detach", worktree, sha);
    }
    root = worktree;
    // Untracked files the app needs (an env file); copied, never linked.
    for (const f of app.copy ?? []) {
      const from = join(REPO, f);
      if (!existsSync(from)) throw new Error(`app.copy: ${f} does not exist in ${REPO}`);
      mkdirSync(dirname(join(root, f)), { recursive: true });
      copyFileSync(from, join(root, f));
    }
    const install = app.install === undefined ? detectInstall(root) : app.install;
    if (install) {
      console.log(`  ${label}: ${install}`);
      sh(install, root);
    }
  }

  const appDir = join(root, app.cwd ?? ".");
  const start = (app.start ?? detectStart(appDir)).replaceAll("{port}", String(port));
  const env = { ...readEnvFile(app.envFile), ...(app.env ?? {}), PORT: String(port) };
  // {root} is the checkout this side runs from, with forward slashes so it survives NODE_OPTIONS.
  for (const [k, v] of Object.entries(env)) env[k] = String(v).replaceAll("{root}", root.replaceAll("\\", "/"));
  console.log(`  ${label}: ${start} (port ${port})`);
  const server = spawn(start, {
    cwd: appDir,
    env: { ...process.env, ...env },
    shell: true,
    detached: !WIN,
    stdio: ["ignore", "pipe", "pipe"],
  });
  const log = [];
  const keepLog = (d) => {
    log.push(String(d));
    if (log.length > 200) log.shift();
  };
  server.stdout.on("data", keepLog);
  server.stderr.on("data", keepLog);
  const base = `http://localhost:${port}`;
  try {
    await waitFor(`${base}${app.ready ?? "/"}`, app.timeoutMs ?? 180_000, server);
  } catch (e) {
    kill(server);
    console.error(log.join("").slice(-3000));
    throw e;
  }
  return {
    base,
    what,
    down: async () => {
      kill(server);
      await sleep(1500);
      if (worktree && !keep) {
        // node_modules paths outrun Windows' 260 characters; git refuses them without longpaths.
        try {
          git(REPO, "-c", "core.longpaths=true", "worktree", "remove", "--force", worktree);
        } catch {
          rmSync(worktree, { recursive: true, force: true, maxRetries: 3 });
          git(REPO, "worktree", "prune");
        }
        // git can deregister it and still leave files a just-killed server held open.
        if (existsSync(worktree)) rmSync(worktree, { recursive: true, force: true, maxRetries: 5, retryDelay: 1000 });
      }
    },
  };
}

/** KEY=value lines, for an env file the config points at. */
function readEnvFile(file) {
  if (!file) return {};
  const out = {};
  for (const line of readFileSync(resolve(dirname(configFile), file), "utf8").split(/\r?\n/)) {
    const m = line.match(/^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)=(.*)$/);
    if (m) out[m[1]] = m[2].replace(/^(['"])(.*)\1$/, "$2");
  }
  return out;
}

/* -------------------------------------------------------------- signing in */

/**
 * Cookies for a pass. `auth.command` is run for every pass and prints JSON:
 * a cookie array, one cookie, or { cookieName, cookieValue }.
 */
function cookiesFor(base) {
  const auth = cfg.auth;
  if (!auth) return [];
  let raw = auth.cookies ?? [];
  if (auth.command) {
    const printed = execSync(auth.command, { cwd: REPO, encoding: "utf8" });
    const got = JSON.parse(printed.slice(printed.search(/[[{]/)));
    raw = Array.isArray(got)
      ? got
      : got.cookieName
        ? [{ name: got.cookieName, value: got.cookieValue }]
        : [got];
  }
  const host = new URL(base).hostname;
  return raw.map((c) => ({ path: "/", sameSite: "Lax", ...c, domain: c.domain ?? host }));
}

/* ------------------------------------------------------------------ a pass */

const HIDE_DEV = `nextjs-portal, vite-error-overlay, astro-dev-toolbar, #__next-build-watcher,
  [data-nextjs-toast], [data-nextjs-dev-tools-button] { display: none !important; }`;

async function shoot(label, server) {
  if (typeof cfg.reset === "function") await cfg.reset({ label });
  else if (cfg.reset) sh(cfg.reset, REPO);

  const browser = await chromium.launch(launchOptions);
  const failed = [];
  try {
    for (const vp of viewports) {
      const { name: vpName, ...size } = vp;
      const { width, height, ...device } = size;
      const ctx = await browser.newContext({
        viewport: { width, height },
        ...device,
        ...(cfg.auth?.storageState ? { storageState: resolve(REPO, cfg.auth.storageState) } : {}),
      });
      const cookies = cookiesFor(server.base);
      if (cookies.length) await ctx.addCookies(cookies);
      const page = await ctx.newPage();
      for (const shot of cfg.shots) {
        if (shot.only && shot.only !== label) continue;
        if (shot.viewports && !shot.viewports.includes(vpName)) continue;
        const file = join(OUT, "shots", `${label}-${vpName}-${shot.id}.png`);
        try {
          if (shot.path !== undefined) {
            await page.goto(`${server.base}${shot.path}`, { waitUntil: "load", timeout: 90_000 });
            await page.waitForLoadState("networkidle", { timeout: 8000 }).catch(() => {});
          }
          if (cfg.hideDevOverlays !== false) await page.addStyleTag({ content: HIDE_DEV }).catch(() => {});
          if (cfg.prepare) await cfg.prepare(page, { label, viewport: vpName });
          if (shot.act) await shot.act(page, { label, viewport: vpName });
          await page.waitForTimeout(shot.settle ?? 1200);
          await page.screenshot({ path: file, fullPage: Boolean(shot.fullPage) });
          console.log(`  ${label} ${vpName}: ${shot.id}`);
        } catch (e) {
          const why = String(e).split("\n")[0];
          failed.push({ id: `${label} ${vpName} ${shot.id}`, why });
          console.error(`  ${label} ${vpName}: ${shot.id} FAILED: ${why}`);
          await page.screenshot({ path: file }).catch(() => {});
        }
      }
      await ctx.close();
    }
  } finally {
    await browser.close();
  }
  return failed;
}

/* ----------------------------------------------------------------- the page */

const esc = (s) =>
  String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);

function report(taken, failed) {
  const sections = [];
  for (const shot of cfg.shots) {
    for (const vp of viewports) {
      if (shot.viewports && !shot.viewports.includes(vp.name)) continue;
      const img = (label) => `shots/${label}-${vp.name}-${esc(shot.id)}.png`;
      const has = (label) => existsSync(join(OUT, img(label)));
      const fig = (label, tag, words) => `
      <figure><figcaption><span class="tag ${tag}">${tag}</span> ${esc(words)}</figcaption>
        ${has(label) ? `<img src="${img(label)}" alt="">` : `<div class="missing">Not captured</div>`}</figure>`;
      const body =
        shot.only === "after"
          ? `<div class="pair solo">${fig("after", "new", shot.afterWords ?? "Nothing here before.")}</div>`
          : shot.only === "before"
            ? `<div class="pair solo">${fig("before", "gone", shot.beforeWords ?? "What it replaced.")}</div>`
            : `<div class="pair">${fig("before", "before", shot.beforeWords ?? "")}${fig("after", "after", shot.afterWords ?? "")}</div>`;
      sections.push(`<section class="screen ${vp.isMobile ? "phone" : "wide"}" data-file="${esc(vp.name)}-${esc(shot.id)}">
  <h2>${esc(shot.say ?? shot.id)} <span class="vp">${esc(vp.name)} · ${vp.width}px</span></h2>${body}
</section>`);
    }
  }
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><title>${esc(cfg.title ?? name)}</title>
<style>
  @page { size: A4 landscape; margin: 10mm; }
  * { box-sizing: border-box; }
  body { font: 13px/1.5 ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif; color: #1a1a1a; margin: 0; padding: 0 4px; background: #fff; }
  header { margin-bottom: 8px; }
  h1 { font-size: 24px; margin: 0 0 4px; letter-spacing: -0.02em; }
  .lede { color: #444; max-width: 110ch; margin: 0 0 4px; }
  .meta { color: #777; font-size: 12px; margin: 0; }
  .fail { color: #9b1c1c; font-size: 12px; }
  .screen { break-before: page; page-break-before: always; padding: 6px 0 10px; background: #fff; }
  header + .screen { break-before: auto; page-break-before: auto; }
  h2 { font-size: 17px; margin: 0 0 8px; }
  .vp { color: #888; font-weight: 500; font-size: 12px; margin-left: 6px; }
  .pair { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; break-inside: avoid; }
  .phone .pair { grid-template-columns: repeat(2, minmax(0, 250px)); justify-content: center; gap: 40px; }
  .pair.solo { grid-template-columns: minmax(0, 66%); }
  .phone .pair.solo { grid-template-columns: minmax(0, 250px); }
  figure { margin: 0; }
  figcaption { margin: 0 0 6px; min-height: 20px; }
  .phone figcaption { min-height: 64px; }
  .tag { font-size: 10px; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; padding: 3px 9px; border-radius: 999px; }
  .before, .gone { background: #fdecec; color: #9b1c1c; }
  .after { background: #e8f5ec; color: #14532d; }
  .new { background: #eef1ff; color: #1e2a78; }
  img { width: 100%; display: block; border: 1px solid #ddd; border-radius: 6px; }
  .missing { border: 1px dashed #c99; border-radius: 6px; padding: 40px; text-align: center; color: #9b1c1c; }
</style></head><body>
<header>
  <h1>${esc(cfg.title ?? name)}</h1>
  ${cfg.lede ? `<p class="lede">${esc(cfg.lede)}</p>` : ""}
  <p class="meta">Before: ${esc(taken.before)}. After: ${esc(taken.after)}.</p>
  ${failed.length ? `<p class="fail">${failed.length} shot(s) did not come out: ${failed.map((f) => esc(`${f.id} (${f.why})`)).join("; ")}</p>` : ""}
</header>
${sections.join("\n")}
</body></html>`;
}

/* -------------------------------------------------------------------- run */

console.log(`before-after: ${cfg.title ?? name}\n  out: ${OUT}`);
const taken = {};
let failed = [];
for (const [label, port] of [
  ["before", cfg.app?.ports?.[0] ?? 3101],
  ["after", cfg.app?.ports?.[1] ?? 3102],
]) {
  const server = await bringUp(cfg[label], label, port);
  taken[label] = server.what;
  try {
    failed = failed.concat(await shoot(label, server));
  } finally {
    await server.down();
  }
}

const html = join(OUT, "index.html");
writeFileSync(html, report(taken, failed));

const browser = await chromium.launch(launchOptions);
try {
  const page = await browser.newPage({ viewport: { width: 1400, height: 900 } });
  await page.goto(pathToFileURL(html).href, { waitUntil: "load" });
  // One PNG per screen, the pair and its caption, for pasting into a chat.
  for (const el of await page.locator("section.screen").all()) {
    const file = await el.getAttribute("data-file");
    await el.screenshot({ path: join(OUT, "pairs", `${file}.png`) });
  }
  await page.pdf({ path: join(OUT, `${name}.pdf`), format: "A4", landscape: true, printBackground: true });
} finally {
  await browser.close();
}

console.log(`\n  ${join(OUT, `${name}.pdf`)}\n  ${html}\n  ${join(OUT, "pairs")}\n  ${join(OUT, "shots")}`);
if (failed.length) {
  console.error(`\n${failed.length} shot(s) did not come out:`);
  for (const f of failed) console.error(`  ${f.id}: ${f.why}`);
  process.exit(1);
}
