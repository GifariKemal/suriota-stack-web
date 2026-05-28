"""Phase 4 extension: noindex + sitemap_exclude 18 ID/ZH legacy slug pages
(translations of the 9 EN legacy slugs we already noindexed)."""
import os
import requests
from requests.auth import HTTPBasicAuth

AUTH = HTTPBasicAuth("admin", os.environ.get("WP_APP_PASS", ""))
AIOSEO = "https://suriota.com/wp-json/aioseo/v1/post"

pages = [
    # ID variants
    (5277, "id/water-treatment-id"),
    (5278, "id/saas-id"),
    (5281, "id/electrical-id"),
    (5282, "id/automation-id"),
    (5283, "id/renewable-energy-id"),
    (5284, "id/internet-of-things-id"),
    (5285, "id/data-analytics-id"),
    (5286, "id/digital-consulting-id"),
    (5381, "id/artificial-intelligence-id"),
    # ZH variants
    (5457, "zh/shuichuli"),
    (5453, "zh/kezaisheng-nengyuan"),
    (5451, "zh/zidonghua"),
    (5452, "zh/dianqi-gongcheng"),
    (5468, "zh/iot"),
    (5471, "zh/rengong-zhineng"),
    (5472, "zh/shujufenxi"),
    (5473, "zh/saas"),
    (5470, "zh/shuzihua-zixun"),
]

ok = 0
for pid, slug in pages:
    payload = {"id": pid, "robots_default": False, "robots_noindex": True, "sitemap_exclude": True}
    r = requests.post(AIOSEO, auth=AUTH, json=payload, timeout=30)
    status = "[+]" if r.status_code == 200 else "[!]"
    print(f"  {status} {r.status_code} id={pid}  {slug}")
    if r.status_code == 200:
        ok += 1
print(f"\nSummary: {ok}/{len(pages)} OK")
