"""Playwright screenshots (desktop + mobile) of a pillar URL.

Stores snapshots under audit/pillar-v2-snapshots/<label>/<post_id>-<viewport>.png.
"""
from __future__ import annotations
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

from pillar_env import ROOT, assert_allowed

URL_BY_ID = {
    5554: "https://suriota.com/industrial-iot-system-integration/",
    5555: "https://suriota.com/ai-industrial-analytics/",
    5556: "https://suriota.com/digital-transformation-consulting/",
    5557: "https://suriota.com/industrial-engineering-automation/",
    5558: "https://suriota.com/surge-saas-platform/",
    5566: "https://suriota.com/id/iot-industri-integrasi-sistem/",
    5567: "https://suriota.com/id/ai-analitik-industri/",
    5568: "https://suriota.com/id/konsultasi-transformasi-digital/",
    5569: "https://suriota.com/id/teknik-industri-otomasi/",
    5570: "https://suriota.com/id/platform-saas-surge/",
    5571: "https://suriota.com/zh/gongye-wulianwang-jicheng/",
    5572: "https://suriota.com/zh/ai-gongye-fenxi/",
    5573: "https://suriota.com/zh/shuzihua-zhuanxing-zixun/",
    5574: "https://suriota.com/zh/gongye-gongcheng-zidonghua/",
    5575: "https://suriota.com/zh/surge-saas-pingtai/",
}


def snap(post_id: int, label: str) -> None:
    assert_allowed(post_id)
    url = URL_BY_ID[post_id]
    out_dir = ROOT / "audit" / "pillar-v2-snapshots" / label
    out_dir.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        for vp, name in [
            ({"width": 1440, "height": 900}, "desktop"),
            ({"width": 390, "height": 844}, "mobile"),
        ]:
            ctx = browser.new_context(viewport=vp, device_scale_factor=2)
            page = ctx.new_page()
            page.goto(url, wait_until="networkidle", timeout=60000)
            page.wait_for_timeout(800)
            page.screenshot(
                path=str(out_dir / f"{post_id}-{name}.png"),
                full_page=True,
            )
            ctx.close()
        browser.close()
    print(f"OK snapshots saved for {post_id} -> {label}/")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit("usage: python tools/py/pillar_snapshot.py <post_id> <before|after>")
    snap(int(sys.argv[1]), sys.argv[2])
