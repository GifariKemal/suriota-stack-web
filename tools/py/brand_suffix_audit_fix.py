"""Audit + fix: append ' | SURIOTA' brand suffix to AIOSEO titles where missing.
Skip: pages already containing SURIOTA, noindex pages, pages whose title is just a brand-only token."""
import os
import requests, re
from requests.auth import HTTPBasicAuth

AUTH = HTTPBasicAuth("admin", os.environ.get("WP_APP_PASS", ""))
PAGES = "https://suriota.com/wp-json/wp/v2/pages"
AIOSEO = "https://suriota.com/wp-json/aioseo/v1/post"

# Fetch all pages
print("Fetching all pages...")
all_pages = requests.get(f"{PAGES}?per_page=100&_fields=id,slug,title,link", auth=AUTH, timeout=30).json()
print(f"Total: {len(all_pages)}")

# Pages that should be skipped (noindexed in earlier batches)
NOINDEXED = {945, 39, 35, 37, 5029, 5035, 5039, 5037, 5033,  # EN legacy
             5277, 5278, 5281, 5282, 5283, 5284, 5285, 5286, 5381,  # ID legacy
             5457, 5453, 5451, 5452, 5468, 5471, 5472, 5473, 5470}  # ZH legacy

missing_suffix = []
already_has = []
skipped = []

for p in all_pages:
    if p['id'] in NOINDEXED:
        skipped.append((p['id'], p['slug'], 'noindexed'))
        continue
    # Fetch live rendered <title>
    try:
        html = requests.get(p['link'], timeout=15).text
    except Exception as e:
        skipped.append((p['id'], p['slug'], f'fetch_error: {e}'))
        continue
    m = re.search(r'<title[^>]*>([^<]+)</title>', html)
    if not m:
        skipped.append((p['id'], p['slug'], 'no_title'))
        continue
    title = m.group(1).strip()
    # Decode HTML entities for accurate check
    title_decoded = title.replace('&#8211;','-').replace('&#8212;','—').replace('&amp;','&').replace('&#039;',"'")
    has_brand = 'SURIOTA' in title_decoded.upper()
    if has_brand:
        already_has.append((p['id'], p['slug'], title))
    else:
        missing_suffix.append((p['id'], p['slug'], title, p['link']))

print(f"\nMissing brand suffix: {len(missing_suffix)}")
print(f"Already has brand: {len(already_has)}")
print(f"Skipped: {len(skipped)}")

# Show the missing list
print("\n=== Pages missing 'SURIOTA' suffix ===")
for pid, slug, title, link in missing_suffix[:30]:
    print(f"  {pid:5d}  {slug[:35]:35s}  title={title[:60]!r}")

# Patch each: append ' | SURIOTA' to AIOSEO title
# Strategy: fetch current AIOSEO title (from window.aioseo.currentPost.title),
# but we don't have that endpoint exposed easily. Instead use AIOSEO POST endpoint
# which accepts "title" field. Set it to current title + " | SURIOTA".
print("\n=== Applying brand suffix ===")
SUFFIX = " | SURIOTA"
ok = 0
fail = 0
for pid, slug, title, link in missing_suffix:
    # New title: append suffix unless already exists
    if 'SURIOTA' in title.upper():
        continue
    # Strip trailing separators if present
    new_title = re.sub(r'\s*[|—\-–]\s*$', '', title).strip() + SUFFIX
    payload = {"id": pid, "title": new_title}
    r = requests.post(AIOSEO, auth=AUTH, json=payload, timeout=30)
    marker = "[+]" if r.status_code == 200 else "[!]"
    print(f"  {marker} {r.status_code} id={pid:5d}  new_title={new_title[:70]!r}")
    if r.status_code == 200:
        ok += 1
    else:
        fail += 1
        print(f"     body: {r.text[:200]}")
print(f"\nSummary: {ok} OK, {fail} FAIL, total {len(missing_suffix)}")
