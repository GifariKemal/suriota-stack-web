import urllib.request, re, time

pages = [
    ('https://suriota.com/electrical/', 'Electrical'),
    ('https://suriota.com/automation/', 'Automation'),
    ('https://suriota.com/water-treatment/', 'Water Treatment'),
    ('https://suriota.com/renewable-energy/', 'Renewable Energy'),
]

for url, lbl in pages:
    r = urllib.request.Request(url + '?cb=' + str(int(time.time())), headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(r).read().decode('utf-8', errors='replace')
    h1 = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.I | re.DOTALL)
    h2s = re.findall(r'<h2[^>]*>(.*?)</h2>', html, re.I | re.DOTALL)
    chips = re.findall(r'class="sx-chip"[^>]*>([^<]+)<', html)

    def clean(s):
        return re.sub(r'<[^>]+>', '', s or '').strip()[:220]

    print(f'\n[{lbl}]')
    print(f'  H1: {clean(h1.group(1)) if h1 else "N/A"}')
    print(f'  H2[0]: {clean(h2s[0]) if h2s else "N/A"}')
    if len(h2s) > 1:
        print(f'  H2[1]: {clean(h2s[1])}')
    print(f'  Industry chips ({len(chips)}): {[c.strip()[:30] for c in chips[:10]]}')
