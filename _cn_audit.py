"""Audit ZH pages — find remaining English chunks per page."""
import sys, urllib.request, base64, json, re
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except: pass

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0'}

# Get all ZH pages (created by me — 5448, 5450-5473)
ZH_PAGES = [5448, 5450, 5451, 5452, 5453, 5454, 5455, 5456, 5457, 5458, 5459, 5460,
            5461, 5462, 5463, 5464, 5465, 5466, 5467, 5468, 5469, 5470, 5471, 5472, 5473]

EN_WORDS = [' the ', ' and ', ' for ', ' with ', ' from ', ' you ', ' will ', ' our ', ' we ', ' is ', ' are ', ' that ', ' this ', ' or ', ' to ', ' by ', ' of ', ' in ', ' as ', ' an ', ' any ', ' your ', ' has ']

for pid in ZH_PAGES:
    r = urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}?context=edit&_fields=meta,title,slug', headers=HDRS), timeout=30)
    d = json.loads(r.read())
    ed = d.get('meta',{}).get('_elementor_data','')
    if isinstance(ed, list): ed = json.dumps(ed)
    title = d.get('title',{}).get('rendered','')
    slug = d.get('slug','')

    # Find English chunks
    chunks = re.split(r'<[^>]+>|\\\\\\\"|\\\\u00a0|\\\\n', ed)
    seen = set()
    en_chunks = []
    for ch in chunks:
        ch = ch.strip()
        if len(ch) < 30 or len(ch) > 500: continue
        en_count = sum(1 for w in EN_WORDS if w in ch.lower())
        if en_count >= 4:
            key = ch[:60]
            if key in seen: continue
            seen.add(key)
            en_chunks.append((en_count, ch))

    print(f'\n=== {pid} {title[:50]} (/{slug}/) ===')
    print(f'  Remaining EN chunks: {len(en_chunks)}')
    for cnt, ch in sorted(en_chunks, key=lambda x: -x[0])[:5]:
        print(f'  EN({cnt}): {ch[:200]}')
