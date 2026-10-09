"""The cinematic layer: one cast, one lighting language (warm ember key from the creators' side, cool cobalt rim from
the brands' side, pitch-black studio, haze), carried through stills and seamless loops.

    python gen_loop_omni.py            # everything missing
    python gen_loop_omni.py maya hero  # only these jobs

Needs GEMINI_API_KEY (see ../gemini_key.py; each call is billed) and ffmpeg on PATH. Shares the client, folders
(SITE_DIR, RAW_DIR) and avatar stills of gen_stills_x.py, which it imports. Stills: Nano Banana Pro. Loops: Gemini Omni with the still as first AND last frame; when a clip opens off-still
anyway, the loop is cut from its settled stretch and the tail crossfaded into the frames before that start.
"""
import base64, pathlib, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed

import av
import numpy as np
from PIL import Image, ImageOps

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import gen_stills_x as g   # client, retries, RAW/OUT, avatar images

OMNI = "gemini-omni-1.1-flash"
LIGHT = ("Shot in a pitch-black studio: a warm ember-orange key light from the left, a cool cobalt-blue rim light from "
         "the right, faint haze in the air, deep black background, cinematic, shallow depth of field, subtle film grain, "
         "high-end editorial campaign photography.")

# creators who get a gel-lit portrait (the avatar anchors identity); pose per person
CAST = {
    "maya": "looking down at her phone, its glow lighting her face, a small smile starting",
    "marcus": "looking straight into the camera, calm and confident, phone held loosely at his side",
    "aisha": "laughing mid-sentence, looking just past the camera",
    "tomas": "holding his phone up to film, eyes on the screen, headphones around his neck",
    "lena": "looking into the camera with a thoughtful half smile, chin slightly raised",
    "kenji": "typing on his phone with both thumbs, face lit by the screen",
    "priya": "looking up from her phone toward the camera, amused",
    "noah": "turned three quarters, looking into the camera, relaxed",
    "sofia": "holding a coffee cup near her face, looking into the camera, warm expression",
    "jordan": "looking into the camera with a slight grin, towel over his shoulder",
    "zara": "reading her phone, thoughtful, soft smile",
    "leo": "looking into the camera, serious and focused, hood down",
}

PRODUCTS = {
    "keyboard": "a custom mechanical keyboard with smoky grey and white keycaps",
    "coffee": "a matte black specialty coffee bag with a small blind-embossed circle and no text, a few coffee beans beside it",
    "band": "a slim matte black fitness band floating at a slight angle",
    "controller": "a sleek dark grey game controller",
    "card": "a brushed dark titanium payment card with no text, numbers or logos, standing on its edge",
}


def omni_loop(still: pathlib.Path, motion: str, name: str, aspect: str, res: str, size: tuple[int, int]) -> pathlib.Path:
    clip, mp4 = g.RAW / f"clip-{name}.mp4", g.OUT / "film" / f"{name}.mp4"
    if not clip.exists():
        it = g.create(model=OMNI,
                      input=[{"type": "image", "data": base64.b64encode(still.read_bytes()).decode(), "mime_type": "image/jpeg"},
                             {"type": "text", "text": "[# Sources <FIRST_FRAME>@Image1 <LAST_FRAME>@Image1] " + motion +
                              " Completely static camera, single continuous shot, no scene cuts, seamless loop. No text, no "
                              "captions. Use Image1 as the first frame and the last frame."}],
                      response_format={"type": "video", "aspect_ratio": aspect, "resolution": res, "delivery": "uri"})
        vid = it.output_video
        if not vid:
            raise RuntimeError(f"{name}: no video ({it.output_text!r})")
        if getattr(vid, "data", None):
            clip.write_bytes(base64.b64decode(vid.data))
        else:
            fname = "files/" + re.search(r"files/([^:/?]+)", vid.uri).group(1)
            while (f := g.client.files.get(name=fname)).state.name != "ACTIVE":
                if f.state.name == "FAILED":
                    raise RuntimeError(f"{name}: file failed")
                time.sleep(5)
            g.client.files.download(file=vid.uri, destination=str(clip))
        g.log(f"clip {name}")
    if not mp4.exists():
        F = [f.to_ndarray(format="rgb24") for f in av.open(str(clip)).decode(video=0)]
        n = len(F)
        luma = [f.mean(axis=2)[::8, ::8].astype(np.float32) for f in F]
        step = float(np.median([np.abs(luma[i + 1] - luma[i]).mean() for i in range(n - 1)]))
        if np.abs(luma[0] - luma[-1]).mean() <= 2.5 * step + .5:
            loop = F                                   # the model honoured first = last: already seamless
        else:                                          # cut from the settled stretch, crossfade the tail into the start
            N = 30
            a = min(range(48, n - 3 * N), key=lambda i: np.abs(luma[i] - luma[-1]).mean())
            loop = F[a:n - N] + [((1 - (m + 1) / (N + 1)) * F[n - N + m].astype(np.float32) +
                                  (m + 1) / (N + 1) * F[a - N + m].astype(np.float32)).round().astype(np.uint8) for m in range(N)]
        h, w = loop[0].shape[:2]
        mp4.parent.mkdir(parents=True, exist_ok=True)
        enc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
                                "-r", "24", "-i", "-", "-an", "-vf", f"scale={size[0]}:{size[1]}:flags=lanczos",
                                "-c:v", "libx264", "-preset", "slow", "-crf", "24", "-pix_fmt", "yuv420p",
                                "-movflags", "+faststart", str(mp4)], stdin=subprocess.PIPE)
        for fr in loop:
            enc.stdin.write(fr.tobytes())
        enc.stdin.close()
        if enc.wait():
            raise RuntimeError(f"{name}: ffmpeg failed")
        poster = mp4.with_suffix(".webp")
        next(av.open(str(mp4)).decode(video=0)).to_image().save(poster, "WEBP", quality=80, method=6)
        g.log(f"loop {name} ({len(loop)} frames, {mp4.stat().st_size // 1024} KB)")
    return mp4


def cast(name):
    still = g.image_ref(g.PRO, f"Cinematic portrait of the same person as in the reference photo, {CAST[name]}. Framed from the "
                               f"waist up, centered, the person fills the frame. {LIGHT} Keep their face, hair and features "
                               "exactly as in the reference. No text, no logos.",
                        f"cast-{name}", "9:16", "2K", g.RAW / f"avatar-{name}.jpg")
    # stills only: on the page a creator is a card, and a card shows the profile photo they bring
    g.save_webp(still, g.OUT / "cast" / f"{name}.webp", (720, 1280), 82)


def hero():
    still = g.image_ref(g.PRO, "Wide cinematic frame of the same woman as in the reference photo, sitting on a low sofa in a "
                               "dark apartment at night, holding her phone in both hands, its glow lighting her face, a warm "
                               "ember-orange lamp glow from the left and cool cobalt-blue city light from a window on the right, "
                               "faint haze. She sits in the right third of the frame; the left half is deep, quiet darkness. "
                               "Shallow depth of field, subtle film grain, premium campaign film still. Keep her face and "
                               "features exactly as in the reference. No text, no logos.",
                        "hero-creator", "16:9", "2K", g.RAW / "avatar-maya.jpg")
    g.save_webp(still, g.OUT / "film" / "hero-creator-still.webp", (1920, 1080), 82)
    # the film carries only the phone's light (an earlier take drew fake notification cards), and the room's light holds
    # perfectly still: asking the lamp to "breathe" made Omni flicker it, which read as a pulse behind the Earnings heading
    omni_loop(still, "She scrolls her phone slowly and a quiet smile builds. The light in the room stays completely steady: "
                     "the lamp does not flicker, dim or breathe, and the city light in the window is constant. The only "
                     "change in light is the soft glow of her phone on her face. No graphics, no interface, no notification "
                     "cards, no floating elements anywhere in the frame.",
              "hero-creator", "16:9", "1080p", (1920, 1080))


def product(name):
    still = g.image(g.PRO, f"Premium product photograph of {PRODUCTS[name]} on a low black stone plinth. {LIGHT} Glossy "
                           "reflections, the product sharp and centered with generous dark space around it. No text, no "
                           "logos, no watermark.", f"product-{name}", "4:5", "2K")
    g.save_webp(still, g.OUT / "products" / f"{name}.webp", (960, 1200), 82)


def lights():
    still = g.image(g.PRO, "Two soft beams of light cut through drifting haze in a vast pitch-black space: a warm ember-orange "
                           "beam from the left and a cool cobalt-blue beam from the right, meeting at the center where they "
                           "blend into a gentle white glow, reflected on a glossy black floor. Minimal, cinematic, premium, "
                           "subtle film grain. No text, no objects, no people.", "lights", "16:9", "2K")
    g.save_webp(still, g.OUT / "film" / "lights-still.webp", (1920, 1080), 82)
    omni_loop(still, "The two beams sway slowly toward each other and apart through the drifting haze, the white glow where "
                     "they meet breathing gently; the reflections shimmer on the floor.", "lights", "16:9", "1080p", (1920, 1080))



def smoke():
    # the Market backdrop: the user kept the haze and dropped the beams, so this is the portraits' smoky room with no light shapes
    still = g.image(g.PRO, "Soft drifting smoke and haze filling a vast pitch-black studio, the same backdrop as a moody "
                           "editorial portrait session: warm ember-orange light tints the smoke from the left, cool cobalt-blue "
                           "tints it from the right, and the two blend softly in the middle. No light beams, no rays, no visible "
                           "light sources, no spotlights, no lens flares, no floor, no objects, no people, no text. Deep black "
                           "overall, low contrast, cinematic, subtle film grain.", "smoke", "16:9", "2K")
    g.save_webp(still, g.OUT / "film" / "smoke-still.webp", (1920, 1080), 82)
    omni_loop(still, "The smoke drifts and curls slowly through the dark, tinted ember from the left and cobalt from the "
                     "right. No beams, no rays, no flashes; the light stays soft and even.", "smoke", "16:9", "1080p", (1920, 1080))



def smoke_settled():
    # the user kept the smoke but not its opening push from the sides: loop the settled, swirling state instead,
    # starting and ending on a frame from the middle of the first take where the smoke already fills the room
    still = g.RAW / "smoke-settled.jpg"
    if not still.exists():
        frames = av.open(str(g.RAW / "clip-smoke.mp4")).decode(video=0)
        next(f for i, f in enumerate(frames) if i == 177).to_image().save(still, quality=95)
    omni_loop(still, "The smoke keeps curling and drifting slowly in place across the whole frame, tinted ember on the left "
                     "and cobalt on the right. Nothing new enters from the edges: no bursts, no puffs, no pushes; the "
                     "motion is slow and even and the smoke stays evenly spread.", "smoke-settled", "16:9", "1080p", (1920, 1080))


JOBS = {**{n: (cast, n) for n in CAST}, "hero": (hero,), **{f"p-{n}": (product, n) for n in PRODUCTS}, "lights": (lights,),
        "smoke": (smoke,), "smoke-settled": (smoke_settled,)}

if __name__ == "__main__":
    g.RAW.mkdir(parents=True, exist_ok=True)
    wanted = sys.argv[1:] or list(JOBS)
    failed = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        futs = {pool.submit(JOBS[n][0], *JOBS[n][1:]): n for n in wanted}
        for f in as_completed(futs):
            try:
                f.result()
            except Exception as e:
                failed.append(futs[f])
                g.log(f"FAIL {futs[f]}: {type(e).__name__}: {str(e)[:300]}")
    g.log("done", "- failed: " + " ".join(failed) if failed else "- all ok")
