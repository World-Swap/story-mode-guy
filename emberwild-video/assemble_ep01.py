#!/usr/bin/env python3
"""Assemble EMBERWILD Episode One from its 41 shots.

Reads shots_ep01.json for the caption of every shot (lifted verbatim from the
author's script) and cuts the shots together in order, substituting any shot
that was re-rolled during QA.
"""
import json, pathlib, sys
from assemble import build, probe, SHOTS as _unused

HERE = pathlib.Path(__file__).parent
SRC = HERE / "shots_ep01"
REROLL = HERE / "shots_out"

# QA re-rolls that supersede the original render
SUBS = {
    17: REROLL / "rr17_alone-at-the-fire.mp4",
    29: REROLL / "rr29_same-place-the-sky-went.mp4",
    34: REROLL / "rr34_the-wrong-light.mp4",
    39: REROLL / "rr39_new-land.mp4",
}

def main():
    ep = json.loads((HERE / "shots_ep01.json").read_text())
    ordered = sorted(ep["shots"], key=lambda s: s["n"])
    by_n = {}
    for p in sorted(SRC.glob("*.mp4")):
        by_n[int(p.stem.split("_")[1])] = p

    clips, captions = [], {}
    for idx, s in enumerate(ordered):
        n = s["n"]
        path = SUBS.get(n) or by_n.get(n)
        if path is None or not path.exists():
            sys.exit(f"missing shot {n}")
        clips.append(path)
        if s.get("caption"):
            captions[idx] = s["caption"]

    out = build(clips, captions, HERE / "EMBERWILD_Ep01_The-Bonding.mp4",
                title="EMBERWILD", subtitle="Episode One — The Bonding")
    print(f"wrote {out.name}  {out.stat().st_size//1024//1024} MB  {probe(out):.1f}s")
    print(f"{len(clips)} shots, {len(captions)} captions, "
          f"{len(SUBS)} re-rolled: {sorted(SUBS)}")

if __name__ == "__main__":
    main()
