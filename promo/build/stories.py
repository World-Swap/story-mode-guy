#!/usr/bin/env python3
"""Google Web Stories (AMP) -> /stories/<slug>.html + /stories/index.html.
Visual, full-screen stories Google can surface in Discover and mobile search.
Self-contained AMP; images are existing site assets. Injects /stories/ into sitemap.
Run from repo root: python3 promo/build/stories.py
"""
import pathlib, json, html
ROOT = pathlib.Path("/home/user/story-mode-guy")
OUT = ROOT / "stories"; OUT.mkdir(exist_ok=True)
SITE = "https://storymodeguy.com"

BOILER = ('<style amp-boilerplate>body{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;'
'-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;'
'animation:-amp-start 8s steps(1,end) 0s 1 normal both}@-webkit-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}'
'@-moz-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-ms-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}'
'@-o-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}'
'</style><noscript><style amp-boilerplate>body{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}</style></noscript>')

AMPCSS = ("""amp-story{font-family:'Inter',system-ui,sans-serif}
.scrim{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.15) 0%,rgba(0,0,0,0) 35%,rgba(0,0,0,.05) 60%,rgba(0,0,0,.78) 100%)}
.txt{position:absolute;left:0;right:0;bottom:0;padding:0 34px 60px;color:#fff}
.kick{font-size:15px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:#ffd9a8;margin-bottom:10px}
.head{font-family:'Fraunces',Georgia,serif;font-weight:600;font-size:40px;line-height:1.08;margin-bottom:12px;text-shadow:0 2px 18px rgba(0,0,0,.5)}
.body{font-size:20px;line-height:1.45;color:#f2f2f2;text-shadow:0 2px 12px rgba(0,0,0,.6)}
.cover .head{font-size:52px}
.brand{position:absolute;top:44px;left:34px;color:#fff;font-family:'Fraunces',serif;font-size:20px;font-weight:600;text-shadow:0 2px 12px rgba(0,0,0,.6)}
.center{display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;inset:0;padding:0 40px}
.center .head{font-size:50px}""")

def img_layer(src, alt):
    return (f'<amp-story-grid-layer template="fill"><amp-img src="/{src}" layout="fill" '
            f'alt="{html.escape(alt)}"></amp-img></amp-story-grid-layer>'
            '<amp-story-grid-layer template="fill"><div class="scrim"></div></amp-story-grid-layer>')

def page(pid, img, alt, kicker, head, body, cover=False):
    cls = "txt cover" if cover else "txt"
    inner = ""
    if kicker: inner += f'<div class="kick">{html.escape(kicker)}</div>'
    inner += f'<div class="head">{html.escape(head)}</div>'
    if body: inner += f'<div class="body">{html.escape(body)}</div>'
    return (f'<amp-story-page id="{pid}">'
            + img_layer(img, alt)
            + '<amp-story-grid-layer template="fill"><div class="brand">Story Mode Guy</div></amp-story-grid-layer>'
            + f'<amp-story-grid-layer template="vertical"><div class="{cls}">{inner}</div></amp-story-grid-layer>'
            + '</amp-story-page>')

def outlink_page(pid, img, alt, head, body, url, label):
    return (f'<amp-story-page id="{pid}">'
            + img_layer(img, alt)
            + f'<amp-story-grid-layer template="vertical"><div class="txt"><div class="head">{html.escape(head)}</div>'
            + f'<div class="body">{html.escape(body)}</div></div></amp-story-grid-layer>'
            + f'<amp-story-page-outlink layout="nodisplay"><a href="{url}">{html.escape(label)}</a></amp-story-page-outlink>'
            + '</amp-story-page>')

def build(story):
    pages = "".join(story["pages"])
    doc = f"""<!doctype html><html amp lang="en"><head>
<meta charset="utf-8">
<title>{html.escape(story['title'])}</title>
<link rel="canonical" href="{SITE}/stories/{story['slug']}.html">
<meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
<meta name="description" content="{html.escape(story['desc'])}">
<script async src="https://cdn.ampproject.org/v0.js"></script>
<script async custom-element="amp-story" src="https://cdn.ampproject.org/v0/amp-story-1.0.js"></script>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
{BOILER}
<style amp-custom>{AMPCSS}</style>
</head><body>
<amp-story standalone title="{html.escape(story['title'])}" publisher="Story Mode Guy"
  publisher-logo-src="{SITE}/smg-logo.png"
  poster-portrait-src="{SITE}/{story['poster']}">
{pages}
</amp-story>
</body></html>"""
    (OUT / f"{story['slug']}.html").write_text(doc)
    print("  wrote stories/"+story["slug"]+".html")

STORIES = [
{
 "slug":"santa-cruz-sunset-spots","title":"The Best Sunset Spots in Santa Cruz","poster":"photo-01.jpg",
 "desc":"Seven of the best places to watch and photograph the sunset in Santa Cruz, California.",
 "pages":[
   page("c","photo-01.jpg","Santa Cruz sunset","Story Mode Guy","Best Sunset Spots in Santa Cruz","Seven places I keep coming back to for the light.",cover=True),
   page("p1","photo-05.jpg","West Cliff Drive","01 · West Cliff Drive","West Cliff Drive","Unbroken western horizon and surf below the bluffs. Stay for the afterglow."),
   page("p2","photo-08.jpg","Natural Bridges","02 · Natural Bridges","Natural Bridges","The sea arch gives you a foreground almost nowhere else in town can match."),
   page("p3","photo-12.jpg","The Wharf","03 · The Wharf","The Santa Cruz Wharf","Pilings marching out to sea with the sun sinking behind them."),
   page("p4","photo-20.jpg","The Boardwalk","04 · Blue Hour","The Boardwalk","Wait for blue hour — deep blue sky, ride lights already on."),
   outlink_page("cta","photo-03.jpg","Santa Cruz coast","See the whole coast","Prints, wallpapers and the full gallery.", "/gallery.html","Open the gallery"),
 ]},
{
 "slug":"photography-guide-library","title":"The Photography Guide Library","poster":"thumb-guide-01.jpg",
 "desc":"Ten photography guides — from your first manual shot to selling your work.",
 "pages":[
   page("c","photo-02.jpg","Photography guides","Story Mode Guy","Learn Photography, Beautifully","Ten guides that fix real problems.",cover=True),
   page("p1","thumb-guide-05.jpg","Why blurry guide","Fix-It","Why Are My Photos Blurry?","Name the blur — shake, motion, or focus — and fix each one."),
   page("p2","thumb-guide-04.jpg","Manual mode guide","Fundamentals","Master Your Camera","The exposure triangle and manual mode, made simple."),
   page("p3","thumb-guide-01.jpg","iPhone guide","Mobile","Pro Photos From Your Pocket","Your phone is a better camera than you think."),
   outlink_page("cta","photo-06.jpg","Learn more","33 guides, one library","Photography, video and drone — genuinely useful, beautifully made.", "/learn/","Browse the guides"),
 ]},
{
 "slug":"start-flying-a-drone","title":"Start Flying a Drone: First-Flight Tips","poster":"thumb-guide-21.jpg",
 "desc":"Five tips for a calm, confident first drone flight — and how to not crash it.",
 "pages":[
   page("c","photo-14.jpg","Drone sky","Story Mode Guy","Fly a Drone Without Crashing It","Five tips for a calm first flight.",cover=True),
   page("p1","photo-18.jpg","Pre-flight","01","Run a pre-flight check","Firmware, props, batteries, GPS lock, home point — every time."),
   page("p2","photo-22.jpg","Wind","02","Respect the wind","Most flyaways start with weather past your drone's limit."),
   page("p3","photo-30.jpg","Return to home","03","Set Return-to-Home right","Above the tallest obstacle — the setting that saves drones."),
   page("p4","photo-05.jpg","Battery","04","Land at 30% battery","Don't chase one more shot. Batteries are the quiet crash cause."),
   outlink_page("cta","thumb-guide-21.jpg","Drone guides","Learn to fly, film & get paid","The complete drone library — flying, laws, cinematic moves and more.", "/learn/d01-drone-beginners.html","See the drone guides"),
 ]},
]

for s in STORIES: build(s)

# index (regular HTML page listing the stories)
cards="".join(f'<a class="scard" href="/stories/{s["slug"]}.html"><div class="b"><h3>{html.escape(s["title"])}</h3><p>{html.escape(s["desc"])}</p></div></a>' for s in STORIES)
idx=f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Web Stories — Story Mode Guy</title>
<meta name="description" content="Visual web stories from Story Mode Guy — Santa Cruz photography, guides, and drone tips.">
<link rel="canonical" href="{SITE}/stories/">
<link rel="icon" type="image/png" href="/smg-logo.png">
<style>body{{font-family:'Inter',system-ui,sans-serif;color:#3a3a40;background:#fefffc;line-height:1.6;margin:0}}
a{{color:#41a1cf;text-decoration:none}}.wrap{{max-width:720px;margin:0 auto;padding:44px 22px}}
h1{{font-family:'Fraunces',Georgia,serif;font-size:38px;color:#1b1b20;margin:0 0 8px}}
.sub{{color:#6a6a72;margin-bottom:24px}}
.scard{{display:block;border:1px solid #e3e6ea;border-radius:14px;margin-bottom:14px;background:#fff}}
.scard .b{{padding:16px 18px}}.scard h3{{font-family:'Fraunces',serif;font-size:20px;color:#1b1b20;margin:0 0 4px}}
.scard p{{color:#6a6a72;font-size:15px;margin:0}}
.foot{{border-top:1px solid #e3e6ea;margin-top:24px;padding-top:18px;color:#b4b8b4;font-size:13px}}</style>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Inter:wght@400;600&display=swap" rel="stylesheet">
</head><body><div class="wrap"><h1>Web Stories</h1>
<div class="sub">Tap through — Santa Cruz photography, guides, and drone tips.</div>
{cards}
<div class="foot">© 2026 Story Mode Guy · <a href="/">storymodeguy.com</a> · <a href="/learn/">Guides</a> · <a href="/blog/">Journal</a></div>
</div></body></html>"""
(OUT/"index.html").write_text(idx)
print("  wrote stories/index.html")

sm=ROOT/"sitemap.xml"
if sm.exists():
    s=sm.read_text();urls=[f"{SITE}/stories/"]+[f"{SITE}/stories/{st['slug']}.html" for st in STORIES]
    add="".join(f'  <url>\n    <loc>{u}</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.6</priority>\n  </url>\n\n' for u in urls if u not in s)
    if add: s=s.replace("</urlset>",add+"</urlset>",1);sm.write_text(s);print("  sitemap +%d"%add.count("<url>"))
print("done")
