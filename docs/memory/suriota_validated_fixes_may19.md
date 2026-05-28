---
name: Validated Fixes Deployed 2026-05-19
description: Production changes deployed after independent validation of Kimi audit — what was fixed, what was deferred, and why
type: project
originSessionId: 95f640f8-e0b2-4e94-a8be-8e13ee3c6f70
---
Deployed 2026-05-19 after cross-validating Kimi audit `audit/COMPREHENSIVE-WEBSITE-AUDIT-2026-05-18.md`. Independent validation report: `audit/VALIDATION-REPORT-2026-05-19.md` (Kimi accuracy ~65%).

**Why:** User asked to fix only the validated findings, not every Kimi claim. Several Kimi claims were wrong (3 → 1 real 404, Electrical 31.7s not reproducible, hardware Product schema not actually missing).

**How to apply:** Before acting on any future external audit (Kimi, Lighthouse, GTmetrix), cross-validate first — the page-by-page validation pattern in `VALIDATION-REPORT-2026-05-19.md` caught major errors that would have wasted engineering time.

### Live changes (verified)

1. **Snippet 5153 → v5.1** (`scripts/fix-emergency-snippet-v5.py`, 26,313 chars)
   - Mobile dropdown sync: `:hover` rule scoped to `@media (hover: hover) and (pointer: fine)`; mobile panel uses `#0E3942` + gradient accent (matches desktop)
   - Ghost-slug redirect: `/modbus-gateway/` → `/suriota-modbus-gateway/`, `/waste-water-loger/` → `/waste-water-logger/` (client-side, fires before any other init)
   - Duplicate-H1 dedup: removes `h1.entry-title` from DOM when ≥2 H1s present. Astra theme injects `h1.entry-title` for ~11 legacy pages.

2. **Title cleanups** (WP REST API `/wp/v2/pages/{id}`):
   - id=1741 THM-30MD — stripped U+200B suffix
   - id=1742 PM1611-WD — stripped U+200B suffix
   - id=1740 ISO-M485 SERIES — stripped U+200B suffix
   - id=929 Waste Water Logger — "Loger" → "Logger"
   - id=934 Modbus Gateway IIoT — U+00A0 non-breaking space → regular space

3. **Elementor Global Kit colors** (MCP `update-global-colors`):
   - primary `#6EC1E4` → `#205B69` (Industrial Editorial teal)
   - accent `#61CE70` → `#C8851F` (Industrial Editorial amber)
   - secondary/text unchanged

### Live changes — Session 2 (2026-05-19, audit validation batch)

From audits: `WEB-HEALTH-CHECK-2026-05-18.md`, `AIOSEO-AUDIT-2026-05-18.md`, `WP-OPTIMIZE-BASELINE-2026-05-18.md`

4. **Snippet 5185** — Ghost Slug Redirects v2 (tentang, modbus-gateway, waste-water-loger)
   - `/tentang/` → `/about-us/`; `/modbus-gateway/` → `/suriota-modbus-gateway/`; `/waste-water-loger/` → `/waste-water-logger/`
   - Note: client-side JS only (server 404 still fires), works in real browser

5. **Snippet 5184** — Global Article CSS for all 64 single posts (`:not(.postid-1925)`)
   - Plus Jakarta Sans headings, IBM Plex Mono code, H2 green border-left, H3 teal, compact spacing

6. **Snippet 5186** — Security Headers Meta Tags (X-Content-Type-Options, X-Frame-Options, Referrer-Policy)

7. **Snippets 5187/5188/5190/5191** — Product JSON-LD schemas for ISO-M485, THM-30MD, PM1611-WD, RS-485 Surge Protector SPD-T485-105

8. **Snippet 5192** — LocalBusiness JSON-LD schema sitewide (address: Batam Centre, tel: +62858-3567-2476)

9. **Snippet 5189** (draft) — Tawk.to defer fix; activate AFTER disabling original embed. Correct ID: `66666723981b6c56477b687b/1i0005pb0`

10. **Article 1925 content fixes** (May 19 early morning):
    - H2 de-stuffing (removed " PJU Hybrid PLTS" suffix from 2 H2s)
    - Filler phrase removed (was already gone from post), internal links added (/renewable-energy/, /internet-of-things/, /electrical/)
    - Snippet 5180 (color sync v3 tokens), 5181 (density), 5182 (Article+FAQPage JSON-LD) — all live

11. **63-article batch content fix** — Agent running (check session for completion status)

### Deferred (needs human decision or copywriting)

- Meta description rewrites for 17+ pages — needs per-page copywriting; AIOSEO scrapes raw widget HTML otherwise
- Meta title expansion for 13 short-title pages — needs copywriting
- `/tentang/` restoration vs 301 to `/about-us/` — business decision
- SoftwareApplication JSON-LD on 3 SURGE SaaS pages (`/surge-energy-mapping/`, `/surge-vessel-tracking/`, `/surge-water-analytic/`)
- Tawk.to CORS fix / defer
- Image WebP optimization

### Watch-outs

- Ghost-slug redirect is client-side JS, so Googlebot sees 404 before redirect. For real 301 need server config or Redirection plugin (no REST API found for AIOSEO/Redirection on this site).
- Duplicate-H1 fix is DOM-removal post-load — Googlebot executes JS so this works in practice, but for guaranteed crawler behavior consider Astra theme settings or `the_title` PHP filter via Code Snippets plugin.
- Elementor color update may require Elementor regenerate-CSS pass per page; new widgets pick up new colors immediately, existing widgets need a save to re-render against the kit.
