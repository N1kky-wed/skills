"""Capture the 8x Meets UI (meets_dev_run.py on :5005, or BASE_URL) in both themes at desktop and phone sizes.
usage: python theme_shots.py <round-dir> [only-name-substring ...]
Writes ./shots/<round-dir>/ in the folder you run from."""
import sys, os, time
from playwright.sync_api import sync_playwright

BASE = os.environ.get("BASE_URL", "http://127.0.0.1:5005").rstrip("/")
OUT = os.path.join("shots", sys.argv[1] if len(sys.argv) > 1 else "r1")
ONLY = sys.argv[2:]
os.makedirs(OUT, exist_ok=True)
DESK = dict(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
PHONE = dict(viewport={"width": 390, "height": 844}, device_scale_factor=2, is_mobile=True, has_touch=True)

# name, who (None = signed out), path, wait seconds, optional action
SHOTS = [
    ("login", None, "/", 2.5, None),
    ("dashboard", "1001", "/", 2.5, None),
    ("newmeeting", "1001", "/", 2.0, "new"),
    ("archive", "1001", "/archive", 2.0, None),
    ("recording", "1001", "/archive/mkr-owqe-jtl", 2.5, "play"),
    ("processing", "1001", "/archive/pcs-xnwe-ubr", 2.0, None),
    ("room", "1001", "/m/qvx-mtab-rkp?mock=default&me=cam", 4.0, None),
    ("room-chat", "1001", "/m/qvx-mtab-rkp?mock=default", 3.5, "chat"),
    ("room-share", "1001", "/m/qvx-mtab-rkp?mock=share", 4.0, None),
    ("room-crowd", "1001", "/m/qvx-mtab-rkp?mock=crowd", 4.0, None),
    ("room-phones", "1001", "/m/qvx-mtab-rkp?mock=phones&me=cam", 4.0, None),
    ("room-solo", "1001", "/m/qvx-mtab-rkp?mock=solo", 3.0, None),
    ("greenroom", "1001", "/m/bnt-kolq-ave?mock=solo", 3.0, None),
    ("event-attendee", "1009", "/m/hpe-ruwn-zdf?mock=events", 3.5, None),
    ("lobby", "1009", "/m/bnt-kolq-ave", 2.5, None),
]


def run():
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
        for name, who, path, wait, action in SHOTS:
            if ONLY and not any(o in name for o in ONLY):
                continue
            for theme in ("light", "dark"):
                for size, opts in (("desk", DESK), ("phone", PHONE)):
                    ctx = br.new_context(**opts, color_scheme=theme)
                    ctx.add_init_script(f"try{{localStorage.setItem('meets-theme','{theme}')}}catch(e){{}}")
                    pg = ctx.new_page()
                    errs = []
                    pg.on("pageerror", lambda e: errs.append(str(e)))
                    pg.on("console", lambda m: errs.append("console: " + m.text) if m.type == "error" else None)
                    if who:
                        pg.goto(f"{BASE}/__login/{who}?next=/", wait_until="domcontentloaded")
                    pg.goto(BASE + path, wait_until="domcontentloaded")
                    time.sleep(wait)
                    if action == "new":
                        pg.click("#newBtn"); time.sleep(0.8)
                    elif action == "chat":
                        pg.click("#btnChat"); time.sleep(0.9)
                    elif action == "play":
                        pg.evaluate("seek(600)"); time.sleep(1.2)
                        pg.evaluate("document.getElementById('player') && document.getElementById('player').pause()")
                    f = os.path.join(OUT, f"{name}-{theme}-{size}.png")
                    pg.screenshot(path=f)
                    if errs:
                        print(name, theme, size, "ERR:", " | ".join(errs[:4]))
                    ctx.close()
            print("done", name)
        br.close()


run()
