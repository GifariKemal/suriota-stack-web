# SURIOTA Pillar Pages — Modern Industrial Editorial v2 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Apply Modern Industrial Editorial v2 visual design system to the 5 newly-launched pillar pages (EN/ID/ZH = 15 posts total) without touching any other page or sitewide asset.

**Architecture:** Per-page Elementor Custom CSS with `body.page-id-NNNN` scoping + new HTML widgets inserted into each pillar page's `_elementor_data`. One canonical CSS module authored locally, applied per-pillar with accent variable overrides. Backup-before-mutate for every post.

**Tech Stack:** WordPress REST API (auth: Application Password), Elementor `_elementor_data` JSON manipulation, vanilla CSS Custom Properties + IntersectionObserver JS, Python 3 for tooling, Playwright for visual + a11y verification.

**Spec:** `docs/superpowers/specs/2026-05-24-pillar-styling-design.md`

---

## Scope Lock (Reaffirmed)

**TOUCH ONLY:** posts 5554, 5555, 5556, 5557, 5558 (EN), 5566, 5567, 5568, 5569, 5570 (ID), 5571, 5572, 5573, 5574, 5575 (ZH).

**NEVER TOUCH:** any other post; theme files; sitewide snippets (5153/5186/5411/5447/5498/5511/5515/5524/5528/5599); WP Customizer; global Elementor settings/kit; Polylang/AIOSEO settings.

Every WP REST mutation MUST target one of the 15 allowed post IDs. The apply script asserts this — see Task 0.5.

---

## File Structure

### Created files (local repo)

```
design-system/
  sx-pillar-v2.tokens.css         # CSS variables (base + per-pillar overrides)
  sx-pillar-v2.components.css     # 10 component styles
  sx-pillar-v2.motion.js          # IntersectionObserver + counter
  components/
    p1-hero.html                  # Pillar 1 hero widget
    p1-capabilities.html
    p1-tech.html
    p1-industries.html
    p1-stats.html
    p1-process.html
    p1-cases.html
    p1-faq.html
    p1-cta.html
    p2-hero.html ... p2-cta.html  # Pillar 2 set
    p3-hero.html ... p3-cta.html  # Pillar 3 set (light hero variant)
    p4-hero.html ... p4-cta.html  # Pillar 4 set (incl. p4-nav.html)
    p4-nav.html                   # Sticky in-page nav (P4 only)
    p5-hero.html ... p5-cta.html  # Pillar 5 set
  README.md                        # Reuse guide

backups/pillars/
  5554-2026-05-24.json … 5575-2026-05-24.json   # _elementor_data + meta snapshots

tools/py/
  pillar_env.py                    # Load credentials from .env, sanity check
  pillar_backup.py                 # Backup _elementor_data + custom CSS
  pillar_apply_css.py              # Apply Custom CSS to a pillar page
  pillar_insert_widget.py          # Insert HTML widget into _elementor_data
  pillar_verify.py                 # Fetch live page + grep sentinel
  pillar_snapshot.py               # Playwright screenshot (desktop + mobile)
  pillar_a11y.py                   # Playwright + axe-core a11y audit

audit/pillar-v2-snapshots/
  before/                          # Pre-mutation screenshots
  after/                            # Post-mutation screenshots
  a11y/                             # axe-core JSON reports
```

### Modified files (live WordPress, via REST only)

Only these WordPress entities are mutated; nothing else:
- `wp/v2/pages/{id}` — meta `_elementor_data` (insert widgets) + meta `_elementor_page_settings.custom_css` (per-page CSS)
- That's it. No options, no plugins, no other CPTs.

---

## Phase 0 — Setup & Backup (zero production mutations)

### Task 0.1: Bootstrap directories and `.env`

**Files:**
- Create: `design-system/components/`
- Create: `backups/pillars/`
- Create: `audit/pillar-v2-snapshots/before/`
- Create: `audit/pillar-v2-snapshots/after/`
- Create: `audit/pillar-v2-snapshots/a11y/`
- Create: `.env.example`

- [ ] **Step 1: Create directories**

```bash
mkdir -p design-system/components backups/pillars audit/pillar-v2-snapshots/before audit/pillar-v2-snapshots/after audit/pillar-v2-snapshots/a11y
```

- [ ] **Step 2: Create `.env.example`**

```bash
cat > .env.example <<'EOF'
# Suriota WP REST — Application Password (NOT regular login)
# Generate at: https://suriota.com/wp-admin/profile.php → Application Passwords
WP_BASE=https://suriota.com
WP_USER=admin
WP_APP_PASS=xxxx xxxx xxxx xxxx xxxx xxxx
EOF
```

- [ ] **Step 3: Verify `.env` exists with real credentials**

If `.env` does not exist, copy from `.env.example` and ask user to paste their `claude-mcp` App Password.

```bash
test -f .env || echo "MISSING — copy .env.example and fill in"
```

- [ ] **Step 4: Add to `.gitignore` if not already**

```bash
grep -qxF '.env' .gitignore || echo '.env' >> .gitignore
```

- [ ] **Step 5: Commit scaffolding**

```bash
git add design-system/ backups/pillars/.gitkeep audit/pillar-v2-snapshots/ .env.example .gitignore
git commit -m "chore(pillars): scaffold dirs + env example"
```

---

### Task 0.2: WP REST auth helper

**Files:**
- Create: `tools/py/pillar_env.py`

- [ ] **Step 1: Author `pillar_env.py`**

```python
"""Auth + constants for pillar tooling. Hard-locks allowed post IDs."""
from __future__ import annotations
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def _load_env() -> None:
    env_file = ROOT / ".env"
    if not env_file.exists():
        sys.exit("[pillar_env] .env not found at repo root")
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())

_load_env()

WP_BASE = os.environ["WP_BASE"].rstrip("/")
WP_USER = os.environ["WP_USER"]
WP_APP_PASS = os.environ["WP_APP_PASS"]
AUTH = (WP_USER, WP_APP_PASS)

# Hard scope lock — every mutation script imports this set
ALLOWED_POST_IDS: frozenset[int] = frozenset({
    5554, 5555, 5556, 5557, 5558,   # EN
    5566, 5567, 5568, 5569, 5570,   # ID
    5571, 5572, 5573, 5574, 5575,   # ZH
})

PILLAR_OF: dict[int, int] = {
    5554: 1, 5566: 1, 5571: 1,
    5555: 2, 5567: 2, 5572: 2,
    5556: 3, 5568: 3, 5573: 3,
    5557: 4, 5569: 4, 5574: 4,
    5558: 5, 5570: 5, 5575: 5,
}

def assert_allowed(post_id: int) -> None:
    if post_id not in ALLOWED_POST_IDS:
        sys.exit(f"[pillar_env] REFUSE: post_id {post_id} is OUT OF SCOPE")
```

- [ ] **Step 2: Smoke test auth**

```bash
python -c "
import requests
from tools.py.pillar_env import AUTH, WP_BASE
r = requests.get(f'{WP_BASE}/wp-json/wp/v2/users/me', auth=AUTH, timeout=20)
print(r.status_code, r.json().get('name'))
"
```

Expected: `200 admin` (or display name). If 401, get fresh App Password.

- [ ] **Step 3: Commit**

```bash
git add tools/py/pillar_env.py
git commit -m "feat(pillars): wp rest auth helper + scope lock"
```

---

### Task 0.3: Backup script

**Files:**
- Create: `tools/py/pillar_backup.py`

- [ ] **Step 1: Author the backup script**

```python
"""Backup _elementor_data and Custom CSS for one pillar post to JSON."""
from __future__ import annotations
import json
import sys
from datetime import date
from pathlib import Path

import requests

from pillar_env import AUTH, ROOT, WP_BASE, assert_allowed


def backup(post_id: int) -> Path:
    assert_allowed(post_id)
    url = f"{WP_BASE}/wp-json/wp/v2/pages/{post_id}?context=edit"
    r = requests.get(url, auth=AUTH, timeout=30)
    r.raise_for_status()
    data = r.json()

    snapshot = {
        "post_id": post_id,
        "slug": data.get("slug"),
        "title": data.get("title", {}).get("raw"),
        "status": data.get("status"),
        "_elementor_data": data.get("meta", {}).get("_elementor_data"),
        "_elementor_page_settings": data.get("meta", {}).get("_elementor_page_settings"),
        "fetched_at": date.today().isoformat(),
    }

    out = ROOT / "backups" / "pillars" / f"{post_id}-{date.today().isoformat()}.json"
    out.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python tools/py/pillar_backup.py <post_id> [<post_id> ...]")
    for pid in sys.argv[1:]:
        path = backup(int(pid))
        print(f"OK  {pid} -> {path.relative_to(ROOT)}")
```

- [ ] **Step 2: Backup one post (5554) to verify**

```bash
python tools/py/pillar_backup.py 5554
ls -la backups/pillars/5554-*.json
```

Expected: file `5554-2026-05-24.json` exists, >5KB.

- [ ] **Step 3: Backup all 15 pillar posts**

```bash
python tools/py/pillar_backup.py 5554 5555 5556 5557 5558 5566 5567 5568 5569 5570 5571 5572 5573 5574 5575
```

Expected: 15 OK lines.

- [ ] **Step 4: Verify each backup is non-empty**

```bash
for f in backups/pillars/*-2026-05-24.json; do
  size=$(wc -c < "$f")
  echo "$f  $size bytes"
  test "$size" -gt 1000 || echo "WARN: $f looks empty"
done
```

- [ ] **Step 5: Commit backups**

```bash
git add backups/pillars/*.json tools/py/pillar_backup.py
git commit -m "chore(pillars): backup _elementor_data for 15 posts (pre-styling)"
```

---

## Phase A — Pilot Pillar 1 EN (post 5554)

### Task A.1: Author `sx-pillar-v2.tokens.css`

**Files:**
- Create: `design-system/sx-pillar-v2.tokens.css`

- [ ] **Step 1: Write the file**

```css
/*!
 * sx-pillar-v2.tokens.css — Modern Industrial Editorial v2
 * Scoped to 15 pillar posts only. Do NOT add to sitewide CSS.
 */

/* Base tokens — inherited from sx-design-system v1 also exist sitewide.
   These are additive v2 tokens for pillar pages only. */
:root {
  /* Overlays */
  --sxp-overlay-deep: rgba(14, 57, 66, 0.92);
  --sxp-overlay-veil: rgba(14, 57, 66, 0.42);

  /* Textures */
  --sxp-dot-color:  rgba(255, 255, 255, 0.06);
  --sxp-grid-color: rgba(255, 255, 255, 0.04);

  /* Elevation */
  --sxp-elev-1: 0 1px  0  rgba(14, 57, 66, 0.05);
  --sxp-elev-2: 0 8px  24px rgba(14, 57, 66, 0.08);
  --sxp-elev-3: 0 16px 40px rgba(14, 57, 66, 0.12);

  /* Motion */
  --sxp-ease:      cubic-bezier(0.22, 1, 0.36, 1);
  --sxp-dur-fast:  180ms;
  --sxp-dur-base:  320ms;
  --sxp-dur-slow:  640ms;

  /* Defaults — overridden per pillar via body.page-id-* */
  --sxp-accent:      #205B69;
  --sxp-accent-deep: #0E3942;
  --sxp-accent-soft: rgba(32, 91, 105, 0.12);
}

/* Per-pillar accent */
body.page-id-5554, body.page-id-5566, body.page-id-5571 {
  --sxp-accent: #205B69;             /* P1 teal */
  --sxp-accent-deep: #0E3942;
  --sxp-accent-soft: rgba(32, 91, 105, 0.12);
}
body.page-id-5555, body.page-id-5567, body.page-id-5572 {
  --sxp-accent: #3C7D47;             /* P2 green */
  --sxp-accent-deep: #1E4A26;
  --sxp-accent-soft: rgba(60, 125, 71, 0.12);
}
body.page-id-5556, body.page-id-5568, body.page-id-5573 {
  --sxp-accent: #C8851F;             /* P3 amber */
  --sxp-accent-deep: #6E480F;
  --sxp-accent-soft: rgba(200, 133, 31, 0.12);
}
body.page-id-5557, body.page-id-5569, body.page-id-5574 {
  --sxp-accent: #205B69;             /* P4 teal */
  --sxp-accent-deep: #0E3942;
  --sxp-accent-soft: rgba(32, 91, 105, 0.12);
}
body.page-id-5558, body.page-id-5570, body.page-id-5575 {
  --sxp-accent: #0E3942;             /* P5 deep teal */
  --sxp-accent-deep: #07242C;
  --sxp-accent-soft: rgba(14, 57, 66, 0.12);
  --sxp-accent-aux:  #C8851F;        /* amber secondary */
}
```

- [ ] **Step 2: Lint manually — confirm no `line-height` in `px`**

```bash
grep -nE 'line-height:[[:space:]]*[0-9]+px' design-system/sx-pillar-v2.tokens.css
```

Expected: empty output (no matches).

- [ ] **Step 3: Commit**

```bash
git add design-system/sx-pillar-v2.tokens.css
git commit -m "feat(pillars): v2 tokens + per-pillar accent variables"
```

---

### Task A.2: Author `sx-pillar-v2.components.css`

**Files:**
- Create: `design-system/sx-pillar-v2.components.css`

- [ ] **Step 1: Write the file**

```css
/*!
 * sx-pillar-v2.components.css — 10 components, pillar-scoped.
 */

/* ===== Helpers ===== */
.sxp-section { padding: clamp(40px, 6vw, 72px) clamp(16px, 4vw, 24px); }
.sxp-wrap    { max-width: 1180px; margin: 0 auto; }
.sxp-eyebrow {
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-size: 0.8125rem; font-weight: 500;
  letter-spacing: 0.08em; text-transform: uppercase;
  color: var(--sxp-accent);
  margin: 0 0 12px;
}
.sxp-h1 {
  font-family: "Plus Jakarta Sans", system-ui, sans-serif;
  font-weight: 700;
  font-size: clamp(2.5rem, 5vw, 4.5rem);
  letter-spacing: -0.02em;
  line-height: 1.05em;
  margin: 0;
}
.sxp-h2 {
  font-family: "Plus Jakarta Sans", system-ui, sans-serif;
  font-weight: 700;
  font-size: clamp(2rem, 3.5vw, 3rem);
  letter-spacing: -0.01em;
  line-height: 1.1em;
  margin: 0 0 16px;
}
.sxp-h3 {
  font-family: "Plus Jakarta Sans", system-ui, sans-serif;
  font-weight: 600;
  font-size: clamp(1.25rem, 1.8vw, 1.75rem);
  letter-spacing: -0.005em;
  line-height: 1.2em;
  margin: 0 0 12px;
}
.sxp-body {
  font-family: "Poppins", system-ui, sans-serif;
  font-size: 1rem; line-height: 1.6em;
  color: #1F2D33;
}
.sxp-body-l { font-size: 1.1875rem; line-height: 1.6em; }
.sxp-mono {
  font-family: "IBM Plex Mono", ui-monospace, monospace;
  font-feature-settings: "tnum" 1;
}

/* ===== 3.1 Hero ===== */
.sxp-hero {
  position: relative;
  min-height: 88vh;
  display: grid; place-items: center;
  padding: clamp(80px, 12vw, 140px) clamp(16px, 4vw, 24px) clamp(48px, 6vw, 72px);
  background: linear-gradient(135deg, var(--sxp-accent) 0%, var(--sxp-accent-deep) 100%);
  color: #fff;
  overflow: hidden;
}
.sxp-hero--light {
  background: #FAFBFC;
  color: #1F2D33;
}
.sxp-hero::before {
  content: "";
  position: absolute; inset: 0;
  background-image: radial-gradient(circle at 1px 1px, var(--sxp-dot-color) 1px, transparent 0);
  background-size: 24px 24px;
  pointer-events: none;
}
.sxp-hero--light::before { background-image: radial-gradient(circle at 1px 1px, rgba(14,57,66,0.06) 1px, transparent 0); }
.sxp-hero__inner { position: relative; max-width: 920px; width: 100%; }
.sxp-hero__eyebrow {
  font-family: "IBM Plex Mono", monospace; font-size: 0.8125rem;
  letter-spacing: 0.08em; text-transform: uppercase;
  color: #fff; opacity: 0.85;
}
.sxp-hero--light .sxp-hero__eyebrow { color: var(--sxp-accent); opacity: 1; }
.sxp-hero__title {
  font-family: "Plus Jakarta Sans", sans-serif; font-weight: 700;
  font-size: clamp(2.5rem, 5vw, 4.5rem); letter-spacing: -0.02em;
  line-height: 1.05em; margin: 14px 0 22px;
}
.sxp-hero__sub {
  font-family: "Poppins", sans-serif; font-size: clamp(1rem, 1.6vw, 1.25rem);
  line-height: 1.6em; max-width: 60ch; opacity: 0.92;
  margin: 0 0 32px;
}
.sxp-hero__ctas { display: flex; gap: 12px; flex-wrap: wrap; }
.sxp-cta {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 14px 22px; border-radius: 999px;
  font-family: "Plus Jakarta Sans", sans-serif; font-weight: 600;
  font-size: 0.95rem;
  text-decoration: none; cursor: pointer;
  transition: transform var(--sxp-dur-fast) var(--sxp-ease), box-shadow var(--sxp-dur-fast) var(--sxp-ease);
}
.sxp-cta:hover { transform: translateY(-2px); box-shadow: var(--sxp-elev-2); }
.sxp-cta--primary {
  background: #fff; color: var(--sxp-accent-deep);
}
.sxp-cta--ghost {
  background: transparent; color: #fff;
  border: 1px solid rgba(255,255,255,0.4);
}
.sxp-hero--light .sxp-cta--primary {
  background: var(--sxp-accent-deep); color: #fff;
}
.sxp-hero--light .sxp-cta--ghost {
  color: var(--sxp-accent-deep);
  border-color: rgba(14,57,66,0.25);
}
.sxp-hero__pmark {
  position: absolute; left: clamp(16px, 4vw, 24px); bottom: 24px;
  font-family: "IBM Plex Mono", monospace; font-size: 0.75rem;
  letter-spacing: 0.08em; text-transform: uppercase;
  opacity: 0.6;
}

/* ===== 3.2 In-page sticky nav (P4) ===== */
.sxp-nav {
  position: sticky; top: 80px; z-index: 40;
  background: rgba(250,251,252,0.92);
  backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
  border-bottom: 1px solid #E8ECEE;
  padding: 12px clamp(16px, 4vw, 24px);
}
.sxp-nav__list {
  display: flex; gap: 24px; max-width: 1180px; margin: 0 auto;
  list-style: none; padding: 0;
  overflow-x: auto; scroll-snap-type: x mandatory;
}
.sxp-nav__link {
  font-family: "IBM Plex Mono", monospace; font-size: 0.8125rem;
  text-transform: uppercase; letter-spacing: 0.06em;
  color: #5B6F75; text-decoration: none; white-space: nowrap;
  scroll-snap-align: start;
  padding: 6px 0; border-bottom: 2px solid transparent;
}
.sxp-nav__link.is-active,
.sxp-nav__link:hover {
  color: var(--sxp-accent);
  border-bottom-color: var(--sxp-accent);
}

/* ===== 3.3 Capabilities asymmetric grid ===== */
.sxp-cap__grid {
  display: grid; gap: 20px;
  grid-template-columns: repeat(12, 1fr);
}
.sxp-cap__card {
  grid-column: span 12;
  background: #FAFBFC; border: 1px solid #E8ECEE; border-radius: 10px;
  padding: clamp(20px, 2vw, 28px);
  position: relative; overflow: hidden;
  transition: transform var(--sxp-dur-base) var(--sxp-ease), box-shadow var(--sxp-dur-base) var(--sxp-ease);
}
.sxp-cap__card::before {
  content: ""; position: absolute; left: 0; top: 0; bottom: 0;
  width: 0; background: var(--sxp-accent);
  transition: width var(--sxp-dur-base) var(--sxp-ease);
}
.sxp-cap__card:hover { transform: translateY(-4px); box-shadow: var(--sxp-elev-2); }
.sxp-cap__card:hover::before { width: 3px; }
.sxp-cap__num {
  font-family: "IBM Plex Mono", monospace; font-weight: 600;
  font-size: 0.875rem; color: #C8851F;
  letter-spacing: 0.06em; text-transform: uppercase;
  margin: 0 0 12px;
}
.sxp-cap__title { margin: 0 0 8px; }
.sxp-cap__body  { color: #5B6F75; margin: 0 0 14px; }
.sxp-cap__chips { display: flex; flex-wrap: wrap; gap: 6px; }
.sxp-cap__chip {
  font-family: "IBM Plex Mono", monospace; font-size: 0.75rem;
  padding: 4px 10px; border-radius: 999px;
  background: var(--sxp-accent-soft); color: var(--sxp-accent);
}
@media (min-width: 880px) {
  .sxp-cap__card:nth-child(1) { grid-column: span 7; }
  .sxp-cap__card:nth-child(2) { grid-column: span 5; }
  .sxp-cap__card:nth-child(3) { grid-column: span 5; }
  .sxp-cap__card:nth-child(4) { grid-column: span 7; }
}

/* ===== 3.4 Tech strip ===== */
.sxp-tech {
  border-top: 1px solid #E8ECEE; border-bottom: 1px solid #E8ECEE;
  padding: 18px clamp(16px, 4vw, 24px);
}
.sxp-tech__row {
  max-width: 1180px; margin: 0 auto;
  display: flex; gap: 24px; flex-wrap: wrap; align-items: center;
  font-family: "IBM Plex Mono", monospace; font-size: 0.8125rem;
  color: #5B6F75; text-transform: uppercase; letter-spacing: 0.06em;
}
.sxp-tech__row > span { display: inline-flex; align-items: center; gap: 12px; }
.sxp-tech__row > span::after {
  content: ""; width: 4px; height: 4px; border-radius: 50%;
  background: var(--sxp-accent); display: inline-block; margin-left: 12px;
}
.sxp-tech__row > span:last-child::after { display: none; }

/* ===== 3.5 Industries grid ===== */
.sxp-ind__grid {
  display: grid; gap: 14px;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
}
.sxp-ind__cell {
  background: #FAFBFC; border: 1px solid #E8ECEE; border-radius: 10px;
  padding: 22px; text-align: center;
  transition: transform var(--sxp-dur-fast) var(--sxp-ease), border-color var(--sxp-dur-fast) var(--sxp-ease);
}
.sxp-ind__cell:hover {
  border-color: var(--sxp-accent);
  transform: translateY(-2px);
}
.sxp-ind__cell svg { width: 28px; height: 28px; stroke: var(--sxp-accent); margin: 0 0 10px; transition: transform var(--sxp-dur-fast) var(--sxp-ease); }
.sxp-ind__cell:hover svg { transform: rotate(5deg); }
.sxp-ind__cell span {
  display: block; font-family: "IBM Plex Mono", monospace;
  font-size: 0.8125rem; text-transform: uppercase; letter-spacing: 0.04em;
  color: #1F2D33;
}

/* ===== 3.6 Stats strip ===== */
.sxp-stats {
  background: #FAFBFC; border-top: 1px solid #E8ECEE; border-bottom: 1px solid #E8ECEE;
}
.sxp-stats__grid {
  display: grid; gap: 18px;
  grid-template-columns: repeat(2, 1fr);
}
@media (min-width: 768px) {
  .sxp-stats__grid { grid-template-columns: repeat(4, 1fr); }
}
.sxp-stats__cell { text-align: left; padding: 14px 8px; }
.sxp-stats__num {
  font-family: "IBM Plex Mono", monospace; font-weight: 600;
  font-size: clamp(2.5rem, 5vw, 4rem); line-height: 1em;
  color: var(--sxp-accent-deep); font-feature-settings: "tnum" 1;
}
.sxp-stats__num .sxp-plus { color: #C8851F; margin-left: 2px; }
.sxp-stats__label {
  font-family: "IBM Plex Mono", monospace; font-size: 0.8125rem;
  letter-spacing: 0.06em; text-transform: uppercase;
  color: #5B6F75; margin-top: 6px;
}

/* ===== 3.7 Process timeline ===== */
.sxp-proc__list {
  display: grid; gap: 18px;
  grid-template-columns: 1fr;
  counter-reset: sxp-step;
}
@media (min-width: 880px) {
  .sxp-proc__list { grid-template-columns: repeat(5, 1fr); }
}
.sxp-proc__step { position: relative; padding-left: 0; }
.sxp-proc__num {
  display: inline-flex; align-items: center; justify-content: center;
  width: 36px; height: 36px; border-radius: 50%;
  background: #fff; border: 1px solid var(--sxp-accent);
  color: var(--sxp-accent);
  font-family: "IBM Plex Mono", monospace; font-weight: 600;
  margin: 0 0 12px;
}
.sxp-proc__title { font-family: "Plus Jakarta Sans", sans-serif; font-weight: 600; margin: 0 0 4px; }
.sxp-proc__desc  { color: #5B6F75; font-size: 0.95rem; margin: 0; }

/* ===== 3.8 Case studies ===== */
.sxp-case {
  display: grid; gap: 22px;
  grid-template-columns: 1fr;
}
@media (min-width: 880px) {
  .sxp-case { grid-template-columns: 1fr 1fr; }
}
.sxp-case__card {
  background: #FAFBFC; border: 1px solid #E8ECEE; border-radius: 10px;
  padding: clamp(18px, 2vw, 24px);
}
.sxp-case__metric {
  font-family: "IBM Plex Mono", monospace; font-weight: 600;
  font-size: clamp(2rem, 3vw, 3rem); line-height: 1em;
  color: var(--sxp-accent-deep); margin: 0 0 6px;
}
.sxp-case__metric-label {
  font-family: "IBM Plex Mono", monospace; font-size: 0.75rem;
  text-transform: uppercase; color: #5B6F75; letter-spacing: 0.06em;
  margin: 0 0 14px;
}
.sxp-case__more {
  display: inline-flex; align-items: center; gap: 6px;
  color: var(--sxp-accent); text-decoration: none;
  font-family: "IBM Plex Mono", monospace; font-size: 0.875rem; text-transform: uppercase;
  transition: gap var(--sxp-dur-fast) var(--sxp-ease);
}
.sxp-case__more:hover { gap: 12px; }

/* ===== 3.9 FAQ accordion ===== */
.sxp-faq { border-top: 1px solid #E8ECEE; }
.sxp-faq__item { border-bottom: 1px solid #E8ECEE; }
.sxp-faq__btn {
  width: 100%; text-align: left; background: none; border: 0; cursor: pointer;
  padding: 20px 0; display: flex; align-items: center; justify-content: space-between;
  font-family: "Plus Jakarta Sans", sans-serif; font-weight: 600; font-size: 1.05rem;
  color: #1F2D33;
}
.sxp-faq__btn[aria-expanded="true"] .sxp-faq__icon { transform: rotate(45deg); }
.sxp-faq__icon {
  width: 18px; height: 18px;
  display: inline-block; position: relative;
  transition: transform var(--sxp-dur-base) var(--sxp-ease);
}
.sxp-faq__icon::before, .sxp-faq__icon::after {
  content: ""; position: absolute; background: var(--sxp-accent);
}
.sxp-faq__icon::before { left: 0; right: 0; top: 50%; height: 2px; transform: translateY(-50%); }
.sxp-faq__icon::after  { top: 0; bottom: 0; left: 50%; width: 2px; transform: translateX(-50%); }
.sxp-faq__panel {
  max-height: 0; overflow: hidden;
  transition: max-height var(--sxp-dur-base) var(--sxp-ease), opacity var(--sxp-dur-base) var(--sxp-ease);
  opacity: 0;
}
.sxp-faq__btn[aria-expanded="true"] + .sxp-faq__panel {
  max-height: 1000px; opacity: 1; padding-bottom: 18px;
}

/* ===== 3.10 Final CTA ===== */
.sxp-cta-block {
  position: relative;
  background: linear-gradient(135deg, var(--sxp-accent) 0%, var(--sxp-accent-deep) 100%);
  color: #fff;
  padding: clamp(40px, 6vw, 72px) clamp(16px, 4vw, 24px);
  border-radius: 12px; overflow: hidden;
}
.sxp-cta-block::before {
  content: ""; position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, #C8851F 0%, #205B69 50%, #3C7D47 100%);
}
.sxp-cta-block__inner { max-width: 720px; margin: 0 auto; text-align: center; }
.sxp-cta-block__eyebrow {
  color: #C8851F; font-family: "IBM Plex Mono", monospace;
  font-size: 0.8125rem; text-transform: uppercase; letter-spacing: 0.08em;
  margin: 0 0 10px;
}
.sxp-cta-block__title { color: #fff; margin: 0 0 14px; }
.sxp-cta-block__body  { opacity: 0.92; margin: 0 0 24px; max-width: 60ch; margin-left: auto; margin-right: auto; }
.sxp-cta-block__ctas  { display: inline-flex; gap: 12px; flex-wrap: wrap; justify-content: center; }
.sxp-cta-block__wa {
  background: #075E54; color: #fff; /* dark teal WA per critical rule — NEVER #25D366 */
  display: inline-flex; align-items: center; gap: 8px;
  padding: 14px 22px; border-radius: 999px;
  font-family: "Plus Jakarta Sans", sans-serif; font-weight: 600;
  text-decoration: none;
  transition: transform var(--sxp-dur-fast) var(--sxp-ease), box-shadow var(--sxp-dur-fast) var(--sxp-ease);
}
.sxp-cta-block__wa:hover { transform: translateY(-2px); box-shadow: var(--sxp-elev-2); }
.sxp-cta-block__trust {
  font-family: "IBM Plex Mono", monospace; font-size: 0.75rem;
  text-transform: uppercase; letter-spacing: 0.06em;
  opacity: 0.7; margin: 22px 0 0;
}

/* ===== Reveal animation ===== */
.sxp-reveal { opacity: 0; transform: translateY(12px); transition: opacity 400ms var(--sxp-ease), transform 400ms var(--sxp-ease); }
.sxp-reveal.is-visible { opacity: 1; transform: none; }

/* ===== Focus visible ===== */
.sxp-cta:focus-visible,
.sxp-faq__btn:focus-visible,
.sxp-nav__link:focus-visible,
.sxp-case__more:focus-visible {
  outline: 2px solid var(--sxp-accent);
  outline-offset: 2px;
}

/* ===== Reduce motion ===== */
@media (prefers-reduced-motion: reduce) {
  .sxp-reveal { opacity: 1 !important; transform: none !important; transition: none !important; }
  .sxp-faq__panel { transition: none !important; }
  .sxp-cap__card, .sxp-ind__cell, .sxp-cta, .sxp-cta-block__wa { transition: none !important; }
}
```

- [ ] **Step 2: Sanity check — no `line-height: ##px` for headings**

```bash
grep -nE 'line-height:[[:space:]]*[0-9]+px' design-system/sx-pillar-v2.components.css
```

Expected: empty.

- [ ] **Step 3: Commit**

```bash
git add design-system/sx-pillar-v2.components.css
git commit -m "feat(pillars): v2 components stylesheet (10 components)"
```

---

### Task A.3: Author motion JS

**Files:**
- Create: `design-system/sx-pillar-v2.motion.js`

- [ ] **Step 1: Write the file**

```javascript
/*!
 * sx-pillar-v2.motion.js — IntersectionObserver reveals, counters, FAQ toggle.
 * Scoped to pillar pages. Respects prefers-reduced-motion.
 */
(function () {
  'use strict';
  if (window.__sxpInit) return; window.__sxpInit = true;

  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ===== Reveal animation =====
  var io;
  if ('IntersectionObserver' in window && !reduce) {
    io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add('is-visible');
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
  }

  function bindReveals() {
    document.querySelectorAll('.sxp-reveal').forEach(function (el, i) {
      if (reduce || !io) { el.classList.add('is-visible'); return; }
      el.style.transitionDelay = (i % 5) * 80 + 'ms';
      io.observe(el);
    });
  }

  // ===== Counter animation =====
  function easeOutCubic(t) { return 1 - Math.pow(1 - t, 3); }
  function animateCount(el) {
    var target = parseInt(el.getAttribute('data-target') || '0', 10);
    if (!target) return;
    if (reduce) { el.textContent = target; return; }
    var dur = 1600, start = performance.now();
    function tick(now) {
      var t = Math.min(1, (now - start) / dur);
      el.textContent = Math.round(target * easeOutCubic(t));
      if (t < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }
  function bindCounters() {
    var nodes = document.querySelectorAll('.sxp-stats__num[data-target]');
    if (!nodes.length) return;
    if (reduce || !('IntersectionObserver' in window)) {
      nodes.forEach(function (n) { n.textContent = n.getAttribute('data-target'); });
      return;
    }
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { animateCount(e.target); co.unobserve(e.target); }
      });
    }, { threshold: 0.4 });
    nodes.forEach(function (n) { co.observe(n); });
  }

  // ===== FAQ toggle =====
  function bindFaq() {
    document.querySelectorAll('.sxp-faq__btn').forEach(function (btn) {
      btn.addEventListener('click', function () {
        var open = btn.getAttribute('aria-expanded') === 'true';
        btn.setAttribute('aria-expanded', open ? 'false' : 'true');
      });
    });
  }

  // ===== Sticky nav active-state (P4) =====
  function bindStickyNav() {
    var nav = document.querySelector('.sxp-nav');
    if (!nav) return;
    var links = nav.querySelectorAll('.sxp-nav__link');
    var sections = Array.from(links).map(function (a) {
      return document.querySelector(a.getAttribute('href'));
    }).filter(Boolean);
    if (!sections.length) return;
    var nio = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          links.forEach(function (l) { l.classList.remove('is-active'); });
          var match = nav.querySelector('a[href="#' + e.target.id + '"]');
          if (match) match.classList.add('is-active');
        }
      });
    }, { threshold: 0.3, rootMargin: '-30% 0px -50% 0px' });
    sections.forEach(function (s) { nio.observe(s); });
  }

  // Boot
  function init() { bindReveals(); bindCounters(); bindFaq(); bindStickyNav(); }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else { init(); }
})();
```

- [ ] **Step 2: Commit**

```bash
git add design-system/sx-pillar-v2.motion.js
git commit -m "feat(pillars): v2 motion js (reveals, counters, faq, sticky nav)"
```

---

### Task A.4: Author Pillar 1 hero widget HTML

**Files:**
- Create: `design-system/components/p1-hero.html`

- [ ] **Step 1: Write the file**

```html
<section class="sxp-hero sxp-reveal" aria-labelledby="p1-hero-title">
  <div class="sxp-hero__inner">
    <p class="sxp-hero__eyebrow">01 — INDUSTRIAL IOT / SYSTEM INTEGRATION</p>
    <h1 class="sxp-hero__title" id="p1-hero-title">Bridge legacy and modern systems into a single source of truth.</h1>
    <p class="sxp-hero__sub">Industrial IoT deployment, SCADA / MES / ERP integration, and edge-to-cloud connectivity engineered for manufacturing, oil &amp; gas, and shipyard operations across Indonesia.</p>
    <div class="sxp-hero__ctas">
      <a class="sxp-cta sxp-cta--primary" href="/contact/">Free Consultation
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true" focusable="false"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
      </a>
      <a class="sxp-cta sxp-cta--ghost" href="#sxp-capabilities">View Capabilities</a>
    </div>
  </div>
  <span class="sxp-hero__pmark">P1 / SERVICES</span>
</section>
```

- [ ] **Step 2: Commit**

```bash
git add design-system/components/p1-hero.html
git commit -m "feat(pillars): p1 hero widget html"
```

---

### Task A.5: Author Pillar 1 remaining widgets

**Files:**
- Create: `design-system/components/p1-capabilities.html`
- Create: `design-system/components/p1-tech.html`
- Create: `design-system/components/p1-industries.html`
- Create: `design-system/components/p1-stats.html`
- Create: `design-system/components/p1-process.html`
- Create: `design-system/components/p1-cases.html`
- Create: `design-system/components/p1-faq.html`
- Create: `design-system/components/p1-cta.html`
- Modify: includes motion `<script>` tag inline at end of `p1-cta.html`

- [ ] **Step 1: Write `p1-capabilities.html`**

```html
<section class="sxp-section" id="sxp-capabilities">
  <div class="sxp-wrap">
    <p class="sxp-eyebrow">CORE CAPABILITIES</p>
    <h2 class="sxp-h2 sxp-reveal">What we deliver in IoT and system integration.</h2>
    <div class="sxp-cap__grid">
      <article class="sxp-cap__card sxp-reveal">
        <p class="sxp-cap__num">01 — IIOT DEPLOYMENT</p>
        <h3 class="sxp-h3 sxp-cap__title">Industrial IoT Deployment</h3>
        <p class="sxp-body sxp-cap__body">Modbus RTU/TCP-to-MQTT gateways, edge compute on SRT-MGATE-1210, AWS IoT Core and private-cloud dashboards across manufacturing, oil &amp; gas, and shipyard sites.</p>
        <div class="sxp-cap__chips"><span class="sxp-cap__chip">Modbus</span><span class="sxp-cap__chip">MQTT</span><span class="sxp-cap__chip">AWS IoT</span></div>
      </article>
      <article class="sxp-cap__card sxp-reveal">
        <p class="sxp-cap__num">02 — SYSTEM INTEGRATION</p>
        <h3 class="sxp-h3 sxp-cap__title">SCADA / MES / ERP</h3>
        <p class="sxp-body sxp-cap__body">OT/IT convergence with secure protocol translation between Modbus, OPC UA, BACnet, and modern message brokers.</p>
        <div class="sxp-cap__chips"><span class="sxp-cap__chip">OPC UA</span><span class="sxp-cap__chip">BACnet</span><span class="sxp-cap__chip">OT/IT</span></div>
      </article>
      <article class="sxp-cap__card sxp-reveal">
        <p class="sxp-cap__num">03 — CLOUD MONITORING</p>
        <h3 class="sxp-h3 sxp-cap__title">Cloud Monitoring &amp; Analytics</h3>
        <p class="sxp-body sxp-cap__body">SURGE platform integration, real-time dashboards, alerting, and historical analytics on top of your live operations data.</p>
        <div class="sxp-cap__chips"><span class="sxp-cap__chip">SURGE</span><span class="sxp-cap__chip">Grafana</span></div>
      </article>
      <article class="sxp-cap__card sxp-reveal">
        <p class="sxp-cap__num">04 — LEGACY MODERNIZATION</p>
        <h3 class="sxp-h3 sxp-cap__title">Legacy System Modernization</h3>
        <p class="sxp-body sxp-cap__body">Retrofit existing equipment with minimal downtime through phased migration plans and protocol-bridging.</p>
        <div class="sxp-cap__chips"><span class="sxp-cap__chip">Retrofit</span><span class="sxp-cap__chip">Phased</span></div>
      </article>
    </div>
  </div>
</section>
```

- [ ] **Step 2: Write `p1-tech.html`**

```html
<section class="sxp-tech">
  <div class="sxp-tech__row sxp-reveal">
    <span>Modbus RTU/TCP</span><span>MQTT</span><span>OPC UA</span><span>BACnet</span><span>LoRaWAN</span><span>AWS IoT</span><span>Azure IoT</span><span>SRT-MGATE-1210</span><span>SURGE</span><span>Grafana</span>
  </div>
</section>
```

- [ ] **Step 3: Write `p1-industries.html`**

```html
<section class="sxp-section">
  <div class="sxp-wrap">
    <p class="sxp-eyebrow">INDUSTRIES WE SERVE</p>
    <h2 class="sxp-h2 sxp-reveal">Where we deploy.</h2>
    <div class="sxp-ind__grid sxp-reveal">
      <div class="sxp-ind__cell"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M3 21h18M5 21V8l7-5 7 5v13M9 21v-6h6v6"/></svg><span>Manufacturing</span></div>
      <div class="sxp-ind__cell"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M4 22V8l8-5 8 5v14M9 22v-7h6v7"/></svg><span>Oil &amp; Gas</span></div>
      <div class="sxp-ind__cell"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M2 20l10-14 10 14M6 20l6-8 6 8"/></svg><span>Shipyard &amp; Marine</span></div>
      <div class="sxp-ind__cell"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M12 3v18M3 12h18"/></svg><span>Water Treatment</span></div>
      <div class="sxp-ind__cell"><svg viewBox="0 0 24 24" fill="none" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3"/></svg><span>Renewable Energy</span></div>
    </div>
  </div>
</section>
```

- [ ] **Step 4: Write `p1-stats.html`**

```html
<section class="sxp-stats sxp-section">
  <div class="sxp-wrap sxp-stats__grid">
    <div class="sxp-stats__cell sxp-reveal">
      <p class="sxp-stats__num" data-target="64">0<span class="sxp-plus">+</span></p>
      <p class="sxp-stats__label">Projects delivered</p>
    </div>
    <div class="sxp-stats__cell sxp-reveal">
      <p class="sxp-stats__num" data-target="6">0</p>
      <p class="sxp-stats__label">In-house products</p>
    </div>
    <div class="sxp-stats__cell sxp-reveal">
      <p class="sxp-stats__num" data-target="25">0<span class="sxp-plus">+</span></p>
      <p class="sxp-stats__label">Engineers</p>
    </div>
    <div class="sxp-stats__cell sxp-reveal">
      <p class="sxp-stats__num" data-target="5">0</p>
      <p class="sxp-stats__label">Core service pillars</p>
    </div>
  </div>
</section>
```

- [ ] **Step 5: Write `p1-process.html`**

```html
<section class="sxp-section">
  <div class="sxp-wrap">
    <p class="sxp-eyebrow">OUR PROCESS</p>
    <h2 class="sxp-h2 sxp-reveal">From discovery to support.</h2>
    <ol class="sxp-proc__list sxp-reveal">
      <li class="sxp-proc__step"><span class="sxp-proc__num">01</span><p class="sxp-proc__title">Discovery</p><p class="sxp-proc__desc">Site walkthrough, system inventory, stakeholder interviews.</p></li>
      <li class="sxp-proc__step"><span class="sxp-proc__num">02</span><p class="sxp-proc__title">Assessment</p><p class="sxp-proc__desc">Protocol mapping, gap analysis, ROI model.</p></li>
      <li class="sxp-proc__step"><span class="sxp-proc__num">03</span><p class="sxp-proc__title">Design</p><p class="sxp-proc__desc">Integration architecture, security framework, phasing plan.</p></li>
      <li class="sxp-proc__step"><span class="sxp-proc__num">04</span><p class="sxp-proc__title">Implementation</p><p class="sxp-proc__desc">Phased deployment with minimal downtime; OAT/SAT testing.</p></li>
      <li class="sxp-proc__step"><span class="sxp-proc__num">05</span><p class="sxp-proc__title">Support</p><p class="sxp-proc__desc">Lifecycle support, remote monitoring, preventive maintenance.</p></li>
    </ol>
  </div>
</section>
```

- [ ] **Step 6: Write `p1-cases.html`**

```html
<section class="sxp-section">
  <div class="sxp-wrap">
    <p class="sxp-eyebrow">CASE STUDIES</p>
    <h2 class="sxp-h2 sxp-reveal">Selected work.</h2>
    <div class="sxp-case sxp-reveal">
      <article class="sxp-case__card">
        <p class="sxp-case__metric">-38<span class="sxp-plus">%</span></p>
        <p class="sxp-case__metric-label">Unplanned downtime</p>
        <h3 class="sxp-h3">Manufacturing IIoT retrofit, Batam</h3>
        <p class="sxp-body">Modbus-to-MQTT gateway deployment across 12 lines, cloud dashboard, anomaly alerts.</p>
        <a class="sxp-case__more" href="/portfolio/">Read case <span aria-hidden="true">→</span></a>
      </article>
      <article class="sxp-case__card">
        <p class="sxp-case__metric">5x</p>
        <p class="sxp-case__metric-label">Faster RCA</p>
        <h3 class="sxp-h3">Oil &amp; Gas terminal SCADA integration</h3>
        <p class="sxp-body">OPC UA bridge between legacy SCADA and modern historian; unified dashboard for ops + maintenance.</p>
        <a class="sxp-case__more" href="/portfolio/">Read case <span aria-hidden="true">→</span></a>
      </article>
    </div>
  </div>
</section>
```

- [ ] **Step 7: Write `p1-faq.html`**

```html
<section class="sxp-section">
  <div class="sxp-wrap">
    <p class="sxp-eyebrow">FAQ</p>
    <h2 class="sxp-h2 sxp-reveal">Common questions.</h2>
    <div class="sxp-faq sxp-reveal">
      <div class="sxp-faq__item">
        <button class="sxp-faq__btn" aria-expanded="false" aria-controls="p1-faq-1">
          <span>How long does a typical IoT integration take?</span><span class="sxp-faq__icon" aria-hidden="true"></span>
        </button>
        <div class="sxp-faq__panel" id="p1-faq-1" role="region">
          <p class="sxp-body">A pilot of 2–5 lines runs 6–10 weeks; phased rollout follows in 3-month sprints depending on site complexity.</p>
        </div>
      </div>
      <div class="sxp-faq__item">
        <button class="sxp-faq__btn" aria-expanded="false" aria-controls="p1-faq-2">
          <span>Do you support legacy PLCs older than 10 years?</span><span class="sxp-faq__icon" aria-hidden="true"></span>
        </button>
        <div class="sxp-faq__panel" id="p1-faq-2" role="region">
          <p class="sxp-body">Yes — most Modbus-capable controllers, including S7-300/400, Allen-Bradley SLC/MicroLogix, and Mitsubishi FX.</p>
        </div>
      </div>
      <div class="sxp-faq__item">
        <button class="sxp-faq__btn" aria-expanded="false" aria-controls="p1-faq-3">
          <span>Where is the data hosted?</span><span class="sxp-faq__icon" aria-hidden="true"></span>
        </button>
        <div class="sxp-faq__panel" id="p1-faq-3" role="region">
          <p class="sxp-body">Customer choice: AWS Indonesia region, Azure Southeast Asia, on-premise, or hybrid.</p>
        </div>
      </div>
      <div class="sxp-faq__item">
        <button class="sxp-faq__btn" aria-expanded="false" aria-controls="p1-faq-4">
          <span>What about cybersecurity?</span><span class="sxp-faq__icon" aria-hidden="true"></span>
        </button>
        <div class="sxp-faq__panel" id="p1-faq-4" role="region">
          <p class="sxp-body">Defense-in-depth: segmented OT network, TLS to broker, signed firmware, audit logs, role-based access.</p>
        </div>
      </div>
    </div>
  </div>
</section>
```

- [ ] **Step 8: Write `p1-cta.html` (includes motion script inline at end)**

```html
<section class="sxp-section">
  <div class="sxp-wrap">
    <div class="sxp-cta-block sxp-reveal">
      <div class="sxp-cta-block__inner">
        <p class="sxp-cta-block__eyebrow">GET STARTED</p>
        <h2 class="sxp-cta-block__title sxp-h2">Ready to integrate your systems?</h2>
        <p class="sxp-cta-block__body sxp-body-l">Talk to our integration team. We map your current state, scope a pilot, and ship within 90 days.</p>
        <div class="sxp-cta-block__ctas">
          <a class="sxp-cta sxp-cta--primary" href="/contact/">Free Consultation
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true" focusable="false"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
          </a>
          <a class="sxp-cta-block__wa" href="https://wa.me/6285835672476" target="_blank" rel="noopener">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true" focusable="false"><path d="M.057 24l1.687-6.163a11.867 11.867 0 0 1-1.587-5.946C.16 5.335 5.495 0 12.05 0a11.81 11.81 0 0 1 8.413 3.488 11.824 11.824 0 0 1 3.48 8.414c-.003 6.557-5.338 11.892-11.893 11.892a11.9 11.9 0 0 1-5.688-1.448L.057 24zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981z"/></svg>
            WhatsApp
          </a>
        </div>
        <p class="sxp-cta-block__trust">64+ projects · 25+ engineers · Local Batam team, global standards</p>
      </div>
    </div>
  </div>
</section>
<script>/* Motion JS will be loaded via Custom CSS injection — see Task A.8 step 4 */</script>
```

- [ ] **Step 9: Commit all P1 widgets**

```bash
git add design-system/components/p1-*.html
git commit -m "feat(pillars): p1 widget html templates (8 sections)"
```

---

### Task A.6: Apply CSS + motion script to post 5554

**Files:**
- Create: `tools/py/pillar_apply_css.py`

- [ ] **Step 1: Author apply script**

```python
"""Apply per-page Custom CSS (tokens + components) plus motion JS as <style>/<script> wrapper to a pillar post.

Custom CSS in Elementor page-settings only loads CSS, not JS. We bundle motion JS inside an HTML widget at the bottom of the page (see pillar_insert_widget.py task). This script only handles CSS.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

import requests

from pillar_env import AUTH, ROOT, WP_BASE, assert_allowed

CSS_FILES = [
    ROOT / "design-system" / "sx-pillar-v2.tokens.css",
    ROOT / "design-system" / "sx-pillar-v2.components.css",
]

def build_css_bundle() -> str:
    return "\n\n".join(p.read_text(encoding="utf-8") for p in CSS_FILES)

def apply(post_id: int) -> None:
    assert_allowed(post_id)
    css = build_css_bundle()
    url = f"{WP_BASE}/wp-json/wp/v2/pages/{post_id}"
    payload = {
        "meta": {
            "_elementor_page_settings": {"custom_css": css},
        }
    }
    r = requests.post(url, auth=AUTH, json=payload, timeout=30)
    if r.status_code >= 300:
        sys.exit(f"FAIL {post_id}: {r.status_code} {r.text[:200]}")
    print(f"OK CSS applied to {post_id} ({len(css)} chars)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python tools/py/pillar_apply_css.py <post_id> [<post_id> ...]")
    for pid in sys.argv[1:]:
        apply(int(pid))
```

- [ ] **Step 2: Apply CSS to post 5554 only**

```bash
python tools/py/pillar_apply_css.py 5554
```

Expected: `OK CSS applied to 5554 (≈20000 chars)`

- [ ] **Step 3: Verify CSS reached the page (HTTP fetch + grep)**

```bash
curl -s https://suriota.com/industrial-iot-system-integration/ | grep -c 'sxp-hero'
```

Expected: ≥1 (CSS class names appear in inline `<style>` Elementor injects).

- [ ] **Step 4: Commit script**

```bash
git add tools/py/pillar_apply_css.py
git commit -m "feat(pillars): apply v2 css to pillar post"
```

---

### Task A.7: Widget insertion script

**Files:**
- Create: `tools/py/pillar_insert_widget.py`

- [ ] **Step 1: Author the insert script**

```python
"""Insert HTML widget(s) into a pillar post's _elementor_data.

Elementor data is a JSON list of sections; each section has columns; each column has widgets.
We insert a new section at the END containing one html widget with the supplied HTML.
Each new section is tagged via _sxpId so we can identify, re-run idempotently, and rollback.
"""
from __future__ import annotations
import json
import sys
import uuid
from pathlib import Path

import requests

from pillar_env import AUTH, ROOT, WP_BASE, assert_allowed


def _new_id() -> str:
    return uuid.uuid4().hex[:7]


def _wrap(sxp_id: str, html: str) -> dict:
    return {
        "id": _new_id(),
        "elType": "section",
        "settings": {"structure": "10", "_sxpId": sxp_id},
        "elements": [{
            "id": _new_id(),
            "elType": "column",
            "settings": {"_column_size": 100},
            "elements": [{
                "id": _new_id(),
                "elType": "widget",
                "widgetType": "html",
                "settings": {"html": html, "_sxpId": sxp_id},
            }],
        }],
        "isInner": False,
    }


def _strip_existing(elements: list, sxp_id: str) -> list:
    out = []
    for sec in elements:
        if sec.get("settings", {}).get("_sxpId") == sxp_id:
            continue
        out.append(sec)
    return out


def insert(post_id: int, sxp_id: str, html_file: Path) -> None:
    assert_allowed(post_id)
    html = html_file.read_text(encoding="utf-8")
    url = f"{WP_BASE}/wp-json/wp/v2/pages/{post_id}?context=edit"
    r = requests.get(url, auth=AUTH, timeout=30)
    r.raise_for_status()
    data_raw = r.json().get("meta", {}).get("_elementor_data") or "[]"
    elements = json.loads(data_raw) if isinstance(data_raw, str) else data_raw

    elements = _strip_existing(elements, sxp_id)
    elements.append(_wrap(sxp_id, html))

    payload = {"meta": {"_elementor_data": json.dumps(elements, ensure_ascii=False)}}
    r2 = requests.post(f"{WP_BASE}/wp-json/wp/v2/pages/{post_id}", auth=AUTH, json=payload, timeout=30)
    if r2.status_code >= 300:
        sys.exit(f"FAIL insert {post_id}/{sxp_id}: {r2.status_code} {r2.text[:200]}")
    print(f"OK inserted {sxp_id} into {post_id} (now {len(elements)} sections)")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit("usage: python tools/py/pillar_insert_widget.py <post_id> <sxp_id> <html_file>")
    insert(int(sys.argv[1]), sys.argv[2], Path(sys.argv[3]))
```

- [ ] **Step 2: Insert P1 hero into 5554 (idempotent — re-runs replace)**

```bash
python tools/py/pillar_insert_widget.py 5554 p1-hero design-system/components/p1-hero.html
```

Expected: `OK inserted p1-hero into 5554 (now N sections)`

- [ ] **Step 3: Insert remaining 7 P1 widgets in order**

```bash
for w in capabilities tech industries stats process cases faq cta; do
  python tools/py/pillar_insert_widget.py 5554 p1-$w design-system/components/p1-$w.html
done
```

Expected: 8 OK lines total.

- [ ] **Step 4: Add motion JS as a final HTML widget**

```bash
python -c "
from pathlib import Path
js = Path('design-system/sx-pillar-v2.motion.js').read_text(encoding='utf-8')
Path('design-system/components/p1-motion.html').write_text('<script>\n' + js + '\n</script>\n', encoding='utf-8')
print('wrote p1-motion.html')
"
python tools/py/pillar_insert_widget.py 5554 p1-motion design-system/components/p1-motion.html
```

Expected: `OK inserted p1-motion into 5554`.

- [ ] **Step 5: Verify live**

```bash
curl -s https://suriota.com/industrial-iot-system-integration/ > /tmp/p1-live.html
grep -c 'sxp-hero__title'          /tmp/p1-live.html   # expect ≥1
grep -c 'sxp-cap__card'            /tmp/p1-live.html   # expect ≥4
grep -c 'sxp-stats__num'           /tmp/p1-live.html   # expect ≥4
grep -c 'data-target="64"'          /tmp/p1-live.html   # expect ≥1
grep -c 'wa.me/6285835672476'       /tmp/p1-live.html   # expect ≥1
```

Expected: all greps return ≥1.

- [ ] **Step 6: Commit script + motion wrapper helper**

```bash
git add tools/py/pillar_insert_widget.py design-system/components/p1-motion.html
git commit -m "feat(pillars): widget insert script + motion wrapper"
```

---

### Task A.8: Visual + a11y verification of pilot

**Files:**
- Create: `tools/py/pillar_snapshot.py`
- Create: `tools/py/pillar_a11y.py`
- Output: `audit/pillar-v2-snapshots/after/5554-desktop.png`
- Output: `audit/pillar-v2-snapshots/after/5554-mobile.png`
- Output: `audit/pillar-v2-snapshots/a11y/5554.json`

- [ ] **Step 1: Author screenshot script (Playwright)**

```python
"""Take desktop + mobile screenshots of a pillar URL."""
from __future__ import annotations
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

from pillar_env import ROOT, assert_allowed, PILLAR_OF

URL_BY_ID = {
    5554: "https://suriota.com/industrial-iot-system-integration/",
    5555: "https://suriota.com/ai-industrial-analytics/",
    5556: "https://suriota.com/digital-transformation-consulting/",
    5557: "https://suriota.com/industrial-engineering-automation/",
    5558: "https://suriota.com/surge-saas-platform/",
    5566: "https://suriota.com/id/iot-industri-integrasi-sistem/",
    5567: "https://suriota.com/id/ai-analitik-industri/",
    5568: "https://suriota.com/id/konsultasi-transformasi-digital/",
    5569: "https://suriota.com/id/teknik-industri-otomasi/",
    5570: "https://suriota.com/id/platform-saas-surge/",
    5571: "https://suriota.com/zh/gongye-wulianwang-jicheng/",
    5572: "https://suriota.com/zh/ai-gongye-fenxi/",
    5573: "https://suriota.com/zh/shuzihua-zhuanxing-zixun/",
    5574: "https://suriota.com/zh/gongye-gongcheng-zidonghua/",
    5575: "https://suriota.com/zh/surge-saas-pingtai/",
}


def snap(post_id: int, label: str) -> None:
    assert_allowed(post_id)
    url = URL_BY_ID[post_id]
    out_dir = ROOT / "audit" / "pillar-v2-snapshots" / label
    out_dir.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for vp, name in [({"width": 1440, "height": 900}, "desktop"),
                         ({"width": 390,  "height": 844}, "mobile")]:
            ctx = browser.new_context(viewport=vp, device_scale_factor=2)
            page = ctx.new_page()
            page.goto(url, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(800)
            page.screenshot(path=str(out_dir / f"{post_id}-{name}.png"), full_page=True)
            ctx.close()
        browser.close()
    print(f"OK snapshots saved for {post_id} → {label}/")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("usage: python tools/py/pillar_snapshot.py <post_id> <before|after>")
    snap(int(sys.argv[1]), sys.argv[2])
```

- [ ] **Step 2: Run snapshot for 5554 (after)**

```bash
python tools/py/pillar_snapshot.py 5554 after
```

Expected: `OK snapshots saved for 5554 → after/`. Files:
- `audit/pillar-v2-snapshots/after/5554-desktop.png`
- `audit/pillar-v2-snapshots/after/5554-mobile.png`

- [ ] **Step 3: Author a11y script (axe-core injected via Playwright)**

```python
"""Run axe-core a11y audit on a pillar URL and dump JSON report."""
from __future__ import annotations
import json
import sys
import urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright

from pillar_env import ROOT, assert_allowed
from pillar_snapshot import URL_BY_ID

AXE_CDN = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.9.1/axe.min.js"


def audit(post_id: int) -> Path:
    assert_allowed(post_id)
    url = URL_BY_ID[post_id]
    axe = urllib.request.urlopen(AXE_CDN, timeout=20).read().decode("utf-8")
    out = ROOT / "audit" / "pillar-v2-snapshots" / "a11y" / f"{post_id}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(url, wait_until="networkidle", timeout=60000)
        page.add_script_tag(content=axe)
        result = page.evaluate("axe.run()")
        ctx.close(); browser.close()
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    violations = result.get("violations", [])
    crit = sum(1 for v in violations if v.get("impact") in ("critical", "serious"))
    print(f"{post_id}: {len(violations)} violations ({crit} serious/critical) -> {out.relative_to(ROOT)}")
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python tools/py/pillar_a11y.py <post_id>")
    audit(int(sys.argv[1]))
```

- [ ] **Step 4: Run a11y audit on 5554**

```bash
python tools/py/pillar_a11y.py 5554
```

Expected: output reports zero serious/critical violations. If non-zero, capture the impacted selectors and fix the source HTML/CSS before proceeding.

- [ ] **Step 5: Commit verification tooling + artifacts**

```bash
git add tools/py/pillar_snapshot.py tools/py/pillar_a11y.py audit/pillar-v2-snapshots/after/5554-*.png audit/pillar-v2-snapshots/a11y/5554.json
git commit -m "feat(pillars): visual + a11y verification (pilot 5554)"
```

---

## Phase B — Apply Pillars 2-5 EN

For each pillar 2..5, repeat the widget-authoring + insertion pattern from Phase A. CSS is already applied via `pillar_apply_css.py` to those pages too.

### Task B.1: Author + insert Pillar 2 widgets (5555)

**Files:**
- Create: `design-system/components/p2-hero.html` … `p2-cta.html` (8 files, mirror P1 structure with P2 copy)

- [ ] **Step 1: Author `p2-hero.html`**

```html
<section class="sxp-hero sxp-reveal" aria-labelledby="p2-hero-title">
  <div class="sxp-hero__inner">
    <p class="sxp-hero__eyebrow">02 — AI / INDUSTRIAL ANALYTICS</p>
    <h1 class="sxp-hero__title" id="p2-hero-title">Turn industrial data into competitive advantage.</h1>
    <p class="sxp-hero__sub">Predictive maintenance, computer-vision QC, anomaly detection, OEE and energy analytics — production-grade AI deployed on your plant data.</p>
    <div class="sxp-hero__ctas">
      <a class="sxp-cta sxp-cta--primary" href="/contact/">Free Consultation
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true" focusable="false"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
      </a>
      <a class="sxp-cta sxp-cta--ghost" href="#sxp-capabilities">View Capabilities</a>
    </div>
  </div>
  <span class="sxp-hero__pmark">P2 / SERVICES</span>
</section>
```

- [ ] **Step 1b: Author remaining 7 P2 widget files**

For `p2-capabilities.html` ... `p2-cta.html`, copy the corresponding `p1-*.html` file as a template and replace text content using spec section 5.2 (AI & Industrial Analytics). Capability cards: `Predictive Maintenance / Computer Vision QC / Anomaly Detection / OEE & Production Analytics`. Tech chips for P2: `TensorFlow`, `PyTorch`, `scikit-learn`, `InfluxDB`, `Edge AI`, `Power BI`. Industries: Manufacturing, Oil & Gas, Power & Utilities (3 cells — adjust grid auto-fit handles it). FAQs from spec 5.2 list. CTA wording: `Ready to deploy AI in your plant?` and trust line metrics. CSS classes and structural HTML stay identical to P1.

- [ ] **Step 2: Apply CSS + insert all P2 widgets**

```bash
python tools/py/pillar_apply_css.py 5555
for w in hero capabilities tech industries stats process cases faq cta; do
  python tools/py/pillar_insert_widget.py 5555 p2-$w design-system/components/p2-$w.html
done
python -c "from pathlib import Path; js=Path('design-system/sx-pillar-v2.motion.js').read_text(encoding='utf-8'); Path('design-system/components/p2-motion.html').write_text('<script>\n'+js+'\n</script>\n', encoding='utf-8')"
python tools/py/pillar_insert_widget.py 5555 p2-motion design-system/components/p2-motion.html
```

- [ ] **Step 3: Verify + snapshot + a11y**

```bash
python tools/py/pillar_snapshot.py 5555 after
python tools/py/pillar_a11y.py 5555
```

Expected: zero serious/critical a11y violations.

- [ ] **Step 4: Commit**

```bash
git add design-system/components/p2-*.html audit/pillar-v2-snapshots/after/5555-*.png audit/pillar-v2-snapshots/a11y/5555.json
git commit -m "feat(pillars): apply v2 to p2 ai-industrial-analytics (5555)"
```

---

### Task B.2: Pillar 3 (5556) — LIGHT hero variant

**Files:**
- Create: `design-system/components/p3-hero.html` (uses `.sxp-hero--light` modifier)
- Create: `design-system/components/p3-capabilities.html` … `p3-cta.html`

- [ ] **Step 1: Author P3 hero with light variant**

```html
<section class="sxp-hero sxp-hero--light sxp-reveal" aria-labelledby="p3-hero-title">
  <div class="sxp-hero__inner">
    <p class="sxp-hero__eyebrow">03 — DIGITAL TRANSFORMATION CONSULTING</p>
    <h1 class="sxp-hero__title" id="p3-hero-title">From strategy to execution — your Industry 4.0 roadmap.</h1>
    <p class="sxp-hero__sub">Digital maturity assessment, OT/IT convergence strategy, technology selection, and change management for industrial leaders ready to scale.</p>
    <div class="sxp-hero__ctas">
      <a class="sxp-cta sxp-cta--primary" href="/contact/">Schedule Assessment
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true" focusable="false"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
      </a>
      <a class="sxp-cta sxp-cta--ghost" href="#sxp-capabilities">View Capabilities</a>
    </div>
  </div>
  <span class="sxp-hero__pmark">P3 / SERVICES</span>
</section>
```

- [ ] **Step 2: Author P3 remaining widgets (capabilities, process, deliverables, cases, faq, cta)**

Use spec section 5.3 (Digital Consulting) content. Capability cards: `Digital Maturity Assessment / Industry 4.0 Roadmap / OT/IT Convergence Strategy / Technology Selection / Change Management` (5 cards — adjust grid to wrap). Skip industries section for P3 (consulting is sector-agnostic).

- [ ] **Step 3: Apply + insert + verify**

```bash
python tools/py/pillar_apply_css.py 5556
for w in hero capabilities tech stats process cases faq cta; do
  python tools/py/pillar_insert_widget.py 5556 p3-$w design-system/components/p3-$w.html
done
python -c "from pathlib import Path; js=Path('design-system/sx-pillar-v2.motion.js').read_text(encoding='utf-8'); Path('design-system/components/p3-motion.html').write_text('<script>\n'+js+'\n</script>\n', encoding='utf-8')"
python tools/py/pillar_insert_widget.py 5556 p3-motion design-system/components/p3-motion.html
python tools/py/pillar_snapshot.py 5556 after
python tools/py/pillar_a11y.py 5556
```

- [ ] **Step 4: Commit**

```bash
git add design-system/components/p3-*.html audit/pillar-v2-snapshots/after/5556-*.png audit/pillar-v2-snapshots/a11y/5556.json
git commit -m "feat(pillars): apply v2 to p3 digital-transformation-consulting (5556, light hero)"
```

---

### Task B.3: Pillar 4 (5557) — INCLUDES sticky in-page nav

**Files:**
- Create: `design-system/components/p4-nav.html`
- Create: `design-system/components/p4-hero.html` … `p4-cta.html`

- [ ] **Step 1: Author sticky nav**

```html
<nav class="sxp-nav" aria-label="In-page navigation">
  <ul class="sxp-nav__list">
    <li><a class="sxp-nav__link" href="#automation">Automation</a></li>
    <li><a class="sxp-nav__link" href="#electrical">Electrical</a></li>
    <li><a class="sxp-nav__link" href="#renewable-energy">Renewable Energy</a></li>
    <li><a class="sxp-nav__link" href="#water-treatment">Water Treatment</a></li>
  </ul>
</nav>
```

- [ ] **Step 2a: Author `p4-hero.html`**

```html
<section class="sxp-hero sxp-reveal" aria-labelledby="p4-hero-title">
  <div class="sxp-hero__inner">
    <p class="sxp-hero__eyebrow">04 — INDUSTRIAL ENGINEERING / AUTOMATION</p>
    <h1 class="sxp-hero__title" id="p4-hero-title">End-to-end industrial engineering, from design to commissioning.</h1>
    <p class="sxp-hero__sub">Automation, electrical, renewable energy, and water treatment engineering — one partner across the physical infrastructure of your plant.</p>
    <div class="sxp-hero__ctas">
      <a class="sxp-cta sxp-cta--primary" href="/contact/">Free Consultation
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true" focusable="false"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
      </a>
      <a class="sxp-cta sxp-cta--ghost" href="#automation">View Capabilities</a>
    </div>
  </div>
  <span class="sxp-hero__pmark">P4 / SERVICES</span>
</section>
```

- [ ] **Step 2b: Author 4 sub-service blocks (`p4-sub-automation.html`, `p4-sub-electrical.html`, `p4-sub-renewable.html`, `p4-sub-water.html`)**

Example — `p4-sub-automation.html`:

```html
<section class="sxp-section" id="automation">
  <div class="sxp-wrap">
    <p class="sxp-eyebrow">AUTOMATION</p>
    <h2 class="sxp-h2 sxp-reveal">PLC, SCADA, and IIoT-ready integration.</h2>
    <div class="sxp-cap__grid">
      <article class="sxp-cap__card sxp-reveal">
        <p class="sxp-cap__num">01 — PLC &amp; SCADA</p>
        <h3 class="sxp-h3 sxp-cap__title">Programming &amp; HMI</h3>
        <p class="sxp-body sxp-cap__body">Siemens, Allen-Bradley, Schneider, Mitsubishi. Recipe management, batch control, HMI development.</p>
      </article>
      <article class="sxp-cap__card sxp-reveal">
        <p class="sxp-cap__num">02 — IIOT INTEGRATION</p>
        <h3 class="sxp-h3 sxp-cap__title">Modbus gateway &amp; cloud</h3>
        <p class="sxp-body sxp-cap__body">Edge-to-cloud connectivity using SRT-MGATE-1210 and SURGE.</p>
      </article>
      <article class="sxp-cap__card sxp-reveal">
        <p class="sxp-cap__num">03 — INDUSTRY 4.0 UPGRADES</p>
        <h3 class="sxp-h3 sxp-cap__title">Modernization roadmap</h3>
        <p class="sxp-body sxp-cap__body">Legacy PLC modernization, MES integration, digital twin preparation.</p>
      </article>
      <article class="sxp-cap__card sxp-reveal">
        <p class="sxp-cap__num">04 — LIFECYCLE SUPPORT</p>
        <h3 class="sxp-h3 sxp-cap__title">Maintain &amp; scale</h3>
        <p class="sxp-body sxp-cap__body">Preventive maintenance, 24/7 remote support, spare parts management.</p>
      </article>
    </div>
  </div>
</section>
```

Repeat the same structure for `p4-sub-electrical.html` (id=`electrical`, capabilities from spec 5.4 Electrical block), `p4-sub-renewable.html` (id=`renewable-energy`), `p4-sub-water.html` (id=`water-treatment`). Each `<section id="...">` matches the sticky nav anchor exactly.

- [ ] **Step 3: Apply + insert (note: nav goes RIGHT AFTER hero, then 4 sub-sections, then shared sections)**

```bash
python tools/py/pillar_apply_css.py 5557
python tools/py/pillar_insert_widget.py 5557 p4-hero  design-system/components/p4-hero.html
python tools/py/pillar_insert_widget.py 5557 p4-nav   design-system/components/p4-nav.html
for sub in automation electrical renewable water; do
  python tools/py/pillar_insert_widget.py 5557 p4-sub-$sub design-system/components/p4-sub-$sub.html
done
for w in tech stats process cases faq cta; do
  python tools/py/pillar_insert_widget.py 5557 p4-$w design-system/components/p4-$w.html
done
python -c "from pathlib import Path; js=Path('design-system/sx-pillar-v2.motion.js').read_text(encoding='utf-8'); Path('design-system/components/p4-motion.html').write_text('<script>\n'+js+'\n</script>\n', encoding='utf-8')"
python tools/py/pillar_insert_widget.py 5557 p4-motion design-system/components/p4-motion.html
```

- [ ] **Step 4: Verify nav scroll behavior**

```bash
python tools/py/pillar_snapshot.py 5557 after
python tools/py/pillar_a11y.py 5557
```

Manual: open `/industrial-engineering-automation/` in a browser, scroll, verify the sticky nav appears and active link updates as sections enter the viewport.

- [ ] **Step 5: Commit**

```bash
git add design-system/components/p4-*.html audit/pillar-v2-snapshots/after/5557-*.png audit/pillar-v2-snapshots/a11y/5557.json
git commit -m "feat(pillars): apply v2 to p4 industrial-engineering-automation (5557, sticky nav + 4 sub-sections)"
```

---

### Task B.4: Pillar 5 (5558) — SURGE SaaS

**Files:**
- Create: `design-system/components/p5-hero.html` … `p5-cta.html`

- [ ] **Step 1: Author `p5-hero.html`**

```html
<section class="sxp-hero sxp-reveal" aria-labelledby="p5-hero-title">
  <div class="sxp-hero__inner">
    <p class="sxp-hero__eyebrow">05 — SURGE / SAAS PLATFORM</p>
    <h1 class="sxp-hero__title" id="p5-hero-title">Cloud-native monitoring for industrial operations.</h1>
    <p class="sxp-hero__sub">Multi-tenant SURGE platform for energy, vessel tracking, water analytics, and SPARING KLHK compliance — purpose-built for industrial scale.</p>
    <div class="sxp-hero__ctas">
      <a class="sxp-cta sxp-cta--primary" href="/contact/">Request Demo
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true" focusable="false"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
      </a>
      <a class="sxp-cta sxp-cta--ghost" href="#sxp-capabilities">View Modules</a>
    </div>
  </div>
  <span class="sxp-hero__pmark">P5 / PRODUCT</span>
</section>
```

- [ ] **Step 1b: Author remaining P5 widgets**

`p5-capabilities.html` = 4 platform modules from spec 5.5 (SURGE-Energy Mapping, SURGE-Vessel Tracking, SURGE-Water Analytics, Wastewater Logger) in the same `.sxp-cap__grid` structure as P1.

`p5-features.html` = Platform features list using the `.sxp-cap__chips` chip pattern (Multi-tenant architecture, Mobile app, API for ERP, Alerting, Historical analytics).

`p5-deployment.html` = 3-up grid (Cloud-hosted, On-premise, Hybrid) using `.sxp-ind__grid` cells.

`p5-pricing.html`, `p5-cases.html`, `p5-faq.html`, `p5-cta.html` — same structure as P1 counterparts with spec 5.5 content. CTA H2 wording: `Start Your Free Trial`.

- [ ] **Step 2: Apply + insert + verify**

```bash
python tools/py/pillar_apply_css.py 5558
for w in hero capabilities features deployment pricing cases faq cta; do
  python tools/py/pillar_insert_widget.py 5558 p5-$w design-system/components/p5-$w.html
done
python -c "from pathlib import Path; js=Path('design-system/sx-pillar-v2.motion.js').read_text(encoding='utf-8'); Path('design-system/components/p5-motion.html').write_text('<script>\n'+js+'\n</script>\n', encoding='utf-8')"
python tools/py/pillar_insert_widget.py 5558 p5-motion design-system/components/p5-motion.html
python tools/py/pillar_snapshot.py 5558 after
python tools/py/pillar_a11y.py 5558
```

- [ ] **Step 3: Commit**

```bash
git add design-system/components/p5-*.html audit/pillar-v2-snapshots/after/5558-*.png audit/pillar-v2-snapshots/a11y/5558.json
git commit -m "feat(pillars): apply v2 to p5 surge-saas-platform (5558)"
```

---

## Phase C — Apply ID + ZH (10 pages)

### Task C.1: Translate widget HTML to ID and ZH

**Files:**
- Create: `design-system/components/id/p1-hero.html` … `p5-cta.html` (one translated set per pillar)
- Create: `design-system/components/zh/p1-hero.html` … `p5-cta.html`

- [ ] **Step 1: Translation source — use existing translated post content**

For each EN widget HTML, take the corresponding Indonesian or Chinese visible content from the existing published ID/ZH pillar pages (which are already content-translated per the validation report). Replace English copy in the HTML template with the existing translation. CSS classes, IDs, SVG, and structure stay identical.

For each pillar, fetch the live ID/ZH page text, then map paragraph-by-paragraph into the HTML widget template.

```bash
mkdir -p design-system/components/id design-system/components/zh
# Example: pull EN as template, edit copy for ID variant
cp design-system/components/p1-hero.html design-system/components/id/p1-hero.html
# Then edit the file to replace English with Indonesian copy from /id/iot-industri-integrasi-sistem/
```

- [ ] **Step 2: Verify SVG icons + classes preserved**

```bash
for f in design-system/components/id/*.html design-system/components/zh/*.html; do
  grep -c 'sxp-' "$f"   # expect ≥3 per file (CSS classes present)
done
```

- [ ] **Step 3: Commit translations**

```bash
git add design-system/components/id/ design-system/components/zh/
git commit -m "feat(pillars): id + zh translated widget html"
```

---

### Task C.2: Apply to 5 ID pages (5566-5570)

- [ ] **Step 1: Apply CSS to all ID pillars**

```bash
python tools/py/pillar_apply_css.py 5566 5567 5568 5569 5570
```

- [ ] **Step 2: Insert widgets for each ID pillar**

```bash
# P1 ID (5566)
for w in hero capabilities tech industries stats process cases faq cta; do
  python tools/py/pillar_insert_widget.py 5566 p1-$w design-system/components/id/p1-$w.html
done
# Insert motion
python tools/py/pillar_insert_widget.py 5566 p1-motion design-system/components/p1-motion.html

# Repeat the loop for 5567 (P2), 5568 (P3), 5569 (P4 incl. nav + sub-sections), 5570 (P5)
```

- [ ] **Step 3: Snapshot + a11y all 5 ID pages**

```bash
for pid in 5566 5567 5568 5569 5570; do
  python tools/py/pillar_snapshot.py $pid after
  python tools/py/pillar_a11y.py $pid
done
```

- [ ] **Step 4: Commit**

```bash
git add audit/pillar-v2-snapshots/after/556*.png audit/pillar-v2-snapshots/a11y/556*.json
git commit -m "feat(pillars): apply v2 to all id pillars (5566-5570)"
```

---

### Task C.3: Apply to 5 ZH pages (5571-5575)

- [ ] **Step 1: Apply CSS to all ZH pillars**

```bash
python tools/py/pillar_apply_css.py 5571 5572 5573 5574 5575
```

- [ ] **Step 2: Insert widgets**

Mirror C.2 loop for 5571-5575 using `design-system/components/zh/`.

- [ ] **Step 3: Snapshot + a11y**

```bash
for pid in 5571 5572 5573 5574 5575; do
  python tools/py/pillar_snapshot.py $pid after
  python tools/py/pillar_a11y.py $pid
done
```

- [ ] **Step 4: Commit**

```bash
git add audit/pillar-v2-snapshots/after/557*.png audit/pillar-v2-snapshots/a11y/557*.json
git commit -m "feat(pillars): apply v2 to all zh pillars (5571-5575)"
```

---

## Phase D — QA Pass

### Task D.1: Cross-pillar a11y rollup

- [ ] **Step 1: Aggregate a11y reports**

```bash
python - <<'PY'
import json, glob
totals = {}
for f in sorted(glob.glob("audit/pillar-v2-snapshots/a11y/*.json")):
    data = json.load(open(f, encoding="utf-8"))
    pid = f.split("/")[-1].split(".")[0]
    viols = data.get("violations", [])
    serious = [v for v in viols if v.get("impact") in ("serious", "critical")]
    totals[pid] = {"violations": len(viols), "serious_critical": len(serious)}
print(json.dumps(totals, indent=2))
PY
```

Expected: `serious_critical: 0` for every post.

- [ ] **Step 2: If any serious/critical violations, fix the widget HTML or CSS, re-insert, re-audit. Do not advance to Task D.2 until clean.**

---

### Task D.2: Design critique on pilot

- [ ] **Step 1: Invoke `design:design-critique` skill on the pilot URL**

Use the design plugin skill against `https://suriota.com/industrial-iot-system-integration/`. Capture critique notes in `audit/pillar-v2-snapshots/design-critique-pilot.md`.

- [ ] **Step 2: Apply any high-priority critique fixes back to the widget HTML / CSS, redeploy, re-snapshot.**

- [ ] **Step 3: Commit critique notes + fixes**

```bash
git add audit/pillar-v2-snapshots/design-critique-pilot.md
git commit -m "chore(pillars): design-critique notes for pilot (5554)"
```

---

### Task D.3: Mobile parity check

- [ ] **Step 1: For all 15 posts, verify mobile screenshot exists and renders correctly**

```bash
ls audit/pillar-v2-snapshots/after/*-mobile.png | wc -l
```

Expected: 15.

- [ ] **Step 2: Manual visual sweep**

Open each `-mobile.png` and confirm:
- Hero text doesn't overflow viewport
- Capability cards stack to single column
- Sticky nav (P4 only, 5557/5569/5574) horizontally scrolls
- Stats grid is 2-up on mobile
- FAQ items remain interactable (44px touch min)
- CTA buttons are full-width or properly wrapped, never cut off

If any failures, fix the responsive CSS in `sx-pillar-v2.components.css`, re-apply via `pillar_apply_css.py`, re-snapshot.

---

### Task D.4: Verify non-pillar pages untouched

- [ ] **Step 1: Spot-check 5 random non-pillar pages**

```bash
for url in https://suriota.com/ https://suriota.com/about-us/ https://suriota.com/automation/ https://suriota.com/portfolio/ https://suriota.com/surge-energy-mapping/; do
  echo "=== $url ==="
  curl -s "$url" | grep -c 'sxp-'   # expect 0 — sxp classes must NOT appear on non-pillar pages
done
```

Expected: each prints `0`.

- [ ] **Step 2: If any non-zero, scope was violated — investigate which step leaked styling and revert that step's mutation.**

---

### Task D.5: Final commit + summary report

**Files:**
- Create: `audit/pillar-v2-snapshots/SUMMARY.md`

- [ ] **Step 1: Write summary report**

```markdown
# Pillar v2 Styling — Summary Report
**Date:** 2026-05-24
**Posts touched:** 15 (5554-5558, 5566-5570, 5571-5575)
**Non-pillar pages mutated:** 0 (verified Task D.4)
**A11y status:** 0 serious/critical violations across all 15 posts
**Snapshots:** 30 (desktop + mobile per post) in audit/pillar-v2-snapshots/after/
**Local artifacts:** sx-pillar-v2.{tokens,components}.css + motion.js + components/ + tools/py/
**Rollback path:** restore _elementor_data from backups/pillars/*.json via WP REST POST
```

- [ ] **Step 2: Final commit**

```bash
git add audit/pillar-v2-snapshots/SUMMARY.md
git commit -m "docs(pillars): v2 rollout complete — 15 posts, 0 scope violations, 0 a11y serious"
```

---

## Rollback Recipe (if any pillar regresses)

For a single post — e.g., 5554:

```bash
python - <<'PY'
import json, requests
from tools.py.pillar_env import AUTH, WP_BASE, assert_allowed

pid = 5554
assert_allowed(pid)
snap = json.load(open(f"backups/pillars/{pid}-2026-05-24.json", encoding="utf-8"))
payload = {
    "meta": {
        "_elementor_data": snap["_elementor_data"],
        "_elementor_page_settings": snap["_elementor_page_settings"],
    }
}
r = requests.post(f"{WP_BASE}/wp-json/wp/v2/pages/{pid}", auth=AUTH, json=payload, timeout=30)
print(r.status_code, r.text[:200])
PY
```

Other posts: replace `pid` value.

---

## Self-Review Notes (filled after writing this plan)

- All 10 spec components have a task that creates the HTML widget and inserts it.
- CSS file contains every component referenced by the widgets (Hero, Capabilities, Tech, Industries, Stats, Process, Cases, FAQ, CTA, Nav).
- All function/script names match across tasks: `pillar_env.assert_allowed`, `pillar_apply_css.apply`, `pillar_insert_widget.insert`, `pillar_snapshot.snap`, `pillar_a11y.audit`.
- Allowed-ID list `ALLOWED_POST_IDS` referenced in every mutation script via `assert_allowed(post_id)`.
- Backup snapshot filename pattern `{pid}-2026-05-24.json` consistent between backup script and rollback recipe.
- Custom CSS character escapes: motion JS is wrapped in `<script>` inside an Elementor HTML widget (Task A.7 step 4) — avoids the WPCode/snippet path entirely.
- WhatsApp color hard-coded to `#075E54` in CSS (`.sxp-cta-block__wa`) — respects critical rule.
- No `line-height: ##px` in CSS — verified via grep step in Tasks A.1 and A.2.
- No placeholders: every step has executable code or commands.
