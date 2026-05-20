import urllib.request, re, time, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

pages = [
    ('https://suriota.com/portfolio/', 'Portfolio'),
    ('https://suriota.com/suriota-modbus-gateway/', 'SRT-MGATE'),
    ('https://suriota.com/surge-energy-mapping/', 'SURGE-E'),
    ('https://suriota.com/surge-water-analytic/', 'SURGE-W'),
    ('https://suriota.com/surge-vessel-tracking/', 'SURGE-V'),
    ('https://suriota.com/iso-m485-series/', 'ISO-M485'),
    ('https://suriota.com/thm-30md/', 'THM-30MD'),
    ('https://suriota.com/pm1611-wd/', 'PM1611-WD'),
    ('https://suriota.com/rs-485-surge-protector-spd-t485-105/', 'SPD-T485'),
    ('https://suriota.com/waste-water-logger/', 'WW Logger'),
    ('https://suriota.com/software-as-a-service/', 'SaaS'),
    ('https://suriota.com/about-us/', 'About'),
]
og_re = re.compile(r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', re.I)
tw_re = re.compile(r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)["\']', re.I)

for url, lbl in pages:
    r = urllib.request.Request(url + '?cb=' + str(int(time.time())), headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(r, timeout=30).read().decode('utf-8', errors='replace')
    og = og_re.search(html)
    tw = tw_re.search(html)
    og_short = og.group(1).rsplit('/', 1)[-1][:50] if og else 'N/A'
    tw_short = tw.group(1).rsplit('/', 1)[-1][:50] if tw else 'N/A'
    print(f'{lbl:12} og={og_short:50} tw={tw_short:50}')
