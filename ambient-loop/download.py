#!/usr/bin/env python3
"""Fetch the rendered clips listed in renders.json into clips/.

renders.json is a list of {"id", "slug", "url"} written as each OpenArt
generation completes. Files are named NN-slug.mp4 so the shot order and the
sort order in assemble.py are the same thing.
"""
import json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CLIPS = os.path.join(HERE, "clips")

CA = "/root/.ccr/ca-bundle.crt"

def fetch(url, dest):
    """curl, not urllib — the CDN 403s requests that bypass the agent proxy."""
    cmd = ["curl", "-sS", "-fL", "-o", dest, url]
    if os.path.exists(CA):
        cmd[1:1] = ["--cacert", CA]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"download failed for {url}\n{r.stderr}")


def main():
    manifest = os.path.join(HERE, "renders.json")
    if not os.path.exists(manifest):
        sys.exit("renders.json not found")
    entries = json.load(open(manifest))
    os.makedirs(CLIPS, exist_ok=True)

    for e in entries:
        dest = os.path.join(CLIPS, f"{e['id']}-{e['slug']}.mp4")
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            print(f"  have  {os.path.basename(dest)}")
            continue
        print(f"  get   {os.path.basename(dest)}")
        fetch(e["url"], dest)

    have = len([f for f in os.listdir(CLIPS) if f.endswith(".mp4")])
    print(f"\n{have}/{len(entries)} clips in clips/")

if __name__ == "__main__":
    main()
