#!/usr/bin/env python3
"""Build a branded vertical (1080x1920) promo reel MP4 — fast crossfade slideshow.

Usage:
  python3 make_reel.py <cards_dir> <out.mp4> <img1> <img2> ...
<cards_dir> must contain title.png, cta.png, bar.png (from cards.py).
"""
import sys, subprocess, pathlib, tempfile, imageio_ffmpeg
from PIL import Image, ImageOps, ImageFilter

FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H, FPS = 1080, 1920, 30
PHOTO_SEC, TITLE_SEC, CTA_SEC, XF = 2.3, 2.0, 2.8, 0.45

cards = pathlib.Path(sys.argv[1]).resolve()
out = pathlib.Path(sys.argv[2]).resolve()
imgs = [pathlib.Path(p).resolve() for p in sys.argv[3:]]
tmp = pathlib.Path(tempfile.mkdtemp())
bar = Image.open(cards / "bar.png").convert("RGBA")

def compose(src, dest):
    """1080x1920 still: darkened blurred cover bg + sharp contain-fit fg + brand bar burned in."""
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    sw, sh = im.size
    s = max(W/sw, H/sh)
    bg = im.resize((round(sw*s), round(sh*s)), Image.LANCZOS)
    l, t = (bg.width-W)//2, (bg.height-H)//2
    bg = bg.crop((l, t, l+W, t+H)).filter(ImageFilter.GaussianBlur(30))
    bg = Image.eval(bg, lambda p: int(p*0.45)).convert("RGBA")
    fw, fh = int(W*0.92), int(H*0.72)
    s2 = min(fw/sw, fh/sh)
    fg = im.resize((round(sw*s2), round(sh*s2)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.4, 60, 2))
    framed = Image.new("RGB", (fg.width+6, fg.height+6), (255,255,255))
    framed.paste(fg, (3,3))
    bg.paste(framed, ((W-framed.width)//2, (H-framed.height)//2))
    bg.alpha_composite(bar)                     # brand bar on top
    bg.convert("RGB").save(dest, "JPEG", quality=92)

# build the still deck: title, photos (composed), cta
stills = [(cards/"title.png", TITLE_SEC)]
for i, p in enumerate(imgs, 1):
    d = tmp / f"c{i:02d}.jpg"; compose(p, d); stills.append((d, PHOTO_SEC))
stills.append((cards/"cta.png", CTA_SEC))

# one ffmpeg pass: loop each still, chain xfades
inp = []
for path, dur in stills:
    inp += ["-loop", "1", "-t", f"{dur}", "-i", str(path)]

fc = []
for i in range(len(stills)):
    fc.append(f"[{i}:v]scale={W}:{H},fps={FPS},format=yuv420p,setsar=1[s{i}]")
# chain
cum = stills[0][1]
prev = "s0"
for i in range(1, len(stills)):
    off = cum - XF
    lab = f"x{i}" if i < len(stills)-1 else "vout"
    fc.append(f"[{prev}][s{i}]xfade=transition=fade:duration={XF}:offset={off:.3f}[{lab}]")
    cum += stills[i][1] - XF
    prev = lab

filtergraph = ";".join(fc)
out.parent.mkdir(parents=True, exist_ok=True)
cmd = [FF, "-y", "-hide_banner", "-loglevel", "error", *inp,
       "-filter_complex", filtergraph, "-map", "[vout]",
       "-c:v", "libx264", "-preset", "veryfast", "-crf", "21",
       "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)]
r = subprocess.run(cmd)
if r.returncode != 0:
    raise SystemExit("ffmpeg failed")
info = subprocess.run([FF, "-hide_banner", "-i", str(out)], capture_output=True, text=True).stderr
print(f"reel -> {out}")
for line in info.splitlines():
    if "Duration" in line or "Stream #0:0" in line:
        print("  " + line.strip())
