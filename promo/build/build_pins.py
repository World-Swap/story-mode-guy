#!/usr/bin/env python3
"""Generate Pinterest pins (1000x1500) from the gallery photos + a bulk pins.csv."""
import re, csv, pathlib
from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter

ROOT = pathlib.Path("/home/user/story-mode-guy")
OUT = ROOT / "promo/pinterest/pins"; OUT.mkdir(parents=True, exist_ok=True)
W, H = 1000, 1500
FSER = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FSANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
LINK = "https://storymodeguy.com/#prints"

tiles = re.findall(r'data-full="(photo-\d+\.jpg)"[^>]*data-cap="([^"]+)"', (ROOT/"gallery.html").read_text())

def board(cap):
    c = cap.lower()
    if any(w in c for w in ["boardwalk","ferris","coaster","wharf","pier"]): return "Santa Cruz Boardwalk"
    if any(w in c for w in ["mushroom","agaric","redwood","forest","moss","creek","caves"]): return "Santa Cruz Nature"
    if any(w in c for w in ["sunset","dusk","golden","amber","purple","fire","glow","dawn","rose","pink","twilight","moon"]): return "Sunset Wallpapers"
    return "Santa Cruz Coast"

def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur+" "+w).strip()
        if draw.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def cover(im):
    im = ImageOps.exif_transpose(im).convert("RGB")
    s = max(W/im.width, H/im.height)
    im = im.resize((round(im.width*s), round(im.height*s)), Image.LANCZOS)
    l, t = (im.width-W)//2, (im.height-H)//2
    return im.crop((l, t, l+W, t+H))

logo = Image.open(ROOT/"smg-logo.png").convert("RGBA").resize((70,70))
rows = []
for f, cap in tiles:
    im = cover(Image.open(ROOT/f)).convert("RGBA")
    # bottom gradient for legibility
    grad = Image.new("L",(1,H),0)
    for y in range(H):
        v = 0 if y < H*0.62 else int(235*min(1,(y-H*0.62)/(H*0.38)))
        grad.putpixel((0,y),v)
    dark = Image.new("RGBA",(W,H),(8,10,14,255)); dark.putalpha(grad.resize((W,H)))
    im.alpha_composite(dark)
    d = ImageDraw.Draw(im)
    ft = ImageFont.truetype(FSER, 58); fb = ImageFont.truetype(FSANS, 26)
    lines = wrap(d, cap, ft, W-120)
    y = H - 150 - len(lines)*66
    for ln in lines:
        d.text((60, y), ln, font=ft, fill=(255,255,255)); y += 66
    # brand row
    im.alpha_composite(logo, (60, H-96))
    d.text((142, H-84), "STORY MODE GUY", font=fb, fill=(255,255,255))
    d.text((142, H-52), "prints & wallpapers · storymodeguy.com", font=ImageFont.truetype(FSANS,20), fill=(200,206,214))
    n = f.replace("photo-","").replace(".jpg","")
    out = OUT / f"pin-{n}.jpg"
    im.convert("RGB").save(out, "JPEG", quality=88, optimize=True)
    title = f"{cap} · Santa Cruz, California"
    desc = (f"{cap} — an original fine-art photograph of the Santa Cruz coast in California. "
            f"Available as a 4K desktop & phone wallpaper and a printable fine-art file at storymodeguy.com. "
            f"Coastal sunset photography, California beach prints, boardwalk & ocean wall art.")
    rows.append([out.name, title, desc, LINK, board(cap)])

with open(ROOT/"promo/pinterest/pins.csv","w",newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["Pin image","Title","Description","Destination link","Suggested board"])
    w.writerows(rows)

print(f"pins: {len(rows)}  -> {OUT}")
print("csv:", ROOT/"promo/pinterest/pins.csv")
