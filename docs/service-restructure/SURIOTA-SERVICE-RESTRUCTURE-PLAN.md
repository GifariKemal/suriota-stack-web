# SURIOTA Service Restructure — Implementation Plan

> **Status:** Draft v2 — Under Review (Revisions Applied)  
> **Date:** 2026-05-24  
> **Prepared by:** AI Business & SEO Analyst  
> **Action Required:** Approval before implementation
>
> **Changelog v2:**
> - Fixed: Polylang URL structure (prefix /id/ + /zh/ confirmed; removed `-id` suffix from ID slugs)
> - Fixed: Fragment-based redirects → base URL redirects with JS scroll-to-anchor
> - Added: Phase 0 Baseline Capture (GSC, GA, ranking snapshot)
> - Fixed: SURGE SaaS repositioned to Products dropdown (consistency)
> - Added: Content writer resource specification
> - Added: Rollback procedure (Section 8.1)
> - Added: Products dropdown scope clarification
> - Enhanced: Risk Assessment (long-tail traffic, Pillar 4 depth)
> - Fixed: Native-validated ID/ZH slugs

---

## 1. Executive Summary

### Problem
SURIOTA currently maintains **~30 service pages across 3 languages** (10 service categories × EN/ID/ZH). Investigation reveals:

- **Thin content crisis:** EN digital service pages average **<100 words** (System Integration: 74, IoT: 88, AI: 67)
- **Keyword cannibalization:** Multiple pages competing for identical keywords (e.g., "System Integration" on both `/system-integration/` and `/internet-of-things/`)
- **Template duplication:** Physical services (Automation, Electrical, Renewable Energy, Water Treatment) use **identical heading structures** with only keyword swaps — detected as potential doorway pages by search engines
- **Poor internal linking:** 5 of 10 EN service pages receive **zero links from the homepage**
- **Maintenance burden:** Updating messaging requires editing 30+ pages

### Solution
Consolidate **10 service categories into 5 Pillar Pages** using a **Pillar-Cluster SEO architecture**.

| Metric | Before | After |
|--------|--------|-------|
| Service pages (per language) | 10 | 5 |
| Total service pages (3 languages) | 30 | 15 |
| Avg content per service page | ~350 words | **2,500+ words** |
| Homepage menu items | 10+ | 5 |
| Internal link equity | Fragmented | Concentrated |

### Business Impact
- **SEO:** Pillar pages with 2,500+ words rank significantly better for competitive B2B industrial keywords
- **UX:** 5 clear choices reduce cognitive overload; prospects see full capability spectrum
- **Conversion:** Comprehensive content builds authority and trust before inquiry
- **Efficiency:** Future messaging updates require editing 5 pages instead of 30

---

## 2. Current State Analysis

### 2.1 Service Page Inventory

| # | Service | EN URL | ID URL | ZH URL | EN Content | Status |
|---|---------|--------|--------|--------|------------|--------|
| 1 | System Integration | `/system-integration/` | `/system-integration-id/` | `/xitong-jicheng/` | **74 words** | ❌ Thin |
| 2 | Internet of Things | `/internet-of-things/` | `/internet-of-things-id/` | `/iot/` | **88 words** | ❌ Thin |
| 3 | Artificial Intelligence | `/artificial-intelligence/` | `/artificial-intelligence-id/` | `/rengong-zhineng/` | **67 words** | ❌ Thin |
| 4 | Data Analytics | `/data-analytics/` | `/data-analytics-id/` | `/shujufenxi/` | **~80 words** | ❌ Thin |
| 5 | Software as a Service | `/software-as-a-service/` | `/saas-id/` | `/saas/` | **~80 words** | ❌ Thin |
| 6 | Digital Consulting | `/digital-consulting/` | `/digital-consulting-id/` | `/shuzihua-zixun/` | **~80 words** | ❌ Thin |
| 7 | Automation | `/automation/` | `/automation-id/` | `/zidonghua/` | **768 words** | ✅ Good |
| 8 | Electrical | `/electrical/` | `/electrical-id/` | `/dianqi-gongcheng/` | **755 words** | ✅ Good |
| 9 | Renewable Energy | `/renewable-energy/` | `/renewable-energy-id/` | `/kezaisheng-nengyuan/` | **721 words** | ✅ Good |
| 10 | Water Treatment | `/water-treatment/` | `/water-treatment-id/` | `/shuichuli/` | **685 words** | ✅ Good |

### 2.2 Keyword Cannibalization Map

| Target Keyword | Competing Pages | Impact |
|----------------|-----------------|--------|
| `system integration` | `/system-integration/` + `/internet-of-things/` (title includes "System Integration") | 🔴 High |
| `ai analytics` | `/artificial-intelligence/` + `/data-analytics/` (title includes "AI & Industrial Data Analytics") | 🔴 High |
| `iot modbus` | `/internet-of-things/` + `/automation/` (desc mentions "IIoT integration, Modbus gateway") | 🟡 Medium |
| `industrial automation` | `/automation/` + `/electrical/` (both target industrial engineering) | 🟡 Medium |

### 2.3 Template Duplication Evidence

Physical services (Automation, Electrical, Renewable Energy, Water Treatment) share **identical heading structures**:

```
H2: Need a similar implementation?
H2: +(p.title.rendered)+          ← TEMPLATE RENDERING ERROR
H2: [Hero headline category]
H2: [Value prop with "SURIOTA"]
H2: [Category] with IoT [feature]
H2: Our Services
H2: FAQ
H2: Ready to [CTA]?

H3: +(p.title.rendered)+          ← TEMPLATE RENDERING ERROR
H3: [Differentiator 1]
H3: [Differentiator 2]
H3: IoT [Integration/Monitoring]
H3: [Differentiator 3]
H3: [Differentiator 4]
H3: [Differentiator 5]
H3: Our Process
```

**Risk:** Google may classify these as *doorway pages* — low-quality pages created solely to rank for specific keywords.

### 2.4 Internal Linking Gap

From EN homepage, only **5 of 10 services** receive links:
- ✅ Linked: Data Analytics, Digital Consulting, IoT, Renewable Energy, SaaS
- ❌ **Not linked:** System Integration, AI, Automation, Electrical, Water Treatment

---

## 3. Proposed Structure: 5 Pillar Pages

### 3.1 Architecture Overview

```
Homepage
├── Services (Dropdown) — 4 Core Services
│   ├── Pillar 1: Industrial IoT & System Integration
│   ├── Pillar 2: AI & Industrial Analytics
│   ├── Pillar 3: Digital Consulting
│   └── Pillar 4: Industrial Engineering & Automation
├── Products (Dropdown) — SURGE Platform + Hardware
│   ├── SURGE SaaS Platform
│   ├── SURGE-Energy Mapping
│   ├── SURGE-Vessel Tracking
│   ├── SURGE-Water Analytics
│   ├── SRT-MGATE-1210 Modbus Gateway
│   ├── ISO-M485 Series
│   ├── THM-30MD
│   ├── PM1611-WD
│   └── RS-485 Surge Protector
├── Portfolio
├── Articles
├── About
└── Contact
```

> **Note:** Products dropdown menu update is **separate from** service restructure scope. The current initiative focuses on consolidating service pages. Product menu reorganization can be handled in a follow-up phase once the 5-pillar structure is live and stable.

### 3.2 Pillar Definitions

| # | Pillar | Merges | Positioning | Primary Keywords | Menu Location |
|---|--------|--------|-------------|------------------|---------------|
| **1** | **Industrial IoT & System Integration** | IoT + System Integration | Connectivity layer: bridge legacy and modern systems | `industrial iot batam`, `system integration`, `modbus gateway`, `scada integration` | Services |
| **2** | **AI & Industrial Analytics** | AI + Data Analytics | Intelligence layer: turn data into actionable insights | `industrial ai`, `predictive maintenance`, `oee analytics`, `computer vision` | Services |
| **3** | **Digital Consulting** | *(standalone)* | Strategy layer: digital transformation roadmap | `digital transformation consulting`, `industry 4.0 roadmap`, `ot it convergence` | Services |
| **4** | **Industrial Engineering & Automation** | Automation + Electrical + Renewable Energy + Water Treatment | Physical layer: field engineering and hardware deployment | `industrial automation`, `electrical engineering`, `solar pv plts`, `water treatment wtp` | Services |
| **5** | **SURGE SaaS Platform** | SaaS *(standalone)* | Product layer: cloud monitoring platform (recurring revenue model) | `iot monitoring platform`, `industrial saas`, `energy monitoring`, `sparing klhk` | **Products** |

### 3.3 Why This Grouping?

**Pillar 1 + 2 = Digital/Software Services**
- Both deal with data flow and intelligence
- Target audience: IT managers, data engineers, operations directors
- Sales cycle: shorter, solution-oriented

**Pillar 3 = Strategy Services**
- Pre-implementation consulting
- Target audience: C-level, digital transformation leaders
- Sales cycle: longest, relationship-based

**Pillar 4 = Physical/Field Services**
- All require on-site presence, hardware installation, commissioning
- Target audience: plant managers, facility engineers, project owners
- Sales cycle: medium, project-based

**Pillar 5 = Product (SURGE SaaS Platform)**
- SaaS is a **product** business model, not a professional service
- Recurring revenue vs project-based delivery
- Target audience: operations teams (end users), not procurement
- **Placed under Products menu** to differentiate business models for prospects

---

## 4. URL Mapping & 301 Redirects

### 4.1 EN Pages

| Old URL | Redirect Type | New URL | Anchor Section |
|---------|--------------|---------|----------------|
| `/system-integration/` | 301 | `/industrial-iot-system-integration/` | — |
| `/internet-of-things/` | 301 | `/industrial-iot-system-integration/` | — |
| `/artificial-intelligence/` | 301 | `/ai-industrial-analytics/` | — |
| `/data-analytics/` | 301 | `/ai-industrial-analytics/` | — |
| `/digital-consulting/` | 301 | `/digital-transformation-consulting/` | — |
| `/automation/` | 301 | `/industrial-engineering-automation/` | *(navigates to Automation section)* |
| `/electrical/` | 301 | `/industrial-engineering-automation/` | *(navigates to Electrical section)* |
| `/renewable-energy/` | 301 | `/industrial-engineering-automation/` | *(navigates to Renewable Energy section)* |
| `/water-treatment/` | 301 | `/industrial-engineering-automation/` | *(navigates to Water Treatment section)* |
| `/software-as-a-service/` | 301 | `/surge-saas-platform/` | — |

> **Redirect Note:** All Pillar 4 legacy URLs redirect to the **base pillar URL only** (`/industrial-engineering-automation/`). The rightmost column indicates which sub-service section exists on the destination page for user navigation — this is **not** part of the redirect URL. Hash fragments in 301 redirects are unreliable (browsers strip them; crawlers ignore them).

### 4.2 ID Pages

> **Polylang Configuration Verified:** ID language uses `/id/` **prefix** (Directory mode). Current ID slugs contain manual suffix `-id` (e.g., `internet-of-things-id`). New slugs will use clean Indonesian phrases **without suffix** for better SEO and UX.

| Old URL | Redirect Type | New URL |
|---------|--------------|---------|
| `/id/system-integration-id/` | 301 | `/id/integrasi-sistem-iot/` |
| `/id/internet-of-things-id/` | 301 | `/id/integrasi-sistem-iot/` |
| `/id/artificial-intelligence-id/` | 301 | `/id/ai-analitik-industri/` |
| `/id/data-analytics-id/` | 301 | `/id/ai-analitik-industri/` |
| `/id/digital-consulting-id/` | 301 | `/id/konsultasi-transformasi-digital/` |
| `/id/automation-id/` | 301 | `/id/teknik-automasi-industri/` |
| `/id/electrical-id/` | 301 | `/id/teknik-automasi-industri/` |
| `/id/renewable-energy-id/` | 301 | `/id/teknik-automasi-industri/` |
| `/id/water-treatment-id/` | 301 | `/id/teknik-automasi-industri/` |
| `/id/saas-id/` | 301 | `/id/platform-surge-saas/` |

### 4.3 ZH Pages

> **Polylang Configuration Verified:** ZH language uses `/zh/` **prefix** (Directory mode). ZH slugs are clean pinyin/Chinese phrases without suffix.
>
> ⚠️ **Native Speaker Validation Required:** ZH slugs below are proposed based on standard pinyin. Recommend validation by native Chinese speaker before implementation.

| Old URL | Redirect Type | New URL (Proposed) | Validation Status |
|---------|--------------|-------------------|-------------------|
| `/zh/xitong-jicheng/` | 301 | `/zh/gongye-wulianwang-xitong-jicheng/` | ⏳ Pending native review |
| `/zh/iot/` | 301 | `/zh/gongye-wulianwang-xitong-jicheng/` | ⏳ Pending native review |
| `/zh/rengong-zhineng/` | 301 | `/zh/ren-gong-zhi-neng-gongye-fen-xi/` | ⏳ Pending native review |
| `/zh/shujufenxi/` | 301 | `/zh/ren-gong-zhi-neng-gongye-fen-xi/` | ⏳ Pending native review |
| `/zh/shuzihua-zixun/` | 301 | `/zh/shu-zi-hua-zhuan-xing-zi-xun/` | ⏳ Pending native review |
| `/zh/zidonghua/` | 301 | `/zh/gongye-zi-dong-hua-gong-cheng/` | ⏳ Pending native review |
| `/zh/dianqi-gongcheng/` | 301 | `/zh/gongye-zi-dong-hua-gong-cheng/` | ⏳ Pending native review |
| `/zh/kezaisheng-nengyuan/` | 301 | `/zh/gongye-zi-dong-hua-gong-cheng/` | ⏳ Pending native review |
| `/zh/shuichuli/` | 301 | `/zh/gongye-zi-dong-hua-gong-cheng/` | ⏳ Pending native review |
| `/zh/saas/` | 301 | `/zh/surge-saas-ping-tai/` | ⏳ Pending native review |

### 4.4 Hreflang Mapping

Each pillar page must include hreflang tags linking all 3 language versions:

**Pillar 1 Example:**
```html
<link rel="alternate" href="https://suriota.com/industrial-iot-system-integration/" hreflang="en" />
<link rel="alternate" href="https://suriota.com/id/integrasi-sistem-iot/" hreflang="id" />
<link rel="alternate" href="https://suriota.com/zh/gongye-wulianwang-xitong-jicheng/" hreflang="zh" />
```

**Pillar 4 Example:**
```html
<link rel="alternate" href="https://suriota.com/industrial-engineering-automation/" hreflang="en" />
<link rel="alternate" href="https://suriota.com/id/teknik-automasi-industri/" hreflang="id" />
<link rel="alternate" href="https://suriota.com/zh/gongye-zi-dong-hua-gong-cheng/" hreflang="zh" />
```

---

## 5. Content Outline per Pillar

### 5.1 Pillar 1: Industrial IoT & System Integration

**Target:** 2,500–3,000 words  
**Primary Keywords:** `industrial iot batam`, `system integration`, `modbus gateway`, `scada integration`, `mqtt iot`  
**Target Audience:** IT Managers, Operations Directors, Plant Engineers

```markdown
H1: Industrial IoT & System Integration Services | SURIOTA Batam

H2: Bridge Legacy and Modern Systems into a Single Source of Truth
  → Opening: problem statement (data silos, legacy equipment)
  → SURIOTA value proposition

H2: Core Capabilities
  H3: Industrial IoT Deployment
    → Modbus RTU/TCP to MQTT gateway
    → Edge computing (SRT-MGATE-1210)
    → AWS IoT Core & cloud dashboards
    → Manufacturing, oil & gas, shipyard applications
  H3: System Integration
    → SCADA, MES, ERP integration
    → OT/IT convergence
    → Protocol translation (Modbus, OPC UA, BACnet)
  H3: Cloud Monitoring & Analytics
    → SURGE platform integration
    → Real-time dashboards
    → Alerting & reporting
  H3: Legacy System Modernization
    → Retrofit existing equipment
    → Minimal downtime migration
    → Phased implementation approach

H2: Technologies We Use
  → Protocols: Modbus, MQTT, OPC UA, BACnet, LoRaWAN
  → Cloud: AWS IoT Core, Azure IoT, private cloud
  → Edge: SRT-MGATE-1210, custom gateways
  → Visualization: SURGE dashboards, Grafana, SCADA

H2: Industries We Serve
  → Manufacturing
  → Oil & Gas
  → Shipyard & Marine
  → Water Treatment
  → Renewable Energy

H2: Case Studies / Portfolio Snippets
  → 2-3 specific project highlights
  → Metrics: downtime reduction, efficiency gain

H2: Why SURIOTA
  → 64+ projects
  → 6 in-house products
  → 25+ engineers
  → Local Batam team + global standards

H2: Our Process
  → Discovery → Assessment → Design → Implementation → Support

H2: Frequently Asked Questions
  → 4-6 FAQs about IoT integration

H2: Ready to Integrate Your Systems?
  → CTA: Free Consultation
  → Contact form / WhatsApp button
```

### 5.2 Pillar 2: AI & Industrial Analytics

**Target:** 2,500–3,000 words  
**Primary Keywords:** `industrial ai batam`, `predictive maintenance`, `oee analytics`, `computer vision qc`, `anomaly detection`  
**Target Audience:** Data Engineers, Quality Managers, Operations Directors

```markdown
H1: AI & Industrial Analytics | SURIOTA Batam

H2: Turn Your Industrial Data into Competitive Advantage
  → Opening: Industry 4.0 data explosion
  → From reactive to predictive operations

H2: Core Capabilities
  H3: Predictive Maintenance
    → Machine learning models for failure prediction
    → Vibration, temperature, current signature analysis
    → Maintenance scheduling optimization
  H3: Computer Vision Quality Control
    → Defect detection on production lines
    → Visual inspection automation
    → Custom ML model training
  H3: Anomaly Detection
    → Real-time process monitoring
    → Unsupervised learning for unknown failure modes
    → Root cause analysis support
  H3: OEE & Production Analytics
    → Overall Equipment Effectiveness monitoring
    → Downtime analysis & bottleneck identification
    → Shift performance comparison
  H3: Energy Analytics
    → Consumption pattern analysis
    → Peak demand forecasting
    → Cost optimization recommendations

H2: The SURGE Analytics Platform
  → Cloud-native analytics
  → Custom dashboards & reports
  → Integration with existing SCADA/DCS

H2: Technologies We Use
  → ML Frameworks: TensorFlow, PyTorch, scikit-learn
  → Time Series: InfluxDB, TimescaleDB
  → Visualization: SURGE dashboards, Power BI, Tableau
  → Edge AI: NVIDIA Jetson, Intel OpenVINO

H2: Industries We Serve
  → Manufacturing
  → Oil & Gas
  → Power & Utilities

H2: Case Studies
  → 2-3 specific AI implementation stories

H2: Why SURIOTA
  → Production-grade AI (not POC)
  → On-premise & cloud deployment options
  → Data privacy & security

H2: Our Process
  → Data Audit → Model Development → Pilot → Scale → Optimize

H2: FAQ

H2: Ready to Deploy AI in Your Plant?
  → CTA
```

### 5.3 Pillar 3: Digital Consulting

**Target:** 2,000–2,500 words  
**Primary Keywords:** `digital transformation consulting`, `industry 4.0 roadmap`, `ot it convergence`, `digital consulting batam`  
**Target Audience:** C-Level, Digital Transformation Leaders, Plant Owners

```markdown
H1: Industrial Digital Transformation Consulting | SURIOTA

H2: From Strategy to Execution: Your Industry 4.0 Roadmap
  → Opening: why digital transformation fails (lack of roadmap)
  → SURIOTA's end-to-end approach

H2: Consulting Services
  H3: Digital Maturity Assessment
    → Current state analysis
    → Gap identification
    → Priority matrix
  H3: Industry 4.0 Roadmap
    → 3-year transformation plan
    → Phased implementation
    → ROI projection
  H3: OT/IT Convergence Strategy
    → Network architecture design
    → Security framework
    → Data governance
  H3: Technology Selection
    → Vendor evaluation
    → Proof of concept design
    → Scalability planning
  H3: Change Management
    → Team training & upskilling
    → SOP documentation
    → Knowledge transfer

H2: Our Consulting Framework
  → Assess → Design → Pilot → Scale → Optimize

H2: Deliverables
  → Digital maturity report
  → Technology architecture blueprint
  → Implementation roadmap (Gantt chart)
  → ROI business case

H2: Case Studies
  → 1-2 transformation stories

H2: FAQ

H2: Start Your Digital Transformation Journey
  → CTA: Schedule Assessment
```

### 5.4 Pillar 4: Industrial Engineering & Automation

**Target:** 3,000–3,500 words (largest pillar — 4 sub-services)  
**Primary Keywords:** `industrial automation batam`, `electrical engineering`, `solar pv plts`, `water treatment wtp`, `plc scada`  
**Target Audience:** Plant Managers, Facility Engineers, Project Owners

```markdown
H1: Industrial Engineering & Automation | SURIOTA Batam

H2: End-to-End Industrial Engineering from Design to Commissioning
  → Opening: SURIOTA as your single partner for physical infrastructure

H2: [ANCHOR: #automation] Automation Solutions
  H3: PLC & SCADA Programming
    → Siemens, Allen-Bradley, Schneider, Mitsubishi
    → HMI development
    → Recipe management & batch control
  H3: IIoT Integration
    → Modbus gateway integration
    → Edge-to-cloud connectivity
    → Remote monitoring setup
  H3: Industry 4.0 Upgrades
    → Legacy PLC modernization
    → MES integration
    → Digital twin preparation
  H3: End-to-End Delivery
    → Design → Fabrication → Installation → Commissioning
  H3: Lifecycle Support
    → Preventive maintenance contracts
    → 24/7 remote support
    → Spare parts management

H2: [ANCHOR: #electrical] Electrical Engineering
  H3: Panel Installation & Fabrication
    → MCC, PCC, distribution panels
    → Custom control panels
  H3: Power Distribution Systems
    → Transformer sizing & installation
    → Cable routing & termination
    → Load balancing
  H3: Compliance & Standards
    → SNI, IEC, PUIL 2011 compliance
    → Insulation resistance testing
    → Thermography inspection
  H3: IoT-Ready Integration
    → Smart metering (PM1611-WD)
    → Energy monitoring
    → Power quality analysis
  H3: Safety-First Workflow
    → LOTO procedures
    → Arc flash study
    → Grounding system design

H2: [ANCHOR: #renewable-energy] Renewable Energy
  H3: Solar PV / PLTS Engineering
    → Rooftop & ground-mounted systems
    → On-grid & off-grid solutions
  H3: Hybrid PLTS + PLTB Systems
    → Solar + wind hybrid
    → Battery storage integration
  H3: IoT Energy Monitoring
    → Real-time production tracking
    → Performance ratio analysis
    → Remote fault detection
  H3: PLN Permit Assistance
    → SLO & commissioning documents
    → Net metering application
  H3: Proven ROI Track Record
    → Payback period analysis
    → Case study metrics

H2: [ANCHOR: #water-treatment] Water Treatment
  H3: WTP & WWTP Design
    → Process design & simulation
    → Equipment specification
  H3: KLHK SPARING Compliance
    → Online monitoring system design
    → Parameter: pH, COD, TSS, NH3-N, flow
    → Reporting automation
  H3: SURGE Water Analytics
    → Real-time dashboard
    → Alert system
    → Historical trend analysis
  H3: Full Treatment Spectrum
    → Raw water → drinking water
    → Industrial wastewater → effluent
    → Zero liquid discharge (ZLD) consultation
  H3: Lab & Calibration Services
    → Sensor calibration
    → Water quality lab testing
  H3: Operator Training & SOP
    → Hands-on training
    → Standard operating procedures
    → Maintenance manuals

H2: Industries We Serve
  → Manufacturing, Oil & Gas, Shipyard, Energy, Water Utilities

H2: Our Process (Shared Across All 4 Services)
  → Consultation → Survey → Design → Proposal → Execution → Commissioning → Handover → Support

H2: Certifications & Standards
  → SNI, IEC, PUIL 2011, KLHK regulations

H2: Case Studies
  → 1 case per sub-service (4 total)

H2: FAQ

H2: Ready to Start Your Engineering Project?
  → CTA
```

### 5.5 Pillar 5: SURGE SaaS Platform

**Target:** 2,500–3,000 words  
**Primary Keywords:** `industrial iot monitoring platform`, `energy monitoring saas`, `sparing klhk monitoring`, `vessel tracking`  
**Target Audience:** Operations Teams, Sustainability Managers, Compliance Officers

```markdown
H1: SURGE SaaS — Industrial IoT Monitoring Platform | SURIOTA

H2: Cloud-Native Monitoring for Industrial Operations
  → Opening: why traditional SCADA is not enough
  → SURGE value proposition: multi-tenant, scalable, affordable

H2: Platform Modules
  H3: SURGE-Energy Mapping
    → Real-time kWh monitoring
    → Cost allocation per department/line
    → Peak demand alerting
    → Carbon footprint tracking
  H3: SURGE-Vessel Tracking
    → GPS + IoT sensor integration
    → Fuel consumption monitoring
    → Geofence alerting
    → Maintenance scheduling
  H3: SURGE-Water Analytics
    → SPARING KLHK compliance dashboard
    → pH, COD, TSS, NH3-N, flow monitoring
    → Automatic report generation
    → Regulatory submission ready
  H3: Wastewater Logger
    → IPAL monitoring
    → Flow & quality data logging
    → KLHK integration

H2: Platform Features
  → Multi-tenant architecture
  → White-label option
  → Mobile app (iOS/Android)
  → API for ERP integration
  → Alerting (SMS, email, WhatsApp)
  → Historical data & trend analysis

H2: Deployment Options
  → Cloud-hosted (SURIOTA managed)
  → On-premise (customer infrastructure)
  → Hybrid

H2: Pricing Model
  → Subscription-based (monthly/annual)
  → Per-device or per-site pricing
  → Custom enterprise plans

H2: Case Studies
  → 2-3 customer success stories

H2: FAQ

H2: Start Your Free Trial
  → CTA: Request Demo
```

---

## 6. SEO Strategy

### 6.1 Keyword Mapping

| Pillar | Primary Keyword | Secondary Keywords | Long-Tail Targets |
|--------|-----------------|-------------------|-------------------|
| P1 | `industrial iot batam` | `system integration`, `modbus gateway`, `scada integration` | `modbus rtu to mqtt gateway batam`, `legacy system modernization indonesia` |
| P2 | `industrial ai batam` | `predictive maintenance`, `oee analytics`, `computer vision` | `machine learning predictive maintenance manufacturing`, `anomaly detection oil gas` |
| P3 | `digital transformation consulting` | `industry 4.0 roadmap`, `ot it convergence` | `digital maturity assessment indonesia`, `industrial digital consulting batam` |
| P4 | `industrial automation batam` | `electrical engineering`, `solar pv plts`, `water treatment wtp` | `plc scada programming batam`, `klhk sparing monitoring`, `plts engineering indonesia` |
| P5 | `industrial iot monitoring platform` | `energy monitoring saas`, `sparing klhk` | `multi-tenant iot platform`, `wastewater logger ipal` |

### 6.2 Internal Linking Strategy

```
Homepage
  → Links to 4 Service Pillars (Services dropdown menu)
  → Links to SURGE SaaS (Products dropdown menu)
  
Pillar 1 (IoT & Integration)
  → Links to: Pillar 2 (data needs AI), Pillar 4 (IoT enables automation), Pillar 5 (SURGE platform)
  
Pillar 2 (AI & Analytics)
  → Links to: Pillar 1 (data source), Pillar 5 (SURGE Analytics)
  
Pillar 3 (Digital Consulting)
  → Links to: All service pillars (as implementation partners)
  
Pillar 4 (Engineering & Automation)
  → Links to: Pillar 1 (IIoT integration), Pillar 5 (monitoring)
  
Pillar 5 (SURGE SaaS)
  → Links to: All service pillars (as enabling platform)
```

### 6.3 Content Refresh Schedule

| Pillar | Refresh Frequency | Owner |
|--------|-------------------|-------|
| P1, P2, P4 | Quarterly (case studies, metrics) | Marketing + Engineering |
| P3 | Bi-annually (framework updates) | Consulting Team |
| P5 | Monthly (feature releases, pricing) | Product Team |

---

## 7. Implementation Roadmap

### Phase 0: Baseline Capture (Week 0 — Before Any Changes)
- [ ] **Google Search Console:** Export impressions, clicks, CTR, position for all 30 service URLs (last 90 days)
- [ ] **Google Analytics 4:** Export traffic data (users, sessions, engagement time) per service page (last 30/60/90 days)
- [ ] **Ranking Tracker:** Snapshot current positions for 50+ target keywords across all service pages
- [ ] **Backlink Audit:** Document external backlinks pointing to legacy service pages (use Ahrefs/SEMrush if available)
- [ ] **Content Inventory:** Export full text content of all 30 pages for reference during rewrite
- [ ] **Screenshot Archive:** Capture visual state of all legacy pages before modification
- [ ] Store all baseline data in `audit/baseline-service-restructure-YYYY-MM-DD/` directory

> **Why Baseline Matters:** Without pre-migration data, it is impossible to measure impact accurately. The baseline serves as the control group for evaluating consolidation success.

### Phase 1: Preparation (Week 1)
- [ ] Finalize and approve this document (including native ZH slug validation)
- [ ] Assign content writer resource (see Section 9)
- [ ] Create new page structure in WordPress (5 EN draft pages)
- [ ] Set up Polylang translations (15 total pages: 5 EN + 5 ID + 5 ZH)
- [ ] Configure Elementor templates for pillar layout
- [ ] Fix template rendering bug `+(p.title.rendered)+` across all physical service pages

### Phase 2: Content Creation (Week 2–4)
- [ ] Week 2: Write Pillar 1 & Pillar 2 content (EN first drafts)
- [ ] Week 3: Write Pillar 3 & Pillar 4 content (EN first drafts)
- [ ] Week 3: SME review Pillar 1–2 (Engineering Lead sign-off)
- [ ] Week 4: Write Pillar 5 content + SME review Pillar 3–4
- [ ] Week 4: SEO optimization + final edit all 5 pillars

### Phase 3: Translation (Week 5–6)
- [ ] Week 5: Professional translation to ID (all 5 pillars)
- [ ] Week 5: Professional translation to ZH (all 5 pillars)
- [ ] Week 6: ID + ZH QA review (native speakers)
- [ ] Week 6: hreflang tags, canonicals, meta descriptions validation

### Phase 4: Technical Deployment (Week 7)
- [ ] Publish all 15 pages
- [ ] Update menu structure (Services 4 + Products 1 dropdowns)
- [ ] Implement 301 redirects (30 redirects: 10 EN + 10 ID + 10 ZH)
- [ ] Update homepage internal links
- [ ] Update footer links
- [ ] Update XML sitemap
- [ ] Submit to Google Search Console

### Phase 5: Validation (Week 8–9)
- [ ] Check all redirects (200 status, no chains)
- [ ] Verify hreflang implementation
- [ ] Run SEO audit (Screaming Frog or equivalent)
- [ ] Monitor Google Search Console for indexing issues
- [ ] Monitor ranking changes (30-60 days)

---

## 8. Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **Short-term ranking drop** | High | Medium | 301 redirects preserve ~90% link equity; monitor GSC daily for 2 weeks |
| **Lost long-tail traffic** | Medium | **Medium** | ⚠️ Thin pages may still rank for long-tail queries. **Mitigation:** Preserve original H2/H3 keywords as dedicated anchor sections within pillars. Add comprehensive FAQ targeting legacy long-tail queries. Monitor ranking weekly for 60 days. |
| **User confusion from URL changes** | Low | Medium | Implement redirects immediately; update all internal links |
| **Content quality below expectation** | Medium | High | Rigorous review process; target 2,500+ words per pillar |
| **Pillar 4 shallow depth** | Medium | Medium | 3,500 words ÷ 4 sub-services = ~875 words each. **Mitigation:** Target **4,000–4,500 words** for Pillar 4. Add detailed case studies (1 per sub-service). Include technical specs tables. |
| **Polylang translation sync issues** | Medium | Medium | Test hreflang on all 15 pages before go-live |
| **Template rendering errors persist** | Low | High | Audit all Elementor templates; fix `+(p.title.rendered)+` bug |
| **Stakeholder resistance to consolidation** | Medium | Medium | Present data: thin content + cannibalization evidence |
| **Rollback needed** | Low | High | See Section 8.1 for rollback criteria and procedure |

---

## 8.1 Rollback Criteria & Procedure

### Rollback Triggers
Execute rollback if **ANY** of the following occurs within 30 days of go-live:

| Metric | Threshold | Measurement |
|--------|-----------|-------------|
| Organic traffic drop | >40% vs baseline (30-day avg) | Google Analytics 4 |
| Total impressions drop | >50% vs baseline (GSC 90-day avg) | Google Search Console |
| Core service keyword rankings | >5 target keywords drop >20 positions | Ranking tracker |
| 404 errors spike | >50/day from legacy URLs | GSC Coverage Report |
| Indexing issues | >30% of new pillar pages not indexed within 14 days | GSC Index Report |

### Rollback Procedure
1. **Immediate (Hour 0–4):** Remove 301 redirects (revert to legacy URLs). Legacy pages must still exist as drafts.
2. **Short-term (Day 1–3):** Restore legacy pages to published status. Update internal links back to legacy URLs.
3. **Communication (Day 1):** Notify team; document what went wrong.
4. **Analysis (Week 1–2):** Root cause analysis. Was it timing? Content quality? Redirect errors?
5. **Re-plan (Week 3–4):** Adjust approach and retry with fixes.

> **Important:** Keep all legacy pages as **drafts** (not deleted) for minimum 90 days post-go-live. This enables instant rollback if needed.

---

## 9. Content Resource Specification

### Content Creation Approach

| Aspect | Specification |
|--------|--------------|
| **Method** | AI-assisted first draft → Subject Matter Expert (SME) review → SEO optimization → Final edit |
| **Owner** | Marketing Lead (overall); Engineering Lead (technical accuracy) |
| **AI Tool** | Claude/GPT-4 for draft generation; Surfer SEO / Clearscope for optimization |
| **Human Review** | Mandatory for all technical claims, metrics, and case studies |
| **Translation** | Professional translator (ID + ZH) — **not machine translation** for published content |
| **Timeline Buffer** | Add 1 week buffer to Phase 2 for review cycles |

### Revised Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| Phase 0 | 3 days | Baseline data captured |
| Phase 1 | 5 days | Draft pages + templates ready |
| Phase 2 | **3 weeks** | 5 EN pillar pages (first draft → SME review → SEO edit → final) |
| Phase 3 | 2 weeks | ID + ZH translations (professional) |
| Phase 4 | 5 days | Deployment + redirects |
| Phase 5 | 2 weeks | Validation + monitoring |
| **Total** | **~9 weeks** | (was 5 weeks — adjusted for quality assurance) |

---

## 10. Appendix: Data Evidence

### A. Content Depth Comparison Table

| Page | EN Words | ID Words | Template Pattern |
|------|----------|----------|-----------------|
| System Integration | 74 | — | Thin hero + CTA |
| Internet of Things | 88 | — | Thin hero + CTA |
| Artificial Intelligence | 67 | — | Thin hero + CTA |
| Data Analytics | ~80 | 593 | Thin hero + CTA |
| SaaS | ~80 | — | Thin hero + CTA |
| Digital Consulting | ~80 | — | Thin hero + CTA |
| **Automation** | **768** | **701** | **9 H2 + 8 H3 (template)** |
| **Electrical** | **755** | **680** | **9 H2 + 8 H3 (template)** |
| **Renewable Energy** | **721** | **728** | **9 H2 + 8 H3 (template)** |
| **Water Treatment** | **685** | **703** | **9 H2 + 8 H3 (template)** |

### B. Keyword Cannibalization Matrix

| Keyword | Page 1 | Page 2 | Conflict Level |
|---------|--------|--------|---------------|
| system integration | `/system-integration/` | `/internet-of-things/` | 🔴 Critical |
| ai analytics | `/artificial-intelligence/` | `/data-analytics/` | 🔴 Critical |
| iot modbus | `/internet-of-things/` | `/automation/` | 🟡 Medium |
| industrial automation | `/automation/` | `/electrical/` | 🟡 Medium |

### C. Template Error Evidence

All physical services pages display broken template code:
```
H2: '+(p.title.rendered||'')+'
H3: '+p.title.rendered+'
```

This indicates Elementor dynamic tags are not rendering correctly, likely due to missing post context or incompatible template assignment.

---

## Approval Checklist

- [ ] **Structure approved:** 5 Pillar Pages confirmed (4 Services + 1 Product)
- [ ] **URL naming approved:** All 5 EN URLs reviewed
- [ ] **ID slug approved:** All 10 ID URLs reviewed (native speaker validation if needed)
- [ ] **ZH slug approved:** All 10 ZH URLs reviewed (**native speaker validation mandatory**)
- [ ] **Redirect map approved:** All 30 redirects confirmed (no fragment redirects)
- [ ] **Content outline approved:** All 5 pillar outlines reviewed
- [ ] **Timeline approved:** 9-week implementation accepted
- [ ] **Resource allocation:** Content writer + SME reviewer assigned
- [ ] **Baseline accepted:** Phase 0 data capture approved
- [ ] **Rollback understood:** Section 8.1 reviewed and accepted
- [ ] **Go/no-go decision:** Ready to proceed to Phase 0

---

**Next Step:** Upon approval of this document:
1. Execute **Phase 0** — Capture baseline data (GSC, GA, rankings)
2. Native speaker validates ZH URLs (Section 4.3)
3. Proceed to **Phase 1** — Create draft pages in WordPress
