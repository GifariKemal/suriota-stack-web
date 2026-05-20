"""Pre-warm WPO Minify cache for all key pages."""
import sys, io, urllib.request, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

URLS = [
    'https://suriota.com/',
    'https://suriota.com/about/',
    'https://suriota.com/portfolio/',
    'https://suriota.com/contact/',
    'https://suriota.com/automation/',
    'https://suriota.com/electrical/',
    'https://suriota.com/renewable-energy/',
    'https://suriota.com/internet-of-things/',
    'https://suriota.com/water-treatment/',
    'https://suriota.com/data-analytics/',
    'https://suriota.com/digital-consulting/',
    'https://suriota.com/artificial-intelligence/',
    'https://suriota.com/system-integration/',
    'https://suriota.com/saas/',
    'https://suriota.com/surge-energy-mapping/',
    'https://suriota.com/surge-vessel-tracking/',
    'https://suriota.com/surge-water-analytic/',
    'https://suriota.com/suriota-modbus-gateway/',
    'https://suriota.com/iso-m485-series/',
    'https://suriota.com/pm1611-wd/',
    'https://suriota.com/thm-30md/',
    'https://suriota.com/rs-485-surge-protector/',
    'https://suriota.com/waste-water-logger/',
    'https://suriota.com/privacy-policy/',
    'https://suriota.com/terms-of-service/',
    'https://suriota.com/id/beranda/',
    'https://suriota.com/id/tentang-kami/',
    'https://suriota.com/id/portfolio-id/',
    'https://suriota.com/id/kontak/',
    'https://suriota.com/id/automation-id/',
    'https://suriota.com/id/electrical-id/',
    'https://suriota.com/id/renewable-energy-id/',
    'https://suriota.com/id/internet-of-things-id/',
    'https://suriota.com/id/water-treatment-id/',
    'https://suriota.com/id/data-analytics-id/',
    'https://suriota.com/id/digital-consulting-id/',
    'https://suriota.com/id/artificial-intelligence-id/',
    'https://suriota.com/id/system-integration-id/',
    'https://suriota.com/id/saas-id/',
    'https://suriota.com/id/surge-energy-mapping-id/',
    'https://suriota.com/id/surge-vessel-tracking-id/',
    'https://suriota.com/id/surge-water-analytic-id/',
    'https://suriota.com/id/suriota-modbus-gateway-id/',
    'https://suriota.com/id/iso-m485-series-id/',
    'https://suriota.com/id/pm1611-wd-id/',
    'https://suriota.com/id/thm-30md-id/',
    'https://suriota.com/id/rs-485-surge-protector-id/',
    'https://suriota.com/id/waste-water-logger-id/',
    'https://suriota.com/id/kebijakan-privasi/',
    'https://suriota.com/id/syarat-layanan/',
    'https://suriota.com/id/magang-srt-team/',
    'https://suriota.com/id/artikel-id/',
]

HDRS = {'User-Agent':'Mozilla/5.0 (Cache-Warmer)'}
total = 0
slow = 0
for url in URLS:
    start = time.time()
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=HDRS), timeout=60)
        body = r.read()
        elapsed = (time.time() - start) * 1000
        cached = r.headers.get('WPO-Cache-Status','?')
        marker = '🐌' if elapsed > 3000 else '⚡' if elapsed < 1000 else '·'
        print(f'  {marker} {elapsed:5.0f}ms [{cached}] {url[28:]}')
        if elapsed > 3000: slow += 1
        total += 1
    except Exception as e:
        print(f'  ERR {url}: {str(e)[:60]}')

print(f'\nWarmed {total} pages, {slow} took >3s (cache miss → now cached)')

# Second pass — should ALL be fast now
print('\n=== Pass 2 (should all be cached) ===')
for url in URLS[:6]:
    start = time.time()
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers=HDRS), timeout=30)
        r.read()
        elapsed = (time.time() - start) * 1000
        cached = r.headers.get('WPO-Cache-Status','?')
        print(f'  {elapsed:5.0f}ms [{cached}] {url[28:]}')
    except Exception as e:
        print(f'  err {url}: {e}')
