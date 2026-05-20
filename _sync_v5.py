"""V5 — finishing push for 7 LOW pages."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

V5 = {
    # ===== SaaS remaining =====
    'is SURIOTA\u2019s multi-tenant SaaS platform \u2014 built for asset-heavy industries that need monitoring real-time, regulatory reporting, and operational insight without standing up their own infrastructure.':
        'adalah platform SaaS multi-tenant SURIOTA \u2014 dibangun untuk industri asset-heavy yang membutuhkan monitoring real-time, regulatory reporting, dan operational insight tanpa membangun infrastruktur sendiri.',
    'Three flagship modules ship today: SURGE-Energy Mapping, SURGE-Vessel Tracking, SURGE-Water Analytics. Need something different? We build custom SaaS on the same proven platform.':
        'Tiga modul unggulan tersedia: SURGE-Energy Mapping, SURGE-Vessel Tracking, SURGE-Water Analytics. Butuh yang berbeda? Kami build SaaS custom di platform yang sama dan terbukti.',
    'REST & GraphQL APIs, webhooks, MQTT ingestion, file imports. Open ecosystem.':
        'REST & GraphQL API, webhook, MQTT ingestion, file import. Ekosistem terbuka.',
    'White-label & OEM': 'White-label & OEM',
    'Re-brand SURGE for your customers. Dedicated tenants, custom domains, isolated billing.':
        'Re-brand SURGE untuk pelanggan Anda. Tenant dedicated, domain custom, billing terisolasi.',
    'SURGE onboarding workflow': 'Alur kerja onboarding SURGE',
    'Demo': 'Demo',
    '30\u201345 minute walkthrough on real data, scoped to your use case.':
        'Walkthrough 30\u201345 menit pada data nyata, sesuai use case Anda.',
    'Trial': 'Trial',
    '2-week trial tenant with your devices. We help connect the first few.':
        'Tenant trial 2-minggu dengan device Anda. Kami bantu connect device pertama.',
    'Activate': 'Aktivasi',
    'Subscription tier signed; production tenant provisioned with SLA.':
        'Tier subscription ditandatangani; tenant production di-provisioned dengan SLA.',
    'Scale': 'Scale',
    'Onboard more sites/users; configure custom dashboards, integrations, reports.':
        'Onboarding lebih banyak site/user; konfigurasi dashboard, integrasi, laporan custom.',
    'Optimise': 'Optimasi',
    'Quarterly reviews, new modules, feature requests, success metrics.':
        'Review kuartal, modul baru, feature request, metrik sukses.',
    'What is the SURGE pricing model?': 'Bagaimana model pricing SURGE?',
    'Where is SURGE hosted?': 'Di mana SURGE di-hosting?',
    'Can we self-host SURGE?': 'Apakah bisa self-host SURGE?',
    'What is the SLA?': 'Bagaimana SLA-nya?',
    'Can we white-label SURGE?': 'Apakah bisa white-label SURGE?',

    # ===== SURGE-W remaining =====
    'rochemical': 'rokimia',
    'Your intelligent platform for monitoring real-time kualitas air, regulatory compliance, dan efisiensi operasional.':
        'Platform cerdas Anda untuk monitoring real-time kualitas air, regulatory compliance, dan efisiensi operasional.',
    'Difficulty ensuring compliance with quality standards set by the government (like KLHK) and international bodies.':
        'Kesulitan memastikan compliance dengan standar kualitas yang ditetapkan pemerintah (seperti KLHK) dan badan internasional.',
    'The risk of environmental pollution due to delayed detection of water quality anomalies.':
        'Risiko polusi lingkungan akibat keterlambatan deteksi anomali kualitas air.',
    'Operational inefficiencies at water and wastewater treatment plants (WTP, WWTP).':
        'Inefisiensi operasional di water dan wastewater treatment plant (WTP, WWTP).',
    'A lack of accurate, structured historical data for analysis and strategic decision-making.':
        'Kurangnya data historis akurat dan terstruktur untuk analisis dan pengambilan keputusan strategis.',
    'is an advanced solution from Suriota, specifically designed to address the challenges of water quality management. This platform empowers Wastewater Treatment Rencanats (WWTPs), Sewage Treatment Rencanats (STPs), Water Treatment Rencanats (WTPs), and Regional Utilitas Air (PDAMs) to perform continuous monitoring, in-depth analysis, and proactive control over water quality parameters.':
        'adalah solusi canggih dari Suriota, dirancang khusus untuk menjawab tantangan manajemen kualitas air. Platform ini memberdayakan Wastewater Treatment Plant (WWTP), Sewage Treatment Plant (STP), Water Treatment Plant (WTP), dan Perusahaan Daerah Air Minum (PDAM) untuk melakukan monitoring berkelanjutan, analisis mendalam, dan kontrol proaktif atas parameter kualitas air.',
    'Monitoring berkelanjutan of pH, COD, BOD, TSS, Ammonia, Turbidity, Flow. Early anomaly detection for preventive action.':
        'Monitoring berkelanjutan pH, COD, BOD, TSS, Ammonia, Turbidity, Flow. Deteksi anomali awal untuk aksi preventif.',
    'Direct integration to KLHK SPARING servers per Permen LHK Tidak. 80/2019. Automated regulatory reporting.':
        'Integrasi langsung ke server SPARING KLHK sesuai Permen LHK No. 80/2019. Pelaporan regulasi otomatis.',
    'Visualize all monitoring points on interactive map. Color-coded compliance status across WTPs, WWTPs, and intake points.':
        'Visualisasi semua titik monitoring di peta interaktif. Status compliance kode warna di WTP, WWTP, dan intake point.',
    'Integrates with Hach, Endress+Hauser, Yokogawa, Krohne, and other major sensor brands via Modbus / 4-20mA / RS-485.':
        'Terintegrasi dengan Hach, Endress+Hauser, Yokogawa, Krohne, dan brand sensor utama lainnya via Modbus / 4-20mA / RS-485.',
    'ML-based threshold learning detects parameter drift before exceedance. Get warned of trending non-compliance days ahead.':
        'Threshold learning berbasis ML mendeteksi parameter drift sebelum exceedance. Dapat peringatan tren non-compliance hari ke depan.',
    'WhatsApp, SMS, push notification alerts on parameter exceedance. Field operators check live status from any phone.':
        'Alert WhatsApp, SMS, push notification saat exceedance parameter. Operator lapangan cek status live dari telepon manapun.',

    # ===== THM-30MD =====
    'When your operations demand accuracy, stability, and jangka panjang durability, the THM-30MD delivers. Powered by the high-performance SHT30 Sensirion sensor, this device ensures precise environmental monitoring in even the toughest industrial conditions. Protecting your equipment, processes, and products.':
        'Saat operasi Anda menuntut akurasi, stabilitas, dan ketahanan jangka panjang, THM-30MD menjawab. Didukung sensor SHT30 Sensirion high-performance, device ini memastikan monitoring lingkungan presisi bahkan di kondisi industri terkeras. Melindungi peralatan, proses, dan produk Anda.',
    'Guard your operations with precise data.': 'Lindungi operasi Anda dengan data presisi.',
    'The THM-30MD gives you the insight you need to maintain optimal conditions, maximize efficiency, and protect what matters most.':
        'THM-30MD memberikan insight yang Anda butuhkan untuk menjaga kondisi optimal, memaksimalkan efisiensi, dan melindungi yang terpenting.',
    'Why facility managers choose THM-30MD': 'Mengapa facility manager memilih THM-30MD',
    'High-Precision Sensing': 'Sensing Presisi Tinggi',
    '\u00b10.3\u00b0C / \u00b12%RH accuracy across full range. SHT30 Sensirion-grade element with calibration stability over years.':
        'Akurasi \u00b10.3\u00b0C / \u00b12%RH di full range. Element SHT30 Sensirion-grade dengan stabilitas kalibrasi bertahun-tahun.',
    'Modbus RTU Native': 'Modbus RTU Native',

    # ===== PM1611 sample untranslated =====
    'Built for landlords, sub-meters, and asset operators': 'Dibangun untuk landlord, sub-meter, dan asset operator',
    'memilih PM1611-WD': 'memilih PM1611-WD',

    # ===== SPD-T485 =====
    'Maximum Surge Protection. Precision Speed. Compact Design.':
        'Proteksi Surge Maksimum. Kecepatan Presisi. Desain Kompak.',
    'High Surge Discharge Capacity': 'Kapasitas Discharge Surge Tinggi',
    'Ultra-Fast Response': 'Respon Ultra-Cepat',
    'Sub-Nanosecond Clamping': 'Clamping Sub-Nanodetik',
    'High-Speed Data Compatible': 'Kompatibel Data High-Speed',
    'Industry-Leading Standards': 'Standar Industri-Terdepan',

    # ===== WW Logger =====
    'Wastewater Compliance Made Smart': 'Compliance Air Limbah Jadi Cerdas',
    'A robust IoT data logger purpose-built for WWTP, industrial effluent, and KLHK SPARING monitoring. Multi-parameter capture, cellular + WiFi, solar-ready.':
        'Data logger IoT yang kokoh, dibangun khusus untuk WWTP, effluent industri, dan monitoring KLHK SPARING. Capture multi-parameter, cellular + WiFi, solar-ready.',
    'Why operators choose Wastewater Logger': 'Mengapa operator memilih Wastewater Logger',
    'memilih Wastewater Logger': 'memilih Wastewater Logger',

    # ===== RE remaining =====
    'PLTS-PLTB sistem hybrid': 'sistem hybrid PLTS-PLTB',

    # ===== Common form/spec phrases =====
    'across its full operating range.': 'di seluruh rentang operasinya.',
    'across the operating range.': 'di seluruh rentang operasi.',
    'over years.': 'bertahun-tahun.',
    'over the years': 'selama bertahun-tahun',
    'over time.': 'seiring waktu.',
    'across years': 'selama bertahun-tahun',
    'EMC compliant': 'EMC compliant',
    'noise-resistant': 'noise-resistant',

    # ===== Internship FAQ =====
    'Open to all majors.': 'Terbuka untuk semua jurusan.',
    'Updated CV (max 2 pages).': 'CV terbaru (maksimal 2 halaman).',
    'Portfolio link or attachment.': 'Link portfolio atau lampiran.',
    'Brief cover letter (\u2264 200 words).': 'Cover letter singkat (\u2264 200 kata).',
    'Letter of recommendation (campus or supervisor).': 'Surat rekomendasi (kampus atau supervisor).',
    'Internship certificate at completion.': 'Sertifikat magang saat selesai.',
    'Monthly stipend': 'Tunjangan bulanan',
    'Real project ownership.': 'Kepemilikan proyek nyata.',
    'Mentorship from senior engineers.': 'Mentorship dari senior engineer.',
    'Career path opportunity.': 'Peluang career path.',
    'Hybrid working arrangement.': 'Pengaturan kerja hybrid.',
    'Free office snacks & coffee.': 'Snack & kopi kantor gratis.',
    'Team outings & company events.': 'Outing tim & event perusahaan.',

    # ===== MGATE remaining =====
    'Industrial Konektivitas': 'Konektivitas Industri',

    # ===== Generic phrases that recur =====
    'in noisy industrial environments': 'di lingkungan industri ber-noise',
    'across years of operation': 'selama bertahun-tahun operasi',
    'in harsh industrial conditions': 'dalam kondisi industri keras',
    'to maintain optimal conditions': 'untuk menjaga kondisi optimal',
    'maximize efficiency': 'memaksimalkan efisiensi',
    'protect what matters most': 'melindungi yang terpenting',
    'cold storage, greenhouse, server rooms': 'cold storage, greenhouse, server room',
    'food/pharma cleanroom': 'cleanroom food/pharma',

    # ===== Section headings =====
    'Open Positions': 'Posisi Terbuka',
    'Required Documents': 'Dokumen yang Diperlukan',
    'Apply Process': 'Proses Lamar',
    'Hiring Process': 'Proses Hiring',
    'Submission Deadline': 'Batas Submisi',

    # ===== Newsletter =====
    'STAY UPDATED': 'TETAP UPDATE',
    'Subscribe to our newsletter': 'Berlangganan newsletter kami',
    'Get the latest updates': 'Dapatkan update terbaru',
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
    for en, idt in V5.items():
        if en in ed:
            ed = ed.replace(en, idt)
            applied += 1
    if applied > 0:
        urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{id_id}', data=json.dumps({'meta':{'_elementor_data':ed}}).encode(), method='POST', headers=HDRS), timeout=60).read()
        print(f'  {id_id}: +{applied}')
        total += applied
print(f'\nV5 total: {total}')

purge = '''
$upload = wp_upload_dir();
$log = $upload['basedir']."/purge-v5.txt";
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
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=json.dumps({'code':purge, 'active':True, 'name':'SX: v5'}).encode(), method='POST', headers=HDRS), timeout=60).read()
time.sleep(3)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print('Done')
