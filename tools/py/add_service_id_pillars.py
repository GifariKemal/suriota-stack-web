"""For each pillar page, parse the inline Service JSON-LD inside _elementor_data,
add @id and replace verbose provider object with @id ref to #organization."""
import os
import requests, json, re, sys
from requests.auth import HTTPBasicAuth

AUTH = HTTPBasicAuth("admin", os.environ.get("WP_APP_PASS", ""))
BASE = "https://suriota.com/wp-json/wp/v2/pages"

# (page_id, expected_service_url_for_@id_root)
# @id = service_url + "#service"  (use page's actual canonical URL)
# We let the script derive @id from the existing "url" field inside the JSON-LD,
# so EN/ID/ZH variants all self-reference their own URL.

PILLAR_IDS = [
    # EN pillars
    5554,  # industrial-iot-system-integration
    934,   # suriota-modbus-gateway
    5558,  # surge-saas-platform
    5557,  # industrial-engineering-automation
    1542,  # surge-energy-mapping
]

# Provider canonical ref (universal across all languages)
ORG_REF = {"@id": "https://suriota.com/#organization"}

# Regex matching escaped JSON-LD <script> block inside Elementor data JSON string
SCRIPT_RE = re.compile(
    r'(<script type=\\"application/ld\+json\\">)(.*?)(</script>)',
    re.DOTALL,
)

def transform_block(escaped_inner: str) -> tuple[str, bool]:
    """Take the escaped JSON string between <script> tags, unescape, parse, modify, re-escape."""
    raw = escaped_inner.encode('utf-8').decode('unicode_escape')
    text = raw.strip()
    try:
        d = json.loads(text)
    except json.JSONDecodeError as e:
        print(f"   ! JSON parse error: {e}")
        return escaped_inner, False
    t = d.get("@type")
    if t != "Service":
        print(f"   ! @type is {t!r}, expected Service - skipping")
        return escaped_inner, False
    url = d.get("url", "").rstrip("/")
    if not url:
        print("   ! No url field - cannot derive @id, skipping")
        return escaped_inner, False
    new_id = f"{url}/#service"
    changed = False
    if d.get("@id") != new_id:
        new_d = {}
        for k, v in d.items():
            new_d[k] = v
            if k == "@type":
                new_d["@id"] = new_id
        d = new_d
        changed = True
    if d.get("provider") != ORG_REF:
        d["provider"] = ORG_REF
        changed = True
    if not changed:
        print("   = already up-to-date")
        return escaped_inner, False
    new_text = "\n" + json.dumps(d, indent=2, ensure_ascii=False) + "\n"
    new_escaped = json.dumps(new_text, ensure_ascii=False)[1:-1]
    return new_escaped, True

def process(pid):
    print(f"\n=== Page {pid} ===")
    r = requests.get(f"{BASE}/{pid}", auth=AUTH, params={"context": "edit", "_fields": "id,slug,meta"}, timeout=30)
    if r.status_code != 200:
        print(f"   GET failed: {r.status_code}")
        return False
    d = r.json()
    slug = d.get("slug", "")
    elem_raw = d.get("meta", {}).get("_elementor_data", "")
    if not elem_raw:
        print("   ! no _elementor_data")
        return False
    print(f"   slug: {slug}  | data len: {len(elem_raw)}")
    matches = list(SCRIPT_RE.finditer(elem_raw))
    print(f"   inline JSON-LD blocks: {len(matches)}")
    if not matches:
        return False
    new_elem = elem_raw
    any_change = False
    # Process in reverse to keep offsets valid
    for m in reversed(matches):
        prefix, inner, suffix = m.group(1), m.group(2), m.group(3)
        new_inner, changed = transform_block(inner)
        if changed:
            any_change = True
            new_elem = new_elem[:m.start()] + prefix + new_inner + suffix + new_elem[m.end():]
    if not any_change:
        print("   = no changes needed")
        return True
    # Save back
    payload = {"meta": {"_elementor_data": new_elem}}
    rp = requests.post(f"{BASE}/{pid}", auth=AUTH, json=payload, timeout=60)
    print(f"   PATCH status: {rp.status_code}")
    if rp.status_code != 200:
        print(rp.text[:400])
        return False
    # Verify
    rv = requests.get(f"{BASE}/{pid}", auth=AUTH, params={"context": "edit", "_fields": "id,meta"}, timeout=30)
    if rv.status_code == 200:
        verified = rv.json().get("meta",{}).get("_elementor_data","")
        if '"@id": "https://suriota.com/' in verified.replace("\\","") or "#service" in verified:
            print("   + verified @id present")
        else:
            print("   ? verification inconclusive")
    return True

def main():
    targets = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else PILLAR_IDS
    for pid in targets:
        process(pid)

if __name__ == "__main__":
    main()
