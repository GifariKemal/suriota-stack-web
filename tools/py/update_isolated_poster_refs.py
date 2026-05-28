"""Update all remaining 5 pages referencing isolated-poster.webp → isolated-poster-v2.webp."""
import os
import requests
from requests.auth import HTTPBasicAuth

AUTH = HTTPBasicAuth("admin", os.environ.get("WP_APP_PASS", ""))
PAGES = "https://suriota.com/wp-json/wp/v2/pages"

old = "isolated-poster.webp"
new = "isolated-poster-v2.webp"

target_pages = [5461, 5448, 5291, 5273, 1740]
for pid in target_pages:
    r = requests.get(f"{PAGES}/{pid}", auth=AUTH, params={"context": "edit", "_fields": "id,slug,meta"}, timeout=30)
    if r.status_code != 200:
        print(f"[!] {pid}: GET failed {r.status_code}")
        continue
    d = r.json()
    em = d['meta']['_elementor_data']
    cnt_before = em.count(old)
    if cnt_before == 0:
        print(f"[=] {pid} ({d['slug']}): no occurrences")
        continue
    new_em = em.replace(old, new)
    rp = requests.post(f"{PAGES}/{pid}", auth=AUTH, json={"meta": {"_elementor_data": new_em}}, timeout=60)
    print(f"[{'+' if rp.status_code == 200 else '!'}] {pid} ({d['slug']}): replaced {cnt_before} -> status {rp.status_code}")
