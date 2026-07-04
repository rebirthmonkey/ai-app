---
name: md-ingest
description: End-to-end pipeline to ingest a web-clipped Markdown article into the perso knowledge base. Runs three skills in order — md-clean (strip boilerplate + fix image syntax), md-understand (add Abstract + mind-map comparison), md-move (file it into the right perso sub-folder under _raw). Use when the user wants to fully process/ingest a clipped article in one step, or mentions the whole clean→understand→move flow.
---

# md-ingest

Run the full ingestion pipeline on a clipped Markdown article by executing three sibling skills **in order**. Each stage depends on the previous one.

```
- [ ] Stage 1: md-clean       → strip boilerplate, convert ![[..]] to ![](..)
- [ ] Stage 2: md-understand   → prepend Abstract + 与脑图对比 chapter
- [ ] Gate:    confirm category → wait for user OK (or new category → redo Stage 2)
- [ ] Stage 3: md-move         → move into perso/<category>/<subfolder>/_raw/
```

Follow each stage by reading and applying that skill's `SKILL.md`, then continue to the next stage on the **same** article.

### Stage 1: md-clean

Read and follow [../md-clean/SKILL.md](../md-clean/SKILL.md) on the target article. Result: clean body, standard image links, frontmatter intact.

### Stage 2: md-understand

Read and follow [../md-understand/SKILL.md](../md-understand/SKILL.md) on the cleaned article. Result: an `## Abstract` and a `## 与脑图对比（…）` chapter at the top; classification chosen.

### Gate: confirm the category before moving

**Do NOT run Stage 3 automatically.** After Stage 2, stop and ask the user to confirm the chosen category / target sub-folder. State the classification md-understand picked and the target path Stage 3 would use, then wait.

- **User confirms** → proceed to Stage 3.
- **User proposes another category** → re-run Stage 2 (md-understand) with the user's category, replacing the previous `## 与脑图对比（…）` chapter (compare against that category's mind map). Then ask for confirmation again. Repeat until the user confirms.
- Do not proceed to Stage 3 without an explicit confirmation.

### Stage 3: md-move

Only after the user confirms: read and follow [../md-move/SKILL.md](../md-move/SKILL.md). It reads the 对比脑图 info Stage 2 wrote, resolves the target perso sub-folder, and moves the article (plus its figures) into `<target>/_raw/`.

**Note:** after Stage 3 the article no longer lives in its original location — report the final `_raw/` path to the user.

## Notes

- Run the stages strictly in order; do not skip. Stage 2 needs Stage 1's clean output, and Stage 3 needs the chapter Stage 2 writes.
- The category-confirmation gate is mandatory: never move the article before the user confirms the category.
- If the user supplied an explicit category/subtopic up front, still run the gate, but that category is the default proposal.
- Operate on one article per run unless the user asks for a batch.
