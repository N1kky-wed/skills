"""Operator tool. Run with the bot's venv python from the bot's directory.

    botctl status              in-flight jobs and the last 15 requests
    botctl show <request_id>   one request in full
    botctl stop <request_id>   kill a running job and say so in its thread
    botctl clean <request_id>  delete every message the bot posted for a job
    botctl rerun <request_id>  run a request again, in this process (the
                               service keeps running; nothing restarts)
    botctl say <thread_ts> <text>   post a line as the bot in a thread

A restart (`sudo systemctl restart slack-agent-bot`) kills every running job;
the bot posts "i got restarted" in each one's thread on the way back up. Check
`botctl status` first.
"""

import json
import os
import signal
import sys

from bot import config, pipeline, slack_io, state

store = state.Store(config.STATE_DB)
slack_io.bind_store(store)


def _row(rid: str) -> dict:
    row = store.get(rid)
    if not row:
        sys.exit(f"no such request: {rid}")
    return row


def status() -> None:
    live = store.inflight()
    print(f"in flight: {len(live)}")
    for r in live:
        print(f"  {r['request_id']}  {r['status']:<10} pid={r.get('pid')}  {(r['request_text'] or '')[:70]!r}")
    print("\nrecent:")
    for r in store.recent(15):
        print(f"  {r['created_at'][:16]}  {r['status']:<14} {r['request_id']}  {(r['request_text'] or '')[:60]!r}")


def show(rid: str) -> None:
    row = _row(rid)
    for k, v in row.items():
        if isinstance(v, str) and v.startswith("{"):
            try:
                v = json.dumps(json.loads(v), indent=2)
            except ValueError:
                pass
        print(f"{k}: {v}")


def stop(rid: str) -> None:
    row = _row(rid)
    if row["status"] not in state.IN_FLIGHT:
        sys.exit(f"{rid} is {row['status']}, not running")
    store.update(rid, status=state.CANCELLED, error="stopped by operator")
    pid = row.get("pid")
    if pid:
        try:
            os.kill(int(pid), signal.SIGTERM)
            print(f"killed pid {pid}")
        except ProcessLookupError:
            print(f"pid {pid} already gone")
    thread = row.get("thread_ts") or row["message_ts"]
    slack_io.post(thread, config.with_name(
        "stopped this one for now, nothing was changed. tag me whenever you want it picked back up",
        row.get("user_id")), rid)
    print("stopped")


def clean(rid: str) -> None:
    posts = store.posts(rid)
    gone = sum(slack_io.delete(p["ts"]) for p in posts)
    print(f"deleted {gone}/{len(posts)} bot messages")


def rerun(rid: str) -> None:
    row = _row(rid)
    if row["status"] in state.IN_FLIGHT:
        sys.exit(f"{rid} is still {row['status']}; stop it first")
    store.update(rid, status=state.RECEIVED, error=None, pid=None)
    request = {"request_id": rid, "slack": {
        "channel_id": row["channel_id"], "message_ts": row["message_ts"],
        "thread_ts": row.get("thread_ts"), "user_id": row.get("user_id"),
        "message": row.get("request_text") or "", "permalink": row.get("permalink"), "files": []}}
    pipeline.process(request, store)
    print(f"done: {store.status(rid)}")


def main(argv: list[str]) -> None:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return
    cmd, args = argv[0], argv[1:]
    if cmd == "status":
        status()
    elif cmd in ("show", "stop", "clean", "rerun") and len(args) == 1:
        {"show": show, "stop": stop, "clean": clean, "rerun": rerun}[cmd](args[0])
    elif cmd == "say" and len(args) >= 2:
        slack_io.post(args[0], " ".join(args[1:]))
    else:
        sys.exit(__doc__.strip())


if __name__ == "__main__":
    main(sys.argv[1:])
