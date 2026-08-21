#!/usr/bin/env bash
# Mux an audio bed into the seamless master loop.
#
#   ./add-audio.sh path/to/track.mp3
#
# Writes nature-loop-sound.mp4. Then rebuild the long cut from it:
#   ./make-long.sh 3 nature-loop-sound.mp4
#
# Two things this does that dragging a file into an editor does not:
#
#  1. The audio is looped to exactly the video's length, then its tail is
#     crossfaded onto its own head - the same wrap the video uses. So the
#     soundtrack loops without a click at the seam.
#  2. The video is stream-copied, never re-encoded. Muxing a 3-hour file this
#     way costs a minute and loses nothing.
#
# Because the audio period equals the video period, the long cut is one
# repeating unit of picture and sound together.
set -euo pipefail

TRACK="${1:-}"
DIR="$(cd "$(dirname "$0")" && pwd)"
SRC="$DIR/nature-loop.mp4"
OUT="$DIR/nature-loop-sound.mp4"
XF=2.0                       # audio crossfade at the loop seam, seconds

[ -n "$TRACK" ] || { echo "usage: ./add-audio.sh path/to/track.mp3"; exit 1; }
[ -f "$TRACK" ] || { echo "ERROR: no such audio file: $TRACK"; exit 1; }
[ -f "$SRC" ]   || { echo "ERROR: nature-loop.mp4 not found next to this script"; exit 1; }

if command -v ffmpeg >/dev/null 2>&1; then
  FF=ffmpeg
elif FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())" 2>/dev/null) && [ -x "$FF" ]; then
  :
else
  echo "ERROR: ffmpeg not found. See the hint in make-long.sh."; exit 1
fi

# Video length. Capture ffmpeg's output first rather than piping into awk:
# awk exiting early would SIGPIPE ffmpeg, and pipefail would kill the script.
INFO=$("$FF" -i "$SRC" -hide_banner 2>&1 || true)
L=$(printf '%s\n' "$INFO" | awk -F'[:,]' '/Duration:/{print $2*3600+$3*60+$4; exit}')
[ -n "$L" ] || { echo "ERROR: could not read the video duration"; exit 1; }
END=$(python3 -c "print(f'{$L + $XF:.3f}')")
BODY=$(python3 -c "print(f'{$L:.3f}')")

echo "Video is ${L}s; looping audio to match and sealing the audio seam"

# -stream_loop -1 repeats the track indefinitely; we take L+XF of it, then fold
# the last XF onto the first XF so the result loops cleanly at exactly L.
"$FF" -y -stream_loop -1 -i "$TRACK" -i "$SRC" -filter_complex "
  [0:a]atrim=0:${END},asetpts=N/SR/TB,aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo[a];
  [a]asplit=3[a1][a2][a3];
  [a1]atrim=${XF}:${BODY},asetpts=N/SR/TB[body];
  [a2]atrim=${BODY}:${END},asetpts=N/SR/TB[tail];
  [a3]atrim=0:${XF},asetpts=N/SR/TB[head];
  [tail][head]acrossfade=d=${XF}[blend];
  [body][blend]concat=n=2:v=0:a=1[aout]
" -map 1:v -map "[aout]" -c:v copy -c:a aac -b:a 192k -movflags +faststart "$OUT"

"$FF" -i "$OUT" -hide_banner 2>&1 | grep -E "Duration|Stream #" || true
echo "Done -> $OUT"
echo "Next:  ./make-long.sh 3 nature-loop-sound.mp4"
