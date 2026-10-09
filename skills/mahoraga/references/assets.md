# Assets

What makes these sites land is real material: the client's own photos and films, generated photography that matches
the reference's grade, product screens drawn as pictures. Never ship gray boxes, stock-feeling icon tiles, or a
section that reads as a wall of text where the reference has an image.

## Order of preference

1. The client's own assets: logo (fetch the SVG; draw it inline with a tone prop), headshots (with permission),
   product screenshots, films and their stills, partner names. Ask once before downloading anything heavy and say
   what (file, source, size).
2. Generated photography in the reference's grade (Gemini, below).
3. Product UI drawn in code (screens, cards, charts, maps), filled with sample data labeled "Sample".
4. Generated motion (Veo/Omni) only where nothing has to line up with page geometry.

## Images with Gemini

`python scripts/gemini_image.py --out public/img/x.webp --prompt "..." --ref <capture> [--crop-ref x0,y0,x1,y1]`

- Pass the reference image, cropped to the part that matters, as an input. Words lose shape, proportion and grade;
  an image carries them. ("its simple bro yk u can send the reference image to gemini"; after nine failed text-only
  renders, the image-input version matched on the first try.)
- Prompt shape that worked for site photography: what the image is for and where its text card will sit ("the
  left half is a calm, softly blurred wall, because a text card will sit there"), the scene, lens and light, then
  "Match the photographic style of the reference image exactly: ... Do not copy the people in the reference; new
  people."
- Models: `gemini-3-pro-image` for hero photographs (2K, 16:9 or 4:3); `gemini-3.1-flash-image` for avatars and small
  items (1K, then `--resize 384x384`).
- Avatars: ask for a full-bleed square photo, "not a circle, no border, no interface element or icon anywhere".
  Otherwise the model draws a round crop with white corners and sometimes copies UI (a mic icon) from the reference.
- Cut-outs: render on solid chroma green and add `--chroma`; anything green itself (plants, a lime brand) goes on
  chroma blue with `--chroma blue`. Check edges against the real page background.
- Check every render side by side with the reference before building on it (`visual-fidelity`: the user judges by
  eye whether it looks physically plausible and seamless, not just close).
- **Requires a Gemini API key** (`GEMINI_API_KEY`, from https://aistudio.google.com/apikey; every call is billed).
  The scripts take it from the environment, else from a `GEMINI_API_KEY=...` line in the .env named by `--env` or
  `$MAHORAGA_ENV`, else `./.env`; without one they stop before calling anything and print how to set it.
  `python scripts/gemini_key.py` checks without printing the key. `local.md`, if present, says which .env holds it and
  whether test generations need asking first. Never print the key.

## Video

Client films (`find_media.py`, then `video_web.py`):
- `film`: H.264 CRF 26 + AAC 128k with faststart (careNext's 46MB launch film became 19.5MB).
- `loop`: a 5 to 8 second muted clip at 1280 wide for the card; `--crop-bottom 0.18` cuts a burned-in logo strip so
  your own title can sit on the frame.
- `poster` and `stills`: frames as WebP; stills from a client's film are excellent mock photography.
- Vimeo films play from Vimeo (their counts stay theirs); only the poster is local.

Generated video (Veo and Omni are Gemini API calls on the same `GEMINI_API_KEY`; if you keep notes on the Veo 3.1 and
Omni Flash APIs, read them first):
- Veo 3.1 (`models.generate_videos`, long-running): passing the same still as first and last frame gives a seamless
  loop; say the object "keeps exactly the same shape, size and position". 1080p, 4k and reference images need 8s.
  Make 3 or 4 takes and pick; there is no seed on the developer API.
- Omni Flash (Interactions API) for conversational edits of a clip ("Keep everything else the same.").
- Never put CSS filters on a playing video; bake tints into the file with ffmpeg.
- Motion in generated loops must cover the whole form (the user traced a light that skipped part of a figure-8), and
  the material itself should move, not a glint travelling over it.
- Veo cannot hold a cluster of small objects still: across 4 takes of an orb with ten porcelain objects around it,
  the objects spun edge-on, multiplied and warped, and water sloshed through the orb (8x Careers / Playmakers). Veo only
  the centrepiece: ask Gemini to remove the objects from the full composition (same place, same light), loop that
  orb alone (it wobbles like liquid glass beautifully), and keep the objects as keyed stills animated in the DOM on the
  video's clock (motion.md, "Objects around a video loop"). Drop the first 0.5s and crossfade the tail into it so the
  seam disappears; the poster is the encode's first frame.
- Veo letterboxes a still that is not exactly 16:9 (Gemini's 2752x1536 is 16:8.93): 4-5 black rows top and bottom
  plus a bright row inside them. Crop 10 rows and 18 columns off each side (still 16:9) and scale back before shipping,
  or the hero draws a black line along the top of the page. Check a poster's edge rows, not just its middle.
- Seamless loops from a still: `scripts/borrowed/gen_loop_omni.py` (same still first and last, a measured seam,
  crossfade fallback). Consistent faces across stills and loops: `scripts/borrowed/gen_face_loop_huly.py`.

## Silk and light fields

The background that made 8x.tweets and 8x Meets feel premium without a flat ground:
1. Generate 8s of Veo footage (iridescent silk in the palette, slow drift, no hard edges, nothing that must line up
   with the page). Make three takes, pick by eye.
2. `python scripts/video_web.py silk take.mp4 public/video/silk.mp4 --crop-edges 4`: crops Veo's black edge rows,
   slows 2x with motion interpolation, crossfades the tail into the head so it loops, denoises (`hqdn3d`) and encodes
   at CRF 23 with `aq-mode=3` so the gradients do not band. `--tint 24` bakes a turn toward rose for a second
   audience; `--night` makes the dark-theme twin (lightness inverted, hue kept).
3. A phone source: the same with `--width 1280`, served with `<source media="(max-width: 900px)">`. The poster is the
   first frame (`video_web.py poster silk.mp4 silk.webp --at 0`).
4. Markup: the poster as the panel's background, a muted `autoplay loop playsinline` video over it that fades in once
   it can play, a wash of the ground color where text sits, and poster only under reduced motion.

For a hero, where the field is the first thing seen at full width, `silk` is not enough (its 30fps resample and
denoise smear the rims, and a 1600px file is soft on big screens). Use `scripts/hero_loop.py` instead (8x Comment
Desk, 2026-10-04):
1. Veo 3.1 at `resolution: "4k"` over REST (the key in an `x-goog-api-key` header), the same still as `image` and `lastFrame`
   (`{"bytesBase64Encoded", "mimeType"}`; `inlineData` is refused). About 6 minutes a take; make three.
2. `python scripts/hero_loop.py out/ take.mp4`: cuts at the tail frame nearest frame 0 (Veo lands on the last frame
   about 8 frames early), slows 2x with motion-compensated interpolation at 24fps so every other frame is real, at
   each output's own size, then AV1 10-bit 2560x1440 (about 1 Mb/s), H.264 1080p (level 4.1, 4 refs), a portrait
   1080x1920 / 720x1280 cut of the centre, and the poster from the same first frame. Colour is tagged BT.709 on the
   frames (`setparams`): encoder flags wrote the matrix alone, and Chromium then decoded it as BT.601, off the poster.
3. Two takes joined (still to a mid pose and back) do not slow anything: Veo fills each 8s with as much motion.
4. Markup: the `<video>` in the server HTML with four `<source>`s (`type` with codecs, `media` on aspect ratio,
   `9/16`, ANDed with `prefers-reduced-motion: no-preference` so nothing loads under reduced motion), fade in on
   `playing` (check `!paused` on mount, since autoplay can start before hydration), pause off screen, and a
   `Cache-Control` rule for the files.

## Code-drawn product UI

- Mocks must be visual: a pay card, coverage icons, a photo with a status chip, a payment path with a moving dot,
  a score ring, a timeline, a map, faces. ("could u make the ui mocks visual?")
- Mocks must fill their frame with no empty band ("dont make it look empty yeah?"): give the screen a fixed height
  larger than the visible part, make it a flex column, and let a photo or map take the slack (`flex-1`).
- Product facts constrain samples (Doc360's max of 4 stars).
- Show the real device (see `direction.md`).

## Housekeeping

- Keep originals (raw headshots, raw films) in the scratchpad, not `public/`. Ship WebP images and web-encoded video.
- Image `sizes` attributes on every `next/image`; posters for every video.
- `scripts/make_grain.py` for the background grain tile.
