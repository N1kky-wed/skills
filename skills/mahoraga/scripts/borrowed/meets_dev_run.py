"""Local-only runner for 8x Meets UI work: throwaway DB, seeded people/meetings/archive,
a dev sign-in route and a mocked LiveKit client. Nothing here ships.

    MEETS_REPO=<the 8x-gmeet checkout> python meets_dev_run.py     # then http://127.0.0.1:5005

The throwaway DB and recordings go to WORK_DIR (default: meets-dev in the system temp folder). AVATARS_DIR is any
folder of sample faces (default <repo>/public/avatars); POSTER_SRC an image for the archived recording's frame
(default: a flat lilac frame). Needs ffmpeg on PATH."""
import os, sys, json, sqlite3, subprocess, tempfile
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))  # lk-mock.js ships beside this file
REPO = os.path.abspath(os.environ.get("MEETS_REPO", "."))  # the 8x-gmeet checkout
AVATARS = os.path.abspath(os.environ.get("AVATARS_DIR", os.path.join(REPO, "public", "avatars")))
POSTER_SRC = os.environ.get("POSTER_SRC")
WORK = os.path.abspath(os.environ.get("WORK_DIR", os.path.join(tempfile.gettempdir(), "meets-dev")))
os.makedirs(WORK, exist_ok=True)
DB = os.path.join(WORK, "meeting.db")
REC = os.path.join(WORK, "recordings")

for f in (DB, DB + "-wal", DB + "-shm"):
    if os.path.exists(f):
        os.remove(f)
os.environ.update({
    "DB_PATH": DB, "RECORDINGS_DIR": REC, "SECRET_KEY": "dev-only-local",
    "LIVEKIT_API_KEY": "devkey", "LIVEKIT_API_SECRET": "dev-only-local-livekit-signing",
    "LIVEKIT_URL": "ws://127.0.0.1:1", "ADMIN_EMAILS": "priya@8x.social",
})
sys.path.insert(0, REPO)
os.chdir(REPO)
import app as meet  # noqa: E402  (init_db runs on import)
from flask import session, redirect, request, send_from_directory, Response  # noqa: E402

meet.app.config["SESSION_COOKIE_SECURE"] = False
meet.app.config["TEMPLATES_AUTO_RELOAD"] = True

now = datetime.now(timezone.utc)
iso = lambda d: d.isoformat()
PEOPLE = [  # sub, name, email, avatar, role
    ("1001", "Priya Nair", "priya@8x.social", "priya", "admin"),
    ("1002", "Maya Chen", "maya@8x.social", "maya", "attendee"),
    ("1003", "Kenji Watanabe", "kenji@8x.social", "kenji", "moderator"),
    ("1004", "Sofía Álvarez", "sofia@gmail.com", "sofia", "attendee"),
    ("1005", "Marcus Hale", "marcus@arcwise.co", "marcus", "attendee"),
    ("1006", "Lena Park", "lena@8x.social", "lena", "attendee"),
    ("1007", "Ethan Brooks", "ethan@gmail.com", "ethan", "attendee"),
    ("1008", "Zara Ali", "zara@8x.social", "zara", "attendee"),
    ("1009", "Noah Kim", "noah@gmail.com", "noah", "attendee"),
    ("1010", "Imani Ross", "imani@gmail.com", "imani", "attendee"),
    ("1011", "Jordan Lee", "jordan@gmail.com", "jordan", "attendee"),
    ("1012", "Tomás Rivera", "tomas@gmail.com", "tomas", "attendee"),
]
db = sqlite3.connect(DB)
for sub, name, email, av, role in PEOPLE:
    db.execute("INSERT INTO users (google_sub,name,email,picture,role,created_at,last_seen) VALUES (?,?,?,?,?,?,?)",
               (sub, name, email, f"/__img/{av}.webp", role, iso(now), iso(now)))
uid = {p[0]: i + 1 for i, p in enumerate(PEOPLE)}


def mtg(slug, title, mtype, state, record=1, cams=0, created=0, started=None, dur=None, minutes=None,
        progress=0, step=None, host="1001", itype="internal", internal_url=None, ti=0, to=0):
    db.execute(
        "INSERT INTO meetings (slug,title,type,host_sub,state,record,record_cams,created_at,started_at,ended_at,"
        "duration_s,minutes_json,proc_progress,proc_step,internal_type,internal_url,ai_tokens_in,ai_tokens_out)"
        " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (slug, title, mtype, host, state, record, cams, iso(now - timedelta(minutes=created)),
         iso(now - timedelta(minutes=started)) if started is not None else None,
         iso(now - timedelta(minutes=started) + timedelta(seconds=dur)) if (started is not None and dur) else None,
         dur, json.dumps(minutes) if minutes else None, progress, step, itype, internal_url, ti, to))
    return db.execute("SELECT id FROM meetings WHERE slug=?", (slug,)).fetchone()[0]


live1 = mtg("qvx-mtab-rkp", "Weekly growth sync", "meeting", "live", created=40, started=23)
live2 = mtg("hpe-ruwn-zdf", "Creator AMA: posting on X", "event", "live", created=90, started=51, host="1003")
mtg("bnt-kolq-ave", "Q4 planning", "meeting", "scheduled", created=120)
mtg("wzr-ploc-ymh", "Sales call: Arcwise", "meeting", "scheduled", created=300, itype="sales_call")
mtg("dfo-kiqa-snb", "Candidate interview: design lead", "meeting", "scheduled", record=0, created=900,
    itype="candidate_interview")

MINUTES = {
    "summary": "The team reviewed September growth: creator sign-ups are up 38% since the X card launch at 02:10, "
               "and paid posts now clear in under two days. Maya walked through the new onboarding funnel at 09:42 "
               "and Kenji flagged payout delays for creators in Brazil at 18:05. The team agreed to ship instant "
               "payouts behind a flag next sprint.",
    "chapters": [{"t": 0, "title": "Check-in and agenda"}, {"t": 130, "title": "September growth numbers"},
                 {"t": 582, "title": "Onboarding funnel walkthrough"}, {"t": 1085, "title": "Payout delays in Brazil"},
                 {"t": 1620, "title": "Instant payouts: decision"}, {"t": 2040, "title": "Owners and next steps"}],
    "action_items": ["Maya to ship the two-step onboarding to 10% of new creators by Friday (09:42)",
                     "Kenji to open a ticket with the payout provider about BRL settlement (18:05)",
                     "Sofía to draft the instant payouts FAQ for the creator help center",
                     "Priya to review the flag rollout plan before Thursday's sync (34:00)"],
    "decisions": ["Instant payouts ship behind a flag next sprint, creators opt in (27:00)",
                  "The X card stays the default share image for all new profiles"],
}
arch = mtg("mkr-owqe-jtl", "Weekly growth sync", "meeting", "archived", created=10090, started=10080, dur=2280,
           minutes=MINUTES, internal_url="https://internal.8x.social/meetings/2291", ti=182000, to=9400)
SEGS = [
    (4, "Priya Nair", "Morning everyone. Quick one today: growth numbers, the onboarding funnel, then payouts."),
    (18, "Maya Chen", "Morning! I have the funnel deck ready whenever you want it."),
    (31, "Kenji Watanabe", "And I want ten minutes on Brazil at the end, it's getting loud in support."),
    (130, "Priya Nair", "Great. So September. Creator sign-ups are up thirty eight percent since the X card went live."),
    (152, "Lena Park", "Most of that is organic. People share the card and their followers sign up from the link."),
    (171, "Priya Nair", "Which is exactly what we hoped. Paid posts are clearing in under two days now too."),
    (204, "Marcus Hale", "From the brand side that's the number that matters. Two days is a real selling point."),
    (240, "Lena Park", "One caveat: retention after the first paid post is flat. We should watch that."),
    (582, "Maya Chen", "Okay, sharing now. This is the new onboarding, two steps instead of five."),
    (611, "Maya Chen", "Step one connects X and pulls the profile. Step two is rates, prefilled from similar creators."),
    (650, "Kenji Watanabe", "Prefilled rates is smart. Most people bounce on that screen today."),
    (688, "Sofía Álvarez", "Yo lo probé ayer, es mucho más rápido. Me tomó menos de un minuto."),
    (731, "Maya Chen", "We'd ship it to ten percent of new creators first and compare completion."),
    (1085, "Kenji Watanabe", "Brazil. Payouts in reais are taking five to seven days, and creators are noticing."),
    (1122, "Sofía Álvarez", "Tengo tres tickets abiertos de creadores en São Paulo esta semana."),
    (1160, "Priya Nair", "Is that us or the provider?"),
    (1172, "Kenji Watanabe", "Mostly the provider's settlement window. I'll open a ticket with them today."),
    (1620, "Priya Nair", "Let's decide instant payouts. My proposal: ship behind a flag, creators opt in."),
    (1648, "Lena Park", "Agreed. The fee is fine as long as it's shown before they confirm."),
    (1701, "Marcus Hale", "Brands won't see any of this, right? It's creator side only."),
    (1712, "Priya Nair", "Creator side only. Decision made, flag next sprint."),
    (2040, "Priya Nair", "Owners: Maya on onboarding, Kenji on the provider, Sofía on the FAQ, and I'll review the rollout."),
    (2210, "Maya Chen", "Sounds good. Thanks all!"),
]
lang = {"Sofía Álvarez": "es"}
tr = {688: "I tried it yesterday, it's much faster. It took me less than a minute.",
      1122: "I have three open tickets from creators in São Paulo this week."}
for i, (t0, spk, text) in enumerate(SEGS):
    t1 = SEGS[i + 1][0] - 2 if i + 1 < len(SEGS) and SEGS[i + 1][0] - t0 < 60 else t0 + min(40, 6 + len(text) // 9)
    db.execute("INSERT INTO transcript_segments (meeting_id,t0,t1,speaker,text,lang,text_en) VALUES (?,?,?,?,?,?,?)",
               (arch, t0, t1, spk, text, lang.get(spk, "en"), tr.get(t0)))
for t, d in [(590, "Slide: 'Onboarding, two steps' with a funnel chart, 41% to 68% completion"),
             (640, "Prototype of step two: rate fields prefilled from similar creators"),
             (1100, "Support dashboard filtered to Brazil, 23 open payout tickets")]:
    db.execute("INSERT INTO screen_notes (meeting_id,t,description) VALUES (?,?,?)", (arch, t, d))
for sub in ("1001", "1002", "1003", "1004", "1005", "1006"):
    db.execute("INSERT INTO meeting_events (user_id,event_type,metadata,created_at,meeting_id) VALUES (?,?,?,?,?)",
               (uid[sub], "join", "{}", iso(now - timedelta(days=7)), arch))
for sub, msg, mins in [("1002", "Deck: the onboarding flow v3 is in the drive", 9),
                       ("1005", "Two days to clear is huge for our Q4 campaigns", 4),
                       ("1004", "Filed the São Paulo tickets under PAY-212", 19)]:
    db.execute("INSERT INTO messages (user_id,message,created_at,meeting_id) VALUES (?,?,?,?)",
               (uid[sub], msg, iso(now - timedelta(days=7) + timedelta(minutes=mins)), arch))
# more archive entries (no video) and one still processing
mtg("zqa-hmvr-pol", "Creator AMA: rates and briefs", "event", "archived", created=20200, started=20160, dur=3120,
    minutes={"summary": "Kenji answered creator questions on rates, briefs and payout timing.", "chapters": [],
             "action_items": [], "decisions": []})
mtg("lwe-bnaz-cxu", "1:1 Priya and Maya", "meeting", "archived", created=14500, started=14460, dur=1740,
    itype="one_on_one")
mtg("gyt-vrop-kei", "Investor update: September", "meeting", "archived", created=30000, started=29950, dur=2640,
    itype="investor")
mtg("pcs-xnwe-ubr", "Client call: Pixelforge", "meeting", "processing", created=70, started=66, dur=2400,
    progress=64, step="Transcribing each speaker")
OTHER = {  # slug: (joiners, [(speaker, seconds talked)])
    "zqa-hmvr-pol": (("1001", "1003", "1009", "1010", "1011"), [("Kenji Watanabe", 1500), ("Imani Ross", 380), ("Noah Kim", 260), ("Jordan Lee", 140)]),
    "lwe-bnaz-cxu": (("1001", "1002"), [("Priya Nair", 820), ("Maya Chen", 760)]),
    "gyt-vrop-kei": (("1001", "1008", "1003"), [("Priya Nair", 1400), ("Zara Ali", 700), ("Kenji Watanabe", 350)]),
    "pcs-xnwe-ubr": (("1001", "1005"), []),
}
for slug, (who, talk) in OTHER.items():
    mid = db.execute("SELECT id FROM meetings WHERE slug=?", (slug,)).fetchone()[0]
    for sub in who:
        db.execute("INSERT INTO meeting_events (user_id,event_type,metadata,created_at,meeting_id) VALUES (?,?,?,?,?)",
                   (uid[sub], "join", "{}", iso(now), mid))
    t0 = 0
    for spk, secs in talk:
        db.execute("INSERT INTO transcript_segments (meeting_id,t0,t1,speaker,text,lang) VALUES (?,?,?,?,?,?)",
                   (mid, t0, t0 + secs, spk, "(seeded line)", "en"))
        t0 += secs + 5
# live meeting: chat history, a raised hand, lobby presence for the event
for sub, msg, mins in [("1003", "Morning! Joining from the train, mic off for a bit", 21),
                       ("1002", "Funnel deck is ready when we get there", 18),
                       ("1006", "Retention numbers are in the sheet, tab 3", 9)]:
    db.execute("INSERT INTO messages (user_id,message,created_at,meeting_id) VALUES (?,?,?,?)",
               (uid[sub], msg, iso(now - timedelta(minutes=mins)), live1))
db.execute("INSERT INTO mtg_state (meeting_id,identity,hand_raised,can_speak,updated_at) VALUES (?,?,?,?,?)",
           (live1, "1005", 1, 0, iso(now)))
for sub in ("1009", "1010", "1011"):
    db.execute("INSERT INTO presence (meeting_id,identity,last_seen) VALUES (?,?,?)", (live2, sub, iso(now + timedelta(days=1))))
for sub, best in [("1001", 184), ("1002", 233), ("1003", 97), ("1006", 150), ("1009", 61)]:
    db.execute("INSERT INTO game_scores (user_id,best,plays,updated_at) VALUES (?,?,?,?)", (uid[sub], best, 3, iso(now)))
db.commit()
db.close()

# a stand-in recording for the archived sync: the poster frame held for the whole meeting
rd = os.path.join(REC, "mkr-owqe-jtl")
os.makedirs(rd, exist_ok=True)
poster = os.path.join(rd, "poster.jpg")
if not os.path.exists(poster):
    src = ["-i", os.path.abspath(POSTER_SRC)] if POSTER_SRC else ["-f", "lavfi", "-i", "color=c=0xd9d4f2:s=1280x720"]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *src, "-frames:v", "1", "-q:v", "3", poster], check=True)
if not os.path.exists(os.path.join(rd, "final.mp4")):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", poster, "-t", "2280", "-r", "1",
                    "-vf", "scale=1280:-2", "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
                    os.path.join(rd, "final.mp4")], check=True)

meet._rooms_ensured.update({"qvx-mtab-rkp", "hpe-ruwn-zdf", "bnt-kolq-ave", "wzr-ploc-ymh", "dfo-kiqa-snb"})


@meet.app.route("/__login/<sub>")
def _dev_login(sub):
    session["sub"] = sub
    session.permanent = True
    return redirect(request.args.get("next", "/"))


@meet.app.route("/__img/<path:name>")
def _dev_img(name):
    return send_from_directory(AVATARS, name)


@meet.app.before_request
def _mock_livekit():
    if request.path == "/static/livekit-client.umd.min.js":
        with open(os.path.join(HERE, "lk-mock.js"), encoding="utf-8") as fh:
            return Response(fh.read(), mimetype="application/javascript", headers={"Cache-Control": "no-store"})


if __name__ == "__main__":
    meet.app.run(host="127.0.0.1", port=5005, debug=False, threaded=True)
