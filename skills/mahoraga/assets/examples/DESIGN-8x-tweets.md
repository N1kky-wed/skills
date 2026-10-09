---
name: 8x.tweets
description: The marketplace for paid posts on X, in one lilac world after AIVENT. A lilac-white ground, white cards on soft violet-tinted shadows, ink set light in Geist, violet for every action and cornflower for links, iridescent silk and frosted glass wherever a screen opens, the web app itself as the hero, and every number large and light.
colors: # :root in src/app/globals.css unless marked literal
  bg: "#f5f4fc"
  slab: "#ffffff"
  slab-2: "#f8f7fd"
  slab-3: "#efedf9"
  line: "rgb(39 42 63 / 0.08)"
  line-2: "rgb(39 42 63 / 0.13)"
  line-3: "rgb(39 42 63 / 0.22)"
  fg: "#272a3f"
  fg-2: "#4b4e67"
  fg-3: "#6a6d86"
  fg-4: "#9a9cb2"
  navy: "#6147c7"       # the name stayed; it is the violet action now
  navy-2: "#5238b5"
  blue: "#4d68d4"
  sky: "#dcd7f6"        # lavender under the silk and glass
  lilac: "#c3bbeb"
  periwinkle: "#9899e4"
  cornflower: "#7795e3"
  lilac-tint: "#efebfd"
  good: "#1a9a63"
  good-tint: "#e3f6ec"
  warn: "#b86b1b"
  warn-tint: "#fdf0e1"
  bad: "#c93a52"
  bad-tint: "#fbe8eb"
  orange: "#f2a65a"
  violet-ink: "#5a45c2" # literal: text on lilac tints
  wash: "#eeedfc"       # literal: Flash, notes, the inbox strip
  haze: "#e3e3fb"       # literal: the radial on a lit card
  good-ink: "#147a4e"   # literal: text on good-tint
  x-text: "#0f1419"
  x-muted: "#536471"
  x-line: "#e6ecf0"
  x-blue: "#1d9bf0"
  x-like: "#f91880"     # literal: likes inside posts
typography:
  display: { fontFamily: "Geist, system-ui, sans-serif", fontSize: "clamp(2.8rem, 1.1rem + 4.2vw, 4.9rem)", fontWeight: 300, lineHeight: 1.02, letterSpacing: "-0.038em" }
  headline: { fontFamily: "Geist, system-ui, sans-serif", fontSize: "clamp(2.1rem, 1.35rem + 2.1vw, 3.15rem)", fontWeight: 300, lineHeight: 1.1, letterSpacing: "-0.032em" }
  page-title: { fontFamily: "Geist, system-ui, sans-serif", fontSize: "clamp(30px, 2.8vw, 42px)", fontWeight: 300, lineHeight: 1.08, letterSpacing: "-0.035em" }
  money: { fontFamily: "Geist, system-ui, sans-serif", fontSize: "clamp(34px, 3.4vw, 48px)", fontWeight: 300, lineHeight: 1, letterSpacing: "-0.04em", fontFeature: "\"tnum\" 1" }
  figure: { fontFamily: "Geist, system-ui, sans-serif", fontSize: "clamp(24px, 2.1vw, 32px)", fontWeight: 300, lineHeight: 1.05, letterSpacing: "-0.035em", fontFeature: "\"tnum\" 1" }
  section: { fontFamily: "Geist, system-ui, sans-serif", fontSize: "20px", fontWeight: 400, lineHeight: 1.2, letterSpacing: "-0.02em" }
  panel-title: { fontFamily: "Geist, system-ui, sans-serif", fontSize: "18px", fontWeight: 500, letterSpacing: "-0.015em" }
  body: { fontFamily: "Geist, system-ui, -apple-system, Segoe UI, sans-serif", fontSize: "16px", fontWeight: 400, lineHeight: 1.55 }
  row: { fontFamily: "Geist, system-ui, -apple-system, Segoe UI, sans-serif", fontSize: "14.5px", fontWeight: 500 }
  button: { fontFamily: "Geist, system-ui, -apple-system, Segoe UI, sans-serif", fontSize: "14.5px", fontWeight: 500 }
  label: { fontFamily: "Geist, system-ui, -apple-system, Segoe UI, sans-serif", fontSize: "13px", fontWeight: 400 }
  tag: { fontFamily: "Geist, system-ui, -apple-system, Segoe UI, sans-serif", fontSize: "12px", fontWeight: 500 }
  post: { fontFamily: "Geist, system-ui, -apple-system, Segoe UI, sans-serif", fontSize: "15.5px", fontWeight: 400, lineHeight: 1.45, letterSpacing: "-0.003em" }
  mono: { fontFamily: "Geist Mono, ui-monospace, SF Mono, Menlo, monospace", fontWeight: 400, letterSpacing: "-0.01em", fontFeature: "\"tnum\" 1" }
rounded:
  xs: "6px"      # --r-xs, the focus ring
  sm: "10px"     # --r-sm, brand tiles
  md: "14px"     # --r-md
  lg: "20px"     # --r-lg, X posts, glass, photo frames
  xl: "26px"     # --r-xl, panels and card shells
  sheet: "30px"  # literal: glass heroes, dialogs, drawers, inbox, door
  stage: "36px"  # literal: the landing's silk stages and its closing card (26px on phones)
  pill: "999px"  # --r-pill, every control, tag and state
spacing:
  base: "4px"    # --s1 to --s10 are declared; components use the literals below
  page-max: "1240px"
  page-pad: "30px clamp(18px, 3.4vw, 44px) 90px"
  rail: "252px"
  rail-tucked: "78px"
  head-to-content: "26px"
  grid-gap: "18px"
  card-gap: "14px"
  panel-pad: "22px"
  card-inset: "8px"
  row-pad: "12px 14px"
  landing-max: "1240px"
  landing-gutter: "clamp(20px, 4.4vw, 64px)"
  landing-section: "clamp(84px, 10vw, 140px)"
components:
  button-primary: { backgroundColor: "{colors.navy}", textColor: "#ffffff", typography: "{typography.button}", rounded: "{rounded.pill}", height: "44px", padding: "0 20px" }
  button-secondary: { backgroundColor: "{colors.slab}", textColor: "{colors.fg}", typography: "{typography.button}", rounded: "{rounded.pill}", height: "44px", padding: "0 18px" }
  button-small: { height: "36px", padding: "0 14px" }
  button-submit: { backgroundColor: "{colors.navy}", textColor: "#ffffff", rounded: "{rounded.pill}", height: "48px", padding: "0 24px" }
  glass-pill: { backgroundColor: "rgb(255 255 255 / 0.6)", textColor: "{colors.fg-2}", rounded: "{rounded.pill}", height: "44px", padding: "0 18px" }
  tab: { textColor: "{colors.fg-3}", rounded: "{rounded.pill}", height: "38px", padding: "0 16px" }
  tab-current: { backgroundColor: "{colors.navy}", textColor: "#ffffff" }
  seg-option: { textColor: "{colors.fg-3}", rounded: "{rounded.pill}", height: "32px", padding: "0 14px" }
  status: { backgroundColor: "{colors.slab-3}", textColor: "{colors.fg-2}", typography: "{typography.tag}", rounded: "{rounded.pill}", height: "24px", padding: "0 10px" }
  status-offer: { backgroundColor: "{colors.lilac-tint}", textColor: "{colors.violet-ink}" }
  status-work: { backgroundColor: "{colors.warn-tint}", textColor: "{colors.warn}" }
  status-live: { backgroundColor: "{colors.good-tint}", textColor: "{colors.good-ink}" }
  status-paid: { backgroundColor: "{colors.navy}", textColor: "#ffffff" }
  panel: { backgroundColor: "{colors.slab}", rounded: "{rounded.xl}", padding: "22px" }
  figure-tile: { backgroundColor: "{colors.slab}", typography: "{typography.figure}", rounded: "22px", padding: "18px 20px" }
  glass-stat: { backgroundColor: "rgb(255 255 255 / 0.55)", typography: "{typography.figure}", rounded: "{rounded.lg}", padding: "16px 18px 14px" }
  money-card: { backgroundColor: "{colors.slab}", typography: "{typography.money}", rounded: "24px", padding: "20px 22px" }
  sky-hero: { backgroundColor: "{colors.sky}", rounded: "{rounded.sheet}", padding: "clamp(22px, 3vw, 34px)" } # glass.webp behind it
  desk: { backgroundColor: "#ffffff", rounded: "1.6em", fontSize: "1.18cqi" } # the web app drawn in code, sized from its own width
  creator-card: { backgroundColor: "{colors.slab-3}", textColor: "#ffffff", rounded: "{rounded.xl}", aspectRatio: "5 / 7" } # a full card: the photo edge to edge
  field: { backgroundColor: "{colors.slab}", textColor: "{colors.fg}", rounded: "16px", height: "48px", padding: "12px 16px" }
  row: { rounded: "16px", padding: "12px 14px" }
  rail-link: { textColor: "{colors.fg-3}", rounded: "{rounded.pill}", height: "44px", padding: "0 10px 0 14px" }
  rail-link-current: { backgroundColor: "{colors.slab}", textColor: "{colors.fg}" }
  dialog: { backgroundColor: "{colors.slab}", rounded: "{rounded.sheet}", width: "560px" }
  x-post: { backgroundColor: "#ffffff", textColor: "{colors.x-text}", typography: "{typography.post}", rounded: "{rounded.lg}", padding: "18px" }
  ask-8x: { backgroundColor: "{colors.navy}", textColor: "#ffffff", rounded: "{rounded.pill}", height: "48px", padding: "0 20px 0 12px" }
  brand-tile: { backgroundColor: "#ffffff", textColor: "{colors.navy}", rounded: "{rounded.sm}" }
---

# Design System: 8x.tweets

## Overview

**Creative North Star: "Silk and Ledger"**

The whole product, landing, door and app, is one lilac world. A screen opens on iridescent silk or frosted glass (moving silk on the landing and the door, still glass on dashboards) and settles onto white cards on a lilac-white ground, with ink set light in Geist, violet for every action and cornflower for links. It is a website, not an app pitch: the landing shows the real web app at a desk, never a phone in a hand. The deal is shown, not told: a face for every person, a tile for every brand, a cover for every campaign, and every number large and light, with a spark, ring, meter or column beside it. Brands and creators share one palette; the side changes the story and the nav, never the light.

The model is AIVENT (LAIN, https://dribbble.com/shots/27749479), chosen on 2026-09-28 after the team turned down the Payno sky and its phone mockups: a lilac-white page, silk and glass forms instead of photographs, and the product's own screen as the hero. No AIVENT file ships in the product. The silk, the glass and the silk 8 in "how it works" are ours, generated with Gemini and Veo (the 8 replaced a paper bloom rendered from a crop of the AIVENT shot on 2026-09-30, when the team found it too close to the reference); the Desk is drawn in code. The contract is the `CONTRACT` comment in `src/app/layout.tsx`. The Payno version is in git history before this change if it is ever wanted back.

**Key Characteristics:**
- Light only: lilac-white `#f5f4fc`, white cards, lavender `#dcd7f6` under the silk and glass.
- Ink `#272a3f` at weight 300 for headlines and figures; violet `#6147c7` for the one action and for done; blue `#4d68d4` for now, links and focus; periwinkle `#9899e4` and cornflower `#7795e3` in charts; green `#1a9a63` for money in and growth.
- Depth from a 1px ink hairline and soft violet-tinted shadows; frosted glass only over pictures.
- Pills for every control and state, 26px cards, 30px sheets, 36px stages; circles for people, rounded tiles for brands.
- Visual first: the product's own screens, faces, covers, charts and big light numbers over paragraphs and tables.
- Calm motion that answers a click; nothing advances on its own except the landing's posts marquee.

Where things live: tokens on `:root` in `src/app/globals.css`; fonts and theme color (`#f5f4fc`) in `src/app/layout.tsx`; the app kit in `src/components/app/`; icons and `BrandTile` in `src/components/ui/`; the landing in `src/components/landing/`; the door in `src/app/(auth)/`.

## Colors

One violet action, one blue accent, a lilac-to-blue family for tints and charts, and four state hues on a white-and-lilac ground; X keeps its own light-mode colors inside posts.

- **Violet** `#6147c7` (`--navy`, hover `--navy-2` `#5238b5`; the token kept its old name so every action it painted turned violet at once): primary buttons, the current tab and Seg option, count badges, done steps, my messages, Paid, icon discs on money. `--key`, `--key-hi` and `--fill` are the same violet and drive the global focus ring, caret and selection.
- **Blue** `#4d68d4` (`--blue`): the accent. The current nav icon, links, unread dots, the now-step, a second chart series, the picked column, one phrase in a landing statement.
- **The lilac family**: lavender `#dcd7f6` (`--sky`) under every silk and glass picture; lilac `#c3bbeb` (`--lilac`); periwinkle `#9899e4` (`--periwinkle`) for "paid" in charts and the range track (`Donut` runs violet, blue, orange, periwinkle, green, `#d3d0ec`); cornflower `#7795e3` (`--cornflower`) for second sparks and meter ends; `#efebfd` (`--lilac-tint`) under offer states, chips, icon discs and the landing's current switch, with text in `#5a45c2`; the wash `#eeedfc` for Flash, notes and the inbox strip.
- **Ground**: lilac-white `#f5f4fc` (`--bg`) is the page; white (`--slab`) every card; `#f8f7fd` (`--slab-2`) insets, hovers and number strips; `#efedf9` (`--slab-3`) tracks, chips and quiet discs. The shell's top glow is a lavender radial at the right and a pale blue one (`rgb(222 234 252)`) at the left: the hint of blue beside the lilac.
- **Ink**: `#272a3f` (`--fg`) headings and figures, `#4b4e67` (`--fg-2`) body, `#6a6d86` (`--fg-3`) labels and meta, `#9a9cb2` (`--fg-4`) times and placeholders. Hairlines are that ink at 8, 13 and 22% (`--line`, `--line-2`, `--line-3`); shadows are tinted `rgb(45 38 99)`.
- **Haze** `#e3e3fb`: a radial at the top of a white card that marks it (a lit `Panel`, `MoneyCard`, dialogs, offers, the draft score, the first to-do); `#e0dffa` on the hot `Figures` tile.
- **Good** `#1a9a63` on `#e3f6ec` (text `#147a4e`): money in, trends up, Live and Link live.
- **Warn** `#b86b1b` on `#fdf0e1`: waiting on someone (signature, escrow, a counter), due days, composer fixes. **Bad** `#c93a52` on `#fbe8eb` (error text `#a8263d`): errors, decline, danger, failed checks. **Orange** `#f2a65a`: unfunded money, a weak password, nearing 280 characters.
- **X's own colors**: `--x-text` `#0f1419`, `--x-muted` `#536471`, `--x-line` `#e6ecf0`, `--x-blue` `#1d9bf0`, likes `#f91880`, only inside posts and the composer's post.
- **The landing's set**, on `.root` in `landing.module.css`: ink `#272a3f` headings, `#33364c` text, `#4b4e67` secondary, `#6a6d86` muted, solid hairlines `#e7e5f3` and `#d8d4ec`, mist `#f7f6fd` behind the hero, white pages, and the same violet, blue, lavender and green. Art cards sit on `#f2f0fa`.

**The One-Action Rule.** Violet marks the one action and what is done; blue marks what is current or clickable. Everything else is ink on white. **The Tint Rule.** A state is its ink on its own tint, in one pill; never a colored card, section or page.

## Typography

**Font:** Geist for everything (`next/font/google`, `--font-geist`; `--font-display` and `--font-ui` both resolve to it). **Mono:** Geist Mono 400 and 500 (`--font-geist-mono`) for codes, tracked links, tags and card numbers. The landing loads Geist again in `src/app/(marketing)/layout.tsx`. The global `.display`, `.h2`, `.h3` and `.lede` classes in `globals.css` are unused; type is sized in the module beside each component.

**Character:** ink set light. Headlines and every number sit at weight 300, tracked -0.03 to -0.045em, so pages read calm; weight goes to labels and actions (450 to 500), never to figures. 600 is for counts and initials; 700 only for the author's name inside an X post.

- **Display** (300, `clamp(2.8rem, 1.1rem + 4.2vw, 4.9rem)`, 1.02, -0.038em): landing type; the hero sets it at `clamp(2.6rem, 1rem + 3.5vw, 4.3rem)` and 12ch so the stage shows in the first viewport. **Headline** (300, `clamp(2.1rem, 1.35rem + 2.1vw, 3.15rem)`, 1.1, -0.032em): landing sections; the statement runs `clamp(1.8rem, 1.1rem + 2.1vw, 2.85rem)` at 1.24 and 26ch.
- **Titles** (300): the door `clamp(34px, 3.1vw, 46px)` at -0.04em; `SkyHero` `clamp(30px, 3vw, 44px)`; `PageHead` `clamp(30px, 2.8vw, 42px)` at -0.035em; onboarding `clamp(30px, 2.6vw, 38px)`; dialogs 26px; Ask 8x 22px.
- **Numbers** (300, tabular): money `clamp(34px, 3.4vw, 48px)` at -0.04em; figures `clamp(24px, 2.1vw, 32px)` at -0.035em (glass stats 2.2vw); offer prices 34px; the draft score and landing prices 46px. The unit follows in a `<small>` at 13px 400 `--fg-3`.
- **Sections** (400, -0.02em): strip heads and campaign titles 20px, creator names 19px (17px dense), empty-state titles 20px. Panel titles are 18px 500 at -0.015em.
- **Body** 16px/1.55 on `body`; page subs 15px `--fg-3` at 62ch; running text in cards 13.5 to 14.5px/1.55. Landing body 14.5 to 16px, subs 16px/1.6 at 54ch.
- **Rows** 14 to 14.5px 500 over 12.5 to 13px `--fg-3` meta; rail links 14.5px 450; tabs 14px 450; `Seg` 13.5px 450; buttons 14.5px 500 (13.5px small, 15px on submits and the landing).
- **Labels** 13px `--fg-3` over figures, 11 to 11.5px under card numbers; `Status` and tags 12px 500; counts 11.5px 600.
- **Post** 15.5px/1.45 at -0.003em in `--x-text` (14.5px small, 17px/1.5 in the composer); the author 15px 700.
- **The Desk** on the landing and the door is sized in em from `.win { font-size: 1.18cqi }` (the `.desk` wrapper is the container), so one drawing holds at any width it is given.

### Copy
- Short and plain: a sub is one sentence, a card says it in numbers. Second person, present tense.
- Sentence case everywhere, buttons included; buttons start with a verb ("New campaign", "Find creators", "Approve", "Withdraw"). The only uppercase is the landing's footer and rate-card labels, kept from the Payno version.
- No em dashes: use a comma, a colon or a full stop. The composer flags em dashes in drafts too (`src/lib/draftRules.ts`). No arrows and no unicode arrow glyphs.
- "Post" and "on X", never "tweet". Join facts with a spaced middle dot: "3 of 5 campaigns live · 12 posts published".
- Numbers go through `src/lib/states.ts`: `compactNum` (12.4K), `money` (whole dollars from cents), `moneyShort` ($12.3K); an en dash (–) stands for no value.
- The product is `8x.tweets` (`SITE.name` in `src/data/site.ts`); the assistant is "Ask 8x"; the footer wordmark reads "8x". The landing footer labels its people, photos, brands and figures as illustrative.

## Layout

**The app frame** (`Shell.tsx`, `shell.module.css`): a 252px sticky rail beside the page, on the lilac-white ground with two radials at the top (lavender `rgb(220 215 246 / 0.95)` at 78% -6%, pale blue `rgb(222 234 252 / 0.9)` at 10% -4%). No footer inside the app.
- The rail (padding 22px 14px 16px): the lockup at 20px 500; for brands, the bell with the newest eight events (no side pill: you know which side you're on); 44px pill links (22px icon, label, violet count), the current one a white card with a hairline, `--shadow-1` and a blue icon; a hairline before the org links; the account row (a white 80% pill padded 7px, a 36px face or a brand tile) with its menu. The lockup's "8x", the icons, the bell and the face share one axis 39px in.
- The rail tucks: the panel button at the top right (`RailToggle`, kept in the `rail` cookie so the server paints it right) narrows it to 78px of icons, the side pill and the words gone, a count shrunk to a 7px navy dot on its icon, the account a 50px circle round the face. Tucked, it opens as itself, never as a sheet over the page: while the pointer is on it or within 16px of its edge, while a key has focus in it, and while its bell or menu is open, RailToggle sets `data-peek`, which is simply the open layout: the rail is 252px again and the page re-centres in the room that's left, its margins shrinking, never pushed off the right edge. The grid never animates (that relays the whole page out every frame): it snaps once and the page glides from where it was on the compositor (FLIP in RailToggle), while the rail's own width moves. Opening waits 50ms and runs 260ms; closing waits 150ms and eases over 300ms, so it's seen to close. Words fade out (120ms) before the width goes and back in (220ms) after it comes; opening waits 110ms so a passing pointer doesn't open it, closing waits 300ms so a slip doesn't shut it; tucking and pinning slide the rail and the page edge together (420ms, `--ease-out`). Desktop only.
- Brands: Dashboard, Campaigns, Creators, Shortlist, Messages, Wallet, then Team, Clients, Company, MCP. Creators: Dashboard, Campaigns, Messages, Community, Wallet, Referrals.
- The page: `u.page`, `min(1600px, 100%)`, padding `30px clamp(18px, 3.4vw, 44px) 90px`; `PageHead` sits 26px above the content.
- Speed: each side's `loading.tsx` shows `PageSkeleton` (the head, a lilac banner, a row of cards, a light passing across) the moment a link is clicked, inside the shell; anything pressed sinks to 0.975 while held (globals, zero specificity); `Submit` shows its spinner while its form works. Empty states carry a crisp icon in a 64px lilac disc with a soft halo (`Empty`'s `icon`, a spark by default), as the inbox draws it.
- At 900px and below the rail becomes a sticky top bar (white 82%, blur 16px) and the nav a fixed 68px tab bar (white 90%, blur 16px, 11px labels, current icon blue) of up to five places; Shortlist and Community drop.

**Composition: show it.** The brand dashboard (`src/app/(app)/brand/dashboard/page.tsx`) is the exemplar:
1. `SkyHero`: the greeting, one sub of facts joined by middle dots, a `glassPill` holding a figure (the wallet), one violet action, and four `GlassStat`s (Views, Engagement, Clicks, Leads) with sparks.
2. `Flash` for the last action's result.
3. A 0.9fr | 1.25fr row: Panel "To do" (`Todo`, five at most, each with its one ghost action) beside Panel "Engagement" (`LineChart`, 12 weeks, marks where posts went up).
4. A 0.8fr | 2fr row: Panel "Money" (`Donut`: Available violet, In escrow blue, Paid periwinkle) beside running campaigns as cards: a 110px cover with its `Status`, the name, two `Meter`s (committed in violet, posts in green), an `AvatarStack`, clicks and leads.
5. A strip head (20px 400 title, a 13.5px link) and the applications: a focus card and three `CreatorCard`s with Approve and Decline.

The creator dashboard runs the same way: `SkyHero` (Withdrawable, In escrow, Average views, Open offers), their own `CreatorCard` beside a Panel with a `Seg` (Do next, Your earnings, Notifications; `Todo` and `Ring` for first steps, `MoneyCard` and `Columns` for earnings), then "Recommended for you" `CampaignCard`s in `cards.grid3`.

Other openings: dashboards, community and shared links open on `SkyHero`; lists and wallets open on `PageHead` straight into figures and cards; the campaign workspace opens on its cover (a 380px banner with a frosted title card and glass figures); the profile on glass with a 112px face and six glass figures; onboarding sits in the door's frame (`.frame`: 0.94fr | 1.06fr, 14px gaps): a full-height white panel with the bar on top and the step centred at up to 440px, beside a sticky full-height stage on the frosted glass (`glass.webp`) with the card being built and its figures; at 900px the panel comes first and the stage follows as a rounded block. Grids: `u.grid`, `u.cols2` and `u.cols3` at 18px; `u.main2` is `1.6fr | minmax(300px, 1fr)`; `cards.grid4` goes 4, 3 at 1180px, 2 at 900px; `cards.grid3` goes 3, 2 at 900px, 1 at 560px. App breakpoints: 1180, 1080 (`main2` stacks), 1000, 900 (the shell folds, `Figures` go 2-up, `Journey` wraps, the inbox shows one pane), 700 (columns stack), 560.

**The landing** ("/" for brands, "/creators" for creators; `src/components/landing/`, the layout in `src/app/(marketing)/layout.tsx` with `data-page="landing"`). Content sits in `.wrap`, `min(1240px, 100% - 2 * gutter)` with a `clamp(20px, 4.4vw, 64px)` gutter; sections pad `clamp(84px, 10vw, 140px)`.
- Sections meet softly: the hero's wash thins into the page's white from 42% of its height down, and the app band rises out of white and settles back into it on eased `color-mix` stops, so the page reads as one surface.
- The two sides share the kit and the palette but not the story; `.page[data-side]` gives each its light: brands lean blue-lilac (`--tintA` `#dcdcf9`, `--tintB` `#e9ecfc`, accent words in blue), creators rose-lilac (`#e9dcf8`, `#f3ecfc`, accent words `#7a4fd4`, and the silk in its rose cut).
- **Brands' hero**: the headline in two lines ("The creators you need | are already here.", `clamp(2.5rem, 4.6vw, 4.4rem)`) left, the promise (two lines in a 480px column, `text-wrap: balance`) and one violet action right; under 1100px the headline takes the full width and the promise and action sit beneath it side by side, so both keep two lines. Under them the stage: a 36px card at 2:1 of moving silk holding the Desk at 78% width from 7% down, so the window fills the stage and runs off its lower edge; an X post at the left (`PostCard`) and a glass payment chip at the right ("Paid to @mayabuilds", "+$2,800").
- **Creators' hero**: split, the headline ("Get paid to | post on X.") and the promise with two actions ("Connect your X account", "See how it works") left; right, a rose silk stage at 1:1.02 holding the creator's own full card (Maya, "Get your card"), an offer from Halcyon (`OfferFrag`) and a payout chip.
- The nav (84px: logo, the For Creators | For Brands switch as a white pill with the current side on `--lilac-tint`, Log in and a white CTA) sits over either hero.
- The sheet, brands: the statement (the two-ring emblem over split words, one phrase in the accent); built for (a campaign on the timeline beside the copy and a 2x2 of promises: on `glass.webp` at 4:5, X's white column at 0.86 with "For you | Following", an ordinary post, the brand's sponsored post lifted out of the feed with a violet hairline and a deep shadow, and one below fading out; four pill pins ride the edges of the lifted post, each the promise beside it with the same icon (the match on the card's top edge, the escrow and the approval on the photo's corners, the clicks under the card), anchored to the post so they follow it at any width; hovering a promise brings its pin forward and sets the others back; on a phone the post above steps out and the frame grows to 4:5.4); the app on a band of light (a full-width `--tintA` to white gradient, three glass cards each with a product fragment peeking out of a lit well: brief, offer, results); how it works (a 1288 x 652 box: one ribbon of the hero's silk folded into the 8 of 8x, a third of the width wide and as tall as the box, standing in the gap between four cards a third of the width each, two a side with the right pair a step lower; each card is white fading to `--cardTint` with a 28px icon tile, a 20px title, a line or two and lavender tag chips; a 1.3px `--wire` runs from a violet dot on each card's inner edge, level, then angled to a white ring on the ribbon's outer edge, drawn in when the section enters; Brief, Match, Approve, Pay; the 8 moves (only the light, flowing through the silk) and the steps flow around it in turn (see Motion); under 1080px the 8 sits above the cards two by two, and the wires go); in their words (one quote at a time with pictures set into the line, the speaker, and three brand tiles to pick the quote, radios driven by `:has()`); rates (one plan card on a glow beside the copy, a format picker, what's included and the follower switch, all `:has()`); the posts marquee; questions; the close; the footer and its fading "8x" wordmark.
- The sheet, creators: the statement; built for (a full card of a campaign: the product edge to edge, the brand's tile, what it pays, "Apply with your rate"); how it works (Connect, Pick, Write, Get paid around the rose 8, with `id="how"` for the hero's second action); the posts marquee; in their words (three creators); the app band (brief, results, payments); rates; questions; the close; the footer.
- **The close** is never the hero again: a 36px card of light (a white glow from the top left over a `--tintB` to `--tintA` to `--tintC` gradient) with the words and two actions on its left and the app running off its right and lower edges: brands see the Creators screen (`Desk view="discover"`) with Kenji's draft waiting (`DraftFrag`) and escrow funded; creators see their dashboard with money ready to withdraw (`WithdrawFrag`) and Kinetic's escrow.
- At 900px and below the switch takes its own row, "Log in" hides, the brands headline drops its break, the stage is `clamp(360px, 96vw, 540px)` at 26px with the Desk 150% wide from 5% (the post at the bottom left); the creators hero stacks, its card centred at up to 300px and the offer hidden; every two-column section stacks (rates put the copy first); the close stacks with the app in a band below the words. At 640px the brands chip goes and the steps and cards go one to a row.

**The door** (`src/app/(auth)/Door.tsx`, `auth.module.css`), every sign-in and sign-up step: a `0.94fr | 1.06fr` grid with 14px gaps on the mist. Left, a white 30px card: the lockup, a Brand | Creator swap pill, a 300-weight title, on sign-in and sign-up a 48px quiet pill "Continue with Google" (the four-colour G) over an "or with your email" rule, the form (420px), demo accounts as `--slab-2` rows with a face or a tile, and local links. Right, a sticky silk panel (30px) with the same moving silk as the side's landing (rose for creators), one line of headline, the Desk at 132% width from 11% (bleeding off the right) and an X post over it; a step that waits on an email shows the letter as a white card instead of the post. At 900px the silk becomes a 250px band with the Desk at 190% and no post or letter, and the form a sheet over it with 28px top corners.

## Elevation & Depth

Paper in soft light: white cards lifted off the lilac-white ground by a 1px ink hairline and a soft shadow tinted violet (`rgb(45 38 99)`), never black.
- `--shadow-1` `0 1px 2px rgb(45 38 99 / 0.05), 0 8px 20px -12px rgb(45 38 99 / 0.18)`: every card, panel and control at rest.
- `--shadow-2` `0 2px 6px rgb(45 38 99 / 0.05), 0 24px 48px -24px rgb(45 38 99 / 0.28)`: hover lift, the workspace banner, the onboarding card.
- `--shadow-3` `0 4px 10px rgb(45 38 99 / 0.06), 0 50px 90px -40px rgb(45 38 99 / 0.36)`: dialogs, drawers, menus, the bell list, Ask 8x.
- Edges: `inset 0 0 0 1px var(--line)`, `--line-2` on controls and fields.
- Glass: white at 46 to 60% with `blur(16px) saturate(1.2)` and a white inset hairline. Labels on photos sit on white 82 to 90% with an 8 to 10px blur. Scrims are the ink at 24% with a 5px blur.
- The Desk sits on the silk with a white 1px ring and `0 2.6em 5.4em -2.8em rgb(45 38 99 / 0.5)`.

**The Hairline-and-Haze Rule.** Surfaces have no CSS borders, only the inset hairline and a soft ink shadow; real borders are dividers (`1px solid var(--line)`) and dashed placeholders. A haze at the top marks the card to read first. **The Glass-Over-Pictures Rule.** Frosted glass sits only over the silk, the glass art, a cover or a photo; on the ground a surface is opaque white.

## Shapes

- The ladder: 6px focus ring; 14px calendar days and feed rows; 16px fields, rows, flashes and number strips; 18px to-dos and menus; 20px photo frames, glass stats, X posts and suggestion cards; 22px figure tiles and offer cards; 24px money and campaign-run cards; 26px (`--r-xl`) panels and card shells; 30px glass heroes, dialogs, drawers, the inbox and door panels; 999px (`--r-pill`) every button, tab, tag, state and rail link.
- Frames: a person is a full card at 5:7 (4:5 when it is the feature on the landing), the photo anchored 50% 22%; a campaign cover is 16:10 in a 26px shell with an 8px inset and a 20px frame; run covers are 110px tall; post media 4:3.
- **The Mark** (`Mark` in `src/components/ui/Icons.tsx`): 8x's serif "8x" from 8x.social (its `assets/brand/8x_icon.svg`, with the off-white tile removed), one path in `currentColor` on a tight viewBox (`43 92 317 218`, about 1.45:1), so it is violet on light grounds and white on violet. Never put a tile or disc behind it, except where it stands in as the 8x.tweets team's avatar (a white 28 to 44px tile in Messages and Community). `size` is its height.
- **The lockup** (`Logo`): the Mark is the name's "8x" and ".tweets" follows in type, baseline to baseline with a 0.05em gap and the Mark at 0.76em, so it sizes from the text around it (20px in the rail, 22px on the door, 23px in the landing nav). Its accessible name is the full `SITE.name`. Ask 8x reads "Ask" followed by the Mark.
- **Favicon**: `src/app/icon.svg` is the Mark on a square viewBox in `#1F201F` that turns white under `prefers-color-scheme: dark`; `src/app/favicon.ico` is the same at 16 to 64px on transparent. **The footer wordmark** is the Mark as a CSS mask (`public/brand/8x.svg`) over the fading `#d6dce8` to transparent gradient, `min(88%, 860px)` wide.
- Icons: inline SVG on a 24 grid, 1.6 stroke, round caps (`Icons.tsx`); X's glyphs as X draws them.

**The Circle-and-Tile Rule.** People are circles (28, 36, 40, 44, 60, 112px); brands are rounded tiles at about a quarter of their size (9px at 30, 12px at 40, 14px at 44 to 46, 18px at 64); the 8x.tweets team is the Mark on a white tile. A glance says who is who.

## Components

The kit lives in `src/components/app/`; reach for it before writing CSS. `Stats` and `Avatar` (`ui.tsx`), `Checks` (`kit.tsx`) and `BrandCampaignCard` (`cards.tsx`) are exported but unused; `Figures` replaces `Stats`.

| For | Use | File |
|---|---|---|
| A page title with actions | `PageHead` | `ui.tsx` |
| A screen that opens on glass with its figures | `SkyHero` + `GlassStat` | `viz.tsx` |
| A white card with a head (`lit` adds the haze) | `Panel` | `ui.tsx` |
| A row of figures (`hot` marks one) / a balance | `Figures` / `MoneyCard` | `kit.tsx` / `viz.tsx` |
| Shares / a small series / a trend | `Donut` / `Columns` / `Spark` | `viz.tsx` |
| How far along | `Meter`, `Ring` | `viz.tsx`, `kit.tsx` |
| Over time / a breakdown / a campaign's dates | `LineChart` / `Bars` / `Calendar` | `kit.tsx` |
| Who is in | `AvatarStack` | `viz.tsx` |
| What only you can move | `Todo` | `kit.tsx` |
| A deal's steps / every step on one thing / what happened | `Journey` / `Timeline` / `Feed` | `kit.tsx` |
| Views of one thing / piles with counts | `Seg` / `Tabs` | `kit.tsx` / `ui.tsx` |
| A state / nothing yet / an action's result | `Status` / `Empty` / `Flash` | `ui.tsx` |
| A person / a campaign / a brand | `CreatorCard` (on `FullCard`) / `CampaignCard` / `BrandTile` | `cards.tsx` / `ui/BrandTile.tsx` |
| A post or a draft | `XPost` | `XPost.tsx` |
| A dialog or a sheet, at `?d=` | `Dialog` / `Drawer` | `kit.tsx` |

**Buttons and switches.**
- `u.pill` is violet, 44px, 14.5px 500, and rises 1px to `--navy-2` on hover: the one thing to do. `u.ghost` is white with a `--line-2` hairline: everything else. `u.small` is 36px at 13.5px. Forms use `f.submit` (48px violet) and `f.quiet` (46px white); `.danger` turns them `--bad`.
- On glass: `glassPill` (white 60%, blur 14px) and the workspace's `glassBtn` (white 80%). `u.iconBtn` is a 36px white circle. `u.link` is blue 500, underlined on hover.
- The landing's `.navyBtn`, `.whiteBtn` and `.lineBtn` (white 16% with a 24% ink hairline, for pictures) are 48px (42px small), 15px 500, and press to 0.98.
- `Tabs` is a white capsule of 38px pill links with counts, the current one violet; `Seg` is the same at 32px for views of one thing. Both are links (`?tab=`, `?view=`), so every view has an address; past three sections a screen uses them.
- Choices are pill radios (`.choice`, `.picks`) that fill violet; checkboxes and ranges take `accent-color: var(--navy)`.

**State and feedback.**
- `Status tone=` is a 24px pill, 12px 500, with a 6px dot in its color: `offer` `#5a45c2` on `#efebfd` (offer sent, invited); `waiting` `--fg-2` on `--slab-3` (applied); `work` and `review` `--warn` on `--warn-tint` (sign next, fund escrow, countered, scheduled); `good` `#147a4e` on `--good-tint` (link live); `live` the same with a dot that pulses out 6px every 1.6s (posted, a live campaign); `paid` white on violet (paid, released); `off` `--fg-3` in a `--line-2` ring (declined, closed, ended). Stages come from `src/lib/deals.ts`, phases from `src/lib/campaigns.ts`. On a cover the pill sits on white 88% with an 8px blur.
- `Flash` is the wash `#eeedfc` with a 22% blue ring and an 8px blue dot, for `?ok=`. Errors are one `--bad-tint` box above the form in `#a8263d`. `Empty` is a 64px soft ripple of blue rings, a 20px title, one 44ch line and one action.

**Figures and charts.**
- `SkyHero` puts `glass.webp` (frosted lilac and blue glass) behind a 30px card (padding `clamp(22px, 3vw, 34px)`): the h1, a 15px sub at 58ch, actions to the right, then its children in an auto-fit row (190px minimum, 12px gaps, 2-up at 640px).
- `GlassStat` and `Figures`: a 12.5 to 13px label, the light figure, a 12 to 12.5px note that turns green when `up`, and in glass a 26px area spark. `Figures` tiles are white, 22px, padded 18px 20px, 2-up at 900px; the `hot` one takes the `#d8e8fb` haze. `MoneyCard` adds a 30px violet disc beside its label and room for actions.
- `LineChart` (server SVG): a 2.2px violet line over a blue fill fading from 20%, white points ringed violet that show their value on hover, an optional blue second series, dashed `--line-3` event marks labelled in blue, 10.5px `--fg-3` axes.
- `Columns`: bars up to 44px wide with 10px tops in `#e4e1f4` to `#efedf9`; the picked bar (the highest by default) turns periwinkle `#9899e4` fading to `#ece9fd` and carries a violet value pill. `Donut`: a 13-unit ring on `--slab-3` with small gaps, a light center figure and a legend of dots, labels and values.
- `Meter` and `Bars`: 8px `--slab-3` tracks with gradient fills (blue: periwinkle to `--blue`; green: `#7fd3a9` to `--good`; violet: periwinkle to `--navy`; warn: `#f6c38d` to orange). `Spark`: 32px, green by default, or blue or violet. `Ring`: 44px with a blue arc and "1/4" inside.
- `Calendar`: a 7-column month of 14px `--slab-2` days; the posting window `#edebfd` with a blue ring, today ringed violet, key days named in blue, due days in warn, and 22px faces on the days posts went up. `AvatarStack`: circles ringed 2px white, overlapping by 28%, then "+n".

**Lists and progress.**
- `Todo`: numbered 30px discs on 18px `--slab-2` rows, each with its one action; the first row is white with the haze and a violet disc; done rows get a green disc and struck text.
- `Journey`: a white rail of 26px rings joined by 2px lines; done is violet with a check, now is white with a 2px blue ring, a 5px halo and a blue center; the lines run violet to blue; at 900px it wraps two or three to a row. `Timeline` is the same, vertical, with 24px discs. `Feed`: 38px round icons (blue tint for the key events, green for money), title, sub and time, split by hairlines.
- Rows (`u.list`, `u.row`): face or tile, text, end; 16px radius, hairlines between, `--slab-2` on hover. Tables (`u.table`) are for dense lists only, usually behind a Cards | Table `Seg`: 12.5px 450 `--fg-3` headers, 1px tops.

**Cards and people.**
- `CreatorCard` is a full card (`FullCard`, after the 8x.social creator card the user pointed to): the person's own photo sits in a square at the top of a 26px card at 5:7 (X profile photos are 1:1, so a real creator's photo shows whole, never stretched or cropped), fading at its foot into the same photo blurred (22px) to fill the rest of the card; photos are asked for at q90 (`images.qualities`); a frosted pill top left (`MatchPill`, "86% match" in violet ink from 80%, or "Not on 8x.tweets"; the landing's cards carry no corner label) and the X-blue shield top right when verified; across the lower part a blur that ramps in from clear under a violet-ink shade (`rgb(30 26 60)` from 0 to 64%), holding the name in white at 20px 500, "niche · city" at 80% white, three numbers split by 24% white rules (Followers, Engagement, Per post) and the buttons in a row. Clicks on the text fall through to the profile link; the photo eases to 1.035 and the card lifts 3px on hover. The card sets its type from its own width: smaller under 230px (two to a row on a phone), larger from 400px.
- `CampaignCard`: a 16:10 cover, a 30px brand tile and name, a 20px title, a Budget | Deliverables | Deadline strip, two actions and a bookmark (`SaveMark`).
- `BrandTile`: white with a `--line-2` hairline and a 10px radius by default, holding the brand's line mark in its tint (Arcwise `#4d68d4`, Halcyon `#6b5bd6`, Brewline `#b8672a`, Kinetic `#1a9a63`, Pixelforge `#4a57c9`, Mintline `#178a74`), its product photo (scaled 1.35), or a logo read off its site (contained, 18% padding).

**Overlays and Ask 8x.**
- `Dialog`: 560px (820px `wide`), 30px, haze on white, `--shadow-3`, rising in 520ms over the scrim. `Drawer`: a 600px white sheet 12px off the right edge, sliding in 560ms. Both live in the address (`?d=`), close by a link, and take Esc and focus from `DialogKeys`. Menus and the bell list are white 18 to 22px popovers on `--shadow-3`.
- Ask 8x (`AskKivo.tsx`, brands only): a 48px violet pill reading "Ask" and the Mark in white, fixed at the bottom right (above the tab bar on phones, hidden in Messages). It opens a 440px white sheet (28px) with a lavender-haze head, suggested questions as `--slab-2` pills, the question as a violet bubble and the answer as plain lines with blue links, read from the brand's own data.

**Forms, inbox, post and composer.**
- Forms (`form.module.css`): white fields, 48px minimum, 16px radius, 15px text, a `--line-2` hairline (`--line-3` on hover) and a blue focus ring (inset 1px at 75% plus a 4px halo at 13%); labels 13.5px 500 `--fg-2`, hints 12.5px `--fg-3`; `$` prefixes and `%` suffixes; emailed codes as 56px mono boxes (62px light Geist in two fours on the door); chips in blue tint; password strength as four 4px bars, orange then green.
- Inbox (`inbox.module.css`): one white 30px sheet, a 330px `--slab-2` list beside the thread. Their bubbles are white with a hairline (corners 20 20 20 6), mine violet (20 20 6 20), the team's the wash; deal events are small centered chips with a blue dot; a blue "New" rule marks the first unread; offers are haze cards with the price at 34px 300 and a state chip; a wash strip above the thread shows what's on the table. At 900px, one pane at a time.
- `XPost.tsx` (styles in `src/components/post/Post.module.css`) draws a post as X does in light mode: white, 20px, a `rgb(15 20 25 / 0.08)` inset, a 42px avatar, the bold name, verified in X blue, "Paid partnership with @brand" and counts in X muted, @mentions and links in X blue, likes in pink. A draft shows "Draft" or "v2" where the X mark sits.
- `Composer.tsx` covers the app on the mist under a 68px glass bar (back link, title, violet submit), in three columns: the post (17px/1.5; fixes underlined orange, considers blue; X's 280 ring in X blue, then orange, then red), suggestion cards (one open, with Apply in violet and Dismiss in white), and the side (the score ring, area filters that fill violet, the tracked link in mono, voice figures, notes on earlier versions in warn tint). Its rules run locally, no model. The product never posts on X for a creator; the one local exception says so on its button, "Post it for me (local simulation)".

**The landing's pieces** (`Desk.tsx` and `desk.module.css`; `Illustrations.tsx` and `ui.module.css`; `FullCard` from the app kit).
- `Desk`: the web app drawn in code, `aria-hidden`, a picture rather than a screen to use: a miniature of the real screens at the app's own proportions (the drawing is 90em wide and 1em stands for 16px of the app at 1440px, so its sizes are the app's divided by 16). The brand dashboard (the rail with the Brand pill and bell; the glass banner with Wallet and New campaign and four GlassStats; To do beside Engagement; Money beside Running campaigns), the creator dashboard (the banner, then their own card beside Your earnings), and for brands the Creators screen (`view="discover"`: filters, topic chips, match-ranked full cards), all with the demo's own figures. When a real screen changes, change its drawing with it. It takes its size from its wrapper, so the hero, the close and the door only set a width.
- `SilkVideo side=` puts the silk loop behind a stage (see Imagery). `PostCard` is an X post as X draws it. The fragments (`BriefFrag`, `OfferFrag`, `ListFrag`, `BarsFrag`, `DraftFrag`, `WithdrawFrag`) are small drawn pieces of the product for the band, the hero and the close.
- The marquee: `PostCard`s 360px wide (300px on phones) in a doubled track, 110s linear (90s on phones), paused on hover and focus, faded over 5% at each end.
- Quotes on the landing are illustrative like everything else there, and the footer says so. Pictures set into a quote are `aria-hidden` chips 1.08em tall: faces, an icon on `--lilac-tint`, or a product crop.
- Exceptions to the craft floor, kept from the Payno version: the 2x2 grid of icon feature cards, the gradient-faded wordmark, and uppercase labels tracked 0.08 to 0.1em in the footer.

**Imagery.**
- Silk: `public/landing/silk.webp` is the first frame of `silk.mp4` (1080p) and `silk-720.mp4` (900px and below): Veo footage of iridescent lilac and blue silk, slowed 2x and crossfaded so it loops without a seam, with the black edge rows cropped. `silk-rose.*` is the same footage turned 24 degrees toward rose with ffmpeg (`hue=h=24:s=1.06`) for the creator side; the tint is baked in because a CSS filter over a playing video let dark pixels escape the stage's rounded corners. `SilkVideo` writes a raw `<video autoplay muted loop playsinline>` over the still so muted autoplay works before any script; reduced motion sees only the still. It runs on the heroes and the door.
- Glass: `glass.webp` (frosted lilac and blue glass) sits behind `SkyHero`, the app's banners, the new-campaign cards and the profile and onboarding stages. The 8 in "how it works" is an 8s loop: `eight.mp4` and `eight-640.mp4` (brands), `eight-rose.mp4` and `eight-rose-640.mp4` (creators, every frame turned 24 degrees toward rose), each with its first frame as the poster (`eight-poster.webp`, `eight-rose-poster.webp`), which is all reduced motion sees. The ribbon is one ribbon of the hero's silk folded into a figure-eight, rendered with Gemini (`gemini-3-pro-image`) from the silk still, on chroma green and keyed out. Veo 3.1 then moved it with that keyed 8 on white as both the first and the last frame, so the loop closes on itself and the ribbon holds its outline under the wires' rings (checked frame by frame); only the light moves, like liquid mother-of-pearl. The page's glow and the lilac shade under the base are baked into the frames on the page's white (the glow's gradient dithered, the white left exact), so there is no alpha and no blend mode and Safari matches Chrome; the video's box runs 4% past the 8's box each side and 7% below it. H.264 at 960 wide (640 under 900px), about 1.5MB and 650KB; `AutoPlay lazy` loads it only as it nears the screen (`preload="none"`, no autoplay attribute) and pauses it off screen. Nothing is a photo of sky, clouds or a phone.
- A creator's X photo is ours to serve: on every import (`importX`) the original upload (else 400x400) is fetched from X's hosts only, fitted inside 1000px, stored as WebP in the `images` table by content hash and served from `/img/<id>.webp` with a year's cache (`src/lib/images.ts`, `src/app/img/[file]/route.ts`; the address rules are checked by `scripts/check_xphoto.mjs`).
- People: `public/landing/people/` holds the demo creators' card photos, square at 1200px like real X photos (upscaled from the first portraits with Gemini, faces unchanged), `public/avatars/` the small profile photos (circles): real-looking, candid, natural light, never moving. Post photos (`public/media/`, from `scripts/gen_assets.py`) and landing covers are daylight phone photos with no real logos or readable text. `public/products/` still holds the dark stage's black-plinth shots (`scripts/gen_cinema.py`), used as five seeded campaign covers, in the new-campaign cover picker and as brand photos; they do not meet the daylight rule.

## Motion

`--ease-out` `cubic-bezier(0.16, 1, 0.3, 1)` carries nearly everything (the landing calls it `--ease`), `--ease-in` `cubic-bezier(0.7, 0, 0.84, 0)` the exits, `--ease-in-out` `cubic-bezier(0.65, 0, 0.35, 1)` the side slide. `--d-2` (280ms) is for hover and color, `--d-3` (520ms) for state and lift; `--d-1` and `--d-4` are declared but unused.
- **App**: calm, and only in answer to a click. Buttons rise 1px; cards rise 2 to 3px to `--shadow-2`; dialogs rise from 14px, 0.985 scale and a 6px blur (520ms); drawers slide 40px (560ms); popovers pop 6px (220ms); Ask 8x opens in 320ms; a 700ms spinner runs while a form is pending. Nothing rises on scroll. On the door the Desk lifts out of a 14px blur (1200ms) and the post or the letter unblurs after 500ms.
- **Landing, on load**: headline words rise out of their masks (1100ms, 160ms plus 55ms a word); the aside unblurs at 560ms; the stage rises 40px into place (1500ms from 200ms); the Desk (brands) or the creator's card (creators) lifts out of a 16px blur inside it (1500ms from 380ms, 1400ms from 420ms); the offer unblurs at 850ms, the post and the chips at 1000ms; the nav drops in at 240ms.
- **Landing, on scroll**: `Motion.tsx` marks each `[data-reveal]` once in view (12% bottom margin). Words rise, cards rise 36px or unblur from 14px, the emblem's rings slide together from 38px apart, the 8 in "how it works" grows from 0.92 out of a 14px blur and its wires draw in after 700ms; 2s later the steps start to flow, a 12s loop in four beats, one per step in order around the 8: its ring on the ribbon flares violet with a halo, a spark runs the wire to the card's dot, the dot pops, and the card lights (a violet hairline and a deeper shadow, the icon tile in violet) and hands on to the next (on phones, without wires, just the cards light in turn); the quote and the plan card cross-fade when picked, and in the close the Desk lifts out of a 16px blur with its two widgets following at 700ms. Without script everything shows (`@media (scripting: enabled)`).
- **Side switch** between "/" and "/creators": a view transition. The old page fades and blurs (240ms) while sliding 6vw toward its own side at 0.985 (520ms); the new one slides in from its side (620ms) and fades up after 160ms. Creators come from the left, brands from the right; the nav stays put.
- **Reduced motion**: `globals.css` cuts every animation and transition to 0.001ms; the landing turns them off, hides the silk video and lets the marquee scroll by hand.

**The Nothing-Advances-On-Its-Own Rule.** Every change is somebody's click: offers don't expire, drafts don't approve themselves, escrow doesn't release itself, and no screen, carousel or list moves on a timer (the flow list opens on a click). The landing's posts marquee is the one exception, asked for by the user, and it pauses on hover and focus. The looping silk and the Live dot are ambient, not advancing.

## Do's and Don'ts

### Do:
- **Do** open a screen with a picture and its handful of figures (`SkyHero` and `GlassStat`, a cover banner, a face), then white cards on the ground.
- **Do** show rather than tell: a face for every person, a tile for every brand, a cover for every campaign, and a chart, ring, meter or column beside every number. Paragraphs belong in empty states, dialogs and briefs.
- **Do** keep one violet action per view; everything else is a white ghost pill.
- **Do** answer "what needs me" first (`Todo`, rail counts, the inbox strip), then how it's going, then history.
- **Do** put every view in the address (`Tabs`, `Seg`, `Dialog` at `?d=`) and answer actions through it (`?ok=`, `?e=`).
- **Do** keep figures light (300), tabular and formatted by `src/lib/states.ts`, with the unit small beside them.
- **Do** draw posts and drafts with `XPost`, in X's light-mode colors, and use those colors nowhere else.
- **Do** use the kit and the `:root` tokens before adding CSS or a new hex.
- **Do** give every animation a reduced-motion end state, and let landing content show without script.

### Don't:
- **Don't** go dark: no dark mode, dark sections, night skies, space or neon. Light and daylight only.
- **Don't** make anything cartoonish: no mascots, illustrated characters or generated cartoon avatars. People are real-looking daylight portraits and never move inside a card.
- **Don't** write paragraphs where a figure, face, chart or card would do; keep copy short and plain, and call the product `8x.tweets`.
- **Don't** use em dashes in product copy; use a comma, a colon or a full stop.
- **Don't** put arrows on buttons or links (no `Arrow` or `Back` icon beside a label) or use unicode arrow glyphs; the words are enough ("All campaigns").
- **Don't** let anything advance on its own: no auto-rotating heroes, carousels, timers or expiring offers. The landing's posts marquee is the one exception and pauses on hover.
- **Don't** put portrait grids or "% match" in a hero or first viewport; the match pill belongs on cards ranked against a campaign.
- **Don't** add a second accent or use state colors as decoration; green means money in, growth or live.
- **Don't** outline surfaces with borders or cast black, hard or sideways shadows; use the hairline and the ink-tinted shadow scale.
- **Don't** put glass on the plain ground; it belongs over the silk, the glass art, covers and photos.
- **Don't** pitch the product as a phone app: no phone mockups, hands holding phones, iOS status bars or lock screens on the landing or the door. The web app at a desk is the picture.
- **Don't** bring the sky back: no clouds, sky photos or cyan glows. The ground is lilac with a hint of blue.
- **Don't** repeat the hero in the close, or let the two sides mirror each other with only the words swapped: each side opens and closes on its own picture.
- **Don't** frame a person's photo on a white card; people are full cards, the photo edge to edge.
- **Don't** build on `--ember`, `--cobalt`, `--hot`, `--key` or `--fill`, or set type in anything but Geist and Geist Mono.
