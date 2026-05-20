import urllib.request, base64, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization': f'Basic {AUTH}', 'User-Agent': 'Mozilla/5.0'}

# Get raw HTML
r = urllib.request.Request('https://suriota.com/about-us/?cb=raw', headers=HDRS)
html = urllib.request.urlopen(r, timeout=30).read().decode('utf-8', errors='replace')

blocks = re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', html, re.DOTALL)
b = blocks[4]

# Print raw bytes around suspicious position 2631
print('Raw chars 2620-2660:')
for i, c in enumerate(b[2620:2680], start=2620):
    print(f'  [{i}] {repr(c)} {ord(c):#x}')
