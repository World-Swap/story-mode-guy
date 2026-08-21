#!/usr/bin/env python3
"""Build channel avatars for The Open Lands (800x800) from real video frames.

The avatar should look like the channel's footage, so these are frames from
the loop itself rather than a drawn mark - same grade, same palette, same
subject.

The constraint that still applies: YouTube crops to a circle and renders down
to ~48px. So the crops chosen here all have one simple high-contrast structure
(a fall of white water, layered fog ridges, a shaft of light) rather than an
even field of foliage, which turns to noise at small size. Each build also
writes a 96px circular preview so that is checkable rather than assumed.
"""
import os, subprocess
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter

HERE = os.getcwd()   # run from an edition directory
OUT = os.path.join(HERE, "avatars")
S = 800
SRC_H = 720          # source clips are 1280x720; a square crop is 720 wide

# name, clip, timestamp, crop x-offset (0..560; 280 is centred)
CANDIDATES = [
    ("valley-fog",   "15-valley-fog",       9,  280),
    ("valley-fog-b", "15-valley-fog",      13,  280),
    ("waterfall",    "05-mossy-waterfall",  8,  330),
    ("god-rays",     "09-god-rays-ferns",  11,  300),
    ("dew",          "14-dew-lichen",       7,  280),
    ("river",        "10-river-bend",       8,  280),
    ("cedars",       "01-cathedral-cedars", 3,  260),
]

def ffmpeg():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()

def vignette(img, strength=0.30):
    """Gentle corner falloff - pulls the eye to the middle of the circle."""
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).ellipse((-S * 0.18, -S * 0.18, S * 1.18, S * 1.18), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(S * 0.16))
    return Image.composite(img, ImageEnhance.Brightness(img).enhance(1 - strength), mask)

def build(name, clip, t, x):
    raw = os.path.join(OUT, f"_{name}.png")
    subprocess.run([ffmpeg(), "-y", "-ss", str(t),
                    "-i", os.path.join(HERE, "clips", clip + ".mp4"),
                    "-frames:v", "1", "-vf", f"crop={SRC_H}:{SRC_H}:{x}:0",
                    raw, "-loglevel", "error"], check=True)

    img = Image.open(raw).convert("RGB").resize((S, S), Image.LANCZOS)
    img = ImageEnhance.Color(img).enhance(1.10)
    img = ImageEnhance.Contrast(img).enhance(1.10)
    img = vignette(img)
    img.save(os.path.join(OUT, f"avatar-{name}.png"))
    os.remove(raw)

    prev = img.convert("RGBA")
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, S - 1, S - 1], fill=255)
    prev.putalpha(mask)
    prev.resize((96, 96), Image.LANCZOS).save(os.path.join(OUT, f"preview-{name}-96.png"))
    print(f"  avatar-{name}.png")

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print("Building avatars from video frames")
    for c in CANDIDATES:
        build(*c)
