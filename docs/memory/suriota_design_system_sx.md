---
name: Suriota sx- Design System
description: Industrial Editorial design tokens, components, fonts, and Elementor template IDs for suriota.com
type: project
originSessionId: 587198fb-6cea-4b87-a692-d8a6e5ea6255
---
Design system locked 2026-05-16 on About Us page. All future pages must apply this for visual consistency.

## Local Files
- `design-system/DESIGN-SYSTEM.md` — Full spec (tokens, components, checklist, reuse playbook)
- `design-system/sx-design-system.css` — Reusable CSS (~360 lines, paste-ready for Elementor Custom CSS)

## Tokens

### Colors
- `--sx-teal: #205B69` — primary brand
- `--sx-teal-deep: #0E3942` — headings/dark hero
- `--sx-green: #3C7D47` — accent (automation/EBT/growth)
- `--sx-amber: #C8851F` — industrial accent (eyebrow //, card numbers, +signs)
- `--sx-surface: #FAFBFC` — off-white card bg
- `--sx-line: #E8ECEE` — hairlines
- `--sx-text: #1F2D33` — body
- `--sx-text-mute: #5B6F75` — secondary text

### Fonts
- Display: **Plus Jakarta Sans** (700 for headings)
- Mono: **IBM Plex Mono** (numerics, eyebrows, badges, "Pelajari/Learn More" CTA)
- Body: Poppins (already brand)

### Per-page Accent (Service Pages)
- Electrical → `#C8851F` amber
- Automation → `#205B69` teal
- Water Treatment → `#205B69` teal
- Renewable Energy → `#3C7D47` green

## Saved Elementor Templates (My Templates in WP Admin)
| Template ID | Title | Use |
|---|---|---|
| 4675 | SX / Stats Bar (Industrial Editorial) | Numeric proof points |
| 4677 | SX / Service Card Grid 01-04 | Service cards with numbers |
| 4679 | SX / Trust Cards (Mengapa Memilih) | Differentiator cards (left-border) |
| 4681 | SX / CTA Dual-Action (Primary + WA + Form) | Conversion section |

## Components (CSS classes)
- `.sx-eyebrow` — mono uppercase small tag (12px, color teal). NO `//` prefix (user removed it)
- `.sx-numlabel` — amber mono label (13px) for 01/VISI, 02/MISI, etc.
- `.sx-card-num` — amber mono card badge (top-left or static)
- `.sx-stat-num` — tabular mono for stats (font-feature-settings: "tnum" 1)
- `.sx-stat-num .sx-plus` — amber + sign accent
- `.sx-hr` — hairline rule
- `.sx-underline` — hover underline-draw effect
- `.sx-reveal` — fade-up entry animation (data-d="100/200/300/400" for stagger)
- `.about-cta--primary` — white pill on dark (download/primary action)
- `.about-cta--wa` — dark teal #075E54 WhatsApp (NEVER use #25D366 — fails WCAG 4.5:1)
- `.about-cta--form` — outline white pill (contact form)

## Critical Rules
- **NEVER use `line-height` in `px`** for headings — causes overlap bug. Always `em` unit.
- **WhatsApp button MUST be `#075E54` dark teal** (7.86:1 AAA), NOT bright `#25D366` (fails 2.00:1 AA).
- **Pulse animation max 3 iterations** (~12s) for WCAG 2.2.2 compliance.
- **Service pages need `html body` prefix** in CSS to override site-wide inline style block.

## Reusable Pattern for New Pages
1. Apply `sx-design-system.css` to page Custom CSS
2. Use sx- eyebrow above every section H2
3. Number multi-item grids (`01 / 02 / 03 / 04`)
4. IBM Plex Mono for all numerics + CTA labels + captions
5. Plus Jakarta Sans for all H1/H2/H3
6. Section padding: 32-60px desktop, 24-40px mobile
7. Add JSON-LD schema appropriate to page type
