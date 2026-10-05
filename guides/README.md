# Story Mode Guy — Photography Guide Catalog

Ten premium, sellable photography PDF guides ($17–$39), built from market research
into the highest-demand, proven-paid photography topics. See
[`00-MARKET-RESEARCH-REPORT.md`](00-MARKET-RESEARCH-REPORT.md) for the demand/pricing rationale.

## The catalog

| # | Guide | Price | Pages | Best buyer |
|---|-------|-------|-------|-----------|
| 01 | Pro Photos From Your Pocket (iPhone/Smartphone) | $34 | 23 | Anyone with a phone |
| 02 | The Lightroom Blueprint | $37 | 22 | RAW shooters with flat edits |
| 03 | Product Photos That Sell | $34 | 23 | Etsy/Shopify/Amazon sellers |
| 04 | Master Your Camera in a Weekend (Exposure) | $27 | 23 | New DSLR/mirrorless owners |
| 05 | Why Are My Photos Blurry? | $22 | 15 | Frustrated hobbyists |
| 06 | Real Estate & Airbnb Photography | $39 | 23 | Side-hustlers, hosts |
| 07 | Natural-Light Portraits & Posing | $29 | 25 | Family/portrait hobbyists |
| 08 | Astrophotography for Beginners | $39 | 24 | Night-sky chasers |
| 09 | Low-Light & Night Photography | $27 | 24 | Event/city shooters |
| 10 | The Photographer's Cheat-Sheet Pack | $17 | 17 | New owners / bundle add-on |

**219 pages total.** Finished PDFs are in [`pdf/`](pdf/). A preview of all ten covers is in
`cover-contact-sheet.pdf`.

### Suggested bundle
All 10 as "The Complete Photography Library" at **$79–99** (vs. $305 à la carte). Pair any
core guide with the Cheat-Sheet Pack to lift a $27 product to a $34–39 bundle.

## How it's built (regenerate any time)

```
guides/
├── manifest.json          # guide metadata: titles, prices, accent colors
├── src/*.html             # editable body content (one file per guide)
├── build/
│   ├── build.py           # wraps a src fragment in the cover+TOC+CSS design shell
│   ├── render.js          # Playwright: HTML → print-ready PDF (page numbers, footer)
│   └── AUTHORING-SPEC.md   # the component system + writing rules
├── html/*.html            # assembled documents (generated)
└── pdf/*.pdf              # final deliverables (generated)
```

To edit content, change a file in `src/` and rebuild:

```bash
cd guides
python3 build/build.py <id>          # or "all"
PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers \
  node build/render.js html/<id>.html pdf/<id>.pdf "Footer Title"
```

To change a guide's title, price, or accent color, edit `manifest.json` and rebuild.

## Selling notes
- Sell on Gumroad, Etsy (digital download), or Payhip. Use `cover-contact-sheet.pdf`
  imagery and the per-guide covers as listing thumbnails.
- The covers are branded to storymodeguy.com and priced on-cover; adjust in `manifest.json`
  if you change pricing.
- Content covers well-established fundamentals that stay accurate across camera brands and
  software versions (no version-specific menu paths that go stale).
