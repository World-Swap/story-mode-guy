#!/usr/bin/env python3
"""Rebuild the photo-driven parts of the site from photos/manifest.json.

Regenerates three regions, each wrapped in <!--PHOTOS:X--> ... <!--/PHOTOS:X-->
markers so this script can safely rewrite them without touching anything else:
  - index.html   Newest Captures slideshow  (NEWEST)  + counter total (COUNT)
  - index.html   Best-of showcase band      (BESTOF)  -> photos with "best": true
  - gallery.html Full gallery grid          (GRID)    -> every photo, newest first

Usage:  python3 photos/build.py
manifest.json is an array, NEWEST FIRST. Each item: {"n": 123, "cap": "...", "best": false}
The file for photo N is photo-N.jpg (full res) and thumb-photo-N.jpg (thumbnail).
"""
import json, re, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
MAN = json.loads((ROOT / "photos" / "manifest.json").read_text(encoding="utf-8"))
NEWEST_COUNT = 14   # how many of the newest photos appear in the homepage slideshow

A = lambda s: html.escape(s, quote=True)   # for attributes
T = lambda s: html.escape(s, quote=False)  # for visible text


def slides_html(items):
    rows = []
    for i, m in enumerate(items):
        n, cap = m["n"], m["cap"]
        active = " is-active" if i == 0 else ""
        lazy = "" if i == 0 else ' loading="lazy"'
        rows.append(f'        <figure class="slide{active}"><img src="photo-{n}.jpg" '
                    f'alt="{A(cap)}"{lazy}><figcaption>{T(cap)}</figcaption></figure>')
    return "\n" + "\n".join(rows) + "\n      "


def bestof_html(items):
    rows = []
    for m in items:
        n, cap = m["n"], m["cap"]
        rows.append(f'      <a class="scard" href="gallery.html" aria-label="{A(cap)}">\n'
                    f'        <img src="photo-{n}.jpg" alt="{A(cap)}" loading="lazy">\n'
                    f'        <span class="scap">{T(cap)}</span>\n'
                    f'      </a>')
    return "\n" + "\n".join(rows) + "\n    "


def grid_html(items):
    rows = []
    for m in items:
        n, cap = m["n"], m["cap"]
        rows.append(f'      <button class="gtile" data-full="photo-{n}.jpg" data-cap="{A(cap)}" aria-label="{A(cap)}">\n'
                    f'        <img src="thumb-photo-{n}.jpg" alt="{A(cap)}" loading="lazy">\n'
                    f'        <span class="gcap">{T(cap)}</span>\n'
                    f'      </button>')
    return "\n" + "\n".join(rows) + "\n  "


def replace_region(text, name, new_inner):
    pat = re.compile(r"(<!--PHOTOS:%s-->).*?(<!--/PHOTOS:%s-->)" % (name, name), re.S)
    if not pat.search(text):
        raise SystemExit(f"ERROR: marker PHOTOS:{name} not found")
    return pat.sub(lambda m: m.group(1) + new_inner + m.group(2), text)


newest = MAN[:NEWEST_COUNT]
best = [m for m in MAN if m.get("best")]

idx = (ROOT / "index.html").read_text(encoding="utf-8")
idx = replace_region(idx, "NEWEST", slides_html(newest))
idx = replace_region(idx, "COUNT", str(len(newest)))
idx = replace_region(idx, "BESTOF", bestof_html(best))
(ROOT / "index.html").write_text(idx, encoding="utf-8")

gal = (ROOT / "gallery.html").read_text(encoding="utf-8")
gal = replace_region(gal, "GRID", grid_html(MAN))
(ROOT / "gallery.html").write_text(gal, encoding="utf-8")

print(f"Rebuilt site: {len(MAN)} photos | newest {len(newest)} in slideshow | {len(best)} in best-of band")
