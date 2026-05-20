"""Apply A: Fix mixed-language English content on ID pages."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

# Per-page translation pairs (text only, exact match)
FIXES = {
    # ID-Portfolio (5275)
    5275: [
        ('Free consultation, response dalam 1 hari kerja.', 'Konsultasi gratis, respons dalam 1 hari kerja.'),
    ],
    # ID-Contact (5378)
    5378: [
        # Hero subtitle
        ('Whether you are scoping an IoT deployment, evaluating our SURGE platform, or looking for SCADA \\/ PLC integration - we will match you with the right engineer within 24 hours.',
         'Baik Anda sedang merancang deployment IoT, mengevaluasi platform SURGE kami, atau membutuhkan integrasi SCADA \\/ PLC - kami akan menghubungkan Anda dengan engineer yang tepat dalam 24 jam.'),
        # FAQ entries
        ('Can I request a free consultation?', 'Apakah saya bisa request konsultasi gratis?'),
        ('Absolutely. We offer a 30-minute discovery call with one of our engineers - free, no obligation. Reach us via WhatsApp or email admin@suriota.com to schedule.',
         'Tentu. Kami menawarkan discovery call 30 menit dengan salah satu engineer kami - gratis, tanpa kewajiban. Hubungi via WhatsApp atau email admin@suriota.com untuk menjadwalkan.'),
        ('What information should I prepare before contacting?', 'Informasi apa yang perlu saya siapkan sebelum menghubungi?'),
        ('For the fastest RFQ turnaround: proyek type, scale (sensors \\/ sites \\/ users), expected timeline, location, compliance needs (KLHK \\u2026)',
         'Untuk RFQ tercepat: jenis proyek, skala (sensor \\/ lokasi \\/ user), timeline yang diharapkan, lokasi, kebutuhan compliance (KLHK \\u2026)'),
        # Section header
        ('WHAT TO INCLUDE IN YOUR MESSAGE', 'YANG PERLU DICANTUMKAN DI PESAN'),
    ],
    # ID-SURGE-E (5288)
    5288: [
        ('Request a free demo of SURGE Energy Mapping. We&#39;ll walk you through a real dashboard with your property type in under 24 hours.',
         'Minta demo gratis SURGE Energy Mapping. Kami akan memandu Anda melalui dashboard nyata dengan tipe properti Anda dalam waktu kurang dari 24 jam.'),
        ('Request a free demo of SURGE Energy Mapping. We\\u2019ll walk you through a real dashboard with your property type in under 24 hours.',
         'Minta demo gratis SURGE Energy Mapping. Kami akan memandu Anda melalui dashboard nyata dengan tipe properti Anda dalam waktu kurang dari 24 jam.'),
    ],
    # ID-Privacy (5379)
    5379: [
        ('please contact us so we can delete it.', 'silakan hubungi kami agar kami dapat menghapusnya.'),
        ('We may update this Kebijakan Privasi from time to time. The latest version will always be posted on this page, with the \\u201cLast updated\\u201d date revised. Material changes will be communicated by email or platform notice at least 14 days in advance.',
         'Kami dapat memperbarui Kebijakan Privasi ini dari waktu ke waktu. Versi terbaru akan selalu diposting di halaman ini, dengan tanggal \\u201cLast updated\\u201d direvisi. Perubahan material akan dikomunikasikan via email atau notifikasi platform paling lambat 14 hari sebelumnya.'),
        ('for IoT deployments using the SURGE platform, we collect device identifiers, sensor readings, geolocation (when consented), and event logs strictly for the purpose of operating the contracted service.',
         'untuk deployment IoT yang menggunakan platform SURGE, kami mengumpulkan identifier perangkat, pembacaan sensor, geolokasi (jika disetujui), dan log event semata-mata untuk tujuan mengoperasikan layanan yang disepakati.'),
    ],
}

total = 0
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
            print(f'  {pid} miss: "{old[:60]}..."')
    if new_ed != ed:
        payload = json.dumps({'meta': {'_elementor_data': new_ed}}).encode()
        urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}', data=payload, method='POST', headers=HDRS), timeout=30).read()
        print(f'  {pid}: +{changes}')
        total += changes

print(f'\nTotal: {total}')

# Clear cache
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/elementor/v1/cache', method='DELETE', headers=HDRS), timeout=30).read()
time.sleep(2)
for url in ['https://suriota.com/id/kontak/', 'https://suriota.com/id/kebijakan-privasi/', 'https://suriota.com/id/surge-energy-mapping-id/']:
    try: urllib.request.urlopen(urllib.request.Request(url+'?nc='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read()
    except: pass
print('Done')
