import urllib.request, re, time

pages = [
    ('https://suriota.com/internet-of-things/', 'IoT'),
    ('https://suriota.com/data-analytics/', 'Data Analytics'),
    ('https://suriota.com/digital-consulting/', 'Digital Consulting'),
    ('https://suriota.com/software-as-a-service/', 'SaaS SURGE'),
    ('https://suriota.com/suriota-modbus-gateway/', 'SRT-MGATE'),
    ('https://suriota.com/surge-energy-mapping/', 'SURGE-Energy'),
    ('https://suriota.com/surge-vessel-tracking/', 'SURGE-Vessel'),
    ('https://suriota.com/surge-water-analytic/', 'SURGE-Water'),
    ('https://suriota.com/iso-m485-series/', 'ISO-M485'),
    ('https://suriota.com/thm-30md/', 'THM-30MD'),
    ('https://suriota.com/pm1611-wd/', 'PM1611-WD'),
    ('https://suriota.com/rs-485-surge-protector-spd-t485-105/', 'SPD-T485'),
    ('https://suriota.com/waste-water-logger/', 'WW Logger'),
    ('https://suriota.com/artikel/', 'Artikel'),
]

for url, lbl in pages:
    try:
        r = urllib.request.Request(url + '?cb=' + str(int(time.time())), headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(r, timeout=20).read().decode('utf-8', errors='replace')
        title = re.search(r'<title>(.*?)</title>', html, re.I)
        desc = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', html, re.I)
        print(f'\n[{lbl}]')
        print(f'  T: {title.group(1) if title else "N/A"}')
        print(f'  D: {desc.group(1)[:140] if desc else "N/A"}')
    except Exception as e:
        print(f'[{lbl}] ERR: {e}')
