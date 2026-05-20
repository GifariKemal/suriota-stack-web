"""Activate ZH in nav language switcher (snippet 5153)."""
import sys, urllib.request, base64, json, time
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except: pass

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

# Fetch snippet 5153
r = urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/wp/v2/elementor_snippet/5153?context=edit', headers=HDRS), timeout=30)
d = json.loads(r.read())
code = d.get('meta',{}).get('_elementor_code','')

# ============== INJECT 1: Add slug map + zhUrl + isZH detection ==============
# Find where isID/enUrl/idUrl are calculated
OLD_DETECT = """var isID = location.pathname.indexOf('/id/') === 0;
    var enUrl = (document.querySelector('link[rel="alternate"][hreflang="en"]') || {}).href || base + '/';
    var idUrl = (document.querySelector('link[rel="alternate"][hreflang="id"]') || {}).href || base + '/id/';"""

NEW_DETECT = """var isID = location.pathname.indexOf('/id/') === 0;

    /* EN slug → {id slug, zh slug} mapping */
    var pageMap = {
      '': { id: 'id/beranda', zh: 'shouye' },
      'about-us': { id: 'id/tentang-kami', zh: 'guanyu-women' },
      'portfolio': { id: 'id/portfolio-id', zh: 'anli' },
      'contact': { id: 'id/kontak', zh: 'lianxi' },
      'automation': { id: 'id/automation-id', zh: 'zidonghua' },
      'electrical': { id: 'id/electrical-id', zh: 'dianqi-gongcheng' },
      'renewable-energy': { id: 'id/renewable-energy-id', zh: 'kezaisheng-nengyuan' },
      'internet-of-things': { id: 'id/internet-of-things-id', zh: 'iot' },
      'water-treatment': { id: 'id/water-treatment-id', zh: 'shuichuli' },
      'data-analytics': { id: 'id/data-analytics-id', zh: 'shujufenxi' },
      'digital-consulting': { id: 'id/digital-consulting-id', zh: 'shuzihua-zixun' },
      'artificial-intelligence': { id: 'id/artificial-intelligence-id', zh: 'rengong-zhineng' },
      'system-integration': { id: 'id/system-integration-id', zh: 'xitong-jicheng' },
      'software-as-a-service': { id: 'id/saas-id', zh: 'saas' },
      'saas': { id: 'id/saas-id', zh: 'saas' },
      'surge-energy-mapping': { id: 'id/surge-energy-mapping-id', zh: 'surge-energy-mapping-2' },
      'surge-vessel-tracking': { id: 'id/surge-vessel-tracking-id', zh: 'surge-vessel-tracking-2' },
      'surge-water-analytic': { id: 'id/surge-water-analytic-id', zh: 'surge-water-analytic-2' },
      'suriota-modbus-gateway': { id: 'id/suriota-modbus-gateway-id', zh: 'modbus-gateway' },
      'iso-m485-series': { id: 'id/iso-m485-series-id', zh: 'iso-m485' },
      'thm-30md': { id: 'id/thm-30md-id', zh: 'thm-30md-2' },
      'pm1611-wd': { id: 'id/pm1611-wd-id', zh: 'pm1611-wd-2' },
      'rs-485-surge-protector-spd-t485-105': { id: 'id/rs-485-surge-protector-id', zh: 'rs-485-spd' },
      'rs-485-surge-protector': { id: 'id/rs-485-surge-protector-id', zh: 'rs-485-spd' },
      'waste-water-logger': { id: 'id/waste-water-logger-id', zh: 'wastewater-logger' },
      'privacy-policy': { id: 'id/kebijakan-privasi', zh: 'yinsi-zhengce' },
      'terms-of-service': { id: 'id/syarat-layanan', zh: 'fuwu-tiaokuan' },
      'internship': { id: 'id/magang-srt-team', zh: 'internship' }
    };

    /* Build reverse maps */
    var idToEn = {};
    var zhToEn = {};
    for (var enKey in pageMap) {
      if (pageMap[enKey].id) idToEn[pageMap[enKey].id] = enKey;
      if (pageMap[enKey].zh) zhToEn[pageMap[enKey].zh] = enKey;
    }

    /* Determine current page's EN equivalent slug */
    var currentPath = location.pathname.replace(/^\\/+|\\/+$/g, '');
    var currentEn = '';
    var isZH = false;
    if (isID) {
      currentEn = idToEn[currentPath] || '';
    } else if (zhToEn[currentPath]) {
      isZH = true;
      currentEn = zhToEn[currentPath];
    } else {
      currentEn = currentPath;
    }

    /* Construct URLs */
    var enFromHreflang = (document.querySelector('link[rel="alternate"][hreflang="en"]') || {}).href;
    var idFromHreflang = (document.querySelector('link[rel="alternate"][hreflang="id"]') || {}).href;
    var zhFromHreflang = (document.querySelector('link[rel="alternate"][hreflang="zh-CN"]') || document.querySelector('link[rel="alternate"][hreflang="zh"]') || {}).href;

    var enUrl = enFromHreflang || (base + '/' + (currentEn ? currentEn + '/' : ''));
    var idSlug = (pageMap[currentEn] && pageMap[currentEn].id) || 'id';
    var idUrl = idFromHreflang || (base + '/' + idSlug + '/');
    var zhSlug = (pageMap[currentEn] && pageMap[currentEn].zh) || 'shouye';
    var zhUrl = zhFromHreflang || (base + '/' + zhSlug + '/');"""

if OLD_DETECT in code:
    code = code.replace(OLD_DETECT, NEW_DETECT)
    print('✅ Replaced URL detection logic')
else:
    print('❌ OLD_DETECT pattern not found')

# ============== INJECT 2: Replace lang dropdown UI ==============
OLD_DROPDOWN = """'<span class="sx-lang-flag">' + (isID?'ID':'EN') + '</span> <span class="sx-hf-v5-caret">&#9662;</span></button>' +
            '<div class="sx-hf-v5-dropcontent sx-hf-v5-lang-content">' +
              (isID? '<a href="' + enUrl + '" hreflang="en"><span class="sx-lang-flag-mini">EN</span> English</a>' : '<a href="' + idUrl + '" hreflang="id"><span class="sx-lang-flag-mini">ID</span> Bahasa Indonesia</a>') +
              '<span class="sx-lang-disabled" aria-disabled="true"><span class="sx-lang-flag-mini">CN</span> 中文 <em class="sx-lang-soon">Coming Soon</em></span>' +
            '</div>' +"""

NEW_DROPDOWN = """'<span class="sx-lang-flag">' + (isZH?'CN':(isID?'ID':'EN')) + '</span> <span class="sx-hf-v5-caret">&#9662;</span></button>' +
            '<div class="sx-hf-v5-dropcontent sx-hf-v5-lang-content">' +
              (isID || isZH ? '<a href="' + enUrl + '" hreflang="en"><span class="sx-lang-flag-mini">EN</span> English</a>' : '') +
              (!isID ? '<a href="' + idUrl + '" hreflang="id"><span class="sx-lang-flag-mini">ID</span> Bahasa Indonesia</a>' : '') +
              (!isZH ? '<a href="' + zhUrl + '" hreflang="zh-CN"><span class="sx-lang-flag-mini">CN</span> 中文</a>' : '') +
            '</div>' +"""

if OLD_DROPDOWN in code:
    code = code.replace(OLD_DROPDOWN, NEW_DROPDOWN)
    print('✅ Replaced dropdown UI')
else:
    print('❌ OLD_DROPDOWN pattern not found')

# Push updated snippet
payload = json.dumps({'meta': {'_elementor_code': code}}).encode()
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/wp/v2/elementor_snippet/5153', data=payload, method='POST', headers=HDRS), timeout=30).read()
print('Snippet 5153 updated')

# Clear cache
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/elementor/v1/cache', method='DELETE', headers=HDRS), timeout=30).read()
print('Cache cleared')

time.sleep(2)
for u in ['https://suriota.com/', 'https://suriota.com/id/beranda/', 'https://suriota.com/shouye/']:
    r = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent':'Mozilla/5.0'}), timeout=15)
    print(f'  {u}: {r.status}')
