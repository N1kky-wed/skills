# App UI

Operate surfaces: dashboards, rails, inboxes and messages, settings, the sign-in door, a meeting room, an archive.
Learned on the Kivo/8x.tweets app (`x-marketplace`), 8x.karma (`8x-reddit`) and 8x Meets (`8x-gmeet`). The landing's
look carries in, quieter: the brand lives in precise details while scanability and speed lead.

## Feel fast ("feel fucking fast")

- Every route segment gets a `loading.tsx` with a skeleton shaped like the page, so a click shows the next page's
  frame at once instead of a wait (`x-marketplace/src/components/app/Skeleton.tsx`).
- Every control reacts on press: a global `:where(button, a, [role=button]):active { transform: scale(.975) }`
  (zero specificity, so components can override), and submit buttons swap to a spinner while pending (`Submit.tsx`).
- Use the width: pages run to 1600px (`u.page`), not a narrow column on a 1900px screen. Reading-heavy pages (an
  archive, settings) can sit in a ~1240px column; a room or editor goes full bleed.
- No decoration that costs clarity: blurry striped spheres in empty states and redundant chrome (a Brand/Creator pill)
  were removed on request.

## Rails and drawers

- A collapsible rail widens in place and the page slides over to make room. Never a sheet or overlay sidebar floating
  over the page ("creates a weird overlay side bar"): the rail has no surface of its own; it bleeds into the ground.
- Open and close must both feel smooth (it was "laggy", and it "collapses instantly"). What worked: the grid column
  snaps once, the rail's own width animates, the page glides with a FLIP translate on the compositor. Open 260ms after
  50ms on an expo ease-out; close 300ms after 150ms on a standard ease. Hover or focus sets `data-peek`, which uses the
  real open layout, so nothing is cut off at the right edge.
- A tucked avatar needs a fixed 36px column (a global `img { max-width: 100% }` collapses it otherwise).
- Code: `x-marketplace/src/components/app/RailToggle.tsx`, `Shell.tsx`, `shell.module.css`;
  `8x-reddit/src/components/app-shell/app-rail.tsx`, `rail-pin.tsx`.

## Grids, cards, symmetry

- No holes: choose the column count from the item count, or span the first or last item; a 3-column grid holding 4
  cards was circled as broken.
- Lock the heights of paired cards so a row never jumps ("lock the height of the card and the quick action div").
- Merge what belongs together (profile with account, earnings with payouts) and drop groupings that add nothing.
- Numbers are numbers: engagement is a count, never a percentage (8x.tweets); a rate can rank things quietly.
- Containers step their radii down as they nest (34, 28, 26, 22, 20, 16, 14, 9 in Meets), so an inner shape is
  never rounder than its parent. If it can be pressed, it is a pill or a circle.

## Messages

- Messaging is full screen like LinkedIn's: the thread reaches the edges, the composer is pinned, no wasted band at
  the bottom.
- Bubbles are pills with one sharp corner toward the speaker (others `6px 18px 18px 18px`, yours
  `18px 6px 18px 18px`, yours in the action color on the right). A reply quotes and jumps to the original, which
  flashes a ring.

## Color carries meaning

From 8x Meets, worth keeping in any app:
- One action color: every primary button, send, switch-on, selected item. No action takes another color except red
  for leaving and deleting.
- Loud means live: red and amber carry state only (recording, live, leaving, your own muted mic, failing connection,
  a raised hand, caution).
- Identity colors (one per person, team, track) are assigned most distinct first and are never red, amber or green,
  so an identity can never read as a state. `scripts/borrowed/contrast_hues.py` finds a set that passes 4.5:1 in
  both themes. Set `--tc: var(--tN)` on the element and mix from it with `color-mix(in oklab, ...)`.
- Emphasis is a crisp ring (2 to 4.5px, often with a 2px surface gap), not a glow.

## Two themes, both first-class

- Every token is declared in `:root` and `[data-theme="dark"]`; a boot script in the head sets `data-theme` before
  first paint (saved choice, else the system's).
- Background video gets a night twin graded in the file (`video_web.py silk --night`), swapped by source, never a
  CSS filter. Glass over moving imagery, paper for reading.
- The switch runs a View Transition with the default cross-fade off and a circle of the new light growing from the
  pointer over 640ms.
- Every text pair clears 4.5:1 in both lights; check it, do not assume it.
- Capture every surface in both themes at desktop and phone (`scripts/borrowed/theme_shots.py`; Meets' bar was 15
  surfaces x 2 themes x 2 sizes = 60 captures) and read every one.

## Motion grammar for apps

- One easing (`cubic-bezier(.16, 1, .3, 1)`) at three durations: 160ms for color, 260ms for fades, shadows and
  presses, 420ms for lifts and panels.
- Entrances rise 14px from scale .98. Presses scale .985 (buttons) or .94 (round dock controls).
- Nothing auto-advances inside an app. Live dots pulse slowly; that is the whole budget.
- Reduced motion cuts transitions to ~0, unloads background video (the poster stays) and switches themes instantly.

## Media in apps

- Never crop a camera: each tile keeps its camera's aspect ratio; only camera-off cards are elastic (3:4 to 2:1).
  Meets' `justify()` tries every row split and scores area times evenness. A shared screen uses `contain`.
- Tiles already on screen keep their slots; newcomers fill vacated slots, so nobody jumps while talking.
- Creator cards are still photos in full cards; moving people only in full-scene film.

## The door (sign-in)

- The door is a designed surface, not a bare form: 8x.tweets shows the side's silk with the app (Desk) drawn in code;
  Meets shows a "studio" panel beside the card where voice lanes take turns going live.
- Code inputs are boxes that match the provider's code length (Supabase OTP 8 -> 8 boxes, `CodeBoxes.tsx`).

## Rules as tests

Turn the taste rules into checks that fail the build, so they never regress:
`assets/examples/em-dash.test.mts` (no em dashes in UI strings) and `assets/examples/palette-rules.test.mts` (only
token colors) from 8x.karma. Run them with `node --test`.

## Verify an app

- Seed a throwaway local database and a dev sign-in route; never touch production data from a test.
- Mock the realtime or third-party SDK so every state can be exercised offline (`scripts/borrowed/lk-mock.js` fakes
  LiveKit: cameras in both orientations, voices, a screen share, hands, chat; `meets_dev_run.py` is the local runner,
  `meets_func_checks.py` the scripted checks: theme switch and memory, player, seek, dedupe, hands, toasts).
- Walk the main flows through the UI with Playwright and assert on state (x-marketplace's `scripts/e2e.py`, 28
  steps); then the theme shots; then contrast.
