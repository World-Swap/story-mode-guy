#!/usr/bin/env bash
# Build a long upload version by repeating the seamless loop.
#
# This is a stream copy, not a re-encode: it is lossless and takes about a
# minute. The loop is only ever repeated whole - trimming to a round number of
# hours mid-loop would put a hard cut at the end of the file.
#
#   ./make-long.sh 3      -> ~3 hours  (52 loops, ~3.4 GB)
#   ./make-long.sh 1      -> ~1 hour   (18 loops, ~1.2 GB)
#   ./make-long.sh 10     -> ~10 hours (171 loops, ~11 GB)
set -euo pipefail

HOURS="${1:-3}"
DIR="$(cd "$(dirname "$0")" && pwd)"
SRC="$DIR/nature-loop.mp4"
LOOP_SECS=210.625

[ -f "$SRC" ] || { echo "ERROR: nature-loop.mp4 not found next to this script."; exit 1; }

# Prefer a real ffmpeg on PATH; fall back to the one pip's imageio-ffmpeg ships.
if command -v ffmpeg >/dev/null 2>&1; then
  FF=ffmpeg
elif FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())" 2>/dev/null) && [ -x "$FF" ]; then
  :
else
  echo "ERROR: ffmpeg not found. Install it with one of:"
  echo "  macOS:    brew install ffmpeg"
  echo "  Ubuntu:   sudo apt install ffmpeg"
  echo "  anywhere: pip install imageio-ffmpeg"
  exit 1
fi

N=$(python3 -c "import math;print(math.ceil($HOURS*3600/$LOOP_SECS))")
OUT="$DIR/nature-loop-${HOURS}h.mp4"
LIST=$(mktemp)
trap 'rm -f "$LIST"' EXIT

# One line per repetition. Absolute path: concat resolves entries relative to
# the list file, which lives in the temp dir.
python3 -c "
import sys
src, n = sys.argv[1], int(sys.argv[2])
sys.stdout.write(''.join(\"file '%s'\n\" % src for _ in range(n)))
" "$SRC" "$N" > "$LIST"

echo "Repeating $N loops -> $(basename "$OUT")"
"$FF" -y -f concat -safe 0 -i "$LIST" -c copy -movflags +faststart "$OUT" -loglevel error
"$FF" -i "$OUT" -hide_banner 2>&1 | grep Duration || true
echo "Done -> $OUT"
