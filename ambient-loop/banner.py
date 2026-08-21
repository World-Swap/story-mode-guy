#!/usr/bin/env python3
"""Build the YouTube channel banner (2048x1152) from a frame of the loop.

YouTube crops the banner differently per device from one uploaded image:

    2048 x 1152   what you upload; TVs show all of it
    2048 x  423   desktop
    1235 x  338   the "safe area" - all that is guaranteed visible everywhere

So every piece of text sits inside the centred 1235x338 band, and the frame is
chosen so its subject survives being cropped to a letterbox strip.

Writes the banner plus a proof image showing the three crops, so the safe area
is verified rather than assumed.
"""
import os, subprocess
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "banners")
W, H = 2048, 1152
SAFE_W, SAFE_H = 1235, 338
DESK_H = 423

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

TITLE = "THE OPEN LANDS"
SUBTITLE = "LONG NATURE AMBIENCE FOR YOUR TV"

# name, clip, timestamp
VARIANTS = [
    ("valley", "15-valley-fog", 9),
    ("godrays", "09-god-rays-ferns", 11),
    ("cedars", "01-cathedral-cedars", 12),
]

def grab(clip, t, dest):
    import imageio_ffmpeg
    subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-ss", str(t),
                    "-i", os.path.join(HERE, "clips", clip + ".mp4"),
                    "-frames:v", "1", "-q:v", "2", dest, "-loglevel", "error"], check=True)

def tracked(draw, xy, text, font, fill, sp):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + sp
    return x

def tracked_w(draw, text, font, sp):
    return sum(draw.textlength(c, font=font) + sp for c in text) - sp

def build(name, clip, t):
    raw = os.path.join(OUT, f"_{name}.jpg")
    grab(clip, t, raw)

    img = Image.open(raw).convert("RGB").resize((W, H), Image.LANCZOS)
    img = ImageEnhance.Color(img).enhance(1.08)
    img = ImageEnhance.Contrast(img).enhance(1.06)

    # Darken toward the centre band so the type reads on any frame.
    scrim = Image.new("L", (1, H), 0)
    for y in range(H):
        d = abs(y - H / 2) / (H / 2)          # 0 at centre, 1 at top/bottom
        scrim.putpixel((0, y), int(150 * (1 - d) ** 1.1))
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.putalpha(scrim.resize((W, H)))
    img = Image.alpha_composite(img.convert("RGBA"), layer)

    # Edge vignette - the parts only a TV will show.
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).ellipse((-W * 0.22, -H * 0.30, W * 1.22, H * 1.30), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(200))
    img = Image.composite(img, ImageEnhance.Brightness(img).enhance(0.55), mask)

    d = ImageDraw.Draw(img)
    title_f = ImageFont.truetype(SERIF, 84)
    sub_f = ImageFont.truetype(SANS, 25)

    tw = tracked_w(d, TITLE, title_f, 9.0)
    tx, ty = (W - tw) / 2, H / 2 - 78
    tracked(d, (tx + 2, ty + 3), TITLE, title_f, (0, 0, 0, 170), 9.0)
    tracked(d, (tx, ty), TITLE, title_f, (255, 255, 255, 246), 9.0)

    ry = ty + 116
    d.line([(tx, ry), (tx + tw, ry)], fill=(255, 255, 255, 110), width=2)

    sw = tracked_w(d, SUBTITLE, sub_f, 4.0)
    sx, sy = (W - sw) / 2, ry + 30
    tracked(d, (sx + 1, sy + 1), SUBTITLE, sub_f, (0, 0, 0, 150), 4.0)
    tracked(d, (sx, sy), SUBTITLE, sub_f, (232, 238, 234, 235), 4.0)

    img = img.convert("RGB")
    dest = os.path.join(OUT, f"banner-{name}.jpg")
    img.save(dest, quality=90, optimize=True)
    os.remove(raw)

    # Proof: the three crops YouTube actually shows.
    desk = img.crop((0, (H - DESK_H) // 2, W, (H + DESK_H) // 2))
    safe = img.crop(((W - SAFE_W) // 2, (H - SAFE_H) // 2,
                     (W + SAFE_W) // 2, (H + SAFE_H) // 2))
    pw = 1100
    parts = [img.resize((pw, int(pw * H / W)), Image.LANCZOS),
             desk.resize((pw, int(pw * DESK_H / W)), Image.LANCZOS),
             safe.resize((pw, int(pw * SAFE_H / SAFE_W)), Image.LANCZOS)]
    ph = sum(p.height for p in parts) + 40
    proof = Image.new("RGB", (pw, ph), (20, 20, 20))
    y = 0
    for p in parts:
        proof.paste(p, (0, y)); y += p.height + 20
    proof.save(os.path.join(OUT, f"proof-{name}.jpg"), quality=88)

    kb = os.path.getsize(dest) / 1024
    print(f"  banner-{name}.jpg  {kb:.0f} KB")
    if kb > 6000:
        print(f"    WARNING: over YouTube's 6 MB limit")

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print("Building banners")
    for v in VARIANTS:
        build(*v)
