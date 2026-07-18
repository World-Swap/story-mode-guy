#!/usr/bin/env python3
"""Compile the big 'Complete Wallpaper Collection' from every high-res original on disk.
Landscapes -> Desktop 4K (3840x2160). Every photo -> Phone (1080x2340).
Outputs into promo/bigbundle/Desktop-4K/ and promo/bigbundle/Phone/.
"""
import pathlib, re, json
from PIL import Image, ImageOps, ImageFilter

ROOT = pathlib.Path("/home/user/story-mode-guy")
OUT = ROOT / "promo/bigbundle"
DESK = OUT / "Desktop-4K"; DESK.mkdir(parents=True, exist_ok=True)
PHONE = OUT / "Phone"; PHONE.mkdir(parents=True, exist_ok=True)

def cover(im, w, h):
    im = ImageOps.exif_transpose(im).convert("RGB")
    sw, sh = im.size
    s = max(w/sw, h/sh)
    nw, nh = round(sw*s), round(sh*s)
    im = im.resize((nw, nh), Image.LANCZOS)
    l, t = (nw-w)//2, (nh-h)//2
    return im.crop((l, t, l+w, t+h))

def finish(im):
    return im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=70, threshold=2))

origs = sorted(ROOT.glob("orig-*.jpg"), key=lambda p: int(re.search(r"(\d+)", p.name).group(1)))
di = pi = 0
manifest = {"desktop_4k": [], "phone": []}
for p in origs:
    im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")
    landscape = im.width >= im.height
    # phone version for every photo
    pi += 1
    pout = PHONE / f"smg-phone-{pi:02d}.jpg"
    finish(cover(im.copy(), 1080, 2340)).save(pout, "JPEG", quality=90, optimize=True)
    manifest["phone"].append(pout.name)
    # desktop 4k for landscapes only (portrait sources can't fill 16:9 without heavy loss)
    if landscape:
        di += 1
        dout = DESK / f"smg-desktop-4k-{di:02d}.jpg"
        finish(cover(im.copy(), 3840, 2160)).save(dout, "JPEG", quality=90, optimize=True)
        manifest["desktop_4k"].append(dout.name)

(OUT / "manifest.json").write_text(json.dumps(manifest, indent=2))
total = di + pi
print(f"source photos: {len(origs)}")
print(f"desktop 4K:    {di}")
print(f"phone:         {pi}")
print(f"TOTAL files:   {total}")
