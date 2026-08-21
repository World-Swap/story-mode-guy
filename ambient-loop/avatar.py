#!/usr/bin/env python3
"""Build channel avatars for The Open Lands (800x800).

YouTube crops the avatar to a circle and renders it as small as ~48px, so
these are flat vector-style marks, not photographs: layered ridgelines in fog,
which is both the channel's subject and a shape that survives being tiny.

Rendered at 4x and downsampled so the edges stay clean.
"""
import math, os
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "avatars")
S = 800
SS = 4                      # supersampling factor
N = S * SS

def lerp(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))

def sky(draw, top, bottom):
    """Vertical gradient background."""
    for y in range(N):
        draw.line([(0, y), (N, y)], fill=lerp(top, bottom, y / N))

def ridge(draw, base, amp, seed, colour):
    """One mountain layer, as a filled polygon under a summed-sine skyline."""
    pts = []
    for x in range(0, N + 1, max(1, N // 400)):
        u = x / N
        h = (math.sin(u * 6.0 + seed) * 0.55
             + math.sin(u * 13.0 + seed * 2.1) * 0.28
             + math.sin(u * 23.0 + seed * 3.7) * 0.17)
        pts.append((x, base * N + h * amp * N))
    pts += [(N, N), (0, N)]
    draw.polygon(pts, fill=colour)

def fog_band(img, y, height, strength):
    """Soft horizontal mist sitting on top of a ridge."""
    band = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    d = ImageDraw.Draw(band)
    d.rectangle([0, y * N, N, y * N + height * N], fill=(226, 235, 231, strength))
    band = band.filter(ImageFilter.GaussianBlur(N * 0.035))
    return Image.alpha_composite(img, band)

def build(name, palette, sun=None):
    img = Image.new("RGBA", (N, N), (0, 0, 0, 255))
    d = ImageDraw.Draw(img)
    sky(d, palette["sky_top"], palette["sky_bottom"])

    if sun:
        glow = Image.new("RGBA", (N, N), (0, 0, 0, 0))
        g = ImageDraw.Draw(glow)
        cx, cy, r = sun["x"] * N, sun["y"] * N, sun["r"] * N
        g.ellipse([cx - r, cy - r, cx + r, cy + r], fill=sun["colour"])
        glow = glow.filter(ImageFilter.GaussianBlur(N * 0.05))
        img = Image.alpha_composite(img, glow)
        d = ImageDraw.Draw(img)

    # Back to front: each ridge darker and lower, which reads as depth.
    for i, (base, amp, seed, colour) in enumerate(palette["ridges"]):
        ridge(d, base, amp, seed, colour)
        if i < len(palette["ridges"]) - 1:
            img = fog_band(img, base - 0.02, 0.10, palette["fog"])
            d = ImageDraw.Draw(img)

    img = img.resize((S, S), Image.LANCZOS).convert("RGB")
    dest = os.path.join(OUT, f"avatar-{name}.png")
    img.save(dest)

    # Circle-cropped preview at real display size, to check it survives small.
    prev = img.copy()
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, S, S], fill=255)
    prev.putalpha(mask)
    prev.resize((96, 96), Image.LANCZOS).save(os.path.join(OUT, f"preview-{name}-96.png"))
    print(f"  avatar-{name}.png")
    return dest

COOL = {
    "sky_top": (206, 220, 216), "sky_bottom": (150, 172, 168), "fog": 120,
    "ridges": [
        (0.44, 0.05, 0.4, (122, 143, 138)),
        (0.56, 0.05, 2.2, (86, 110, 102)),
        (0.68, 0.05, 4.1, (55, 79, 68)),
        (0.80, 0.05, 6.3, (32, 51, 43)),
        (0.92, 0.04, 8.0, (18, 32, 27)),
    ],
}
WARM = {
    "sky_top": (233, 226, 205), "sky_bottom": (188, 196, 180), "fog": 130,
    "ridges": [
        (0.46, 0.05, 1.1, (140, 152, 132)),
        (0.58, 0.05, 3.0, (99, 118, 97)),
        (0.70, 0.05, 5.2, (62, 84, 64)),
        (0.82, 0.05, 7.4, (36, 55, 40)),
        (0.93, 0.04, 9.1, (20, 34, 25)),
    ],
}
DEEP = {
    "sky_top": (176, 198, 199), "sky_bottom": (96, 126, 130), "fog": 105,
    "ridges": [
        (0.42, 0.06, 0.9, (96, 122, 124)),
        (0.55, 0.06, 2.7, (64, 92, 92)),
        (0.68, 0.05, 4.9, (39, 64, 62)),
        (0.81, 0.05, 7.1, (22, 42, 40)),
        (0.93, 0.04, 9.6, (12, 26, 25)),
    ],
}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print("Building avatars")
    build("cool", COOL)
    build("warm", WARM, sun={"x": 0.62, "y": 0.30, "r": 0.10,
                             "colour": (255, 243, 214, 190)})
    build("deep", DEEP)
