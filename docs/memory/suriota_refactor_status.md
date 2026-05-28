---
name: Suriota Website Refactor Status
description: Current refactor state of suriota.com pages — what's done and pending per page (May 2026)
type: project
originSessionId: 587198fb-6cea-4b87-a692-d8a6e5ea6255
---
Major refactor of suriota.com in progress since 2026-05-13. All pages migrating to "sx- Industrial Editorial v1" design system with English content.

## Page Status (as of 2026-05-17)

| Page | post_id | sx- CSS | Content EN | Status |
|---|---|---|---|---|
| About Us | **29** | ✅ v2 | ✅ Full EN | ✅ DONE — Stats Bar + 5 Services REMOVED (moved to Homepage to avoid duplication). Sections: Hero + Visi/Misi + Siapa SURIOTA + CIPTA + CTA |
| Homepage | **12** | ✅ v2 | ✅ Full EN | ✅ DONE — Stats Bar added (64+/6/5/25+), 5 SX service cards in hero, 3 sub-eyebrows (Products/Trusted By/Portfolio), Trusted By dark callout #0E3942 with rounded corners |
| Portfolio | **839** | ✅ | ✅ Full EN | ✅ DONE — 64 projects translated, IBM Plex Mono numerics, JSON-LD ItemList with 10 featured items |
| Internship | **1127** | ✅ | ✅ Full EN | ✅ DONE — Yogyakarta→Batam fix applied, dual-CTA (Email+WA), 4 numbered position cards |
| Electrical | **37** | ✅ v4.5 | ✅ Full EN | ✅ DONE — Industries + Why Us + new CTA card + tight spacing. Mid heading + old CTA H2/button DELETED |
| Automation | **35** | ✅ v4.5 | ✅ Full EN | ✅ DONE — same v4.5 applied |
| Water Treatment | **945** | ✅ v4.5 | ✅ Full EN | ✅ DONE — same v4.5 applied |
| Renewable Energy | **39** | ✅ v4.5 | ✅ Full EN | ✅ DONE — same v4.5 applied |

## Product Pages — v1 Enrichment Applied (2026-05-17)

All 9 product pages got 4 new HTML widgets + custom CSS:

| Page | post_id | Accent | Apps chips | Why Us | CTA | JSON-LD |
|---|---|---|---|---|---|---|
| SRT-MGATE-1210 | 934 | Teal | 0b364e4 | 60b9f62 | 80a6472 | 6245235 |
| SURGE-Energy | 1542 | Amber | 8c45206 | 101a1de | dd093e4 | d93946b |
| SURGE-Vessel | 1546 | Teal | d46546d | b2c6522 | 81404b2 | 6751602 |
| SURGE-Water | 1547 | Teal | 5d87220 | 24b77ee | 4ec0b15 | be4b73d |
| ISO-M485 | 1740 | Amber | 3a97014 | 2932b30 | dabc330 | 03c3845 |
| THM-30MD | 1741 | Teal | 50616fd | 348a240 | 77d97f6 | f01325e |
| PM1611-WD | 1742 | Amber | 494b0c4 | 4e7bbb3 | c2a29b1 | 2bab597 |
| SPD-T485-105 | 1765 | Amber | 52047da | a6020e9 | 0583b05 | 9cecc5b |
| Wastewater Logger | 929 | Green | 4761556 | 2d96125 | 9c447a7 | b09f152 |

### Structure (per product page)
0: Applications chips (NEW)
1-3: Existing H3 + image + intro text-editor
4: Key Features 4-card grid (NEW)
5-6: Existing Tokopedia/Datasheet buttons
7: CTA card sx-cta-final (NEW)
8: JSON-LD Product + BreadcrumbList (NEW)

### Schema Types
- **Hardware** (Modbus, ISO-M485, THM-30MD, PM1611-WD, SPD-T485-105, Wastewater Logger): `Product` schema
- **SaaS** (SURGE-Energy, SURGE-Vessel, SURGE-Water): `SoftwareApplication` schema

### Pending Phase 2 (not done yet)
- Technical specifications table (semantic markup)
- FAQ accordion per product (with faq_schema:yes)
- How It Works diagrams
- Related Portfolio cross-link (where deployed)
- Compatible With / pairs-with cross-product links

## Pages NOT Yet Refactored
Per AGENTS.md page reference:
- Desain Grafis (33)
- Teknologi Informasi (41)
- Tentang (376) — possibly older Indonesian version
- Modbus Gateway (934)
- Waste Water Loger (929)
- SURGE-Energy Mapping (1542)
- SURGE-Vessel Tracking (1546)
- SURGE-Water Analytic (1547)
- ISO-M485 SERIES (1740)
- THM-30MD (1741)
- PM1611-WD (1742)
- RS-485 Surge Protector (1765)

## Service Pages v4 Enrichment (2026-05-17)

All 4 service pages got these new widgets via Elementor MCP:
- **Industries chips** HTML widget at column position 0 (top of content) — 8 chips with `.sx-chip` styling, per-page accent color
- **Why Us 4-card grid** HTML widget at column position 4 (after mid heading, before Our Services H2) — left-border cards with internal cross-links to SURGE/SRT-MGATE products
- **BreadcrumbList + WebPage JSON-LD** HTML widget at column end — appended to content column
- **Keyword-rich hero subtitle** — replaced generic subtitle with H2 keyword-dense version
- **v4 CSS appended** with `html body` specificity prefix and per-page `--sx-accent` color

### New widget IDs per page
| Page | Industries | Why Us | JSON-LD |
|---|---|---|---|
| Electrical 37 | 4561f38 | 290817d | 36fdeef |
| Automation 35 | 997c12e | 4bee829 | 720c669 |
| WT 945 | 51b42e7 | 0948521 | 82ae13c |
| RE 39 | 19fcca0 | 890145e | 8225123 |

### FAQPage schema
NOT manually injected — accordion widget already has `faq_schema:yes` setting, Elementor auto-generates FAQPage schema from accordion tabs.

## Service Pages v4.5 — CTA Redesign + Cleanup (2026-05-17)

### New CTA Card (sx-cta-final)
Dark teal gradient card (#0E3942 → #205B69) with top accent bar (amber→teal→green), eyebrow "GET STARTED", service-specific H2, subtitle, dual-CTA (white pill Free Consultation + #075E54 WhatsApp), trust line.
- New widget IDs: Electrical 138ea1b · Automation 9a7efa5 · WT 9c526b8 · RE db92458

### Permanently DELETED widgets (12 total)
Old CTA H2 + button per page (Elementor's stacked card hack):
- Electrical: a74c0c1, 6ee0147
- Automation: fd16c61, 08b621f
- WT: 5df88d8, 28786ca
- RE: cbc70bf, de36f6e

Mid heading callouts (duplicated Main H2 message):
- Electrical 3610c37 · Automation 3c0ca08 · WT af4eae9 · RE 4911eff

### v4.4 Compact Spacing
Reduced section H2 gaps from 78-108px → 20-32px (margin+padding combos that were stacked). Content section padding 32+48px → 14+20px. Intro flex container 40px → 16px bottom margin.

### v4.3 Stat-card flex fix
Stat cards (2+/SNI-IEC-PUIL/64+) now `display:flex column` with `min-height:88px` + `gap:10px` to ensure clean number/label stacking.

## Key Decisions
- **Stats Bar lives ONLY on Homepage** (removed from About Us 2026-05-16)
- **5 Services lives ONLY on Homepage** (removed from About Us 2026-05-16)
- **About Us** = brand story (Hero + Vision/Mission + Siapa SURIOTA + CIPTA + CTA)
- **Homepage** = visual entry (Hero + Stats + Products + Trusted By + Portfolio + Maps/Contact)
- **All pages full English** (Indonesian removed completely)
- **64+ projects** (not 55+ which was earlier mistake)
- **Internship location = Batam** (not Yogyakarta — corrected 2026-05-17)
- **CIPTA values** = Committed Outcome, Integrity of Innovation, Precision in Execution, Trust Through Reliability, Adaptive Growth
- **Headings always use `em` line-height, NEVER `px`** (caused overlap bug)
