---
name: Gifari Suriota Website Preferences
description: Direct feedback patterns from CEO Gifari during suriota.com refactor — language, structure, design, content rules
type: feedback
originSessionId: 587198fb-6cea-4b87-a692-d8a6e5ea6255
---
## Language & Content Rules

**Rule: All suriota.com pages must be FULL ENGLISH.**
**Why:** User explicitly switched from mixed Bahasa Indonesia to English mid-session. Wants consistent international tone for the website (different from internal/chat communication which stays Bahasa).
**How to apply:** When refactoring any page, translate Indonesian widgets/headings/buttons/FAQ/JSON-LD descriptions to English. Don't mix.

**Rule: No content duplication between Homepage and About Us.**
**Why:** User explicitly said "jangan duplikasi" — if it's on homepage, don't repeat on About Us.
**How to apply:** Stats Bar (64+/6/5/25+) and 5 Services list belong ONLY on Homepage. About Us shows brand story (Vision/Mission, paragraph, CIPTA values, CTA) without re-listing services or stats.

**Rule: Content must match official company profile.**
**Why:** Company profile at `C:\Users\Administrator\Desktop\Suriota AI Analys\01. Company Profile\Suriota - Company Profile.md` is the canonical source.
**How to apply:** When in doubt about content (services, values, products, location), defer to company profile. Key facts: 64+ projects (not 55), CIPTA core values, Industrial IoT positioning (not just engineering services), Batam Centre HQ.

## Design Preferences

**Rule: Conservative visual changes — V4 was reverted.**
**Why:** Homepage "V4 visual enhancement" was previously reverted because "jadi hancur" (looks broken). User scarred by over-styling.
**How to apply:** Refactors should be additive/refinement, not radical rewrites. Keep working visual elements (product images, client logos, portfolio cover). Improve typography + spacing + colors WITHOUT removing assets.

**Rule: No `//` prefix on eyebrows.**
**Why:** User said "hapus //, gk jelas itu" — found code-comment style confusing.
**How to apply:** sx-eyebrow class CSS pseudo `::before { content: "// "; }` REMOVED. Keep small mono uppercase tag style without slash.

**Rule: Industrial Editorial aesthetic, not maximalist.**
**Why:** User prefers refined/professional look (Linear, Siemens, Bosch style). Not flashy/colorful.
**How to apply:** Use Plus Jakarta Sans + IBM Plex Mono fonts, off-white surface (#FAFBFC), 8px radius, hairline borders, ONE per-page accent color (amber/teal/green), letter-spacing tight on headings.

**Rule: Compact spacing — no excessive scroll.**
**Why:** User feedback: "kalau bisa dibuat compact, gk banyak space, scroll up dan down tidak terlalu jauh".
**How to apply:** Section padding: ~30-60px desktop (not 100px). Card padding: 18-24px (not 32+). Mobile padding tighter ~20-32px.

## Specific Corrections Applied

- Internship location: **Batam** (not Yogyakarta — user corrected 2026-05-17)
- Project count: **64+** (not 55+ which was company profile typo — user clarified)
- WhatsApp number: **+62 858-3567-2476** (from homepage social icons widget)
- Contact form path: **`/contact/`** (not `/contact-us/`)
- "Free Consultation" button (NOT "Konsultasi Gratis" — English even when surrounding text is mixed)

## Workflow Preferences

**Rule: Use Claude Design plugin skills for UI/UX tasks.**
**Why:** User specifically requested using design plugin at https://claude.com/plugins/design.
**How to apply:** For UI/UX work, invoke `design:design-critique`, `design:design-system`, `design:design-handoff`, `design:accessibility-review`, `design:ux-copy` from the design plugin (skills available in user scope).

**Rule: Save reusable templates + design system docs for cross-page reuse.**
**Why:** User said "kalau bisa dibuat template style UI bisa di pakai" — wants pattern reuse across pages.
**How to apply:** Save Elementor templates (IDs 4675/4677/4679/4681), maintain `design-system/DESIGN-SYSTEM.md` + `design-system/sx-design-system.css` files for paste-into-Custom-CSS workflow.
