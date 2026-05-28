"""Patch snippet 5640: add guard so nav doesn't hide while mobile menu is open."""
import os
import requests
from requests.auth import HTTPBasicAuth

AUTH = HTTPBasicAuth("admin", os.environ.get("WP_APP_PASS", ""))
URL = "https://suriota.com/wp-json/wp/v2/elementor_snippet/5640"

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
    function menuOpen(){
      var t = nav.querySelector('.sx-hf-v5-toggle');
      if (t && t.getAttribute('aria-expanded') === 'true') return true;
      if (nav.classList.contains('is-open') || nav.classList.contains('menu-open')) return true;
      if (document.body.classList.contains('sx-menu-open') || document.body.classList.contains('menu-open')) return true;
      return false;
    }
    function update(){
      var y = window.pageYOffset;
      if (y < 0) y = 0;
      if (Math.abs(y - lastY) < DELTA) { ticking = false; return; }
      if (menuOpen()) {
        nav.classList.remove('sx-nav--hidden');
        ticking = false;
        lastY = y;
        return;
      }
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
    document.addEventListener('click', function(e){
      if (e.target.closest('.sx-hf-v5-toggle')) {
        setTimeout(function(){
          if (menuOpen()) nav.classList.remove('sx-nav--hidden');
        }, 50);
      }
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
    "meta": {
        "_elementor_code": CODE,
        "_elementor_location": "elementor_body_end",
        "_elementor_priority": 6
    }
}

r = requests.post(URL, auth=AUTH, json=payload, timeout=30)
print("Status:", r.status_code)
if r.status_code != 200:
    print(r.text[:600])
else:
    d = r.json()
    code = d.get("meta",{}).get("_elementor_code","")
    print("Updated. Code length:", len(code))
    print("Contains menuOpen():", "menuOpen()" in code)
    print("Contains aria-expanded check:", "aria-expanded" in code)
