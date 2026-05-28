"""Phase 4: apply robots_noindex + sitemap_exclude on 9 legacy slug pages."""
import os
import requests
from requests.auth import HTTPBasicAuth

AUTH = HTTPBasicAuth("admin", os.environ.get("WP_APP_PASS", ""))
AIOSEO = "https://suriota.com/wp-json/aioseo/v1/post"

legacy_pages = [
    (945,  "water-treatment"),
    (39,   "renewable-energy"),
    (35,   "automation"),
    (37,   "electrical"),
    (5029, "internet-of-things"),
    (5035, "artificial-intelligence"),
    (5039, "software-as-a-service"),
    (5037, "data-analytics"),
    (5033, "digital-consulting"),
]

for pid, slug in legacy_pages:
    payload = {
        "id": pid,
        "robots_default": False,
        "robots_noindex": True,
        "robots_nofollow": False,
        "sitemap_exclude": True
    }
    r = requests.post(AIOSEO, auth=AUTH, json=payload, timeout=30)
    print(f"  {slug:30s} id={pid:5d}  status={r.status_code}  body={r.text[:80]}")
