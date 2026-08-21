# 9:16 covers — Shorts / Reels / TikTok

1080 × 1920, built from the same episode frames as the 16:9 thumbnails so a viewer who
meets the series on a Short recognises it on the main channel.

| File | Frame |
|---|---|
| `trailer_9x16_A.jpg` | Rook and Cinder running through burning forest — **recommended** |
| `trailer_9x16_B.jpg` | The Rings under the broken silver sky |
| `trailer_9x16_C.jpg` | The Iron Warden — highest contrast, but spoils the Ep6 reveal |
| `ep01_9x16_A.jpg` | Sorrel's face in ember-light — **recommended**, a single centred face is the strongest vertical subject |
| `ep01_9x16_B.jpg` | Moth in the ceremony fire |
| `ep02_9x16_A.jpg` | Rook and Sedge across the mist — **recommended** |
| `ep02_9x16_B.jpg` | Sedge alone in the pole-boat |
| `ep03_9x16_A.jpg` | Wren in the Rings under the broken sky — **recommended** |
| `ep03_9x16_B.jpg` | Rook and Cinder under a red sky |

## How these are composed

A 16:9 frame cannot fill a 9:16 canvas — a straight cover-crop keeps only the central
third of the width, which destroys every two-shot and every wide landscape. So the frame
is widened to 1.28× and cropped to the canvas (keeping ~78% of the original width, which
two-shots survive), then laid as a tall band over a softly blurred, darkened fill of the
same frame. The margins carry the scene's own colour instead of reading as dead black
bars, and the wordmark sits in a gradient scrim below the band.

Ep1's vertical A uses a different frame from its 16:9 A: the horizontal thumbnail is a
two-shot of Cinder and Sorrel, which loses its composition at this ratio. A single
centred face works far harder in a vertical feed.

Rebuild with:

    python3 make_thumbnail_vertical.py <source-frame.jpg> <out.jpg>

or import `build(src, out, sub=..., strap=...)` for the episode labels.

**Note on YouTube Shorts:** a Short's still is normally pulled from the video itself, and
custom thumbnail upload for Shorts is not available on every account. These work
regardless as covers for Reels and TikTok, and as the first frame if you'd rather open a
Short on a title card — in that case hold it for about half a second, no longer.
