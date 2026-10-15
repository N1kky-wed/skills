"""Slack Socket Mode listener: the bot's front door.

Deliberately thin. It decides whether a message is for the bot, claims it
(idempotency), and hands it to a worker thread. The handler returns at once
because Slack re-delivers any event not acknowledged within three seconds, and
a re-delivery racing a slow handler is how a job runs twice.
"""

import logging
import os
import queue
import signal
import sys
import threading
import time
from datetime import datetime

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

from bot import config, followups, phrases, pipeline, slack_io, state

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"),
                    format="%(asctime)s %(levelname)-7s %(name)s: %(message)s")
log = logging.getLogger("bot.app")

store = state.Store(config.STATE_DB)
slack_io.bind_store(store)
work: "queue.Queue[dict]" = queue.Queue()


def is_human(event: dict) -> bool:
    """A real person's message in the bot's channel. The bot's own posts carry
    a bot_id and are dropped here, so it can never trigger itself."""
    if event.get("channel") != config.CHANNEL_ID:
        return False
    if event.get("subtype") not in (None, "thread_broadcast", "file_share"):
        return False
    if event.get("bot_id") or event.get("app_id"):
        return False
    return bool(event.get("user"))


def is_for_bot(event: dict) -> bool:
    """A tag always counts. An untagged reply counts when it is in a thread the
    bot is active in and comes from the person it was talking to."""
    if not is_human(event):
        return False
    if config.MENTION_TOKEN in (event.get("text") or ""):
        return True
    thread_ts = event.get("thread_ts")
    if not thread_ts:
        return False
    history = store.thread_history(thread_ts)
    if not history:
        return False
    last = history[-1]
    age = time.time() - datetime.fromisoformat(last["updated_at"]).timestamp()
    return age <= config.FOLLOW_UP_WINDOW_SECONDS and last.get("user_id") == event.get("user")


def _queued_ack(request: dict) -> None:
    time.sleep(config.QUEUE_ACK_AFTER_SECONDS)
    row = store.get(request["request_id"])
    if row and row["status"] == state.RECEIVED:
        slack_io.post(request["slack"].get("thread_ts") or request["slack"]["message_ts"],
                      phrases.QUEUED, request["request_id"])


def _worker() -> None:
    while True:
        request = work.get()
        try:
            pipeline.process(request, store)
        except Exception:  # noqa: BLE001
            log.exception("[%s] worker crashed", request.get("request_id"))
        finally:
            work.task_done()


def handle(event: dict) -> None:
    if not is_for_bot(event):
        return
    rid = f"{event['channel']}-{event['ts']}"
    text = event.get("text") or ""
    if config.DRY_RUN:
        log.info("DRY RUN %s from %s: %s", rid, event.get("user"), text[:200])
        return
    if not store.claim(rid, channel_id=event["channel"], message_ts=event["ts"],
                       thread_ts=event.get("thread_ts"), user_id=event.get("user"),
                       request_text=text):
        log.info("[%s] duplicate delivery ignored", rid)
        return
    reply_to = event.get("thread_ts") or event["ts"]
    user = event.get("user")
    body = text.replace(config.MENTION_TOKEN, "").strip()

    social = phrases.social_reply(body)
    if social and not event.get("files"):
        store.update(rid, status=state.COMPLETED)
        slack_io.post(reply_to, config.with_name(social, user), rid)
        return

    running = store.inflight_in_thread(reply_to, rid)
    if running:
        n = followups.attach(store, running["request_id"], event)
        store.update(rid, status=state.ATTACHED)
        log.info("[%s] attached to %s as follow-up #%d", rid, running["request_id"], n)
        slack_io.post(reply_to, config.with_name(phrases.followup_ack(), user), rid)
        return

    permalink = slack_io.permalink(event["ts"])
    store.update(rid, permalink=permalink)
    request = {"request_id": rid, "slack": {
        "channel_id": event["channel"], "message_ts": event["ts"],
        "thread_ts": event.get("thread_ts"), "user_id": user, "message": text,
        "permalink": permalink,
        "files": [{k: f.get(k) for k in ("id", "name", "mimetype", "size",
                                         "url_private_download", "url_private")}
                  for f in event.get("files") or []],
    }}
    log.info("[%s] accepted from %s", rid, user)
    work.put(request)
    threading.Thread(target=_queued_ack, args=(request,), daemon=True).start()


def main() -> None:
    missing = config.missing()
    if missing:
        log.error("missing settings in .env: %s", ", ".join(missing))
        sys.exit(1)
    log.info("config: %s", config.redacted_summary())

    app = App(token=config.SLACK_BOT_TOKEN)

    @app.event("message")
    def on_message(event, logger):  # noqa: ARG001
        handle(event)

    @app.event("app_mention")
    def on_mention(event, logger):  # noqa: ARG001
        return  # mentions also arrive as `message`; this stops double handling

    pipeline.recover(store)
    for i in range(config.WORKERS):
        threading.Thread(target=_worker, daemon=True, name=f"worker-{i}").start()

    handler = SocketModeHandler(app, config.SLACK_APP_TOKEN)

    def shutdown(signum, _frame):
        log.info("signal %s, shutting down", signum)
        handler.close()
        sys.exit(0)

    signal.signal(signal.SIGTERM, shutdown)
    signal.signal(signal.SIGINT, shutdown)
    log.info("listening in %s for %s with %d worker(s)", config.CHANNEL_ID,
             config.MENTION_TOKEN, config.WORKERS)
    handler.start()


if __name__ == "__main__":
    main()
