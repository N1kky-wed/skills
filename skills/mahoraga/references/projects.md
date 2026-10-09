# Past projects

What each site was, what made it land, and where its code lives (folders are in `local.md`), so you can borrow a proven piece instead of
reinventing it. Read the code before copying: each piece was tuned to its own page. Never open `.env*` files in any of
these folders.

| Need | Borrow from |
|---|---|
| Pinned hero receding under the next sheet, scroll-linked reveals, page transitions | careNext `globals.css` (now `assets/templates/motion.css`) |
| A film card that opens to full screen | careNext `film.tsx` (now `assets/templates/film.tsx`) |
| Product UI drawn in code as the hero picture | 8x.tweets `Desk.tsx`; careNext `hero/screens.tsx` |
| Silk or light-field background video | 8x.tweets `SilkVideo` + `scripts/gen_cinema.py`; `video_web.py silk` |
| A reference visual recreated to measurement | huly `js/beam.js`; 8x.karma's dome fit |
| Day and night themes | 8x Meets `static/meets.css`, `templates/_head.html` |
| An app shell with a rail that widens in place | Kivo `RailToggle.tsx`, `Shell.tsx`; 8x.karma `app-shell/` |
| Generated faces that stay one person across stills and loops | huly `scripts/gen_assets.py` |

## careNext redesign (2026-10-02, pitch)

- `carenext-redesign`; live at https://carenext-redesign.vercel.app.
  Next.js 16 + Tailwind v4 + motion.
- Brief: redesign carenexthealth.com without its code, same copy word for word, pitched to careNext. The user pinned
  VitAI (dribbble.com/shots/27639760): lime field lit in the middle, cream sheets, ink, Manrope, hairlines with square
  nodes, giant footer wordmark.
- What landed: the hero as a slider of the four products in a browser window drawn in code (auto-advances while in
  view, pause button, no hover pause); the hero receding under the next sheet; scroll-linked reveals that vary by
  section; films (their Vimeo launch and demo films) opening from their card to full screen; real leadership faces;
  partners marquee.
- Corrections that became rules: device truth (the phone became a browser window), mocks visual and full, scrolling
  never blocked, footer not cut off, slider keeps moving when focused.
- Code: `src/app/globals.css`, `src/components/film.tsx`, `hero/{hero,screens,window}.tsx`, `home-sections.tsx`,
  `page-shell.tsx`, `src/content/*` (verbatim copy).

## 8x.tweets landing + the Kivo app (x-marketplace, 2026-09-25 to 10-01)

- `x-marketplace` (repo 8xsocial/8x-twitter, live www.8xtweet.com). Next.js,
  Postgres. `DESIGN.md` (copy in `assets/examples/DESIGN-8x-tweets.md`).
- Direction "Silk and Ledger": AIVENT's lilac world (dribbble.com/shots/27749479) after the team rejected a sky and a
  hand holding a phone. Ground `#f5f4fc`, ink `#272a3f`, violet `#6147c7` for every action, blue `#4d68d4` links,
  light blue in glows.
- Signatures: Veo silk slowed 2x, crossfaded into a loop, black edge rows cropped, a rose twin baked with
  `hue=h=24:s=1.06`, a 720p source for phones; the web app drawn in code (`Desk`, sized in container units) filling
  the hero stage and running off its bottom; full creator cards (photo edge to edge, frosted lower part); keyed glass
  objects (`sculpture-cut`, `orb-cut`); a posts marquee, the only thing that auto-advances.
- Rules born here: hero and close differ; brand and creator sides each get their own pictures and order; two-line
  desktop headline; no sky, phones, hands or status bars; nothing dark, cartoonish or mascot-like; still cards;
  engagement as numbers; no arrows on buttons; no CSS filters on video.
- Code: `src/components/landing/{Hero,Desk,Sections,AutoPlay,Motion,Words}.tsx`, `landing.module.css`,
  `desk.module.css`; app `src/components/app/{Shell,RailToggle,Skeleton,Submit,Inbox,Composer,cards,CodeBoxes}.tsx`;
  `scripts/gen_cinema.py` (loops, borrowed as `gen_loop_omni.py`), `scripts/gen_assets.py` (stills, `gen_stills_x.py`).

## 8x Meets, the meetings platform (8x-gmeet)

- `8x-gmeet`: Flask + vanilla JS on LiveKit (`app.py`, `templates/`, `static/meets.css`,
  `static/meets.js`). `DESIGN.md` (copy in `assets/examples/DESIGN-8x-meets.md`), `HANDOVER.md`.
- Direction "The Lilac Studio": a recording studio for conversations. Every voice is a track (a color, a lane, a
  ring); two lights (lilac day, violet-ink night) share one silk, the night file graded with
  `negate,hue=h=180:s=1.15,eq=gamma=0.85:contrast=1.08` and encoded with `hqdn3d=1.5:1.5:4:4`, CRF 23, `aq-mode=3`.
- Signatures: the speaking ring (the silk gradient masked to a 3px frame); the stage's `justify()` gallery that keeps
  every camera's aspect; a glass dock; archive "voice posters" and a who-spoke-when timeline per speaker color; the
  door's studio panel; a canvas lobby game themed per light.
- Rules: Violet Acts, Loud Means Live, the Track rule (never red, amber or green), Ring Not Glow, Glass Over Motion,
  Mono Means Measured, sentence case, light display type (300).
- Quality bar: 60 theme captures, 21 functional checks with LiveKit mocked, every text pair at 4.5:1 in both lights.
  Harness: `scripts/borrowed/meets_dev_run.py`, `lk-mock.js`, `meets_func_checks.py`, `theme_shots.py`,
  `contrast_hues.py`.

## 8x.karma (8x-reddit)

- `8x-reddit-main`: Next.js (pnpm), i18n messages, Sentry. `DESIGN.md`.
- Direction: the reference landing the user pinned (Taiko's) rebuilt in Reddit's colors. Its dome was fitted to the
  reference's frames (circle fits per frame, mean error 9px) and its type matched by setting candidate fonts beside a
  crop of the original.
- Signatures: a three.js upvote (`karma/upvote-3d.tsx`), hero ribbons, a pinned showcase with tabs, a fan of people
  in one shared portrait grade.
- Rules as tests: `src/em-dash.test.mts`, `src/palette-rules.test.mts` (copies in `assets/examples/`).
- Tools: `scripts/borrowed/{ref_frames,fit_circle,compare_frames,font_compare,record_scroll,grade_portraits}.py`.

## The huly hero recreation (huly-recreation, 2026-09-26)

- `huly-recreation`: static HTML (`index.html`, `css/`, `js/beam.js`,
  `js/main.js`). `DESIGN.md` ("The Lit Workbench", copy in `assets/examples/DESIGN-huly-lumora.md`).
- Brief: recreate huly.io's hero light over a flat app mockup. Generated video looked great alone but could not honor
  the mock's geometry (rim lines, a neon corner, a floating shelf), so the light became WebGL fitted to measured
  cross-sections: a rounded-box SDF so it follows the mock's outline, fbm haze, rendered at 0.6x device pixels
  (`assets/examples/beam-fitted-webgl.js`).
- Rules: live-only (pause motion off-screen via `[data-live]` and an IntersectionObserver); under reduced motion show
  the answered, finished state rather than nothing.
- Faces: portrait, then a webcam still locked to that face by passing the portrait in, then an Omni loop with the still
  as first and last frame (`scripts/borrowed/gen_face_loop_huly.py`).
