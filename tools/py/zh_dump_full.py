"""Dump full text of remaining EN strings (no truncation)."""
from __future__ import annotations
import base64, json, re, sys, urllib.request
sys.stdout.reconfigure(encoding="utf-8")

AUTH = base64.b64encode(b"admin:hCYK JqF1 khdB WDzI LQdQ WEBr").decode()
H = {"Authorization": f"Basic {AUTH}", "User-Agent": "Mozilla/5.0", "Accept": "application/json"}

TARGETS = [5448, 5450, 5452, 5453, 5457]
TR_KEYS = {"title","subtitle","heading","subheading","description","text","editor","html",
           "label","button_text","field_label","placeholder","tab_title","tab_content",
           "title_text","sub_text","after_text","before_text","highlighted_text",
           "rotating_text","link_text","icon_text","tooltip","caption","alt","content",
           "header_label"}
SKIP = {"url","link","image","background_image","background_video_link"}

def collect(n, out):
    if isinstance(n, dict):
        for k, v in n.items():
            if k in SKIP: continue
            if isinstance(v, str):
                if (k in TR_KEYS or k.endswith("_text") or k.endswith("_title")) and v:
                    if not re.search(r"[\u4e00-\u9fff]", v) and re.search(r"[A-Za-z]{3,}", v):
                        out.append((k, v))
            elif isinstance(v, (dict, list)):
                collect(v, out)
    elif isinstance(n, list):
        for x in n: collect(x, out)

for pid in TARGETS:
    req = urllib.request.Request(f"https://suriota.com/wp-json/wp/v2/pages/{pid}?context=edit", headers=H)
    page = json.loads(urllib.request.urlopen(req, timeout=30).read())
    raw = (page.get("meta") or {}).get("_elementor_data") or ""
    data = json.loads(raw)
    out = []
    collect(data, out)
    seen = set()
    print(f"\n## {pid}")
    for k, v in out:
        h = v[:60]
        if h in seen: continue
        seen.add(h)
        print(f"---KEY={k}---")
        print(v)
