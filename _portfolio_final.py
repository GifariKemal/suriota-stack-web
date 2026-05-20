"""Pinpoint fixes for portfolio + project descriptions."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

FIXES = {
    'Tidak Klien Proyek Tahun': 'No Klien Proyek Tahun',
    'Tidak</th>': 'No</th>',
    '<th>Tidak</th>': '<th>No</th>',

    # HTML-encoded versions
    'SURGE Energy Mapping (HVAC Monitoring &amp; Management)': 'SURGE Energy Mapping (Monitoring &amp; Manajemen HVAC)',
    'SURGE Energy Mapping (Electrical Power Monitoring &amp; Control)': 'SURGE Energy Mapping (Monitoring &amp; Kontrol Daya Listrik)',
    'SURGE Water Analytics (Water Quality &amp; Flowmeter Monitoring)': 'SURGE Water Analytics (Monitoring Kualitas Air &amp; Flowmeter)',
    'Flowmeter Discharge Monitoring &amp; Control System Prototype': 'Prototype Sistem Monitoring &amp; Kontrol Discharge Flowmeter',
    'NPK Hardware Monitoring &amp; Control Prototype': 'Prototype Hardware Monitoring &amp; Kontrol NPK',
    'KLHK Server Migration &amp; SPARING IoT Dashboard Development': 'Migrasi Server KLHK &amp; Pengembangan Dashboard IoT SPARING',
    'Replacement &amp; Repair of SPARING Sensors': 'Penggantian &amp; Perbaikan Sensor SPARING',
    'pH, Temp, Humidity Monitoring &amp; Soil Control IoT System': 'Sistem IoT Monitoring pH, Suhu, Kelembaban &amp; Kontrol Tanah',
    'Smart NPK &amp; Plantation Soil Monitoring IoT System': 'Sistem IoT Smart NPK &amp; Monitoring Tanah Perkebunan',
    'Plantation pH, Temp, Humidity Monitoring &amp; Soil Control IoT System': 'Sistem IoT Monitoring pH, Suhu, Kelembaban &amp; Kontrol Tanah Perkebunan',
    'Automatic IoT-Based Mini Capacitor Bank System': 'Sistem Mini Capacitor Bank Otomatis Berbasis IoT',
    'Engineering Calculation Flow Rate': 'Kalkulasi Engineering Flow Rate',
    'Engineering Calculation Smoke Detector': 'Kalkulasi Engineering Smoke Detector',
    'Load Suppression &amp; Electrical Power Calculations': 'Load Suppression &amp; Kalkulasi Daya Listrik',
    'Procurement of Genset Sensors': 'Procurement Sensor Genset',
    'Webmail Maintenance': 'Maintenance Webmail',
    'Wedding Invitation Hardcopy': 'Undangan Pernikahan Hardcopy',
    'Anshun Sticker Design': 'Desain Stiker Anshun',
    'MnS Logo Design': 'Desain Logo MnS',
    'Jamu Logo and Product Design': 'Logo Jamu dan Desain Produk',
    'Company Product Logo, Icon, PrintUP Design': 'Logo Produk Perusahaan, Ikon, Desain PrintUP',
    'Design CAD Water Treatment': 'Desain CAD Water Treatment',
    'Design CAD Tempat Pembuangan Sampah': 'Desain CAD Tempat Pembuangan Sampah',
    'Design CAD Canopy POS Security': 'Desain CAD Canopy POS Security',
    'Module Absensi IoT': 'Modul Absensi IoT',
    'School Website': 'Website Sekolah',
    'Object Yolo AI': 'Object Detection Yolo AI',
    'Design CAD SLD Penang Chendul': 'Desain CAD SLD Penang Chendul',
    'Electrical Wiring &amp; Commissioning': 'Wiring &amp; Commissioning Electrical',
    'IoT Robot Tank Prototype': 'Prototype Robot Tank IoT',
    'Project Archive': 'Arsip Proyek',
    '2D Splingker P&amp;ID': '2D Splingker P&amp;ID',  # keep technical
}

ID_PAGES = [5275, 5273, 5274, 5276, 5277, 5278, 5279, 5281, 5282, 5283, 5284, 5285, 5286, 5287, 5288, 5289, 5290, 5291, 5292, 5293, 5294, 5295, 5378, 5379, 5380, 5381, 5382]
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
    for en, idt in FIXES.items():
        if en in new_ed:
            new_ed = new_ed.replace(en, idt)
            changes += 1
    content_raw = d.get('content', {}).get('raw', '')
    new_content = content_raw
    for en, idt in FIXES.items():
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
        except Exception as e:
            print(f'  {pid}: push fail {e}')

print(f'\nTotal: {total}')

# Purge
purge = """
$upload = wp_upload_dir();
$log = $upload['basedir']."/purge-pf-final.txt";
if (file_exists($log)) { if (function_exists('code_snippets')) { code_snippets()->deactivate(5); } return; }
if (class_exists('\\\\Elementor\\\\Plugin')) {
    foreach ([5275,5273,5274,5276,5277,5278,5279,5281,5282,5283,5284,5285,5286,5287,5288,5289,5290,5291,5292,5293,5294,5295,5378,5379,5380,5381,5382] as $pid) {
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
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=json.dumps({'code':purge, 'active':True, 'name':'SX: pf final'}).encode(), method='POST', headers=HDRS), timeout=60).read()
time.sleep(3)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/id/portfolio-id/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print('Purged')
