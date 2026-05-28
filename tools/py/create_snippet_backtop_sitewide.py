"""Create sitewide back-to-top snippet with self-contained CSS+JS.
CSS extracted from homepage custom_css; vars hardcoded so it works on every page."""
import os
import requests
from requests.auth import HTTPBasicAuth

AUTH = HTTPBasicAuth("admin", os.environ.get("WP_APP_PASS", ""))
BASE = "https://suriota.com/wp-json/wp/v2/elementor_snippet"

CODE = r'''<style id="sx-backtop-css">
.sx-backtop {
  position: fixed;
  bottom: 24px;
  left: 24px;
  z-index: 60;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 0;
  padding: 0;
  background: #205B69;
  color: #fff;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  opacity: 0;
  pointer-events: none;
  transform: translateY(8px);
  transition:
    opacity 280ms cubic-bezier(0.22, 1, 0.36, 1),
    transform 280ms cubic-bezier(0.22, 1, 0.36, 1),
    box-shadow 280ms cubic-bezier(0.22, 1, 0.36, 1),
    background 160ms cubic-bezier(0.22, 1, 0.36, 1);
  box-shadow: 0 8px 24px rgba(14, 57, 66, 0.18);
}
.sx-backtop svg {
  width: 18px;
  height: 18px;
  display: block;
  stroke: currentColor;
  fill: none;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}
.sx-backtop.is-visible {
  opacity: 1;
  pointer-events: auto;
  transform: translateY(0);
}
.sx-backtop:hover {
  background: #0E3942;
  box-shadow: 0 12px 32px rgba(14, 57, 66, 0.22);
  transform: translateY(-2px);
}
.sx-backtop:focus-visible {
  outline: 2px solid #205B69;
  outline-offset: 3px;
}
@media (max-width: 600px) {
  .sx-backtop { bottom: 16px; left: 16px; width: 40px; height: 40px; }
  .sx-backtop svg { width: 16px; height: 16px; }
}
@media (prefers-reduced-motion: reduce) {
  .sx-backtop { transition: opacity 0.1s linear; transform: none; }
  .sx-backtop.is-visible { transform: none; }
  .sx-backtop:hover { transform: none; }
}
</style>
<script>
(function () {
  if (window.__sxBacktopSitewide) return;
  window.__sxBacktopSitewide = true;
  function init() {
    if (document.querySelector('.sx-backtop')) return;
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'sx-backtop';
    b.setAttribute('aria-label', 'Back to top');
    b.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5"/><path d="M6 11l6-6 6 6"/></svg>';
    b.addEventListener('click', function () {
      try { window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' }); }
      catch (e) { window.scrollTo(0, 0); }
    });
    document.body.appendChild(b);
    function onScroll() {
      if (window.pageYOffset > 320) b.classList.add('is-visible');
      else b.classList.remove('is-visible');
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
</script>
'''

payload = {
    "title": "SX / Back-to-Top Button (Sitewide)",
    "status": "publish",
    "meta": {
        "_elementor_location": "elementor_body_end",
        "_elementor_priority": 7,
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
