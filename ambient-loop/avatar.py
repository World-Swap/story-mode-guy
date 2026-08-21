#!/usr/bin/env python3
"""Build channel avatars for The Open Lands (800x800).

YouTube crops to a circle and renders down to ~48px, so legibility at small
size drives every choice here: three ridge layers, not five; hard tonal steps
between them rather than blended fog; one dominant peak per layer so there is
a real silhouette to recognise.

An earlier version used five low-contrast layers with soft fog between them.
It looked fine at 800px and turned into an indistinct blob at 96px, which is
the size that actually matters.

Rendered at 4x and downsampled for clean edges.
"""
import math, os
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "avatars")
S = 800
SS = 4
N = S * SS

def lerp(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))

def sky(draw, top, bottom):
    for y in range(N):
        draw.line([(0, y), (N, y)], fill=lerp(top, bottom, y / N))

def ridge(draw, base, amp, phase, freq, colour):
    """One layer, dominated by a single low-frequency peak so it reads small."""
    pts = []
    for x in range(0, N + 1, max(1, N // 600)):
        u = x / N
        h = (math.sin(u * freq + phase)
             + math.sin(u * freq * 2.7 + phase * 1.9) * 0.22
             + math.sin(u * freq * 5.1 + phase * 3.3) * 0.08)
        pts.append((x, base * N - h * amp * N))
    pts += [(N, N), (0, N)]
    draw.polygon(pts, fill=colour)

def build(name, p):
    img = Image.new("RGB", (N, N), (0, 0, 0))
    d = ImageDraw.Draw(img)
    sky(d, p["sky_top"], p["sky_bottom"])

    if p.get("disc"):
        cx, cy, r = (p["disc"]["x"] * N, p["disc"]["y"] * N, p["disc"]["r"] * N)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=p["disc"]["colour"])

    for base, amp, phase, freq, colour in p["ridges"]:
        ridge(d, base, amp, phase, freq, colour)

    img = img.resize((S, S), Image.LANCZOS)
    img.save(os.path.join(OUT, f"avatar-{name}.png"))

    prev = img.copy().convert("RGBA")
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, S - 1, S - 1], fill=255)
    prev.putalpha(mask)
    prev.resize((96, 96), Image.LANCZOS).save(os.path.join(OUT, f"preview-{name}-96.png"))
    print(f"  avatar-{name}.png")

# base, amplitude, phase, frequency, colour - back layer first.
DAWN = {
    "sky_top": (226, 232, 226), "sky_bottom": (198, 210, 203),
    "disc": {"x": 0.60, "y": 0.34, "r": 0.085, "colour": (247, 238, 216)},
    "ridges": [
        (0.62, 0.10, 0.6, 3.0, (139, 160, 152)),
        (0.78, 0.11, 2.4, 2.4, (72, 100, 89)),
        (0.94, 0.10, 4.3, 2.0, (26, 44, 36)),
    ],
}
COOL = {
    "sky_top": (219, 228, 224), "sky_bottom": (176, 195, 190),
    "ridges": [
        (0.60, 0.11, 1.4, 2.7, (125, 150, 145)),
        (0.77, 0.11, 3.1, 2.2, (62, 92, 84)),
        (0.94, 0.10, 5.0, 1.8, (22, 40, 34)),
    ],
}
DUSK = {
    "sky_top": (188, 206, 209), "sky_bottom": (120, 148, 154),
    "disc": {"x": 0.36, "y": 0.30, "r": 0.070, "colour": (232, 240, 236)},
    "ridges": [
        (0.61, 0.10, 2.0, 2.9, (94, 124, 126)),
        (0.78, 0.11, 3.8, 2.3, (46, 76, 76)),
        (0.94, 0.10, 5.7, 1.9, (16, 34, 34)),
    ],
}

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print("Building avatars")
    for n, p in (("dawn", DAWN), ("cool", COOL), ("dusk", DUSK)):
        build(n, p)
