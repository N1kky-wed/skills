# Taste: the user's rules (the wheel)

Every line here is something the user said or corrected on a real site. Quotes are their words. When a new
correction comes in, add it under the right heading with the project and date, and say why it matters.

## Process

- **No design boards.** Never present your own design options as Artifact design canvases or mockup boards. Build the
  chosen look in the real code with real assets, show real screenshots, and let git be the rollback. ("do not do the
  boards like that, they are bad ... never use those design boards again", 8x.tweets, 2026-09-28)
- **Ten references on one page is how a direction gets chosen.** When nothing is pinned, show ten numbered hero
  references at full size on one page in the pane and let them pick ("i like this way of showing make it a default
  for the mahoraga skill to show 10 references like this", 8x.careers + Playmakers, 2026-10-03). Two concept
  references offered on their own were both turned down ("dont like both show me 10 refernce hero screens in one
  page"), and references are opened in the pane, never only described ("show me them in the browser pane").
- **Research where they can see it.** Browse references in the browser pane, not in a headless agent. ("could u
  research in the browser pane so i can also see?", careNext, 2026-10-02)
- **Their link is the direction.** When they answer a direction question with a reference ("i love this"), build that
  reference's world faithfully; it beats anything rolled or proposed. (AIVENT for 8x.tweets, VitAI for careNext)
- **A pinned reference is matched in composition and proportion, not just palette.** Measure its hero height,
  headline size, rails, section order and spacing at the target width and build to those numbers; drop your own
  habits (a giant hero, another project's signature motion). ("looks bad doesnt look like the selected design at
  all...", 8x.careers + Playmakers on Stackly, 2026-10-04: the first pass had an 84px headline in an 80svh hero, selfie
  frames as the collage and careNext's receding hero; the rebuild at Stackly's measured 48px, compact hero and
  posed black-and-white photography landed.)
- **Never compose a new landing from your own taste first.** With nothing pinned, the ten-reference page comes
  before any build, even on a rush ("asap"). Two self-composed passes of the comment desk (warm photography with a
  serif, then the platform's own hero with a prompt bar and floating cards) were called "looks like ai slop" (8x
  Comment Desk, 2026-10-04); the user then pinned SphereAI and the faithful rebuild replaced both. A pinned reference
  for a marketing page outranks the platform-theme rule below; the product screens keep the platform theme.
- **A moodboard pins the look, not the layout.** A brand board (colour, type, photo rules, a graphic) tells you how things look, not how the page is built. Still run the ten-reference page for the layout, inside the board's world. A first pass that applied the 8x visual-system board to a stock layout (hero, bento, stats, rules list, footer) got "the idea is right but the entire layout is wayy to simple and lame rn, mahoraga research" (8x ecosystem site, 2026-10-10).
- **"Love N" is not always a pin.** Liking a reference can be just liking it. When the same message also names other
  sources (designers to study, a material like liquid glass) and asks for something unique, ask or treat it as one
  input among several, not the layout to copy. ("dont pin the first one its just something i liked thats it, doesnt
  mean anything", 8x X + LinkedIn POC, 2026-10-09)
- **Designers to study are references, not a brief for your own concept.** When the user names designers ("get more
  transitions and animations ... from <profiles>") and a material ("true liquid glass"), put their actual shots (and
  the material's best examples) on the ten-reference page and let them pick; do not invent a concept from them. A
  self-made concept (a WebGL glass 8 over a feed of posts, dark, light type) got "not a fan of this at all ... the
  whole direction" (8x X + LinkedIn POC, 2026-10-09).
- **"More of N"** means: open that reference's own screens (every attachment on the shot) first, then ten more in its
  family, on one page. The pick that follows is the pinned reference.
- **Measure the reference, fit to it.** Cross-sections, colors at offsets, falloffs; then fit parameters and compare
  side by side before showing. The user judges by eye and flags anything not physically plausible: "static, should
  be flowing", "too thin and sharp, not like liquid", "too much smoke, unnatural", rim lines, neon outlines,
  floating shelves. (huly hero recreation, 2026-09-26)
- **Send the reference image to Gemini** instead of describing it. ("its simple bro yk u can send the reference image
  to gemini..", 2026-09-28)
- **An object's motion must flow the way the reference's does.** Study the reference's frames for the motion's shape
  before generating anything: Alex Bender's coin rolls forward round a hoop without ever stopping or reversing. A
  Veo take that spun the coin in place and flipped it read as "the coin doesnt flow.. properly" (8x POC brand hero,
  2026-10-09). When the motion is the point (rolling, orbiting, scroll-driven), build the object in real 3D
  (three.js, physical glass with transmission) so it moves continuously at 60fps and obeys physics.
- **Generated video only where nothing must line up with page geometry**; make light follow real outlines in code.
  Motion must cover the whole form; animate the material itself, not a glint travelling over it. ("just a random
  glowing ball now, before thing was better", silk 8 loop, 2026-09-30)
- **Fix a flaw without changing the look they already approved.**
- **Keep them posted.** Short status lines while working; they get uneasy after long silent stretches.
- **A board is evidence, not the answer, and their circled picks lead.** Expand a team moodboard into a system
  rather than copying it ("expand on it, the mood board is not the final answer"), but grow it from the picks they
  point at; never write off a pick in your own notes. A "drop the colourful gradient cards" note was answered with
  those exact cards circled: "lean more into this slightly color full glassmorphic/liquid glass". Board tiles are
  pictures; no notes tile unless asked ("no need any notes"). (8x brand moodboard, 2026-10-08)
- **A product is not a brand exercise.** Don't carry a moodboard's identity idea (a slogan concept, a "grey world"
  rule, a photo-and-glass gimmick) onto a product's landing and app screens. A product POC still goes through the
  full loop: research in the pane, the ten-reference page, their pick, then a build that is premium and unique on its
  own terms. ("dont go at it as a brand kinda thing u are free to use the full mahoraga cycle and make it as periumum
  and unique as possible from scratch", 8x X + LinkedIn POC, 2026-10-09)
- **Audit every section before showing it, at their pane's size, after the entrances have played.** Shoot each
  section (not just the hero) and look for: a word cut off at an edge (a static footer wordmark), a word left alone on
  a line, a label crossing a graphic (a gauge's caption over its arc), an empty band inside a card, a box left behind
  a cut-out, a row clipped at the page padding instead of running to the window edge, a placeholder mark. ("many other
  sections are broken why can't u put some care into it", 8x X + LinkedIn POC, 2026-10-09) Read their pane's size
  with `innerWidth`/`innerHeight` in the pane and audit there.
- **A port into an existing app looks exactly like the approved original; the host's legacy never leaks in.** When
  an approved page moves into an older codebase, the host's globals (a base layer that sets its face and weight on
  every heading, press-to-shrink on links, its scrollbars and page ground) and its older libraries (framer-motion 12
  against the original's motion 14 mapped the hero's scroll timeline differently and left a label over the brand
  strip) are the bugs. Run the original's exact library versions, undo the host's globals for the ported page only
  (in the right cascade layer so the page's own utilities still win), then diff computed styles element by element
  against the original at the same scroll stops in both themes and on a phone until only font naming differs.
  Delete what the port replaced: the old components, the CSS only they used, the tests that pinned them. ("why are u
  messing it up, i told u to override all of linkedin stuff ... remove any legacy stuff", 8x-linkedin landing,
  2026-10-10)
- **Python for scripts**, not PowerShell or curl pipelines.

## Look

- **An app's home screen is the way in, not a dashboard.** A ready page with two header buttons, an embedded
  terminal and a six-row details card was "this page looks dumb no need all of this keep it clean" (8x Desktops,
  2026-10-22). One big picture tile per tool that opens it, and the few facts worth knowing in one quiet line (with
  click-to-copy where it helps); no facts card restating what the header already says.

- **Premium is restraint; count the effects.** Each piece of the POC landing was copied from the pinned crypto shot
  or asked for on its own (soft sparkles, glows, gauge and ring widgets, floating 3D app tiles, a rippling video field,
  rings in the passage shader, a marquee). Stacked on one page they read as "gimicish and cheap simple design.. not
  luxry preimum" (8x X + LinkedIn POC, 2026-10-09). Luxury comes from fewer, bigger moves: a typeface with character,
  real photography or one considered object, generous space, quiet motion. When the user doubts that a direction is
  premium, put ten premium references on one page (light editorial, cinematic, gallery-minimal, members club, private
  bank, one precious object) rather than polishing the old direction.
- **A hero carries one picture and one line.** Copying everything a reference's hero holds (Curiosity Lab's hairline
  grid, two great circles, a project card, a side note, palette squares) on top of a giant word and a figure of light
  was "not a fan of the hero section btw, a bit too much it is" (8x POC on Curiosity + Velora, 2026-10-09). Keep the
  picture, the word and one line with one button; move the rest into the sections below.
- **No people in the hero.** A figure of light and then an editorial portrait were both turned down: "i dont think we
  want any people in the hero section, can it be any iluustrations or animations or video loops?" (8x POC,
  2026-10-09). Open on a quiet video loop of the page's world with nobody in it (a grassy hill under a deep sky, a
  sea of clouds at sunrise), framed in a panel beside the headline, and let the card at its edge carry the product
  without a face (a campaign's reach, an offer).
- **"Double down on N" means the whole page in N's world, not just its hero.** After a mix of two references (Velora's
  members club + Curiosity Lab's daylight) and three heroes, the user re-pinned Velora: "actually double down on this,
  with silk in the background". Swapping only the hero and keeping the daylight sections below drew "i said double
  down on this members club, why are u still using the dreamlike.." (8x POC, 2026-10-09). Rebuild every section in
  the re-pinned reference's language (one black ground, centred lines with one gold word, tall black-and-white
  cards, smoked and gold pills, hairlines), drop the other reference entirely, and keep the earlier iteration on its
  own route for showing.
- **Silk is a house favourite for a hero field, and it must visibly move.** Lilac silk carried 8x.tweets; here black
  satin with one cool silver sheen, flipped so the bright band sweeps behind the cards and the headline sits on the
  dark. Six Veo takes locked to the still (first frame = last frame), with two prompts, all crumpled the cloth mid-loop
  and snapped back. A WebGL shader breathing the still drew "i dont think the background hero section is moving..":
  its swell moved the folds a few pixels a second, and the browser pane ran requestAnimationFrame at about 1fps, so
  anything drawn per frame in script looked frozen there. Use real footage: a free Veo take (no last frame), its end
  crossfaded into its start, then `hero_loop.py` (2x, AV1 + H.264, phone cut). Video keeps playing where script
  animation is throttled. (8x POC, 2026-10-09)
- **Motion that stands out is studied, not invented.** "we need like some amazing transitions between sections or
  like really good animations from somewhere so it kinda standsout", then "really study the transitions and
  animations from other websites yeah? awwards winning other animations from dribble or other well known websites"
  (8x POC, 2026-10-09). Record six or so winners and product sites scrolling (`scripts/scroll_frames.py`), show the
  study board, and give each section one of their moves (`references/motion.md` 7b).
- **A landing that feels short is missing the category's sections.** "the landing page is a bit too short, u can
  find more sections from the competetiors pages as well": run `scripts/sections.py` over the category's leaders and
  add the sections they share (a manifesto, both sides, the process, the trust story, an FAQ), with only the
  product's own facts in them. (8x POC, 2026-10-09)
- **Background silk moves slowly.** A Veo silk take slowed 2x was "moving too fast"; a quarter of Veo's speed
  (`hero_loop.py --slow 4`) reads as calm. (8x POC, 2026-10-09)
- **A light mode is the same page turned over, not a new one** ("do a light mode as well"): tokens for the ground,
  its text and the filled pill; the accent darkened until it keeps 4.5:1 on the light ground (Velora's gold became
  #8A6A2A on ivory); its own silk; the product window stays dark like a device on linen; the switch opens as a
  circle from the button. (8x POC, 2026-10-09)
- **Show the product as its real, full dashboard: the user's own 8x.tweets landing mock is the bar.** A bar chart in
  a white SaaS window drew "why are we underselling with some cheap dashboard here"; a sparse "statement" version (one
  big serif figure, two hairlines, three post rows) then drew "this isn't a good mock ui" (8x POC, 2026-10-09/10).
  What lands is 8x.tweets' own `x-marketplace/src/components/landing/Desk.tsx`, redrawn at the app's proportions (90em
  = a 1440px app, so it scales from its own width): a rail with icons and counts, a greeting banner over the page's
  own material (its silk) with facts, actions and four glass stat tiles with sparklines, a numbered to-do list with
  pill actions, one smooth chart with a callout on the peak, a money donut, running campaigns with cover photos and
  network chips. Set it on a stage of the page's material, cropped at the bottom like a screenshot, with a real post
  and a payout toast floating off its edges at their own depths. It follows the page's theme. (`8x-poc` lux/desk.tsx)
- **Graphs are smooth.** "we dont want the graphs to be sharp..": draw lines as monotone cubic curves (they never
  overshoot, so a quiet week stays at zero), give the data a rounded rise and fall instead of spikes, round the line
  ends, and lay a soft gradient fill under each line; sparklines too.
- **Step pictures are the product living through the step, never monochrome objects.** Black-and-white object photos
  (an envelope, a microphone, a vault) for "how it works" drew "can this be some sort of ui mockup with live things
  happening or like nice visual image instead of this monochrome bs" (8x POC, 2026-10-10). Each step's picture is a
  real screen of that step acting itself out in a loop while on screen (the brief typing, creators being checked, a
  draft approved, the fee released), on the page's material in a jewel tone per step, flowing, softened (a baked blur,
  lower contrast: the sharp version was "too prominent"). (`8x-poc` lux/live.tsx)
- **One face, taken from the user's own products.** "i dont like the font, use one font from 8x.business or twitter":
  read the live sites' computed fonts (8x.business is Inter, 8x.tweets is Geist) and set the whole page in one of them;
  Geist Light for display matched the quiet luxury direction. No display serif beside it. (8x POC, 2026-10-10)
- **Light mode is very light blue, never cream or gold.** "i told u i dont like cream/gold in the light mode for the
  hue u can maybe use vvv light blue": ground #F3F7FC, blue-black ink #0E1726, and the brand's own blue for accents and
  the filled pill (8x.business's #2F55E0, measured off its live site); light-mode silk recoloured to sky blue (keep the
  approved motion: desaturate, then tint per channel with ffmpeg). (8x POC, 2026-10-10) Very light still has to read
  as blue: a tint of r×0.88 g×0.97 b+12 under the 50% veil came out grey-white ("the main background silk doesnt seem
  like light blue it seems white"); r×0.74 g×0.88 b+22 (`silk-azure`) reads as light blue. Judge a tint on a frame
  under its veil, side by side with the others, before encoding, and check the video's edge rows: a take's few black
  rows vanish on a dark theme and show as grey lines on a light one.
- **A live mock never holds room for what arrives later.** An invisible "Your rate per post" row waiting for the
  scene's last beat left each account half empty: "empty space" (8x POC connect scene, 2026-10-10). Late details
  join a line that is already there (the follower line gains "· $525 a post") or the mock is laid out for its first
  state, never a blank band kept at opacity 0.
- **A card's picture shows its label.** A colour card labelled "Founders" that cropped an empty office chair out of
  its room "dont make sense". When a card is a window onto a wider photo, compose that photo so the part the card
  crops is the subject (a founder's desk: laptop, lamp, a sketched plan) and the part behind the room's words is calm.
- **Background silk stays quiet and keeps flowing.** "the background silk is too noticeable": a veil of the ground
  over it (62% by night, 50% by day). "keep the background flowing here as well": every silk field on the page is the
  loop, not a still. (8x POC, 2026-10-10)
- **Nothing decorative is cut off by a section edge.** A halo larger than its section showed a hard horizontal cut
  ("cut off"); fade it out toward the section's top and bottom with a mask on a full-section wrapper. (8x POC)
- **The brand's real logo, everywhere, never a drawn stand-in.** Find the actual mark (the product's `icon.svg`,
  brand SVGs, a logo PNG) before drawing anything, render it as a reference, and pass it to Gemini for any object that
  carries it (a 3D tile embosses exactly those letterforms). An "8" drawn as two rings on a tile and in the nav was "8
  doesnt look right like our logo" (8x X + LinkedIn POC, 2026-10-09).
- **Each section's object is its own version, as in the reference.** Where the reference shows a different
  rendering of the mark per section (PvX: teal tiles in the hero, a near-black glass app tile with a lit aqua rim in
  the toolkit and statement, the mark itself as glowing glass over falling light in the closing card), generate each
  one from a crop of that section, never reuse the hero asset, and make it a Veo loop where the reference moves. ("u
  are reusing the same 8x logo asset instead of generating a different version there see and compare properly,
  should be a video", 8x X + LinkedIn POC, 2026-10-09)
- **Light is soft and volumetric, with dust in it.** A beam is a column of haze with feathered edges (layered
  gradients under a horizontal mask, its top outside the frame), breathing slowly, with tiny soft sparkles drifting
  in it, never a hard-edged clip-path cone ("look at the light here at pvx and u just made it lame"). Copy the small
  ambient details too: PvX's pixel-sized soft sparkles in the light around the hero tiles ("like u see those little
  soft sparkles?"). A drifting background glow blob behind a statement can go when they say so ("no background glow
  here please"); the object's own light carries the section. (8x X + LinkedIn POC, 2026-10-09)
- **A reference's decorative motif can be dropped when it reads as out of place.** PvX's drawn line strands, copied
  faithfully, got "i dont like the background green lines doing something thing, it sucks and out of place do
  something else really nice video loops". The field behind a hero can be a generated loop (dark liquid rippling out
  from under the hero objects: Veo 3.1, first frame = last frame, `hero_loop.py`) as long as the layout, type and
  motion stay the reference's.

- **Backgrounds are never plain.** Texture, light, grain or motion on every field ("being plain would be boring"),
  made cheaply (a baked grain tile, gradients) so it costs nothing per frame.
- **A new direction rebuilds every section, not just the hero.** Pieces carried over from a rejected direction and
  only recoloured (a dark stats card, a black-and-white portrait grid, text-heavy mock windows) read as leftovers. Take
  each section from the pinned hero's own motif instead (8x: faces in glass bubbles, figures inside glass orbs, each
  step's object held in the orb). ("could be more visual, find a better way to display them feels like they were left
  overs from the previous stuff", 8x.careers + Playmakers, 2026-10-04)
- **Sibling sites get the same finish.** When two sites share a hero motif, make the second centrepiece from the
  first one's best still (same sphere, light and background; only the mark changes) instead of generating it fresh,
  and don't repeat the mark as an object beside it. ("playmakers hero section doesnt seem all that polished like the
  hero section on the 8x careers", 2026-10-04)
- **A data story is a scene, not a chart.** A grid of a thousand dots in a white box is dull even when it animates;
  tell the same numbers in the hero's world (a turning sphere of porcelain beads that thins out until five become
  faces). ("this section can be made way more interesting", Playmakers' round, 2026-10-04)
- **Bubbles are whole.** A sphere is never cut by the frame or covered by a label; leave it room and float the label
  below it. ("make them properly bubbles some feel like they are stuck with half bubble")
- **Faces in black and white come to colour on hover**, and the film they open plays in colour; make the colour twin
  from the same frame with the same tone curve so the hover reads as colour arriving, not a new photo. ("color of their
  faces when hover")
- **Real profile pictures, never initials in a circle.** An example person gets a proper portrait (generated and
  labelled as example content), and lists of people use their photos. ("put proper pfp")
- **Visuals over text.** Prefer pictures, product UI, photography, film; a section that reads as a wall of text where
  a picture could carry it is unfinished.
- **Neighbouring dark sections share one ground, and texture covers whole sections.** Two near-blacks a shade apart
  (#0b0c0e over #111214) make a visible seam, and grain laid on an inner max-width container shows as a lighter
  rectangle inside the section. Give consecutive dark sections the same colour, put grain on the section itself, and
  fade any light (a beam) in from the section's top edge so it never starts at a line. Measure row brightness across
  the join before showing it. ("softer blend here with the above section, why different shades inside this box?", 8x
  X + LinkedIn POC, 2026-10-09)
- **A product mock is a real-size screen seen through its frame, not a miniature.** Lay the app out at its own
  pixel size (17px nav, 18px titles, a chart with dotted grid and axis labels) and scale it so its left part fills the
  card while the rest runs off the edge, the way PvX's Growth Engine screenshot is cropped. One chart carries the
  story, with one callout (a face on the week a post took off); never a dashboard shrunk to fit with 9px KPI chips,
  crude blocky bars and a cramped truncated list. ("not good mock", 8x X + LinkedIn POC, 2026-10-09)
- **Mocks are pictures and fill their frames.** ("could u make the ui mocks visual?"; "dont make it look empty
  yeah?", with an empty band circled inside a browser mock, careNext 2026-10-02)
- **Show the real device.** Web products in a browser window, tablet apps on a tablet, phones only for phone apps.
  ("didn't like ... the phone mockup since it makes it look like an mobile app instead of the website", 8x.tweets
  team; "are they doing mobile apps or is it a website?", careNext)
- **No sky-and-clouds, hands holding phones, iOS status bars or lock screens** as the product picture (8x.tweets).
- **Hero and close must differ**, and two audiences (brand vs creator) each need their own pictures and order, not
  swapped words. ("the footer and the hero sections feel the same", 8x.tweets)
- **Use the space.** No empty bands in a hero stage, no holes in grids ("maintain symmtery among the boxes ... no
  empty space"), pages up to 1600px wide in apps.
- **Two-line hero headline on desktop** (8x.tweets).
- **No blurry or low-fidelity decoration** (a blurred striped sphere in empty states was removed) and no redundant
  chrome.
- **No arrows on buttons or links** in the lilac 8x.tweets world; carried as the default lean elsewhere.
- **Creator cards are full cards and still**: photo edge to edge, frosted lower part with name, stats, buttons; no
  moving people in cards; no Tinder-style portrait grids, match percentages or "brand wants you" offer cards.
  Engagement is always a number, never a percentage (x-marketplace, 2026-09-26 and 10-01).
  The name and role sit centred over the photo, each figure centred in its column ("center the names and the roles",
  8x POC, 2026-10-10).
- **Real faces when allowed.** With permission, the client's own people go in (careNext leadership and advisors);
  never use a real person as sample data.
- **Selfie frames are not photography.** Stills pulled from talking-head clips look amateur in a polished collage;
  keep them for the people's own section (their films) and generate posed black-and-white work scenes for the hero,
  never presented as the client's team.
- **Soft and light for 8x.tweets**: nothing dark, cartoonish or mascot-like; lilac glass and silk instead.
- **Objects on a light page are light.** A brand object (the comment desk's glass orb) on pale pages is pale glass
  with tinted cavities, not deep cobalt, and anything drawn on it (glyphs) turns dark to stay legible. ("lighter
  colors maybe", 8x Comment Desk, 2026-10-04)
- **Emphasis is a ring, not a glow** (8x Meets): a crisp ring marks the speaker, the selection, the raised hand.
- **Glass is liquid, not frosted.** What is behind shows through sharp and bends at the slab's lips like a lens:
  an SVG displacement map through `backdrop-filter: url(#…)` (Chromium), soften the map and add a sub-pixel pass
  so the bend has no steps, light the lips with inset highlights, and fall back to clear glass with lit lips
  elsewhere. A blur that frosts it reads wrong. ("want liquid glass not frosted glass", 8x Comment Desk,
  2026-10-04) The slab is flat: the bend lives only in a rim about 15% of its height (24px on a 160px box), so
  the middle shows the field straight; a band reaching the middle made it a lens that waved the ribbon into an S
  ("feels unatural does glass really do that?", same day).
- **No eyebrow label over a hero headline** (a small mono "Creator posts on X and LinkedIn" above the title was
  "remove these text", 8x POC brand hero, 2026-10-09). The headline opens the page on its own.
- **Hero titles stay clean and readable.** No object set inside a headline line (the orb in "Be the [orb]
  comment" was removed: "remove this"), and over a bright field the title gets a thin outline (2px text-stroke
  with `paint-order: stroke fill` plus a soft shadow). ("add borders to the hero titles so people can read it
  better", 8x Comment Desk, 2026-10-04)
- **Every word over a picture gets that border, without being asked.** Not only the hero title: any line set
  over a photo, a video or a bright field (the line under it, small labels, the logo strip) gets the dark outline
  (or a 1px ring of eight hard text-shadows) plus a wide soft halo, the line under it near full white, and a little
  extra dark behind the block. Judge it at the brightest moment of a reveal, while the veil is still fading in,
  not the settled state. The second time this was asked: "ensure u add borders to those text to make them properly
  readable" (the room under the 8x POC hero window, 2026-10-10).
  **But the border must not show as one.** On 8x LinkedIn the 1px ring of eight hard shadows was called out twice
  as an outline ("borders too agress again", the Team Desk sign-in over silk, 2026-10-12, after the same fix in the
  apps). Default to a soft halo only: dark words `0 2px 22px rgb(255 255 255 / 0.7)`, white words
  `0 1px 3px rgb(0 0 0 / 0.3), 0 2px 26px rgb(0 0 0 / 0.55)`; reach for a stroke only where a halo truly fails
  (white type on a very bright photo), and then thinner and fainter than you think.
- **A new page on an existing platform wears that platform's theme.** Its palette and theme switch, its typeface,
  its nav and footer, its hero language and glass; "fresh" means a fresh composition, never a new palette, serif or
  photography the rest of the product does not use. ("not in the color/theme of the rest of the platform at all.
  please try to match themes fonts etc", 8x Comment Desk, 2026-10-03)

## Copy and truth

- **Copy is direct and obvious, never a riddle.** Clever lines ("Be in the posts your buyers read", "Money moves only
  when the post does", "Your next launch deserves to be read") drew "make the copy not read like a riddle and make it
  seem direct and obvious and easily understandable everywhere, like look at naano.com" (8x POC, 2026-10-10). Read the
  references' copy in the pane first (naano.com, the client's own live sites), then write: the hero names what it is
  and the platforms ("Sponsor creator posts on X and LinkedIn."); the line under it lists what you do and get, in order
  (find, brief, approve, pay when live); section titles say what the section shows ("How it works", "How payment
  works", "Common questions", "Track every campaign in one place"); step titles are plain verbs ("Write your brief",
  "Choose your creators", "Approve every post", "Pay when it's live"); no metaphors, no wordplay, every fact the
  product's own.
- **Words that arrive with a transition come in while it is still moving**, not after it settles ("can the words
  appear a bit sooner"): the line written in the opening room fades in at about 60% of the opening.

- **Same copy, new look** for redesigns ("make sure that we convey the same copy but in this different
  visual/animation/transitional style yeah?", careNext). Shape it; do not rewrite it.
- **No invented claims.** Samples are labeled and obey product facts.
- **Money flows in a mock are the client's real ones.** Payment methods, providers and their states come from the
  client's own app, never from what such products usually offer: a "Bank / PayPal / UPI" picker drew "we dont support
  all of these its just a seperate payout system" (8x POC, 2026-10-10). 8x pays creators to one payout route set up
  with its payments provider, money released to a wallet and withdrawn; read the app's payout screens first.
- **No promises about time.** "You're paid within seven days" drew "not a good promise to make" (8x POC, 2026-10-10),
  even where an old page of the client's said it. Say what happens and in what order (the fee is in escrow before you
  post and released once the post is live and verified), never how fast; "fast payouts" and "in minutes" are the
  same promise.
- **The client's live site is the source for their own facts.** When the user points at something of theirs ("those
  4 brands"), open their live site in the pane first and take it from there (8x.business's "Brands on 8x" strip),
  copying the real logo SVGs from the page; old repos and marketing branches lag or hold placeholders. ("chcek the live
  site itself 8x.business", 8x X + LinkedIn POC, 2026-10-09) When a name could be several companies ("Mate"), find
  the one the user named in their own messages or logs before taking its logo or facts: they meant mate-ai.chat, and
  an earlier demo had guessed usemate.ai.
- **Keep the original logo when asked** ("u can use the carenext og logo"), adapted in tone for the field.
- **A pitched redesign wears the client's own colors.** A pinned reference sets the layout, type and motion. Its
  palette does not carry over. careNext liked the VitAI build but asked for "their color scheme". So measure the
  client's palette (`capture_site.py` colors) at the start. Map it onto the reference's roles: their brand blue as a
  tint scale for the fields, their darkest navy as ink, their CTA color as the one action color. Their film posters and
  logo then sit in the world instead of clashing with it.
- **No em dashes in copy you write**; use a comma, a colon or a full stop. (8x.karma and 8x Meets enforce it with a
  test.) A client's verbatim copy keeps its own punctuation.
- **Sentence case** for labels, buttons and headings; no uppercase, letter-spaced labels in the 8x apps.

## Motion

- **Smooth, never blocking.** ("i cant even scroll to the next section form the hero section..") Compositor-only
  animation; no big blurs, no blended overlays, no width animations, no html smooth-scroll.
- **Really smooth transitions** ("make better transitions ... like really smooth transition"): a pinned hero receding
  under the next sheet, pages rising as a rounded sheet, films opening from their place to full screen.
- **Films open to full screen and play; nothing pins** ("have a section to make it go to full screen and play if
  needed no need to pin it tho!").
- **Sliders keep moving while visible** ("hero section not moving to the next product when in focus"): no
  hover/focus pause on a full-screen hero; a pause button instead.
- **Nothing cut off at the end** ("feels cut off", the footer wordmark): scroll-linked ranges must be reachable.
- **Copy a reference's motion frame by frame, not from a few stills.** When a pinned reference is a video, seek it at
  10fps (`scripts/seek_frames.py`), lay out 3-second strips, and write the motion down before building: how text
  enters (PvX: each word fades dim grey to full colour with a light blur, left to right, ~100ms apart, not a
  slide-up), how cards enter (blur to sharp, staggered), what animates after landing (counters, bars, a dot on rings),
  what drifts forever (glow, lines, logos). ("ur not getting the frame by frame transitions and animations", 8x POC on
  PvX, 2026-10-09)
- **Motion follows the reference's temperament.** A calm, precise reference gets small quick motion (14px lifts that
  finish early, photos settling from 1.04, corner ticks drawing in), never big floaty reveals or a receding hero.
  ("the animations transitions all suck", 8x.careers + Playmakers, 2026-10-04)
- **Textures can answer the pointer.** Halftone dots read as metal: they light up around the cursor with a sheen,
  through one throttled listener and a CSS mask on the same dot grid, off for touch and reduced motion. ("the
  background reacts to the hover since its like metalic dots", Stackly language, 2026-10-04)
- **Exits are animations too.** Whatever comes out of something goes back into it on screen, timed to the scene (the
  objects shrink back into the orb as it starts to wobble), never a cut to nothing. When a CSS cycle follows a video,
  drive it with a clock that only moves forward: wrapping it to zero at the video's loop made the later set vanish.
  ("i dont like how at the end of it the out side graphics just disappear instead of their animation of going inside
  when the bubble rotates again for the next cycle", Mattered hero, 8x.careers + Playmakers, 2026-10-04)
- **Only a marquee auto-advances** (8x.tweets), plus a hero slider that has a visible pause button (careNext).
- **No CSS filters on playing video.** Bake tints and grades into the file; a filter over a playing video let dark
  pixels escape the stage's rounded corners.
- **A hero video is sharp and plays at once.** Generate it at 4K, slow it only by a whole factor at the source's own
  24fps so every other frame is a real one, and encode per screen: AV1 10-bit at 2560 wide with an H.264 fallback,
  a portrait cut of the centre for phones, `+faststart`, the poster the exact first frame (`scripts/hero_loop.py`).
  The `<video>` is in the server HTML from the start, never mounted after load or idle, and its files are cached.
  A 1600px VP9 at 0.4 Mb/s, resampled to 30fps and mounted after load, was "so low quality and doesnt even load
  properly.. v unoptimized" (8x Comment Desk, 2026-10-04).
- **A heading is never blurred where it is read.** Word-by-word reveals (dim and blurred to sharp) start as the
  heading enters the bottom of the screen and finish within about a second, so it is sharp by the time it reaches
  the reading line. A reveal that waited for the block to be 18% inside the screen, then took 1.6s, was caught
  mid-way: "blured" (8x X + LinkedIn POC, 2026-10-09).
- **Reduced motion shows the finished state**, never a blank or half-revealed section (huly's answered state), and
  live motion pauses when it is off screen.

## App UI

- **A port of an approved mock is the mock, screen for screen.** When a proof of concept the user approved becomes the
  real app, rebuild each page from the mock's own markup (its sections in its order, its cards, type, spacing and
  copy) and swap only the data and the actions for the real ones. A restyle of the old page in the new colours drew
  "the poc dashboards are wayy better.. u didnt even keep any faitful for the poc" (8x brand app port, 2026-10-11).
  Put every screenshot beside the mock's before calling a page done. Where the real product has a part the mock lacks
  (a fee disclosure, team scopes, show-once keys), draw it in the mock's own visual language, never as the old widget.
- **Real data is longer than mock data: give every card one short line.** A mock's "Founder, devtools" becomes four
  lines of LinkedIn headline and a name with its certificates. A person card prints one line of name (ellipsis) and one
  short line under it, what they do and where ("influencer marketing · India"), the same rule on every page. "too much
  from the head line and big names", then, pointing at the creators tab: "i like how this is instead of the dashboard"
  (8x brand app, 2026-10-11). Test cards with the longest real names and headlines, not the mock's. The figures match
  too: an estimate the creators tab shows ("~$135, est. per post") shows on the dashboard and the campaign page as well
  ("estimated price? why not showing in the dashboard..").
- **Text on an accent takes that accent's ink, in every theme.** A pill or button filled with the primary uses the
  token made to sit on it (--on-pri), never a hard-coded white: the dark theme's primary is yellow, and white on it
  "cant read here" (the working-as pill, 2026-10-11). Check every filled control in both themes.
- **No outline on text over silk or photos.** Legibility comes from a scrim or a soft wide halo, never from 1px
  text-shadow offsets round each glyph: those read as a border on the letters. "the border on text is too visible"
  (8x brand app, 2026-10-11).
- **Chat runs edge to edge, in a fixed frame.** Messages fill the width beside the rail and the full height at any
  window size, never a centred max-width page with empty bands either side, and only the list and the conversation
  scroll: the page under them never does. "for messaging use edge to edge properly", "why can i scroll on the
  outside container?" (2026-10-11).
- **A dot means one thing: something for you to answer.** An unread dot on a conversation is for a message the other
  side wrote that you have not read; your own messages, system notes and pending decisions never light it (the line
  under the name already states a decision). "why is there a dot when there is nothing to reply to?" (2026-10-11).
- **A sheet's close lives in its corner.** Never at the end of the actions row, where it reads as an action and pushes
  the actions around ("the close icon is at the wrong place"). A profile sheet shows the person, their numbers and
  their work, not their bio ("no need the profile bio", 2026-10-11).
- **Long text takes the whole width.** A headline or description gets its own row across the full column, never a
  narrow column beside buttons with empty space next to it. Measure the line count with the longest real text before
  shipping: "why are u not using proper width for the headline are u dumb" (2026-10-11).
- **Filters sit in one neat row at the top.** Search beside the title; then one row of segments and dropdown pills
  (who, network, place, size, topic), each pill tinted while it narrows the list, with the order and its direction at
  the row's far end. Never a sprawl of raw tags as pills: noisy data (a creator's LinkedIn skills) goes in one "Any
  topic" dropdown of the most common values, cased properly ("AI", "SaaS"). "proper filters like the legacy
  8x.business that was much neater at the top", "the current page also has random topics all over the place" (8x
  brand Creators page, 2026-10-11). When a rebuild drops filters the old page had, bring them back in the new kit.
- **A person's work sits on the person's row, and quoted text is a preview.** Two tabs that list the same people
  (a campaign's Creators and its Results) are one tab: each creator's row carries every post with its figures, and the
  totals head the tab. A post quoted inside the app shows its first three lines with a way to open the original, never
  the whole wall of text: "merge creators and results tab in the campaign workspace and do not expand the post fully"
  (8x brand app, 2026-10-11). Drafts awaiting approval are the exception: they are read in full to be approved.
- **A list of thousands is pages, and the market is browsable.** A long roster or an index splits into numbered pages
  (24, six rows of four) with "1–24 of N" and Previous / pages / Next, and a page turn lands back on the filters and
  the first new row. When a rebuild drops the old product's reach (the 250k creator index), bring it back: "u are not
  tapping into the 250k creator index, and could u split by page in the creator discovery like the legacy one"
  (2026-10-11).
- **Faces of people are stored, not hotlinked.** Any list of people (commenters, reactors, applicants) shows their
  photo, copied once into our own bucket and drawn from there, with initials only when there is none; CDN addresses
  like LinkedIn's expire in weeks. "render pfps for these as well and store them properly instead of refetching"
  (2026-10-11).
- **Fill a product's gaps without its sprawl, and keep its parts.** When a rebuild takes over a product, carry what a
  customer needs (team, sign out, notifications, receipts, ending or rerunning a campaign) and leave only the sprawl
  behind: per-campaign settings rails, workspaces, roles. "Keep it simple" cuts settings and steps, never the
  product's parts: a campaign keeps its tabs (shortlist, applications, creators, drafts, results, share, brief), an
  agency keeps its clients and the review link it hands them, the builder keeps invite only and drafts read first.
  Make each part simpler instead of removing it. Actions sit in an object's head (a More menu for the rare ones),
  settings are one tabbed page, and flows go straight to the thing (invite from the campaign opens Creators aimed at
  it; edit opens the same builder, saved in place). ("drop unecessary things and overly complicated stuff like
  campaign workspace settings etc etc ykwim? keep it simple keep it modern rework the flows to be more direct and
  straight forward", then, after the tabs, the agency view, review sharing and the builder's switches had gone with the
  sprawl: "what happen to different tabs on the campaign workspace ... and for agency view, clients and company and the
  campaign review sharing thing, and during campaign creation draft review? invite only options are missing", 8x brand
  app, 2026-10-10)
- **Words over silk or a photo get a border, everywhere.** ("add borders to text everwhere", the dashboard banner,
  8x POC, 2026-10-10) One shared text border (`--edge` in globals.css, which follows the theme; `--edge-photo` for
  white words on photographs) goes under every word sitting on the silk or a picture: banners, glass tiles on silk,
  empty-page rooms, creator cards, captions, cover chips, and the sign-in room. SVG marks get the matching
  `--edge-mark` drop shadow.
- **An empty page is a room, not a text box.** A lone line and a button on a blank page drew "use the space here for
  something cool.. instead of this lame shit" (8x POC Campaigns and Messages, 2026-10-10). Fill the page with the
  product's ground (the silk room). Put the way in on glass with its real actions (the two ways to start, opening the
  next screen at that step). Beside it, put a picture of what will fill the page: the creators who match, or a sample
  thread arriving line by line, labelled as a sample.
- **No verification boxes after onboarding.** The "Checked against <site>" card on the Company page drew "here not even
  needed this box". The checks belong to the moment of the scan. Afterwards that space shows something the user acts
  on: the live card creators see, and who the topics match as they are edited.
- **A step fills the screen, with something worth the space.** ("empty space at the bottom", the brief builder, 8x
  POC, 2026-10-10) The panel runs to the foot of the window. The last block takes the room left, and it must be useful
  there: a box to drop the brief's images into on page one, and the creators who ask within the typed price on page
  two. Padding out a gap does not count.
- **Edit a thing where it is.** The banner gets its own "Edit banner" button on the banner in the preview (presets, an
  upload, a dropped picture), never a picker on the form beside it. ("have edit button on the banner itself instead of
  on the left pannel", same day)
- **A preview's facts are labelled.** A bare value over a small word ("– a post") was read as a missing post count
  ("the post number doesnt reflect on the side preview"). Each fact gets a label above its value: Posts, Price,
  Out by, Creators.
- **Don't say what the product does anyway.** "Every post opens with #ad, and you approve every draft first" drew "no
  need to mention this"; the explaining line under Go live went with it. A footer holds buttons, plus a warning only
  when something is missing.
- **No sidebar toggle.** The rail sits tucked to its icons and opens in place on hover with 8x.tweets' motion (only
  its width animates, the words fade, the page glides on the compositor). ("on the side bar no need the collapse
  button and get the sidebar animation and smoothness from twitter"). No group labels in it either ("i dont want your
  company label at all"). It must feel smooth, not fast. "opens slowly but collapses too fast" came first. A sharp
  220ms ease-out then drew "opens too fast as well seems jumpy instead of smooth". The jump was the page re-laying out
  as its column narrowed. Sliding the page whole then cut it off ("cut off on the right side when sidebar is open
  instead of resizing"). The answer is to animate the grid column itself, so the page resizes as the rail opens, on one
  soft curve (see app-ui.md, Rails).
  Leaving the window past its edge must not close it ("if i move the mouse of the left most edge, the side bar is
  closing").
- **Logos are sharp.** A site's PNG icon shrunk into a rounded tile reads "low quality and less sharp". Draw known
  brands' marks in code (vector), and fall back to the site's largest icon only for unknown companies.
- **Side-by-side columns end together** ("height match"). The flexible block (a grid of tiles) takes the height the
  other column sets.
- **A step in a flow fits one screen.** ("make it fit prefer no scrolling", on the onboarding "Looks right?" step,
  8x POC, 2026-10-10) Onboarding and builder steps are measured at 1280x800, 1440x900 and the user's own window, and
  fixed until nothing scrolls: fields share rows in two columns, text boxes grow with their text instead of scrolling
  inside, a note that repeats the step pill goes, and short windows tighten type and spacing. Long pages (dashboards,
  lists) may scroll; a step should not.
- **Custom scrollbars everywhere.** ("have custom scroll bars everywhere", same day) Thin, rounded, in the theme's
  own ink, no arrows, on every scroller: the page, panels, lists, text boxes. Never the grey system bar.
- **Every flow is obvious, and nothing complex stays.** ("make sure all the flows are obvious and make sense do not
  keep anything complex in the rework okay?", 8x POC brand app, 2026-10-10) What that cut:
  - one money step: approving a creator holds their fee in escrow there and then (adding money first if the wallet is
    short), not "Approve" on one tab and "Fund escrow" on another;
  - one page per thing with the next step inline where the item is: a campaign is its applications, then every creator
    as a row carrying the one button that moves them on (approve the post, pay them), then the brief; no tabs to hop;
  - no dead or half options: a "Talk to us" that can't book, a "Save draft" that can't be reopened, "Invite" on someone
    already on the campaign, a draft-review switch, post types, segments and a cover picker all went;
  - only questions whose answers change something: the onboarding questions nothing used were cut, leaving website,
    "Looks right?", welcome;
  - every action shows its result where you are (a toast when the item leaves view), and a badge sits on the place you
    act, not on a page that only shows.
- **A link people are sent reads in full.** No sign-in gate or blurred "sign in to read the rest" over a brief or other page
  shared for outreach: signing up is the call to action, never the price of reading. ("looks ugly fix it, they can read it
  freely", 8x.tweets Kylon brief, 2026-10-07)
- **A long ask is a list, not display type.** One lead line at the large size, then numbered cards with a bold title each,
  the way "What you'll make" reads. A paragraph of six angles in 28px type was the "ugly" (same brief).
- **Brands wear their real logo, in mockups too.** An initial in a tile is a fallback, not a design. When asked, take the logo from the
  brand's own LinkedIn company page (the `company-logo_200_200` image), keep our own copy, and show it on the page and its
  share image. ("put their actual logo get the link from linkedin") The same holds for the product mockups on a
  landing: invented sample brands in letter tiles ("Lumen", "Fieldnote") drew "proper logos, and can brands on 8x shown
  in this section directly" (8x POC, 2026-10-10). Use the client's real customers (8x's "Brands on 8x"), each as the
  app icon its own site serves (read the favicon SVG and the touch icon's pixel colours in the pane, then draw it in
  code so it stays sharp), and put the customer logos right under the hero's first line, not only in a row far down.
- **A page says each fact once.** Hero chips, fact tiles and a sidebar that repeat budget, deliverables and dates, plus a
  second timeline, read as "too much text". The hero says only the state, the tiles hold the facts, the side card is the
  way in. Each angle is a title plus one line (the hook), not its step-by-step. (same brief, 2026-10-07)

- **A Dribbble shot's scale is an artboard, not a screen.** Matching the pinned bento's proportions at 1600px made
  the gauge panel alone fill a 1913x1003 window: "too big" (8x priorities dashboard, 2026-10-29). Copy a shot's
  composition and ratios, then size the app so the whole summary (both bento rows) plus the start of the list fits
  one laptop screen: 15–17px card titles, 13–14px body, ~52px rings, ~24px panel padding. Screenshot at the user's
  real window size before showing.
- **An app is pages, not one long scroll.** A dashboard that stacked the summary bento over every list drew "please
  dont have so much scrolling split them into different pages" (8x priorities dashboard, 2026-10-29). Give the
  summary its own page that fills the window, put each list (per priority, per project, overdue) behind a tab with
  its count, and split long lists into numbered pages sized to fit the window (measure rows, shrink the page size
  until nothing scrolls). Summary cards link to their page rather than scrolling down to a list.
- **A rail widens in place** and pushes the page; never an overlay sheet. Opening and closing feel equally smooth
  (close was "instant", open "slow"); animate the rail's width and translate the page on the compositor.
- **Fast feel**: skeletons on click, instant press feedback (global `:active` scale .975), spinners on submit.
- **Lock heights** of paired cards so a grid row does not jump ("lock the height of the card and the quick action
  div"), and keep boxes symmetric.
- **Full-screen messaging** like LinkedIn's, bubbles reaching the edges, no wasted bottom space.
- **Agent and chat views sit on a quiet ground.** No photograph or busy picture behind a working conversation: a
  plain warm field with the baked grain, and the glass reads by its edges. Photographs belong to the landing.
  ("the background in the agent view is distracting keep it simple there", 8x Comment Desk, 2026-10-03)
- **App screens carry almost no copy.** No explainer paragraphs, kickers, sentences under starter cards, rail intros
  or footnotes: an empty app screen is one line, the action itself front and centre (the composer, as on the
  landing) and a few one- or two-word chips; a press that sends a long instruction shows only its short label in
  the bubble. ("why internal platform so text heavy? what is worng with you", 8x Comment Desk, 2026-10-04)
- **One product, one world.** A product's own app screens match its landing: its quiet ground and white glass, its
  pills, icons and type carry over, light only if the landing is. ("make the desk match the landing too", 8x
  Comment Desk, 2026-10-04) The landing's picture of the app is drawn with the app's own classes under one shared
  palette class, so it changes when the app does; a mock left in the old dark desk drew "change this mockup".
- **App rails are clean.** No picture, render or graphic in a rail, even the landing's own hero field: plain white
  glass with the actions on it. ("dont like the graphic on the side bar, would prefer it clean", 8x Comment Desk,
  2026-10-04)
- **Agentic first means a real agent, not a command bar.** An agent bar is a tool-using model with complete context
  on the user (calendar, people, history, where they are in the app), many tools (reuse the product's MCP tools),
  the power to drive the app (navigate, open sheets, highlight) and rich cards in the thread that act in place (a
  recording card that plays right there, Join on a meeting card, confirm before anything that emails or changes
  data). A keyword router with canned replies was the first pass and got "the agent should have many tools +
  complete context on the user + browser navigation + rendering archive meeting preview cards so u can directly
  playfrom there and so much more" (8x Meets office, 2026-10-07).
- **A card is the answer; the text doesn't repeat it.** When the agent shows a day, recording, meeting or list
  card, its text is one short line ("Here's your day.") or only what the card can't show. Tell the model next
  to the tool result, not just in the system prompt: the system rule alone still echoed. ("duplicate
  information", 8x Meets office, 2026-10-07)
- **No "You" badge on your own tile**; its tint marks it. ("remove the you text", 8x Meets office, 2026-10-07)
- **Name things by what the user sees.** The guard on an uninvited room is "Ask to join" everywhere, never
  "knock", in copy and in code names. ("dont call it knock..", 8x Meets office, 2026-10-07)
- **No landing page unless asked.** An interface ask ("change the interface", "show me a poc") is the app screen
  itself; skip the ten-reference landing flow. ("we do not need any landing page", 8x Meets office, 2026-10-07)
- **Merge what belongs together** (profile + account, earnings + payouts) and remove grouping that adds nothing.
- **A light-only product is checked under the dark theme too.** Global classes that switch with the platform theme
  (the silver `sheen` text) turn white in dark and vanish on the product's white cards; inside a scoped light world,
  figures are plain ink. ("not readable", 8x Comment Desk stats, 2026-10-04)
- **Two themes are equals** (8x Meets): every color declared in both, every text pair at 4.5:1 in both, background
  video graded per theme, every surface captured in both.
- **Color means something**: one action color; red and amber only for state; identity colors never red, amber or
  green.

## Learned on the 8x ecosystem site (2026-10-10)

- **No custom cursor dots.** A follower dot drawn on top of the page read as a stray black dot on the buttons:
  "remove this". Keep the native cursor; put the hover delight into the element itself.
- **A ribbon wraps around a person, it does not sit behind them.** Draw it twice: the loop behind the cut-out and
  only the crossover stroke in front ("the infinity loops around him not behind him").
- **Colour on hover is a layered pair, painted like liquid.** Generate the portrait in full colour, derive the B&W
  layer from that same file (so they line up pixel for pixel), and let an ink-particle mask with a goo threshold paint
  the colour in under the cursor, with a slow ghost trail when idle ("layered assets one with color and one without
  color ... fluid color when hovering", after the Ferrari site). Never put a CSS mask-image on an element whose canvas
  redraws every frame: it repaints the whole layer each frame and cost 15fps.
- **Brand graphics touching a person are rendered assets, not code strokes.** An SVG loop (even split front/back) read as "some drawings": render the ribbon wrapping the person in one Gemini image (cut-out + the board's loop slide as refs, chroma key opposite to the ribbon colour), and re-roll any take that loses the shape (a clean ∞, not orbit rings).
- **Team touchpoint mocks are inspiration, not layouts** ("do not straight up copy these but u can do something with
  them"): take their rules ("a dot is a person", halftone with one colour object) and build new pieces from them.
- **Backgrounds bleed to the body's edges; content fills the page** ("use proper width on the team desk", 8x Team
  Desk, 2026-10-13): a silk backdrop clipped to a 1400px content box showed hard vertical edges on a 1914px screen,
  and a 920px chat column left half the screen empty. Anchor the backdrop to the full body beside the rail, run the
  page at 1600px, and spend the width on a second column (the draft beside its image) instead of long prose lines.

## Learned on the 8x dots site (2026-10-13)

- **Dot people are real people: in colour, detailed, faces finest.** Grey bead figures were asked to carry colour "like their clothes and all", and to be "more detailed". The fix: sample full-colour studio photos per bead, weight density to edges and features, and calm the breathing motion on people (it smeared them). Then "more detailed face models pelase? smaller dots? for the faces?": faces need 2–3x smaller, denser dots than clothes, so eyes, mouth and hairline read.
- **A crowd has no duplicates and nothing cut off.** A close built from the same five people repeated, and clipped by the footer and its wordmark, drew "duplicate and cutting off". Generate a crowd of distinct people. Give the crowd, the copy and the footer each their own room.
- **First paint never stalls.** Sampling every formation on the main thread at load made the hero "lag for 1 or 2 seconds". Precompute formations offline into compact binaries, load the hero's first, stream the rest after first paint, and measure long tasks before and after.
- **Dotted outline type is crisp.** Dashes drawn as little scatters of dots made the round letters look hairy ("the "e" can be better"). Put dots exactly on the stroke centreline, evenly spaced, one size, with no jitter or breathing on type.
- **Solid colour fields per product are a keeper.** The user picked direction B but asked for C's full-bleed product-colour grounds ("i like the solid background colors u used on c during products part"), and the dotted outline word along the bottom. Crossfade the fields in OKLab so no handover goes grey.
- **Icons and infographics are welcome in a dot world.** Replacing product icons with people was waved off ("i dont mind the icons and infographcics and all btw its cool"). Don't assume every formation must be a figure.
- **Text never wraps early when there is room** ("for the text use the full width do not wrap it unecessarily if u
  have the space for it, make it a standard", 8x brief page, 2026-10-13): a 658px prose cap left a brief at half its
  panel on a wide screen. Body text gets no ch/em/px measure; the container sets the width. Caps stay only on
  containers (dialogs, forms, bubbles), balanced display headings and truncated cells.
- **Morphs are organic, never a wipe.** A straight left-to-right sweep left a hard vertical line through the crowd and a crisp rectangular hole at the front ("too sharp in most transitions looks like boxes rather natuural"). Drive each dot's start time from a smooth noise field plus jitter, so the front is a soft wandering edge many dots wide. Overlap leaving and arriving dots so density never drops to zero in a region. Check frames at 20–80% of every handover for any straight edge or box.
- **Chat screens follow Stellar, on one scrolling page** ("bad ui look at https://github.com/N1kky-wed/Stellar for good
  chat interface design", "there are scroll bars inside scroll bars etc make it one clean clear ui seemless page",
  8x Team Desk, 2026-10-14): replies sit on the ground with no box (a box per answer plus a box per card read "all
  over the place"); your own message is a quiet glass bubble, not a loud fill; the chat list is small cards under a
  heading, an outline New chat and search; the composer floats as a glass pill pinned to the foot. The page is the
  only scroller: never a scrolling thread inside a scrolling page. Generated media for an item starts by itself.
- **Things enter from somewhere, never pop in.** Composited coins that appeared whole at a shop's arch drew "coins coming out of no where". Anything that leaves an object (coins from a door, cards from a slot) is revealed by the object's own geometry: mask it with the door's wall so the leading edge shows first, with interior shade at the mouth.
- **The 4K rule applies to every hero film, generated plates included.** A 1080p Veo plate upscaled to the hero drew "low res video" (8x Referral, 2026-10-16). Ask Veo for 4k, composite at full size, and compare a 100% crop against the still before shipping.
- **One scene, one video: reach for Gemini Omni before compositing.** A Veo people-only plate with code-drawn coins on top drew "are coins and the hero section not the same video? u are under utilizing gemini omni" (8x Referral, 2026-10-16). Generate the whole scene in one Omni take: same still as first and last frame for the loop, 4k, and the reference's own motion as a 3s `<VIDEO_REF>`. Fix flaws with short conversational edits ("... Keep everything else the same."). Composite only if Omni truly can't hold the motion.
- **A rolling object stays in the film, and it must truly roll.** Thirteen Veo and Omni takes either slid the 8x coins, flipped them or made them hop frame to frame ("the coins are not rolling and some frames are skipping randomly not smooth loop", 8x Referral, 2026-10-16). Moving the coins into a three.js layer was waved off ("no i think u can make it roll properly actually").
  - First make the motion physically right in a composite (rotation = distance / radius, emerging behind the scene's own wall).
  - Then hand that clip to Gemini Omni as a video edit, or as a `<VIDEO_REF>`, so one model renders the whole scene with the correct roll.
  - Before shipping any film, run a per-tile frame-diff check over the whole loop, seam included. Even timestamps can hide content that jumps.
- **A hero built around one novelty object is a gimmick, however well it moves.** The 8x Referral clay storefront with people walking in and coins rolling out took four rounds of polish (sharpness, coins emerging, true rolling, no skipping) and was then dropped whole: "not happy with the gimic overall, lets try something else" (2026-10-17). When a direction's whole point is a trick object, show the ten-reference page again before polishing it further; polish cannot save a premise the user has gone cold on.
- **A word-behind-the-picture hero needs the picture shot for it.** The Yates cut-through (giant word, subject layered in front of its lower half) only works when the still has empty field above the subject: a sky band, the subject's top edge below the word's cap. Full-frame subjects hide the word entirely, and a word behind a centred subject shows as a fragment either way. Brief the stills with the framing numbers (horizon at ~0.36, subject top at ~0.55), make alpha cut-outs offline by keying the field (not luminance: pale sky is as bright as paper), and give inner pages the photo without a word. (8x Referral paper direction, 2026-10-17)
- **Two whole directions bounced on one site: a pick is a layout, not a mandate for the representation.** 8x Referral went clay-storefront-and-coins (dropped: "not happy with the gimic") and then Yates-style giant word behind luxury stationery (dropped: "not a fan start from scratch", 2026-10-17). Both were faithful to their reference and polished; neither landed. Before a third build on the same site, ask one question about what they want the page to FEEL like, and put the representation on the ten-reference page as a choice (several subjects per layout), not just the layout.
- **Category searches on Dribbble return template-grade work; after one bounced round, change the source.** Three ten-reference rounds for 8x Referral came from Dribbble searches ("referral program", "private bank", "wealth", "poster"); the third drew "simple and lame and cringe these aree" (2026-10-18). For the next round, pull from award galleries of shipped sites (Awwwards Sites of the Day and of the Month, Godly) and screenshot the live sites at 1440, so every pick is real, finished work with motion behind it, not a Dribbble mock.
- **Match the ambition to the page's job.** For the 8x Referral page, Dribbble category picks were "simple and lame and cringe", and Awwwards showpieces (Zentry, Lusion, Igloo, Lando Norris) were "too much for a referal page" (2026-10-18). A utility page for partners sits between the two: crafted and specific, not a portfolio stunt. After two bounces in opposite directions, stop showing reference pages and pin the weight with one concrete question anchored to sites the user knows.
- **A faithful layout is not a finished page: match the reference's density, then add the pictures it would have.** The Rogo rebuild of 8x Referral copied Rogo's split sections with small grey UI cards and text rows, and set three lines of 140px headline plus a three-line paragraph in the hero: "the other sections and simple and plain, and also too much text in the hero section" (2026-10-18). Rogo's hero is one line and two short lines under it; keep a hero to that, shaping the client's copy to a fragment rather than setting the whole paragraph. Every section below needs a picture that fills its frame: real faces, photography or film of people at work, UI that fills its panel, never a small card on an empty grey field or a list of text rows.
- **A hero line says what the thing is, in plain words, with no numbers.** "Earn 2% when they sign." read as "still too much random text in the hero title instead of being clear", and asked to choose a line the user said "no numbers theres" (8x Referral, 2026-10-18). Name the thing and the action ("Introduce brands to 8x."), keep figures for the sections below.
- **A pinned reference's typeface is part of the pin.** Swapping Rogo's Arizona Mix for a loosely similar serif drew "i want the font to be same". When the face is commercial, say so, offer the licence, and otherwise test every free candidate against a crop of the reference headline with an overlay and a score; never pick by eye from a shortlist of three.
- **Pointer effects are small and physical, never a glow.** A 400px lit patch following the cursor over Rogo-style scales drew "this glow is too agressive i need something more subtle and better animation like scales flipping to a different color when i hover? ... keep the effect radius small" (8x Referral, 2026-10-18). Make the texture's own pieces move (scales flip to a back colour, about 2–3 pieces across, then flip back after a beat; 3–5 across was still "reduce the radius even more"); no light patch, no field-wide lean.
- **Never show a page whose centrepiece is still a stand-in.** The Lanes landing went out for review with a placeholder SVG sphere where the real WebGL night globe would go, and drew "there is no real globe.. looks trash and fake" (2026-10-18). When the hero object is being built in parallel, wait for it (or show only the sections that are real) before sending tours; the hero is what gets judged first.
- **No coloured glow washes.** Soft violet radial glows behind sections on the Lanes landing drew "i dont like the weird purple glow on the rest of the landing page" (2026-10-18). Light comes from the page's real object (the globe, a film, a photo) or from grain and edges, never from big blurred colour blobs behind sections.
- **When the hero is a 3D object, it carries the whole page.** "utlize the 3d globe more throughout the landing page" (Lanes, 2026-10-18): one persistent object that the scroll moves, zooms and re-stages per section (a call zoomed in, the boundary around your server, everyone at the close), not a hero ornament followed by flat sections.
- **Section motion has to be studied and choreographed, not default fades.** "the rest of the landing page animations and transitions and v simple and lame not godly at all.." (Lanes, 2026-10-18). Record award sites scrolling (`scripts/scroll_frames.py`), write the move each section borrows, and make sections pin, scrub and hand over to each other.
- **Position the product by what it means to the buyer, not by the mechanism.** A self-hosted meeting platform pitched as "Video meetings that run on your own server" drew "the moto is connecting remote companies together not some ooo video calls bull shit" (Parley, 2026-10-18). Lead with the outcome the company buys (a team across countries working as one), and keep the mechanism for the sections below.

- **Natural colour on real-world things.** "in the light mode the water is too vibrant" (Parley, 2026-10-18). Saturated brand blue painted onto the day globe's sea read as a toy. Real things (oceans, land, skin, sky) take their natural, muted tones, here a deep steel blue (#21426e) and not the action blue. Save the saturated brand colour for the lines and marks laid on top, so they read first.

- **Liking one element of a site is not a pin for the whole page.** The user praised edolus.com's Earth ("so smooth, and good looking than the actual earth model") and its cloud-dive transition; a full rebuild of Parley in Edolus's world (orbit film, scroll-scrubbed dive onto a city, HUD frames, mono callouts, glass cards, a server hall) was "dont like it scrap this idea" (2026-10-27). Treat a liked element as an ingredient on the ten-reference page, and confirm the whole-page direction before building a site around one reference's spectacle.
