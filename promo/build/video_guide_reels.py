#!/usr/bin/env python3
"""Covers-only VIDEOGRAPHY guide promo reels + a collection reel. No interior pages shown.
Per guide: title -> cover -> 'what's inside' features -> CTA (xfade, 1080x1920, silent).
Mirrors guide_reels_v2.py but for the videography line (v01..v10).
Usage: python3 video_guide_reels.py [guide-id | all | collection]
"""
import sys, json, subprocess, pathlib, tempfile, fitz, imageio_ffmpeg
from PIL import Image, ImageOps, ImageFilter

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = pathlib.Path("/home/user/story-mode-guy")
GUIDES = ROOT / "guides"
BUILD = ROOT / "promo/build"
OUT = ROOT / "promo/reels/video-guides"; OUT.mkdir(parents=True, exist_ok=True)
M = json.loads((GUIDES / "manifest.json").read_text())
VIDEO = [g for g in M["guides"] if g.get("line") == "videography"]
W, H, FPS, XF = 1080, 1920, 30, 0.45

BULLETS = {
 "v01-cinematic-look": ["The 180° shutter rule","Frame rate & picture profiles","The cinematic depth look","An anti-'video-look' checklist"],
 "v02-phone-video": ["The settings that matter","Lock focus & exposure","Stabilize & hold it right","Fix the audio + right gear"],
 "v03-editing-blueprint": ["A repeatable edit order","Assembly → rough → fine cut","Cut on motion & pacing","Export for YouTube & Reels"],
 "v04-color-grading": ["Color-correct vs. grade","Read scopes with confidence","Log & LUTs, demystified","Match every shot in a scene"],
 "v05-audio-for-video": ["Why your built-in mic fails","Pick the right mic","Kill echo & set levels","Clean it up in post"],
 "v06-video-lighting": ["Soft vs. hard light","One-light setups that shine","Three-point lighting","Ready-to-copy scene setups"],
 "v07-broll-storytelling": ["Why b-roll saves every edit","Think in sequences","The 5-shot method","Tell a story without a script"],
 "v08-camera-movement": ["Fix shaky handheld","The core gimbal moves","Balance a gimbal right","Stabilize in post"],
 "v09-real-estate-video": ["Bright, sellable interiors","Smooth room-to-room moves","A fast delivery edit","What to charge & find clients"],
 "v10-video-cheat-sheet": ["Grab-and-go field cards","Frame rate & shutter table","Audio & export settings","A pre-shoot checklist"],
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

def make_cards(spec, cards):
    sp = pathlib.Path(tempfile.mktemp(suffix=".json")); sp.write_text(json.dumps(spec))
    subprocess.run(["python3", str(BUILD/"guide_cards.py"), str(sp), str(cards)],
                   env={"PATH":"/opt/node22/bin:/usr/bin:/bin","PLAYWRIGHT_BROWSERS_PATH":"/opt/pw-browsers"},
                   check=True, capture_output=True)

def build_guide(g):
    gid = g["id"]
    cards = OUT / f"{gid}-cards"
    spec = {"title": g["title"], "subtitle": g["subtitle"], "bullets": BULLETS[gid],
            "accent": g["accent"], "price": g["price"], "kicker": "Videography Guide"}
    make_cards(spec, cards)
    cov = cover_img(gid)
    cslide = pathlib.Path(tempfile.mktemp(suffix=".jpg"))
    cover_slide(cov, g["accent"], cards/"bar.png", cslide)
    out = OUT / f"reel-{gid}.mp4"
    xfade([cards/"title.png", cslide, cards/"features.png", cards/"cta.png"],
          [2.0, 2.6, 3.2, 2.8], out)
    print(f"  reel-{gid}.mp4")

def build_collection():
    cards = OUT / "collection-cards"
    spec = {"title": "The Videography\nGuide Library",
            "subtitle": "10 guides. From your first cinematic shot to a paid property tour.",
            "bullets": ["Cinematic settings & phone video","Editing, color & audio","Lighting & camera movement","B-roll & visual storytelling","Real estate video tours","Printable cheat-sheet pack"],
            "accent": "#6d28d9", "price": "10 guides · from $17", "kicker": "The Complete Library"}
    make_cards(spec, cards)
    slides = [cards/"title.png"]; durs = [2.2]
    for g in VIDEO:
        cov = cover_img(g["id"])
        cslide = pathlib.Path(tempfile.mktemp(suffix=".jpg"))
        cover_slide(cov, g["accent"], cards/"bar.png", cslide)
        slides.append(cslide); durs.append(1.35)
    slides += [cards/"features.png", cards/"cta.png"]; durs += [3.0, 2.8]
    out = OUT / "reel-v00-collection.mp4"
    xfade(slides, durs, out)
    print("  reel-v00-collection.mp4")

arg = sys.argv[1] if len(sys.argv) > 1 else "all"
if arg == "collection":
    build_collection()
else:
    gs = VIDEO if arg == "all" else [g for g in VIDEO if g["id"] == arg]
    for g in gs: build_guide(g)
    if arg == "all": build_collection()
print("done")
