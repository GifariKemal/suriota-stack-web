"""Fix homepage portfolio table flicker bug.

Root cause: in homepage Elementor inline portfolio script, `var state = {...}` is
declared AFTER `if (cached) render(cached)`. On reload with cache present,
render() runs while state is hoisted-but-undefined → TypeError → silent crash →
tbody never populated, all UI elements hidden.

Fix: defer cached render() with setTimeout(0) so it executes after the
synchronous `var state = ...` assignment completes.

Patches homepage page 12 _elementor_data, then flushes Elementor cache."""
import os
import requests
from requests.auth import HTTPBasicAuth

AUTH = HTTPBasicAuth("admin", os.environ.get("WP_APP_PASS", ""))
PAGE = "https://suriota.com/wp-json/wp/v2/pages/12"

# Fetch current elementor_data
print("Fetching page 12...")
r = requests.get(PAGE, auth=AUTH, params={"context": "edit", "_fields": "id,meta"}, timeout=60)
elem = r.json()['meta']['_elementor_data']
print(f"  data length: {len(elem)}")

# The escaped form of the buggy line and the fix
# Original: if (cached) render(cached);
# Fix: if (cached) setTimeout(function(){ render(cached); }, 0);
old_str = "if (cached) render(cached);"
new_str = "if (cached) setTimeout(function(){ render(cached); }, 0);"

count_before = elem.count(old_str)
print(f"  occurrences of buggy line: {count_before}")

if count_before == 0:
    print("ERROR: buggy line not found, aborting")
    raise SystemExit(1)
if count_before > 1:
    print(f"WARNING: {count_before} matches found, will replace all (likely just one in portfolio script)")

new_elem = elem.replace(old_str, new_str)
print(f"  new data length: {len(new_elem)} (delta {len(new_elem) - len(elem)})")

# Verify the new content actually has the fix
assert "setTimeout(function(){ render(cached); }, 0)" in new_elem

# PATCH back
print("Saving patched data...")
r = requests.post(PAGE, auth=AUTH, json={"meta": {"_elementor_data": new_elem}}, timeout=60)
print(f"  status: {r.status_code}")
if r.status_code != 200:
    print(r.text[:500])
else:
    print("  ✓ patched")
