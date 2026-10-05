#!/usr/bin/env python3
"""Covers-only guide promo reels + a collection reel. No interior pages shown.
Per guide: title -> cover -> 'what's inside' features -> CTA (xfade, 1080x1920, silent).
Usage: python3 guide_reels_v2.py [guide-id | all | collection]
"""
import sys, json, subprocess, pathlib, tempfile, fitz, imageio_ffmpeg
from PIL import Image, ImageOps, ImageFilter

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = pathlib.Path("/home/user/story-mode-guy")
GUIDES = ROOT / "guides"
BUILD = ROOT / "promo/build"
OUT = ROOT / "promo/reels/guides"; OUT.mkdir(parents=True, exist_ok=True)
M = json.loads((GUIDES / "manifest.json").read_text())
W, H, FPS, XF = 1080, 1920, 30, 0.45

BULLETS = {
 "01-iphone-photography": ["Your 3 lenses, demystified","Nail exposure & focus every time","A full mobile-editing walkthrough","A 30-day photo challenge"],
 "02-lightroom-blueprint": ["A repeatable editing order","Color that pops — not fake","Build & save your own presets","Batch a whole shoot in minutes"],
 "03-product-photography": ["A $30 home-studio setup","Marketplace-ready white shots","Styled shots that actually sell","A reusable per-product shot list"],
 "04-exposure-manual-mode": ["The exposure triangle, made simple","Meter & histogram, decoded","12 real-world settings recipes","Get off Auto in a weekend"],
 "05-why-blurry": ["The 3 kinds of blur","Fix focus, shake & motion","Back-button focus setup","A 60-second field diagnostic"],
 "06-real-estate-photography": ["Bright, sellable interiors","Window + flash + HDR blending","Room-by-room shot checklist","Pricing & finding first clients"],
 "07-natural-light-portraits": ["Find & shape natural light","A full posing library","Flattering lenses & settings","A smooth 20-minute session flow"],
 "08-astrophotography": ["The gear you actually need","Plan the Milky Way","Focus on stars in the dark","Settings + editing recipes"],
 "09-low-light-night": ["Sharp handheld shots after dark","Tame noise the right way","City lights & light trails","6 night-scene settings"],
 "10-cheat-sheet-pack": ["Grab-and-go field cards","Every scene's settings","Exposure, WB, AF & composition","A troubleshooting flowchart"],
}

def cover_img(gid):
    d = fitz.open(GUIDES / "pdf" / f"{gid}.pdf")
    pix = d[0].get_pixmap(matrix=fitz.Matrix(2.4, 2.4))
    p = pathlib.Path(tempfile.mktemp(suffix=".png")); pix.save(p); return p

def cover_slide(cover_png, accent, bar_png, dest):
    im = Image.open(cover_png).convert("RGB")
    s = max(W/im.width, H/im.height)
    bg = im.resize((round(im.width*s), round(im.height*s)), Image.LANCZOS)
    l, t = (bg.width-W)//2, (bg.height-H)//2
    bg = bg.crop((l, t, l+W, t+H)).filter(ImageFilter.GaussianBlur(34))
    bg = Image.eval(bg, lambda p: int(p*0.5)).convert("RGBA")
    fw, fh = int(W*0.66), int(H*0.72)
    s2 = min(fw/im.width, fh/im.height)
    fg = im.resize((round(im.width*s2), round(im.height*s2)), Image.LANCZOS)
    framed = Image.new("RGB", (fg.width+8, fg.height+8), (255,255,255))
    framed.paste(fg, (4,4))
    bg.paste(framed, ((W-framed.width)//2, (H-framed.height)//2 - 40))
    bg.alpha_composite(Image.open(bar_png).convert("RGBA"))
    bg.convert("RGB").save(dest, "JPEG", quality=92)

def xfade(slides, durs, out):
    tmp = pathlib.Path(tempfile.mkdtemp())
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

def build_guide(g):
    gid = g["id"]
    cards = OUT / f"{gid}-cards"
    spec = {"title": g["title"], "subtitle": g["subtitle"], "bullets": BULLETS[gid],
            "accent": g["accent"], "price": g["price"], "kicker": "Photography Guide"}
    sp = pathlib.Path(tempfile.mktemp(suffix=".json")); sp.write_text(json.dumps(spec))
    subprocess.run(["python3", str(BUILD/"guide_cards.py"), str(sp), str(cards)],
                   env={"PATH":"/opt/node22/bin:/usr/bin:/bin","PLAYWRIGHT_BROWSERS_PATH":"/opt/pw-browsers"},
                   check=True, capture_output=True)
    cov = cover_img(gid)
    cslide = pathlib.Path(tempfile.mktemp(suffix=".jpg"))
    cover_slide(cov, g["accent"], cards/"bar.png", cslide)
    out = OUT / f"reel-{gid}.mp4"
    xfade([cards/"title.png", cslide, cards/"features.png", cards/"cta.png"],
          [2.0, 2.6, 3.2, 2.8], out)
    print(f"  reel-{gid}.mp4")

def build_collection():
    cards = OUT / "collection-cards"
    spec = {"title": "The Photography\\nGuide Library", "subtitle": "10 guides. From your first manual shot to selling your work.",
            "bullets": ["iPhone & smartphone","Lightroom editing","Exposure & manual mode","Portraits, product & real estate","Astro, low-light & more","Printable cheat-sheet pack"],
            "accent": "#1d4ed8", "price": "10 guides · from $17", "kicker": "The Complete Library"}
    sp = pathlib.Path(tempfile.mktemp(suffix=".json")); sp.write_text(json.dumps(spec).replace("\\\\n","\\n"))
    subprocess.run(["python3", str(BUILD/"guide_cards.py"), str(sp), str(cards)],
                   env={"PATH":"/opt/node22/bin:/usr/bin:/bin","PLAYWRIGHT_BROWSERS_PATH":"/opt/pw-browsers"},
                   check=True, capture_output=True)
    slides = [cards/"title.png"]; durs = [2.2]
    for g in M["guides"]:
        cov = cover_img(g["id"])
        cslide = pathlib.Path(tempfile.mktemp(suffix=".jpg"))
        cover_slide(cov, g["accent"], cards/"bar.png", cslide)
        slides.append(cslide); durs.append(1.35)
    slides += [cards/"features.png", cards/"cta.png"]; durs += [3.0, 2.8]
    out = OUT / "reel-00-collection.mp4"
    xfade(slides, durs, out)
    print("  reel-00-collection.mp4")

arg = sys.argv[1] if len(sys.argv) > 1 else "all"
if arg == "collection":
    build_collection()
else:
    gs = M["guides"] if arg == "all" else [g for g in M["guides"] if g["id"] == arg]
    for g in gs: build_guide(g)
    if arg == "all": build_collection()
print("done")
