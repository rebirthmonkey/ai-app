#!/usr/bin/env python3
"""Resolve the md-lint sidecar report for an OPML file and summarize prior state.

The report lives next to the OPML as `<stem>.lint.md` and accumulates one
`## Round N` section (10 proposals) per md-lint run. This helper lets the skill
know what has already been proposed so a re-run can produce the *next* 10
without repeating earlier items.

Usage:
    python3 lint_report.py <file.opml>

Prints:
    REPORT: <absolute path to the .lint.md report>
    EXISTS: yes|no
    ROUNDS: <number of ## Round sections found>
    ITEMS:  <number of numbered proposals found>
    NEXT_ROUND: <ROUNDS + 1>
    ---
    PRIOR ITEMS:
    <each prior proposal's first line, so the agent can avoid duplicates>
"""
import os
import re
import sys

ROUND_RE = re.compile(r"^##\s+Round\s+\d+", re.IGNORECASE)
ITEM_RE = re.compile(r"^\s*\d+\.\s+(.*\S)")


def report_path_for(opml: str) -> str:
    d = os.path.dirname(os.path.abspath(opml))
    stem = os.path.splitext(os.path.basename(opml))[0]
    return os.path.join(d, f"{stem}.lint.md")


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 1

    opml = argv[1]
    report = report_path_for(opml)

    if not os.path.isfile(report):
        print(f"REPORT: {report}")
        print("EXISTS: no")
        print("ROUNDS: 0")
        print("ITEMS:  0")
        print("NEXT_ROUND: 1")
        return 0

    with open(report, encoding="utf-8") as f:
        lines = f.read().splitlines()

    rounds = sum(1 for ln in lines if ROUND_RE.match(ln))
    items = [m.group(1).strip() for ln in lines for m in [ITEM_RE.match(ln)] if m]

    print(f"REPORT: {report}")
    print("EXISTS: yes")
    print(f"ROUNDS: {rounds}")
    print(f"ITEMS:  {len(items)}")
    print(f"NEXT_ROUND: {rounds + 1}")
    print("---")
    print("PRIOR ITEMS:")
    for it in items:
        print(f"- {it}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
