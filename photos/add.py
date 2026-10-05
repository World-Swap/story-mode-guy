#!/usr/bin/env python3
"""Add new photos to the site in one step.

Each new photo gets the next number, is resized to full-res (1920px long edge)
+ a thumbnail (800px) at the repo root, added to the TOP of photos/manifest.json
(newest first), and then the site is rebuilt (slideshow, best-of band, gallery).

Usage:
  python3 photos/add.py "<image>" "Caption"  ["<image2>" "Caption2" ...]
  python3 photos/add.py --best "<image>" "Caption"   # also feature it in the Best-of band

Images may be any size/orientation (phone EXIF rotation is handled). After it
runs, commit the new photo-*.jpg / thumb-photo-*.jpg, photos/manifest.json,
index.html and gallery.html (or zip them up to drop into the repo).
"""
import sys, json, subprocess, pathlib
from PIL import Image, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
MANP = ROOT / "photos" / "manifest.json"


def fit(im, long_edge):
    w, h = im.size
    s = long_edge / max(w, h)
    return im.resize((round(w * s), round(h * s)), Image.LANCZOS) if s < 1 else im


def process(src, n):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    fit(im.copy(), 1920).save(ROOT / f"photo-{n}.jpg", "JPEG", quality=85, optimize=True, progressive=True)
    fit(im.copy(), 800).save(ROOT / f"thumb-photo-{n}.jpg", "JPEG", quality=82, optimize=True, progressive=True)


def main():
    args = sys.argv[1:]
    best = False
    if args and args[0] == "--best":
        best = True
        args = args[1:]
    if len(args) < 2 or len(args) % 2 != 0:
        raise SystemExit(__doc__)

    man = json.loads(MANP.read_text(encoding="utf-8"))
    nextn = max(m["n"] for m in man) + 1
    added = []
    for src, cap in zip(args[0::2], args[1::2]):
        n = nextn
        nextn += 1
        process(src, n)
        added.append({"n": n, "cap": cap, "best": best})
        print(f"  + photo-{n}.jpg   {cap}")

    # newest first: the just-added photos (highest number first), then the rest
    man = sorted(added, key=lambda m: m["n"], reverse=True) + man
    MANP.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"manifest now holds {len(man)} photos. Rebuilding site...")
    subprocess.run([sys.executable, str(ROOT / "photos" / "build.py")], check=True)


if __name__ == "__main__":
    main()
