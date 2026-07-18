#!/usr/bin/env python3
"""Build Desktop 4K and Phone wallpaper packs from the full-res originals."""
import pathlib
from PIL import Image, ImageOps, ImageFilter

ROOT = pathlib.Path("/home/user/story-mode-guy")
DESK = ROOT / "promo/wallpapers/desktop"; DESK.mkdir(parents=True, exist_ok=True)
PHONE = ROOT / "promo/wallpapers/phone"; PHONE.mkdir(parents=True, exist_ok=True)

def cover(im, w, h):
    """Scale to cover w x h then center-crop."""
    im = ImageOps.exif_transpose(im).convert("RGB")
    sw, sh = im.size
    scale = max(w / sw, h / sh)
    nw, nh = round(sw * scale), round(sh * scale)
    im = im.resize((nw, nh), Image.LANCZOS)
    left, top = (nw - w) // 2, (nh - h) // 2
    return im.crop((left, top, left + w, left * 0 + top + h))

def finish(im):
    return im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=70, threshold=2))

# ---- Desktop 4K (3840x2160) ----
desktop_ids = [54, 59, 60, 62, 64, 66, 68, 73, 75, 76, 77, 78]
for i, n in enumerate(desktop_ids, 1):
    src = ROOT / f"orig-{n}.jpg"
    out = DESK / f"smg-desktop-4k-{i:02d}.jpg"
    finish(cover(Image.open(src), 3840, 2160)).save(out, "JPEG", quality=90, optimize=True)
print(f"desktop: {len(desktop_ids)} files @ 3840x2160")

# ---- Phone (1080x2340) ----
phone_ids = [57, 58, 67, 70, 62, 64, 66, 78]   # 4 native portraits + 4 hero verticals
for i, n in enumerate(phone_ids, 1):
    src = ROOT / f"orig-{n}.jpg"
    out = PHONE / f"smg-phone-{i:02d}.jpg"
    finish(cover(Image.open(src), 1080, 2340)).save(out, "JPEG", quality=90, optimize=True)
print(f"phone: {len(phone_ids)} files @ 1080x2340")

# quick report
for d in (DESK, PHONE):
    for f in sorted(d.glob("*.jpg")):
        im = Image.open(f)
        print(f"  {f.name}: {im.size[0]}x{im.size[1]}  {round(f.stat().st_size/1024)}KB")
