"""Pull Dribbble search results at full resolution and lay them out as a numbered contact sheet, for reading many
shots at once (the pane is too small to judge thumbnails).

    python dribbble_pull.py hiring "ai hiring landing page" --out <scratch>/insp
    python dribbble_pull.py popweb https://dribbble.com/shots/popular/web-design --out <scratch>/insp --count 24

Writes OUT/<slug>/NN.jpg (800px), OUT/<slug>/shots.json (title, author, shot link, image src) and
OUT/<slug>-sheet.jpg (4 columns, numbered). Pick from the sheets, then build the page with refs_page.py.
Run several pulls in parallel; set PYTHONIOENCODING=utf-8 on Windows (author names are not ASCII).
"""
import argparse, io, json, os, urllib.request
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0 Safari/537.36"
SHOTS_JS = """() => [...document.querySelectorAll('li.shot-thumbnail, li[id^="screenshot-"]')].map(li => {
    const a = li.querySelector('a.shot-thumbnail-link, a[href*="/shots/"]');
    const img = li.querySelector('figure img, img');
    let src = img ? (img.getAttribute('data-srcset') || img.getAttribute('srcset') || img.src || '') : '';
    if (src.includes(',')) { const parts = src.split(',').map(s => s.trim().split(' ')[0]); src = parts.find(p => p.includes('resize=800x600')) || parts[parts.length - 1]; }
    const title = (li.querySelector('.shot-title, [class*=title]') || {}).textContent || (img && img.alt) || '';
    const who = (li.querySelector('.display-name, .user-information a') || {}).textContent || '';
    return { href: a ? a.href : '', src, title: title.trim(), who: who.trim() };
}).filter(s => s.src && s.href && !/advertis/i.test(s.href))"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("query", help="search words, or a full dribbble.com URL")
    ap.add_argument("--out", default=".")
    ap.add_argument("--count", type=int, default=24)
    a = ap.parse_args()
    url = a.query if a.query.startswith("http") else "https://dribbble.com/search/" + a.query.replace(" ", "-")

    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={"width": 1600, "height": 1200}, user_agent=UA)
        pg.goto(url, wait_until="domcontentloaded")
        pg.wait_for_timeout(3500)
        for _ in range(4):
            pg.mouse.wheel(0, 2400)
            pg.wait_for_timeout(900)
        shots = pg.evaluate(SHOTS_JS)[:a.count]
        br.close()

    folder = os.path.join(a.out, a.slug)
    os.makedirs(folder, exist_ok=True)
    json.dump(shots, open(os.path.join(folder, "shots.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    W, H, cols = 480, 360, 4
    sheet = Image.new("RGB", (cols * W, ((len(shots) + cols - 1) // cols) * (H + 26)), "white")
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("arial.ttf", 15)
    except Exception:
        font = ImageFont.load_default()
    for i, s in enumerate(shots):
        src = s["src"].replace("resize=400x300", "resize=800x600")
        try:
            req = urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0"})
            im = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=20).read())).convert("RGB")
            im.save(os.path.join(folder, f"{i:02d}.jpg"), quality=90)
            im.thumbnail((W, H))
        except Exception:
            im = Image.new("RGB", (W, H), "#ddd")
        x, y = (i % cols) * W, (i // cols) * (H + 26)
        sheet.paste(im, (x + (W - im.width) // 2, y))
        d.text((x + 6, y + H + 4), f"{i:02d}  {s['title'][:52]}", fill="black", font=font)
    sheet.save(os.path.join(a.out, f"{a.slug}-sheet.jpg"), quality=88)
    print(len(shots), "shots ->", os.path.join(a.out, f"{a.slug}-sheet.jpg"))
    for i, s in enumerate(shots):
        print(f"{i:02d}", s["title"][:70], "|", s["who"][:30], "|", s["href"])


if __name__ == "__main__":
    main()
