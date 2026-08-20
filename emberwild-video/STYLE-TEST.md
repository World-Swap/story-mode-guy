# Style test — 2026-08-20

Two reference plates generated on the **Free plan's 40 credits** to prove the pipeline before
committing to a paid plan. **30 credits spent, 10 remaining.**

Model: `byte-plus-seedream-4-5` text2image · 2K · 16:9 · 15 credits each.

| Plate | File | Tests |
|---|---|---|
| Rook + Cinder under the Riven Sky | `plates/plate_rook-cinder_riven-sky.jpg` | House style, ember palette, character design, **the Riven Sky** — the riskiest element in the whole series |
| Vane, with a Vael for scale | `plates/plate_vane_scale.jpg` | **The curve-vs-straight-line rule**, the faceless helm, forge-red discipline, cross-plate style consistency |

## Verdict: viable

Both plates came back on-style and, critically, **consistent with each other** — same flat
vector-cel rendering, same ink weight, same lighting logic. That cross-plate consistency is the
thing the whole series depends on, and it held on the first attempt with no reference images
attached at all. With reference plates attached in `element2video`, it gets stronger.

**What rendered correctly:**

- **The Riven Sky.** The single biggest risk — a *broken* ring of pale silver light, segmented,
  with gaps. Models usually default to a complete planetary ring. It came out right first try.
- **The locked palette.** Ember orange, gold, bloodwarm, bone-cream, with pale silver reserved
  for the ring. No drift.
- **The curve-vs-straight rule.** Vane is all hard facets and diamond rivets; the smoke and
  landscape behind him are all flowing curves. The contrast reads exactly as the comic intends.
- **Vane's faceless helm** with the full-width forge-red slit, and the straight command rod.
- **Rook's canon details** — the curved bone knife, arm tattoos, barefoot, layered hide in
  ember and bone.
- **Cinder's canon details** — scarred muzzle, one torn ear, curved ridged horns.

## Two corrections, now applied to the prompt blocks

1. **Vane came out 2–3× human height.** Canon is **~1.34×** — taller and broader, not a colossus.
   His menace is meant to come from *wrongness*, not size. The block now ends
   `…taller and broader than a man but not a giant, human-scaled`.
2. **Cinder came out lion-sized.** He is a flame-**lynx**, and canon calls him the runt of his
   litter. The block now says `about the size of a big hound, not lion-sized`.

Both fixes are in `shots.json` and bible §4, and both are added to the continuity guards.

## What this does not yet prove

No **video** was generated — the cheapest video job on the platform is 50 credits and the account
had 40. Motion quality, temporal stability and `element2video` identity-locking across shots are
still untested. The stills prove the *look*; the first 8-shot trailer will prove the *motion*.
