"""Generate site imagery with Gemini (Nano Banana), steered by reference images.

    python gemini_image.py --out public/img/hero.webp --prompt "..." --ref refs/vitai-2.png --aspect 16:9 --size 2K
    python gemini_image.py --out public/img/orb.png --prompt "... on a solid chroma green (#00ff00) background" --key
    python gemini_image.py --out public/img/ferns.webp --prompt "... on a solid chroma blue (#0000ff) background" --key blue
    python gemini_image.py --out a.webp --prompt "..." --ref crop.png --crop-ref 0,713,338,1043   # crop the ref first

Key: GEMINI_API_KEY from the environment, or --env <path to a .env file holding GEMINI_API_KEY=...>. Never print it.
Models: gemini-3-pro-image (best, world knowledge, text), gemini-3.1-flash-image (fast default, cheap avatars),
gemini-3.1-flash-lite-image (1K only). Sizes "512" (3.1 flash only), "1K", "2K", "4K" (uppercase K).
Aspect: 1:1 2:3 3:2 3:4 4:3 4:5 5:4 9:16 16:9 21:9. Output comes back JPEG; this saves by extension (.webp/.png/.jpg).

Why references: a written description loses shape, proportion and grade. Passing the cropped reference as an image
block carries them; say in the prompt what to keep (lighting, grade, style) and what to change (new people, layout).
--key turns a chroma-green render into an image with alpha (for cut-outs that sit on the page's own background);
--key blue does the same for a blue screen, which green subjects (plants, a lime brand) need.
Retries are off: a dropped call must not silently re-bill.
"""
import argparse, base64, io, os, sys, time
from PIL import Image


def load_key(env_path):
    if os.environ.get('GEMINI_API_KEY'):
        return
    if env_path and os.path.exists(env_path):
        for line in open(env_path, encoding='utf-8'):
            if line.startswith('GEMINI_API_KEY='):
                os.environ['GEMINI_API_KEY'] = line.split('=', 1)[1].strip().strip('"').strip("'")
                return
    sys.exit('GEMINI_API_KEY not set (export it or pass --env path/to/.env)')


def b64png(im):
    buf = io.BytesIO()
    im.save(buf, 'PNG')
    return base64.b64encode(buf.getvalue()).decode()


def chroma_key(im, screen='green', low=0.10, high=0.30):
    """Screen color to alpha, the recipe proven on 8x.tweets' silk "8": alpha from how far the screen channel exceeds
    the other two, eased with a smoothstep, then despill (that channel pulled down to the others' mean). Key before
    resizing: Pillow resizes RGBA premultiplied, so the edges stay clean. Despill mutes the screen's hue in the subject
    too, so green subjects (plants, a lime brand) go on a blue screen with --key blue."""
    import numpy as np
    a = np.asarray(im.convert('RGB')).astype(np.float32) / 255.0
    k = {'green': 1, 'blue': 2}[screen]
    o1, o2 = [a[..., i] for i in range(3) if i != k]
    t = np.clip((a[..., k] - np.maximum(o1, o2) - low) / (high - low), 0, 1)
    alpha = 1 - t * t * (3 - 2 * t)
    a[..., k] = np.minimum(a[..., k], (o1 + o2) / 2)
    out = np.concatenate([a, alpha[..., None]], -1)
    return Image.fromarray((out * 255).round().astype('uint8'), 'RGBA')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--prompt', required=True)
    ap.add_argument('--ref', action='append', default=[], help='reference image path (repeatable)')
    ap.add_argument('--crop-ref', help='x0,y0,x1,y1 crop applied to the first --ref')
    ap.add_argument('--model', default='gemini-3-pro-image')
    ap.add_argument('--aspect', default='16:9')
    ap.add_argument('--size', default='1K')
    ap.add_argument('--resize', help='WxH final size, e.g. 384x384 for avatars')
    ap.add_argument('--key', nargs='?', const='green', choices=['green', 'blue'],
                    help='screen color to alpha (default green; blue for green subjects)')
    ap.add_argument('--env', default=os.environ.get('MAHORAGA_ENV', '.env'),
                    help='a .env file holding GEMINI_API_KEY (default: $MAHORAGA_ENV, else ./.env)')
    ap.add_argument('--quality', type=int, default=84)
    a = ap.parse_args()

    load_key(a.env)
    from google import genai

    client = genai.Client()
    ix = client.interactions
    rc = ix.sdk_configuration.retry_config
    rc.max_retries, rc.retry_connection_errors = 0, False

    blocks = []
    for i, path in enumerate(a.ref):
        im = Image.open(path).convert('RGB')
        if i == 0 and a.crop_ref:
            im = im.crop(tuple(int(v) for v in a.crop_ref.split(',')))
        blocks.append({'type': 'image', 'data': b64png(im), 'mime_type': 'image/png'})
    blocks.append({'type': 'text', 'text': a.prompt})

    t = time.time()
    it = ix.create(
        model=a.model,
        input=blocks if a.ref else a.prompt,
        response_format={'type': 'image', 'aspect_ratio': a.aspect, 'image_size': a.size},
        timeout=300,
    )
    im = Image.open(io.BytesIO(base64.b64decode(it.output_image.data)))
    if a.key:
        im = chroma_key(im, a.key)
    if a.resize:
        w, h = (int(v) for v in a.resize.lower().split('x'))
        im = im.resize((w, h), Image.LANCZOS)
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    ext = os.path.splitext(a.out)[1].lower()
    if ext == '.webp':
        im.save(a.out, 'WEBP', quality=a.quality, exact=bool(a.key))  # exact keeps colour under transparent pixels
    elif ext in ('.jpg', '.jpeg'):
        im.convert('RGB').save(a.out, 'JPEG', quality=a.quality)
    else:
        im.save(a.out, 'PNG', optimize=True)
    print(f'ok {a.out} {im.size} {time.time() - t:.0f}s')


if __name__ == '__main__':
    main()
