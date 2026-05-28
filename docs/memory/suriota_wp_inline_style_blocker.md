---
name: WP Customizer Inline Style Block Conflicts
description: Persistent inline <style> in suriota.com page HEAD overrides sx- design with !important — must be cleaned manually in WP Admin Customizer
type: project
originSessionId: 587198fb-6cea-4b87-a692-d8a6e5ea6255
---
**Why:** Live page HTML contains an inline `<style>` block (NOT from Elementor MCP) that injects `!important` rules for all 4 service pages, forcing OLD design tokens that conflict with sx- design system. Source is likely WP Admin → Appearance → Customize → Additional CSS, or a plugin.

**How to apply:** When refactoring service pages, expect visual chaos from these overrides unless cleaned. Override with higher specificity using `html body` prefix in page-level Custom CSS, OR ask user to manually delete the inline CSS in Customizer.

## What the Inline Block Forces

```css
/* Forces Poppins on ALL headings (kills Plus Jakarta Sans) */
h1, h2, h3, h4, h5, h6, .elementor-heading-title {
  font-family: 'Poppins', sans-serif !important;
}

/* Hero gradient #17505D → #0C2F38 on each service page (dark teal) */
/* Hero button bg #16A34A green (kills brand teal) */
/* Mid heading bg #FFFBEB (Electrical amber-tint) / #EEF2FF (Auto indigo-tint) /
   #F0F9FF (WT cyan-tint) / #ECFDF5 (RE green-tint) — CHAOTIC color mix */
/* H2 text color #1E293B (kills #0E3942) */
```

## My v3 Override Strategy

Use `html body` prefix to win specificity (0,0,3,2 vs inline 0,0,3,0) — both with `!important`:

```css
html body .elementor-37 .elementor-element-XXX .elementor-heading-title { ... !important; }
```

This works AT CSS LEVEL but the inline overrides remain in DOM forever unless manually cleaned.

## Permanent Fix (Manual — User Action Required)

1. **WP Admin → Appearance → Customize → Additional CSS** — check for block:
   ```
   /* === PAGE 37: ELECTRICAL — Amber Accent === */
   /* === PAGE 35: AUTOMATION — Indigo Accent === */
   /* === PAGE 945: WATER TREATMENT — Sky Blue Accent === */
   /* === PAGE 39: RENEWABLE ENERGY — Emerald Accent === */
   /* Force Poppins on all headings */
   ```
   Delete entire block.

2. **Or check active plugins** — could be from page builder addon / SEO plugin / theme customization that injects CSS.

## Verification

After cleaning, fetch live page and grep for #1E293B, #16A34A, #FFFBEB, Poppins,sans-serif in the page HTML. If 0 occurrences = cleaned.

## Other Inline CSS Issues Encountered (Same Project)
- `line-height:1.3px` bug on Elementor heading widgets (caused overlap on mobile) — fixed by changing to `em` unit
- Theme `.entry-title` H1 still in DOM (hidden via CSS `display:none`) — creates dual-H1 SEO issue. Set `hide_title:yes` via update-page-settings; theme may or may not respect.
