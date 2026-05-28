"""Collapse 4 redirect chains. Redirection plugin requires PUT with full payload."""
import os
import requests
from requests.auth import HTTPBasicAuth

AUTH = HTTPBasicAuth("admin", os.environ.get("WP_APP_PASS", ""))
BASE = "https://suriota.com/wp-json/redirection/v1/redirect"

chain_fixes = [
    (43, "/water-treatment-services/", "/ai-industrial-analytics/"),
    (42, "/renewable-energy-services/", "/industrial-engineering-automation/"),
    (41, "/automation-services/", "/digital-transformation-consulting/"),
    (40, "/electrical-services/", "/industrial-iot-system-integration/"),
]

for rid, src, new_target in chain_fixes:
    # Full payload with all required fields
    payload = {
        "id": rid,
        "url": src,
        "action_code": 301,
        "action_type": "url",
        "action_data": {"url": new_target},
        "match_type": "url",
        "group_id": 1,
        "title": f"SX: {src.strip('/')} -> {new_target} (collapsed chain)"
    }
    r = requests.post(f"{BASE}/{rid}", auth=AUTH, json=payload, timeout=30)
    print(f"  id={rid} {src} -> {new_target}  status={r.status_code}")
    if r.status_code != 200:
        print(f"     body: {r.text[:300]}")
