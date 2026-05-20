"""Replace fonts + bump h3 to 18px in per-page custom_css."""
import sys, io, json, urllib.request, base64, time, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

REPLACEMENTS = [
    # Google Fonts URLs
    ('family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600',
     'family=Geist:wght@300;400;500;600;700;800&family=Geist+Mono:wght@400;500;600'),
    ('family=Plus+Jakarta+Sans:wght@400;500;600;700;800', 'family=Geist:wght@300;400;500;600;700;800'),
    ('family=IBM+Plex+Mono:wght@400;500;600', 'family=Geist+Mono:wght@400;500;600'),
    ('IBM+Plex+Mono', 'Geist+Mono'),
    ('Plus+Jakarta+Sans', 'Geist'),
    ('Plus+Jakarta', 'Geist'),
    # CSS font-family
    ("'Plus Jakarta Sans'", "'Geist'"),
    ('"Plus Jakarta Sans"', '"Geist"'),
    ('Plus Jakarta Sans', 'Geist'),
    ("'IBM Plex Mono'", "'Geist Mono'"),
    ('"IBM Plex Mono"', '"Geist Mono"'),
    ('IBM Plex Mono', 'Geist Mono'),
]

# Fetch all pages
r = urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages?per_page=100&context=edit&_fields=id,title,meta', headers=HDRS)
pages = json.loads(urllib.request.urlopen(r, timeout=60).read())

grand_total = 0
fixed_pages = 0
for p in pages:
    pid = p['id']
    ps = p.get('meta', {}).get('_elementor_page_settings', {})
    if isinstance(ps, str):
        try: ps = json.loads(ps) if ps else {}
        except: ps = {}
    if not isinstance(ps, dict): continue
    css = ps.get('custom_css', '')
    if not css: continue
    new_css = css
    changes = 0
    for old, new in REPLACEMENTS:
        c = new_css.count(old)
        if c > 0:
            new_css = new_css.replace(old, new)
            changes += c
    # Bump h3 card title sizes from 16px to 18px (only in card contexts)
    h3_bumps = re.findall(r'\.sx-whyus-h3[^{]*\{[^}]*font-size:\s*16px[^}]*\}', new_css)
    for block in h3_bumps:
        new_block = block.replace('font-size: 16px', 'font-size: 18px').replace('font-size:16px', 'font-size: 18px')
        new_css = new_css.replace(block, new_block)
        changes += 1
    # Same for sx-card-title patterns
    for sel in ['.sx-card-title', '.sx-trust-card h3', '.sx-service-card h3']:
        blocks = re.findall(re.escape(sel) + r'[^{]*\{[^}]*font-size:\s*16px[^}]*\}', new_css)
        for block in blocks:
            new_block = block.replace('font-size: 16px', 'font-size: 18px').replace('font-size:16px', 'font-size: 18px')
            new_css = new_css.replace(block, new_block)
            changes += 1
    if new_css != css:
        ps['custom_css'] = new_css
        payload = json.dumps({'meta': {'_elementor_page_settings': ps}}).encode()
        try:
            urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}', data=payload, method='POST', headers=HDRS), timeout=60).read()
            print(f'  {pid:5d}: +{changes} replacements')
            grand_total += changes
            fixed_pages += 1
        except Exception as e:
            print(f'  {pid:5d}: push fail {e}')

print(f'\nFixed {fixed_pages} pages, {grand_total} total replacements')

# Clear Elementor cache
try:
    urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/elementor/v1/cache', method='DELETE', headers=HDRS), timeout=30).read()
    print('✓ Elementor cache cleared')
except Exception as e:
    print(f'cache err: {e}')

# Trigger refresh
time.sleep(3)
for url in ['https://suriota.com/about/', 'https://suriota.com/automation/']:
    try: urllib.request.urlopen(urllib.request.Request(url + '?nc='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read()
    except: pass
print('Frontend triggered')
