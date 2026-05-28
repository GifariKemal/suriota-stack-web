---
name: suriota-homepage-portfolio-flicker-fix-2026-05-28
description: JS hoisting bug in homepage portfolio widget — render(cached) crashed because var state hoisted but undefined; cache made the bug intermittent
metadata: 
  node_type: memory
  type: project
  originSessionId: 632eaef5-07d2-4ba1-8394-c8327af57fa1
---

## Symptom
User: "tabel portfolio di homepage versi EN sering hilang timbul" — portfolio table disappears/reappears on reload.

## Root cause
The inline portfolio script in homepage Elementor data (page 12) has classic JS variable hoisting bug:

```js
ready(function () {
  // ... setup ...
  var cached = null;
  try { cached = JSON.parse(sessionStorage.getItem(CACHE_KEY)).rows; } catch (e) {}

  if (cached) render(cached);   // ← Line A — calls render BEFORE state is assigned
  fetchSource();

  // ... function declarations ...

  var state = { rows: [], top10: [], ... };  // ← Line B — state assigned HERE

  function render(rows) {
    loadingEl.hidden = true;
    var top10 = rows.slice().sort(...);
    state.rows = rows;   // ← TypeError: Cannot set properties of undefined
    ...
  }
});
```

`var state` is hoisted to function top but the ASSIGNMENT happens at Line B. When Line A executes (only on cached path — first visit has cached=null and skips this), it calls render() which dereferences state → throws TypeError → IIFE exits → fetchSource() never runs → all UI elements remain hidden → tbody empty → user sees "missing" portfolio.

## Why "hilang timbul"
- First visit: cached=null → render(cached) skipped → fetchSource queued → state initialized → fetch completes → render(fresh rows) works fine → tbody populated → cache saved
- Second visit (within 5min TTL): cached=rows → render(cached) throws → IIFE exits → tbody empty
- Cache expires after 5min → next visit is "first visit" again → works
- Effectively: alternating broken/working on rapid reloads

## Fix
Defer `render(cached)` with `setTimeout(0)` so it executes after sync init completes:

```js
if (cached) setTimeout(function(){ render(cached); }, 0);
```

The setTimeout(0) callback runs after the current synchronous block finishes (after `var state = {...}` assigns). By the time render() is called, state is defined.

## Patch applied
- Page 12 `_elementor_data` patched via REST POST: replaced `if (cached) render(cached);` with `if (cached) setTimeout(function(){ render(cached); }, 0);`
- Elementor cache flushed via Playwright admin session
- Verified live: post-load HTML contains setTimeout patch (1 occurrence)
- Verified UX: 1st/2nd/3rd reload all show 10 rows, table.hidden=false, no flicker

## Better fix (not applied)
Move the `var state = ...` line to BEFORE `if (cached)` block. Would avoid hoisting trap entirely. Not done because it requires more invasive string replacement in escaped JSON.

## Verification commands
```bash
# Confirm patched JS is in live HTML
curl -s https://suriota.com/ | grep -c 'setTimeout(function(){ render(cached); }, 0)'
# expect 1
```

```js
// In browser, force cached state and reload — table should be 10 rows
sessionStorage.setItem('sxPortfolioCache_en', JSON.stringify({ts:Date.now(),rows:[/*10 rows*/]}));
location.reload();
// Then: document.querySelectorAll('.sx-portfolio-live tbody tr').length === 10
```
