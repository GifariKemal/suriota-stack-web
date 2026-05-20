"""V4 — final per-page deep translation for 9 LOW pages."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization': f'Basic {AUTH}', 'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

V4 = {
    # ===== Internship specifics =====
    'MAGANG PROGRAM BATCH 3 \u00b7 TIDAKW OPEN': 'MAGANG PROGRAM BATCH 3 \u00b7 SEKARANG OPEN',
    'NOW OPEN': 'SEKARANG OPEN',
    'TIDAKW OPEN': 'SEKARANG OPEN',
    'Build Your Tech Career with SURIOTA': 'Bangun Karier Teknologi Anda Bersama SURIOTA',
    'Learn directly from real IoT Industri, automation, and renewable energi projects with the SURIOTA engineering team di Batam.':
        'Belajar langsung dari proyek nyata IoT Industri, otomasi, dan renewable energi bersama tim engineer SURIOTA di Batam.',
    'Apply Tidakw': 'Lamar Sekarang',
    'Apply Now': 'Lamar Sekarang',
    '3\u20136 MONTHS': '3\u20136 BULAN',
    'HYBRID \u00b7 BATAM': 'HYBRID \u00b7 BATAM',
    '4 OPEN POSITIONS': '4 POSISI TERSEDIA',
    'OPEN POSITIONS': 'POSISI TERSEDIA',
    'Where You\u2019ll Make an Impact': 'Tempat Anda Memberikan Dampak',
    'R&D App Developer': 'R&D App Developer',
    'Next.js, React & SURplatform SURGE development.': 'Pengembangan Next.js, React & platform SURGE.',
    'DevOps Engineer': 'DevOps Engineer',
    'Caprover, VPS infrastructure & CI/CD pipelines.': 'Caprover, infrastruktur VPS & pipeline CI/CD.',
    'QA Specialist': 'QA Specialist',
    'Manual & automated testing for SURplatform SURGE.': 'Testing manual & otomatis untuk platform SURGE.',
    'UI/UX Designer': 'UI/UX Designer',
    'Figma, design systems & user research.': 'Figma, design system & user research.',
    'Why Intern at SURIOTA?': 'Mengapa Magang di SURIOTA?',
    'Hands-on internship for real-world experience in IoT Industri, automation, and renewable energi projects. Work alongside senior engineers, ship real products, and build a portfolio that opens doors.':
        'Magang langsung untuk pengalaman dunia nyata dalam proyek IoT Industri, otomasi, dan renewable energi. Bekerja bersama senior engineer, ship produk nyata, dan bangun portfolio yang membuka peluang.',
    'Qualifications & Required Documents': 'Kualifikasi & Dokumen yang Diperlukan',
    'Benefits & Perks': 'Benefit & Perks',
    'Ready to Start Your Tech Career?': 'Siap Memulai Karier Teknologi Anda?',
    'Kirim your CV & documents to': 'Kirim CV & dokumen Anda ke',
    'with subject:': 'dengan subjek:',
    '[Nama Anda] \u2014 Magang Batch 3': '[Nama Anda] \u2014 Magang Batch 3',
    'Apply via Email': 'Lamar via Email',
    'ALSO SEE:': 'LIHAT JUGA:',
    'TENTANG SURIOTA \u2022 PORTFOLIO \u2022 MODBUS GATEWAY \u2022 SURGE ENERGY':
        'TENTANG SURIOTA \u2022 PORTFOLIO \u2022 MODBUS GATEWAY \u2022 SURGE ENERGY',

    # ===== Renewable Energy =====
    'INDUSTRIES WE POWER': 'INDUSTRI YANG KAMI DAYAI',
    'Solar PV & hybrid renewable energi di seluruh Indonesia': 'Solar PV & hybrid renewable energi di seluruh Indonesia',
    'Menuju masa depan yang lebih hijau dengan SURIOTA renewable energi solutions': 'Menuju masa depan yang lebih hijau dengan solusi renewable energi SURIOTA',
    'ON/OFF-GRID HYBRID': 'ON/OFF-GRID HYBRID',
    'IOT HYBRID': 'IOT HYBRID',
    'FEASIBILITY STUDY': 'STUDI KELAYAKAN',
    'Renewable energi is the future \u2014 and the future starts now. SURIOTA delivers integrated renewable energi solutions untuk industri, public facilities, and communities di seluruh Indonesia.':
        'Renewable energi adalah masa depan \u2014 dan masa depan dimulai sekarang. SURIOTA menyediakan solusi renewable energi terintegrasi untuk industri, fasilitas publik, dan komunitas di seluruh Indonesia.',
    'SURIOTA has experience designing PLTS (solar) and PLTB (wind) systems standalone or hybrid. Our PLTS-PLTB sistem hybrid are ideal untuk off-grid applications like IoT-based street lighting (PJU).':
        'SURIOTA memiliki pengalaman merancang sistem PLTS (solar) dan PLTB (wind) standalone atau hybrid. Sistem hybrid PLTS-PLTB kami ideal untuk aplikasi off-grid seperti street lighting (PJU) berbasis IoT.',
    'Every project begins with a comprehensive studi kelayakan: irradiation analysis, load calculation, ROI projection, and optimal system planning \u2014 minimizing investment risk.':
        'Setiap proyek dimulai dengan studi kelayakan komprehensif: analisis irradiasi, kalkulasi beban, proyeksi ROI, dan perencanaan sistem optimal \u2014 meminimalkan risiko investasi.',
    'Hybrid renewable energi with IoT performance tracking': 'Hybrid renewable energi dengan tracking performa IoT',
    'Feasibility-First Approach': 'Pendekatan Feasibility-First',
    'Solar irradiance study, load profile analysis, financial modeling (IRR, payback) \u2014 before a single panel is quoted. Right-sized systems, not oversized invoices.':
        'Studi irradiance solar, analisis load profile, financial modeling (IRR, payback) \u2014 sebelum satu panel pun di-quote. Sistem ukuran tepat, bukan invoice over-sized.',
    'Hybrid PLTS + PLTB Systems': 'Sistem Hybrid PLTS + PLTB',
    'Combined solar & wind generation with battery storage \u2014 proven on Hybrid PJU PLTS + PLTB deployments.':
        'Kombinasi generasi solar & wind dengan storage baterai \u2014 terbukti pada deployment Hybrid PJU PLTS + PLTB.',
    'IoT Energy Monitoring': 'Monitoring Energi IoT',
    'Per-string PV monitoring, inverter telemetry, battery SOC tracking via SURGE Energy Mapping \u2014 catch underperformance early.':
        'Monitoring PV per-string, telemetri inverter, tracking SOC baterai via SURGE Energy Mapping \u2014 deteksi underperformance lebih awal.',
    'On-Grid & Off-Grid': 'On-Grid & Off-Grid',
    'PLN net-metering compliant on-grid, plus off-grid systems for remote sites, vessels, mining camps, and street lighting projects.':
        'On-grid compliant PLN net-metering, plus sistem off-grid untuk lokasi remote, kapal, mining camp, dan proyek street lighting.',
    'PLN Permit Assistance': 'Bantuan Permit PLN',
    'End-to-end PLN net-metering registration, SLO certification, AEROSOL permit processing. We handle paperwork while you focus on operations.':
        'Registrasi PLN net-metering end-to-end, sertifikasi SLO, processing permit AEROSOL. Kami handle paperwork sementara Anda fokus operasi.',
    'Proven ROI Track Record': 'Track Record ROI Terbukti',
    '5-8 year payback on industrial PLTS deployments': '5-8 tahun payback pada deployment PLTS industri',

    # ===== SaaS =====
    'D/TSS/NH3) & vessel tracking. 70% cheaper than ThingsBoard, made di Indonesia.':
        'D/TSS/NH3) & vessel tracking. 70% lebih murah dari ThingsBoard, buatan Indonesia.',
    'Energy Companies': 'Perusahaan Energi',
    'Utilitas Air (PDAM)': 'Utilitas Air (PDAM)',
    'Maritim & Logistics': 'Maritim & Logistik',
    'Smart Building': 'Smart Building',
    'Mining': 'Pertambangan',
    'Public Sector': 'Sektor Publik',
    'SURGE \u2014 one platform, three industrial verticals': 'SURGE \u2014 satu platform, tiga vertical industri',
    'SLA UPTIME': 'SLA UPTIME',
    'ARSITEKTUR': 'ARSITEKTUR',
    'HOSTED': 'HOSTED',
    'SURGE is SURIOTA\u2019s multi-tenant SaaS platform \u2014 built for asset-heavy industries that need monitoring real-time, regulatory reporting, and operational insight without standing up their own infrastructure.':
        'SURGE adalah platform SaaS multi-tenant SURIOTA \u2014 dibangun untuk industri asset-heavy yang membutuhkan monitoring real-time, regulatory reporting, dan operational insight tanpa harus membangun infrastruktur sendiri.',
    'Three flagship modules ship today: SURGE-Energy Mapping, SURGE-Vessel Tracking, SURGE-Water Analytics. Need something different? We build custom SaaS on the same proven platform.':
        'Tiga modul unggulan tersedia hari ini: SURGE-Energy Mapping, SURGE-Vessel Tracking, SURGE-Water Analytics. Butuh yang berbeda? Kami build custom SaaS di platform yang sama dan terbukti.',
    'REST & Gra': 'REST & Gra',

    # ===== MGATE =====
    'Daya & Energi': 'Daya & Energi',
    'Fabrication': 'Fabrikasi',
    'Agriculture': 'Agrikultur',
    'Elevate Your Industrial Konektivitas with Suriota Modbus Gateway IIoT': 'Tingkatkan Konektivitas Industri Anda dengan Suriota Modbus Gateway IIoT',
    'Seamless Integration Between Otomasi Systems and Modern IoT Ecosystems': 'Integrasi Seamless Antara Sistem Otomasi dan Ekosistem IoT Modern',
    'The Suriota Modbus Gateway IIoT is an industrial-standard gateway solution designed to efficiently bridge Modbus-based automation systems with Internet of Things (IoT) ecosystems. This device converts data from industrial assets such as sensors, PLCs, or machinery into modern IoT protocols like MQTT and HTTP. With support for Modbus RTU (RS-485) and Modbus TCP/IP (Wi-Fi/Ethernet), the gateway ensures compatibility between existing industrial infrastructure and IoT cloud platforms (AWS, Azure, etc.) as well as on-premises servers.':
        'Suriota Modbus Gateway IIoT adalah solusi gateway standar industri yang dirancang untuk menghubungkan sistem otomasi berbasis Modbus dengan ekosistem Internet of Things (IoT). Device ini mengonversi data dari aset industri seperti sensor, PLC, atau mesin ke protokol IoT modern seperti MQTT dan HTTP. Dengan dukungan Modbus RTU (RS-485) dan Modbus TCP/IP (Wi-Fi/Ethernet), gateway memastikan kompatibilitas antara infrastruktur industri existing dan platform cloud IoT (AWS, Azure, dll) serta server on-premise.',
    'Key Spesifikasi': 'Spesifikasi Utama',
    'CPU: ESPRESSIF dual-core': 'CPU: ESPRESSIF dual-core',
    'Wireless Konektivitas: WiFi 2.4 GHz': 'Konektivitas Wireless: WiFi 2.4 GHz',
    'Ports: 2\u00d7 Isolated RS-485 (up to 32 devices per port), 1\u00d7 RJ45 Ethernet 10/100 Mbps':
        'Port: 2\u00d7 Isolated RS-485 (hingga 32 device per port), 1\u00d7 RJ45 Ethernet 10/100 Mbps',
    'Power: Dual DC 12-48VDC inputs for redundancy, PoE (IEEE 802.3af/at) option on specific versions':
        'Power: Input dual DC 12-48VDC untuk redundancy, opsi PoE (IEEE 802.3af/at) di versi spesifik',
    'Komunikasi Protokols: MQTT (ISO/IEC 20922), HTTP/HTTPS, REST API':
        'Protokol Komunikasi: MQTT (ISO/IEC 20922), HTTP/HTTPS, REST API',
    'Multi-Protokol Bridge': 'Bridge Multi-Protokol',
    'Converts Modbus RTU (RS-485) \u2194 Modbus TCP/IP \u2194 MQTT \u2194 HTTP/REST. Tidak-code register mapping, output JSON/topic custom.':
        'Konversi Modbus RTU (RS-485) \u2194 Modbus TCP/IP \u2194 MQTT \u2194 HTTP/REST. Register mapping no-code, output JSON/topic custom.',

    # ===== SURGE-W extra =====
    'and operational efficiency.': 'dan efisiensi operasional.',

    # ===== SURGE-V extra =====
    'operations into an integrated digital ecosystem': 'operasi menjadi ekosistem digital terintegrasi',

    # ===== THM-30MD =====
    'industrial-grade sensor with': 'sensor industrial-grade dengan',

    # ===== PM1611 =====
    'Prepaid Token System': 'Sistem Token Prabayar',
    'Multi-tenant electricity billing with auto-disconnect at zero balance and token-based reload via cashier portal. Per-tenant consumption tracking.':
        'Billing listrik multi-tenant dengan auto-disconnect pada saldo nol dan reload berbasis token via portal kasir. Tracking konsumsi per-tenant.',

    # ===== Common labels that recur =====
    'Real-time': 'Real-time',
    'Real time': 'Real time',
    'Hands-on': 'Hands-on',
    'Work alongside': 'Bekerja bersama',
    'senior engineers': 'senior engineer',
    'ship real products': 'ship produk nyata',
    'build a portfolio': 'build portfolio',
    'that opens doors': 'yang membuka peluang',

    # ===== Hero subtitles untranslated =====
    'is the foundation of every efficient business operation. Untreated electrical issues not only disrupt productivity but also threaten the safety of your assets and personnel.':
        'adalah fondasi setiap operasi bisnis yang efisien. Masalah electrical yang tidak ditangani tidak hanya mengganggu produktivitas tetapi juga mengancam keselamatan aset dan personil Anda.',

    # ===== SURGE-E extra =====
    'You can run your operations efficiently': 'Anda bisa menjalankan operasi secara efisien',

    # ===== Common stat labels =====
    'KEY SPECS': 'SPESIFIKASI UTAMA',
    'TECHNICAL SPECS': 'SPESIFIKASI TEKNIS',
    'COMPLIANCE': 'COMPLIANCE',
    'CERTIFICATIONS': 'SERTIFIKASI',

    # ===== Workflow keywords =====
    'Process Analysis': 'Analisis Proses',
    'System Design': 'Desain Sistem',
    'Manufacturing and installing units': 'Manufaktur dan instalasi unit',

    # ===== Forms / CTA =====
    'Request Quote': 'Minta Quote',
    'Get Pricing': 'Dapatkan Harga',
    'Schedule a Call': 'Jadwalkan Panggilan',
    'Talk to Sales': 'Bicara dengan Sales',
    'Talk to Engineer': 'Bicara dengan Engineer',
    'Speak with our team': 'Bicara dengan tim kami',

    # ===== Generic phrases =====
    'Looking for': 'Mencari',
    'Need help with': 'Butuh bantuan dengan',
    'You need': 'Anda butuh',
    'We make it easy': 'Kami buat mudah',
    'It\u2019s simple.': 'Sederhana.',
    'How it works': 'Cara kerjanya',
    'See it in action': 'Lihat dalam aksi',
}


PAGES = [
    (12,5273),(29,5274),(839,5275),(1127,5276),(945,5277),(5039,5278),
    (5260,5279),(37,5281),(35,5282),(39,5283),(5029,5284),(5037,5285),
    (5033,5286),(934,5287),(1542,5288),(1546,5289),(1547,5290),
    (1740,5291),(1741,5292),(1742,5293),(1765,5294),(929,5295),
]

total = 0
for en_id, id_id in PAGES:
    r = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{id_id}?context=edit&_fields=meta', headers=HDRS)
    cur = json.loads(urllib.request.urlopen(r, timeout=60).read())
    ed = cur['meta']['_elementor_data']
    if not isinstance(ed, str): ed = json.dumps(ed)
    applied = 0
    for en, idt in V4.items():
        if en in ed:
            ed = ed.replace(en, idt)
            applied += 1
    if applied > 0:
        urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{id_id}', data=json.dumps({'meta':{'_elementor_data':ed}}).encode(), method='POST', headers=HDRS), timeout=60).read()
        print(f'  {id_id}: +{applied}')
        total += applied
print(f'\nTotal V4: {total}')

# Purge
purge = '''
$upload = wp_upload_dir();
$log = $upload['basedir']."/purge-v4.txt";
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
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=json.dumps({'code':purge, 'active':True, 'name':'SX: v4 final'}).encode(), method='POST', headers=HDRS), timeout=60).read()
time.sleep(3)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print('Purged')
