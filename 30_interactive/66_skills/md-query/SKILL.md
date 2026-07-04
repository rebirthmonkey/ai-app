---
name: md-query
description: Answer a question strictly from the perso knowledge base. Selects the most relevant perso category / sub-folder(s), analyzes that category's OPML mind map and the ingested articles in its `_raw/` sub-folders, and synthesizes an answer grounded ONLY in those sources (no external knowledge). Use when the user asks a question and wants it answered from their own perso notes and mind maps.
---

# md-query

Answer a question using **only** the perso knowledge base: the OPML mind maps and the ingested articles under `_raw/`. Do not use outside knowledge. If the knowledge base does not cover the question, say so explicitly instead of filling the gap.

## Sources of truth (only these)

- Perso root: `persospace/perso`
- Category mind maps: `perso/<category>/*.opml`
- Ingested articles: `perso/<category>/**/_raw/*.md` (each has an `## Abstract`, a `## 与脑图对比` chapter, and the article body)

Categories: `10_belief`, `20_thinking-framework`, `30_self-management`, `40_eq`, `50_goal`.

## Workflow

```
- [ ] Step 1: Index the knowledge base
- [ ] Step 2: Pick the most related category / sub-folder(s)
- [ ] Step 3: Analyze the mind map
- [ ] Step 4: Analyze related _raw articles
- [ ] Step 5: Synthesize a grounded answer
```

### Step 1: Index the KB

```bash
python3 scripts/list_kb.py persospace/perso
```

This prints each category's OPML file(s) and the `_raw` articles available.

### Step 2: Select the most related area

From the question's key concepts, choose the most relevant category (and sub-folder if applicable). Pick more than one only when clearly relevant; prefer precision over breadth.

### Step 3: Analyze the mind map

Extract the relevant OPML outline (reuse the md-understand parser — do NOT read the raw XML):

```bash
python3 ../md-understand/scripts/opml_outline.py "persospace/perso/<category>/<file>.opml"
# --flat for keyword matching
```

Identify the branches / nodes that address the question and note their node paths (for citation).

### Step 4: Analyze related _raw articles

Find and read the relevant ingested articles:

```bash
# discover
ls "persospace/perso/<category>"/**/_raw/*.md 2>/dev/null
# keyword search across all ingested articles in the category
rg -l "<keyword>" "persospace/perso/<category>"/**/_raw/*.md
```

Read each candidate's `## Abstract` first to gauge relevance, then the specific body sections that bear on the question. Note article title + section for citation.

### Step 5: Synthesize a grounded answer

Write the answer from the mind map + `_raw` articles only:

- Every substantive claim must trace to a source — cite mind-map node paths and article titles (with section).
- Prefer the knowledge base's own framing and wording.
- If sources conflict or only partially cover the question, say so.
- **If the KB lacks enough to answer, state what is missing. Do NOT substitute external knowledge.**

Answer template (match the question's language):

```markdown
## 回答
<answer grounded in the KB>

## 依据
- 脑图：`<category>/<file>.opml` › <node path>
- 文章：<article title> › <section>

## 知识库缺口（如有）
- <what the KB does not cover>
```

## Notes

- Grounding is strict: this is retrieval over the user's own notes, not a general answer.
- The KB is in Chinese; match on meaning, not exact wording.
- If Step 1 shows a category has no OPML or no `_raw` articles, rely on whichever exists; if neither exists for the relevant area, report the gap.
