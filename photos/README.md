# Photos pipeline

One command turns new photos into live site updates. New shots flow into the
**full gallery** and the homepage **Newest Captures** slideshow automatically;
nothing ever falls off the site — older frames just move down the gallery.

## Add new photos

```bash
# from the repo root
python3 photos/add.py "/path/to/IMG_1234.jpg" "Sunset over the wharf"

# several at once (image, caption, image, caption, ...)
python3 photos/add.py "a.jpg" "First light" "b.jpg" "Fog on the cliffs"

# also feature a photo big in the homepage "Best of" band
python3 photos/add.py --best "hero.jpg" "Mackerel sky off West Cliff"
```

Each photo is resized to full-res (1920px) + a thumbnail (800px) at the repo
root, added to the **top** of `photos/manifest.json` (newest first), and the
site is rebuilt. Then commit / zip the changed files:
`photo-*.jpg`, `thumb-photo-*.jpg`, `photos/manifest.json`, `index.html`, `gallery.html`.

**Easiest path:** just send me (Claude) the new photos + captions and I'll run this
and hand you a drop-in zip.

## How it works

- `photos/manifest.json` — the single source of truth. An array, **newest first**.
  Each item: `{"n": 123, "cap": "Caption", "best": false}`. Photo N = `photo-N.jpg`.
- `photos/build.py` — rewrites only the marked regions of the pages:
  - **Newest Captures** slideshow = the first `NEWEST_COUNT` (14) photos in the manifest.
  - **Best of** band = every photo with `"best": true`.
  - **Gallery grid** = every photo, in manifest order.
- `photos/add.py` — processes images, updates the manifest, calls `build.py`.

## Tweaks you can make by hand

- **Change a caption:** edit it in `photos/manifest.json`, run `python3 photos/build.py`.
- **Feature / unfeature in Best-of:** flip `"best"` true/false, run `build.py`.
- **How many photos in the slideshow:** change `NEWEST_COUNT` in `build.py`.
- **Reorder:** the manifest order is the gallery order (top = newest). Move items, run `build.py`.

The regions are wrapped in `<!--PHOTOS:NEWEST-->`, `<!--PHOTOS:BESTOF-->`,
`<!--PHOTOS:COUNT-->` (index.html) and `<!--PHOTOS:GRID-->` (gallery.html).
Don't delete those marker comments — the build needs them.
