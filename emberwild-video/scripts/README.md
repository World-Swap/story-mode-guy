# Episode scripts

Source of truth for every episode's captions and dialogue.

Extracted from the finished comic PDFs in Google Drive (EMBERWILD folder) via the
Drive connector's `read_file_content`, which returns the lettering as text — speaker
names, balloon copy, caption boxes and page numbers all survive.

**Use these verbatim.** The comic's written lines are the reason the saga works; the
video adaptation must not paraphrase them. Where a shot needs a caption, lift it from
here rather than rewriting it.

One caveat: balloons within a page come out in layout order, not reading order, so the
lines inside a page sometimes appear shuffled. Re-sequence against the page's dramatic
logic when writing shots — the wording is exact, the ordering is not.

## Two kinds of source

**Author-supplied full scripts are the source of truth** where they exist. They carry panel
descriptions, correct reading order, and the artist's staging notes — everything the PDF
extraction loses. Episodes 1 and 2 have them.

PDF extraction is the fallback for the rest. It recovers the exact wording but scrambles
balloon order within a page and carries no panel direction. A `_PDF-EXTRACT` suffix marks
a file that came from a PDF rather than from the author.

## Availability

| Ep | Title | Script source | Status |
|---|---|---|---|
| 1 | The Bonding | `ep01_the-bonding.txt` | supplied by the author |
| 2 | Strangers in the Reeds | `ep02_strangers-in-the-reeds.txt` | **author-supplied** (full script with panel directions) |
| 3 | Old Wounds | Drive PDF | extractable |
| 4 | The Sky Cage | Drive PDF + .md | extractable |
| 5 | The Deserter | Drive PDF | extractable |
| 6 | The Straight Scar | Drive PDF | extractable |
| 7 | The Long Winter | Drive PDF | extractable |
| 8 | The Ruins That Shouldn't Be | Drive PDF + .md | extractable |
| 9 | The Fallen Ring | Drive PDF | extractable |
| 10 | The Sleeping Ones | Drive PDF | extractable |

Episode 1's PDF and script are in neither the `EMBERWILD`, `EMBERWILD - FINAL`, nor
`emberwild-final` Drive folders. The project handoff notes place them in a Claude
project workspace (`/mnt/project`, `/mnt/user-data/outputs`) that this session cannot
reach. **To build Episode 1, add its PDF or script to the Drive EMBERWILD folder.**
