"""Upload compressed isolated-poster as new media, then update homepage references."""
import os
import requests, io
from PIL import Image
from requests.auth import HTTPBasicAuth

AUTH = HTTPBasicAuth("admin", os.environ.get("WP_APP_PASS", ""))
MEDIA = "https://suriota.com/wp-json/wp/v2/media"
PAGES = "https://suriota.com/wp-json/wp/v2/pages"

# Load the locally-saved compressed file
with open("C:/Users/Administrator/Music/Website Suriota/isolated-poster-compressed.webp", "rb") as f:
    new_bytes = f.read()
print(f"Compressed size: {len(new_bytes)} bytes")

# Upload as new media
print("\nUploading as new media...")
headers = {
    "Content-Type": "image/webp",
    "Content-Disposition": 'attachment; filename="isolated-poster-v2.webp"'
}
r = requests.post(MEDIA, auth=AUTH, data=new_bytes, headers=headers, timeout=60)
print(f"Status: {r.status_code}")
if r.status_code not in (200, 201):
    print(r.text[:500])
    raise SystemExit(1)
d = r.json()
new_id = d['id']
new_url = d['source_url']
print(f"New media id: {new_id}")
print(f"New URL: {new_url}")
print(f"Size: {d.get('media_details',{}).get('filesize')}")

# Set alt text
requests.post(f"{MEDIA}/{new_id}", auth=AUTH, json={
    "alt_text": "Isolated industrial gateway poster — Modbus, Pacific Network"
}, timeout=30)

# Now update homepage references
print("\nUpdating homepage Elementor data references...")
old_filename = "isolated-poster.webp"
new_filename = new_url.split("/")[-1]
print(f"  Replace: {old_filename} -> {new_filename}")

pr = requests.get(f"{PAGES}/12", auth=AUTH, params={"context": "edit", "_fields": "id,meta"}, timeout=30)
elem = pr.json()['meta']['_elementor_data']
count_before = elem.count(old_filename)
print(f"  Occurrences in homepage data: {count_before}")

if count_before > 0:
    new_elem = elem.replace(old_filename, new_filename)
    new_count = new_elem.count(new_filename)
    print(f"  After replace: {new_count} occurrences of {new_filename}")
    rp = requests.post(f"{PAGES}/12", auth=AUTH, json={"meta": {"_elementor_data": new_elem}}, timeout=60)
    print(f"  PATCH status: {rp.status_code}")
else:
    print("  No reference to old file in homepage; nothing to update")

# Also check Elementor data on other top pages
print("\nChecking other pages for references...")
all_pages_r = requests.get(f"{PAGES}?per_page=100&_fields=id,slug", auth=AUTH, timeout=30)
all_pages = all_pages_r.json()
hits = []
for p in all_pages:
    if p['id'] == 12:
        continue
    pr2 = requests.get(f"{PAGES}/{p['id']}", auth=AUTH, params={"context": "edit", "_fields": "id,slug,meta"}, timeout=30)
    if pr2.status_code != 200:
        continue
    try:
        em = pr2.json().get('meta', {}).get('_elementor_data', '')
    except Exception:
        continue
    if isinstance(em, str) and old_filename in em:
        hits.append((p['id'], p['slug'], em.count(old_filename)))
print(f"Other pages referencing {old_filename}: {len(hits)}")
for pid, slug, count in hits:
    print(f"  page {pid} ({slug}): {count} occurrences")
