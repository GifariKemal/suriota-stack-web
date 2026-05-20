"""Standardize modern CSS rgb(255 255 255 / .X) variants."""
import sys, io, json, urllib.request, base64, time, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

# Modern syntax replacements
REPLACEMENTS = [
    # White opacity standardize → keep .3, .6, .7, .86, 1.0 as the palette
    # .85 → .86
    ('rgb(255 255 255 / .85)', 'rgb(255 255 255 / .86)'),
    ('rgb(255 255 255 / 0.85)', 'rgb(255 255 255 / .86)'),
    # .82 → .86
    ('rgb(255 255 255 / .82)', 'rgb(255 255 255 / .86)'),
    ('rgb(255 255 255 / 0.82)', 'rgb(255 255 255 / .86)'),
    # .88 → .86
    ('rgb(255 255 255 / .88)', 'rgb(255 255 255 / .86)'),
    ('rgb(255 255 255 / 0.88)', 'rgb(255 255 255 / .86)'),
    # .92 / .94 → keep separate (hover/strong-emphasis)
    # 248,250,251 modern
    ('rgb(248 250 251)', 'rgb(248 250 252)'),
    # max-width modern
    # (already handled before)
]

# Process pages
r = urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages?per_page=100&context=edit&_fields=id,title,meta', headers=HDRS)
items = json.loads(urllib.request.urlopen(r, timeout=60).read())

total = 0
for it in items:
    pid = it['id']
    ps = it.get('meta',{}).get('_elementor_page_settings', {})
    if isinstance(ps, str):
        try: ps = json.loads(ps) if ps else {}
        except: ps = {}
    css = ps.get('custom_css','') if isinstance(ps, dict) else ''
    ed = it.get('meta',{}).get('_elementor_data','')
    if isinstance(ed, list): ed = json.dumps(ed)
    if not isinstance(ed, str): ed = ''
    new_css = css
    new_ed = ed
    page_changes = 0
    for old, new in REPLACEMENTS:
        c1 = new_css.count(old)
        if c1 > 0:
            new_css = new_css.replace(old, new)
            page_changes += c1
        c2 = new_ed.count(old)
        if c2 > 0:
            new_ed = new_ed.replace(old, new)
            page_changes += c2
    if page_changes > 0:
        payload_meta = {}
        if new_css != css:
            ps['custom_css'] = new_css
            payload_meta['_elementor_page_settings'] = ps
        if new_ed != ed:
            payload_meta['_elementor_data'] = new_ed
        if payload_meta:
            payload = json.dumps({'meta': payload_meta}).encode()
            urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}', data=payload, method='POST', headers=HDRS), timeout=30).read()
            print(f'  page {pid}: +{page_changes}')
            total += page_changes

# Snippets
r = urllib.request.Request('https://suriota.com/wp-json/wp/v2/elementor_snippet?per_page=100&context=edit&_fields=id,title,meta', headers=HDRS)
snippets = json.loads(urllib.request.urlopen(r, timeout=60).read())
for s in snippets:
    sid = s['id']
    code = s.get('meta',{}).get('_elementor_code','')
    if not isinstance(code, str): continue
    new_code = code
    ch = 0
    for old, new in REPLACEMENTS:
        c = new_code.count(old)
        if c > 0:
            new_code = new_code.replace(old, new)
            ch += c
    if ch > 0:
        payload = json.dumps({'meta': {'_elementor_code': new_code}}).encode()
        urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/elementor_snippet/{sid}', data=payload, method='POST', headers=HDRS), timeout=30).read()
        print(f'  snippet {sid}: +{ch}')
        total += ch

print(f'\nTotal: {total}')

urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/elementor/v1/cache', method='DELETE', headers=HDRS), timeout=30).read()
time.sleep(2)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/automation/?nc='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read()
print('Done')
