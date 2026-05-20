"""Claude grammar review — fix common Bahasa Indonesia errors + translation artifacts across 27 ID pages."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

# === Grammar corrections — Claude native Indonesian review ===
GRAMMAR = {
    # ===== Word order: Indonesian uses noun-adjective (Bahasa: noun first) =====
    'In-House Produk': 'Produk In-House',
    'In-House Products': 'Produk In-House',
    'Profesional Tim': 'Tim Profesional',
    'Komunikasi Protokols': 'Protokol Komunikasi',
    'Komunikasi Protokol': 'Protokol Komunikasi',
    'Wireless Konektivitas': 'Konektivitas Wireless',
    'BLE Mobile Configuration': 'Konfigurasi Mobile BLE',
    'Konfigurasi BLE Mobile': 'Konfigurasi Mobile BLE',
    'Failover Jaringan Dual': 'Dual Failover Jaringan',
    'Industrial Konektivitas': 'Konektivitas Industri',
    'Industrial-Grade Hardware': 'Hardware Industrial-Grade',
    'Cloud-Agnostic Integrasi': 'Integrasi Cloud-Agnostic',
    'Multi-Protokol Bridge': 'Bridge Multi-Protokol',

    # ===== Translation artifacts (calque) =====
    'Our 5 Layanan Inti': '5 Layanan Inti Kami',
    'Our 5 LAYANAN INTI': '5 LAYANAN INTI KAMI',
    'OUR 5 LAYANAN INTI': '5 LAYANAN INTI KAMI',
    'Our jangka panjang partnership': 'Kemitraan jangka panjang kami',
    'Our partnership': 'Kemitraan kami',
    'is a technology company specializing in': 'adalah perusahaan teknologi yang berfokus pada',
    'SURIOTA is a technology company': 'SURIOTA adalah perusahaan teknologi',
    '(SURIOTA) is a technology company': '(SURIOTA) adalah perusahaan teknologi',
    '(SURIOTA) SURIOTA is a technology': '(SURIOTA) adalah perusahaan teknologi yang',
    'PT Surya Inovasi Prioritas SURIOTA is a technology company': 'PT Surya Inovasi Prioritas (SURIOTA) adalah perusahaan teknologi yang',

    # Mixed-language fixes
    'with compliance SPARING KLHK': 'dengan compliance SPARING KLHK',
    'with monitoring real-time': 'dengan monitoring real-time',
    'with real-time monitoring': 'dengan monitoring real-time',
    'and the SURGE Water Analytics platform': 'dan platform SURGE Water Analytics',
    'and the SURGE': 'dan SURGE',
    'consistent berkualitas tinggi water supply': 'pasokan air berkualitas tinggi yang konsisten',
    'consistent berkualitas tinggi': 'yang konsisten dan berkualitas tinggi',
    'while complying with environmental regulations': 'sambil mematuhi regulasi lingkungan',

    # "Tidak X" → "Tanpa X" where X is English noun phrase (broken machine translation)
    'Tidak-code register': 'No-code register',
    'Tidak code register': 'No-code register',
    'Tidak PC, no cables, no Telnet required.': 'Tanpa PC, tanpa kabel, tanpa Telnet diperlukan.',
    'Tidak vendor lock-in': 'Tanpa vendor lock-in',
    'Tidak third-party gateway lock-in': 'Tanpa lock-in gateway third-party',
    'Tidak infrastructure required': 'Tanpa infrastruktur tambahan',
    'Tidak infrastructure to provision': 'tanpa infrastruktur yang perlu di-provision',
    'Tidak handover gap': 'Tanpa handover gap',
    'Tidak reseller incentive': 'Tanpa reseller incentive',
    'Tidak site visit needed': 'Tanpa kunjungan lokasi',

    # "Tidak. X" (period inserted) — broken translations of "No. X" (number)
    'Permen LHK Tidak. 80/2019': 'Permen LHK No. 80/2019',
    'Permen LHK Tidak 80/2019': 'Permen LHK No. 80/2019',

    # ===== Capitalization/spelling fixes =====
    'Water Treatment Layanan': 'Layanan Water Treatment',
    'Water Treatment Services': 'Layanan Water Treatment',
    'Water Treatment Rencanat': 'Water Treatment Plant',
    'Water Treatment Rencanats': 'Water Treatment Plants',
    'Wastewater Treatment Rencanat': 'Wastewater Treatment Plant',
    'Wastewater Treatment Rencanats': 'Wastewater Treatment Plants',
    'Sewage Treatment Rencanat': 'Sewage Treatment Plant',
    'Sewage Treatment Rencanats': 'Sewage Treatment Plants',
    'Treatment Rencanat': 'Treatment Plant',

    # Untranslated remnants
    'water utilitas': 'utilitas air',
    'Water Utilitas': 'Utilitas Air',
    'long-term': 'jangka panjang',
    'Long-term Partner': 'Partner Jangka Panjang',
    'IoT Real-Time Monitor': 'Monitor IoT Real-Time',
    'KLHK SPARING Certified': 'Bersertifikat SPARING KLHK',

    # ===== Awkward Indonesian phrasing =====
    'Anda untuk untuk': 'Anda untuk',
    'untuk untuk': 'untuk',
    'yang yang': 'yang',
    'dan dan': 'dan',
    'kami kami': 'kami',
    ',,': ',',
    '  ': ' ',  # double spaces

    # ===== Specific awkward phrases from review =====
    'menyediakaners': 'menyediakan layanan',  # broken word
    'otomasited': 'otomasi terintegrasi',  # broken word
    'SURIOTA delivers': 'SURIOTA menyediakan',
    'SURIOTA deliv': 'SURIOTA menyediakan',
    'SURplatform SURGE': 'platform SURGE',  # double-word
    'SURIOTA\u2019s': 'SURIOTA',  # remove possessive
    'Suriota\u2019s': 'Suriota',

    # English remnants in ID pages
    'Operasi -40\u00b0C hingga +85\u00b0C. DIN rail mountable.': 'Operasi -40\u00b0C hingga +85\u00b0C. DIN rail mountable.',  # keep
    'When your operations depend on': 'Saat operasi Anda bergantung pada',
    'When it comes to': 'Untuk',
    'Take full control of': 'Ambil kontrol penuh atas',
    'Take your': 'Bawa',
    'Boost Your Komunikasi': 'Tingkatkan Komunikasi Anda',
    'Boost Your': 'Tingkatkan',
    'Take it to the next level': 'bawa ke level berikutnya',
    'Drive higher': 'Tingkatkan',
    'Eliminate billing disputes': 'Eliminasi sengketa billing',
    'Unleash the power of': 'Manfaatkan kekuatan',
    'Powered by': 'Didukung oleh',
    'Engineered for': 'Dirancang untuk',
    'Designed for': 'Dirancang untuk',
    'Built for': 'Dibangun untuk',
    'Rated for': 'Rated untuk',
    'Optimized for': 'Dioptimasi untuk',

    # Common partial-translation patterns
    'compliant': 'compliant',  # keep technical term
    'guaranteed': 'dijamin',
    'ensures': 'memastikan',
    'ensuring': 'memastikan',
    'including': 'termasuk',
    'including the': 'termasuk',
    'such as': 'seperti',
    'such as the': 'seperti',
    'whether you': 'baik Anda',
    'whether your': 'baik',
    'in case': 'jika',
    'in case of': 'dalam kasus',

    # Industries chips proper format (singular vs plural)
    'Industries We Serve': 'Industri yang Kami Layani',
    'Industries We Automate': 'Industri yang Kami Otomatisasi',
    'Industries We Power': 'Industri yang Kami Dayai',

    # FAQ titles
    'Frequently Asked Questions': 'Pertanyaan Umum',

    # Form fields untranslated
    'Your name': 'Nama Anda',
    'Your email': 'Email Anda',
    'Your message': 'Pesan Anda',
    'Type your message': 'Ketik pesan Anda',

    # Footer/header bits
    'Read More': 'Selengkapnya',
    'Read more': 'Selengkapnya',
    'See more': 'Lihat selengkapnya',
    'View more': 'Lihat selengkapnya',
    'Show more': 'Tampilkan lebih banyak',
    'Show less': 'Tampilkan lebih sedikit',
    'Load more': 'Muat lebih banyak',
    'Load More': 'Muat Lebih Banyak',

    # ===== KBBI/PUEBI compliance fixes =====
    'di seluruh': 'di seluruh',  # correct
    'di indonesia': 'di Indonesia',  # capitalize country
    'manfaat': 'manfaat',  # KBBI standard
    'fasilitas': 'fasilitas',  # KBBI standard

    # Casing fixes for technical terms
    'iot': 'IoT',  # standalone lowercase iot → IoT
    'plc': 'PLC',
    'scada': 'SCADA',
    'mqtt': 'MQTT',
    'modbus': 'Modbus',
    # Note: these single-word matches are risky — only apply to standalone
    # Will be handled differently
}

# Remove single-word casing fixes (too risky to apply globally)
RISKY_KEYS = ['iot', 'plc', 'scada', 'mqtt', 'modbus']
for k in RISKY_KEYS:
    GRAMMAR.pop(k, None)

# Apply to all 27 ID pages
ID_PAGE_IDS = [5273, 5274, 5275, 5276, 5277, 5278, 5279, 5281, 5282, 5283, 5284, 5285, 5286,
               5287, 5288, 5289, 5290, 5291, 5292, 5293, 5294, 5295,
               5378, 5379, 5380, 5381, 5382]  # incl 5 new priority pages

print(f'Applying {len(GRAMMAR)} grammar corrections to {len(ID_PAGE_IDS)} ID pages...')
total = 0
pages_changed = 0
for pid in ID_PAGE_IDS:
    try:
        r = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}?context=edit&_fields=id,content,meta', headers=HDRS)
        d = json.loads(urllib.request.urlopen(r, timeout=60).read())
    except Exception as e:
        print(f'  {pid}: fetch fail {e}')
        continue

    changes = 0
    payload = {}

    # Apply to _elementor_data
    ed = d.get('meta', {}).get('_elementor_data', '')
    if not isinstance(ed, str): ed = json.dumps(ed)
    new_ed = ed
    for en, idt in GRAMMAR.items():
        if en in new_ed:
            new_ed = new_ed.replace(en, idt)
            changes += 1

    # Apply to content
    content_raw = d.get('content', {}).get('raw', '')
    new_content = content_raw
    for en, idt in GRAMMAR.items():
        if en in new_content:
            new_content = new_content.replace(en, idt)
            changes += 1

    if new_ed != ed or new_content != content_raw:
        if new_ed != ed: payload['meta'] = {'_elementor_data': new_ed}
        if new_content != content_raw: payload['content'] = new_content
        try:
            urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}', data=json.dumps(payload).encode(), method='POST', headers=HDRS), timeout=60).read()
            print(f'  page {pid}: +{changes} corrections')
            total += changes
            pages_changed += 1
        except Exception as e:
            print(f'  page {pid}: push fail {e}')

print(f'\nTotal: {total} corrections across {pages_changed} pages')

# Purge all
purge = '''
$upload = wp_upload_dir();
$log = $upload['basedir']."/purge-grammar.txt";
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
'''
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=json.dumps({'code':purge, 'active':True, 'name':'SX: grammar purge'}).encode(), method='POST', headers=HDRS), timeout=60).read()
time.sleep(3)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print('Purged')
