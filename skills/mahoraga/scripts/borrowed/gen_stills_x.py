"""Generate the site's photographic material with Gemini: creator profile photos and product photos for posts.

    python scripts/gen_assets.py           # everything missing
    python scripts/gen_assets.py maya kbd  # only these jobs (existing outputs are kept)

Everything else on the site (posts, cards, charts, light) is drawn in code.
"""
import base64, os, pathlib, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from google import genai
from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "public"
RAW = ROOT.parent / "x-assets-raw"   # full-size originals, kept outside the web root
ENV = pathlib.Path(os.environ.get("MAHORAGA_ENV", ".env"))  # a .env holding GEMINI_API_KEY; never print the key
key = next(l.split("=", 1)[1].strip() for l in ENV.read_text(encoding="utf-8-sig").splitlines()
           if l.startswith("GEMINI_API_KEY="))
client = genai.Client(api_key=key)
# the Interactions client retries dropped connections by default, which can re-run (and re-bill) a finished
# generation; only 429/503 are retried below
ix = client.interactions
rc = ix.sdk_configuration.retry_config
rc.max_retries, rc.retry_connection_errors = 0, False
PRO, NB2 = "gemini-3-pro-image", "gemini-3.1-flash-image"

# fictional creators; the look of each profile photo
CREATORS = {
    "maya": "an East Asian woman in her late twenties with shoulder-length black hair and round glasses, warm smile, in a bright cafe with plants behind her",
    "marcus": "a Black man in his thirties with a short beard and a navy crewneck, apartment window with city dusk behind him",
    "priya": "a South Asian woman in her early thirties with long wavy hair and a grey hoodie, home office with a bookshelf behind her",
    "tomas": "a Latino man in his mid twenties with headphones around his neck, a softly blurred room with colored LED light behind him",
    "lena": "a Northern European woman in her early thirties with a blonde bob and a black turtleneck, against a plain white gallery wall",
    "aisha": "a Nigerian woman in her late twenties with long braids and a denim jacket, outdoors on a sunny city street",
    "kenji": "a Japanese man in his early thirties with short hair and a grey t-shirt, lit by a laptop screen in a dim room",
    "sofia": "a Spanish woman in her early thirties with dark curly hair and a canvas apron, behind a coffee bar",
    "jordan": "a mixed-race man in his late twenties with an athletic build and a black training shirt, softly blurred gym behind him",
    "noah": "a Korean-American man in his late thirties with an open-collar white shirt, bright modern office behind him",
    "zara": "a British Pakistani woman in her late twenties wearing a soft beige hijab, in a cozy bookshop",
    "leo": "a German man in his early thirties with stubble and a black hoodie, night city lights blurred behind him",
    "imani": "a Black woman in her mid thirties with natural curls and a camel blazer, beside a bright window",
    "ethan": "a white man in his early thirties in a baseball cap, stadium lights at dusk blurred behind him",
    "ryo": "a Japanese man in his late twenties holding a small film camera at chest height, street at golden hour behind him",
    "chloe": "a French woman in her late twenties with safety glasses pushed up on her head, a workshop with tools behind her",
}

# product photos the creators "post"; brands are fictional, so nothing may carry a real logo or readable text
MEDIA = {
    "kbd": "Overhead phone photo of a custom mechanical keyboard with smoky grey and white keycaps on a dark walnut desk, a small ceramic mug beside it, warm desk-lamp light, shallow depth of field.",
    "coffee": "Phone photo of a matte black coffee bag with no label next to a latte with leaf latte art on a pale stone counter, soft morning window light.",
    "ring": "Close-up phone photo of a runner's wrist wearing a slim matte black fitness band, early morning run on a coastal path, sunrise light, slight motion.",
    "desk": "Phone photo of a tidy desk from above: an open notebook with handwritten notes, a fountain pen, wireless earbuds case and a coffee cup, soft daylight.",
    "controller": "Phone photo of a sleek dark grey game controller resting on a wooden table in a dim living room, TV glow in the blurred background.",
}


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def create(**kw):
    for attempt in range(5):
        try:
            return ix.create(timeout=540, **kw)
        except Exception as e:
            code = getattr(e, "status_code", None) or (429 if "429" in str(e) else 503 if "503" in str(e) else None)
            if code in (429, 503) and attempt < 4:
                log(f"  {code}, backing off")
                time.sleep(10 * (attempt + 1))
                continue
            raise


def image(model, prompt, name, aspect, size="1K"):
    return image_ref(model, prompt, name, aspect, size)


def image_ref(model, prompt, name, aspect, size="1K", ref=None):
    """One still, cached in RAW by name; `ref` is an optional reference photo (identity, composition)."""
    raw = RAW / f"{name}.jpg"
    if not raw.exists():
        blocks = [{"type": "image", "data": base64.b64encode(ref.read_bytes()).decode(),
                   "mime_type": "image/png" if ref.suffix == ".png" else "image/jpeg"}] if ref else []
        it = create(model=model, input=blocks + [{"type": "text", "text": prompt}],
                    response_format={"type": "image", "aspect_ratio": aspect, "image_size": size})
        if not it.output_image:
            raise RuntimeError(f"{name}: no image ({it.output_text!r})")
        raw.write_bytes(base64.b64decode(it.output_image.data))
        log(f"image {name}")
    return raw


def save_webp(src, dst, size, quality=84):
    im = ImageOps.fit(Image.open(src).convert("RGB"), size, Image.LANCZOS)
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst, "WEBP", quality=quality, method=6)


def avatar(name):
    raw = image(NB2, f"Candid social media profile photo of {CREATORS[name]}. Framed head and shoulders, centered, looking at "
                     "the camera with a natural relaxed expression, shot on a phone, natural light, real skin texture, "
                     "realistic colors. Not a studio headshot. No text, no watermark.", f"avatar-{name}", "1:1")
    save_webp(raw, OUT / "avatars" / f"{name}.webp", (256, 256))


def media(name):
    raw = image(PRO, MEDIA[name] + " Realistic, natural colors, no text, no logos, no watermark.", f"media-{name}", "4:3")
    save_webp(raw, OUT / "media" / f"{name}.webp", (1200, 900), 80)


JOBS = {**{n: (avatar, n) for n in CREATORS}, **{n: (media, n) for n in MEDIA}}

if __name__ == "__main__":
    RAW.mkdir(parents=True, exist_ok=True)
    wanted = sys.argv[1:] or list(JOBS)
    failed = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futs = {pool.submit(JOBS[n][0], *JOBS[n][1:]): n for n in wanted}
        for f in as_completed(futs):
            try:
                f.result()
            except Exception as e:
                failed.append(futs[f])
                log(f"FAIL {futs[f]}: {type(e).__name__}: {str(e)[:300]}")
    log("done", "- failed: " + " ".join(failed) if failed else "- all ok")
