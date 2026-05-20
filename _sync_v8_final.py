"""V8 — apostrophe variants + exact remaining English chunks."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

V8 = {
    # ===== Internship =====
    'Hands-on internship for real-world experience in IoT Industri, automation, and renewable energi projects.':
        'Magang langsung untuk pengalaman dunia nyata dalam proyek IoT Industri, otomasi, dan renewable energi.',

    # ===== Automation (with curly apostrophe ’) =====
    'SURIOTA\u2019s team designs and implements automation systems from small to large scale using Siemens S7, Omron, Schneider, and IEC 61131-3 compl':
        'Tim SURIOTA merancang dan mengimplementasi sistem otomasi dari skala kecil hingga besar menggunakan Siemens S7, Omron, Schneider, dan compliant IEC 61131-3',
    'SURIOTA\u2019s team designs and implements automation systems from small to large scale':
        'Tim SURIOTA merancang dan mengimplementasi sistem otomasi dari skala kecil hingga besar',
    'using Siemens S7, Omron, Schneider, and IEC 61131-3 compl':
        'menggunakan Siemens S7, Omron, Schneider, dan compliant IEC 61131-3',
    'We integrate Siemens, Schneider, Mitsubishi, Omron, Allen-Bradley - picking the right controller for your plant, not for our supply chain.':
        'Kami integrasi Siemens, Schneider, Mitsubishi, Omron, Allen-Bradley - pilih controller yang tepat untuk plant Anda, bukan untuk supply chain kami.',
    'OT/IT network segregation, firewall zones, role-based HMI access, and encrypted telemetry per IEC 62443. Reduce attack surface from day one.':
        'Segregasi jaringan OT/IT, firewall zone, akses HMI role-based, dan telemetri terenkripsi sesuai IEC 62443. Kurangi attack surface sejak hari pertama.',
    'Integrated SaaS IIoT solution: Energy Mapping, Water Analytics, and Vessel Tracking with web & mobile interfaces.':
        'Solusi SaaS IIoT terintegrasi: Energy Mapping, Water Analytics, dan Vessel Tracking dengan interface web & mobile.',

    # ===== SURGE-V =====
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

    # ===== ISO-M485 (curly apostrophe) =====
    'When your operations depend on fast, stable, and secure data communication, you can\u2019t afford downtime or interference. ISO-M485 Series diran':
        'Saat operasi Anda bergantung pada komunikasi data yang cepat, stabil, dan aman, Anda tidak boleh ada downtime atau interferensi. ISO-M485 Series diran',
    'you can\u2019t afford downtime or interference':
        'Anda tidak boleh ada downtime atau interferensi',
    'Optocoupler isolation between RS-485 ports protects upstream PLC/SCADA from ground loops and field-side faults.':
        'Isolasi optocoupler antar port RS-485 melindungi PLC/SCADA upstream dari ground loop dan fault field-side.',
    'Integrated TVS diodes + gas discharge tubes guard against lightning-induced and switching transients on outdoor cables.':
        'TVS diode + gas discharge tube terintegrasi melindungi dari transient akibat petir dan switching pada kabel outdoor.',
    '-40\u00b0C to +85\u00b0C operation. DIN rail mountable. Rated for continuous operation in harsh field cabinets.':
        'Operasi -40\u00b0C hingga +85\u00b0C. DIN rail mountable. Rated untuk operasi berkelanjutan di field cabinet keras.',
    'Accepts 7-15VDC or 9-24VDC supply variants for easy integration with industrial 12V or 24V control panels.':
        'Menerima supply 7-15VDC atau 9-24VDC untuk integrasi mudah dengan panel kontrol industri 12V atau 24V.',
    'Supports up to 500 kbps data rate (within distance limits) for high-throughput SCADA and PLC networks.':
        'Mendukung data rate hingga 500 kbps (dalam batas jarak) untuk jaringan SCADA dan PLC high-throughput.',

    # ===== PM1611 =====
    'Local LCD shows balance and consumption. WhatsApp/SMS notifications on low balance, anomalies, and top-ups.':
        'LCD lokal menampilkan saldo dan konsumsi. Notifikasi WhatsApp/SMS saat saldo rendah, anomali, dan top-up.',
    'Review up to 6 days of detailed energi usage per tenant. Identify abnormal consumption and resolve disputes with data.':
        'Review hingga 6 hari penggunaan energi detail per tenant. Identifikasi konsumsi abnormal dan selesaikan sengketa dengan data.',
    'Configure and monitor remotely via web interface using Blynk or MQTT protocol. RTC with NTP sync ensures accurate billing time.':
        'Konfigurasi dan monitor remote via interface web menggunakan protokol Blynk atau MQTT. RTC dengan sync NTP memastikan waktu billing akurat.',

    # ===== WW (curly apostrophe) =====
    'Suriota\u2019s Wastewater Logger V.3 can take your water management to the next level. Increase operational efficiency and ensure environmental c':
        'Wastewater Logger V.3 dari Suriota dapat membawa manajemen air Anda ke level berikutnya. Tingkatkan efisiensi operasional dan pastikan compliance lingkungan',
    'Suriota\u2019s Wastewater Logger V.3 can take your water management to the next level.':
        'Wastewater Logger V.3 dari Suriota dapat membawa manajemen air Anda ke level berikutnya.',
    'Increase operational efficiency and ensure environmental c':
        'Tingkatkan efisiensi operasional dan pastikan compliance lingkungan',
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
    for en, idt in V8.items():
        if en in ed:
            ed = ed.replace(en, idt)
            applied += 1
    if applied > 0:
        urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{id_id}', data=json.dumps({'meta':{'_elementor_data':ed}}).encode(), method='POST', headers=HDRS), timeout=60).read()
        print(f'  {id_id}: +{applied}')
        total += applied
print(f'\nV8 total: {total}')

purge = '''
$upload = wp_upload_dir();
$log = $upload['basedir']."/purge-v8.txt";
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
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=json.dumps({'code':purge, 'active':True, 'name':'SX: v8'}).encode(), method='POST', headers=HDRS), timeout=60).read()
time.sleep(3)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print('Done')
