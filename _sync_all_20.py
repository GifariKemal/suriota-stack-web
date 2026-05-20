"""Batch sync 20 remaining ID pages with comprehensive shared translation dict."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from _sync_lib import sync_page

# === MASSIVE SHARED TRANSLATION DICT — common SURIOTA terms ===
# Order: long-first to avoid partial match collisions
GLOBAL = {
    # ===== Common phrases & buttons =====
    'Free Consultation': 'Konsultasi Gratis',
    'View All Portfolio': 'Lihat Semua Portfolio',
    'Read More': 'Selengkapnya',
    'Learn More': 'Pelajari Lebih Lanjut',
    'Contact Us': 'Hubungi Kami',
    'Get Started': 'Mulai Sekarang',
    'Download Datasheet': 'Unduh Datasheet',
    'Download Brochure': 'Unduh Brosur',
    'Buy on Tokopedia': 'Beli di Tokopedia',
    'Chat via WhatsApp': 'Chat via WhatsApp',
    'Send': 'Kirim',
    'SEND': 'KIRIM',
    'Submit': 'Kirim',

    # ===== Page section headings =====
    'Industries We Serve': 'Industri yang Kami Layani',
    'INDUSTRIES WE SERVE': 'INDUSTRI YANG KAMI LAYANI',
    'Why SURIOTA': 'Mengapa SURIOTA',
    'WHY SURIOTA': 'MENGAPA SURIOTA',
    'Our Services': 'Layanan Kami',
    'Our Capabilities': 'Kapabilitas Kami',
    'Our IoT capabilities': 'Kapabilitas IoT Kami',
    'What We Deliver': 'Yang Kami Sediakan',
    'WHAT WE DELIVER': 'YANG KAMI SEDIAKAN',
    'How We Work': 'Cara Kami Bekerja',
    'HOW WE WORK': 'CARA KAMI BEKERJA',
    'Our Workflow': 'Alur Kerja Kami',
    'Our delivery workflow': 'Alur Kerja Pengiriman Kami',
    'Frequently Asked Questions': 'Pertanyaan Umum',
    'FAQ': 'FAQ',
    'Related Portfolio Projects': 'Proyek Portfolio Terkait',
    'Ready to start your': 'Siap memulai',
    'GET STARTED': 'MULAI',
    'Get Started': 'Mulai',
    'No obligation': 'Tanpa keterikatan',
    'Response within 24h': 'Respon dalam 24 jam',
    'Batam-based engineering team': 'Tim engineer berbasis Batam',

    # ===== Industry chips =====
    'Manufacturing': 'Manufaktur',
    'Oil & Gas': 'Oil & Gas',
    'Maritime & Shipyard': 'Maritim & Shipyard',
    'Maritime &amp; Shipyard': 'Maritim & Shipyard',
    'Maritime': 'Maritim',
    'Food & Beverage': 'Makanan & Minuman',
    'Food &amp; Beverage': 'Makanan & Minuman',
    'Logistics & Warehousing': 'Logistik & Pergudangan',
    'Logistics &amp; Warehousing': 'Logistik & Pergudangan',
    'Commercial Buildings': 'Gedung Komersial',
    'Mining & Energy': 'Pertambangan & Energi',
    'Mining &amp; Energy': 'Pertambangan & Energi',
    'Mining & Mineral': 'Pertambangan & Mineral',
    'Mining &amp; Mineral': 'Pertambangan & Mineral',
    'Mining & Quarry': 'Pertambangan & Quarry',
    'Mining &amp; Quarry': 'Pertambangan & Quarry',
    'Construction': 'Konstruksi',
    'Pharmaceutical': 'Farmasi',
    'Textile & Garment': 'Tekstil & Garmen',
    'Textile &amp; Garment': 'Tekstil & Garmen',
    'Hospitality & Tourism': 'Perhotelan & Pariwisata',
    'Hospitality &amp; Tourism': 'Perhotelan & Pariwisata',
    'Hospitality': 'Perhotelan',
    'Healthcare & Hospital': 'Kesehatan & Rumah Sakit',
    'Healthcare &amp; Hospital': 'Kesehatan & Rumah Sakit',
    'Power & Energy': 'Daya & Energi',
    'Power &amp; Energy': 'Daya & Energi',
    'Water Utilities': 'Utilitas Air',
    'Maritime & Port': 'Maritim & Pelabuhan',
    'Maritime &amp; Port': 'Maritim & Pelabuhan',
    'Municipality & PDAM': 'Pemerintah & PDAM',
    'Municipality &amp; PDAM': 'Pemerintah & PDAM',
    'Agriculture & Aqua': 'Agrikultur & Akuakultur',
    'Agriculture &amp; Aqua': 'Agrikultur & Akuakultur',
    'Government & Public': 'Pemerintah & Publik',
    'Government &amp; Public': 'Pemerintah & Publik',
    'Residential Estates': 'Perumahan',
    'Smart Building': 'Smart Building',
    'Smart Buildings': 'Smart Buildings',
    'Energy & Utilities': 'Energi & Utilitas',
    'Energy &amp; Utilities': 'Energi & Utilitas',
    'Water Treatment': 'Water Treatment',
    'Renewable Energy': 'Energi Terbarukan',

    # ===== Why Us card content =====
    '64+ live deployments': '64+ deployment aktif',
    'End-to-end ownership': 'Kepemilikan menyeluruh',
    'Security by design': 'Keamanan terintegrasi',
    'Indonesia-ready': 'Siap untuk Indonesia',
    'Engineering Excellence': 'Keunggulan Engineering',
    'Indonesian Manufacturing': 'Manufaktur Indonesia',
    'Local SLA Support': 'Dukungan SLA Lokal',
    'IEC 62443 Compliance': 'Compliance IEC 62443',
    '64+ Industrial Projects': '64+ Proyek Industri',

    # ===== FAQ common =====
    'What is the typical': 'Berapa lama biasanya',
    'project duration?': 'durasi proyek?',
    'Can SURIOTA work with': 'Bisakah SURIOTA bekerja dengan',
    'existing PLCs and sensors?': 'PLC dan sensor yang sudah ada?',
    'Do you provide the cloud platform or use ours?': 'Apakah Anda menyediakan cloud atau menggunakan platform kami?',
    'Both options.': 'Kedua opsi tersedia.',
    'How is IoT security handled?': 'Bagaimana keamanan IoT ditangani?',
    'What is the ongoing support model?': 'Bagaimana model dukungan berkelanjutan?',

    # ===== Hero subtitle parts =====
    'across Indonesia': 'di seluruh Indonesia',
    'across manufacturing, oil & gas, shipyard': 'di sektor manufaktur, oil & gas, shipyard',
    'Indonesian production environments': 'lingkungan produksi Indonesia',
    'high humidity, fluctuating power, intermittent connectivity': 'kelembaban tinggi, daya yang fluktuatif, konektivitas intermiten',
    'starting with a single line or scaling across multiple plants': 'mulai dari satu line atau scale ke banyak pabrik',
    'unified architecture': 'arsitektur terpadu',
    'patchwork of point solutions': 'kumpulan solusi terpisah',
    'certificate-based device identity, signed firmware, and IEC 62443 segmentation': 'identitas device berbasis sertifikat, firmware ter-sign, dan segmentasi IEC 62443',
    'secure, reliable, and observable telemetry': 'telemetri yang aman, andal, dan dapat diobservasi',
    'Built by engineers, for engineers': 'Dibangun oleh engineer, untuk engineer',
    'production across manufacturing, energy, maritime, and utilities': 'produksi di sektor manufaktur, energi, maritim, dan utilitas',
    'one accountable partner, no finger-pointing': 'satu mitra yang bertanggung jawab, tanpa saling menyalahkan',
    'From sensor selection to dashboard delivery': 'Dari pemilihan sensor hingga delivery dashboard',
    'TLS, certificate-based device auth, signed firmware': 'TLS, autentikasi device berbasis sertifikat, firmware ter-sign',
    'isolated network segments per IEC 62443': 'segmen jaringan terisolasi sesuai IEC 62443',
    'SNI, IEC, PUIL, KLHK compliance built-in': 'Compliance SNI, IEC, PUIL, KLHK built-in',
    'Local SLA, on-site team in Batam, Bahasa Indonesia support': 'SLA lokal, tim on-site di Batam, dukungan Bahasa Indonesia',

    # ===== Service-specific common =====
    'IoT Architecture Design': 'Desain Arsitektur IoT',
    'Edge Computing': 'Edge Computing',
    'Protocol Translation': 'Penerjemahan Protokol',
    'Device Management': 'Manajemen Device',
    'IoT Security': 'Keamanan IoT',
    'Cloud & Dashboards': 'Cloud & Dashboard',
    'Cloud &amp; Dashboards': 'Cloud & Dashboard',
    'Discovery': 'Discovery',
    'Architecture': 'Arsitektur',
    'Proof of Concept': 'Proof of Concept',
    'Roll-out': 'Roll-out',
    'Operate': 'Operasi',
    'Site walk, asset inventory': 'Survey lokasi, inventaris aset',
    'current data flows, business objectives': 'data flow saat ini, tujuan bisnis',
    'Solution design, BoM, security model, cost estimate': 'Desain solusi, BoM, model keamanan, estimasi biaya',
    'Pilot on a representative subset': 'Pilot di subset representatif',
    'Full deployment with commissioning, training, and runbook handover': 'Deployment penuh dengan commissioning, training, dan serah-terima runbook',
    'SLA-backed support, observability, capacity planning, continuous improvement': 'Dukungan SLA, observability, capacity planning, peningkatan berkelanjutan',

    # ===== Common menu items =====
    'Home': 'Beranda',
    'About': 'Tentang',
    'Services': 'Layanan',
    'Products': 'Produk',
    'Portfolio': 'Portfolio',
    'Blog': 'Blog',
    'Contact': 'Hubungi',
    'Internship': 'Magang',

    # ===== Form labels =====
    'Your Name': 'Nama Anda',
    'Your Email': 'Email Anda',
    'Your Message': 'Pesan Anda',
    'Subject': 'Subjek',
    'Phone Number': 'Nomor Telepon',
    'Company': 'Perusahaan',
    'Industry': 'Industri',

    # ===== Service descriptions =====
    'Connect, monitor, and optimise your industrial assets with secure end-to-end IoT architecture':
        'Hubungkan, monitor, dan optimasi aset industri Anda dengan arsitektur IoT menyeluruh yang aman',
    'from edge devices to cloud analytics': 'dari edge device hingga analitik cloud',

    # ===== Capabilities labels =====
    'Industrial Projects': 'Proyek Industri',
    'In-House Products': 'Produk In-House',
    'Team Professionals': 'Profesional Tim',
    'Years of Operation': 'Tahun Beroperasi',
    'Capabilities': 'Kapabilitas',
    'CAPABILITIES': 'KAPABILITAS',

    # ===== Misc =====
    'Made in Indonesia': 'Buatan Indonesia',
    'Indonesian manufacturer': 'Produsen Indonesia',
    'turnkey': 'turnkey',
    'turnkey solutions': 'solusi turnkey',
    'real-time monitoring': 'monitoring real-time',
    'predictive maintenance': 'predictive maintenance',
    'Industry 4.0': 'Industry 4.0',
    'manufacturing': 'manufaktur',
    'energy': 'energi',
    'logistics': 'logistik',
    'utilities': 'utilitas',
    'shipyard': 'shipyard',

    # ===== Specific common phrases =====
    'a trusted partner': 'mitra terpercaya',
    'we have been': 'kami telah',
    'we have delivered': 'kami telah menyelesaikan',
    'We design': 'Kami merancang',
    'We deliver': 'Kami menyediakan',
    'We provide': 'Kami menyediakan',
    'We support': 'Kami mendukung',
    'engineering team responds within 24 hours': 'tim engineer merespon dalam 24 jam',
    'feasibility check': 'pengecekan kelayakan',
    'engineering project': 'proyek engineering',
    'share your scope': 'bagikan scope Anda',
    'initial consultation': 'konsultasi awal',

    # ===== Eyebrow tags =====
    'OUR SERVICES': 'LAYANAN KAMI',
    'OUR PRODUCTS': 'PRODUK KAMI',
    'KEY FEATURES': 'FITUR UTAMA',
    'APPLICATIONS': 'APLIKASI',
    'SPECIFICATIONS': 'SPESIFIKASI',
    'TECHNICAL DETAILS': 'DETAIL TEKNIS',
    'WHAT WE OFFER': 'YANG KAMI TAWARKAN',
    'BENEFITS': 'MANFAAT',
    'WHY CHOOSE US': 'MENGAPA PILIH KAMI',

    # ===== KLHK / regulatory =====
    'KLHK SPARING compliance': 'compliance SPARING KLHK',
    'Real-time water quality monitoring': 'Monitoring kualitas air real-time',
    'water quality monitoring': 'monitoring kualitas air',
    'wastewater monitoring': 'monitoring air limbah',
    'pH, COD, TSS, NH3': 'pH, COD, TSS, NH3',
    'IPAL': 'IPAL',
    'WTP, WWTP': 'WTP, WWTP',
    'IPAL design-build': 'desain-build IPAL',

    # ===== Service page hero subtitles =====
    'Panel installation, power distribution & commissioning per SNI, IEC, PUIL 2011':
        'Instalasi panel, distribusi daya & commissioning sesuai SNI, IEC, PUIL 2011',
    'turnkey electrical engineering for oil & gas, shipyard, manufacturing & commercial buildings':
        'electrical engineering turnkey untuk oil & gas, shipyard, manufaktur & commercial buildings',
    'PLC, SCADA & IIoT integration with Modbus gateway for Industry 4.0':
        'Integrasi PLC, SCADA & IIoT dengan gateway Modbus untuk Industry 4.0',
    'vendor-agnostic automation across manufacturing, oil & gas, shipyard, energy & utilities':
        'otomasi vendor-agnostic di sektor manufaktur, oil & gas, shipyard, energi & utilitas',
    'WTP, WWTP & IPAL design-build with KLHK SPARING compliance & real-time IoT monitoring':
        'Desain-build WTP, WWTP & IPAL dengan compliance SPARING KLHK & monitoring IoT real-time',
    'Solar PV PLTS, hybrid PLTS-PLTB & smart street light (PJU) with IoT energy monitoring':
        'Solar PV PLTS, hybrid PLTS-PLTB & smart street light (PJU) dengan monitoring energi IoT',
    'feasibility study, design & installation for industries & commercial buildings':
        'studi kelayakan, desain & instalasi untuk industri & commercial buildings',
}


# === PAGES TO SYNC ===
PAGES = [
    (839, 5275, 'Portfolio',          'https://suriota.com/id/portfolio-id/'),
    (1127, 5276, 'Internship',        'https://suriota.com/id/magang-srt-team/'),
    (945, 5277, 'Water Treatment',    'https://suriota.com/id/water-treatment-id/'),
    (5039, 5278, 'SaaS',              'https://suriota.com/id/saas-id/'),
    (5260, 5279, 'Artikel',           'https://suriota.com/id/artikel-id/'),
    (37, 5281, 'Electrical',          'https://suriota.com/id/electrical-id/'),
    (35, 5282, 'Automation',          'https://suriota.com/id/automation-id/'),
    (39, 5283, 'Renewable Energy',    'https://suriota.com/id/renewable-energy-id/'),
    (5029, 5284, 'IoT',               'https://suriota.com/id/internet-of-things-id/'),
    (5037, 5285, 'Data Analytics',    'https://suriota.com/id/data-analytics-id/'),
    (5033, 5286, 'Digital Consulting','https://suriota.com/id/digital-consulting-id/'),
    (934, 5287, 'SRT-MGATE',          'https://suriota.com/id/suriota-modbus-gateway-id/'),
    (1542, 5288, 'SURGE-Energy',      'https://suriota.com/id/surge-energy-mapping-id/'),
    (1546, 5289, 'SURGE-Vessel',      'https://suriota.com/id/surge-vessel-tracking-id/'),
    (1547, 5290, 'SURGE-Water',       'https://suriota.com/id/surge-water-analytic-id/'),
    (1740, 5291, 'ISO-M485',          'https://suriota.com/id/iso-m485-series-id/'),
    (1741, 5292, 'THM-30MD',          'https://suriota.com/id/thm-30md-id/'),
    (1742, 5293, 'PM1611-WD',         'https://suriota.com/id/pm1611-wd-id/'),
    (1765, 5294, 'SPD-T485',          'https://suriota.com/id/rs-485-surge-protector-id/'),
    (929, 5295, 'WW Logger',          'https://suriota.com/id/waste-water-logger-id/'),
]

ok = 0
for en_id, id_id, label, url in PAGES:
    if sync_page(en_id, id_id, GLOBAL, page_label=label, trigger_url=url):
        ok += 1

print(f'\n========== DONE {ok}/{len(PAGES)} pages synced ==========')
