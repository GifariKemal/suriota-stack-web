"""Flush Elementor's HTML render cache via admin-ajax.

Required after any batch widget insertion via REST — otherwise only the first
new section renders. See memory: suriota_elementor_cache_flush.md.

Usage:
    python tools/py/pillar_clear_cache.py        # global cache clear
"""
from __future__ import annotations
import re
import sys

from pillar_env import WP_BASE, make_session


def clear_cache(session) -> bool:
    tools_html = session.get(
        f"{WP_BASE}/wp-admin/admin.php?page=elementor-tools",
        timeout=30,
    ).text
    # The <button id="elementor-clear-cache-button"> tag in Elementor renders
    # `data-nonce` either before or after the `id` attribute depending on
    # version, so we accept either order.
    m = re.search(
        r'<button[^>]*id="elementor-clear-cache-button"[^>]*data-nonce="([^"]+)"',
        tools_html,
    ) or re.search(
        r'<button[^>]*data-nonce="([^"]+)"[^>]*id="elementor-clear-cache-button"',
        tools_html,
    )
    if not m:
        sys.exit("FAIL: could not scrape elementor_clear_cache nonce from tools page")
    nonce = m.group(1)
    # make_session() globally sets Content-Type: application/json for REST
    # calls; admin-ajax requires form-encoded, so override per-request.
    r = session.post(
        f"{WP_BASE}/wp-admin/admin-ajax.php",
        data={"action": "elementor_clear_cache", "_nonce": nonce},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )
    try:
        ok = r.json().get("success") is True
    except Exception:
        ok = False
    if not ok:
        sys.exit(f"FAIL: elementor_clear_cache returned {r.status_code} {r.text[:200]}")
    print("OK elementor cache cleared")
    return True


if __name__ == "__main__":
    sess = make_session()
    clear_cache(sess)
