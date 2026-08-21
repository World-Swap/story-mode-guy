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
SRC="$(cd "$(dirname "$0")" && pwd)/nature-loop.mp4"
LOOP_SECS=210.625

[ -f "$SRC" ] || { echo "nature-loop.mp4 not found next to this script"; exit 1; }
command -v ffmpeg >/dev/null || { echo "ffmpeg not found (try: pip install imageio-ffmpeg)"; exit 1; }

N=$(python3 -c "import math;print(math.ceil($HOURS*3600/$LOOP_SECS))")
OUT="nature-loop-${HOURS}h.mp4"
LIST=$(mktemp)
python3 -c "print(\"file '$SRC'\n\"*$N, end='')" > "$LIST"

echo "Repeating $N loops -> $OUT"
ffmpeg -y -f concat -safe 0 -i "$LIST" -c copy -movflags +faststart "$OUT" -loglevel error
rm -f "$LIST"
ffmpeg -i "$OUT" -hide_banner 2>&1 | grep Duration
echo "Done -> $OUT"
