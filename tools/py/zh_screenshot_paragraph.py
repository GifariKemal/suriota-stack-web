"""Screenshot the intro paragraph + '5 Core Services' eyebrow on EN/ID/ZH home.

Captures the section containing the text so we can compare visual rendering.
"""
from __future__ import annotations
import sys, time, pathlib
sys.stdout.reconfigure(encoding="utf-8")

from playwright.sync_api import sync_playwright

OUT = pathlib.Path(r"C:\Users\Administrator\Music\Website Suriota\screenshots\zh_paragraph")
OUT.mkdir(parents=True, exist_ok=True)

TARGETS = [
    ("en", "https://suriota.com/",        "5 Core Services"),
    ("id", "https://suriota.com/id/",     "5 Layanan Inti"),
    ("zh", "https://suriota.com/shouye/", "五大核心服务"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=2)
    for code, url, needle in TARGETS:
        page = ctx.new_page()
        page.goto(url, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(800)
        # Find the eyebrow text and screenshot a region around it
        try:
            loc = page.get_by_text(needle, exact=False).first
            loc.scroll_into_view_if_needed(timeout=10000)
            page.wait_for_timeout(400)
            # Capture from intro paragraph through eyebrow + first row of cards
            # Walk up to find a section/container element
            box = loc.bounding_box()
            if box:
                # Expand region: 600px up (to cover intro paragraph) and 200px down
                y = max(0, int(box["y"]) - 600)
                clip = {"x": 0, "y": y, "width": 1440, "height": min(900, int(box["y"]) - y + 240)}
                out = OUT / f"home_{code}_paragraph.png"
                page.screenshot(path=str(out), clip=clip)
                print(f"  {code}: {out}  (needle row y={int(box['y'])})")
            else:
                print(f"  {code}: bounding_box None")
        except Exception as e:
            print(f"  {code}: ERR {e}")
        page.close()
    browser.close()
print("DONE")
