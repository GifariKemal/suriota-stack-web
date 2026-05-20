"""Fix nav JS swap - defer to body ready."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

JS_CODE = '''<script id="sx-nav-id-swap">
(function(){
  var isID = document.documentElement.lang === "id"
          || document.documentElement.lang === "id-ID"
          || location.pathname.indexOf("/id/") === 0;
  if (!isID) return;
  var map = {
    "About Us": "Tentang Kami",
    "Internship": "Magang",
    "Our Services": "Layanan Kami",
    "Automation": "Otomasi",
    "Renewable Energy": "Energi Terbarukan",
    "System Integration": "Integrasi Sistem",
    "Product": "Produk"
  };
  function applySwap(root) {
    if (!root) return;
    var selectors = "header a, nav a, .elementor-nav-menu a, .menu-item > a, .sx-hf-v5-nav a, .sx-hf-v5-mobile a, .sx-emergency-hf a";
    var elements = root.querySelectorAll ? root.querySelectorAll(selectors) : [];
    elements.forEach(function(el){
      el.childNodes.forEach(function(n){
        if (n.nodeType === 3) {
          var txt = n.textContent.trim();
          if (map[txt]) n.textContent = n.textContent.replace(txt, map[txt]);
        }
      });
      el.querySelectorAll("span").forEach(function(sp){
        var txt = sp.textContent.trim();
        if (map[txt] && sp.children.length === 0) sp.textContent = map[txt];
      });
    });
  }
  function init() {
    if (!document.body) { setTimeout(init, 50); return; }
    applySwap(document);
    try {
      var mo = new MutationObserver(function(mutations){
        mutations.forEach(function(m){ if (m.addedNodes.length) applySwap(m.target); });
      });
      mo.observe(document.body, {childList:true, subtree:true});
    } catch(e) { /* ignore */ }
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
</script>'''

payload = {'meta': {'_elementor_code': JS_CODE, '_elementor_location':'elementor_head', '_elementor_priority': 999}}
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/wp/v2/elementor_snippet/5447', data=json.dumps(payload).encode(), method='POST', headers=HDRS), timeout=30).read()
print('Updated snippet 5447')

urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/elementor/v1/cache', method='DELETE', headers=HDRS), timeout=30).read()
time.sleep(2)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/id/beranda/?nc='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read()
print('Done')
