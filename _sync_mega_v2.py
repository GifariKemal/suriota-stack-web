"""Mega dict V2 — automation, DA, DC, product pages specific phrases."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization': f'Basic {AUTH}', 'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

MEGA_V2 = {
    # ===== Automation page =====
    'GE platform': 'platform SURGE',  # cleanup
    '\u2014 energi mapping, vessel tracking, water analytics \u2014 no third-party gateway lock-in.': '\u2014 energy mapping, vessel tracking, water analytics \u2014 tanpa lock-in gateway third-party.',
    'Modbus & OPC UA Ready': 'Modbus & OPC UA Ready',
    'In-house SRT-MGATE-1210 Modbus Gateway bridges legacy RTU/TCP devices to modern MQTT/OPC UA cloud telemetry.':
        'SRT-MGATE-1210 Modbus Gateway in-house menghubungkan device legacy RTU/TCP ke telemetri cloud modern MQTT/OPC UA.',
    'End-to-End Delivery': 'Delivery Menyeluruh',
    'Feasibility \u2192 design \u2192 wiring \u2192 PLC code \u2192 HMI/SCADA \u2192 commissioning \u2192 operator training. One accountable partner, one contract.':
        'Feasibility \u2192 desain \u2192 wiring \u2192 PLC code \u2192 HMI/SCADA \u2192 commissioning \u2192 training operator. Satu mitra bertanggung jawab, satu kontrak.',
    'Cybersecurity-Aware Design': 'Desain Cybersecurity-Aware',
    'OT/IT network segregation, firewall zones, role-based HMI access, and encrypted telemetry per IEC 62443. Reduce attack surface from day one.':
        'Segregasi jaringan OT/IT, firewall zone, akses HMI role-based, dan telemetri terenkripsi sesuai IEC 62443. Mengurangi attack surface dari hari pertama.',
    'Lifecycle Support': 'Dukungan Siklus Hidup',
    '12-month warranty, indexed spare parts, annual SCADA backup, and remote diagnostics. We stay engaged long after go-live.':
        'Garansi 12 bulan, spare part terindeks, backup SCADA tahunan, dan diagnostik remote. Kami tetap engaged jauh setelah go-live.',
    'Real-Time IoT Monitoring': 'Monitoring IoT Real-Time',
    'Sensors, gateways, and dashboards for monitoring industrial parameters': 'Sensor, gateway, dan dashboard untuk monitoring parameter industri',
    'water quality, temperature, and pressure in real-time.': 'kualitas air, suhu, dan tekanan secara real-time.',
    'SURGE IIoT Platform': 'Platform SURGE IIoT',
    'Integrated SaaS IIoT solution: Energy Mapping, Water Analytics, and Vessel Tracking with web & mobile interfaces.':
        'Solusi SaaS IIoT terintegrasi: Energy Mapping, Water Analytics, dan Vessel Tracking dengan interface web & mobile.',
    'Automated Control Systems': 'Sistem Kontrol Otomatis',
    'Design and implementation of PLC, SCADA, and microcontroller systems for industrial process and infrastructure automation.':
        'Desain dan implementasi sistem PLC, SCADA, dan microcontroller untuk otomasi proses industri dan infrastruktur.',
    'Integration & Programming': 'Integrasi & Programming',
    'Modbus, MQTT, OPC-UA protocol integration between sensors, actuators, management systems, and existing IT infrastructure.':
        'Integrasi protokol Modbus, MQTT, OPC-UA antara sensor, aktuator, sistem manajemen, dan infrastruktur IT yang ada.',
    'HMI & Operator Interface': 'HMI & Interface Operator',
    'Custom HMI design with Wonderware, FactoryTalk, Ignition. Touchscreen panels, alarm management, and operator training included.':
        'Desain HMI custom dengan Wonderware, FactoryTalk, Ignition. Panel touchscreen, manajemen alarm, dan training operator termasuk.',
    'Industri 4.0 Digital Twin': 'Digital Twin Industri 4.0',
    'Edge computing, MQTT-to-cloud telemetry, and digital twin modeling for predictive maintenance dan OEE optimization.':
        'Edge computing, telemetri MQTT-ke-cloud, dan pemodelan digital twin untuk predictive maintenance dan optimasi OEE.',
    'Process Analysis': 'Analisis Proses',
    'Identify automation potential': 'Identifikasi potensi otomasi',
    'PLC/SCADA, HMI, IoT architecture': 'Arsitektur PLC/SCADA, HMI, IoT',
    'Installation & Wiring': 'Instalasi & Wiring',
    'Control panels, instrumentation, IoT network': 'Panel kontrol, instrumentasi, jaringan IoT',
    'Software config, testing, validation': 'Konfigurasi software, testing, validasi',
    'Training & Support': 'Training & Support',
    'Operator training and ongoing support': 'Training operator dan dukungan berkelanjutan',
    'What communication': 'Komunikasi apa',

    # ===== Data Analytics =====
    'retention controls.': 'kontrol retensi.',
    'Our analytics capabilities': 'Kapabilitas analytics kami',
    'Real-time Dashboards': 'Dashboard Real-time',
    'Operational dashboards on Grafana, Metabase, Power BI. Sub-second refresh for time-critical KPIs.':
        'Dashboard operasional di Grafana, Metabase, Power BI. Refresh sub-detik untuk KPI time-critical.',
    'KPI & Performance': 'KPI & Performa',
    'OEE, MTBF, MTTR, energi intensity, water quality, asset utilisation \u2014 with targets and trend.':
        'OEE, MTBF, MTTR, intensitas energi, kualitas air, utilisasi aset \u2014 dengan target dan tren.',
    'Regulatory Reporting': 'Pelaporan Regulasi',
    'KLHK SPARING (water effluent), KEMENPERIN, BPS, OJK, BSSN. Auto-generated, audit-traceable.':
        'SPARING KLHK (effluent air), KEMENPERIN, BPS, OJK, BSSN. Auto-generate, audit-traceable.',
    'Predictive Analytics': 'Analytics Prediktif',
    'Forecasting, what-if simulation, root-cause analysis on operational and business data.':
        'Forecasting, simulasi what-if, analisis root-cause pada data operasional dan bisnis.',
    'Data Engineering': 'Data Engineering',
    'Pipelines (Kafka, Airflow, dbt), data quality, schema evolution, time-series databases.':
        'Pipeline (Kafka, Airflow, dbt), data quality, evolusi schema, database time-series.',
    'Business Intelligence': 'Business Intelligence',
    'Self-service BI for analysts, semantic layer, governed access, scheduled distribution.':
        'BI self-service untuk analis, semantic layer, akses ter-governance, distribusi terjadwal.',
    'Our analytics workflow': 'Alur kerja analytics kami',
    'KPI definition': 'Definisi KPI',
    'Co-create the metrics that matter, who owns each, what target counts as success.':
        'Co-create metrik yang penting, siapa pemilik masing-masing, target apa yang dihitung sebagai sukses.',
    'Data plumbing': 'Data plumbing',
    'Connect sources, model the schema, build pipelines, test data quality.':
        'Connect sumber, model schema, build pipeline, test data quality.',
    'Dashboard design': 'Desain dashboard',
    'Wireframe with users, iterate on real data, tune for fast load and clarity.':
        'Wireframe dengan user, iterasi pada data nyata, tune untuk load cepat dan clarity.',
    'Train & launch': 'Training & launch',
    'Onboard operators and analysts; document drill paths and alert routes.':
        'Onboarding operator dan analis; dokumentasi drill path dan alert route.',
    'Iterate': 'Iterasi',
    'Monthly review of usage, retire dead metrics, add new use cases, evolve schema.':
        'Review bulanan penggunaan, retire metrik mati, tambah use case baru, evolve schema.',
    'Which BI tools do you support?': 'BI tool apa yang Anda support?',
    'Can you handle KLHK SPARING?': 'Apakah Anda menangani SPARING KLHK?',
    'Where is the data stored?': 'Di mana data disimpan?',
    'How fast can we see results?': 'Seberapa cepat kami melihat hasil?',
    'What about data security?': 'Bagaimana dengan keamanan data?',
    'Ready to build your KPI cockpit?': 'Siap membangun cockpit KPI Anda?',
    'share your data sources, our team responds': 'bagikan sumber data Anda, tim kami merespon',
    'with a KPI map and a phased dashboard delivery plan.':
        'dengan peta KPI dan rencana delivery dashboard berfase.',

    # ===== Digital Consulting =====
    'business, not the one with the best margin for us.': 'bisnis, bukan yang terbaik untuk margin kami.',
    'Build-ready': 'Siap-Build',
    'If you choose to execute, the same team that scoped the plan can implement it.':
        'Jika Anda memilih eksekusi, tim yang sama yang scope rencana bisa implementasi.',
    'Our consulting capabilities': 'Kapabilitas konsultasi kami',
    'Digital Strategy': 'Strategi Digital',
    'Define digital ambition, target operating model, and the use-case portfolio aligned to business outcomes.':
        'Definisikan ambisi digital, target operating model, dan portfolio use-case yang sejalan dengan outcome bisnis.',
    'Industri 4.0 Assessment': 'Assessment Industri 4.0',
    'Maturity diagnostic across data, automation, analytics, organisation, and culture. Benchmark vs peers.':
        'Diagnostik maturitas di data, otomasi, analytics, organisasi, dan budaya. Benchmark vs peer.',
    'Technology Roadmap': 'Roadmap Teknologi',
    '12\u201336 month sequenced plan with milestones, dependencies, capex/opex budget, and risk register.':
        'Rencana sekuensial 12\u201336 bulan dengan milestone, dependency, budget capex/opex, dan risk register.',
    'ROI & Business Case': 'ROI & Business Case',
    'Quantified business cases per use case: investment, payback, NPV, sensitivity analysis, KPI targets.':
        'Business case terkuantifikasi per use case: investasi, payback, NPV, analisis sensitivitas, target KPI.',
    'Compliance Advisory': 'Advisory Compliance',
    'KLHK, SNI, IEC, PUIL, OJK fintech, BSSN cybersecurity \u2014 mapping requirements to your architecture.':
        'KLHK, SNI, IEC, PUIL, OJK fintech, BSSN cybersecurity \u2014 mapping requirement ke arsitektur Anda.',
    'Change Management': 'Manajemen Perubahan',
    'Operator training plans, governance structures, communication, KPIs that drive adoption.':
        'Rencana training operator, struktur governance, komunikasi, KPI yang mendorong adopsi.',
    'Our consulting workflow': 'Alur kerja konsultasi kami',
    'Listen': 'Dengarkan',
    'Interviews with leaders and operators \u2014 surface pain, ambition, constraints.':
        'Wawancara dengan leader dan operator \u2014 angkat pain, ambisi, constraint.',
    'Assess': 'Asses',
    'Current-state diagnostic across people, process, technology, data.':
        'Diagnostik current-state di people, process, teknologi, data.',
    'Ideate': 'Ideasi',
    'Long-list of use cases; score by value, feasibility, urgency.':
        'Long-list use case; skor berdasarkan value, feasibility, urgency.',
    'Plan': 'Rencana',
    'Roadmap, budget, governance, KPIs. Defend it to your CFO.':
        'Roadmap, budget, governance, KPI. Pertahankan ke CFO Anda.',
    'Hand off (or build)': 'Serah-terima (atau build)',
    'Deliver the plan to your team, or execute it with you. Your call.':
        'Serahkan rencana ke tim Anda, atau eksekusi bersama. Pilihan Anda.',
    'How long does a consulting engagement take?': 'Berapa lama engagement konsultasi?',
    'Do you only recommend SURIOTA products?': 'Apakah Anda hanya merekomendasikan produk SURIOTA?',
    'Will the roadmap be specific or generic?': 'Apakah roadmap akan spesifik atau generik?',
    'Can you defend the business case to leadership?': 'Apakah Anda bisa pertahankan business case ke leadership?',
    'Do you sign NDAs?': 'Apakah Anda menandatangani NDA?',
    'Ready to plan your digital roadmap?': 'Siap merencanakan roadmap digital Anda?',

    # ===== SRT-MGATE =====
    'mapping, JSON/custom topic output.': 'mapping, output JSON/topic custom.',
    'Dual Network Failover': 'Failover Jaringan Dual',
    'WiFi 2.4 GHz (802.11 b/g/n) + Ethernet 10/100 with auto-failover. Optional PoE (IEEE 802.3af/at) on select versions.':
        'WiFi 2.4 GHz (802.11 b/g/n) + Ethernet 10/100 dengan auto-failover. PoE opsional (IEEE 802.3af/at) di versi tertentu.',
    'Industrial-Grade Hardware': 'Hardware Industrial-Grade',
    '-40\u00b0C to 75\u00b0C operating range, 2kV isolation on RS-485, dual 12-48VDC redundant inputs. Built for harsh environments.':
        'Rentang operasi -40\u00b0C hingga 75\u00b0C, isolasi 2kV pada RS-485, input redundant dual 12-48VDC. Built untuk lingkungan keras.',
    'Mobile BLE Configuration': 'Konfigurasi BLE Mobile',
    'Configure via Suriota Config app (Android/iOS) over BLE 5.0, up to 50m range. Tidak PC, no cables, no Telnet required.':
        'Konfigurasi via app Suriota Config (Android/iOS) lewat BLE 5.0, jangkauan hingga 50m. Tanpa PC, tanpa kabel, tanpa Telnet.',
    'Cloud-Agnostic Integration': 'Integrasi Cloud-Agnostic',
    'Connects to AWS IoT, Azure IoT Hub, Google Cloud, ThingsBoard, and on-premises MQTT brokers. Tidak vendor lock-in.':
        'Terhubung ke AWS IoT, Azure IoT Hub, Google Cloud, ThingsBoard, dan MQTT broker on-premise. Tanpa vendor lock-in.',
    'Secure Local Data Logging': 'Logging Data Lokal Aman',
    'MicroSD slot for CSV/JSON local logging during outages. TLS/SSL encryption and firewall rules ensure end-to-end security.':
        'Slot MicroSD untuk logging lokal CSV/JSON saat outage. Enkripsi TLS/SSL dan rule firewall memastikan keamanan end-to-end.',
    'What protocols does the Modbus Gateway support?': 'Protokol apa yang didukung Modbus Gateway?',
    'Does it support offline data buffering?': 'Apakah mendukung buffering data offline?',
    'How is the gateway configured?': 'Bagaimana gateway dikonfigurasi?',
    'Ready to bridge your industrial assets to IoT?': 'Siap menghubungkan aset industri Anda ke IoT?',
    'Request a quote, RFQ, or live technical demo.': 'Minta quote, RFQ, atau demo teknis live.',
    'with sample register-map configurations for your existing equipment.':
        'dengan konfigurasi register-map sample untuk peralatan existing Anda.',

    # ===== Header menu items + footer =====
    'Internet of Things': 'Internet of Things',  # keep
    'System Integration': 'Integrasi Sistem',
    'Digital Consulting': 'Digital Consulting',
    'Artificial Intelligence': 'Kecerdasan Buatan',
    'Data Analytics': 'Data Analytics',
    'Software as a Service': 'Software sebagai Layanan',
    'Electrical': 'Electrical',
    'Automation': 'Otomasi',
    'Water Treatment': 'Water Treatment',
    'Renewable Energy': 'Renewable Energy',
    'Waste Water Logger': 'Waste Water Logger',
    'SURGE-Energy Mapping': 'SURGE-Energy Mapping',
    'SURGE-Vessel Tracking': 'SURGE-Vessel Tracking',
    'SURGE-Water Analytic': 'SURGE-Water Analytic',
    'ISO-M485 Series': 'ISO-M485 Series',
    'RS-485 Surge Protector': 'RS-485 Surge Protector',
    'OUR SERVICES': 'LAYANAN KAMI',
    'PRODUCTS': 'PRODUK',

    # ===== Stats labels =====
    '2+': '2+',
    'YEARS EXPERIENCE': 'TAHUN PENGALAMAN',
    'PROJECTS': 'PROYEK',
    'STANDARDS': 'STANDAR',

    # ===== Common phrases =====
    'No third-party gateway lock-in.': 'Tanpa lock-in gateway third-party.',
    'No vendor lock-in.': 'Tanpa vendor lock-in.',
    'Audit-traceable.': 'Audit-traceable.',
    'real-time': 'real-time',
    'real time': 'real time',
    'best margin for us': 'margin terbaik untuk kami',
    'No handover gap.': 'Tanpa handover gap.',
    'Tanpa handover gap.': 'Tanpa handover gap.',
}


PAGES = [
    (12, 5273), (29, 5274), (839, 5275), (1127, 5276), (945, 5277), (5039, 5278),
    (5260, 5279), (37, 5281), (35, 5282), (39, 5283), (5029, 5284), (5037, 5285),
    (5033, 5286), (934, 5287), (1542, 5288), (1546, 5289), (1547, 5290),
    (1740, 5291), (1741, 5292), (1742, 5293), (1765, 5294), (929, 5295),
]

total = 0
for en_id, id_id in PAGES:
    r = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{id_id}?context=edit&_fields=meta', headers=HDRS)
    cur = json.loads(urllib.request.urlopen(r, timeout=60).read())
    ed = cur['meta']['_elementor_data']
    if not isinstance(ed, str): ed = json.dumps(ed)
    applied = 0
    for en, idt in MEGA_V2.items():
        if en in ed:
            ed = ed.replace(en, idt)
            applied += 1
    if applied > 0:
        urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{id_id}', data=json.dumps({'meta': {'_elementor_data': ed}}).encode(), method='POST', headers=HDRS), timeout=60).read()
        print(f'  {id_id}: +{applied}')
        total += applied

print(f'\nTotal: {total} replacements applied')

# Purge
purge = '''
$upload = wp_upload_dir();
$log = $upload['basedir']."/purge-mega-v2.txt";
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
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=json.dumps({'code':purge, 'active':True, 'name':'SX: purge mega v2'}).encode(), method='POST', headers=HDRS), timeout=60).read()
time.sleep(3)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print('Purged')
