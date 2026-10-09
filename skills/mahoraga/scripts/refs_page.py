"""Build the ten-reference page: numbered heroes at 1600px on one scrolling page, each with a one-line note on what it
would become for this project. This is the default way to set a direction (the user: "i like this way of showing
make it a default for the mahoraga skill to show 10 references like this").

    python refs_page.py picks.json <scratch>/refs --title "Ten reference heroes" --lede "Pick a number, or two to mix."

picks.json is a list of up to ten picks, either from a dribbble_pull.py folder or given directly:
    [{"sheet": "<scratch>/insp/aihiring", "index": 17, "name": "Photographic, moody green",
      "note": "The product on a real laptop in a real room. Both sites: work shown where it happens."},
     {"image": "https://... or C:/path.png", "href": "https://site", "title": "Site name", "who": "Studio",
      "name": "...", "note": "..."}]
Any pick may carry "label" to replace its number badge: when the user asks to see "more of 9", put that shot's own
screens first as "9.1", "9.2" ... (grab them all from the shot page), then ten new picks in the same family.

Then serve it and open it in the browser pane (a file:// page outside the project only shows as a static snapshot
that no tool can check): add a launch config running `python -m http.server <port> --bind 127.0.0.1 --directory
<out>` and preview_start it, and confirm every image loaded (naturalWidth 1600).
"""
import argparse, html, io, json, pathlib, urllib.request
from PIL import Image


def fetch(src, dest):
    if src.startswith("http"):
        src = src.replace("resize=400x300", "resize=1600x1200").replace("resize=800x600", "resize=1600x1200")
        req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0"})
        im = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=30).read()))
    else:
        im = Image.open(src)
    im.convert("RGB").save(dest, quality=90)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("picks")
    ap.add_argument("out")
    ap.add_argument("--title", default="Ten reference heroes")
    ap.add_argument("--lede", default="Pick a number, or two to mix. Each line says what it would become for this project.")
    a = ap.parse_args()
    out = pathlib.Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    picks = json.loads(pathlib.Path(a.picks).read_text(encoding="utf-8"))

    cards, n = [], 0
    for i, p in enumerate(picks, 1):
        label = p.get("label")
        if not label:
            n += 1
            label = str(n)
        if "sheet" in p:
            folder = pathlib.Path(p["sheet"])
            shot = json.loads((folder / "shots.json").read_text(encoding="utf-8"))[p["index"]]
            src, fallback = shot["src"], folder / f"{p['index']:02d}.jpg"
        else:
            shot, src, fallback = p, p["image"], None
        dest = out / f"{i:02d}.jpg"
        try:
            fetch(src, dest)
        except Exception as e:
            if not fallback:
                raise
            fetch(str(fallback), dest)
            print("fell back to the 800px copy for", i, e)
        w, h = Image.open(dest).size
        print(i, w, h, shot.get("title", "")[:60])
        link = (f'<a href="{html.escape(shot.get("href", ""))}" target="_blank" rel="noreferrer">'
                f'{html.escape(shot.get("title", ""))} &middot; {html.escape(shot.get("who", ""))}</a>') if shot.get("href") else ""
        cards.append(f"""
<figure id="r{i}">
  <div class="num">{html.escape(label)}</div>
  <img src="{dest.name}" width="{w}" height="{h}" alt="">
  <figcaption><h2>{html.escape(label)}. {html.escape(p['name'])}</h2><p>{html.escape(p['note'])}</p>{link}</figcaption>
</figure>""")

    (out / "index.html").write_text(f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(a.title)}</title>
<style>
  :root {{ color-scheme: light; }}
  body {{ margin: 0; background: #eceae6; color: #1b1b1a; font: 15px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif; }}
  header {{ max-width: 1240px; margin: 0 auto; padding: 32px 20px 8px; }}
  header h1 {{ font-size: 26px; margin: 0 0 6px; letter-spacing: -0.02em; }}
  header p {{ margin: 0; color: #5d5b57; }}
  main {{ max-width: 1240px; margin: 0 auto; padding: 16px 20px 80px; display: grid; gap: 40px; }}
  figure {{ margin: 0; position: relative; }}
  img {{ display: block; width: 100%; height: auto; border-radius: 14px;
         box-shadow: 0 1px 2px rgb(0 0 0 / .06), 0 18px 40px -24px rgb(0 0 0 / .35); }}
  .num {{ position: absolute; top: 14px; left: 14px; min-width: 44px; height: 44px; padding: 0 10px; box-sizing: border-box;
          border-radius: 22px; background: #1b1b1a;
          color: #fff; display: grid; place-items: center; font-weight: 700; font-size: 18px; box-shadow: 0 4px 12px rgb(0 0 0 / .25); }}
  figcaption {{ padding: 12px 4px 0; }}
  figcaption h2 {{ font-size: 18px; margin: 0 0 4px; letter-spacing: -0.01em; }}
  figcaption p {{ margin: 0 0 6px; color: #3d3c39; max-width: 70ch; }}
  figcaption a {{ color: #6b6964; font-size: 13px; }}
</style></head>
<body>
<header><h1>{html.escape(a.title)}</h1><p>{html.escape(a.lede)}</p></header>
<main>{''.join(cards)}
</main></body></html>""", encoding="utf-8")
    print("ok", out / "index.html")


if __name__ == "__main__":
    main()
