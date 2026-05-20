"""Translate remaining 'What to include' block on ID-Contact."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

# Storage uses literal \u00b7 (6 chars). In Python source, \\u00b7 → \u00b7 (6 chars). Match.
PAIRS = [
    ('Proyek type (IoT deployment \\u00b7 system integration \\u00b7 custom hardware \\u00b7 SaaS)',
     'Jenis proyek (deployment IoT \\u00b7 integrasi sistem \\u00b7 custom hardware \\u00b7 SaaS)'),
    ('Compliance requirements (KLHK \\u00b7 SNI \\u00b7 IEC \\u00b7 PUIL)',
     'Kebutuhan compliance (KLHK \\u00b7 SNI \\u00b7 IEC \\u00b7 PUIL)'),
]

r = urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages/5378?context=edit&_fields=meta', headers=HDRS)
d = json.loads(urllib.request.urlopen(r, timeout=30).read())
ed = d.get('meta',{}).get('_elementor_data','')
if isinstance(ed, list): ed = json.dumps(ed)
new_ed = ed
total = 0
for old, new in PAIRS:
    c = new_ed.count(old)
    if c > 0:
        new_ed = new_ed.replace(old, new)
        total += c
        print(f'+{c}: {old[:60]}')
    else:
        print(f'miss: {old[:60]}')

if total > 0:
    payload = json.dumps({'meta': {'_elementor_data': new_ed}}).encode()
    urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages/5378', data=payload, method='POST', headers=HDRS), timeout=30).read()
    print(f'\nTotal: {total}')

urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/elementor/v1/cache', method='DELETE', headers=HDRS), timeout=30).read()
time.sleep(2)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/id/kontak/?nc='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read()
print('Done')
