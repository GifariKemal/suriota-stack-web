---
name: feedback-sticky-nav-interpretation
description: "User wants \"sticky nav follows scroll\" = always-visible, NOT Medium-style hide-on-scroll-down"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 632eaef5-07d2-4ba1-8394-c8327af57fa1
---

When Gifari says "navbar ikut turun saat scroll" / "header ikut scroll" / "stick" / "follow", he means **always-visible fixed/sticky header** that stays pinned to the top of the viewport at every scroll position.

**Why:** I initially misinterpreted "ikut turun" as the Medium/Stripe smart-sticky pattern (hide on scroll-down, show on scroll-up). User corrected: "saya scroll down gk ikut turun tuh navbar header" — meaning they saw the navbar hiding and considered that a bug.

**How to apply:**
- For SURIOTA: snippet 5640 v3 uses `position: fixed; top: 0` with auto body padding-top sync, no hide animation
- If user ever explicitly asks for "hide on scroll down, show on scroll up" or names patterns like "Headroom" / "smart sticky" / "auto-hide nav", THEN implement the smart-hide variant
- Default assumption for any sticky nav request: ALWAYS visible

[[suriota_active_snippets]]
