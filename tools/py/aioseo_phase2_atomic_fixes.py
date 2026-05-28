"""AIOSEO Phase 2: atomic credibility fixes.
1. Fix /zh/yinsi-zhengce/ (5466) placeholder description
2. Strip duplicate SURIOTA suffix on 4 pages (5378, 5379, 5380, 5541)
3. Collapse 4 redirect chains (ids 40, 41, 42, 43)
4. Add 3 known 404 redirects (/blog/, /waste-water-loger/, /surge-energi-mapping-...)
"""
import os
import requests, json
from requests.auth import HTTPBasicAuth

AUTH = HTTPBasicAuth("admin", os.environ.get("WP_APP_PASS", ""))
PAGES = "https://suriota.com/wp-json/wp/v2/pages"
AIOSEO = "https://suriota.com/wp-json/aioseo/v1/post"
REDIRECT = "https://suriota.com/wp-json/redirection/v1/redirect"

results = []

# ===== 1. /zh/yinsi-zhengce/ description fix =====
print("=== 1. Fix /zh/yinsi-zhengce/ description ===")
zh_yinsi_desc = (
    "SURIOTA 隐私政策 — 我们如何收集、使用、存储和保护您在 suriota.com 上提交的个人信息。"
    "符合印尼数据保护法规，涵盖联系表单、Cookies、第三方分析与服务集成。"
)
r = requests.post(AIOSEO, auth=AUTH, json={
    "id": 5466,
    "description": zh_yinsi_desc
}, timeout=30)
print(f"  status={r.status_code}  len_desc={len(zh_yinsi_desc)}")
results.append(("zh-yinsi-desc", r.status_code))

# ===== 2. Strip duplicate SURIOTA in WP titles =====
print("\n=== 2. Strip duplicate SURIOTA from page titles ===")
title_fixes = [
    (5541, "实习计划"),       # was "实习计划 – SURIOTA"
    (5380, "Syarat Layanan"),  # was "Syarat Layanan — SURIOTA"
    (5379, "Kebijakan Privasi"),  # was "Kebijakan Privasi — SURIOTA"
    (5378, "Hubungi Kami"),    # was "Hubungi Kami — SURIOTA"
]
for pid, new_title in title_fixes:
    r = requests.post(f"{PAGES}/{pid}", auth=AUTH, json={"title": new_title}, timeout=30)
    d = r.json() if r.status_code == 200 else None
    actual = d['title']['raw'] if d else r.text[:200]
    print(f"  id={pid} status={r.status_code} new_title={actual!r}")
    results.append((f"title-{pid}", r.status_code))

# ===== 3. Collapse 4 redirect chains =====
print("\n=== 3. Collapse 4 redirect chains to single hop ===")
chain_fixes = [
    (43, "/ai-industrial-analytics/"),         # /water-treatment-services/
    (42, "/industrial-engineering-automation/"), # /renewable-energy-services/
    (41, "/digital-transformation-consulting/"), # /automation-services/
    (40, "/industrial-iot-system-integration/"), # /electrical-services/
]
for rid, new_target in chain_fixes:
    # Redirection plugin uses action_data.url + action_type=url
    r = requests.post(f"{REDIRECT}/{rid}", auth=AUTH, json={
        "action_data": {"url": new_target},
        "action_type": "url",
        "action_code": 301
    }, timeout=30)
    print(f"  redirect id={rid} -> {new_target}  status={r.status_code}")
    results.append((f"redirect-collapse-{rid}", r.status_code))

# ===== 4. Add 3 new redirects for known 404s =====
print("\n=== 4. Add 3 new redirects for known 404 paths ===")
new_redirects = [
    ("/blog/", "/artikel/", "Old blog path -> articles archive"),
    ("/waste-water-loger/", "/waste-water-logger/", "Typo fix"),
    ("/surge-energi-mapping-monitoring-control-daya-listrik/", "/surge-energy-mapping/", "Old ID slug bingbot still hits"),
]
for src, tgt, note in new_redirects:
    payload = {
        "url": src,
        "action_data": {"url": tgt},
        "action_type": "url",
        "action_code": 301,
        "match_type": "url",
        "group_id": 1,
        "title": note
    }
    r = requests.post(REDIRECT, auth=AUTH, json=payload, timeout=30)
    d = r.json() if r.status_code in (200, 201) else None
    new_id = d.get('items',[{}])[0].get('id', d.get('id','?')) if d else '?'
    print(f"  + {src} -> {tgt}  status={r.status_code}  new_id={new_id}")
    results.append((f"new-redirect-{src}", r.status_code))

print("\n=== Summary ===")
ok = sum(1 for _,s in results if s in (200, 201))
fail = sum(1 for _,s in results if s not in (200, 201))
print(f"OK: {ok}  FAIL: {fail}  TOTAL: {len(results)}")
for name, s in results:
    marker = "+" if s in (200, 201) else "!"
    print(f"  [{marker}] {s}  {name}")
