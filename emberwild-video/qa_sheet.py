#!/usr/bin/env python3
"""Build review montages: one mid-frame per shot, tiled, for continuity QA."""
import subprocess, pathlib, sys, imageio_ffmpeg
FF=imageio_ffmpeg.get_ffmpeg_exe()
SRC=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else "shots_ep01")
OUT=pathlib.Path("/tmp/claude-0/-home-user-story-mode-guy/5a8aad61-a781-5653-81b6-5214d4221d3e/scratchpad")
clips=sorted(SRC.glob("*.mp4"))
frames=[]
for c in clips:
    f=OUT/f"fr_{c.stem}.jpg"
    subprocess.run([FF,"-y","-ss","2.5","-i",str(c),"-vf","scale=400:-1","-frames:v","1",str(f)],capture_output=True)
    frames.append(f)
# tile in groups of 12 (4x3)
for gi in range(0,len(frames),12):
    grp=frames[gi:gi+12]
    cmd=[FF,"-y"]
    for f in grp: cmd+=["-i",str(f)]
    n=len(grp)
    cmd+=["-filter_complex",f"{''.join(f'[{i}:v]' for i in range(n))}xstack=inputs={n}:layout={'|'.join(f'{(i%4)*400}_{(i//4)*225}' for i in range(n))}" if n==12 else
          f"{''.join(f'[{i}:v]' for i in range(n))}hstack=inputs={n}", "-frames:v","1",str(OUT/f"qa_{SRC.name}_{gi//12+1}.jpg")]
    subprocess.run(cmd,capture_output=True)
print("\n".join(f"{i+1:2d}. {c.stem}" for i,c in enumerate(clips)))
