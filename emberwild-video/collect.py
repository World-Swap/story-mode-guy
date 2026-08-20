#!/usr/bin/env python3
"""Download a finished OpenArt shot and build a 4-frame contact sheet for review."""
import subprocess, sys, pathlib, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
OUT = pathlib.Path(__file__).parent / "shots_out"
OUT.mkdir(exist_ok=True)

def collect(url, name, sheet_dir="/tmp/claude-0/-home-user-story-mode-guy/5a8aad61-a781-5653-81b6-5214d4221d3e/scratchpad"):
    mp4 = OUT / f"{name}.mp4"
    subprocess.run(["curl", "-sS", "-o", str(mp4), url], check=True)
    sheet = pathlib.Path(sheet_dir) / f"contact_{name}.jpg"
    subprocess.run([FF, "-y", "-i", str(mp4),
        "-vf", r"select='eq(n\,0)+eq(n\,40)+eq(n\,80)+eq(n\,119)',scale=560:-1,tile=2x2",
        "-frames:v", "1", str(sheet)], capture_output=True)
    return mp4, sheet

if __name__ == "__main__":
    for pair in sys.argv[1:]:
        url, name = pair.split("|")
        mp4, sheet = collect(url, name)
        print(f"{name}: {mp4.stat().st_size//1024}KB -> {sheet}")
