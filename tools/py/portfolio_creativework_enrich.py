"""Enrich Portfolio CreativeWork items with `creator: {@id: #organization}` and `url`.
The 10 CreativeWork items in /portfolio/ ItemList have only name + description + dateCreated.
Add provider/creator ref to link back to SURIOTA in graph."""
import os
import requests, re
from requests.auth import HTTPBasicAuth

AUTH = HTTPBasicAuth("admin", os.environ.get("WP_APP_PASS", ""))
PORTFOLIO = "https://suriota.com/wp-json/wp/v2/pages/839"

r = requests.get(f"{PORTFOLIO}?context=edit&_fields=id,meta", auth=AUTH, timeout=30)
elem = r.json()['meta']['_elementor_data']
print(f"Original len: {len(elem)}")

# The escaped substring to find:
# ,"dateCreated":"2025"}},
# Replace with:
# ,"dateCreated":"2025","creator":{"@id":"https:\/\/suriota.com\/#organization"},"url":"https:\/\/suriota.com\/portfolio\/"}},

# Pattern: find each CreativeWork closing pattern. The escaped form in elementor_data has \" instead of "
# Look for: \"dateCreated\":\"YYYY\"}}
# Replace by inserting creator + url before }} closing

patterns_replaced = 0
for year in ["2025", "2024", "2023"]:
    old = f'\\"dateCreated\\":\\"{year}\\"}}}}'
    new = f'\\"dateCreated\\":\\"{year}\\",\\"creator\\":{{\\"@id\\":\\"https:\\/\\/suriota.com\\/#organization\\"}},\\"url\\":\\"https:\\/\\/suriota.com\\/portfolio\\/\\"}}}}'
    cnt = elem.count(old)
    if cnt > 0:
        elem = elem.replace(old, new)
        patterns_replaced += cnt
        print(f"  Year {year}: replaced {cnt} items")

print(f"\nTotal items enriched: {patterns_replaced}")
print(f"New len: {len(elem)}")
print(f"Contains \\\"creator\\\": {elem.count(chr(92)+chr(34)+'creator'+chr(92)+chr(34))} times")

# Save back
rp = requests.post(PORTFOLIO, auth=AUTH, json={"meta": {"_elementor_data": elem}}, timeout=60)
print(f"PATCH status: {rp.status_code}")
if rp.status_code != 200:
    print(rp.text[:400])
