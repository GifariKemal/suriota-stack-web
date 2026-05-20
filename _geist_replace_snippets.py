"""Replace Plus Jakarta + IBM Plex Mono with Geist + Geist Mono in elementor_snippets."""
import sys, io, json, urllib.request, base64, time, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

# 3 snippets with Plus Jakarta
TARGETS = [5184, 5153, 5261]

# Replacements (order matters — do font URL first)
REPLACEMENTS = [
    # Google Fonts URL
    ("family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600",
     "family=Geist:wght@300;400;500;600;700;800&family=Geist+Mono:wght@400;500;600"),
    ("family=Plus+Jakarta+Sans:wght@400;500;600;700;800",
     "family=Geist:wght@300;400;500;600;700;800"),
    ("family=IBM+Plex+Mono:wght@400;500;600",
     "family=Geist+Mono:wght@400;500;600"),
    # CSS font-family
    ("'Plus Jakarta Sans'", "'Geist'"),
    ('"Plus Jakarta Sans"', '"Geist"'),
    ("Plus Jakarta Sans", "Geist"),
    ("'IBM Plex Mono'", "'Geist Mono'"),
    ('"IBM Plex Mono"', '"Geist Mono"'),
    ("IBM Plex Mono", "Geist Mono"),
]

total = 0
for sid in TARGETS:
    r = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/elementor_snippet/{sid}?context=edit', headers=HDRS)
    d = json.loads(urllib.request.urlopen(r, timeout=30).read())
    code = d.get('meta',{}).get('_elementor_code','')
    new_code = code
    snippet_changes = 0
    for old, new in REPLACEMENTS:
        count = new_code.count(old)
        if count > 0:
            new_code = new_code.replace(old, new)
            snippet_changes += count
    if new_code != code:
        payload = json.dumps({'meta': {'_elementor_code': new_code}}).encode()
        try:
            urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/elementor_snippet/{sid}', data=payload, method='POST', headers=HDRS), timeout=30).read()
            print(f'  ID:{sid} +{snippet_changes} replacements')
            total += snippet_changes
        except Exception as e:
            print(f'  ID:{sid} push fail: {e}')
    else:
        print(f'  ID:{sid} no changes')

print(f'\nTotal replacements: {total}')

# Clear Elementor cache
print('\nClearing Elementor cache...')
try:
    urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/elementor/v1/cache', method='DELETE', headers=HDRS), timeout=30).read()
    print('  ✓ Elementor cache cleared')
except Exception as e:
    print(f'  err: {e}')

# Trigger refresh
time.sleep(3)
for url in ['https://suriota.com/', 'https://suriota.com/id/beranda/']:
    try:
        urllib.request.urlopen(urllib.request.Request(url + '?nc='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read()
    except: pass
print('Frontend triggered')
