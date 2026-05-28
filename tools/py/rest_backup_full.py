"""REST-based backup of critical suriota.com data: snippets, pages, posts, redirects, AIOSEO options.
Output: backups/2026-05-28/<type>.json"""
import os
import requests, json, os
from datetime import datetime
from requests.auth import HTTPBasicAuth

AUTH = HTTPBasicAuth("admin", os.environ.get("WP_APP_PASS", ""))
BASE = "https://suriota.com/wp-json"
TS = datetime.now().strftime("%Y-%m-%d")
OUT_DIR = f"C:/Users/Administrator/Music/Website Suriota/backups/{TS}"
os.makedirs(OUT_DIR, exist_ok=True)

def fetch_all_paginated(url, name):
    """Fetch all pages of a paginated REST endpoint."""
    all_items = []
    page = 1
    while True:
        sep = '&' if '?' in url else '?'
        r = requests.get(f"{url}{sep}per_page=100&page={page}", auth=AUTH, timeout=60)
        if r.status_code == 400 and page > 1:
            break
        if r.status_code != 200:
            print(f"  [{name}] page {page} failed: {r.status_code}")
            break
        items = r.json()
        if not isinstance(items, list):
            print(f"  [{name}] non-list response, aborting pagination")
            break
        if not items:
            break
        all_items.extend(items)
        if len(items) < 100:
            break
        page += 1
    return all_items

def save(name, data):
    path = f"{OUT_DIR}/{name}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    size = os.path.getsize(path)
    print(f"  [+] {name}: {size:>10} bytes  ({len(data) if isinstance(data,list) else 'object'})")

print(f"Backup target dir: {OUT_DIR}\n")

# 1. Elementor snippets (custom HTML/CSS/JS overlays)
print("1. Elementor snippets...")
snippets = fetch_all_paginated(f"{BASE}/wp/v2/elementor_snippet?context=edit", "snippets")
save("elementor_snippets", snippets)

# 2. Pages (with full Elementor data)
print("2. Pages (with _elementor_data)...")
pages = fetch_all_paginated(f"{BASE}/wp/v2/pages?context=edit", "pages")
save("pages", pages)

# 3. Posts (with content)
print("3. Posts (with content)...")
posts = fetch_all_paginated(f"{BASE}/wp/v2/posts?context=edit", "posts")
save("posts", posts)

# 4. Redirects (Redirection plugin)
print("4. Redirects...")
r = requests.get(f"{BASE}/redirection/v1/redirect?per_page=200", auth=AUTH, timeout=30)
if r.status_code == 200:
    save("redirects", r.json())

# 5. AIOSEO global options
print("5. AIOSEO options...")
r = requests.get(f"{BASE}/aioseo/v1/options", auth=AUTH, timeout=30)
if r.status_code == 200:
    save("aioseo_options", r.json())

# 6. Media library metadata (no actual files, just URLs + alt text + meta)
print("6. Media library metadata...")
media = fetch_all_paginated(f"{BASE}/wp/v2/media?_fields=id,slug,source_url,alt_text,title,media_details,date,mime_type", "media")
save("media_metadata", media)

# 7. Plugins list
print("7. Plugins...")
r = requests.get(f"{BASE}/wp/v2/plugins", auth=AUTH, timeout=30)
if r.status_code == 200:
    save("plugins", r.json())

# 8. Themes list
print("8. Themes...")
r = requests.get(f"{BASE}/wp/v2/themes", auth=AUTH, timeout=30)
if r.status_code == 200:
    save("themes", r.json())

# 9. Polylang languages + translations (if exposed)
print("9. Polylang language taxonomy terms...")
r = requests.get(f"{BASE}/wp/v2/language?per_page=20", auth=AUTH, timeout=30)
if r.status_code == 200:
    save("polylang_languages", r.json())

print(f"\nBackup complete: {OUT_DIR}")
total_size = sum(os.path.getsize(f"{OUT_DIR}/{f}") for f in os.listdir(OUT_DIR))
print(f"Total size: {total_size / 1024 / 1024:.2f} MB")
