"""Universal em-dash fix - handle \u2014, &mdash;, AND raw em-dash variants."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

# Translation patterns base — we'll generate 3 variants of each for em-dash
BASE_TRANS = {
    # Privacy
    'How PT Surya Inovasi Prioritas (SURIOTA) collects, uses, and protects your personal data.':
        'Bagaimana PT Surya Inovasi Prioritas (SURIOTA) mengumpulkan, menggunakan, dan melindungi data pribadi Anda.',
    'PT Surya Inovasi Prioritas ("SURIOTA", "we", "us", or "our") respects your privacy and is committed to protecting your personal data.':
        'PT Surya Inovasi Prioritas ("SURIOTA", "kami") menghormati privasi Anda dan berkomitmen melindungi data pribadi Anda.',
    'Account credentials: if you create an account on the SURGE platform, we collect your username, hashed password, and authentication tokens.':
        'Kredensial akun: jika Anda membuat akun di platform SURGE, kami mengumpulkan username, password ter-hash, dan token autentikasi Anda.',
    'Correspondence: emails, WhatsApp messages, and call logs you exchange with our team.':
        'Korespondensi: email, pesan WhatsApp, dan log panggilan yang Anda tukarkan dengan tim kami.',
    'Marketing communications EM only with your opt-in consent for the newsletter. You may unsubscribe at any time.':
        'Komunikasi marketing EM hanya dengan persetujuan opt-in Anda untuk newsletter. Anda dapat unsubscribe kapan saja.',
    'Contract performance EM to fulfil engagement and service agreements.':
        'Pelaksanaan kontrak EM untuk memenuhi perjanjian engagement dan layanan.',
    'Legitimate interests EM to operate our business, secure our services, and develop our products.':
        'Kepentingan sah EM untuk mengoperasikan bisnis kami, mengamankan layanan kami, dan mengembangkan produk kami.',
    'Consent EM for marketing and optional cookies. You may withdraw consent at any time.':
        'Persetujuan EM untuk marketing dan cookies opsional. Anda dapat menarik persetujuan kapan saja.',
    'Legal obligation EM to comply with tax, accounting, and regulatory requirements.':
        'Kewajiban hukum EM untuk mematuhi requirement pajak, akuntansi, dan regulasi.',
    'Service providers processing data on our behalf (cloud hosting, email delivery, analytics, payment) under written data-processing agreements.':
        'Penyedia layanan yang memproses data atas nama kami (cloud hosting, email delivery, analytics, payment) berdasarkan perjanjian pemrosesan data tertulis.',
    "Successor entities in the event of merger, acquisition, or asset transfer, with continuity of this Policy's protections.":
        'Entitas penerus dalam hal merger, akuisisi, atau transfer aset, dengan kelanjutan perlindungan Kebijakan ini.',

    # AI
    'Production-grade AI for industrial use cases. Predictive maintenance, computer vision QC, anomaly detection EM built on your data, deployed on your terms.':
        'AI grade produksi untuk use case industri. Predictive maintenance, computer vision QC, deteksi anomali EM dibangun di atas data Anda, di-deploy sesuai term Anda.',
    'Many industrial AI proyek die in POC. SURIOTA treats AI like any other engineering discipline EM with version control, observability, model registries, and SLA.':
        'Banyak proyek AI industri mati di POC. SURIOTA memperlakukan AI seperti disiplin engineering lainnya EM dengan version control, observability, model registry, dan SLA.',
    'Edge-capable, retrainable, and governed EM we build AI you can audit and trust.':
        'Edge-capable, retrainable, dan ter-governance EM kami build AI yang bisa Anda audit dan percaya.',
    'Free initial consultation EM share your data and use case, our ML team responds within 24 hours with a feasibility check termasuk data sufficiency, baseline, and target metrics.':
        'Konsultasi awal gratis EM bagikan data dan use case Anda, tim ML kami merespon dalam 24 jam dengan feasibility check termasuk kecukupan data, baseline, dan target metrik.',

    # SysInt
    'Most industrial operations run a patchwork of vendor systems: PLCs from one brand, SCADA from another, an ERP that does not talk to either. SURIOTA designs integration architectures EM data buses, APIs':
        'Sebagian besar operasi industri menjalankan campuran sistem vendor: PLC dari satu brand, SCADA dari brand lain, ERP yang tidak terhubung keduanya. SURIOTA merancang arsitektur integrasi EM data bus, API',
    'Free initial consultation EM share your stack, our engineering team responds within 24 hours with a phased integration plan that minimises operational risk.':
        'Konsultasi awal gratis EM bagikan stack Anda, tim engineer kami merespon dalam 24 jam dengan rencana integrasi berfase yang meminimalkan risiko operasional.',
}

# Expand for all 3 em-dash variants
DASH_VARIANTS = [
    (' EM ', ' - ', ' - '),      # placeholder → ascii hyphen replacement (key→value)
    (' EM ', ' &mdash; ', ' - '),  # &mdash; entity
    (' EM ', ' \\u2014 ', ' - '),  # JSON-escaped em-dash
    (' EM ', ' \u2014 ', ' - '),    # raw em-dash char
]

# Build full dict with all variants
FULL = {}
for base_en, base_id in BASE_TRANS.items():
    for em_placeholder, em_replacement_en, em_replacement_id in DASH_VARIANTS:
        en_variant = base_en.replace(em_placeholder, em_replacement_en)
        id_variant = base_id.replace(em_placeholder, em_replacement_id)
        FULL[en_variant] = id_variant

print(f'Total patterns: {len(FULL)}')

PAGES = [5273,5274,5275,5276,5277,5278,5279,5281,5282,5283,5284,5285,5286,5287,5288,5289,5290,5291,5292,5293,5294,5295,5378,5379,5380,5381,5382]
total = 0
for pid in PAGES:
    try:
        r = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}?context=edit&_fields=meta,content', headers=HDRS)
        d = json.loads(urllib.request.urlopen(r, timeout=60).read())
    except: continue
    changes = 0
    payload = {}
    ed = d.get('meta', {}).get('_elementor_data', '')
    if not isinstance(ed, str): ed = json.dumps(ed)
    new_ed = ed
    for en, idt in FULL.items():
        if en in new_ed:
            new_ed = new_ed.replace(en, idt)
            changes += 1
    content_raw = d.get('content', {}).get('raw', '')
    new_content = content_raw
    for en, idt in FULL.items():
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
        except: pass
print(f'\nTotal: {total}')

# Purge
purge = """
$upload = wp_upload_dir();
$log = $upload['basedir']."/purge-mdash-univ.txt";
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
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=json.dumps({'code':purge, 'active':True, 'name':'SX: mdash univ'}).encode(), method='POST', headers=HDRS), timeout=60).read()
time.sleep(3)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print('Purged')
