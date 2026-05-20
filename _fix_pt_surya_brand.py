"""Replace PT Surya Inovasi Prioritas eyebrow with proper brand display style (Option C)."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

# Two variants: escaped (in JSON-encoded _elementor_data) and unescaped
# Variant 1: Escaped slashes (`<\/span>`)
OLD_ESC = '<span class=\\"sx-eyebrow\\" style=\\"display:inline-block;font-family:\'Geist Mono\',monospace;font-size:12px;font-weight:500;letter-spacing:1.5px;text-transform:uppercase;color:#205B69;\\">PT Surya Inovasi Prioritas<\\/span>'
NEW_ESC = '<span class=\\"sx-brand-name\\" style=\\"display:inline-block;font-family:\'Geist\',system-ui,sans-serif;font-size:16px;font-weight:600;letter-spacing:-0.005em;color:#205B69;\\">PT Surya Inovasi Prioritas<\\/span>'

# Variant 2: Unescaped
OLD = '<span class="sx-eyebrow" style="display:inline-block;font-family:\'Geist Mono\',monospace;font-size:12px;font-weight:500;letter-spacing:1.5px;text-transform:uppercase;color:#205B69;">PT Surya Inovasi Prioritas</span>'
NEW = '<span class="sx-brand-name" style="display:inline-block;font-family:\'Geist\',system-ui,sans-serif;font-size:16px;font-weight:600;letter-spacing:-0.005em;color:#205B69;">PT Surya Inovasi Prioritas</span>'

PAGES = [(12, 'EN Home'), (5273, 'ID Home')]
for pid, lbl in PAGES:
    r = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}?context=edit&_fields=meta', headers=HDRS)
    d = json.loads(urllib.request.urlopen(r, timeout=30).read())
    ed = d.get('meta',{}).get('_elementor_data','')
    if isinstance(ed, list): ed = json.dumps(ed)
    if not isinstance(ed, str):
        print(f'{lbl}: ed not str')
        continue
    new_ed = ed
    c1 = new_ed.count(OLD_ESC)
    c2 = new_ed.count(OLD)
    if c1 > 0: new_ed = new_ed.replace(OLD_ESC, NEW_ESC)
    if c2 > 0: new_ed = new_ed.replace(OLD, NEW)
    total = c1 + c2
    if total > 0:
        payload = json.dumps({'meta': {'_elementor_data': new_ed}}).encode()
        urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}', data=payload, method='POST', headers=HDRS), timeout=30).read()
        print(f'  {lbl} (page {pid}): +{total} replacements (esc:{c1}, raw:{c2})')
    else:
        print(f'  {lbl} (page {pid}): no match')

# Clear cache
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/elementor/v1/cache', method='DELETE', headers=HDRS), timeout=30).read()
print('Cache cleared')

time.sleep(3)
for url in ['https://suriota.com/', 'https://suriota.com/id/beranda/']:
    urllib.request.urlopen(urllib.request.Request(url+'?nc='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read()
print('Done')
