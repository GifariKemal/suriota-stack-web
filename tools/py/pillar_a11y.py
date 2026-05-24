"""axe-core a11y audit on a pillar URL via Playwright.

Writes JSON report to audit/pillar-v2-snapshots/a11y/<post_id>.json
and prints violation/serious-critical counts.
"""
from __future__ import annotations
import json
import sys
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

from pillar_env import ROOT, assert_allowed
from pillar_snapshot import URL_BY_ID

AXE_CDN = "https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.9.1/axe.min.js"


def audit(post_id: int) -> Path:
    assert_allowed(post_id)
    url = URL_BY_ID[post_id]
    axe = urllib.request.urlopen(AXE_CDN, timeout=20).read().decode("utf-8")
    out = ROOT / "audit" / "pillar-v2-snapshots" / "a11y" / f"{post_id}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(viewport={"width": 1440, "height": 900})
        page = ctx.new_page()
        page.goto(url, wait_until="networkidle", timeout=60000)
        page.add_script_tag(content=axe)
        result = page.evaluate("axe.run()")
        ctx.close()
        browser.close()
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    violations = result.get("violations", []) or []
    crit = sum(1 for v in violations if v.get("impact") in ("critical", "serious"))
    print(f"{post_id}: {len(violations)} violations ({crit} serious/critical) -> {out.relative_to(ROOT)}")
    if crit:
        for v in violations:
            if v.get("impact") in ("critical", "serious"):
                print(f"  - [{v['impact']}] {v['id']}: {v.get('help')}")
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("usage: python tools/py/pillar_a11y.py <post_id>")
    audit(int(sys.argv[1]))
