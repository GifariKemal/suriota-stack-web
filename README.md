# 🌐 Website Suriota — MCP Elementor Project

> **Project:** UI/UX Improvement untuk website [suriota.com](https://suriota.com)  
> **Platform:** WordPress + Elementor  
> **MCP Server:** MCP Tools for Elementor (v1.4.3) via WordPress MCP Adapter (v0.4.1)  
> **Managed by:** Kimi Code CLI via MCP stdio wrapper + Agent Swarm

---

## 📁 Struktur Folder

```
Website Suriota/
├── README.md                 # Dokumentasi ini
├── AGENTS.md                 # Instruction untuk AI agent
├── swarm-config.md           # Agent Swarm decomposition config
├── package.json              # Node dependencies (playwright, etc)
├── backups/                  # Backup data website
│   ├── pages.json            # 20 WordPress pages
│   ├── posts.json            # 64 blog posts
│   ├── media.json            # 100 media items
│   ├── site_info.json        # Site metadata
│   ├── elementor_globals.json
│   ├── elementor_colors.json
│   ├── elementor_typography.json
│   ├── elementor_templates.json  # 9 templates
│   ├── page_homepage.json
│   ├── page_about.json
│   ├── page_portfolio.json
│   └── YYYY-MM-DDTHH-MM-SS/  # Timestamped backups (via script)
├── screenshots/              # Visual audit screenshots
│   └── YYYY-MM-DD/
│       ├── homepage-desktop.png
│       ├── homepage-mobile.png
│       └── ...
├── scripts/                  # Automation scripts
│   ├── backup-all.js         # Batch backup script
│   └── screenshot-audit.js   # Visual audit script
├── audit/                    # Audit reports
├── content/                  # Exported content & structures
├── media/                    # Downloaded media assets
├── templates/                # Elementor template exports
└── skills/                   # Kimi CLI skills untuk Elementor
```

---

## 🔌 Koneksi MCP

### Status: ✅ ACTIVE

| Komponen | Detail |
|----------|--------|
| **Site URL** | `https://suriota.com` |
| **WP Admin** | `https://suriota.com/wp-admin` |
| **Username** | `admin` |
| **App Password** | `hCYK JqF1 khdB WDzI LQdQ WEBr` |
| **MCP Endpoint** | `https://suriota.com/wp-json/mcp/elementor-mcp-server` |
| **Abilities API** | `https://suriota.com/wp-json/wp-abilities/v1` |

### Plugin Terinstall di WordPress
- ✅ **MCP Adapter** v0.4.1
- ✅ **MCP Tools for Elementor** v1.4.3
- ✅ Elementor (Free + Pro)

### Wrapper Location
```
~/.kimi/mcp-wrappers/elementor-mcp-wrapper.js
```

### MCP Config (`~/.kimi/mcp.json`)
```json
{
  "elementor-mcp": {
    "command": "node",
    "args": ["C:\\Users\\Administrator\\.kimi\\mcp-wrappers\\elementor-mcp-wrapper.js"]
  }
}
```

---

## 🛠️ Semua Tools & Skills yang Tersedia

### MCP Servers (Aktif)
| Server | Fungsi untuk Project Ini |
|--------|-------------------------|
| `elementor-mcp` | Edit Elementor langsung (100 tools) |
| `puppeteer` | Screenshot & visual regression testing |
| `fetch` | Crawl competitor & research UI trends |
| `sqlite` | Track audit issues & improvement tasks |
| `sequential-thinking` | Deep analysis & planning |
| `filesystem` | Manage project files |

### Kimi Skills (Tersedia)
| Skill | Gunakan Saat... |
|-------|-----------------|
| `agent-swarm` | Parallel audit multiple pages |
| `batch-tasks` | Batch screenshot / batch backup |
| `deep-research` | Research UI/UX trends & competitor |
| `data-analysis` | Analisis Lighthouse metrics |
| `slides-creator` | Buat presentation hasil audit |

---

## 🛠️ Total MCP Tools: 100

### Kategori Tools

| Kategori | Tools | Contoh |
|----------|-------|--------|
| **Query & Discovery** | `list-widgets`, `get-widget-schema`, `get-container-schema`, `get-page-structure`, `get-element-settings`, `find-element`, `list-pages`, `list-templates`, `get-global-settings` | |
| **Page Management** | `create-page`, `update-page-settings`, `delete-page-content`, `import-template`, `export-page` | |
| **Layout** | `add-container`, `update-container`, `update-element`, `batch-update`, `reorder-elements`, `move-element`, `remove-element`, `duplicate-element` | |
| **Widgets (Free)** | `add-heading`, `add-text-editor`, `add-image`, `add-button`, `add-video`, `add-icon`, `add-spacer`, `add-divider`, `add-icon-box`, `add-accordion`, `add-alert`, `add-counter`, `add-google-maps`, `add-icon-list`, `add-image-box`, `add-image-carousel`, `add-progress`, `add-social-icons`, `add-star-rating`, `add-tabs`, `add-testimonial`, `add-toggle`, `add-html`, `add-menu-anchor`, `add-shortcode`, `add-rating`, `add-text-path` | |
| **Widgets (Pro)** | `add-form`, `add-posts-grid`, `add-countdown`, `add-price-table`, `add-flip-box`, `add-animated-headline`, `add-call-to-action`, `add-slides`, `add-testimonial-carousel`, `add-price-list`, `add-gallery`, `add-share-buttons`, `add-table-of-contents`, `add-blockquote`, `add-lottie`, `add-hotspot`, `add-nav-menu`, `add-loop-grid`, `add-loop-carousel`, `add-media-carousel`, `add-nested-tabs`, `add-nested-accordion`, `add-portfolio`, `add-author-box`, `add-login`, `add-code-highlight`, `add-reviews`, `add-off-canvas` | |

---

## 📄 Daftar Pages (20 Total)

| ID | Page | Slug | Status | Builder |
|----|------|------|--------|---------|
| 12 | **Homepage** | `elementor-12` | publish | Elementor |
| 29 | **About Us** | `about-us` | publish | Elementor |
| 33 | Desain Grafis | `desain-grafis` | publish | Elementor |
| 35 | Automation Services | `automation` | publish | Elementor |
| 37 | Electrical Services | `electrical` | publish | Elementor |
| 39 | Renewable Energy Services | `renewable-energy` | publish | Elementor |
| 41 | Teknologi Informasi | `teknologi-informasi` | publish | Elementor |
| 376 | Tentang | `another` | publish | Elementor |
| 839 | **Portfolio** | `portfolio` | publish | Elementor |
| 934 | Modbus Gateway IIoT | `suriota-modbus-gateway` | publish | Elementor |
| 929 | Waste Water Loger | `waste-water-loger` | publish | Elementor |
| 945 | Water Treatment Services | `water-treatment` | publish | Elementor |
| 1127 | Internship | `internship` | publish | Elementor |
| 1542 | SURGE-Energy Mapping | `surge-energy-mapping` | publish | Elementor |
| 1546 | SURGE-Vessel Tracking | `surge-vessel-tracking` | publish | Elementor |
| 1547 | SURGE-Water Analytic | `surge-water-analytic` | publish | Elementor |
| 1740 | ISO-M485 SERIES | `iso-m485-series` | publish | Elementor |
| 1741 | THM-30MD | `thm-30md` | publish | Elementor |
| 1742 | PM1611-WD | `pm1611-wd` | publish | Elementor |
| 1765 | RS-485 Surge Protector SPD-T485-105 | `rs-485-surge-protector-spd-t485-105` | publish | Elementor |

---

## 🤖 Agent Swarm Workflow

Lihat `swarm-config.md` untuk detail decomposition.

### Phase 1: Parallel Audit
- **Agent A** (Visual Design): Screenshot + color/typography/spacing audit
- **Agent B** (UX & Interaction): Navigation, CTA, forms, accessibility
- **Agent C** (Technical): Lighthouse, responsive, Elementor structure
- **Agent D** (Content & Competitor): Copy, SEO, competitor comparison

### Phase 2: Aggregation
- Merge findings → priority matrix → improvement roadmap

### Phase 3: Parallel Implementation
- **Agent E**: Elementor layout edits
- **Agent F**: Content & SEO updates
- **Agent G**: Performance optimizations

---

## 🚀 Scripts Automation

### Batch Backup
```bash
node scripts/backup-all.js
```
Menghasilkan timestamped backup folder di `backups/YYYY-MM-DDTHH-MM-SS/`

### Visual Audit Screenshot
```bash
node scripts/screenshot-audit.js
```
Screenshot 9 key pages (desktop + mobile) ke `screenshots/YYYY-MM-DD/`

---

## 🎨 Global Design Tokens (Backup)

File: `backups/elementor_globals.json`
- Colors
- Typography
- Spacing
- Breakpoints

---

## 🗄️ Audit Tracking (SQLite)

Database: `~/.kimi/data/allegretto.db`

Tables:
- `website_pages` — Daftar 20 pages suriota.com
- `website_audit` — Findings & improvement tasks

Query contoh:
```sql
SELECT page_name, audit_type, finding, severity, status
FROM website_audit
WHERE status = 'open'
ORDER BY severity DESC;
```

---

## 📋 Workflow UI/UX Improvement (Single Page)

### Step 1: Audit Page
```
Gunakan tool: elementor-mcp-get-page-structure
Parameter: { "post_id": 12 }
```

### Step 2: Analyze & Plan
- Identifikasi elemen yang perlu diupdate
- Cek consistency dengan global design tokens
- Review responsive behavior

### Step 3: Edit Element
```
Gunakan tool: elementor-mcp-update-element
Parameter: { "post_id": 12, "element_id": "...", "settings": { ... } }
```

### Step 4: Batch Update (jika banyak)
```
Gunakan tool: elementor-mcp-batch-update
Parameter: { "post_id": 12, "operations": [ ... ] }
```

### Step 5: Flush CSS Cache
Regenerate CSS via WP Admin → Elementor → Tools → Regenerate CSS

### Step 6: Verify
- Preview page di browser
- Cek mobile responsive

---

## ⚠️ Safety Rules

1. **Always backup sebelum edit** → `node scripts/backup-all.js`
2. **Export page sebelum modify** → `elementor-mcp-export-page`
3. **Test di staging** → Kalau ada staging site, test dulu di sana
4. **Flush CSS** → Setelah edit Elementor, selalu regenerate CSS
5. **Version control** → Backup disimpan di folder `backups/` dengan timestamp
6. **Jangan hapus element tanpa export** → Selalu duplicate/save template dulu

---

## 📚 Resources

- [MCP Tools for Elementor Docs](https://github.com/msrbuilds/elementor-mcp)
- [WordPress REST API Reference](https://developer.wordpress.org/rest-api/reference/)
- [Elementor Developer Docs](https://developers.elementor.com/docs/)
- `swarm-config.md` — Agent Swarm decomposition

---

*Generated by Kimi Code CLI | Last updated: 2026-05-13*
