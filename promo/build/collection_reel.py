#!/usr/bin/env python3
"""Branded promo reel for the Complete Wallpaper Collection.
title -> a few wallpaper previews (phone full-bleed + desktop framed) -> 'what's inside' -> CTA."""
import json, subprocess, pathlib, tempfile, imageio_ffmpeg
from PIL import Image, ImageOps, ImageFilter

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = pathlib.Path("/home/user/story-mode-guy")
BUILD = ROOT / "promo/build"
BB = ROOT / "promo/bigbundle"
OUT = ROOT / "promo/reels/guides"; OUT.mkdir(parents=True, exist_ok=True)
W, H, FPS, XF = 1080, 1920, 30, 0.45

def bar_overlay(base, bar_png):
    base.alpha_composite(Image.open(bar_png).convert("RGBA")); return base

def phone_slide(src, bar_png, dest):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    s = max(W/im.width, H/im.height)
    im = im.resize((round(im.width*s), round(im.height*s)), Image.LANCZOS)
    l, t = (im.width-W)//2, (im.height-H)//2
    im = im.crop((l, t, l+W, t+H)).convert("RGBA")
    bar_overlay(im, bar_png).convert("RGB").save(dest, "JPEG", quality=92)

def desktop_slide(src, bar_png, dest):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    s = max(W/im.width, H/im.height)
    bg = im.resize((round(im.width*s), round(im.height*s)), Image.LANCZOS)
    l, t = (bg.width-W)//2, (bg.height-H)//2
    bg = bg.crop((l, t, l+W, t+H)).filter(ImageFilter.GaussianBlur(34))
    bg = Image.eval(bg, lambda p: int(p*0.5)).convert("RGBA")
    fw = int(W*0.92); s2 = fw/im.width
    fg = im.resize((fw, round(im.height*s2)), Image.LANCZOS)
    framed = Image.new("RGB", (fg.width+8, fg.height+8), (255,255,255)); framed.paste(fg,(4,4))
    bg.paste(framed, ((W-framed.width)//2, (H-framed.height)//2 - 30))
    bar_overlay(bg, bar_png).convert("RGB").save(dest, "JPEG", quality=92)

def xfade(slides, durs, out):
    inp = []
    for p, d in zip(slides, durs):
        inp += ["-loop","1","-t",f"{d}","-i",str(p)]
    fc = [f"[{i}:v]scale={W}:{H},fps={FPS},format=yuv420p,setsar=1[s{i}]" for i in range(len(slides))]
    cum = durs[0]; prev = "s0"
    for i in range(1, len(slides)):
        off = cum - XF
        lab = f"x{i}" if i < len(slides)-1 else "vout"
        fc.append(f"[{prev}][s{i}]xfade=transition=fade:duration={XF}:offset={off:.3f}[{lab}]")
        cum += durs[i] - XF; prev = lab
    r = subprocess.run([FF,"-y","-hide_banner","-loglevel","error",*inp,
        "-filter_complex",";".join(fc),"-map","[vout]","-c:v","libx264","-preset","veryfast",
        "-crf","21","-pix_fmt","yuv420p","-movflags","+faststart",str(out)])
    if r.returncode: raise SystemExit("ffmpeg failed")

cards = OUT / "collection-wall-cards"
spec = {"title":"The Complete\\nWallpaper Collection","subtitle":"95 original Santa Cruz wallpapers, for every screen you own.",
        "bullets":["45 desktop wallpapers in 4K","50 phone wallpapers","Fiery sunsets & glassy dawns","The wharf, boardwalk & forest","Instant download, every screen"],
        "accent":"#0e7490","price":"$19","kicker":"95 Wallpapers",
        "cta_kicker":"Get the collection","cta_pill":"Instant download · Every screen"}
sp = pathlib.Path(tempfile.mktemp(suffix=".json")); sp.write_text(json.dumps(spec).replace("\\\\n","\\n"))
subprocess.run(["python3", str(BUILD/"guide_cards.py"), str(sp), str(cards)],
               env={"PATH":"/opt/node22/bin:/usr/bin:/bin","PLAYWRIGHT_BROWSERS_PATH":"/opt/pw-browsers"},
               check=True, capture_output=True)

# alternate phone (full-bleed) + desktop (framed) previews for variety
phones = ["smg-phone-05","smg-phone-20","smg-phone-35","smg-phone-45"]
desks  = ["smg-desktop-4k-08","smg-desktop-4k-22","smg-desktop-4k-38"]
slides = [cards/"title.png"]; durs = [2.2]
order = [("p",phones[0]),("d",desks[0]),("p",phones[1]),("d",desks[1]),("p",phones[2]),("d",desks[2]),("p",phones[3])]
for kind, name in order:
    dst = pathlib.Path(tempfile.mktemp(suffix=".jpg"))
    if kind == "p": phone_slide(BB/"Phone"/f"{name}.jpg", cards/"bar.png", dst)
    else: desktop_slide(BB/"Desktop-4K"/f"{name}.jpg", cards/"bar.png", dst)
    slides.append(dst); durs.append(1.5)
slides += [cards/"features.png", cards/"cta.png"]; durs += [3.0, 2.8]
out = OUT / "reel-00b-wallpaper-collection.mp4"
xfade(slides, durs, out)
print("  ", out)
