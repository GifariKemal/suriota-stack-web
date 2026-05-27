"""Repoint + reorder + retitle the 5 service cards on the homepage (EN/ID/ZH).

Replaces the editor field of widget id `3f586b9` in section[0] of each homepage's
_elementor_data with a fresh, canonical-P1->P5-ordered grid pointing to the new
pillar URLs.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pillar_env import make_session, WP_BASE  # noqa: E402

WIDGET_ID = "3f586b9"

# Per-pillar accent (matches sx-pillar-v3.tokens.css body.page-id-* overrides).
ACCENT = {
    "p1": "#205B69",  # teal
    "p2": "#3C7D47",  # green
    "p3": "#C8851F",  # amber
    "p4": "#205B69",  # teal
    "p5": "#0E3942",  # deep teal
}

# Inline SVG content per pillar (kept compact; existing icon set).
SVG = {
    "p1": '<rect x="7" y="7" width="10" height="10" rx="1"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
    "p2": '<path d="M3 17l5-5 4 4 8-9"/><path d="M16 7h4v4"/>',
    "p3": '<path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"/>',
    "p4": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 11-2.83 2.83l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 11-4 0v-.09a1.65 1.65 0 00-1-1.51 1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 11-2.83-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 110-4h.09a1.65 1.65 0 001.51-1 1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 112.83-2.83l.06.06a1.65 1.65 0 001.82.33h0a1.65 1.65 0 001-1.51V3a2 2 0 114 0v.09a1.65 1.65 0 001 1.51h0a1.65 1.65 0 001.82-.33l.06-.06a2 2 0 112.83 2.83l-.06.06a1.65 1.65 0 00-.33 1.82v0a1.65 1.65 0 001.51 1H21a2 2 0 110 4h-.09a1.65 1.65 0 00-1.51 1z"/>',
    "p5": '<path d="M18 10h-1.26A8 8 0 109 20h9a5 5 0 000-10z"/><path d="M8 14h.01M12 14h.01M16 14h.01"/>',
}

# Card content per language. Order = P1, P2, P3, P4, P5.
CARDS = {
    "en": [
        {
            "pillar": "p1", "num": "01",
            "href": "https://suriota.com/industrial-iot-system-integration/",
            "title": "Industrial IoT & System Integration",
            "desc": "End-to-end Industrial IoT. Modbus gateway, MQTT, edge computing, SCADA, sensor-to-cloud pipelines with IEC 62443 security for manufacturing, oil &amp; gas, and maritime operations.",
        },
        {
            "pillar": "p2", "num": "02",
            "href": "https://suriota.com/ai-industrial-analytics/",
            "title": "AI &amp; Industrial Analytics",
            "desc": "Predictive maintenance, OEE dashboards, computer-vision QC, and real-time operational intelligence. Turning raw machine data into actionable plant-floor decisions.",
        },
        {
            "pillar": "p3", "num": "03",
            "href": "https://suriota.com/digital-transformation-consulting/",
            "title": "Digital Transformation Consulting",
            "desc": "Industry 4.0 roadmap, OT/IT convergence assessment, IIoT readiness audit, SCADA modernization, and cloud migration strategy for Indonesian manufacturers.",
        },
        {
            "pillar": "p4", "num": "04",
            "href": "https://suriota.com/industrial-engineering-automation/",
            "title": "Industrial Engineering &amp; Automation",
            "desc": "PLC integration, SCADA modernization, Solar PV PLTS design, hybrid PLTS-PLTB systems, and smart street light (PJU). Turnkey industrial energy transition.",
        },
        {
            "pillar": "p5", "num": "05",
            "href": "https://suriota.com/surge-saas-platform/",
            "title": "SURGE SaaS Platform",
            "desc": "SURGE multi-tenant IoT platform. Energy Mapping (kWh, power factor), Water Analytic (KLHK SPARING compliance), Vessel Tracking (fleet + fuel monitoring).",
        },
    ],
    "id": [
        {
            "pillar": "p1", "num": "01",
            "href": "https://suriota.com/id/iot-industri-integrasi-sistem/",
            "title": "IoT Industri &amp; Integrasi Sistem",
            "desc": "IoT Industri menyeluruh. Gateway Modbus, MQTT, edge computing, SCADA, dan pipeline sensor-ke-cloud dengan keamanan IEC 62443 untuk manufaktur, oil &amp; gas, serta operasi maritim.",
        },
        {
            "pillar": "p2", "num": "02",
            "href": "https://suriota.com/id/ai-analitik-industri/",
            "title": "AI &amp; Analitik Industri",
            "desc": "Predictive maintenance, dashboard OEE, computer-vision QC, dan intelligence operasional real-time. Mengubah data mesin menjadi keputusan plant-floor yang actionable.",
        },
        {
            "pillar": "p3", "num": "03",
            "href": "https://suriota.com/id/konsultasi-transformasi-digital/",
            "title": "Konsultasi Transformasi Digital",
            "desc": "Roadmap Industry 4.0, assessment konvergensi OT/IT, audit kesiapan IIoT, modernisasi SCADA, dan strategi migrasi cloud untuk manufaktur Indonesia.",
        },
        {
            "pillar": "p4", "num": "04",
            "href": "https://suriota.com/id/teknik-industri-otomasi/",
            "title": "Teknik Industri &amp; Otomasi",
            "desc": "Integrasi PLC, modernisasi SCADA, desain Solar PV PLTS, sistem hybrid PLTS-PLTB, dan smart street light (PJU). Transisi energi industri turnkey.",
        },
        {
            "pillar": "p5", "num": "05",
            "href": "https://suriota.com/id/platform-saas-surge/",
            "title": "Platform SaaS SURGE",
            "desc": "Platform IoT multi-tenant SURGE. Energy Mapping (kWh, power factor), Water Analytic (compliance SPARING KLHK), Vessel Tracking (armada + monitoring bahan bakar).",
        },
    ],
    "zh": [
        {
            "pillar": "p1", "num": "01",
            "href": "https://suriota.com/zh/gongye-wulianwang-jicheng/",
            "title": "工业物联网与系统集成",
            "desc": "端到端工业物联网。Modbus 网关、MQTT、边缘计算、SCADA、传感器到云端数据管道，符合 IEC 62443 安全标准，适用于制造业、石油天然气及海事运营。",
        },
        {
            "pillar": "p2", "num": "02",
            "href": "https://suriota.com/zh/ai-gongye-fenxi/",
            "title": "AI 与工业分析",
            "desc": "预测性维护、OEE 仪表盘、计算机视觉质检及实时运营洞察。将原始机器数据转化为可执行的车间决策。",
        },
        {
            "pillar": "p3", "num": "03",
            "href": "https://suriota.com/zh/shuzihua-zhuanxing-zixun/",
            "title": "数字化转型咨询",
            "desc": "工业 4.0 路线图、OT/IT 融合评估、IIoT 准备度审计、SCADA 现代化升级与云迁移战略，专为印尼制造业打造。",
        },
        {
            "pillar": "p4", "num": "04",
            "href": "https://suriota.com/zh/gongye-gongcheng-zidonghua/",
            "title": "工业工程与自动化",
            "desc": "PLC 集成、SCADA 现代化升级、太阳能光伏 PLTS 设计、PLTS-PLTB 混合系统及智能路灯 (PJU)。工业能源转型一站式方案。",
        },
        {
            "pillar": "p5", "num": "05",
            "href": "https://suriota.com/zh/surge-saas-pingtai/",
            "title": "SURGE SaaS 平台",
            "desc": "SURGE 多租户物联网平台。能源监测 (千瓦时、功率因数), 水质分析 (KLHK SPARING 合规), 船舶追踪 (船队+燃油监控).",
        },
    ],
}


def _card_html(c: dict) -> str:
    accent = ACCENT[c["pillar"]]
    svg = SVG[c["pillar"]]
    delay = (int(c["num"]) - 1) * 100
    delay_attr = f' data-d="{delay}"' if delay else ""
    # aria-label without HTML entities (decode &amp; → &)
    aria = c["title"].replace("&amp;", "&")
    return (
        f'\n    <a class="about-service-card-link" href="{c["href"]}" '
        f'aria-label="{aria}" style="text-decoration:none;">\n'
        f'      <article class="about-service-card sx-reveal"{delay_attr} '
        f'style="position:relative;height:100%;background:#FAFBFC;border:1px solid #E8ECEE;'
        f'border-radius:8px;padding:22px 18px 20px;display:flex;flex-direction:column;text-align:left;">\n'
        f'        <span class="sx-card-num" '
        f'style="position:static;display:block;font-family:&apos;Geist Mono&apos;,monospace;'
        f'font-size:11px;font-weight:500;letter-spacing:1px;color:#C8851F;margin-bottom:6px;">{c["num"]}</span>\n'
        f'        <svg width="26" height="26" viewBox="0 0 24 24" fill="none" '
        f'stroke="{accent}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" '
        f'style="margin:4px 0 12px;" aria-hidden="true">{svg}</svg>\n'
        f'        <h3 style="font-family:&apos;Geist&apos;,sans-serif;font-size:15px;font-weight:600;'
        f'color:#0E3942;margin:0 0 6px;letter-spacing:-0.2px;line-height:1.25;">{c["title"]}</h3>\n'
        f'        <p style="font-size:13px;color:#5B6F75;line-height:1.55;margin:0;flex:1;">{c["desc"]}</p>\n'
        f'      </article>\n'
        f'    </a>'
    )


def build_editor_html(lang: str) -> str:
    cards_html = "".join(_card_html(c) for c in CARDS[lang])
    return (
        '<div style="max-width:1100px;margin:0 auto;">\n'
        '  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;">\n'
        f'{cards_html}\n'
        '  </div>\n'
        '</div>'
    )


def find_and_replace(el: dict, target_id: str, new_html: str) -> bool:
    if el.get("id") == target_id and el.get("widgetType") == "text-editor":
        el.setdefault("settings", {})["editor"] = new_html
        return True
    for c in el.get("elements", []) or []:
        if find_and_replace(c, target_id, new_html):
            return True
    return False


def patch(session, lang: str, pid: int) -> None:
    r = session.get(f"{WP_BASE}/wp-json/wp/v2/pages/{pid}?context=edit", timeout=30)
    r.raise_for_status()
    body = r.json()
    meta = body.get("meta") or {}
    raw = meta.get("_elementor_data") or "[]"
    sections = json.loads(raw) if isinstance(raw, str) else raw
    new_html = build_editor_html(lang)
    found = False
    for sec in sections:
        if find_and_replace(sec, WIDGET_ID, new_html):
            found = True
            break
    if not found:
        sys.exit(f"FAIL {lang}/{pid}: widget {WIDGET_ID} not found")
    payload = {"meta": {"_elementor_data": json.dumps(sections, ensure_ascii=False)}}
    r2 = session.post(f"{WP_BASE}/wp-json/wp/v2/pages/{pid}", json=payload, timeout=30)
    if r2.status_code >= 300:
        sys.exit(f"FAIL POST {lang}/{pid}: {r2.status_code} {r2.text[:300]}")
    print(f"OK patched {lang} home (id {pid}) — 5 cards reordered+repointed")


if __name__ == "__main__":
    sess = make_session()
    for lang, pid in [("en", 12), ("id", 5273), ("zh", 5448)]:
        patch(sess, lang, pid)
