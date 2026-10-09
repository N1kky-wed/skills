"""Bake a film-grain tile for big color fields (backgrounds are never plain, but never pay for grain per frame).

    python make_grain.py public/img/grain.png [--ink 20,27,15] [--size 160]

Use with the .grain class in motion.css: a tiled PNG at normal blending is painted once with its section. Do not
use an SVG feTurbulence overlay with mix-blend-mode: blending a full-screen layer every frame is what made a page
stall at the hero-to-next-section boundary.
"""
import argparse, random
from PIL import Image


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('--ink', default='20,27,15', help='speck color r,g,b (use the page ink)')
    ap.add_argument('--size', type=int, default=160)
    a = ap.parse_args()
    r, g, b = (int(v) for v in a.ink.split(','))
    random.seed(7)
    im = Image.new('RGBA', (a.size, a.size), (0, 0, 0, 0))
    px = im.load()
    for y in range(a.size):
        for x in range(a.size):
            v = random.random()
            if v < 0.5:
                px[x, y] = (r, g, b, int(random.random() ** 2 * 26))
            elif v > 0.85:
                px[x, y] = (255, 255, 255, int(random.random() * 22))
    im.save(a.out, optimize=True)
    print('ok', a.out)


if __name__ == '__main__':
    main()
