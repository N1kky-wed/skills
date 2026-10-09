"""Set the hero line in each candidate beside Taiko's own headline crop."""
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
TAIKO = (HERE.parent / "insp" / "taiko" / "f" / "011.png").resolve().as_uri()
faces = [("Switzer", "switzer__Switzer-Variable.woff2"), ("General Sans", "general-sans__GeneralSans-Variable.woff2"), ("Satoshi", "satoshi__Satoshi-Variable.woff2")]
css = "".join(f"@font-face{{font-family:'{n}';src:url('{(HERE / f).resolve().as_uri()}') format('woff2');font-weight:100 900}}" for n, f in faces)
rows = "".join(
    f"""<div class=row><div class=lab>{n} {w}</div><div class=h style="font-family:'{n}';font-weight:{w}">Organic Reddit,<br>without the bots.</div>
    <div class=s style="font-family:'{n}'">Taiko is based · For brands · For Redditors · Get matched</div></div>"""
    for n, _ in faces for w in (500, 600))
html = f"""<html><head><style>{css}
body{{margin:0;background:#f7f6f4;color:#10131a;font-family:sans-serif}} .ref{{display:block;width:760px;clip-path:inset(47% 20% 18% 38%);margin:-340px 0 -190px -260px}}
.row{{display:grid;grid-template-columns:130px 1fr;align-items:center;padding:14px 24px;border-bottom:1px solid #e6e4e8}} .lab{{font:12px monospace;color:#777}}
.h{{font-size:64px;line-height:.98;letter-spacing:-.045em}} .s{{grid-column:2;font-size:16px;font-weight:500;letter-spacing:-.01em;margin-top:8px}}</style></head>
<body><img class=ref src="{TAIKO}">{rows}</body></html>"""
(HERE / "compare.html").write_text(html, encoding="utf-8")
with sync_playwright() as pw:
    b = pw.chromium.launch(); p = b.new_page(viewport={"width": 1100, "height": 900})
    p.goto((HERE / "compare.html").resolve().as_uri()); p.wait_for_timeout(800)
    p.screenshot(path=str(HERE / "compare.png"), full_page=True); b.close()
print("ok")
