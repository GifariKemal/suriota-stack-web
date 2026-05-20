"""Apply A v2: Comprehensive mixed language fix on ID pages."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

FIXES = {
    # ID-Contact (5378) — FAQ + section translations
    5378: [
        # FAQ #1
        ('How quickly can SURIOTA respond?', 'Seberapa cepat SURIOTA merespons?'),
        ('We reply within 24 hours on business days. For urgent matters or live discussions, WhatsApp is the fastest channel.',
         'Kami merespons dalam 24 jam di hari kerja. Untuk hal mendesak atau diskusi langsung, WhatsApp adalah channel tercepat.'),
        # FAQ #2
        ('Do you serve clients outside Batam?', 'Apakah Anda melayani klien di luar Batam?'),
        ('Yes - SURIOTA has completed 64+ proyek di seluruh Indonesia in manufaktur, energi, maritim, and utilities. Our team travels for site surveys, commissioning, and on-site training.',
         'Ya - SURIOTA telah menyelesaikan 64+ proyek di seluruh Indonesia di sektor manufaktur, energi, maritim, dan utilitas. Tim kami bepergian untuk site survey, commissioning, dan training on-site.'),
        # FAQ #4 answer
        ('For the fastest RFQ turnaround: proyek type, scale (sensors \\/ sites \\/ users), expected timeline, location, compliance needs (KLHK \\u00b7 SNI \\u00b7 IEC \\u00b7 PUIL), and any current pain points.',
         'Untuk RFQ tercepat: jenis proyek, skala (sensor \\/ lokasi \\/ user), timeline yang diharapkan, lokasi, kebutuhan compliance (KLHK \\u00b7 SNI \\u00b7 IEC \\u00b7 PUIL), dan pain point yang Anda hadapi saat ini.'),
        # FAQ #5 answer
        ('Yes - we provide tiered support contracts for SURGE platform deployments, Modbus Gateway fleets, and SCADA \\/ PLC installations. Hubungi us for SLA options.',
         'Ya - kami menyediakan tiered support contract untuk deployment platform SURGE, fleet Modbus Gateway, dan instalasi SCADA \\/ PLC. Hubungi kami untuk opsi SLA.'),
        # FAQ #6
        ('Where can I purchase SURIOTA hardware products?', 'Di mana saya bisa membeli produk hardware SURIOTA?'),
        ('For Modbus Gateway, ISO-M485, THM-30MD, PM1611-WD, and RS-485 SPD - visit our official Tokopedia store or contact us for bulk pricing and proyek quotations.',
         'Untuk Modbus Gateway, ISO-M485, THM-30MD, PM1611-WD, dan RS-485 SPD - kunjungi toko resmi Tokopedia kami atau hubungi kami untuk harga bulk dan quotation proyek.'),
        # Section header
        ('WHAT TO INCLUDE IN YOUR MESSAGE', 'YANG PERLU DICANTUMKAN DI PESAN'),
    ],
    # ID-Privacy (5379)
    5379: [
        ('We may update this Kebijakan Privasi from time to time. The latest version will always be posted on this page, with the \\u201cLast updated\\u201d date revised. Material changes will be communicated by email or prominent notice on our website at least 14 days before they take effect.',
         'Kami dapat memperbarui Kebijakan Privasi ini dari waktu ke waktu. Versi terbaru akan selalu diposting di halaman ini, dengan tanggal \\u201cLast updated\\u201d direvisi. Perubahan material akan dikomunikasikan via email atau notifikasi yang jelas di website kami paling lambat 14 hari sebelum berlaku.'),
    ],
}

total = 0
miss = []
for pid, pairs in FIXES.items():
    r = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}?context=edit&_fields=meta', headers=HDRS)
    d = json.loads(urllib.request.urlopen(r, timeout=30).read())
    ed = d.get('meta',{}).get('_elementor_data','')
    if isinstance(ed, list): ed = json.dumps(ed)
    if not isinstance(ed, str): continue
    new_ed = ed
    changes = 0
    for old, new in pairs:
        c = new_ed.count(old)
        if c > 0:
            new_ed = new_ed.replace(old, new)
            changes += c
        else:
            miss.append((pid, old[:80]))
    if new_ed != ed:
        payload = json.dumps({'meta': {'_elementor_data': new_ed}}).encode()
        urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}', data=payload, method='POST', headers=HDRS), timeout=30).read()
        print(f'  {pid}: +{changes}')
        total += changes

print(f'\nTotal: {total}')
if miss:
    print(f'\nMisses ({len(miss)}):')
    for pid, t in miss:
        print(f'  {pid}: "{t}"')

# Clear cache
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/elementor/v1/cache', method='DELETE', headers=HDRS), timeout=30).read()
time.sleep(2)
for url in ['https://suriota.com/id/kontak/', 'https://suriota.com/id/kebijakan-privasi/']:
    try: urllib.request.urlopen(urllib.request.Request(url+'?nc='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read()
    except: pass
print('Done')
