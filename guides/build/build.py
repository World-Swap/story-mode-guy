#!/usr/bin/env python3
"""Assemble a guide's HTML body fragment into a full, print-ready HTML document.

Usage:
    python3 build.py <guide-id>          # build one
    python3 build.py all                 # build every guide with a src file

Reads:  guides/manifest.json  and  guides/src/<id>.html   (body fragment)
Writes: guides/html/<id>.html            (full document, ready for render.js)
"""
import json, re, sys, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent      # .../guides
MANIFEST = json.loads((ROOT / "manifest.json").read_text())
SRC = ROOT / "src"
OUT = ROOT / "html"
OUT.mkdir(exist_ok=True)

CSS = r"""
:root{
  --accent: __ACCENT__;
  --accent2: __ACCENT2__;
  --ink:#1c1e21;
  --muted:#5b6470;
  --line:#e3e7ec;
  --bg-tint:#f6f8fa;
}
*{box-sizing:border-box}
@page{ size:letter; margin:22mm 18mm 20mm; }
@page:first{ margin:0; }
html{ -webkit-print-color-adjust:exact; print-color-adjust:exact; }
body{
  font-family:"Bitstream Charter","Charter","Liberation Serif",Georgia,serif;
  font-size:10.6pt; line-height:1.58; color:var(--ink); margin:0;
  text-rendering:optimizeLegibility;
}
p{ margin:0 0 .72em; }
strong{ color:#101317; }
em{ color:#2a2d31; }
a{ color:var(--accent); text-decoration:none; }
.sans{ font-family:"DejaVu Sans","Liberation Sans",Arial,sans-serif; }

/* ---------- COVER ---------- */
.cover{
  position:relative; width:100%; height:279.4mm; page-break-after:always;
  color:#fff; overflow:hidden;
  background:linear-gradient(150deg, var(--accent) 0%, color-mix(in srgb, var(--accent) 55%, #05070a) 100%);
  font-family:"DejaVu Sans","Liberation Sans",Arial,sans-serif;
}
.cover .wm{
  position:absolute; right:-30mm; top:-30mm; width:150mm; height:150mm;
  border-radius:50%; background:var(--accent2); opacity:.16;
}
.cover .wm2{
  position:absolute; left:-40mm; bottom:-50mm; width:150mm; height:150mm;
  border-radius:50%; border:2mm solid rgba(255,255,255,.10);
}
.cover-inner{ position:absolute; inset:0; padding:26mm 22mm; display:flex; flex-direction:column; }
.cover .kicker{
  font-size:11pt; letter-spacing:.32em; font-weight:700; text-transform:uppercase;
  color:var(--accent2); filter:brightness(1.5); margin-bottom:auto;
}
.cover .badge{
  display:inline-block; margin-bottom:auto; padding:5px 12px; border:1.5px solid rgba(255,255,255,.5);
  border-radius:40px; font-size:9pt; letter-spacing:.28em; font-weight:700;
}
.cover h1{
  font-size:41pt; line-height:1.04; font-weight:800; letter-spacing:-.5px; margin:0 0 10mm;
  font-family:"Bitstream Charter","Liberation Serif",Georgia,serif;
  color:#fff; page-break-before:avoid;
}
.cover h1::after{ display:none; }
.cover .sub{ font-size:15pt; font-weight:400; line-height:1.4; opacity:.94; max-width:150mm; }
.cover .rule{ width:56mm; height:3px; background:var(--accent2); margin:9mm 0; filter:brightness(1.3); }
.cover .foot{ margin-top:auto; display:flex; justify-content:space-between; align-items:flex-end; font-size:10pt; }
.cover .foot .brand{ font-size:13pt; font-weight:800; letter-spacing:.02em; }
.cover .foot .brand span{ opacity:.7; font-weight:400; display:block; font-size:9pt; letter-spacing:.2em; margin-top:2px; }
.cover .price{ text-align:right; opacity:.85; font-size:9.5pt; line-height:1.6; }

/* ---------- CONTENTS ---------- */
.toc{ page-break-after:always; padding-top:4mm; }
.toc h2{ font-size:24pt; margin:0 0 8mm; }
.toc ol{ list-style:none; margin:0; padding:0; counter-reset:t; }
.toc li{ counter-increment:t; display:flex; align-items:baseline; padding:9px 0; border-bottom:1px solid var(--line); font-family:"DejaVu Sans","Liberation Sans",Arial,sans-serif; font-size:11pt; }
.toc li::before{ content:counter(t,decimal-leading-zero); color:var(--accent); font-weight:800; width:14mm; font-size:12pt; }
.toc li .t{ font-weight:600; }
.toc .lead{ font-size:11pt; color:var(--muted); font-family:"Bitstream Charter",serif; margin:0 0 10mm; max-width:150mm; }

/* ---------- HEADINGS ---------- */
h1{
  font-family:"DejaVu Sans","Liberation Sans",Arial,sans-serif;
  font-size:23pt; font-weight:800; letter-spacing:-.4px; line-height:1.12;
  color:#12151a; margin:0 0 5mm; padding-top:2mm; page-break-before:always; page-break-after:avoid;
}
h1:first-of-type{ page-break-before:avoid; }
h1 .n{ display:block; font-size:11pt; letter-spacing:.28em; color:var(--accent); margin-bottom:3mm; font-weight:800; }
h1::after{ content:""; display:block; width:26mm; height:3px; background:var(--accent); margin-top:5mm; }
h2{ font-family:"DejaVu Sans","Liberation Sans",Arial,sans-serif; font-size:14.5pt; font-weight:700; color:#171a1f; margin:8mm 0 3mm; page-break-after:avoid; }
h3{ font-family:"DejaVu Sans","Liberation Sans",Arial,sans-serif; font-size:11.6pt; font-weight:700; color:var(--accent); margin:6mm 0 2mm; page-break-after:avoid; letter-spacing:.01em; }
ul,ol{ margin:0 0 .8em; padding-left:5.5mm; }
li{ margin:.28em 0; }

/* ---------- CALLOUTS ---------- */
.callout{ border:1px solid var(--line); border-left:4px solid var(--accent); background:var(--bg-tint);
  border-radius:7px; padding:10px 14px 10px 14px; margin:5mm 0; page-break-inside:avoid; font-size:10.2pt; }
.callout .ct{ font-family:"DejaVu Sans","Liberation Sans",Arial,sans-serif; font-weight:700; font-size:10pt;
  margin-bottom:3px; display:flex; align-items:center; gap:7px; color:#14171c; }
.callout .ct .ico{ font-size:12.5pt; }
.callout p:last-child{ margin-bottom:0; }
.callout.tip{ --accent:#0f766e; border-left-color:#0f766e; background:#f0faf7; }
.callout.warn{ border-left-color:#c2410c; background:#fff6ef; }
.callout.note{ border-left-color:#475569; background:#f4f6f8; }
.callout.pro{ border-left-color:#7e22ce; background:#faf5ff; }
.callout.try{ border-left-color:#0e7490; background:#eefafe; }
.callout.gear{ border-left-color:#a16207; background:#fefbeb; }

/* ---------- KEY TAKEAWAY ---------- */
.key{ background:linear-gradient(135deg, var(--accent), color-mix(in srgb,var(--accent) 60%, #05070a));
  color:#fff; border-radius:9px; padding:14px 18px; margin:6mm 0; page-break-inside:avoid;
  font-family:"DejaVu Sans","Liberation Sans",Arial,sans-serif; }
.key .kt{ font-size:8.6pt; letter-spacing:.24em; text-transform:uppercase; opacity:.8; font-weight:700; margin-bottom:4px; }
.key p{ margin:0; font-size:12.5pt; line-height:1.4; font-weight:600; }

/* ---------- STEPS ---------- */
ol.steps{ list-style:none; counter-reset:s; padding:0; margin:5mm 0; }
ol.steps>li{ counter-increment:s; position:relative; padding:0 0 5mm 15mm; page-break-inside:avoid; }
ol.steps>li::before{ content:counter(s); position:absolute; left:0; top:-1mm; width:10mm; height:10mm;
  background:var(--accent); color:#fff; border-radius:50%; display:flex; align-items:center; justify-content:center;
  font-family:"DejaVu Sans","Liberation Sans",Arial,sans-serif; font-weight:800; font-size:12pt; }
ol.steps>li>.sh{ font-family:"DejaVu Sans","Liberation Sans",Arial,sans-serif; font-weight:700; font-size:11pt; display:block; margin-bottom:1mm; color:#14171c; }

/* ---------- CHECKLIST ---------- */
ul.check{ list-style:none; padding:0; margin:4mm 0; }
ul.check li{ position:relative; padding:4px 0 4px 9mm; font-size:10.4pt; page-break-inside:avoid; }
ul.check li::before{ content:""; position:absolute; left:0; top:3px; width:5mm; height:5mm; border:1.6px solid var(--accent); border-radius:3px; }
ul.check li::after{ content:"\2713"; position:absolute; left:.7mm; top:1.5px; color:var(--accent); font-weight:800; font-size:10pt; }

/* ---------- RECIPE CARDS ---------- */
.recipe{ border:1px solid var(--line); border-radius:9px; overflow:hidden; margin:5mm 0; page-break-inside:avoid; }
.recipe .rh{ background:var(--accent); color:#fff; padding:7px 13px; font-family:"DejaVu Sans","Liberation Sans",Arial,sans-serif; font-weight:700; font-size:10.6pt; display:flex; justify-content:space-between; align-items:center; }
.recipe .rh .tag{ font-size:8pt; letter-spacing:.16em; opacity:.85; font-weight:700; }
.recipe .rb{ padding:10px 13px; font-size:10pt; }
.chips{ display:flex; flex-wrap:wrap; gap:6px; margin:0 0 7px; }
.chip{ font-family:"DejaVu Sans","Liberation Sans",Arial,sans-serif; font-size:9pt; font-weight:600; background:var(--bg-tint);
  border:1px solid var(--line); border-radius:30px; padding:3px 10px; color:#22262c; }
.chip b{ color:var(--accent); }

/* ---------- CARD GRID (cheat cards) ---------- */
.cards{ display:grid; grid-template-columns:1fr 1fr; gap:5mm; margin:5mm 0; }
.cards.three{ grid-template-columns:1fr 1fr 1fr; }
.card{ border:1px solid var(--line); border-radius:9px; padding:11px 13px; page-break-inside:avoid; background:#fff; }
.card .ch{ font-family:"DejaVu Sans","Liberation Sans",Arial,sans-serif; font-weight:800; font-size:10.4pt; color:var(--accent); margin-bottom:4px; display:flex; align-items:center; gap:6px; }
.card ul{ margin:0; padding-left:4.5mm; font-size:9.6pt; }
.card p{ font-size:9.6pt; margin:0; }
.card.solid{ background:var(--bg-tint); }

/* ---------- TABLE ---------- */
table{ width:100%; border-collapse:collapse; margin:5mm 0; font-size:9.8pt; page-break-inside:avoid; }
th{ background:var(--accent); color:#fff; font-family:"DejaVu Sans","Liberation Sans",Arial,sans-serif; font-weight:700;
  text-align:left; padding:7px 10px; font-size:9.4pt; }
td{ padding:6px 10px; border-bottom:1px solid var(--line); vertical-align:top; }
tr:nth-child(even) td{ background:var(--bg-tint); }

/* ---------- MISC ---------- */
blockquote{ margin:5mm 0; padding:2mm 0 2mm 6mm; border-left:3px solid var(--accent2); font-style:italic; color:#33373d; font-size:11pt; }
hr{ border:none; border-top:1px solid var(--line); margin:7mm 0; }
.lead-in{ font-size:12pt; color:var(--muted); line-height:1.5; margin:0 0 5mm; }
.small{ font-size:8.8pt; color:var(--muted); }
.mono{ font-family:"DejaVu Sans Mono","Liberation Mono",monospace; font-size:9pt; }
.center{ text-align:center; }
.pill{ display:inline-block; background:var(--accent); color:#fff; font-family:"DejaVu Sans","Liberation Sans",Arial,sans-serif; font-size:8.4pt; font-weight:700; letter-spacing:.08em; padding:2px 9px; border-radius:20px; text-transform:uppercase; }
.end{ text-align:center; margin:14mm 0 0; page-break-inside:avoid; }
.end .mark{ font-family:"DejaVu Sans","Liberation Sans",Arial,sans-serif; font-weight:800; font-size:13pt; color:var(--accent); }
.end .sub{ color:var(--muted); font-size:10pt; margin-top:2mm; }
"""

DOC = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{title} — {brand}</title>
<style>{css}</style></head>
<body>
<div class="cover">
  <div class="wm"></div><div class="wm2"></div>
  <div class="cover-inner">
    <div class="kicker">{kicker}</div>
    <div style="margin-top:auto"></div>
    <h1>{title}</h1>
    <div class="rule"></div>
    <div class="sub">{subtitle}</div>
    <div class="foot">
      <div class="brand">{brand}<span>{site}</span></div>
      <div class="price">Reader's Edition · {year}<br>{price} value</div>
    </div>
  </div>
</div>
<div class="toc">
  <h2>What's Inside</h2>
  <div class="lead">{subtitle}. Written for {reader_lc}.</div>
  <ol>{toc}</ol>
</div>
{body}
</body></html>
"""

def build_one(g):
    src = SRC / f"{g['id']}.html"
    if not src.exists():
        print(f"  skip {g['id']} (no src)"); return False
    body = src.read_text()
    # collect chapter titles from top-level <h1>...</h1>
    titles = re.findall(r"<h1[^>]*>(.*?)</h1>", body, flags=re.S)
    def clean(t):
        t = re.sub(r"<span class=\"n\">.*?</span>", "", t, flags=re.S)
        t = re.sub(r"<[^>]+>", "", t)
        return html.unescape(t).strip()
    toc = "".join(f'<li><span class="t">{clean(t)}</span></li>' for t in titles)
    doc = DOC.format(
        css=CSS.replace("__ACCENT__", g["accent"]).replace("__ACCENT2__", g["accent2"]),
        title=html.escape(g["title"]), subtitle=html.escape(g["subtitle"]),
        kicker=html.escape(g["kicker"]), brand=html.escape(MANIFEST["brand"]),
        site=MANIFEST["site"], year=MANIFEST["year"], price=html.escape(g["price"]),
        reader_lc=html.escape(g["reader"][0].lower()+g["reader"][1:]),
        toc=toc, body=body,
    )
    (OUT / f"{g['id']}.html").write_text(doc)
    print(f"  built {g['id']}  ({len(titles)} chapters, {len(body)//1000}k chars)")
    return True

def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    gs = MANIFEST["guides"] if arg == "all" else [g for g in MANIFEST["guides"] if g["id"] == arg]
    if not gs:
        print(f"no guide matching '{arg}'"); sys.exit(1)
    for g in gs:
        build_one(g)

if __name__ == "__main__":
    main()
