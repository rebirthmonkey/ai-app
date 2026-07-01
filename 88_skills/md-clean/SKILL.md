---
name: md-clean
description: Clean up Markdown articles clipped from the web (WeChat/公众号, blogs, etc.). Removes unrelated boilerplate (bylines, editor credits, ads, social CTAs, "继续滑动看下一个" footers) and converts Obsidian embed image syntax ![[XXX]] to standard Markdown ![](XXX). Use when the user asks to clean up, tidy, or normalize a clipped Markdown article, or mentions Obsidian clippings.
---

# Clean Web Markdown

Clean a Markdown article that was clipped from the internet so it contains only the real article content in portable, standard Markdown.

Two jobs:
1. **Convert Obsidian image embeds** `![[XXX]]` → standard Markdown `![](XXX)`.
2. **Remove unrelated boilerplate** (marketing, bylines, navigation cruft) while keeping the YAML frontmatter and the actual article body.

## Workflow

Copy this checklist and track progress:

```
- [ ] Step 1: Read the target file
- [ ] Step 2: Convert Obsidian image embeds (run the script)
- [ ] Step 3: Remove unrelated boilerplate (edit by judgment)
- [ ] Step 4: Verify result
```

### Step 1: Read the file

Read the whole file first. Preserve the YAML frontmatter (the `---` block at the top) unchanged.

### Step 2: Convert Obsidian image embeds

Run the helper script (deterministic, do not hand-edit each image):

```bash
python3 scripts/convert_obsidian_images.py "<path-to-article.md>"
```

Rule: `![[figures/abc_MD5.webp]]` → `![](figures/abc_MD5.webp)`. The script reports how many embeds were converted.

### Step 3: Remove unrelated boilerplate

This needs judgment. Keep the article's real title, body text, section headings, and content images. **Delete** clipping cruft such as:

- Author/account byline + timestamp lines (e.g. `笔记侠 *2026年5月1日 21:31*`)
- Editor/production credits (`**责编** | ... **排版** | ...`)
- "篇深度好文 / 字 / 分钟阅读" stat banners and column tags when they are just metadata, not content
- End-of-article marketing: course/product ads, enrollment pitches, promo images
- "好文阅读推荐" / related-article link lists appended by the platform
- Social CTAs: `分享、点赞、在看`, `点个在看`, `星标`, etc.
- WeChat navigation artifacts: `继续滑动看下一个`, `向上滑动看下一个`, trailing repeated account name

When unsure whether a passage is content vs. boilerplate, keep it and note it to the user rather than deleting silently.

### Step 4: Verify

- Frontmatter intact.
- No remaining `![[` embeds: `rg '!\[\[' "<path>"` returns nothing.
- No remaining CTA/navigation lines like `继续滑动看下一个`.
- Article reads cleanly start to finish.

## Notes

- Edit the file in place unless the user asks for a copy.
- Do not rewrite or paraphrase the article body — only remove boilerplate and fix image syntax.
