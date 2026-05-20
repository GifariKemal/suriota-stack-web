"""Mega dict expansion — final push for all 22 pages to 75%+ Bahasa."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization': f'Basic {AUTH}', 'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

MEGA = {
    # ===== Common label fixes =====
    'KEY FITUR': 'FITUR UTAMA',
    'KEY FEATURES': 'FITUR UTAMA',
    'YEARS EXPERIENCE': 'TAHUN PENGALAMAN',
    'PROJECTS': 'PROYEK',
    'STANDARDS': 'STANDAR',
    'Order on Tokopedia': 'Pesan di Tokopedia',
    'Request Quote': 'Minta Penawaran',
    'Request Free Demo': 'Minta Demo Gratis',
    'Try Live Demo': 'Coba Demo Live',
    'Schedule Demo': 'Jadwalkan Demo',
    'Wiring diagram': 'Skema wiring',
    'Bulk pricing available': 'Tersedia harga bulk',
    'Response within 24h': 'Respon dalam 24 jam',
    'Free initial consultation': 'Konsultasi awal gratis',

    # ===== Hero CTAs / engagement =====
    'Ready to start your': 'Siap memulai',
    'Ready to harden your': 'Siap memperkuat',
    'Ready to upgrade your': 'Siap upgrade',
    'Ready to scale your': 'Siap scale',
    'Ready to modernize your': 'Siap modernisasi',
    'project?': 'proyek?',
    'network?': 'jaringan Anda?',
    'system?': 'sistem Anda?',
    'Request a quote or technical sample. Our team responds': 'Minta penawaran atau sample teknis. Tim kami merespon',
    'Our team responds within 24 hours': 'Tim kami merespon dalam 24 jam',
    'with wiring diagram and isolation topology recommendations.': 'dengan skema wiring dan rekomendasi topologi isolasi.',
    'with compliance SPARING KLHK roadmap.': 'dengan roadmap compliance SPARING KLHK.',
    'with a feasibility check': 'dengan feasibility check',
    'aligned to IEC 62443 security and IIoT best practices.': 'sesuai dengan keamanan IEC 62443 dan IIoT best practices.',

    # ===== Service hero subtitles intro =====
    'Reliable and safe electrical systems are the foundation of every efficient business operation. Untreated electrical issues not only disrupt productivity but also threaten the safety of your assets and personnel.':
        'Sistem electrical yang andal dan aman adalah fondasi setiap operasi bisnis yang efisien. Masalah electrical yang tidak ditangani tidak hanya mengganggu produktivitas tetapi juga mengancam keselamatan aset dan personil Anda.',
    'experienced engineering team has handled various electrical installation and maintenance projects across': 'tim engineer berpengalaman telah menangani berbagai proyek instalasi dan maintenance electrical di sektor',
    'and surrounding regions.': 'dan wilayah sekitarnya.',
    'Using quality materials and following SNI, IEC, and PUIL standards, SURIOTA guarantees safe, efficient, and long-lasting workmanship.':
        'Menggunakan material berkualitas dan mengikuti standar SNI, IEC, dan PUIL, SURIOTA menjamin pekerjaan yang aman, efisien, dan tahan lama.',
    'Compliant, IoT-enabled electrical engineering': 'Electrical engineering compliant, IoT-enabled',
    'Compliance & Standards': 'Compliance & Standar',
    'All installation, panel building, and commissioning follow SNI, IEC, and PUIL 2011. Documented test reports and as-built drawings for every project.':
        'Seluruh instalasi, pembangunan panel, dan commissioning mengikuti SNI, IEC, dan PUIL 2011. Laporan test terdokumentasi dan as-built drawing untuk setiap proyek.',
    'Field-Proven Experience': 'Pengalaman Lapangan Terbukti',
    '64+ industrial projects delivered since 2023 across': '64+ proyek industri diselesaikan sejak 2023 di sektor',
    'and commercial sectors': 'dan komersial',
    'and beyond.': 'dan sekitarnya.',
    'IoT-Ready Integration': 'Integrasi IoT-Ready',
    'Power systems integrated with SURGE Energy for real-time consumption, demand, and fault monitoring.':
        'Sistem daya terintegrasi dengan SURGE Energy untuk monitoring konsumsi, demand, dan fault secara real-time.',
    'Local Engineering Support': 'Dukungan Engineering Lokal',
    'with rapid mobilization across Sumatera, Java, Kalimantan. Maintenance contracts available.':
        'dengan mobilisasi cepat di Sumatera, Jawa, Kalimantan. Kontrak maintenance tersedia.',
    'Safety-First Workflow': 'Alur Kerja Safety-First',
    'HSE-driven procedures with JSA, LOTO, and PTW documentation. Insurance-backed installations with zero LTI track record on industrial sites.':
        'Prosedur HSE-driven dengan dokumentasi JSA, LOTO, dan PTW. Instalasi dengan asuransi dan rekam jejak nol LTI di lokasi industri.',
    'Complete Handover Package': 'Paket Serah-Terima Lengkap',
    'Every project delivered with As-Built Drawings, Commissioning Reports, BAST, and recommended maintenance schedules. Audit-ready documentation.':
        'Setiap proyek diserahkan dengan As-Built Drawings, Laporan Commissioning, BAST, dan jadwal maintenance rekomendasi. Dokumentasi audit-ready.',

    # ===== Service items (Electrical, Automation, RE, WT all use similar) =====
    'Electrical Installation': 'Instalasi Electrical',
    'Commissioning & Testing': 'Commissioning & Testing',
    'Maintenance & Repair': 'Maintenance & Repair',
    'Design & Technical Calculation': 'Desain & Kalkulasi Teknis',
    'Switchgear & Panel Building': 'Switchgear & Panel Building',
    'Design and installation of': 'Desain dan instalasi',
    'systems, distribution panels, cables, and industrial wiring harnesses per SNI and IEC standards.':
        'sistem, panel distribusi, kabel, dan industrial wiring harness sesuai standar SNI dan IEC.',
    'Insulation resistance, continuity, ground resistance, and load testing to ensure safe installation before operation.':
        'Insulation resistance, continuity, ground resistance, dan load testing untuk memastikan instalasi aman sebelum operasi.',
    'Periodic maintenance, troubleshooting, motor rewinding, and component replacement to maintain electrical system reliability.':
        'Maintenance berkala, troubleshooting, rewinding motor, dan penggantian komponen untuk menjaga keandalan sistem electrical.',
    'Load calculation, power factor analysis, SLD design, and engineering drawings for optimal electrical system planning.':
        'Kalkulasi beban, analisis power factor, desain SLD, dan engineering drawings untuk perencanaan sistem electrical optimal.',
    'Custom LV/MV switchgear, MCC panels, ATS, and distribution boards built to IEC 61439 standards.':
        'Switchgear LV/MV custom, panel MCC, ATS, dan distribution board sesuai standar IEC 61439.',

    # ===== Generic "Why X" patterns =====
    'Why engineers choose': 'Mengapa engineer memilih',
    'Why PDAM & industries trust': 'Mengapa PDAM & industri mempercayai',
    'Why operators choose': 'Mengapa operator memilih',
    'Why we lead in': 'Mengapa kami unggul di',

    # ===== Product ISO-M485 =====
    'and secure data communication, you can\u2019t afford downtime or interference.': 'dan komunikasi data yang aman, Anda tidak boleh ada downtime atau interferensi.',
    'The ISO-M485 Series is engineered for industrial-grade RS-485 connections with built-in galvanic isolation and robust surge protection, ensuring maximum reliability in the most demanding environments.':
        'ISO-M485 Series dirancang untuk koneksi RS-485 industrial-grade dengan galvanic isolation built-in dan proteksi surge yang kokoh, memastikan reliability maksimal di lingkungan paling demanding.',
    'Boost Your Komunikasi. Protect Your Investment.': 'Tingkatkan Komunikasi Anda. Lindungi Investasi Anda.',
    'With the ISO-M485 Series, you get speed, stability, and protection all in one compact, andal device.':
        'Dengan ISO-M485 Series, Anda mendapatkan kecepatan, stabilitas, dan proteksi dalam satu device kompak dan andal.',
    '2.5kV Optical Isolation': '2.5kV Optical Isolation',
    'Optocoupler isolation between RS-485 ports protects upstream PLC/SCADA from ground loops and field-side faults.':
        'Isolasi optocoupler antar port RS-485 melindungi PLC/SCADA upstream dari ground loop dan fault field-side.',
    'Built-in Surge Protection': 'Proteksi Surge Built-in',
    'Integrated TVS diodes + gas discharge tubes guard against lightning-induced and switching transients on outdoor cables.':
        'TVS diode + gas discharge tube terintegrasi melindungi dari transient akibat petir dan switching di kabel outdoor.',
    '256 Devices Per Bus': '256 Device Per Bus',
    'Extended driver capacity supports up to 256 nodes per segment. Auto direction control simplifies wiring.':
        'Kapasitas driver yang diperpanjang mendukung hingga 256 node per segmen. Kontrol arah otomatis menyederhanakan wiring.',
    'Industrial Temp Range': 'Rentang Suhu Industri',
    '-40\u00b0C to +85\u00b0C operation. DIN rail mountable. Rated for continuous operation in harsh field cabinets.':
        'Operasi -40\u00b0C hingga +85\u00b0C. DIN rail mountable. Rated untuk operasi berkelanjutan di field cabinet keras.',
    'Flexible Wide Power Input': 'Input Daya Lebar Fleksibel',
    'Accepts 7-15VDC or 9-24VDC supply variants for easy integration with industrial 12V or 24V control panels.':
        'Menerima supply 7-15VDC atau 9-24VDC untuk integrasi mudah dengan panel kontrol industri 12V atau 24V.',
    'High-Speed Data Rate': 'Data Rate Kecepatan Tinggi',
    'Supports up to 500 kbps data rate (within distance limits) for high-throughput SCADA and PLC networks.':
        'Mendukung data rate hingga 500 kbps (dalam batas jarak) untuk jaringan SCADA dan PLC high-throughput.',
    'What isolation voltage does ISO-M485 provide?': 'Tegangan isolasi apa yang disediakan ISO-M485?',
    'How many devices per RS-485 bus?': 'Berapa banyak device per bus RS-485?',
    'What is the operating temperature range?': 'Berapa rentang suhu operasi?',
    'Does it include built-in surge protection?': 'Apakah termasuk proteksi surge built-in?',

    # ===== SURGE-W =====
    'Are You Facing Challenges in Water Quality Management?': 'Apakah Anda Menghadapi Tantangan dalam Manajemen Kualitas Air?',
    'Managing water quality, whether for consumption or wastewater discharge, requires rigorous monitoring and regulatory adherence. Without an integrated system, you may be facing:':
        'Mengelola kualitas air, baik untuk konsumsi maupun pembuangan limbah, memerlukan monitoring ketat dan kepatuhan regulasi. Tanpa sistem terintegrasi, Anda mungkin menghadapi:',
    'Difficulty ensuring compliance with quality standards set by the government (like KLHK) and international bodies.':
        'Kesulitan memastikan compliance dengan standar kualitas yang ditetapkan pemerintah (seperti KLHK) dan badan internasional.',
    'The risk of environmental pollution due to delayed detection of water quality anomalies.':
        'Risiko polusi lingkungan akibat keterlambatan deteksi anomali kualitas air.',
    'Operational inefficiencies at water and wastewater treatment plants (WTP, WWTP).':
        'Inefisiensi operasional di water dan wastewater treatment plant (WTP, WWTP).',
    'A lack of accurate, structured historical data for analysis and strategic decision-making.':
        'Kurangnya data historis yang akurat dan terstruktur untuk analisis dan pengambilan keputusan strategis.',
    'Introducing SURGE-Water Analytic: The Smart Water Management Solution':
        'Memperkenalkan SURGE-Water Analytic: Solusi Smart Water Management',
    'SURGE-Water Analytic is an advanced solution from Suriota, specifically designed to address the challenges of water quality management. This platform empowers Wastewater Treatment Plants (WWTPs), Sewage Treatment Plants (STPs), Water Treatment Plants (WTPs), and Regional Utilitas Air (PDAMs) to perform continuous monitoring, in-depth analysis, and proactive control over water quality parameters.':
        'SURGE-Water Analytic adalah solusi canggih dari Suriota, khusus dirancang untuk menjawab tantangan manajemen kualitas air. Platform ini memberdayakan Wastewater Treatment Plant (WWTP), Sewage Treatment Plant (STP), Water Treatment Plant (WTP), dan Perusahaan Daerah Air Minum (PDAM) untuk melakukan monitoring berkelanjutan, analisis mendalam, dan kontrol proaktif atas parameter kualitas air.',
    'Real-Time Water Parameters': 'Parameter Air Real-Time',
    'of pH, COD, BOD, TSS, Ammonia, Turbidity, Flow. Early anomaly detection for preventive action.':
        'pH, COD, BOD, TSS, Ammonia, Turbidity, Flow. Deteksi anomali awal untuk aksi preventif.',
    'Direct integration to KLHK SPARING servers per Permen LHK No. 80/2019. Automated regulatory reporting.':
        'Integrasi langsung ke server SPARING KLHK sesuai Permen LHK No. 80/2019. Pelaporan regulasi otomatis.',
    'Multi-Site Map Dashboard': 'Dashboard Peta Multi-Site',
    'Visualize all monitoring points on interactive map. Color-coded compliance status across WTPs, WWTPs, and intake points.':
        'Visualisasi semua titik monitoring di peta interaktif. Status compliance kode warna untuk WTP, WWTP, dan intake point.',
    'Multi-Brand Sensor Compatible': 'Kompatibel Sensor Multi-Brand',
    'Integrates with Hach, Endress+Hauser, Yokogawa, Krohne, and other major sensor brands via Modbus / 4-20mA / RS-485.':
        'Terintegrasi dengan Hach, Endress+Hauser, Yokogawa, Krohne, dan brand sensor utama lainnya via Modbus / 4-20mA / RS-485.',
    'Predictive Anomaly Detection': 'Deteksi Anomali Prediktif',
    'ML-based threshold learning detects parameter drift before exceedance. Get warned of trending non-compliance days ahead.':
        'Threshold learning berbasis ML mendeteksi drift parameter sebelum exceedance. Dapatkan peringatan tren non-compliance hari ke depan.',
    'Mobile Dashboard & Push Alerts': 'Dashboard Mobile & Push Alert',
    'WhatsApp, SMS, push notification alerts on parameter exceedance. Field operators check live status from any phone.':
        'Alert WhatsApp, SMS, push notification saat exceedance parameter. Operator lapangan cek status live dari telepon manapun.',
    'Is SURGE Water Analytic KLHK SPARING compliant?': 'Apakah SURGE Water Analytic compliant SPARING KLHK?',
    'What water quality parameters can be monitored?': 'Parameter kualitas air apa yang bisa dimonitor?',
    'Does it support multiple sensor brands?': 'Apakah mendukung multi-brand sensor?',
    'Can monitoring data be exported for audit?': 'Apakah data monitoring bisa di-export untuk audit?',
    'Request a free demo with sample sensor data from a real WWTP.': 'Minta demo gratis dengan data sensor sample dari WWTP nyata.',
    'KLHK compliance plan': 'Rencana compliance KLHK',
    'PDAM-trusted': 'Dipercaya PDAM',

    # ===== Common workflow / process patterns =====
    'Step 01': 'Langkah 01',
    'Step 02': 'Langkah 02',
    'Step 03': 'Langkah 03',
    'Step 04': 'Langkah 04',
    'Step 05': 'Langkah 05',
    'Step 06': 'Langkah 06',

    # ===== Time/contact =====
    'within 24 hours': 'dalam 24 jam',
    'within 1 business day': 'dalam 1 hari kerja',
    'free initial consultation': 'konsultasi awal gratis',
    'preliminary feasibility study': 'studi kelayakan awal',

    # ===== Misc product common =====
    'Spec Sheet': 'Lembar Spek',
    'Datasheet': 'Datasheet',
    'Quick Buy': 'Beli Cepat',
    'Add to Cart': 'Tambah ke Keranjang',
    'Available Now': 'Tersedia Sekarang',
    'In Stock': 'Tersedia',
    'Out of Stock': 'Stok Habis',

    # ===== Section eyebrows =====
    'OUR PROCESS': 'PROSES KAMI',
    'PROCESS': 'PROSES',
    'WORKFLOW': 'ALUR KERJA',
    'APPROACH': 'PENDEKATAN',
    'PARTNERSHIPS': 'KEMITRAAN',
    'TESTIMONIALS': 'TESTIMONI',

    # ===== Header navigation menu items =====
    'Internet of Things': 'Internet of Things',  # keep technical
    'System Integration': 'Integrasi Sistem',
    'Artificial Intelligence': 'Artificial Intelligence',
    'Modbus Gateway IIoT': 'Modbus Gateway IIoT',
    'Waste Water Logger': 'Waste Water Logger',
    'STAY UPDATED': 'TETAP UPDATE',
    'CONNECT WITH US': 'HUBUNGI KAMI',
    'NEXT GEN. INDUSTRIAL PARTNER': 'MITRA INDUSTRI GENERASI BARU',
    'Privacy Policy': 'Kebijakan Privasi',
    'Terms of Service': 'Syarat Layanan',
    'All rights reserved': 'Semua hak dilindungi',

    # ===== Generic statement patterns =====
    'Optimize your business with': 'Optimasi bisnis Anda dengan',
    'industrial electrical systems from SURIOTA': 'sistem industrial electrical dari SURIOTA',
    'Boost efficiency and productivity with': 'Tingkatkan efisiensi dan produktivitas dengan',
    'SURIOTA automation solutions': 'solusi otomasi SURIOTA',
    'Pure water treatment solutions for a sustainable future with SURIOTA':
        'Solusi water treatment murni untuk masa depan berkelanjutan dengan SURIOTA',
    'Toward a greener future with': 'Menuju masa depan yang lebih hijau dengan',
    'SURIOTA renewable energy solutions': 'solusi renewable energy SURIOTA',
}

PAGES = [
    (12, 5273, 'Homepage'), (29, 5274, 'About'),
    (839, 5275, 'Portfolio'), (1127, 5276, 'Internship'),
    (945, 5277, 'WT'), (5039, 5278, 'SaaS'),
    (5260, 5279, 'Artikel'), (37, 5281, 'Electrical'),
    (35, 5282, 'Automation'), (39, 5283, 'RE'),
    (5029, 5284, 'IoT'), (5037, 5285, 'DA'),
    (5033, 5286, 'DC'), (934, 5287, 'MGATE'),
    (1542, 5288, 'SURGE-E'), (1546, 5289, 'SURGE-V'),
    (1547, 5290, 'SURGE-W'), (1740, 5291, 'ISO-M485'),
    (1741, 5292, 'THM-30MD'), (1742, 5293, 'PM1611'),
    (1765, 5294, 'SPD-T485'), (929, 5295, 'WW Logger'),
]

total_replacements = 0
for en_id, id_id, label in PAGES:
    r = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{id_id}?context=edit&_fields=meta', headers=HDRS)
    cur = json.loads(urllib.request.urlopen(r, timeout=60).read())
    ed = cur['meta']['_elementor_data']
    if not isinstance(ed, str): ed = json.dumps(ed)
    applied = 0
    for en, idt in MEGA.items():
        if en in ed:
            ed = ed.replace(en, idt)
            applied += 1
    if applied > 0:
        urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{id_id}', data=json.dumps({'meta': {'_elementor_data': ed}}).encode(), method='POST', headers=HDRS), timeout=60).read()
        print(f'  {label}: +{applied} replacements')
        total_replacements += applied
    else:
        print(f'  {label}: 0')

print(f'\nTotal: {total_replacements} new replacements applied')

# Final purge
purge = '''
$upload = wp_upload_dir();
$log = $upload['basedir']."/purge-mega.txt";
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
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=json.dumps({'code':purge, 'active':True, 'name':'SX: purge mega'}).encode(), method='POST', headers=HDRS), timeout=60).read()
time.sleep(3)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print('Purged + triggered')
