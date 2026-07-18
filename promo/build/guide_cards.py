#!/usr/bin/env python3
"""Render branded guide reel cards (title, features, cta, bar) as 1080x1920 PNGs.
Usage: python3 guide_cards.py <spec.json> <outdir>
spec.json: {"title","subtitle","bullets":[...],"accent","cta","kicker"}
"""
import sys, json, subprocess, pathlib, html

spec = json.loads(pathlib.Path(sys.argv[1]).read_text())
OUT = pathlib.Path(sys.argv[2]).resolve(); OUT.mkdir(parents=True, exist_ok=True)
LOGO = "file:///home/user/story-mode-guy/smg-logo.png"
ACC = spec["accent"]
KICK = spec.get("kicker", "Photography Guide")
bullets = "".join(f"<li>{html.escape(b)}</li>" for b in spec["bullets"])

CSS = f"""
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'DejaVu Sans','Liberation Sans',sans-serif}}
.card{{position:relative;width:1080px;height:1920px;overflow:hidden;color:#fff}}
.dark{{background:linear-gradient(160deg, {ACC} 0%, color-mix(in srgb, {ACC} 42%, #0a0c10) 100%)}}
.glow{{position:absolute;width:820px;height:820px;border-radius:50%;top:-240px;right:-160px;
  background:radial-gradient(circle, rgba(255,255,255,.14), transparent 62%)}}
.wrap{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;text-align:center;padding:150px 96px}}
.logo{{width:112px;height:112px;border-radius:26px;object-fit:cover;box-shadow:0 12px 40px rgba(0,0,0,.45)}}
.kick{{margin-top:36px;font-size:27px;letter-spacing:.34em;font-weight:700;text-transform:uppercase;color:rgba(255,255,255,.9)}}
.serif{{font-family:'Bitstream Charter','DejaVu Serif',Georgia,serif}}
h1{{font-size:96px;line-height:1.03;font-weight:800;margin-top:auto;letter-spacing:-1px;text-shadow:0 4px 24px rgba(0,0,0,.35)}}
.rule{{width:150px;height:6px;background:rgba(255,255,255,.9);border-radius:4px;margin:44px 0}}
.sub{{font-size:42px;font-weight:400;line-height:1.35;opacity:.95;max-width:820px}}
.handle{{margin-top:auto;font-size:38px;font-weight:700}}
.handle span{{opacity:.7;font-weight:400}}
/* features */
.ftitle{{font-family:'Bitstream Charter',serif;font-size:60px;font-weight:800;line-height:1.08;margin-top:26px}}
ul.feat{{list-style:none;margin:auto 0;padding:0;text-align:left;width:100%;max-width:760px}}
ul.feat li{{position:relative;font-size:44px;font-weight:600;line-height:1.3;padding:22px 0 22px 84px;border-bottom:1px solid rgba(255,255,255,.16)}}
ul.feat li::before{{content:"\\2713";position:absolute;left:12px;top:20px;width:56px;height:56px;border-radius:50%;
  background:rgba(255,255,255,.16);display:flex;align-items:center;justify-content:center;font-size:34px;font-weight:800}}
/* cta */
.big{{font-size:104px;font-weight:800;line-height:1.03;margin-top:auto}}
.price{{margin-top:20px;font-family:'Bitstream Charter',serif;font-size:64px;font-weight:800}}
.url{{margin-top:14px;font-size:46px;font-weight:700;opacity:.95}}
.pill{{margin-top:40px;display:inline-block;border:2px solid rgba(255,255,255,.55);border-radius:60px;padding:20px 46px;font-size:34px;font-weight:600;letter-spacing:.03em}}
/* bar */
.barcard{{position:relative;width:1080px;height:1920px;background:transparent}}
.bar{{position:absolute;left:0;right:0;bottom:0;height:230px;
  background:linear-gradient(0deg, rgba(6,7,10,.82) 0%, rgba(6,7,10,.4) 55%, rgba(6,7,10,0) 100%);
  display:flex;align-items:flex-end;justify-content:space-between;padding:0 60px 60px;color:#fff}}
.bl{{display:flex;align-items:center;gap:22px}}
.bl img{{width:82px;height:82px;border-radius:16px;object-fit:cover}}
.bl .nm{{font-size:38px;font-weight:800}}
.bl .nm span{{display:block;font-size:22px;font-weight:400;opacity:.7;letter-spacing:.16em;margin-top:3px}}
.br{{font-size:34px;font-weight:700;opacity:.92}}
"""

DOC = f"""<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>
<div class="card dark" id="title"><div class="glow"></div><div class="wrap">
  <img class="logo" src="{LOGO}"><div class="kick">{html.escape(KICK)}</div>
  <h1 class="serif">{html.escape(spec['title'])}</h1><div class="rule"></div>
  <div class="sub">{html.escape(spec['subtitle'])}</div>
  <div class="handle">@storymodeguy <span>· storymodeguy.com</span></div>
</div></div>

<div class="card dark" id="features"><div class="glow"></div><div class="wrap">
  <img class="logo" src="{LOGO}"><div class="kick">What's Inside</div>
  <div class="ftitle serif">{html.escape(spec['title'])}</div>
  <ul class="feat">{bullets}</ul>
  <div class="handle">@storymodeguy</div>
</div></div>

<div class="card dark" id="cta"><div class="glow"></div><div class="wrap">
  <img class="logo" src="{LOGO}"><div class="kick">{html.escape(spec.get('cta_kicker','Get the guide'))}</div>
  <div class="big serif">{html.escape(spec['title'])}</div>
  <div class="price">{html.escape(spec.get('price',''))}</div>
  <div class="url">storymodeguy.com</div>
  <div class="pill">{html.escape(spec.get('cta_pill','Instant PDF download'))}</div>
  <div class="handle">@storymodeguy</div>
</div></div>

<div class="barcard" id="bar"><div class="bar">
  <div class="bl"><img src="{LOGO}"><div class="nm">Story Mode Guy<span>@STORYMODEGUY</span></div></div>
  <div class="br">storymodeguy.com</div>
</div></div>
</body></html>"""

hp = OUT / "_gcards.html"; hp.write_text(DOC)
node = f"""
const pw=require('/opt/node22/lib/node_modules/playwright');
(async()=>{{const b=await pw.chromium.launch({{args:['--no-sandbox','--disable-gpu']}});
const p=await b.newPage({{viewport:{{width:1080,height:1920}}}});
await p.goto('file://{hp}',{{waitUntil:'networkidle'}});
for(const id of ['title','features','cta','bar']){{
  const el=await p.$('#'+id);
  await el.screenshot({{path:'{OUT}/'+id+'.png', omitBackground: id==='bar'}});
}}
await b.close();}})().catch(e=>{{console.error(e);process.exit(1)}});
"""
(OUT/"_g.js").write_text(node)
subprocess.run(["node", str(OUT/"_g.js")],
               env={"PATH":"/opt/node22/bin:/usr/bin:/bin","PLAYWRIGHT_BROWSERS_PATH":"/opt/pw-browsers"}, check=True)
print("guide cards ->", OUT)
