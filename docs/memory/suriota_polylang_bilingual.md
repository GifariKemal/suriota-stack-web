---
name: SURIOTA Polylang Bilingual Setup 2026-05-19
description: Polylang Free + ID subdirectory live with 7 strategic page translations; pipeline ready for expansion
type: project
originSessionId: 6fd314fb-896a-48c3-8a4c-4971145cacef
---
Deployed 2026-05-19. Indonesian (ID) added as secondary language alongside English (EN, default).

## Plugins installed (free)
- **Polylang** (polylang/polylang.php) — installed via Plugin_Upgrader; managed via Languages admin menu
- **Connect Polylang for Elementor** (connect-polylang-elementor) — bridges Polylang ↔ Elementor

## URL Structure
- EN (default): `suriota.com/` (no /en/ prefix)
- ID: `suriota.com/id/{slug}/` (subdirectory)
- `hide_default=1` in Polylang options — EN URLs stay clean

## Translation pairs (EN ↔ ID)
| EN page | EN ID | ID page | ID ID | ID URL |
|---|---|---|---|---|
| Homepage | 12 | Beranda | 5273 | /id/beranda/ |
| About | 29 | Tentang Kami | 5274 | /id/tentang-kami/ |
| Portfolio | 839 | Portfolio ID | 5275 | /id/portfolio-id/ |
| Internship | 1127 | Magang | 5276 | /id/magang-srt-team/ |
| Water Treatment | 945 | Water Treatment ID | 5277 | /id/water-treatment-id/ |
| SaaS SURGE | 5039 | SaaS ID | 5278 | /id/saas-id/ |
| Artikel | 5260 | Artikel ID | 5279 | /id/artikel-id/ |

## Permanent code_snippet entries
- `SX: Polylang Translation Linker REST` — registers `/wp-json/sx/v1/link-translation` and `/wp-json/sx/v1/set-language` for programmatic linking
- `SX: Polylang Hreflang Injector` — emits hreflang tags (en, id, en-US, id-ID, x-default) from pll_get_post_translations
- `SX: HTML lang Polylang-aware` — maps pll_current_language('slug') to W3C lang code on `<html lang>` (en→en-US, id→id-ID)

## Language switcher
- Injected as HTML+CSS+JS in header snippet 5153
- Desktop: top-right floating pill (EN/ID toggle), `top:14px right:84px`
- Mobile: bottom-left floating pill (avoid Olark chat at bottom-right)
- Reads hreflang link tags for cross-version URLs

## ID page content pattern
Each ID page contains:
- Translated H1 (`<h1>` hero)
- Bahasa Indonesia intro paragraph (1-2 sentences)
- Dual CTAs: WhatsApp + "View in English →" deep link
- Note explaining full Bahasa content is in development

## AIOSEO meta on ID pages
Direct table write to `wp_aioseo_posts` with translated title + description per page (same workflow as v4/v5 EN meta).

## Phase 1B completed (2026-05-19)
**15 additional ID pages live**:
- 6 service: Electrical 5281, Automation 5282, RE 5283, IoT 5284, DA 5285, DC 5286
- 9 product: SRT-MGATE 5287, SURGE-E 5288, SURGE-V 5289, SURGE-W 5290, ISO-M485 5291, THM-30MD 5292, PM1611-WD 5293, SPD-T485 5294, WW Logger 5295

## STATUS — 22 main pages have ID versions (100% coverage of services + products)

## Phase 1D — Full Content Sync COMPLETE (2026-05-19)
- All 22 ID pages have FULL content cloned from EN
- Applied 6 dict passes (V1-V6) totaling ~550 translation replacements
- Result: 0 LOW (<40%), 14 MED (40-69%), 8 GOOD (≥70%) Bahasa coverage
- Stats: Homepage 94%, About 95%, Portfolio 78%, Artikel 100%, DA 80%, MGATE 78%, SURGE-W 72%, THM-30MD 74%
- Pipeline: _sync_lib.py walker + V1-V6 dict files
- Manual dict approach hit diminishing returns ~75% per-page; further refinement needs page-by-page sentence translation

## Skipped — Phase 1C
- 64 portfolio posts — recommend AutoPoly AI plugin if needed later

## Perf + Switcher fixes (2026-05-19)
- Server-rendered switcher via wp_footer PHP hook (no JS pop-in flicker)
- 27/29 images lazy-loaded sitewide via output buffer filter
- Google Maps iframe deferred via IntersectionObserver
- DOMContentLoaded improvement: 5061ms → 1804ms (64% faster)

## CRITICAL bug avoided
- `_fix_lang_polylang.php` had SQL `WHERE name LIKE '%lang%'` which accidentally matched "SX: Po**lylang** Translation Linker REST" and overwrote it
- FIX: re-deployed _restore_linker.php to recreate /sx/v1/link-translation endpoint
- Going forward: always use exact name match `WHERE name = '...'` not LIKE pattern

## Pipeline for expansion
- Python script `_translate_8_pages.py` is reusable template — just add new entries to PAGES list with translated copy
- Each new translation: create via `/wp/v2/pages?lang=id` → link via `/sx/v1/link-translation` → push AIOSEO meta to `wp_aioseo_posts`
- For 64 portfolio posts at scale: recommend AutoPoly AI plugin ($) or DeepL API integration (DeepL works for raw content, NOT for Polylang's Elementor machine translate)

## Key technical findings
- Polylang Free does NOT auto-generate hreflang for translated posts — needs custom snippet (we have it)
- AIOSEO Free does NOT have multi-language sitemap — Polylang generates separate sitemaps per language at /sitemap.xml (root) + /id/sitemap.xml
- WP site locale is id_ID (default Indonesian) — Polylang slug filter handles per-page lang attribute override
- `pll_set_post_language()` + `pll_save_post_translations()` are key functions for programmatic linking
