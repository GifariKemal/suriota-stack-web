"""Legal v4 - exact storage strings."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

TRANS = {
    # Privacy 5379
    'This policy is aligned with Indonesia\\u2019s Personal Data Protection Law (UU PDP No.27\\/2022) and the EU General Data Protection Regulation (GDPR).':
        'Kebijakan ini sejalan dengan UU Pelindungan Data Pribadi Indonesia (UU PDP No.27\\/2022) dan EU General Data Protection Regulation (GDPR).',
    'Telemetry from products:': 'Telemetri dari produk:',
    ' for IoT deployments using the SURGE platform, we collect device identifiers, sensor readings, geolocation (when consented), and event logs strictly for the purpose of operating the service.':
        ' untuk deployment IoT yang menggunakan platform SURGE, kami mengumpulkan identifier perangkat, pembacaan sensor, geolokasi (jika disetujui), dan log event semata-mata untuk tujuan mengoperasikan layanan.',
    'Under UU PDP No.27\\/2022 (Indonesia) and GDPR (EU), you have the right to:':
        'Berdasarkan UU PDP No.27\\/2022 (Indonesia) dan GDPR (UE), Anda berhak untuk:',
    'We may update this Kebijakan Privasi from time to time. The latest version will always be posted on this page, with the \\u201cLast updated\\u201d date revised. Material changes will be communicated by email or platform notice at least 14 days in advance.':
        'Kami dapat memperbarui Kebijakan Privasi ini dari waktu ke waktu. Versi terbaru akan selalu diposting di halaman ini, dengan tanggal \\u201cLast updated\\u201d direvisi. Perubahan material akan dikomunikasikan via email atau notifikasi platform paling lambat 14 hari sebelumnya.',
    'For questions about this Kebijakan Privasi or to exercise your data-protection rights, please contact:':
        'Untuk pertanyaan tentang Kebijakan Privasi ini atau untuk menggunakan hak pelindungan data Anda, silakan hubungi:',

    # Terms 5380
    'These Syarat Layanan (\\u201c<strong>Terms<\\/strong>\\u201d) form a binding agreement between you (\\u201cyou\\u201d or \\u201cKlien\\u201d) and PT Surya Inovasi Prioritas (\\u201c<strong>SURIOTA<\\/strong>\\u201d, \\u201cwe\\u201d, \\u201cus\\u201d, or \\u201cour\\u201d). By accessing our website, purchasing our products, or engaging our services, you agree to these Terms.':
        'Syarat Layanan ini (\\u201c<strong>Syarat<\\/strong>\\u201d) merupakan perjanjian mengikat antara Anda (\\u201cAnda\\u201d atau \\u201cKlien\\u201d) dan PT Surya Inovasi Prioritas (\\u201c<strong>SURIOTA<\\/strong>\\u201d, \\u201ckami\\u201d). Dengan mengakses situs web kami, membeli produk kami, atau menggunakan layanan kami, Anda menyetujui Syarat ini.',
    'Each party will protect the other\\u2019s Confidential Information with the same degree of care it uses to protect its own (no less than reasonable care), use it solely to perform the Engagement, and not disclose it to third parties without consent, except to employees, contractors, or advisors with a need to know who are bound by similar confidentiality obligations.':
        'Setiap pihak akan melindungi Informasi Rahasia pihak lain dengan tingkat kehati-hatian yang sama seperti melindungi miliknya sendiri (tidak kurang dari kehati-hatian yang wajar), menggunakannya semata-mata untuk melaksanakan Engagement, dan tidak mengungkapkannya kepada pihak ketiga tanpa persetujuan, kecuali kepada karyawan, kontraktor, atau penasihat yang perlu tahu dan terikat kewajiban kerahasiaan serupa.',
    'Each party will protect the other\\u2019s Confidential Information with the same degree of care it uses to protect its own (no less than reasonable care), use it solely to perform the Engagement, and not disclose it to third parties without consent, e':
        'Setiap pihak akan melindungi Informasi Rahasia pihak lain dengan kehati-hatian yang sama seperti melindungi miliknya sendiri (tidak kurang dari kehati-hatian wajar), menggunakannya semata-mata untuk melaksanakan Engagement, dan tidak mengungkapkannya kepada pihak ketiga tanpa persetujuan, kecuali kepada e',
    'Notices<\\/strong> - written notices to ': 'Pemberitahuan<\\/strong> - pemberitahuan tertulis ke ',
    ' for SURIOTA, or to the address you provided.': ' untuk SURIOTA, atau ke alamat yang Anda berikan.',

    # AI 5381
    'We pick high-ROI use cases, train on your data, and deploy with rollback and monitoring.':
        'Kami memilih use case ROI tinggi, training pada data Anda, dan deploy dengan rollback serta monitoring.',
    'Edge-capable, <strong>retrainable, and governed<\\/strong> &mdash; we build AI you can audit and trust.':
        'Edge-capable, <strong>retrainable, dan ter-governance<\\/strong> &mdash; kami build AI yang dapat Anda audit dan percaya.',
}

PAGES = [5379, 5380, 5381]
total = 0
for pid in PAGES:
    try:
        r = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}?context=edit&_fields=meta,content', headers=HDRS)
        d = json.loads(urllib.request.urlopen(r, timeout=60).read())
    except Exception as e:
        print(f'  {pid}: fetch fail {e}')
        continue
    changes = 0
    payload = {}
    ed = d.get('meta', {}).get('_elementor_data', '')
    if not isinstance(ed, str): ed = json.dumps(ed)
    new_ed = ed
    for en, idt in TRANS.items():
        if en in new_ed:
            new_ed = new_ed.replace(en, idt)
            changes += 1
    content_raw = d.get('content', {}).get('raw', '')
    new_content = content_raw
    for en, idt in TRANS.items():
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
$log = $upload['basedir']."/purge-legal-v4.txt";
if (file_exists($log)) { if (function_exists('code_snippets')) { code_snippets()->deactivate(5); } return; }
if (class_exists('\\\\Elementor\\\\Plugin')) {
    foreach ([5379,5380,5381] as $pid) {
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
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=json.dumps({'code':purge, 'active':True, 'name':'SX: legal v4'}).encode(), method='POST', headers=HDRS), timeout=60).read()
time.sleep(3)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/id/kebijakan-privasi/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print('Purged')
