---
name: Suriota AIOSEO Templates per Page
description: SEO Title + Meta Description copy templates for AIOSEO sidebar — manual paste required (Elementor MCP can't update AIOSEO settings)
type: reference
originSessionId: 587198fb-6cea-4b87-a692-d8a6e5ea6255
---
AIOSEO auto-generates meta from page content (which dumps raw stats text — bad). User must manually paste these in WP Admin → edit page → AIOSEO sidebar.

## Per-Page Templates

| Page | SEO Title (≤60c) | Meta Description (~155c) |
|---|---|---|
| **About Us** | `About SURIOTA — Industrial IoT & System Integration \| PT Surya Inovasi Prioritas` | `PT Surya Inovasi Prioritas (SURIOTA) — technology company specializing in Industrial IoT & System Integration in Batam, Indonesia. 64+ projects, 6 in-house products.` |
| **Homepage** | `SURIOTA — Industrial IoT & System Integration \| Engineering Partner Batam` | `SURIOTA — Industrial IoT, System Integration & Engineering Services in Batam, Indonesia. 64+ projects, 6 in-house products, 5 core services. Get free consultation.` |
| **Portfolio** | `Portfolio — 64+ Industrial Projects \| SURIOTA Engineering Batam` | `Explore 64+ SURIOTA industrial projects 2023-2025: PDAM Tirta Kepri, manufacturing, energy, maritime. Modbus Gateway, SCADA, PLTS hybrid across Indonesia.` |
| **Internship** | `Internship Program Batch 3 — Industrial IoT \| SURIOTA Batam` | `SURIOTA Internship Batch 3 — open positions: R&D App Developer, DevOps, QA, UI/UX. Real Industrial IoT projects in Batam. Apply by Aug 2026.` |
| **Electrical** | `Industrial Electrical Engineering Services Batam \| SURIOTA` | `Panel installation, power distribution, commissioning & testing per SNI, IEC, PUIL. SURIOTA serves industrial & commercial in Batam, Indonesia.` |
| **Automation** | `Industrial Automation & IoT Services \| SURIOTA SCADA PLC` | `PLC, SCADA, IIoT integration & SURGE platform for Industry 4.0. SURIOTA delivers automation solutions across Indonesia.` |
| **Water Treatment** | `Water Treatment Plant & IoT Monitoring \| SURIOTA Batam` | `WTP, WWTP, SPARING monitoring for KLHK compliance, real-time water quality via SURGE Water Analytics. SURIOTA serves PDAM Tirta Kepri.` |
| **Renewable Energy** | `Solar PV & Renewable Energy Services \| SURIOTA Indonesia` | `PLTS, PLTS-PLTB hybrid, IoT energy monitoring. Feasibility study, design & installation. SURIOTA serves industries across Indonesia.` |

## Social (Facebook OG) — Homepage Example
- OG Title: `SURIOTA — Next Gen. Industrial Partner | IoT & System Integration`
- OG Description: `Mentransformasi industri Indonesia lewat IoT, AI & SaaS. 64+ proyek selesai, 6 produk in-house (SURGE, Modbus Gateway, RS-485). Hubungi tim engineer SURIOTA di Batam.`
- OG Image: Upload page-specific 1200×630 (NOT generic `Cover-Link-Share.png`)

## JSON-LD Already Implemented (in Elementor widgets)
- About Us: Organization + LocalBusiness + AboutPage + BreadcrumbList + hasOfferCatalog (5 services)
- Homepage: relies on AIOSEO auto-generated WebPage/Organization
- Portfolio: ItemList with 10 featured projects
- Internship: JobPosting (location Batam, +62-858-3567-2476, admin@suriota.com)
- Service pages (4): Service schema per page with serviceType, areaServed, hasOfferCatalog

## Critical Reference Data (used in schemas)
- **Company**: PT Surya Inovasi Prioritas (SURIOTA)
- **Founded**: January 2023
- **Founder/CEO**: Gifari Kemal Suryo
- **Phone**: +62-858-3567-2476
- **Email**: admin@suriota.com
- **Full Address**: Batam Centre, Jl. Legenda Malaka, Baloi Permai, Kec. Batam Kota, Kepulauan Riau 29431
- **WhatsApp Link**: `https://wa.me/6285835672476`
- **Contact Form**: `/contact/` (NOT `/contact-us/`)
- **Slogan**: "Next Gen. Industrial Partner"
- **Services (5)**: IoT & System Integration / AI & Data Analytics / SaaS (SURGE) / Automation & Renewable Energy / Digital Consulting
- **Products (6)**: SURGE platform, SRT-MGATE-1210, RS-485 SPD, ISO-M485, THM-30MD, PM1611-WD
- **Stats**: 64+ projects / 6 in-house products / 5 core services / 25+ team / 20+ clients / 3+ years
