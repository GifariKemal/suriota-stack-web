"""V9 — exact remaining English on 6 MED pages."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

V9 = {
    # ===== Generic deployed labels =====
    'Where PM1611-WD is deployed': 'Di mana PM1611-WD digunakan',
    'Where SPD-T485-105 is deployed': 'Di mana SPD-T485-105 digunakan',
    'Where Wastewater Logger is deployed': 'Di mana Wastewater Logger digunakan',
    'Where THM-30MD is deployed': 'Di mana THM-30MD digunakan',
    'Where ISO-M485 is deployed': 'Di mana ISO-M485 digunakan',
    'Where SRT-MGATE-1210 is deployed': 'Di mana SRT-MGATE-1210 digunakan',
    'Where SURGE-Energy is deployed': 'Di mana SURGE-Energy digunakan',
    'Where SURGE-Vessel is deployed': 'Di mana SURGE-Vessel digunakan',
    'Where SURGE-Water is deployed': 'Di mana SURGE-Water digunakan',

    # ===== PM1611 =====
    'Smart, Secure, and Efficient Prepaid Energy Management': 'Manajemen Prepaid Energy Cerdas, Aman, dan Efisien',
    'Take full control of your power consumption.': 'Ambil kontrol penuh atas konsumsi daya Anda.',
    'Built-in relay memungkinkan remote service control via WiFi/4G. Tidak site visit needed for activation or disconnection.':
        'Relay built-in memungkinkan kontrol service remote via WiFi/4G. Tanpa kunjungan lokasi untuk aktivasi atau disconnection.',
    'Set peak/off-peak rates, flat tariffs, custom plans. Auto-calculate based on time-of-use schedules per tenant.':
        'Set tarif peak/off-peak, tarif flat, rencana custom. Auto-calculate berdasarkan jadwal time-of-use per tenant.',
    'Our team responds dalam 24 jam dengan checklist site survey dan timeline instalasi.':
        'Tim kami merespon dalam 24 jam dengan checklist site survey dan timeline instalasi.',

    # ===== Automation =====
    'INDUSTRIES WE AUTOMATE': 'INDUSTRI YANG KAMI OTOMATISASI',
    'PLC, SCADA & IIoT integration for Industri 4.0': 'Integrasi PLC, SCADA & IIoT untuk Industri 4.0',
    'tetapi keharusan untuk bertahan dan tumbuh.': 'tetapi keharusan untuk bertahan dan tumbuh.',
    'SURIOTA menyediakaners IoT, SCADA': 'SURIOTA menyediakan IoT, SCADA',
    'With our in-house SURGE platform': 'Dengan platform SURGE in-house kami',
    'kami menyediakan monitoring energi, water analytics, vessel tracking, dan otomasited':
        'kami menyediakan monitoring energi, water analytics, vessel tracking, dan otomasi terintegrasi',
    'Industri 4.0 automation, built for operational scale': 'Otomasi Industri 4.0, dibangun untuk skala operasional',
    'In-house SRT-MGATE-1210 Modbus Gateway bridges legacy RTU/TCP devices to modern MQTT/OPC UA cloud telemetry.':
        'Gateway Modbus SRT-MGATE-1210 in-house menghubungkan device legacy RTU/TCP ke telemetri cloud modern MQTT/OPC UA.',

    # ===== SURGE-V =====
    'High and unpredictable fuel costs that impact your profitability.':
        'Biaya bahan bakar tinggi dan tidak terprediksi yang berdampak pada profitabilitas Anda.',
    'Concerns over crew and vessel safety without proactive monitoring and alerts.':
        'Kekhawatiran atas keselamatan crew dan kapal tanpa monitoring proaktif dan alert.',
    'Introducing SURGE-Vessel Tracking: The Smart Maritim Solution':
        'Memperkenalkan SURGE-Vessel Tracking: Solusi Maritim Cerdas',
    'Define operation zones, restricted areas, route corridors. Instant alerts on zone entry/exit, deviation, speed breach.':
        'Definisikan zona operasi, area terbatas, koridor rute. Alert instant saat masuk/keluar zona, deviasi, pelanggaran kecepatan.',

    # ===== SPD =====
    'Certified Protection for High-Speed RS-485 Komunikasi': 'Proteksi Bersertifikat untuk Komunikasi RS-485 High-Speed',
    'the first di Indonesia certifi': 'pertama di Indonesia bersertifik',
    'Sub-nanosecond clamp protects sensitive RS-485 transceivers before damaging energi reaches the line driver.':
        'Clamp sub-nanodetik melindungi transceiver RS-485 sensitif sebelum energi merusak mencapai line driver.',
    'Compliant with IEC 61643-21 Class III data line surge protection.':
        'Compliant dengan proteksi surge data line Class III IEC 61643-21.',
    '35mm DIN rail mountable, screw terminals for in/out, ground bonding terminal. Compact form for crowded panels.':
        'DIN rail mountable 35mm, terminal screw untuk in/out, terminal ground bonding. Bentuk kompak untuk panel padat.',
    'Two-step sequencing barrier preserves device lifespan and enhances surge suppression performance.':
        'Sequencing barrier dua-tahap menjaga lifespan device dan meningkatkan performa surge suppression.',
    'Industri-leading design.': 'Desain industri-terdepan.',

    # ===== WW =====
    'Tingkatkan efisiensi operasional dan pastikan compliance lingkungano':
        'Tingkatkan efisiensi operasional dan pastikan compliance lingkungan',
    'Logs pH, TDS, Flow, Pressure, Level via Modbus RS-485 sensor inputs. Dapat dikonfigurasi channels and sampling intervals.':
        'Log pH, TDS, Flow, Pressure, Level via input sensor Modbus RS-485. Channel dan interval sampling dapat dikonfigurasi.',
    'Cellular 4G LTE for remote sites, WiFi for local network.': 'Cellular 4G LTE untuk lokasi remote, WiFi untuk jaringan lokal.',
    'Auto-failover ensures upload data berkelanjutan.': 'Auto-failover memastikan upload data berkelanjutan.',
    'Pre-konfigurasi for KLHK SPARING reporting.': 'Pre-konfigurasi untuk pelaporan SPARING KLHK.',
    'Compliance-ready effluent data submission per Permen LHK Tidak. 80/2019.':
        'Submission data effluent compliance-ready sesuai Permen LHK No. 80/2019.',
    'Supports Modbus RS232, SDI-12, Wi-Fi, Bluetooth for diverse sensor integration. Plus suhu onboard & sensor kelembaban.':
        'Mendukung Modbus RS232, SDI-12, Wi-Fi, Bluetooth untuk integrasi sensor beragam. Plus sensor suhu & kelembaban onboard.',
    'Built-in solar charging support with charging indicator and battery connector.':
        'Dukungan solar charging built-in dengan indikator charging dan konektor baterai.',
    'Our team responds dalam 24 jam dengan parameter mapping dan workflow pelaporan.':
        'Tim kami merespon dalam 24 jam dengan parameter mapping dan workflow pelaporan.',

    # ===== Internship =====
    'Manual & automated testing for SURplatform SURGE.': 'Testing manual & otomatis untuk platform SURGE.',
    'Hands-on internship for real-world experience in IoT Industri, automation, and renewable energi projects.':
        'Magang langsung untuk pengalaman dunia nyata dalam proyek IoT Industri, otomasi, dan renewable energi.',
    'Kirim your CV & documents to admin@suriota.com dengan subjek:':
        'Kirim CV & dokumen Anda ke admin@suriota.com dengan subjek:',

    # ===== Common remaining =====
    'no third-party gateway lock-in.': 'tanpa lock-in gateway third-party.',
    'CONNECT WITH US': 'HUBUNGI KAMI',
    'STAY UPDATED': 'TETAP UPDATE',
}

PAGES = [
    (12,5273),(29,5274),(839,5275),(1127,5276),(945,5277),(5039,5278),
    (5260,5279),(37,5281),(35,5282),(39,5283),(5029,5284),(5037,5285),
    (5033,5286),(934,5287),(1542,5288),(1546,5289),(1547,5290),
    (1740,5291),(1741,5292),(1742,5293),(1765,5294),(929,5295),
]

# Also update permanent snippets if they have "CONNECT WITH US" etc.
print('Updating snippets...')
r = urllib.request.Request('https://suriota.com/wp-json/wp/v2/elementor_snippet?per_page=50&_fields=id&status=publish', headers=HDRS)
snips = json.loads(urllib.request.urlopen(r).read())
for s in snips:
    sid = s['id']
    try:
        rs = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/elementor_snippet/{sid}?context=edit&_fields=meta', headers=HDRS)
        sd = json.loads(urllib.request.urlopen(rs, timeout=30).read())
        code = sd.get('meta', {}).get('_elementor_code', '')
        if not code: continue
        new_code = code
        for en, idt in V9.items():
            if en in new_code:
                new_code = new_code.replace(en, idt)
        if new_code != code:
            urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/elementor_snippet/{sid}', data=json.dumps({'meta':{'_elementor_code':new_code}}).encode(), method='POST', headers=HDRS), timeout=60).read()
            print(f'  snippet {sid}: updated')
    except: pass

print('\nUpdating pages...')
total = 0
for en_id, id_id in PAGES:
    r = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{id_id}?context=edit&_fields=meta', headers=HDRS)
    cur = json.loads(urllib.request.urlopen(r, timeout=60).read())
    ed = cur['meta']['_elementor_data']
    if not isinstance(ed, str): ed = json.dumps(ed)
    applied = 0
    for en, idt in V9.items():
        if en in ed:
            ed = ed.replace(en, idt)
            applied += 1
    if applied > 0:
        urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{id_id}', data=json.dumps({'meta':{'_elementor_data':ed}}).encode(), method='POST', headers=HDRS), timeout=60).read()
        print(f'  {id_id}: +{applied}')
        total += applied
print(f'\nV9 total: {total}')

purge = '''
$upload = wp_upload_dir();
$log = $upload['basedir']."/purge-v9.txt";
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
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=json.dumps({'code':purge, 'active':True, 'name':'SX: v9'}).encode(), method='POST', headers=HDRS), timeout=60).read()
time.sleep(3)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print('Done')
