"""Side by side: our dome passage vs Taiko's frames, matched by crown height.

usage: python domecmp.py <path> <section-start-text> <mode: statement|passage> <taiko dir> <taiko times csv> <our s csv> <out>
"""
import sys
import time
from pathlib import Path

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

path, marker, mode, tdir, ttimes, svals, out = sys.argv[1:8]
ttimes = [float(t) for t in ttimes.split(',')]
svals = [float(s) for s in svals.split(',')]
W, H = 1512, 850
shots = []
with sync_playwright() as p:
    b = p.chromium.launch(args=['--enable-gpu-rasterization'])
    pg = b.new_page(viewport={'width': W, 'height': H})
    pg.add_init_script("try{localStorage.setItem('8x_analytics_consent','denied')}catch(e){}")
    pg.goto(f'http://localhost:3200{path}', wait_until='networkidle')
    time.sleep(2)
    for s in svals:
        y = pg.evaluate(
            """([marker, mode, s]) => {
              const sec = [...document.querySelectorAll('section')].find(x => (x.innerText || '').startsWith(marker))
              let target
              if (mode === 'statement') {
                const top = sec.getBoundingClientRect().top + scrollY, Hs = sec.offsetHeight, vh = innerHeight
                const start = top - 0.8 * vh, range = Hs - vh + 0.8 * vh
                target = start + (0.52 + s * 0.48) * range
              } else {
                const pas = sec.nextElementSibling
                const top = pas.getBoundingClientRect().top + scrollY, Hs = pas.offsetHeight, vh = innerHeight
                target = top + (0.04 + s * 0.92) * (Hs - vh)
              }
              window.scrollTo(0, Math.round(target)); return Math.round(target)
            }""",
            [marker, mode, s],
        )
        time.sleep(0.9)
        f = Path(out).with_suffix(f'.{s:.2f}.png')
        pg.screenshot(path=str(f))
        shots.append(f)
    b.close()

tw, th = 756, 425
sheet = Image.new('RGB', (tw * 2, th * len(shots)), 'white')
d = ImageDraw.Draw(sheet)
for i, (t, f) in enumerate(zip(ttimes, shots)):
    ours = Image.open(f).convert('RGB').resize((tw, th))
    tf = sorted(Path(tdir).glob('*.png'))
    taiko = None
    if t >= 0:
        # disc frames were cut at 10fps starting from the folder's start time, encoded in its first line of meta
        idx = round((t - float(Path(tdir, 'start.txt').read_text())) * 10)
        taiko = Image.open(tf[idx]).convert('RGB').resize((tw, th))
        sheet.paste(taiko, (0, i * th))
    sheet.paste(ours, (tw, i * th))
    d.text((8, i * th + 8), f'taiko {t:.1f}s', fill=(255, 0, 0))
    d.text((tw + 8, i * th + 8), f'ours s={svals[i]:.2f}', fill=(255, 0, 0))
sheet.save(out, quality=86)
print(out)
