# Borrowed scripts

Working scripts lifted from past sites. They carry their original project's paths, prompts and sizes: read one, then
adapt it (or copy its approach into a fresh script) rather than running it blind. The ones that touch Gemini read
`GEMINI_API_KEY` from the .env file in `$MAHORAGA_ENV` (else `./.env`); never print the key. Folder paths come from
environment variables named at the top of each script.

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
