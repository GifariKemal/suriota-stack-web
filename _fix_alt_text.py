"""Fix missing alt text on 5 images via WP REST media endpoint."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import json, urllib.request, urllib.error, base64

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization': f'Basic {AUTH}', 'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

# (search slug fragment, alt text)
FIXES = [
    ('surge-eco-poster',  'SURGE Energy Mapping — multi-location kWh monitoring dashboard for industrial energy savings'),
    ('modbus-poster',     'SRT-MGATE-1210 Modbus Gateway IIoT — RTU/TCP to MQTT industrial gateway by SURIOTA'),
    ('Porto',             'SURIOTA portfolio — 64+ industrial IoT, automation, water treatment & renewable energy projects across Indonesia'),
    ('GTWY-SRT-VD',       'SRT-MGATE-1210 Modbus Gateway product photo — vertical view of industrial IIoT gateway by SURIOTA'),
    ('SURGE-WA',          'SURGE Water Analytics dashboard — KLHK SPARING compliant real-time pH, COD, TSS, NH3 monitoring'),
]

def search_media(slug):
    """Search media library for filename containing slug. Returns first match id."""
    r = urllib.request.Request(
        f'https://suriota.com/wp-json/wp/v2/media?search={urllib.parse.quote(slug)}&per_page=5&_fields=id,slug,source_url,alt_text',
        headers=HDRS
    )
    try:
        d = json.loads(urllib.request.urlopen(r, timeout=30).read())
        return d
    except Exception as e:
        return []

def update_alt(media_id, alt):
    payload = json.dumps({'alt_text': alt}).encode()
    req = urllib.request.Request(
        f'https://suriota.com/wp-json/wp/v2/media/{media_id}',
        data=payload, method='POST', headers=HDRS
    )
    try:
        urllib.request.urlopen(req, timeout=30).read()
        return True
    except urllib.error.HTTPError as e:
        print(f'  HTTP {e.code}: {e.read().decode()[:200]}')
        return False

import urllib.parse

for slug, alt in FIXES:
    print(f'\n[{slug}]')
    results = search_media(slug)
    if not results:
        print('  not found')
        continue
    # find best match by slug containing the fragment
    best = None
    for m in results:
        if slug.lower() in m['source_url'].lower():
            best = m
            break
    if not best:
        best = results[0]
    print(f"  id={best['id']} slug={best['slug']} current_alt='{best['alt_text']}'")
    ok = update_alt(best['id'], alt)
    print(f"  UPDATED alt → '{alt[:60]}...' {'OK' if ok else 'FAIL'}")
