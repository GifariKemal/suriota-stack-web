# Audit Cluster 4 — Portfolio + Internship
**Date:** 2026-05-18  
**Auditor:** Kimi Code CLI (subagent)  
**Tools Used:** Playwright (screenshot + DOM extraction), FetchURL/curl (raw HTML), Python analysis (meta/schema/widget audit)  
*Note: `elementor-mcp-get-page-structure` and `puppeteer_*` MCP tools were not directly available in this subagent context; equivalent audits were performed via shell scripts and raw HTML analysis.*

---

## Page 1: Portfolio

```
Page: Portfolio
URL: https://suriota.com/portfolio/
Post ID: 839
Scores: Design=12/Mobile=12/Performance=5/SEO=13/A11y=6/Content=6 = 54/100
Screenshots:
  - screenshots/audit-cluster4/audit-cluster4-portfolio-desktop.png (1440×900)
  - screenshots/audit-cluster4/audit-cluster4-portfolio-mobile.png (375×812)
```

### Headings (6 total)
| Level | Text | Notes |
|-------|------|-------|
| H1 | Portfolio | `.entry-title` — duplicate H1 |
| H1 | Portfolio | Elementor heading — duplicate H1 |
| H2 | Interested in Working Together? | CTA section at bottom |
| H4 | Our Services | Footer (emergency injected) |
| H4 | Products | Footer (emergency injected) |
| H4 | Connect with Us | Footer (emergency injected) |

**Heading Hierarchy Issues:**
- **CRITICAL:** Two H1 tags (entry-title + Elementor widget). SEO penalty risk.
- No H2 or H3 between the hero H1 and the footer H4s in DOM order.
- The massive project table (64 rows) contains zero heading tags — screen-reader users cannot navigate by heading within the primary content.

### Images
- **Total:** 2 images
- **Missing Alt:** 0 ✅
- **LCP Candidate:** Logo image (`Logo-Suriota-Putih-512x109.png`, ~6,782 px² area)

### Meta Tags
- **Title:** `Portfolio - Suriota` — **19 chars** ❌ (target: 50–60)
- **Description:** 440 chars ❌ (target: 150–160; truncated by Google)
- **Canonical:** `https://suriota.com/portfolio/` ✅
- **OG Tags:** Complete (locale, site_name, type, title, description, url, image 1200×620, twitter card) ✅

### Schema Markup (JSON-LD)
Script 1 (AIOSEO): `BreadcrumbList`, `Organization`, `WebPage`, `WebSite`  
Script 2 (manual): `ItemList`

### Elementor Widget Audit
- **Sections:** 2 top-level
- **Columns:** 2
- **Widgets:** `heading.default` ×1, `text-editor.default` ×1
- **Structure Note:** The entire 64-row project table and stats bar are rendered inside a single `text-editor.default` widget (HTML table + inline stats). No dedicated Counter, Loop, or Posts widgets are used.

### Performance Metrics
- **Load Time:** ~7,620 ms (networkidle) ❌ Very slow for a text-heavy page
- **Scroll Height:** 9,774 px ❌ Extremely long single-page scroll
- **Console Errors:** 2× CORS errors from Tawk.to embed (`embed.tawk.to`) — non-critical but noisy
- **Asset Count:** Only 2 images; bloat is likely from Elementor JS/CSS and the massive inline HTML table

### Accessibility Findings
- **Table Semantics:** `<table>` with 65 rows (1 header + 64 data) but **no `<caption>`** and **no `scope` attributes** on `<th>` cells ❌
- **ARIA:** 7 `aria-label` attributes (navigation), 0 `role` definitions
- **Contrast:** White text on teal header (#205B69) estimated ~5.6:1 ✅; dark text on white background ✅
- **Touch Targets:** One anchor at 178×38 px (hamburger area); dropdown nav items measure 0×0 px in collapsed state (expected for hidden menu)

### Design Assessment
- **Visual Hierarchy:** Weak. Flat table layout with no project imagery, case-study cards, or interactivity beyond year-filter pills.
- **Stats Bar:** Four stat cards (64+ Projects, 20+ Clients, 3+ Years, 5 Services) use simple boxed layout — no icons, no animated counters, no hover states.
- **Year Filters:** Three pill buttons (2025 / 2024 / 2023) — unclear if they actually filter or are purely visual.
- **Mobile Adaptation:** Table collapses into vertical cards with amber year badges. Readable but still extremely long.
- **Brand Alignment:** Teal/amber color tokens present, but the plain HTML table feels out of step with the Industrial Editorial design system established on About Us and Internship.

### Content Assessment
- **Grammar/Clarity:** Good. Project names and client names are clear.
- **CTA:** "Interested in Working Together?" appears at the bottom — generic, no email link or form button visible in the screenshot.
- **Value Proposition Missing:** No intro paragraph explaining SURIOTA's methodology, industries served, or success metrics beyond the raw stat numbers.

---

### Critical Issues (Portfolio)
1. **Duplicate H1** — entry-title + Elementor heading both read "Portfolio"
2. **Meta description 440 chars** — will be truncated in SERPs, poor click-through rate
3. **Page load ~7.6 s** — unacceptable for a text page; likely render-blocking JS/CSS
4. **Table lacks `<caption>` and `scope`** — screen-reader navigation impaired
5. **No project detail links** — 64 rows of dead-end text; no way to explore a case study

### Warnings (Portfolio)
- Title tag only 19 characters (missing keyword opportunity)
- Page height 9,774 px creates cognitive overload
- Tawk.to CORS console errors
- Footer H4s semantically outrank the main H2 in DOM order

### Recommendations (Portfolio)
1. Hide `.entry-title` via CSS (`display:none !important`) to resolve duplicate H1
2. Rewrite `<title>` to: `Project Portfolio | Industrial IoT & Engineering — SURIOTA` (~58 chars)
3. Rewrite meta description to 150–160 char summary with value prop and CTA
4. Refactor table into paginated/filterable project cards (reuse `sx-card` pattern from About Us)
5. Add `<caption>` and `scope="col"` to table headers (or migrate to accessible card grid)
6. Add project detail/case-study links (even if anchor links to blog posts)
7. Defer non-critical JS to reduce load time below 3 s
8. Add a "Trusted By" client-logo section above the table for social proof

---

---

## Page 2: Internship

```
Page: Internship
URL: https://suriota.com/internship/
Post ID: 1127
Scores: Design=20/Mobile=14/Performance=8/SEO=16/A11y=8/Content=9 = 75/100
Screenshots:
  - screenshots/audit-cluster4/audit-cluster4-internship-desktop.png (1440×900)
  - screenshots/audit-cluster4/audit-cluster4-internship-mobile.png (375×812)
```

### Headings (12 total)
| Level | Text | Notes |
|-------|------|-------|
| H1 | Internship | `.entry-title` — duplicate H1 |
| H1 | Build Your Tech Career with SURIOTA | Hero heading |
| H2 | Where You'll Make an Impact | Section title |
| H3 | R&D App Developer | Position card |
| H3 | DevOps Engineer | Position card |
| H3 | QA Specialist | Position card |
| H3 | UI/UX Designer | Position card |
| H2 | Why Intern at SURIOTA? | Section title |
| H2 | Ready to Start Your Tech Career? | CTA section |
| H4 | Our Services | Footer (emergency injected) |
| H4 | Products | Footer (emergency injected) |
| H4 | Connect with Us | Footer (emergency injected) |

**Heading Hierarchy:** Excellent progression H1 → H2 → H3 in main content body. Only issue is the duplicate H1 from entry-title.

### Images
- **Total:** 3 images
- **Missing Alt:** 0 ✅
- **LCP Candidate:** Poster image (`4.png`, ~97,860 px² area) — dominates LCP

### Meta Tags
- **Title:** `Internship - Suriota` — **20 chars** ❌ (target: 50–60)
- **Description:** 322 chars ❌ (target: 150–160; truncated by Google)
- **Canonical:** `https://suriota.com/internship/` ✅
- **OG Tags:** Complete (same cover image 1200×620, twitter card) ✅

### Schema Markup (JSON-LD)
Script 1 (AIOSEO): `BreadcrumbList`, `Organization`, `WebPage`, `WebSite`  
Script 2 (manual): `JobPosting` ✅ (valuable for Google for Jobs)

### Elementor Widget Audit
- **Sections:** 1 top-level (content rendered via `text-editor.default` with heavy inline HTML/CSS)
- **Columns:** 1
- **Widgets:** `text-editor.default` ×1
- **Structure Note:** The entire refactored Internship page (hero, cards, collapsible sections, tech stack, CTA) is rendered inside a single Text Editor widget with inline CSS. This matches the 2026-05-13 refactor documented in AGENTS.md.

### Performance Metrics
- **Load Time:** ~6,505 ms (networkidle) ❌ Slow
- **Scroll Height:** 3,976 px — reasonable for content depth
- **Console Errors:** 2× CORS errors from Tawk.to embed — non-critical
- **LCP Estimate:** Poster image (`4.png`) is massive; likely the LCP element

### Accessibility Findings
- **Collapsible Sections:** 2× native `<details>` / `<summary>` elements used for Qualifications and Benefits ✅ Zero-JS, keyboard-accessible, screen-reader friendly
- **ARIA:** 7 `aria-label` attributes, 6 `aria-hidden` attributes (likely decorative poster elements)
- **Contrast:** White on teal header ✅; teal CTA buttons on white (#205B69 on #FFFFFF ≈ 5.6:1) ✅; amber badges on white (#C8851F on #FFFFFF ≈ 3.1:1 — may be borderline for small text)
- **Touch Targets:** Apply Now button and position cards appear well-sized; nav dropdown items 0×0 when collapsed (expected)

### Design Assessment
- **Visual Hierarchy:** Strong. Eyebrow (`INTERNSHIP PROGRAM`), amber badge (`BATCH 3 · NOW OPEN`), large H1, subtitle, primary CTA, poster image, info pills, section titles, numbered position cards (01–04), tech-stack badges, collapsible details.
- **Industrial Editorial Compliance:** Uses mono numerics for badges, teal deep headings, amber accents, disciplined spacing. Aligns well with the `sx-` design system.
- **Mobile Adaptation:** Hero stacks vertically (poster on top, text below on 375 px). Position cards become 2×2 grid. Collapsible sections remain functional.
- **Poster Image:** Prominent and clear on both desktop and mobile — addresses earlier feedback about poster visibility.

### Content Assessment
- **Grammar/Clarity:** Excellent. Professional tone, clear role descriptions.
- **CTA:** Strong — "Apply Now" primary button + email CTA with explicit subject-line instruction.
- **Value Proposition:** Complete — duration (3–6 months), modality (hybrid), location (Batam), 4 open positions, required documents, benefits, tech stack.

---

### Critical Issues (Internship)
1. **Duplicate H1** — entry-title "Internship" + hero H1
2. **Meta description 322 chars** — will be truncated in SERPs
3. **Title tag only 20 chars** — missing "Program", "Batch 3", "Batam", "IoT" keywords
4. **Load time ~6.5 s** — poster image and render-blocking assets need optimization

### Warnings (Internship)
- LCP candidate is a large poster image; if unoptimized, mobile users on slow networks will see delayed paint
- Tawk.to CORS console errors
- Amber badge text (#C8851F on white) may fail WCAG AA for small text if font weight is below 400

### Recommendations (Internship)
1. Hide `.entry-title` via CSS to fix duplicate H1
2. Rewrite `<title>` to: `Internship Batch 3 | Industrial IoT & Engineering — SURIOTA` (~56 chars)
3. Rewrite meta description to 150–160 char summary focusing on Batam, 4 roles, and real-project experience
4. Compress and serve poster image (`4.png`) in WebP/AVIF with `srcset`; add `fetchpriority="high"`
5. Add `JobPosting` schema validation in Google's Rich Results Test (currently present but should be verified)
6. Add an application form or direct Calendly link in addition to the email CTA
7. Consider converting the single Text Editor widget into reusable Elementor templates (SX Hero, SX Card Grid, SX CTA) for easier maintenance

---

## Cross-Page Findings

| Issue | Portfolio | Internship |
|-------|-----------|------------|
| Duplicate H1 | ❌ Yes | ❌ Yes |
| Title < 50 chars | ❌ 19 | ❌ 20 |
| Description > 160 chars | ❌ 440 | ❌ 322 |
| Missing Alt Images | ✅ 0 | ✅ 0 |
| Schema Present | ✅ Yes | ✅ Yes |
| Canonical Correct | ✅ Yes | ✅ Yes |
| OG Tags Complete | ✅ Yes | ✅ Yes |
| Console Errors (Tawk.to) | ⚠️ 2 | ⚠️ 2 |
| Load Time | ❌ 7.6 s | ❌ 6.5 s |
| Custom CSS / SX Design System | ❌ None | ✅ Inline SX CSS |

## Files Generated
- `screenshots/audit-cluster4/audit-cluster4-portfolio-desktop.png`
- `screenshots/audit-cluster4/audit-cluster4-portfolio-mobile.png`
- `screenshots/audit-cluster4/audit-cluster4-internship-desktop.png`
- `screenshots/audit-cluster4/audit-cluster4-internship-mobile.png`
- `screenshots/audit-cluster4/audit-results.json`
- `audit/audit-cluster4-portfolio-internship-2026-05-18.md` (this report)
