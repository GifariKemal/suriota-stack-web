"""Find the bad escape sequence in About page JSON-LD."""
import json, urllib.request, base64, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization': f'Basic {AUTH}', 'User-Agent': 'Mozilla/5.0'}

r = urllib.request.Request('https://suriota.com/about-us/?cb=findbad', headers=HDRS)
html = urllib.request.urlopen(r, timeout=30).read().decode('utf-8', errors='replace')

blocks = re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.DOTALL)
print(f'Found {len(blocks)} JSON-LD blocks')

for i, b in enumerate(blocks):
    try:
        json.loads(b)
        print(f'  Block {i}: OK (len {len(b)})')
    except json.JSONDecodeError as e:
        print(f'\nINVALID Block {i}: {e}')

# Inspect block 4 in detail — find non-standard escapes
print('\n--- Block 4 ---')
b = blocks[4]
# Browser JSON.parse rejects: \', \v, \x, \0, unescaped control chars
suspicious = re.finditer(r"\\.", b)
seen = set()
for m in suspicious:
    s = m.group(0)
    if s in seen: continue
    seen.add(s)
    print(f"Found escape: {repr(s)}")

# Check position 2631
print(f'\nBlock 4 around position 2631:')
print(repr(b[2580:2680]))
