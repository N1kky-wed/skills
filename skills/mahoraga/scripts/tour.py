"""See a page the way a visitor does: scroll it, shoot the viewport at each stop, and lay the shots out as one sheet.
Use this instead of full-page screenshots whenever the page has scroll-linked motion (view() timelines, sticky
heroes): a full-page capture renders everything at one scroll position and lies about what people see.

    python tour.py http://localhost:3000/ OUT_DIR --name home                 # desktop 1440x900
    python tour.py http://localhost:3000/ OUT_DIR --name home --phone --step 1400
    python tour.py https://site.vercel.app/about OUT_DIR --name about --step 900

Read the sheet (OUT_DIR/<name>-<desk|phone>-tour.jpg) and look for: blank or half-revealed sections, text over busy
images, empty bands inside mock frames, overlapping cards, things cut off at the page end.
"""
import argparse, os, time
from playwright.sync_api import sync_playwright
from PIL import Image


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('url')
    ap.add_argument('out')
    ap.add_argument('--name', default='page')
    ap.add_argument('--phone', action='store_true')
    ap.add_argument('--step', type=int)
    ap.add_argument('--settle', type=float, default=0.45)
    a = ap.parse_args()
    kind = 'phone' if a.phone else 'desk'
    step = a.step or (700 if a.phone else 760)
    os.makedirs(a.out, exist_ok=True)
    size = dict(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True) if a.phone else dict(viewport={'width': 1440, 'height': 900})

    shots = []
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(**size)
        pg.goto(a.url, wait_until='networkidle', timeout=180000)
        time.sleep(1.5)
        h = pg.evaluate('document.documentElement.scrollHeight')
        y = 0
        while y < h:
            pg.evaluate(f'window.scrollTo(0,{y})')
            time.sleep(a.settle)
            f = os.path.join(a.out, f'{a.name}-{kind}-{len(shots):02d}.png')
            pg.screenshot(path=f)
            shots.append(f)
            y += step
        # always include the very bottom: ranges that cannot complete at the page end show up here
        pg.evaluate('window.scrollTo(0, document.documentElement.scrollHeight)')
        time.sleep(a.settle + 0.4)
        f = os.path.join(a.out, f'{a.name}-{kind}-end.png')
        pg.screenshot(path=f)
        shots.append(f)
        br.close()

    tw = 220 if a.phone else 480
    tiles = [Image.open(f).convert('RGB') for f in shots]
    tiles = [t.resize((tw, int(t.size[1] * tw / t.size[0]))) for t in tiles]
    cols = 6 if a.phone else 4
    rows = (len(tiles) + cols - 1) // cols
    th = tiles[0].size[1]
    sheet = Image.new('RGB', (cols * (tw + 8), rows * (th + 8)), (40, 40, 40))
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % cols) * (tw + 8), (i // cols) * (th + 8)))
    out = os.path.join(a.out, f'{a.name}-{kind}-tour.jpg')
    sheet.save(out, quality=82)
    print(out, len(shots))


if __name__ == '__main__':
    main()
