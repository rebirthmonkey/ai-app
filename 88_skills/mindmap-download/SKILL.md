---
name: mindmap-download
description: Use when the user gives a mubu.com (幕布) mind-map/outline URL and wants it exported/downloaded as OPML, PDF, Word, HTML, image, or FreeMind. Also use when an export attempt on mubu.com shows the wrong format options (e.g. OPML missing) or a "导出/下载" click does nothing.
---

# mindmap-download

Download a mubu.com (幕布) document as OPML / PDF / Word / HTML / 图片 / FreeMind, driving the user's real logged-in browser via the `web-access` skill's CDP proxy.

**REQUIRED SUB-SKILL:** Use `web-access` first — this skill assumes its CDP proxy is already up at `http://localhost:3456` (run its `check-deps.mjs` if unsure).

## Key fact: mubu has two view modes, and export formats differ by mode

| Current view mode | Formats in "导出为" dialog |
|---|---|
| 大纲笔记 (outline) | Word, PDF, 图片, HTML, **OPML** |
| 思维导图 (mind map, radiating tree) | 图片, FreeMind |

**OPML only exists in outline mode.** PDF/图片 exist in both modes (content differs: outline mode PDF is a paginated document, mind-map mode PDF/图片 is the radial diagram). FreeMind only exists in mind-map mode.

**OPML export additionally requires a 幕布高级版 (premium) account.** On a free account the OPML tile is simply absent from the dialog even in outline mode — this is not a bug to work around, tell the user they need premium.

## The mode-toggle button is inverted — read this before touching it

The button at the top of the document (next to "已保存") shows the mode you will switch **TO**, not the current mode:

- Button reads **"思维导图"** → you are currently in outline mode already.
- Button reads **"大纲笔记"** → you are currently in mind-map mode; click it to switch to outline mode.

Don't infer current mode from the label without this inversion — it's the most common mistake when doing this by hand. Confirm by screenshot instead of trusting the label alone: outline mode renders as a vertical bullet list; mind-map mode renders as a horizontal radiating tree.

## Workflow

```
- [ ] Step 1: Open the doc in a background tab
- [ ] Step 2: Screenshot to confirm current mode; switch mode if the target format needs the other one
- [ ] Step 3: Open the "更多操作" menu → click "导出/下载"
- [ ] Step 4: Click the target format tile in the "导出为" dialog
- [ ] Step 5: Verify the file landed in ~/Downloads and close the tab
```

### Step 1: Open the doc

```bash
curl -s -X POST --data-raw '<mubu-url>' http://localhost:3456/new
# → {"targetId": "..."}
sleep 3
curl -s "http://localhost:3456/info?target=<targetId>"   # wait for "ready":"complete"
```

### Step 2: Confirm mode, switch if needed

Screenshot and look at the canvas layout (vertical list vs. radiating tree), not just the button text.

To switch: find the div whose exact text is the *current* button label and click it (the click toggles):

```bash
curl -s -X POST "http://localhost:3456/eval?target=<id>" -d '(() => {
  const el = Array.from(document.querySelectorAll("div,span")).find(e => e.textContent.trim() === "大纲笔记" && e.children.length === 0);
  if (!el) return "not found";
  el.id = "cdp-mode-toggle";
  return "tagged";
})()'
curl -s -X POST "http://localhost:3456/click?target=<id>" -d '#cdp-mode-toggle'
sleep 1
```

(Substitute `"思维导图"` for the text if you need to go the other direction.)

### Step 3: Open export dialog

Menu items are `<span>` text with no stable class name and no usable CSS selector — **tag the exact node by its text content via `/eval`, then click it by the tag you just added.** Clicking an ancestor div "a few levels up" by guesswork is the most common failure mode here (it either hits nothing or closes the menu) — always locate the exact `<span>` whose `textContent.trim()` equals the label, and click *that node* (its own `.click()` bubbles correctly), not a parent.

```bash
# open the "..." more-actions menu (icon button just left of the "..." kebab)
curl -s -X POST "http://localhost:3456/click?target=<id>" -d 'button.sc-fIbDzs.sc-cQMCMF'
sleep 1

# tag and click "导出/下载"
curl -s -X POST "http://localhost:3456/eval?target=<id>" -d '(() => {
  const span = Array.from(document.querySelectorAll("span")).find(e => e.textContent.trim() === "导出/下载");
  if (!span) return "not found";
  span.id = "cdp-export-entry";
  return "tagged";
})()'
curl -s -X POST "http://localhost:3456/click?target=<id>" -d '#cdp-export-entry'
sleep 1
```

If `button.sc-fIbDzs.sc-cQMCMF` no longer matches (styled-components hashes can change across mubu deploys), rediscover it: screenshot the toolbar, then `/eval` to list `svg[type]` or button elements near the top-right and re-identify the export icon (it's the box-with-up-arrow, just left of the "..." kebab).

### Step 4: Click the target format tile

The clickable element is the icon's `.figure` ancestor (two levels up from the format `<svg>`/`.img-wrap`), not the bare label span and not further-up wrapper divs:

```bash
curl -s -X POST "http://localhost:3456/eval?target=<id>" -d '(() => {
  const label = Array.from(document.querySelectorAll("*")).find(e => e.childNodes.length===1 && e.childNodes[0].nodeType===3 && e.textContent.trim()==="OPML");
  if (!label) return "not found";  // format tile absent = wrong mode, or (for OPML) non-premium account
  const figure = label.closest(".figure");
  figure.id = "cdp-format-btn";
  return "tagged";
})()'
curl -s -X POST "http://localhost:3456/click?target=<id>" -d '#cdp-format-btn'
sleep 2
```

Swap `"OPML"` for `"PDF"` / `"Word"` / `"图片"` / `"HTML"` / `"FreeMind"` as needed. If `label` comes back "not found", re-check Step 2 — the format isn't offered in the current mode (or, for OPML specifically, the account isn't premium).

Clicking the figure closes the dialog immediately and triggers a background export + browser download — no further confirmation dialog to click through. The server-side conversion takes a few seconds (longer for larger docs / heavier formats like Word); the file does not appear in Downloads instantly, so don't treat an empty check immediately after the click as failure — wait ~3-5s before checking, and re-check once more if needed.

### Step 5: Verify and clean up

```bash
sleep 3
ls -lt ~/Downloads/ | head -5   # newest file should be "<doc-title>.<ext>", just-now timestamp
curl -s "http://localhost:3456/close?target=<id>"
```

For OPML, sanity-check the outline count matches the doc's own "N条主题" stat:
```bash
grep -c "<outline" ~/Downloads/"<doc-title>.opml"
```

## Common mistakes

| Symptom | Cause | Fix |
|---|---|---|
| Export dialog only shows PDF/图片/FreeMind, user insists they want OPML | Currently in mind-map mode | Do Step 2 mode switch first |
| OPML tile never appears even in outline mode | Account is not 幕布高级版 | Tell the user; not fixable client-side |
| `/click` on a menu item returns `clicked:true` but nothing visibly happens | Selector matched a wrong/ambiguous element (e.g. bare `span` matches dozens of nodes across the page) | Always tag the *specific* node found via exact `textContent` match with a unique `id`, then click by that `id` |
| Clicking "更多" → nothing opens | It's a plain menu item here, not the format-tile pattern — real `clickAt` (not synthetic `dispatchEvent`) is required for submenu hover/click triggers in some mubu menus | Use `/clickAt` with the tagged id if `/click` doesn't visibly change the screenshot |
| Modal won't close via the X icon's `/click` | The X is an `<svg>`, and `el.click()` isn't a function on SVG elements in this DOM | Dispatch a real `MouseEvent("click")` via `/eval` instead, or just click a valid format tile / real click outside the modal |

## Worked example

```bash
curl -s -X POST --data-raw 'https://mubu.com/app/edit/home/13rDxznf_2p?sidebarFolded=1' http://localhost:3456/new
# → {"targetId":"ABC123"}
sleep 3
# screenshot shows radiating tree → currently mind-map mode; button reads "大纲笔记" → click it to switch
curl -s -X POST "http://localhost:3456/eval?target=ABC123" -d '(() => { const el = [...document.querySelectorAll("div,span")].find(e=>e.textContent.trim()==="大纲笔记"&&e.children.length===0); el.id="cdp-mode-toggle"; return "ok"; })()'
curl -s -X POST "http://localhost:3456/click?target=ABC123" -d '#cdp-mode-toggle'
sleep 1
curl -s -X POST "http://localhost:3456/click?target=ABC123" -d 'button.sc-fIbDzs.sc-cQMCMF'
sleep 1
curl -s -X POST "http://localhost:3456/eval?target=ABC123" -d '(() => { const s=[...document.querySelectorAll("span")].find(e=>e.textContent.trim()==="导出/下载"); s.id="cdp-export-entry"; return "ok"; })()'
curl -s -X POST "http://localhost:3456/click?target=ABC123" -d '#cdp-export-entry'
sleep 1
curl -s -X POST "http://localhost:3456/eval?target=ABC123" -d '(() => { const l=[...document.querySelectorAll("*")].find(e=>e.childNodes.length===1&&e.childNodes[0].nodeType===3&&e.textContent.trim()==="OPML"); const f=l.closest(".figure"); f.id="cdp-format-btn"; return "ok"; })()'
curl -s -X POST "http://localhost:3456/click?target=ABC123" -d '#cdp-format-btn'
sleep 2
ls -lt ~/Downloads/ | head -3   # → 30_自我管理.opml
curl -s "http://localhost:3456/close?target=ABC123"
```

## Notes

- All curl bodies use `--data-raw`/`-d` as-is per `web-access`'s CDP API — no URL-encoding needed.
- The doc's filename on export matches its mubu title, not the URL slug.
- `sidebarFolded=1` in the URL is cosmetic; keep whatever query the user gave you.
