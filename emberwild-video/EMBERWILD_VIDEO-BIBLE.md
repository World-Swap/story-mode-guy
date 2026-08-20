# EMBERWILD — Video Series Bible
### Adaptation of the 13-episode comic saga into an AI-generated video series
Source of truth: `EMBERWILD_Series-Bible_v2.md` + `EMBERWILD_HANDOFF-NOTES.md` (Google Drive → EMBERWILD).
Nothing in this document may contradict those. Where they disagree, the comic bible wins.

---

## 1 · What we are making

A **motion-saga** adaptation: cinematic 2D-animated sequences generated shot-by-shot,
cut together into episodes. Not a page-turn motion comic — no panel borders, no balloons,
no on-screen lettering. The comic's *art direction* carries over; its *page furniture* does not.

**Three production tiers**, cheapest and highest-leverage first:

| Tier | Asset | Shots | Runtime | Purpose |
|---|---|---|---|---|
| **T1** | Series trailer | 8 | ~40s | One hero asset for the whole saga. Sells the shelf. |
| **T2** | Per-episode trailer ×10 | 6 each | ~30s each | Short-form (Reels/Shorts/TikTok) driving Payhip episode sales. |
| **T3** | Full motion episode ×13 | ~18 each | ~90s each | The actual series. Build only after T1/T2 prove the look. |

Build order is **T1 → T2 → T3**. T1 doubles as the style test: if the trailer's look is right,
every later shot inherits it.

---

## 2 · The one rule that must survive the adaptation

> **The Vael world is made of curves. The Ironfolk are the only thing that draws a straight line.**

This is the visual and thematic spine of the comic and it must be the spine of the video.
Rivers, roots, hair, horns, smoke, the broken ring — all flowing curves.
Ironfolk armour, machinery, the Cage, the Forge, the scar cut through the land — rigid
straight lines and hard facets, and they should read as *wrong* in frame.

Two supporting rules from the comic canon:

- **The Riven Sky is in almost every exterior.** A vast shattered ring of pale silver light
  arcing overhead, day and night, broken into segments. It is beautiful and wrong. It is the
  central mystery, so it is never absent and never explained by the visuals alone.
- **Scale sells mass, not detail.** Vane draws ~1.34× any Vael in the same shot. Overflow the
  frame and crop rather than adding fussy detail.

---

## 3 · The STYLE BLOCK (locked)

Every generation prompt — image or video — is `SHOT TEXT` + `, ` + `STYLE BLOCK`.
Never send a shot prompt without it. This is what holds 13 episodes to one look.

```
STYLE BLOCK:
2D animated fantasy illustration in flat vector-cel colour over soft gradient skies,
Art Nouveau flowing linework, anime-influenced expressive faces with large eyes,
heavy dark ink outlines, painterly comic key-art lighting, cinematic composition,
warm ember palette of burnt orange, gold, deep blood-red and bone-cream, with pale
silver reserved for the broken sky-ring, organic curves in every natural form,
rigid straight lines and hard facets only on Ironfolk metal,
no text, no lettering, no speech bubbles, no watermark, no logo, no signature
```

### Colour keys (from the locked comic palette — do not drift)

| Role | Hex | Use in frame |
|---|---|---|
| Ember | `#e8662e` | primary warmth, firelight, flame-lynx tribe |
| Gold | `#f2cd84` | highlights, embers in air |
| Bloodwarm | `#a8451d` | deep warm shadow |
| Nightwood | `#14100d` | near-black, outlines, night |
| Ring-silver | `#bcd4e2` | **the Riven Sky only** — shared across all tribes |
| Bone | `#d8c6a0` | hide, cloth, bone tools |
| Paper-cream | `#efe6cf` | mist, light haze |
| Reed-teal | `#2f8f7a` | Marsh Vael |
| Storm-violet | `#6d6f9c` | Sky Clan |
| Iron grey | `#4a4d55` | Ironfolk armour |
| Forge-red | `#c14a24` | Ironfolk furnace light |
| Soot | `#0d0d10` | Ironfolk shadow |

**One tribe = one accent colour per shot.** A marsh scene is teal-dominant; a peaks scene is
violet-dominant; an Ironfolk scene is grey/soot with forge-red as the only warmth. The ember
palette is the forest Vael's. This is what makes each episode its own object while the run
still reads as one series — exactly as the covers do.

---

## 4 · Character prompt blocks

Paste the block verbatim into any shot that character appears in. These are the identity
anchors; consistency across shots depends on them being reused word-for-word.

**ROOK** — `a young man with wind-blown loose dark hair, sharp quiet eyes, layered hide and
bark-cloth clothing in ember-orange and bone, barefoot, a curved bone knife at his belt,
tribal tattoos on his arms`
> Reluctant young chief. Walks last. Won't lie, even to comfort. The knife is the stolen blade.

**CINDER** — `a large horned wildcat with orange and cream fur, a scarred muzzle and one torn
ear, curved ridged horns sweeping back from its brow`
> Rook's flame-lynx. Runt of his litter. Feels danger before Rook does. Life-linked to Rook.

**SORREL** — `a wiry thirteen-year-old girl with dark braided hair, bright open face, ember-orange
and bone hide clothing, barefoot, tribal tattoos`
> The initiate whose bonding opens the saga. The story's honest heart. **The namer.**

**MOTH** — `a small flame-lynx cub with silver and orange fur, oversized paws, tiny budding horns`
> Sorrel's cub. Keeps looking at Wren.

**BRAM** — `a proud headstrong seventeen-year-old with tied-back dark hair, heavier build, ember
and bone hide clothing, tribal tattoos`
> Rival, then reluctant ally. Bonded to the lynx **THORNCLAW** (`a lean dark-furred horned wildcat`).

**KEEPER YARROW** — `an ancient Vael elder, blind in one eye, deeply lined face, long grey hair,
draped bone and ember robes hung with charms`
> Reads the fire. Keeps the forest's memory in smoke and song.

**SEDGE** — `a wary man in reed-teal and bone marsh clothing, wet dark hair, marsh-dry expression,
a long green serpent coiled about his shoulders`
> Marsh Vael. Serpent-bonded to **RILL**. Living proof the Vael are not the last.

**MARSH-MOTHER BRACKEN** — `a straight-backed older matriarch in teal and bone robes, grey hair
bound tight, guarded expression, a great pale serpent coiled at her feet`
> Keeper of the old wound. Reads the water, not the fire. Swears the Pact.

**WREN** — `a nineteen-year-old marsh woman with cropped dark hair, teal and bone clothing,
carrying a thick bundle of knotted record-cords at her hip, no bonded creature beside her`
> **19, marsh, UNBONDED, keeper of the knot-cords, raised by Bracken.** Never draw a creature
> with her. Her aloneness is the point.

**KESTREL** — `a proud clan leader in storm-violet and bone, feathered shoulder mantle, windburnt
face, standing beside a huge violet-grey storm-bird`
> Sky Clan. Bonded to **SQUALL**. Already lost eleven in a failed rescue.

**SKY-KEEPER HALCYON** — `a very old seated Sky Clan keeper in storm-violet robes, white hair,
frail hands, calm unreadable face`
> The one who remembers the sky. Held by the Ironfolk. Rescued in Ep4.

**SHRIKE** — `a hooded one-eyed Sky Clan man in weathered storm-violet, hard set jaw, no bird
beside him`
> His storm-bird Vesper is dead. A Vael with no other half left — literally the recipe for an
> Ironfolk, who chose the other road. Mirrors Ash.

**ASH** — `a gaunt soot-grey woman, hair shorn to stubble, an angular brand half-filed off her
own brow, stripped dark Ironfolk under-armour, no bonded creature`
> The Ironfolk deserter. Name and bond **cut out of her** as a child. Her bondlessness is a
> wound, not a boast. Sorrel names her.

**IRON WARDEN VANE** — `a towering armoured figure built entirely of hard flat angular plates and
diamond rivets in cold grey iron, no eyes, a full-width horizontal forge-red glow slit across
the helm, a tall crest fin, carrying a perfectly straight command rod`
> **Draws at ~1.34× any Vael in the same shot.** No curves anywhere on him. Never show his face —
> there isn't one.

---

## 5 · Environment plates

**FOREST / FIRE** — `ancient old-growth forest of vast curving trunks and hanging moss, warm
ember firelight, drifting sparks and smoke`
**MARSH / REEDS** — `a still teal marsh at dawn, banded mist over dark water, tall reeds, a
stilt-and-raft village strung with teal lanterns`
**MOOR / THE RINGS** — `a wide bleak moor under low cloud, a broken circle of tall standing
stones, bone-pale grass, the shattered sky-ring hanging directly above the broken circle`
**PEAKS / EYRIE** — `high jagged snow peaks, curving wind-streams in the air, nests on rock
ledges, storm-violet light`
**THE CAGE** — `a rigid iron structure of straight beams and hard facets cut into a mountainside,
tall iron posts, everything geometric and wrong against the curving rock`
**IRONFOLK FORGE** — `a vast soot-black industrial forge, furnace glow in forge-red, straight
gantries and angular machinery, no curve anywhere`
**THE STRAIGHT SCAR** — `a perfectly straight geometric cut gouged through curving forest and
hills to the horizon, burnt edges`
**THE RUINS** — `impossible ruins of a third geometry — neither organic curve nor iron
straight-line, smooth alien arcs and true circles, half-buried in earth`

---

## 6 · Motion grammar (video prompts)

Current video models generate a **single continuous shot**. Never ask for a cut inside a shot.
Each shot is one camera move on one subject. Cutting happens in the edit.

Preferred moves, in rough order of reliability:
- **slow push in** on a held subject (most reliable, most cinematic)
- **slow drift / parallax** across a landscape
- **slow tilt up** to reveal the Riven Sky (the series' signature move)
- **hold, with motion inside the frame only** — firelight flicker, embers rising, hair and
  cloth in wind, reeds moving, snow falling

Avoid: whip pans, fast dollies, orbiting, crowd choreography, hand close-ups, anything with
more than two figures doing distinct actions. These are where AI video breaks.

**Ambient motion to name explicitly**, because it sells the world: drifting embers and sparks,
smoke curling, the faint shimmer of the ring-light, breath in cold air, fur and feathers
ruffling, water moving under reeds.

---

## 7 · Consistency strategy — how 13 episodes stay one series

Text prompts alone will drift. The fix, in order of strength:

1. **Reference-locked generation (strongest).** Generate a small set of **reference plates** as
   still images first — one per principal character, one per environment. Then generate every
   video shot in **`element2video`** mode with the relevant plate(s) attached as identity
   references. This is what `element2video` exists for and it is the difference between a
   series and a pile of clips.
2. **The existing cover art is already canonical.** `ep-1cover.png` … `emberwild_ep10_cover_sleeping-ones.png`
   in the repo root are finished art in the locked style. Uploading them as reference images is
   the cheapest possible style lock — no generation needed to establish the look.
   ⚠️ Upload must be done by the account holder through OpenArt's upload picker; there is no
   programmatic upload available from this session.
3. **Verbatim character blocks** (§4) in every prompt.
4. **One tribe accent per scene** (§3).

**Recommended model split:**
- Reference plates → an image model. `kling-3-omni` text2image is the cheapest at **10 credits**;
  `byte-plus-seedream-4-5` at **15** is the better stylistic match (anime/2D-illustration leaning).
- Video shots → `byte-plus-seedance-2-fast` or `kling-3-omni` element2video, both of which take
  image identity references. `pixverseV6` is the cheapest video at 50 credits but has no
  element2video mode, so it cannot carry character identity — use it only for landscape plates.

---

## 8 · Cost reality

Priced from OpenArt's own quote at default configs, per **5-second shot**. Longer shots scale
roughly linearly, so a 10s shot ≈ double. **Video is the entire cost of this project.**

| Job | Model / config | Credits |
|---|---|---|
| Reference plate (image) | kling-3-omni text2image, 1K | **10** |
| Reference plate (image) | seedream-4-5 text2image, 2K | **15** |
| Video shot, 5s 540p, no audio | pixverseV6 | **50** |
| Video shot, 5s 720p | wan2-7 | **125** |
| Video shot, 5s, w/ sound + element refs | kling-3-omni | **175** |
| Video shot, 5s 720p, w/ audio | seedance-2-mini | **200** |
| Video shot, 5s 720p, w/ audio | seedance-2-fast | **350** |
| Video shot, 5s 720p, w/ audio | seedance-2.0 / grok-imagine | **400** |

### On the 24,000 credits/month plan

Two things about this plan matter more than the headline number.

**1. The unlimited image models make the entire image side free.** Nano Banana 2 Lite, Qwen
Image 3.0, MiniMax H3 and FLUX 3 are unlimited on this plan. Every reference plate, character
sheet, environment plate, thumbnail and poster costs **zero credits**. That means 100% of the
24,000 goes to video, and the reference-locking strategy in §7 — which is what holds the series
to one look — becomes free to iterate on. Generate reference plates until they are exactly
right; it costs nothing.

**2. "~300 videos" is optimistic.** 24,000 ÷ 300 = 80 credits per video, which only holds at the
cheapest tier. The real number depends entirely on model:

| Model (5s shot) | Credits | Shots / month | Episode trailers | Full episodes |
|---|---|---|---|---|
| pixverseV6 540p, no audio | 50 | **480** | 80 | 26.7 |
| wan2-7 720p | 125 | **192** | 32 | 10.7 |
| kling-3-omni + sound + element refs | 175 | **137** | 22 | 7.6 |
| seedance-2-mini 720p + audio | 200 | **120** | 20 | 6.7 |
| seedance-2-fast 720p + audio | 350 | **68** | 11 | 3.8 |
| seedance-2.0 / grok 720p | 400 | **60** | 10 | 3.3 |

### What one month buys, in Emberwild terms

| Model | T1 trailer + all ten T2 episode trailers (68 shots) | Full 13-episode series (234 shots) |
|---|---|---|
| pixverseV6 | 3,400 cr — **14% of one month** | 11,700 cr — **half a month** |
| wan2-7 | 8,500 cr — 35% of a month | 29,250 cr — 1.2 months |
| kling-3-omni | 11,900 cr — **half a month** | 40,950 cr — 1.7 months |
| seedance-2-mini | 13,600 cr — 57% of a month | 46,800 cr — 1.9 months |
| seedance-2-fast | 23,800 cr — one full month | 81,900 cr — 3.4 months |

**The recommendation: `kling-3-omni` element2video at 175/shot.** It is the cheapest model that
has *both* synchronized audio *and* `element2video` — the identity-reference mode that keeps Rook
looking like Rook across 234 shots. At that price, **month one delivers the series trailer plus
all ten episode trailers using half the allowance**, leaving ~12,000 credits to re-roll shots
that come out wrong. Re-rolls are not optional in AI video; budget a third of every run for them.

Then **the complete 13-episode series lands inside month two**, with the whole image side —
every reference plate and every re-roll of it — costing nothing throughout.

The plan's other relevant features: **~80 consistent characters** (Emberwild's principal cast is
14 — fits several times over), **32 parallel generations** (a 6-shot episode trailer renders in
one batch), **commercial use rights** and **watermark-free** (both required, since these drive
paid Payhip sales), and **Director** access, billed separately from the credit pool.

> ### Current account state: **Free plan, 40 credits.**
> The cheapest single video job costs **50 credits**, so **no video can be generated as it
> stands** — not one 5-second clip. Everything in this package is finished and runs the moment
> the plan is active.

---

## 9 · Audio

`seedance-2.x`, `kling-3-omni` and `gemini-omni-flash` generate synchronized audio.
Recommendation: **generate ambience only, not dialogue.** The comic's power is in its written
lines, and AI lip-sync on stylized 2D faces is where the illusion dies. Score and voice-over
should be laid over the cut in an editor instead. Where audio is generated, ask for:
*"ambient only — fire crackle, wind, reeds, distant low drone. No speech."*

---

## 10 · Decisions

- ~~**Aspect ratio.**~~ **DECIDED: 16:9 (YouTube).** The shot list is written natively for this
  ratio — the landscapes, the Riven Sky tilts and the Vane scale shots all depend on it. A
  vertical cut for Reels/Shorts remains possible later via `build_prompts.py --vertical`, but
  wide landscape drifts should be regenerated framed vertically rather than cropped.
- **Whether Act III's reveals may appear in T1.** The series trailer is strongest if it teases
  the fall from the sky — but the handoff notes say *"Ep9 'The Fallen Ring' is the big reveal…
  do not leak it before Act III."* The shot list keeps T1 clean of it; overriding that is the
  author's call.
- **Episodes 11–13** are roadmap-only in the comic and have no shot list here yet.

---
*Adapted from the comic Series Bible v2. The story is the point. The art serves it.*
