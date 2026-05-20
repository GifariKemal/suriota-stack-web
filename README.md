<div align="center">

<!-- Logo placeholder -->
<img src="https://via.placeholder.com/120x120/2563EB/FFFFFF?text=S" width="100" alt="SURIOTA Logo" />

<h1>SURIOTA Website Toolkit</h1>

<p><strong>AI-assisted automation toolkit for managing suriota.com</strong><br/>
WordPress + Elementor | Playwright | Python | MCP Servers</p>

<!-- Badges -->
[![GitHub stars](https://img.shields.io/github/stars/GifariKemal/suriota-website-toolkit?style=social)](https://github.com/GifariKemal/suriota-website-toolkit)
[![License](https://img.shields.io/badge/License-Proprietary-2563EB.svg)](LICENSE)
[![WordPress](https://img.shields.io/badge/WordPress-6.x-21759b?logo=wordpress)](https://wordpress.org)
[![Elementor](https://img.shields.io/badge/Elementor-Pro-92003B?logo=elementor)](https://elementor.com)
[![Playwright](https://img.shields.io/badge/Playwright-1.x-2EAD33?logo=playwright)](https://playwright.dev)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Quick Start](#quick-start)
- [Folder Structure](#folder-structure)
- [Tools Reference](#tools-reference)
- [Audit Reports](#audit-reports)
- [Design System](#design-system)
- [Tech Stack](#tech-stack)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

Repository ini berisi toolkit otomasi, audit report, design system, dan backup data untuk pengelolaan website **suriota.com** milik **PT Surya Inovasi Prioritas (SURIOTA)**. Semua script dan asset diorganisir untuk workflow AI-assisted website management menggunakan Claude Code + MCP Servers.

> **Website:** [suriota.com](https://suriota.com)  
> **Company:** PT Surya Inovasi Prioritas (SURIOTA)  
> **Platform:** WordPress + Elementor Pro  
> **Managed by:** Claude Code + MCP Servers

---

## Architecture

```mermaid
graph TB
    subgraph "Developer Workflow"
        A[Claude Code] -->|MCP Protocol| B[MCP Server]
    end

    subgraph "Automation Layer"
        B --> C[Python Scripts]
        B --> D[Node.js Scripts]
        C --> E[Elementor API]
        D --> F[Playwright/Puppeteer]
    end

    subgraph "WordPress Instance"
        E --> G[(WordPress DB)]
        F --> H[suriota.com]
        H --> I[Elementor Frontend]
    end

    subgraph "Assets & Backup"
        J[backups/] --> K[JSON Exports]
        J --> L[Template Backups]
        M[exports/] --> N[Content Data]
    end

    subgraph "Quality Assurance"
        O[audit/] --> P[Audit Reports]
        Q[tools/js/] --> R[Visual Regression]
    end
```

---

## Workflow

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant CC as Claude Code
    participant MCP as MCP Server
    participant WP as WordPress
    participant DB as SQLite Audit DB

    Dev->>CC: Request page update
    CC->>MCP: Query page structure
    MCP->>WP: GET /wp-json/elementor/
    WP-->>MCP: Return element tree
    MCP-->>CC: Display structure
    CC->>MCP: Batch update elements
    MCP->>WP: POST updates
    WP-->>MCP: Confirm changes
    CC->>DB: Log audit entry
    Dev->>CC: Request screenshot verify
    CC->>WP: Playwright screenshot
    WP-->>CC: Visual confirmation
```

---

## Features

| Feature | Description | Status |
|:--------|:------------|:------:|
| **Batch Backup** | Automated WordPress data backup dengan timestamp | ✅ Stable |
| **Visual Audit** | Screenshot regression testing dengan Playwright | ✅ Stable |
| **Elementor API** | Direct manipulation via MCP Tools for Elementor | ✅ Stable |
| **Design System** | Centralized tokens, typography, spacing, colors | ✅ Stable |
| **Audit Tracking** | SQLite database untuk tracking findings | ✅ Stable |
| **SEO Audit** | AIOSEO meta audit dan validation | ✅ Stable |
| **Multi-language** | Polylang EN/ID/ZH support scripts | ✅ Stable |
| **Font Management** | Sitewide font deployment dan cleanup | ✅ Stable |

---

## Quick Start

### Prerequisites

- Node.js 18+
- Python 3.10+
- Playwright (untuk screenshot automation)

### Install

```bash
# Clone repository
git clone https://github.com/GifariKemal/suriota-website-toolkit.git
cd suriota-website-toolkit

# Install Node dependencies
npm install

# Install Playwright browsers
npx playwright install
```

### Usage

```bash
# Backup semua data WordPress
node tools/js/backup-all.js

# Screenshot audit 9 key pages
node tools/js/screenshot-audit.js

# Insert audit findings ke database
python tools/py/audit_insert.py

# Build final page structure
python tools/py/build_final.py
```

---

## Folder Structure

```
suriota-website-toolkit/
├── README.md                 # Dokumentasi ini
├── LICENSE                   # License file
├── CONTRIBUTING.md           # Contribution guidelines
├── package.json              # Node.js dependencies
├── .gitignore                # Git ignore rules
│
├── docs/                     # Dokumentasi
│   ├── AGENTS.md             # AI agent instructions
│   └── swarm-config.md       # Agent swarm configuration
│
├── tools/                    # Automation scripts
│   ├── py/                   # Python scripts
│   │   ├── audit_insert.py       # Audit DB insertion
│   │   ├── build_final.py        # Page builder
│   │   ├── build_retina.py       # Retina asset builder
│   │   ├── mkjson.py             # JSON payload generator
│   │   └── update_sections.py    # Batch section updater
│   └── js/                   # JavaScript scripts
│       ├── backup-all.js         # WordPress backup
│       ├── screenshot-audit.js   # Visual regression
│       └── take-screenshots.js   # Playwright screenshots
│
├── audit/                    # Website audit reports (11 files)
│   ├── COMPREHENSIVE-WEBSITE-AUDIT-2026-05-18.md
│   ├── VALIDATION-REPORT-2026-05-19.md
│   └── ...
│
├── backups/                  # WordPress backup data
│   ├── elementor_*.json      # Elementor globals/colors/typography
│   ├── pages.json            # Page structures
│   ├── posts.json            # Post data
│   └── templates/            # Elementor template backups
│
├── design-system/            # Design system assets
│   ├── DESIGN-SYSTEM.md      # Design tokens documentation
│   └── sx-design-system.css  # CSS design system
│
├── exports/                  # Exported data
│   └── json/                 # JSON content exports
│
├── data/                     # Database & data
│   └── db/
│       └── website_audit.db  # SQLite audit database
│
├── content/                  # Content exports
├── media/                    # Media assets
└── templates/                # Template exports
```

---

## Tools Reference

### Python Scripts

| Script | Purpose | Input | Output |
|:-------|:--------|:------|:-------|
| `audit_insert.py` | Insert audit findings | Audit data | SQLite DB |
| `build_final.py` | Build page structures | JSON config | Elementor payload |
| `build_retina.py` | Generate retina assets | Images | 2x/3x variants |
| `mkjson.py` | Generate Elementor JSON | Parameters | API payload |
| `mkjson_compact.py` | Compact JSON generator | Parameters | Minified payload |
| `update_sections.py` | Batch update sections | Section IDs | Updated pages |

### JavaScript Scripts

| Script | Purpose | Input | Output |
|:-------|:--------|:------|:-------|
| `backup-all.js` | Full WordPress backup | WP REST API | Timestamped JSON |
| `screenshot-audit.js` | Visual regression test | URLs | PNG screenshots |
| `take-screenshots.js` | Playwright screenshots | Page list | Organized PNGs |
| `audit-cluster*.js` | Clustered page audits | Page groups | Audit reports |

---

## Audit Reports

| Report | Date | Focus | Severity |
|:-------|:-----|:------|:--------:|
| COMPREHENSIVE-WEBSITE-AUDIT | 2026-05-18 | Full site audit | 🔴 High |
| VALIDATION-REPORT | 2026-05-19 | Post-fix validation | 🟡 Medium |
| AIOSEO-AUDIT | 2026-05-18 | SEO meta audit | 🟡 Medium |
| WP-OPTIMIZE-BASELINE | 2026-05-18 | Performance baseline | 🟡 Medium |
| FINAL-AUDIT-CLUSTER1 | 2026-05-18 | Homepage cluster | 🔴 High |
| CLUSTER2-SERVICE-PAGES | 2026-05-18 | Service pages | 🟡 Medium |
| CLUSTER3-AUDIT | 2026-05-18 | Product pages | 🟡 Medium |
| CLUSTER4-PORTFOLIO | 2026-05-18 | Portfolio + Internship | 🟢 Low |
| WEB-HEALTH-CHECK | 2026-05-18 | General health | 🟡 Medium |
| ABOUT-US-AUDIT | 2026-05-14 | About page | 🟢 Low |
| DESIGN-CRITIQUE-PORTFOLIO | 2026-05-18 | Portfolio post | 🟢 Low |

---

## Design System

SX Design System — Industrial Editorial style untuk suriota.com.

| Token | Value |
|:------|:------|
| **Primary Font** | Geist, Geist Mono |
| **Color Primary** | `#2563EB` |
| **Color Secondary** | `#1E40AF` |
| **Spacing Base** | 8px |
| **Border Radius** | 4px |
| **Container Max** | 1280px |

Lihat lengkapnya di [`design-system/DESIGN-SYSTEM.md`](design-system/DESIGN-SYSTEM.md).

---

## Tech Stack

```mermaid
graph LR
    A[WordPress 6.x] --> B[Elementor Pro]
    B --> C[PHP 8.x]
    C --> D[MySQL]
    E[Playwright 1.x] --> F[Node.js 18+]
    G[Python 3.10+] --> H[SQLite]
    I[MCP Server] --> J[Claude Code]
    style A fill:#21759b,color:#fff
    style B fill:#92003B,color:#fff
    style E fill:#2EAD33,color:#fff
    style G fill:#3776AB,color:#fff
    style I fill:#000,color:#fff
```

| Layer | Technologies |
|:------|:-------------|
| **CMS** | WordPress 6.x + Elementor Pro |
| **Automation** | Python 3.10+, Node.js 18+ |
| **Screenshot** | Playwright, Puppeteer |
| **Database** | SQLite (audit), MySQL (WordPress) |
| **AI Integration** | Claude Code, MCP Servers |
| **Version Control** | Git, GitHub |

---

## Contributing

Lihat [`CONTRIBUTING.md`](CONTRIBUTING.md) untuk detail kontribusi.

Quick guidelines:
1. Fork repository
2. Buat branch: `git checkout -b feature/nama-fitur`
3. Commit dengan [Conventional Commits](https://conventionalcommits.org)
4. Push dan buat Pull Request

---

## License

Proprietary — PT Surya Inovasi Prioritas (SURIOTA)

All rights reserved. Unauthorized copying, distribution, or modification is prohibited.

Lihat [`LICENSE`](LICENSE) untuk detail lengkap.

---

<div align="center">

**[suriota.com](https://suriota.com)** · Made with precision by SURIOTA Engineering

</div>
