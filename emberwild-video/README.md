# Emberwild — Video Series Production Package

Turns the Emberwild comic saga into an AI-generated video series on OpenArt.
Story and canon come from the comic Series Bible; nothing here invents lore.

| File | What it is |
|---|---|
| `EMBERWILD_VIDEO-BIBLE.md` | The adaptation. Style lock, character prompt blocks, motion grammar, consistency strategy, cost model. **Read first.** |
| `SHOTLIST.md` | All 68 shots, human-readable, with beats and camera moves. |
| `shots.json` | The same 68 shots, machine-readable. The actual source of truth for generation. |
| `build_prompts.py` | Assembles ready-to-send prompts from `shots.json`. |

**Sources pulled from:** `EMBERWILD_Series-Bible_v2.md`, `EMBERWILD_HANDOFF-NOTES.md`,
`emberwild_art-toolkit_v5.py` (locked palette) in Google Drive → EMBERWILD, plus the ten
episode cards recovered from this repo's git history (`git show be2fec6^:index.html`).

---

## What's in the box

**68 shots across 11 sequences**, all written from locked canon:

- **T1 — Series trailer**, 8 shots / ~40s. The hero asset. Spoiler-safe.
- **T2 — Episode trailers**, 6 shots / ~30s each, for all ten published episodes.
  Episodes 9 and 10 are flagged as Act III spoilers and excluded by `--safe`.

Episodes 11–13 are roadmap-only in the comic and have no shot list yet.

---

## Runbook

```bash
# see everything
python3 build_prompts.py

# one sequence
python3 build_prompts.py T1_series_trailer

# marketing-safe only (drops the Act III reveals)
python3 build_prompts.py --safe

# vertical reframe for Reels / Shorts / TikTok
python3 build_prompts.py --vertical T2_ep01

# ready-to-send params for openart_generate_video
python3 build_prompts.py --json T1_series_trailer

# what a selection costs, per model
python3 build_prompts.py --cost T1_series_trailer
```

### Order of operations

1. **Upload the existing cover art as style references.** `ep-1cover.png` … `emberwild_ep10_cover_sleeping-ones.png`
   in the repo root are finished art in the locked style — the cheapest possible style lock.
   This must be done by the account holder through OpenArt's upload picker; no programmatic
   upload is exposed to this session.
2. **Generate the reference plates** — one still per principal character, one per environment
   (bible §4 and §5). On the 24,000-credit plan the unlimited image models make these **free**,
   so iterate until they are exactly right.
3. **Generate T1**, the 8-shot series trailer, in `element2video` with the plates attached.
   This is the style test. If T1 looks right, everything after it inherits the look.
4. **Generate T2** episode trailers, one episode at a time, in order — matching how the comic
   was built.
5. **Cut, grade and score in an editor.** Do not generate dialogue (bible §9).

---

## The two things that make or break this

**Reference-locked generation.** Text prompts alone will drift across 68 shots. Every shot must
run in `element2video` with character and environment plates attached. `pixverseV6` is the
cheapest video model but has **no** `element2video` mode, so it cannot hold character identity —
use it only for pure landscape shots.

**The curve rule.** The Vael world is made of curves; the Ironfolk are the only thing that draws
a straight line. This is the spine of the comic and it must be the spine of the video. Every
shot prompt and the style block both carry it. Check every generated shot against the
continuity guards in `shots.json` before accepting it.

---

## Status

The package is complete and runs as soon as credits exist.
**The Free plan's 40 credits cannot generate a single video shot** — the cheapest video job on
the platform is 50. See bible §8 for what the 24,000-credit plan buys (short version: T1 plus
all ten episode trailers for about half of one month, with the whole image side free).
