"""Generate the demo's media with Gemini.

    python scripts/gen_assets.py            # everything missing
    python scripts/gen_assets.py maya arch  # only these jobs (existing outputs are kept)

Pipeline per call participant: portrait -> webcam still (same person, via reference image)
-> seamless Omni loop (still used as first AND last frame). Outputs land in assets/.
"""
import base64, io, os, pathlib, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from google import genai
from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "assets"
RAW = ROOT.parent / "huly-assets-raw"  # full-size Gemini originals, kept outside the web root
ENV = pathlib.Path(os.environ.get("MAHORAGA_ENV", ".env"))  # a .env holding GEMINI_API_KEY; never print the key
key = next(l.split("=", 1)[1].strip() for l in ENV.read_text(encoding="utf-8-sig").splitlines()
           if l.startswith("GEMINI_API_KEY="))
client = genai.Client(api_key=key)

# The Interactions client retries up to 4x by default, including on dropped connections, which
# would re-run (and re-bill) a finished generation. Only 429/503 are retried below: never processed.
ix = client.interactions
rc = ix.sdk_configuration.retry_config
rc.max_retries, rc.retry_connection_errors = 0, False

PRO, NB2, OMNI = "gemini-3-pro-image", "gemini-3.1-flash-image", "gemini-omni-1.1-flash"

PEOPLE = {  # fictional team, reused across every mockup
    "maya": "a woman in her early 30s of East Asian descent with a short black bob, wearing a cream knit sweater",
    "theo": "a man in his late 20s of Latino descent with curly dark hair and light stubble, wearing a navy t-shirt",
    "priya": "a woman in her 30s of South Asian descent with long dark wavy hair, wearing a mustard blouse",
    "jonas": "a man in his 40s of Northern European descent with short blond hair and round glasses, wearing a grey henley",
    "amara": "a woman in her late 20s of West African descent with natural coily hair, wearing an emerald top",
    "luca": "a man in his 30s of Southern European descent with a trimmed dark beard, wearing a white linen shirt",
    "sofia": "a woman in her 50s with silver hair in a low bun, wearing a black turtleneck",
    "kenji": "a man in his 20s of Japanese descent with a textured fringe haircut, wearing a denim overshirt",
    "nadia": "a woman in her 30s of Middle Eastern descent with long dark hair, wearing a soft pink blouse",
    "omar": "a man in his 30s of North African descent with a shaved head and short beard, wearing an olive jacket",
}
CALLS = {  # participant -> (room behind them, what they do on the loop)
    "maya": ("a bright apartment with trailing plants and a bookshelf behind her", "talks warmly while explaining an idea with small hand gestures"),
    "theo": ("a cozy studio with warm lamps and a guitar hanging on the wall", "listens attentively, then nods slowly and smiles"),
    "amara": ("a minimal white room with a large window and sheer curtains", "laughs softly at something said, then keeps listening"),
    "jonas": ("a home office with a wooden shelf and framed prints", "listens thoughtfully, then nods in agreement"),
}
ICONS = {
    "icon-rooms": "a painter's palette with three glossy paint dabs in coral, blue and yellow, and a small brush",
    "icon-calls": "a rounded video camera with a soft glowing blue lens",
    "icon-guests": "an envelope with a round badge showing a plus sign",
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
                log(f"  {code} from API, backing off ({kw['model']})")
                time.sleep(10 * (attempt + 1))
                continue
            raise


def image(model, prompt, name, aspect="1:1", size="1K", refs=()):
    raw = RAW / f"{name}.jpg"
    if not raw.exists():
        blocks = [{"type": "image", "data": base64.b64encode(p.read_bytes()).decode(),
                   "mime_type": "image/png" if p.suffix == ".png" else "image/jpeg"} for p in refs]
        it = create(model=model, input=blocks + [{"type": "text", "text": prompt}],
                    response_format={"type": "image", "aspect_ratio": aspect, "image_size": size})
        if not it.output_image:
            raise RuntimeError(f"{name}: no image ({it.output_text!r})")
        raw.write_bytes(base64.b64decode(it.output_image.data))
        log(f"image  {name}")
    return raw


def save_webp(src, dst, size):
    im = ImageOps.fit(Image.open(src).convert("RGB"), size, Image.LANCZOS)  # center-crop to aspect, then scale
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.save(dst, "WEBP", quality=86, method=6)


def portrait(name):
    raw = image(NB2, f"Professional studio headshot photograph of {PEOPLE[name]}. Shoulders-up, facing the camera, "
                     "relaxed genuine smile, soft window light, plain light grey background, shallow depth of field, "
                     "natural skin texture, 85mm lens. No text, no watermark.", f"portrait-{name}")
    save_webp(raw, OUT / "people" / f"{name}.webp", (192, 192))
    return raw


def call(name):
    room, action = CALLS[name]
    face = portrait(name)
    still = image(PRO, f"Create a still frame from a laptop webcam during a video call, showing the same person as in the "
                       f"reference photo sitting at a desk in {room}. Framed from the chest up and centered, looking into "
                       "the camera, soft natural daylight, slightly soft focus like real webcam footage, realistic colors. "
                       "The image IS the camera feed, full-bleed edge to edge: no laptop, monitor, screen or bezel "
                       "visible. No text, no user interface, no watermark.", f"still-{name}", "16:9", "1K", refs=[face])
    save_webp(still, OUT / "calls" / f"{name}.webp", (640, 360))
    mp4 = OUT / "calls" / f"{name}.mp4"
    if not mp4.exists():
        it = create(model=OMNI,
                    input=[{"type": "image", "data": base64.b64encode(still.read_bytes()).decode(), "mime_type": "image/jpeg"},
                           {"type": "text", "text": "[# Sources <FIRST_FRAME>@Image1 <LAST_FRAME>@Image1] A person on a video "
                                                    f"call {action}. Static webcam framing, single continuous shot, no scene "
                                                    "cuts, subtle natural movement. No text. Use Image1 as the first frame "
                                                    "and the last frame."}],
                    response_format={"type": "video", "aspect_ratio": "16:9", "resolution": "360p"})
        if not it.output_video:
            raise RuntimeError(f"{name}: no video ({it.output_text!r})")
        tmp = RAW / f"call-{name}.mp4"
        tmp.write_bytes(base64.b64decode(it.output_video.data))
        # muted autoplay tiles: drop the audio track, move the index up front for instant start
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp), "-an", "-c:v", "copy",
                        "-movflags", "+faststart", str(mp4)], check=True)
        log(f"video  {name} ({mp4.stat().st_size // 1024} KB)")
    return mp4


def arch():
    raw = image(PRO, "Architectural photograph looking up at a modern glass-and-steel office building facade against a "
                     "clear blue sky, crisp geometric lines, bright midday light, cool blue reflections, a second tower "
                     "at the right edge. No people, no text, no logos.", "arch", "16:9", "2K")
    save_webp(raw, OUT / "doc-architecture.webp", (1600, 900))


def cover():
    raw = image(NB2, "Abstract close-up photograph of flowing warm amber and rose silk fabric folds in soft studio "
                     "light, shallow depth of field. No text.", "cover", "16:9", "1K")
    save_webp(raw, OUT / "card-cover.webp", (640, 360))


def icon(name):
    raw = image(PRO, f"A single glossy 3D app icon of {ICONS[name]}. Soft matte plastic and frosted glass materials, "
                     "gentle pastel colors, rendered in 3D, centered with generous margin, isolated on a pure white "
                     "background, soft studio lighting with a subtle contact shadow. No text.", name, "1:1", "1K")
    save_webp(raw, OUT / f"{name}.webp", (192, 192))


JOBS = {**{n: (call, n) for n in CALLS}, **{n: (portrait, n) for n in PEOPLE if n not in CALLS},
        "arch": (arch,), "cover": (cover,), **{n: (icon, n) for n in ICONS}}

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
                log(f"FAIL  {futs[f]}: {type(e).__name__}: {str(e)[:300]}")
    log("done", "- failed:" if failed else "- all ok", " ".join(failed))
