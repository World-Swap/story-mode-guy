#!/usr/bin/env python3
"""Build YouTube thumbnails (1280x720) from frames of the loop.

Frame + minimal text: a real frame from the video, lightly graded, with a
letterspaced serif title and a duration line over a bottom scrim. Nothing is
claimed here that the video does not deliver - no resolution or audio badge.
"""
import os, subprocess
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "thumbnails")
W, H = 1280, 720

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

TITLE = "MISTY RAINFOREST"
SUBTITLE = "3 HOURS  ·  TV SCREENSAVER  ·  NO MUSIC"

# (output name, source clip, timestamp) - one frame per candidate composition.
VARIANTS = [
    ("a-god-rays", "09-god-rays-ferns", 11),
    ("b-cathedral", "01-cathedral-cedars", 12),
    ("c-valley-fog", "15-valley-fog", 9),
]

def grab(clip, t, dest):
    """Pull a single full-resolution frame out of a clip."""
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ff, "-y", "-ss", str(t), "-i", os.path.join(HERE, "clips", clip + ".mp4"),
                    "-frames:v", "1", "-q:v", "2", dest, "-loglevel", "error"], check=True)

def tracked(draw, xy, text, font, fill, spacing):
    """Draw text with manual letterspacing - PIL has no tracking control."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + spacing
    return x

def tracked_width(draw, text, font, spacing):
    return sum(draw.textlength(c, font=font) + spacing for c in text) - spacing

def vignette(img, strength=0.55):
    """Darken the corners so the centre reads first."""
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).ellipse((-W * 0.35, -H * 0.45, W * 1.35, H * 1.45), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(160))
    dark = ImageEnhance.Brightness(img).enhance(1 - strength)
    return Image.composite(img, dark, mask)

def scrim(img, frac=0.52, peak=205):
    """Bottom-up black gradient so the type always has contrast under it."""
    grad = Image.new("L", (1, H), 0)
    top = int(H * (1 - frac))
    for y in range(top, H):
        grad.putpixel((0, y), int(peak * ((y - top) / (H - top)) ** 1.5))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.putalpha(grad.resize((W, H)))
    return Image.alpha_composite(img.convert("RGBA"), layer)

def build(name, clip, t):
    raw = os.path.join(OUT, f"_frame-{name}.jpg")
    grab(clip, t, raw)

    img = Image.open(raw).convert("RGB").resize((W, H), Image.LANCZOS)
    img = ImageEnhance.Color(img).enhance(1.10)
    img = ImageEnhance.Contrast(img).enhance(1.07)
    img = vignette(img)
    img = scrim(img)

    d = ImageDraw.Draw(img)
    title_f = ImageFont.truetype(SERIF, 66)
    sub_f = ImageFont.truetype(SANS, 23)

    x0, y_title = 74, 476
    # Soft shadow under the title, then the title itself.
    tracked(d, (x0 + 2, y_title + 3), TITLE, title_f, (0, 0, 0, 160), 5.5)
    end_x = tracked(d, (x0, y_title), TITLE, title_f, (255, 255, 255, 242), 5.5)

    rule_y = y_title + 92
    d.line([(x0, rule_y), (end_x - 5.5, rule_y)], fill=(255, 255, 255, 105), width=2)

    tracked(d, (x0 + 1, rule_y + 25), SUBTITLE, sub_f, (0, 0, 0, 150), 2.4)
    tracked(d, (x0, rule_y + 24), SUBTITLE, sub_f, (236, 240, 238, 232), 2.4)

    dest = os.path.join(OUT, f"thumbnail-{name}.jpg")
    img.convert("RGB").save(dest, quality=92, optimize=True)
    os.remove(raw)
    print(f"  {os.path.basename(dest)}  {os.path.getsize(dest)/1024:.0f} KB")
    return dest

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print("Building thumbnails")
    for v in VARIANTS:
        build(*v)
