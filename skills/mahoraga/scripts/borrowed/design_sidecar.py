"""Build .impeccable/design.json from DESIGN.md (narrative, verbatim) + colormeta.json (ramps)."""
import datetime, json, os, re, sys

ROOT = os.environ.get("MEETS_REPO", ".")  # the 8x-gmeet checkout
HERE = os.path.dirname(os.path.abspath(__file__))
md = open(os.path.join(ROOT, "DESIGN.md"), encoding="utf-8").read()
body = md.split("\n---\n", 1)[1]
color_meta = json.load(open(os.path.join(HERE, "colormeta.json"), encoding="utf-8"))

# ---------------- narrative, verbatim ----------------
sections, cur = {}, None
for line in body.splitlines():
    m = re.match(r"^## (.+)$", line)
    if m:
        cur = m.group(1).strip(); sections[cur] = []
    elif cur:
        sections[cur].append(line)

ov = "\n".join(sections["Overview"])
north = re.search(r'\*\*Creative North Star: "([^"]+)"\*\*', ov).group(1)
philo = ov.split("**Key Characteristics:**")[0]
philo = philo.split("**", 2)[-1] if "Creative North Star" in philo else philo
paras = [p.strip() for p in re.split(r"\n\s*\n", philo) if p.strip() and "Creative North Star" not in p]
key_chars = [l[2:].strip() for l in ov.split("**Key Characteristics:**")[1].splitlines() if l.startswith("- ")]

SECTION_TAG = {"Colors": "colors", "Typography": "typography", "Layout": "layout",
               "Elevation & Depth": "elevation", "Shapes": "shapes", "Components": "components"}
rules = []
for name, lines in sections.items():
    for l in lines:
        m = re.match(r"^\*\*(The .+? Rule)\.\*\* (.+)$", l.strip())
        if m:
            rules.append({"name": m.group(1), "body": m.group(2), "section": SECTION_TAG.get(name, name.lower())})

dd = "\n".join(sections["Do's and Don'ts"])
dos_block = dd.split("### Do:")[1].split("### Don't:")[0]
donts_block = dd.split("### Don't:")[1]
bullets = lambda b: [l[2:].strip() for l in b.splitlines() if l.startswith("- ")]
dos, donts = bullets(dos_block), bullets(donts_block)

# ---------------- extensions ----------------
typography_meta = {
    "display": {"displayName": "Display", "purpose": "Page titles only: the door headline, the dashboard greeting, Archive and recording titles. Weight 300, tracked -0.04em."},
    "headline": {"displayName": "Headline", "purpose": "Dashboard section heads and sheet titles; 22px for the spotlight, 20px for archive panel heads."},
    "title": {"displayName": "Title", "purpose": "Meeting card titles; 15-16px under recording posters; 15.5px for the room's meeting title."},
    "body-large": {"displayName": "Body large", "purpose": "Ledes and intros (15.5-16.5px); long reading such as the minutes summary runs at line-height 1.7."},
    "body": {"displayName": "Body", "purpose": "The base size on body; chat and transcript lines at 14px."},
    "label": {"displayName": "Label", "purpose": "Buttons (13px small, 15px large), segmented tabs, nav links, form labels, menu items."},
    "caption": {"displayName": "Caption", "purpose": "Chips, name pills, quick questions, filters, minutes sub-heads; 12px tooltips."},
    "mono": {"displayName": "Mono", "purpose": "Geist Mono with tabular numerals for codes, clocks, timestamps, durations and percentages only."},
}
shadows = [
    {"name": "shadow-1 (rest)", "value": "0 1px 2px rgb(45 38 99 / 0.05), 0 8px 20px -12px rgb(45 38 99 / 0.2)", "purpose": "Buttons, chips on posters, cards at rest, active segments. Night: 0 1px 2px rgb(0 0 0 / 0.3), 0 8px 20px -12px rgb(0 0 0 / 0.6)."},
    {"name": "shadow-2 (raised)", "value": "0 2px 6px rgb(45 38 99 / 0.05), 0 24px 48px -24px rgb(45 38 99 / 0.3)", "purpose": "Heroes, bands, room tiles, the side panel, lobby HUD, hovered cards, the focused Ask bar. Night: 0 2px 6px rgb(0 0 0 / 0.3), 0 24px 48px -24px rgb(0 0 0 / 0.7)."},
    {"name": "shadow-3 (floating)", "value": "0 4px 10px rgb(45 38 99 / 0.06), 0 50px 90px -40px rgb(45 38 99 / 0.42)", "purpose": "Door card, studio, spotlight, sheets, menus, toast, dock, a speaking tile. Night: 0 4px 10px rgb(0 0 0 / 0.35), 0 50px 90px -40px rgb(0 0 0 / 0.85)."},
    {"name": "primary-lift", "value": "inset 0 1px 0 rgb(255 255 255 / 0.18)", "purpose": "The one inner highlight, on violet buttons, stacked on shadow-1."},
    {"name": "focus-ring", "value": "0 0 0 4px var(--violet-soft)", "purpose": "Fields and bars on focus, with a violet-line border; elsewhere :focus-visible is outline 2px solid var(--violet), offset 2px."},
    {"name": "speaking-ring", "value": "padding: 3px; background: var(--silk); mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0); mask-composite: exclude", "purpose": "The silk gradient masked to a 3px frame on a speaking tile (1.5px on the focused Ask bar)."},
    {"name": "glass", "value": "background: var(--glass | --glass-strong); border: 1px solid var(--glass-line); backdrop-filter: blur(14px to 28px) saturate(1.3 to 1.5)", "purpose": "Anything floating over silk, video, the stage, a poster, or content under the sticky topbar."},
    {"name": "video-glass", "value": "background: rgb(14 11 32 / 0.5 to 0.62); backdrop-filter: blur(10px to 16px); color: #fff", "purpose": "Name pills, pin button, filmstrip labels, presenting badge and player controls over live video."},
]
motion = [
    {"name": "ease", "value": "cubic-bezier(0.16, 1, 0.3, 1)", "purpose": "The only easing in use (exponential ease-out). --ease-io is declared and unused."},
    {"name": "d1", "value": "160ms", "purpose": "Colour, background and border changes."},
    {"name": "d2", "value": "260ms", "purpose": "Shadows, fades, the switch knob, presses."},
    {"name": "d3", "value": "420ms", "purpose": "Hover lifts, the side panel folding, the toast's travel."},
    {"name": "meets-rise", "value": "from { opacity: 0; transform: translateY(14px) scale(0.98) }", "purpose": "Entrances: sheets 380ms, menus 260ms, cards 600ms, heroes 700ms, spotlight 800ms, door card 900ms, studio 1100ms."},
    {"name": "meets-sheet", "value": "from { transform: translateY(100%) } 420ms", "purpose": "Phone bottom sheets."},
    {"name": "meets-pulse", "value": "1.9s ring 0 to 7px of var(--rec)", "purpose": "Live and recording dots."},
    {"name": "theme-reveal", "value": "clip-path circle(0 to r) on ::view-transition-new(root), 640ms, cubic-bezier(.16,1,.3,1)", "purpose": "The new light spreads from the theme switch."},
    {"name": "silk-video-in", "value": "opacity 0 to 1, 900ms", "purpose": "A silk video fades in once it can play (and on every theme swap)."},
    {"name": "tile-layout", "value": "left, top, width, height 480ms var(--ease); enter scale 0.92 to 1, 560ms", "purpose": "Room tiles glide to their justified rectangles."},
    {"name": "voice-level", "value": "box-shadow 140ms linear; meter transform 110ms linear", "purpose": "The camera-off halo and the name-pill meter follow --lvl."},
    {"name": "studio-wave", "value": "scaleY 0.45 to 1, 820ms ease-in-out alternate, -71ms stagger per bar", "purpose": "The door studio's active lane."},
    {"name": "reaction", "value": "pop 460ms (scale 0.3, 1.12, 1 with rotation); float 3.1s cubic-bezier(0.2, 0.5, 0.4, 1)", "purpose": "Emoji reactions on a tile and rising across the stage."},
    {"name": "playhead", "value": "left 260ms linear", "purpose": "The multitrack timeline's playhead."},
    {"name": "reduced-motion", "value": "all animation and transition durations 0.001ms; silk video unloaded", "purpose": "prefers-reduced-motion: reduce."},
]
breakpoints = [
    {"name": "stage-narrow", "value": "560px (stage width)"}, {"name": "sheet-bottom", "value": "640px"},
    {"name": "dashboard-phone", "value": "680px"}, {"name": "topbar-compact", "value": "720px"},
    {"name": "archive-phone", "value": "760px"}, {"name": "room-phone", "value": "860px"},
    {"name": "dashboard-hero-stack", "value": "900px"}, {"name": "door-stack", "value": "980px"},
    {"name": "recording-stack", "value": "1080px"}, {"name": "room-me-compact", "value": "1100px"},
    {"name": "stage-nine-up", "value": "960px x 500px (stage box)"},
]

# ---------------- components (self-contained, ds- prefixed, tokens with fallbacks) ----------------
F = "font-family: Geist, ui-sans-serif, system-ui, sans-serif;"
FM = 'font-family: "Geist Mono", ui-monospace, Menlo, Consolas, monospace; font-variant-numeric: tabular-nums;'
EASE = "cubic-bezier(0.16, 1, 0.3, 1)"
SH1 = "0 1px 2px rgb(45 38 99 / 0.05), 0 8px 20px -12px rgb(45 38 99 / 0.2)"
SH3 = "0 4px 10px rgb(45 38 99 / 0.06), 0 50px 90px -40px rgb(45 38 99 / 0.42)"
SILK = "linear-gradient(115deg, #8b74ff 0%, #6fa3ff 42%, #f0a4e6 78%, #8b74ff 100%)"
IC = 'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"'
MIC_OFF = f'<svg {IC}><path d="M2.5 2.5l19 19"/><path d="M18.9 13.2A7 7 0 0 0 19 12v-1.5"/><path d="M5 10.5v1a7 7 0 0 0 12 5"/><path d="M15 9.3V5.5a3 3 0 0 0-5.7-1.3"/><path d="M9 9v2.5a3 3 0 0 0 5.1 2.1"/><path d="M12 18.5v3"/></svg>'
CAM = f'<svg {IC}><path d="M16 10.2 21.5 7v10L16 13.8"/><rect x="2.5" y="6" width="13.5" height="12" rx="2.5"/></svg>'
HAND = f'<svg {IC}><path d="M18 11V6a2 2 0 0 0-4 0v5"/><path d="M14 10V4a2 2 0 0 0-4 0v2"/><path d="M10 10.5V6a2 2 0 0 0-4 0v8"/><path d="M18 8a2 2 0 1 1 4 0v6a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.82L7 15"/></svg>'
CHAT = f'<svg {IC}><path d="M20.5 14.5a2 2 0 0 1-2 2H8l-4.5 4v-15a2 2 0 0 1 2-2h13a2 2 0 0 1 2 2z"/></svg>'
HANGUP = f'<svg {IC}><path d="M3.6 14.6c-.8-.8-.8-2.1.1-2.9 4.6-3.9 12-3.9 16.6 0 .9.8.9 2.1.1 2.9l-1.3 1.3c-.6.6-1.5.7-2.2.2l-1.7-1.2c-.5-.4-.8-.9-.8-1.5v-1.6c-1.5-.5-3.3-.5-4.8 0v1.6c0 .6-.3 1.1-.8 1.5l-1.7 1.2c-.7.5-1.6.4-2.2-.2z"/></svg>'
PLUS = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.3" stroke-linecap="round" aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg>'

def bars(heights, cls="ds-vw"):
    return f'<span class="{cls}">' + "".join(f'<b style="--h:{h}"></b>' for h in heights) + "</span>"

components = [
    {"name": "Primary Button", "kind": "button", "refersTo": "button-primary",
     "description": "Every action: violet pill, white label, inner highlight.",
     "html": f'<button class="ds-btn-primary" type="button">{PLUS}New meeting</button>',
     "css": f".ds-btn-primary {{ display: inline-flex; align-items: center; gap: 8px; height: 40px; padding: 0 18px; border: 1px solid transparent; border-radius: 999px; background: var(--violet, #6147c7); color: #fff; {F} font-size: 14px; font-weight: 500; line-height: 1; letter-spacing: -0.01em; box-shadow: inset 0 1px 0 rgb(255 255 255 / 0.18), {SH1}; cursor: pointer; transition: background-color 160ms, transform 260ms {EASE}; }} .ds-btn-primary svg {{ width: 16px; height: 16px; }} .ds-btn-primary:hover {{ background: var(--violet-hover, #5236bb); }} .ds-btn-primary:active {{ transform: translateY(1px) scale(0.985); }} .ds-btn-primary:focus-visible {{ outline: 2px solid var(--violet, #6147c7); outline-offset: 2px; }}"},
    {"name": "Ghost Button", "kind": "button", "refersTo": "button-ghost",
     "description": "The quiet partner beside a primary (Cancel, Done).",
     "html": '<button class="ds-btn-ghost" type="button">Cancel</button>',
     "css": f".ds-btn-ghost {{ display: inline-flex; align-items: center; height: 40px; padding: 0 18px; border-radius: 999px; background: var(--surface, #fff); color: var(--ink, #222439); border: 1px solid var(--line-2, rgb(35 37 57 / 0.13)); box-shadow: {SH1}; {F} font-size: 14px; font-weight: 500; line-height: 1; letter-spacing: -0.01em; cursor: pointer; transition: background-color 160ms, border-color 160ms, transform 260ms {EASE}; }} .ds-btn-ghost:hover {{ background: var(--surface-2, #fbfaff); border-color: var(--line-3, rgb(35 37 57 / 0.22)); }} .ds-btn-ghost:active {{ transform: translateY(1px) scale(0.985); }} .ds-btn-ghost:focus-visible {{ outline: 2px solid var(--violet, #6147c7); outline-offset: 2px; }}"},
    {"name": "Chips", "kind": "chip", "refersTo": "chip",
     "description": "26px pills: neutral, live with a pulsing dot, violet, and mono for codes and durations.",
     "html": '<div class="ds-chips"><span class="ds-chip">Transcript</span><span class="ds-chip ds-live"><i></i>Live now</span><span class="ds-chip ds-violet">Ask this meeting</span><span class="ds-chip ds-mono">42 min</span></div>',
     "css": f".ds-chips {{ display: flex; flex-wrap: wrap; gap: 6px; }} .ds-chip {{ display: inline-flex; align-items: center; gap: 6px; height: 26px; padding: 0 10px; border-radius: 999px; {F} font-size: 12.5px; font-weight: 500; line-height: 1; color: var(--ink-2, #474a64); background: var(--surface-3, #f0eef9); border: 1px solid var(--line, rgb(35 37 57 / 0.08)); white-space: nowrap; }} .ds-live {{ color: var(--rec-text, #c9353a); background: var(--rec-soft, rgb(229 72 77 / 0.1)); border-color: color-mix(in oklab, var(--rec, #e5484d) 26%, transparent); }} .ds-live i {{ width: 7px; height: 7px; border-radius: 50%; background: var(--rec, #e5484d); animation: ds-pulse 1.9s {EASE} infinite; }} .ds-violet {{ color: var(--violet-text, #5a3fc4); background: var(--violet-soft, rgb(97 71 199 / 0.1)); border-color: color-mix(in oklab, var(--violet, #6147c7) 22%, transparent); }} .ds-mono {{ {FM} font-size: 12px; letter-spacing: 0.02em; }} @keyframes ds-pulse {{ 0% {{ box-shadow: 0 0 0 0 color-mix(in oklab, var(--rec, #e5484d) 60%, transparent); }} 70% {{ box-shadow: 0 0 0 7px transparent; }} 100% {{ box-shadow: 0 0 0 0 transparent; }} }}"},
    {"name": "Text Field", "kind": "input", "refersTo": "field",
     "description": "46px field, 14px corners; focus is a violet edge with a 4px violet wash ring.",
     "html": '<label class="ds-label">Title<input class="ds-field" type="text" placeholder="Weekly sync"></label>',
     "css": f".ds-label {{ display: grid; gap: 8px; {F} font-size: 13px; font-weight: 500; line-height: 1.2; color: var(--ink-2, #474a64); }} .ds-field {{ width: 100%; height: 46px; padding: 0 16px; border-radius: 14px; background: var(--surface, #fff); border: 1px solid var(--line-2, rgb(35 37 57 / 0.13)); color: var(--ink, #222439); {F} font-size: 15px; font-weight: 400; caret-color: var(--violet, #6147c7); transition: border-color 160ms, box-shadow 260ms; }} .ds-field::placeholder {{ color: var(--ink-4, #737591); }} .ds-field:focus {{ outline: none; border-color: var(--violet-line, rgb(97 71 199 / 0.34)); box-shadow: 0 0 0 4px var(--violet-soft, rgb(97 71 199 / 0.1)); }}"},
    {"name": "Segmented Navigation", "kind": "nav", "refersTo": "segmented",
     "description": "A pill track with the active item lifted onto paper; the topbar and side-panel tabs.",
     "html": '<nav class="ds-seg" aria-label="Sections"><a href="#" class="ds-on" aria-current="page">Meetings</a><a href="#">Archive</a></nav>',
     "css": f".ds-seg {{ display: inline-flex; gap: 2px; padding: 4px; border-radius: 999px; background: var(--surface-3, #f0eef9); }} .ds-seg a {{ display: inline-flex; align-items: center; height: 34px; padding: 0 16px; border-radius: 999px; {F} font-size: 13.5px; font-weight: 500; line-height: 1; color: var(--ink-3, #5f617b); text-decoration: none; transition: background-color 160ms, color 160ms, box-shadow 260ms; }} .ds-seg a:hover {{ color: var(--ink, #222439); }} .ds-seg a:focus-visible {{ outline: 2px solid var(--violet, #6147c7); outline-offset: 2px; }} .ds-seg a.ds-on {{ background: var(--surface, #fff); color: var(--ink, #222439); box-shadow: {SH1}; }}"},
    {"name": "Switch", "kind": "custom", "refersTo": "switch-on",
     "description": "42 by 26px pill, violet when on, with a white knob that slides on the house easing.",
     "html": '<label class="ds-chk">Record, transcribe and write minutes<input type="checkbox" checked><span class="ds-tgl"></span></label>',
     "css": f".ds-chk {{ display: flex; align-items: center; justify-content: space-between; gap: 14px; {F} font-size: 14px; color: var(--ink, #222439); cursor: pointer; }} .ds-chk input {{ position: absolute; opacity: 0; pointer-events: none; }} .ds-tgl {{ position: relative; flex: none; width: 42px; height: 26px; border-radius: 999px; background: var(--surface-4, #e7e4f4); transition: background-color 260ms; }} .ds-tgl::after {{ content: ''; position: absolute; top: 3px; left: 3px; width: 20px; height: 20px; border-radius: 50%; background: #fff; box-shadow: 0 2px 6px rgb(0 0 0 / 0.2); transition: transform 260ms {EASE}; }} .ds-chk input:checked + .ds-tgl {{ background: var(--violet, #6147c7); }} .ds-chk input:checked + .ds-tgl::after {{ transform: translateX(16px); }} .ds-chk input:focus-visible + .ds-tgl {{ outline: 2px solid var(--violet, #6147c7); outline-offset: 2px; }}"},
    {"name": "Call Dock", "kind": "custom", "refersTo": "dock",
     "description": "Floating glass pill of 48px circular controls; your muted mic on the red wash, Leave as a red pill.",
     "html": f'<div class="ds-dock" role="toolbar" aria-label="Call controls"><button class="ds-ctl ds-mic" aria-label="Unmute">{MIC_OFF}</button><button class="ds-ctl ds-off" aria-label="Turn camera on">{CAM}</button><span class="ds-sep"></span><button class="ds-ctl" aria-label="Raise hand">{HAND}</button><button class="ds-ctl ds-active" aria-label="Chat">{CHAT}</button><button class="ds-ctl ds-leave" aria-label="Leave the meeting">{HANGUP}</button></div>',
     "css": f".ds-dock {{ display: inline-flex; align-items: center; gap: 4px; padding: 7px; border-radius: 999px; background: var(--glass-strong, rgb(255 255 255 / 0.84)); border: 1px solid var(--glass-line, rgb(255 255 255 / 0.75)); backdrop-filter: blur(22px) saturate(1.5); -webkit-backdrop-filter: blur(22px) saturate(1.5); box-shadow: {SH3}; }} .ds-ctl {{ width: 48px; height: 48px; flex: none; display: grid; place-items: center; border: 0; border-radius: 50%; background: transparent; color: var(--ink, #222439); cursor: pointer; transition: background-color 160ms, color 160ms, transform 260ms {EASE}; }} .ds-ctl svg {{ width: 20px; height: 20px; }} .ds-ctl:hover {{ background: var(--surface-3, #f0eef9); }} .ds-ctl:active {{ transform: scale(0.94); }} .ds-ctl:focus-visible {{ outline: 2px solid var(--violet, #6147c7); outline-offset: 2px; }} .ds-mic {{ background: var(--rec-soft, rgb(229 72 77 / 0.1)); color: var(--rec-text, #c9353a); }} .ds-mic:hover {{ background: color-mix(in oklab, var(--rec, #e5484d) 22%, transparent); }} .ds-off {{ color: var(--ink-3, #5f617b); }} .ds-active {{ background: var(--violet-soft, rgb(97 71 199 / 0.1)); color: var(--violet-text, #5a3fc4); }} .ds-sep {{ width: 1px; height: 26px; margin: 0 5px; background: var(--line-2, rgb(35 37 57 / 0.13)); }} .ds-leave {{ width: 66px; margin-left: 4px; border-radius: 999px; background: var(--rec, #e5484d); color: #fff; }} .ds-leave:hover {{ background: var(--rec-hover, #d33b40); }}"},
    {"name": "Speaking Tile (camera off)", "kind": "card", "refersTo": "tile",
     "description": "An elastic camera-off card: the voice's track-colour glow, a face with a level halo, the silk speaking ring and the name pill's meter.",
     "html": '<div class="ds-tile" style="--tc:#0b7f78;--lvl:0.55"><div class="ds-face">M</div><div class="ds-tlbl"><span class="ds-meter" aria-hidden="true"><i></i><i></i><i></i></span>Maya <span class="ds-ln">Okafor</span></div></div>',
     "css": f".ds-tile {{ position: relative; width: 300px; height: 200px; overflow: hidden; border-radius: 22px; background: radial-gradient(52% 58% at 50% 46%, color-mix(in oklab, var(--tc) 30%, transparent), transparent 74%), radial-gradient(80% 60% at 50% 120%, color-mix(in oklab, var(--tc) 22%, transparent), transparent 70%), var(--tile, #fbfaff); box-shadow: {SH3}, inset 0 0 0 1px var(--tile-line, rgb(35 37 57 / 0.06)); display: grid; place-items: center; }} .ds-tile::after {{ content: ''; position: absolute; inset: 0; border-radius: inherit; padding: 3px; background: {SILK}; -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0); -webkit-mask-composite: xor; mask-composite: exclude; pointer-events: none; }} .ds-face {{ width: 76px; height: 76px; border-radius: 50%; display: grid; place-items: center; background: var(--tc); color: #fff; {F} font-size: 32px; font-weight: 500; box-shadow: 0 0 0 calc(3px + var(--lvl) * 16px) color-mix(in oklab, var(--tc) 34%, transparent), 0 22px 44px -18px rgb(0 0 0 / 0.35); transition: box-shadow 140ms linear; }} .ds-tlbl {{ position: absolute; left: 10px; bottom: 10px; display: flex; align-items: center; gap: 7px; height: 30px; padding: 0 12px 0 9px; border-radius: 999px; background: var(--glass-strong, rgb(255 255 255 / 0.84)); color: var(--ink, #222439); box-shadow: {SH1}; {F} font-size: 12.5px; font-weight: 500; line-height: 1; }} .ds-meter {{ display: flex; align-items: center; justify-content: center; gap: 2px; width: 14px; height: 14px; }} .ds-meter i {{ width: 3px; height: 14px; border-radius: 2px; background: color-mix(in oklab, var(--tc) 55%, #fff); transform: scaleY(calc(0.28 + var(--lvl) * 0.5)); transition: transform 110ms linear; }} .ds-meter i:nth-child(2) {{ transform: scaleY(calc(0.28 + var(--lvl) * 0.72)); }}"},
    {"name": "Voice Poster", "kind": "card", "refersTo": "voice-plate",
     "description": "A recording's poster: its own crop of the silk, with voices as tracks in talk-time order on a glass plate.",
     "html": '<div class="ds-poster"><div class="ds-vplate">'
             f'<div class="ds-vlane" style="--tc:#6a4de6;--w:1"><span class="ds-av">P</span>{bars([0.4, 0.8, 0.95, 0.7, 0, 0.5, 0.9, 0.6, 0.3, 0, 0.7, 1, 0.8, 0.45, 0, 0.6, 0.85, 0.5, 0, 0.4, 0.75, 0.9, 0.55, 0.3, 0, 0.6, 0.8, 0.5, 0.35, 0.7, 0.9, 0.4])}</div>'
             f'<div class="ds-vlane" style="--tc:#0b7f78;--w:0.62"><span class="ds-av">M</span>{bars([0.5, 0.9, 0.7, 0.3, 0, 0.6, 1, 0.8, 0.4, 0, 0.55, 0.85, 0.6, 0.3, 0, 0.7, 0.9, 0.5, 0.35, 0.6])}</div>'
             f'<div class="ds-vlane" style="--tc:#c93a80;--w:0.4"><span class="ds-av">K</span>{bars([0.6, 0.85, 0.5, 0, 0.4, 0.9, 0.7, 0.3, 0, 0.5, 0.8, 0.55, 0.3, 0.65, 0.4])}</div>'
             '</div></div>',
     "css": f".ds-poster {{ position: relative; width: 320px; aspect-ratio: 16 / 10; overflow: hidden; border-radius: 24px; background: linear-gradient(140deg, hsl(262 72% 64% / 0.3), transparent 62%), {SILK}; box-shadow: {SH1}, inset 0 0 0 1px var(--line, rgb(35 37 57 / 0.08)); }} .ds-vplate {{ position: absolute; left: 12px; right: 12px; bottom: 12px; display: grid; gap: 6px; padding: 10px 12px; border-radius: 16px; background: var(--glass-strong, rgb(255 255 255 / 0.84)); border: 1px solid var(--glass-line, rgb(255 255 255 / 0.75)); backdrop-filter: blur(14px) saturate(1.3); -webkit-backdrop-filter: blur(14px) saturate(1.3); }} .ds-vlane {{ display: flex; align-items: center; gap: 9px; height: 22px; }} .ds-av {{ width: 22px; height: 22px; flex: none; border-radius: 50%; display: grid; place-items: center; background: var(--tc); color: #fff; {F} font-size: 11px; font-weight: 500; box-shadow: 0 0 0 1.5px var(--surface, #fff), 0 0 0 3px var(--tc); }} .ds-vw {{ display: flex; align-items: center; gap: 2px; height: 18px; min-width: 0; overflow: hidden; }} .ds-vw b {{ flex: none; width: 2.5px; height: max(2.5px, calc(var(--h) * 100%)); border-radius: 2px; background: var(--tc); }}"},
    {"name": "Multitrack Timeline", "kind": "custom", "refersTo": "timeline-track",
     "description": "Who spoke when: one lane per voice, every turn where it happened, a mono share, and the ink playhead.",
     "html": '<div class="ds-tl">'
             '<div class="ds-lane" style="--tc:#6a4de6"><span class="ds-who"><i></i><span class="ds-n">Priya</span><span class="ds-pc">46%</span></span><div class="ds-track"><b style="left:2%;width:14%"></b><b style="left:31%;width:9%"></b><b style="left:58%;width:18%"></b><b style="left:88%;width:7%"></b></div></div>'
             '<div class="ds-lane" style="--tc:#0b7f78"><span class="ds-who"><i></i><span class="ds-n">Maya</span><span class="ds-pc">31%</span></span><div class="ds-track"><b style="left:17%;width:12%"></b><b style="left:42%;width:14%"></b><b style="left:78%;width:8%"></b></div></div>'
             '<span class="ds-head" style="left:calc(160px + 12px + (100% - 172px) * 0.47)"></span></div>',
     "css": f".ds-tl {{ position: relative; display: grid; gap: 6px; width: 520px; padding: 10px 12px; }} .ds-lane {{ display: grid; grid-template-columns: 160px minmax(0, 1fr); align-items: center; gap: 12px; height: 38px; }} .ds-who {{ display: flex; align-items: center; gap: 9px; min-width: 0; padding-left: 6px; }} .ds-who i {{ width: 10px; height: 10px; flex: none; border-radius: 50%; background: var(--tc); box-shadow: 0 0 0 3px color-mix(in oklab, var(--tc) 22%, transparent); }} .ds-n {{ {F} font-size: 13.5px; font-weight: 500; color: var(--ink, #222439); }} .ds-pc {{ margin-left: auto; {FM} font-size: 12px; font-weight: 500; color: var(--ink-3, #5f617b); }} .ds-track {{ position: relative; height: 26px; border-radius: 9px; background: var(--surface-3, #f0eef9); overflow: hidden; cursor: pointer; }} .ds-track b {{ position: absolute; top: 5px; bottom: 5px; min-width: 3px; border-radius: 4px; background: var(--tc); opacity: 0.85; transition: opacity 160ms; }} .ds-track b:hover {{ opacity: 1; }} .ds-head {{ position: absolute; top: 6px; bottom: 6px; width: 2px; margin-left: -1px; border-radius: 2px; background: var(--ink, #222439); opacity: 0.8; pointer-events: none; }} .ds-head::before {{ content: ''; position: absolute; top: -5px; left: -4px; width: 10px; height: 10px; border-radius: 50%; background: var(--ink, #222439); }}"},
]

extensions = {"colorMeta": color_meta, "typographyMeta": typography_meta, "shadows": shadows,
              "motion": motion, "breakpoints": breakpoints}
doc = {
    "schemaVersion": 2,
    "generatedAt": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
    "title": "Design System: 8x Meets",
    "extensions": extensions,
    "components": components,
    "narrative": {"northStar": north, "overview": "\n\n".join(paras), "keyCharacteristics": key_chars,
                  "rules": rules, "dos": dos, "donts": donts},
}
os.makedirs(os.path.join(ROOT, ".impeccable"), exist_ok=True)
out = os.path.join(ROOT, ".impeccable", "design.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(doc, f, indent=2, ensure_ascii=False)

# self-check: the narrative really came across, and every ramp has 8 steps
assert north == "The Lilac Studio", north
assert len(paras) == 3, len(paras)
assert len(key_chars) == 6, key_chars
assert len(rules) >= 9, [r["name"] for r in rules]
assert len(dos) == 10 and len(donts) == 11, (len(dos), len(donts))
assert all(len(v.get("tonalRamp", [0] * 8)) == 8 for v in color_meta.values())
assert 5 <= len(components) <= 10
print("wrote", out, "|", len(color_meta), "colours,", len(rules), "rules,", len(dos), "dos,", len(donts), "donts,", len(components), "components")
print("rules:", ", ".join(f"{r['name']} [{r['section']}]" for r in rules))
