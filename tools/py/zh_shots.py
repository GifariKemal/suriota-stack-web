"""Screenshot intro paragraph EN/ID/ZH for visual comparison."""
from __future__ import annotations
import sys, pathlib
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright

OUT = pathlib.Path(r"C:\Users\Administrator\Music\Website Suriota\audit")
OUT.mkdir(parents=True, exist_ok=True)

TARGETS = [
    ("en", "https://suriota.com/",        "5 Core Services"),
    ("id", "https://suriota.com/id/",     "5 Layanan Inti"),
    ("zh", "https://suriota.com/shouye/", "五大核心服务"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    for code, url, needle in TARGETS:
        page = ctx.new_page()
        page.goto(url, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(800)
        try:
            loc = page.get_by_text(needle, exact=False).first
            loc.scroll_into_view_if_needed(timeout=10000)
            page.wait_for_timeout(500)
            box = loc.bounding_box()
            if box:
                y = max(0, int(box["y"]) - 500)
                h = min(900, int(box["y"]) - y + 200)
                out = OUT / f"_zh_shot_home_{code}.png"
                page.screenshot(path=str(out), clip={"x": 0, "y": y, "width": 1440, "height": h})
                print(f"  {code}: {out}")
            else:
                print(f"  {code}: no box")
        except Exception as e:
            print(f"  {code}: ERR {e}")
        page.close()
    browser.close()
print("DONE")
