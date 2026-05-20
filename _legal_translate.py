"""Targeted Privacy + Terms full translation."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

LEGAL = {
    # ===== Privacy section headers =====
    'On this page': 'Di halaman ini',
    '1. Introduction': '1. Pendahuluan',
    '2. Data Controller': '2. Pengendali Data',
    '3. Information We Collect': '3. Informasi yang Kami Kumpulkan',
    '4. How We Use Information': '4. Bagaimana Kami Menggunakan Informasi',
    '5. Legal Basis (GDPR)': '5. Dasar Hukum (GDPR)',
    '6. Sharing & Disclosure': '6. Pembagian & Pengungkapan',
    '6. Sharing &amp; Disclosure': '6. Pembagian & Pengungkapan',
    '7. Cookies & Tracking': '7. Cookies & Tracking',
    '7. Cookies &amp; Tracking': '7. Cookies & Tracking',
    '8. Data Retention': '8. Retensi Data',
    '9. Security': '9. Keamanan',
    '10. International Transfers': '10. Transfer Internasional',
    '11. Your Rights': '11. Hak Anda',
    '12. Children\u2019s Privacy': '12. Privasi Anak',
    '13. Changes to this Policy': '13. Perubahan pada Kebijakan Ini',
    'Effective:': 'Berlaku:',
    'Last updated:': 'Terakhir diperbarui:',
    'Version:': 'Versi:',

    # Privacy body
    'PT Surya Inovasi Prioritas (\u201cSURIOTA\u201d, \u201cwe\u201d, \u201cus\u201d, or \u201cour\u201d) respects your privacy and is committed to protecting your personal data.':
        'PT Surya Inovasi Prioritas (\u201cSURIOTA\u201d, \u201ckami\u201d, \u201cmilik kami\u201d) menghormati privasi Anda dan berkomitmen melindungi data pribadi Anda.',
    'This Kebijakan Privasi explains how we collect, use, store, share, and protect personal data obtained through our website':
        'Kebijakan Privasi ini menjelaskan bagaimana kami mengumpulkan, menggunakan, menyimpan, membagikan, dan melindungi data pribadi yang diperoleh melalui website kami',
    ', our products (termasuk the SURGE platform, SRT-MGATE-1210 Modbus Gateway, ISO-M485, THM-30MD, PM1611-WD, and RS-485 Surge Protector), and any related services.':
        ', produk kami (termasuk platform SURGE, SRT-MGATE-1210 Modbus Gateway, ISO-M485, THM-30MD, PM1611-WD, dan RS-485 Surge Protector), serta layanan terkait.',
    'By accessing our website, using our products, or engaging our services, you acknowledge that you have read and understood this Kebijakan Privasi.':
        'Dengan mengakses website kami, menggunakan produk kami, atau menggunakan layanan kami, Anda mengakui bahwa Anda telah membaca dan memahami Kebijakan Privasi ini.',
    'The data controller responsible for your personal data is:': 'Pengendali data yang bertanggung jawab atas data pribadi Anda adalah:',
    '3.1 Information You Provide': '3.1 Informasi yang Anda Berikan',
    '3.2 Information Collected Automatically': '3.2 Informasi yang Dikumpulkan Otomatis',
    '3.3 Information From Third Parties': '3.3 Informasi dari Pihak Ketiga',
    'Hubungi details: name, email, phone, company, job role \u2014 when you submit RFQs, contact forms, or newsletter subscriptions.':
        'Detail kontak: nama, email, telepon, perusahaan, peran pekerjaan - saat Anda submit RFQ, formulir kontak, atau berlangganan newsletter.',
    'Proyek information: technical specifications, deployment scope, location, and compliance requirements shared during quotation or consultation.':
        'Informasi proyek: spesifikasi teknis, scope deployment, lokasi, dan requirement compliance yang dibagikan saat quotation atau konsultasi.',
    'Account credentials: if you create an account on the SURGE platform, we collect your username, hashed password, and authentication tokens.':
        'Kredensial akun: jika Anda membuat akun di platform SURGE, kami mengumpulkan username, password ter-hash, dan token autentikasi Anda.',
    'Payment data: billing address and invoice details. We do not store full credit-card numbers \u2014 payments are processed by certified third-party gateways.':
        'Data pembayaran: alamat billing dan detail invoice. Kami tidak menyimpan nomor kartu kredit lengkap - pembayaran diproses oleh gateway third-party bersertifikat.',
    'Correspondence: emails, WhatsApp messages, and call logs you exchange with our team.':
        'Korespondensi: email, pesan WhatsApp, dan log panggilan yang Anda tukarkan dengan tim kami.',
    'Device & usage: IP address, browser type, operating system, referring URL, pages visited, time on site, and clickstream data.':
        'Device & penggunaan: alamat IP, tipe browser, sistem operasi, URL referral, halaman yang dikunjungi, waktu di site, dan data clickstream.',
    'Device &amp; usage:': 'Device & penggunaan:',
    'Telemetry from products: for IoT deployments using the SURGE platform, we collect device identifiers, sensor readings, geolocation (when consented), and event logs strictly for the purpose of operating, maintaining, and improving the service.':
        'Telemetri dari produk: untuk deployment IoT menggunakan platform SURGE, kami mengumpulkan identifier device, pembacaan sensor, geolocation (saat disetujui), dan log event semata untuk tujuan mengoperasikan, memelihara, dan meningkatkan layanan.',
    'We may receive information from publicly available business directories, professional networks (e.g., LinkedIn), and our partners (e.g., distributors, integrators) when you interact with them about SURIOTA products or services.':
        'Kami dapat menerima informasi dari direktori bisnis publik, jaringan profesional (mis. LinkedIn), dan partner kami (mis. distributor, integrator) saat Anda berinteraksi dengan mereka tentang produk atau layanan SURIOTA.',
    'We use personal data for the following purposes:': 'Kami menggunakan data pribadi untuk tujuan berikut:',
    'Responding to inquiries, quotations, and providing customer support.': 'Merespons inquiry, penawaran, dan memberikan customer support.',
    'Delivering, operating, and improving our products and services (termasuk the SURGE platform).': 'Memberikan, mengoperasikan, dan meningkatkan produk dan layanan kami (termasuk platform SURGE).',
    'Marketing communications \u2014 only with your opt-in consent for the newsletter. You may unsubscribe at any time.': 'Komunikasi marketing - hanya dengan persetujuan opt-in Anda untuk newsletter. Anda dapat unsubscribe kapan saja.',
    'Compliance with legal obligations under Indonesian law and applicable foreign jurisdictions.': 'Pemenuhan kewajiban hukum sesuai hukum Indonesia dan yurisdiksi asing yang berlaku.',
    'Fraud prevention, security monitoring, and protecting our rights.': 'Pencegahan fraud, monitoring keamanan, dan perlindungan hak kami.',
    'For users in the European Economic Area, our legal bases under GDPR Article 6 are:': 'Untuk pengguna di Wilayah Ekonomi Eropa, dasar hukum kami berdasarkan GDPR Pasal 6 adalah:',
    'Contract performance \u2014 to fulfil engagement and service agreements.': 'Pelaksanaan kontrak - untuk memenuhi perjanjian engagement dan layanan.',
    'Legitimate interests \u2014 to operate our business, secure our services, and develop our products.': 'Kepentingan sah - untuk mengoperasikan bisnis kami, mengamankan layanan kami, dan mengembangkan produk kami.',
    'Consent \u2014 for marketing and optional cookies. You may withdraw consent at any time.': 'Persetujuan - untuk marketing dan cookies opsional. Anda dapat menarik persetujuan kapan saja.',
    'Legal obligation \u2014 to comply with tax, accounting, and regulatory requirements.': 'Kewajiban hukum - untuk mematuhi requirement pajak, akuntansi, dan regulasi.',
    'We do not sell personal data.': 'Kami tidak menjual data pribadi.',
    'We may share personal data with:': 'Kami dapat membagikan data pribadi dengan:',
    'Service providers processing data on our behalf (cloud hosting, email delivery, analytics, payment) under written data-processing agreements.':
        'Penyedia layanan yang memproses data atas nama kami (cloud hosting, email delivery, analytics, payment) berdasarkan perjanjian pemrosesan data tertulis.',
    'Proyek partners \u2014 integrators, certified installers, or auditors involved in delivering your proyek, only as necessary.':
        'Partner proyek - integrator, installer bersertifikat, atau auditor yang terlibat dalam pengerjaan proyek Anda, hanya sesuai kebutuhan.',
    'Government authorities when required by law (e.g., tax, KLHK reporting, customs).': 'Otoritas pemerintah saat diwajibkan hukum (mis. pajak, pelaporan KLHK, customs).',
    'Successor entities in the event of merger, acquisition, or asset transfer, with continuity of this Policy\u2019s protections.':
        'Entitas penerus dalam hal merger, akuisisi, atau transfer aset, dengan kelanjutan perlindungan Kebijakan ini.',
    'Right of access': 'Hak akses',
    'Right to rectification': 'Hak perbaikan',
    'Right to erasure': 'Hak penghapusan',
    'Right to restrict processing': 'Hak membatasi pemrosesan',
    'Right to data portability': 'Hak portabilitas data',
    'Right to object': 'Hak menolak',
    'Our services are not directed at children under 13 (or 16 in EEA). We do not knowingly collect data from minors.':
        'Layanan kami tidak ditujukan untuk anak di bawah 13 tahun (atau 16 tahun di EEA). Kami tidak dengan sengaja mengumpulkan data dari anak di bawah umur.',
    'We may update this Policy from time to time. Material changes will be notified by email or in-app notification.':
        'Kami dapat memperbarui Kebijakan ini dari waktu ke waktu. Perubahan material akan diberitahukan via email atau notifikasi in-app.',

    # Terms section headers
    '1. Definitions': '1. Definisi',
    '2. Services Provided': '2. Layanan yang Disediakan',
    '3. Account & Access': '3. Akun & Akses',
    '3. Account &amp; Access': '3. Akun & Akses',
    '4. Acceptable Use': '4. Penggunaan yang Dapat Diterima',
    '5. Intellectual Property': '5. Hak Kekayaan Intelektual',
    '6. Fees & Payment': '6. Biaya & Pembayaran',
    '6. Fees &amp; Payment': '6. Biaya & Pembayaran',
    '7. Confidentiality': '7. Kerahasiaan',
    '8. Warranties': '8. Garansi',
    '9. Disclaimer': '9. Disclaimer',
    '10. Limitation of Liability': '10. Pembatasan Liabilitas',
    '11. Indemnification': '11. Ganti Rugi',
    '12. Term & Termination': '12. Jangka Waktu & Pengakhiran',
    '12. Term &amp; Termination': '12. Jangka Waktu & Pengakhiran',
    '13. Governing Law': '13. Hukum yang Mengatur',
    '14. Dispute Resolution': '14. Penyelesaian Sengketa',
    '15. Miscellaneous': '15. Lain-lain',
    '16. Contact': '16. Hubungi',
    'These Syarat Layanan (\u201cTerms\u201d) form a binding agreement between you (\u201cyou\u201d or \u201cKlien\u201d) and PT Surya Inovasi Prioritas (\u201cSURIOTA\u201d, \u201cwe\u201d, \u201cus\u201d, or \u201cour\u201d).':
        'Syarat Layanan ini (\u201cKetentuan\u201d) membentuk perjanjian mengikat antara Anda (\u201cAnda\u201d atau \u201cKlien\u201d) dan PT Surya Inovasi Prioritas (\u201cSURIOTA\u201d, \u201ckami\u201d).',
    'By accessing our website, purchasing our products, or engaging our services, you accept these Terms.':
        'Dengan mengakses website kami, membeli produk kami, atau menggunakan layanan kami, Anda menerima Ketentuan ini.',
    'Products \u2014 SURGE platform and Hardware Products listed on our website.': 'Produk - platform SURGE dan Produk Hardware yang terdaftar di website kami.',
    'Services \u2014 engineering, integration, consultation, and SaaS offerings provided by SURIOTA, termasuk the SURGE platform.':
        'Layanan - engineering, integrasi, konsultasi, dan penawaran SaaS yang disediakan SURIOTA, termasuk platform SURGE.',
    'Engagement \u2014 a written agreement (proposal, SOW, or order form) covering specific Services.':
        'Engagement - perjanjian tertulis (proposal, SOW, atau order form) yang mencakup Layanan spesifik.',
    'Confidential Information \u2014 any non-public information disclosed by either party that should reasonably be understood to be confidential.':
        'Informasi Rahasia - informasi non-publik apapun yang diungkapkan oleh salah satu pihak yang seharusnya dipahami sebagai rahasia.',
    'SURIOTA provides IoT Industri system integration, automation, water-treatment instrumentation, renewable-energi services, electrical engineering, dan SURGE Software-as-a-Service platform for energi mapping, water analytics, and vessel tracking.':
        'SURIOTA menyediakan integrasi sistem IoT Industri, otomasi, instrumentasi water treatment, layanan renewable energi, electrical engineering, dan platform Software-as-a-Service SURGE untuk energy mapping, water analytics, dan vessel tracking.',
    'SURIOTA may modify, suspend, or discontinue any portion of the Services with reasonable notice, except where prohibited by contract.':
        'SURIOTA dapat memodifikasi, menangguhkan, atau menghentikan bagian apapun dari Layanan dengan pemberitahuan wajar, kecuali dilarang oleh kontrak.',
    'You agree to: (a) provide accurate, current information; (b) maintain the security of your credentials; (c) promptly notify us of unauthorised access; and (d) take responsibility for all activities under your account.':
        'Anda setuju untuk: (a) memberikan informasi yang akurat dan terkini; (b) menjaga keamanan kredensial Anda; (c) segera memberitahu kami tentang akses tidak sah; dan (d) bertanggung jawab atas semua aktivitas di bawah akun Anda.',
    'You agree not to:': 'Anda setuju untuk tidak:',
    'Use the Services to violate any law or regulation, termasuk export controls.':
        'Menggunakan Layanan untuk melanggar hukum atau regulasi apapun, termasuk kontrol ekspor.',
    'Upload malware, conduct security testing without prior written consent, or otherwise interfere with the integrity of our systems.':
        'Mengunggah malware, melakukan security testing tanpa persetujuan tertulis sebelumnya, atau dengan cara lain mengganggu integritas sistem kami.',
    'Resell, sublicense, or commercially exploit the Services without our written agreement.':
        'Menjual kembali, men-sublisensi, atau mengeksploitasi Layanan secara komersial tanpa perjanjian tertulis kami.',
    'Reverse-engineer or extract source code from the SURGE platform or our Hardware Products except as permitted by law.':
        'Reverse-engineer atau mengekstrak source code dari platform SURGE atau Produk Hardware kami kecuali diizinkan hukum.',
    'You retain ownership of materials you provide to us. You grant SURIOTA a licence to use such materials as necessary to perform the Services.':
        'Anda tetap memiliki kepemilikan atas materi yang Anda berikan kepada kami. Anda memberikan SURIOTA lisensi untuk menggunakan materi tersebut sesuai kebutuhan untuk melaksanakan Layanan.',
    'Pricing \u2014 as quoted in writing. Quotes are valid for 30 days unless extended.':
        'Harga - sesuai quote tertulis. Quote berlaku 30 hari kecuali diperpanjang.',
    'Payment terms \u2014 unless otherwise agreed, 50% mobilisation, 40% on delivery, 10% on final acceptance.':
        'Term pembayaran - kecuali disepakati lain, 50% mobilisasi, 40% saat pengiriman, 10% saat penerimaan akhir.',
    'Taxes \u2014 VAT (PPN), withholding tax (PPh), and other applicable taxes are added to invoiced amounts unless quoted as tax-inclusive.':
        'Pajak - PPN, PPh, dan pajak lain yang berlaku ditambahkan ke jumlah invoice kecuali di-quote sebagai tax-inclusive.',
    'Late payment \u2014 we may suspend services and charge interest at 1.5% per month on overdue balances, to the extent permitted by law.':
        'Keterlambatan pembayaran - kami dapat menangguhkan layanan dan mengenakan bunga 1.5% per bulan pada saldo lewat jatuh tempo, sejauh diizinkan hukum.',

    # ===== Common legal terms =====
    'We respect your privacy': 'Kami menghormati privasi Anda',
    'we are committed to': 'kami berkomitmen untuk',
    'shall be': 'akan',
    'subject to': 'tunduk pada',
    'with respect to': 'sehubungan dengan',
    'herein': 'di sini',
    'hereinafter': 'selanjutnya',
    'herefor': 'untuk itu',
    'thereof': 'darinya',
    'thereto': 'untuk itu',
}

# Apply to Privacy + Terms only (5379, 5380)
PAGES = [5378, 5379, 5380, 5381, 5382]  # Contact, Privacy, Terms, AI, SysInt
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
    for en, idt in LEGAL.items():
        if en in new_ed:
            new_ed = new_ed.replace(en, idt)
            changes += 1
    content_raw = d.get('content', {}).get('raw', '')
    new_content = content_raw
    for en, idt in LEGAL.items():
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
        except Exception as e: print(f'  {pid}: fail')

print(f'\nTotal: {total}')

# Purge
purge = """
$upload = wp_upload_dir();
$log = $upload['basedir']."/purge-legal.txt";
if (file_exists($log)) { if (function_exists('code_snippets')) { code_snippets()->deactivate(5); } return; }
if (class_exists('\\\\Elementor\\\\Plugin')) {
    foreach ([5378,5379,5380,5381,5382] as $pid) {
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
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=json.dumps({'code':purge, 'active':True, 'name':'SX: legal purge'}).encode(), method='POST', headers=HDRS), timeout=60).read()
time.sleep(3)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/id/kebijakan-privasi/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print('Purged')
