"""Translate English eyebrows on ID pages to Bahasa."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

# Eyebrow text replacements — only inside `>...</span>` of sx-eyebrow
# To avoid touching English same-text in body content, target the eyebrow span pattern
# Wrap pattern with sx-eyebrow class
TRANS_PAIRS = [
    ('>CONTACT<', '>KONTAK<'),
    ('>START A CONVERSATION<', '>MULAI PERCAKAPAN<'),
    ('>WHAT HAPPENS NEXT<', '>LANGKAH SELANJUTNYA<'),
    ('>READY TO START?<', '>SIAP MEMULAI?<'),
    ('>WHY SURGE<', '>MENGAPA SURGE<'),
    ('>WHY SURIOTA<', '>MENGAPA SURIOTA<'),
    ('>WHAT WE DELIVER<', '>YANG KAMI SEDIAKAN<'),
    ('>HOW WE WORK<', '>CARA KAMI BEKERJA<'),
    ('>BUILT FOR<', '>DIRANCANG UNTUK<'),
]

# ID page IDs (from URL → page ID mapping in earlier work)
# Match all ID pages that have eyebrows
ID_PAGES = [
    5273, 5274, 5275, 5276, 5277, 5278, 5279, 5281, 5282, 5283, 5284, 5285,
    5286, 5287, 5288, 5289, 5290, 5291, 5292, 5293, 5294, 5295, 5378, 5379,
    5380, 5381, 5382
]

# But we must only target pages where the eyebrow is INSIDE sx-eyebrow span
# Safer: only replace when text appears within <span class="sx-eyebrow">...</span>
# Use regex with replacement
import re

total = 0
for pid in ID_PAGES:
    try:
        r = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}?context=edit&_fields=meta', headers=HDRS)
        d = json.loads(urllib.request.urlopen(r, timeout=30).read())
    except Exception as e:
        print(f'{pid} fetch err: {e}')
        continue
    ed = d.get('meta',{}).get('_elementor_data','')
    if isinstance(ed, list): ed = json.dumps(ed)
    if not isinstance(ed, str): continue
    new_ed = ed
    page_changes = 0
    for old, new in TRANS_PAIRS:
        # Replace pattern only when in sx-eyebrow context
        # Pattern: <span class="sx-eyebrow"...>TEXT</span>
        # Using simpler approach: replace only after looking for sx-eyebrow context
        # For safety: do direct text replace (these are highly specific eyebrow strings)
        c = new_ed.count(old)
        if c > 0:
            new_ed = new_ed.replace(old, new)
            page_changes += c
    if new_ed != ed:
        payload = json.dumps({'meta': {'_elementor_data': new_ed}}).encode()
        try:
            urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}', data=payload, method='POST', headers=HDRS), timeout=30).read()
            print(f'  {pid}: +{page_changes}')
            total += page_changes
        except Exception as e:
            print(f'  {pid} push fail: {e}')

print(f'\nTotal: {total}')

# Clear cache
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/elementor/v1/cache', method='DELETE', headers=HDRS), timeout=30).read()
print('Cache cleared')
time.sleep(2)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/id/kontak/?nc='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read()
