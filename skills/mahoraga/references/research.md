# Research

Research happens in the browser pane, in front of the user. They asked for it ("could u research in the browser
pane so i can also see?") and they steer from it: twice they answered a direction question with a link of their own,
and that link became the design. A background agent screenshotting headlessly is invisible to them; use headless
scripts only for measuring and bulk capture, after the user has seen the sites.

## 1. The existing site (redesigns and pitches)

1. Open it in the pane, screenshot the first viewport, scroll a few screens. Note what a visitor actually sees.
2. Check for breakage, because it is the strongest pitch material: read the console (`read_console_messages`,
   errors only) and probe suspicious blanks with `javascript_tool` (opacity, visibility of hero slides). careNext's
   homepage hero and its careSumerPAY page both rendered blank because a theme script threw (`k is not a function`).
3. Capture everything: `python scripts/capture_site.py <url> <scratch>/site` (desktop + phone full-page shots,
   visible text, deep text from `textContent` so collapsed FAQ answers and "Read More" bios come along, images,
   links, colors, fonts, media). Read `.deep.txt` files for copy; `.json` for structure.
4. Pages built from images: if a page's text capture is nearly empty, its copy is baked into images. Open those
   images in the pane (full size: strip the `-768x432` WordPress suffix) and transcribe them exactly.
5. Media: `python scripts/find_media.py --site <url> --paths ...` finds mp4/Vimeo/YouTube sources; then open their
   Vimeo/YouTube account page in the pane (it often holds more films than the site shows; careNext had six) and run
   `find_media.py --vimeo-ids ... --posters public/video` for titles, lengths, descriptions and posters.
6. Note contradictions and stale bits (a 14- vs 10-question survey, "Prime" vs "Patient", last post three years
   ago). Flag them; never silently fix someone else's facts.

## 2. The category scan

Visit 5 to 8 category leaders and closest analogs of each product (a doctor-grading product next to Garner and
Zocdoc; patient financing next to Cedar), plus a Dribbble search for the category ("healthcare landing page",
popular). For each, a screenshot and one line: hero composition, palette, type (read computed `fontFamily` with
`javascript_tool` where the site allows it), one thing worth taking. Decline cookie banners ("Reject"), never sign in.

Then pull Dribbble wide with `scripts/dribbble_pull.py` (the category, its analogs, popular web design, strong heroes
outside the category) and read the contact sheets yourself: these feed the ten-reference page in `direction.md`.
Write pulls to the scratchpad, never into the skill folder.

Then name the category defaults to avoid. For healthcare it was: smiling doctor photo or cut-out with floating stat
badges, teal/sage/forest green with cream and a serif display, phone mockups, generic icon tiles. Naming them is what
lets you refuse them on purpose.

Some sites refuse tool scripting (Dribbble returns "not approved for tool access" to `javascript_tool`): use
screenshots there, and `scripts/capture_reference.py` headlessly for 2x element captures.

## 3. The questions (one round, structured)

Ask with AskUserQuestion, at most three, only what changes the build. The ones that mattered:
- Purpose: pitch to win the client / they are a client / portfolio. (A pitch means a preview link, the client's own
  copy, no invented claims, a "concept" label.)
- Audience: who the first screen speaks to (careNext: both careSumers and providers, then split).
- Brand survival: logo + colors / logo only / nothing. (The user said "nothing", then "u can use the og logo": keep
  a door open to the original mark.)
- Stack only if not obvious; default is Next.js on Vercel.

Do not ask for aesthetic adjectives or colors. Show; let them react.

## 4. Present findings briefly

A short list: what is there now (with the breakage), the category defaults, and the plan. Then either the
user's pinned reference, or the ten-reference page in the pane (see `direction.md`).
