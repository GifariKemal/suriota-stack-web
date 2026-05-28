"""Create snippet: CollectionPage + ItemList schema on /artikel/ URL (URL-conditional JS injection)."""
import os
import requests, json
from requests.auth import HTTPBasicAuth

AUTH = HTTPBasicAuth("admin", os.environ.get("WP_APP_PASS", ""))
SNIPPET = "https://suriota.com/wp-json/wp/v2/elementor_snippet"

# Fetch latest 20 posts for ItemList
posts_resp = requests.get(
    "https://suriota.com/wp-json/wp/v2/posts?per_page=20&_fields=id,slug,title,link,date",
    auth=AUTH, timeout=30
).json()

# Build ItemList items (just url + name + position)
item_list = []
for i, p in enumerate(posts_resp[:20], start=1):
    item_list.append({
        "@type": "ListItem",
        "position": i,
        "url": p['link'],
        "name": p['title']['rendered']
    })

schema = {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    "@id": "https://suriota.com/artikel/#collection",
    "name": "SURIOTA Articles — Industrial IoT, SCADA, Automation Case Studies",
    "description": "Latest case studies, technical articles, and project deployment notes from SURIOTA on Industrial IoT, SCADA, automation, energy mapping, and water treatment projects across Indonesia.",
    "url": "https://suriota.com/artikel/",
    "isPartOf": { "@id": "https://suriota.com/#website" },
    "about": { "@id": "https://suriota.com/#organization" },
    "inLanguage": "en-US",
    "mainEntity": {
        "@type": "ItemList",
        "name": "Latest Articles",
        "numberOfItems": len(item_list),
        "itemListElement": item_list
    }
}

schema_json = json.dumps(schema, ensure_ascii=False)

CODE = f'''<script>
(function(){{
  var p = location.pathname;
  if (p !== '/artikel/' && p !== '/artikel') return;
  var s = document.createElement('script');
  s.type = 'application/ld+json';
  s.textContent = {json.dumps(schema_json)};
  (document.head || document.documentElement).appendChild(s);
}})();
</script>
'''

payload = {
    "title": "SX / CollectionPage Schema (/artikel/)",
    "status": "publish",
    "meta": {
        "_elementor_location": "elementor_head",
        "_elementor_priority": 4,
        "_elementor_code": CODE
    }
}

r = requests.post(SNIPPET, auth=AUTH, json=payload, timeout=30)
print("Status:", r.status_code)
if r.status_code in (200, 201):
    d = r.json()
    print(f"Created snippet id={d.get('id')} slug={d.get('slug')}")
    print(f"Schema items: {len(item_list)}")
    print(f"Code length: {len(d.get('meta',{}).get('_elementor_code',''))}")
else:
    print(r.text[:500])
