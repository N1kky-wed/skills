"""End-to-end tests with a fake `claude`, a local bare git remote and a fake
`gh`. No Slack, no network, no cost.

    .venv/bin/python -m unittest discover -s tests -v
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
TMP = Path(tempfile.mkdtemp(prefix="botdemo-"))
REMOTE, REPO, BIN = TMP / "remote.git", TMP / "repo", TMP / "fakebin"

# Settings must exist before `bot` is imported: config is read at import time.
os.environ.update({
    "BOT_ROOT": str(TMP), "SLACK_BOT_TOKEN": "", "SLACK_APP_TOKEN": "xapp-test",
    "BOT_CHANNEL_ID": "C1", "BOT_USER_ID": "UBOT", "OWNER_USER_ID": "UOWNER",
    "WRITE_ALLOWED_USER_IDS": "UOWNER", "REPO_SLUG": "acme/demo", "REPO_PATH": str(REPO),
    "CLAUDE_BIN": str(BIN / "claude"), "BOT_OPEN_ISSUES": "false", "BOT_FORCE_PR": "false",
    "READ_ENV_KEYS": "DB_READ_URL", "WRITE_ENV_KEYS": "DB_WRITE_URL",
    "DB_READ_URL": "postgres://read", "DB_WRITE_URL": "postgres://write", "DB_OTHER_SECRET": "x",
    "PROGRESS_INTERVAL_SECONDS": "1", "ADDRESS_AS": '{"UFRIEND": "boss"}',
})
os.environ["PATH"] = f"{BIN}:{os.environ['PATH']}"
sys.path.insert(0, str(HERE.parent))

from bot import agents, config, followups, phrases, pipeline, slack_io, state  # noqa: E402
import app  # noqa: E402

POSTS: list[tuple] = []
UPLOADS: list[str] = []


def sh(*a, cwd=None):
    return subprocess.run(a, cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def setUpModule():
    BIN.mkdir()
    shutil.copy(HERE / "fake_claude.py", BIN / "claude")
    (BIN / "claude").chmod(0o755)
    (BIN / "gh").write_text("#!/bin/sh\ncase \"$*\" in *'pr create'*) echo https://github.com/acme/demo/pull/7;; "
                            "*) exit 1;; esac\n")
    (BIN / "gh").chmod(0o755)
    sh("git", "init", "-q", "--bare", "-b", "main", str(REMOTE))
    sh("git", "clone", "-q", str(REMOTE), str(REPO))
    sh("git", "config", "user.email", "bot@example.com", cwd=REPO)
    sh("git", "config", "user.name", "bot", cwd=REPO)
    (REPO / "README.md").write_text("demo\n")
    sh("git", "add", ".", cwd=REPO)
    sh("git", "commit", "-qm", "init", cwd=REPO)
    sh("git", "push", "-q", "origin", "main", cwd=REPO)
    # A pre-push hook that rejects a file called bad.txt, like a repo's lint gate.
    hook = REPO / ".git" / "hooks" / "pre-push"
    hook.write_text("#!/bin/sh\nif git ls-tree -r --name-only HEAD | grep -qx bad.txt; then "
                    "echo 'lint: bad.txt is not allowed' >&2; exit 1; fi\n")
    hook.chmod(0o755)
    slack_io.post = lambda thread, text, rid=None: POSTS.append((thread, text)) or "1.0"
    slack_io.upload = lambda thread, path: UPLOADS.append(path) or True
    slack_io.read_thread = lambda ts, limit=80: []
    slack_io.permalink = lambda ts: None


def tearDownModule():
    shutil.rmtree(TMP, ignore_errors=True)


def scenario(**kw):
    (BIN / "scenario.json").write_text(json.dumps(kw))


TRIAGE_CODE = {"request_kind": "actionable", "task_type": "feature", "priority": "normal",
               "message": "on it, adding hello.txt", "resolved_request": "add a hello.txt file"}
PLAN = {"classification": {"task_type": "feature", "scope": "small", "risk": "low",
                           "priority": "normal", "confidence": 0.9, "execution_mode": "DIRECT_PUSH"},
        "plan": ["add hello.txt"], "blockers": []}


class Pipeline(unittest.TestCase):
    def setUp(self):
        POSTS.clear()
        UPLOADS.clear()
        self.store = state.Store(TMP / f"state-{self.id()}.db")

    def run_request(self, user, text="<@UBOT> do it", ts=None):
        ts = ts or f"{time.time():.6f}"
        rid = f"C1-{ts}"
        self.assertTrue(self.store.claim(rid, channel_id="C1", message_ts=ts, user_id=user,
                                         request_text=text))
        pipeline.process({"request_id": rid, "slack": {"channel_id": "C1", "message_ts": ts,
                          "thread_ts": None, "user_id": user, "message": text, "files": []}},
                         self.store)
        return self.store.get(rid)

    def texts(self):
        return "\n".join(t for _, t in POSTS)

    def test_owner_direct_push_lands_on_main(self):
        scenario(triage=TRIAGE_CODE, plan=PLAN, impl="commit")
        row = self.run_request("UOWNER")
        self.assertEqual(row["status"], state.PUSHED, self.texts())
        sh("git", "fetch", "-q", cwd=REPO)
        self.assertIn("hello.txt", sh("git", "ls-tree", "-r", "--name-only", "origin/main", cwd=REPO))
        self.assertIn("pushed", self.texts())
        self.assertFalse(list(config.WORK_ROOT.iterdir()), "worktree not cleaned up")
        sh("git", "reset", "-q", "--hard", "origin/main", cwd=REPO)

    def test_non_writer_gets_a_pr_never_a_push(self):
        before = sh("git", "rev-parse", "origin/main", cwd=REPO)
        scenario(triage=TRIAGE_CODE, plan=PLAN, impl="commit")
        row = self.run_request("USOMEONE")
        self.assertEqual(row["status"], state.PR_CREATED, self.texts())
        self.assertEqual(row["pull_request_url"], "https://github.com/acme/demo/pull/7")
        sh("git", "fetch", "-q", cwd=REPO)
        self.assertEqual(before, sh("git", "rev-parse", "origin/main", cwd=REPO))

    def test_push_hook_rejection_is_fixed_by_resuming_the_agent(self):
        scenario(triage=TRIAGE_CODE, plan=PLAN, impl="bad_then_fix")
        row = self.run_request("UOWNER")
        self.assertEqual(row["status"], state.PUSHED, self.texts())
        self.assertIn("push hook flagged", self.texts())
        calls = (BIN / "calls.log").read_text()
        self.assertIn('"--resume", "s1"', calls)
        sh("git", "fetch", "-q", cwd=REPO)
        self.assertNotIn("bad.txt", sh("git", "ls-tree", "-r", "--name-only", "origin/main", cwd=REPO))
        sh("git", "reset", "-q", "--hard", "origin/main", cwd=REPO)

    def test_claimed_success_without_a_commit_fails(self):
        scenario(triage=TRIAGE_CODE, plan=PLAN, impl="nothing")
        row = self.run_request("UOWNER")
        self.assertEqual(row["status"], state.FAILED)
        self.assertIn("no commit", self.texts())

    def test_lookup_answers_attaches_and_sees_only_read_creds(self):
        scenario(triage={"request_kind": "actionable", "task_type": "lookup",
                         "message": "checking", "resolved_request": "count rows"}, impl="file")
        row = self.run_request("USOMEONE")
        self.assertEqual(row["status"], state.COMPLETED, self.texts())
        self.assertIn("42 rows", self.texts())
        self.assertIn("env=DB_READ_URL", self.texts())   # not the write url, not other secrets
        self.assertTrue(UPLOADS and UPLOADS[0].endswith("report.csv"))

    def test_action_by_owner_gets_write_creds(self):
        scenario(triage={"request_kind": "actionable", "task_type": "action",
                         "message": "fixing it", "resolved_request": "fix the row"}, impl="file")
        self.run_request("UOWNER")
        self.assertIn("env=DB_READ_URL,DB_WRITE_URL", self.texts())

    def test_action_by_non_writer_is_refused_without_running(self):
        scenario(triage={"request_kind": "actionable", "task_type": "action",
                         "message": "ok", "resolved_request": "delete user 5"}, impl="file")
        row = self.run_request("USOMEONE")
        self.assertEqual(row["status"], state.COMPLETED)
        self.assertIn("<@UOWNER>", self.texts())
        self.assertFalse(UPLOADS)

    def test_unclear_waits_for_a_reply(self):
        scenario(triage={"request_kind": "unclear", "message": "which page?"})
        row = self.run_request("USOMEONE")
        self.assertEqual(row["status"], state.AWAITING_REPLY)
        self.assertEqual(POSTS[-1][1], "which page?")

    def test_answered_in_triage_runs_nothing_else(self):
        scenario(triage={"request_kind": "answered", "message": "12 users signed up today"})
        row = self.run_request("USOMEONE")
        self.assertEqual(row["status"], state.COMPLETED)
        self.assertEqual(len(POSTS), 1)

    def test_blocked_plan(self):
        scenario(triage=TRIAGE_CODE, plan={**PLAN, "blockers": ["needs a decision on the API shape"]})
        row = self.run_request("UOWNER")
        self.assertEqual(row["status"], state.BLOCKED)
        self.assertIn("couldn't do this one", self.texts())

    def test_stop_marks_cancelled_and_stays_quiet(self):
        import threading
        scenario(triage={"request_kind": "actionable", "task_type": "lookup",
                         "message": "checking", "resolved_request": "slow"}, impl="sleep")
        ts = f"{time.time():.6f}"
        rid = f"C1-{ts}"
        t = threading.Thread(target=self.run_request, args=("UOWNER", "<@UBOT> slow", ts))
        t.start()
        for _ in range(100):
            row = self.store.get(rid)
            if row and row.get("pid"):
                break
            time.sleep(0.1)
        import botctl
        botctl.store = self.store
        botctl.stop(rid)
        t.join(30)
        self.assertEqual(self.store.status(rid), state.CANCELLED)
        self.assertNotIn("failed", self.texts())
        self.assertIn("stopped this one", self.texts())

    def test_restart_recovery_tells_the_thread(self):
        self.store.claim("C1-9.9", channel_id="C1", message_ts="9.9", user_id="U")
        self.store.update("C1-9.9", status=state.EXECUTING)
        pipeline.recover(self.store)
        self.assertEqual(self.store.status("C1-9.9"), state.FAILED)
        self.assertIn("restarted", self.texts())


class Listener(unittest.TestCase):
    def setUp(self):
        POSTS.clear()
        app.store = self.store = state.Store(TMP / f"l-{self.id()}.db")
        self.queued = []
        app.work.put = self.queued.append

    def ev(self, **kw):
        return {"channel": "C1", "user": "UA", "ts": f"{time.time():.6f}", "text": "<@UBOT> hi there x", **kw}

    def test_filters(self):
        self.assertFalse(app.is_for_bot(self.ev(channel="C2")))
        self.assertFalse(app.is_for_bot(self.ev(bot_id="B1")))
        self.assertFalse(app.is_for_bot(self.ev(subtype="message_changed")))
        self.assertFalse(app.is_for_bot(self.ev(text="no tag")))
        self.assertTrue(app.is_for_bot(self.ev()))
        self.assertTrue(app.is_for_bot(self.ev(subtype="file_share")))

    def test_duplicate_delivery_runs_once(self):
        e = self.ev(text="<@UBOT> fix the login page")
        app.handle(e)
        app.handle(e)
        self.assertEqual(len(self.queued), 1)

    def test_greeting_is_answered_without_a_model(self):
        app.handle(self.ev(text="<@UBOT> thanks!"))
        self.assertFalse(self.queued)
        self.assertEqual(len(POSTS), 1)

    def test_nickname(self):
        app.handle(self.ev(text="<@UBOT> hey", user="UFRIEND"))
        self.assertTrue(POSTS[-1][1].endswith(", boss"))

    def test_message_in_a_running_thread_becomes_a_followup(self):
        first = self.ev(text="<@UBOT> pull 30 rows")
        app.handle(first)
        rid = f"C1-{first['ts']}"
        self.store.update(rid, status=state.EXECUTING)
        wt = followups.worktree_for(rid)
        wt.mkdir(parents=True)
        app.handle(self.ev(text="make it 50", thread_ts=first["ts"]))   # untagged, same person
        self.assertEqual(len(self.queued), 1)
        self.assertEqual(len(self.store.followups(rid)), 1)
        self.assertIn("make it 50", (wt / ".bot" / "followups.md").read_text())
        shutil.rmtree(wt)

    def test_untagged_reply_from_someone_else_is_ignored(self):
        first = self.ev(text="<@UBOT> pull 30 rows")
        app.handle(first)
        self.assertFalse(app.is_for_bot(self.ev(text="lol", user="UB", thread_ts=first["ts"])))


class Units(unittest.TestCase):
    def test_find_json_takes_the_report_not_a_later_object(self):
        text = 'thinking {"x": 1}\n```json\n{"status": "success", "summary": "a {b}"}\n```\ndone'
        self.assertEqual(agents.find_json(text, "status")["summary"], "a {b}")
        self.assertIsNone(agents.find_json("no json here", "status"))

    def test_chunks_keep_everything(self):
        text = "\n\n".join("para %d " % i + "x" * 900 for i in range(10))
        parts = slack_io.chunks(text, 3900)
        self.assertTrue(all(len(p) <= 3900 for p in parts))
        self.assertEqual("".join(parts).replace("\n", ""), text.replace("\n", ""))

    def test_social(self):
        self.assertIsNotNone(phrases.social_reply("thanks!"))
        self.assertIsNotNone(phrases.social_reply("hey how are you"))
        self.assertIsNone(phrases.social_reply("thanks, now fix the bug"))

    def test_scoped_env_never_leaks_unlisted_secrets(self):
        env = config.implementer_env(writes_allowed=False)
        self.assertIn("DB_READ_URL", env)
        self.assertNotIn("DB_WRITE_URL", env)
        self.assertNotIn("DB_OTHER_SECRET", env)
        self.assertNotIn("SLACK_APP_TOKEN", env)

    def test_implementer_can_never_push(self):
        self.assertIn("Bash(git push:*)", config.IMPLEMENTER_DENY)
        self.assertIn("Write", config.READ_ONLY_DENY)


if __name__ == "__main__":
    unittest.main()
