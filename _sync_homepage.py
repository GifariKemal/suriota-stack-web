"""Sync Homepage — clone EN _elementor_data + Bahasa translations."""
import json, urllib.request, urllib.error, base64, sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization': f'Basic {AUTH}', 'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

EN_ID = 12
ID_ID = 5273

print(f'Fetching EN page {EN_ID}...')
r = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{EN_ID}?context=edit&_fields=meta', headers=HDRS)
en = json.loads(urllib.request.urlopen(r, timeout=60).read())
ed = en['meta']['_elementor_data']
if not isinstance(ed, str): ed = json.dumps(ed)
en_page_settings = en['meta'].get('_elementor_page_settings', {})
print(f'  Size: {len(ed)} chars')

# Translation pairs (order: long-first to avoid partial matches)
REPLACEMENTS = [
    # === Hero ===
    ('Next Gen. Industrial Partner', 'Mitra Industri Generasi Baru'),
    ('PT Surya Inovasi Prioritas', 'PT Surya Inovasi Prioritas'),  # keep
    ('is a technology company specializing in <strong>Industrial IoT &amp; System Integration</strong>, headquartered in Batam, Riau Islands. Since January 2023, we have delivered',
     'adalah perusahaan teknologi yang berfokus pada <strong>IoT Industri &amp; Integrasi Sistem</strong>, berkantor pusat di Batam, Kepulauan Riau. Sejak Januari 2023, kami telah menyelesaikan'),
    ('64+ industrial projects', '64+ proyek industri'),
    ('from Modbus gateways to complete IoT platforms across manufacturing, energy, logistics, and maritime sectors.',
     'dari gateway Modbus hingga platform IoT lengkap untuk sektor manufaktur, energi, logistik, dan maritim.'),

    # === 5 Core Services ===
    ('OUR 5 CORE SERVICES', '5 LAYANAN INTI KAMI'),
    ('IoT &amp; System Integration', 'IoT &amp; Integrasi Sistem'),
    ('End-to-end Industrial IoT \\u2014 Modbus gateway, MQTT, edge computing, SCADA, sensor-to-cloud pipelines with IEC 62443 security for manufacturing, oil &amp; gas, and maritime operations.',
     'IoT Industri menyeluruh \\u2014 gateway Modbus, MQTT, edge computing, SCADA, pipeline sensor-ke-cloud dengan keamanan IEC 62443 untuk manufaktur, oil &amp; gas, dan operasi maritim.'),
    ('AI &amp; Data Analytics', 'AI &amp; Analitik Data'),
    ('Predictive maintenance, OEE dashboards, computer-vision QC, and real-time operational intelligence \\u2014 turning raw machine data into actionable plant-floor decisions.',
     'Predictive maintenance, dashboard OEE, computer-vision QC, dan intelligence operasional real-time \\u2014 mengubah data mesin menjadi keputusan plant-floor yang actionable.'),
    ('Software as a Service', 'Software sebagai Layanan'),
    ('SURGE multi-tenant IoT platform \\u2014 Energy Mapping (kWh, power factor), Water Analytic (KLHK SPARING compliance), Vessel Tracking (fleet + fuel monitoring).',
     'Platform IoT multi-tenant SURGE \\u2014 Energy Mapping (kWh, power factor), Water Analytic (compliance SPARING KLHK), Vessel Tracking (armada + monitoring bahan bakar).'),
    ('Automation &amp; Renewable Energy', 'Otomasi &amp; Energi Terbarukan'),
    ('PLC integration, SCADA modernization, Solar PV PLTS design, hybrid PLTS-PLTB systems, and smart street light (PJU) \\u2014 turnkey industrial energy transition.',
     'Integrasi PLC, modernisasi SCADA, desain Solar PV PLTS, sistem hybrid PLTS-PLTB, dan smart street light (PJU) \\u2014 transisi energi industri turnkey.'),
    ('Digital Consulting', 'Digital Consulting'),  # keep
    ('Industry 4.0 roadmap, OT/IT convergence assessment, IIoT readiness audit, SCADA modernization, and cloud migration strategy for Indonesian manufacturers.',
     'Roadmap Industry 4.0, assessment konvergensi OT/IT, audit kesiapan IIoT, modernisasi SCADA, dan strategi migrasi cloud untuk manufaktur Indonesia.'),

    # === Trust line ===
    ('With our commitment to the highest technical standards, SURIOTA is a trusted partner in improving efficiency, productivity, and business sustainability for clients across Indonesia.',
     'Dengan komitmen kami terhadap standar teknis tertinggi, SURIOTA adalah mitra terpercaya dalam meningkatkan efisiensi, produktivitas, dan keberlanjutan bisnis klien di seluruh Indonesia.'),

    # === Buttons ===
    ('Free Consultation', 'Konsultasi Gratis'),
    ('View All Portfolio', 'Lihat Semua Portfolio'),

    # === Capabilities section ===
    ('Capabilities', 'Kapabilitas'),
    ('Industrial Projects', 'Proyek Industri'),
    ('In-House Products', 'Produk In-House'),
    ('Core Services', 'Layanan Inti'),
    ('Team Professionals', 'Profesional Tim'),

    # === Section headings ===
    ('>Products<', '>Produk<'),
    ('>Trusted By<', '>Dipercaya Oleh<'),
    ('>Portfolio<', '>Portfolio<'),
    ('>Our Location<', '>Lokasi Kami<'),
    ('>Contact Us<', '>Hubungi Kami<'),

    # === Form ===
    ('"text":"SEND"', '"text":"KIRIM"'),
    ('"button_text":"SEND"', '"button_text":"KIRIM"'),
    ('"button_text":"Send"', '"button_text":"Kirim"'),

    # === Image labels ===
    ('aria-label=\\"IoT & System Integration\\"', 'aria-label=\\"IoT & Integrasi Sistem\\"'),
    ('aria-label=\\"AI & Data Analytics\\"', 'aria-label=\\"AI & Analitik Data\\"'),
    ('aria-label=\\"SaaS SURGE Platform\\"', 'aria-label=\\"Platform SaaS SURGE\\"'),
    ('aria-label=\\"Automation & Renewable Energy\\"', 'aria-label=\\"Otomasi & Energi Terbarukan\\"'),
    ('aria-label=\\"Digital Consulting\\"', 'aria-label=\\"Digital Consulting\\"'),
]

applied = 0
not_found = []
id_data = ed
for en, idt in REPLACEMENTS:
    if en in id_data:
        id_data = id_data.replace(en, idt)
        applied += 1
    else:
        not_found.append(en[:70])

print(f'\nApplied {applied}/{len(REPLACEMENTS)} replacements')
if not_found:
    print(f'Not found ({len(not_found)}):')
    for nf in not_found[:5]: print(f'  - {nf}...')

# Push
payload = json.dumps({'meta': {'_elementor_data': id_data, '_elementor_page_settings': en_page_settings, '_elementor_edit_mode': 'builder', '_elementor_template_type': 'wp-page'}}).encode()
req = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{ID_ID}', data=payload, method='POST', headers=HDRS)
try:
    urllib.request.urlopen(req, timeout=60).read()
    print(f'\nPushed to ID page {ID_ID} OK')
except urllib.error.HTTPError as e:
    print(f'PUSH FAIL: {e.code} {e.read().decode()[:300]}')

# Purge
purge = '''
$upload = wp_upload_dir();
$log = $upload['basedir'].'/purge-sync-hp.txt';
if (file_exists($log)) { if (function_exists('code_snippets')) { code_snippets()->deactivate(5); } return; }
if (class_exists('\\\\Elementor\\\\Plugin')) {
    $f = \\Elementor\\Core\\Files\\CSS\\Post::create(''' + str(ID_ID) + ''');
    if ($f) { $f->delete(); $f->update(); }
    \\Elementor\\Plugin::instance()->files_manager->clear_cache();
}
if (class_exists('WPO_Page_Cache')) WPO_Page_Cache::instance()->purge();
if (class_exists('WP_Optimize_Minify_Cache_Functions')) \\WP_Optimize_Minify_Cache_Functions::purge();
wp_cache_flush();
file_put_contents($log, 'done');
if (function_exists('code_snippets')) { code_snippets()->deactivate(5); }
'''
data = json.dumps({'code': purge, 'active': True, 'name': 'SX: purge sync hp'}).encode()
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=data, method='POST', headers=HDRS), timeout=60).read()
time.sleep(2)
urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/id/beranda/?cb={int(time.time())}', headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print('purged + triggered')
