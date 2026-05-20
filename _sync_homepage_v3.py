"""Sync Homepage v3 — RE-FETCH from EN, apply complete translation in single pass."""
import json, urllib.request, urllib.error, base64, sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization': f'Basic {AUTH}', 'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

# Fresh fetch from EN
r = urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages/12?context=edit&_fields=meta', headers=HDRS)
en = json.loads(urllib.request.urlopen(r, timeout=60).read())
ed = en['meta']['_elementor_data']
if not isinstance(ed, str): ed = json.dumps(ed)
print(f'Fresh EN size: {len(ed)}')

# COMPLETE replacement list — use actual escaped forms as they appear in JSON
R = [
    # Hero
    ('Next Gen. Industrial Partner', 'Mitra Industri Generasi Baru'),
    ('SURIOTA</strong> is a technology company specializing in <strong>Industrial IoT &amp; System Integration</strong>, headquartered in Batam, Riau Islands. Since January 2023, we have delivered <strong>64+ industrial projects</strong>',
     'SURIOTA</strong> adalah perusahaan teknologi yang berfokus pada <strong>IoT Industri &amp; Integrasi Sistem</strong>, berkantor pusat di Batam, Kepulauan Riau. Sejak Januari 2023, kami telah menyelesaikan <strong>64+ proyek industri</strong>'),
    ('from Modbus gateways to complete IoT platforms across manufacturing, energy, logistics, and maritime sectors.',
     'dari gateway Modbus hingga platform IoT lengkap untuk sektor manufaktur, energi, logistik, dan maritim.'),

    # 5 Services
    ('>OUR 5 CORE SERVICES<', '>5 LAYANAN INTI KAMI<'),
    ('>OUR 5 LAYANAN INTI<', '>5 LAYANAN INTI KAMI<'),  # cleanup partial

    # Service card titles
    ('>IoT &amp; System Integration<', '>IoT &amp; Integrasi Sistem<'),
    ('>AI &amp; Data Analytics<', '>AI &amp; Analitik Data<'),
    ('>Software as a Service<', '>Software sebagai Layanan<'),
    ('>Automation &amp; Renewable Energy<', '>Otomasi &amp; Energi Terbarukan<'),
    ('>Digital Consulting<', '>Digital Consulting<'),

    # Service descriptions
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

    # Aria labels (escaped)
    ('aria-label=\\"IoT &amp; System Integration\\"', 'aria-label=\\"IoT &amp; Integrasi Sistem\\"'),
    ('aria-label=\\"AI &amp; Data Analytics\\"', 'aria-label=\\"AI &amp; Analitik Data\\"'),
    ('aria-label=\\"SaaS SURGE Platform\\"', 'aria-label=\\"Platform SaaS SURGE\\"'),
    ('aria-label=\\"Automation &amp; Renewable Energy\\"', 'aria-label=\\"Otomasi &amp; Energi Terbarukan\\"'),

    # Trust statement
    ('With our commitment to the highest technical standards, SURIOTA is a trusted partner in improving efficiency, productivity, and business sustainability for clients across Indonesia.',
     'Dengan komitmen kami terhadap standar teknis tertinggi, SURIOTA adalah mitra terpercaya dalam meningkatkan efisiensi, produktivitas, dan keberlanjutan bisnis klien di seluruh Indonesia.'),

    # Buttons
    ('"text":"Free Consultation"', '"text":"Konsultasi Gratis"'),
    ('"text":"View All Portfolio"', '"text":"Lihat Semua Portfolio"'),

    # Section headings (heading widget titles in JSON)
    ('"title":"Products"', '"title":"Produk"'),
    ('"title":"Trusted By"', '"title":"Dipercaya Oleh"'),
    ('"title":"Portfolio"', '"title":"Portfolio"'),
    ('"title":"Our Location"', '"title":"Lokasi Kami"'),
    ('"title":"Contact Us"', '"title":"Hubungi Kami"'),

    # Capabilities section
    ('>Capabilities<', '>Kapabilitas<'),
    ('Industrial Projects', 'Proyek Industri'),
    ('In-House Products', 'Produk In-House'),
    ('Core Services', 'Layanan Inti'),
    ('Team Professionals', 'Profesional Tim'),

    # Form fields
    ('"text":"SEND"', '"text":"KIRIM"'),
    ('"button_text":"SEND"', '"button_text":"KIRIM"'),

    # Form labels (common fields)
    ('"field_label":"Name"', '"field_label":"Nama"'),
    ('"field_label":"Email"', '"field_label":"Email"'),
    ('"field_label":"Message"', '"field_label":"Pesan"'),
    ('"placeholder":"Name"', '"placeholder":"Nama"'),
    ('"placeholder":"Email"', '"placeholder":"Email"'),
    ('"placeholder":"Message"', '"placeholder":"Pesan"'),
]

applied = 0
for en_str, id_str in R:
    if en_str in ed:
        ed = ed.replace(en_str, id_str)
        applied += 1
print(f'Applied {applied}/{len(R)}')

# Push REPLACING current ID page content
payload = json.dumps({'meta': {'_elementor_data': ed}}).encode()
req = urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages/5273', data=payload, method='POST', headers=HDRS)
urllib.request.urlopen(req, timeout=60).read()
print('Pushed to ID 5273')

# Purge
purge = '''
$upload = wp_upload_dir();
$log = $upload['basedir'].'/purge-hp-v3.txt';
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
data = json.dumps({'code': purge, 'active': True, 'name': 'SX: hp v3'}).encode()
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=data, method='POST', headers=HDRS), timeout=60).read()
time.sleep(3)
urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/id/beranda/?cb={int(time.time())}', headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print('purged + triggered')
