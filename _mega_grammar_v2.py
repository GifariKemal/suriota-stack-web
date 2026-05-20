"""Mega grammar V2 — comprehensive translation for remaining English on all 27 ID pages."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

# Comprehensive translation dict — covers all 27 ID pages remaining English
MEGA_V2 = {
    # ===== WT =====
    'Kemitraan jangka panjang kami with PDAM Tirta Kepri proves SURIOTA\u2019s competence in managing city-scale water infrastructure':
        'Kemitraan jangka panjang kami dengan PDAM Tirta Kepri membuktikan kompetensi SURIOTA dalam mengelola infrastruktur air skala kota',
    'with PDAM Tirta Kepri proves SURIOTA\u2019s competence in managing city-scale water infrastructure':
        'dengan PDAM Tirta Kepri membuktikan kompetensi SURIOTA dalam mengelola infrastruktur air skala kota',
    'and the SURGE Water Analytics platform, kami membantu Anda merespons':
        'dan platform SURGE Water Analytics, kami membantu Anda merespons',
    'In-house sensor calibration traceable to national standards. Lab testing for raw water and effluent verification before SPARING data submission.':
        'Kalibrasi sensor in-house dengan traceability ke standar nasional. Lab testing untuk verifikasi raw water dan effluent sebelum submisi data SPARING.',

    # ===== SaaS =====
    'SURGE is SURIOTA\u2019s multi-tenant SaaS platform - built for asset-heavy industries that need monitoring real-time, regulatory reporting, and operational insight without standing up their own infrastruct':
        'SURGE adalah platform SaaS multi-tenant SURIOTA - dibangun untuk industri asset-heavy yang butuh monitoring real-time, regulatory reporting, dan operational insight tanpa membangun infrastruktur sendiri',
    'Three flagship modules ship today: SURGE-Energy Mapping, SURGE-Vessel Tracking, SURGE-Water Analytics. Need something different? We build custom SaaS on the same proven platform.':
        'Tiga modul unggulan tersedia: SURGE-Energy Mapping, SURGE-Vessel Tracking, SURGE-Water Analytics. Butuh yang lain? Kami build SaaS custom di platform yang sama.',
    '30\u201345 minute walkthrough on real data, scoped to your use case.':
        'Walkthrough 30\u201345 menit pada data nyata, sesuai use case Anda.',

    # ===== Electrical =====
    'All installation, panel building, and commissioning follow SNI, IEC, and PUIL 2011. Documented test reports and as-built drawings for every proyek.':
        'Seluruh instalasi, panel building, dan commissioning mengikuti SNI, IEC, dan PUIL 2011. Test report terdokumentasi dan as-built drawing untuk setiap proyek.',
    'Power systems terintegrasi dengan SURGE Energy for real-time consumption, demand, and fault monitoring.':
        'Sistem daya terintegrasi dengan SURGE Energy untuk monitoring konsumsi, demand, dan fault real-time.',
    'HSE-driven procedures with JSA, LOTO, and PTW documentation. Insurance-backed installations with zero LTI track record on industrial sites.':
        'Prosedur HSE-driven dengan dokumentasi JSA, LOTO, dan PTW. Instalasi ber-asuransi dengan track record zero LTI di site industri.',
    'Every proyek delivered with As-Built Drawings, Commissioning Reports, BAST, and recommended maintenance schedules. Audit-ready documentation.':
        'Setiap proyek diserahkan dengan As-Built Drawings, Laporan Commissioning, BAST, dan jadwal maintenance rekomendasi. Dokumentasi audit-ready.',

    # ===== Automation =====
    'control accessible real-time from anywhere':
        'kontrol yang dapat diakses real-time dari manapun',
    'SURIOTA\u2019s team designs and implements automation systems from small to large scale using Siemens S7, Omron, Schneider, and IEC 61131-3 compliant microcontrollers.':
        'Tim SURIOTA merancang dan mengimplementasi sistem otomasi dari skala kecil hingga besar menggunakan Siemens S7, Omron, Schneider, dan microcontroller compliant IEC 61131-3.',
    'We integrate Siemens, Schneider, Mitsubishi, Omron, Allen-Bradley - picking the right controller for your plant, not for our supply chain.':
        'Kami integrasi Siemens, Schneider, Mitsubishi, Omron, Allen-Bradley - pilih controller yang tepat untuk plant Anda, bukan untuk supply chain kami.',
    'Native integration with our platform SURGE - energi mapping, vessel tracking, water analytics - tanpa lock-in gateway third-party.':
        'Integrasi native dengan platform SURGE kami - energy mapping, vessel tracking, water analytics - tanpa lock-in gateway third-party.',
    'OT/IT network segregation, firewall zones, role-based HMI access, and encrypted telemetry per IEC 62443. Reduce attack surface from day one.':
        'Segregasi jaringan OT/IT, firewall zone, akses HMI role-based, dan telemetri terenkripsi sesuai IEC 62443. Kurangi attack surface sejak hari pertama.',
    '12-month warranty, indexed spare parts, annual SCADA backup, and remote diagnostics. We stay engaged long after go-live.':
        'Garansi 12 bulan, spare part terindeks, backup SCADA tahunan, dan diagnostik remote. Kami tetap engaged jauh setelah go-live.',
    'Integrated SaaS IIoT solution: Energy Mapping, Water Analytics, and Vessel Tracking with web & mobile interfaces.':
        'Solusi SaaS IIoT terintegrasi: Energy Mapping, Water Analytics, dan Vessel Tracking dengan interface web & mobile.',
    'Platform SURGE mendukung protokol industri standar termasuk Modbus RTU/TCP, MQTT, HTTP REST API, dan OPC-UA. Kami juga bisa integrasite custom protocols specific to your system requirements.':
        'Platform SURGE mendukung protokol industri standar termasuk Modbus RTU/TCP, MQTT, HTTP REST API, dan OPC-UA. Kami juga bisa integrasi protokol custom spesifik untuk requirement sistem Anda.',
    'integrasite custom protocols specific to your system requirements':
        'integrasi protokol custom spesifik untuk requirement sistem Anda',
    'Ready to automate your industrial operations?': 'Siap mengotomatisasi operasi industri Anda?',

    # ===== RE =====
    'SURIOTA has experience designing PLTS (solar) and PLTB (wind) systems standalone or hybrid. Our sistem hybrid PLTS-PLTB are ideal untuk off-grid applications like IoT-based street lighting (PJU).':
        'SURIOTA memiliki pengalaman merancang sistem PLTS (solar) dan PLTB (wind) standalone atau hybrid. Sistem hybrid PLTS-PLTB kami ideal untuk aplikasi off-grid seperti street lighting (PJU) berbasis IoT.',
    'Combined solar & wind generation with battery storage - proven on Hybrid PJU PLTS + PLTB deployments.':
        'Kombinasi generasi solar & wind dengan storage baterai - terbukti pada deployment Hybrid PJU PLTS + PLTB.',
    'End-to-end PLN net-metering registration, SLO certification, AEROSOL permit processing. We handle paperwork while you focus on operations.':
        'Registrasi PLN net-metering end-to-end, sertifikasi SLO, processing permit AEROSOL. Kami handle paperwork sementara Anda fokus operasi.',
    'PJU PLTS & Hybrid PJU PLTS-PLTB with IoT remote monitoring. Government-spec compliant for municipal road lighting proyek.':
        'PJU PLTS & Hybrid PJU PLTS-PLTB dengan monitoring IoT remote. Compliant spec pemerintah untuk proyek penerangan jalan municipal.',

    # ===== IoT =====
    'IoT Industri & system integration - Modbus RTU/TCP to MQTT gateways, edge computing, AWS IoT Core & SURGE cloud dashboards for manufaktur, oil & gas, shipyard, utilitas air & renewable energi di selur':
        'IoT Industri & integrasi sistem - gateway Modbus RTU/TCP ke MQTT, edge computing, AWS IoT Core & dashboard cloud SURGE untuk manufaktur, oil & gas, shipyard, utilitas air & renewable energi di seluruh',
    'SURIOTA merancang dan deploy sistem IIoT yang survive kondisi industri Indonesia - kelembaban tinggi, daya fluktuatif, konektivitas intermiten. Our stack covers sensors and gateways at the edge, secur':
        'SURIOTA merancang dan men-deploy sistem IIoT yang bertahan di kondisi industri Indonesia - kelembaban tinggi, daya fluktuatif, konektivitas intermiten. Stack kami mencakup sensor dan gateway di edge, dengan keamanan',

    # ===== DA =====
    'SURIOTA builds analytics platforms that combine real-time plant data with business systems - production, maintenance, energi, compliance - into role-based dashboards engineers and executives actually':
        'SURIOTA membangun platform analytics yang menggabungkan data plant real-time dengan sistem bisnis - produksi, maintenance, energi, compliance - ke dashboard role-based yang engineer dan eksekutif benar-benar',
    'We work across the stack: ETL/ELT pipelines, time-series databases, BI tools (Metabase, Grafana, Power BI), and regulatory reporting (KLHK SPARING, BPS, OJK).':
        'Kami bekerja di seluruh stack: pipeline ETL/ELT, database time-series, BI tools (Metabase, Grafana, Power BI), dan pelaporan regulasi (KLHK SPARING, BPS, OJK).',
    'Every metric ties to an action: who is alerted, what runbook applies, expected SLA.':
        'Setiap metrik terhubung ke aksi: siapa yang dialert, runbook apa yang berlaku, SLA yang diharapkan.',
    'OEE, MTBF, MTTR, energi intensity, water quality, asset utilisation - with targets and trend.':
        'OEE, MTBF, MTTR, intensitas energi, kualitas air, utilisasi aset - dengan target dan tren.',

    # ===== DC =====
    'Banyak program digital transformation mandek karena roadmap ditulis konsultan yang belum pernah build apapun. Konsultan SURIOTA adalah practising engineers - we have shipped 64+ industrial systems - s':
        'Banyak program digital transformation mandek karena roadmap ditulis konsultan yang belum pernah membangun apapun. Konsultan SURIOTA adalah praktisi engineer - kami telah ship 64+ sistem industri - s',
    'practising engineers': 'praktisi engineer',
    'we have shipped 64+ industrial systems': 'kami telah men-ship 64+ sistem industri',
    'We help you pick the right Industri 4.0 use cases, sequence them by ROI and risk, and budget realistically. Then we can build them too, if you want one accountable partner.':
        'Kami bantu Anda memilih use case Industri 4.0 yang tepat, mengurutkan berdasarkan ROI dan risiko, dan budget realistis. Lalu kami bisa build juga, jika Anda ingin satu mitra yang bertanggung jawab.',
    '12\u201336 month sequenced plan with milestones, dependencies, capex/opex budget, and risk register.':
        'Rencana sekuensial 12\u201336 bulan dengan milestone, dependency, budget capex/opex, dan risk register.',
    'KLHK, SNI, IEC, PUIL, OJK fintech, BSSN cybersecurity - mapping requirements to your architecture.':
        'KLHK, SNI, IEC, PUIL, OJK fintech, BSSN cybersecurity - mapping requirement ke arsitektur Anda.',

    # ===== MGATE =====
    'Power: Dual DC 12-48VDC inputs for redundancy, PoE (IEEE 802.3af/at) option on specific versions':
        'Power: Input dual DC 12-48VDC untuk redundancy, opsi PoE (IEEE 802.3af/at) di versi spesifik',
    'WiFi 2.4 GHz (802.11 b/g/n) + Ethernet 10/100 with auto-failover. Optional PoE (IEEE 802.3af/at) on select versions.':
        'WiFi 2.4 GHz (802.11 b/g/n) + Ethernet 10/100 dengan auto-failover. PoE opsional (IEEE 802.3af/at) di versi tertentu.',
    '-40\u00b0C to 75\u00b0C operating range, 2kV isolation on RS-485, dual 12-48VDC redundant inputs. Dibangun untuk harsh environments.':
        'Rentang operasi -40\u00b0C hingga 75\u00b0C, isolasi 2kV pada RS-485, input dual 12-48VDC redundant. Dibangun untuk lingkungan keras.',
    'Connects to AWS IoT, Azure IoT Hub, Google Cloud, ThingsBoard, and on-premises MQTT brokers. Tanpa vendor lock-in.':
        'Terhubung ke AWS IoT, Azure IoT Hub, Google Cloud, ThingsBoard, dan broker MQTT on-premise. Tanpa vendor lock-in.',
    'MicroSD slot for CSV/JSON local logging during outages. TLS/SSL encryption and firewall rules ensure end-to-end security.':
        'Slot MicroSD untuk logging lokal CSV/JSON saat outage. Enkripsi TLS/SSL dan rule firewall memastikan keamanan end-to-end.',

    # ===== SURGE-E =====
    'Unexpectedly high utility bills that hurt your bottom line.':
        'Tagihan utilitas tinggi tak terduga yang merugikan bottom line Anda.',
    'Difficulty identifying which devices or locations are wasting the most energi.':
        'Kesulitan mengidentifikasi device atau lokasi mana yang paling boros energi.',
    'Inability to track energi usage patterns for strategic decision-making.':
        'Ketidakmampuan melacak pola penggunaan energi untuk pengambilan keputusan strategis.',
    'Visualize all device locations on an interactive map. Instant Online/Offline status across your entire portfolio at a glance.':
        'Visualisasi semua lokasi device di peta interaktif. Status Online/Offline instan di seluruh portfolio Anda dalam sekilas.',
    'Add, edit, and remotely control AC, lighting, machines from one screen. Enforce efficiency policies automatically.':
        'Tambah, edit, dan kontrol AC, lighting, mesin secara remote dari satu layar. Terapkan policy efisiensi otomatis.',
    '99.9% Uptime SLA, critical alert response under 35s. Scales from 10 to 10,000+ devices simultaneously.':
        'SLA Uptime 99.9%, respon alert critical di bawah 35 detik. Scale dari 10 hingga 10,000+ device simultan.',
    'Drill into weeks, months, years of consumption data. Export CSV/PDF reports for energi audits and BAU planning.':
        'Drill ke data konsumsi mingguan, bulanan, tahunan. Export laporan CSV/PDF untuk audit energi dan perencanaan BAU.',
    "Request a free demo of SURGE Energy Mapping. We'll walk you through a real dashboard with your property type in under 24 hours.":
        'Minta demo gratis SURGE Energy Mapping. Kami akan walkthrough dashboard nyata dengan tipe properti Anda dalam 24 jam.',

    # ===== SURGE-V (already partly covered, but redo) =====
    'Live vessel positions with speed, heading, and route trail on interactive map. Multi-vessel dashboard view.':
        'Posisi kapal live dengan kecepatan, heading, dan jejak rute di peta interaktif. Tampilan dashboard multi-kapal.',
    'Voyage replay, daily/weekly reports, compliance documentation. Export CSV/PDF for audit and operational review.':
        'Replay voyage, laporan harian/mingguan, dokumentasi compliance. Export CSV/PDF untuk audit dan review operasional.',
    'Coastal 4G LTE with Iridium/Inmarsat satellite failover for offshore voyages. Continuous tracking, even out of cellular range.':
        'Coastal 4G LTE dengan failover satelit Iridium/Inmarsat untuk voyage offshore. Tracking berkelanjutan, bahkan di luar jangkauan cellular.',
    'Digital logbook for crew manifests, cargo loading, fuel logs, maintenance. Replace paper records with audit-ready data.':
        'Logbook digital untuk manifest crew, loading kargo, log bahan bakar, maintenance. Ganti record kertas dengan data audit-ready.',

    # ===== SURGE-W =====
    'Difficulty memastikan compliance with quality standards set by the government (like KLHK) and international bodies.':
        'Kesulitan memastikan compliance dengan standar kualitas yang ditetapkan pemerintah (seperti KLHK) dan badan internasional.',
    'A lack of accurate, structured historical data for analysis and strategic decision-making.':
        'Kurangnya data historis yang akurat dan terstruktur untuk analisis dan pengambilan keputusan strategis.',
    'Visualize all monitoring points on interactive map. Color-coded compliance status across WTPs, WWTPs, and intake points.':
        'Visualisasi semua titik monitoring di peta interaktif. Status compliance kode warna di WTP, WWTP, dan intake point.',
    'Integrates with Hach, Endress+Hauser, Yokogawa, Krohne, and other major sensor brands via Modbus / 4-20mA / RS-485.':
        'Terintegrasi dengan Hach, Endress+Hauser, Yokogawa, Krohne, dan brand sensor utama lainnya via Modbus / 4-20mA / RS-485.',
    'WhatsApp, SMS, push notification alerts on parameter exceedance. Field operators check live status from any phone.':
        'Alert WhatsApp, SMS, push notification saat exceedance parameter. Operator lapangan cek status live dari telepon manapun.',

    # ===== ISO-M485 =====
    'Saat operasi Anda bergantung pada fast, stable, and secure data communication, you can\u2019t afford downtime or interference. ISO-M485 Series dirancang untuk koneksi RS-485 industrial-grade dengan galvani':
        'Saat operasi Anda bergantung pada komunikasi data cepat, stabil, dan aman, Anda tidak boleh ada downtime atau interferensi. ISO-M485 Series dirancang untuk koneksi RS-485 industrial-grade dengan galvanic',
    'fast, stable, and secure data communication, you can\u2019t afford downtime or interference':
        'komunikasi data cepat, stabil, dan aman, Anda tidak boleh ada downtime atau interferensi',
    'Optocoupler isolation between RS-485 ports protects upstream PLC/SCADA from ground loops and field-side faults.':
        'Isolasi optocoupler antar port RS-485 melindungi PLC/SCADA upstream dari ground loop dan fault field-side.',
    'Integrated TVS diodes + gas discharge tubes guard against lightning-induced and switching transients on outdoor cables.':
        'TVS diode + gas discharge tube terintegrasi melindungi dari transient akibat petir dan switching pada kabel outdoor.',
    '-40\u00b0C to +85\u00b0C operation. DIN rail mountable. Rated untuk continuous operation in harsh field cabinets.':
        'Operasi -40\u00b0C hingga +85\u00b0C. DIN rail mountable. Rated untuk operasi berkelanjutan di field cabinet keras.',
    'Accepts 7-15VDC or 9-24VDC supply variants for easy integration with industrial 12V or 24V control panels.':
        'Menerima supply 7-15VDC atau 9-24VDC untuk integrasi mudah dengan panel kontrol industri 12V atau 24V.',
    'Supports up to 500 kbps data rate (within distance limits) for high-throughput SCADA and PLC networks.':
        'Mendukung data rate hingga 500 kbps (dalam batas jarak) untuk jaringan SCADA dan PLC high-throughput.',

    # ===== THM-30MD =====
    '-40\u00b0C to +80\u00b0C, 0-100%RH range. Suitable for cold storage, greenhouse, server room, and outdoor enclosures.':
        '-40\u00b0C hingga +80\u00b0C, rentang 0-100%RH. Cocok untuk cold storage, greenhouse, server room, dan enclosure outdoor.',

    # ===== PM1611 =====
    'Dirancang uor rental spaces, kiosks, offices, and machinery':
        'Dirancang untuk rental space, kios, kantor, dan mesin',
    'Kontrol penggunaan energi, eliminasi sengketa billing, dan tingkatkan efisiensi operasional dengan PM1611-WD Prepaid Energy Meter IoT. Dirancang uor rental spaces, kiosks, offices, and machinery, this':
        'Kontrol penggunaan energi, eliminasi sengketa billing, dan tingkatkan efisiensi operasional dengan PM1611-WD Prepaid Energy Meter IoT. Dirancang untuk rental space, kios, kantor, dan mesin, alat ini',
    'Local LCD shows balance and consumption. WhatsApp/SMS notifications on low balance, anomalies, and top-ups.':
        'LCD lokal menampilkan saldo dan konsumsi. Notifikasi WhatsApp/SMS saat saldo rendah, anomali, dan top-up.',
    'Review up to 6 days of detailed energi usage per tenant. Identify abnormal consumption and resolve disputes with data.':
        'Review hingga 6 hari penggunaan energi detail per tenant. Identifikasi konsumsi abnormal dan selesaikan sengketa dengan data.',
    'Configure and monitor remotely via web interface using Blynk or MQTT protocol. RTC with NTP sync memastikan accurate billing time.':
        'Konfigurasi dan monitor remote via interface web menggunakan protokol Blynk atau MQTT. RTC dengan sync NTP memastikan waktu billing akurat.',

    # ===== SPD-T485 =====
    'Untuk jaringan komunikasi industri, downtime akibat surge damage bukan opsi. SPD-T485-105 RS-485 Surge Protector adalah pertama di Indonesia bersertifiked to EN 61643-21, delivering world-class protec':
        'Untuk jaringan komunikasi industri, downtime akibat surge damage bukan opsi. SPD-T485-105 RS-485 Surge Protector adalah yang pertama di Indonesia bersertifikat EN 61643-21, memberikan proteksi kelas dunia',
    'bersertifiked to EN 61643-21, delivering world-class protec':
        'bersertifikat EN 61643-21, memberikan proteksi kelas dunia',
    'Dirancang untuk sistem RS-485 yang beroperasi hingga 1 Mbps, melindungi data flow Anda dari sambaran petir, surge listrik, dan elektromagnetic interference, memastikan uninterrupted connectivity in ev':
        'Dirancang untuk sistem RS-485 yang beroperasi hingga 1 Mbps, melindungi data flow Anda dari sambaran petir, surge listrik, dan interferensi elektromagnetik, memastikan konektivitas tanpa terputus di',
    'uninterrupted connectivity': 'konektivitas tanpa terputus',
    'Low capacitive load mendukung RS-485 data rates up to 1 Mbps. Harsh environment coating per IEC 60950 for jangka panjang stability.':
        'Capacitive load rendah mendukung data rate RS-485 hingga 1 Mbps. Coating lingkungan keras sesuai IEC 60950 untuk stabilitas jangka panjang.',

    # ===== WW =====
    'Tingkatkan efisiensi operasional dan pastikan compliance lingkunganmpliance with our innovative solution.':
        'Tingkatkan efisiensi operasional dan pastikan compliance lingkungan dengan solusi inovatif kami.',
    'lingkunganmpliance with our innovative solution': 'lingkungan dengan solusi inovatif kami',
    'Built-in solar charging support with charging indicator and battery connector. Perfect for lokasi remote off-grid.':
        'Dukungan solar charging built-in dengan indikator charging dan konektor baterai. Sempurna untuk lokasi remote off-grid.',

    # ===== Contact =====
    'Talk to our engineers about IoT Industri, system integration, or a custom proyek. We respond within 24 hours on business days.':
        'Bicara dengan engineer kami tentang IoT Industri, integrasi sistem, atau proyek custom. Kami merespon dalam 24 jam pada hari kerja.',
    'Whether you are scoping an IoT deployment, evaluating our SURGE platform, or looking for SCADA / PLC integration \u2014 we will match you with the right engineer within 24 hours.':
        'Baik Anda sedang scoping deployment IoT, evaluasi platform SURGE kami, atau mencari integrasi SCADA / PLC - kami akan menghubungkan Anda dengan engineer yang tepat dalam 24 jam.',
    'WHAT TO INCLUDE IN YOUR MESSAGE': 'YANG PERLU DICANTUMKAN DI PESAN ANDA',
    'Do you offer support and SLA contracts?': 'Apakah Anda menawarkan kontrak support dan SLA?',
    'From message to engagement \u2014 in 4 steps': 'Dari pesan ke engagement - dalam 4 langkah',
    'Kirim us a WhatsApp message or email with your proyek brief.': 'Kirim pesan WhatsApp atau email kepada kami dengan brief proyek Anda.',
    'Within 24 hours, we route your inquiry to the right domain expert (IoT, SCADA, water, solar, electrical).':
        'Dalam 24 jam, kami arahkan inquiry Anda ke expert domain yang tepat (IoT, SCADA, water, solar, electrical).',
    'A free 30-minute scoping call to clarify objectives, constraints, and compliance needs.':
        'Panggilan scoping 30 menit gratis untuk klarifikasi tujuan, constraint, dan kebutuhan compliance.',
    'You receive a written proposal with deliverables, timeline, milestones, and acceptance criteria.':
        'Anda menerima proposal tertulis dengan deliverable, timeline, milestone, dan kriteria penerimaan.',
    'Talk to our engineers today': 'Bicara dengan engineer kami hari ini',
    'Free consultation. No obligation. We respond within 24 hours on business days.':
        'Konsultasi gratis. Tanpa keterikatan. Kami merespon dalam 24 jam pada hari kerja.',

    # ===== Privacy Policy (legal page) =====
    'How PT Surya Inovasi Prioritas (SURIOTA) collects, uses, and protects your personal data. This policy is aligned with Indonesia\u2019s Personal Data Protection Law (UU PDP No.27/2022) and the EU General Da':
        'Bagaimana PT Surya Inovasi Prioritas (SURIOTA) mengumpulkan, menggunakan, dan melindungi data pribadi Anda. Kebijakan ini selaras dengan Undang-Undang Perlindungan Data Pribadi Indonesia (UU PDP No.27/2022) dan EU General Da',
    '13. Changes to this Policy': '13. Perubahan pada Kebijakan Ini',
    '14. Contact': '14. Hubungi',
    '12. Children\u2019s Privacy': '12. Privasi Anak',
    '11. International Data Transfers': '11. Transfer Data Internasional',
    '10. Your Rights': '10. Hak Anda',
    '9. Cookies and Tracking': '9. Cookies dan Tracking',
    '8. Data Security': '8. Keamanan Data',
    '7. Data Retention': '7. Retensi Data',
    '6. Data Sharing': '6. Pembagian Data',
    '5. Legal Basis (GDPR)': '5. Dasar Hukum (GDPR)',
    '4. How We Use Your Data': '4. Bagaimana Kami Menggunakan Data Anda',
    '3. Data We Collect': '3. Data yang Kami Kumpulkan',
    '2. Data Controller': '2. Pengendali Data',
    '1. Overview': '1. Ikhtisar',
    'PT Surya Inovasi Prioritas (\u201cSURIOTA\u201d, \u201cwe\u201d, \u201cus\u201d, or \u201cour\u201d) respects your privacy and is committed to protecting your personal data. This Kebijakan Privasi explains how we collect, use, store, share,':
        'PT Surya Inovasi Prioritas (\u201cSURIOTA\u201d, \u201ckami\u201d, \u201cmilik kami\u201d) menghormati privasi Anda dan berkomitmen melindungi data pribadi Anda. Kebijakan Privasi ini menjelaskan bagaimana kami mengumpulkan, menggunakan, menyimpan, membagi,',
    'By accessing our website, using our products, or engaging our services, you acknowledge that you have read and understood this Kebijakan Privasi.':
        'Dengan mengakses website kami, menggunakan produk kami, atau menggunakan layanan kami, Anda mengakui bahwa Anda telah membaca dan memahami Kebijakan Privasi ini.',
    'The data controller responsible for your personal data is:': 'Pengendali data yang bertanggung jawab atas data pribadi Anda adalah:',
    'Account credentials: if you create an account on the SURGE platform, we collect your username, hashed password, and authentication tokens.':
        'Kredensial akun: jika Anda membuat akun di platform SURGE, kami mengumpulkan username, password ter-hash, dan token autentikasi Anda.',
    'Payment data: billing address and invoice details. We do not store full credit-card numbers \u2014 payments are processed by certified third-party gateways.':
        'Data pembayaran: alamat billing dan detail invoice. Kami tidak menyimpan nomor kartu kredit lengkap - pembayaran diproses oleh gateway third-party bersertifikat.',
    'Correspondence: emails, WhatsApp messages, and call logs you exchange with our team.':
        'Korespondensi: email, pesan WhatsApp, dan log panggilan yang Anda bertukar dengan tim kami.',
    'Device & usage: IP address, browser type, operating system, referring URL, pages visited, time on site, and clickstream data.':
        'Device & penggunaan: alamat IP, tipe browser, sistem operasi, URL referral, halaman yang dikunjungi, waktu di site, dan data clickstream.',
    'Telemetry from products: for IoT deployments using the SURGE platform, we collect device identifiers, sensor readings, geolocation (when consented), and event logs strictly for the purpose of operatin':
        'Telemetri dari produk: untuk deployment IoT menggunakan platform SURGE, kami mengumpulkan identifier device, pembacaan sensor, geolocation (saat disetujui), dan log event semata untuk tujuan operasional',
    'We may receive information from publicly available business directories, professional networks (e.g., LinkedIn), and our partners (e.g., distributors, integrators) when you interact with them about SU':
        'Kami dapat menerima informasi dari direktori bisnis publik, jaringan profesional (mis. LinkedIn), dan partner kami (mis. distributor, integrator) saat Anda berinteraksi dengan mereka tentang SU',
    'We use personal data for the following purposes:': 'Kami menggunakan data pribadi untuk tujuan berikut:',
    'Responding to inquiries, quotations, and providing customer support.': 'Merespons inquiry, penawaran, dan memberikan customer support.',
    'Delivering, operating, and improving our products and services (termasuk the SURGE platform).': 'Memberikan, mengoperasikan, dan meningkatkan produk dan layanan kami (termasuk platform SURGE).',
    'Marketing communications \u2014 only with your opt-in consent for the newsletter. You may unsubscribe at any time.': 'Komunikasi marketing - hanya dengan persetujuan opt-in Anda untuk newsletter. Anda dapat unsubscribe kapan saja.',
    'Compliance with legal obligations under Indonesian law and applicable foreign jurisdictions.': 'Pemenuhan kewajiban hukum sesuai hukum Indonesia dan yurisdiksi asing yang berlaku.',
    'Fraud prevention, security monitoring, and protecting our rights.': 'Pencegahan fraud, monitoring keamanan, dan perlindungan hak kami.',
    'For users in the European Economic Area, our legal bases under GDPR Article 6 are:': 'Untuk pengguna di Wilayah Ekonomi Eropa, dasar hukum kami berdasarkan GDPR Pasal 6 adalah:',
    'Contract performance \u2014 to fulfil engagement and service agreements.': 'Pelaksanaan kontrak - untuk memenuhi perjanjian engagement dan layanan.',
    'Legitimate interests \u2014 to operate our business, secure our services, and develop our products.': 'Kepentingan sah - untuk mengoperasikan bisnis kami, mengamankan layanan kami, dan mengembangkan produk kami.',
    'Consent \u2014 for marketing and optional cookies. You may withdraw consent at any time.': 'Persetujuan - untuk marketing dan cookies opsional. Anda dapat menarik persetujuan kapan saja.',
    'Legal obligation \u2014 to comply with tax, accounting, and regulatory requirements.': 'Kewajiban hukum - untuk mematuhi requirement pajak, akuntansi, dan regulasi.',
    'Service providers processing data on our behalf (cloud hosting, email delivery, analytics, payment) under written data-processing agreements.':
        'Penyedia layanan yang memproses data atas nama kami (cloud hosting, email delivery, analytics, payment) berdasarkan perjanjian pemrosesan data tertulis.',
    'Proyek partners \u2014 integrators, certified installers, or auditors involved in delivering your proyek, only as necessary.':
        'Partner proyek - integrator, installer bersertifikat, atau auditor yang terlibat dalam pengerjaan proyek Anda, hanya sesuai kebutuhan.',
    'Successor entities in the event of merger, acquisition, or asset transfer, with continuity of this Policy\u2019s protections.':
        'Entitas penerus dalam hal merger, akuisisi, atau transfer aset, dengan kelanjutan perlindungan Kebijakan ini.',

    # ===== Terms (legal page) =====
    'The agreement that governs your use of the SURIOTA website, our products (SURGE platform, SRT-MGATE-1210, ISO-M485, THM-30MD, PM1611-WD, RS-485 Surge Protector), and our engineering services. Please r':
        'Perjanjian yang mengatur penggunaan website SURIOTA, produk kami (platform SURGE, SRT-MGATE-1210, ISO-M485, THM-30MD, PM1611-WD, RS-485 Surge Protector), dan layanan engineering kami. Mohon baca',
    'These Syarat Layanan (\u201cTerms\u201d) form a binding agreement between you (\u201cyou\u201d or \u201cKlien\u201d) and PT Surya Inovasi Prioritas (\u201cSURIOTA\u201d, \u201cwe\u201d, \u201cus\u201d, or \u201cour\u201d). By accessing our website, purchasing our produc':
        'Syarat Layanan ini (\u201cKetentuan\u201d) membentuk perjanjian mengikat antara Anda (\u201cAnda\u201d atau \u201cKlien\u201d) dan PT Surya Inovasi Prioritas (\u201cSURIOTA\u201d, \u201ckami\u201d). Dengan mengakses website kami, membeli produ',
    'Services \u2014 engineering, integration, consultation, and SaaS offerings provided by SURIOTA, termasuk the SURGE platform.':
        'Layanan - engineering, integrasi, konsultasi, dan penawaran SaaS yang disediakan SURIOTA, termasuk platform SURGE.',
    'Confidential Information \u2014 any non-public information disclosed by either party that should reasonably be understood to be confidential.':
        'Informasi Rahasia - informasi non-publik apapun yang diungkapkan oleh salah satu pihak yang seharusnya dipahami sebagai rahasia.',
    'SURIOTA provides IoT Industri system integration, automation, water-treatment instrumentation, renewable-energi services, electrical engineering, dan SURGE Software-as-a-Service platform for energi ma':
        'SURIOTA menyediakan integrasi sistem IoT Industri, otomasi, instrumentasi water treatment, layanan renewable energi, electrical engineering, dan platform Software-as-a-Service SURGE untuk manajemen energi',
    'SURIOTA may modify, suspend, or discontinue any portion of the Services with reasonable notice, except where prohibited by contract.':
        'SURIOTA dapat memodifikasi, menangguhkan, atau menghentikan bagian apapun dari Layanan dengan pemberitahuan wajar, kecuali dilarang oleh kontrak.',
    'Some Services require account registration. You agree to: (a) provide accurate, current information; (b) maintain the security of your credentials; (c) promptly notify us of unauthorised access; and (':
        'Beberapa Layanan memerlukan registrasi akun. Anda setuju untuk: (a) memberikan informasi akurat dan terkini; (b) menjaga keamanan kredensial Anda; (c) segera memberitahu kami tentang akses tidak sah; dan (',
    'Use the Services to violate any law or regulation, termasuk export controls.':
        'Menggunakan Layanan untuk melanggar hukum atau regulasi apapun, termasuk kontrol ekspor.',
    'Upload malware, conduct security testing without prior written consent, or otherwise interfere with the integrity of our systems.':
        'Mengunggah malware, melakukan security testing tanpa persetujuan tertulis sebelumnya, atau dengan cara lain mengganggu integritas sistem kami.',
    'Resell, sublicense, or commercially exploit the Services without our written agreement.':
        'Menjual kembali, men-sublisensi, atau mengeksploitasi Layanan secara komersial tanpa perjanjian tertulis kami.',
    'All firmware, software, designs, schematics, documentation, trademarks, and know-how created or owned by SURIOTA \u2014 termasuk the SURGE platform and all Products \u2014 remain the exclusive property of SURIO':
        'Seluruh firmware, software, desain, skematik, dokumentasi, trademark, dan know-how yang dibuat atau dimiliki SURIOTA - termasuk platform SURGE dan semua Produk - tetap menjadi milik eksklusif SURIO',
    'You retain ownership of materials you provide to us. You grant SURIOTA a licence to use such materials as necessary to perform the Services.':
        'Anda tetap memiliki kepemilikan atas materi yang Anda berikan kepada kami. Anda memberikan SURIOTA lisensi untuk menggunakan materi tersebut sesuai kebutuhan untuk melaksanakan Layanan.',
    'Unless otherwise stated in the Engagement, custom Deliverables are licensed (not sold) to you upon full payment. SURIOTA retains rights to reusable components, frameworks, and tooling.':
        'Kecuali ditentukan lain dalam Engagement, Deliverable custom dilisensikan (bukan dijual) kepada Anda setelah pembayaran penuh. SURIOTA tetap memiliki hak atas komponen, framework, dan tooling yang dapat digunakan ulang.',
    'Pricing \u2014 as quoted in writing. Quotes are valid for 30 days unless extended.':
        'Harga - sesuai quote tertulis. Quote berlaku 30 hari kecuali diperpanjang.',
    'Taxes \u2014 VAT (PPN), withholding tax (PPh), and other applicable taxes are added to invoiced amounts unless quoted as tax-inclusive.':
        'Pajak - PPN, PPh, dan pajak lain yang berlaku ditambahkan ke jumlah invoice kecuali di-quote sebagai tax-inclusive.',
    'Late payment \u2014 we may suspend services and charge interest at 1.5% per month on overdue balances, to the extent permitted by law.':
        'Keterlambatan pembayaran - kami dapat menangguhkan layanan dan mengenakan bunga 1.5% per bulan pada saldo lewat jatuh tempo, sejauh diizinkan hukum.',
    'Each party will protect the other\u2019s Confidential Information with the same degree of care it uses to protect its own (no less than reasonable care), use it solely to perform the Engagement, and not di':
        'Setiap pihak akan melindungi Informasi Rahasia pihak lain dengan tingkat perhatian yang sama yang digunakan untuk melindungi miliknya sendiri (tidak kurang dari perhatian wajar), menggunakannya hanya untuk melaksanakan Engagement, dan tidak men',
    'We warrant that the Services will be performed in a professional and workmanlike manner consistent with industry standards. Hardware Products carry the manufacturer-specified warranty period as printe':
        'Kami menjamin bahwa Layanan akan dilaksanakan secara profesional dan terampil sesuai standar industri. Produk Hardware membawa periode garansi yang ditentukan manufacturer sebagaimana tercetak',
    'EXCEPT AS EXPRESSLY STATED, THE SERVICES AND PRODUCTS ARE PROVIDED \u201cAS IS\u201d AND \u201cAS AVAILABLE\u201d, WITHOUT WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING MERCHANTABILITY, FITNESS FOR A PARTICULAR P':
        'KECUALI DINYATAKAN SECARA TEGAS, LAYANAN DAN PRODUK DISEDIAKAN \u201cAS IS\u201d DAN \u201cAS AVAILABLE\u201d, TANPA JAMINAN APAPUN, TERSURAT MAUPUN TERSIRAT, TERMASUK MERCHANTABILITY, KESESUAIAN UNTUK TUJUAN TERTENTU',
    'TO THE MAXIMUM EXTENT PERMITTED BY LAW, SURIOTA\u2019S TOTAL CUMULATIVE LIABILITY ARISING OUT OF OR RELATED TO THESE TERMS OR ANY ENGAGEMENT SHALL NOT EXCEED THE AMOUNT PAID BY YOU TO SURIOTA UNDER THE APP':
        'SEJAUH MAKSIMUM YANG DIIZINKAN OLEH HUKUM, TOTAL LIABILITAS KUMULATIF SURIOTA YANG TIMBUL DARI ATAU TERKAIT DENGAN KETENTUAN INI ATAU ENGAGEMENT APAPUN TIDAK AKAN MELEBIHI JUMLAH YANG ANDA BAYAR KE SURIOTA DI BAWAH APP',
    'IN NO EVENT SHALL SURIOTA BE LIABLE FOR INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, OR FOR LOSS OF PROFITS, REVENUE, DATA, OR USE \u2014 EVEN IF ADVISED OF THE POSSIBILITY.':
        'DALAM SITUASI APAPUN SURIOTA TIDAK BERTANGGUNG JAWAB ATAS KERUSAKAN TIDAK LANGSUNG, INSIDENTAL, KHUSUS, KONSEKUENSIAL, ATAU PUNITIF, ATAU KEHILANGAN KEUNTUNGAN, REVENUE, DATA, ATAU PENGGUNAAN - BAHKAN JIKA DIBERITAHU TENTANG KEMUNGKINANNYA.',
    'You agree to defend, indemnify, and hold harmless SURIOTA, its officers, directors, employees, and agents from and against any claims, damages, losses, liabilities, costs, and expenses (termasuk reaso':
        'Anda setuju untuk membela, mengganti rugi, dan membebaskan SURIOTA, pengurus, direktur, karyawan, dan agennya dari dan terhadap klaim, kerusakan, kerugian, liabilitas, biaya, dan pengeluaran apapun (termasuk biaya wajar',
    'These Terms remain in effect while you use the Services. Either party may terminate an Engagement with thirty (30) days\u2019 written notice, or immediately for material breach not cured within fifteen (15':
        'Ketentuan ini tetap berlaku selama Anda menggunakan Layanan. Salah satu pihak dapat mengakhiri Engagement dengan pemberitahuan tertulis tiga puluh (30) hari, atau segera untuk pelanggaran material yang tidak diperbaiki dalam lima belas (15',
    'These Terms are governed by the laws of the Republic of Indonesia, without regard to its conflict-of-laws principles. Subjek to Section 14 below, any legal proceeding shall be brought exclusively in t':
        'Ketentuan ini diatur oleh hukum Republik Indonesia, tanpa memperhatikan prinsip konflik-hukumnya. Tunduk pada Pasal 14 di bawah, proses hukum apapun harus diajukan secara eksklusif di',
    'The parties will first attempt to resolve any dispute through good-faith negotiation between authorised representatives. If unresolved within thirty (30) days, the dispute shall be submitted to bindin':
        'Para pihak akan terlebih dahulu mencoba menyelesaikan sengketa apapun melalui negosiasi itikad baik antara perwakilan yang berwenang. Jika tidak terselesaikan dalam tiga puluh (30) hari, sengketa akan diajukan ke binding',

    # ===== AI =====
    'Production-grade AI for industrial use cases. Predictive maintenance, computer vision QC, anomaly detection \u2014 built on your data, deployed on your terms.':
        'AI grade produksi untuk use case industri. Predictive maintenance, computer vision QC, deteksi anomali - dibangun di atas data Anda, di-deploy sesuai term Anda.',
    'AI that ships to production, not just demo': 'AI yang ship ke produksi, bukan hanya demo',
    'Many industrial AI proyek die in POC. SURIOTA treats AI like any other engineering discipline \u2014 with version control, observability, model registries, and SLA. We pick high-ROI use cases, train on you':
        'Banyak proyek AI industri mati di POC. SURIOTA memperlakukan AI seperti disiplin engineering lainnya - dengan version control, observability, model registry, dan SLA. Kami pilih use case high-ROI, train pada',
    'From predictive maintenance on rotating equipment to computer-vision quality control on production lines, our models run reliably in conditions where cloud GPUs are not available.':
        'Dari predictive maintenance pada rotating equipment hingga computer-vision quality control di production line, model kami berjalan andal dalam kondisi di mana cloud GPU tidak tersedia.',
    'Edge-capable, retrainable, and governed \u2014 we build AI you can audit and trust.':
        'Edge-capable, retrainable, dan ter-governance - kami build AI yang bisa Anda audit dan percaya.',
    'AI that lives beyond the demo': 'AI yang bertahan setelah demo',
    'Every AI use case ships with measured baseline, target, and post-deployment value tracking.':
        'Setiap use case AI ship dengan baseline terukur, target, dan tracking nilai post-deployment.',
    'Train and run on your infrastructure if needed. Your data never leaves your control.':
        'Train dan jalankan di infrastruktur Anda jika diperlukan. Data Anda tidak pernah keluar dari kontrol Anda.',
    'Pick the highest-ROI AI use case grounded in data availability and operational constraints.':
        'Pilih use case AI dengan ROI tertinggi berdasarkan ketersediaan data dan constraint operasional.',
    'Do we need a lot of data to start?': 'Apakah kami butuh banyak data untuk mulai?',
    'Free initial consultation \u2014 share your data and use case, our ML team responds within 24 hours with a feasibility check termasuk data sufficiency, baseline, and target metrics.':
        'Konsultasi awal gratis - bagikan data dan use case Anda, tim ML kami merespon dalam 24 jam dengan pengecekan kelayakan termasuk data sufficiency, baseline, dan target metric.',

    # ===== SysInt =====
    'Bridge SCADA, ERP, MES, and IoT into a single source of truth. SURIOTA connects legacy and modern systems so your data flows without silos.':
        'Hubungkan SCADA, ERP, MES, dan IoT menjadi satu sumber kebenaran. SURIOTA menghubungkan sistem legacy dan modern sehingga data Anda mengalir tanpa silo.',
    'Most industrial operations run a patchwork of vendor systems: PLCs from one brand, SCADA from another, an ERP that does not talk to either. SURIOTA designs integration architectures \u2014 data buses, APIs':
        'Sebagian besar operasi industri menjalankan campuran sistem vendor: PLC dari satu brand, SCADA dari brand lain, ERP yang tidak terhubung keduanya. SURIOTA merancang arsitektur integrasi - data bus, API',
    'The result: production KPIs, maintenance schedules, energi bills, and customer orders all reconcile in real time.':
        'Hasilnya: KPI produksi, jadwal maintenance, tagihan energi, dan order pelanggan semuanya rekonsiliasi secara real time.',
    'No vendor lock-in. We work with Siemens, Schneider, Rockwell, SAP, Oracle, Microsoft equally.':
        'Tanpa vendor lock-in. Kami bekerja dengan Siemens, Schneider, Rockwell, SAP, Oracle, Microsoft secara setara.',
    'Every integration ships with API specs, runbooks, monitoring, and handover so you stay in control.':
        'Setiap integrasi ship dengan spec API, runbook, monitoring, dan handover sehingga Anda tetap mengontrol.',
    'Bridge SCADA historians (OSIsoft PI, Wonderware, Ignition) to cloud, BI tools, and reporting systems.':
        'Hubungkan SCADA historian (OSIsoft PI, Wonderware, Ignition) ke cloud, BI tools, dan sistem reporting.',
    'Wrap legacy systems behind modern APIs. No need to rebuild a 20-year-old asset register from scratch.':
        'Bungkus sistem legacy di balik API modern. Tidak perlu rebuild asset register 20 tahun dari awal.',
    'Implement adapters and APIs with automated test coverage and observability.':
        'Implementasi adapter dan API dengan automated test coverage dan observability.',
    'Can you integrate systems we built in-house?': 'Apakah Anda bisa integrasi sistem yang kami build in-house?',
    'Do you handle IT security and identity?': 'Apakah Anda menangani IT security dan identity?',
    'Ready to integrate your systems?': 'Siap mengintegrasikan sistem Anda?',
    'Free initial consultation \u2014 share your stack, our engineering team responds within 24 hours with a phased integration plan that minimises operational risk.':
        'Konsultasi awal gratis - bagikan stack Anda, tim engineer kami merespon dalam 24 jam dengan rencana integrasi berfase yang meminimalkan risiko operasional.',
}

# Apply to all 27 ID pages
ID_PAGES = [5273,5274,5275,5276,5277,5278,5279,5281,5282,5283,5284,5285,5286,5287,5288,5289,5290,5291,5292,5293,5294,5295,5378,5379,5380,5381,5382]
total = 0
for pid in ID_PAGES:
    try:
        r = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}?context=edit&_fields=meta,content', headers=HDRS)
        d = json.loads(urllib.request.urlopen(r, timeout=60).read())
    except: continue
    changes = 0
    payload = {}
    ed = d.get('meta', {}).get('_elementor_data', '')
    if not isinstance(ed, str): ed = json.dumps(ed)
    new_ed = ed
    for en, idt in MEGA_V2.items():
        if en in new_ed:
            new_ed = new_ed.replace(en, idt)
            changes += 1
    content_raw = d.get('content', {}).get('raw', '')
    new_content = content_raw
    for en, idt in MEGA_V2.items():
        if en in new_content:
            new_content = new_content.replace(en, idt)
            changes += 1
    if new_ed != ed or new_content != content_raw:
        if new_ed != ed: payload['meta'] = {'_elementor_data': new_ed}
        if new_content != content_raw: payload['content'] = new_content
        try:
            urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}', data=json.dumps(payload).encode(), method='POST', headers=HDRS), timeout=60).read()
            print(f'  {pid}: +{changes}')
            total += changes
        except Exception as e: print(f'  {pid}: fail {e}')

print(f'\nTotal: {total}')

# Purge
purge = """
$upload = wp_upload_dir();
$log = $upload['basedir']."/purge-mega-v2.txt";
if (file_exists($log)) { if (function_exists('code_snippets')) { code_snippets()->deactivate(5); } return; }
if (class_exists('\\\\Elementor\\\\Plugin')) {
    foreach ([5273,5274,5275,5276,5277,5278,5279,5281,5282,5283,5284,5285,5286,5287,5288,5289,5290,5291,5292,5293,5294,5295,5378,5379,5380,5381,5382] as $pid) {
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
"""
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=json.dumps({'code':purge, 'active':True, 'name':'SX: mega v2 purge'}).encode(), method='POST', headers=HDRS), timeout=60).read()
time.sleep(3)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print('Purged')
