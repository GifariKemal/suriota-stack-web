"""Update alt text for 20 partner logos in WP Media Library via REST API."""
import os
import requests
from requests.auth import HTTPBasicAuth
import sys

AUTH = HTTPBasicAuth("admin", os.environ.get("WP_APP_PASS", ""))
BASE = "https://suriota.com/wp-json/wp/v2/media"

MAPPING = {
    "1-1":  "Caterpillar logo",
    "2-1":  "PT Citra Lautan Teduh logo",
    "3-1":  "Santarli logo",
    "4-1":  "Anshun Travel logo",
    "5-1":  "PT Panbil Utilitas Sentosa logo",
    "6-1":  "Tirta Kepri logo",
    "7-1":  "PT Ably Metal Indonesia logo",
    "8-1":  "Trans Interior logo",
    "9-1":  "DAS Darmawan Antar Sarana logo",
    "10-1": "Sandifox logo",
    "11-1": "Amanah Komputer logo",
    "12-1": "Hijrah Travel logo",
    "13-1": "Papa Aii Group logo",
    "14-1": "Geulis logo",
    "15-1": "Avanti logo",
    "16-1": "Kelvi logo",
    "17-1": "Universitas Pendidikan Indonesia logo",
    "18-1": "Politeknik Negeri Batam logo",
    "smk":  "SMK Negeri 6 Batam logo",
    "uis":  "Universitas Ibnu Sina logo",
}

def find_media(slug):
    """Find media by exact slug match, then fall back to search."""
    r = requests.get(f"{BASE}?slug={slug}&per_page=10", auth=AUTH, timeout=20)
    if r.status_code == 200 and r.json():
        return r.json()[0]
    r = requests.get(f"{BASE}?search={slug}&per_page=20", auth=AUTH, timeout=20)
    if r.status_code != 200:
        return None
    items = r.json()
    for it in items:
        src = it.get("source_url", "")
        s = it.get("slug", "")
        if f"/{slug}." in src or s == slug or s.startswith(f"{slug}-"):
            return it
    return items[0] if items else None

def update_alt(mid, alt):
    r = requests.post(f"{BASE}/{mid}", auth=AUTH, json={"alt_text": alt}, timeout=20)
    return r.status_code, r.text[:200]

def main():
    results = []
    for slug, alt in MAPPING.items():
        m = find_media(slug)
        if not m:
            results.append((slug, None, "NOT_FOUND", ""))
            print(f"[X] {slug}: not found")
            continue
        mid = m["id"]
        old_alt = m.get("alt_text", "")
        src = m.get("source_url", "")
        if old_alt == alt:
            results.append((slug, mid, "UNCHANGED", old_alt))
            print(f"[=] {slug} (id={mid}): already '{alt}'")
            continue
        status, body = update_alt(mid, alt)
        results.append((slug, mid, status, src))
        marker = "+" if status == 200 else "!"
        print(f"[{marker}] {slug} (id={mid}, {status}): '{old_alt}' -> '{alt}'  src={src}")
    ok = sum(1 for r in results if r[2] == 200)
    unchanged = sum(1 for r in results if r[2] == "UNCHANGED")
    fail = len(results) - ok - unchanged
    print(f"\nSummary: {ok} updated, {unchanged} unchanged, {fail} failed (total {len(results)})")
    return 0 if fail == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
