"""MED batch A:
1. Update AIOSEO Schema global: phone, email, foundingDate, numberOfEmployees
2. Add robots.txt rule: Disallow /?s=
3. Patch snippet 5524 to inject x-default hreflang on homepage triad
"""
import os
import requests, json
from requests.auth import HTTPBasicAuth

AUTH = HTTPBasicAuth("admin", os.environ.get("WP_APP_PASS", ""))
OPTIONS = "https://suriota.com/wp-json/aioseo/v1/options"
SNIPPET = "https://suriota.com/wp-json/wp/v2/elementor_snippet"

# ===== 1. Update AIOSEO Schema global =====
print("=== 1. AIOSEO Schema fields ===")
payload = {
    "options": {
        "searchAppearance": {
            "global": {
                "schema": {
                    "phone": "+62858-3567-2476",
                    "email": "admin@suriota.com",
                    "foundingDate": "2021-01-01",
                    "numberOfEmployees": {
                        "isRange": True,
                        "from": 10,
                        "to": 25,
                        "number": 0
                    }
                }
            }
        }
    }
}
r = requests.post(OPTIONS, auth=AUTH, json=payload, timeout=30)
print(f"  status={r.status_code}  body_head={r.text[:200]}")

# ===== 2. Robots.txt rules =====
print("\n=== 2. Robots.txt enable + add Disallow /?s= ===")
robots_payload = {
    "options": {
        "tools": {
            "robots": {
                "enable": True,
                "rules": [
                    {"userAgents": ["*"], "rule": "disallow", "directoryPath": "/?s=", "fieldHash": ""},
                    {"userAgents": ["*"], "rule": "disallow", "directoryPath": "/search/", "fieldHash": ""}
                ]
            }
        }
    }
}
r = requests.post(OPTIONS, auth=AUTH, json=robots_payload, timeout=30)
print(f"  status={r.status_code}  body_head={r.text[:200]}")

# ===== 3. Patch snippet 5524 to add x-default for homepage triad =====
print("\n=== 3. Fetch snippet 5524 current code ===")
r = requests.get(f"{SNIPPET}/5524?context=edit", auth=AUTH, timeout=30)
data = r.json()
current_code = data['meta']['_elementor_code']
print(f"  current length: {len(current_code)}")
print(f"  has x-default: {'x-default' in current_code}")
# Skip the actual update here for now; print so we can decide
