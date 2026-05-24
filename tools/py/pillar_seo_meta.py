"""Phase G.3 - Update AIOSEO title + description for the 15 pillar posts.

Uses the AIOSEO REST endpoint POST /wp-json/aioseo/v1/post with body
{"id": <post_id>, "title": "...", "description": "..."}. Discovery probe
in this phase confirmed this is the working write path (other variants
returned 404 / "Post ID is missing"). After update we GET back the same
endpoint to confirm persistence.

The 15 pillar post IDs are gated by pillar_env.assert_allowed so this
script cannot accidentally touch a non-pillar post.
"""
from __future__ import annotations

import sys

from pillar_env import WP_BASE, assert_allowed, make_session

# (post_id, title, description) for the 15 pillars: EN x5, ID x5, ZH x5
TARGETS: list[tuple[int, str, str]] = [
    # ----- EN (5554-5558) -----
    (5554,
     "Industrial IoT & System Integration in Batam | SURIOTA",
     "Modbus/OPC UA/MQTT gateways, SCADA-MES-ERP integration, and edge-to-cloud analytics for manufacturing, oil & gas, and shipyards in Indonesia."),
    (5555,
     "Industrial AI & Analytics \u2014 Predictive, Vision, OEE",
     "Production-grade AI for predictive maintenance, computer vision QC, OEE analytics, and anomaly detection. Deploy on plant data, not slideware."),
    (5556,
     "Industrial Digital Transformation Consulting | SURIOTA",
     "Vendor-neutral Industry 4.0 roadmaps. Digital maturity assessment, OT/IT convergence, technology selection, and change management for industrial leaders."),
    (5557,
     "Industrial Engineering & Automation Services | Batam",
     "End-to-end engineering: PLC/SCADA, electrical panels, solar PV (PLTS), and water treatment (WTP/WWTP) with KLHK SPARING compliance."),
    (5558,
     "SURGE \u2014 Industrial IoT Monitoring SaaS Platform",
     "Cloud-native industrial IoT monitoring platform. Energy mapping, vessel tracking, water analytics, KLHK SPARING compliance. Free 30-day trial."),
    # ----- ID (5566-5570) -----
    (5566,
     "Integrasi Sistem IoT Industri di Batam | SURIOTA",
     "Gateway Modbus/OPC UA/MQTT, integrasi SCADA-MES-ERP, dan analitik edge-to-cloud untuk manufaktur, migas, dan galangan kapal di Indonesia."),
    (5567,
     "AI & Analitik Industri \u2014 Prediktif, Vision, OEE",
     "AI industri grade produksi: predictive maintenance, computer vision QC, OEE analytics, anomaly detection. Deploy di data pabrik nyata."),
    (5568,
     "Konsultasi Transformasi Digital Industri | SURIOTA",
     "Roadmap Industry 4.0 vendor-netral. Asesmen kematangan digital, OT/IT convergence, seleksi teknologi, dan change management."),
    (5569,
     "Teknik Industri & Automasi \u2014 PLTS, KLHK, PLC | SURIOTA",
     "Engineering end-to-end: PLC/SCADA, panel listrik, PLTS, dan pengolahan air (WTP/WWTP) dengan kepatuhan KLHK SPARING."),
    (5570,
     "SURGE \u2014 Platform SaaS Monitoring IoT Industri",
     "Platform monitoring IoT industri cloud-native. Energy mapping, vessel tracking, water analytics, KLHK SPARING. Trial gratis 30 hari."),
    # ----- ZH (5571-5575) -----
    (5571,
     "\u5de5\u4e1a IoT \u4e0e\u7cfb\u7edf\u96c6\u6210 | SURIOTA \u5df4\u6de1\u5c9b",
     "Modbus / OPC UA / MQTT \u5de5\u4e1a\u7f51\u5173\uff0cSCADA-MES-ERP \u96c6\u6210\u4e0e\u8fb9\u7f18\u5230\u4e91\u7aef\u5206\u6790\u3002\u670d\u52a1\u5370\u5ea6\u5c3c\u897f\u4e9a\u5236\u9020\u4e1a\u3001\u6cb9\u6c14\u3001\u9020\u8239\u4e1a\u3002"),
    (5572,
     "\u5de5\u4e1a AI \u4e0e\u5206\u6790 \u2014 \u9884\u6d4b\u6027\u7ef4\u62a4\u3001\u89c6\u89c9\u3001OEE",
     "\u751f\u4ea7\u7ea7\u5de5\u4e1a AI\uff1a\u9884\u6d4b\u6027\u7ef4\u62a4\u3001\u8ba1\u7b97\u673a\u89c6\u89c9\u8d28\u68c0\u3001OEE \u5206\u6790\u4e0e\u5f02\u5e38\u68c0\u6d4b\u3002\u57fa\u4e8e\u771f\u5b9e\u5de5\u5382\u6570\u636e\u90e8\u7f72\uff0c\u975e\u6982\u5ff5\u6f14\u793a\u3002"),
    (5573,
     "\u5de5\u4e1a\u6570\u5b57\u5316\u8f6c\u578b\u54a8\u8be2 | SURIOTA",
     "\u5382\u5546\u4e2d\u7acb\u7684\u5de5\u4e1a 4.0 \u8def\u7ebf\u56fe\u3002\u6570\u5b57\u5316\u6210\u719f\u5ea6\u8bc4\u4f30\u3001OT/IT \u878d\u5408\u3001\u6280\u672f\u9009\u578b\u4e0e\u53d8\u9769\u7ba1\u7406\uff0c\u9762\u5411\u5de5\u4e1a\u9886\u5bfc\u8005\u3002"),
    (5574,
     "\u5de5\u4e1a\u5de5\u7a0b\u4e0e\u81ea\u52a8\u5316\u670d\u52a1 | SURIOTA \u5df4\u6de1\u5c9b",
     "\u7aef\u5230\u7aef\u5de5\u7a0b\uff1aPLC/SCADA\u3001\u7535\u6c14\u914d\u7535\u67dc\u3001\u592a\u9633\u80fd (PLTS)\u3001\u6c34\u5904\u7406 (WTP/WWTP)\uff0c\u7b26\u5408 KLHK SPARING \u5408\u89c4\u8981\u6c42\u3002"),
    (5575,
     "SURGE \u2014 \u5de5\u4e1a IoT \u76d1\u63a7 SaaS \u5e73\u53f0",
     "\u4e91\u539f\u751f\u5de5\u4e1a IoT \u76d1\u63a7\u5e73\u53f0\u3002\u80fd\u6e90\u6620\u5c04\u3001\u8239\u961f\u8ffd\u8e2a\u3001\u6c34\u5206\u6790\u3001KLHK SPARING \u5408\u89c4\u3002\u63d0\u4f9b 30 \u5929\u514d\u8d39\u8bd5\u7528\u3002"),
]


def update_aioseo(session, post_id: int, title: str, description: str) -> bool:
    """POST title + description to AIOSEO REST.

    The AIOSEO endpoint accepts {"id", "title", "description"} and returns
    {"success": true, "posts": <id>} on success. We GET it back after to
    verify persistence.
    """
    assert_allowed(post_id)
    payload = {"id": post_id, "title": title, "description": description}
    r = session.post(f"{WP_BASE}/wp-json/aioseo/v1/post", json=payload, timeout=30)
    if r.status_code >= 300:
        print(f"FAIL {post_id}: POST {r.status_code} {r.text[:200]}")
        return False
    try:
        body = r.json()
    except Exception:  # noqa: BLE001
        body = {}
    if not body.get("success"):
        print(f"FAIL {post_id}: not success in body {r.text[:200]}")
        return False

    # Verify via GET
    g = session.get(
        f"{WP_BASE}/wp-json/aioseo/v1/post?postId={post_id}", timeout=30
    )
    if g.status_code >= 300:
        print(f"WARN {post_id}: verify GET {g.status_code}")
        return True  # POST succeeded; just couldn't verify
    try:
        cp = g.json()["data"]["currentPost"]
    except Exception:  # noqa: BLE001
        print(f"WARN {post_id}: verify parse failed")
        return True
    got_title = cp.get("title", "")
    got_desc = cp.get("description", "")
    if got_title == title and got_desc == description:
        print(f"OK {post_id}: title={len(title)}c desc={len(description)}c")
        return True
    print(
        f"WARN {post_id}: persisted but not exact match. "
        f"got_title={got_title!r:.120} got_desc={got_desc!r:.120}"
    )
    return True


def main() -> int:
    sess = make_session()
    ok = 0
    fail = 0
    for pid, title, desc in TARGETS:
        if update_aioseo(sess, pid, title, desc):
            ok += 1
        else:
            fail += 1
    print(f"\nSummary: {ok} ok, {fail} failed (of {len(TARGETS)})")
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
