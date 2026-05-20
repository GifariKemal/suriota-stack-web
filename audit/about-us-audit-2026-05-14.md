# About Us Page Audit Report — 2026-05-14

**URL:** https://suriota.com/about-us/  
**Tools:** Playwright (chromium), computed-style evaluation, full-page screenshots (1920×1080 & 375×812)

---

## 1. Entry Title Hidden

| Check | Result |
|-------|--------|
| `.entry-title` display | `none` ✅ |
| Mobile | `none` ✅ |

**Status:** PASS — entry title is correctly hidden on both desktop and mobile.

---

## 2. Button Shape (Pill vs Rectangular)

| Button | border-radius | height | Pill-shaped? |
|--------|---------------|--------|--------------|
| "Unduh Company Profile" (CTA) | `8px` | `64px` | ❌ NO (needs ≥32 px) |
| "Consulting Engineering Service" (footer) | `1px` | `72px` | ❌ NO (almost square) |
| "About Us" nav item | `0px` | auto | ❌ NO |

**Status:** ISSUE — No buttons are pill-shaped. The primary CTA "Unduh Company Profile" is a rounded rectangle (8 px radius). The footer button is effectively square-cornered. Per design guidelines, primary CTAs should be pill-shaped for stronger visual identity.

**Recommendation:** Change CTA buttons to `border-radius: 9999px` (or ≥ height/2).

---

## 3. Layout Issues, Missing Elements, Overlaps

### Desktop (1920 px)
- No horizontal overflow detected.
- No near-zero-height sections.
- No overlapping elements detected via bounding-box checks.
- **Status:** ✅ PASS

### Mobile (375 px)
- No body overflow.
- **Stats section stacks in a single column** (64+, 2+, 4, 500+ each on its own row). AGENTS.md specifies stats should use a **2-column grid** on mobile.
- Vision/Mission cards stack vertically — ✅ correct.
- 4 Bidang cards stack vertically — ✅ correct.
- Makna Logo cards stack vertically — ✅ correct.
- Footer "Consulting Engineering Service" button appears as a full-width block — acceptable but very large.

**Status:** ⚠️ PARTIAL — Stats mobile layout is 1-column instead of intended 2×2 grid.

---

## 4. Section Checks

### Stats Section
- **Found:** Yes — text: `64+ PROYEK SELESAI  2+ TAHUN BEROPERASI  4 BIDANG LAYANAN  500+ SENSOR IIOT DIPASANG`
- **Desktop:** Displays in a single horizontal bar (good).
- **Mobile:** Stacks vertically (1 column). Expected 2×2 grid.
- **Status:** ⚠️ Needs mobile grid fix.

### Vision / Mission Section
- **Found:** Yes — two cards side-by-side on desktop.
- **Content:** VISI KAMI (teal) & MISI KAMI (green) with icon badges.
- **Cards:** White background, 12 px radius, subtle shadow (`rgba(32,91,105,0.08) 0px 2px 12px`).
- **Mobile:** Stacks correctly.
- **Status:** ✅ PASS

### Services / 4 Bidang Fokus Section
- **Found:** Yes — 4 cards: Elektrikal, Otomasi & IoT, Water Treatment, Energi Terbarukan.
- **Cards:** `.about-service-card` — white bg, 14 px radius, shadow `rgba(0,0,0,0.07) 0px 2px 12px`, padding 28×20 px.
- **Desktop:** 4 columns in one row.
- **Mobile:** Stacked vertically.
- **Status:** ✅ PASS

### Makna Logo Section
- **Found:** Yes — 4 meaning cards (S, cloud, gear, refresh icons).
- **Cards:** `.about-logo-card` — white bg, 10 px radius, shadow `rgba(0,0,0,0.06) 0px 1px 6px`.
- **Status:** ✅ PASS

### CTA Section
- **Found:** Yes — "Siap Berkolaborasi dengan SURIOTA?"
- **Background:** `rgb(32, 91, 105)` (teal).
- **Button:** "Unduh Company Profile" (white bg, teal text, 8 px radius).
- **Status:** ✅ PASS

---

## 5. Heading Font Consistency

| Heading | Text | font-family | font-size | Issue |
|---------|------|-------------|-----------|-------|
| H1 | About Us (hidden) | system sans | 40 px | Hidden — acceptable |
| **H1** | **Tentang SURIOTA** | **Poppins** | **52 px** | ✅ Correct |
| H2 | Siapa SURIOTA? | system sans | 28 px | ❌ Should be Poppins |
| H2 | 4 Bidang Fokus SURIOTA | system sans | 32 px | ❌ Should be Poppins |
| H2 | Siap Berkolaborasi… | Lato | 32 px | ❌ Should be Poppins |
| H3 | VISI KAMI | Poppins | 22 px | ✅ Correct |
| H3 | MISI KAMI | Poppins | 22 px | ✅ Correct |
| H3 | Elektrikal (card) | system sans | 16 px | ❌ Should be Poppins |
| H3 | Otomasi & IoT (card) | system sans | 16 px | ❌ Should be Poppins |
| H3 | Water Treatment (card) | system sans | 16 px | ❌ Should be Poppins |
| H3 | Energi Terbarukan (card) | system sans | 16 px | ❌ Should be Poppins |

**Summary:**
- Only the hero H1 and Vision/Mission H3s use **Poppins**.
- All other H2s and card H3s fall back to **system sans-serif** or **Lato**.
- **Status:** ❌ FAIL — Inconsistent typography. Headings should uniformly use Poppins (or the brand heading font) per global typography tokens.

**Additional SEO Issue:** There are **two H1 tags** on the page (`About Us` hidden entry-title + `Tentang SURIOTA` visible). Even though one is hidden, best practice is to have a single H1. The visible hero heading should ideally be H1 (it is), but the entry-title should be demoted to `<div>` or `<span>` rather than hidden H1.

---

## 6. V4 Leftover Styling

The audit searched for unintended Elementor V4 container defaults (white backgrounds + large rounded corners + shadows).

| Finding | Context | Verdict |
|---------|---------|---------|
| White cards with 14 px radius + shadow | 4 Bidang Fokus | ✅ Intentional (`.about-service-card` from refactor) |
| White cards with 10 px radius + shadow | Makna Logo | ✅ Intentional (`.about-logo-card` from refactor) |
| White cards with 12 px radius + shadow | Vision/Mission | ✅ Intentional (custom card layout) |
| `.elementor-column` backgrounds | Mostly `rgba(0,0,0,0)` | ✅ No V4 white column backgrounds left |

**Status:** ✅ PASS — No unintended V4 leftover styling detected. All white cards with radius/shadow are the custom inline-CSS cards introduced in the 2026-05-13 refactor.

---

## 📋 Issue Summary

| # | Issue | Severity | Location |
|---|-------|----------|----------|
| 1 | Buttons not pill-shaped | Medium | CTA "Unduh Company Profile", footer button |
| 2 | Stats mobile layout = 1 col instead of 2×2 | Medium | Stats bar |
| 3 | Heading font inconsistency (system sans vs Poppins/Lato) | **High** | H2s and card H3s |
| 4 | Duplicate H1 (`entry-title` + hero) | Low | Page header |

---

## 📁 Artifacts

- Screenshots: `screenshots/2026-05-14-audit/about-desktop.png`
- Screenshots: `screenshots/2026-05-14-audit/about-mobile.png`
- JSON data: output of `scripts/about-audit-deep.js`
