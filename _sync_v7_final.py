"""V7 — comprehensive translation for remaining English in 14 MED pages."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

V7 = {
    # ===== Internship =====
    'Hands-on internship for real-world experience in IoT Industri, automation, and renewable energi projects.': 'Magang langsung untuk pengalaman dunia nyata dalam proyek IoT Industri, otomasi, dan renewable energi.',

    # ===== Water Treatment =====
    'Clean water is a fundamental need for every industrial operation, public facility, and community. Well-designed water treatment systems ensure': 'Air bersih adalah kebutuhan dasar untuk setiap operasi industri, fasilitas publik, dan komunitas. Sistem water treatment yang dirancang dengan baik memastikan',
    'Clean water is a fundamental need for every industrial operation, public facility, and community.': 'Air bersih adalah kebutuhan dasar untuk setiap operasi industri, fasilitas publik, dan komunitas.',
    'Well-designed water treatment systems ensure': 'Sistem water treatment yang dirancang dengan baik memastikan',
    'Our jangka panjang partnership with PDAM Tirta Kepri proves SURIOTA\u2019s competence in managing city-scale water infrastructure': 'Kemitraan jangka panjang kami dengan PDAM Tirta Kepri membuktikan kompetensi SURIOTA dalam mengelola infrastruktur air skala kota',
    'Dengan sensor kualitas air terintegrasi (pH, turbidity, DO, flowmeter) and the SURGE Water Analytics platform, kami membantu Anda merespons': 'Dengan sensor kualitas air terintegrasi (pH, turbidity, DO, flowmeter) dan platform SURGE Water Analytics, kami membantu Anda merespons',
    'and the SURGE Water Analytics platform': 'dan platform SURGE Water Analytics',
    'In-house sensor calibration traceable to national standards. Lab testing for raw water and effluent verification before SPARING data submission.': 'Kalibrasi sensor in-house dengan traceability ke standar nasional. Lab testing untuk verifikasi raw water dan effluent sebelum submisi data SPARING.',
    'What is SPARING and why is it important?': 'Apa itu SPARING dan mengapa penting?',

    # ===== SaaS =====
    'is SURIOTA\u2019s multi-tenant SaaS platform - built for asset-heavy industries that need monitoring real-time, regulatory reporting, and operational insight without standing up their own infrastructure.':
        'adalah platform SaaS multi-tenant SURIOTA - dibangun untuk industri asset-heavy yang butuh monitoring real-time, regulatory reporting, dan operational insight tanpa membangun infrastruktur sendiri.',
    'Three flagship modules ship today: SURGE-Energy Mapping, SURGE-Vessel Tracking, SURGE-Water Analytics. Need something different? We build custom SaaS on the same proven platform.':
        'Tiga modul unggulan tersedia: SURGE-Energy Mapping, SURGE-Vessel Tracking, SURGE-Water Analytics. Butuh yang lain? Kami build SaaS custom di platform yang sama dan terbukti.',
    'Cloud SaaS - no infrastructure to provision.': 'Cloud SaaS - tanpa infrastruktur yang perlu di-provision.',
    'First dashboards live in 1\u20132 weeks.': 'Dashboard pertama live dalam 1\u20132 minggu.',
    'Tiered subscription - start with one site or 100 assets, scale to thousands without re-platforming.':
        'Subscription bertingkat - mulai dengan satu lokasi atau 100 aset, scale ke ribuan tanpa re-platforming.',
    '30\u201345 minute walkthrough on real data, scoped to your use case.':
        'Walkthrough 30\u201345 menit pada data nyata, sesuai use case Anda.',
    'Tidak infrastructure required.': 'Tanpa infrastruktur tambahan.',
    'Our team will walk you through SURGE on data similar to yours dalam 24 jam of request - energi, vessel, water':
        'Tim kami akan walkthrough SURGE pada data serupa milik Anda dalam 24 jam dari permintaan - energi, vessel, water',

    # ===== Electrical =====
    'All installation, panel building, and commissioning follow SNI, IEC, and PUIL 2011. Documented test reports and as-built drawings for every project.':
        'Seluruh instalasi, panel building, dan commissioning mengikuti SNI, IEC, dan PUIL 2011. Test report terdokumentasi dan as-built drawing untuk setiap proyek.',
    'Power systems terintegrasi dengan SURGE Energy for real-time consumption, demand, and fault monitoring.':
        'Sistem daya terintegrasi dengan SURGE Energy untuk monitoring konsumsi real-time, demand, dan fault.',
    'HSE-driven procedures with JSA, LOTO, and PTW documentation. Insurance-backed installations with zero LTI track record on industrial sites.':
        'Prosedur HSE-driven dengan dokumentasi JSA, LOTO, dan PTW. Instalasi ber-asuransi dengan track record zero LTI di site industri.',
    'Every project delivered with As-Built Drawings, Commissioning Reports, BAST, and recommended maintenance schedules. Audit-ready documentation.':
        'Setiap proyek diserahkan dengan As-Built Drawings, Laporan Commissioning, BAST, dan rekomendasi jadwal maintenance. Dokumentasi audit-ready.',
    'Custom LV/MV switchgear, MCC panels, ATS, and distribution boards built to IEC 61439 standards with full FAT documentation.':
        'Switchgear LV/MV custom, panel MCC, ATS, dan distribution board sesuai standar IEC 61439 dengan dokumentasi FAT lengkap.',
    'Industrial LED lighting design, cable tray routing, conduit installation, and lightning protection systems for warehouses and plants.':
        'Desain industrial LED lighting, routing cable tray, instalasi conduit, dan sistem lightning protection untuk warehouse dan pabrik.',
    'SURIOTA uses SNI (Indonesian National Standard), IEC (International Electrotechnical Commission), and PUIL (General Instalasi Electrical Req':
        'SURIOTA menggunakan SNI (Standar Nasional Indonesia), IEC (International Electrotechnical Commission), dan PUIL (Persyaratan Umum Instalasi Listrik',
    'bagikan scope Anda, our tim engineer merespon dalam 24 jam with an SNI/IEC/PUIL-compliant pengecekan kelayakan.':
        'bagikan scope Anda, tim engineer kami merespon dalam 24 jam dengan pengecekan kelayakan compliant SNI/IEC/PUIL.',

    # ===== Automation =====
    'PLC, SCADA & IIoT integration with gateway Modbus for Industri 4.0. Vendor-agnostic automation di sektor manufaktur, oil & gas, shipyard, en':
        'Integrasi PLC, SCADA & IIoT dengan gateway Modbus untuk Industri 4.0. Otomasi vendor-agnostic di sektor manufaktur, oil & gas, shipyard, en',
    'In the Industri 4.0 era, automation and smart monitoring are no longer luxuries':
        'Di era Industri 4.0, otomasi dan smart monitoring bukan lagi kemewahan',
    'they are essentials for survival and growth.': 'tetapi keharusan untuk bertahan dan tumbuh.',
    'SURIOTA deliv': 'SURIOTA menyediakan',
    'SURIOTA delivers': 'SURIOTA menyediakan',
    'With our in-house SURGE platform': 'Dengan platform SURGE in-house kami',
    'an integrated IIoT ecosystem': 'ekosistem IIoT terintegrasi',
    'we deliver energi monitoring, water analytics, vessel tracking, and automa': 'kami menyediakan monitoring energi, water analytics, vessel tracking, dan otomasi',
    'SURIOTA\u2019s team designs and implements automation systems from small to large scale using Siemens S7, Omron, Schneider, and IEC 61131-3 compl':
        'Tim SURIOTA merancang dan mengimplementasi sistem otomasi dari skala kecil hingga besar menggunakan Siemens S7, Omron, Schneider, dan IEC 61131-3 compliant',
    'We integrate Siemens, Schneider, Mitsubishi, Omron, Allen-Bradley - picking the right controller for your plant, not for our supply chain.':
        'Kami integrasi Siemens, Schneider, Mitsubishi, Omron, Allen-Bradley - memilih controller yang tepat untuk plant Anda, bukan untuk supply chain kami.',
    'Native integration with our SURplatform SURGE - energi mapping, vessel tracking, water analytics - no third-party gateway lock-in.':
        'Integrasi native dengan platform SURGE - energy mapping, vessel tracking, water analytics - tanpa lock-in gateway third-party.',
    'OT/IT network segregation, firewall zones, role-based HMI access, and encrypted telemetry per IEC 62443. Reduce attack surface from day one.':
        'Segregasi jaringan OT/IT, firewall zone, akses HMI role-based, dan telemetri terenkripsi sesuai IEC 62443. Kurangi attack surface dari hari pertama.',
    '12-month warranty, indexed spare parts, annual SCADA backup, and remote diagnostics. We stay engaged long after go-live.':
        'Garansi 12 bulan, spare part terindeks, backup SCADA tahunan, dan diagnostik remote. Kami tetap engaged jauh setelah go-live.',
    'Integrated SaaS IIoT solution: Energy Mapping, Water Analytics, and Vessel Tracking with web & mobile interfaces.':
        'Solusi SaaS IIoT terintegrasi: Energy Mapping, Water Analytics, dan Vessel Tracking dengan interface web & mobile.',
    'The SURplatform SURGE mendukung standard industrial protocols including Modbus RTU/TCP, MQTT, HTTP REST API, and OPC-UA. We can also integra':
        'Platform SURGE mendukung protokol industri standar termasuk Modbus RTU/TCP, MQTT, HTTP REST API, dan OPC-UA. Kami juga bisa integrasi',

    # ===== RE =====
    'Renewable energi is the future': 'Renewable energi adalah masa depan',
    'and the future starts now.': 'dan masa depan dimulai sekarang.',
    'SURIOTA delivers integrated renewable energi solutions untuk industri, public facilities, and communities di seluruh Indonesia.':
        'SURIOTA menyediakan solusi renewable energi terintegrasi untuk industri, fasilitas publik, dan komunitas di seluruh Indonesia.',
    'SURIOTA has experience designing PLTS (solar) and PLTB (wind) systems standalone or hybrid. Our sistem hybrid PLTS-PLTB are ideal untuk off-':
        'SURIOTA memiliki pengalaman merancang sistem PLTS (solar) dan PLTB (wind) standalone atau hybrid. Sistem hybrid PLTS-PLTB kami ideal untuk off-',
    'Every project begins with a comprehensive studi kelayakan: irradiation analysis, load calculation, ROI projection, and optimal system planni':
        'Setiap proyek dimulai dengan studi kelayakan komprehensif: analisis irradiasi, kalkulasi beban, proyeksi ROI, dan perencanaan sistem optimal',
    'Combined solar & wind generation with battery storage - proven on Hybrid PJU PLTS + PLTB deployments.':
        'Kombinasi generasi solar & wind dengan storage baterai - terbukti pada deployment Hybrid PJU PLTS + PLTB.',
    'End-to-end PLN net-metering registration, SLO certification, AEROSOL permit processing. We handle paperwork while you focus on operations.':
        'Registrasi PLN net-metering end-to-end, sertifikasi SLO, processing permit AEROSOL. Kami handle paperwork sementara Anda fokus operasi.',
    'Combined solar and wind turbines for stable energi supply, ideal untuk off-grid applications and IoT-based street lighting.':
        'Kombinasi turbin solar dan wind untuk supply energi stabil, ideal untuk aplikasi off-grid dan street lighting berbasis IoT.',
    'SURGE Energy Mapping platform integration for real-time renewable energi production and consumption monitoring.':
        'Integrasi platform SURGE Energy Mapping untuk monitoring produksi dan konsumsi renewable energi real-time.',
    'Feasibility studies, technical calculations, and optimal renewable energi system planning tailored to your needs.':
        'Studi kelayakan, kalkulasi teknis, dan perencanaan sistem renewable energi optimal sesuai kebutuhan Anda.',
    'Lithium battery storage systems (LiFePO4) for peak shaving, load shifting, and backup. Sized for residential to industrial BESS deployments.':
        'Sistem storage baterai lithium (LiFePO4) untuk peak shaving, load shifting, dan backup. Diukur untuk deployment BESS residential hingga industri.',
    'PJU PLTS & Hybrid PJU PLTS-PLTB with IoT remote monitoring. Government-spec compliant for municipal road lighting projects.':
        'PJU PLTS & Hybrid PJU PLTS-PLTB dengan monitoring IoT remote. Compliant spec pemerintah untuk proyek penerangan jalan municipal.',
    'What are the advantages of PLTS-PLTB hybrid over PLTS alone?': 'Apa keunggulan hybrid PLTS-PLTB dibanding PLTS saja?',
    'Hybrid systems leverage two renewable energy sources simultaneously. When solar production is low (night or cloudy), wind turbines continue':
        'Sistem hybrid memanfaatkan dua sumber renewable energy secara simultan. Saat produksi solar rendah (malam atau mendung), turbin wind tetap',
    'What is the estimated ROI for industrial PLTS systems?': 'Berapa estimasi ROI untuk sistem PLTS industri?',

    # ===== IoT =====
    'IoT Industri & system integration - Modbus RTU/TCP to MQTT gateways, edge computing, AWS IoT Core & SURGE cloud dashboards for manufaktur, o':
        'IoT Industri & integrasi sistem - gateway Modbus RTU/TCP ke MQTT, edge computing, AWS IoT Core & dashboard cloud SURGE untuk manufaktur, o',
    'SURIOTA designs and deploys IIoT systems that survive Indonesian industrial conditions - kelembaban tinggi, daya yang fluktuatif, konektivit':
        'SURIOTA merancang dan deploy sistem IIoT yang survive kondisi industri Indonesia - kelembaban tinggi, daya fluktuatif, konektivit',
    'Whether you are mulai dari satu line atau scale ke banyak pabrik, we deliver a arsitektur terpadu':
        'Baik Anda mulai dari satu line atau scale ke banyak pabrik, kami menyediakan arsitektur terpadu',
    'not a kumpulan solusi terpisah.': 'bukan kumpulan solusi terpisah.',
    'Reference designs covering edge, network, security, and cloud layers. Sized for your scale and compliance needs.':
        'Desain referensi mencakup edge, network, security, dan cloud layer. Diukur sesuai scale dan kebutuhan compliance Anda.',
    'Gateway and PLC-edge deployments with local data preprocessing, store-and-forward, and offline resilience.':
        'Deployment gateway dan PLC-edge dengan preprocessing data lokal, store-and-forward, dan resilience offline.',
    'SURplatform SURGE deployment or integration with AWS IoT, Azure IoT Hub, Google Cloud IoT with dashboards and alerts.':
        'Deployment platform SURGE atau integrasi dengan AWS IoT, Azure IoT Hub, Google Cloud IoT dengan dashboard dan alert.',
    'bagikan scope Anda, our tim engineer merespon dalam 24 jam with a pengecekan kelayakan aligned to keamanan IEC 62443':
        'bagikan scope Anda, tim engineer kami merespon dalam 24 jam dengan pengecekan kelayakan sesuai keamanan IEC 62443',

    # ===== DC =====
    'Many digital transformation programs stall because the roadmap was written by consultants who never built a thing. SURIOTA consultants are p':
        'Banyak program digital transformation mandek karena roadmap ditulis konsultan yang belum pernah build apapun. Konsultan SURIOTA adalah p',
    'We help you pick the right Industri 4.0 use cases, sequence them by ROI and risk, and budget realistically. Then we can build them too, if y':
        'Kami bantu Anda memilih use case Industri 4.0 yang tepat, mengurutkan berdasarkan ROI dan risiko, dan budget realistis. Lalu kami bisa build juga, jika',
    'Recommendations based on what we have built, not slide decks. We know what fails di Indonesian conditions.':
        'Rekomendasi berdasarkan apa yang kami sudah build, bukan slide deck. Kami tahu apa yang gagal di kondisi Indonesia.',
    'Tidak reseller incentive.': 'Tanpa reseller incentive.',
    'We pick the right stack for your bisnis, bukan yang terbaik untuk margin kami.':
        'Kami pilih stack yang tepat untuk bisnis Anda, bukan yang terbaik untuk margin kami.',
    '12\u201336 month sequenced plan with milestones, dependencies, capex/opex budget, and risk register.':
        'Rencana sekuensial 12\u201336 bulan dengan milestone, dependency, budget capex/opex, dan risk register.',
    'Interviews with leaders and operators - surface pain, ambition, constraints.':
        'Wawancara dengan leader dan operator - angkat pain, ambisi, constraint.',
    'share your context, our consulting team responds dalam 24 jam with a scoped engagement proposal aligned to your busin':
        'bagikan konteks Anda, tim konsultan kami merespon dalam 24 jam dengan proposal engagement scoped sesuai bisnis',

    # ===== SURGE-E =====
    'Your all-in-one SaaS platform for real-time energi monitoring, smart device control, and significant operational cost reduction.':
        'Platform SaaS all-in-one Anda untuk monitoring energi real-time, kontrol device smart, dan reduksi biaya operasional signifikan.',
    'Are You Struggling with Uncontrolled Energy Costs Across Your Properties?':
        'Apakah Anda Berjuang dengan Biaya Energi Tidak Terkontrol di Properti Anda?',
    'Difficulty identifying which devices or locations are wasting the most energi.':
        'Kesulitan mengidentifikasi device atau lokasi mana yang paling boros energi.',
    'Inability to track energi usage patterns for strategic decision-making.':
        'Ketidakmampuan melacak pola penggunaan energi untuk pengambilan keputusan strategis.',
    'Add, edit, and remotely control AC, lighting, machines from one screen. Enforce efficiency policies automatically.':
        'Tambah, edit, dan kontrol AC, lighting, mesin secara remote dari satu layar. Terapkan policy efisiensi otomatis.',
    '99.9% Uptime SLA, critical alert response under 35s. Scales from 10 to 10,000+ devices simultaneously.':
        'SLA Uptime 99.9%, respon alert critical di bawah 35 detik. Scale dari 10 hingga 10,000+ device simultan.',
    'Drill into weeks, months, years of consumption data. Export CSV/PDF reports for energi audits and BAU planning.':
        'Drill ke data konsumsi mingguan, bulanan, tahunan. Export laporan CSV/PDF untuk audit energi dan perencanaan BAU.',
    'Request a free demo of SURGE Energy Mapping. We\'ll walk you through a real dashboard with your property type in under 24 hours.':
        'Minta demo gratis SURGE Energy Mapping. Kami akan walkthrough dashboard nyata dengan tipe properti Anda dalam 24 jam.',

    # ===== SURGE-V =====
    'Your intelligent platform for live monitoring, real-time tracking, and maritime operational excellence.':
        'Platform cerdas Anda untuk monitoring live, tracking real-time, dan operational excellence maritim.',
    'Are You Facing Challenges in Managing Your Maritim Fleet?':
        'Apakah Anda Menghadapi Tantangan dalam Manajemen Armada Maritim Anda?',
    'Managing a fleet of vessels comes with unique and complex challenges. Without an integrated system, you might be dealing with:':
        'Mengelola armada kapal datang dengan tantangan unik dan kompleks. Tanpa sistem terintegrasi, Anda mungkin menghadapi:',
    'Lack of real-time visibility on vessel location, status, and critical systems.':
        'Kurangnya visibilitas real-time pada lokasi kapal, status, dan sistem kritis.',
    'Manual and time-consuming operational reporting for compliance and analysis.':
        'Pelaporan operasional manual dan time-consuming untuk compliance dan analisis.',
    'Live vessel positions with speed, heading, and route trail on interactive map. Multi-vessel dashboard view.':
        'Posisi kapal live dengan kecepatan, heading, dan jejak rute di peta interaktif. Tampilan dashboard multi-kapal.',
    'Voyage replay, daily/weekly reports, compliance documentation. Export CSV/PDF for audit and operational review.':
        'Replay voyage, laporan harian/mingguan, dokumentasi compliance. Export CSV/PDF untuk audit dan review operasional.',
    'Coastal 4G LTE with Iridium/Inmarsat satellite failover for offshore voyages. Continuous tracking, even out of cellular range.':
        'Coastal 4G LTE dengan failover satelit Iridium/Inmarsat untuk voyage offshore. Tracking berkelanjutan, bahkan di luar jangkauan cellular.',
    'Digital logbook for crew manifests, cargo loading, fuel logs, maintenance. Replace paper records with audit-ready data.':
        'Logbook digital untuk manifest crew, loading kargo, log bahan bakar, maintenance. Ganti record kertas dengan data audit-ready.',
    'operations with sample vessels and geofences dalam 24 jam.':
        'operasi dengan kapal sample dan geofence dalam 24 jam.',

    # ===== ISO-M485 =====
    'When your operations depend on fast, stable, and secure data communication, you can\u2019t afford downtime or interference. ISO-M485 Series diran':
        'Saat operasi Anda bergantung pada komunikasi data yang cepat, stabil, dan aman, Anda tidak boleh ada downtime atau interferensi. ISO-M485 Series diran',
    'Optocoupler isolation between RS-485 ports protects upstream PLC/SCADA from ground loops and field-side faults.':
        'Isolasi optocoupler antar port RS-485 melindungi PLC/SCADA upstream dari ground loop dan fault field-side.',
    'Integrated TVS diodes + gas discharge tubes guard against lightning-induced and switching transients on outdoor cables.':
        'TVS diode + gas discharge tube terintegrasi melindungi dari transient akibat petir dan switching di kabel outdoor.',
    '-40\u00b0C to +85\u00b0C operation. DIN rail mountable. Rated for continuous operation in harsh field cabinets.':
        'Operasi -40\u00b0C hingga +85\u00b0C. DIN rail mountable. Rated untuk operasi berkelanjutan di field cabinet keras.',
    'Accepts 7-15VDC or 9-24VDC supply variants for easy integration with industrial 12V or 24V control panels.':
        'Menerima supply 7-15VDC atau 9-24VDC untuk integrasi mudah dengan panel kontrol industri 12V atau 24V.',
    'Supports up to 500 kbps data rate (within distance limits) for high-throughput SCADA and PLC networks.':
        'Mendukung data rate hingga 500 kbps (dalam batas jarak) untuk jaringan SCADA dan PLC high-throughput.',

    # ===== PM1611 =====
    'Control energi usage, eliminate billing disputes, and improve operational efficiency with the PM1611-WD Prepaid Energy Meter IoT. Designed f':
        'Kontrol penggunaan energi, eliminasi sengketa billing, dan tingkatkan efisiensi operasional dengan PM1611-WD Prepaid Energy Meter IoT. Dirancang u',
    'With the PM1611-WD, you can monitor, manage, and secure energi usage ensuring fair billing, preventing wastage, and optimizing performance.':
        'Dengan PM1611-WD, Anda bisa monitor, kelola, dan amankan penggunaan energi memastikan billing adil, mencegah pemborosan, dan optimasi performa.',
    'Local LCD shows balance and consumption. WhatsApp/SMS notifications on low balance, anomalies, and top-ups.':
        'LCD lokal menampilkan saldo dan konsumsi. Notifikasi WhatsApp/SMS saat saldo rendah, anomali, dan top-up.',
    'Review up to 6 days of detailed energi usage per tenant. Identify abnormal consumption and resolve disputes with data.':
        'Review hingga 6 hari penggunaan energi detail per tenant. Identifikasi konsumsi abnormal dan selesaikan sengketa dengan data.',
    'Configure and monitor remotely via web interface using Blynk or MQTT protocol. RTC with NTP sync ensures accurate billing time.':
        'Konfigurasi dan monitor remote via interface web menggunakan protokol Blynk atau MQTT. RTC dengan sync NTP memastikan waktu billing akurat.',

    # ===== SPD-T485 =====
    'When it comes to industrial communication networks, downtime from surge damage is not an option. The SPD-T485-105 RS-485 Surge Protector is':
        'Untuk jaringan komunikasi industri, downtime akibat surge damage bukan opsi. SPD-T485-105 RS-485 Surge Protector adalah',
    'Engineered for RS-485 systems operating up to 1 Mbps, it safeguards your data flow against lightning strikes, electrical surges, and electro':
        'Dirancang untuk sistem RS-485 yang beroperasi hingga 1 Mbps, melindungi data flow Anda dari sambaran petir, surge listrik, dan elektro',
    'Low capacitive load mendukung RS-485 data rates up to 1 Mbps. Harsh environment coating per IEC 60950 for jangka panjang stability.':
        'Capacitive load rendah mendukung data rate RS-485 hingga 1 Mbps. Coating lingkungan keras sesuai IEC 60950 untuk stabilitas jangka panjang.',
    'Our engineers recommend SPD topology and grounding scheme for your specific cable runs dalam 24 jam.':
        'Engineer kami rekomendasi topologi SPD dan skema grounding untuk cable run spesifik Anda dalam 24 jam.',

    # ===== WW =====
    'Suriota\u2019s Wastewater Logger V.3 can take your water management to the next level. Increase operational efficiency and ensure environmental c':
        'Wastewater Logger V.3 dari Suriota dapat membawa manajemen air Anda ke level berikutnya. Tingkatkan efisiensi operasional dan pastikan compliance lingkungan',
    'Built-in solar charging support with charging indicator and battery connector. Perfect for lokasi remote off-grid.':
        'Dukungan solar charging built-in dengan indikator charging dan konektor baterai. Sempurna untuk lokasi remote off-grid.',
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
    for en, idt in V7.items():
        if en in ed:
            ed = ed.replace(en, idt)
            applied += 1
    if applied > 0:
        urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{id_id}', data=json.dumps({'meta':{'_elementor_data':ed}}).encode(), method='POST', headers=HDRS), timeout=60).read()
        print(f'  {id_id}: +{applied}')
        total += applied
print(f'\nV7 total: {total}')

# Purge
purge = '''
$upload = wp_upload_dir();
$log = $upload['basedir']."/purge-v7.txt";
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
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=json.dumps({'code':purge, 'active':True, 'name':'SX: v7'}).encode(), method='POST', headers=HDRS), timeout=60).read()
time.sleep(3)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print('Done')
