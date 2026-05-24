"""Backup _elementor_data + page settings for one pillar post to JSON."""
from __future__ import annotations
import json
import sys
from datetime import date
from pathlib import Path

from pillar_env import ROOT, WP_BASE, assert_allowed, make_session


def backup(session, post_id: int) -> Path:
    assert_allowed(post_id)
    r = session.get(f"{WP_BASE}/wp-json/wp/v2/pages/{post_id}?context=edit", timeout=30)
    r.raise_for_status()
    data = r.json()
    snapshot = {
        "post_id": post_id,
        "slug": data.get("slug"),
        "title": (data.get("title") or {}).get("raw") if isinstance(data.get("title"), dict) else data.get("title"),
        "status": data.get("status"),
        "_elementor_data": (data.get("meta") or {}).get("_elementor_data"),
        "_elementor_page_settings": (data.get("meta") or {}).get("_elementor_page_settings"),
        "fetched_at": date.today().isoformat(),
    }
    out = ROOT / "backups" / "pillars" / f"{post_id}-{date.today().isoformat()}.json"
    out.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python tools/py/pillar_backup.py <post_id> [<post_id> ...]")
    sess = make_session()
    for pid in sys.argv[1:]:
        path = backup(sess, int(pid))
        print(f"OK  {pid} -> {path.relative_to(ROOT)}")
