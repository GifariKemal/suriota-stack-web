"""V11 — final tiny push for SURGE-V"""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

V11 = {
    'Define operation zones, restricted areas, and route corridors on the map.':
        'Tetapkan zona operasi, area terbatas, dan koridor rute di peta.',
    'Engine hours, fuel consumption, RPM, and alarms are integrated via NMEA-2000 or Modbus connections to the vessel ECU.':
        'Jam mesin, konsumsi bahan bakar, RPM, dan alarm terintegrasi via koneksi NMEA-2000 atau Modbus ke vessel ECU.',
    'Monitor engine hours, fuel consumption, RPM, alarms via NMEA-2000 / Modbus integration.':
        'Monitor jam mesin, konsumsi bahan bakar, RPM, alarm via integrasi NMEA-2000 / Modbus.',
    'Reduce idle waste & theft.': 'Kurangi waste idle & pencurian.',
    'crew & cargo logbook': 'logbook crew & kargo',
    'Crew & Cargo Logbook': 'Logbook Crew & Kargo',
    'Geofencing & Alerts': 'Geofencing & Alert',
    'Engine & Fuel Telemetry': 'Telemetri Mesin & Bahan Bakar',
    'Historical Analytics & Reports': 'Analitik & Laporan Historis',
}

r = urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages/5289?context=edit&_fields=meta', headers=HDRS)
cur = json.loads(urllib.request.urlopen(r, timeout=60).read())
ed = cur['meta']['_elementor_data']
if not isinstance(ed, str): ed = json.dumps(ed)
applied = 0
for en, idt in V11.items():
    if en in ed:
        ed = ed.replace(en, idt)
        applied += 1
if applied > 0:
    urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages/5289', data=json.dumps({'meta':{'_elementor_data':ed}}).encode(), method='POST', headers=HDRS), timeout=60).read()
    print(f'V11 SURGE-V: +{applied}')

# Purge
purge = '''
$upload = wp_upload_dir();
$log = $upload['basedir']."/purge-v11.txt";
if (file_exists($log)) { if (function_exists('code_snippets')) { code_snippets()->deactivate(5); } return; }
if (class_exists('\\\\Elementor\\\\Plugin')) {
    $f = \\Elementor\\Core\\Files\\CSS\\Post::create(5289);
    if ($f) { $f->delete(); $f->update(); }
    \\Elementor\\Plugin::instance()->files_manager->clear_cache();
}
if (class_exists('WPO_Page_Cache')) WPO_Page_Cache::instance()->purge();
if (class_exists('WP_Optimize_Minify_Cache_Functions')) \\WP_Optimize_Minify_Cache_Functions::purge();
wp_cache_flush();
file_put_contents($log, 'done');
if (function_exists('code_snippets')) { code_snippets()->deactivate(5); }
'''
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=json.dumps({'code':purge, 'active':True, 'name':'SX: v11'}).encode(), method='POST', headers=HDRS), timeout=60).read()
time.sleep(3)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/id/surge-vessel-tracking-id/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print('Done')
