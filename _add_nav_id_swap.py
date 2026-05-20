"""Add JS snippet that translates nav header labels on ID pages."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

JS_CODE = """<script id="sx-nav-id-swap">
(function(){
  // Detect Indonesian page via html lang or URL prefix
  var isID = document.documentElement.lang === 'id'
          || document.documentElement.lang === 'id-ID'
          || location.pathname.indexOf('/id/') === 0
          || location.pathname.startsWith('/id/');
  if (!isID) return;

  // Translation map for nav labels (only translate generic categories; preserve product/tech names)
  var map = {
    'About Us': 'Tentang Kami',
    'Internship': 'Magang',
    'Our Services': 'Layanan Kami',
    'Automation': 'Otomasi',
    'Renewable Energy': 'Energi Terbarukan',
    'System Integration': 'Integrasi Sistem',
    'Product': 'Produk'
  };

  function applySwap(root) {
    // Match menu item text nodes (Elementor nav menu)
    var selectors = [
      'header a', 'nav a', '.elementor-nav-menu a', '.menu-item > a',
      '.sx-hf-v5-nav a', '.sx-hf-v5-mobile a', '.sx-emergency-hf a'
    ];
    var elements = (root || document).querySelectorAll(selectors.join(','));
    elements.forEach(function(el){
      // Walk text nodes only (preserve child icons like dropdown arrows)
      el.childNodes.forEach(function(n){
        if (n.nodeType === 3) {
          var txt = n.textContent.trim();
          if (map[txt]) {
            n.textContent = n.textContent.replace(txt, map[txt]);
          }
        }
      });
      // Also handle <span> wrappers inside menu links
      el.querySelectorAll('span').forEach(function(sp){
        var txt = sp.textContent.trim();
        if (map[txt] && sp.children.length === 0) {
          sp.textContent = map[txt];
        }
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function(){ applySwap(document); });
  } else {
    applySwap(document);
  }
  // Re-apply after any late DOM changes (mobile menu open, lazy load)
  var mo = new MutationObserver(function(mutations){
    mutations.forEach(function(m){ if (m.addedNodes.length) applySwap(m.target); });
  });
  mo.observe(document.body, {childList:true, subtree:true});
})();
</script>"""

# Create new elementor_snippet at footer location
payload = {
    'title': 'SX / Nav Header ID Swap (JS Runtime)',
    'status': 'publish',
    'meta': {
        '_elementor_location': 'elementor_footer',
        '_elementor_priority': 999,
        '_elementor_code': JS_CODE
    }
}
try:
    resp = urllib.request.urlopen(urllib.request.Request(
        'https://suriota.com/wp-json/wp/v2/elementor_snippet',
        data=json.dumps(payload).encode(),
        method='POST',
        headers=HDRS
    ), timeout=30).read()
    res = json.loads(resp)
    print(f'Created snippet ID:{res.get("id")} status:{res.get("status")}')
except Exception as e:
    print(f'create fail: {e}')

# Clear Elementor cache
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/elementor/v1/cache', method='DELETE', headers=HDRS), timeout=30).read()
time.sleep(2)
for url in ['https://suriota.com/id/beranda/', 'https://suriota.com/id/tentang-kami/']:
    urllib.request.urlopen(urllib.request.Request(url+'?nc='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read()
print('Done')
