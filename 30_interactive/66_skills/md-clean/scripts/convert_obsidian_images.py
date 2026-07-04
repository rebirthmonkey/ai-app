#!/usr/bin/env python3
"""Convert Obsidian embed image syntax to standard Markdown.

    ![[path/to/img.png]]          -> ![](path/to/img.png)
    ![[path/to/img.png|alt text]] -> ![alt text](path/to/img.png)

Edits the file in place and prints the number of conversions.

Usage:
    python3 convert_obsidian_images.py <file.md> [<file2.md> ...]
"""
import re
import sys

# ![[target]] or ![[target|alt]] ; target/alt may contain anything but ] or |
EMBED = re.compile(r"!\[\[([^\]|]+?)(?:\|([^\]]*))?\]\]")


def _replace(match: "re.Match[str]") -> str:
    target = match.group(1).strip()
    alt = (match.group(2) or "").strip()
    return f"![{alt}]({target})"


def convert(path: str) -> int:
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    new_text, count = EMBED.subn(_replace, text)
    if count:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_text)
    return count


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1
    total = 0
    for path in argv[1:]:
        try:
            n = convert(path)
        except OSError as exc:
            print(f"error: {path}: {exc}", file=sys.stderr)
            return 2
        total += n
        print(f"{path}: converted {n} image embed(s)")
    print(f"total: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
