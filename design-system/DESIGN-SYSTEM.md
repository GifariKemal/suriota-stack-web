# SURIOTA Design System — Industrial Editorial v1

Locked on About Us page (`post_id=29`) — 2026-05-16. All future pages MUST apply this system to ensure visual consistency.

## Aesthetic Direction
**Industrial Editorial** — refined B2B engineering. Inspired by Linear changelog, Siemens corporate, Bosch annual reports. Disciplined, technical, trustworthy. NOT playful or maximalist.

---

## 1. Tokens

### Color
| Token | Hex | Use |
|---|---|---|
| `--sx-teal` | `#205B69` | Primary brand, headings on light, CTAs |
| `--sx-teal-deep` | `#0E3942` | High-contrast headings (h2/h3 over light) |
| `--sx-green` | `#3C7D47` | Accent — automation/EBT/growth signals |
| `--sx-amber` | `#C8851F` | Industrial accent (eyebrow slash, card numbers, plus signs) |
| `--sx-surface` | `#FAFBFC` | Card background (off-white, not pure white) |
| `--sx-line` | `#E8ECEE` | Hairline rules, card borders |
| `--sx-text` | `#1F2D33` | Body text on light |
| `--sx-text-mute` | `#5B6F75` | Secondary text, descriptions |

### Typography
| Token | Family | Use |
|---|---|---|
| `--sx-font-display` | **Plus Jakarta Sans** 600/700 | All H1, H2, H3 headings |
| `--sx-font-mono` | **IBM Plex Mono** 500/600 | Eyebrows, stat numerics, card numbers, "Pelajari" CTA |
| `--sx-font-body` | **Poppins** 400 | Body paragraphs (existing brand font) |

### Scale (responsive via `clamp()`)
- **H1**: `clamp(34px, 5vw, 56px)` Plus Jakarta Sans 700, letter-spacing −1.5
- **H2**: `clamp(28px, 4vw, 38px)` Plus Jakarta Sans 700, letter-spacing −0.5
- **H3**: `18–22px` Plus Jakarta Sans 600, letter-spacing −0.2 to −0.3
- **Body**: `15.5–17px` Poppins/system 400, line-height 1.65–1.75
- **Mono caption**: `11–13px` IBM Plex Mono 500, letter-spacing 1–1.5
- **Stat number**: `clamp(40px, 6vw, 60px)` IBM Plex Mono 600 tabular

### Motion
| Token | Value |
|---|---|
| `--sx-ease` | `cubic-bezier(0.22, 1, 0.36, 1)` |
| Reveal duration | 620ms |
| Hover lift duration | 280ms |
| Underline draw | 320ms |
| Stagger delays | 0 / 100 / 200 / 300 ms |

---

## 2. Components

### `.sx-eyebrow`
Mono uppercase tag with `// ` amber prefix. Above section headings.
```html
<span class="sx-eyebrow">Layanan Utama</span>
<!-- Renders: // LAYANAN UTAMA  (// in amber, rest in teal) -->
```
Variant `.sx-eyebrow--light` for dark backgrounds.

### `.sx-numlabel`
Amber mono label. For section/card numbering (`01 / VISI`, `02 / MISI`).
```html
<span class="sx-numlabel">01 / VISI</span>
```

### `.sx-card-num`
Absolutely-positioned amber card number badge (top-left of cards).
```html
<article style="position:relative; padding-top:36px;">
  <span class="sx-card-num">01</span>
  <!-- card content -->
</article>
```

### `.sx-stat-num`
Tabular mono numeric for stats. Use `<span class="sx-plus">+</span>` for amber plus sign.
```html
<div class="sx-stat-num" style="font-size:clamp(40px,6vw,60px);">
  64<span class="sx-plus">+</span>
</div>
```

### `.sx-hr`
Hairline 1px rule. `.sx-hr--light` for dark backgrounds.
```html
<hr class="sx-hr" style="margin:64px 0 40px;" />
```

### `.sx-underline`
Hover underline-draw effect (currently scoped to `.about-service-card-link` hover).
```html
<span class="sx-underline">Pelajari</span>
```

### `.sx-reveal`
Fade-up entry animation. Use `data-d` for stagger.
```html
<div class="sx-reveal" data-d="100">...</div>
```

---

## 3. Section Templates (Elementor)

Saved as Elementor templates (Mei 2026). Insert via Elementor → Templates → My Templates.

| Template ID | Title | Use |
|---|---|---|
| **4675** | SX / Stats Bar (Industrial Editorial) | Numeric proof points |
| **4677** | SX / Service Card Grid 01-04 | 4 service/category cards w/ numbers |
| **4679** | SX / Trust Cards (Mengapa Memilih) | Differentiators (left-border) |
| **4681** | SX / CTA Dual-Action (Primary + WA + Form) | Conversion section |

---

## 4. CTA Pattern

### Dual-action
Always 1 primary + 2 secondary (WhatsApp + Form).
- Primary: white pill on dark bg
- WhatsApp: `#075E54` (WCAG AA dark teal) — **NEVER use `#25D366`** (fails 4.5:1)
- Form: outline white, transparent bg
- All buttons have SVG icon left, focus-visible 3px outline
- Mobile: stack vertical, full-width

WA link format:
```
https://wa.me/6285835672476?text=Halo%20SURIOTA%2C%20saya%20ingin%20konsultasi...
```
Number: **+62 858 3567 2476** (from homepage social icons widget `208da1c7`)

---

## 5. SEO Schema Pattern

Each page should have JSON-LD with `@graph` array containing:
1. `Organization` + `LocalBusiness` (singleton, `@id: https://suriota.com/#organization`)
2. Page type (`AboutPage`, `WebPage`, `Service`, `Product`)
3. `BreadcrumbList`
4. `Service` entries for relevant offerings

Reference implementation: About Us widget `8ef5419`.

### Required fields
- `name`, `url`, `description`, `logo`, `image`
- `address` (PostalAddress: Batam, Kepulauan Riau, ID)
- `contactPoint` (phone, email, languages)
- `sameAs` (Instagram, LinkedIn, Tokopedia)
- `foundingDate` (2023-01)

---

## 6. Accessibility (WCAG 2.1 AA)

- All interactive elements: `:focus-visible` 3px outline
- Color contrast: text ≥ 4.5:1 on bg; UI ≥ 3:1
- Touch target: ≥ 44×44 (CTA min 47px height)
- Motion: `@media (prefers-reduced-motion: reduce)` disables animations
- Pulse animations: max 3 iterations (≤12s)
- SVG icons: `aria-hidden="true"`
- Anchors: descriptive `aria-label` when icon-only

---

## 7. Responsive Breakpoints

| Range | Behavior |
|---|---|
| `≥1024px` | Desktop baseline — design here first |
| `640–1023px` | Tablet — 2-col grids |
| `360–639px` | Mobile — 1-col stacks, full-width buttons |
| `≤359px` | Small mobile — tighter padding, smaller fonts |

Apply via media queries in `sx-design-system.css`. Section padding via Elementor `padding_tablet` / `padding_mobile` settings (desktop=100%, tablet ~85%, mobile ~75%).

---

## 8. Implementation Checklist (per new page)

1. ☐ Paste `sx-design-system.css` content to **Elementor → Site Settings → Custom CSS** (or per-page Custom CSS)
2. ☐ Apply saved Elementor templates as section starting points
3. ☐ Use `.sx-eyebrow` above every section H2
4. ☐ Number all multi-item lists/grids (`01 / 02 / 03 / 04`)
5. ☐ Use `IBM Plex Mono` for all numerics, CTA labels, captions
6. ☐ Use `Plus Jakarta Sans` for all headings (override Elementor heading defaults)
7. ☐ Set section padding responsive (tablet/mobile values)
8. ☐ Add JSON-LD schema appropriate to page type
9. ☐ Verify contrast + keyboard nav + screen reader announcement
10. ☐ Test at 1440 / 768 / 375 / 360 widths

---

## 9. AIOSEO Per-Page Checklist (MANUAL — di WP Admin)

Setiap page baru WAJIB di-set via AIOSEO sidebar saat editing page di WP Admin:

### General Tab
- **SEO Title** format: `[Page Topic with primary keyword] | PT Surya Inovasi Prioritas`
  - Max 60 chars (terlihat penuh di Google)
  - Selalu include 1 primary keyword + brand
- **Meta Description**: 150-160 chars, narrative + 1 CTA verb
  - Format: `[Brand + value prop]. [Key proof/numbers]. [CTA action verb].`

### Social Tab — Facebook
- **OG Title**: berbeda dari SEO title, lebih punchy, max 60 chars
- **OG Description**: 150-200 chars, social-friendly
- **OG Image**: page-specific 1200×630 (NOT generic Cover-Link-Share.png)

### Social Tab — Twitter
- Default biasanya inherit Facebook — verify

### Schema Tab
- Page Type: AboutPage / WebPage / Service / Product (per konteks)
- Person/Organization linked properly

### Content templates for next pages
| Page | SEO Title (≤60c) | Meta Desc (≤160c) |
|---|---|---|
| Tentang Kami | `Tentang SURIOTA — Industrial IoT & System Integration di Batam` | `PT Surya Inovasi Prioritas (SURIOTA) — Industrial IoT & System Integration di Batam. 64+ proyek, 6 produk in-house. Hubungi tim engineer.` |
| Homepage | `SURIOTA — Industrial IoT Partner di Indonesia` | `Industrial IoT, AI Analytics & System Integration di Indonesia. SURGE platform, Modbus Gateway, 64+ proyek industri. Konsultasi gratis.` |
| Portfolio | `Portfolio Proyek SURIOTA — 64+ Implementasi Industrial IoT` | `Lihat 64+ proyek SURIOTA: PDAM Tirta Kepri, manufaktur, energi, maritim. Modbus Gateway, SCADA, PLTS hybrid. Studi kasus lengkap.` |
| Electrical | `Jasa Engineering Elektrikal Industri — SURIOTA Batam` | `Panel industrial, distribusi daya, commissioning & testing. Standar IEC/IEEE/SNI. Konsultasi engineer SURIOTA di Batam.` |
| Automation | `Otomasi Industri & SCADA — SURIOTA IoT Solutions` | `PLC, SCADA, IIoT integration end-to-end. SURGE platform real-time monitoring. Tim engineer SURIOTA Batam berpengalaman.` |
| Water Treatment | `Water Treatment Plant & IoT Monitoring — SURIOTA` | `WTP, WWTP, SPARING IoT, monitoring kualitas air real-time. Proyek PDAM Tirta Kepri. Hubungi tim SURIOTA.` |
| Renewable Energy | `PLTS & Energi Terbarukan — SURIOTA Solar Engineering` | `Desain & instalasi PLTS, sistem hybrid PLTS-PLTB, monitoring energi berbasis IoT. SURIOTA Batam, Kepulauan Riau.` |

### Verifying SEO post-publish
1. View source: `Ctrl+U`
2. Check `<title>`, `<meta name="description">`, `og:title`, `og:description`
3. Run https://validator.schema.org/ untuk JSON-LD
4. Run https://search.google.com/test/rich-results untuk Rich Results Test
5. Lighthouse SEO audit (target ≥ 95)

---

## 10. Mobile Responsive Notes (v2)

Issues addressed 2026-05-16:
- Grid layouts (`auto-fit` minmax) — force `1fr` columns at ≤639px
- Cards overflow — `min-width:0; overflow:hidden; overflow-wrap:break-word`
- Stats borders — replace L/R strokes with bottom border on mobile stack
- Container widths — `max-width:1080px/960px` containers respect viewport on mobile
- Tablet (640-1023) — service & CIPTA grids force 2-column

All fixes baked into `sx-design-system.css` — apply to every new page.

---

## 11. References

- Live implementation: https://suriota.com/about-us/
- Source page: `post_id=29` (About Us)
- CSS file: `design-system/sx-design-system.css`
- Backup of pre-refactor state: `backups/elementor_doc_29.json`

Version 1 / 2026-05-16 / Locked.
