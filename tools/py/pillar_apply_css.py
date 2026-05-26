"""Apply per-page Custom CSS (tokens + components) to a pillar post."""
from __future__ import annotations
import sys
from pathlib import Path

from pillar_env import ROOT, WP_BASE, assert_allowed, make_session

CSS_FILES = [
    ROOT / "design-system" / "sx-pillar-v3.tokens.css",
    ROOT / "design-system" / "sx-pillar-v3.components.css",
    ROOT / "design-system" / "sx-pillar-v3.atmosphere.css",
]

def build_css_bundle() -> str:
    return "\n\n".join(p.read_text(encoding="utf-8") for p in CSS_FILES)

def apply(session, post_id: int) -> None:
    assert_allowed(post_id)
    css = build_css_bundle()
    payload = {"meta": {"_elementor_page_settings": {"custom_css": css}}}
    r = session.post(f"{WP_BASE}/wp-json/wp/v2/pages/{post_id}", json=payload, timeout=30)
    if r.status_code >= 300:
        sys.exit(f"FAIL {post_id}: {r.status_code} {r.text[:300]}")
    print(f"OK CSS applied to {post_id} ({len(css)} chars)")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python tools/py/pillar_apply_css.py <post_id> [<post_id> ...]")
    sess = make_session()
    for pid in sys.argv[1:]:
        apply(sess, int(pid))
