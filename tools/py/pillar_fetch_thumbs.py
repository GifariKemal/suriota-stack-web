"""Fetch featured-image URLs for portfolio posts via WP REST."""
from __future__ import annotations
import json
import sys

from pillar_env import WP_BASE, make_session

# Per pillar: list of portfolio post IDs (top 6 from audit doc).
P1_IDS = [2129, 1925, 1918, 1911, 1862, 1848]
P2_IDS = [1480, 1466, 2129, 1925, 1918, 1911]
P3_IDS = [2266, 2221, 2214, 2201, 2181, 2174]
P4_IDS = [2253, 2246, 2194, 2122, 2115, 2068]
P5_IDS = [1904, 1890, 1869, 1840, 1454, 1450]

ALL_IDS = sorted(set(P1_IDS + P2_IDS + P3_IDS + P4_IDS + P5_IDS))

def fetch(session, post_id: int) -> dict:
    # Use `_embed` (not `_embed=...`) and no `_fields` — restricting fields
    # strips the `_embedded` block from the response.
    r = session.get(f"{WP_BASE}/wp-json/wp/v2/posts/{post_id}?_embed", timeout=30)
    r.raise_for_status()
    data = r.json()
    media_url = None
    if "_embedded" in data:
        fm_list = data["_embedded"].get("wp:featuredmedia") or []
        if fm_list:
            m = fm_list[0] or {}
            sizes = (m.get("media_details") or {}).get("sizes") or {}
            # Prefer a reasonably-sized version, fall back to source_url.
            media_url = (
                (sizes.get("large") or {}).get("source_url")
                or (sizes.get("medium_large") or {}).get("source_url")
                or m.get("source_url")
            )
    return {
        "id": data["id"],
        "title": data["title"]["rendered"],
        "link": data["link"],
        "image": media_url,
    }

if __name__ == "__main__":
    sess = make_session()
    out = {pid: fetch(sess, pid) for pid in ALL_IDS}
    print(json.dumps(out, indent=2, ensure_ascii=False))
