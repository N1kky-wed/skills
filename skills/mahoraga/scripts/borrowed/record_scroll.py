"""Record a scroll-through of a page as video: pointer play in the hero, a vote, then a slow wheel scroll to the end.
usage: python record.py <path> <out.mp4> [--seconds N]"""
import sys, os, time, glob, shutil, subprocess
from playwright.sync_api import sync_playwright

path, out = sys.argv[1], sys.argv[2]
tmp = os.path.join(os.path.dirname(out) or ".", "_rec")
shutil.rmtree(tmp, ignore_errors=True)
with sync_playwright() as pw:
    br = pw.chromium.launch(args=["--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"])
    ctx = br.new_context(viewport={"width": 1280, "height": 800}, record_video_dir=tmp, record_video_size={"width": 1280, "height": 800})
    ctx.add_init_script("try{localStorage.setItem('8x_analytics_consent','denied')}catch(e){}")
    pg = ctx.new_page()
    pg.goto("http://localhost:3200" + path, wait_until="domcontentloaded")
    time.sleep(1.0)
    # dismiss the consent card so it does not sit over the film
    for label in ("Decline",):
        try:
            pg.get_by_role("button", name=label).click(timeout=4000)
        except Exception:
            pass
    time.sleep(2.8)
    # pointer play across the hero, then vote twice
    for x, y in ((400, 500), (900, 420), (1100, 650), (640, 600)):
        pg.mouse.move(x, y, steps=18); time.sleep(0.25)
    try:
        box = pg.locator("canvas").first.bounding_box()
        if box:
            cx, cy = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
            pg.mouse.click(cx, cy); time.sleep(1.1)
            pg.mouse.click(cx, cy); time.sleep(1.4)
    except Exception:
        pass
    total = pg.evaluate("document.documentElement.scrollHeight - innerHeight")
    y = 0
    while y < total:
        pg.mouse.wheel(0, 120); y += 120; time.sleep(0.045)
        if y % 2400 < 120:
            pg.mouse.move(300 + (y // 7) % 700, 400, steps=4)
    time.sleep(1.5)
    video = pg.video.path()
    ctx.close(); br.close()
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", video, "-vf", "fps=30,scale=1280:-2", "-c:v", "libx264", "-crf", "24", "-preset", "slow", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], check=True)
shutil.rmtree(tmp, ignore_errors=True)
print("wrote", out, os.path.getsize(out) // 1024, "KB")
