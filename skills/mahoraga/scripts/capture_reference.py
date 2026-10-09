"""Capture a design reference (a Dribbble/Behance shot, an Awwwards site) at 2x so it can be studied, measured, and
passed to Gemini as an image input. Shoots each large image/video element on the page as its own file, plus the
first viewport. These are your own screenshots of a public page, not downloads of the author's files.

    python capture_reference.py https://dribbble.com/shots/123-name OUT_DIR [--prefix vitai] [--min-width 700]

Then: palette.py on the files for exact colors, and crop regions to pass to gemini_image.py --ref.
"""
import argparse, os, time
from playwright.sync_api import sync_playwright


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('url')
    ap.add_argument('out')
    ap.add_argument('--prefix', default='ref')
    ap.add_argument('--min-width', type=int, default=700)
    ap.add_argument('--max', type=int, default=12)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={'width': 1440, 'height': 1000}, device_scale_factor=2)
        pg.goto(a.url, wait_until='domcontentloaded', timeout=90000)
        time.sleep(5)
        for y in range(0, 12000, 500):
            pg.evaluate(f'window.scrollTo(0,{y})')
            time.sleep(0.2)
        pg.evaluate('window.scrollTo(0,0)')
        time.sleep(1)
        pg.screenshot(path=os.path.join(a.out, f'{a.prefix}-viewport.png'))
        n = 0
        for h in pg.query_selector_all('img, video, canvas'):
            box = h.bounding_box()
            if not box or box['width'] < a.min_width or box['height'] < 250:
                continue
            try:
                h.scroll_into_view_if_needed()
                time.sleep(1.2)
                n += 1
                path = os.path.join(a.out, f'{a.prefix}-{n}.png')
                h.screenshot(path=path)
                print(path, int(box['width']), int(box['height']))
            except Exception as e:
                print('skip', str(e)[:80])
            if n >= a.max:
                break
        br.close()


if __name__ == '__main__':
    main()
