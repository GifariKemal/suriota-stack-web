"""Final legal translation - exact strings from audit."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

# Direct translations of remaining English content
TRANS = {
    # Privacy - direct sentences
    'This policy is aligned with Indonesia&#8217;s Personal Data Protection Law (UU PDP No.27/2022)':
        'Kebijakan ini sejalan dengan Undang-Undang Pelindungan Data Pribadi Indonesia (UU PDP No.27/2022)',
    "This policy is aligned with Indonesia's Personal Data Protection Law (UU PDP No.27/2022)":
        'Kebijakan ini sejalan dengan Undang-Undang Pelindungan Data Pribadi Indonesia (UU PDP No.27/2022)',
    'PT Surya Inovasi Prioritas (&#8220;SURIOTA&#8221;, &#8220;we&#8221;, &#8220;us&#8221;, or &#8220;our&#8221;) respects your privacy and is committed to protecting your personal data.':
        'PT Surya Inovasi Prioritas (&#8220;SURIOTA&#8221;, &#8220;kami&#8221;) menghormati privasi Anda dan berkomitmen melindungi data pribadi Anda.',
    'PT Surya Inovasi Prioritas ("SURIOTA", "we", "us", or "our") respects your privacy and is committed to protecting your personal data.':
        'PT Surya Inovasi Prioritas ("SURIOTA", "kami") menghormati privasi Anda dan berkomitmen melindungi data pribadi Anda.',
    'Account credentials: if you create an account on the SURGE platform, we collect your username, hashed password, and authentication tokens.':
        'Kredensial akun: jika Anda membuat akun di platform SURGE, kami mengumpulkan nama pengguna, kata sandi ter-hash, dan token autentikasi Anda.',
    'Correspondence: emails, WhatsApp messages, and call logs you exchange with our team.':
        'Korespondensi: email, pesan WhatsApp, dan log panggilan yang Anda pertukarkan dengan tim kami.',
    'Telemetry from products: for IoT deployments using the SURGE platform, we collect device identifiers, sensor readings, geolocation (when consented), and event logs strictly for the purpose of operating the service.':
        'Telemetri dari produk: untuk deployment IoT menggunakan platform SURGE, kami mengumpulkan identifier perangkat, pembacaan sensor, geolokasi (jika disetujui), dan log event semata-mata untuk tujuan mengoperasikan layanan.',
    'Contract performance - to fulfil engagement and service agreements.':
        'Pelaksanaan kontrak - untuk memenuhi perjanjian engagement dan layanan.',
    'Legitimate interests - to operate our business, secure our services, and develop our products.':
        'Kepentingan sah - untuk mengoperasikan bisnis kami, mengamankan layanan kami, dan mengembangkan produk kami.',
    'Consent - for marketing and optional cookies. You may withdraw consent at any time.':
        'Persetujuan - untuk pemasaran dan cookie opsional. Anda dapat menarik persetujuan kapan saja.',
    'Legal obligation - to comply with tax, accounting, and regulatory requirements.':
        'Kewajiban hukum - untuk mematuhi persyaratan pajak, akuntansi, dan regulasi.',
    'Service providers processing data on our behalf (cloud hosting, email delivery, analytics, payment) under written data-processing agreements.':
        'Penyedia layanan yang memproses data atas nama kami (cloud hosting, pengiriman email, analytics, pembayaran) berdasarkan perjanjian pemrosesan data tertulis.',
    'Proyek partners - integrators, certified installers, or auditors involved in delivering your proyek, only as necessary.':
        'Mitra proyek - integrator, installer bersertifikat, atau auditor yang terlibat dalam menjalankan proyek Anda, hanya sesuai keperluan.',
    "Successor entities in the event of merger, acquisition, or asset transfer, with continuity of this Policy's protections.":
        'Entitas penerus dalam hal merger, akuisisi, atau transfer aset, dengan kelanjutan perlindungan Kebijakan ini.',
    'Successor entities in the event of merger, acquisition, or asset transfer, with continuity of this Policy&#8217;s protections.':
        'Entitas penerus dalam hal merger, akuisisi, atau transfer aset, dengan kelanjutan perlindungan Kebijakan ini.',
    'Analytics cookies - to understand traffic and improve content (e.g., Google Analytics). You may opt out via your browser settings.':
        'Cookie analytics - untuk memahami trafik dan meningkatkan konten (mis. Google Analytics). Anda dapat opt-out melalui pengaturan browser.',
    'Marketing cookies - only set with your explicit consent (where applicable).':
        'Cookie pemasaran - hanya diatur dengan persetujuan eksplisit Anda (jika berlaku).',
    'Lead &amp; inquiry data: up to 24 months from last interaction.':
        'Data lead &amp; inquiry: hingga 24 bulan sejak interaksi terakhir.',
    'Lead & inquiry data: up to 24 months from last interaction.':
        'Data lead & inquiry: hingga 24 bulan sejak interaksi terakhir.',
    'Pelanggan / proyek records: for the duration of the engagement plus 10 years (Indonesian commercial-records requirement).':
        'Catatan pelanggan / proyek: selama durasi engagement plus 10 tahun (persyaratan catatan komersial Indonesia).',
    'IoT telemetry: as defined in the service-specific data-processing agreement.':
        'Telemetri IoT: sebagaimana didefinisikan dalam perjanjian pemrosesan data spesifik layanan.',
    'Under UU PDP No.27/2022 (Indonesia) and GDPR (EU), you have the right to:':
        'Berdasarkan UU PDP No.27/2022 (Indonesia) dan GDPR (UE), Anda berhak untuk:',
    'Access - obtain confirmation of and a copy of your data we hold.':
        'Akses - memperoleh konfirmasi dan salinan data Anda yang kami simpan.',
    'Portability - receive your data in a structured, machine-readable format.':
        'Portabilitas - menerima data Anda dalam format terstruktur dan terbaca mesin.',
    'Objection - object to processing based on legitimate interests, termasuk profiling for marketing.':
        'Keberatan - menolak pemrosesan berdasarkan kepentingan sah, termasuk profiling untuk pemasaran.',
    "Lodge a complaint with Indonesia's Personal Data Protection Agency or your EU supervisory authority.":
        'Mengajukan keluhan kepada Lembaga Pelindungan Data Pribadi Indonesia atau otoritas pengawas UE Anda.',
    'Lodge a complaint with Indonesia&#8217;s Personal Data Protection Agency or your EU supervisory authority.':
        'Mengajukan keluhan kepada Lembaga Pelindungan Data Pribadi Indonesia atau otoritas pengawas UE Anda.',
    'To exercise these rights, contact admin@suriota.com. We will respond within 30 calendar days.':
        'Untuk menggunakan hak-hak ini, hubungi admin@suriota.com. Kami akan merespons dalam 30 hari kalender.',

    # Terms - direct sentences
    'These Syarat Layanan (&#8220;Terms&#8221;) form a binding agreement between you (&#8220;you&#8221; or &#8220;Klien&#8221;) and PT Surya Inovasi Prioritas (&#8220;SURIOTA&#8221;, &#8220;we&#8221;, &#8220;us&#8221;, or &#8220;our&#8221;). By accessing our website, purchasing our products, or engaging our services, you agree to these Terms.':
        'Syarat Layanan ini (&#8220;Syarat&#8221;) merupakan perjanjian mengikat antara Anda (&#8220;Anda&#8221; atau &#8220;Klien&#8221;) dan PT Surya Inovasi Prioritas (&#8220;SURIOTA&#8221;, &#8220;kami&#8221;). Dengan mengakses situs web kami, membeli produk kami, atau menggunakan layanan kami, Anda menyetujui Syarat ini.',
    'These Syarat Layanan ("Terms") form a binding agreement between you ("you" or "Klien") and PT Surya Inovasi Prioritas ("SURIOTA", "we", "us", or "our"). By accessing our website, purchasing our products, or engaging our services, you agree to these Terms.':
        'Syarat Layanan ini ("Syarat") merupakan perjanjian mengikat antara Anda ("Anda" atau "Klien") dan PT Surya Inovasi Prioritas ("SURIOTA", "kami"). Dengan mengakses situs web kami, membeli produk kami, atau menggunakan layanan kami, Anda menyetujui Syarat ini.',
    'Services - engineering, integration, consultation, and SaaS offerings provided by SURIOTA, termasuk the SURGE platform.':
        'Layanan - engineering, integrasi, konsultasi, dan penawaran SaaS yang disediakan oleh SURIOTA, termasuk platform SURGE.',
    'Confidential Information - any non-public information disclosed by either party that should reasonably be understood to be confidential.':
        'Informasi Rahasia - informasi non-publik apapun yang diungkap oleh salah satu pihak yang sepatutnya dipahami sebagai rahasia.',
    'All firmware, software, designs, schematics, documentation, trademarks, and know-how created or owned by SURIOTA - termasuk the SURGE platform and all Products - remain the exclusive property of SURIOTA.':
        'Seluruh firmware, perangkat lunak, desain, skematik, dokumentasi, merek dagang, dan know-how yang dibuat atau dimiliki oleh SURIOTA - termasuk platform SURGE dan semua Produk - tetap menjadi milik eksklusif SURIOTA.',
    'Pricing - as quoted in writing. Quotes are valid for 30 days unless extended.':
        'Harga - sesuai penawaran tertulis. Penawaran berlaku 30 hari kecuali diperpanjang.',
    'Taxes - VAT (PPN), withholding tax (PPh), and other applicable taxes are added to invoiced amounts unless quoted as tax-inclusive.':
        'Pajak - PPN, PPh (withholding), dan pajak lain yang berlaku ditambahkan ke jumlah faktur kecuali ditawarkan inclusive pajak.',
    'Late payment - we may suspend services and charge interest at 1.5% per month on overdue balances, to the extent permitted by law.':
        'Keterlambatan pembayaran - kami dapat menangguhkan layanan dan mengenakan bunga 1,5% per bulan atas saldo jatuh tempo, sejauh diperbolehkan hukum.',
    "Each party will protect the other's Confidential Information with the same degree of care it uses to protect its own (no less than reasonable care), use it solely to perform the Engagement, and not disclose it except to those with a need to know who are bound by similar confidentiality obligations.":
        'Setiap pihak akan melindungi Informasi Rahasia pihak lain dengan tingkat kehati-hatian yang sama seperti melindungi miliknya sendiri (tidak kurang dari kehati-hatian yang wajar), menggunakannya semata-mata untuk melaksanakan Engagement, dan tidak mengungkapkannya kecuali kepada mereka yang perlu tahu dan terikat kewajiban kerahasiaan serupa.',
    'Each party will protect the other&#8217;s Confidential Information with the same degree of care it uses to protect its own (no less than reasonable care), use it solely to perform the Engagement, and not disclose it except to those with a need to know who are bound by similar confidentiality obligations.':
        'Setiap pihak akan melindungi Informasi Rahasia pihak lain dengan tingkat kehati-hatian yang sama seperti melindungi miliknya sendiri (tidak kurang dari kehati-hatian yang wajar), menggunakannya semata-mata untuk melaksanakan Engagement, dan tidak mengungkapkannya kecuali kepada mereka yang perlu tahu dan terikat kewajiban kerahasiaan serupa.',
    'EXCEPT AS EXPRESSLY STATED, THE SERVICES AND PRODUCTS ARE PROVIDED &#8220;AS IS&#8221; AND &#8220;AS AVAILABLE&#8221;, WITHOUT WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.':
        'KECUALI DINYATAKAN SECARA TEGAS, LAYANAN DAN PRODUK DISEDIAKAN &#8220;APA ADANYA&#8221; DAN &#8220;SEBAGAIMANA TERSEDIA&#8221;, TANPA JAMINAN APAPUN, TERSURAT MAUPUN TERSIRAT, TERMASUK DAYA JUAL, KESESUAIAN UNTUK TUJUAN TERTENTU, ATAU NON-PELANGGARAN.',
    'EXCEPT AS EXPRESSLY STATED, THE SERVICES AND PRODUCTS ARE PROVIDED "AS IS" AND "AS AVAILABLE", WITHOUT WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT.':
        'KECUALI DINYATAKAN SECARA TEGAS, LAYANAN DAN PRODUK DISEDIAKAN "APA ADANYA" DAN "SEBAGAIMANA TERSEDIA", TANPA JAMINAN APAPUN, TERSURAT MAUPUN TERSIRAT, TERMASUK DAYA JUAL, KESESUAIAN UNTUK TUJUAN TERTENTU, ATAU NON-PELANGGARAN.',
    "TO THE MAXIMUM EXTENT PERMITTED BY LAW, SURIOTA'S TOTAL CUMULATIVE LIABILITY ARISING OUT OF OR RELATED TO THESE TERMS OR ANY ENGAGEMENT SHALL NOT EXCEED THE AMOUNT PAID BY YOU TO SURIOTA UNDER THE APPLICABLE ENGAGEMENT IN THE TWELVE (12) MONTHS PRECEDING THE EVENT GIVING RISE TO THE CLAIM.":
        'SEJAUH DIIZINKAN OLEH HUKUM, LIABILITAS KUMULATIF TOTAL SURIOTA YANG TIMBUL DARI ATAU TERKAIT SYARAT INI ATAU ENGAGEMENT APAPUN TIDAK AKAN MELEBIHI JUMLAH YANG ANDA BAYARKAN KEPADA SURIOTA BERDASARKAN ENGAGEMENT TERKAIT DALAM DUA BELAS (12) BULAN SEBELUM PERISTIWA YANG MENIMBULKAN KLAIM.',
    'TO THE MAXIMUM EXTENT PERMITTED BY LAW, SURIOTA&#8217;S TOTAL CUMULATIVE LIABILITY ARISING OUT OF OR RELATED TO THESE TERMS OR ANY ENGAGEMENT SHALL NOT EXCEED THE AMOUNT PAID BY YOU TO SURIOTA UNDER THE APPLICABLE ENGAGEMENT IN THE TWELVE (12) MONTHS PRECEDING THE EVENT GIVING RISE TO THE CLAIM.':
        'SEJAUH DIIZINKAN OLEH HUKUM, LIABILITAS KUMULATIF TOTAL SURIOTA YANG TIMBUL DARI ATAU TERKAIT SYARAT INI ATAU ENGAGEMENT APAPUN TIDAK AKAN MELEBIHI JUMLAH YANG ANDA BAYARKAN KEPADA SURIOTA BERDASARKAN ENGAGEMENT TERKAIT DALAM DUA BELAS (12) BULAN SEBELUM PERISTIWA YANG MENIMBULKAN KLAIM.',
    'IN NO EVENT SHALL SURIOTA BE LIABLE FOR INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, OR FOR LOSS OF PROFITS, REVENUE, DATA, OR USE - EVEN IF ADVISED OF THE POSSIBILITY.':
        'DALAM HAL APAPUN, SURIOTA TIDAK BERTANGGUNG JAWAB ATAS KERUGIAN TIDAK LANGSUNG, INSIDENTAL, KHUSUS, KONSEKUENSIAL, ATAU PUNITIF, ATAU ATAS HILANGNYA KEUNTUNGAN, PENDAPATAN, DATA, ATAU PENGGUNAAN - SEKALIPUN TELAH DIBERITAHU KEMUNGKINANNYA.',
    'These Terms remain in effect while you use the Services. Either party may terminate an Engagement with thirty (30) days&#8217; written notice, or immediately for material breach not cured within fifteen (15) days of written notice.':
        'Syarat ini tetap berlaku selama Anda menggunakan Layanan. Salah satu pihak dapat mengakhiri Engagement dengan pemberitahuan tertulis tiga puluh (30) hari, atau segera atas pelanggaran material yang tidak diperbaiki dalam lima belas (15) hari sejak pemberitahuan tertulis.',
    "These Terms remain in effect while you use the Services. Either party may terminate an Engagement with thirty (30) days' written notice, or immediately for material breach not cured within fifteen (15) days of written notice.":
        'Syarat ini tetap berlaku selama Anda menggunakan Layanan. Salah satu pihak dapat mengakhiri Engagement dengan pemberitahuan tertulis tiga puluh (30) hari, atau segera atas pelanggaran material yang tidak diperbaiki dalam lima belas (15) hari sejak pemberitahuan tertulis.',
    'Entire Agreement - these Terms (together with any Engagement and our Kebijakan Privasi) constitute the entire agreement.':
        'Keseluruhan Perjanjian - Syarat ini (bersama dengan Engagement apapun dan Kebijakan Privasi kami) merupakan keseluruhan perjanjian.',
    'Amendments - SURIOTA may update these Terms; material changes will be notified at least 14 days in advance.':
        'Amandemen - SURIOTA dapat memperbarui Syarat ini; perubahan material akan diberitahukan paling lambat 14 hari sebelumnya.',
    'Severability - if any provision is held unenforceable, the remainder remains in effect.':
        'Severability - jika ada ketentuan yang tidak dapat ditegakkan, sisanya tetap berlaku.',
    'Assignment - you may not assign these Terms without our written consent; SURIOTA may assign to an affiliate or successor.':
        'Pengalihan - Anda tidak boleh mengalihkan Syarat ini tanpa persetujuan tertulis kami; SURIOTA boleh mengalihkan kepada afiliasi atau penerus.',
    'Force Majeure - neither party is liable for delays caused by events beyond reasonable control (natural disasters, war, pandemic, government action).':
        'Force Majeure - tidak ada pihak yang bertanggung jawab atas keterlambatan akibat peristiwa di luar kendali yang wajar (bencana alam, perang, pandemi, tindakan pemerintah).',
    'Notices - written notices to admin@suriota.com for SURIOTA, or to the address you provided.':
        'Pemberitahuan - pemberitahuan tertulis ke admin@suriota.com untuk SURIOTA, atau ke alamat yang Anda berikan.',

    # AI page remaining
    'We pick high-ROI use cases, train on your data, and deploy with confidence.':
        'Kami memilih use case ROI tinggi, training pada data Anda, dan deploy dengan percaya diri.',
    'Edge-capable, retrainable, and governed &mdash; we build AI you can audit and trust.':
        'Edge-capable, retrainable, dan ter-governance &mdash; kami build AI yang dapat Anda audit dan percaya.',
    'Edge-capable, retrainable, and governed \u2014 we build AI you can audit and trust.':
        'Edge-capable, retrainable, dan ter-governance \u2014 kami build AI yang dapat Anda audit dan percaya.',
}

PAGES = [5379, 5380, 5381, 5382]
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
$log = $upload['basedir']."/purge-legal-final2.txt";
if (file_exists($log)) { if (function_exists('code_snippets')) { code_snippets()->deactivate(5); } return; }
if (class_exists('\\\\Elementor\\\\Plugin')) {
    foreach ([5379,5380,5381,5382] as $pid) {
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
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=json.dumps({'code':purge, 'active':True, 'name':'SX: legal final2'}).encode(), method='POST', headers=HDRS), timeout=60).read()
time.sleep(3)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/id/kebijakan-privasi/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print('Purged')
