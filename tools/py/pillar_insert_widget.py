"""Insert HTML widget(s) into a pillar post's _elementor_data idempotently.

Each new section is tagged via settings._sxpId so re-runs replace previous insertion.
Also ensures _elementor_edit_mode is 'builder' so Elementor renders the new data.
"""
from __future__ import annotations
import json
import sys
import uuid
from pathlib import Path

from pillar_env import ROOT, WP_BASE, assert_allowed, make_session


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
            "settings": {"_column_size": 100, "_inline_size": None},
            "elements": [{
                "id": _new_id(),
                "elType": "widget",
                "widgetType": "html",
                "settings": {"html": html, "_sxpId": sxp_id},
            }],
        }],
        "isInner": False,
    }


def _parse_data(raw) -> list:
    if not raw:
        return []
    if isinstance(raw, list):
        return raw
    if isinstance(raw, str):
        try:
            parsed = json.loads(raw)
            return parsed if isinstance(parsed, list) else []
        except json.JSONDecodeError:
            return []
    return []


def _strip_existing(elements: list, sxp_id: str) -> list:
    return [
        sec for sec in elements
        if (sec.get("settings") or {}).get("_sxpId") != sxp_id
    ]


def insert(session, post_id: int, sxp_id: str, html_file: Path) -> None:
    assert_allowed(post_id)
    html = html_file.read_text(encoding="utf-8")

    r = session.get(f"{WP_BASE}/wp-json/wp/v2/pages/{post_id}?context=edit", timeout=30)
    r.raise_for_status()
    body = r.json()
    meta = body.get("meta") or {}
    elements = _parse_data(meta.get("_elementor_data"))
    elements = _strip_existing(elements, sxp_id)
    elements.append(_wrap(sxp_id, html))

    payload = {
        "meta": {
            "_elementor_data": json.dumps(elements, ensure_ascii=False),
            "_elementor_edit_mode": "builder",
        }
    }
    r2 = session.post(f"{WP_BASE}/wp-json/wp/v2/pages/{post_id}", json=payload, timeout=30)
    if r2.status_code >= 300:
        sys.exit(f"FAIL insert {post_id}/{sxp_id}: {r2.status_code} {r2.text[:300]}")
    print(f"OK inserted {sxp_id} into {post_id} (now {len(elements)} sections)")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit("usage: python tools/py/pillar_insert_widget.py <post_id> <sxp_id> <html_file>")
    sess = make_session()
    insert(sess, int(sys.argv[1]), sys.argv[2], Path(sys.argv[3]))
