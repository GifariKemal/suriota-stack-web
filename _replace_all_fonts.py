"""Replace IBM Plex Mono + Plus Jakarta Sans → Geist + Geist Mono everywhere."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

REPLACEMENTS = [
    # Google Fonts URLs
    ('family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600',
     'family=Geist:wght@300;400;500;600;700;800&family=Geist+Mono:wght@400;500;600'),
    ('family=Plus+Jakarta+Sans:wght@400;500;600;700;800',
     'family=Geist:wght@300;400;500;600;700;800'),
    ('family=IBM+Plex+Mono:wght@400;500;600', 'family=Geist+Mono:wght@400;500;600'),
    ('IBM+Plex+Mono', 'Geist+Mono'),
    ('Plus+Jakarta+Sans', 'Geist'),
    ('Plus+Jakarta', 'Geist'),
    # CSS / JSON serialized font-family values
    ("'Plus Jakarta Sans'", "'Geist'"),
    ('"Plus Jakarta Sans"', '"Geist"'),
    ('\\u0022Plus Jakarta Sans\\u0022', '\\u0022Geist\\u0022'),
    ('\\"Plus Jakarta Sans\\"', '\\"Geist\\"'),
    ('Plus Jakarta Sans', 'Geist'),
    ("'IBM Plex Mono'", "'Geist Mono'"),
    ('"IBM Plex Mono"', '"Geist Mono"'),
    ('\\u0022IBM Plex Mono\\u0022', '\\u0022Geist Mono\\u0022'),
    ('\\"IBM Plex Mono\\"', '\\"Geist Mono\\"'),
    ('IBM Plex Mono', 'Geist Mono'),
]

def apply_replacements(s):
    """Apply all replacements, return new string + count."""
    cnt = 0
    for old, new in REPLACEMENTS:
        c = s.count(old)
        if c > 0:
            s = s.replace(old, new)
            cnt += c
    return s, cnt

def process_resource(endpoint, rid, meta_field='_elementor_data', extra_fields=None):
    """Fetch, replace, push back."""
    url = f'https://suriota.com/wp-json/wp/v2/{endpoint}/{rid}?context=edit'
    try:
        r = urllib.request.Request(url, headers=HDRS)
        d = json.loads(urllib.request.urlopen(r, timeout=60).read())
    except Exception as e:
        return f'fetch fail: {e}', 0
    payload = {}
    total = 0
    # _elementor_data
    ed = d.get('meta', {}).get(meta_field, '')
    if isinstance(ed, list): ed = json.dumps(ed)
    if isinstance(ed, str) and ed:
        new_ed, c = apply_replacements(ed)
        if c > 0:
            payload['meta'] = payload.get('meta', {})
            payload['meta'][meta_field] = new_ed
            total += c
    # content
    if extra_fields and 'content' in extra_fields:
        content = d.get('content', {}).get('raw', '') if isinstance(d.get('content'), dict) else str(d.get('content',''))
        if content:
            new_content, c = apply_replacements(content)
            if c > 0:
                payload['content'] = new_content
                total += c
    if payload:
        try:
            urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/{endpoint}/{rid}', data=json.dumps(payload).encode(), method='POST', headers=HDRS), timeout=60).read()
            return f'OK +{total}', total
        except Exception as e:
            return f'push fail: {e}', 0
    return 'no change', 0

# Target lists from prior audit
PAGE_IDS = [5295,5294,5293,5292,5291,5290,5289,5288,5287,5286,5285,5284,5283,5282,5281,5279,5278,5277,5276,5275,5274,5273,1127,945,839,39,37,35,29,12]
POST_IDS = [1925]
TEMPLATE_IDS = [4679, 4677, 4675, 1079]

grand_total = 0

print('=== PAGES ===')
for pid in PAGE_IDS:
    msg, c = process_resource('pages', pid, extra_fields=['content'])
    print(f'  {pid:5d}: {msg}')
    grand_total += c

print('\n=== POSTS ===')
for pid in POST_IDS:
    msg, c = process_resource('posts', pid, extra_fields=['content'])
    print(f'  {pid:5d}: {msg}')
    grand_total += c

print('\n=== TEMPLATES ===')
for tid in TEMPLATE_IDS:
    msg, c = process_resource('elementor_library', tid)
    print(f'  {tid:5d}: {msg}')
    grand_total += c

print(f'\n=== GRAND TOTAL: {grand_total} replacements ===')

# Clear Elementor cache
print('\nClearing Elementor cache...')
try:
    urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/elementor/v1/cache', method='DELETE', headers=HDRS), timeout=30).read()
    print('  ✓ Elementor cache cleared')
except Exception as e:
    print(f'  err: {e}')

# Trigger
time.sleep(3)
for url in ['https://suriota.com/about/', 'https://suriota.com/automation/', 'https://suriota.com/id/tentang-kami/']:
    try:
        urllib.request.urlopen(urllib.request.Request(url + '?nc='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read()
    except: pass
print('Frontend triggered')
