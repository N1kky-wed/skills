/**
 * A worked config: 8x business (8xsocial/8x-linkedin) PR 283, "saved topics
 * show as picked, not left in the box", photographed on the local stack.
 *
 *   cd <8x-linkedin checkout>
 *   node ~/.claude/skills/before-after/scripts/before-after.mjs \
 *     ~/.claude/skills/before-after/examples/8x-linkedin-local-stack.mjs
 *
 * What makes 8x different from a plain web app, and how this file handles it:
 * - Its env file names the real project, so the app is started with the local
 *   stack's block in front of it (the one apps/web/scripts/local-stack/up.sh
 *   prints), keys minted here against the harness secret. Postgres, PostgREST
 *   and the gateway must already be up (54422, 54423, 54421).
 * - Nothing to sign in against: a session is minted for a seeded account and
 *   planted as the cookie @supabase/ssr reads.
 * - The flow writes, so `reset` puts the account back before each pass.
 */
import { execFileSync } from "node:child_process";
import { createRequire } from "node:module";
import { resolve } from "node:path";

const MINT = "apps/web/scripts/local-stack/mint.mjs";
const mint = (sub, email, role) =>
  JSON.parse(execFileSync("node", [MINT, sub, email, role], { encoding: "utf8" })).access_token;

const DB = "postgres://postgres:postgres@127.0.0.1:54422/postgres"; // not-a-secret: the local stack
const USER = { id: "d95268d2-0065-4656-81ef-3730c0335c87", email: "maya.mvff5vou@gmail.com" };
const STANDIN = "stands-in-for-the-key-the-mock-answers-for";

export default {
  name: "8x-pr283-saved-topics",
  title: "Saved topics show as picked",
  lede: "8x business PR 283. Team Desk, Profile > Settings: type two topics into the box and save.",

  before: { ref: "45e002fb^" },
  after: { ref: "45e002fb" },

  app: {
    cwd: "apps/web",
    copy: ["apps/web/.env.local"],
    start: "pnpm exec next dev --port {port}",
    ready: "/login",
    env: {
      DATABASE_URL: DB,
      MCP_READER_DATABASE_URL: DB,
      LI_SUPABASE_URL: "http://127.0.0.1:9",
      LI_SUPABASE_SECRET_KEY: STANDIN,
      PAYOUT_GATEWAY_URL: "http://127.0.0.1:9",
      PAYOUT_GATEWAY_API_KEY: STANDIN,
      SLACK_BOT_TOKEN_2: "xox" + "b-not-a-secret-local-stand-in",
      XAI_API_KEY: STANDIN,
      VOYAGE_API_KEY: STANDIN,
      PRODUCTHUNT_CLIENT_SECRET: STANDIN,
      NEXT_PUBLIC_POSTHOG_KEY: STANDIN,
      NEXT_PUBLIC_SUPABASE_URL: "http://127.0.0.1:54421",
      NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY: mint("00000000-0000-4000-8000-0000000000a0", "anon@local", "anon"),
      SUPABASE_SECRET_KEY: mint("00000000-0000-4000-8000-0000000000b0", "service@local", "service_role"),
      SUPABASE_JWT_SECRET: "super-secret-jwt-token-with-at-least-32-characters-long", // not-a-secret: harness
      STRIPE_SECRET_KEY: STANDIN,
      RESEND_API_KEY: STANDIN,
      GEMINI_API_KEY: STANDIN,
      RAPIDAPI_KEY: STANDIN,
      RAPIDAPI_LINKEDIN_HOST: "linkedin-api.local.test",
      SLACK_BOT_TOKEN: "xox" + "b-not-a-secret-local-stand-in",
      SLACK_CHANNEL_APPLICATIONS: "C0LOCALAPPLICATIONS",
      SLACK_CHANNEL_SIGNUPS: "C0LOCALSIGNUPS",
      SLACK_CHANNEL_ALERTS: "C0LOCALALERTS",
      STRIPE_WEBHOOK_SECRET: STANDIN,
      EMAIL_FROM: "8x@local.test",
      MOCK_INTEGRATIONS: "1",
      NODE_OPTIONS: "--require {root}/apps/web/scripts/local-stack/mock-integrations.cjs",
    },
  },

  auth: { command: `node ${MINT} ${USER.id} ${USER.email} authenticated` },

  // The save writes, so each pass starts from an account with nothing answered.
  reset: async () => {
    const pg = createRequire(resolve("apps/web/package.json"))("pg");
    const db = new pg.Client({ connectionString: DB });
    await db.connect();
    await db.query(
      "update company_employees set topics = '{}', audience = null, voice = null where user_id = $1",
      [USER.id],
    );
    await db.end();
  },

  shots: [
    {
      id: "profile-topics",
      path: "/employee/app/profile?tab=settings",
      say: "Profile settings, right after saving two typed topics",
      beforeWords: "Saved, but the typed topics are still sitting in the box.",
      afterWords: "The topics move into the picked chips and the box is empty.",
      act: async (page) => {
        const box = page.getByPlaceholder("Add your own, separated by commas");
        await box.scrollIntoViewIfNeeded();
        await box.fill("climate tech, B2B sales");
        await page.getByRole("button", { name: "Save my answers" }).click();
        await page.getByText("Saved. Every draft leans on these now.").waitFor({ timeout: 30_000 });
        await page.getByText("What do you want to be known for?").scrollIntoViewIfNeeded();
      },
    },
  ],
};
