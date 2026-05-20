"""Comprehensive search for IBM Plex / Plus Jakarta across all WP content."""
import urllib.request, base64, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0'}

PATTERNS = ['IBM Plex Mono', 'IBM+Plex+Mono', 'Plus Jakarta', 'Plus+Jakarta']

def count_patterns(text):
    return {p: text.count(p) for p in PATTERNS if p in text}

# 1. All pages (wp/v2/pages)
print('=== PAGES ===')
r = urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages?per_page=100&context=edit&_fields=id,title,meta,content', headers=HDRS)
pages = json.loads(urllib.request.urlopen(r, timeout=60).read())
for p in pages:
    ed = p.get('meta', {}).get('_elementor_data', '')
    if isinstance(ed, list): ed = json.dumps(ed)
    content = p.get('content', {}).get('raw', '') if isinstance(p.get('content'), dict) else str(p.get('content',''))
    combined = ed + content
    hits = count_patterns(combined)
    if hits:
        title = p.get('title',{}).get('rendered','')[:50]
        print(f"  ID:{p['id']:5d} {title:50s} {hits}")

# 2. Posts
print('\n=== POSTS ===')
r = urllib.request.Request('https://suriota.com/wp-json/wp/v2/posts?per_page=100&context=edit&_fields=id,title,meta,content', headers=HDRS)
posts = json.loads(urllib.request.urlopen(r, timeout=60).read())
for p in posts:
    ed = p.get('meta', {}).get('_elementor_data', '')
    if isinstance(ed, list): ed = json.dumps(ed)
    content = p.get('content', {}).get('raw', '') if isinstance(p.get('content'), dict) else str(p.get('content',''))
    combined = ed + content
    hits = count_patterns(combined)
    if hits:
        title = p.get('title',{}).get('rendered','')[:50]
        print(f"  ID:{p['id']:5d} {title:50s} {hits}")

# 3. Elementor templates
print('\n=== ELEMENTOR LIBRARY ===')
r = urllib.request.Request('https://suriota.com/wp-json/wp/v2/elementor_library?per_page=100&context=edit&_fields=id,title,meta', headers=HDRS)
tpls = json.loads(urllib.request.urlopen(r, timeout=60).read())
for t in tpls:
    ed = t.get('meta', {}).get('_elementor_data', '')
    if isinstance(ed, list): ed = json.dumps(ed)
    hits = count_patterns(ed)
    if hits:
        title = t.get('title',{}).get('rendered','')[:50]
        print(f"  ID:{t['id']:5d} {title:50s} {hits}")

# 4. Elementor snippets
print('\n=== ELEMENTOR SNIPPETS ===')
r = urllib.request.Request('https://suriota.com/wp-json/wp/v2/elementor_snippet?per_page=100&context=edit&_fields=id,title,meta', headers=HDRS)
sns = json.loads(urllib.request.urlopen(r, timeout=60).read())
for s in sns:
    code = s.get('meta', {}).get('_elementor_code', '')
    hits = count_patterns(code)
    if hits:
        title = s.get('title',{}).get('rendered','')[:50]
        print(f"  ID:{s['id']:5d} {title:50s} {hits}")
