"""Final fix — handle JSON-escaped em-dash + remaining legal translations."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

# Use raw backslash-u-2014 (6 chars literal) to match JSON-escaped em-dash in stored string
# r"\u2014" gives backslash-u-2-0-1-4 (6 chars literal)

FIX = {
    # First: remove ALL JSON-escaped em-dashes
    r" \u2014 ": " - ",
    r"\u2014": "-",

    # Then translate remaining English using HYPHEN
    'How PT Surya Inovasi Prioritas (SURIOTA) collects, uses, and protects your personal data. This policy is aligned with Indonesia\\u2019s Personal Data Protection Law (UU PDP No.27/2022)':
        'Bagaimana PT Surya Inovasi Prioritas (SURIOTA) mengumpulkan, menggunakan, dan melindungi data pribadi Anda. Kebijakan ini selaras dengan Undang-Undang Perlindungan Data Pribadi Indonesia (UU PDP No.27/2022)',
    'PT Surya Inovasi Prioritas (\\u201cSURIOTA\\u201d, \\u201cwe\\u201d, \\u201cus\\u201d, or \\u201cour\\u201d) respects your privacy and is committed to protecting your personal data.':
        'PT Surya Inovasi Prioritas (\\u201cSURIOTA\\u201d, \\u201ckami\\u201d, \\u201cmilik kami\\u201d) menghormati privasi Anda dan berkomitmen melindungi data pribadi Anda.',
    'Account credentials: if you create an account on the SURGE platform, we collect your username, hashed password, and authentication tokens.':
        'Kredensial akun: jika Anda membuat akun di platform SURGE, kami mengumpulkan username, password ter-hash, dan token autentikasi Anda.',
    'Correspondence: emails, WhatsApp messages, and call logs you exchange with our team.':
        'Korespondensi: email, pesan WhatsApp, dan log panggilan yang Anda tukarkan dengan tim kami.',
    'Telemetry from products: for IoT deployments using the SURGE platform, we collect device identifiers, sensor readings, geolocation (when consented), and event logs strictly for the':
        'Telemetri dari produk: untuk deployment IoT menggunakan platform SURGE, kami mengumpulkan identifier device, pembacaan sensor, geolocation (saat disetujui), dan log event semata untuk',
    'Marketing communications - only with your opt-in consent for the newsletter. You may unsubscribe at any time.':
        'Komunikasi marketing - hanya dengan persetujuan opt-in Anda untuk newsletter. Anda dapat unsubscribe kapan saja.',
    'Contract performance - to fulfil engagement and service agreements.':
        'Pelaksanaan kontrak - untuk memenuhi perjanjian engagement dan layanan.',
    'Legitimate interests - to operate our business, secure our services, and develop our products.':
        'Kepentingan sah - untuk mengoperasikan bisnis kami, mengamankan layanan kami, dan mengembangkan produk kami.',
    'Consent - for marketing and optional cookies. You may withdraw consent at any time.':
        'Persetujuan - untuk marketing dan cookies opsional. Anda dapat menarik persetujuan kapan saja.',
    'Legal obligation - to comply with tax, accounting, and regulatory requirements.':
        'Kewajiban hukum - untuk mematuhi requirement pajak, akuntansi, dan regulasi.',
    'Service providers processing data on our behalf (cloud hosting, email delivery, analytics, payment) under written data-processing agreements.':
        'Penyedia layanan yang memproses data atas nama kami (cloud hosting, email delivery, analytics, payment) berdasarkan perjanjian pemrosesan data tertulis.',
    'Successor entities in the event of merger, acquisition, or asset transfer, with continuity of this Policy\\u2019s protections.':
        'Entitas penerus dalam hal merger, akuisisi, atau transfer aset, dengan kelanjutan perlindungan Kebijakan ini.',

    # AI
    'Production-grade AI for industrial use cases. Predictive maintenance, computer vision QC, anomaly detection - built on your data, deployed on your terms.':
        'AI grade produksi untuk use case industri. Predictive maintenance, computer vision QC, deteksi anomali - dibangun di atas data Anda, di-deploy sesuai term Anda.',
    'Many industrial AI proyek die in POC. SURIOTA treats AI like any other engineering discipline - with version control, observability, model registries, and SLA. We pick high-ROI use cases, train on you':
        'Banyak proyek AI industri mati di POC. SURIOTA memperlakukan AI seperti disiplin engineering lainnya - dengan version control, observability, model registry, dan SLA. Kami pilih use case ROI-tinggi, train pada',
    'Edge-capable, retrainable, and governed - we build AI you can audit and trust.':
        'Edge-capable, retrainable, dan ter-governance - kami build AI yang bisa Anda audit dan percaya.',
    'Free initial consultation - share your data and use case, our ML team responds within 24 hours with a feasibility check termasuk data sufficiency, baseline, and target metrics.':
        'Konsultasi awal gratis - bagikan data dan use case Anda, tim ML kami merespon dalam 24 jam dengan feasibility check termasuk kecukupan data, baseline, dan target metrik.',

    # SysInt
    'Most industrial operations run a patchwork of vendor systems: PLCs from one brand, SCADA from another, an ERP that does not talk to either. SURIOTA designs integration architectures - data buses, APIs':
        'Sebagian besar operasi industri menjalankan campuran sistem vendor: PLC dari satu brand, SCADA dari brand lain, ERP yang tidak terhubung keduanya. SURIOTA merancang arsitektur integrasi - data bus, API',
    'Free initial consultation - share your stack, our engineering team responds within 24 hours with a phased integration plan that minimises operational risk.':
        'Konsultasi awal gratis - bagikan stack Anda, tim engineer kami merespon dalam 24 jam dengan rencana integrasi berfase yang meminimalkan risiko operasional.',
}

# Apply
PAGES = [5273,5274,5275,5276,5277,5278,5279,5281,5282,5283,5284,5285,5286,5287,5288,5289,5290,5291,5292,5293,5294,5295,5378,5379,5380,5381,5382]
total = 0
for pid in PAGES:
    try:
        r = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}?context=edit&_fields=meta,content', headers=HDRS)
        d = json.loads(urllib.request.urlopen(r, timeout=60).read())
    except: continue
    changes = 0
    payload = {}
    # Work directly with the JSON-encoded string (which has \u2014 as 6 chars)
    ed_raw = d.get('meta', {}).get('_elementor_data', '')
    if not isinstance(ed_raw, str):
        ed_raw = json.dumps(ed_raw)
    new_ed = ed_raw
    for en, idt in FIX.items():
        if en in new_ed:
            new_ed = new_ed.replace(en, idt)
            changes += 1
    content_raw = d.get('content', {}).get('raw', '')
    new_content = content_raw
    for en, idt in FIX.items():
        if en in new_content:
            new_content = new_content.replace(en, idt)
            changes += 1
    if new_ed != ed_raw or new_content != content_raw:
        if new_ed != ed_raw: payload['meta'] = {'_elementor_data': new_ed}
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
$log = $upload['basedir']."/purge-em-final.txt";
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
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=json.dumps({'code':purge, 'active':True, 'name':'SX: em final'}).encode(), method='POST', headers=HDRS), timeout=60).read()
time.sleep(3)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print('Purged')
