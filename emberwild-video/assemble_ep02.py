#!/usr/bin/env python3
"""Assemble EMBERWILD Episode Two from its 42 shots.

Same pipeline as Episode One, with one addition: Episode 2 was generated with
generateSound off, so a continuous ambient bed is harvested from Episode 1's
clips and laid under the whole cut. That is deliberately better than per-shot
generated audio, which restarts its ambience every five seconds.
"""
import json, pathlib, sys, subprocess, imageio_ffmpeg
from assemble import build, probe

FF = imageio_ffmpeg.get_ffmpeg_exe()
HERE = pathlib.Path(__file__).parent
SRC = HERE / "shots_ep02"
REROLL = HERE / "shots_out"
SUBS = {}          # QA re-rolls that supersede the original render


def ambient_bed(seconds, out):
    """Build a continuous ambient bed by concatenating Ep1 audio and looping it."""
    srcs = sorted((HERE / "shots_ep01").glob("*.mp4"))
    picks = [srcs[i] for i in (2, 26, 30, 12, 34) if i < len(srcs)]   # camp, celebration, night, drum, glow
    if not picks:
        return None
    tmp = HERE / "_tmp"; tmp.mkdir(exist_ok=True)
    wavs = []
    for i, p in enumerate(picks):
        w = tmp / f"amb{i}.wav"
        subprocess.run([FF, "-y", "-i", str(p), "-vn", "-ac", "2", "-ar", "44100", str(w)],
                       capture_output=True)
        if w.exists() and w.stat().st_size > 1000:
            wavs.append(w)
    if not wavs:
        return None
    lst = tmp / "amb.txt"
    lst.write_text("".join(f"file '{w.resolve()}'\n" for w in wavs))
    joined = tmp / "amb_joined.wav"
    subprocess.run([FF, "-y", "-f", "concat", "-safe", "0", "-i", str(lst), str(joined)],
                   capture_output=True)
    subprocess.run([FF, "-y", "-stream_loop", "-1", "-i", str(joined), "-t", str(seconds),
                    "-af", "volume=0.5,afade=t=in:st=0:d=2,"
                           f"afade=t=out:st={max(seconds-3,0):.2f}:d=3",
                    "-c:a", "aac", "-b:a", "160k", str(out)], capture_output=True)
    return out if out.exists() else None


def main():
    ep = json.loads((HERE / "shots_ep02.json").read_text())
    ordered = sorted(ep["shots"], key=lambda s: s["n"])
    by_n = {int(p.stem.split("_")[1]): p for p in sorted(SRC.glob("*.mp4"))}

    clips, captions = [], {}
    for idx, s in enumerate(ordered):
        p = SUBS.get(s["n"]) or by_n.get(s["n"])
        if p is None or not p.exists():
            sys.exit(f"missing shot {s['n']}")
        clips.append(p)
        if s.get("caption"):
            captions[idx] = s["caption"]

    silent = HERE / "_ep02_silent.mp4"
    build(clips, captions, silent, title="EMBERWILD",
          subtitle="Episode Two — Strangers in the Reeds")

    dur = probe(silent)
    bed = ambient_bed(dur, HERE / "_tmp" / "bed.m4a")
    out = HERE / "EMBERWILD_Ep02_Strangers-in-the-Reeds.mp4"
    if bed:
        subprocess.run([FF, "-y", "-i", str(silent), "-i", str(bed),
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                        "-c:a", "aac", "-b:a", "160k", "-shortest",
                        "-movflags", "+faststart", str(out)], capture_output=True, check=True)
        silent.unlink(missing_ok=True)
        print(f"wrote {out.name} with a continuous ambient bed")
    else:
        silent.rename(out)
        print(f"wrote {out.name} (no ambient bed - Ep1 audio unavailable)")
    print(f"{out.stat().st_size//1024//1024} MB  {probe(out):.1f}s  "
          f"{len(clips)} shots, {len(captions)} captions")


if __name__ == "__main__":
    main()
