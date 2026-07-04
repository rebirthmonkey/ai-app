#!/usr/bin/env python3
"""Print a readable indented outline from an OPML mind map (e.g. Mubu export).

The readable content of each node lives in its `text` attribute; the raw XML
also carries large URL-encoded `_mubu_*` attributes that are not worth reading.
This script strips all that and prints just the outline.

Usage:
    python3 opml_outline.py <file.opml> [--flat] [--notes]

    (default)  indented tree of node text
    --flat     one node text per line, no indentation (handy for matching)
    --notes    also print each node's _note when present
"""
import sys
import xml.etree.ElementTree as ET


def iter_outlines(node, depth=0):
    for child in node.findall("outline"):
        yield depth, child
        yield from iter_outlines(child, depth + 1)


def main(argv: list[str]) -> int:
    flags = {a for a in argv[1:] if a.startswith("--")}
    args = [a for a in argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 1

    path = args[0]
    try:
        root = ET.parse(path).getroot()
    except (OSError, ET.ParseError) as exc:
        print(f"error: {path}: {exc}", file=sys.stderr)
        return 2

    body = root.find("body")
    if body is None:
        print("error: no <body> element in OPML", file=sys.stderr)
        return 2

    flat = "--flat" in flags
    show_notes = "--notes" in flags

    for depth, node in iter_outlines(body):
        text = (node.get("text") or "").strip()
        line = text if flat else ("  " * depth + "- " + text)
        if show_notes:
            note = (node.get("_note") or "").strip()
            if note:
                line += f"  [note: {note}]"
        print(line)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv))
    except BrokenPipeError:
        # Downstream (e.g. `head`) closed the pipe; exit quietly.
        try:
            sys.stdout.close()
        except Exception:
            pass
        raise SystemExit(0)
