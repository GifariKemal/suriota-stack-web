---
name: SURIOTA SEO v4/v5 Keyword Deploy 2026-05-19
description: AIOSEO meta + Organization JSON-LD + hero subtitle keyword enrichment across 22 pages — supersedes manual paste templates
type: project
originSessionId: 6fd314fb-896a-48c3-8a4c-4971145cacef
---
Deployed 2026-05-19 from KEYWORDS_SCOPE_ANALYSIS.md + SURIOTA_KEYWORD_ANALYSIS.md cross-validation.

## Live AIOSEO Meta (22 pages via wp_aioseo_posts direct UPDATE)
**v4 (8 pages)**: Homepage 12, About 29, Portfolio 839, Internship 1127, Electrical 37, Automation 35, WT 945, RE 39
**v5 (14 pages)**: IoT 5029, DA 5037, DC 5033, SaaS 5039, SRT-MGATE 934, SURGE-E 1542, SURGE-V 1546, SURGE-W 1547, ISO-M485 1740, THM-30MD 1741, PM1611-WD 1742, SPD-T485 1765, WW Logger 929, Artikel 5260

## Permanent Organization JSON-LD Snippet
- Name: "SX: Organization JSON-LD sitewide" in wp_snippets table
- Fires on wp_head, priority 5
- Includes: 24 knowsAbout keywords, 8 services OfferCatalog, 8 products makesOffer, full address, contactPoint, sameAs (LinkedIn + Instagram)
- Product URLs verified: /suriota-modbus-gateway/, /rs-485-surge-protector-spd-t485-105/ (not /modbus-gateway/ or /rs-485-surge-protector/)

## Hero Subtitle Keyword Enrichment (8 service pages)
Tier-2 industry verticals (oil & gas, shipyard, manufacturing, maritime, mining) + Tier-3 compliance (KLHK SPARING, pH/COD/TSS/NH3) integrated into:
- /electrical/ → ae7cdea (heading widget)
- /automation/ → b11aad7
- /water-treatment/ → 3bec8b7
- /renewable-energy/ → 2416991
- /internet-of-things/ → b82358c (HTML widget sx-hero-sub)
- /data-analytics/ → 6546043
- /digital-consulting/ → 7bf887c
- /software-as-a-service/ → 5996e42

## Deploy Pattern
- PHP via Code Snippets slot ID 5 (POST to /wp-json/code-snippets/v1/snippets/5)
- Self-deactivates after first run via `code_snippets()->deactivate(5)` + log file existence check
- Cache purge: AIOSEO core cache, WPO Page Cache, WPO Minify, wp_cache_flush

## Files
- _seo_v4.php: 8 page meta + JSON-LD snippet creation
- _seo_v5.php: 14 page meta + JSON-LD product URL fix
- _seo_v6.php: HTML lang=en + og_title/og_desc sync + WebSite SearchAction schema
- _seo_v7_ogimage.php: per-page og:image for 12 pages (products + portfolio + SURGE + About)
- _update_hero_html.py: regex patch sx-hero-sub on 4 raw-HTML service pages
- _artikel_v2.html: artikel page rewrite — English copy + 3 H2 sections + 8 topic links to services

## Subsequent Fixes (post-v5)
- Fixed INVALID JSON-LD in snippet 5182 (article-1925 schema wrapper: `application/ld+json` → `text/javascript`)
- Fixed INVALID JSON-LD in About page widget 8ef5419 (`\u2014` → literal em-dash)
- Added 5 missing alt attributes via /wp/v2/media: surge-eco-poster, modbus-poster, Porto, GTWY-SRT-VD, SURGE-WA
- Deleted 14 legacy "Remove Em Dash" snippets (5160-5173)
- Forced `<html lang="en">` via permanent code_snippets entry
- Added WebSite + SearchAction schema sitewide (sitelinks search box eligible)
- /artikel/ page (5260): H1 + 3 H2 hierarchy, 8 topic cross-link cards, English UI strings in snippet 5261

## Mobile UX Improvements (2026-05-19, post-SEO batch)
- Homepage 5 Core Services cards: removed "Learn More"/"Contact" CTAs, extended descriptions to 150-180 chars with keyword density
- Homepage Capabilities section: section bg removed (was full-viewport dark teal), inner widget wrapped in boxed card max-width:1100px, 10px radius, soft shadow — now visually consistent with Trusted By/Portfolio panels
- Mobile menu touch targets fixed via header snippet 5153 CSS injection: top-level items 38→48px, submenu items 20→44px (Apple HIG compliant)
- ~~Sticky WhatsApp FAB~~ — added then removed per user request (Olark chat widget already serves contact CTA)
- Sitemap verified healthy: sitemap.xml is INDEX (953 bytes), sub-sitemaps cover 200+ URLs (post: 64, page: 185, category, tag)
