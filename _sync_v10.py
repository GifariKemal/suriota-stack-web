"""V10 — final micro-push for SURGE-V + ISO-M485 to GOOD."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

V10 = {
    # SURGE-V remaining
    'Lack of real-time visibility on vessel location, status, and critical systems.':
        'Kurangnya visibilitas real-time pada lokasi kapal, status, dan sistem kritis.',
    'High and unpredictable fuel costs that impact your profitability.':
        'Biaya bahan bakar yang tinggi dan tidak terprediksi berdampak pada profitabilitas Anda.',
    'Concerns over crew and vessel safety without proactive monitoring and alerts.':
        'Kekhawatiran atas keselamatan crew dan kapal tanpa monitoring proaktif dan alert.',
    'Manual and time-consuming operational reporting for compliance and analysis.':
        'Pelaporan operasional manual dan memakan waktu untuk compliance dan analisis.',
    'Live vessel positions with speed, heading, and route trail on interactive map. Multi-vessel dashboard view.':
        'Posisi kapal live dengan kecepatan, heading, dan jejak rute di peta interaktif. Tampilan dashboard multi-kapal.',
    'Define operation zones, restricted areas, route corridors. Instant alerts on zone entry/exit, deviation, speed breach.':
        'Tetapkan zona operasi, area terbatas, koridor rute. Alert instan saat masuk/keluar zona, deviasi, pelanggaran kecepatan.',
    'Voyage replay, daily/weekly reports, compliance documentation. Export CSV/PDF for audit and operational review.':
        'Replay voyage, laporan harian/mingguan, dokumentasi compliance. Export CSV/PDF untuk audit dan review operasional.',
    'Coastal 4G LTE with Iridium/Inmarsat satellite failover for offshore voyages. Continuous tracking, even out of cellular range.':
        'Coastal 4G LTE dengan failover satelit Iridium/Inmarsat untuk voyage offshore. Tracking berkelanjutan, bahkan di luar jangkauan cellular.',
    'Digital logbook for crew manifests, cargo loading, fuel logs, maintenance. Replace paper records with audit-ready data.':
        'Logbook digital untuk manifest crew, loading kargo, log bahan bakar, maintenance. Ganti record kertas dengan data audit-ready.',

    # ISO-M485 remaining
    'Reliable RS-485 Komunikasi, Reinforced with Isolation & Surge Protection':
        'Komunikasi RS-485 Andal, Diperkuat dengan Isolasi & Proteksi Surge',
    'When your operations depend on fast, stable, and secure data communication, you can\u2019t afford downtime or interference.':
        'Saat operasi Anda bergantung pada komunikasi data cepat, stabil, dan aman, Anda tidak boleh ada downtime atau interferensi.',
    'ISO-M485 Series dirancang untuk': 'ISO-M485 Series dirancang untuk',
    'Optocoupler isolation between RS-485 ports protects upstream PLC/SCADA from ground loops and field-side faults.':
        'Isolasi optocoupler antar port RS-485 melindungi PLC/SCADA upstream dari ground loop dan fault field-side.',
    'Integrated TVS diodes + gas discharge tubes guard against lightning-induced and switching transients on outdoor cables.':
        'TVS diode + gas discharge tube terintegrasi melindungi dari transient akibat petir dan switching pada kabel outdoor.',
    'Extended driver capacity mendukung up to 256 nodes per segment. Auto direction control simplifies wiring.':
        'Kapasitas driver yang diperpanjang mendukung hingga 256 node per segmen. Kontrol arah otomatis menyederhanakan wiring.',
    '-40\u00b0C to +85\u00b0C operation. DIN rail mountable. Rated for continuous operation in harsh field cabinets.':
        'Operasi -40\u00b0C hingga +85\u00b0C. DIN rail mountable. Rated untuk operasi berkelanjutan di field cabinet keras.',
    'Accepts 7-15VDC or 9-24VDC supply variants for easy integration with industrial 12V or 24V control panels.':
        'Menerima supply 7-15VDC atau 9-24VDC untuk integrasi mudah dengan panel kontrol industri 12V atau 24V.',
    'Supports up to 500 kbps data rate (within distance limits) for high-throughput SCADA and PLC networks.':
        'Mendukung data rate hingga 500 kbps (dalam batas jarak) untuk jaringan SCADA dan PLC high-throughput.',
}

# Apply only to specific pages
TARGETS = [(1546, 5289), (1740, 5291)]
total = 0
for _, id_id in TARGETS:
    r = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{id_id}?context=edit&_fields=meta', headers=HDRS)
    cur = json.loads(urllib.request.urlopen(r, timeout=60).read())
    ed = cur['meta']['_elementor_data']
    if not isinstance(ed, str): ed = json.dumps(ed)
    applied = 0
    for en, idt in V10.items():
        if en in ed:
            ed = ed.replace(en, idt)
            applied += 1
    if applied > 0:
        urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{id_id}', data=json.dumps({'meta':{'_elementor_data':ed}}).encode(), method='POST', headers=HDRS), timeout=60).read()
        print(f'  {id_id}: +{applied}')
        total += applied

# Purge
purge = '''
$upload = wp_upload_dir();
$log = $upload['basedir']."/purge-v10.txt";
if (file_exists($log)) { if (function_exists('code_snippets')) { code_snippets()->deactivate(5); } return; }
if (class_exists('\\\\Elementor\\\\Plugin')) {
    foreach ([5289, 5291] as $pid) {
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
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=json.dumps({'code':purge, 'active':True, 'name':'SX: v10'}).encode(), method='POST', headers=HDRS), timeout=60).read()
time.sleep(3)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print(f'V10 total: {total} | Done')
