"""Create sitewide snippet: refined interactivity overrides for portfolio table.
Adds micro-interactions on top of existing inline portfolio CSS."""
import os
import requests
from requests.auth import HTTPBasicAuth

AUTH = HTTPBasicAuth("admin", os.environ.get("WP_APP_PASS", ""))
BASE = "https://suriota.com/wp-json/wp/v2/elementor_snippet"

CODE = '''<style id="sx-portfolio-interactive">
/* Refined interactivity overrides for .sx-portfolio-live table */

/* Row container - prep for accent bar */
.sx-portfolio-live .sx-pl-table tbody tr {
  position: relative;
  transition: background 220ms cubic-bezier(0.22, 1, 0.36, 1),
              transform 280ms cubic-bezier(0.22, 1, 0.36, 1),
              box-shadow 220ms cubic-bezier(0.22, 1, 0.36, 1);
}

/* Left amber accent bar - slides in on hover */
.sx-portfolio-live .sx-pl-table tbody tr::before {
  content: "";
  position: absolute;
  left: 0; top: 8px; bottom: 8px;
  width: 3px;
  background: #C8851F;
  border-radius: 0 2px 2px 0;
  transform: scaleY(0);
  transform-origin: center;
  transition: transform 320ms cubic-bezier(0.22, 1, 0.36, 1);
  pointer-events: none;
  z-index: 1;
}
.sx-portfolio-live .sx-pl-table tbody tr:hover::before {
  transform: scaleY(1);
}

/* Number column - amber + bolder on row hover */
.sx-portfolio-live .sx-pl-table tbody tr td:first-child {
  transition: color 220ms cubic-bezier(0.22, 1, 0.36, 1),
              font-weight 220ms cubic-bezier(0.22, 1, 0.36, 1),
              padding-left 280ms cubic-bezier(0.22, 1, 0.36, 1);
}
.sx-portfolio-live .sx-pl-table tbody tr:hover td:first-child {
  color: #C8851F;
  font-weight: 700;
}

/* Client column - subtle underline anim */
.sx-portfolio-live .sx-pl-table tbody tr td:nth-child(2) {
  position: relative;
}
.sx-portfolio-live .sx-pl-table tbody tr td:nth-child(2)::after {
  content: "";
  position: absolute;
  left: 18px;
  bottom: 11px;
  height: 1.5px;
  width: 0;
  background: #205B69;
  transition: width 340ms cubic-bezier(0.22, 1, 0.36, 1);
  pointer-events: none;
}
.sx-portfolio-live .sx-pl-table tbody tr:hover td:nth-child(2)::after {
  width: calc(100% - 36px);
}

/* Year badge - pulse + shadow on row hover */
.sx-portfolio-live .sx-pl-yb {
  transition: transform 240ms cubic-bezier(0.22, 1, 0.36, 1),
              box-shadow 240ms cubic-bezier(0.22, 1, 0.36, 1);
}
.sx-portfolio-live .sx-pl-table tbody tr:hover .sx-pl-yb {
  transform: scale(1.06);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

/* Sort header chevron - preview on hover (when not active) */
.sx-portfolio-live .sx-pl-table thead th:not([data-sort-active])::after {
  content: "";
  display: inline-block;
  width: 8px; height: 8px;
  margin-left: 5px;
  opacity: 0;
  vertical-align: -1px;
  background: no-repeat center / contain;
  background-image: url("data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='%238B9CA3'%3E%3Cpath d='M8 4L12 9H4z M8 12L4 7h8z'/%3E%3C/svg%3E");
  transition: opacity 200ms cubic-bezier(0.22, 1, 0.36, 1);
}
.sx-portfolio-live .sx-pl-table thead th:not([data-sort-active]):hover::after {
  opacity: 0.5;
}

/* Active sort header - amber accent */
.sx-portfolio-live .sx-pl-table thead th[data-sort-active] {
  color: #0E3942;
}
.sx-portfolio-live .sx-pl-table thead th[data-sort-active]::after {
  filter: drop-shadow(0 0 1px rgba(200, 133, 31, 0.4));
}

/* Year pill ACTIVE - amber + lift */
.sx-portfolio-live .sx-pl-year-pill {
  transition: background 220ms cubic-bezier(0.22, 1, 0.36, 1),
              border-color 220ms cubic-bezier(0.22, 1, 0.36, 1),
              color 220ms cubic-bezier(0.22, 1, 0.36, 1),
              transform 220ms cubic-bezier(0.22, 1, 0.36, 1),
              box-shadow 220ms cubic-bezier(0.22, 1, 0.36, 1);
}
.sx-portfolio-live .sx-pl-year-pill:hover {
  border-color: #C8851F;
  color: #0E2530;
  transform: translateY(-1px);
}
.sx-portfolio-live .sx-pl-year-pill[aria-pressed="true"] {
  background: #C8851F;
  border-color: #C8851F;
  color: #FFFFFF;
  box-shadow: 0 3px 10px rgba(200, 133, 31, 0.32);
  transform: translateY(-1px);
}

/* Filter input - amber focus accent (was teal) */
.sx-portfolio-live .sx-pl-filter input:focus {
  border-color: #C8851F;
  box-shadow: 0 0 0 3px rgba(200, 133, 31, 0.14);
  background: #FFFEFA;
}

/* Loading spinner - amber accent */
.sx-portfolio-live .sx-pl-loading::before {
  border-top-color: #C8851F !important;
  border-width: 2.5px;
}

/* Empty state - more visual */
.sx-portfolio-live .sx-pl-empty {
  padding: 56px 24px 48px;
}
.sx-portfolio-live .sx-pl-empty::before {
  content: "⌀";
  display: block;
  font-size: 28px;
  color: #D7DEE2;
  margin-bottom: 12px;
  font-family: 'Geist Mono', monospace;
}

/* Header columns - sortable cursor hint on hover (non-touch) */
@media (hover: hover) {
  .sx-portfolio-live .sx-pl-table thead th {
    transition: color 180ms cubic-bezier(0.22, 1, 0.36, 1),
                background 180ms cubic-bezier(0.22, 1, 0.36, 1);
  }
  .sx-portfolio-live .sx-pl-table thead th:hover {
    background: #E8EDF0;
    color: #0E3942;
  }
}

/* Reduced motion - keep functionality, drop motion */
@media (prefers-reduced-motion: reduce) {
  .sx-portfolio-live .sx-pl-table tbody tr,
  .sx-portfolio-live .sx-pl-table tbody tr::before,
  .sx-portfolio-live .sx-pl-table tbody tr td:first-child,
  .sx-portfolio-live .sx-pl-table tbody tr td:nth-child(2)::after,
  .sx-portfolio-live .sx-pl-yb,
  .sx-portfolio-live .sx-pl-year-pill,
  .sx-portfolio-live .sx-pl-table thead th {
    transition: none !important;
  }
  .sx-portfolio-live .sx-pl-table tbody tr:hover::before { transform: scaleY(1); }
  .sx-portfolio-live .sx-pl-table tbody tr:hover td:nth-child(2)::after { width: calc(100% - 36px); transition: none; }
  .sx-portfolio-live .sx-pl-table tbody tr:hover .sx-pl-yb { transform: none; }
  .sx-portfolio-live .sx-pl-year-pill[aria-pressed="true"] { transform: none; }
}

/* Mobile - keep card layout, simplify hover (no hover on touch) */
@media (max-width: 720px) {
  .sx-portfolio-live .sx-pl-table tbody tr::before {
    top: 14px; bottom: 14px;
    border-radius: 0 3px 3px 0;
  }
  .sx-portfolio-live .sx-pl-table tbody tr:active::before {
    transform: scaleY(1);
  }
}
</style>
'''

payload = {
    "title": "SX / Portfolio Table Interactive Refinements",
    "status": "publish",
    "meta": {
        "_elementor_location": "elementor_body_end",
        "_elementor_priority": 8,
        "_elementor_code": CODE
    }
}

r = requests.post(BASE, auth=AUTH, json=payload, timeout=30)
print("Status:", r.status_code)
if r.status_code in (200, 201):
    d = r.json()
    print(f"Created snippet id={d.get('id')} slug={d.get('slug')}")
    print(f"Code length: {len(d.get('meta',{}).get('_elementor_code',''))}")
else:
    print(r.text[:500])
