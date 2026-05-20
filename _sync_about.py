"""Sync About Us — clone EN _elementor_data + Bahasa Indonesia translations."""
import json, urllib.request, urllib.error, base64, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization': f'Basic {AUTH}', 'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

# 1) Fetch EN page 29
print('Fetching EN page 29 _elementor_data...')
r = urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages/29?context=edit&_fields=id,meta', headers=HDRS)
en = json.loads(urllib.request.urlopen(r, timeout=60).read())
elementor_data = en['meta']['_elementor_data']
if not isinstance(elementor_data, str):
    elementor_data = json.dumps(elementor_data)
print(f'  EN _elementor_data: {len(elementor_data)} chars')

# 2) Replacements EN → ID. Apply to raw JSON string (preserves HTML structure)
# Order matters: longer phrases first to avoid partial replacements
REPLACEMENTS = [
    # Main headings
    ('Next Gen. Industrial Partner \\u2014 Industrial IoT & System Integration in Batam, Indonesia',
     'Mitra Industri Generasi Baru \\u2014 IoT Industri & Integrasi Sistem di Batam, Indonesia'),
    ('About SURIOTA', 'Tentang SURIOTA'),
    ('Ready to Collaborate with SURIOTA?', 'Siap Berkolaborasi dengan SURIOTA?'),

    # Vision card
    ('01 / VISION', '01 / VISI'),
    ('Transforming industries through smart, connected solutions.',
     'Mentransformasi industri melalui solusi cerdas dan terhubung.'),
    ('Transforming Indonesia&rsquo;s industries through smart, connected end-to-end IoT, AI, and SaaS solutions.',
     'Mentransformasi industri Indonesia melalui solusi IoT, AI, dan SaaS yang cerdas, terhubung, dan menyeluruh.'),

    # Mission card
    ('02 / MISSION', '02 / MISI'),
    ('DELIVER</strong> &mdash; End-to-end solutions connecting hardware, software &amp; cloud.',
     'MENYEDIAKAN</strong> &mdash; Solusi menyeluruh yang menghubungkan hardware, software &amp; cloud.'),
    ('ENABLE</strong> &mdash; Real-time monitoring &amp; data-driven decisions to reduce downtime.',
     'MEMBERDAYAKAN</strong> &mdash; Monitoring real-time &amp; keputusan berbasis data untuk mengurangi downtime.'),
    ('BUILD</strong> &mdash; Cross-sector partnerships: manufacturing, energy, logistics, maritime.',
     'MEMBANGUN</strong> &mdash; Kemitraan lintas sektor: manufaktur, energi, logistik, maritim.'),
    ('DEVELOP</strong> &mdash; Continuous expertise in IoT, AI, and emerging technologies.',
     'MENGEMBANGKAN</strong> &mdash; Keahlian berkelanjutan dalam IoT, AI, dan teknologi terkini.'),
    ('UPHOLD</strong> &mdash; Highest standards of integrity &amp; professionalism.',
     'MENJUNJUNG</strong> &mdash; Standar integritas &amp; profesionalisme tertinggi.'),

    # Hero card
    ('SURIOTA &mdash; Industrial IoT &amp; System Integration', 'SURIOTA &mdash; IoT Industri &amp; Integrasi Sistem'),
    ('is a technology company specializing in <strong>Industrial IoT Services and System Integration</strong>, headquartered in Batam Centre, Riau Islands. Since <strong>January 2023</strong>, we have been designing and manufacturing industrial connectivity solutions &mdash; from Modbus gateways to complete IoT platforms.',
     'adalah perusahaan teknologi yang berfokus pada <strong>Layanan IoT Industri dan Integrasi Sistem</strong>, berkantor pusat di Batam Centre, Kepulauan Riau. Sejak <strong>Januari 2023</strong>, kami merancang dan memproduksi solusi konektivitas industri &mdash; dari gateway Modbus hingga platform IoT lengkap.'),
    ('industrial projects</strong> across <a href=\\"https://suriota.com/automation/\\" style=\\"color:#205B69;text-decoration:none;font-weight:600;border-bottom:1px solid #C8851F;\\">manufacturing</a>, <a href=\\"https://suriota.com/renewable-energy/\\" style=\\"color:#205B69;text-decoration:none;font-weight:600;border-bottom:1px solid #C8851F;\\">energy</a>, logistics, and maritime sectors. In-house products:',
     'proyek industri</strong> di sektor <a href=\\"https://suriota.com/automation/\\" style=\\"color:#205B69;text-decoration:none;font-weight:600;border-bottom:1px solid #C8851F;\\">manufaktur</a>, <a href=\\"https://suriota.com/renewable-energy/\\" style=\\"color:#205B69;text-decoration:none;font-weight:600;border-bottom:1px solid #C8851F;\\">energi</a>, logistik, dan maritim. Produk in-house:'),
    ('IIoT platform (Energy Mapping, Water Analytic, Vessel Tracking),', 'platform IIoT (Energy Mapping, Water Analytic, Vessel Tracking),'),
    ('gateway, RS-485 SPD,', 'gateway, RS-485 SPD,'),
    ('Independent &middot; Self-funded &middot; Integrity &amp; Technical Excellence',
     'Independen &middot; Mandiri &middot; Integritas &amp; Keunggulan Teknis'),

    # CIPTA section
    ('SURIOTA Core Values', 'Nilai-Nilai Inti SURIOTA'),
    ('CIPTA &mdash; Core Values', 'CIPTA &mdash; Nilai-Nilai Inti'),
    ('Five principles guiding every SURIOTA project, execution, and partnership.',
     'Lima prinsip yang membimbing setiap proyek, eksekusi, dan kemitraan SURIOTA.'),
    ('Committed Outcome', 'Komitmen pada Hasil'),
    ('Consistent focus on the best results &amp; defined targets.',
     'Fokus konsisten pada hasil terbaik &amp; target yang jelas.'),
    ('Integrity of Innovation', 'Integritas dalam Inovasi'),
    ('Innovating with honesty, ethics, &amp; responsibility.',
     'Berinovasi dengan kejujuran, etika, &amp; tanggung jawab.'),
    ('Precision in Execution', 'Presisi dalam Eksekusi'),
    ('Precision, discipline, &amp; high quality standards.',
     'Presisi, disiplin, &amp; standar kualitas tinggi.'),
    ('Trust Through Reliability', 'Kepercayaan melalui Keandalan'),
    ('Consistency, dependability, &amp; commitment.',
     'Konsistensi, ketepatan, &amp; komitmen.'),
    ('Adaptive Growth', 'Pertumbuhan Adaptif'),
    ('Embracing change &amp; continuous improvement.',
     'Merangkul perubahan &amp; peningkatan berkelanjutan.'),

    # CTA section
    ('Discuss your engineering needs with the SURIOTA team. Response within 1 business day.',
     'Diskusikan kebutuhan engineering Anda dengan tim SURIOTA. Respon dalam 1 hari kerja.'),
    ('Download Company Profile', 'Unduh Company Profile'),
    ('Free Consultation', 'Konsultasi Gratis'),
    ('Free consultation via form', 'Konsultasi gratis via formulir'),
    ('Hello%20SURIOTA%2C%20I%27d%20like%20to%20discuss%20an%20engineering%20project.%20Please%20share%20more%20information.',
     'Halo%20SURIOTA%2C%20saya%20ingin%20diskusi%20proyek%20engineering.%20Mohon%20info%20lebih%20lanjut.'),

    # About Us labels
    ('\\"sx-eyebrow\\" style=\\"margin-bottom:10px;display:inline-block;\\">About Us<',
     '\\"sx-eyebrow\\" style=\\"margin-bottom:10px;display:inline-block;\\">Tentang Kami<'),

    # AboutPage schema
    ('"inLanguage": "en"', '"inLanguage": "id"'),
    ('"url": "https://suriota.com/about-us/"', '"url": "https://suriota.com/id/tentang-kami/"'),
    ('"name": "About SURIOTA \\u2014 Next Gen. Industrial Partner"',
     '"name": "Tentang SURIOTA \\u2014 Mitra Industri Generasi Baru"'),

    # BreadcrumbList
    ('"name": "Home", "item": "https://suriota.com/"',
     '"name": "Beranda", "item": "https://suriota.com/id/beranda/"'),
    ('"name": "About Us", "item": "https://suriota.com/about-us/"',
     '"name": "Tentang Kami", "item": "https://suriota.com/id/tentang-kami/"'),
]

# Apply replacements
id_data = elementor_data
applied = 0
for en_str, id_str in REPLACEMENTS:
    if en_str in id_data:
        id_data = id_data.replace(en_str, id_str)
        applied += 1
    else:
        print(f'  WARN: not found: {en_str[:60]}...')
print(f'\nApplied {applied}/{len(REPLACEMENTS)} replacements')
print(f'Result size: {len(id_data)} chars')

# 3) Push to ID page 5274
payload = json.dumps({'meta': {'_elementor_data': id_data}}).encode()
req = urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages/5274', data=payload, method='POST', headers=HDRS)
try:
    resp = urllib.request.urlopen(req, timeout=60).read()
    print('\nPushed to ID page 5274 — OK')
except urllib.error.HTTPError as e:
    print(f'\nPUSH FAIL: HTTP {e.code} {e.read().decode()[:300]}')
