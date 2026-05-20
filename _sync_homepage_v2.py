"""Sync Homepage v2 — fix missed replacements."""
import json, urllib.request, urllib.error, base64, sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization': f'Basic {AUTH}', 'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

# Fetch current ID 5273 data (already partially translated)
r = urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages/5273?context=edit&_fields=meta', headers=HDRS)
idp = json.loads(urllib.request.urlopen(r, timeout=60).read())
ed = idp['meta']['_elementor_data']
if not isinstance(ed, str): ed = json.dumps(ed)
print(f'Current ID 5273 size: {len(ed)} chars')

# v2 replacements — character-level (& not &amp;), and missed strings
REPLACEMENTS_V2 = [
    # Service card titles (& issue)
    ('IoT &amp; System Integration', 'IoT &amp; Integrasi Sistem'),
    ('IoT & System Integration', 'IoT & Integrasi Sistem'),
    ('AI &amp; Data Analytics', 'AI &amp; Analitik Data'),
    ('AI & Data Analytics', 'AI & Analitik Data'),
    ('Automation &amp; Renewable Energy', 'Otomasi &amp; Energi Terbarukan'),
    ('Automation & Renewable Energy', 'Otomasi & Energi Terbarukan'),

    # Section headings (already handled but in case)
    ('"title":"Our Location"', '"title":"Lokasi Kami"'),
    ('"title":"Contact Us"', '"title":"Hubungi Kami"'),
    ('"title":"Products"', '"title":"Produk"'),
    ('"title":"Portfolio"', '"title":"Portfolio"'),
    ('"title":"Trusted By"', '"title":"Dipercaya Oleh"'),

    # Capabilities labels
    ('Industrial Projects', 'Proyek Industri'),
    ('In-House Products', 'Produk In-House'),
    ('Core Services', 'Layanan Inti'),
    ('Team Professionals', 'Profesional Tim'),
    ('>Capabilities<', '>Kapabilitas<'),

    # OUR 5 CORE SERVICES heading
    ('OUR 5 CORE SERVICES', '5 LAYANAN INTI KAMI'),

    # Service card descriptions — using actual characters
    ('End-to-end Industrial IoT \u2014 Modbus gateway, MQTT, edge computing, SCADA, sensor-to-cloud pipelines with IEC 62443 security for manufacturing, oil &amp; gas, and maritime operations.',
     'IoT Industri menyeluruh \u2014 gateway Modbus, MQTT, edge computing, SCADA, pipeline sensor-ke-cloud dengan keamanan IEC 62443 untuk manufaktur, oil &amp; gas, dan operasi maritim.'),
    ('Predictive maintenance, OEE dashboards, computer-vision QC, and real-time operational intelligence \u2014 turning raw machine data into actionable plant-floor decisions.',
     'Predictive maintenance, dashboard OEE, computer-vision QC, dan intelligence operasional real-time \u2014 mengubah data mesin menjadi keputusan plant-floor yang actionable.'),
    ('SURGE multi-tenant IoT platform \u2014 Energy Mapping (kWh, power factor), Water Analytic (KLHK SPARING compliance), Vessel Tracking (fleet + fuel monitoring).',
     'Platform IoT multi-tenant SURGE \u2014 Energy Mapping (kWh, power factor), Water Analytic (compliance SPARING KLHK), Vessel Tracking (armada + monitoring bahan bakar).'),
    ('PLC integration, SCADA modernization, Solar PV PLTS design, hybrid PLTS-PLTB systems, and smart street light (PJU) \u2014 turnkey industrial energy transition.',
     'Integrasi PLC, modernisasi SCADA, desain Solar PV PLTS, sistem hybrid PLTS-PLTB, dan smart street light (PJU) \u2014 transisi energi industri turnkey.'),
    ('Industry 4.0 roadmap, OT/IT convergence assessment, IIoT readiness audit, SCADA modernization, and cloud migration strategy for Indonesian manufacturers.',
     'Roadmap Industry 4.0, assessment konvergensi OT/IT, audit kesiapan IIoT, modernisasi SCADA, dan strategi migrasi cloud untuk manufaktur Indonesia.'),

    # Hero intro
    ('is a technology company specializing in <strong>Industrial IoT &amp; System Integration</strong>, headquartered in Batam, Riau Islands. Since January 2023, we have delivered',
     'adalah perusahaan teknologi yang berfokus pada <strong>IoT Industri &amp; Integrasi Sistem</strong>, berkantor pusat di Batam, Kepulauan Riau. Sejak Januari 2023, kami telah menyelesaikan'),

    # ENGLISH variant of hero intro (in case &amp; is actually &)
    ('is a technology company specializing in <strong>Industrial IoT & System Integration</strong>, headquartered in Batam, Riau Islands. Since January 2023, we have delivered',
     'adalah perusahaan teknologi yang berfokus pada <strong>IoT Industri & Integrasi Sistem</strong>, berkantor pusat di Batam, Kepulauan Riau. Sejak Januari 2023, kami telah menyelesaikan'),

    # Project tagline
    ('64+ industrial projects', '64+ proyek industri'),
    ('from Modbus gateways to complete IoT platforms across manufacturing, energy, logistics, and maritime sectors.',
     'dari gateway Modbus hingga platform IoT lengkap untuk sektor manufaktur, energi, logistik, dan maritim.'),

    # Trusted line
    ('With our commitment to the highest technical standards, SURIOTA is a trusted partner in improving efficiency, productivity, and business sustainability for clients across Indonesia.',
     'Dengan komitmen kami terhadap standar teknis tertinggi, SURIOTA adalah mitra terpercaya dalam meningkatkan efisiensi, produktivitas, dan keberlanjutan bisnis klien di seluruh Indonesia.'),

    # Form button
    ('"SEND"', '"KIRIM"'),
    ('"Send"', '"Kirim"'),
]

applied = 0
not_found = []
for en, idt in REPLACEMENTS_V2:
    if en in ed:
        ed = ed.replace(en, idt)
        applied += 1
    else:
        not_found.append(en[:60])

print(f'\nApplied {applied}/{len(REPLACEMENTS_V2)} v2 replacements')
if not_found:
    print(f'Still not found ({len(not_found)}):')
    for nf in not_found[:8]: print(f'  - {nf}')

# Push
payload = json.dumps({'meta': {'_elementor_data': ed}}).encode()
req = urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages/5273', data=payload, method='POST', headers=HDRS)
urllib.request.urlopen(req, timeout=60).read()
print('Pushed')

# Purge
purge = '''
$upload = wp_upload_dir();
$log = $upload['basedir'].'/purge-hp-v2.txt';
if (file_exists($log)) { if (function_exists('code_snippets')) { code_snippets()->deactivate(5); } return; }
if (class_exists('\\\\Elementor\\\\Plugin')) {
    $f = \\Elementor\\Core\\Files\\CSS\\Post::create(5273);
    if ($f) { $f->delete(); $f->update(); }
    \\Elementor\\Plugin::instance()->files_manager->clear_cache();
}
if (class_exists('WPO_Page_Cache')) WPO_Page_Cache::instance()->purge();
if (class_exists('WP_Optimize_Minify_Cache_Functions')) \\WP_Optimize_Minify_Cache_Functions::purge();
wp_cache_flush();
file_put_contents($log, 'done');
if (function_exists('code_snippets')) { code_snippets()->deactivate(5); }
'''
data = json.dumps({'code': purge, 'active': True, 'name': 'SX: hp v2'}).encode()
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=data, method='POST', headers=HDRS), timeout=60).read()
time.sleep(2)
urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/id/beranda/?cb={int(time.time())}', headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print('purged + triggered')
