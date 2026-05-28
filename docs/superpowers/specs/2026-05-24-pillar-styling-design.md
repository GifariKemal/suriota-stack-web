# SURIOTA Pillar Pages — Modern Industrial Editorial v2 Design Spec

**Date:** 2026-05-24
**Status:** Approved (user delegated decision-making in-session)
**Scope:** Visual / UX styling of the 5 new pillar pages
**Owner:** Frontend design — handed off to writing-plans
**Companion docs:**
- `docs/service-restructure/SURIOTA-SERVICE-RESTRUCTURE-PLAN.md` (content plan)
- `audit/VALIDATION-REPORT-COMPLETE-2026-05-24.md` (current live state)

---

## 0. Scope Lock (Hard Boundary)

### IN SCOPE — touch ONLY these 15 posts

| Pillar | EN | ID | ZH |
|---|---|---|---|
| P1 Industrial IoT & System Integration | 5554 | 5566 | 5571 |
| P2 AI & Industrial Analytics | 5555 | 5567 | 5572 |
| P3 Digital Transformation Consulting | 5556 | 5568 | 5573 |
| P4 Industrial Engineering & Automation | 5557 | 5569 | 5574 |
| P5 SURGE SaaS Platform | 5558 | 5570 | 5575 |

### OUT OF SCOPE — DO NOT touch

- Other pages: homepage (12), about (29), portfolio (839), internship (1127), contact, service pages (35 Automation, 37 Electrical, 39 Renewable Energy, 945 Water Treatment), product pages (929, 934, 1542, 1546, 1547, 1740, 1741, 1742, 1765), any ZH legacy pages
- Sitewide Elementor snippets: 5153, 5186, 5411, 5447, 5498, 5511, 5515, 5524, 5528, 5599
- Theme files (`functions.php`, theme CSS/JS)
- WP Customizer global CSS
- Global Elementor settings / kit
- Polylang configuration
- AIOSEO meta (already deployed per memory)

### Allowed surface area

- Each pillar page's Elementor **Page Settings → Custom CSS** (per-page, scoped)
- New HTML widgets **inside** each pillar page's Elementor data (`_elementor_data`)
- New saved Elementor templates prefixed `SX-Pillar/...` (not assigned globally)
- Local files under `design-system/` (new file: `sx-pillar-v2.css`)

---

## 1. Visual Direction

**Aesthetic:** Modern Industrial Editorial v2 — evolution of existing `sx-` v1 design system. Refined B2B, contemporary, not flashy.

**Reference points:** Linear (typography + motion), Vercel (clean dark blocks), Siemens Xcelerator (industrial credibility), Bosch Connected Industry (technical density), Stripe Atlas (pull-quote + numbered structure).

**Principles:**
- Editorial typographic hierarchy over decorative imagery
- Per-pillar accent (one color) — never mixed accents on a page
- Generous whitespace AT structural boundaries, **compact spacing INSIDE sections** (user preference from memory)
- Numbered grids (01 / 02 / 03) carried forward from v1
- Mono numerals (IBM Plex Mono tabular-nums) as visual identity
- Subtle motion — never decorative, always functional (reveal, focus, feedback)
- Zero parallax, zero autoplay loops (Reduce Motion compliance)

---

## 2. Architecture

### 2.1 CSS Scoping Strategy

Per-page Elementor Custom CSS using `body.page-id-{POST_ID}` scope. This guarantees zero leakage to other pages.

```css
/* Pillar 1 only */
body.page-id-5554 .sxp-hero { ... }
body.page-id-5566 .sxp-hero { ... }  /* ID variant */
body.page-id-5571 .sxp-hero { ... }  /* ZH variant */
```

### 2.2 Naming Convention

`.sxp-*` namespace (sx-pillar) — distinct from sitewide `.sx-*` and Elementor `.elementor-*`. Documented in `design-system/sx-pillar-v2.css`.

### 2.3 CSS Distribution Model

1. Author one canonical file: `design-system/sx-pillar-v2.css` (~400 lines)
2. Per-pillar variant: top-of-file CSS variables override block sets accent
3. Paste each variant into Elementor Page Settings → Custom CSS for that pillar's 3 language posts (EN/ID/ZH share identical CSS — content differs, structure identical)

### 2.4 HTML Widget Library

Each component below = one Elementor HTML widget, copied as Saved Template under name `SX-Pillar/{component}`. Templates are NOT assigned globally — manually inserted per pillar page.

---

## 3. Component Inventory

### 3.1 Hero (`sxp-hero`)

- Full-bleed, ~88vh desktop / 72vh mobile
- Background variant by pillar:
  - **P1, P2, P4, P5:** Dark gradient (pillar accent → `--sx-teal-deep`) + dot-grid SVG layer @ 6% opacity
  - **P3 Consulting (LIGHT variant):** `--sx-surface` background + mono grid SVG @ 8% opacity, dark text on light. Distinguishes strategy/advisory positioning from technical pillars.
- Eyebrow per pillar (IBM Mono 13px uppercase, accent color):
  - P1 → `01 — INDUSTRIAL IOT / SYSTEM INTEGRATION`
  - P2 → `02 — AI / INDUSTRIAL ANALYTICS`
  - P3 → `03 — DIGITAL TRANSFORMATION CONSULTING`
  - P4 → `04 — INDUSTRIAL ENGINEERING / AUTOMATION`
  - P5 → `05 — SURGE / SAAS PLATFORM`
- H1: Plus Jakarta Sans 700, clamp(2.5rem, 5vw, 4.5rem), letter-spacing -0.02em, line-height 1.05em (em unit per critical rule)
- Subhead: Poppins 400, 18–20px, max 60ch
- Dual CTA:
  - Primary `Free Consultation` (white pill on dark hero / dark pill on light hero, links to `/contact/`)
  - Secondary `View Capabilities` (outline, anchor link to `#sxp-capabilities`)
- Bottom-left accent caption: `P{n} / SERVICES` for P1–P4, `P5 / PRODUCT` for P5 (mono small)

### 3.2 In-Page Sticky Nav (`sxp-nav`) — P4 ONLY

- Sticky at `top: 80px` (offset for site header)
- 4 anchor links: `#automation`, `#electrical`, `#renewable-energy`, `#water-treatment`
- Background: `rgba(250,251,252,0.92)` with `backdrop-filter: blur(8px)`
- Active state: amber underline + dot
- Mobile: horizontal scroll
- Hides on scroll-down, reveals on scroll-up (intersection-based)

### 3.3 Capabilities Grid (`sxp-cap`)

- CSS Grid 12-col asymmetric layout:
  - Card 1 span 7
  - Card 2 span 5
  - Card 3 span 5
  - Card 4 span 7
- Each card: amber mono number (01-04), H3 (PJS 600, 24-28px), body (Poppins 16px), tech chip row
- Hover: lift 4px (transform translateY), accent border-left grows 0 → 3px
- Mobile: stacks to single column, all spans become 12

### 3.4 Tech Strip (`sxp-tech`)

- Hairline top + bottom borders
- Items inline-flex with mono labels separated by amber dot bullet
- Mobile: horizontal scroll with snap

### 3.5 Industries Grid (`sxp-ind`) — P1, P2, P4, P5

- 5-up grid desktop / 2-col mobile
- Each: inline SVG icon (24x24px, stroke 1.5px) + label below
- Hover: icon stroke color shifts to accent + 5deg rotate

### 3.6 Stats Strip (`sxp-stats`)

- 4 canonical stats (per memory `suriota_user_preferences.md` — must match Homepage):
  - `64+` projects delivered
  - `6` in-house products
  - `25+` engineers
  - `5` core service pillars
- Number: IBM Mono 600, 56-72px, tabular-nums, with `+` in amber
- Label: mono caption uppercase, letter-spacing +0.06em
- Animated counter: 0 → target, 1.6s easeOutCubic, triggered by IntersectionObserver (threshold 0.4)
- `prefers-reduced-motion`: snap to final value, no animation
- All 5 pillars use identical stat values for sitewide consistency

### 3.7 Process Timeline (`sxp-proc`)

- Horizontal 5-step desktop / vertical mobile
- Connector: 1px line, fills to 2px accent on scroll progress through section
- Step: circle number (mono amber on light bg), title (PJS 600 18px), micro-description (Poppins 14px)

### 3.8 Case Studies (`sxp-case`)

- 2-col layout: image left, content right (alternates per row)
- Metric callout: large mono number (48-56px) + label
- "Read case →" link: arrow translateX 4px on hover
- Image: 4:3 ratio, subtle inner shadow, hover scale 1.02

### 3.9 FAQ Accordion (`sxp-faq`)

- Borderless, divider lines only (1px `--sx-line`)
- Question: PJS 600 18-20px
- Toggle icon: `+` rotates to `-` (45deg) — 300ms ease
- Content: max-height transition with opacity
- `aria-expanded`, `aria-controls`, proper button semantics

### 3.10 Final CTA Block (`sxp-cta`)

- Dark gradient: pillar accent → `--sx-teal-deep`
- Top accent bar (3px, gradient amber→teal→green) — carry-over from v1 CTA card
- Eyebrow `GET STARTED` (mono amber)
- H2: PJS 700 32-44px
- Body: Poppins 16-18px, max 60ch
- Dual CTA: White pill `Free Consultation` + dark teal `#075E54` WhatsApp (NEVER bright green — critical rule from memory)
- Trust line below: mono caption low-opacity (e.g., `64+ projects · ISO standards · 25+ engineers`)

---

## 4. Design Tokens (extend v1)

### 4.1 Inherited from v1 (`sx-design-system.css`)

All colors, fonts, spacing tokens from v1 carried unchanged.

### 4.2 New tokens for v2

```css
:root {
  /* Overlays */
  --sxp-overlay-deep: rgba(14, 57, 66, 0.92);
  --sxp-overlay-veil: rgba(14, 57, 66, 0.42);

  /* Textures */
  --sxp-dot-color: rgba(255, 255, 255, 0.06);
  --sxp-grid-color: rgba(255, 255, 255, 0.04);

  /* Elevation */
  --sxp-elev-1: 0 1px 0 rgba(14, 57, 66, 0.05);
  --sxp-elev-2: 0 8px 24px rgba(14, 57, 66, 0.08);
  --sxp-elev-3: 0 16px 40px rgba(14, 57, 66, 0.12);

  /* Motion */
  --sxp-ease: cubic-bezier(0.22, 1, 0.36, 1);
  --sxp-dur-fast: 180ms;
  --sxp-dur-base: 320ms;
  --sxp-dur-slow: 640ms;

  /* Per-pillar accent (overridden per body.page-id) */
  --sxp-accent: var(--sx-teal);
  --sxp-accent-soft: rgba(32, 91, 105, 0.12);
}

/* Per-pillar overrides */
body.page-id-5554, body.page-id-5566, body.page-id-5571 {
  --sxp-accent: #205B69;          /* P1 teal */
}
body.page-id-5555, body.page-id-5567, body.page-id-5572 {
  --sxp-accent: #3C7D47;          /* P2 green */
}
body.page-id-5556, body.page-id-5568, body.page-id-5573 {
  --sxp-accent: #C8851F;          /* P3 amber */
}
body.page-id-5557, body.page-id-5569, body.page-id-5574 {
  --sxp-accent: #205B69;          /* P4 teal */
}
body.page-id-5558, body.page-id-5570, body.page-id-5575 {
  --sxp-accent: #0E3942;          /* P5 deep teal */
  --sxp-accent-aux: #C8851F;       /* amber secondary */
}
```

### 4.3 Typography Scale

```
Display H1   clamp(2.5rem, 5vw, 4.5rem)   PJS 700  -0.02em  1.05em
Display H2   clamp(2rem, 3.5vw, 3rem)     PJS 700  -0.01em  1.1em
H3           clamp(1.25rem, 1.8vw, 1.75rem)  PJS 600  -0.005em  1.2em
Eyebrow      0.8125rem (13px)             IBM Mono 500 uppercase +0.08em
Body L       1.1875rem (19px)             Poppins 400 1.6em
Body M       1rem (16px)                  Poppins 400 1.6em
Caption      0.875rem (14px)              IBM Mono 400 uppercase +0.04em
Numeric      varies                        IBM Mono 600 tabular-nums
```

---

## 5. Motion System

### 5.1 Patterns

- **Scroll-reveal:** IntersectionObserver, threshold 0.15. `opacity: 0; transform: translateY(12px)` → `opacity: 1; transform: none`. 400ms ease-out. Stagger 80ms per child.
- **Counter:** 0 → target over 1.6s, easeOutCubic, on intersect.
- **Hover lift:** `translateY(-4px)` + shadow change, 200ms.
- **Link arrow slide:** `translateX(4px)` on hover, 180ms.
- **Accordion:** max-height + opacity transition, 300ms.

### 5.2 Reduce Motion compliance

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
  .sxp-stat-num { /* snap counter */ }
}
```

JS: Counter checks `window.matchMedia('(prefers-reduced-motion: reduce)').matches` before animating; if true, set final value directly.

---

## 6. Accessibility Targets

| Item | Standard |
|---|---|
| Text contrast | WCAG AA 4.5:1 min, AAA 7:1 preferred |
| Touch targets | ≥44×44 px |
| Keyboard nav | All interactive elements focusable, visible focus ring |
| Focus ring | 2px outline accent + 2px offset, never `outline: none` |
| Accordion semantics | `<button aria-expanded aria-controls>` |
| Sticky nav | Skip-to-content link visible on focus |
| Counter | Respect reduce-motion (snap to value) |
| Decorative SVG | `aria-hidden="true"`, `focusable="false"` |
| Image alt | All meaningful images alt; decorative empty `alt=""` |
| Heading order | H1 once, then H2 → H3 (no jump to H4 without H3) |

---

## 7. Implementation Approach

### 7.1 Build order (Phase A → D)

| Phase | Goal | Deliverable |
|---|---|---|
| **A** | Pilot Pillar 1 EN (5554) | Full design applied, validated visually + a11y |
| **B** | Apply Pillars 2–5 EN | Replicate templates with per-pillar accent |
| **C** | Apply ID + ZH (10 pages) | Mirror structure; CSS identical, content already translated per validation report |
| **D** | QA pass | `design:design-critique`, `design:accessibility-review`, manual visual review |

### 7.2 Tools per phase

| Phase | Primary tool | Purpose |
|---|---|---|
| All | Elementor REST `_elementor_data` | Insert HTML widgets, set Custom CSS |
| All | WP REST `/wp/v2/pages/{id}` | Update meta if needed |
| A | Local CSS author `design-system/sx-pillar-v2.css` | Single canonical source |
| D | `design:accessibility-review` skill | a11y audit |
| D | `design:design-critique` skill | design QA |
| D | Browser snapshot (Playwright/Puppeteer) | Visual regression vs prior state |

### 7.3 Rollback safety

- Each pillar's existing `_elementor_data` and Custom CSS is **backed up to local JSON** before modification (e.g., `backups/pillar-5554-before-styling-2026-05-24.json`)
- Per-page changes are independent → rollback one pillar doesn't affect others
- No global state changes → site-wide rollback not needed

---

## 8. Open Questions (None — user delegated)

All decisions made autonomously per user directive in session. No clarifications needed before plan.

---

## 9. Success Criteria

- [ ] All 15 pillar pages visually polished with v2 design system
- [ ] Zero regression on any non-pillar page
- [ ] All pillar pages WCAG AA compliant (verified via design:accessibility-review)
- [ ] `prefers-reduced-motion` respected (snap behavior tested)
- [ ] Mobile (≤768px) parity with desktop quality
- [ ] CSS file `sx-pillar-v2.css` committed to repo
- [ ] All Elementor changes logged with backup JSONs

---

## 10. Next Step

Invoke `writing-plans` skill to produce an executable implementation plan from this spec. No code or Elementor mutation until plan exists.
