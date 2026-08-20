#!/usr/bin/env python3
"""EMBERWILD — assemble ready-to-send OpenArt prompts from shots.json.

The whole point: every prompt is built the same way, so 68 shots across 11 sequences
stay one series instead of 68 unrelated clips.

    prompt = shot text + character blocks + STYLE BLOCK

Usage
    python3 build_prompts.py                     # every sequence, human-readable
    python3 build_prompts.py T1_series_trailer   # one sequence
    python3 build_prompts.py --safe              # skip Act III spoiler sequences (ep9, ep10)
    python3 build_prompts.py --json T2_ep01      # params objects ready for openart_generate_video
    python3 build_prompts.py --vertical          # add 9:16 framing guidance
    python3 build_prompts.py --cost              # what the selected shots cost, per model
"""
import json, sys, pathlib

HERE = pathlib.Path(__file__).parent
D = json.loads((HERE / "shots.json").read_text())

VERTICAL = ", vertical composition, subject centred, generous headroom"

# credits per 5s shot, from OpenArt's own quote at default config
COST = {"pixverseV6": 50, "wan2-7": 125, "kling-3-omni": 175,
        "byte-plus-seedance-2-mini": 200, "byte-plus-seedance-2-fast": 350,
        "byte-plus-seedance-2": 400}


def build(shot, vertical=False):
    """shot text + character blocks + style block."""
    parts = [shot["shot"]]
    for name in shot["characters"]:
        block = D["character_blocks"].get(name)
        if block:
            parts.append(block)
    text = ", ".join(parts)
    if vertical:
        text += VERTICAL
    return text + ", " + D["style_block"]


def select(keys, safe=False):
    out = {}
    for k, v in D["sequences"].items():
        if keys and k not in keys:
            continue
        if safe and not v["spoiler_safe"]:
            continue
        out[k] = v
    return out


def main():
    args = [a for a in sys.argv[1:]]
    flags = {a for a in args if a.startswith("--")}
    keys = [a for a in args if not a.startswith("--")]
    vertical = "--vertical" in flags
    seqs = select(keys, safe="--safe" in flags)

    if not seqs:
        sys.exit(f"no sequences matched. available: {', '.join(D['sequences'])}")

    if "--cost" in flags:
        n = sum(len(v["shots"]) for v in seqs.values())
        print(f"{n} shots across {len(seqs)} sequence(s), at 5s each\n")
        for model, c in sorted(COST.items(), key=lambda x: x[1]):
            print(f"  {model:30} {c:>4} cr/shot  ->  {n * c:>6} cr")
        print(f"\n  budget one re-roll in three: {int(n * 1.33) * 175:>6} cr "
              f"at the recommended kling-3-omni")
        return

    if "--json" in flags:
        jobs = []
        for k, v in seqs.items():
            for s in v["shots"]:
                jobs.append({
                    "sequence": k, "shot": s["n"], "beat": s["beat"],
                    "model": D["defaults"]["recommended_model"],
                    "mode": D["defaults"]["mode"],
                    "params": {"prompt": build(s, vertical),
                               "duration": D["defaults"]["duration_s"]},
                    "motion_note": s["motion"],
                    "reference_plates": s["characters"] + ([s["environment"]] if s["environment"] else []),
                })
        print(json.dumps(jobs, indent=2, ensure_ascii=False))
        return

    for k, v in seqs.items():
        spoiler = "" if v["spoiler_safe"] else "   [ACT III SPOILER - not for pre-Act-III marketing]"
        print(f"\n{'=' * 78}\n{v['title']}  ({len(v['shots'])} shots, ~{v['runtime_s']}s, accent {v['accent']}){spoiler}\n{'=' * 78}")
        for s in v["shots"]:
            refs = ", ".join(s["characters"] + ([s["environment"]] if s["environment"] else [])) or "none"
            print(f"\n--- shot {s['n']} · {s['beat']}")
            print(f"    motion: {s['motion']}")
            print(f"    plates: {refs}")
            print(f"    prompt: {build(s, vertical)}")
    n = sum(len(v["shots"]) for v in seqs.values())
    print(f"\n{'=' * 78}\n{n} shots ready. Guards: " + " | ".join(D["continuity_guards"][:3]))


if __name__ == "__main__":
    main()
