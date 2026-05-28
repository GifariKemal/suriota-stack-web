"""Hreflang dedup: AIOSEO and Polylang both emit hreflang tags causing duplicates.
This snippet runs early in head, removes duplicate <link rel=alternate hreflang> tags
keeping the first occurrence per language code."""
import os
import requests
from requests.auth import HTTPBasicAuth

AUTH = HTTPBasicAuth("admin", os.environ.get("WP_APP_PASS", ""))
BASE = "https://suriota.com/wp-json/wp/v2/elementor_snippet"

CODE = '''<script>
(function(){
  function dedup(){
    var seen = {};
    var dupes = [];
    document.querySelectorAll('link[rel="alternate"][hreflang]').forEach(function(l){
      var key = l.getAttribute('hreflang') + '|' + l.getAttribute('href');
      if (seen[key]) {
        dupes.push(l);
      } else {
        seen[key] = true;
      }
    });
    dupes.forEach(function(l){ if (l.parentNode) l.parentNode.removeChild(l); });
  }
  // Run on parse + DOMContentLoaded to catch late-inserted ones (snippet 5524)
  dedup();
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', dedup);
  }
  setTimeout(dedup, 100);
  setTimeout(dedup, 500);
})();
</script>
'''

payload = {
    "title": "SX / Hreflang Dedup (AIOSEO + Polylang)",
    "status": "publish",
    "meta": {
        "_elementor_location": "elementor_head",
        "_elementor_priority": 2,
        "_elementor_code": CODE
    }
}

r = requests.post(BASE, auth=AUTH, json=payload, timeout=30)
print("Status:", r.status_code)
if r.status_code in (200, 201):
    d = r.json()
    print(f"Created snippet id={d.get('id')} slug={d.get('slug')}")
else:
    print(r.text[:400])
