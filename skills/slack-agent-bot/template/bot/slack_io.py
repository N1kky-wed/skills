"""Everything the bot says to and reads from Slack.

Best-effort: a failed post is logged and never breaks a job. Every post is
recorded against its request so an operator can delete a job's replies.
The listener drops messages carrying a bot_id, so nothing posted here can
re-enter the pipeline.
"""

import logging
from typing import Optional

from slack_sdk import WebClient

from . import config

log = logging.getLogger("bot.slack")

_client = WebClient(token=config.SLACK_BOT_TOKEN) if config.SLACK_BOT_TOKEN else None
_store = None  # set by the listener so posts are recorded


def bind_store(store) -> None:
    global _store
    _store = store


def _house_style(text: str) -> str:
    """Prompts ask for no em/en dashes; this guarantees it."""
    return (text.replace(" — ", ", ").replace("—", ", ")
                .replace(" – ", ", ").replace("–", "-"))


def post(thread_ts: Optional[str], text: str, request_id: Optional[str] = None) -> Optional[str]:
    """Post into a thread. Returns the message ts, or None. Never raises."""
    if not _client or not text.strip():
        return None
    try:
        resp = _client.chat_postMessage(channel=config.CHANNEL_ID, thread_ts=thread_ts,
                                        text=_house_style(text), unfurl_links=False)
        ts = resp.get("ts")
        if _store and ts:
            _store.record_post(request_id, thread_ts, ts)
        return ts
    except Exception as exc:  # noqa: BLE001
        log.warning("post failed: %s", _error(exc))
        return None


def _error(exc: Exception) -> str:
    response = getattr(exc, "response", None)
    try:
        return str(response.get("error")) if response is not None else exc.__class__.__name__
    except Exception:  # noqa: BLE001
        return exc.__class__.__name__


def post_long(thread_ts: Optional[str], text: str, request_id: Optional[str] = None,
              limit: int = 3900) -> None:
    """Post a long answer as several messages split on paragraphs. Nothing is cut."""
    for part in chunks(text, limit):
        post(thread_ts, part, request_id)


def chunks(text: str, limit: int) -> list[str]:
    text = text.strip()
    if len(text) <= limit:
        return [text] if text else []
    out: list[str] = []
    current = ""
    for para in text.split("\n\n"):
        while len(para) > limit:
            cut = para.rfind("\n", 0, limit)
            cut = cut if cut > 0 else limit
            if current:
                out.append(current)
                current = ""
            out.append(para[:cut].rstrip())
            para = para[cut:].lstrip()
        joined = f"{current}\n\n{para}" if current else para
        if len(joined) <= limit:
            current = joined
        else:
            out.append(current)
            current = para
    if current:
        out.append(current)
    return out


def upload(thread_ts: Optional[str], path: str) -> bool:
    """Attach a file (needs files:write). False if refused."""
    if not _client:
        return False
    try:
        _client.files_upload_v2(channel=config.CHANNEL_ID, thread_ts=thread_ts,
                                file=path, title=path.rsplit("/", 1)[-1])
        return True
    except Exception as exc:  # noqa: BLE001
        log.warning("upload failed: %s", exc.__class__.__name__)
        return False


def delete(ts: str) -> bool:
    if not _client:
        return False
    try:
        _client.chat_delete(channel=config.CHANNEL_ID, ts=ts)
        return True
    except Exception as exc:  # noqa: BLE001
        log.warning("delete %s failed: %s", ts, exc.__class__.__name__)
        return False


def permalink(ts: str) -> Optional[str]:
    if not _client:
        return None
    try:
        return _client.chat_getPermalink(channel=config.CHANNEL_ID, message_ts=ts)["permalink"]
    except Exception:  # noqa: BLE001
        return None


def message_text(m: dict) -> str:
    """A message's text including Block Kit and attachments: digests and other
    app posts keep everything but the headline in blocks."""
    parts: list[str] = []

    def walk(node):
        if isinstance(node, dict):
            if node.get("type") in ("mrkdwn", "plain_text") and node.get("text"):
                parts.append(str(node["text"]))
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(m.get("blocks"))
    for a in m.get("attachments") or []:
        for key in ("pretext", "title", "text", "fallback"):
            if a.get(key):
                parts.append(str(a[key]))
    text = (m.get("text") or "").strip()
    blocks = "\n".join(p.strip() for p in parts if p.strip())
    full = blocks if len(blocks) > len(text) else text
    return full[:12000]


def read_thread(thread_ts: str, limit: int = 80) -> list[dict]:
    """A thread in THE bot's channel, oldest first. Never any other channel."""
    if not _client:
        return []
    try:
        resp = _client.conversations_replies(channel=config.CHANNEL_ID, ts=thread_ts, limit=limit)
    except Exception as exc:  # noqa: BLE001
        log.warning("could not read thread %s: %s", thread_ts, exc.__class__.__name__)
        return []
    out = []
    for m in resp.get("messages") or []:
        if m.get("subtype") in ("channel_join", "channel_leave"):
            continue
        out.append({
            "user": m.get("user") or m.get("bot_id") or "?",
            "ts": m.get("ts"),
            "text": message_text(m),
            "is_bot": bool(m.get("bot_id")) or m.get("user") == config.BOT_USER_ID,
            "files": [f for f in (m.get("files") or []) if f.get("url_private")],
        })
    return out
