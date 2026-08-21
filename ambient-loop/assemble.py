#!/usr/bin/env python3
"""Assemble the rendered clips into one seamlessly-looping ambience video.

Two passes:
  1. Crossfade every clip into the next  -> chain.mp4
  2. Wrap the chain's tail onto its own head so the loop point is invisible
     -> nature-loop.mp4

Pass 2 is what makes it loop cleanly. Given a chain of duration D and a
transition length t, we rebuild it as:  chain[t:D-t]  +  xfade(chain[D-t:D], chain[0:t])
The output therefore starts on the frame at time t and ends on that same
frame, so a player looping it never shows a cut.
"""
import glob, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
XFADE = 1.0          # crossfade length, seconds
FPS = 24             # matches the source clips; resampling here would judder
CRF, PRESET = 18, "slow"

def ffmpeg_exe():
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()

FF = ffmpeg_exe()
FFPROBE = FF.replace("ffmpeg", "ffprobe")

def duration(path):
    """Clip length in seconds, read from the container."""
    out = subprocess.run(
        [FF, "-i", path, "-hide_banner"], capture_output=True, text=True).stderr
    for line in out.splitlines():
        if "Duration:" in line:
            h, m, s = line.split("Duration:")[1].split(",")[0].strip().split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)
    raise RuntimeError(f"could not read duration of {path}")

def run(args):
    print("  ffmpeg", " ".join(args[1:6]), "...")
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"ffmpeg failed:\n{r.stderr[-3000:]}")

def build_chain(clips, out):
    """Crossfade clips together end to end."""
    durs = [duration(c) for c in clips]
    inputs = []
    for c in clips:
        inputs += ["-i", c]

    # Every clip is normalised to a common format first so xfade can chain them.
    parts, acc = [], durs[0]
    for i in range(len(clips)):
        parts.append(f"[{i}:v]scale=1280:720:force_original_aspect_ratio=increase,"
                     f"crop=1280:720,fps={FPS},format=yuv420p,setsar=1[c{i}]")
    last = "c0"
    for i in range(1, len(clips)):
        offset = acc - XFADE
        parts.append(f"[{last}][c{i}]xfade=transition=fade:"
                     f"duration={XFADE}:offset={offset:.3f}[v{i}]")
        last = f"v{i}"
        acc = acc + durs[i] - XFADE

    run([FF, "-y", *inputs, "-filter_complex", ";".join(parts),
         "-map", f"[{last}]", "-an", "-c:v", "libx264", "-crf", str(CRF),
         "-preset", PRESET, "-pix_fmt", "yuv420p", out])
    return acc

def wrap_seamless(src, total, out):
    """Fold the tail onto the head so the file loops without a visible cut."""
    t, end = XFADE, total
    # trim drops the constant frame rate that xfade and concat both require,
    # so each branch is re-timed with fps= before it is used.
    retime = f"setpts=PTS-STARTPTS,fps={FPS},setsar=1"
    fc = (
        f"[0:v]trim=start={t}:end={end - t},{retime}[body];"
        f"[0:v]trim=start={end - t}:end={end},{retime}[tail];"
        f"[0:v]trim=start=0:end={t},{retime}[head];"
        f"[tail][head]xfade=transition=fade:duration={t}:offset=0[blend];"
        f"[body][blend]concat=n=2:v=1:a=0[out]"
    )
    run([FF, "-y", "-i", src, "-filter_complex", fc, "-map", "[out]", "-an",
         "-c:v", "libx264", "-crf", str(CRF), "-preset", PRESET,
         "-pix_fmt", "yuv420p", "-movflags", "+faststart", out])
    return end - t

def main():
    clips = sorted(glob.glob(os.path.join(HERE, "clips", "*.mp4")))
    if not clips:
        sys.exit("No clips in clips/ — run download.py first.")
    print(f"Assembling {len(clips)} clips")

    chain = os.path.join(HERE, "chain.mp4")
    final = os.path.join(HERE, "nature-loop.mp4")

    print("Pass 1/2: crossfading clips")
    total = build_chain(clips, chain)
    print(f"  chain = {total:.1f}s")

    print("Pass 2/2: sealing the loop point")
    length = wrap_seamless(chain, total, final)
    os.remove(chain)

    mins, secs = divmod(length, 60)
    print(f"\nDone -> {final}")
    print(f"Runtime {int(mins)}m{secs:04.1f}s, loops seamlessly.")

if __name__ == "__main__":
    main()
