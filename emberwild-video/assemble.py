#!/usr/bin/env python3
"""Assemble Emberwild shots into a finished cut.

The bundled ffmpeg has no drawtext (no freetype), so captions are rendered to
transparent PNGs with PIL and composited with the overlay filter. Caption styling
follows the comic's locked spec: cream text, dark ink outline, serif italic.

    python3 assemble.py                 # build the series trailer
    python3 assemble.py --no-captions   # clean cut, no burned-in text
"""
import subprocess, pathlib, sys, re, imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

FF = imageio_ffmpeg.get_ffmpeg_exe()
HERE = pathlib.Path(__file__).parent
SHOTS = HERE / "shots_out"
FONTS = pathlib.Path("/mnt/skills/examples/canvas-design/canvas-fonts")
FONT_CAP, FONT_TITLE = FONTS / "CrimsonPro-Italic.ttf", FONTS / "Gloock-Regular.ttf"
CREAM, GOLD, INK = (239, 228, 198), (242, 205, 132), (20, 16, 13)
W, H = 1280, 720


def has_audio(p):
    """Ep2 onward is generated with generateSound off, so clips have no audio stream."""
    err = subprocess.run([FF, "-i", str(p)], capture_output=True, text=True).stderr
    return "Audio:" in err


def probe(p):
    err = subprocess.run([FF, "-i", str(p)], capture_output=True, text=True).stderr
    h, m, s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err).groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


def text_png(text, path, font_path, size, colour, y_frac, wrap=46):
    """Transparent full-frame PNG with the text laid out per the comic caption spec."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    font = ImageFont.truetype(str(font_path), size)
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if len(trial) <= wrap:
            cur = trial
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    lh = int(size * 1.25)
    total = lh * len(lines)
    y0 = int(H * y_frac) - total // 2
    for i, line in enumerate(lines):
        bb = d.textbbox((0, 0), line, font=font)
        x = (W - (bb[2] - bb[0])) // 2 - bb[0]
        y = y0 + i * lh
        for dx in (-3, -2, 0, 2, 3):          # ink outline, per the panel spec
            for dy in (-3, -2, 0, 2, 3):
                if dx or dy:
                    d.text((x + dx, y + dy), line, font=font, fill=INK + (235,))
        d.text((x, y), line, font=font, fill=colour + (255,))
    img.save(path)
    return path


def build(clips, captions, out, title=None, subtitle=None):
    tmp = HERE / "_tmp"; tmp.mkdir(exist_ok=True)
    staged = []
    src_audio = any(has_audio(c) for c in clips)
    for i, c in enumerate(clips):
        dur = probe(c)
        st = tmp / f"s{i:02d}.mp4"
        cmd = [FF, "-y", "-i", str(c)]
        filt = []
        if i in captions:
            png = text_png(captions[i], tmp / f"cap{i:02d}.png", FONT_CAP, 44, CREAM, 0.80)
            cmd += ["-loop", "1", "-framerate", "24", "-t", f"{dur:.3f}", "-i", str(png)]
            fi, fo = 0.5, max(dur - 0.6, 1.0)
            filt.append(
                f"[1:v]format=rgba,fade=t=in:st={fi}:d=0.5:alpha=1,"
                f"fade=t=out:st={fo:.2f}:d=0.5:alpha=1[cap];[0:v][cap]overlay=0:0:shortest=1[v]")
        if i == 0:
            filt.append(("[v]" if filt else "[0:v]") + "fade=t=in:st=0:d=0.8[v]")
        if filt:
            cmd += ["-filter_complex", ";".join(filt), "-map", "[v]"]
            cmd += ["-map", "0:a"] if src_audio else ["-an"]
        cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "16"]
        if src_audio:
            cmd += ["-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2"]
        cmd += [str(st)]
        subprocess.run(cmd, capture_output=True, check=True)
        staged.append(st)

    if title:
        card, layers = tmp / "title.mp4", []
        text_png(title, tmp / "t1.png", FONT_TITLE, 108, GOLD, 0.44)
        cmd = [FF, "-y", "-f", "lavfi", "-i", f"color=c=0x14100d:s={W}x{H}:d=3.2"]
        if src_audio:
            cmd += ["-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo:d=3.2"]
        cmd += ["-loop", "1", "-framerate", "24", "-t", "3.2", "-i", str(tmp / "t1.png")]
        ti = 2 if src_audio else 1
        chain = f"[{ti}:v]format=rgba,fade=t=in:st=0.2:d=0.7:alpha=1,fade=t=out:st=2.5:d=0.6:alpha=1[t1];[0:v][t1]overlay=0:0[v1]"
        if subtitle:
            text_png(subtitle, tmp / "t2.png", FONT_CAP, 36, CREAM, 0.60)
            cmd += ["-loop", "1", "-framerate", "24", "-t", "3.2", "-i", str(tmp / "t2.png")]
            chain += f";[{ti+1}:v]format=rgba,fade=t=in:st=0.9:d=0.6:alpha=1,fade=t=out:st=2.5:d=0.6:alpha=1[t2];[v1][t2]overlay=0:0[v]"
        else:
            chain += ";[v1]null[v]"
        cmd += ["-filter_complex", chain, "-map", "[v]"]
        cmd += ["-map", "1:a", "-c:a", "aac", "-b:a", "192k"] if src_audio else ["-an"]
        cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-shortest", str(card)]
        subprocess.run(cmd, capture_output=True, check=True)
        staged.append(card)

    lst = tmp / "list.txt"
    lst.write_text("".join(f"file '{p.resolve()}'\n" for p in staged))
    subprocess.run([FF, "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                    "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)],
                   capture_output=True, check=True)
    return out


CAPTIONS = {
    1: "To bond is to stop being alone.",
    4: "We thought we were the last.",
    5: "So they bonded to iron instead.",
    6: "No living Vael remembers the sky whole.",
    7: "No one takes anyone. Ever again. We ask.",
}

if __name__ == "__main__":
    names = ["forest-tilt", "the-bond", "straight-scar", "fire-flight",
             "sedge-marsh", "vane", "the-rings", "the-pact"]
    clips = [SHOTS / f"T1_shot0{i}_{n}.mp4" for i, n in enumerate(names, 1)]
    missing = [c.name for c in clips if not c.exists()]
    if missing:
        sys.exit(f"missing shots: {missing}")
    caps = {} if "--no-captions" in sys.argv else CAPTIONS
    out = build(clips, caps, HERE / "EMBERWILD_series-trailer.mp4",
                title="EMBERWILD", subtitle="An original illustrated saga")
    print(f"wrote {out.name}  {out.stat().st_size//1024} KB  {probe(out):.1f}s")
