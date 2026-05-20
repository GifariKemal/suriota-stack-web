"""Dump remaining EN strings per ZH page for translation-map extension."""
from __future__ import annotations
import base64, json, re, sys, urllib.request
sys.stdout.reconfigure(encoding="utf-8")

AUTH = base64.b64encode(b"admin:hCYK JqF1 khdB WDzI LQdQ WEBr").decode()
H = {"Authorization": f"Basic {AUTH}", "User-Agent": "Mozilla/5.0", "Accept": "application/json"}

ZH = {5448:"shouye",5450:"guanyu-women",5451:"zidonghua",5452:"dianqi-gongcheng",
      5453:"kezaisheng-nengyuan",5454:"anli",5456:"modbus-gateway",5457:"shuichuli",
      5461:"iso-m485",5463:"pm1611-wd-2",5465:"lianxi",5466:"yinsi-zhengce",
      5467:"fuwu-tiaokuan",5468:"iot",5469:"xitong-jicheng",5470:"shuzihua-zixun",
      5471:"rengong-zhineng",5472:"shujufenxi",5473:"saas"}

TR_KEYS = {"title","subtitle","heading","subheading","description","text","editor","html",
           "label","button_text","field_label","placeholder","tab_title","tab_content",
           "title_text","sub_text","after_text","before_text","highlighted_text",
           "rotating_text","link_text","icon_text","tooltip","caption","alt","content",
           "header_label"}
SKIP = {"url","link","image","background_image","background_video_link"}

def fetch(pid):
    req = urllib.request.Request(f"https://suriota.com/wp-json/wp/v2/pages/{pid}?context=edit", headers=H)
    return json.loads(urllib.request.urlopen(req, timeout=30).read())

def collect(n, out):
    if isinstance(n, dict):
        for k, v in n.items():
            if k in SKIP: continue
            if isinstance(v, str):
                if (k in TR_KEYS or k.endswith("_text") or k.endswith("_title")) and v:
                    if not re.search(r"[\u4e00-\u9fff]", v) and re.search(r"[A-Za-z]{3,}", v):
                        out.append((k, v.strip()))
            elif isinstance(v, (dict, list)):
                collect(v, out)
    elif isinstance(n, list):
        for x in n: collect(x, out)

for pid, slug in ZH.items():
    page = fetch(pid)
    raw = (page.get("meta") or {}).get("_elementor_data") or ""
    try:
        data = json.loads(raw) if isinstance(raw, str) else raw
    except Exception:
        print(f"\n## {pid} {slug} — JSON INVALID"); continue
    out = []
    collect(data, out)
    if not out:
        continue
    print(f"\n## {pid} {slug} — {len(out)} residual")
    seen = set()
    for k, v in out:
        key = v[:120]
        if key in seen: continue
        seen.add(key)
        print(f"  [{k}] {v[:200]}")
