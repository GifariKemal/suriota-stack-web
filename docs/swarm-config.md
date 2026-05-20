# Agent Swarm Config — Suriota UI/UX Improvement

## Swarm Objective
Audit dan improve UI/UX website suriota.com secara komprehensif menggunakan multi-agent parallelism.

## Task Decomposition

### Phase 1: Parallel Audit (4 Agents)

#### Agent A: Visual Design Auditor (`explore`)
**Scope:** Audit visual design, color theory, typography, spacing, imagery
**Tasks:**
- Screenshot semua 20 pages (desktop + mobile)
- Analisis color consistency dengan global design tokens
- Review typography hierarchy
- Evaluate image quality dan relevance
- Cek whitespace dan padding consistency

#### Agent B: UX & Interaction Auditor (`explore`)
**Scope:** Audit user experience, navigation, CTA, forms, accessibility
**Tasks:**
- Review navigation flow dan information architecture
- Audit CTA visibility dan clickability
- Test form validation dan feedback states
- Cek accessibility (contrast, alt text, ARIA)
- Analisis user journey dari homepage ke conversion

#### Agent C: Technical Performance Auditor (`explore`)
**Scope:** Audit performance, responsive, Elementor structure
**Tasks:**
- Lighthouse audit (performance, accessibility, SEO, best practices)
- Cek responsive breakpoints
- Audit Elementor structure per page (container depth, widget usage)
- Identify unused CSS/JS bloat
- Cek image optimization dan lazy loading

#### Agent D: Content & Competitor Auditor (`explore`)
**Scope:** Audit content quality, competitor comparison, SEO
**Tasks:**
- Review copywriting clarity dan persuasiveness
- Analisis competitor websites (similar engineering consulting firms)
- Audit SEO metadata (title, description, headings)
- Cek content freshness dan accuracy
- Review product descriptions completeness

### Phase 2: Aggregation & Planning (`plan`)
**Aggregator Agent:**
- Merge findings dari Agent A, B, C, D
- Deduplicate dan prioritize issues
- Buat improvement roadmap (quick wins vs long-term)
- Assign severity dan effort estimation

### Phase 3: Implementation (`coder`)
**Implementation Agents:**
- Agent E: Implement layout & visual improvements via Elementor MCP
- Agent F: Implement content updates & SEO fixes
- Agent G: Implement performance optimizations

## Tools Available
- `elementor-mcp` — Direct Elementor editing (100 tools)
- `puppeteer` — Screenshot & visual testing
- `fetch` — Crawl & competitor analysis
- `sqlite` — Track issues & progress
- `filesystem` — Manage project files
- `sequential-thinking` — Deep analysis & planning

## Execution Plan
```
Phase 1 (Parallel):
  Agent A ──→ screenshots + visual audit
  Agent B ──→ UX audit + navigation test
  Agent C ──→ Lighthouse + structure audit
  Agent D ──→ content + competitor audit
      ↓
Phase 2 (Sequential):
  Aggregator ──→ merged report + roadmap
      ↓
Phase 3 (Parallel):
  Agent E ──→ Elementor layout edits
  Agent F ──→ content & SEO updates
  Agent G ──→ performance optimizations
```

## Checkpointing
- Setelah Phase 1: Simpan hasil audit ke `audit/` folder
- Setelah Phase 2: Simpan roadmap ke `roadmap.md`
- Setelah Phase 3: Backup final dan regenerate CSS
