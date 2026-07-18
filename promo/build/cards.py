#!/usr/bin/env python3
"""Generate branded reel overlay cards (title, CTA) and a persistent brand bar
as 1080x1920 PNGs, rendered via headless Chromium for nice typography.

Usage: python3 cards.py "<PACK TITLE>" "<SUBTITLE>" "<CTA LINE>" <out-dir> <accent>
Outputs: <out-dir>/title.png, <out-dir>/cta.png, <out-dir>/bar.png
"""
import sys, json, subprocess, pathlib, html

TITLE, SUB, CTA, OUTDIR, ACCENT = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
OUT = pathlib.Path(OUTDIR).resolve(); OUT.mkdir(parents=True, exist_ok=True)
LOGO = "file:///home/user/story-mode-guy/smg-logo.png"

CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'DejaVu Sans','Liberation Sans',sans-serif}}
.card{{position:relative;width:1080px;height:1920px;overflow:hidden;color:#fff}}
.dark{{background:radial-gradient(120% 80% at 50% 15%, #23232e 0%, #16161c 55%, #0c0c10 100%)}}
.glow{{position:absolute;width:900px;height:900px;border-radius:50%;top:-260px;left:50%;transform:translateX(-50%);
  background:radial-gradient(circle, {ACCENT}44, transparent 62%)}}
.wrap{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;text-align:center;padding:150px 90px}}
.logo{{width:150px;height:150px;border-radius:26px;object-fit:cover;box-shadow:0 12px 40px rgba(0,0,0,.5)}}
.kick{{margin-top:38px;font-size:30px;letter-spacing:.42em;font-weight:700;color:{ACCENT};text-transform:uppercase}}
.serif{{font-family:'Bitstream Charter','Liberation Serif',Georgia,serif}}
h1{{font-size:118px;line-height:1.02;font-weight:800;margin-top:auto;letter-spacing:-1px}}
.rule{{width:150px;height:6px;background:{ACCENT};border-radius:4px;margin:44px 0}}
.sub{{font-size:44px;font-weight:400;line-height:1.35;opacity:.94;max-width:820px}}
.handle{{margin-top:auto;font-size:38px;font-weight:700;letter-spacing:.02em}}
.handle span{{opacity:.6;font-weight:400}}
/* CTA specifics */
.big{{font-size:96px;font-weight:800;line-height:1.05;margin-top:auto}}
.url{{font-family:'Bitstream Charter',serif;font-size:60px;color:{ACCENT};margin-top:26px;font-weight:700}}
.pill{{margin-top:40px;display:inline-block;border:2px solid rgba(255,255,255,.5);border-radius:60px;
  padding:20px 46px;font-size:34px;font-weight:600;letter-spacing:.04em}}
/* brand bar (transparent, content at bottom) */
.barcard{{position:relative;width:1080px;height:1920px;background:transparent}}
.bar{{position:absolute;left:0;right:0;bottom:0;height:230px;
  background:linear-gradient(0deg, rgba(6,7,10,.82) 0%, rgba(6,7,10,.45) 55%, rgba(6,7,10,0) 100%);
  display:flex;align-items:flex-end;justify-content:space-between;padding:0 60px 60px}}
.bl{{display:flex;align-items:center;gap:22px}}
.bl img{{width:82px;height:82px;border-radius:16px;object-fit:cover}}
.bl .nm{{font-size:38px;font-weight:800;letter-spacing:.01em}}
.bl .nm span{{display:block;font-size:22px;font-weight:400;color:{ACCENT};letter-spacing:.16em;margin-top:3px}}
.br{{font-size:34px;font-weight:700;opacity:.92}}
"""

DOC = f"""<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="card dark" id="title">
  <div class="glow"></div>
  <div class="wrap">
    <img class="logo" src="{LOGO}">
    <div class="kick">Story Mode Guy</div>
    <h1 class="serif">{html.escape(TITLE)}</h1>
    <div class="rule"></div>
    <div class="sub">{html.escape(SUB)}</div>
    <div class="handle">@storymodeguy <span>· storymodeguy.com</span></div>
  </div>
</div>

<div class="card dark" id="cta">
  <div class="glow"></div>
  <div class="wrap">
    <img class="logo" src="{LOGO}">
    <div class="kick">Story Mode Guy</div>
    <div class="big serif">{html.escape(CTA)}</div>
    <div class="url">storymodeguy.com</div>
    <div class="pill">Wallpapers &amp; Prints</div>
    <div class="handle">@storymodeguy</div>
  </div>
</div>

<div class="barcard" id="bar">
  <div class="bar">
    <div class="bl"><img src="{LOGO}"><div class="nm">Story Mode Guy<span>@STORYMODEGUY</span></div></div>
    <div class="br">storymodeguy.com</div>
  </div>
</div>
</body></html>"""

htmlpath = OUT / "_cards.html"
htmlpath.write_text(DOC)

node = f"""
const pw = require('/opt/node22/lib/node_modules/playwright');
(async () => {{
  const b = await pw.chromium.launch({{args:['--no-sandbox','--disable-gpu']}});
  const p = await b.newPage({{viewport:{{width:1080,height:1920}}, deviceScaleFactor:1}});
  await p.goto('file://{htmlpath}', {{waitUntil:'networkidle'}});
  for (const id of ['title','cta','bar']) {{
    const el = await p.$('#'+id);
    await el.screenshot({{path:'{OUT}/'+id+'.png', omitBackground: id==='bar'}});
  }}
  await b.close();
}})().catch(e=>{{console.error(e);process.exit(1)}});
"""
(OUT / "_shot.js").write_text(node)
subprocess.run(["node", str(OUT / "_shot.js")], env={"PATH":"/opt/node22/bin:/usr/bin:/bin","PLAYWRIGHT_BROWSERS_PATH":"/opt/pw-browsers"}, check=True)
print("cards ->", OUT)
