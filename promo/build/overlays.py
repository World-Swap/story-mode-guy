#!/usr/bin/env python3
"""Render per-photo reel text overlays (1080x1920 transparent PNGs) in one Chromium pass.
Reads items.json: [{"n":53,"title":"...","kicker":"SANTA CRUZ COAST"}, ...]
Writes <outdir>/ov-<n>.png
"""
import sys, json, pathlib, subprocess, html

items = json.loads(pathlib.Path(sys.argv[1]).read_text())
OUT = pathlib.Path(sys.argv[2]).resolve(); OUT.mkdir(parents=True, exist_ok=True)
LOGO = "file:///home/user/story-mode-guy/smg-logo.png"
ACC = "#41a1cf"

CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
.card{{position:relative;width:1080px;height:1920px;overflow:hidden;
  font-family:'DejaVu Sans','Liberation Sans',sans-serif;color:#fff}}
.gtop{{position:absolute;top:0;left:0;right:0;height:620px;
  background:linear-gradient(180deg, rgba(6,8,12,.62) 0%, rgba(6,8,12,.18) 55%, rgba(6,8,12,0) 100%)}}
.gbot{{position:absolute;bottom:0;left:0;right:0;height:520px;
  background:linear-gradient(0deg, rgba(6,8,12,.72) 0%, rgba(6,8,12,.22) 55%, rgba(6,8,12,0) 100%)}}
.top{{position:absolute;top:96px;left:0;right:0;text-align:center;padding:0 90px}}
.logo{{width:104px;height:104px;border-radius:50%;object-fit:cover;
  box-shadow:0 6px 24px rgba(0,0,0,.5);border:3px solid rgba(255,255,255,.85)}}
.title{{font-family:'Bitstream Charter','DejaVu Serif',Georgia,serif;font-weight:700;
  font-size:62px;line-height:1.08;margin-top:30px;text-shadow:0 3px 20px rgba(0,0,0,.55);letter-spacing:-.5px}}
.kicker{{margin-top:18px;font-size:25px;letter-spacing:.34em;font-weight:700;
  color:rgba(255,255,255,.92);text-transform:uppercase;text-shadow:0 2px 10px rgba(0,0,0,.6)}}
.bot{{position:absolute;bottom:120px;left:0;right:0;text-align:center}}
.brand{{font-size:46px;font-weight:800;letter-spacing:.06em;text-shadow:0 3px 16px rgba(0,0,0,.6)}}
.tag{{margin-top:14px;font-size:23px;letter-spacing:.28em;font-weight:700;text-transform:uppercase;
  color:rgba(255,255,255,.9);text-shadow:0 2px 10px rgba(0,0,0,.6)}}
.tag b{{color:{ACC}}}
"""

def card(it):
    return (f'<div class="card" id="ov{it["n"]}">'
            f'<div class="gtop"></div><div class="gbot"></div>'
            f'<div class="top"><img class="logo" src="{LOGO}">'
            f'<div class="title">{html.escape(it["title"])}</div>'
            f'<div class="kicker">{html.escape(it["kicker"])}</div></div>'
            f'<div class="bot"><div class="brand">STORYMODEGUY.COM</div>'
            f'<div class="tag">PRINTS <b>·</b> WALLPAPERS <b>·</b> ORIGINAL EBOOKS</div></div>'
            f'</div>')

doc = f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>" \
      + "".join(card(it) for it in items) + "</body></html>"
hp = OUT / "_overlays.html"; hp.write_text(doc)

ids = ",".join(str(it["n"]) for it in items)
node = f"""
const pw=require('/opt/node22/lib/node_modules/playwright');
(async()=>{{
  const b=await pw.chromium.launch({{args:['--no-sandbox','--disable-gpu']}});
  const p=await b.newPage({{viewport:{{width:1080,height:1920}},deviceScaleFactor:1}});
  await p.goto('file://{hp}',{{waitUntil:'networkidle'}});
  for(const n of [{ids}]){{
    const el=await p.$('#ov'+n);
    await el.screenshot({{path:'{OUT}/ov-'+n+'.png', omitBackground:true}});
  }}
  await b.close();
}})().catch(e=>{{console.error(e);process.exit(1)}});
"""
(OUT/"_ov.js").write_text(node)
subprocess.run(["node", str(OUT/"_ov.js")],
               env={"PATH":"/opt/node22/bin:/usr/bin:/bin","PLAYWRIGHT_BROWSERS_PATH":"/opt/pw-browsers"}, check=True)
print(f"overlays -> {OUT}  ({len(items)} rendered)")
