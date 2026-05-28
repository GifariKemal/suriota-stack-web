"""Snippet 5640 v3: switch from hide-on-scroll-down to ALWAYS-VISIBLE sticky nav.
Uses position:fixed for maximum compatibility (sticky can break under certain parent
overflow/transform contexts). Body padding-top compensates for the out-of-flow nav."""
import os
import requests
from requests.auth import HTTPBasicAuth

AUTH = HTTPBasicAuth("admin", os.environ.get("WP_APP_PASS", ""))
URL = "https://suriota.com/wp-json/wp/v2/elementor_snippet/5640"

CODE = '''<style id="sx-nav-scroll">
header.sx-hf-v5 {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  width: 100%;
  z-index: 9990;
  transition: box-shadow 220ms ease, background-color 220ms ease;
  will-change: box-shadow;
}
header.sx-hf-v5.sx-nav--scrolled {
  box-shadow: 0 2px 12px rgba(0,0,0,0.18);
}
body { padding-top: 66px; }
@media (max-width: 900px) { body { padding-top: 60px; } }
:target { scroll-margin-top: 96px; }
html { scroll-padding-top: 80px; }
</style>
<script>
(function(){
  function init(){
    var nav = document.querySelector('header.sx-hf-v5');
    if (!nav) { setTimeout(init, 200); return; }
    function syncBodyPadding(){
      var h = nav.offsetHeight;
      if (h > 0) document.body.style.paddingTop = h + 'px';
    }
    syncBodyPadding();
    if (window.ResizeObserver) {
      try { new ResizeObserver(syncBodyPadding).observe(nav); } catch(e) {}
    } else {
      window.addEventListener('resize', syncBodyPadding, { passive: true });
    }
    var ticking = false;
    function update(){
      var y = window.pageYOffset || 0;
      if (y > 8) nav.classList.add('sx-nav--scrolled');
      else nav.classList.remove('sx-nav--scrolled');
      ticking = false;
    }
    window.addEventListener('scroll', function(){
      if (!ticking) { requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
    update();
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
    print("position fixed:", "position: fixed" in code)
    print("no translateY hide:", "translateY(-100%)" not in code)
    print("body padding-top sync:", "syncBodyPadding" in code)
