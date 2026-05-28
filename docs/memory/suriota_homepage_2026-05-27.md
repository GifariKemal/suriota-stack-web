---
name: Suriota Homepage State 2026-05-27 (post modbus + portfolio + backtop work)
description: Homepage EN/ID/ZH final state — 11 sections each, products section[4]/[5] images, interactive portfolio table widget, backtop section[10], modbus poster v2
type: project
originSessionId: 13e95821-5ff9-473c-b59f-932e6f2ac11c
---
## Homepage section layout (identical EN/ID/ZH; page IDs 12 / 5273 / 5448)

| Idx | Section ID (EN) | Content |
|-----|-----------------|---------|
| 0 | e916bb8 | Hero — brand + 5 about-service cards + CTA |
| 1 | 49b2d08 | Wide impact text block |
| 2 | 7d40b0e | Divider |
| 3 | 242deed | "Products" heading |
| 4 | 96f1119 | Product row 1 — ISO-M485 / SURGE Energy Map / **Modbus Gateway IIoT** |
| 5 | 4d0b943 | Product row 2 — THM-30MD / PM1611-WD / SPD T485-105 |
| 6 | 9570a11 | Trusted By logos carousel |
| 7 | 66a7c22 | Portfolio heading + interactive live table widget |
| 8 | 9445d91 | Divider |
| 9 | 3f10b949 | Our Location (map iframe) + Contact form |
| 10 | (EN: b08b89d / ID: 7cd727f / ZH: 2adf449) | Back-to-top HTML widget (`_sxpId: homepage-backtop`) |

All product images render at 1242×626 (2:1 ratio).

## Modbus Gateway poster regeneration (2026-05-27)
Original `modbus-poster-scaled.webp` was 2560×615 (4.16:1) — broke visual consistency vs siblings at 2:1. Replaced with **`modbus-poster-v2.webp`** (1242×626, media ID 5611, URL `wp-content/uploads/2026/05/modbus-poster-v2.webp`). Generated via Pillow: single device photo (cropped from x=1990..2520 of original) on left, orange title + green subtitle + grey desc on right (matches sibling poster layout). Updated image widget `8ef32ff` on EN/ID/ZH section[4].

## Backtop widget (EN was missing → restored)
EN section[10] was lost during a previous save cycle. Restored 2026-05-27 by copying ZH template + ID-rotating. Also injected the same backtop init script into the portfolio widget HTML in section[7] as a fallback. Script self-guards via `window.__sxHomeBacktop` so dual presence is harmless.

## Portfolio live table widget
Widget IDs: EN `7ff1e85`, ID `70cc889`, ZH `0b89840`. Fetches from `/portfolio/`, `/id/portfolio-id/`, `/zh/anli/` via DOMParser of `<table class="port-table">`. SessionStorage cache 5min TTL. Renders top 10. Sort + filter. Mobile uses CSS Grid card layout. Source spec: `design-system/components/homepage-portfolio-live.html`.

## Cache state
WP-Optimize page caching: **OFF**. Elementor render cache is the only layer. After any REST `_elementor_data` edit, run Elementor → Tools → Clear Files & Data (see `suriota_elementor_cache_flush.md`).
