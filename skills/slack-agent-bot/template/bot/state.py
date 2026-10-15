"""Durable request state in SQLite.

One row per Slack message, keyed by `<channel>-<ts>`, so a re-delivered event
or a replay can never start a second execution: `claim()` is an INSERT, and
whoever wins it owns the work.
"""

import json
import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

RECEIVED = "RECEIVED"
TRIAGING = "TRIAGING"
PLANNED = "PLANNED"
EXECUTING = "EXECUTING"
PUSHED = "PUSHED"
PR_CREATED = "PR_CREATED"
COMPLETED = "COMPLETED"
AWAITING_REPLY = "AWAITING_REPLY"   # the bot asked something and is waiting
ATTACHED = "ATTACHED"               # folded into a job already running in the thread
FAILED = "FAILED"
BLOCKED = "BLOCKED"
CANCELLED = "CANCELLED"             # stopped by an operator (botctl stop)

IN_FLIGHT = {RECEIVED, TRIAGING, PLANNED, EXECUTING}

SCHEMA = """
CREATE TABLE IF NOT EXISTS requests (
    request_id       TEXT PRIMARY KEY,
    channel_id       TEXT NOT NULL,
    message_ts       TEXT NOT NULL,
    thread_ts        TEXT,
    user_id          TEXT,
    request_text     TEXT,
    permalink        TEXT,
    status           TEXT NOT NULL,
    triage_result    TEXT,
    plan_result      TEXT,
    run_result       TEXT,
    commit_sha       TEXT,
    branch           TEXT,
    pull_request_url TEXT,
    issue_url        TEXT,
    pid              INTEGER,
    error            TEXT,
    created_at       TEXT NOT NULL,
    updated_at       TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_requests_status ON requests(status);
CREATE INDEX IF NOT EXISTS idx_requests_thread ON requests(thread_ts);

CREATE TABLE IF NOT EXISTS followups (
    request_id TEXT NOT NULL,
    message_ts TEXT NOT NULL,
    user_id    TEXT,
    text       TEXT,
    created_at TEXT NOT NULL,
    PRIMARY KEY (request_id, message_ts)
);

-- Every message the bot posted, so an operator can delete a job's replies.
CREATE TABLE IF NOT EXISTS posts (
    request_id TEXT,
    thread_ts  TEXT,
    ts         TEXT PRIMARY KEY,
    created_at TEXT NOT NULL
);
"""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Store:
    def __init__(self, path: Path):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(path, check_same_thread=False, timeout=30)
        self._conn.row_factory = sqlite3.Row
        with self._lock:
            self._conn.executescript(SCHEMA)
            self._conn.commit()

    def _rows(self, sql: str, params: tuple = ()) -> list[dict]:
        with self._lock:
            return [dict(r) for r in self._conn.execute(sql, params).fetchall()]

    def _exec(self, sql: str, params: Any = ()) -> None:
        with self._lock:
            self._conn.execute(sql, params)
            self._conn.commit()

    # ── requests ────────────────────────────────────────────────────────────
    def claim(self, request_id: str, **fields: Any) -> bool:
        """True if this caller now owns the request; False if it existed."""
        now = _now()
        row = {"request_id": request_id, "status": RECEIVED,
               "created_at": now, "updated_at": now, **fields}
        cols = ", ".join(row)
        marks = ", ".join(f":{k}" for k in row)
        try:
            self._exec(f"INSERT INTO requests ({cols}) VALUES ({marks})", row)
            return True
        except sqlite3.IntegrityError:
            return False

    def update(self, request_id: str, **fields: Any) -> None:
        if not fields:
            return
        enc = {k: json.dumps(v) if isinstance(v, (dict, list)) else v
               for k, v in fields.items()}
        enc["updated_at"] = _now()
        sets = ", ".join(f"{k} = :{k}" for k in enc)
        self._exec(f"UPDATE requests SET {sets} WHERE request_id = :request_id",
                   {**enc, "request_id": request_id})

    def get(self, request_id: str) -> Optional[dict]:
        rows = self._rows("SELECT * FROM requests WHERE request_id = ?", (request_id,))
        return rows[0] if rows else None

    def delete(self, request_id: str) -> None:
        self._exec("DELETE FROM requests WHERE request_id = ?", (request_id,))

    def status(self, request_id: str) -> Optional[str]:
        row = self.get(request_id)
        return row["status"] if row else None

    def thread_history(self, thread_ts: str) -> list[dict]:
        return self._rows("SELECT * FROM requests WHERE thread_ts = ? OR message_ts = ? "
                          "ORDER BY created_at", (thread_ts, thread_ts))

    def inflight_in_thread(self, thread_ts: str, exclude_id: str) -> Optional[dict]:
        marks = ", ".join("?" for _ in IN_FLIGHT)
        rows = self._rows(
            "SELECT * FROM requests WHERE (thread_ts = ? OR message_ts = ?) "
            f"AND request_id != ? AND status IN ({marks}) ORDER BY created_at DESC LIMIT 1",
            (thread_ts, thread_ts, exclude_id, *IN_FLIGHT))
        return rows[0] if rows else None

    def inflight(self) -> list[dict]:
        marks = ", ".join("?" for _ in IN_FLIGHT)
        return self._rows(f"SELECT * FROM requests WHERE status IN ({marks})", tuple(IN_FLIGHT))

    def recent(self, limit: int = 20) -> list[dict]:
        return self._rows("SELECT * FROM requests ORDER BY created_at DESC LIMIT ?", (limit,))

    def search(self, keyword: str, limit: int = 15) -> list[dict]:
        like = f"%{keyword}%"
        return self._rows("SELECT * FROM requests WHERE request_text LIKE ? OR run_result LIKE ? "
                          "ORDER BY created_at DESC LIMIT ?", (like, like, limit))

    # ── follow-ups ──────────────────────────────────────────────────────────
    def add_followup(self, request_id: str, message_ts: str, user_id: Optional[str], text: str) -> None:
        self._exec("INSERT OR IGNORE INTO followups VALUES (?, ?, ?, ?, ?)",
                   (request_id, message_ts, user_id, text, _now()))

    def followups(self, request_id: str) -> list[dict]:
        return self._rows("SELECT * FROM followups WHERE request_id = ? ORDER BY message_ts",
                          (request_id,))

    # ── what the bot said ───────────────────────────────────────────────────
    def record_post(self, request_id: Optional[str], thread_ts: Optional[str], ts: str) -> None:
        self._exec("INSERT OR IGNORE INTO posts VALUES (?, ?, ?, ?)",
                   (request_id, thread_ts, ts, _now()))

    def posts(self, request_id: str) -> list[dict]:
        return self._rows("SELECT * FROM posts WHERE request_id = ? ORDER BY ts", (request_id,))
