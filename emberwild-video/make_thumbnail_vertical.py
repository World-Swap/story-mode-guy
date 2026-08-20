#!/usr/bin/env python3
"""Build a 1080x1920 (9:16) cover from an episode frame, for Shorts / Reels / TikTok.

Same art, palette and fonts as make_thumbnail.py, but recomposed for vertical:
the source 16:9 frame cannot fill a 9:16 canvas without losing most of the width,
so the frame is placed as a centred band over a blurred, darkened fill of itself.
That keeps the whole composition intact — faces, two-shots and wide landscapes all
survive — instead of cropping to a narrow slice of the middle.
"""
import sys, pathlib
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FONTS = pathlib.Path("/mnt/skills/examples/canvas-design/canvas-fonts")
TITLE_F, SUB_F = FONTS / "Gloock-Regular.ttf", FONTS / "CrimsonPro-Italic.ttf"
GOLD, CREAM, INK = (242, 205, 132), (239, 228, 198), (20, 16, 13)
W, H = 1080, 1920


def backdrop(img):
    """Softly blurred cover-crop of the frame itself, so the margins carry the scene's colour."""
    sw, sh = img.size
    scale = max(W / sw, H / sh)
    b = img.resize((int(sw * scale), int(sh * scale)), Image.LANCZOS)
    left, top = (b.width - W) // 2, (b.height - H) // 2
    b = b.crop((left, top, left + W, top + H)).filter(ImageFilter.GaussianBlur(26))
    return Image.blend(b, Image.new("RGB", (W, H), INK), 0.38)


def outlined(d, xy, text, font, fill, ow=6):
    x, y = xy
    for dx in range(-ow, ow + 1, 2):
        for dy in range(-ow, ow + 1, 2):
            if dx or dy:
                d.text((x + dx, y + dy), text, font=font, fill=INK + (255,))
    d.text((x, y), text, font=font, fill=fill)


def centred(d, y, text, font, fill, ow=6):
    bb = d.textbbox((0, 0), text, font=font)
    outlined(d, ((W - (bb[2] - bb[0])) // 2 - bb[0], y), text, font, fill, ow)


def build(src, out, title="EMBERWILD", sub="EPISODE ONE", strap="THE BONDING"):
    img = Image.open(src).convert("RGB")
    canvas = backdrop(img)

    # The frame is widened past the canvas and cropped, so the art band is tall enough
    # to carry the poster rather than reading as a letterboxed strip. 1.28x keeps ~78%
    # of the original width, which two-shots survive.
    band_w = int(W * 1.28)
    band_h = int(band_w * img.height / img.width)
    band = img.resize((band_w, band_h), Image.LANCZOS)
    band = band.crop(((band_w - W) // 2, 0, (band_w - W) // 2 + W, band_h))
    band_y = int(H * 0.355) - band_h // 2
    canvas.paste(band, (0, band_y))

    d = ImageDraw.Draw(canvas, "RGBA")
    for i in range(60):                      # feather both band edges into the backdrop
        a = int(200 * (1 - i / 60))
        d.line([(0, band_y - 1 - i), (W, band_y - 1 - i)], fill=INK + (a,))
        d.line([(0, band_y + band_h + i), (W, band_y + band_h + i)], fill=INK + (a,))
    lo = band_y + band_h                     # scrim under the text block
    for i in range(H - lo):
        a = int(215 * min(1.0, (i / max(1, (H - lo) * 0.45))) ** 1.2)
        d.line([(0, lo + i), (W, lo + i)], fill=INK + (min(a, 215),))

    d = ImageDraw.Draw(canvas)
    ft = ImageFont.truetype(str(TITLE_F), 132)
    fk = ImageFont.truetype(str(TITLE_F), 62)
    fs = ImageFont.truetype(str(SUB_F), 52)

    y = int(H * 0.655)
    centred(d, y, sub, fs, CREAM + (235,), ow=4)
    centred(d, y + 96, title, ft, GOLD + (255,), ow=7)

    words, lines, cur = strap.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if len(trial) <= 18:
            cur = trial
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    ys = y + 96 + 168
    for line in lines:
        centred(d, ys, line, fk, CREAM + (255,), ow=5)
        ys += 82

    canvas.save(out, quality=92)
    return out


if __name__ == "__main__":
    print(build(*sys.argv[1:3]))
