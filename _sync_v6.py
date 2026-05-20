"""V6 — final push for WW Logger + boost MEDs to GOOD."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

V6 = {
    # ===== WW Logger =====
    'Pertambangan Tailings': 'Tailing Pertambangan',
    'F&B Wastewater': 'Air Limbah F&B',
    'Textile Effluent': 'Effluent Tekstil',
    'Hospital Wastewater': 'Air Limbah Rumah Sakit',
    'Sewage Networks': 'Jaringan Sewage',
    'KLHK SPARING Sites': 'Lokasi SPARING KLHK',
    'Industrial Effluent': 'Effluent Industri',
    'Optimize Your Water Management with the Latest Technology': 'Optimasi Manajemen Air Anda dengan Teknologi Terkini',
    'Introducing the latest Wastewater Logger from Suriota, a powerful device that mendukung Modbus RS232, SDI-12, Wi-Fi, and Bluetooth protocols for seamless integration. This logger memungkinkan real-time data monitoring, resource utilization optimization, and anomaly detection with ease.':
        'Memperkenalkan Wastewater Logger terbaru dari Suriota, device powerful yang mendukung protokol Modbus RS232, SDI-12, Wi-Fi, dan Bluetooth untuk integrasi seamless. Logger ini memungkinkan monitoring data real-time, optimasi utilisasi sumber daya, dan deteksi anomali dengan mudah.',
    'With wireless connectivity, you can access and control this device remotely, ensuring more efficient and responsive water management.':
        'Dengan konektivitas wireless, Anda bisa akses dan kontrol device secara remote, memastikan manajemen air lebih efisien dan responsif.',
    'Suriota\u2019s Wastewater Logger V.3 can take your water management to the next level. Increase operational efficiency and ensure environmental compliance with our innovative solution.':
        'Wastewater Logger V.3 dari Suriota dapat membawa manajemen air Anda ke level berikutnya. Tingkatkan efisiensi operasional dan pastikan compliance lingkungan dengan solusi inovatif kami.',
    'Logs pH, TDS, Flow, Pressure, Level via Modbus RS-485 sensor inputs. Configurable channels and sampling intervals.':
        'Log pH, TDS, Flow, Pressure, Level via input sensor Modbus RS-485. Channel dan interval sampling dapat dikonfigurasi.',
    'Cellular 4G LTE for remote sites, WiFi for local network. Auto-failover ensures continuous data upload.':
        'Cellular 4G LTE untuk lokasi remote, WiFi untuk jaringan lokal. Auto-failover memastikan upload data berkelanjutan.',
    'Pre-configured for KLHK SPARING reporting. Compliance-ready effluent data submission per Permen LHK Tidak. 80/2019.':
        'Pre-konfigurasi untuk pelaporan SPARING KLHK. Submission data effluent compliance-ready sesuai Permen LHK No. 80/2019.',
    'Internal Li-ion battery keeps logging during outages. Cloud sync resumes automatically when power/network returns.':
        'Baterai Li-ion internal tetap logging saat outage. Cloud sync resume otomatis saat power/network kembali.',
    'Supports Modbus RS232, SDI-12, Wi-Fi, Bluetooth for diverse sensor integration. Plus onboard temperature & humidity sensors.':
        'Mendukung Modbus RS232, SDI-12, Wi-Fi, Bluetooth untuk integrasi sensor beragam. Plus sensor suhu & kelembaban onboard.',
    'Built-in solar charging support with charging indicator and battery connector. Perfect for remote off-grid sites.':
        'Dukungan solar charging built-in dengan indikator charging dan konektor baterai. Sempurna untuk lokasi remote off-grid.',

    # ===== Boost remaining MEDs =====
    # Automation extra
    'In-house SRT-MGATE-1210 Modbus Gateway bridges legacy RTU/TCP devices to modern MQTT/OPC UA cloud telemetry.':
        'SRT-MGATE-1210 Modbus Gateway in-house menghubungkan device legacy RTU/TCP ke telemetri cloud modern MQTT/OPC UA.',
    'Feasibility \u2192 design \u2192 wiring \u2192 PLC code \u2192 HMI/SCADA \u2192 commissioning \u2192 operator training. One accountable partner, one contract.':
        'Feasibility \u2192 desain \u2192 wiring \u2192 PLC code \u2192 HMI/SCADA \u2192 commissioning \u2192 training operator. Satu mitra bertanggung jawab, satu kontrak.',
    'What communica': 'Komunikasi apa',

    # SURGE-V FAQ + intro
    'Komunikasi apa does the vessel hardware use?': 'Komunikasi apa yang digunakan hardware kapal?',

    # DC chunk
    'best margin for us': 'margin terbaik untuk kami',
    'No handover gap.': 'Tidak ada handover gap.',
    'If you choose to execute, the same team that scoped the plan can implement it. Tidak handover gap.':
        'Jika Anda memilih eksekusi, tim yang sama yang scope rencana bisa mengimplementasi. Tidak ada handover gap.',

    # Common product page footer
    'Industrial Strength Konektivitas': 'Konektivitas Industrial-Strength',
    'Long-Range Wireless': 'Wireless Long-Range',
    'Real-time Tracking': 'Tracking Real-time',
    'Reduce Costs by': 'Kurangi Biaya hingga',
    'Increase Efficiency': 'Tingkatkan Efisiensi',

    # RE remaining
    'Solar PV (PLTS)': 'Solar PV (PLTS)',
    'Hybrid PJU': 'Hybrid PJU',
    'Solar Inverter': 'Solar Inverter',
    'Battery Energy Storage': 'Battery Energy Storage',
    'Net-Metering': 'Net-Metering',
    'PLN compliance': 'Compliance PLN',

    # Generic
    'Tested per IEEE': 'Diuji sesuai IEEE',
    'Compliant with IEC': 'Compliant dengan IEC',
    'compatible with': 'kompatibel dengan',
    'Configurable': 'Dapat dikonfigurasi',
    'Dedicated': 'Dedicated',
    'Pre-configured': 'Pre-konfigurasi',
    'Built-in': 'Built-in',
    'Cellular 4G LTE': 'Cellular 4G LTE',
    'Wi-Fi for local network': 'Wi-Fi untuk jaringan lokal',
    'continuous data upload': 'upload data berkelanjutan',
    'remote off-grid sites': 'lokasi remote off-grid',
    'onboard temperature': 'suhu onboard',
    'humidity sensors': 'sensor kelembaban',

    # PM1611 detailed
    'Smart digital prepaid energi meter built for landlords, sub-meters, and asset operators. Token-based billing, remote control, and tenant-level analytics.':
        'Smart digital prepaid energy meter dibangun untuk landlord, sub-meter, dan asset operator. Billing berbasis token, kontrol remote, dan analytics level-tenant.',
    'memilih PM1611-WD': 'memilih PM1611-WD',
    'Prepaid Token Billing': 'Billing Prepaid Token',
    'Multi-tenant electricity billing with auto-disconnect at zero balance and token-based reload via cashier portal. Per-tenant consumption tracking.':
        'Billing listrik multi-tenant dengan auto-disconnect pada saldo nol dan reload berbasis token via portal kasir. Tracking konsumsi per-tenant.',

    # SPD-T485 detail
    'Maximum Surge Protection. Precision Speed. Compact Design.':
        'Proteksi Surge Maksimum. Kecepatan Presisi. Desain Kompak.',
    'When you depend on industrial RS-485 networks for mission-critical data, surge events can cripple operations.':
        'Saat Anda bergantung pada jaringan RS-485 industri untuk data mission-critical, event surge dapat melumpuhkan operasi.',
    'Designed and certified per IEC 61643-21 / EN IEC 61000-6-4:2019 & EN IEC 61000-6-2:2019.':
        'Dirancang dan disertifikasi sesuai IEC 61643-21 / EN IEC 61000-6-4:2019 & EN IEC 61000-6-2:2019.',

    # SURGE-W extra phrases
    'tantangan manajemen kualitas air': 'tantangan manajemen kualitas air',
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
    for en, idt in V6.items():
        if en in ed:
            ed = ed.replace(en, idt)
            applied += 1
    if applied > 0:
        urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{id_id}', data=json.dumps({'meta':{'_elementor_data':ed}}).encode(), method='POST', headers=HDRS), timeout=60).read()
        print(f'  {id_id}: +{applied}')
        total += applied
print(f'\nV6 total: {total}')

purge = '''
$upload = wp_upload_dir();
$log = $upload['basedir']."/purge-v6.txt";
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
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=json.dumps({'code':purge, 'active':True, 'name':'SX: v6'}).encode(), method='POST', headers=HDRS), timeout=60).read()
time.sleep(3)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print('Done')
