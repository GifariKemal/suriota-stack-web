---
name: Suriota Elementor Render-Cache Flush Required After REST Edits
description: Elementor caches rendered HTML in DB; REST API edits to _elementor_data don't invalidate it. Application Password auth can't call admin-ajax (nonce 400). Working flush via Playwright browser-login.
type: project
originSessionId: 13e95821-5ff9-473c-b59f-932e6f2ac11c
---
## Symptom
After successful `POST /wp/v2/pages/{id}` updating `_elementor_data` (add/remove sections, modify widget HTML, swap image URLs), the live page renders the OLD version. DB read-back confirms new data persisted. Affects single sections too — not just bulk inserts. Single-page-localized: same edit on ID/ZH may render correctly while EN stays frozen.

## Root cause
Elementor maintains a render cache (CSS files + cached rendered HTML/JS/CSS assets in DB). REST API meta updates don't trigger Elementor's save lifecycle that invalidates this cache. See `Elementor → Tools → General → Elementor Cache`: "Clear outdated CSS files and cached data in the database (rendered HTML, JS/CSS assets, etc.)".

## What does NOT work via Application Password REST session
1. Republish (`status: publish`) — no effect
2. Touching `modified_gmt` — no effect
3. Title bump + revert — no effect
4. Re-saving `_elementor_data` with rotated IDs — no effect
5. Clearing `_elementor_css` meta — no effect
6. `POST /wp-admin/admin-ajax.php` with `action=elementor_clear_cache&_nonce=<scraped>` — **returns 400 `0`**. Application Password authenticates but the WP nonce system requires a real cookie-login session; `check_ajax_referer` fails.

## What DOES work
Playwright cookie-login as admin + click the Tools button.

**Why:** `Reason: admin-ajax nonces require a real wp_login session, which Application Password doesn't provide. How to apply:** Use after any REST `_elementor_data` edit that affects rendered output.

```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_context().new_page()
    page.goto('https://suriota.com/wp-login.php')
    page.fill('input[name="log"]', WP_ADMIN_USER)
    page.fill('input[name="pwd"]', WP_ADMIN_PASS)
    page.click('input[name="wp-submit"]')
    page.wait_for_load_state('networkidle')
    page.goto('https://suriota.com/wp-admin/admin.php?page=elementor-tools')
    page.on('dialog', lambda d: d.accept())
    page.locator('button:has-text("Clear Files & Data")').first.click()
    page.wait_for_timeout(5000)
    browser.close()
```

## Cache topology on suriota.com (2026-05-27 verified)
- **WP-Optimize page caching: DISABLED** (toggle off, confirmed in `wp-admin/admin.php?page=wpo_cache`). So WPO is NOT a layer.
- **Cloudflare: DYNAMIC** (cf-cache-status header) — not caching HTML at edge.
- **Elementor cache: ACTIVE** — the single cache layer. Always flush this after REST edits.

## When to apply
Run ONCE after a batch of REST edits completes (per-page edit or sitewide). Verify with `requests.get('https://suriota.com/...?cb=<ts>')` checking for expected new content.
