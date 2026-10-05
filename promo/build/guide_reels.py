#!/usr/bin/env python3
"""Build a branded flip-through reel for each photography guide:
title card -> cover -> 3 interior pages -> CTA card. 1080x1920, silent.

Usage: python3 guide_reels.py [guide-id | all]
"""
import sys, json, subprocess, pathlib, fitz

ROOT = pathlib.Path("/home/user/story-mode-guy")
GUIDES = ROOT / "guides"
BUILD = ROOT / "promo/build"
OUT = ROOT / "promo/reels/guides"; OUT.mkdir(parents=True, exist_ok=True)
TMP = ROOT / "promo/reels/guide-frames"; TMP.mkdir(parents=True, exist_ok=True)
M = json.loads((GUIDES / "manifest.json").read_text())

def rasterize(pdf, pages, outdir):
    d = fitz.open(pdf)
    files = []
    for i, pno in enumerate(pages):
        pno = min(pno, d.page_count - 1)
        pix = d[pno].get_pixmap(matrix=fitz.Matrix(2.0, 2.0))
        f = outdir / f"pg{i:02d}.png"; pix.save(f); files.append(str(f))
    return files

def build(g):
    gid = g["id"]
    pdf = GUIDES / "pdf" / f"{gid}.pdf"
    n = fitz.open(pdf).page_count
    # cover (0) + three interior content pages spread through the guide (skip TOC pg 1)
    pages = [0, round(n*0.32), round(n*0.58), round(n*0.82)]
    frames = TMP / gid; frames.mkdir(exist_ok=True)
    imgs = rasterize(pdf, pages, frames)
    cards = OUT / f"{gid}-cards"
    subprocess.run(["python3", str(BUILD/"cards.py"),
                    g["title"], g["subtitle"], "Get the guide",
                    str(cards), g["accent"], "Photography Guides"],
                   env={"PATH":"/opt/node22/bin:/usr/bin:/bin","PLAYWRIGHT_BROWSERS_PATH":"/opt/pw-browsers"},
                   check=True, capture_output=True)
    out = OUT / f"reel-{gid}.mp4"
    subprocess.run(["python3", str(BUILD/"make_reel.py"), str(cards), str(out), *imgs], check=True)
    print(f"  reel-{gid}.mp4")

arg = sys.argv[1] if len(sys.argv) > 1 else "all"
gs = M["guides"] if arg == "all" else [g for g in M["guides"] if g["id"] == arg]
for g in gs:
    build(g)
print("done")
