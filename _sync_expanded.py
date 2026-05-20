"""Expanded translation dict — covers technical phrases from product/service pages."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from _sync_lib import sync_page

# Apply ONLY new entries — don't re-fetch from EN (would undo previous work)
# Instead, fetch CURRENT ID page, apply new dict, push back

import json, urllib.request, base64, time
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization': f'Basic {AUTH}', 'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

# EXPANDED DICT — 200+ entries for technical phrases
EXPANDED = {
    # ===== Service descriptions (water treatment, electrical, automation, etc.) =====
    'Our long-term partnership with PDAM Tirta Kepri proves SURIOTA\u2019s competence in managing city-scale water infrastructure': 'Kemitraan jangka panjang kami dengan PDAM Tirta Kepri membuktikan kompetensi SURIOTA dalam mengelola infrastruktur air skala kota',
    'from WTP, WWTP, to KLHK-integrated SPARING monitoring systems.': 'dari WTP, WWTP, hingga sistem monitoring SPARING terintegrasi KLHK.',
    'With integrated water quality sensors': 'Dengan sensor kualitas air terintegrasi',
    'we help you respond to water quality changes in real-time': 'kami membantu Anda merespons perubahan kualitas air secara real-time',

    # ===== Why Choose card titles =====
    'WHY CHOOSE SURIOTA': 'MENGAPA PILIH SURIOTA',
    'Why Choose SURIOTA': 'Mengapa Pilih SURIOTA',
    'Compliant water treatment with IoT monitoring': 'Water treatment yang patuh dengan monitoring IoT',
    'KLHK SPARING Compliance': 'Compliance SPARING KLHK',
    'PDAM-Trusted Delivery': 'Delivery Terpercaya PDAM',
    'SURGE Water Analytics': 'SURGE Water Analytics',
    'Full Treatment Spectrum': 'Spektrum Treatment Lengkap',
    'Lab & Calibration Services': 'Layanan Lab & Kalibrasi',
    'Operator Training & SOP': 'Training Operator & SOP',
    'SPARING-ready effluent monitoring per KLHK Permen LHK No. 80/2019. Continuous COD, BOD, TSS, pH, NH3-N reporting to government servers.': 'Monitoring effluent siap-SPARING sesuai KLHK Permen LHK No. 80/2019. Pelaporan COD, BOD, TSS, pH, NH3-N berkelanjutan ke server pemerintah.',
    'Active project partner of PDAM Tirta Kepri. Municipal-grade monitoring kualitas air across Kepulauan Riau.': 'Partner proyek aktif PDAM Tirta Kepri. Monitoring kualitas air kelas municipal di seluruh Kepulauan Riau.',
    'Real-time dashboards via SURGE Water Analytics \u2014 flowmeter, water quality, leak detection, NRW management.': 'Dashboard real-time via SURGE Water Analytics \u2014 flowmeter, kualitas air, deteksi kebocoran, manajemen NRW.',
    'WTP, WWTP, RO, UF, sea water desalination, sludge handling, chemical dosing \u2014 design & build for industrial & municipal capacities.': 'WTP, WWTP, RO, UF, desalinasi air laut, penanganan lumpur, chemical dosing \u2014 design & build untuk kapasitas industri & municipal.',
    'In-house sensor calibration traceable to national standards. Lab testing for raw water and effluent verification before SPARING data submission.': 'Kalibrasi sensor in-house dengan traceability ke standar nasional. Lab testing untuk verifikasi raw water dan effluent sebelum submission data SPARING.',
    'Comprehensive operator training, plant SOP documentation, and ongoing technical support. Reduce operational errors and downtime.': 'Training operator komprehensif, dokumentasi SOP plant, dan dukungan teknis berkelanjutan. Mengurangi kesalahan operasional dan downtime.',

    # ===== Service titles =====
    'Water Treatment Plant (WTP)': 'Water Treatment Plant (WTP)',
    'Waste Water Treatment (WWTP)': 'Waste Water Treatment (WWTP)',
    'Pumps & Mechanical': 'Pompa & Mekanikal',
    'Water Quality Monitoring': 'Monitoring Kualitas Air',
    'RO & UF Membrane Systems': 'Sistem Membran RO & UF',
    'Chemical Dosing & Sludge Handling': 'Chemical Dosing & Penanganan Sludge',
    'Design, installation, and maintenance of WTP systems producing high-quality clean water from various raw water sources.': 'Desain, instalasi, dan maintenance sistem WTP untuk menghasilkan air bersih berkualitas tinggi dari berbagai sumber raw water.',
    'Industrial wastewater treatment per environmental quality standards, including KLHK-integrated SPARING monitoring.': 'Treatment air limbah industri sesuai standar kualitas lingkungan, termasuk monitoring SPARING terintegrasi KLHK.',
    'Rewinding, repair, and procurement of centrifugal and submersible pumps for clean water and wastewater distribution systems.': 'Rewinding, repair, dan procurement pompa centrifugal dan submersible untuk sistem distribusi air bersih dan air limbah.',
    'Sensor implementation': 'Implementasi sensor',
    'Reverse Osmosis (RO) and Ultrafiltration (UF) systems for high-purity industrial water, sea water desalination, and process water.': 'Sistem Reverse Osmosis (RO) dan Ultrafiltration (UF) untuk air industri murni, desalinasi air laut, dan air proses.',
    'Automated chemical dosing pumps, coagulation/flocculation systems, sludge thickening, dewatering, and disposal compliance.': 'Pompa chemical dosing otomatis, sistem coagulation/flocculation, thickening sludge, dewatering, dan compliance pembuangan.',

    # ===== Process steps =====
    'Our Process': 'Proses Kami',
    'STEP': 'LANGKAH',
    'Water Quality Analysis': 'Analisis Kualitas Air',
    'Lab testing for treatment parameters': 'Lab testing untuk parameter treatment',
    'System Design': 'Desain Sistem',
    'Process units per quality and capacity': 'Unit proses sesuai kualitas dan kapasitas',
    'Fabrication & Installation': 'Fabrikasi & Instalasi',
    'Manufacturing and installing units': 'Manufaktur dan instalasi unit',
    'Commissioning': 'Commissioning',
    'Performance testing, calibration': 'Performance testing, kalibrasi',
    'Monitoring & Maintenance': 'Monitoring & Maintenance',
    'Continuous monitoring & periodic care': 'Monitoring berkelanjutan & perawatan berkala',

    # ===== Common phrases =====
    'with monitoring real-time dashboard via': 'dengan dashboard monitoring real-time via',
    'Design, installation, and maintenance': 'Desain, instalasi, dan maintenance',
    'maintenance of': 'maintenance dari',
    'maintenance and': 'maintenance dan',
    'Continuous monitoring': 'Monitoring berkelanjutan',
    'periodic care': 'perawatan berkala',

    # ===== FAQ patterns =====
    'What is the difference between WTP and WWTP?': 'Apa perbedaan antara WTP dan WWTP?',
    'WTP (Water Treatment Plant)': 'WTP (Water Treatment Plant)',
    'WWTP (Waste Water Treatment Plant)': 'WWTP (Waste Water Treatment Plant)',
    'How does SPARING monitoring work?': 'Bagaimana cara kerja monitoring SPARING?',
    'What sensors are required?': 'Sensor apa yang dibutuhkan?',
    'Do you handle commissioning?': 'Apakah Anda menangani commissioning?',
    'Yes': 'Ya',
    'No': 'Tidak',

    # ===== Electrical/Automation phrases =====
    'Industrial Electrical': 'Industrial Electrical',
    'Panel installation': 'Instalasi panel',
    'power distribution': 'distribusi daya',
    'commissioning': 'commissioning',
    'electrical testing': 'electrical testing',
    'wiring & commissioning': 'wiring & commissioning',
    'electrical engineering': 'electrical engineering',
    'PLC integration': 'Integrasi PLC',
    'SCADA modernization': 'modernisasi SCADA',
    'industrial automation': 'otomasi industri',
    'vendor-agnostic': 'vendor-agnostic',

    # ===== Renewable energy =====
    'Solar PV PLTS': 'Solar PV PLTS',
    'PLTS-PLTB hybrid': 'PLTS-PLTB hybrid',
    'hybrid systems': 'sistem hybrid',
    'smart street light': 'smart street light',
    'energy monitoring': 'monitoring energi',
    'feasibility study': 'studi kelayakan',
    'design & installation': 'desain & instalasi',

    # ===== IoT phrases =====
    'Industrial IoT': 'IoT Industri',
    'Modbus gateway': 'gateway Modbus',
    'edge computing': 'edge computing',
    'sensor-to-cloud pipelines': 'pipeline sensor-ke-cloud',
    'sensor pipeline to cloud': 'pipeline sensor ke cloud',
    'IEC 62443 security': 'keamanan IEC 62443',
    'maritime operations': 'operasi maritim',

    # ===== Product specs common =====
    'Specifications': 'Spesifikasi',
    'Datasheet': 'Datasheet',
    'Features': 'Fitur',
    'Key Features': 'Fitur Utama',
    'Applications': 'Aplikasi',
    'Power Supply': 'Power Supply',
    'Operating Temperature': 'Suhu Operasi',
    'Communication': 'Komunikasi',
    'Protocol': 'Protokol',
    'Connectivity': 'Konektivitas',
    'Made in Indonesia by SURIOTA': 'Buatan Indonesia oleh SURIOTA',
    'industrial-grade': 'industrial-grade',
    'plug-and-play': 'plug-and-play',
    'High accuracy': 'Akurasi tinggi',
    'Industrial enclosure': 'Casing industri',
    'real-time monitoring': 'monitoring real-time',

    # ===== Marketing copy patterns =====
    'is designed to': 'dirancang untuk',
    'provides': 'menyediakan',
    'enables': 'memungkinkan',
    'allows you to': 'memungkinkan Anda untuk',
    'helps you': 'membantu Anda',
    'reduces': 'mengurangi',
    'improves': 'meningkatkan',
    'optimizes': 'mengoptimalkan',
    'features': 'menampilkan',
    'includes': 'mencakup',
    'supports': 'mendukung',
    'compatible with': 'kompatibel dengan',
    'integrated with': 'terintegrasi dengan',
    'designed for': 'dirancang untuk',
    'suitable for': 'cocok untuk',
    'ideal for': 'ideal untuk',
    'perfect for': 'sempurna untuk',
    'used in': 'digunakan di',
    'deployed in': 'di-deploy di',
    'installed in': 'di-install di',

    # ===== Misc descriptions =====
    'high-quality': 'berkualitas tinggi',
    'high-purity': 'kemurnian tinggi',
    'cost-effective': 'cost-effective',
    'cost effective': 'cost effective',
    'reliable': 'andal',
    'rugged': 'rugged',
    'durable': 'tahan lama',
    'long-term': 'jangka panjang',
    'short-term': 'jangka pendek',
    'across Indonesia': 'di seluruh Indonesia',
    'in Batam': 'di Batam',
    'in Indonesia': 'di Indonesia',
    'for industries': 'untuk industri',
    'for businesses': 'untuk bisnis',
    'for clients': 'untuk klien',
    'for customers': 'untuk pelanggan',

    # ===== Section titles =====
    'Our Approach': 'Pendekatan Kami',
    'Our Team': 'Tim Kami',
    'Our Mission': 'Misi Kami',
    'Our Vision': 'Visi Kami',
    'Our Values': 'Nilai Kami',
    'Our History': 'Sejarah Kami',
    'Get in Touch': 'Hubungi Kami',
    'Talk to an Engineer': 'Bicara dengan Engineer',

    # ===== Eyebrows / labels =====
    'OVERVIEW': 'IKHTISAR',
    'INTRODUCTION': 'PENGANTAR',
    'SOLUTION': 'SOLUSI',
    'CASE STUDY': 'STUDI KASUS',
    'INDUSTRIES': 'INDUSTRI',
    'TECHNOLOGY': 'TEKNOLOGI',
    'PARTNERS': 'MITRA',
    'CLIENTS': 'KLIEN',

    # ===== Indonesian-targeted phrases (already partially Indonesian) =====
    'monitoring kualitas air': 'monitoring kualitas air',
    'Layanan Kami': 'Layanan Kami',
    'Pertanyaan Umum': 'Pertanyaan Umum',

    # ===== Time/scheduling =====
    'within 24 hours': 'dalam 24 jam',
    'within 1 business day': 'dalam 1 hari kerja',
    'business hours': 'jam kerja',
    'next-day delivery': 'pengiriman next-day',
    'same-day support': 'dukungan same-day',
}

PAGES = [
    (12, 5273, 'Homepage', 'https://suriota.com/id/beranda/'),
    (29, 5274, 'About', 'https://suriota.com/id/tentang-kami/'),
    (839, 5275, 'Portfolio', 'https://suriota.com/id/portfolio-id/'),
    (1127, 5276, 'Internship', 'https://suriota.com/id/magang-srt-team/'),
    (945, 5277, 'Water Treatment', 'https://suriota.com/id/water-treatment-id/'),
    (5039, 5278, 'SaaS', 'https://suriota.com/id/saas-id/'),
    (5260, 5279, 'Artikel', 'https://suriota.com/id/artikel-id/'),
    (37, 5281, 'Electrical', 'https://suriota.com/id/electrical-id/'),
    (35, 5282, 'Automation', 'https://suriota.com/id/automation-id/'),
    (39, 5283, 'RE', 'https://suriota.com/id/renewable-energy-id/'),
    (5029, 5284, 'IoT', 'https://suriota.com/id/internet-of-things-id/'),
    (5037, 5285, 'DA', 'https://suriota.com/id/data-analytics-id/'),
    (5033, 5286, 'DC', 'https://suriota.com/id/digital-consulting-id/'),
    (934, 5287, 'SRT-MGATE', 'https://suriota.com/id/suriota-modbus-gateway-id/'),
    (1542, 5288, 'SURGE-E', 'https://suriota.com/id/surge-energy-mapping-id/'),
    (1546, 5289, 'SURGE-V', 'https://suriota.com/id/surge-vessel-tracking-id/'),
    (1547, 5290, 'SURGE-W', 'https://suriota.com/id/surge-water-analytic-id/'),
    (1740, 5291, 'ISO-M485', 'https://suriota.com/id/iso-m485-series-id/'),
    (1741, 5292, 'THM-30MD', 'https://suriota.com/id/thm-30md-id/'),
    (1742, 5293, 'PM1611-WD', 'https://suriota.com/id/pm1611-wd-id/'),
    (1765, 5294, 'SPD-T485', 'https://suriota.com/id/rs-485-surge-protector-id/'),
    (929, 5295, 'WW Logger', 'https://suriota.com/id/waste-water-logger-id/'),
]

ok = 0
for en_id, id_id, label, url in PAGES:
    # Apply expanded dict to CURRENT ID page (not re-fetch from EN)
    r = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{id_id}?context=edit&_fields=meta', headers=HDRS)
    cur = json.loads(urllib.request.urlopen(r, timeout=60).read())
    ed = cur['meta']['_elementor_data']
    if not isinstance(ed, str): ed = json.dumps(ed)

    applied = 0
    for en, idt in EXPANDED.items():
        if en in ed:
            ed = ed.replace(en, idt)
            applied += 1

    if applied > 0:
        payload = json.dumps({'meta': {'_elementor_data': ed}}).encode()
        try:
            urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{id_id}', data=payload, method='POST', headers=HDRS), timeout=60).read()
            print(f'[{label}] applied {applied} expanded replacements')
            ok += 1
        except Exception as e:
            print(f'[{label}] push fail: {e}')
    else:
        print(f'[{label}] 0 new replacements')

# Global purge
print('\nFinal global purge...')
purge_php = '''
$upload = wp_upload_dir();
$log = $upload['basedir']."/purge-final-expanded.txt";
if (file_exists($log)) { if (function_exists('code_snippets')) { code_snippets()->deactivate(5); } return; }
if (class_exists('\\\\Elementor\\\\Plugin')) {
    foreach ([5273,5274,5275,5276,5277,5278,5279,5281,5282,5283,5284,5285,5286,5287,5288,5289,5290,5291,5292,5293,5294,5295] as $pid) {
        $f = \\Elementor\\Core\\Files\\CSS\\Post::create($pid);
        if ($f) { $f->delete(); $f->update(); }
    }
    \\Elementor\\Plugin::instance()->files_manager->clear_cache();
}
if (class_exists('WPO_Page_Cache')) WPO_Page_Cache::instance()->purge();
if (class_exists('WP_Optimize_Minify_Cache_Functions')) \\WP_Optimize_Minify_Cache_Functions::purge();
wp_cache_flush();
file_put_contents($log, 'done');
if (function_exists('code_snippets')) { code_snippets()->deactivate(5); }
'''
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=json.dumps({'code':purge_php, 'active':True, 'name':'SX: purge final all'}).encode(), method='POST', headers=HDRS), timeout=60).read()
time.sleep(3)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print(f'\n{ok}/22 pages got expansion updates')
