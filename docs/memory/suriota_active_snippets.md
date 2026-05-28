---
name: Suriota Active SX/ Snippets Inventory (post 2026-05-21 cleanup)
description: Live Elementor code snippets on suriota.com — their purpose, why they exist, and what would remove them
type: reference
originSessionId: faffb55c-0f12-4249-8b3c-88d2f28ccb36
---
## Workaround snippets (KEEP until upstream fix)

| ID | Title | Location | Why exists | Removable when |
|---|---|---|---|---|
| 5511 | SX / Document.body Guard | head pri 1 | `sx-schema-1925` (snippet 5182) calls `document.body.classList` in `<head>` before body parses → null TypeError on every page | Snippet 5182 rewritten with `DOMContentLoaded` wrapper |
| 5515 | SX / Carousel e396a55 RAF Marquee | body_end pri 10 | Elementor `SwiperHandler.applyMotionPreferences()` force-disables autoplay+speed when `prefers-reduced-motion:reduce` (Windows 11 default). Carousel `e396a55` (Trusted-By logos) freezes on desktop. Snippet replaces Swiper with `requestAnimationFrame` driving `margin-left` (transform property is also blocked by sitewide reduce-motion CSS, so we use margin) | Elementor adds per-widget reduce-motion opt-out, OR user accepts no-motion compromise |
| 5524 | SX / Inject ZH hreflang v2 | head pri 3 | Polylang free can't link translations across 3 languages via REST. Snippet injects `<link rel="alternate" hreflang="zh-CN">` based on slug map (26 page pairs). Also replaces stale `/zh/` hreflang on home with `/shouye/` | Polylang Pro upgrade OR manual link 26 page pairs via WP admin |
| 5528 | SX / Block Specific Broken Tawk Property | head pri 1 | Tawk widget property `66666723981b6c56477b687b` doesn't exist in user's Tawk account but is still configured in the Tawk.to plugin AND embed code uses invalid `crossorigin='*'` AND Tawk CDN serves non-standard `application/x-javascript` MIME (Chrome ORB blocks). Snippet intercepts `document.createElement` to drop script src containing the broken property ID | User creates new Tawk property and updates plugin settings to use new ID |
| 5599 | SX / Language Switcher Patch – New Pillar Pages | body_end pri 5 | Header EN/ID/ZH dropdown links hardcoded in `sx-hf-v5` template; only updates the language-switcher dropdown URLs when on a pillar page (created 2026-05-24) | Header template refactored to use Polylang theme location instead of hardcoded HTML |
| 5638 | SX / Nav Header URL+Label Swap (Pillar+Top+Products) v2 | body_end pri 4 | Header+footer navigation in `sx-hf-v5` template hardcodes EN URLs (and full labels for pillars). On `/id/` and `/zh/`, snippet rewrites href for **18 entries** (5 pillars + 3 top-level + 8 products + 2 legal) AND swaps label text only when EN-pillar-label match. Translation labels for non-pillar items (e.g., "Tentang Kami", "关于我们") still handled by snippet 5447. Verified 2026-05-27: `stillEN: 0` on /id/ and /zh/ header | Same as 5599 — Elementor template 1075 (`navbar`) refactored to render menu from Polylang theme location |
| 5639 | SX / Service Hub OfferCatalog (Sitewide) | head pri 3 | Schema graph entity — declares `OfferCatalog @id=#service-catalog` referencing 5 pillar Services (`#service` per pillar URL). Linked from LocalBusiness via `makesOffer`. Provides catalog-level structured data that Google can render in Knowledge Graph. Created 2026-05-28 | Replaced by AIOSEO Pro Schema Catalog module OR consolidated into snippet 5192 |
| 5640 | SX / Always-Visible Sticky Navbar (Sitewide) v3 | body_end pri 6 | **v3 (2026-05-28): switched from "hide-on-scroll-down" to always-visible.** Uses `position: fixed; top: 0` (more robust than sticky which breaks under parent overflow/transform). Auto-syncs `body { padding-top }` to nav height via ResizeObserver. Adds `.sx-nav--scrolled` class at y>8 for box-shadow accent. rAF-throttled, passive listener. **Reason for v3**: user clarified they want navbar to FOLLOW the scroll (always visible at top), not hide. v1/v2 misinterpreted as Medium-style smart hide | Header template 1075 refactored to use native Elementor sticky widget |
| 5641 | SX / Back-to-Top Button (Sitewide) | body_end pri 7 | Sitewide back-to-top button — extracted CSS+JS from homepage-only `_elementor_page_settings.custom_css` and made universal. Self-contained colors (#205B69 accent, #0E3942 hover) not depending on `--sxh-*` vars which only exist on page-id-12/5273/5448. Created 2026-05-28 after audit found widget missing on contact/portfolio/modbus/energy pages | Per-page widget standardized in Elementor or moved to theme template |
| 5642 | SX / Dequeue Unused Roboto Font | head pri 1 | Roboto Google Font is enqueued by Elementor (`elementor-gf-roboto-css`) but only 2 refs in HTML vs Geist 102. JS strips the `<link>` tag at parse → DOM-load → 300ms → 1.2s to ensure removal. Saves ~30KB Google Fonts request. Keeps Roboto Slab (locally hosted, used in some article CSS). Created 2026-05-28 | Elementor Site Settings → Typography removes Roboto OR Hello Elementor child theme dequeues via PHP |
| 5643 | SX / Geist Font Preload Hint | head pri 1 | Adds `<link rel=preload as=style>` for Geist + Geist Mono CSS so browser fetches with high priority. Also includes redundant preconnect (safe; idempotent). Reduces FOIT/FOUT on first paint. Created 2026-05-28 | Same as 5411 ownership — could be merged into Geist Font System snippet |
| 5644 | SX / CLS Shield Pillar Hero Min-Height | head pri 5 | Pillar pages use CSS `background-image` heroes with no intrinsic dimensions → CLS risk on slow connections. Reserves `min-height: 360px` (mobile) / `480px` (tablet+) on first elementor-top-section for 12 known pillar page IDs (EN+ID+ZH for IoT/Modbus/SaaS/SCADA/Energy). Created 2026-05-28 | Pillar Elementor templates updated to set explicit section min-height in their Layout settings |
| 5649 | SX / Pillar Service Schema (Modbus, SaaS, Energy) | head pri 4 | JS-injected Service JSON-LD with `@id` + provider→#organization ref for 3 pillars that lack inline Service in their Elementor data. URL-conditional via `location.pathname` check. Created 2026-05-28 after AIOSEO audit found schema gap | Inline Service JSON-LD added directly to those pillars' Elementor HTML widgets |
| 5650 | SX / CollectionPage Schema (/artikel/) | head pri 4 | URL-conditional JS injects CollectionPage + ItemList JSON-LD on `/artikel/` (article archive). 20 latest posts as ListItems with position+url+name. Created 2026-05-28 after audit found archive lacked schema | AIOSEO Pro Archive Schema module enabled, OR Elementor archive widget upgraded |
| 5651 | SX / Portfolio Table Interactive Refinements v2.1 | body_end pri 8 | **v2 (2026-05-28)**: substantial visual redesign — dropped nth-child striping (clean white rows), bigger editorial leading numbers (17px mono), stronger container (radius 14px + layered shadow), refined padding (18px vertical), refined year badge variants, amber-themed interactions (accent bar, underline, badge pulse, filter input focus). **Bug fix v2**: moved accent bar from `tr::before` to `td:first-child::before` — Chrome's table layout was treating absolutely-positioned `tr::before` as phantom column cell, shifting body cells right by 87px. **Bug fix v2.1**: forced `td { background: transparent !important }` — global theme adds `rgba(128,128,128,0.07)` bg on all `td` elements that becomes visible on mobile where cells are `display:block` inside card rows. Created 2026-05-28 after user feedback "berantakan dan biasa" + mobile bg flaw | Inline CSS in homepage Elementor data rewritten with these tokens |
| 5656 | SX / Pillar Related Capabilities Cross-Links | body_end pri 9 | URL-conditional JS injects "Related Capabilities" card grid above FAQ section on 5 pillar pages × 3 languages (15 pages). Each card has num (01-05) + title + 1-sentence description + arrow icon, links to sibling pillars (4 other pillars per page). EN/ID/ZH copy embedded. Hover: amber border + lift + shadow + arrow shift. Created 2026-05-28 to fix internal-linking density audit finding (IoT pillar had only 3 of 4 sibling cross-links inline) | Pillar Elementor templates updated to include native related-pillar widgets |
| 5659 | SX / Hreflang Dedup (AIOSEO + Polylang) | head pri 2 | Both AIOSEO and Polylang emit `<link rel="alternate" hreflang>` independently, creating duplicates on pillar pages. This JS scans on parse + DOMContentLoaded + 100ms + 500ms and removes duplicates (same hreflang + same href), keeping first occurrence. Created 2026-05-28 to fix HIGH audit finding | Either AIOSEO Multilingual disabled OR Polylang hreflang disabled (UI-only toggles) |

## NEVER touch (existing core)

- **5447** `SX / Nav Header ID Swap (JS Runtime)` — translation runtime for header/footer text
- **5153** `SX / Emergency Header-Footer v2` — full custom header/footer injector with slug map for language switcher
- **5498** `SX / ZH Pages CSS (Bypass WPO Minify)` — 380KB CSS bundle, includes most sitewide styling
- **5411** `SX / Geist Font System Sitewide` — font foundation
- **5186** `SX / Security Headers Meta Tags` — note: X-Frame-Options should be HTTP header, not meta (browser warns but harmless)
- **5184, 5182** — single post layout + article schema (5182 is the head-script that needs `document.body` guard 5511)
- **5180–5191** — article/product schema snippets
- **5192** `SX / LocalBusiness JSON-LD Schema - Sitewide` — **rewritten 2026-05-28** to use `@type: ["Organization","LocalBusiness"]` with `@id=https://suriota.com/#organization` (merges with AIOSEO Organization node). Adds detailed address/telephone/contactPoint/areaServed/knowsAbout/makesOffer→#service-catalog

## Deleted in 2026-05-21 cleanup

5512, 5513, 5514 (failed carousel attempts), 5516, 5517 (failed Tawk fixes), 5518 (replaced by surgical 5528), 5522 (JS redirect, replaced by server 301), 5523 (broken regex v1, replaced by 5524), 5527 (intermediate strip)

## Polylang menus (created 2026-05-27, currently unused)

- Menu id 294 "Suriota Menu ID" — assigned to `Header Bahasa Indonesia` + `Footer Bahasa Indonesia` Polylang locations
- Menu id 295 "Suriota Menu ZH" — assigned to `Header 中文` + `Footer 中文` Polylang locations

These are **inert** because the `sx-hf-v5` header is custom HTML in Elementor template 1075 (not a WP nav-menu widget). They were created as fallback while diagnosing the menu issue. Leave them — they cost nothing and become live the moment someone refactors template 1075 to use a real Elementor Nav widget bound to theme location.

## Tawk.to deep-fix path (when user has time)

1. Tawk dashboard → create/locate active property + widget IDs
2. WP Admin → Tawk.to plugin settings → Use Existing → pick correct property
3. If Chrome still blocks (ORB on `application/x-javascript` MIME), the only solutions are:
   - Switch to Crisp/LiveChat/Intercom (all serve proper MIME)
   - Self-proxy the Tawk script through suriota.com with correct Content-Type header
4. After fix verified working, delete snippet 5528
