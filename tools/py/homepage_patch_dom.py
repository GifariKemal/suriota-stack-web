"""Homepage DOM patches:
  1. Section[5] — remove empty 4th column, rebalance remaining 3 to match section[4] (25/25/50).
  2. "Our Location" — swap broken google_maps widget for an HTML iframe embed (no API key needed).
  3. Append a new section at the end with HTML widget containing the back-to-top button + scroll JS.

Idempotent: re-running detects existing sx-backtop section + iframe and skips re-insert.
Applied to EN(12), ID(5273), ZH(5448).
"""
from __future__ import annotations
import json
import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pillar_env import make_session, WP_BASE  # noqa: E402

PAGES = [("en", 12), ("id", 5273), ("zh", 5448)]
PRODUCTS_SECTION_ID = "4d0b943"
EMPTY_COLUMN_ID = "028bf21"
GOOGLE_MAPS_WIDGET_ID = "6088deaa"
BACKTOP_SXP_ID = "homepage-backtop"

# Google Maps free embed (no API key). Search query → SURIOTA Batam.
MAP_QUERY = "PT+Surya+Inovasi+Prioritas+Batam"
MAP_IFRAME_HTML = (
    '<div class="sx-map-embed">'
    f'<iframe src="https://www.google.com/maps?q={MAP_QUERY}&output=embed&hl=en" '
    'loading="lazy" referrerpolicy="no-referrer-when-downgrade" '
    'title="SURIOTA — Batam, Indonesia" '
    'allowfullscreen></iframe>'
    '</div>'
)

# Back-to-top button + scroll JS as a single inline HTML widget.
BACKTOP_HTML = """<script>
(function () {
  if (window.__sxHomeBacktop) return;
  window.__sxHomeBacktop = true;
  function init() {
    if (document.querySelector('.sx-backtop')) return;
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'sx-backtop';
    b.setAttribute('aria-label', 'Back to top');
    b.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5"/><path d="M6 11l6-6 6 6"/></svg>';
    b.addEventListener('click', function () {
      try { window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); }
      catch (e) { window.scrollTo(0, 0); }
    });
    document.body.appendChild(b);
    function onScroll() {
      if (window.pageYOffset > 320) b.classList.add('is-visible');
      else b.classList.remove('is-visible');
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
</script>"""


def _new_id() -> str:
    return uuid.uuid4().hex[:7]


def _backtop_section() -> dict:
    return {
        "id": _new_id(),
        "elType": "section",
        "settings": {"structure": "10", "_sxpId": BACKTOP_SXP_ID},
        "elements": [{
            "id": _new_id(),
            "elType": "column",
            "settings": {"_column_size": 100, "_inline_size": None},
            "elements": [{
                "id": _new_id(),
                "elType": "widget",
                "widgetType": "html",
                "settings": {"html": BACKTOP_HTML, "_sxpId": BACKTOP_SXP_ID},
            }],
        }],
        "isInner": False,
    }


def _patch_products_row(section: dict) -> tuple[bool, str]:
    """Remove empty column 028bf21; rebalance remaining columns to 25/25/50."""
    cols = section.get("elements", []) or []
    # Already patched?
    if not any(c.get("id") == EMPTY_COLUMN_ID for c in cols):
        return False, "products row already balanced"
    new_cols = [c for c in cols if c.get("id") != EMPTY_COLUMN_ID]
    # Rebalance remaining 3 cols to 25/25/50 (matches section[4] visual rhythm)
    sizes = [25, 25, 50]
    for c, s in zip(new_cols, sizes):
        st = c.setdefault("settings", {})
        st["_column_size"] = s
    section["elements"] = new_cols
    return True, f"removed empty col {EMPTY_COLUMN_ID}, rebalanced {len(new_cols)} cols to 25/25/50"


def _patch_map_widget(root: dict) -> tuple[bool, str]:
    """Find google_maps widget by id and convert to inline HTML iframe."""
    def walk(parent):
        children = parent.get("elements", []) or []
        for i, el in enumerate(children):
            if el.get("id") == GOOGLE_MAPS_WIDGET_ID:
                if el.get("widgetType") == "html" and "sx-map-embed" in (el.get("settings") or {}).get("html", ""):
                    return False, "map already converted"
                el["widgetType"] = "html"
                el["settings"] = {"html": MAP_IFRAME_HTML, "_sxhMapEmbed": True}
                return True, f"converted google_maps -> html iframe at id {GOOGLE_MAPS_WIDGET_ID}"
            r = walk(el)
            if r is not None:
                return r
        return None
    r = walk(root)
    return r if r else (False, "google_maps widget not found")


def _patch_backtop(sections: list) -> tuple[bool, str]:
    """Ensure exactly one sx-backtop section exists at the end (idempotent via _sxpId)."""
    existing_idx = [i for i, s in enumerate(sections)
                    if (s.get("settings") or {}).get("_sxpId") == BACKTOP_SXP_ID]
    for i in reversed(existing_idx):
        sections.pop(i)
    sections.append(_backtop_section())
    return True, f"backtop section appended (removed {len(existing_idx)} stale)"


def patch_page(session, lang: str, pid: int) -> None:
    r = session.get(f"{WP_BASE}/wp-json/wp/v2/pages/{pid}?context=edit", timeout=30)
    r.raise_for_status()
    body = r.json()
    meta = body.get("meta") or {}
    raw = meta.get("_elementor_data") or "[]"
    sections = json.loads(raw) if isinstance(raw, str) else raw

    # 1. Products row
    prod_sec = next((s for s in sections if s.get("id") == PRODUCTS_SECTION_ID), None)
    if not prod_sec:
        print(f"  {lang}: section {PRODUCTS_SECTION_ID} not found, skipping products patch")
    else:
        changed, msg = _patch_products_row(prod_sec)
        print(f"  {lang} products: {msg}")

    # 2. Map widget — search in any section
    found = False
    for s in sections:
        changed, msg = _patch_map_widget(s)
        if msg != "google_maps widget not found":
            found = True
            print(f"  {lang} map: {msg}")
            break
    if not found:
        print(f"  {lang} map: google_maps widget id {GOOGLE_MAPS_WIDGET_ID} not found")

    # 3. Backtop
    _, msg = _patch_backtop(sections)
    print(f"  {lang} backtop: {msg}")

    # POST back
    payload = {"meta": {"_elementor_data": json.dumps(sections, ensure_ascii=False)}}
    r2 = session.post(f"{WP_BASE}/wp-json/wp/v2/pages/{pid}", json=payload, timeout=30)
    if r2.status_code >= 300:
        sys.exit(f"FAIL {lang}/{pid}: {r2.status_code} {r2.text[:300]}")
    print(f"OK {lang} home (id {pid}) patched — {len(sections)} sections")


if __name__ == "__main__":
    sess = make_session()
    for lang, pid in PAGES:
        print(f"\n== {lang} (id {pid}) ==")
        patch_page(sess, lang, pid)
