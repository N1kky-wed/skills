# Direction

## When the user pins a reference

A link the user loves ("i love this") beats any direction you would have proposed. It happened on 8x.tweets
(AIVENT) and careNext (VitAI); both times the build followed the reference closely and the user was happy.

1. Study it in the pane, section by section, so the user sees what you are reading.
2. Capture it at 2x: `python scripts/capture_reference.py <url> <scratch>/refs --prefix <name>`.
3. Measure, do not eyeball: `python scripts/palette.py <capture> --points ...` on the field (center and rim),
   cards, buttons, text, gradient stops. Write the hexes straight into `@theme` tokens. careNext/VitAI measured:
   hero field #B9D941 to #8EBA22 (lit in the middle), light lime #CBED75, cream #FAF7F2, ink #141B0F, range bars
   amber #D8912B to leaf #79B43F.
4. Identify the type from the capture (letterforms: single- or double-storey a and g, terminals) and choose the
   closest free face (VitAI read as Manrope; its italic accent line is a synthesized oblique of the same face).
5. List the signature details, because they carry the look more than the palette: VitAI's were hairlines with
   square end-nodes holding a short label, a dark pill on the hairline, a device rising out of the hero panel's
   rounded base cut off by it, floating cards either side, range bars, big rounded panels (132px bottom radius at
   desktop), a giant wordmark in the footer.
6. Map the reference's sections one to one onto the client's real content, then extend in the same language for
   content the reference never shows (careNext needed leadership, FAQs, posts, films). Present that mapping in a
   few lines before building.
7. Where the pinned reference contradicts a default lean in `taste.md` (its buttons carry arrows), follow the
   reference and say so in one line. A flat ground still gets the baked grain: it measures as the same color and is
   no longer plain. Truth (no invented claims, labeled samples) and never blocking the scroll always hold.

## When nothing is pinned: the ten-reference page

This is the default. The user asked for it ("i like this way of showing make it a default for the mahoraga skill to
show 10 references like this", 8x.careers and Playmakers, 2026-10-03) after turning down two concept references
offered on their own, a sports-scouting world and a broadcast control room ("dont like both show me 10 refernce hero
screens in one page").

1. Pull wide: `python scripts/dribbble_pull.py <slug> "<query>" --out <scratch>/insp` for the category and its
   closest analogs, Dribbble's popular web design (`https://dribbble.com/shots/popular/web-design`), and strong heroes
   outside the category ("hero section", "landing page hero", "website hero animation", "ai landing page"). Run six to
   twelve pulls in parallel and read the sheets yourself; the pane is too small to judge thumbnails.
2. Pick ten heroes that are each a different direction: light and dark, photographic, 3D object, editorial type,
   silk or light field, product-led. Favor polished shots in the families the user has loved (AIVENT's lilac silk,
   VitAI's lime field with the device rising), refuse the category's defaults, and let one or two picks carry the
   product's own story. Never ten variations of one idea.
3. Write `picks.json`: per pick a short direction name and one line on what it would become for this project (which
   section, which side, which of their real material). Then `python scripts/refs_page.py picks.json <scratch>/refs`.
4. Serve it with a launch config (`python -m http.server <port> --bind 127.0.0.1 --directory <scratch>/refs`; a
   file:// page outside the project only shows as a static snapshot), `preview_start` it, check that every image
   loaded at 1600px, and leave it fronted in the pane.
5. In chat, list the ten names one line each and ask for a number, two to mix, or a link of their own. The pick
   becomes the pinned reference: capture it at 2x and follow the section above.

The page shows other people's references, so it is not a design board. Boards of your own design options stay banned
("never use those design boards again"): build the chosen look in code and show real screenshots, with git as the
undo.

## Copy

- A redesign keeps the client's copy word for word ("make sure that we convey the same copy but in this different
  visual/animation/transitional style"). Put it in `src/content/*.ts` files with a header saying so, generated from
  the captured text with a script where possible, so nothing is retyped wrong.
- Shape the copy, do not rewrite it: split a long sentence into a title line and an italic accent line, use a
  sentence's fragment as a hairline label, move the rest of a paragraph lower on the page.
- Never invent claims: no counts, customers, outcomes, testimonials, prices or ratings the client did not publish.
  Their own published figures are fair game (careNext's FAQ: 1.1M doctors graded, 5M+ providers, 50+ specialties).
- Mock-UI microcopy may be new, but any invented value (names, amounts, grades, dates) wears a "Sample" tag, and it
  must respect product facts (Doc360 says no doctor grades above 4 stars, so samples stay under 4).
- Real people (leadership, advisors) appear only with permission, and never as sample data (a real person is never
  shown as a graded doctor).

## Device truth

Show products in the form they actually ship in. Find out before drawing a device: careNext's products were websites
and one tablet app, so the phone the hero started with was wrong ("idk if the ui should be around a mobile? are they
doing mobile apps or is it a website?"). Websites go in a browser window, tablet apps on a tablet, phones only for
real phone apps. The 8x.tweets team rejected a hand holding a phone for the same reason: it reads as a mobile app,
not a website.

## Pitch hygiene

A redesign pitched to a company is a concept: `robots: noindex`, a footer line ("A concept redesign of <domain>,
using <company>'s published copy. Not the official site."), forms that say they do not send, and a link on a
non-official domain. Use their real logo when the user says so, drawn inline so it can switch to a single ink
color on fields where the original colors vanish (an orange star on lime).
