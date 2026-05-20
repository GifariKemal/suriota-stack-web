import urllib.request, re, time, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

urls = [
    ('https://suriota.com/id/beranda/', 'ID Beranda'),
    ('https://suriota.com/id/tentang-kami/', 'ID Tentang'),
    ('https://suriota.com/id/portfolio-id/', 'ID Portfolio'),
    ('https://suriota.com/id/water-treatment-id/', 'ID WT'),
    ('https://suriota.com/id/saas-id/', 'ID SaaS'),
    ('https://suriota.com/id/artikel-id/', 'ID Artikel'),
    ('https://suriota.com/id/magang-srt-team/', 'ID Magang'),
]
title_re = re.compile(r'<title>(.*?)</title>', re.I)
desc_re = re.compile(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)["\']', re.I)
hreflang_re = re.compile(r'<link[^>]+hreflang=["\']([a-z-]+)["\'][^>]+href=["\']([^"\']+)["\']', re.I)

for url, lbl in urls:
    try:
        r = urllib.request.Request(url + '?cb=' + str(int(time.time())), headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(r, timeout=30).read().decode('utf-8', errors='replace')
        title = title_re.search(html)
        desc = desc_re.search(html)
        hreflang = hreflang_re.findall(html)
        print(f'\n[{lbl}] {url}')
        print(f'  Title: {title.group(1) if title else "N/A"}')
        print(f'  Desc:  {(desc.group(1)[:130] if desc else "N/A")}')
        print(f'  hreflang ({len(hreflang)}):')
        for h, link in hreflang[:5]:
            print(f'    {h} -> {link}')
    except Exception as e:
        print(f'[{lbl}] ERR: {e}')
