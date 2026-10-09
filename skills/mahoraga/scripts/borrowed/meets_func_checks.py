"""Functional checks: theme switch, custom player, timeline seek, dashboard dedupe, room hand/toast.
Against meets_dev_run.py on :5005, or BASE_URL."""
import os, time
from playwright.sync_api import sync_playwright

B = os.environ.get("BASE_URL", "http://127.0.0.1:5005").rstrip("/")
ok = lambda c, m: print(("PASS " if c else "FAIL ") + m)
with sync_playwright() as pw:
    br = pw.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])
    ctx = br.new_context(viewport={"width": 1440, "height": 900}, color_scheme="light")
    pg = ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(B + "/__login/1001?next=/"); pg.goto(B + "/"); time.sleep(1.5)
    t0 = pg.evaluate("document.documentElement.dataset.theme")
    pg.click(".theme-btn"); time.sleep(1.0)
    t1 = pg.evaluate("document.documentElement.dataset.theme")
    ok(t0 == "light" and t1 == "dark", f"theme switch light -> {t1}")
    ok(pg.evaluate("localStorage.getItem('meets-theme')") == "dark", "theme choice remembered")
    ok(pg.evaluate("document.querySelector('.theme-btn').getAttribute('aria-pressed')") == "true", "switch reports pressed in dark")
    silk = pg.evaluate("document.querySelector('video[data-silk]').getAttribute('src')")
    ok("night" in (silk or ""), f"dark theme plays the night silk ({silk})")
    pg.reload(); time.sleep(1)
    ok(pg.evaluate("document.documentElement.dataset.theme") == "dark", "dark survives a reload")
    # dashboard: each meeting once
    titles = pg.evaluate("[...document.querySelectorAll('.spot h3, #liveCards .ttl, #myCards .ttl')].map(e=>e.textContent)")
    ok(titles.count("Weekly growth sync") == 1, f"live meeting shown once ({titles})")
    # recording page: custom player
    pg.goto(B + "/archive/mkr-owqe-jtl"); time.sleep(2)
    ok(pg.evaluate("!document.getElementById('player').hasAttribute('controls')"), "no native controls")
    pg.click("#pPlay"); time.sleep(1.5)
    ok(pg.evaluate("!document.getElementById('player').paused"), "play button plays")
    pg.click("#pRate"); ok(pg.evaluate("document.getElementById('player').playbackRate") == 1.25, "speed steps to 1.25x")
    pg.click("#pCc"); ok(pg.evaluate("document.getElementById('pCc').getAttribute('aria-pressed')") == "true", "captions toggle on")
    box = pg.locator(".tl-track").first.bounding_box()
    pg.mouse.click(box["x"] + box["width"] * 0.5, box["y"] + box["height"] / 2); time.sleep(0.8)
    cur = pg.evaluate("document.getElementById('player').currentTime")
    ok(1080 < cur < 1240, f"clicking the middle of a lane seeks to the middle ({cur:.0f}s of 2280)")
    ok(pg.evaluate("!!document.querySelector('.tline.on')"), "transcript follows the playhead")
    y = pg.evaluate("scrollY"); pg.evaluate("seek(2100)"); time.sleep(0.8)
    ok(abs(pg.evaluate("scrollY") - y) < 5, "seeking keeps the page where it is")
    pg.click(".spk button:nth-child(2)"); time.sleep(0.3)
    vis = pg.evaluate("[...document.querySelectorAll('#tlist .tline:not(.hidden) .who')].map(e=>e.textContent.trim())")
    ok(len(set(vis)) == 1, f"speaker filter shows one voice ({set(vis)})")
    # room: hand toast for staff, pager hidden with 6 people, solo note hidden
    pg.goto(B + "/m/qvx-mtab-rkp?mock=default"); time.sleep(3.5)
    ok(pg.evaluate("document.getElementById('pager').classList.contains('hide')"), "no pager for six people")
    ok(pg.evaluate("document.getElementById('soloNote').classList.contains('hide')"), "no solo note with company")
    ok(pg.evaluate("document.getElementById('btnMeeting').textContent.includes('End')"), "live meeting shows End")
    ok(pg.evaluate("document.querySelectorAll('#grid .tile').length") == 6, "six tiles")
    over = pg.evaluate("""(()=>{const t=[...document.querySelectorAll('#grid .tile')].map(e=>e.getBoundingClientRect());
      for(let i=0;i<t.length;i++)for(let j=i+1;j<t.length;j++){const a=t[i],b=t[j];
        if(a.left<b.right-1&&b.left<a.right-1&&a.top<b.bottom-1&&b.top<a.bottom-1)return true}return false})()""")
    ok(not over, "tiles never overlap")
    pg.goto(B + "/m/qvx-mtab-rkp?mock=solo"); time.sleep(2.5)
    ok(not pg.evaluate("document.getElementById('soloNote').classList.contains('hide')"), "solo note when alone")
    ok(not errs, "no page errors " + (" | ".join(errs[:3]) if errs else ""))
    br.close()
