# SURIOTA Pillar Pages v2 — Deployment Summary

**Date:** 2026-05-24
**Spec:** docs/superpowers/specs/2026-05-24-pillar-styling-design.md
**Plan:** docs/superpowers/plans/2026-05-24-pillar-styling.md

## Scope adherence — VERIFIED

Posts mutated: 15 / 15 allowed (no out-of-scope mutations)

| Lang | Posts | Slugs |
|---|---|---|
| EN | 5554, 5555, 5556, 5557, 5558 | industrial-iot-system-integration, ai-industrial-analytics, digital-transformation-consulting, industrial-engineering-automation, surge-saas-platform |
| ID | 5566, 5567, 5568, 5569, 5570 | iot-industri-integrasi-sistem, ai-analitik-industri, konsultasi-transformasi-digital, teknik-industri-otomasi, platform-saas-surge |
| ZH | 5571, 5572, 5573, 5574, 5575 | gongye-wulianwang-jicheng, ai-gongye-fenxi, shuzihua-zhuanxing-zixun, gongye-gongcheng-zidonghua, surge-saas-pingtai |

## Non-pillar leakage check — VERIFIED

12 non-pillar URLs sampled, all returned 0 sxp- class occurrences:

```
0  https://suriota.com/
0  https://suriota.com/about-us/
0  https://suriota.com/automation/
0  https://suriota.com/electrical/
0  https://suriota.com/renewable-energy/
0  https://suriota.com/water-treatment/
0  https://suriota.com/portfolio/
0  https://suriota.com/surge-energy-mapping/
0  https://suriota.com/internship/
0  https://suriota.com/contact/
0  https://suriota.com/id/
0  https://suriota.com/zh/shouye/
```

Legacy service URLs verified to still redirect cleanly (301):

```
https://suriota.com/internet-of-things/      -> 301 https://suriota.com/industrial-iot-system-integration/
https://suriota.com/artificial-intelligence/ -> 301 https://suriota.com/ai-industrial-analytics/
https://suriota.com/data-analytics/          -> 301 https://suriota.com/ai-industrial-analytics/
https://suriota.com/system-integration/      -> 301 https://suriota.com/industrial-iot-system-integration/
```

## Accessibility — baseline maintained

15/15 pillars sit at the established sitewide baseline of ~3 violations / 1 serious-critical.

The 1 serious violation across all pillars is `color-contrast` — pre-existing sitewide issue not introduced by this rollout (also present on non-pillar pages).

The 2 moderate violations:
- `heading-order` on the global footer (`<h4>` without preceding `<h3>`) — pre-existing
- `landmark-unique` on the FAQ region (pattern reused across all pillars)

Zero new violations introduced.

Per-pillar a11y rollup (all 15 identical):

| Post | Total violations | Serious/critical | Serious rules |
|---|---|---|---|
| 5554-5558 (EN) | 3 | 1 | color-contrast |
| 5566-5570 (ID) | 3 | 1 | color-contrast |
| 5571-5575 (ZH) | 3 | 1 | color-contrast |

## Components delivered

10 v2 components: hero, in-page nav (P4 only), capabilities grid, tech strip, industries grid, stats with animated counter, process timeline, case studies, FAQ accordion, final CTA block.

Per-pillar variations:
- P1 IoT — teal `#205B69` dark hero
- P2 AI — green `#3C7D47` dark hero
- P3 Consulting — amber `#C8851F` LIGHT hero + deliverables instead of industries
- P4 Engineering — teal sticky in-page nav + 4 anchored sub-sections (automation, electrical, renewable-energy, water-treatment)
- P5 SaaS — deep teal `#0E3942` + amber aux, features/deployment/pricing sections

## Local artifacts

- `design-system/sx-pillar-v2.tokens.css` (60 lines) — CSS variables + per-pillar accent
- `design-system/sx-pillar-v2.components.css` (~384 lines) — 10 component styles + reduce-motion
- `design-system/sx-pillar-v2.motion.js` (~100 lines) — reveals + counters + FAQ + sticky nav
- `design-system/components/p{1..5}-*.html` (EN widget templates)
- `design-system/components/id/p{1..5}-*.html` (ID translations)
- `design-system/components/zh/p{1..5}-*.html` (ZH translations)
- `tools/py/pillar_{env,backup,apply_css,insert_widget,clear_cache,snapshot,a11y}.py`
- `backups/pillars/{5554..5575}-2026-05-24.json` (15 pre-mutation backups)
- `audit/pillar-v2-snapshots/{after/{desktop,mobile},a11y/}` (30 snapshots + 15 a11y JSON reports)

## Rollback path

Per-post rollback supported via `backups/pillars/<post_id>-2026-05-24.json`. Each backup contains `_elementor_data` and `_elementor_page_settings` snapshots before any mutation. Restore via REST POST.

## Critical operational note

Elementor caches rendered HTML separately from `_elementor_data`. After bulk REST widget insertion, the page only renders the FIRST new section until cache is flushed via admin-ajax `elementor_clear_cache`. The helper `tools/py/pillar_clear_cache.py` is REQUIRED after every batch insert. Documented in `~/.claude/projects/.../memory/suriota_elementor_cache_flush.md`.

## Git history

Session commits (28 total, oldest first):

```
8daa5ab chore(pillars): scaffold dirs + env example
30bcea0 feat(pillars): wp rest auth helper + scope lock
2c1264b chore(pillars): backup _elementor_data for 15 posts (pre-styling)
24a958d feat(pillars): v2 tokens + per-pillar accent variables
e72c0dd feat(pillars): v2 components stylesheet (10 components)
6f36da9 feat(pillars): v2 motion js (reveals, counters, faq, sticky nav)
e24e613 feat(pillars): p1 hero widget html
248ca6e feat(pillars): p1 widget html templates (8 sections)
b4f5a27 feat(pillars): apply css + insert widget scripts (session auth, idempotent)
bca5e7e feat(pillars): p1 motion wrapper + deployed to pilot 5554
7218de2 feat(pillars): elementor render-cache flush helper
8d1c02c feat(pillars): visual + a11y verification (pilot 5554)
66c0dbf fix(pillars): reveal in-viewport elements immediately on bind (UX + screenshotability)
b2e0cdb fix(pillars): force-reveal all sxp-reveal elements before screenshot
1011d6c chore(pillars): re-snapshot 5554 after reveal-on-load fix
cb94275 fix(pillars): faq button focus-visible specificity (a11y wcag 2.4.7)
608637e feat(pillars): p2 widget html templates (ai & industrial analytics)
fdf9176 feat(pillars): apply v2 to p2 ai-industrial-analytics (5555)
3a4deba feat(pillars): p3 widget html templates (digital transformation consulting, light hero)
4ae39e3 feat(pillars): apply v2 to p3 digital-transformation-consulting (5556, light hero)
a5b6720 feat(pillars): p4 widget html templates (industrial engineering & automation)
8eda98a feat(pillars): apply v2 to p4 industrial-engineering-automation (5557, sticky nav + 4 sub-sections)
ba37b29 feat(pillars): p5 widget html templates (surge saas platform)
749724f feat(pillars): apply v2 to p5 surge-saas-platform (5558)
217644c feat(pillars): id widget html templates (46 files, all 5 pillars translated)
5ba8716 feat(pillars): apply v2 to 5 id pillars (5566-5570)
d2f5d17 feat(pillars): zh widget html templates (46 files, all 5 pillars translated)
13e5a58 feat(pillars): apply v2 to 5 zh pillars (5571-5575)
```
