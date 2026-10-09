"""Extract a reference's frames at a given rate and time range, cropped to the browser content, into labelled
contact sheets.

usage: python ref_frames.py <start> <end> <fps> <out_prefix> [cols] [thumb_w]

Reads the screen recording 00.mp4 in FRAMES_DIR (default: the folder you run from) and writes the frames and sheets
there. The crop (1512x850 at 44,175) is the browser content of the original Taiko recording: measure your own.
"""
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def label_font(size):
    try:
        return ImageFont.truetype('arial.ttf', size)
    except OSError:  # no Arial (Linux, some macOS setups): Pillow's own font
        return ImageFont.load_default(size)


HERE = Path(os.environ.get('FRAMES_DIR', '.'))
start, end, fps, prefix = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
cols = int(sys.argv[5]) if len(sys.argv) > 5 else 6
tw = int(sys.argv[6]) if len(sys.argv) > 6 else 480
out = HERE / f'{prefix}-raw'
out.mkdir(exist_ok=True)
for f in out.glob('*.png'):
    f.unlink()
subprocess.run(
    ['ffmpeg', '-v', 'error', '-ss', str(start), '-t', str(end - start), '-i', str(HERE / '00.mp4'),
     '-vf', f'fps={fps},crop=1512:850:44:175', str(out / '%04d.png')],
    check=True,
)
frames = sorted(out.glob('*.png'))
th = round(tw * 850 / 1512)
font = label_font(16)
per = cols * 5
for s in range(0, len(frames), per):
    chunk = frames[s:s + per]
    rows = (len(chunk) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * tw, rows * (th + 22)), 'white')
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(chunk):
        t = start + (s + i) / fps
        im = Image.open(f).convert('RGB').resize((tw, th), Image.LANCZOS)
        x, y = (i % cols) * tw, (i // cols) * (th + 22)
        sheet.paste(im, (x, y))
        d.rectangle([x, y, x + tw - 1, y + th - 1], outline=(200, 200, 200))
        d.text((x + 4, y + th + 2), f'{t:.2f}s', fill=(0, 0, 0), font=font)
    p = HERE / f'{prefix}-sheet-{s // per:02d}.jpg'
    sheet.save(p, quality=86)
    print(p.name, len(chunk))
