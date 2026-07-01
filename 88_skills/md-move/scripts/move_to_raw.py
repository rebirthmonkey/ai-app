#!/usr/bin/env python3
"""Move a Markdown article (and the figures it references) into <target_dir>/_raw/.

Usage:
    python3 move_to_raw.py <source.md> <target_dir>

- Creates <target_dir>/_raw/ (and any needed figures/ subdir) if missing.
- Moves image files referenced as ![](figures/...) or ![[figures/...]] from the
  article's sibling folder into <target_dir>/_raw/, preserving the relative path
  so the links keep working.
- Moves the .md into <target_dir>/_raw/.
- Refuses to overwrite an existing destination file.
"""
import os
import re
import shutil
import sys

# ![[target]]  or  ![alt](target)
IMG = re.compile(r"!\[\[([^\]]+?)\]\]|!\[[^\]]*\]\(([^)]+)\)")


def referenced_images(text: str) -> list[str]:
    refs: list[str] = []
    for m in IMG.finditer(text):
        ref = (m.group(1) or m.group(2) or "").strip()
        ref = ref.split("|", 1)[0].strip()   # drop Obsidian alias
        ref = ref.split(" ", 1)[0].strip()   # drop Markdown title
        if ref and not ref.startswith(("http://", "https://", "/", "#")):
            refs.append(ref)
    return refs


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(__doc__)
        return 1

    src = os.path.abspath(argv[1])
    target = os.path.abspath(argv[2])
    if not os.path.isfile(src):
        print(f"error: not a file: {src}", file=sys.stderr)
        return 2

    src_dir = os.path.dirname(src)
    raw = os.path.join(target, "_raw")
    dst_md = os.path.join(raw, os.path.basename(src))
    if os.path.exists(dst_md):
        print(f"error: destination already exists: {dst_md}", file=sys.stderr)
        return 3

    with open(src, encoding="utf-8") as f:
        text = f.read()
    refs = list(dict.fromkeys(referenced_images(text)))  # dedupe, keep order

    os.makedirs(raw, exist_ok=True)

    moved_imgs = 0
    issues: list[str] = []
    for ref in refs:
        src_img = os.path.normpath(os.path.join(src_dir, ref))
        dst_img = os.path.normpath(os.path.join(raw, ref))
        if not os.path.isfile(src_img):
            issues.append(f"{ref} (source missing)")
            continue
        if os.path.exists(dst_img):
            issues.append(f"{ref} (dest exists, skipped)")
            continue
        os.makedirs(os.path.dirname(dst_img), exist_ok=True)
        shutil.move(src_img, dst_img)
        moved_imgs += 1

    shutil.move(src, dst_md)

    print(f"moved article -> {dst_md}")
    print(f"moved {moved_imgs}/{len(refs)} referenced image(s) into {raw}/")
    if issues:
        print("unresolved refs:")
        for i in issues:
            print(f"  - {i}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
