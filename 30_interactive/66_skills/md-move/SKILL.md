---
name: md-move
description: Move a Markdown article into its corresponding perso sub-folder, under a `_raw` subfolder, based on the "与脑图对比 / 对比脑图" information the md-understand skill wrote into the article. Also relocates the figures the article references so image links keep working. Use when the user asks to move, file, or archive an ingested article into the perso knowledge base.
---

# md-move

Move an ingested article into the right `perso` sub-folder, inside a `_raw/` subfolder (created if missing). The destination is derived from the article's **对比脑图** comparison chapter.

Prerequisite: the article must already contain a `## 与脑图对比（…）` chapter (added by the `md-understand` skill). If it does not, stop and tell the user to run `md-understand` first.

## Workflow

```
- [ ] Step 1: Read the article's 对比脑图 chapter
- [ ] Step 2: Resolve the target sub-folder in perso
- [ ] Step 3: Move the article + figures into <target>/_raw/
- [ ] Step 4: Verify
```

### Step 1: Read the 对比脑图 info

From the article extract:
- The comparison heading: `## 与脑图对比（<category> / <subtopic>）`
- The line: `对比脑图：\`perso/<category-dir>/<file>.opml\`（重点：\`<branch>\` 分支）`

`<category-dir>` (e.g. `30_self-management`) is the perso category. `<subtopic>` / `<branch>` (e.g. `目标管理`) selects the sub-folder.

### Step 2: Resolve the target sub-folder

The perso root is `persospace/perso`. List the category's sub-folders and pick the one that matches the subtopic:

```bash
ls -d "persospace/perso/<category-dir>"/*/
```

Match `<subtopic>` to a sub-folder by its name / README title. Known mapping for `30_self-management`:

| 对比脑图 subtopic | Sub-folder |
|-------------------|------------|
| 目标管理 / 方向感 | `20_goal` |
| 时间管理 / 专注力 | `30_time` |
| 运动 | `36_sports` |
| 精力管理 / 效率 | `40_energy` |
| 外表管理 | `50_appearance` |
| 效率管理 / 执行 | `60_efficience` |

If the category has **no** matching sub-folder (e.g. `10_belief`, `40_eq` have none), use the category directory itself as the target.

The final target directory is that sub-folder (or category dir). The article will land in `<target>/_raw/`.

### Step 3: Move article + figures

Run the helper script (it creates `_raw/`, moves referenced figures so links stay valid, then moves the `.md`):

```bash
python3 scripts/move_to_raw.py "<article.md>" "persospace/perso/<category-dir>/<sub-folder>"
```

The script:
- Creates `<target>/_raw/` if missing.
- Moves every image the article references (`![](figures/…)` / `![[figures/…]]`) from the article's sibling `figures/` into `<target>/_raw/figures/`, preserving the relative path so links keep working.
- Moves the `.md` into `<target>/_raw/`.
- Refuses to overwrite an existing destination.

### Step 4: Verify

- `<target>/_raw/<article>.md` exists; the original path no longer has it.
- Referenced figures now live under `<target>/_raw/figures/`; the script reports 0 unresolved refs.
- Report the final destination path to the user.

## Worked example

`persospace/Clippings/1.7亿…重塑你的一生？.md` has:
`## 与脑图对比（self-management / 目标管理）` → category `30_self-management`, subtopic `目标管理` → sub-folder `20_goal`.

```bash
python3 scripts/move_to_raw.py \
  "persospace/Clippings/1.7亿人已读神作：如何用一天时间，彻底重塑你的一生？.md" \
  "persospace/perso/30_self-management/20_goal"
```

Result: the article moves to `persospace/perso/30_self-management/20_goal/_raw/`.

## Notes

- Only referenced figures are moved; unrelated figures in the source folder stay put.
- Paths with spaces / non-ASCII must be quoted.
