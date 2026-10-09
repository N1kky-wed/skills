# Borrowed scripts

Working scripts lifted from past sites. Each was tuned to its own project (prompts, sizes, crops, routes): read one,
then adapt it (or copy its approach into a fresh script) rather than running it blind.

- **Files:** every script reads and writes in the folder you run it from, or in folders named by the environment
  variables its docstring lists (`SITE_DIR`, `RAW_DIR`, `WORK_DIR`, `FRAMES_DIR`, `MEETS_REPO`, ...). None writes
  into the skill folder.
- **Gemini API key:** `gen_stills_x.py`, `gen_loop_omni.py`, `gen_face_loop_huly.py` and `grade_portraits.py` call the
  Gemini API and need `GEMINI_API_KEY` (https://aistudio.google.com/apikey; calls are billed). They find it like
  `../gemini_image.py` does: the environment, then the .env named by `$MAHORAGA_ENV`, then `./.env`, and stop with
  setup instructions when there is none (`python ../gemini_key.py` checks). Never print the key. The other scripts
  need no key.
- **Running sites:** the page scripts open `BASE_URL` (default `http://localhost:3000`; the 8x Meets ones default to
  `meets_dev_run.py` on `http://127.0.0.1:5005`).
- **ffmpeg** on PATH for the video ones.

| Script | From | What it does |
|---|---|---|
| `gen_loop_omni.py` | 8x.tweets `scripts/gen_cinema.py` | Seamless Omni Flash loops: the same still as first and last frame, a numeric seam check (luma difference), crossfade fallback, ffmpeg encode, poster |
| `gen_stills_x.py` | 8x.tweets `scripts/gen_assets.py` | Batch Gemini stills (pro + flash), raw files kept outside the web root, retries only on 429/503, WebP export |
| `gen_face_loop_huly.py` | huly recreation `scripts/gen_assets.py` | Portrait, then a webcam still locked to that face, then an Omni loop, then a `+faststart` encode |
| `ref_frames.py` | 8x.karma research | Cut a screen recording of a reference into frame contact sheets |
| `fit_circle.py` | 8x.karma research | Measure a shape per frame with circle fits (the dome was fitted to Taiko's frames, mean error 9px) |
| `compare_frames.py` | 8x.karma research | Our build's frames next to the reference's, for side-by-side judgement |
| `font_compare.py` | 8x.karma research | Candidate fonts set beside a crop of the reference's lettering |
| `record_scroll.py` | 8x.karma | Record a scroll-through video of a page (WebGL needs the swiftshader flags) |
| `grade_portraits.py` | 8x.karma | Profile photos generated in one shared colour grade |
| `contrast_hues.py` | 8x meetings | Find N distinct hues that all pass 4.5:1 contrast in both themes |
| `theme_shots.py` | 8x meetings | Capture every surface in day and night themes, desktop and phone |
| `design_sidecar.py` | impeccable tooling | Build `design.json` from a DESIGN.md |
| `hero_media_sweep.py` | 8x Careers + Playmakers | 10-bit lossless masters from Veo takes (seamless, letterbox cropped) and a codec quality sweep scored by SSIM |
| `make_hero_media.py` | 8x Careers + Playmakers | AV1/HEVC/H.264 hero loops at 1080p+720p, AVIF/WebP posters, inline blur frame, hashed names and a TS manifest |
