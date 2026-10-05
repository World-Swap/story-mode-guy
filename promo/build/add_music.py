#!/usr/bin/env python3
"""Batch-add music to every reel (rotating tracks), with fades. Silent reels -> reels with sound.
Outputs mirror the source structure under promo/reels-music/. Writes a track-map.csv."""
import subprocess, pathlib, csv, imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = pathlib.Path("/home/user/story-mode-guy")
REELS = ROOT / "promo/reels"
MUSIC = sorted((ROOT/"promo/music").glob("track-*.mp3"), key=lambda p: int(p.stem.split("-")[1]))
OUT = ROOT / "promo/reels-music"; OUT.mkdir(parents=True, exist_ok=True)
VOL = 0.9

def dur(p):
    r = subprocess.run([FF,"-hide_banner","-i",str(p)], capture_output=True, text=True).stderr
    for line in r.splitlines():
        if "Duration" in line:
            t = line.split("Duration:")[1].split(",")[0].strip()
            h,m,s = t.split(":"); return int(h)*3600+int(m)*60+float(s)
    return 0

# collect all reels (photo/, guides/, and the two pack reels at reels/ root)
reels = sorted((REELS/"photo").glob("reel-*.mp4")) \
      + sorted((REELS/"guides").glob("reel-*.mp4")) \
      + sorted(REELS.glob("smg-*-reel.mp4"))

rows = []
for i, reel in enumerate(reels):
    track = MUSIC[i % len(MUSIC)]
    d = dur(reel)
    fo = max(0, d-0.7)
    rel = reel.relative_to(REELS)
    dst = OUT / rel; dst.parent.mkdir(parents=True, exist_ok=True)
    af = f"[1:a]atrim=0:{d},afade=t=in:st=0:d=0.4,afade=t=out:st={fo:.2f}:d=0.6,volume={VOL}[a]"
    r = subprocess.run([FF,"-y","-hide_banner","-loglevel","error","-i",str(reel),"-i",str(track),
        "-filter_complex",af,"-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-b:a","192k",
        "-shortest",str(dst)])
    if r.returncode != 0:
        print("FAILED:", reel.name); continue
    rows.append([str(rel), track.name, f"{d:.1f}s"])
    print(f"  {rel}  <- {track.name}")

with open(OUT/"track-map.csv","w",newline="") as fh:
    w = csv.writer(fh); w.writerow(["Reel","Music track","Length"]); w.writerows(rows)
print(f"done: {len(rows)} reels with music -> {OUT}")
