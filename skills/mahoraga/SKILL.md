---
name: mahoraga
description: The user's own design + research + asset pipeline for building, redesigning or pitching websites, landing pages and app UI, distilled from the sites built together (8x.tweets, the huly hero recreation, 8x.karma, the 8x meetings platform, the Kivo app, the careNext redesign). Use it whenever the user asks to build, redesign, restyle, rework or pitch a website, landing page, hero section or app screen; to match or recreate a Dribbble, Behance, Awwwards or live-site reference ("make it like this", "i love this" + a link); to generate imagery, video loops or visuals for a site; to research design inspiration; to make transitions or motion smoother; or to deploy a site to share, even if they never say "design". Also use it whenever the user says "mahoraga".
---

# Mahoraga

Mahoraga adapts: every hit it takes becomes a resistance it keeps. This skill is that wheel for web work. Each rule in
it is a correction the user made on a real site, written down so it never has to be made twice. Follow the loop
below, open the reference file for the stage you are in, and add to `references/taste.md` whenever the user corrects
something new.

Paths below are relative to this skill's folder. Scripts are Python (the user prefers Python) and are
run as `python <skill>/scripts/<name>.py`; each has its usage in its docstring.

## Before anything

If `local.md` sits next to this file, read it: it holds this machine's setup (the Gemini key file, the
git identity, the deploy scope, where past projects live, folders that are off limits). It is not committed; start
one from `local.example.md`.

Then read `references/taste.md`. It is short and it is the difference between work the user keeps and work they bounce.
The ones broken most often:

- No design boards or mockup canvases of your own options. Build the real thing in code, show real screenshots, git
  is the undo. (A page of ten references in the pane is different: it is how a direction gets chosen.)
- Research in the browser pane where the user can watch; a link they answer with beats any direction you had.
- Backgrounds are never plain, and visuals beat text: mocks are pictures, and they fill their frames.
- Show products in their real form (a website in a browser window, not a phone).
- Redesigns keep the client's copy word for word; nothing invented; samples labeled.
- Motion is smooth and never blocks scrolling: compositor-only, measured.
- Grids have no holes and pages have no empty space.

## The loop

Keep the user posted with one-line status updates as you go; long silent stretches read as stalls.

### 1. Research (`references/research.md`)
- For a redesign: open the site in the pane, find what is broken (console errors, blank sections), then
  `scripts/capture_site.py` for every page's copy (including collapsed FAQ answers and bios), images, colors, fonts and
  media; `scripts/find_media.py` for their films (check their Vimeo/YouTube account too).
- Scan 5 to 8 category leaders and a Dribbble search in the pane; name the category defaults you will refuse.
- Ask one round of at most three questions with AskUserQuestion (purpose, audience, what of the brand survives).

### 2. Direction (`references/direction.md`)
- If the user pins a reference: capture it at 2x (`scripts/capture_reference.py`), measure its palette
  (`scripts/palette.py`), identify its type and signature details, map its sections onto the real content, say the
  mapping in a few lines, then build.
- If not, the default is the ten-reference page: pull wide Dribbble searches (`scripts/dribbble_pull.py`: the
  category, popular web design, strong heroes beyond the category), pick ten heroes that are each a different
  direction, build them into one numbered page (`scripts/refs_page.py`) with a line each on what it becomes for this
  project, serve it, open it in the pane and ask for a number (or two to mix, or their own link). The pick becomes the
  pinned reference above.
- Copy rules, device truth and pitch hygiene are in that file.

### 3. Assets (`references/assets.md`)
- Client assets first (logo drawn inline, real faces only with permission, their films and stills).
- Generated photography with the reference passed in as an image: `scripts/gemini_image.py --ref`.
- Films: `scripts/video_web.py` (web encode, muted loop with the logo strip cropped, poster, stills).
- Product UI drawn in code with sample data that respects product facts.

### 4. Build (`references/build-verify-deploy.md`, `references/motion.md`, `references/app-ui.md`)
- Next.js + Tailwind v4 + motion; measured tokens; verbatim content modules.
- Start from `assets/templates/`: `motion.css` (scroll-linked reveals, pinned hero, page transitions, marquee, grain),
  `film.tsx` (opens to full screen), `page-shell.tsx`, `browser-window.tsx`, `words.tsx`, `count-up.tsx`.
- Give the site a signature transition (the pinned hero receding under the next sheet, pages rising as a rounded
  sheet, films opening from their place) and vary how sections enter.
- App screens: rails widen in place, skeletons on click, instant press feedback, 1600px pages, no holes.

### 5. Verify (two rounds at most)
- Type-check and production build; `scripts/check_site.py --perf` over every route; `scripts/tour.py` desktop and
  phone (never trust full-page shots on scroll-linked pages); script the key interactions.
- Fix everything a round shows in one batch, confirm once, stop polishing.
- Send the user real screenshots (SendUserFile) and keep the pane on the running site.

### 6. Ship
- Commit as the user (identity and format in `build-verify-deploy.md`).
- Deploy with the Vercel CLI to the scope the user names, verify the public alias, hand over the clean link.

### 7. Turn the wheel
- When the user corrects something, fix it, then add the rule (with their words and why) to `references/taste.md`,
  and to memory if it is about one project. A correction made twice is a failure of this step.

## Scripts

| Script | Purpose |
|---|---|
| `capture_site.py` | Every page of a live site: copy (visible and hidden), images, colors, fonts, media, desktop+phone shots |
| `find_media.py` | Videos in a site's HTML and on its Vimeo account: titles, lengths, descriptions, posters |
| `dribbble_pull.py` | A Dribbble search (or popular feed) at 800px plus a numbered contact sheet, for reading many shots |
| `refs_page.py` | The ten-reference page: numbered heroes at 1600px with a line each on what they become here |
| `capture_reference.py` | A design reference's images at 2x as your own screenshots |
| `palette.py` | Exact colors at points and the dominant palette of a capture |
| `gemini_image.py` | Gemini image generation with reference images, aspect, size, resize, chroma-key |
| `video_web.py` | probe, web film, muted loop, poster, stills (with logo-strip crop), `silk` background loops |
| `hero_loop.py` | A 4K Veo take into a hero loop: seam cut, 2x at 24fps, AV1 + H.264, portrait cut, poster |
| `make_grain.py` | The baked grain tile for color fields |
| `tour.py` | Scroll-through viewport screenshots as one sheet, desktop or phone |
| `check_site.py` | Route statuses, console errors, overflow, frame rate, wheel-scroll test |

`scripts/borrowed/` holds proven scripts from past sites (seamless Omni loops, one face across stills and loops,
fitting a shape to a reference's frames, font matching, theme captures, contrast-safe identity colors, a mocked
realtime SDK for app checks); its README says what each does. They carry their old project's paths, so read and adapt
rather than run blind. `assets/examples/` holds three complete DESIGN.md files (8x.tweets, huly, 8x Meets) as models
for writing one, the measured WebGL beam, and taste rules written as tests.

## Reference files

- `references/taste.md`: the user's rules across every site, with the words they used. Read first, every time.
- `references/research.md`: the pane workflow, capturing a live site, finding films, the category scan, the questions.
- `references/direction.md`: pinned references, committed directions, copy rules, device truth, pitch hygiene.
- `references/assets.md`: client assets, Gemini images, video, code-drawn product UI.
- `references/motion.md`: performance rules, scroll-linked reveals, pinned hero, page transitions, slider, film.
- `references/app-ui.md`: app screens (rails, skeletons, messages, color meaning, two themes, rooms, verifying an
  app), learned on the Kivo app, 8x.karma and 8x Meets.
- `references/projects.md`: what each past site was, what worked, where its code lives (for borrowing).
- `references/build-verify-deploy.md`: stack, Windows quirks, the verify loop, commits, Vercel.
