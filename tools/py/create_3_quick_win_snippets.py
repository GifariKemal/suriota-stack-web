"""Deploy 3 quick win snippets:
1. Roboto Google Font dequeue (HEAD pri 1)
2. Geist preload hint (HEAD pri 1)
3. CLS shield: min-height on pillar hero sections (HEAD pri 5)
"""
import os
import requests
from requests.auth import HTTPBasicAuth

AUTH = HTTPBasicAuth("admin", os.environ.get("WP_APP_PASS", ""))
BASE = "https://suriota.com/wp-json/wp/v2/elementor_snippet"

# ---------- 1. Roboto dequeue ----------
ROBOTO_CODE = '''<script>
(function(){
  function strip(){
    var sels = ['link[id*="elementor-gf-roboto"]','link[href*="family=Roboto:"]','link[href*="family=Roboto&"]','link[href*="family=Roboto+"]'];
    sels.forEach(function(s){
      document.querySelectorAll(s).forEach(function(el){
        if (el.id && el.id.indexOf('robotoslab') !== -1) return;
        if (el.href && el.href.indexOf('Roboto+Slab') !== -1) return;
        el.parentNode && el.parentNode.removeChild(el);
      });
    });
  }
  strip();
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', strip);
  setTimeout(strip, 300);
  setTimeout(strip, 1200);
})();
</script>
'''

# ---------- 2. Geist preload ----------
GEIST_CODE = '''<link rel="preconnect" href="https://fonts.googleapis.com" crossorigin />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;600;700&family=Geist+Mono:wght@400;500;600&display=swap" />
'''

# ---------- 3. CLS shield for pillar heroes ----------
# Pillar page IDs: EN(5554,934,5558,5557,1542) + ID(5566,5567,5569,5570) + ZH(5571,5572,5574)
CLS_CODE = '''<style id="sx-cls-pillar-hero">
body.page-id-5554 .elementor-top-section:first-of-type,
body.page-id-934  .elementor-top-section:first-of-type,
body.page-id-5558 .elementor-top-section:first-of-type,
body.page-id-5557 .elementor-top-section:first-of-type,
body.page-id-1542 .elementor-top-section:first-of-type,
body.page-id-5566 .elementor-top-section:first-of-type,
body.page-id-5567 .elementor-top-section:first-of-type,
body.page-id-5569 .elementor-top-section:first-of-type,
body.page-id-5570 .elementor-top-section:first-of-type,
body.page-id-5571 .elementor-top-section:first-of-type,
body.page-id-5572 .elementor-top-section:first-of-type,
body.page-id-5574 .elementor-top-section:first-of-type {
  min-height: 360px;
}
@media (min-width: 768px) {
  body.page-id-5554 .elementor-top-section:first-of-type,
  body.page-id-934  .elementor-top-section:first-of-type,
  body.page-id-5558 .elementor-top-section:first-of-type,
  body.page-id-5557 .elementor-top-section:first-of-type,
  body.page-id-1542 .elementor-top-section:first-of-type,
  body.page-id-5566 .elementor-top-section:first-of-type,
  body.page-id-5567 .elementor-top-section:first-of-type,
  body.page-id-5569 .elementor-top-section:first-of-type,
  body.page-id-5570 .elementor-top-section:first-of-type,
  body.page-id-5571 .elementor-top-section:first-of-type,
  body.page-id-5572 .elementor-top-section:first-of-type,
  body.page-id-5574 .elementor-top-section:first-of-type {
    min-height: 480px;
  }
}
</style>
'''

snippets = [
    {
        "title": "SX / Dequeue Unused Roboto Font",
        "code": ROBOTO_CODE,
        "loc": "elementor_head",
        "pri": 1
    },
    {
        "title": "SX / Geist Font Preload Hint",
        "code": GEIST_CODE,
        "loc": "elementor_head",
        "pri": 1
    },
    {
        "title": "SX / CLS Shield Pillar Hero Min-Height",
        "code": CLS_CODE,
        "loc": "elementor_head",
        "pri": 5
    },
]

for s in snippets:
    payload = {
        "title": s["title"],
        "status": "publish",
        "meta": {
            "_elementor_location": s["loc"],
            "_elementor_priority": s["pri"],
            "_elementor_code": s["code"]
        }
    }
    r = requests.post(BASE, auth=AUTH, json=payload, timeout=30)
    if r.status_code in (200, 201):
        d = r.json()
        print(f"[+] Created snippet {d.get('id')}: {d.get('title',{}).get('rendered',s['title'])[:60]}")
        print(f"    location={d.get('meta',{}).get('_elementor_location','')} priority={d.get('meta',{}).get('_elementor_priority','')}")
        print(f"    code length: {len(d.get('meta',{}).get('_elementor_code',''))}")
    else:
        print(f"[!] Failed: {r.status_code} {r.text[:200]}")
