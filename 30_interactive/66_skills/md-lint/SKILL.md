---
name: md-lint
description: Review an OPML mind map and propose concrete improvements based on general domain knowledge and the MECE principle (Mutually Exclusive, Collectively Exhaustive). Each run proposes 10 prioritized, actionable improvements (overlaps, gaps, mis-grouping, naming, granularity, ordering, missing branches). Re-running proposes the NEXT 10 improvements without repeating earlier ones, tracked in a sidecar `<name>.lint.md` report. Use when the user asks to lint, review, critique, or improve a mind map / opml file.
---

# md-lint

Audit an OPML mind map and output **10 improvement proposals per run**, grounded in (a) general knowledge of the subject and (b) the **MECE** principle. Successive runs continue where the last left off — proposing the *next* 10 — so the map can be refined incrementally.

## Workflow

```
- [ ] Step 1: Resolve the report file + read prior rounds (avoid repeats)
- [ ] Step 2: Load the mind-map outline
- [ ] Step 3: Analyze (general knowledge + MECE) → find issues
- [ ] Step 4: Write the next 10 proposals as a new round in the report
- [ ] Step 5: Summarize to the user
```

### Step 1: Report state (enables "next 10" on re-run)

Every run appends a numbered **round** of 10 proposals to a sidecar report that lives next to the OPML:

```
<opml_dir>/<opml_stem>.lint.md
```

Check the current state first:

```bash
python3 scripts/lint_report.py "path/to/map.opml"
```

It prints the report path, whether it exists, how many rounds/items already exist, and the titles of all prior proposals. **Read those prior titles** and make the new 10 non-overlapping (cover new nodes / new issue types). If the report does not exist yet, this is Round 1.

### Step 2: Load the mind-map outline

Do NOT read the raw OPML XML (it is large and URL-encoded). Use the parser:

```bash
python3 scripts/opml_outline.py "path/to/map.opml"          # indented tree
python3 scripts/opml_outline.py "path/to/map.opml" --flat   # one node per line
python3 scripts/opml_outline.py "path/to/map.opml" --notes  # include node notes
```

Study the structure: the top-level branches, their children, depth, and how nodes are grouped.

### Step 3: Analyze — general knowledge + MECE

Evaluate the map on two axes and hunt for concrete, node-specific issues.

**MECE checks:**
- **Overlap (not Mutually Exclusive):** two branches/nodes cover the same idea → merge or re-scope.
- **Gaps (not Collectively Exhaustive):** an important part of the topic is missing at a given level → add a branch.
- **Mixed dimensions:** siblings split by inconsistent criteria (e.g. mixing "by phase" with "by tool") → pick one classification axis per level.
- **Mis-placement:** a node sits under the wrong parent.
- **Granularity imbalance:** one branch is 5 levels deep, a sibling is a single leaf → rebalance.

**General-knowledge checks:**
- Missing well-known concepts/frameworks/subtopics a domain expert would expect.
- Outdated, incorrect, or vague node labels.
- Naming inconsistency (mixed language, verb vs. noun phrasing, abbreviations).
- Ordering that doesn't follow a natural logic (chronological, priority, general→specific).

Prioritize the 10 that give the biggest structural clarity gain. Prefer specific ("merge X and Y under Z") over generic advice.

### Step 4: Write the next 10 proposals (a new round)

Append a new `## Round N` section to the report. Use the report's language to match the mind map (Chinese map → Chinese proposals). Each item:

```markdown
## Round <N> — <YYYY-MM-DD>

1. **[类型] 简短标题** — 针对节点「<节点路径>」：问题说明。建议：具体改法。
2. ...
10. ...
```

`[类型]` tags (choose the fitting one): `重叠` (overlap) · `遗漏` (gap) · `维度混杂` (mixed dimension) · `错位` (mis-placement) · `粒度` (granularity) · `命名` (naming) · `排序` (ordering) · `更新` (outdated/incorrect).

Rules:
- Exactly **10** items per round.
- None may duplicate a prior round's proposal (you already read them in Step 1).
- Reference actual node names/paths from the map so each suggestion is actionable.
- Do not edit the OPML itself — this skill only proposes. (If the user then asks to apply changes, that's a separate action.)

### Step 5: Summarize

Tell the user: which round this was, the report path, and a 2–3 line highlight of the most impactful proposals. Mention they can re-run md-lint for the next 10.

## Notes

- One OPML per run.
- The `<name>.lint.md` report is the memory that makes "next 10 on re-run" work — never overwrite it, always append a new round.
- If the user explicitly asks to "start over", they can delete the report (or say so) and Round numbering restarts.
- Keep proposals concrete and grounded in the map's actual nodes; avoid generic mind-mapping platitudes.
