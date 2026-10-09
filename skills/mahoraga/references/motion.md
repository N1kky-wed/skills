# Motion and transitions

The bar the user set: "really smooth transition", "better transitions", and never "I can't even scroll". Every
technique here was shipped and verified on a real site; the failures that taught each rule are noted, because they
are the ones that recur.

## Contents
1. The performance rules (read first)
2. Scroll-linked reveals (`data-reveal`)
3. The pinned hero that recedes under the next sheet
4. Page transitions (React ViewTransition, Next 16)
5. The hero slider
6. The film that opens to full screen
7. Small pieces: words, count-up, marquee, reading lines, moving dots
8. Verifying motion

## 1. Performance rules

These come from a page that "could not scroll past the hero". Each item was a measured cause.

- Animate only `transform`, `opacity` and (sparingly) `clip-path`. They stay on the compositor.
- No `filter: blur()` on large elements in reveals or transitions. Several big cards blurring in at once at the hero/next-section boundary is exactly where the page stalled. Small text lines can take a blur; cards, windows, full pages cannot.
- No full-screen `mix-blend-mode` overlays (an SVG-noise grain blended `soft-light` over every section). Bake the grain into a PNG (`scripts/make_grain.py`) and lay it at normal blending; it is painted once.
- Decorative glows are `radial-gradient` backgrounds, not `blur-3xl` discs (a 64px blur filter repaints).
- Progress bars scale (`scaleX` with `origin-left`), never animate `width` (that is a layout per frame).
- No `scroll-behavior: smooth` on `html`. Next warns about it and it fights route scrolling.
- Scroll-linked ranges must be reachable. A range that ends in `cover` on the last element of a page can never complete (the page cannot scroll that far), so the footer logo stayed half inside its mask. End such ranges in `entry` (`entry 0% entry 100%`).
- Respect `prefers-reduced-motion`: switch scroll-linked animations off (`animation: none !important`) rather than shortening them.
- Big composited layers are fine; big repaints are not. Measure with `scripts/check_site.py --perf` (60fps at rest and while wheel-scrolling, full scroll distance).

## 2. Scroll-linked reveals

`assets/templates/motion.css` holds the system. Reveals ride the element's own trip through the viewport with
`animation-timeline: view()`, so they need no script, run on the compositor and rewind when scrolling back. Browsers
without scroll timelines (Firefox today) simply show everything, which is the right fallback: content is never
hidden behind a script.

Kinds (each section should not enter the same way; vary them):
- `rise`: copy and cards rise 64px from slight depth (scale .97) and fade in.
- `line-l` / `line-r`: hairline halves draw outward from their nodes. `line-v` for vertical connectors.
- `open`: a photograph opens from an inset rounded clip while the picture inside drifts (scale 1.16 to 1.04).
- `sheet`: a whole section slides up 120px and settles from scale .92 (cream sheets over lime fields, film frames).
- `climb`: a mark climbs out of an `overflow-hidden` mask (footer wordmark). Range ends in `entry`.
- `words`: a heading set word by word (`assets/templates/words.tsx`); each word rises in turn (`--w` index).

Stagger with `style={{ '--r': n }}` (a later start, n percent of the range), not with delays, which mean nothing to a
scroll timeline. Typical: cards `i * 3` to `i * 4`.

Earlier sites used an IntersectionObserver that toggled `data-shown` with CSS transitions behind a `js` class. It
works, but it needs a script before paint, it leaves content invisible if the observer stalls (hidden panes, slow
hydration), and full-page screenshots show nothing. Prefer the scroll-linked version.

## 3. The pinned hero

The most "premium" transition on the careNext home: the hero holds still and shrinks back while the first section
slides up over it like a sheet.

```tsx
<div className="stick-hero"><Hero /></div>
<div className="relative z-10">
  <Suite />   {/* rounded-t-[132px] + a soft upward shadow + an opaque background */}
  ...
</div>
```

`.stick-hero` is `position: sticky; top: 0` with a `scroll(root)` animation over `0 105svh` that scales the hero to
.86 and fades it to `opacity: 0; visibility: hidden`. The fade-to-hidden matters: the sticky element stays stuck
behind everything for the rest of the page, so once it is covered it must disappear, or the rounded corners of later
sections would show it, and it would catch clicks.

## 4. Page transitions

React's `<ViewTransition>` works in the Next 16 App Router without config (read
`node_modules/next/dist/docs/01-app/02-guides/view-transitions.md` in the project first; this Next is newer than
training data). `assets/templates/page-shell.tsx` wraps each page (in every `page.tsx`, never the layout: layouts
persist and never enter or exit).

The careNext transition: the page you leave sinks back (scale .9, opacity .25, 560ms in-out); the next rises over it
as a sheet with the panel's big rounded corners (`clip-path: inset(100% 0 0 0 round 140px 140px 0 0)` to full, plus a
12% translate, 760ms expo-out). The site header carries `viewTransitionName: 'site-header'` with its animation set to
none, so the bar stays put while the pages move.

A view transition blocks input while it runs; keep the whole thing under about 0.8s. Dev-server Fast Refresh replays
page transitions; that is a dev artifact, not a bug to chase.

## 5. The hero slider

When the client's site has a slider (careNext's broken three-slide hero), make it work rather than drop it.

- Headline lines swap through a mask: each line in `overflow-hidden`, `motion.span` from `y: 105%` to `0` on enter,
  to `-105%` on exit, `AnimatePresence mode="wait"`. The accent line in white italic.
- The product screen in the window swaps with `AnimatePresence mode="popLayout"` (opacity + y only). Animate the
  address bar with it, or it will show the next URL over the old screen mid-transition.
- Auto-advance (7s) while the hero is in view (`useInView(ref, { amount: 0.3 })`). Do not pause on hover or focus
  when the hero fills the screen: the pointer is always over it, so it never moved ("hero not moving to the next
  product"). Give an explicit pause/play button beside the slide squares instead (WCAG 2.2.2), and stop for
  `prefers-reduced-motion`.
- Slide squares: the live one stretches into a bar whose fill is a `scaleX` animation keyed on `${slide}-${running}`.
- `aria-live="polite"` only while paused; `off` while auto-rotating.

## 6. The film

`assets/templates/film.tsx`: a film card in the page (muted loop or poster, big play button, title) that grows out of
its exact place to fill the screen (`motion` `layoutId`, borderRadius animated via `style`), darkening the page
behind it, and plays with sound; Esc, the close button or the backdrop shrink it back into the page. It locks page
scroll while open, focuses the close button, and returns focus to the play button. mp4 sources play natively; Vimeo
ones load `player.vimeo.com/video/<id>?autoplay=1` in the frame. `size="sm"` gives grid cards a solid caption strip,
because white titles do not read over white logo posters. The user's words: "make it go to full screen and play...
no need to pin it... like really smooth transition".

## 7. Small pieces

- `count-up.tsx`: figures count up once in view; the final number is server-rendered, so it is there without script.
- Marquee: content duplicated 4x, `translate3d(-50%)` over ~48s, pauses on hover, off for reduced motion.
- Reading lines (a manifesto): each line's opacity peaks as it crosses the middle (`animation-range: cover 10% cover
  90%`, keyframes .14 to 1 at 38-62% to .32). Mid-page only (it needs the full cover range).
- Moving dots along a path (money from patient to provider): animate `left` on a tiny element; cheap enough.
- Floating cards: a 7-9s `translate3d` float, phases offset with negative delays.

- Objects around a video loop (the Mattered hero, 8x Careers): a 16:9 stage that covers the hero like object-fit
  (`container-type: size` wrapper, stage `width: max(100cqw, 177.78cqh)`), objects placed in the stage's cqw in orb
  radii, one CSS cycle of two loops per object (burst out on an overshoot bezier as the orb's wobble settles, float,
  ease-in back to the centre as the next wobble starts). Keep the clocks together by setting each CSS animation's
  `currentTime` from `video.currentTime` on `playing` and `timeupdate`, counting wraps into a clock that only moves
  forward (`(loops * LOOP + t)`; taking it modulo the cycle threw the second set back into its delay and it vanished); pause both off screen; start
  the objects on their own after 3s if autoplay never comes. Fade the stage's bottom with a mask, never a painted
  colour (the page under it is a gradient).

## 8. Verifying motion

- Full-page screenshots render scroll-linked pages at one scroll position and lie. Use `scripts/tour.py` (viewport
  shots while scrolling, plus the very bottom) on desktop and phone.
- `scripts/check_site.py --perf` for frame rate and "does a wheel over the hero scroll the page".
- Script the interactions that matter (open/close the film, the slider advancing with the mouse resting on the hero,
  the pause button) with Playwright and assert on state, not just pixels.
- The browser pane can report `visibilityState: hidden` while you test (rAF paused, observers idle). Timing tests
  there are unreliable; use headless Playwright for numbers and the pane for showing the user.
- A hidden pane also pauses video and can hand back a stale screenshot. To see a timed scene, scrub it: pause the
  animations and set `currentTime` (seek the video first and wait for `seeked`, or its `timeupdate` sync undoes you),
  then shoot full resolution with Playwright; the pane only gives a scaled view.
