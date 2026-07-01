#!/usr/bin/env python3
"""Index the perso knowledge base: each category's OPML mind maps and _raw articles.

Usage:
    python3 list_kb.py <perso_root>

Prints, per top-level category directory, the OPML files and the Markdown
articles living inside any `_raw/` sub-folder. This is the menu of grounding
sources available to answer a question.
"""
import os
import sys


def scan(catdir: str, root: str):
    opmls: list[str] = []
    raws: list[str] = []
    for dirpath, dirnames, filenames in os.walk(catdir):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        in_raw = "_raw" in os.path.relpath(dirpath, root).split(os.sep)
        for fn in filenames:
            rel = os.path.relpath(os.path.join(dirpath, fn), root)
            low = fn.lower()
            if low.endswith(".opml"):
                opmls.append(rel)
            elif low.endswith(".md") and in_raw:
                raws.append(rel)
    return sorted(opmls), sorted(raws)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 1
    root = argv[1]
    if not os.path.isdir(root):
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2

    for cat in sorted(os.listdir(root)):
        catdir = os.path.join(root, cat)
        if not os.path.isdir(catdir) or cat.startswith((".", "_")):
            continue
        opmls, raws = scan(catdir, root)
        print(f"# {cat}")
        if opmls:
            print("  opml:")
            for o in opmls:
                print(f"    - {o}")
        if raws:
            print("  _raw articles:")
            for r in raws:
                print(f"    - {r}")
        if not opmls and not raws:
            print("  (no opml / _raw articles yet)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
