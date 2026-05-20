"""Translate 5 priority pages (Contact, Privacy, Terms, AI, System Integration) + cleanup 3 legacy."""
import sys, io, json, urllib.request, urllib.error, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization': f'Basic {AUTH}', 'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

# 5 priority pages — (en_id, id_slug, id_title)
PRIORITY = [
    {
        'en_id': 4983, 'slug': 'kontak', 'title': 'Hubungi Kami — SURIOTA',
        'meta_title': 'Hubungi Kami — SURIOTA Industrial IoT Batam',
        'meta_desc': 'Hubungi tim SURIOTA untuk konsultasi proyek Industrial IoT, otomasi, water treatment & renewable energi. Respon dalam 24 jam.'
    },
    {
        'en_id': 4985, 'slug': 'kebijakan-privasi', 'title': 'Kebijakan Privasi — SURIOTA',
        'meta_title': 'Kebijakan Privasi | SURIOTA',
        'meta_desc': 'Kebijakan privasi PT Surya Inovasi Prioritas (SURIOTA) — bagaimana kami mengumpulkan, menggunakan, dan melindungi data pribadi Anda.'
    },
    {
        'en_id': 4987, 'slug': 'syarat-layanan', 'title': 'Syarat Layanan — SURIOTA',
        'meta_title': 'Syarat Layanan | SURIOTA',
        'meta_desc': 'Syarat dan ketentuan penggunaan layanan SURIOTA — Industrial IoT, System Integration, SaaS platform, dan produk hardware.'
    },
    {
        'en_id': 5035, 'slug': 'artificial-intelligence-id', 'title': 'Artificial Intelligence Industri — SURIOTA',
        'meta_title': 'AI Industri & Machine Learning | SURIOTA',
        'meta_desc': 'Solusi Artificial Intelligence industri SURIOTA — computer vision, predictive analytics, anomaly detection untuk manufaktur, oil & gas, maritim.'
    },
    {
        'en_id': 5031, 'slug': 'system-integration-id', 'title': 'System Integration Industri — SURIOTA',
        'meta_title': 'System Integration Industri | SURIOTA',
        'meta_desc': 'Layanan System Integration end-to-end SURIOTA — PLC, SCADA, MES, ERP integration dengan platform IoT modern untuk manufaktur Indonesia.'
    },
]


def fetch_en(en_id):
    r = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{en_id}?context=edit&_fields=meta,template,content', headers=HDRS)
    return json.loads(urllib.request.urlopen(r, timeout=60).read())


# Translation dictionary — reuses common patterns from V1-V12
TRANS = {
    'Contact Us': 'Hubungi Kami',
    'Contact': 'Hubungi',
    'Get in Touch': 'Hubungi Kami',
    'Send Message': 'Kirim Pesan',
    'Send': 'Kirim',
    'SEND': 'KIRIM',
    'Name': 'Nama',
    'Your Name': 'Nama Anda',
    'Email': 'Email',
    'Your Email': 'Email Anda',
    'Message': 'Pesan',
    'Your Message': 'Pesan Anda',
    'Subject': 'Subjek',
    'Phone': 'Telepon',
    'Phone Number': 'Nomor Telepon',
    'Company': 'Perusahaan',
    'Address': 'Alamat',
    'Our Address': 'Alamat Kami',
    'Our Location': 'Lokasi Kami',
    'Business Hours': 'Jam Kerja',
    'Customer Support': 'Dukungan Pelanggan',
    'Office Hours': 'Jam Kantor',
    'Free Consultation': 'Konsultasi Gratis',
    'Request a Quote': 'Minta Penawaran',
    'Privacy Policy': 'Kebijakan Privasi',
    'Terms of Service': 'Syarat Layanan',
    'Terms and Conditions': 'Syarat dan Ketentuan',
    'Last Updated': 'Terakhir Diperbarui',
    'Effective Date': 'Tanggal Berlaku',

    # AI page
    'Artificial Intelligence': 'Artificial Intelligence',  # keep as technical term
    'Predictive Analytics': 'Predictive Analytics',
    'Computer Vision': 'Computer Vision',
    'Anomaly Detection': 'Deteksi Anomali',
    'Machine Learning': 'Machine Learning',
    'Deep Learning': 'Deep Learning',
    'Neural Networks': 'Neural Networks',

    # System Integration
    'System Integration': 'Integrasi Sistem',
    'PLC Integration': 'Integrasi PLC',
    'SCADA Integration': 'Integrasi SCADA',
    'MES Integration': 'Integrasi MES',
    'ERP Integration': 'Integrasi ERP',
    'IT/OT Integration': 'Integrasi IT/OT',

    # Common
    'Our Services': 'Layanan Kami',
    'Industries We Serve': 'Industri yang Kami Layani',
    'Why Choose Us': 'Mengapa Pilih Kami',
    'Why Choose SURIOTA': 'Mengapa Pilih SURIOTA',
    'Get Started': 'Mulai',
    'Learn More': 'Pelajari Lebih Lanjut',
    'Industrial IoT': 'IoT Industri',
    'Industrial Automation': 'Otomasi Industri',
    'System Integration & Engineering Services': 'Layanan Integrasi Sistem & Engineering',
    'across Indonesia': 'di seluruh Indonesia',
    'in Batam': 'di Batam',
    'manufacturing': 'manufaktur',
    'energy': 'energi',
    'logistics': 'logistik',
    'maritime': 'maritim',
    'shipyard': 'shipyard',
    'oil & gas': 'oil & gas',
    'oil and gas': 'oil dan gas',

    # FAQ patterns
    'Frequently Asked Questions': 'Pertanyaan Umum',
    'FAQ': 'FAQ',
}


def link_translation(en_id, id_id):
    payload = json.dumps({'en_id': en_id, 'id_id': id_id}).encode()
    req = urllib.request.Request('https://suriota.com/wp-json/sx/v1/link-translation', data=payload, method='POST', headers=HDRS)
    return json.loads(urllib.request.urlopen(req, timeout=30).read())


def create_id_page(p, en_data):
    # Clone EN _elementor_data and apply translations
    ed = en_data['meta']['_elementor_data']
    if not isinstance(ed, str): ed = json.dumps(ed)
    page_settings = en_data['meta'].get('_elementor_page_settings', {})
    content_raw = en_data.get('content', {}).get('raw', '')

    # Apply translations
    for en, idt in TRANS.items():
        ed = ed.replace(en, idt)
        content_raw = content_raw.replace(en, idt)

    payload = {
        'title': p['title'],
        'slug': p['slug'],
        'content': content_raw,
        'status': 'publish',
        'meta': {
            '_elementor_data': ed,
            '_elementor_edit_mode': 'builder',
            '_elementor_template_type': 'wp-page',
            '_elementor_page_settings': page_settings,
        }
    }
    req = urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages?lang=id', data=json.dumps(payload).encode(), method='POST', headers=HDRS)
    return json.loads(urllib.request.urlopen(req, timeout=60).read())


# === 1) Translate 5 priority pages ===
created_pairs = []
print('=== Translating 5 priority pages ===')
for p in PRIORITY:
    print(f"\nEN {p['en_id']} → /id/{p['slug']}/")
    try:
        en_data = fetch_en(p['en_id'])
        result = create_id_page(p, en_data)
        id_id = result['id']
        link_translation(p['en_id'], id_id)
        created_pairs.append((p['en_id'], id_id, p['slug'], p['meta_title'], p['meta_desc']))
        print(f"  Created ID {id_id} linked")
    except urllib.error.HTTPError as e:
        print(f"  FAIL: {e.code} {e.read().decode()[:200]}")
    except Exception as e:
        print(f"  EXC: {e}")

# === 2) Apply AIOSEO meta for 5 new ID pages ===
print('\n=== AIOSEO meta for 5 new pages ===')
seo_php_lines = []
for en_id, id_id, slug, title, desc in created_pairs:
    # Use AIOSEO direct table write
    seo_php_lines.append(f"""
\$row = \$wpdb->get_row(\$wpdb->prepare("SELECT id FROM \$table WHERE post_id=%d", {id_id}));
if (\$row) {{
    \$wpdb->update(\$table, ['title'=>{json.dumps(title)}, 'description'=>{json.dumps(desc)}, 'updated'=>current_time('mysql')], ['post_id'=>{id_id}]);
}} else {{
    \$wpdb->insert(\$table, ['post_id'=>{id_id}, 'title'=>{json.dumps(title)}, 'description'=>{json.dumps(desc)}, 'created'=>current_time('mysql'), 'updated'=>current_time('mysql')]);
}}""")

cleanup_legacy_ids = [376, 33, 41]
seo_legacy_lines = []
for lid in cleanup_legacy_ids:
    seo_legacy_lines.append(f"wp_update_post(['ID' => {lid}, 'post_status' => 'draft']);")

seo_php = f"""
\$upload = wp_upload_dir();
\$log_path = \$upload['basedir'] . '/seo-priority-5.txt';
if (file_exists(\$log_path)) {{ if (function_exists('code_snippets')) {{ code_snippets()->deactivate(5); }} return; }}
global \$wpdb;
\$table = \$wpdb->prefix . 'aioseo_posts';
{''.join(seo_php_lines)}

// === Cleanup 3 legacy pages → set to draft ===
{chr(10).join(seo_legacy_lines)}

// Cache purge
if (function_exists('aioseo')) {{ \$a = aioseo(); if (isset(\$a->core->cache) && method_exists(\$a->core->cache, 'clear')) \$a->core->cache->clear(); }}
if (class_exists('\\\\Elementor\\\\Plugin')) \\\\Elementor\\\\Plugin::instance()->files_manager->clear_cache();
if (class_exists('WPO_Page_Cache')) WPO_Page_Cache::instance()->purge();
if (class_exists('WP_Optimize_Minify_Cache_Functions')) \\\\WP_Optimize_Minify_Cache_Functions::purge();
wp_cache_flush();

file_put_contents(\$log_path, 'done @ ' . date('c'));
if (function_exists('code_snippets')) {{ code_snippets()->deactivate(5); }}
"""

urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=json.dumps({'code':seo_php, 'active':True, 'name':'SX: priority-5 SEO'}).encode(), method='POST', headers=HDRS), timeout=60).read()
time.sleep(3)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read()
print('AIOSEO + legacy cleanup applied')
time.sleep(3)

print(f'\n=== SUMMARY ===')
print(f'Created {len(created_pairs)} ID pages')
print(f'Demoted {len(cleanup_legacy_ids)} legacy pages to draft')
for en, idd, slug, _, _ in created_pairs:
    print(f"  EN {en} <-> ID {idd}  /id/{slug}/")
