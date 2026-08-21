# YouTube upload kit — Misty Rainforest

## Channel

**Name:** The Open Lands
**Handle:** @theopenlands
**Tagline:** Long nature ambience for your TV, hours at a time.

### About page description

```
Quiet places, on your screen, for hours at a time.

The Open Lands makes long, seamless ambient video for televisions — forests in fog, coastlines, rain on still water, open country. Gentle natural sound, no narration, no cuts. Just a window onto somewhere calm.

Every video is a true loop. Picture and sound run together for hours with no visible restart and no audible seam, so you can leave it on through dinner, a working afternoon, or a night's sleep.

New places added regularly. If there is somewhere you would like to sit for a few hours, say so in the comments.

All footage is created using generative AI.
```

### Title convention

Keep every upload on one pattern so the channel reads as a series and the
keywords stay in front:

```
{Place} — {N} Hours of {Sound} | Ambient Video for Your TV
```

The channel name carries the brand; the title carries the search terms. Do not
put "The Open Lands" in titles — it costs characters and earns nothing.

### Channel keywords

```
rain sounds, nature sounds, ambient video, tv screensaver, forest ambience,
nature loop, relaxing background, background video for tv
```

## Title

**Primary (55 chars):**
```
Misty Rainforest — 3 Hours of Rain & Forest Wind Sounds
```

Alternates:
```
Misty Rainforest Ambience — 3 Hours of Rain & Forest Wind | Sleep & Focus
3 Hours of Rain in an Old-Growth Rainforest — Ambient Video for Your TV
Rainforest Fog & Light — 3 Hour Ambience | Rain, Wind, Seamless Loop
```

Keywords are front-loaded. "Rain" carries far more search volume than any other
term available here, so it goes early.

---

## Description

```
Three hours of quiet old-growth rainforest — drifting fog, shafts of morning light, running water and rain on ferns, over a soft bed of rain and forest wind. No narration, no interruptions. Made to sit on a TV in a living room or bedroom and simply be there.

The sound is gentle and unchanging by design: nothing builds, nothing resolves, nothing asks for your attention.

▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

HOW TO USE IT
• Cast or AirPlay to your TV and set playback to loop
• Full screen, then leave it — the loop is seamless, with no visible restart
• Works well as a dinner-party backdrop, a reading or working background,
  or a calm screen to fall asleep to

WHAT'S IN IT
Fifteen scenes, cycling gently:
cathedral cedars in fog · moss-draped maple · a shallow creek over stones
· sword ferns in a breeze · a mossy waterfall · a nurse log · rain on needles
· a still reflecting pool · god-rays through the ferns · a slow river bend
· stream boulders · the canopy from below · rain rings on a pond
· dew on lichen · fog rolling through a conifer valley

DETAILS
• 3 hours 2 minutes, seamless loop in both picture and sound
• 1280×720, 16:9
• Rain and forest wind ambience, no narration
• No people, no animals, no text on screen

▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

This video was created using generative AI.

#rainsounds #ambience #rainforest #relaxing #sleepsounds
```

---

## Tags

```
rain sounds, rain sounds for sleeping, forest rain, rainforest ambience, rain
ambience, forest ambience, nature sounds, rain and wind sounds, misty forest,
3 hours rain sounds, ambient video, tv screensaver, background video for tv,
living room ambience, bedroom ambience, relaxing rain, calm background, sleep
sounds, study background, seamless loop
```

Paste as one comma-separated line. YouTube caps the field at 500 characters
across all tags — this set is well under, leaving room to add.

Tags are a weak ranking signal now; title, thumbnail and description do the
real work. Their remaining value is catching phrasings the title cannot hold,
so the list leans on search terms rather than describing the video again.

Tags live behind **SHOW MORE** at the bottom of the Details step, both in the
upload flow and when editing an existing video. Hashtags are separate: they go
in the description body, and the first three appear above the video title.

---

## Upload settings

| Field | Value |
|---|---|
| Category | Film & Animation (or People & Blogs) |
| Language | English |
| Comments | On — ambience channels get useful feedback on length and scenes |
| **Altered or synthetic content** | **Yes — must be disclosed** |
| End screen | Skip. It interrupts an ambience loop. |
| Cards | Skip, same reason. |

### On the AI disclosure

YouTube requires disclosing realistic synthetic content, and photorealistic
AI-generated nature footage is squarely in scope. Tick "Altered or synthetic
content" in the upload flow, and keep the line in the description. It is a
small label, not a demotion — and misdeclaring risks a strike on the channel.

### On the soundtrack

The bed is Forest Wind Summer with Rain On Rooftop mixed underneath at 55%,
both from the YouTube Audio Library, so the video carries no Content ID risk.

The audio is looped to exactly the length of the picture loop and its tail is
crossfaded onto its own head, the same wrap the picture uses. Both cycle
together every 3 minutes 30, so the three hours is one repeating unit rather
than two cycles drifting against each other. Measured at the junction, the
sample-to-sample jump is 1.00x the surrounding baseline — no click.

Rebuild or re-balance any time:

```sh
./add-audio.sh -w 1,0.55 "Forest Wind Summer.mp3" "Rain On Rooftop.mp3"
./make-long.sh 3 nature-loop-sound.mp4
```

Raise the second weight for a rain-forward mix, lower it for wind-forward.

### Pinned comment

```
Three hours, with no cuts and no repeat you can see or hear. If you want a
longer cut, or one scene on its own for an hour, tell me which and I'll make it.
```
