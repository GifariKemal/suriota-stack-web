"""Fix remaining residuals."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

# Use raw strings to preserve \u escapes as literal
FIXES = {
    5378: [
        (r'Mon\u2013Fri \u00b7 09:00\u201318:00 WIB', r'Sen\u2013Jum \u00b7 09:00\u201318:00 WIB'),
    ],
    5380: [
        # h2 main heading 15
        (r'<h2>15. General Provisions<\/h2>', r'<h2>15. Ketentuan Umum<\/h2>'),
    ],
}

total = 0
for pid, pairs in FIXES.items():
    r = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}?context=edit&_fields=meta', headers=HDRS)
    d = json.loads(urllib.request.urlopen(r, timeout=30).read())
    ed = d.get('meta',{}).get('_elementor_data','')
    if isinstance(ed, list): ed = json.dumps(ed)
    if not isinstance(ed, str): continue
    new_ed = ed
    changes = 0
    for old, new in pairs:
        c = new_ed.count(old)
        if c > 0:
            new_ed = new_ed.replace(old, new)
            changes += c
            print(f'  +{c}: {old[:60]}')
        else:
            print(f'  miss: {old[:60]}')
    if new_ed != ed:
        payload = json.dumps({'meta': {'_elementor_data': new_ed}}).encode()
        urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}', data=payload, method='POST', headers=HDRS), timeout=30).read()
        print(f'  {pid}: +{changes}')
        total += changes

print(f'\nTotal: {total}')
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/elementor/v1/cache', method='DELETE', headers=HDRS), timeout=30).read()
time.sleep(2)
for url in ['https://suriota.com/id/kontak/', 'https://suriota.com/id/syarat-layanan/']:
    urllib.request.urlopen(urllib.request.Request(url+'?nc='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read()
print('Done')
