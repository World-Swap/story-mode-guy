# The Open Lands — ambient video pipeline

Long, seamlessly-looping nature ambience for televisions, built from OpenArt
clips. Each video is an *edition*; the scripts are shared.

```
channel/channel.md              channel name, About copy, keywords, art in use
editions/01-misty-rainforest/   published — https://youtu.be/YQVLMjDPSX4
editions/02-coastal/            in progress
```

## Scripts

Every script runs **from inside an edition directory** and resolves paths
against the current directory, so one copy serves all editions:

```sh
cd editions/02-coastal
python3 ../../download.py          # pull rendered clips listed in renders.json
python3 ../../assemble.py          # clips/ -> nature-loop.mp4 (seamless)
../../add-audio.sh -w 1,0.55 wind.mp3 rain.mp3   # -> nature-loop-sound.mp4
../../make-long.sh 3 nature-loop-sound.mp4       # -> nature-loop-3h-sound.mp4
python3 ../../thumbnail.py         # -> thumbnails/
```

Channel art is made once, from whichever edition has the best frames:

```sh
python3 ../../avatar.py            # -> avatars/   800x800 + 96px previews
python3 ../../banner.py            # -> banners/   2048x1152 + crop proofs
```

## How the loop is made seamless

`assemble.py` crossfades each clip into the next, then folds the chain's tail
onto its own head, so the last frame matches the first and a looping player
never shows a cut. `add-audio.sh` applies the same wrap to the soundtrack, and
because the audio period equals the video period, a long cut is one repeating
unit of picture and sound.

`make-long.sh` repeats that master a whole number of times with `-c copy` —
lossless, no re-encode, about a minute for three hours. Whole loops only:
trimming to a round runtime would leave a hard cut at the end of the file.

Geometry and frame rate are probed from the clips, not assumed, so editions can
differ in resolution (01 is 720p, 02 is 1080p).

## Long cuts are not committed

A 3-hour file is ~3.4 GB, past GitHub's 100 MB per-file limit, so it is
gitignored and rebuilt locally. The 3m30s master is committed.

## ffmpeg

If `brew install ffmpeg` compiles from source and stalls (macOS 13 and older
have no bottle), use a venv instead — no PEP 668 trouble, nothing to compile:

```sh
python3 -m venv ~/ffmpeg-venv
~/ffmpeg-venv/bin/pip install imageio-ffmpeg
source ~/ffmpeg-venv/bin/activate
```

## Costs

| Config | Per 15s clip | 15 clips |
|---|---|---|
| PixVerse V6, 720p | 210 | 3,150 |
| PixVerse V6, 1080p | 450 | 6,750 |

720p carries an SD badge on YouTube; HD starts at 1080p.
