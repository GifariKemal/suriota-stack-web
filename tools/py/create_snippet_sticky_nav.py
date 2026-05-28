"""Create sitewide sticky scroll-aware navbar snippet for header.sx-hf-v5."""
import os
import requests
from requests.auth import HTTPBasicAuth

AUTH = HTTPBasicAuth("admin", os.environ.get("WP_APP_PASS", ""))
BASE = "https://suriota.com/wp-json/wp/v2/elementor_snippet"

CODE = '''<style id="sx-nav-scroll">
header.sx-hf-v5 {
  position: sticky;
  top: 0;
  z-index: 9990;
  transform: translateY(0);
  transition: transform 220ms cubic-bezier(.2,.7,.2,1), box-shadow 220ms ease;
  will-change: transform;
  backface-visibility: hidden;
}
header.sx-hf-v5.sx-nav--hidden { transform: translateY(-100%); }
header.sx-hf-v5.sx-nav--scrolled {
  box-shadow: 0 2px 12px rgba(0,0,0,0.18);
}
header.sx-hf-v5:focus-within {
  transform: translateY(0) !important;
}
@media (prefers-reduced-motion: reduce) {
  header.sx-hf-v5 { transition: none; }
  header.sx-hf-v5.sx-nav--hidden { transform: translateY(0); }
}
:target { scroll-margin-top: 96px; }
html { scroll-padding-top: 80px; }
</style>
<script>
(function(){
  function init(){
    var nav = document.querySelector('header.sx-hf-v5');
    if (!nav) { setTimeout(init, 200); return; }
    var lastY = window.pageYOffset || 0;
    var ticking = false;
    var THRESHOLD = 80;
    var DELTA = 6;
    function update(){
      var y = window.pageYOffset;
      if (y < 0) y = 0;
      if (Math.abs(y - lastY) < DELTA) { ticking = false; return; }
      if (y < THRESHOLD) {
        nav.classList.remove('sx-nav--hidden');
        nav.classList.remove('sx-nav--scrolled');
      } else {
        nav.classList.add('sx-nav--scrolled');
        if (y > lastY) {
          nav.classList.add('sx-nav--hidden');
        } else {
          nav.classList.remove('sx-nav--hidden');
        }
      }
      lastY = y;
      ticking = false;
    }
    window.addEventListener('scroll', function(){
      if (!ticking) { requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
</script>
'''

payload = {
    "title": "SX / Sticky Scroll-Aware Navbar (Sitewide)",
    "status": "publish",
    "meta": {
        "_elementor_location": "elementor_body_end",
        "_elementor_priority": 6,
        "_elementor_code": CODE
    }
}

r = requests.post(BASE, auth=AUTH, json=payload, timeout=30)
print("Status:", r.status_code)
if r.status_code not in (200, 201):
    print(r.text[:600])
else:
    d = r.json()
    print("Created snippet ID:", d.get("id"))
    print("Slug:", d.get("slug"))
    print("Code length:", len(d.get("meta",{}).get("_elementor_code","")))
