# Misty Rainforest — Ambient TV Loop

A ~3.5 minute seamlessly-looping nature ambience video for a living room or
bedroom TV. Silent, 720p, 16:9, no cuts or camera moves — built to sit on a
screen indefinitely without drawing attention to itself.

## What's here

| File | |
|---|---|
| `nature-loop.mp4` | The finished loop. This is the deliverable. |
| `player.html` | Fullscreen looping player — open it, click for fullscreen. |
| `shots.json` | The 15 shot prompts and the exact generation config. |
| `renders.json` | Generated clip URLs, written as each render completes. |
| `download.py` | Pulls the clips in `renders.json` into `clips/`. |
| `assemble.py` | Crossfades the clips and seals the loop point. |
| `clips/` | The 15 raw 15-second source clips. |

## How it was made

15 clips × 15s were generated on OpenArt with **PixVerse V6** (`text2video`,
720p, 16:9, silent) at 210 credits each — 3,150 credits total.

720p at 15s was the cheapest usable configuration on offer, at 14 credits per
second of footage. 1080p costs 30 credits/second, which would have bought only
1m45s of runtime; for soft, fog-heavy nature footage viewed across a room, more
runtime is worth more than more pixels.

Every prompt pins the camera down (`static locked-off camera`, `no camera
movement`, `no cuts`) and asks for continuous motion — drifting fog, running
water, trembling ferns. Motion that never resolves is what lets a shot be cut
into a loop without an obvious beginning or end.

## Rebuilding

```sh
pip install imageio-ffmpeg
python3 download.py     # clips/ <- renders.json
python3 assemble.py     # -> nature-loop.mp4
```

## The loop seam

`assemble.py` runs two passes.

**Pass 1** crossfades each clip into the next with a 1s `xfade`, giving a chain
of `15×15 − 14×1 = 211s`.

**Pass 2** is what makes it actually loop. Playing the chain on repeat would
still snap from shot 15 back to shot 1. So the chain is rebuilt as:

```
chain[1s … 210s]  +  xfade(chain[210s … 211s], chain[0s … 1s])
```

The result starts on the frame at `t=1s` and *ends* on that same frame, so a
player set to loop shows no discontinuity at all. Final runtime is 210s (3m30s).

## Playing it on a TV

- **Cast / AirPlay** — open `player.html` on a laptop, fullscreen it, cast the tab.
- **USB stick** — copy `nature-loop.mp4` across; most TVs have a repeat setting
  in their media player.
- **Plex / Jellyfin** — drop it in a library and enable repeat.

It has no audio track, so anything you're already playing keeps running over it.
