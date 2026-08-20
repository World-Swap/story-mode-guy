#!/usr/bin/env python3
"""Build a 1280x720 YouTube thumbnail from an episode frame.

Uses real episode art rather than a fresh generation, so the thumbnail is
guaranteed to match the video, and composites the wordmark in the series'
locked palette and fonts.
"""
import sys, pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONTS = pathlib.Path("/mnt/skills/examples/canvas-design/canvas-fonts")
TITLE_F, SUB_F = FONTS / "Gloock-Regular.ttf", FONTS / "CrimsonPro-Italic.ttf"
GOLD, CREAM, INK = (242, 205, 132), (239, 228, 198), (20, 16, 13)
W, H = 1280, 720


def scrim(img, side="bottom", depth=0.55, strength=210):
    """Dark gradient so text stays legible over busy art."""
    g = Image.new("L", (1, H) if side == "bottom" else (W, 1), 0)
    px = g.load()
    n = H if side == "bottom" else W
    for i in range(n):
        t = i / (n - 1)
        if side == "bottom":
            v = 0 if t < 1 - depth else (t - (1 - depth)) / depth
        else:
            v = max(0.0, 1 - t / depth)
        px[(0, i) if side == "bottom" else (i, 0)] = int(strength * (v ** 1.4))
    mask = g.resize((W, H))
    return Image.composite(Image.new("RGB", (W, H), INK), img, mask)


def outlined(d, xy, text, font, fill, ow=5):
    x, y = xy
    for dx in range(-ow, ow + 1, 2):
        for dy in range(-ow, ow + 1, 2):
            if dx or dy:
                d.text((x + dx, y + dy), text, font=font, fill=INK + (255,))
    d.text((x, y), text, font=font, fill=fill)


def build(src, out, title="EMBERWILD", sub="EPISODE ONE", strap="THE BONDING", side="bottom"):
    img = Image.open(src).convert("RGB")
    # cover-crop to 16:9 at 1280x720
    sw, sh = img.size
    scale = max(W / sw, H / sh)
    img = img.resize((int(sw * scale), int(sh * scale)), Image.LANCZOS)
    left, top = (img.width - W) // 2, (img.height - H) // 2
    img = img.crop((left, top, left + W, top + H))
    img = scrim(img, side=side)

    d = ImageDraw.Draw(img)
    ft = ImageFont.truetype(str(TITLE_F), 104)
    fs = ImageFont.truetype(str(SUB_F), 40)
    fk = ImageFont.truetype(str(TITLE_F), 52)

    tw = d.textbbox((0, 0), title, font=ft)
    x = (W - (tw[2] - tw[0])) // 2 - tw[0]
    outlined(d, (x, H - 232), title, ft, GOLD + (255,), ow=6)

    kw = d.textbbox((0, 0), strap, font=fk)
    xk = (W - (kw[2] - kw[0])) // 2 - kw[0]
    outlined(d, (xk, H - 124), strap, fk, CREAM + (255,), ow=4)

    sw2 = d.textbbox((0, 0), sub, font=fs)
    xs = (W - (sw2[2] - sw2[0])) // 2 - sw2[0]
    outlined(d, (xs, H - 300), sub, fs, CREAM + (235,), ow=3)

    img.save(out, quality=92)
    return out


if __name__ == "__main__":
    print(build(sys.argv[1], sys.argv[2]))
