---
name: Lumora
description: A violet-blue beam of light lands on live product UI; near-black and bone bands, tight Satoshi display, ember glow CTAs.
colors:
  near-black: "#090a0c"
  graphite: "#111112"
  bone: "#f5f5f5"
  ink: "#0b0b0d"
  ink-body: "#2a2a30"
  fog: "#e2e2e8"
  fog-muted: "#a0a0ab"
  card-black: "#0c0c0e"
  ui-surface: "#0f0f12"
  ui-card: "#16161a"
  ui-hairline: "#1c1c21"
  ui-border: "#26262c"
  ui-muted: "#6f6f79"
  ui-secondary: "#8a8a94"
  beam: "#8ea3ff"
  blue: "#4f7cff"
  ui-blue: "#5b8cff"
  violet: "#8b6cff"
  ember: "#ff7a2f"
  ember-ink: "#f06a36"
  green: "#37c98b"
  red: "#ff453a"
  highlighter: "#ffe38a"
typography:
  display:
    fontFamily: "Satoshi, Inter, system-ui, sans-serif"
    fontSize: "clamp(2.5rem, 5.84vw, 5.25rem)"
    fontWeight: 700
    lineHeight: 0.9
    letterSpacing: "-0.04em"
  display-section:
    fontFamily: "Satoshi, Inter, system-ui, sans-serif"
    fontSize: "clamp(2.9rem, 6.25vw, 5.6rem)"
    fontWeight: 700
    lineHeight: 0.92
    letterSpacing: "-0.04em"
  headline:
    fontFamily: "Satoshi, Inter, system-ui, sans-serif"
    fontSize: "clamp(2.6rem, 5.1vw, 4.6rem)"
    fontWeight: 700
    lineHeight: 0.95
    letterSpacing: "-0.04em"
  title:
    fontFamily: "Satoshi, Inter, system-ui, sans-serif"
    fontSize: "28px"
    fontWeight: 500
    lineHeight: 1.05
    letterSpacing: "-0.03em"
  lede:
    fontFamily: "Inter, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "18px"
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: "-0.012em"
  statement:
    fontFamily: "Inter, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "clamp(1.3rem, 2vw, 1.65rem)"
    fontWeight: 500
    lineHeight: 1.3
    letterSpacing: "-0.02em"
  body:
    fontFamily: "Inter, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.5
  caption:
    fontFamily: "Inter, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: "-0.01em"
  nav:
    fontFamily: "Inter, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "15px"
    fontWeight: 500
    letterSpacing: "-0.01em"
  label:
    fontFamily: "Inter, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "12.5px"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "-0.02em"
  label-sm:
    fontFamily: "Inter, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "11.5px"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "0.01em"
  ui:
    fontFamily: "Inter, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "11.5px"
    fontWeight: 500
    lineHeight: 1.35
  ui-caps:
    fontFamily: "Inter, system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
    fontSize: "10px"
    fontWeight: 700
    letterSpacing: "0.02em"
rounded:
  tag: "5px"
  control-sm: "7px"
  control: "8px"
  card-sm: "9px"
  item: "10px"
  popover: "12px"
  window: "14px"
  panel: "16px"
  card: "18px"
  map-card: "26px"
  pill: "999px"
spacing:
  wrap: "1230px"
  gutter: "24px"
  gutter-phone: "20px"
  nav-height: "64px"
  bento-gap: "20px"
  heading-to-lede: "18px"
  lede-to-stage: "64px"
  stage-to-grid: "90px"
  section-y: "150px"
  section-y-phone: "96px"
components:
  button-glow:
    backgroundColor: "#e7e7eb"
    textColor: "#4a2210"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "0 28px"
    height: "40px"
    width: "240px"
  button-outline:
    backgroundColor: "#0c0d10"
    textColor: "#ffffff"
    typography: "{typography.label}"
    rounded: "{rounded.pill}"
    padding: "0 26px"
    height: "40px"
    width: "174px"
  button-outline-hover:
    backgroundColor: "#16171b"
  button-pill:
    backgroundColor: "transparent"
    textColor: "#ffffff"
    typography: "{typography.label-sm}"
    rounded: "{rounded.pill}"
    padding: "0 16px"
    height: "34px"
  button-pill-hover:
    backgroundColor: "rgba(255, 255, 255, 0.09)"
  button-pill-solid:
    backgroundColor: "#ffffff"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
  nav-link:
    textColor: "#ffffff"
    typography: "{typography.nav}"
    rounded: "{rounded.control}"
    padding: "8px 12px"
  nav-link-hover:
    backgroundColor: "rgba(255, 255, 255, 0.06)"
  dropdown-panel:
    backgroundColor: "rgba(15, 15, 18, 0.94)"
    rounded: "{rounded.window}"
    padding: "8px"
    width: "270px"
  card-bento:
    backgroundColor: "{colors.card-black}"
    textColor: "#ffffff"
    typography: "{typography.caption}"
    rounded: "{rounded.card}"
    height: "420px"
  card-map:
    backgroundColor: "#212126"
    textColor: "#ffffff"
    typography: "{typography.caption}"
    rounded: "{rounded.map-card}"
    height: "250px"
  kanban-card:
    backgroundColor: "{colors.ui-card}"
    textColor: "#e6e6ec"
    typography: "{typography.ui}"
    rounded: "{rounded.card-sm}"
    padding: "10px"
  sync-panel:
    backgroundColor: "#151518"
    textColor: "#dcdce3"
    rounded: "{rounded.panel}"
    width: "430px"
  tag-blue:
    backgroundColor: "#b9ccff"
    textColor: "#1d3a8f"
    rounded: "{rounded.tag}"
    padding: "2px 6px"
  tag-coral:
    backgroundColor: "#f7a58e"
    textColor: "#6b2311"
    rounded: "{rounded.tag}"
    padding: "2px 6px"
  tag-amber:
    backgroundColor: "#f5ca7c"
    textColor: "#5d3c05"
    rounded: "{rounded.tag}"
    padding: "2px 6px"
  tag-violet:
    backgroundColor: "#bcaeff"
    textColor: "#33218a"
    rounded: "{rounded.tag}"
    padding: "2px 6px"
  glow-icon:
    backgroundColor: "#1d2233"
    textColor: "#cfd6ff"
    rounded: "{rounded.pill}"
    size: "64px"
  call-control:
    backgroundColor: "#56565c"
    textColor: "#ffffff"
    rounded: "{rounded.pill}"
    size: "46px"
  call-control-pressed:
    backgroundColor: "#ffffff"
    textColor: "{colors.ink}"
---

# Design System: Lumora

## Overview

**Creative North Star: "The Lit Workbench"**

A dark room, one beam of light, and working tools on the bench that answer when touched. The hero's beam falls onto the top edge of a live tracker mock, floods along it and pours over its far corner like liquid light, in a faint blue haze; every section after it shows product UI actually running (cards drag, palettes type, repos sync, calls rotate speakers), lit from within rather than illustrated. The brief pins this world to huly.io's visual language (dark light-beam hero, dark and light bands, bento cards, glow CTAs, product-UI mocks) with original brand, copy and media, and every UI surface, light and animation is code.

Dark bands carry the light: the beam, radial pools, halftone dots, glow rings. Bone bands act as a daylight table where dark product objects sit ringed in white. Type is compressed and confident (Satoshi 700 at -0.04em) over plain, hard-working Inter. Density lives inside the mocks (9 to 12.5px UI type, hairline dividers); the marketing layer around them stays sparse: one headline, one lede, one stage per section.

Motion is continuous but economical: each element reveals once, loops run only while their section is on screen, and every demo has a resolved still state for reduced motion.

**Key Characteristics:**
- Full-bleed near-black and bone bands; dark bands open, punctuate and close the page.
- One violet-blue beam as the ambient and interactive light; ember as the call to act and the present moment.
- Satoshi 700 display at -0.04em, hand-broken into one or two lines, over Inter.
- Live product mocks authored at a fixed design size and scaled as one unit.
- Dark product surfaces on bone wear a solid white ring.
- Depth from light (glows, pools, halftone), not from shadow.
- Reveal once, loop only on screen, freeze to an answered state under reduced motion.

## Colors

A near-monochrome night-and-bone field lit by two lights: violet-blue for ambience and interaction, ember for action and "now"; everything else is quiet product-UI status colour.

### Primary
- **Beam Violet-Blue** (beam): the page's light. The shader's halo and glow, the focus ring, dark-band `::selection` (38% alpha), carets, the command palette's hot icon, glow rings on the sync hub, mic and feature icons (rgba(142, 163, 255, .14 to .6)), the travelling sync packet, calendar event dots, the feature-list light pass (text-shadow 0 0 18px at 90%), and the favicon's dot.
- **Ember** (ember): the call to act and the present moment. The glow CTA's inner light and halo, the planner now-line and its pill, today in the map calendar, the rail's to-do widget and unread dot, `@everyone` mentions, the gauge's resting zone and needle, the CTA streak. On bone it deepens to **Ember Ink** (ember-ink) for the docs author cursor and typed insertion.

### Secondary
- **Signal Blue** (blue): the focus ring on bone (`.light :focus-visible`), the docs author pin, a planner and time-block hue, the Growth project ring marker.
- **Tracker Blue** (ui-blue): active state inside product UI: tab underlines, current breadcrumb, inbox badge, unread dots, the Invite button, the speaking tile and talking avatar rings, in-progress status, row-flash and new-note tints. Untokenized in CSS (11 literal uses).
- **Event Violet** (violet): a planner and time-block hue; the notes card's light pool.

### Tertiary
- **Done Green** (green): toast check, completed checkbox, synced/closed status (the kanban Done dot and done ring use #3fd08f).
- **Live Red** (red): the pulsing live dot and the end-call control.
- **Highlighter** (highlighter): bone-band `::selection`, the docs highlight sweep, the notes "Goal:" mark.
- **Tag pastels**: pastel fill with deep same-hue text (blue, coral, amber, violet; see `tag-*` components). Kanban status dots: coral #ff7a59, white #e8e8ee, ui-blue, green #3fd08f.

### Neutral
- **Near-Black** (near-black): body, hero, CTA and footer; the shader's base colour; `theme-color`.
- **Graphite** (graphite): the `.dark` band (repo sync). The CTA overrides it back to near-black so it runs into the footer.
- **Bone** (bone): the `.light` bands (productivity, office, graph, docs).
- **Ink** (ink): headline ink on bone and text on white pills; the same value is the mock's rail surface and the scrollbar track.
- **Ink Body** (ink-body): long-form text on bone (statement paragraph, docs). Section ledes on bone sit at #34343b, feature copy at #4a4a52.
- **Fog** (fog): default text on dark (hero lede #dfdfe7).
- **Fog Muted** (fog-muted): ledes on dark; card captions sit at #a1a1ac to #a3a3ad, feature copy at #9a9aa5.
- **Card Black** (card-black): the bento card body.
- **Product-UI ladder**: ui-surface (sidebars, inbox), #0d0d10 (app main), ui-card (kanban cards, rooms, inputs), ui-hairline (every internal divider; the direction contract's #1f1f23 does not appear in the build), ui-border (card and tile outlines, #222228 to #26262c), ui-muted (placeholders, inactive icons, meta), ui-secondary (counts, timestamps).

### Named Rules
**The Two Lights Rule.** Beam violet-blue is the ambient and interactive light; ember marks the action and the present moment. Atmosphere (background glows, blobs, waves, card light pools, gradient text) is tinted only from beam, violet or ember, plus white.

**The Status-Is-Not-Atmosphere Rule.** Green, red and the tag pastels report state inside product UI; they never become a background glow or a section colour.

## Typography

**Display Font:** Satoshi (Fontshare; weights 700 and 500 in use) with Inter, system-ui fallback
**Body Font:** Inter (Google Fonts, 400 to 700) with system-ui, -apple-system, Segoe UI, Roboto
**Label/Mono Font:** none; ids, clocks, badges and calendars use Inter with tabular numerals

**Character:** A tight geometric grotesk speaking in two short lines over a neutral, legible text face; the pairing reads as product, not editorial. Text renders antialiased with `optimizeLegibility`.

### Hierarchy
- **Display** (700, clamp(2.5rem, 5.84vw, 5.25rem), max 84px, 0.9): hero h1 only. Two hand-broken `.ln` lines share one continuous gradient fill (white 30% to #d5d8f6 80% to #fdf7fe, `background-size: 100% 200%`, line two takes the lower half); the CTA title reuses it.
- **Display Section** (700, clamp(2.9rem, 6.25vw, 5.6rem), 0.92): `.h-xl`, the bone-band openers (productivity, docs).
- **Headline** (700, clamp(2.6rem, 5.1vw, 4.6rem), 0.95): `.h-lg`; `.h-lg--light` sets it white on dark.
- **Title** (Satoshi 500, 28px, 1.05 to 1.08, -0.03em): feature-grid titles, always two lines via `<br>`.
- **Lede** (Inter 400, 18px, 1.4, -0.012em, max 660px; hero 470px): directly under every headline. The CTA lede is 17px/1.35, max 400px.
- **Statement** (Inter 500, clamp(1.3rem, 2vw, 1.65rem), 1.3, -0.02em, max 680px): `.big-para`; the docs lede and doc body use the same large register at weight 400 (up to 1.5rem and 1.4rem).
- **Body** (Inter 400, 16px, 1.5): base.
- **Caption** (Inter 400, 16px, 1.3 to 1.4, -0.01em): bento and map card captions; feature-grid copy is 15px/1.4 to 1.45 at max 220 to 270px.
- **Nav** (Inter 500, 15px, -0.01em): nav links and dropdown titles; dropdown descriptions 14px #7e7e89.
- **Label** (Inter 700, 12.5px, uppercase; -0.02em on the glow button; nav pills 11.5px at +0.01em): buttons only.
- **UI** (Inter 400 to 600, 9 to 12.5px): inside mocks. Panel titles 16px 600; column headers 10px 700 uppercase +0.02em; sidebar section label 10.5px 600 uppercase +0.04em.
- **Wordmark** Satoshi 700 23px, -0.045em, lowercase; mobile menu links Satoshi 700 26px/1.1, -0.03em.

### Named Rules
**The Tight Display Rule.** Satoshi headlines are 700, tracked -0.04em, line-height 0.9 to 0.95, broken by hand into one or two short `.ln` lines; Satoshi never sets running text or captions.

**The Bold Lead-in Rule.** Card captions open with a bold sentence naming the feature in white, then continue in grey at the same size ("**Command palette.** Jump anywhere…").

**The Uppercase-Is-for-Buttons Rule.** Uppercase appears only on buttons and product-UI micro labels; headings, ledes and captions are sentence case, and no label or kicker sits above a headline.

## Layout

- **Container:** `.container` is min(var(--wrap), 100% minus two gutters): 1230px with a 24px gutter (20px at 760px and below).
- **Offset columns (1240px and up):** `.narrow` (864px) starts 288px in from the container's left edge, `.mid` (1056px) 128px in (192px in the graph band), `.office__stage` (960px) 270px in. Section copy is left-aligned on these staggered edges.
- **Wide stages** break the container: sync 1120px, map 1320px, docs grid 1306px (30% sticky labels | 706px text | remainder).
- **Hero:** 64px nav laid absolutely over it; 184px top / 92px bottom padding; copy top-left; the stage 238px below the CTA; mock 1024 design px; a 340px fade hands the hero to the next band; the feature list sits 16px under the stage.
- **Band order:** hero (near-black) → productivity, office (bone) → sync (graphite) → graph, docs (bone) → CTA + footer (near-black).
- **Section rhythm:** 150px vertical padding (graph 170 top, sync 180 bottom, docs 120/190, CTA 150/170 with min-height 640px); headline to lede 18px; lede to stage 40 to 72px (bento 40, office and map 64, sync 72); stage to the follow-on copy 90 to 110px (six grid 90, statement 96, trio 110 after the statement).
- **Bento:** 12-column grid, 20px gap, rows alternate 5+7 and 7+5 spans, cards 420px tall, `perspective: 1400px`.
- **Feature grids:** trio 3 columns with 40px gap; six 3 by 2 with 72px rows and 40px columns.
- **Scaled stages:** `.scaler` holds a mock authored at `--w` by `--h` design px (app 1024x569, office 1000x560, sync 1120x520, map 1320x600); a ResizeObserver sets `--s` = width / `--w` and the inner layer scales from its top-left. Map cards sit at design coordinates (`--x`, `--y`, `--gw`, `--gh`).
- **CTA:** art (haze, ember streak, 400px gauge) pinned top-left; copy starts at 44.3% of the container (46% at 1180px and below); a 1px horizon line at 311px.

**Responsive rules**
- **1180px and below:** wordmark margin 86 to 36px, "Star us" hidden, docs grid 22% | 1fr | 4%, CTA copy at 46%.
- **980px and below:** links and actions collapse to a burger and full-width sheet; bento goes single-column; six goes to 2 columns; docs labels hide and the grid collapses; the CTA stacks (art centred above with 360px top padding, copy and buttons centred).
- **760px and below:** gutter 20px; hero 116/72px with the stage 64px below; sections 96px; the feature list becomes a 22s marquee; bento cards 380px and the palette drops a row; the planner zooms (`--lead` 34px, `--zoom` 1.75, `nowMoveSm`); the time-block calendar hides (list only); sync unpacks into stacked panels (4 rows each, wires and packet hidden, hub inline); the map unpacks into a stacked grid (22px gap, 250px cards, connectors and calendar card hidden); trio and six go single-column at 48px gap.

### Named Rules
**The Offset Column Rule.** Above 1240px, section copy hangs on staggered left edges (+128, +192, +270, +288px from the container edge), never centred.

**The Authored-Size Rule.** Mocks are authored once at a fixed design size and scaled as one unit; they reflow only at 760px and below, where they are unpacked into simpler stacked versions rather than squeezed.

## Elevation & Depth

Hybrid, split by band. On dark bands depth is light: the beam, radial pools, halftone dots and glow rings; drop shadows only seat floating UI, and every one has a negative spread so it pools beneath the object. On bone, dark product objects are framed by a solid white ring and a long, soft, cool shadow.

### Shadow Vocabulary
- **White ring, bento** (`box-shadow: 0 0 0 4px rgba(255,255,255,.78), 0 30px 60px -30px rgba(18,18,40,.42)`): bento cards on bone.
- **White ring, map card** (`box-shadow: 0 0 0 4px rgba(255,255,255,.8), 0 30px 60px -30px rgba(0,0,0,.45)`): connected-map cards.
- **White ring, office** (`box-shadow: 0 0 0 6px rgba(255,255,255,.72), 0 50px 100px -40px rgba(20,20,50,.55)`): the large office demo.
- **Stage drop** (`box-shadow: 0 50px 60px -30px rgba(0,0,0,.7)`; sync panels `0 40px 80px -30px rgba(0,0,0,.9)`): mocks on dark.
- **Popover** (`box-shadow: 0 24px 50px -14px rgba(0,0,0,.75)`; palette `0 30px 60px -20px rgba(0,0,0,.9)`; event popover `0 24px 40px -16px rgba(0,0,0,.9)`): floating UI.
- **Lifted** (`box-shadow: 0 26px 48px -10px rgba(0,0,0,.9)`; flying task `0 18px 30px -10px rgba(0,0,0,.8)`): an object in the hand mid-drag.
- **Beam glow ring** (`box-shadow: 0 0 0 1px rgba(142,163,255,.35), 0 0 40px rgba(91,110,255,.35)`, busy `.7` and 60px): the sync hub; the mic uses a 2px ring at .6 with 34px glow; the speaking tile `0 0 0 2px #5b8cff, 0 0 24px rgba(91,140,255,.45)`.
- **Ember glow** (`box-shadow: 0 0 10px var(--ember)` now-line; `0 0 14px rgba(255,122,47,.6)` today). The CTA's halo is a blurred radial pseudo-element, not a shadow.
- **Glass highlight** (`box-shadow: inset 0 1px 0 rgba(255,255,255,.85), inset 0 -1px 0 rgba(0,0,0,.1)`): the glow button's body; call controls use `inset 0 1px 0 rgba(255,255,255,.16)`.

### Light and material techniques
- **WebGL beam** (`js/beam.js` on `.hero__beam`): one fragment shader rendered at 0.6x the device pixel ratio, capped at CSS resolution (soft by design). Every part's cross-section was fitted to measurements of the reference frame, then set in motion. The beam: a white core (sigma 2px at the very top, 3px lower) in a blue glow (rgb .24/.31/1, decay 14px), swelling as light streams down it. The flare: a white trumpet whose width grows as 153.6·e^(-u/45.5) toward the mock's top edge, over a blue swell of haze; a white-hot sheet hugging the edge (reaching ~380px to the long side and all the way to the far corner), measured from the mock's rounded outline so it wraps the corner's arc; a pool of light above it, cyan-blue toward the long side and violet toward the corner. The corner: the light falls outside the right edge as a curtain, a white band widening from ~4 to ~30px, a cyan fringe turning pink lower down, fanning into blue, with streaks running down it. Around it all, slow fbm haze and blue clouds drift past the beam's upper half, with pointer parallax; exponential tone-map; grain against banding; a fade over the hero's last 380px. Geometry is read from the DOM each frame and every length scales by k = mock width / 1024. Past the mock's ends there is no surface, so light fades the same way above and below the edge's level there. Hovering the hero CTA eases in a +45% beam boost (+25% on the flare). Without WebGL, `.hero.no-gl` swaps in two radial violet gradients.
- **CSS light:** `.hero__core` is a 2px white hairline with two light packets racing down at 1.7s and 2.6s, shown only without WebGL; `.mock::before` is a 2px rim on the mock's top edge, warm peach right under the beam (69%), cooling and dimming toward the far left.
- **Ghost UI:** faint beam-outlined interface (`.hero__ghost`) revealed only through a 260px pointer spotlight mask and a resting patch lit beside the beam.
- **Halftone dots:** the hero (a fixed 3px white dot grid at 14%, overlay-blended over the light so it only surfaces where the haze is lit, under the ghost UI and the mock); map cards (0.7px white dots on a 5px grid at 17%, masked to fade out of each card's light pool); the CTA streak (#ffc29a, 5px); the gauge face (beam dots, with ember dots masked onto the left half).
- **Radial pools:** each map card carries its own coloured pool at a named edge (`--gp` position, `--gg` colour: blue, white, ember, coral, violet, violet-blue); feature icons sit on a soft radial halo reaching 42px beyond their edge; the voice card has a violet pool below; the CTA has a grey haze.
- **Pointer light:** bento and map cards gain a 420px radial white light (8%) under the pointer; bento cards also tilt up to about 5.7 degrees via the `rotate` property.
- **Bone atmosphere:** three pastel blobs blurred 90px at 60% (peach #ffd9c9, periwinkle #d7dcff, lavender #e6e1ff) drift behind the bento; gradient wave strokes (beam tint to ember tint) run behind the office.

### Named Rules
**The Light-Is-Depth Rule.** On dark bands, depth comes from light, not shadow; any drop shadow uses a negative spread so it pools beneath the object.

**The White Ring Rule.** Dark product surfaces placed on bone wear a solid white ring (4px at 78 to 80%, 6px at 72% for the office demo) plus a long, soft, negative-spread shadow.

## Shapes

- **Pills** (999px) for every button; 99px for chips, badges, video name tags and the chat bar.
- **A radius ladder that grows with the object:** tags 5px; small UI controls 7px; nav links, planner events, time blocks and the focus ring 8px; kanban cards and inputs 9px; menu items, video tiles and floating event cards 10px; popovers, the doc image and icon tiles 12px; the app window, dropdown, office rooms and keycaps 14px; sync panels 16px; bento cards and the office demo 18px; map cards 26px. Circles for avatars, status glyphs, call controls, glow icons, the bell, hub and gauge.
- **Borders** are 1px hairlines: rgba(255,255,255,.08 to .24) on marketing chrome over dark, ui-hairline and ui-border inside mocks, dashed for empty slots (the ghost kanban card, office seats, backlog status).
- **Rims** are drawn with a padded pseudo-element and `mask-composite: exclude` (the glow button's rim, the mock's corner, the bell's spinning conic rim).
- **Clip reveals:** the doc image wipes down from `inset(0 0 100% 0 round 12px)` over 1.6s while its photo settles from 1.08 scale.
- **Icons:** one inline SVG sprite on a 24px grid, stroke 1.7 (1.5 to 1.8 at large sizes), round caps and joins, `currentColor`, sized 1em by `.i`. The mark is a rounded L with a detached dot.

## Components

### Buttons
- **Shape:** full pill (999px).
- **Ember glow (primary, `.btn-glow`):** 40px tall, min-width 240px, padding 0 28px. A silver-to-bone glass body (`linear-gradient(90deg, #c7c7cd, #e7e7eb 55%, #f3efe9)`) holding a warm light (74x46px radial, #fffaf2 to #ffe8cc) at `--gx`; an ember halo behind it (170x90px radial of ember, blurred 10px); a 2px masked rim that brightens to #ffb27a near the light. Label #4a2210, Inter 700 12.5px uppercase, -0.02em, with an 18px trailing arrow.
- **Hover / Focus:** `--gx` (a registered `@property`, default 88%) follows the pointer, clamped 10 to 90%, easing .75s `--out`; hover stretches the halo 1.25x wide and nudges the arrow 4px; active scales to .97. In the hero it boosts the beam; in the CTA it revs the gauge.
- **Outline (`.btn-outline`):** 40px, min-width 174px, padding 0 26px, #0c0d10 fill, 1px rgba(255,255,255,.2); hover lifts the border to .5 and the fill to #16171b; active .97. Sits 28px right of the glow button.
- **Nav pill (`.btn-pill`):** 34px, padding 0 16px, 1px rgba(255,255,255,.24), Inter 700 11.5px uppercase +0.01em; hover fill 9% and border 45%; active .96. The `--solid` variant is white with ink text.
- **Call controls (`.ctl`):** 46px circles in #56565c with an inset top highlight; hover lifts 3px on `--spring`; `aria-pressed="true"` inverts to white with ink; end-call is Live Red.

### Chips
- **Tags (`.tag`):** 9px 600 text, 2px 6px padding, 5px radius, pastel fill with deep same-hue text.
- **Badges:** inbox count is a 14px ui-blue circle with an 8.5px white number; the bell badge is a #ff6b4a pill ringed 3px in the card colour and pops on `--spring`; the planner's "now" is an ember pill with #1a0d05 text.
- **Name tags** on video tiles: 99px radius, rgba(10,10,12,.62) with 6px backdrop blur, 9 to 11px white.

### Cards / Containers
- **Bento card (`.bcard`):** card-black, 18px radius, 420px tall (380 at 760px and below), white ring. A live demo fills the top; the bottom 42% fades to the card colour beneath a caption pinned 24px from the sides and 22px from the bottom (max 470px), written to the Bold Lead-in Rule. Pointer light and tilt on fine pointers.
- **Map card (`.gcard`):** 26px radius; body `linear-gradient(180deg, #212126, #0e0e10 72%)` under its own coloured pool and halftone; caption inset 22px/24px. Cards are joined by 1.5px #cfcfd7 connectors that draw in once (1.6s) and then carry #7f95ff light pulses (3.2s loop).
- **Office demo (`.odemo`):** #101013 window, 18px radius, 52px title bar, a 3x2 grid of rooms (14px radius, ui-card; the live room tinted and bordered in ui-blue) beside a #0c0c0f call column.
- **Sync panel (`.spanel`):** #151518, 16px radius, 1px #25252b, 50px header, 52px rows split by ui-hairline. Status glyphs are 15px circles (dashed, outline, half-filled ui-blue, green check); ids in tabular Inter 11px ui-muted; a changed row flashes ui-blue at 24% for 1.3s.

### Inputs / Fields
- **Style:** no live form fields ship. Inputs depicted inside mocks are 28 to 36px tall, #141418 to #1b1b20 fill, 1px #25252b to #2c2c33 stroke, 7 to 10px radius (99px for chat bars), ui-muted placeholder.
- **Focus (depicted):** a beam-coloured leading icon and a 1.5px beam caret blinking at 1s steps.

### Navigation
- **Bar:** absolute over the hero, 64px, inside the container: wordmark (86px right margin), links (Inter 500 15px white, 8px 12px padding, 8px radius, hover fill 6%), then the "Star us" link and two nav pills pushed right.
- **Dropdowns (`.dd`):** 12px chevron in #8b8b95 rotates 180 degrees when open; the panel is min 270px with 8px padding, rgba(15,15,18,.94) behind a 16px backdrop blur, 1px rgba(255,255,255,.08), 14px radius and the popover shadow, entering from translateY(-6px) scale(.98) over .25 to .35s. Items are 10px 14px with 10px radius: a 15px white title over a 14px #7e7e89 line. Opens on hover (fine pointers), click and `:focus-within`; Escape closes and returns focus.
- **Star link:** the star spins 72 degrees and fills #ffcf6e on hover (.6s `--spring`).
- **Mobile (980px and below):** a 42px burger opens a fixed sheet under the bar (rgba(9,10,12,.97), 16px backdrop blur) with Satoshi 700 26px links and the pills below; it slides in 10px over .4s; a link or Escape closes it; `aria-expanded` and the label swap.

### Hero beam stage
Back to front: shader canvas, spotlit ghost UI, the halftone, the 1024px mock with its top-edge rim, a 340px fade, then copy and the feature list. The beam lands at 69.3% of the mock's width; the core's height and the ghost patch are recomputed every frame from the mock's rect. Below the stage, a beam-glow highlight passes along the feature list every 1.7s.

### Product-mock grammar
Every mock is live HTML/CSS, `aria-hidden`, and labelled once by `role="img"` on its figure. Surfaces step #0b0b0d rail, #0d0d10 main, ui-surface side and inbox, ui-card cards, divided by ui-hairline. Active state is white text over a 2px ui-blue underline; unread is a 6px dot (ui-blue in lists, ember with a 2px surface ring on the rail). Avatar stacks overlap 5 to 7px with a 1.5 to 2px surface-coloured border. Progress is an 11px conic ring (ember, deeper ember near completion, green when done). Column headers are 10px 700 uppercase with a 6px status dot and an italic count.

### CTA gauge
A 400px SVG dial: metallic bezel gradient with a specular rim and crown, a beam-dotted face with ember dots on its left half, 60 ticks every 6 degrees (major every 30, numerals from 9 to 3 o'clock), an ember arc (-120 to -30 degrees) and a blue arc (-30 to 90 degrees) each over a blurred glow copy, an ember-gradient needle with glow, and the Lumora mark at the hub. The needle is a damped spring (stiffness 120, damping 13) idling near -42 degrees in the ember zone; hovering either CTA button swings it to 72 degrees and brightens the ember streak. Ticks within 13 degrees of the needle light (#e8e8f0, ember #ffb27a, blue #b8c4ff).

### Docs co-editing
A highlighter sweep (`.sel`, registered `--selw` 0 to 100% over 1.8s) with black selection handles and a floating #2a2b31 format toolbar (#4a78ef active chip). An ember-ink author cursor under a 56px ember ring types an insertion while the old phrase strikes through. The title carries a bobbing avatar pin on a Signal Blue stem. Sticky side labels crossfade as each block crosses the viewport's middle 20%.

### Motion grammar
- **Easing tokens:** `--out` cubic-bezier(.16, 1, .3, 1) for reveals, state changes, FLIP and flights; `--spring` cubic-bezier(.22, 1, .36, 1) for pops and lifts (badge, time blocks, controls, icon tiles, pin, star).
- **Reveal:** `[data-reveal]` rises 26px out of a 6px blur and zero opacity (.9s opacity and filter, 1.1s transform), staggered by `--d` (0 to .3s). Headings instead wipe each `.ln` line up from 110% inside an overflow mask (1.15s, +.09s per line). A one-shot IntersectionObserver (threshold .12, bottom margin -10%) triggers it, gated by `html.js` so no-JS renders everything.
- **Live sections:** every section is `[data-live]`. Off screen (15% margin) it gets `.is-paused`, which pauses every CSS animation beneath it; JS loops await it, the hero's frame loop stops, videos pause and the call clock halts.
- **Named loops:** hero core stream (1.7s/2.6s), kanban drag (7.5s), inbox arrivals (3.8s), feature-list light pass (1.7s), command-palette sequence, planner hop (2.8s) and now-line drift (26s alternate), time-block flights (950ms), bell ring with badge pop and ripples (2.4s) and a conic rim spin (4s), wave strokes (7 to 14s), blob drift (22 to 26s), office walkers (2.6s hops, 1.5s moves), speaker FLIP (4.8s, 750ms), call chat (5.2s), live-dot pulse (1.6s), wire dash (1.2s), hub spin (6s, 1s when busy) and packet (1.1s), map pulses (3.2s), typed tasks and chat bubbles (3.2s), floating voice avatars (6 to 7s), pin bob (4s), selection cycle, strike-and-type, gauge idle (2.4s), caret blink (1s), phone marquee (22s).
- **Pointer-driven:** the glow button's light, smoke parallax (lerp .04 per frame), the CTA beam boost (.07), the ghost spotlight (alpha .08, position .2), card light and tilt, gauge rev.
- **Reduced motion:** CSS collapses every duration to .001ms and one iteration, reveals render in place, the marquee stops and wraps. JS loops never start, the beam draws one still frame, videos stay on posters, card tilt is off, and each demo is preset to its answered state (palette open on "create iss", blocks placed with the event popover, selection drawn, phrase struck, gauge at -42 degrees).

**The Live-Only Rule.** Nothing animates off screen; every loop lives inside a `[data-live]` section and waits for it.

**The Answered-State Rule.** Under reduced motion every demo freezes in its resolved state, never its empty start.

**The Pointer-Is-a-Light Rule.** Hover answers first with light (a moving glow, a spotlight, a card light); colour shifts and 2 to 4px lifts stay secondary.

### Browser surface and accessibility
- **Selection:** rgba(142,163,255,.38) with white text on dark; highlighter with ink text on bone.
- **Focus:** `:focus-visible` is a 2px solid beam outline at 3px offset, rounding to 8px on elements without their own radius; on bone the outline is Signal Blue.
- **Scrollbar:** `scrollbar-color: #2b2c33 #0b0b0d`; WebKit 11px, #2b2c33 thumb with a 3px track-coloured border and 8px radius.
- **Chrome:** `theme-color` near-black; the favicon is the white mark on near-black with a beam dot.
- **Semantics:** decorative mocks are `aria-hidden` inside a labelled `role="img"` figure; dropdowns and the burger carry `aria-expanded` and `aria-controls`; call controls use `aria-pressed`.

## Do's and Don'ts

### Do:
- **Do** run full-bleed near-black (#090a0c, graphite #111112) and bone (#f5f5f5) bands, and ring dark product surfaces on bone in solid white (0 0 0 4px rgba(255,255,255,.78 to .8)).
- **Do** draw every glow, focus ring, caret and dark-band selection from the beam violet-blue (#8ea3ff, rgba(142,163,255,…)).
- **Do** keep ember's glow (#ff7a2f) for action and the present moment: the glow CTA, the gauge and streak, the now-line, today, the unread dot.
- **Do** set headlines in Satoshi 700 at -0.04em, line-height 0.9 to 0.95, hand-broken into `.ln` lines that wipe up on reveal.
- **Do** open card captions with a bold lead-in sentence and continue in grey at the same size.
- **Do** build product UI as live HTML/CSS/SVG at a fixed design size inside `.scaler`, `aria-hidden` inside and labelled once on the figure.
- **Do** put every loop inside a `[data-live]` section and give it a resolved reduced-motion state.
- **Do** use `--out` for reveals and state changes and `--spring` for pops and lifts, and give every drop shadow a negative spread.

### Don't:
- **Don't** introduce a third light: atmosphere (background glows, blobs, waves, card pools, gradient text) stays beam, violet, ember and white.
- **Don't** use status hues (green #37c98b, red #ff453a, tag pastels) as a background glow or a section colour.
- **Don't** set running text or captions in Satoshi; it is for headlines, feature titles, the wordmark and menu links.
- **Don't** put uppercase kickers or eyebrows above headings; uppercase belongs to buttons and product-UI micro labels.
- **Don't** render product UI as screenshots; generated raster media is for photographs, portraits, call footage, card covers and the small icon tiles.
- **Don't** use hard, zero-blur offset shadows for elevation; depth is light or a soft negative-spread shadow (the command-palette keycaps' stacked wall depicts a physical key and sets no precedent).
- **Don't** centre section headings above 980px; they hang on the offset column edges.
- **Don't** animate anything off screen, or leave a reduced-motion demo at its empty start.
