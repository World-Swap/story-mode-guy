#!/usr/bin/env python3
"""Build per-photo branded reels (1080x1920, ~7.5s, silent) matching the example style:
blurred vertical fill + sharp centered photo band + slow pan, with a static text overlay.

Reads items.json: [{"n":53,"src":"photo-53.jpg","title":"...","kicker":"..."}, ...]
Uses overlays from <ovdir>/ov-<n>.png. Writes <outdir>/reel-<n>.mp4
"""
import sys, json, pathlib, subprocess, tempfile, imageio_ffmpeg
from PIL import Image, ImageOps, ImageFilter

FF = imageio_ffmpeg.get_ffmpeg_exe()
items = json.loads(pathlib.Path(sys.argv[1]).read_text())
OVDIR = pathlib.Path(sys.argv[2]).resolve()
OUT = pathlib.Path(sys.argv[3]).resolve(); OUT.mkdir(parents=True, exist_ok=True)
ROOT = pathlib.Path("/home/user/story-mode-guy")
tmp = pathlib.Path(tempfile.mkdtemp())
DUR = 7.5
BW, BH = 1210, 2150            # oversized canvas for pan headroom

def big_still(src, dest):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    s = max(BW/im.width, BH/im.height)
    bg = im.resize((round(im.width*s), round(im.height*s)), Image.LANCZOS)
    l, t = (bg.width-BW)//2, (bg.height-BH)//2
    bg = bg.crop((l, t, l+BW, t+BH)).filter(ImageFilter.GaussianBlur(30))
    bg = Image.eval(bg, lambda p: int(p*0.58))
    # sharp full-width band, centered
    fg = im.resize((BW, round(im.height*BW/im.width)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.4,55,2))
    if fg.height > int(BH*0.82):    # portrait source: fit by height instead
        fg = im.resize((round(im.width*BH*0.82/im.height), int(BH*0.82)), Image.LANCZOS)
    bg.paste(fg, ((BW-fg.width)//2, (BH-fg.height)//2))
    bg.save(dest, "JPEG", quality=92)

def run(cmd):
    r = subprocess.run([FF, "-y", "-hide_banner", "-loglevel", "error", *cmd])
    if r.returncode != 0:
        raise SystemExit("ffmpeg failed: " + " ".join(map(str, cmd)))

for idx, it in enumerate(items):
    n = it["n"]
    big = tmp / f"big-{n}.jpg"
    big_still(ROOT / it["src"], big)
    ov = OVDIR / f"ov-{n}.png"
    out = OUT / f"reel-{n}.mp4"
    # alternate pan direction so a scroll of reels feels varied
    if idx % 2 == 0:
        xexpr = f"-(w-1080)*(0.12+0.72*t/{DUR})"; yexpr = f"-(h-1920)*(0.12+0.72*t/{DUR})"
    else:
        xexpr = f"-(w-1080)*(0.85-0.72*t/{DUR})"; yexpr = f"-(h-1920)*(0.10+0.72*t/{DUR})"
    fc = (f"[1][0]overlay=x='{xexpr}':y='{yexpr}':shortest=1[bgm];"
          f"[bgm][2]overlay=0:0:shortest=1,fade=t=in:st=0:d=0.4,fade=t=out:st={DUR-0.5}:d=0.5,format=yuv420p[v]")
    run(["-loop","1","-t",str(DUR),"-i",str(big),
         "-f","lavfi","-i",f"color=black:s=1080x1920:r=30",
         "-loop","1","-t",str(DUR),"-i",str(ov),
         "-filter_complex",fc,"-map","[v]","-t",str(DUR),
         "-r","30","-c:v","libx264","-preset","veryfast","-crf","21",
         "-pix_fmt","yuv420p","-movflags","+faststart",str(out)])
    print(f"  reel-{n}.mp4")

print(f"done -> {OUT}  ({len(items)} reels)")
