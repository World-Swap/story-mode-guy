# EMBERWILD — Shot List
Companion to `EMBERWILD_VIDEO-BIBLE.md`. Every prompt below is **shot text only**.
The full generation prompt is always:

> `SHOT TEXT` + `, ` + **STYLE BLOCK** (bible §3) + any **character blocks** (bible §4) named in the shot.

`build_prompts.py` assembles these automatically from `shots.json`.

**Default shot length: 5 seconds.** Ten shots ≈ 50s of cut footage before trims.
**Mode: `element2video`** with the relevant reference plate attached (bible §7) — not `text2video`,
except for the pure-landscape plates where no character identity is at stake.

---

## T1 · SERIES TRAILER — 8 shots, ~40s
The one hero asset. Covers the whole arc without leaking Act III. Ends on the Pact.

| # | Beat | Shot text | Motion |
|---|---|---|---|
| 1 | The world is curves | `a vast old-growth forest of enormous curving trunks and hanging moss at dusk, a shattered ring of pale silver light arcing across the whole sky above the canopy, broken into segments` | slow tilt up from forest floor to the broken ring |
| 2 | The bond | SORREL + MOTH — `a wiry thirteen-year-old girl kneeling at a bonfire at night, a small silver-and-orange horned lynx cub stepping out of the flames toward her, sparks rising between them` | slow push in, firelight flicker, embers rising |
| 3 | The straight line arrives | `a perfectly straight geometric cut gouged through curving forest to the horizon, edges still burning, black smoke rising in straight columns` | slow drift along the scar |
| 4 | Fire | ROOK + CINDER — `a young man with wind-blown dark hair and a large scarred horned wildcat running through burning forest at night, orange firelight, embers filling the air` | tracking push, heavy ember particles |
| 5 | Not the last | SEDGE — `a wary man in reed-teal marsh clothing standing in a pole-boat among tall reeds at dawn, a long green serpent coiled about his shoulders, banded mist over dark water` | slow push in, mist drifting, reeds moving |
| 6 | The enemy | VANE — `a towering figure of hard flat angular iron plates and diamond rivets, no eyes, a full-width forge-red glow slit across the helm, standing motionless in soot-black smoke, dwarfing everything around him` | very slow push in, smoke only — he does not move |
| 7 | The mystery | `a broken circle of tall standing stones on a bleak moor under low cloud, the shattered silver sky-ring hanging directly above the broken circle, bone-pale grass moving in wind` | slow tilt up from stones to the ring above |
| 8 | The Pact | ROOK — `a young man's hand holding a curved bone knife over a knotted record-cord by firelight, tribal tattoos on his forearm, warm ember light` | slow push in on the knife, firelight flicker |

---

## T2 · EPISODE TRAILERS — 6 shots each, ~30s each

### EP 1 — The Bonding · ember `#e8662e`
> *"To bond is to stop being alone."*

| # | Shot text | Motion |
|---|---|---|
| 1 | `a Vael forest camp at night, a great bonfire ringed by figures in hide and bone, vast curving trunks behind, the shattered silver sky-ring overhead` | slow drift around the fire |
| 2 | SORREL — `a wiry thirteen-year-old girl stepping alone toward a tall bonfire, firelight on her face, uncertain and brave` | slow push in on her face |
| 3 | MOTH — `a small silver-and-orange horned lynx cub stepping out through the flames of a bonfire, sparks scattering around it` | hold, flames and sparks moving |
| 4 | `dawn over a forest canopy, a single straight column of black smoke rising on the far horizon, everything else curved` | slow tilt from canopy to the smoke |
| 5 | ROOK + CINDER — `a young man with a curved bone knife and a large scarred horned wildcat leading a column of tribespeople west through burning forest` | tracking drift, embers falling |
| 6 | SEDGE — `a hooded figure with a serpent coiled at his shoulders standing on the far bank of a wide river at dusk, watching, mist on the water` | slow push in across the water |

### EP 2 — Strangers in the Reeds · reed-teal `#2f8f7a`
> *"We thought we were the last."*

| # | Shot text | Motion |
|---|---|---|
| 1 | `a still teal marsh at dawn, banded mist lying over dark water, tall reeds, everything soft and curved` | slow drift through the reeds |
| 2 | SEDGE — `a wary man in reed-teal and bone lowering his hood in a pole-boat, marsh-dry expression, a green serpent moving across his shoulders` | slow push in |
| 3 | `a stilt-and-raft village strung with teal lanterns standing over dark marsh water at dusk, rope bridges curving between platforms` | slow parallax drift past the huts |
| 4 | BRACKEN — `a straight-backed older matriarch in teal and bone robes on a raft deck, a great pale serpent coiled at her feet, guarded expression` | hold, lantern light and water moving |
| 5 | ROOK + BRACKEN — `two groups of tribespeople facing each other across dark water at dusk, one in ember-orange hide, one in reed-teal, neither moving` | very slow push in |
| 6 | WREN — `a nineteen-year-old marsh woman with cropped dark hair holding a thick bundle of knotted record-cords, alone, no creature beside her, teal lantern light` | slow push in on the cords |

### EP 3 — Old Wounds · teal + ember, ring-silver dominant
> *"Two tribes who each thought they were the last. One knife to undo it all."*

| # | Shot text | Motion |
|---|---|---|
| 1 | `a wide bleak moor under low cloud, a broken circle of tall standing stones, bone-pale grass, the shattered silver sky-ring hanging directly above the broken circle` | slow drift toward the stones |
| 2 | SORREL + MOTH — `a girl and a small horned lynx cub inside a circle of standing stones, a faint warm glow passing between them, stronger than the light around` | hold, glow pulsing gently |
| 3 | WREN — `a nineteen-year-old marsh woman standing alone at the exact centre of a broken stone circle, arms at her sides, looking up, nothing beside her` | very slow push in, grass moving |
| 4 | `a column of angular iron-armoured figures advancing in a perfectly straight line across a curving moor toward standing stones` | slow lateral drift, rigid formation |
| 5 | `a single tall iron-masked figure pausing among standing stones and turning to look back at them as it withdraws` | hold, then the turn — this is the whole shot |
| 6 | ROOK + BRACKEN — `a curved bone knife laid across a knotted record-cord on stone, two pairs of hands above it, firelight in a stone hollow` | slow push in on the knife and cord |

### EP 4 — The Sky Cage · storm-violet `#6d6f9c`

| # | Shot text | Motion |
|---|---|---|
| 1 | `high jagged snow peaks under a storm-violet sky, curving wind-streams visible in the air, the shattered silver sky-ring above` | slow drift across the peaks |
| 2 | KESTREL — `a proud clan leader in storm-violet and bone with a feathered shoulder mantle standing on a rock ledge beside a huge violet-grey storm-bird, wind in the feathers` | slow push in, feathers ruffling |
| 3 | `a rigid iron structure of straight beams and hard facets cut into a curving mountainside, tall iron posts along a straight road, geometric and wrong against the rock` | slow drift along the straight road |
| 4 | `tall iron posts lighting up one after another in cold blue as a figure passes, the light running away down the line` | hold, the light runs down the posts |
| 5 | HALCYON — `a very old seated figure in storm-violet robes in a clean bare iron room, hands folded, calm unreadable face, one hard straight light above` | very slow push in |
| 6 | SHRIKE — `a hooded one-eyed man in weathered storm-violet turning his back on a snow mountain and walking downhill toward distant firelight, no bird beside him` | tracking behind him, snow falling |

### EP 5 — The Deserter · soot + forge-red
> *"You got the fire. We got the ash."*

| # | Shot text | Motion |
|---|---|---|
| 1 | `a cornered angular iron-armoured figure backed against rock at night, firelight on the flat plates, hands open and empty` | slow push in |
| 2 | ASH — `a gaunt soot-grey woman with hair shorn to stubble and an angular brand half-filed off her own brow, an iron mask lowered in her hands, firelight on her face` | slow push in on her face |
| 3 | `a vast soot-black forge interior, furnace glow in forge-red, straight gantries and angular machinery, small figures of children in a rigid line` | slow drift into the forge |
| 4 | SHRIKE + ASH — `a hooded one-eyed man in storm-violet and a gaunt soot-grey shorn woman sitting opposite each other by a fire, neither with any creature beside them` | hold, firelight flicker |
| 5 | ROOK — `a young man standing between a gaunt soot-grey woman and a crowd of angry tribespeople, arms loose at his sides, refusing to move` | very slow push in |
| 6 | SORREL + ASH — `a thirteen-year-old girl looking up at a gaunt shorn woman by firelight, the woman's face breaking` | slow push in on the woman's face |

### EP 6 — The Straight Scar · iron grey `#4a4d55` + forge-red

| # | Shot text | Motion |
|---|---|---|
| 1 | `a perfectly straight geometric cut running through curving forest and hills all the way to the horizon, seen from high above` | slow descent toward the scar |
| 2 | `a small line of tribespeople walking along the edge of an enormous straight gouge in the earth, dwarfed by it` | slow drift, tiny figures |
| 3 | `a vast soot-black industrial forge under a sky of straight smoke columns, furnace glow in forge-red` | slow push in toward the forge |
| 4 | `an enormous angular cutting machine of flat iron plates and diamond rivets grinding forward, throwing sparks, no curve anywhere on it` | slow lateral tracking, sparks |
| 5 | VANE — `a towering figure of hard flat angular iron plates, no eyes, a full-width forge-red glow slit across the helm, a tall crest fin, filling the frame and cropped by it` | very slow push in — he does not move |
| 6 | VANE — `a perfectly straight iron command rod held level against a background of curving smoke and curving hills` | hold, only the smoke moves |

### EP 7 — The Long Winter · ember dimmed, bone-white

| # | Shot text | Motion |
|---|---|---|
| 1 | `a gathered camp of many tribes under heavy snow at dusk, fires burnt low, the shattered silver sky-ring faint above the cloud` | slow drift across the camp |
| 2 | `empty storage baskets and bare drying racks in snow, a thin fire, figures huddled` | slow push in |
| 3 | CINDER — `a large scarred horned wildcat lying on its side by a low fire, breathing shallowly, its fur dull` | hold, shallow breathing, firelight |
| 4 | ROOK + CINDER — `a young man sitting on the ground beside a sick horned wildcat, one hand on its ribs, head down` | very slow push in |
| 5 | BRAM + ROOK — `a headstrong young man squared off against a young chief in falling snow, a crowd of tribespeople watching in silence` | hold, snow falling |
| 6 | ROOK — `a young man's face in cold firelight, breath clouding, saying nothing comforting` | slow push in |

### EP 8 — The Ruins That Shouldn't Be · ring-silver dominant

| # | Shot text | Motion |
|---|---|---|
| 1 | `figures standing at the foot of an impossible ruin of smooth alien arcs, neither organic curves nor iron straight lines, half-buried in earth, vastly larger than anything around` | slow tilt up the structure |
| 2 | `a perfect true circle burnt into open ground, exact and geometric, unlike anything else in the landscape` | slow descent looking straight down |
| 3 | `figures with lanterns descending into a smooth curved corridor of pale material, warm lantern light on alien surfaces` | slow push in down the corridor |
| 4 | `a wall of smooth pale material carrying markings that are neither curved Vael forms nor angular iron forms, lantern light raking across them` | slow lateral drift along the wall |
| 5 | HALCYON — `a very old figure in storm-violet robes reaching out to touch markings on a smooth pale wall, lantern light, recognition on their face` | slow push in on the hand and face |
| 6 | `an enormous smooth curved shape receding into darkness far below, lantern light reaching only a fraction of it` | slow tilt down into the dark |

### EP 9 — The Fallen Ring · ring-silver `#bcd4e2`
> Act III reveal. **Do not use these shots in T1 or in any pre-Act-III marketing.**

| # | Shot text | Motion |
|---|---|---|
| 1 | `bare scraped stones in open ground, deliberately cleared, an arc shape emerging from the earth beneath them` | slow descent, dust moving |
| 2 | `a vision of an unbroken ring of pale silver light complete and whole across a night sky, perfect and continuous` | very slow push in, the ring shimmering |
| 3 | `an enormous curved segment of pale silver material embedded deep in the earth, its scale filling the whole frame, earth and trees growing over it` | slow tilt along the segment |
| 4 | `figures standing tiny at the base of a vast fallen silver arc, looking up` | slow push in from behind the figures |
| 5 | `a wide shot of a landscape where the shattered ring in the sky and a buried arc in the ground are the same shape, one above and one below` | slow tilt from sky to ground |
| 6 | VANE — `a towering angular iron figure standing at the same buried silver arc, already there, unsurprised` | hold, only smoke moves |

### EP 10 — The Sleeping Ones · ring-silver + soot
> Act III reveal. Same restriction as Ep 9.

| # | Shot text | Motion |
|---|---|---|
| 1 | `a buried vessel of smooth pale material opened in the earth, warm lantern light spilling from a curved doorway into darkness` | slow push in toward the doorway |
| 2 | `a long corridor of smooth pale material curving away, lanterns held low, dust suspended in the air` | slow push in down the corridor |
| 3 | `rows of tall sealed pods of pale material receding into darkness, faint silver light inside each one` | slow lateral drift past the pods |
| 4 | `a face visible through the frosted surface of a sealed pod, still and sleeping, unmistakably one of the tribespeople` | very slow push in on the face |
| 5 | `figures standing among rows of sleeping pods, lantern light small against the scale of the chamber` | slow tilt up from the figures |
| 6 | `an eye opening behind the frosted surface of a sealed pod, silver light brightening` | hold — the eye opens. That is the shot. |

---

## Reframing notes

- **16:9 (YouTube).** Take the shot text as written. The landscapes, the Riven Sky tilts and the
  scale shots (T1/6, EP6/5, EP9/3) are all built for this ratio and lose most of their force in
  vertical.
- **9:16 (Reels / Shorts / TikTok).** Favour the single-figure shots and the vertical tilts.
  Add `, vertical composition, subject centred, generous headroom` to the shot text. Shots that
  survive the crop well: any push-in on a face, any tilt from ground to sky, EP4/4 (posts
  lighting down a line becomes a vertical run), EP10/4. Shots that do not: wide landscape
  drifts — regenerate those framed vertically rather than cropping them.

## Re-roll budget

Assume **one shot in three needs regenerating** — wrong number of fingers, a curve appearing on
Vane, a creature appearing beside Wren, drifting faces. Budget accordingly (bible §8). The
cheapest guard against re-rolls is a good reference plate, and on the 24,000-credit plan those
are free.

## Continuity guards — check every shot before accepting it

- **Wren has no bonded creature.** If anything animal is beside her, the shot is wrong.
- **Vane has no curves and no face.** A visible eye or a rounded pauldron means re-roll.
- **Vane is ~1.34× any Vael sharing his frame.** If he reads human-sized, re-roll.
- **The Riven Sky is broken.** A complete ring is only ever correct in EP9/2 as a vision.
- **The Ironfolk draw straight lines; nothing else does.** A straight-edged Vael object is wrong.
- **Ash's brand is half-filed off** — she did it herself. Not a clean brand, not no brand.
- **Moth is a cub** and stays small until the saga's later episodes.
