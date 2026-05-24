"""Reorder sections in a pillar post's _elementor_data by _sxpId.

Reads current _elementor_data, finds each section's _sxpId, then re-emits
sections in the order specified by SXPID_ORDER for that pillar.
Sections whose _sxpId is not in the order list are appended at the end
(safety: never silently drop anything).
"""
from __future__ import annotations
import json
import sys

from pillar_env import WP_BASE, assert_allowed, make_session

# Local PILLAR_BY_POST override — pillar_env.py's PILLAR_OF has labeling drift
# vs. the actual content/URLs (see pillar_snapshot.URL_BY_ID). We do NOT touch
# pillar_env.py per scope discipline; we resolve pillar number locally.
PILLAR_BY_POST: dict[int, int] = {
    # P1 — Industrial IoT & System Integration
    5554: 1, 5566: 1, 5571: 1,
    # P2 — AI Industrial Analytics
    5555: 2, 5567: 2, 5572: 2,
    # P3 — Digital Transformation Consulting
    5556: 3, 5568: 3, 5573: 3,
    # P4 — Industrial Engineering & Automation
    5557: 4, 5569: 4, 5574: 4,
    # P5 — SURGE SaaS Platform
    5558: 5, 5570: 5, 5575: 5,
}

# Canonical section order per pillar number (1-5). Items refer to _sxpId
# values used in the existing insert scripts.
# Sections with no _sxpId (legacy) preserve their relative position (appended
# at the very end as a safety net).

P1_ORDER = ["p1-hero", "p1-intro", "p1-capabilities", "p1-approach", "p1-tech",
            "p1-industries", "p1-stats", "p1-process", "p1-impact", "p1-cases",
            "p1-faq", "p1-related", "p1-cta", "p1-schema", "p1-motion"]

P2_ORDER = ["p2-hero", "p2-intro", "p2-capabilities", "p2-approach", "p2-tech",
            "p2-industries", "p2-stats", "p2-process", "p2-impact", "p2-cases",
            "p2-faq", "p2-related", "p2-cta", "p2-schema", "p2-motion"]

P3_ORDER = ["p3-hero", "p3-intro", "p3-capabilities", "p3-deliverables",
            "p3-approach", "p3-stats", "p3-process", "p3-impact", "p3-cases",
            "p3-faq", "p3-related", "p3-cta", "p3-schema", "p3-motion"]

P4_ORDER = ["p4-hero", "p4-intro", "p4-nav", "p4-sub-automation",
            "p4-sub-electrical", "p4-sub-renewable", "p4-sub-water",
            "p4-approach", "p4-tech", "p4-stats", "p4-process", "p4-impact",
            "p4-cases", "p4-faq", "p4-related", "p4-cta", "p4-schema",
            "p4-motion"]

P5_ORDER = ["p5-hero", "p5-intro", "p5-capabilities", "p5-features",
            "p5-approach", "p5-deployment", "p5-pricing", "p5-impact",
            "p5-cases", "p5-faq", "p5-related", "p5-cta", "p5-schema",
            "p5-motion"]

ORDER_BY_PILLAR = {1: P1_ORDER, 2: P2_ORDER, 3: P3_ORDER, 4: P4_ORDER, 5: P5_ORDER}


def reorder(session, post_id: int) -> None:
    assert_allowed(post_id)
    pillar_num = PILLAR_BY_POST[post_id]
    target_order = ORDER_BY_PILLAR[pillar_num]

    r = session.get(f"{WP_BASE}/wp-json/wp/v2/pages/{post_id}?context=edit", timeout=30)
    r.raise_for_status()
    meta = r.json().get("meta") or {}
    raw = meta.get("_elementor_data") or "[]"
    elements = json.loads(raw) if isinstance(raw, str) else raw

    # Bucket sections by _sxpId
    by_sxpid: dict[str, dict] = {}
    no_sxpid_sections: list[dict] = []
    for sec in elements:
        sxp_id = (sec.get("settings") or {}).get("_sxpId")
        if sxp_id:
            by_sxpid[sxp_id] = sec
        else:
            no_sxpid_sections.append(sec)

    # Reassemble in target order. Append any unknown _sxpId values to preserve them.
    out: list[dict] = []
    used: set[str] = set()
    for sxp_id in target_order:
        if sxp_id in by_sxpid:
            out.append(by_sxpid[sxp_id])
            used.add(sxp_id)

    # Append any sxp-tagged sections that weren't in the target order (safety net)
    unknown = sorted(set(by_sxpid) - used)
    for sxp_id in unknown:
        out.append(by_sxpid[sxp_id])

    # Append any sections without _sxpId at the very end (legacy content)
    out.extend(no_sxpid_sections)

    payload = {"meta": {"_elementor_data": json.dumps(out, ensure_ascii=False)}}
    r2 = session.post(f"{WP_BASE}/wp-json/wp/v2/pages/{post_id}", json=payload, timeout=30)
    if r2.status_code >= 300:
        sys.exit(f"FAIL reorder {post_id}: {r2.status_code} {r2.text[:300]}")
    print(
        f"OK reordered {post_id} (P{pillar_num}): "
        f"sxp={len(by_sxpid)} ordered={len(used)} "
        f"unknown={len(unknown)} legacy={len(no_sxpid_sections)} "
        f"total={len(out)}"
    )


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python tools/py/pillar_reorder.py <post_id> [<post_id> ...]")
    sess = make_session()
    for pid in sys.argv[1:]:
        reorder(sess, int(pid))
