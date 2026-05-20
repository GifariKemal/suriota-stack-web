"""Standardize design tokens: colors + opacity + max-width + h3 margin."""
import sys, io, json, urllib.request, base64, time, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

# Pattern → replacement (apply in order)
REPLACEMENTS = [
    # 1) Light grey duplicate — #F8FAFB → #F8FAFC (rgb 248,250,251 → 248,250,252)
    ('#F8FAFB', '#F8FAFC'),
    ('#f8fafb', '#F8FAFC'),
    ('rgb(248, 250, 251)', 'rgb(248, 250, 252)'),
    ('rgb(248,250,251)', 'rgb(248,250,252)'),

    # 2) White opacity standardization → 0.86 (single value for "soft white")
    ('rgba(255, 255, 255, 0.85)', 'rgba(255, 255, 255, 0.86)'),
    ('rgba(255,255,255,0.85)', 'rgba(255,255,255,0.86)'),
    ('rgba(255, 255, 255, .85)', 'rgba(255, 255, 255, .86)'),
    ('rgba(255,255,255,.85)', 'rgba(255,255,255,.86)'),
    ('rgba(255, 255, 255, 0.88)', 'rgba(255, 255, 255, 0.86)'),
    ('rgba(255,255,255,0.88)', 'rgba(255,255,255,0.86)'),
    ('rgba(255, 255, 255, .88)', 'rgba(255, 255, 255, .86)'),
    ('rgba(255,255,255,.88)', 'rgba(255,255,255,.86)'),
    ('rgba(255, 255, 255, 0.82)', 'rgba(255, 255, 255, 0.86)'),
    ('rgba(255,255,255,0.82)', 'rgba(255,255,255,0.86)'),
    ('rgba(255, 255, 255, .82)', 'rgba(255, 255, 255, .86)'),
    ('rgba(255,255,255,.82)', 'rgba(255,255,255,.86)'),
    # 0.68 — keep as "muted white" (different intent, ~70% which is meaningful break)
    ('rgba(255, 255, 255, 0.68)', 'rgba(255, 255, 255, 0.7)'),
    ('rgba(255,255,255,0.68)', 'rgba(255,255,255,0.7)'),
    ('rgba(255, 255, 255, .68)', 'rgba(255, 255, 255, .7)'),
    ('rgba(255,255,255,.68)', 'rgba(255,255,255,.7)'),

    # 3) Container max-width — 960px, 1080px → 1180px
    ('max-width:960px', 'max-width:1180px'),
    ('max-width: 960px', 'max-width: 1180px'),
    ('max-width:1080px', 'max-width:1180px'),
    ('max-width: 1080px', 'max-width: 1180px'),
    # Also clamp() expressions with these widths
    ('clamp(280px, 90vw, 960px)', 'clamp(280px, 92vw, 1180px)'),
    ('clamp(280px,90vw,960px)', 'clamp(280px,92vw,1180px)'),
    ('clamp(280px, 90vw, 1080px)', 'clamp(280px, 92vw, 1180px)'),
    ('clamp(280px,90vw,1080px)', 'clamp(280px,92vw,1180px)'),
    ('min(96vw, 960px)', 'min(96vw, 1180px)'),
    ('min(96vw,960px)', 'min(96vw,1180px)'),
    ('min(96vw, 1080px)', 'min(96vw, 1180px)'),
    ('min(96vw,1080px)', 'min(96vw,1180px)'),

    # 4) h3 margin 9px → 10px (only in card title context)
    # In context of .sx-whyus-h3 — limited replacement on SURGE-E (5288 + 1542)
    # Since this is hard to context-match safely, will be handled separately if needed
]

# Process every page's custom_css + _elementor_data
r = urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages?per_page=100&context=edit&_fields=id,title,meta', headers=HDRS)
items = json.loads(urllib.request.urlopen(r, timeout=60).read())

grand_total = 0
pages_changed = 0
for it in items:
    pid = it['id']
    ps = it.get('meta',{}).get('_elementor_page_settings', {})
    if isinstance(ps, str):
        try: ps = json.loads(ps) if ps else {}
        except: ps = {}
    css = ps.get('custom_css','') if isinstance(ps, dict) else ''
    ed = it.get('meta',{}).get('_elementor_data','')
    if isinstance(ed, list): ed = json.dumps(ed)

    new_css = css
    new_ed = ed if isinstance(ed, str) else ''
    page_changes = 0

    for old, new in REPLACEMENTS:
        c1 = new_css.count(old)
        if c1 > 0:
            new_css = new_css.replace(old, new)
            page_changes += c1
        if isinstance(new_ed, str):
            c2 = new_ed.count(old)
            if c2 > 0:
                new_ed = new_ed.replace(old, new)
                page_changes += c2

    if page_changes > 0:
        payload_meta = {}
        if new_css != css:
            ps['custom_css'] = new_css
            payload_meta['_elementor_page_settings'] = ps
        if isinstance(ed, str) and new_ed != ed:
            payload_meta['_elementor_data'] = new_ed
        if payload_meta:
            try:
                payload = json.dumps({'meta': payload_meta}).encode()
                urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}', data=payload, method='POST', headers=HDRS), timeout=60).read()
                print(f'  {pid}: +{page_changes}')
                grand_total += page_changes
                pages_changed += 1
            except Exception as e:
                print(f'  {pid}: push fail {e}')

# Also process elementor_snippet
r = urllib.request.Request('https://suriota.com/wp-json/wp/v2/elementor_snippet?per_page=100&context=edit&_fields=id,title,meta', headers=HDRS)
snippets = json.loads(urllib.request.urlopen(r, timeout=60).read())
for s in snippets:
    sid = s['id']
    code = s.get('meta',{}).get('_elementor_code','')
    if not isinstance(code, str): continue
    new_code = code
    changes = 0
    for old, new in REPLACEMENTS:
        c = new_code.count(old)
        if c > 0:
            new_code = new_code.replace(old, new)
            changes += c
    if changes > 0:
        try:
            payload = json.dumps({'meta': {'_elementor_code': new_code}}).encode()
            urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/elementor_snippet/{sid}', data=payload, method='POST', headers=HDRS), timeout=60).read()
            print(f'  snippet {sid}: +{changes}')
            grand_total += changes
        except Exception as e:
            print(f'  snippet {sid}: fail {e}')

print(f'\n=== Grand total: {grand_total} replacements in {pages_changed} pages ===')

# Clear cache
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/elementor/v1/cache', method='DELETE', headers=HDRS), timeout=30).read()
print('Cache cleared')

time.sleep(2)
for url in ['https://suriota.com/automation/', 'https://suriota.com/iso-m485-series/']:
    try: urllib.request.urlopen(urllib.request.Request(url+'?nc='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read()
    except: pass
print('Done')
