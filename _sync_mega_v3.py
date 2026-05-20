"""Mega V3 — final product page patterns, SaaS, RE, Internship specifics."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization': f'Basic {AUTH}', 'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

V3 = {
    # ===== Why X trust patterns =====
    'Why teams trust': 'Mengapa tim mempercayai',
    'Why fleet operators trust': 'Mengapa operator armada mempercayai',
    'Why we lead in': 'Mengapa kami unggul di',
    'Why PDAM & industries trust': 'Mengapa PDAM & industri mempercayai',

    # ===== SURGE-E specifics =====
    'is a powerful, integrated solution designed to give you complete visibility and control over your energi usage. Our web-based SaaS platform empowers you to monitor, control, and optimize your business assets in real-time from a single, intuitive dashboard.':
        'adalah solusi terintegrasi yang powerful, dirancang untuk memberikan visibilitas dan kontrol lengkap atas penggunaan energi Anda. Platform SaaS berbasis web kami memberdayakan Anda untuk monitor, kontrol, dan optimasi aset bisnis secara real-time dari satu dashboard intuitif.',
    'Live Energy Map View': 'Live Energy Map View',
    'Visualize all device locations on an interactive map. Instant Online/Offline status across your entire portfolio at a glance.':
        'Visualisasi semua lokasi device di peta interaktif. Status Online/Offline instant di seluruh portfolio Anda dalam sekejap.',
    'Real-Time Trend Monitoring': 'Monitoring Tren Real-Time',
    'Track Voltage, Amperage, kWh, Power Factor, Temperature, Humidity via live gauges and trend graphs.':
        'Pantau Voltage, Amperage, kWh, Power Factor, Suhu, Kelembaban via gauge dan grafik tren live.',
    'Centralized Multi-Device Control': 'Kontrol Multi-Device Terpusat',
    'Add, edit, and remotely control AC, lighting, machines from one screen. Enforce efficiency policies automatically.':
        'Tambah, edit, dan kontrol AC, lighting, mesin dari satu layar. Terapkan policy efisiensi otomatis.',
    'Enterprise-Grade Reliability': 'Reliability Enterprise-Grade',
    '99.9% Uptime SLA, critical alert response under 35s. Scales from 10 to 10,000+ devices simultaneously.':
        'SLA Uptime 99.9%, respon critical alert di bawah 35 detik. Scale dari 10 hingga 10,000+ device secara simultan.',
    'Historical Analytics & Export': 'Analytics Historis & Export',
    'Drill into weeks, months, years of consumption data. Export CSV/PDF reports for energi audits and BAU planning.':
        'Drill ke data konsumsi mingguan, bulanan, tahunan. Export laporan CSV/PDF untuk audit energi dan perencanaan BAU.',
    'Role-Based Multi-User Access': 'Akses Multi-User Berbasis Peran',
    'Assign admin, manager, viewer, auditor roles. Secure permissions ensure right data reaches right stakeholder.':
        'Tugaskan role admin, manager, viewer, auditor. Permission aman memastikan data tepat sampai ke stakeholder tepat.',
    'Is SURGE Energy Mapping a cloud SaaS or installed software?': 'Apakah SURGE Energy Mapping SaaS cloud atau software yang di-install?',
    'How many devices can SURGE handle per account?': 'Berapa device yang bisa di-handle SURGE per akun?',
    'What is the SLA uptime guarantee?': 'Berapa garansi uptime SLA?',
    'Can SURGE integrate with my existing ERP or BMS?': 'Apakah SURGE bisa terintegrasi dengan ERP atau BMS existing?',
    'Ready to gain full energi visibility?': 'Siap mendapat visibilitas energi penuh?',

    # ===== SURGE-V specifics =====
    'into an integrated digital ecosystem. More than just a vessel tracker, it is a smart operational management system that converts raw data into actionable insights.':
        'menjadi ekosistem digital terintegrasi. Lebih dari sekedar vessel tracker, ini adalah sistem manajemen operasional cerdas yang mengubah data mentah menjadi insight actionable.',
    'Real-Time GPS Tracking': 'GPS Tracking Real-Time',
    'Live vessel positions with speed, heading, and route trail on interactive map. Multi-vessel dashboard view.':
        'Posisi kapal live dengan kecepatan, heading, dan jejak rute di peta interaktif. Tampilan dashboard multi-kapal.',
    'Geofencing & Alerts': 'Geofencing & Alert',
    'Define operation zones, restricted areas, route corridors. Instant alerts on zone entry/exit, deviation, speed breach.':
        'Definisikan zona operasi, area terbatas, koridor rute. Alert instant saat masuk/keluar zona, deviasi, pelanggaran kecepatan.',
    'Engine & Fuel Telemetry': 'Telemetri Mesin & Bahan Bakar',
    'Monitor engine hours, fuel consumption, RPM, alarms via NMEA-2000 / Modbus integration. Reduce idle waste & theft.':
        'Monitor jam mesin, konsumsi bahan bakar, RPM, alarm via integrasi NMEA-2000 / Modbus. Kurangi waste idle & pencurian.',
    'Historical Analytics & Reports': 'Analytics & Laporan Historis',
    'Voyage replay, daily/weekly reports, compliance documentation. Export CSV/PDF for audit and operational review.':
        'Replay voyage, laporan harian/mingguan, dokumentasi compliance. Export CSV/PDF untuk audit dan review operasional.',
    '4G + Satellite Failover': 'Failover 4G + Satelit',
    'Coastal 4G LTE with Iridium/Inmarsat satellite failover for offshore voyages. Continuous tracking, even out of cellular range.':
        'Coastal 4G LTE dengan failover satelit Iridium/Inmarsat untuk voyage offshore. Tracking berkelanjutan, bahkan di luar jangkauan cellular.',
    'Crew & Cargo Logbook': 'Logbook Crew & Kargo',
    'Digital logbook for crew manifests, cargo loading, fuel logs, maintenance. Replace paper records with audit-ready data.':
        'Logbook digital untuk manifest crew, loading kargo, log bahan bakar, maintenance. Ganti record kertas dengan data audit-ready.',
    'Komunikasi apa does the vessel hardware use?': 'Komunikasi apa yang digunakan hardware kapal?',
    'Does it support geofencing and zone alerts?': 'Apakah mendukung geofencing dan alert zona?',
    'Can engine telemetry be added to vessels?': 'Apakah telemetri mesin bisa ditambahkan ke kapal?',
    'Is historical voyage data available for compliance?': 'Apakah data historis voyage tersedia untuk compliance?',
    'Ready to track your fleet smarter?': 'Siap melacak armada Anda lebih cerdas?',
    'Request a live demo of SURGE Vessel Tracking. Our team will simulate your fleet': 'Minta demo live SURGE Vessel Tracking. Tim kami akan simulasikan armada Anda',

    # ===== THM-30MD =====
    'RS-485 Modbus output. Plug into any PLC, SCADA, BMS, or IoT gateway. Configurable slave ID and baud rate.':
        'Output RS-485 Modbus. Plug ke PLC, SCADA, BMS, atau IoT gateway manapun. Slave ID dan baud rate dapat dikonfigurasi.',
    'IP65 Industrial Housing': 'Housing Industri IP65',
    'Dust-tight + jet-water resistant. Stainless probe for food/pharma cleanroom hygiene. Wall & duct mounting.':
        'Dust-tight + jet-water resistant. Probe stainless untuk hygiene cleanroom food/pharma. Mounting wall & duct.',
    'Wide Operating Range': 'Rentang Operasi Luas',
    '-40\u00b0C to +80\u00b0C, 0-100%RH range. Suitable for cold storage, greenhouse, server rooms, and outdoor enclosures.':
        '-40\u00b0C hingga +80\u00b0C, rentang 0-100%RH. Cocok untuk cold storage, greenhouse, server room, dan enclosure outdoor.',
    'Wide Supply Voltage': 'Tegangan Supply Luas',
    'Powered by 5-38VDC. EMC compliant for stable readings without electrical interference in noisy industrial environments.':
        'Didayai 5-38VDC. EMC compliant untuk pembacaan stabil tanpa interferensi listrik di lingkungan industri ber-noise.',
    'Quick DIN Rail Install': 'Install DIN Rail Cepat',
    '35mm DIN rail mount for hassle-free panel deployment. Low-power MCU design minimizes drift while saving energi.':
        'DIN rail mount 35mm untuk deployment panel hassle-free. Desain MCU low-power meminimalkan drift sambil menghemat energi.',
    'What is the sensor accuracy?': 'Berapa akurasi sensor?',
    'What output protocol does THM-30MD use?': 'Protokol output apa yang digunakan THM-30MD?',
    'Is it IP-rated for outdoor or wash-down use?': 'Apakah IP-rated untuk penggunaan outdoor atau wash-down?',
    'What is the operating range?': 'Berapa rentang operasi?',
    'Ready to deploy industrial temp & humidity sensing?': 'Siap deploy sensing suhu & kelembaban industri?',
    'Request a quote with sample Modbus register map.': 'Minta quote dengan register map Modbus sample.',
    'We respond dalam 24 jam with mounting and calibration guidance for your application.': 'Kami respon dalam 24 jam dengan panduan mounting dan kalibrasi untuk aplikasi Anda.',
    'Register map sample': 'Register map sample',

    # ===== PM1611 =====
    'disconnects at zero balance.': 'memutus saat saldo nol.',
    'Remote Connect/Disconnect': 'Connect/Disconnect Remote',
    'Built-in relay memungkinkan remote service control via WiFi/4G. Tidak site visit needed for activation or disconnection.':
        'Relay built-in memungkinkan kontrol service remote via WiFi/4G. Tanpa kunjungan lokasi untuk aktivasi atau disconnection.',
    'Multi-Tariff Configuration': 'Konfigurasi Multi-Tarif',
    'Set peak/off-peak rates, flat tariffs, custom plans. Auto-calculate based on time-of-use schedules per tenant.':
        'Set tarif peak/off-peak, tarif flat, rencana custom. Auto-calculate berdasarkan jadwal time-of-use per tenant.',
    'LCD + Mobile Alerts': 'LCD + Alert Mobile',
    'Local LCD shows balance and consumption. WhatsApp/SMS notifications on low balance, anomalies, and top-ups.':
        'LCD lokal menampilkan saldo dan konsumsi. Notifikasi WhatsApp/SMS saat saldo rendah, anomali, dan top-up.',
    'Historical Usage Tracking': 'Tracking Penggunaan Historis',
    'Review up to 6 days of detailed energi usage per tenant. Identify abnormal consumption and resolve disputes with data.':
        'Review hingga 6 hari penggunaan energi detail per tenant. Identifikasi konsumsi abnormal dan selesaikan sengketa dengan data.',
    'Web Management Portal': 'Portal Manajemen Web',
    'Configure and monitor remotely via web interface using Blynk or MQTT protocol. RTC with NTP sync ensures accurate billing time.':
        'Konfigurasi dan monitor remote via interface web menggunakan protokol Blynk atau MQTT. RTC dengan sync NTP memastikan waktu billing akurat.',
    'Does PM1611-WD support remote disconnect?': 'Apakah PM1611-WD mendukung disconnect remote?',
    'How does the prepaid token system work?': 'Bagaimana cara kerja sistem token prabayar?',
    'Can multi-tariff rates be configured?': 'Apakah tarif multi-tarif dapat dikonfigurasi?',
    'What notification options are available?': 'Opsi notifikasi apa yang tersedia?',
    'Ready to digitize your sub-metering?': 'Siap mendigitalisasi sub-metering Anda?',
    'Request a quote for bulk deployment.': 'Minta quote untuk deployment bulk.',
    'with site survey checklist and installation timeline.': 'dengan checklist site survey dan timeline instalasi.',
    'Site survey checklist': 'Checklist site survey',
    'Bulk deployment ready': 'Siap deployment bulk',

    # ===== SPD-T485 =====
    'EMC compatibility and high immunity to electromagnetic interference.': 'Kompatibilitas EMC dan imunitas tinggi terhadap interferensi elektromagnetik.',
    'Protect your network. Secure your data.': 'Lindungi jaringan Anda. Amankan data Anda.',
    'With the SPD-T485-105, you get certified, proven surge protection keeping your RS-485 communication stable, safe, and running at peak speed.':
        'Dengan SPD-T485-105, Anda mendapat proteksi surge bersertifikat dan terbukti menjaga komunikasi RS-485 Anda stabil, aman, dan berjalan pada kecepatan puncak.',
    '10kA Surge Discharge': 'Discharge Surge 10kA',
    '10kA (8/20\u03bcs) nominal discharge current handles direct lightning-induced transients. 20kA peak capacity.':
        'Discharge current nominal 10kA (8/20\u03bcs) menangani transient akibat petir langsung. Kapasitas peak 20kA.',
    '<25ns Response Time': 'Response Time <25ns',
    'Sub-nanosecond clamp protects sensitive RS-485 transceivers before damaging energi reaches the line driver.':
        'Clamp sub-nanodetik melindungi transceiver RS-485 sensitif sebelum energi merusak mencapai line driver.',
    'IEC 61643-21 Certified': 'Bersertifikat IEC 61643-21',
    'Compliant with IEC 61643-21 Class III data line surge protection. Tested per IEEE C62.41 surge waveforms.':
        'Compliant dengan proteksi surge data line Class III IEC 61643-21. Diuji sesuai surge waveform IEEE C62.41.',
    'DIN Rail Plug-and-Play': 'DIN Rail Plug-and-Play',
    '35mm DIN rail mountable, screw terminals for in/out, ground bonding terminal. Compact form for crowded panels.':
        'DIN rail mountable 35mm, terminal screw untuk in/out, terminal ground bonding. Bentuk kompak untuk panel padat.',
    'Dual-Stage Protection': 'Proteksi Dual-Stage',
    'Two-step sequencing barrier preserves device lifespan and enhances surge suppression performance.':
        'Sequencing barrier dua-tahap menjaga lifespan device dan meningkatkan performa suppression surge.',
    'High-Speed Data Compatible': 'Kompatibel Data High-Speed',
    'Low capacitive load mendukung RS-485 data rates up to 1 Mbps. Harsh environment coating per IEC 60950 for jangka panjang stability.':
        'Capacitive load rendah mendukung data rate RS-485 hingga 1 Mbps. Coating lingkungan keras sesuai IEC 60950 untuk stabilitas jangka panjang.',
    'What is the surge discharge capacity?': 'Berapa kapasitas discharge surge?',
    'How fast does it respond to transients?': 'Seberapa cepat respon terhadap transient?',
    'Is it IEC-certified?': 'Apakah bersertifikat IEC?',
    'How is SPD-T485-105 installed?': 'Bagaimana SPD-T485-105 di-install?',
    'Ready to protect your RS-485 communications?': 'Siap melindungi komunikasi RS-485 Anda?',
    'Request a quote with site survey.': 'Minta quote dengan site survey.',

    # ===== WW Logger =====
    'memilih Wastewater Logger': 'memilih Wastewater Logger',
    'Multi-Parameter Logging': 'Logging Multi-Parameter',
    'Logs pH, TDS, Flow, Pressure, Level via Modbus RS-485 sensor inputs. Configurable channels and sampling intervals.':
        'Log pH, TDS, Flow, Pressure, Level via input sensor Modbus RS-485. Channel dan interval sampling dapat dikonfigurasi.',
    '4G + WiFi Konektivitas': 'Konektivitas 4G + WiFi',
    'Cellular 4G LTE for remote sites, WiFi for local network. Auto-failover ensures continuous data upload.':
        'Cellular 4G LTE untuk lokasi remote, WiFi untuk jaringan lokal. Auto-failover memastikan upload data berkelanjutan.',
    'KLHK SPARING Ready': 'Siap SPARING KLHK',
    'Pre-configured for KLHK SPARING reporting. Compliance-ready effluent data submission per Permen LHK Tidak. 80/2019.':
        'Pre-konfigurasi untuk pelaporan SPARING KLHK. Submission data effluent compliance-ready sesuai Permen LHK No. 80/2019.',
    'Battery Backup + Cloud Sync': 'Backup Baterai + Cloud Sync',
    'Internal Li-ion battery keeps logging during outages. Cloud sync resumes automatically when power/network returns.':
        'Baterai Li-ion internal tetap logging saat outage. Cloud sync resume otomatis saat power/network kembali.',
    'Multi-Protokol Sensor Support': 'Dukungan Sensor Multi-Protokol',
    'Supports Modbus RS232, SDI-12, Wi-Fi, Bluetooth for diverse sensor integration. Plus onboard temperature & humidity sensors.':
        'Mendukung Modbus RS232, SDI-12, Wi-Fi, Bluetooth untuk integrasi sensor beragam. Plus sensor suhu & kelembaban onboard.',
    'Solar Charging Compatible': 'Kompatibel Solar Charging',
    'Built-in solar charging support with charging indicator and battery connector. Perfect for remote off-grid sites.':
        'Dukungan solar charging built-in dengan indikator charging dan konektor baterai. Sempurna untuk lokasi remote off-grid.',
    'Is the logger KLHK SPARING-ready?': 'Apakah logger siap KLHK SPARING?',
    'What sensors does it support?': 'Sensor apa yang didukung?',
    'Does it work without continuous internet?': 'Apakah berfungsi tanpa internet berkelanjutan?',
    'What connectivity options are available?': 'Opsi konektivitas apa yang tersedia?',
    'Ready to automate wastewater compliance?': 'Siap otomasi compliance air limbah?',
    'Request a quote with KLHK SPARING setup plan.': 'Minta quote dengan rencana setup SPARING KLHK.',
    'with parameter mapping and reporting workflow.': 'dengan parameter mapping dan workflow pelaporan.',
    'KLHK setup plan': 'Rencana setup KLHK',
    'Batam-based support': 'Dukungan berbasis Batam',

    # ===== SaaS page =====
    'Indonesian cloud regions for data residency. White-label option for system integrators and regional partners.':
        'Region cloud Indonesia untuk data residency. Opsi white-label untuk system integrator dan partner regional.',
    'Built for Indonesian industrial operations': 'Dibangun untuk operasi industri Indonesia',
    'Quick to deploy': 'Cepat di-deploy',
    'Cloud SaaS \u2014 no infrastructure to provision. First dashboards live in 1\u20132 weeks.':
        'Cloud SaaS \u2014 tanpa infrastruktur untuk di-provision. Dashboard pertama live dalam 1\u20132 minggu.',
    'Indonesia-hosted': 'Hosted di Indonesia',
    'Data residency di Indonesia. UU PDP compliant. Latency optimised for SE Asia.':
        'Data residency di Indonesia. Compliant UU PDP. Latency dioptimasi untuk SE Asia.',
    'Pay as you grow': 'Bayar sesuai pertumbuhan',
    'Tiered subscription \u2014 start with one site or 100 assets, scale to thousands without re-platforming.':
        'Subscription bertingkat \u2014 mulai dari satu lokasi atau 100 aset, scale ke ribuan tanpa re-platforming.',
    'White-label option': 'Opsi White-label',
    'Brand SURGE as your own product. Common for systems integrators and regional partners.':
        'Brand SURGE sebagai produk Anda sendiri. Umum untuk system integrator dan partner regional.',
    'SURGE MODULES': 'MODUL SURGE',
    'What SURGE delivers': 'Yang disediakan SURGE',
    'Real-time energi monitoring across buildings, plants, feeders. Demand response, tariff optimisation, ISO 50001 reports.':
        'Monitoring energi real-time di gedung, pabrik, feeder. Demand response, optimasi tarif, laporan ISO 50001.',
    'Maritim fleet visibility \u2014 AIS, GPS, fuel, engine telemetry. Route optimisation, voyage replay, compliance.':
        'Visibilitas armada maritim \u2014 AIS, GPS, fuel, telemetri mesin. Optimasi rute, replay voyage, compliance.',
    'PDAM & WTP monitoring. KLHK SPARING automated reporting. Leak detection, demand forecasting.':
        'Monitoring PDAM & WTP. Pelaporan SPARING KLHK otomatis. Deteksi kebocoran, forecasting demand.',
    'Custom SaaS Development': 'Custom SaaS Development',
    'Build your domain-specific SaaS on the SURplatform SURGE. We handle multi-tenant, auth, billing, infra.':
        'Build SaaS domain-specific Anda di platform SURGE. Kami handle multi-tenant, auth, billing, infra.',

    # ===== Common tail =====
    'No third-party gateway lock-in.': 'Tanpa lock-in gateway third-party.',
    'Tanpa lock-in gateway third-party.': 'Tanpa lock-in gateway third-party.',
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
    for en, idt in V3.items():
        if en in ed:
            ed = ed.replace(en, idt)
            applied += 1
    if applied > 0:
        urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{id_id}', data=json.dumps({'meta':{'_elementor_data':ed}}).encode(), method='POST', headers=HDRS), timeout=60).read()
        print(f'  {id_id}: +{applied}')
        total += applied
print(f'\nTotal V3: {total}')

# Final mega purge
purge = '''
$upload = wp_upload_dir();
$log = $upload['basedir']."/purge-final-v3.txt";
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
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=json.dumps({'code':purge, 'active':True, 'name':'SX: final v3'}).encode(), method='POST', headers=HDRS), timeout=60).read()
time.sleep(3)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print('Done')
