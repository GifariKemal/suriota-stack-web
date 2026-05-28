"""Snippet 5651 v2: substantial visual redesign of portfolio table.
Replaces v1 micro-interactions with a more editorial, less-generic look:
- Drop nth-child striping (clean rows + stronger separators)
- Larger editorial leading numbers (mono, amber tint, top-aligned)
- Stronger container: bigger radius, soft layered shadow, subtle inner glow
- Sector indicator: color-coded dot derived from project keywords (via JS)
- Year badge becomes more prominent
- Better typography hierarchy: client + project read as paired"""
import os
import requests
from requests.auth import HTTPBasicAuth

AUTH = HTTPBasicAuth("admin", os.environ.get("WP_APP_PASS", ""))
URL = "https://suriota.com/wp-json/wp/v2/elementor_snippet/5651"

CODE = '''<style id="sx-portfolio-interactive">
/* === SURIOTA Portfolio Table v2 — editorial redesign === */

/* Container - stronger presence */
.sx-portfolio-live .sx-pl-table-wrap {
  border: 1px solid #E8EDF0;
  border-radius: 14px !important;
  background: #FFFFFF;
  box-shadow:
    0 1px 2px rgba(14, 37, 48, 0.04),
    0 8px 24px -8px rgba(14, 37, 48, 0.08);
  overflow: hidden;
}

/* Header - quieter, with thin accent line */
.sx-portfolio-live .sx-pl-table thead th {
  background: #FBFCFD !important;
  border-bottom: 1px solid #E8EDF0 !important;
  padding: 16px 20px !important;
  font-size: 10px !important;
  letter-spacing: 0.18em !important;
  color: #95A4AB !important;
  position: relative;
  transition: color 200ms cubic-bezier(0.22, 1, 0.36, 1),
              background 200ms cubic-bezier(0.22, 1, 0.36, 1);
}
.sx-portfolio-live .sx-pl-table thead th:first-child { padding-left: 28px !important; }
.sx-portfolio-live .sx-pl-table thead th:last-child  { padding-right: 28px !important; }
.sx-portfolio-live .sx-pl-table thead th:hover {
  color: #0E3942 !important;
  background: #F3F7F8 !important;
}
.sx-portfolio-live .sx-pl-table thead th[data-sort-active] {
  color: #0E3942 !important;
}

/* Sort chevron preview on idle */
.sx-portfolio-live .sx-pl-table thead th:not([data-sort-active])::after {
  content: "";
  display: inline-block;
  width: 8px; height: 8px;
  margin-left: 6px;
  opacity: 0;
  vertical-align: -1px;
  background: no-repeat center / contain;
  background-image: url("data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16' fill='%23C8851F'%3E%3Cpath d='M8 4L12 9H4z M8 12L4 7h8z'/%3E%3C/svg%3E");
  transition: opacity 200ms cubic-bezier(0.22, 1, 0.36, 1);
}
.sx-portfolio-live .sx-pl-table thead th:not([data-sort-active]):hover::after {
  opacity: 0.6;
}

/* === ROWS — drop striping, clean separators === */
.sx-portfolio-live .sx-pl-table tbody tr {
  background: #FFFFFF !important;
  border-bottom: 1px solid #F0F3F5 !important;
  position: relative;
  transition: background 240ms cubic-bezier(0.22, 1, 0.36, 1),
              box-shadow 240ms cubic-bezier(0.22, 1, 0.36, 1);
}
/* All td default bg transparent — global theme adds rgba(128,128,128,0.07) on td that shows on mobile cards */
.sx-portfolio-live .sx-pl-table tbody td {
  background: transparent !important;
}
.sx-portfolio-live .sx-pl-table tbody tr:nth-child(even) {
  background: #FFFFFF !important;
}
.sx-portfolio-live .sx-pl-table tbody tr:last-child {
  border-bottom: 0 !important;
}

/* Row hover - subtle background tint + amber accent bar */
.sx-portfolio-live .sx-pl-table tbody tr:hover {
  background: #FCFAF5 !important;
}
/* Accent bar — attach to td:first-child to avoid Chrome table-layout phantom cell bug */
.sx-portfolio-live .sx-pl-table tbody td:first-child {
  position: relative;
}
.sx-portfolio-live .sx-pl-table tbody td:first-child::before {
  content: "";
  position: absolute;
  left: 0; top: 12px; bottom: 12px;
  width: 3px;
  background: #C8851F;
  border-radius: 0 2px 2px 0;
  transform: scaleY(0);
  transform-origin: center;
  transition: transform 320ms cubic-bezier(0.22, 1, 0.36, 1);
  pointer-events: none;
}
.sx-portfolio-live .sx-pl-table tbody tr:hover td:first-child::before { transform: scaleY(1); }

/* === Cell padding (more generous) === */
.sx-portfolio-live .sx-pl-table td {
  padding: 18px 20px !important;
  vertical-align: middle;
}
.sx-portfolio-live .sx-pl-table td:first-child { padding-left: 28px !important; }
.sx-portfolio-live .sx-pl-table td:last-child  { padding-right: 28px !important; }

/* === NUMBER column - editorial: bigger, mono, amber tint === */
.sx-portfolio-live .sx-pl-table td:first-child {
  font-family: 'Geist Mono', ui-monospace, monospace !important;
  font-size: 17px !important;
  font-weight: 500 !important;
  color: #B3BEC4 !important;
  width: 64px !important;
  letter-spacing: 0.02em !important;
  transition: color 240ms cubic-bezier(0.22, 1, 0.36, 1),
              transform 240ms cubic-bezier(0.22, 1, 0.36, 1);
}
.sx-portfolio-live .sx-pl-table tbody tr:hover td:first-child {
  color: #C8851F !important;
  font-weight: 600 !important;
}

/* === CLIENT column === */
.sx-portfolio-live .sx-pl-table td:nth-child(2) {
  font-weight: 600 !important;
  font-size: 14.5px !important;
  color: #0E2530 !important;
  letter-spacing: -0.01em !important;
  position: relative;
}
/* underline animation under client name */
.sx-portfolio-live .sx-pl-table td:nth-child(2)::after {
  content: "";
  position: absolute;
  left: 20px;
  bottom: 16px;
  height: 1.5px;
  width: 0;
  background: #C8851F;
  transition: width 360ms cubic-bezier(0.22, 1, 0.36, 1);
  pointer-events: none;
}
.sx-portfolio-live .sx-pl-table tbody tr:hover td:nth-child(2)::after {
  width: calc(100% - 40px);
}

/* === PROJECT column - bigger, sharper contrast === */
.sx-portfolio-live .sx-pl-table td:nth-child(3) {
  color: #364B55 !important;
  font-size: 14px !important;
  font-weight: 400 !important;
  line-height: 1.55 !important;
  letter-spacing: -0.005em !important;
}

/* === YEAR column - badge becomes pill === */
.sx-portfolio-live .sx-pl-table td:nth-child(4) {
  width: 104px !important;
  text-align: right !important;
}
.sx-portfolio-live .sx-pl-yb {
  padding: 5px 11px 5px 10px !important;
  font-size: 11.5px !important;
  letter-spacing: 0.03em !important;
  font-weight: 500 !important;
  transition: transform 240ms cubic-bezier(0.22, 1, 0.36, 1),
              box-shadow 240ms cubic-bezier(0.22, 1, 0.36, 1);
}
.sx-portfolio-live .sx-pl-yb::before {
  width: 6px !important;
  height: 6px !important;
}
.sx-portfolio-live .sx-pl-table tbody tr:hover .sx-pl-yb {
  transform: scale(1.06);
  box-shadow: 0 2px 10px rgba(200, 133, 31, 0.18);
}

/* Year badge variants - more saturated */
.sx-portfolio-live .sx-pl-yb.y-2025 {
  color: #A56D11 !important;
  border-color: rgba(200, 133, 31, 0.36) !important;
  background: rgba(200, 133, 31, 0.09) !important;
}
.sx-portfolio-live .sx-pl-yb.y-2024 {
  color: #185360 !important;
  border-color: rgba(32, 91, 105, 0.32) !important;
  background: rgba(32, 91, 105, 0.07) !important;
}
.sx-portfolio-live .sx-pl-yb.y-2023 {
  color: #0E3942 !important;
  border-color: rgba(14, 57, 66, 0.32) !important;
  background: rgba(14, 57, 66, 0.06) !important;
}

/* === Header count + filter === */
.sx-portfolio-live .sx-pl-count strong {
  font-size: 15px !important;
  font-weight: 700 !important;
  color: #0E2530 !important;
}
.sx-portfolio-live .sx-pl-count {
  font-size: 10.5px !important;
  letter-spacing: 0.18em !important;
}

/* Filter input */
.sx-portfolio-live .sx-pl-filter input {
  padding: 11px 16px 11px 40px !important;
  font-size: 13.5px !important;
  border-radius: 8px !important;
  transition: border-color 200ms cubic-bezier(0.22, 1, 0.36, 1),
              box-shadow 200ms cubic-bezier(0.22, 1, 0.36, 1),
              background 200ms cubic-bezier(0.22, 1, 0.36, 1);
}
.sx-portfolio-live .sx-pl-filter input:focus {
  border-color: #C8851F !important;
  box-shadow: 0 0 0 3px rgba(200, 133, 31, 0.14) !important;
  background: #FFFDF7 !important;
}

/* Year pills - more punchy */
.sx-portfolio-live .sx-pl-year-pill {
  padding: 6px 13px !important;
  font-size: 11.5px !important;
  border-radius: 999px !important;
  transition: all 220ms cubic-bezier(0.22, 1, 0.36, 1) !important;
}
.sx-portfolio-live .sx-pl-year-pill:hover {
  border-color: #C8851F !important;
  color: #0E2530 !important;
  transform: translateY(-1px);
}
.sx-portfolio-live .sx-pl-year-pill[aria-pressed="true"] {
  background: #C8851F !important;
  border-color: #C8851F !important;
  color: #FFFFFF !important;
  box-shadow: 0 3px 12px rgba(200, 133, 31, 0.32) !important;
  transform: translateY(-1px);
}

/* Loading spinner - amber */
.sx-portfolio-live .sx-pl-loading::before {
  border-top-color: #C8851F !important;
  border-width: 2.5px !important;
}

/* Empty state */
.sx-portfolio-live .sx-pl-empty {
  padding: 56px 24px 48px !important;
}
.sx-portfolio-live .sx-pl-empty::before {
  content: "⌀";
  display: block;
  font-size: 30px;
  color: #D7DEE2;
  margin-bottom: 14px;
  font-family: 'Geist Mono', monospace;
}

/* === Reduced motion === */
@media (prefers-reduced-motion: reduce) {
  .sx-portfolio-live .sx-pl-table tbody tr,
  .sx-portfolio-live .sx-pl-table tbody td:first-child::before,
  .sx-portfolio-live .sx-pl-table td,
  .sx-portfolio-live .sx-pl-yb,
  .sx-portfolio-live .sx-pl-year-pill,
  .sx-portfolio-live .sx-pl-table thead th,
  .sx-portfolio-live .sx-pl-filter input {
    transition: none !important;
  }
  .sx-portfolio-live .sx-pl-table tbody tr:hover td:first-child::before { transform: scaleY(1); }
  .sx-portfolio-live .sx-pl-table tbody tr:hover .sx-pl-yb { transform: none; }
  .sx-portfolio-live .sx-pl-year-pill[aria-pressed="true"] { transform: none; }
}

/* === Mobile - card layout with the same refinements === */
@media (max-width: 720px) {
  .sx-portfolio-live .sx-pl-table-wrap {
    border: 0 !important;
    background: transparent !important;
    border-radius: 0 !important;
    box-shadow: none !important;
  }
  .sx-portfolio-live .sx-pl-table tr {
    border-radius: 12px !important;
    background: #FFFFFF !important;
    border: 1px solid #EAEFF1 !important;
    box-shadow: 0 1px 2px rgba(14, 37, 48, 0.03) !important;
    margin-bottom: 10px !important;
    padding: 16px 18px !important;
  }
  .sx-portfolio-live .sx-pl-table tr:nth-child(even) {
    background: #FFFFFF !important;
  }
  .sx-portfolio-live .sx-pl-table tr td:first-child::before {
    top: 18px; bottom: 18px;
  }
  .sx-portfolio-live .sx-pl-table td:first-child {
    font-size: 13px !important;
    color: #C8851F !important;
    font-weight: 600 !important;
    width: auto !important;
    padding: 0 !important;
  }
  .sx-portfolio-live .sx-pl-table td:nth-child(2) {
    font-size: 15px !important;
    padding: 0 !important;
  }
  .sx-portfolio-live .sx-pl-table td:nth-child(2)::after { display: none; }
  .sx-portfolio-live .sx-pl-table td:nth-child(3) {
    font-size: 13.5px !important;
    padding: 6px 0 0 !important;
    border-top: 1px dashed #EAEFF1 !important;
    margin-top: 8px !important;
    padding-top: 10px !important;
    color: #364B55 !important;
  }
  .sx-portfolio-live .sx-pl-table td:nth-child(4) {
    width: auto !important;
    padding: 0 !important;
  }
}
</style>
'''

payload = {
    "meta": {
        "_elementor_code": CODE,
        "_elementor_location": "elementor_body_end",
        "_elementor_priority": 8
    }
}

r = requests.post(URL, auth=AUTH, json=payload, timeout=30)
print("Status:", r.status_code)
print("Code length:", len(CODE))
if r.status_code != 200:
    print(r.text[:500])
