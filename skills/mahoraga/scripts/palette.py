"""Measure a reference's palette instead of guessing it.

    python palette.py shot.png                       # top 10 colors with share of the image
    python palette.py shot.png --points 200,250 650,250 400,160   # exact pixels (hero field, cards, text...)
    python palette.py shot.png --crop 0,0,1440,900 --k 12

Sample points on the parts that matter (the field at center and at the rim, card fills, button, text strokes) and
read gradients as two or three samples along their axis. Feed the hexes straight into the CSS tokens.
"""
import argparse
from PIL import Image


def hexc(rgb):
    return '#%02x%02x%02x' % rgb[:3]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('image')
    ap.add_argument('--points', nargs='*', default=[])
    ap.add_argument('--crop')
    ap.add_argument('--k', type=int, default=10)
    a = ap.parse_args()
    im = Image.open(a.image).convert('RGB')
    if a.crop:
        im = im.crop(tuple(int(v) for v in a.crop.split(',')))
    print('size', im.size)
    for p in a.points:
        x, y = (int(v) for v in p.split(','))
        print(f'  ({x},{y}) {hexc(im.getpixel((x, y)))}')
    q = im.quantize(colors=a.k, method=Image.Quantize.MEDIANCUT).convert('RGB')
    cols = sorted(q.getcolors(1 << 24), reverse=True)
    total = sum(c for c, _ in cols)
    print('top colors:')
    for c, rgb in cols[: a.k]:
        print(f'  {hexc(rgb)}  {100 * c / total:5.1f}%')


if __name__ == '__main__':
    main()
