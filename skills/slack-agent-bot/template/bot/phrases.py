"""Canned lines: greetings, acks, progress. Edit the lists freely.

"hi" and "thanks" are answered from these tables without a model call: a
greeting that triggers a full triage run reads as broken and costs money.
Progress lines are a sign of life every PROGRESS_INTERVAL_SECONDS while a long
job runs. If PROGRESS_MODEL is set, a cheap model writes a fresh one each time
and these pools are the fallback.
"""

import logging
import random
import re
import subprocess

from . import config

log = logging.getLogger("bot.phrases")

GREETINGS = {"hi", "hey", "hello", "yo", "hiya", "heya", "sup", "gm", "good morning", "morning"}
CHECKINS = {"how are you", "how r u", "hows it going", "you there", "u there", "are you there", "you up"}
THANKS = {"thanks", "thank you", "thx", "ty", "tysm", "cheers", "nice", "great", "perfect",
          "awesome", "cool", "ok thanks", "okay thanks", "thanks a lot", "nice one", "legend"}

GREETING_REPLY = ["hey", "hii", "yo", "hey, what do you need"]
CHECKIN_REPLY = ["all good, what do you need", "here, what's up", "alive and well"]
THANKS_REPLY = ["anytime", "np", "glad it helped", "any time 🫡"]
FOLLOWUP_ACK = [
    "noted, adding that to the job already running here",
    "got it, the running job will pick that up before it finishes",
]
QUEUED = "got it, i'm in the middle of something, will get to this in a bit"

PROGRESS = [
    "still on it, {t} in",
    "{t} in, still going",
    "still at it, {t}. good things take time",
    "chipping away, {t} so far",
    "not stuck, just thorough. {t}",
    "{t} and counting, still cooking",
    "still on it, {t}. this is the montage part",
]

_STRIP = str.maketrans("", "", "!?.,'’")


def social_reply(text: str) -> str | None:
    words = text.lower().translate(_STRIP).split()
    while words and words[-1] in {"bot", "man", "dude", "bro", "mate", "team", "all", "guys", "today"}:
        words.pop()
    joined = " ".join(words)
    if not joined:
        return None
    if joined in CHECKINS or (len(words) > 1 and words[0] in GREETINGS and " ".join(words[1:]) in CHECKINS):
        return random.choice(CHECKIN_REPLY)
    if joined in GREETINGS:
        return random.choice(GREETING_REPLY)
    if joined in THANKS:
        return random.choice(THANKS_REPLY)
    return None


def followup_ack() -> str:
    return random.choice(FOLLOWUP_ACK)


def _elapsed(minutes: int) -> str:
    return f"{minutes} min" if minutes < 90 else f"{minutes // 60}h {minutes % 60}m"


class Progress:
    """Progress lines for one run: never the same line twice in a row."""

    def __init__(self) -> None:
        self.used: list[str] = []

    def line(self, minutes: int) -> str:
        t = _elapsed(minutes)
        fresh = self._generate(t)
        if fresh:
            self.used.append(fresh)
            return fresh
        pool = [p for p in PROGRESS if p not in self.used] or PROGRESS
        choice = random.choice(pool)
        self.used.append(choice)
        return choice.format(t=t)

    def _generate(self, t: str) -> str | None:
        if not config.PROGRESS_MODEL:
            return None
        prompt = (
            f'Write ONE short Slack status line for a job still running after "{t}". '
            f'Weave "{t}" into the sentence. Lowercase, under 90 characters, dry and a bit '
            f"funny, no implementation details, no swearing. Do not reuse: {self.used[-6:]}. "
            "Output the line only.\n\n" + config.voice())
        try:
            r = subprocess.run([config.CLAUDE_BIN, "-p", prompt, "--model", config.PROGRESS_MODEL,
                                "--allowedTools", ""], capture_output=True, text=True,
                               timeout=30, env=config.scoped_env([]))
        except (subprocess.TimeoutExpired, OSError):
            return None
        line = " ".join(r.stdout.strip().split()).strip("\"'")
        if r.returncode or not line or len(line) > 120 or t not in line:
            return None
        if re.match(r"^(elapsed|status|update)\b\s*[:\-]", line, re.I):
            return None
        return line
