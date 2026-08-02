#!/usr/bin/env python3
"""Static SEO blog generator for storymodeguy.com.
Reads blog-src/manifest.json + blog-src/<slug>.html (body fragments),
writes blog/<slug>.html (full SEO pages) + blog/index.html, and injects
the blog URLs into sitemap.xml. On-brand, self-contained, additive to the site.
"""
import json, pathlib, html, re

ROOT = pathlib.Path("/home/user/story-mode-guy")
SRC = ROOT / "blog-src"
OUT = ROOT / "blog"; OUT.mkdir(exist_ok=True)
M = json.loads((SRC / "manifest.json").read_text())

CSS = """
.freebar{display:flex;align-items:center;justify-content:center;gap:8px;flex-wrap:wrap;background:#0b7a6f;color:#fff;padding:9px 16px;font-size:14px;font-weight:500;text-align:center;line-height:1.4}
.freebar:hover{text-decoration:none;filter:brightness(1.06)}
.freebar strong{font-weight:700}
.freebar .get{text-decoration:underline;white-space:nowrap}

:root{--paper:#fff;--parch:#fefffc;--linen:#f9faf7;--ink:#1b1b20;--char:#3a3a40;--ash:#6a6a72;
--fog:#b4b8b4;--mist:#e3e6ea;--blue:#41a1cf;--serif:'Fraunces',Georgia,serif;--sans:'Inter',system-ui,sans-serif}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--sans);color:var(--char);background:var(--parch);line-height:1.7;font-size:17px;-webkit-font-smoothing:antialiased}
a{color:var(--blue);text-decoration:none}a:hover{text-decoration:underline}
.nav{position:sticky;top:0;z-index:10;display:flex;align-items:center;gap:14px;justify-content:center;
background:rgba(255,255,255,.86);backdrop-filter:blur(12px);border-bottom:1px solid var(--mist);padding:12px 16px}
.nav .brand{display:flex;align-items:center;gap:9px;font-family:var(--serif);font-size:17px;color:var(--ink)}
.nav .brand img{width:30px;height:30px;border-radius:50%}
.nav .sp{flex:1}
.nav .lnk{font-size:14px;font-weight:500;color:var(--char)}
.wrap{max-width:720px;margin:0 auto;padding:44px 22px 30px}
.eyebrow{font-size:12px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--blue);margin-bottom:12px}
h1{font-family:var(--serif);font-weight:600;font-size:clamp(30px,5vw,46px);line-height:1.1;letter-spacing:-.02em;color:var(--ink);margin-bottom:12px}
.meta{font-size:14px;color:var(--ash);margin-bottom:26px}
.hero{width:100%;border-radius:14px;border:1px solid var(--mist);margin:8px 0 30px;aspect-ratio:16/9;object-fit:cover}
article h2{font-family:var(--serif);font-weight:600;font-size:27px;color:var(--ink);margin:34px 0 10px}
article h3{font-size:19px;font-weight:600;color:var(--ink);margin:24px 0 6px}
article p{margin:0 0 16px}
article ul,article ol{margin:0 0 18px;padding-left:22px}article li{margin:6px 0}
article strong{color:var(--ink)}
.cta{background:linear-gradient(135deg,var(--blue),#0081c0);color:#fff;border-radius:14px;padding:22px 24px;margin:30px 0;text-align:center}
.cta h3{color:#fff;font-family:var(--serif);font-weight:600;font-size:23px;margin-bottom:6px}
.cta p{color:rgba(255,255,255,.92);margin-bottom:14px;font-size:15px}
.cta a.btn{display:inline-block;background:#fff;color:#0b5675;font-weight:600;padding:11px 22px;border-radius:40px;font-size:15px}
.cta a.btn:hover{text-decoration:none;filter:brightness(.97)}
.related{border-top:1px solid var(--mist);margin-top:36px;padding-top:22px}
.related h4{font-size:13px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;color:var(--ash);margin-bottom:10px}
.related a{display:block;padding:5px 0}
.foot{border-top:1px solid var(--mist);margin-top:30px;padding:26px 22px;text-align:center;font-size:13px;color:var(--fog);max-width:720px;margin-left:auto;margin-right:auto}
.foot a{color:var(--ash)}
/* index */
.cards{display:grid;gap:18px;margin-top:8px}
.pcard{display:block;border:1px solid var(--mist);border-radius:14px;overflow:hidden;background:#fff;transition:transform .15s}
.pcard:hover{transform:translateY(-2px);text-decoration:none}
.pcard img{width:100%;aspect-ratio:16/9;object-fit:cover}
.pcard .b{padding:16px 18px}
.pcard h2{font-family:var(--serif);font-size:22px;color:var(--ink);margin:0 0 6px}
.pcard p{color:var(--ash);font-size:15px;margin:0}
"""

NAV = """<div class="nav">
  <a class="brand" href="/"><img src="/smg-logo.png" alt="Story Mode Guy">Story Mode Guy</a>
  <span class="sp"></span>
  <a class="lnk" href="/#prints">Prints</a><a class="lnk" href="/#guides">Guides</a><a class="lnk" href="/gallery.html">Gallery</a>
</div>"""

FOOT = """<div class="foot">© 2026 Story Mode Guy · <a href="/">storymodeguy.com</a> ·
<a href="/blog/">Journal</a> · <a href="/privacy.html">Privacy</a></div>"""

FREEBAR = '<a class="freebar" href="https://payhip.com/b/aUu78" target="_blank" rel="noopener">🎁 <span><strong>Free:</strong> The Field Cheat Sheet — photography, video &amp; drone quick-reference.</span> <span class="get">Grab it free →</span></a>'

def page(a, related):
    body = (SRC / f"{a['slug']}.html").read_text()
    ld = {
        "@context":"https://schema.org","@type":"Article",
        "headline":a["title"],"description":a["description"],
        "image":f"https://storymodeguy.com/{a['hero']}",
        "datePublished":a["date"],"dateModified":a["date"],
        "author":{"@type":"Organization","name":"Story Mode Guy","@id":"https://storymodeguy.com/#org"},
        "publisher":{"@id":"https://storymodeguy.com/#org"},
        "mainEntityOfPage":f"https://storymodeguy.com/blog/{a['slug']}.html"
    }
    rel = "".join(f'<a href="/blog/{r["slug"]}.html">{html.escape(r["title"])}</a>' for r in related)
    return f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(a['title'])} — Story Mode Guy</title>
<meta name="description" content="{html.escape(a['description'])}">
<meta name="keywords" content="{html.escape(a['keywords'])}">
<link rel="canonical" href="https://storymodeguy.com/blog/{a['slug']}.html">
<link rel="icon" type="image/png" href="/smg-logo.png">
<link rel="alternate" type="application/rss+xml" title="Story Mode Guy — Journal" href="/blog/feed.xml">
<meta property="og:type" content="article"><meta property="og:title" content="{html.escape(a['title'])}">
<meta property="og:description" content="{html.escape(a['description'])}">
<meta property="og:url" content="https://storymodeguy.com/blog/{a['slug']}.html">
<meta property="og:image" content="https://storymodeguy.com/{a['hero']}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld)}</script>
</head><body>
{NAV}
{FREEBAR}
<main class="wrap">
<div class="eyebrow">Journal</div>
<h1>{html.escape(a['title'])}</h1>
<div class="meta">Story Mode Guy · {a['date_h']}</div>
<img class="hero" src="/{a['hero']}" alt="{html.escape(a['hero_alt'])}">
<article>{body}</article>
<div class="related"><h4>More from the journal</h4>{rel}</div>
</main>
{FOOT}
</body></html>"""

# write article pages
arts = M["articles"]
for a in arts:
    related = [x for x in arts if x["slug"] != a["slug"]][:3]
    (OUT / f"{a['slug']}.html").write_text(page(a, related))
    print("  wrote blog/"+a["slug"]+".html")

# index
cards = "".join(
    f'<a class="pcard" href="/blog/{a["slug"]}.html"><img src="/{a["hero"]}" alt="{html.escape(a["hero_alt"])}">'
    f'<div class="b"><h2>{html.escape(a["title"])}</h2><p>{html.escape(a["description"])}</p></div></a>'
    for a in arts)
idx = f"""<!DOCTYPE html><html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Journal — Story Mode Guy</title>
<meta name="description" content="Photography stories, tips, and guides from the Santa Cruz coast — Story Mode Guy.">
<link rel="canonical" href="https://storymodeguy.com/blog/">
<link rel="icon" type="image/png" href="/smg-logo.png">
<meta property="og:title" content="Journal — Story Mode Guy"><meta property="og:type" content="website">
<link rel="alternate" type="application/rss+xml" title="Story Mode Guy — Journal" href="/blog/feed.xml">
<meta property="og:image" content="https://storymodeguy.com/og-image.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
{NAV}
{FREEBAR}
<main class="wrap"><div class="eyebrow">The Journal</div>
<h1>Stories, tips & guides from the coast</h1>
<div class="meta">Photography from Santa Cruz — and how it's made.</div>
<div class="cards">{cards}</div></main>
{FOOT}</body></html>"""
(OUT / "index.html").write_text(idx)
print("  wrote blog/index.html")

# RSS 2.0 feed
import datetime as _dt
def _rfc822(d):
    try: return _dt.datetime.strptime(d, "%Y-%m-%d").strftime("%a, %d %b %Y 08:00:00 GMT")
    except Exception: return d
items = "".join(
    f"""  <item>
    <title>{html.escape(a['title'])}</title>
    <link>https://storymodeguy.com/blog/{a['slug']}.html</link>
    <guid>https://storymodeguy.com/blog/{a['slug']}.html</guid>
    <pubDate>{_rfc822(a['date'])}</pubDate>
    <description>{html.escape(a['description'])}</description>
  </item>
""" for a in arts)
feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>Story Mode Guy — Journal</title>
  <link>https://storymodeguy.com/blog/</link>
  <atom:link href="https://storymodeguy.com/blog/feed.xml" rel="self" type="application/rss+xml"/>
  <description>Photography, video &amp; drone stories, tips, and guides from the Santa Cruz coast.</description>
  <language>en-us</language>
{items}</channel>
</rss>
"""
(OUT / "feed.xml").write_text(feed)
print("  wrote blog/feed.xml")

# sitemap injection
sm = ROOT / "sitemap.xml"
if sm.exists():
    s = sm.read_text()
    urls = ["https://storymodeguy.com/blog/"] + [f"https://storymodeguy.com/blog/{a['slug']}.html" for a in arts]
    add = ""
    for u in urls:
        if u not in s:
            add += f'  <url>\n    <loc>{u}</loc>\n    <lastmod>{M["articles"][0]["date"]}</lastmod>\n    <changefreq>monthly</changefreq>\n    <priority>0.7</priority>\n  </url>\n\n'
    if add:
        s = s.replace("</urlset>", add + "</urlset>", 1)
        sm.write_text(s); print("  sitemap updated (+%d urls)" % add.count("<url>"))
print(f"blog: {len(arts)} articles")
