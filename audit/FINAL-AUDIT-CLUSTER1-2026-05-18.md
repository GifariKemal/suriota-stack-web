# Audit Report — Cluster 1 (Homepage, About Us, Tentang)
**Date:** 2026-05-18  
**Auditor:** Kimi Code CLI  
**Method:** Puppeteer DOM audit + raw HTML crawl + visual screenshot review  

---

## 1. HOMEPAGE

```
Page: Homepage
URL: https://suriota.com/
Post ID: 12
Scores: Design=17/25 | Mobile=10/15 | Performance=7/15 | SEO=10/25 | A11y=5/10 | Content=7/10
Total: 56/100
```

### Screenshots
- Desktop: `screenshots/audit-2026-05-18/audit-cluster1-homepage-desktop.png` (1440×3826)
- Mobile: `screenshots/audit-2026-05-18/audit-cluster1-homepage-mobile.png` (375×6458)

### Headings (12 total)
| Tag | Text | Note |
|-----|------|------|
| H1 | Homepage | `.entry-title` — hidden via `display:none` |
| H1 | Next Gen. Industrial Partner | Visible hero heading |
| H3 | IoT & System Integration | Service card |
| H3 | AI & Data Analytics | Service card |
| H3 | Software as a Service | Service card |
| H3 | Automation & Renewable Energy | Service card |
| H3 | Digital Consulting | Service card |
| H2 | Our Location | |
| H2 | Contact Us | |
| H4 | OUR SERVICES | Footer column |
| H4 | PRODUCTS | Footer column |
| H4 | CONNECT WITH US | Footer column |

**Heading hierarchy issue:** H1 → H3 (skips H2). Two H1s present.

### Missing Alt Text
**3 images missing alt:**
1. `surge-eco-poster-512x258.webp` (512×258, visible)
2. `modbus-poster-512x123.webp` (512×123, visible)
3. `Porto.jpg` (1439×809, visible) — portfolio table background/image

### Meta Tags
- **Title:** `Suriota - Surya Inovasi Prioritas` — **33 chars** (❌ too short; target 50–60)
- **Description:** `PT Surya Inovasi Prioritas atau Suriota merupakan sebuah perusahaan yang bergerak di Technology Engineering Service berlokasi di Batam.` — **111 chars** (⚠️ could be expanded to 150–160)
- **Canonical:** `https://suriota.com/` ✅
- **OG Tags:** Complete (locale, site_name, type, title, desc, url, image 1200×620) ✅
- **Twitter Cards:** 4 tags present (summary_large_image) ✅
- **Robots:** `max-image-preview:large`

### Schema Markup
**0 JSON-LD blocks found** ❌ CRITICAL — no Organization, WebSite, or LocalBusiness schema.

### Elementor Structure
- **Widgets:** 25
- **Sections:** 11
- **hasElementorConfig:** true

### Console Errors (2)
1. `Access to script at 'https://embed.tawk.to/...' has been blocked by CORS policy`
2. `Failed to load resource: net::ERR_FAILED` (Tawk.to)

### Performance
- **Load time:** 8,785 ms (networkidle2 + 3s settle)
- **LCP candidate:** H1 text "Next Gen. Industrial Partner" (1400×53)
- **JS files:** 12 (jQuery, Elementor, Swiper, Elementor Pro)
- **Preload hints:** 0
- **Horizontal scroll:** No ✅
- **Small touch targets:** 43 (social icons, footer links, product card CTAs)

### Critical Issues
1. **Zero schema markup** — missing Organization, WebSite, LocalBusiness structured data
2. **Duplicate H1** — `.entry-title` hidden but still in DOM; visible H1 is "Next Gen. Industrial Partner"
3. **3 product/portfolio images missing alt text**
4. **Title too short** (33 chars)
5. **8.8s load time** — heavy page with many JS assets

### Warnings
1. Heading hierarchy skips H2 (H1 → H3)
2. 43 touch targets below 44px
3. Tawk.to CORS error on every load
4. Meta description could be longer (111 chars)
5. No preload hints for critical assets

### Recommendations
1. Add JSON-LD `@graph` schema (Organization + WebSite + LocalBusiness) — follow About Us pattern
2. Fix `.entry-title` to use `<div>` or remove entirely; keep single H1
3. Add `alt` attributes to surge-eco-poster, modbus-poster, and Porto.jpg
4. Expand title to 50–60 chars: *"Suriota | Industrial IoT & System Integration — Batam, Indonesia"*
5. Expand meta description to 150–160 chars
6. Add `loading="lazy"` to below-fold images; preload hero font/CSS
7. Audit Tawk.to embed — consider defer or fix CORS
8. Convert H3 service cards to H2 (or add H2 section heading above them)

---

## 2. ABOUT US

```
Page: About Us
URL: https://suriota.com/about-us/
Post ID: 29
Scores: Design=21/25 | Mobile=12/15 | Performance=9/15 | SEO=14/25 | A11y=6/10 | Content=9/10
Total: 71/100
```

### Screenshots
- Desktop: `screenshots/audit-2026-05-18/audit-cluster1-about-us-desktop.png` (1440×2248)
- Mobile: `screenshots/audit-2026-05-18/audit-cluster1-about-us-mobile.png` (375×4529)

### Headings (14 total)
| Tag | Text | Note |
|-----|------|------|
| H1 | About Us | `.entry-title` — hidden via `display:none` |
| H1 | About SURIOTA | Visible hero heading |
| H3 | Transforming industries through smart, connected solutions. | |
| H2 | SURIOTA Industrial IoT & System Integration | |
| H2 | *(empty)* | ❌ Empty heading in DOM |
| H3 | *(empty)* | ❌ Empty heading |
| H3 | *(empty)* | ❌ Empty heading |
| H3 | *(empty)* | ❌ Empty heading |
| H3 | *(empty)* | ❌ Empty heading |
| H3 | *(empty)* | ❌ Empty heading |
| H2 | Ready to Collaborate with SURIOTA? | CTA section |
| H4 | OUR SERVICES | Footer column |
| H4 | PRODUCTS | Footer column |
| H4 | CONNECT WITH US | Footer column |

**Heading hierarchy issue:** Duplicate H1s. Six completely empty headings (H2×1 + H3×5).

### Missing Alt Text
**0 images missing alt** ✅

### Meta Tags
- **Title:** `About Us - Suriota` — **19 chars** (❌ far too short; target 50–60)
- **Description:** `About SURIOTA Next Gen. Industrial Partner — Industrial IoT & System Integration in Batam, Indonesia 01 / VISION Transforming industries through smart, connected solutions...` — **~431 chars** (❌ far too long; will be truncated by Google)
- **Canonical:** `https://suriota.com/about-us/` ✅
- **OG Tags:** Complete ✅
- **Twitter Cards:** 4 tags present ✅
- **Robots:** `max-image-preview:large`

### Schema Markup
**1 JSON-LD block found** ✅
- `@graph`: `[Organization, LocalBusiness]`, `AboutPage`, `BreadcrumbList`

### Elementor Structure
- **Widgets:** 8
- **Sections:** 5
- **hasElementorConfig:** true

### Console Errors (2)
1. Tawk.to CORS policy error
2. `Failed to load resource: net::ERR_FAILED`

### Performance
- **Load time:** 4,715 ms
- **LCP candidate:** H1 text "About SURIOTA" (1120×48)
- **JS files:** 11
- **Preload hints:** 0
- **Horizontal scroll:** No ✅
- **Small touch targets:** 38

### Critical Issues
1. **6 empty headings** in DOM — severe screen-reader pollution
2. **Title extremely short** (19 chars)
3. **Meta description extremely long** (~431 chars)
4. **Duplicate H1** (hidden `.entry-title` + visible "About SURIOTA")

### Warnings
1. 38 small touch targets
2. Tawk.to CORS error
3. No preload hints
4. Heading hierarchy could be cleaner (H1→H3→H2 jump)

### Recommendations
1. **Remove or fill empty headings** — 1 empty H2 and 5 empty H3s are likely spacer/animation widgets; convert to `<div>`
2. Rewrite title: *"About Us | Suriota — Industrial IoT & System Integration"* (54 chars)
3. Trim meta description to 150–160 chars; remove vision/mission body text from meta
4. Consolidate to single H1 (remove hidden `.entry-title` or make it `<div>`)
5. Add `preload` for Plus Jakarta Sans / IBM Plex Mono fonts
6. Consider adding `BreadcrumbList` visible breadcrumb navigation

---

## 3. TENTANG

```
Page: Tentang
URL: https://suriota.com/tentang/
Post ID: 376
Scores: Design=2/25 | Mobile=3/15 | Performance=3/15 | SEO=2/25 | A11y=2/10 | Content=1/10
Total: 13/100
```

### Screenshots
- Desktop: `screenshots/audit-2026-05-18/audit-cluster1-tentang-desktop.png` (1440×900)
- Mobile: `screenshots/audit-2026-05-18/audit-cluster1-tentang-mobile.png` (375×1489)

### Headings (4 total)
| Tag | Text | Note |
|-----|------|------|
| H1 | Halaman tidak dapat ditemukan. | 404 page title |
| H4 | OUR SERVICES | Footer column |
| H4 | PRODUCTS | Footer column |
| H4 | CONNECT WITH US | Footer column |

### Missing Alt Text
**0 images**

### Meta Tags
- **Title:** `Laman tidak ditemukan – Suriota` — **38 chars** (❌ 404 title)
- **Description:** *None found* ❌
- **Canonical:** *None found* ❌
- **OG Tags:** Only basic `og:locale` and `og:site_name`
- **Twitter Cards:** 0 tags ❌
- **Robots:** `noindex` ❌

### Schema Markup
**0 JSON-LD blocks found** ❌

### Elementor Structure
- **Widgets:** 0
- **Sections:** 0
- **hasElementorConfig:** false
- This is **NOT an Elementor page** — it renders the theme's 404 template.

### Console Errors (3)
1. `Failed to load resource: the server responded with a status of 404 ()`
2. Tawk.to CORS error
3. `Failed to load resource: net::ERR_FAILED`

### Performance
- **Load time:** 5,097 ms
- **LCP candidate:** H1 text "Halaman tidak dapat ditemukan." (1140×48)
- **JS files:** 0 in raw HTML (404 template)
- **Horizontal scroll:** No ✅
- **Small touch targets:** 36

### Critical Issues
1. **Page is completely broken (404)** — URL returns "Halaman tidak dapat ditemukan"
2. **Noindex** — explicitly blocked from search engines
3. **No meta description, no canonical, no schema**
4. **No Elementor content** — post_id 376 appears to be deleted, draft, or slug mismatch

### Warnings
1. 404 page load time is 5.1s (slow for an error page)
2. Footer is still the emergency reconstructed footer

### Recommendations
1. **Investigate post_id 376** in WP Admin — check if page is trashed, draft, or slug changed
2. If page is intentionally removed, set up a **301 redirect** from `/tentang/` to `/about-us/`
3. If page should exist, restore/publish it and ensure Elementor template is assigned
4. Customize 404 template to include search bar + suggested links (About Us, Services, Contact)
5. Ensure 404 page has basic meta description and branded messaging

---

## CROSS-PAGE FINDINGS

### Shared Critical Issues
| Issue | Homepage | About Us | Tentang |
|-------|----------|----------|---------|
| Duplicate H1 (hidden `.entry-title`) | ✅ | ✅ | N/A |
| Tawk.to CORS console error | ✅ | ✅ | ✅ |
| No preload hints | ✅ | ✅ | ✅ |
| Zero or weak schema | ✅ (0) | ✅ (good) | ✅ (0) |
| Emergency header/footer dependency | ✅ | ✅ | ✅ |

### Shared Recommendations
1. **Fix Tawk.to embed** — the CORS error appears on every page. Check Tawk.to dashboard or defer script loading.
2. **Add `rel="preload"`** for critical fonts (Poppins, Lato, Plus Jakarta Sans, IBM Plex Mono) and the first viewport image.
3. **Standardize H1 handling** — either remove `.entry-title` from the DOM entirely or change it to `<div class="entry-title">` so it doesn't create duplicate H1s.
4. **Review Elementor Pro Theme Builder** — the emergency header/footer JS (snippets 5153/5154) is still active. Monitor native template restoration.

---

*Report generated by automated audit pipeline. Screenshots and raw JSON saved to `screenshots/audit-2026-05-18/`.*
