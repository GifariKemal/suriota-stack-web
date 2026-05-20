# Cluster 2 Audit Report — Service Pages
**Date:** 2026-05-18  
**Auditor:** Automated Playwright + cURL audit pipeline  
**Cluster:** Desain Grafis, Automation, Electrical, Renewable Energy, Teknologi Informasi, Water Treatment  
**Screenshots:** `screenshots/audit-cluster2-2026-05-18/`

---

## Executive Summary

| Page | Score | Status |
|------|-------|--------|
| Water Treatment | **84/100** | ✅ Best-in-cluster |
| Electrical | **79/100** | ✅ Strong |
| Automation | **77/100** | ✅ Good |
| Renewable Energy | **77/100** | ✅ Good |
| Teknologi Informasi | **69/100** | ⚠️ Needs refactor |
| Desain Grafis | **65/100** | 🔴 Needs full rebuild |

**Cluster average: 75/100**

---

## Page 1 — Desain Grafis
**URL:** https://suriota.com/desain-grafis/  
**Post ID:** 33  
**Scores:** Design 23/25 | Mobile 10/15 | Performance 7/15 | SEO 12/25 | Accessibility 7/10 | Content 6/10 = **65/100**

### Screenshots
- Desktop: `screenshots/audit-cluster2-2026-05-18/audit-cluster2-desain-grafis-desktop.png`
- Mobile: `screenshots/audit-cluster2-2026-05-18/audit-cluster2-desain-grafis-mobile.png`

### Headings
| Tag | Text |
|-----|------|
| H1 | Desain Grafis |
| H1 | DESAIN GRAFIS |
| H4 | OUR SERVICES |
| H4 | PRODUCTS |
| H4 | CONNECT WITH US |

### Meta
- **Title:** "Desain Grafis - Suriota" — **23 chars** ❌ (optimal 50-60)
- **Description:** 380 chars ❌ (optimal 150-160; **severely overlong**)
- **Canonical:** ✅ `https://suriota.com/desain-grafis/`
- **OG Tags:** ✅ Title, desc, image, URL present
- **Schema:** BreadcrumbList, Organization, WebPage, WebSite — **missing Service schema**

### Elementor Widgets
```json
{
  "heading.default": 3,
  "text-editor.default": 1,
  "gallery.default": 1
}
```
Only **5 widgets total**. This page is on the **legacy basic template** — no Industrial Editorial design system applied.

### Findings
- **Images:** 2 total, 0 missing alt ✅
- **LCP:** Text-based ("Desain Grafis" H1) — no large hero image
- **Console errors:** 2
- **Load time:** 6,545ms ⚠️
- **CTA:** None detected ❌
- **Body text:** 1,644 chars — very thin content
- **Horizontal overflow:** None ✅
- **Tap targets:** 36 small on desktop, 32 on mobile

### Critical Issues
1. **Duplicate H1** — WordPress entry-title + Elementor heading widget both render H1
2. **Title too short** — 23 chars will be rewritten by Google
3. **Meta description 2.5× overlong** — 380 chars; will be truncated in SERP
4. **No CTA button** — No "Hubungi Kami", WA, or consultation button
5. **Legacy design** — Not using the Industrial Editorial v2 system (no cards, stats, process, FAQ)
6. **Thin content** — Only 1,644 chars; no service detail cards, no portfolio link

### Recommendations
- **Full rebuild** to match Automation/Water Treatment template structure
- Add hero gradient, industry badges, stats bar, service cards, process steps, FAQ accordion, CTA dual-action section
- Hide `.entry-title` via CSS (snippet 5154 may not be targeting this page)
- Rewrite title: "Jasa Desain Grafis Industrial & Branding | SURIOTA Batam" (~55 chars)
- Rewrite meta description to 150-160 chars
- Add `Service` JSON-LD schema
- Add portfolio gallery or case studies section

---

## Page 2 — Automation
**URL:** https://suriota.com/automation/  
**Post ID:** 35  
**Scores:** Design 23/25 | Mobile 10/15 | Performance 7/15 | SEO 20/25 | Accessibility 7/10 | Content 10/10 = **77/100**

### Screenshots
- Desktop: `screenshots/audit-cluster2-2026-05-18/audit-cluster2-automation-desktop.png`
- Mobile: `screenshots/audit-cluster2-2026-05-18/audit-cluster2-automation-mobile.png`

### Headings
| Tag | Text |
|-----|------|
| H1 | Automation Services |
| H1 | Automation & IoT Services |
| H2 | PLC, SCADA & IIoT integration for Industry 4.0 |
| H2 | Boost efficiency and productivity with SURIOTA automation solutions |
| H2 | Industry 4.0 automation, built for operational scale |
| H2 | Our Services |
| H2 | Frequently Asked Questions |
| H2 | Ready to automate your industrial operations? |
| H2 | Related Portfolio Projects |
| H3 | Vendor Agnostic PLC & SCADA |
| H3 | SURGE IIoT Platform |
| H3 | Modbus & OPC UA Ready |
| H3 | End to End Delivery |
| H3 | Cybersecurity Aware Design |
| H3 | Lifecycle Support |
| H3 | Our Process |
| H4 | Real Time IoT Monitoring |
| H4 | SURGE IIoT Platform |
| H4 | Automated Control Systems |
| H4 | Integration & Programming |
| H4 | HMI & Operator Interface |
| H4 | Industry 4.0 Digital Twin |
| H4 | OUR SERVICES (footer) |
| H4 | PRODUCTS (footer) |
| H4 | CONNECT WITH US (footer) |

### Meta
- **Title:** "Industrial Automation & IoT Services | SURIOTA SCADA PLC" — **60 chars** ✅
- **Description:** 134 chars ⚠️ (slightly short; optimal 150-160)
- **Canonical:** ✅
- **OG Tags:** ✅
- **Schema:** BreadcrumbList, Organization, WebPage, WebSite, **Service**, **FAQPage** — excellent ✅

### Elementor Widgets
```json
{
  "heading.default": 6,
  "button.default": 1,
  "html.default": 5,
  "text-editor.default": 4,
  "accordion.default": 1
}
```
**17 widgets** — full Industrial Editorial v2 layout.

### Findings
- **Images:** 3 total, 0 missing alt ✅
- **LCP:** Image — `Suriota-Automation-Services-scaled.jpg` (323×214px)
- **Console errors:** 2
- **Load time:** 6,075ms ⚠️
- **CTA:** ✅ Present ("Free Consultation" button + WhatsApp)
- **Body text:** 4,953 chars — rich content
- **Horizontal overflow:** None ✅
- **Tap targets:** 44 small on desktop, 40 on mobile

### Critical Issues
1. **Duplicate H1** — entry-title + Elementor heading both render

### Warnings
- Meta description slightly short (134 chars)
- 2 console errors (likely from emergency header/footer JS injector)
- Load time >6s (may be transient CDN/server issue)
- 40 small tap targets on mobile (mostly footer links)

### Recommendations
- Fix duplicate H1 by hiding `.entry-title` or changing Elementor widget to H2
- Expand meta description to 150-160 chars
- Add `primaryImageOfPage` to main JSON-LD @graph (already present in WebPage schema)

---

## Page 3 — Electrical
**URL:** https://suriota.com/electrical/  
**Post ID:** 37  
**Scores:** Design 23/25 | Mobile 10/15 | Performance 7/15 | SEO 22/25 | Accessibility 7/10 | Content 10/10 = **79/100**

### Screenshots
- Desktop: `screenshots/audit-cluster2-2026-05-18/audit-cluster2-electrical-desktop.png`
- Mobile: `screenshots/audit-cluster2-2026-05-18/audit-cluster2-electrical-mobile.png`

### Headings
| Tag | Text |
|-----|------|
| H1 | Electrical Services |
| H1 | Electrical Services |
| H2 | Industrial electrical engineering across Indonesia |
| H2 | Optimize your business with industrial electrical systems from SURIOTA |
| H2 | Compliant, IoT enabled electrical engineering |
| H2 | Our Services |
| H2 | Frequently Asked Questions |
| H2 | Ready to start your industrial electrical project? |
| H2 | Related Portfolio Projects |
| H3 | Compliance & Standards |
| H3 | Field Proven Experience |
| H3 | IoT Ready Integration |
| H3 | Local Engineering Support |
| H3 | Safety First Workflow |
| H3 | Complete Handover Package |
| H3 | Our Process |
| H4 | Electrical Installation |
| H4 | Commissioning & Testing |
| H4 | Maintenance & Repair |
| H4 | Design & Technical Calculation |
| H4 | Switchgear & Panel Building |
| H4 | Lighting & Cabling Systems |
| H4 | OUR SERVICES (footer) |
| H4 | PRODUCTS (footer) |
| H4 | CONNECT WITH US (footer) |

### Meta
- **Title:** "Industrial Electrical Engineering Services Batam | SURIOTA" — **58 chars** ✅
- **Description:** 159 chars ✅ (optimal)
- **Canonical:** ✅
- **OG Tags:** ✅
- **Schema:** BreadcrumbList, Organization, WebPage, WebSite, **FAQPage** — **missing explicit `Service` schema** (has WebPage but not Service)

### Elementor Widgets
```json
{
  "heading.default": 6,
  "button.default": 1,
  "html.default": 5,
  "text-editor.default": 4,
  "accordion.default": 1
}
```
**17 widgets** — full Industrial Editorial v2 layout.

### Findings
- **Images:** 3 total, 0 missing alt ✅
- **LCP:** Image — `listrik-logo.jpg` (323×225px)
- **Console errors:** 2
- **Load time:** 31,686ms 🔴 (extreme outlier — likely transient server issue)
- **CTA:** ✅ Present
- **Body text:** 5,052 chars — richest content in cluster
- **Horizontal overflow:** None ✅
- **Tap targets:** 43 small on desktop, 39 on mobile

### Critical Issues
1. **Duplicate H1** — both identical text "Electrical Services"

### Warnings
- Load time spiked to ~32s during audit (re-test recommended)
- Missing explicit `Service` JSON-LD schema (has FAQPage but no Service type)
- 2 console errors
- 39 small tap targets on mobile

### Recommendations
- Fix duplicate H1
- Add `Service` schema markup (copy from Automation or Water Treatment)
- Re-test performance; if consistent, investigate image/asset blocking

---

## Page 4 — Renewable Energy
**URL:** https://suriota.com/renewable-energy/  
**Post ID:** 39  
**Scores:** Design 23/25 | Mobile 10/15 | Performance 7/15 | SEO 20/25 | Accessibility 7/10 | Content 10/10 = **77/100**

### Screenshots
- Desktop: `screenshots/audit-cluster2-2026-05-18/audit-cluster2-renewable-energy-desktop.png`
- Mobile: `screenshots/audit-cluster2-2026-05-18/audit-cluster2-renewable-energy-mobile.png`

### Headings
| Tag | Text |
|-----|------|
| H1 | Renewable Energy Services |
| H1 | Renewable Energy Services |
| H2 | Solar PV & hybrid renewable energy across Indonesia |
| H2 | Toward a greener future with SURIOTA renewable energy solutions |
| H2 | Hybrid renewable energy with IoT performance tracking |
| H2 | Our Services |
| H2 | Frequently Asked Questions |
| H2 | Ready to switch to renewable energy? |
| H2 | Related Portfolio Projects |
| H3 | Feasibility First Approach |
| H3 | Hybrid PLTS + PLTB Systems |
| H3 | IoT Energy Monitoring |
| H3 | On Grid & Off Grid |
| H3 | PLN Permit Assistance |
| H3 | Proven ROI Track Record |
| H3 | Our Process |
| H4 | PLTS (Solar Panel) |
| H4 | PLTS PLTB Hybrid System |
| H4 | IoT Energy Monitoring |
| H4 | Consulting & Engineering |
| H4 | Battery Storage & BESS |
| H4 | Solar Street Lighting (PJU) |
| H4 | OUR SERVICES (footer) |
| H4 | PRODUCTS (footer) |
| H4 | CONNECT WITH US (footer) |

### Meta
- **Title:** "Solar PV & Renewable Energy Services | SURIOTA Indonesia" — **60 chars** ✅
- **Description:** 136 chars ⚠️ (slightly short)
- **Canonical:** ✅
- **OG Tags:** ✅
- **Schema:** BreadcrumbList, Organization, WebPage, WebSite, **Service**, **FAQPage** ✅

### Elementor Widgets
```json
{
  "heading.default": 6,
  "button.default": 1,
  "html.default": 5,
  "text-editor.default": 4,
  "accordion.default": 1
}
```
**17 widgets** — full Industrial Editorial v2 layout.

### Findings
- **Images:** 3 total, 0 missing alt ✅
- **LCP:** Image — `Suriota-Renewable-Energy-Services-scaled.jpg` (323×214px)
- **Console errors:** 2
- **Load time:** 10,908ms 🔴
- **CTA:** ✅ Present
- **Body text:** 4,940 chars
- **Horizontal overflow:** None ✅
- **Tap targets:** 44 small on desktop, 40 on mobile

### Critical Issues
1. **Duplicate H1** — both identical text

### Warnings
- Load time >10s
- Meta description slightly short
- 2 console errors
- 40 small tap targets on mobile

### Recommendations
- Fix duplicate H1
- Expand meta description to 150-160 chars
- Investigate load time (may be large hero image or transient issue)

---

## Page 5 — Teknologi Informasi
**URL:** https://suriota.com/teknologi-informasi/  
**Post ID:** 41  
**Scores:** Design 23/25 | Mobile 10/15 | Performance 7/15 | SEO 12/25 | Accessibility 7/10 | Content 10/10 = **69/100**

### Screenshots
- Desktop: `screenshots/audit-cluster2-2026-05-18/audit-cluster2-teknologi-informasi-desktop.png`
- Mobile: `screenshots/audit-cluster2-2026-05-18/audit-cluster2-teknologi-informasi-mobile.png`

### Headings
| Tag | Text |
|-----|------|
| H1 | Teknologi Informasi |
| H1 | TEKNOLOGI INFORMASI |
| H4 | OUR SERVICES |
| H4 | PRODUCTS |
| H4 | CONNECT WITH US |

### Meta
- **Title:** "Teknologi Informasi - Suriota" — **29 chars** ❌ (far too short)
- **Description:** 419 chars ❌ (severely overlong)
- **Canonical:** ✅
- **OG Tags:** ✅
- **Schema:** BreadcrumbList, Organization, WebPage, WebSite — **missing Service schema**

### Elementor Widgets
```json
{
  "heading.default": 3,
  "image.default": 1,
  "text-editor.default": 1
}
```
Only **5 widgets** — legacy basic template. Not using Industrial Editorial v2.

### Findings
- **Images:** 3 total, 0 missing alt ✅
- **LCP:** Image — `teknologi-informasi-logo.jpg` (355×295px)
- **Console errors:** 2
- **Load time:** 12,557ms 🔴
- **CTA:** ✅ Present (text-based "Hubungi kami" link in body)
- **Body text:** 1,542 chars — thin content
- **Horizontal overflow:** None ✅
- **Tap targets:** 36 small on desktop, 32 on mobile

### Critical Issues
1. **Duplicate H1** — entry-title sentence case + Elementor widget ALL CAPS
2. **Title far too short** — 29 chars
3. **Meta description 2.8× overlong** — 419 chars
4. **Legacy design** — no cards, stats, process, FAQ, CTA section
5. **Thin content** — only 1,542 chars
6. **Missing Service schema**

### Recommendations
- **Full rebuild** to match Water Treatment/Automation template
- Rewrite title: "IT Solutions & Industrial Software Development | SURIOTA" (~58 chars)
- Rewrite meta description to 150-160 chars
- Add service detail cards (IoT Development, Web App, SaaS, System Integration)
- Add process steps, FAQ accordion, CTA dual-action section
- Add portfolio/case study links
- Hide `.entry-title` to fix duplicate H1

---

## Page 6 — Water Treatment
**URL:** https://suriota.com/water-treatment/  
**Post ID:** 945  
**Scores:** Design 23/25 | Mobile 10/15 | Performance 10/15 | SEO 24/25 | Accessibility 7/10 | Content 10/10 = **84/100**

### Screenshots
- Desktop: `screenshots/audit-cluster2-2026-05-18/audit-cluster2-water-treatment-desktop.png`
- Mobile: `screenshots/audit-cluster2-2026-05-18/audit-cluster2-water-treatment-mobile.png`

### Headings
| Tag | Text |
|-----|------|
| H1 | Water Treatment Services |
| H2 | WTP, WWTP & SPARING monitoring across Indonesia |
| H2 | Pure water treatment solutions for a sustainable future with SURIOTA |
| H2 | Compliant water treatment with IoT monitoring |
| H2 | Our Services |
| H2 | Frequently Asked Questions |
| H2 | Ready to upgrade your water treatment system? |
| H2 | Related Portfolio Projects |
| H3 | KLHK SPARING Compliance |
| H3 | PDAM Trusted Delivery |
| H3 | SURGE Water Analytics |
| H3 | Full Treatment Spectrum |
| H3 | Lab & Calibration Services |
| H3 | Operator Training & SOP |
| H3 | Our Process |
| H4 | Water Treatment Plant (WTP) |
| H4 | Waste Water Treatment (WWTP) |
| H4 | Pumps & Mechanical |
| H4 | Water Quality Monitoring |
| H4 | RO & UF Membrane Systems |
| H4 | Chemical Dosing & Sludge Handling |
| H4 | OUR SERVICES (footer) |
| H4 | PRODUCTS (footer) |
| H4 | CONNECT WITH US (footer) |

### Meta
- **Title:** "Water Treatment Plant & IoT Monitoring | SURIOTA Batam" — **58 chars** ✅
- **Description:** 134 chars ⚠️ (slightly short)
- **Canonical:** ✅
- **OG Tags:** ✅
- **Schema:** BreadcrumbList, Organization, WebPage, WebSite, **Service**, **FAQPage** ✅ — **best schema coverage in cluster**

### Elementor Widgets
```json
{
  "heading.default": 6,
  "button.default": 1,
  "html.default": 5,
  "text-editor.default": 4,
  "accordion.default": 1
}
```
**17 widgets** — full Industrial Editorial v2 layout.

### Findings
- **Images:** 3 total, 0 missing alt ✅
- **LCP:** Image — `Suriota-Water-Treatment-Services-scaled.jpg` (323×323px)
- **Console errors:** 2
- **Load time:** 4,794ms ✅ (fastest in cluster)
- **CTA:** ✅ Present (Free Consultation + WhatsApp)
- **Body text:** ~5,000 chars
- **Horizontal overflow:** None ✅
- **Tap targets:** 40 small on mobile

### Critical Issues
**NONE** — This is the reference page for the cluster.

### Warnings
- Meta description slightly short (134 chars)
- 2 console errors
- 40 small tap targets on mobile

### Recommendations
- Expand meta description to 150-160 chars
- Consider adding `LocalBusiness` or `ProfessionalService` schema for Batam location
- Use as the **template reference** for rebuilding Desain Grafis and Teknologi Informasi

---

## Cross-Page Pattern Analysis

### Design System Consistency
| Page | Design System | Hero Gradient | Stats | Cards | Process | FAQ | CTA | Portfolio |
|------|--------------|---------------|-------|-------|---------|-----|-----|-----------|
| Desain Grafis | ❌ Legacy | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Automation | ✅ v2 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Electrical | ✅ v2 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Renewable Energy | ✅ v2 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Teknologi Informasi | ❌ Legacy | ❌ | ❌ | ❌ | ❌ | ❌ | ⚠️ text only | ❌ |
| Water Treatment | ✅ v2 | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

**4 of 6 pages** use the new Industrial Editorial v2 design. **2 pages** (Desain Grafis, Teknologi Informasi) are stuck on the legacy basic template.

### SEO Meta Quality
| Page | Title Len | Status | Desc Len | Status | H1 Count | Schema Service |
|------|-----------|--------|----------|--------|----------|----------------|
| Desain Grafis | 23 | 🔴 | 380 | 🔴 | 2 | ❌ |
| Automation | 60 | ✅ | 134 | ⚠️ | 2 | ✅ |
| Electrical | 58 | ✅ | 159 | ✅ | 2 | ❌ |
| Renewable Energy | 60 | ✅ | 136 | ⚠️ | 2 | ✅ |
| Teknologi Informasi | 29 | 🔴 | 419 | 🔴 | 2 | ❌ |
| Water Treatment | 58 | ✅ | 134 | ⚠️ | 1 | ✅ |

### Duplicate H1 Analysis
All pages **except Water Treatment** have duplicate H1 elements. Root cause: the WordPress `entry-title` H1 and the Elementor Heading widget H1 both render on the page. The `.entry-title` hiding CSS (snippet 5154) is not effective on these pages.

**Water Treatment** correctly has only 1 H1 because its `.entry-title` is successfully hidden or the page template handles it differently.

### Console Errors
All 6 pages show **2 console errors**. These are consistent across the cluster and correlate with the known **Elementor Pro Theme Builder template index corruption** bug. The emergency JS injector (snippet 5153) reconstructs header/footer, and these errors likely stem from missing template fragments or DOM manipulation race conditions.

### Performance
| Page | Load Time | Status |
|------|-----------|--------|
| Water Treatment | 4,794ms | ✅ |
| Automation | 6,075ms | ⚠️ |
| Desain Grafis | 6,545ms | ⚠️ |
| Renewable Energy | 10,908ms | 🔴 |
| Teknologi Informasi | 12,557ms | 🔴 |
| Electrical | 31,686ms | 🔴 |

Note: Electrical's 31s is likely a transient outlier. All pages are served through Cloudflare; spikes may be due to cache misses or origin server load during the audit window.

---

## Accessibility Findings

### Alt Text
- **All 6 pages:** 0 images missing alt text ✅
- All images have descriptive alt text (e.g., "SURIOTA Industrial Automation & IoT Services Batam")

### Contrast
- **Low-contrast elements detected:** 6-7 per page
- These are primarily subtle text elements (footer secondary text, eyebrow labels) that may fall below WCAG AA against light backgrounds
- The Industrial Editorial v2 pages use a lighter teal `#205B69` which on white passes AA for large text but may be marginal for small body text

### ARIA
- **1 nav element missing `aria-label`** on all pages — likely the mobile menu toggle or a navigation wrapper
- Footer navigation uses H4 headings as visual labels but lacks `role="navigation"` or `aria-label`

### Keyboard Focus
- Not tested in this automated audit; manual verification recommended for:
  - FAQ accordion keyboard expand/collapse
  - CTA button focus rings
  - Mobile menu trap-focus behavior

---

## Action Priority Matrix

### 🔴 P0 — Critical (Fix This Week)
| # | Action | Pages | Impact |
|---|--------|-------|--------|
| 1 | Fix duplicate H1 | All except Water Treatment | SEO |
| 2 | Rewrite title + meta description | Desain Grafis, Teknologi Informasi | SEO |
| 3 | Rebuild Desain Grafis to v2 template | Desain Grafis | Design, Content, CRO |
| 4 | Rebuild Teknologi Informasi to v2 template | Teknologi Informasi | Design, Content, CRO |

### 🟡 P1 — High (Fix Within 2 Weeks)
| # | Action | Pages | Impact |
|---|--------|-------|--------|
| 5 | Expand meta descriptions to 150-160 chars | Automation, Renewable Energy, Water Treatment | SEO |
| 6 | Add `Service` schema markup | Electrical, Desain Grafis, Teknologi Informasi | SEO |
| 7 | Investigate and resolve 2 console errors | All | A11y, Stability |
| 8 | Add `aria-label="Main navigation"` to nav | All | A11y |

### 🟢 P2 — Medium (Fix Within Month)
| # | Action | Pages | Impact |
|---|--------|-------|--------|
| 9 | Optimize hero images (WebP/AVIF, lazy loading) | Automation, Electrical, Renewable, Water Treatment | Performance |
| 10 | Reduce small tap targets in footer | All | Mobile UX |
| 11 | Add `LocalBusiness` schema with Batam coordinates | All | Local SEO |
| 12 | Add `review` or `aggregateRating` to Service schema | All | SERP Rich Snippets |

---

## Appendix: Elementor Structure Summary

```
Desain Grafis (33)     →  5 widgets  → Legacy basic
Teknologi Informasi(41)→  5 widgets  → Legacy basic
Automation (35)        → 17 widgets  → Industrial Editorial v2
Electrical (37)        → 17 widgets  → Industrial Editorial v2
Renewable Energy (39)  → 17 widgets  → Industrial Editorial v2
Water Treatment (945)  → 17 widgets  → Industrial Editorial v2
```

The v2 template uses a consistent widget pattern:
- `heading.default` ×6 (hero H1, eyebrow, section H2s)
- `button.default` ×1 (hero CTA)
- `html.default` ×5 (stats bar, service cards, process steps, trust cards — inline HTML/CSS)
- `text-editor.default` ×4 (body copy blocks)
- `accordion.default` ×1 (FAQ section)

---

*Report generated by `scripts/audit-cluster2.js` on 2026-05-18.*
*Raw data: `screenshots/audit-cluster2-2026-05-18/audit-cluster2-raw.json`*
