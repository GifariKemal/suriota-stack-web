"""V12 — fix SURGE-V with HTML-wrapped strings."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

V12 = {
    '<strong>Lack of real-time visibility</strong> on vessel location, status, and critical systems.':
        '<strong>Kurangnya visibilitas real-time</strong> pada lokasi kapal, status, dan sistem kritis.',
    '<strong>High and unpredictable fuel costs</strong> that impact your profitability.':
        '<strong>Biaya bahan bakar yang tinggi dan tidak terprediksi</strong> yang berdampak pada profitabilitas Anda.',
    '<strong>Concerns over crew and vessel safety</strong> without proactive monitoring and alerts.':
        '<strong>Kekhawatiran atas keselamatan crew dan kapal</strong> tanpa monitoring proaktif dan alert.',
    '<strong>Manual and time-consuming operational reporting</strong> for compliance and analysis.':
        '<strong>Pelaporan operasional manual dan memakan waktu</strong> untuk compliance dan analisis.',
    'Live vessel positions with speed, heading, and route trail on interactive map. Multi-vessel dashboard view.':
        'Posisi kapal live dengan kecepatan, heading, dan jejak rute di peta interaktif. Tampilan dashboard multi-kapal.',
    'Voyage replay, daily/weekly reports, compliance documentation. Export CSV/PDF for audit and operational review.':
        'Replay voyage, laporan harian/mingguan, dokumentasi compliance. Export CSV/PDF untuk audit dan review operasional.',
    'Coastal 4G LTE with Iridium/Inmarsat satellite failover for offshore voyages. Continuous tracking, even out of cellular range.':
        'Coastal 4G LTE dengan failover satelit Iridium/Inmarsat untuk voyage offshore. Tracking berkelanjutan, bahkan di luar jangkauan cellular.',
    'Digital logbook for crew manifests, cargo loading, fuel logs, maintenance. Replace paper records with audit-ready data.':
        'Logbook digital untuk manifest crew, loading kargo, log bahan bakar, maintenance. Ganti record kertas dengan data audit-ready.',
}

r = urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages/5289?context=edit&_fields=meta', headers=HDRS)
cur = json.loads(urllib.request.urlopen(r, timeout=60).read())
ed = cur['meta']['_elementor_data']
if not isinstance(ed, str): ed = json.dumps(ed)
applied = 0
for en, idt in V12.items():
    if en in ed:
        ed = ed.replace(en, idt)
        applied += 1
        print(f'  matched: {en[:60]}...')
    else:
        print(f'  miss: {en[:60]}...')
if applied > 0:
    urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages/5289', data=json.dumps({'meta':{'_elementor_data':ed}}).encode(), method='POST', headers=HDRS), timeout=60).read()
    print(f'\nV12 SURGE-V: +{applied} applied')

# Purge
purge = '''
$upload = wp_upload_dir();
$log = $upload['basedir']."/purge-v12.txt";
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
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=json.dumps({'code':purge, 'active':True, 'name':'SX: v12'}).encode(), method='POST', headers=HDRS), timeout=60).read()
time.sleep(3)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/id/surge-vessel-tracking-id/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print('Done')
