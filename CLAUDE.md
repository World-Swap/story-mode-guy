# Story Mode Guy — project notes

## Delivery preference (IMPORTANT)
When delivering changes to this user, **bundle every new/changed file into a single `.zip`**
and send it with `SendUserFile`. The user updates their repo by extracting that zip into the
repo root — this is their preferred and reliable workflow. Do this instead of (or in addition to)
committing, because **`git push` from this environment is blocked** (proxy returns HTTP 403 on all
GitHub write paths — org egress policy). Always commit locally too, but the zip is what actually
reaches their live repo.

- Include the updated `index.html` plus any referenced assets (images, etc.) so the drop is self-contained.
- Keep files at the paths they live at in the repo (repo root for site files) so extraction overwrites cleanly.

## What this repo is
Static site for storymodeguy.com — photography, ebooks (Emberwild comic series), and film.
Products sell via Payhip (`payhip.com/storymodeguy`); product links look like `payhip.com/b/XXXXX`.
`index.html` is the whole homepage (inline CSS + JS). `gallery.html` is the full photo gallery.

### Homepage sections & the card-slider pattern
Sections are `<section class="chapter" id="...">`. Product grids use a slider: `.strack` of cards
inside `.slider`, driven by `makeSlider('<track>','<prev>','<next>','<dots>')` near the end of the
`<script>`. Prints use `.pcard`; Emberwild + Guides use their own card markup. To add a product,
copy an existing card, point its `href` at the Payhip product URL, and add a matching `makeSlider(...)`
call if it's a new slider.

## Photography guides (`guides/` folder)
Ten sellable photography PDF guides ($17–39) + a $89 bundle, built from market research.
- `guides/manifest.json` — titles, prices, accent colors (edit here, then rebuild).
- `guides/src/*.html` — editable body content per guide (component vocabulary in `guides/build/AUTHORING-SPEC.md`).
- `guides/build/build.py` — wraps a src fragment in the cover+TOC+CSS shell → `guides/html/`.
- `guides/build/render.js` — Playwright HTML→PDF → `guides/pdf/`.
- Rebuild one: `python3 build/build.py <id>` then `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node build/render.js html/<id>.html pdf/<id>.pdf "Footer Title"` (run from `guides/`).
- Cover thumbnails for the site cards: `thumb-guide-01.jpg … 10.jpg` (repo root). Bundle cover: `bundle-cover.jpg`.
- `guides/PAYHIP-LISTINGS.md` — copy-paste product titles/descriptions/prices/tags for Payhip.
- The homepage `#guides` section is live and each card links to its Payhip product page.

## Rendering / tooling notes
- Chromium: `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`; Playwright at `/opt/node22/lib/node_modules/playwright` (set `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers`).
- PDF page rasterizing/thumbnails use `pymupdf` (fitz) + `pillow` (pip-installed).
- Commit signing shows "Unverified" in this env (no SSH signing private key present); identity is set to `noreply@anthropic.com` / `Claude`. Not fixable here — don't chase it.
