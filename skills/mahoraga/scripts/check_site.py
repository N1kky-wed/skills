"""Health check for a built site: every route's status, console errors, horizontal overflow, frame rate at rest and
while wheel-scrolling, and whether a wheel scroll that starts over the hero actually moves the page.

    python check_site.py http://localhost:3000 --paths / /about /pricing /nope
    python check_site.py https://site.vercel.app --paths / --perf

"/nope" should come back 404. Any route with pageerrors, console errors or overflow-x needs fixing before you
show it. --perf adds the scroll test: 60fps and a full-distance scroll are the bar (a hero that eats the wheel, or a
page that stalls entering the next section, reads to the user as "I can't even scroll").
"""
import argparse, sys, time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', errors='replace')  # page text is rarely ASCII; Windows pipes default to cp1252

FPS = """() => new Promise(res => { let n = 0; const t0 = performance.now(); let worst = 0, last = t0;
  const f = (t) => { n++; worst = Math.max(worst, t - last); last = t;
    if (t - t0 < 2000) requestAnimationFrame(f); else res({ fps: Math.round(n / ((t - t0) / 1000)), worstFrameMs: Math.round(worst) }) };
  requestAnimationFrame(f) })"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('base')
    ap.add_argument('--paths', nargs='*', default=['/'])
    ap.add_argument('--perf', action='store_true')
    ap.add_argument('--phone', action='store_true')
    a = ap.parse_args()
    size = dict(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True, has_touch=True) if a.phone else dict(viewport={'width': 1440, 'height': 900})
    bad = 0
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(**size)
        errs = []
        pg.on('pageerror', lambda e: errs.append('pageerror ' + str(e)[:160]))
        pg.on('console', lambda m: errs.append('console ' + m.text[:160]) if m.type == 'error' else None)
        for p in a.paths:
            errs.clear()
            r = pg.goto(a.base.rstrip('/') + p, wait_until='networkidle', timeout=180000)
            time.sleep(1)
            # against the set width, not innerWidth: mobile emulation zooms out to fit overflow, so innerWidth grows with it
            over = pg.evaluate(f"document.documentElement.scrollWidth > {size['viewport']['width']} + 1")
            real_errs = [e for e in errs if not ('404' in e and p == '/nope')]
            flag = 'OK ' if (r and r.status < 400 or p == '/nope') and not real_errs and not over else 'BAD'
            bad += flag == 'BAD'
            print(flag, r.status if r else None, p, 'overflow-x' if over else '', ' | '.join(real_errs[:3]))
        if a.perf:
            pg.goto(a.base.rstrip('/') + a.paths[0], wait_until='networkidle', timeout=180000)
            time.sleep(2)
            rest = pg.evaluate(FPS)
            pg.mouse.move(size['viewport']['width'] // 2, int(size['viewport']['height'] * 0.6))
            task = pg.evaluate_handle(FPS)
            for _ in range(10):
                pg.mouse.wheel(0, 120)
                time.sleep(0.1)
            scrolling = task.json_value()
            time.sleep(0.6)
            y = pg.evaluate('scrollY')
            print(f'perf: rest {rest}, scrolling {scrolling}, scrollY after 1200px of wheel over the hero: {y}')
            bad += y < 1000 or scrolling['fps'] < 45
        br.close()
    print('ALL GOOD' if not bad else f'{bad} problem(s)')


if __name__ == '__main__':
    main()
