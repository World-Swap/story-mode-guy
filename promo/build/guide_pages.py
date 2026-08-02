#!/usr/bin/env python3
"""Free SEO landing page per guide -> /learn/<id>.html + /learn/index.html.
Each page ranks for the guide's search term and funnels to the paid PDF/bundle.
Shows the hook, what's-inside (real chapter list), and a strong CTA. Does NOT
dump the paid body. Adds Product JSON-LD. Injects /learn/ URLs into sitemap.xml.
Run from repo root: python3 promo/build/guide_pages.py
"""
import json, re, html, pathlib

ROOT = pathlib.Path("/home/user/story-mode-guy")
G = ROOT / "guides"
OUT = ROOT / "learn"; OUT.mkdir(exist_ok=True)
M = json.loads((G / "manifest.json").read_text())

# guide id -> live Payhip product URL (photo + video). Drone = bundle CTA.
PAY = {
 "01-iphone-photography":"https://payhip.com/b/Hf8YW","02-lightroom-blueprint":"https://payhip.com/b/1gXQa",
 "03-product-photography":"https://payhip.com/b/Ynu1K","04-exposure-manual-mode":"https://payhip.com/b/1TJzr",
 "05-why-blurry":"https://payhip.com/b/pZADo","06-real-estate-photography":"https://payhip.com/b/kPbJX",
 "07-natural-light-portraits":"https://payhip.com/b/y8H6g","08-astrophotography":"https://payhip.com/b/bKhSu",
 "09-low-light-night":"https://payhip.com/b/HYs6z","10-cheat-sheet-pack":"https://payhip.com/b/lhZE4",
 "v01-cinematic-look":"https://payhip.com/b/k9Tvz","v02-phone-video":"https://payhip.com/b/30nYZ",
 "v03-editing-blueprint":"https://payhip.com/b/5t1AY","v04-color-grading":"https://payhip.com/b/QtcBz",
 "v05-audio-for-video":"https://payhip.com/b/tAeQd","v06-video-lighting":"https://payhip.com/b/AxJ4B",
 "v07-broll-storytelling":"https://payhip.com/b/1olQD","v08-camera-movement":"https://payhip.com/b/zhSxf",
 "v09-real-estate-video":"https://payhip.com/b/BcxD9","v10-video-cheat-sheet":"https://payhip.com/b/9QMfo",
}
DRONE_BUNDLE = "https://payhip.com/b/4QFxq"   # The Complete Drone Library

LINE_LABEL = {"photography":"Photography Guide","videography":"Videography Guide","drone":"Drone Guide"}

def thumb_for(gid):
    ids = [g["id"] for g in M["guides"]]
    n = ids.index(gid) + 1  # 1..33 == thumb-guide-01..33
    return f"thumb-guide-{n:02d}.jpg" if n < 10 else f"thumb-guide-{n}.jpg"

def extract(gid):
    src = (G / "src" / f"{gid}.html")
    body = src.read_text() if src.exists() else ""
    titles = re.findall(r"<h1[^>]*>(.*?)</h1>", body, flags=re.S)
    def clean(t):
        t = re.sub(r'<span class="n">.*?</span>', "", t, flags=re.S)
        return html.unescape(re.sub(r"<[^>]+>", "", t)).strip()
    chapters = [clean(t) for t in titles]
    lead = re.search(r'<p class="lead-in">(.*?)</p>', body, flags=re.S)
    lead = html.unescape(re.sub(r"<[^>]+>", "", lead.group(1))).strip() if lead else ""
    return chapters, lead

CSS = """
:root{--parch:#fefffc;--ink:#1b1b20;--char:#3a3a40;--ash:#6a6a72;--fog:#b4b8b4;--mist:#e3e6ea;
--blue:#41a1cf;--serif:'Fraunces',Georgia,serif;--sans:'Inter',system-ui,sans-serif;--accent:__ACCENT__}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--sans);color:var(--char);background:var(--parch);line-height:1.7;font-size:17px;-webkit-font-smoothing:antialiased}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.nav{position:sticky;top:0;z-index:10;display:flex;align-items:center;gap:14px;justify-content:center;background:rgba(255,255,255,.9);backdrop-filter:blur(12px);border-bottom:1px solid var(--mist);padding:12px 16px}
.nav .brand{display:flex;align-items:center;gap:9px;font-family:var(--serif);font-size:17px;color:var(--ink)}
.nav .brand img{width:30px;height:30px;border-radius:50%}
.nav .sp{flex:1}.nav .lnk{font-size:14px;font-weight:500;color:var(--char)}
.wrap{max-width:820px;margin:0 auto;padding:40px 22px 30px}
.hero{display:grid;grid-template-columns:1fr 300px;gap:32px;align-items:start}
@media(max-width:720px){.hero{grid-template-columns:1fr}.hero .cover{order:-1;max-width:240px;margin:0 auto}}
.eyebrow{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--accent);margin-bottom:12px}
h1{font-family:var(--serif);font-weight:600;font-size:clamp(28px,4.6vw,42px);line-height:1.08;letter-spacing:-.02em;color:var(--ink);margin-bottom:12px}
.sub{font-size:19px;color:var(--ash);margin-bottom:18px}
.cover img{width:100%;border-radius:12px;border:1px solid var(--mist);box-shadow:0 14px 40px rgba(0,0,0,.13)}
.buy{display:inline-flex;align-items:center;gap:10px;background:var(--accent);color:#fff;font-weight:600;padding:13px 24px;border-radius:44px;font-size:16px;margin-top:8px}
.buy:hover{text-decoration:none;filter:brightness(.96)}
.price{font-size:15px;color:var(--ash);margin-top:10px}
.price b{color:var(--ink);font-size:17px}
section{margin-top:40px}
h2{font-family:var(--serif);font-weight:600;font-size:26px;color:var(--ink);margin-bottom:14px}
.lead{font-size:18px;color:var(--char);border-left:3px solid var(--accent);padding-left:16px;margin:6px 0 8px;font-style:italic}
ul.inside{list-style:none;padding:0;display:grid;gap:9px}
ul.inside li{position:relative;padding:8px 0 8px 30px;border-bottom:1px solid var(--mist);font-weight:500;color:var(--ink)}
ul.inside li::before{content:"";position:absolute;left:2px;top:12px;width:14px;height:14px;border-radius:4px;background:var(--accent)}
.cta{background:linear-gradient(135deg,var(--accent),#0b1220);color:#fff;border-radius:16px;padding:28px 26px;margin-top:40px;text-align:center}
.cta h3{color:#fff;font-family:var(--serif);font-weight:600;font-size:25px;margin-bottom:8px}
.cta p{color:rgba(255,255,255,.9);margin-bottom:16px}
.cta a.btn{display:inline-block;background:#fff;color:#111;font-weight:600;padding:12px 26px;border-radius:44px}
.cta a.btn:hover{text-decoration:none;filter:brightness(.97)}
.related{border-top:1px solid var(--mist);margin-top:36px;padding-top:20px}
.related h4{font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--ash);margin-bottom:10px}
.related a{display:block;padding:5px 0}
.foot{border-top:1px solid var(--mist);margin-top:30px;padding:26px 22px;text-align:center;font-size:13px;color:var(--fog);max-width:820px;margin:30px auto 0}
.foot a{color:var(--ash)}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px;margin-top:10px}
.gcard{display:block;border:1px solid var(--mist);border-radius:14px;overflow:hidden;background:#fff;transition:transform .15s}
.gcard:hover{transform:translateY(-2px);text-decoration:none}
.gcard img{width:100%;aspect-ratio:3/4;object-fit:cover}
.gcard .b{padding:12px 14px}.gcard h3{font-family:var(--serif);font-size:17px;color:var(--ink);margin:0 0 4px}
.gcard p{font-size:13px;color:var(--ash);margin:0}
"""

NAV = """<div class="nav"><a class="brand" href="/"><img src="/smg-logo.png" alt="Story Mode Guy">Story Mode Guy</a>
<span class="sp"></span><a class="lnk" href="/#guides">Guides</a><a class="lnk" href="/learn/">Learn</a><a class="lnk" href="/blog/">Journal</a></div>"""
FOOT = """<div class="foot">© 2026 Story Mode Guy · <a href="/">storymodeguy.com</a> · <a href="/learn/">All guides</a> · <a href="/blog/">Journal</a></div>"""

def buy_for(g):
    return PAY.get(g["id"], DRONE_BUNDLE)

def page(g, related):
    gid=g["id"]; chapters, lead = extract(gid)
    thumb = thumb_for(gid)
    buy = buy_for(g)
    is_drone = g["line"]=="drone"
    price_line = (f'<div class="price"><b>{html.escape(g["price"])}</b> · instant PDF download</div>'
                  if not is_drone else
                  f'<div class="price">Included in <b>The Complete Drone Library ($79)</b> &amp; the Everything bundle</div>')
    inside = "".join(f"<li>{html.escape(c)}</li>" for c in chapters)
    ld={"@context":"https://schema.org","@type":"Product","name":g["title"],
        "description":g["subtitle"],"image":f"https://storymodeguy.com/{thumb}",
        "brand":{"@type":"Brand","name":"Story Mode Guy"},
        "offers":{"@type":"Offer","priceCurrency":"USD","price":re.sub(r"[^0-9.]","",g["price"]),
                  "url":buy,"availability":"https://schema.org/InStock"}}
    rel="".join(f'<a href="/learn/{r["id"]}.html">{html.escape(r["title"])}</a>' for r in related)
    cta_label = "Get the guide" if not is_drone else "Get the Drone Library"
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(g['title'])} — {html.escape(g['subtitle'])} | Story Mode Guy</title>
<meta name="description" content="{html.escape(g['subtitle'])}. {html.escape(lead[:120])}">
<link rel="canonical" href="https://storymodeguy.com/learn/{gid}.html">
<link rel="icon" type="image/png" href="/smg-logo.png">
<meta property="og:type" content="product"><meta property="og:title" content="{html.escape(g['title'])}">
<meta property="og:description" content="{html.escape(g['subtitle'])}">
<meta property="og:image" content="https://storymodeguy.com/{thumb}">
<meta property="og:url" content="https://storymodeguy.com/learn/{gid}.html">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS.replace("__ACCENT__", g["accent"])}</style>
<script type="application/ld+json">{json.dumps(ld)}</script>
</head><body>
{NAV}
<main class="wrap">
<div class="hero">
  <div>
    <div class="eyebrow">{html.escape(LINE_LABEL[g['line']])}</div>
    <h1>{html.escape(g['title'])}</h1>
    <div class="sub">{html.escape(g['subtitle'])}</div>
    <a class="buy" href="{buy}" target="_blank" rel="noopener">{cta_label} →</a>
    {price_line}
  </div>
  <div class="cover"><img src="/{thumb}" alt="{html.escape(g['title'])} guide cover"></div>
</div>

<section>
  <h2>Who it's for</h2>
  <p>{html.escape(g['reader'])}. {html.escape(lead)}</p>
</section>

<section>
  <h2>What's inside</h2>
  <ul class="inside">{inside}</ul>
</section>

<div class="cta">
  <h3>{html.escape(g['title'])}</h3>
  <p>{html.escape(g['subtitle'])} — instant PDF download.</p>
  <a class="btn" href="{buy}" target="_blank" rel="noopener">{cta_label} →</a>
</div>

<div class="related"><h4>More guides</h4>{rel}</div>
</main>
{FOOT}
</body></html>"""

guides = [g for g in M["guides"] if g.get("line") != "free"]
for g in guides:
    same = [x for x in guides if x["line"]==g["line"] and x["id"]!=g["id"]][:4]
    (OUT / f"{g['id']}.html").write_text(page(g, same))
print(f"  wrote {len(guides)} /learn pages")

# index
def card(g):
    return (f'<a class="gcard" href="/learn/{g["id"]}.html"><img src="/{thumb_for(g["id"])}" alt="{html.escape(g["title"])}">'
            f'<div class="b"><h3>{html.escape(g["title"])}</h3><p>{html.escape(g["subtitle"])}</p></div></a>')
groups=""
for line,label in [("photography","Photography Guides"),("videography","Videography Guides"),("drone","Drone Guides")]:
    gs=[g for g in guides if g["line"]==line]
    groups+=f'<section><h2>{label}</h2><div class="cards">'+"".join(card(g) for g in gs)+'</div></section>'
idx=f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Learn — Photography, Video &amp; Drone Guides | Story Mode Guy</title>
<meta name="description" content="Premium photography, videography, and drone guides — from your first manual photo to paid aerial work. Instant PDF downloads.">
<link rel="canonical" href="https://storymodeguy.com/learn/">
<link rel="icon" type="image/png" href="/smg-logo.png">
<meta property="og:title" content="Learn — Photography, Video & Drone Guides"><meta property="og:image" content="https://storymodeguy.com/og-image.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS.replace("__ACCENT__","#41a1cf")}</style></head><body>
{NAV}
<main class="wrap"><div class="eyebrow">The Library</div>
<h1>Learn the craft</h1><div class="sub">33 guides across photography, video, and drone — genuinely useful, beautifully made.</div>
{groups}</main>
{FOOT}</body></html>"""
(OUT/"index.html").write_text(idx)
print("  wrote learn/index.html")

# sitemap injection
sm=ROOT/"sitemap.xml"
if sm.exists():
    s=sm.read_text()
    urls=["https://storymodeguy.com/learn/"]+[f"https://storymodeguy.com/learn/{g['id']}.html" for g in guides]
    add=""
    for u in urls:
        if u not in s:
            add+=f'  <url>\n    <loc>{u}</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n\n'
    if add:
        s=s.replace("</urlset>", add+"</urlset>",1); sm.write_text(s); print("  sitemap +%d"%add.count("<url>"))
print("done")
