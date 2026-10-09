"""Measure a reference's dark disc (Taiko's): per frame, the black core's boundary profile, a circle fit, and the rim
colours.

usage: python fit_circle.py <start> <end> <fps> <mode: top|bottom>

Reads the screen recording 00.mp4 in FRAMES_DIR (default: the folder you run from), as ref_frames.py does.
"""
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(os.environ.get('FRAMES_DIR', '.'))
start, end, fps, mode = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
out = HERE / f'disc-{mode}'
out.mkdir(exist_ok=True)
for f in out.glob('*.png'):
    f.unlink()
# content area below the nav: the site is 1512 x 850 at (44,175); skip the 40px nav strip
subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(start), '-t', str(end - start), '-i', str(HERE / '00.mp4'),
                '-vf', f'fps={fps},crop=1512:850:44:175', str(out / '%04d.png')], check=True)

W, H = 1512, 850
NAV = 44


def fit_circle(xs, ys):
    A = np.c_[2 * xs, 2 * ys, np.ones_like(xs)]
    b = xs ** 2 + ys ** 2
    (cx, cy, c), *_ = np.linalg.lstsq(A, b, rcond=None)
    return cx, cy, np.sqrt(c + cx ** 2 + cy ** 2)


for i, f in enumerate(sorted(out.glob('*.png'))):
    t = start + i / fps
    im = np.asarray(Image.open(f).convert('RGB')).astype(float)
    lum = im @ [0.299, 0.587, 0.114]
    sat = im.max(2) - im.min(2)
    core = lum < 40
    white = (lum > 247) & (sat < 10)
    cx_, cy_, gx, gy = [], [], [], []
    for x in range(8, W - 8, 16):
        if mode == 'top':
            y = H - 1
            if not core[y, x]:
                continue
            while y > NAV and core[y, x]:
                y -= 1
            yc = y
            while y > NAV and not white[y, x]:
                y -= 1
            yg = y
        else:
            y = NAV + 4
            if not core[y, x]:
                continue
            while y < H - 1 and core[y, x]:
                y += 1
            yc = y
            while y < H - 1 and not white[y, x]:
                y += 1
            yg = y
        if NAV + 4 < yc < H - 2:
            cx_.append(x); cy_.append(yc)
        if NAV + 4 < yg < H - 2:
            gx.append(x); gy.append(yg)
    line = f'{t:6.2f}s dark={core[NAV:].mean():.2f}'
    if len(cx_) > 6:
        a, b, r = fit_circle(np.array(cx_, float), np.array(cy_, float))
        line += f' | core n={len(cx_):2d} c=({a:5.0f},{b:6.0f}) R={r:5.0f} mid={cy_[len(cy_)//2]:4d}'
    if len(gx) > 6:
        a, b, r = fit_circle(np.array(gx, float), np.array(gy, float))
        line += f' | glow n={len(gx):2d} c=({a:5.0f},{b:6.0f}) R={r:5.0f}'
    print(line)

# rim colours along the centre column for one mid-transition frame
mid = sorted(out.glob('*.png'))[len(list(out.glob('*.png'))) // 2]
im = np.asarray(Image.open(mid).convert('RGB'))
print('rim along x=756 in', mid.name)
col = im[NAV:, 756]
for y in range(0, H - NAV, 12):
    r, g, b = col[y]
    print(f'  y={y + NAV:4d}  #{r:02x}{g:02x}{b:02x}')
