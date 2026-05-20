"""Final push — Privacy/Terms/AI/SysInt remaining English."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

FINAL = {
    # ===== Privacy =====
    'How PT Surya Inovasi Prioritas (SURIOTA) collects, uses, and protects your personal data. This policy is aligned with Indonesia\u2019s Personal Data Protection Law (UU PDP No.27/2022) and the EU General Da':
        'Bagaimana PT Surya Inovasi Prioritas (SURIOTA) mengumpulkan, menggunakan, dan melindungi data pribadi Anda. Kebijakan ini selaras dengan Undang-Undang Perlindungan Data Pribadi Indonesia (UU PDP No.27/2022) dan EU General Da',
    'PT Surya Inovasi Prioritas (\u201cSURIOTA\u201d, \u201cwe\u201d, \u201cus\u201d, or \u201cour\u201d) respects your privacy and is committed to protecting your personal data.':
        'PT Surya Inovasi Prioritas (\u201cSURIOTA\u201d, \u201ckami\u201d, \u201cmilik kami\u201d) menghormati privasi Anda dan berkomitmen melindungi data pribadi Anda.',
    'Account credentials: if you create an account on the SURGE platform, we collect your username, hashed password, and authentication tokens.':
        'Kredensial akun: jika Anda membuat akun di platform SURGE, kami mengumpulkan username, password ter-hash, dan token autentikasi Anda.',
    'Payment data: billing address and invoice details. We do not store full credit-card numbers':
        'Data pembayaran: alamat billing dan detail invoice. Kami tidak menyimpan nomor kartu kredit lengkap',
    'Payment data: billing address and invoice details.': 'Data pembayaran: alamat billing dan detail invoice.',
    'We do not store full credit-card numbers':
        'Kami tidak menyimpan nomor kartu kredit lengkap',
    'payments are processed by certified third-party gateways.': 'pembayaran diproses oleh gateway third-party bersertifikat.',
    'Correspondence: emails, WhatsApp messages, and call logs you exchange with our team.':
        'Korespondensi: email, pesan WhatsApp, dan log panggilan yang Anda tukarkan dengan tim kami.',
    'Device & penggunaan: IP address, browser type, operating system, referring URL, pages visited, time on site, and clickstream data.':
        'Device & penggunaan: alamat IP, tipe browser, sistem operasi, URL referral, halaman yang dikunjungi, waktu di site, dan data clickstream.',
    'IP address, browser type, operating system, referring URL, pages visited, time on site, and clickstream data.':
        'alamat IP, tipe browser, sistem operasi, URL referral, halaman yang dikunjungi, waktu di site, dan data clickstream.',
    'Telemetry from products: for IoT deployments using the SURGE platform, we collect device identifiers, sensor readings, geolocation (when consented), and event logs strictly for the purpose of operatin':
        'Telemetri dari produk: untuk deployment IoT menggunakan platform SURGE, kami mengumpulkan identifier device, pembacaan sensor, geolocation (saat disetujui), dan log event semata untuk tujuan operasional',
    'Marketing communications - only with your opt-in consent for the newsletter. You may unsubscribe at any time.':
        'Komunikasi marketing - hanya dengan persetujuan opt-in Anda untuk newsletter. Anda dapat unsubscribe kapan saja.',
    'Marketing communications \u2014 only with your opt-in consent for the newsletter. You may unsubscribe at any time.':
        'Komunikasi marketing - hanya dengan persetujuan opt-in Anda untuk newsletter. Anda dapat unsubscribe kapan saja.',
    'Contract performance - to fulfil engagement and service agreements.': 'Pelaksanaan kontrak - untuk memenuhi perjanjian engagement dan layanan.',
    'Contract performance \u2014 to fulfil engagement and service agreements.': 'Pelaksanaan kontrak - untuk memenuhi perjanjian engagement dan layanan.',
    'Legitimate interests - to operate our business, secure our services, and develop our products.': 'Kepentingan sah - untuk mengoperasikan bisnis kami, mengamankan layanan kami, dan mengembangkan produk kami.',
    'Legitimate interests \u2014 to operate our business, secure our services, and develop our products.': 'Kepentingan sah - untuk mengoperasikan bisnis kami, mengamankan layanan kami, dan mengembangkan produk kami.',
    'Consent - for marketing and optional cookies. You may withdraw consent at any time.': 'Persetujuan - untuk marketing dan cookies opsional. Anda dapat menarik persetujuan kapan saja.',
    'Consent \u2014 for marketing and optional cookies. You may withdraw consent at any time.': 'Persetujuan - untuk marketing dan cookies opsional. Anda dapat menarik persetujuan kapan saja.',
    'Legal obligation - to comply with tax, accounting, and regulatory requirements.': 'Kewajiban hukum - untuk mematuhi requirement pajak, akuntansi, dan regulasi.',
    'Legal obligation \u2014 to comply with tax, accounting, and regulatory requirements.': 'Kewajiban hukum - untuk mematuhi requirement pajak, akuntansi, dan regulasi.',
    'Service providers processing data on our behalf (cloud hosting, email delivery, analytics, payment) under written data-processing agreements.':
        'Penyedia layanan yang memproses data atas nama kami (cloud hosting, email delivery, analytics, payment) berdasarkan perjanjian pemrosesan data tertulis.',
    'Successor entities in the event of merger, acquisition, or asset transfer, with continuity of this Policy\u2019s protections.':
        'Entitas penerus dalam hal merger, akuisisi, atau transfer aset, dengan kelanjutan perlindungan Kebijakan ini.',
    'Analytics cookies - to understand traffic and improve content (e.g., Google Analytics). You may opt out via your browser settings.':
        'Analytics cookies - untuk memahami traffic dan meningkatkan konten (mis. Google Analytics). Anda dapat opt out via setting browser.',
    'Analytics cookies \u2014 to understand traffic and improve content (e.g., Google Analytics). You may opt out via your browser settings.':
        'Analytics cookies - untuk memahami traffic dan meningkatkan konten (mis. Google Analytics). Anda dapat opt out via setting browser.',
    'Most browsers allow you to refuse or delete cookies. Disabling strictly-necessary cookies may impact site functionality.':
        'Sebagian besar browser memungkinkan Anda menolak atau menghapus cookies. Menonaktifkan cookies yang strictly-necessary dapat mempengaruhi fungsi site.',
    'We retain personal data only as long as necessary for the purposes for which it was collected, or as required by law:':
        'Kami menyimpan data pribadi hanya selama diperlukan untuk tujuan pengumpulannya, atau sesuai kebutuhan hukum:',
    'Lead & inquiry data: up to 24 months from last interaction.':
        'Data lead & inquiry: hingga 24 bulan dari interaksi terakhir.',
    'Pelanggan / proyek records: for the duration of the engagement plus 10 years (Indonesian commercial-records requirement).':
        'Record pelanggan / proyek: selama durasi engagement plus 10 tahun (requirement record komersial Indonesia).',
    'We implement technical and organisational measures termasuk encryption in transit (TLS 1.2+), encryption at rest, role-based access controls, audit logging, regular security assessments, and staff tra':
        'Kami menerapkan ukuran teknis dan organisasi termasuk enkripsi dalam transit (TLS 1.2+), enkripsi at rest, akses kontrol berbasis peran, audit logging, security assessment berkala, dan training staf',
    'Some of our service providers may process data outside Indonesia. When transferring personal data internationally, we ensure adequate protection through Standard Contractual Clauses (SCCs), adequacy d':
        'Beberapa penyedia layanan kami dapat memproses data di luar Indonesia. Saat transfer data pribadi secara internasional, kami memastikan perlindungan memadai melalui Standard Contractual Clauses (SCC), keputusan',
    'Under UU PDP No.27/2022 (Indonesia) and GDPR (EU), you have the right to:':
        'Berdasarkan UU PDP No.27/2022 (Indonesia) dan GDPR (UE), Anda berhak untuk:',
    'Access - obtain confirmation of and a copy of your data we hold.':
        'Akses - mendapatkan konfirmasi dan salinan data Anda yang kami simpan.',
    'Access \u2014 obtain confirmation of and a copy of your data we hold.':
        'Akses - mendapatkan konfirmasi dan salinan data Anda yang kami simpan.',
    'Objection - object to processing based on legitimate interests, termasuk profiling for marketing.':
        'Keberatan - menolak pemrosesan berdasarkan kepentingan sah, termasuk profiling untuk marketing.',
    'Objection \u2014 object to processing based on legitimate interests, termasuk profiling for marketing.':
        'Keberatan - menolak pemrosesan berdasarkan kepentingan sah, termasuk profiling untuk marketing.',
    'Our services are intended for businesses and adult professionals. We do not knowingly collect personal data from individuals under 18 years of age. If you believe a minor has provided us with personal':
        'Layanan kami ditujukan untuk bisnis dan profesional dewasa. Kami tidak dengan sengaja mengumpulkan data pribadi dari individu di bawah 18 tahun. Jika Anda yakin anak di bawah umur telah memberi kami data pribadi',
    'We may update this Kebijakan Privasi from time to time. The latest version will always be posted on this page, with the \u201cLast updated\u201d date revised. Material changes will be communicated by email or p':
        'Kami dapat memperbarui Kebijakan Privasi ini dari waktu ke waktu. Versi terbaru akan selalu dipublikasikan di halaman ini, dengan tanggal \u201cTerakhir diperbarui\u201d direvisi. Perubahan material akan dikomunikasikan via email atau p',

    # ===== Terms =====
    'These Syarat Layanan (\u201cTerms\u201d) form a binding agreement between you (\u201cyou\u201d or \u201cKlien\u201d) and PT Surya Inovasi Prioritas (\u201cSURIOTA\u201d, \u201cwe\u201d, \u201cus\u201d, or \u201cour\u201d). By accessing our website, purchasing our produc':
        'Syarat Layanan ini (\u201cKetentuan\u201d) membentuk perjanjian mengikat antara Anda (\u201cAnda\u201d atau \u201cKlien\u201d) dan PT Surya Inovasi Prioritas (\u201cSURIOTA\u201d, \u201ckami\u201d). Dengan mengakses website kami, membeli produ',
    'Services - engineering, integration, consultation, and SaaS offerings provided by SURIOTA, termasuk the SURGE platform.':
        'Layanan - engineering, integrasi, konsultasi, dan penawaran SaaS yang disediakan SURIOTA, termasuk platform SURGE.',
    'Services \u2014 engineering, integration, consultation, and SaaS offerings provided by SURIOTA, termasuk the SURGE platform.':
        'Layanan - engineering, integrasi, konsultasi, dan penawaran SaaS yang disediakan SURIOTA, termasuk platform SURGE.',
    'SURIOTA menyediakan integrasi sistem IoT Industri, otomasi, instrumentasi water treatment, layanan renewable energi, electrical engineering, dan platform Software-as-a-Service SURGE untuk manajemen en':
        'SURIOTA menyediakan integrasi sistem IoT Industri, otomasi, instrumentasi water treatment, layanan renewable energi, electrical engineering, dan platform Software-as-a-Service SURGE untuk manajemen energi',
    'All firmware, software, designs, schematics, documentation, trademarks, and know-how created or owned by SURIOTA - termasuk the SURGE platform and all Products - remain the exclusive property of SURIO':
        'Seluruh firmware, software, desain, skematik, dokumentasi, trademark, dan know-how yang dibuat atau dimiliki SURIOTA - termasuk platform SURGE dan semua Produk - tetap menjadi milik eksklusif SURIO',
    'All firmware, software, designs, schematics, documentation, trademarks, and know-how created or owned by SURIOTA \u2014 termasuk the SURGE platform and all Products \u2014 remain the exclusive property of SURIO':
        'Seluruh firmware, software, desain, skematik, dokumentasi, trademark, dan know-how yang dibuat atau dimiliki SURIOTA - termasuk platform SURGE dan semua Produk - tetap menjadi milik eksklusif SURIO',
    'Pricing - as quoted in writing. Quotes are valid for 30 days unless extended.':
        'Harga - sesuai quote tertulis. Quote berlaku 30 hari kecuali diperpanjang.',
    'Pricing \u2014 as quoted in writing. Quotes are valid for 30 days unless extended.':
        'Harga - sesuai quote tertulis. Quote berlaku 30 hari kecuali diperpanjang.',
    'Taxes - VAT (PPN), withholding tax (PPh), and other applicable taxes are added to invoiced amounts unless quoted as tax-inclusive.':
        'Pajak - PPN, PPh, dan pajak lain yang berlaku ditambahkan ke jumlah invoice kecuali di-quote sebagai tax-inclusive.',
    'Taxes \u2014 VAT (PPN), withholding tax (PPh), and other applicable taxes are added to invoiced amounts unless quoted as tax-inclusive.':
        'Pajak - PPN, PPh, dan pajak lain yang berlaku ditambahkan ke jumlah invoice kecuali di-quote sebagai tax-inclusive.',
    'Late payment - we may suspend services and charge interest at 1.5% per month on overdue balances, to the extent permitted by law.':
        'Keterlambatan pembayaran - kami dapat menangguhkan layanan dan mengenakan bunga 1.5% per bulan pada saldo lewat jatuh tempo, sejauh diizinkan hukum.',
    'Late payment \u2014 we may suspend services and charge interest at 1.5% per month on overdue balances, to the extent permitted by law.':
        'Keterlambatan pembayaran - kami dapat menangguhkan layanan dan mengenakan bunga 1.5% per bulan pada saldo lewat jatuh tempo, sejauh diizinkan hukum.',
    'Each party will protect the other\u2019s Confidential Information with the same degree of care it uses to protect its own (no less than reasonable care), use it solely to perform the Engagement, and not di':
        'Setiap pihak akan melindungi Informasi Rahasia pihak lain dengan tingkat perhatian yang sama yang digunakan untuk melindungi miliknya (tidak kurang dari perhatian wajar), menggunakannya hanya untuk Engagement, dan tidak meng',
    'Kami menjamin bahwa Layanan akan dilaksanakan secara profesional dan terampil sesuai standar industri. Produk Hardware membawa periode garansi yang ditentukan manufacturer sebagaimana tercetakd on the':
        'Kami menjamin bahwa Layanan akan dilaksanakan secara profesional dan terampil sesuai standar industri. Produk Hardware membawa periode garansi yang ditentukan manufacturer sebagaimana tercetak di',
    'EXCEPT AS EXPRESSLY STATED, THE SERVICES AND PRODUCTS ARE PROVIDED \u201cAS IS\u201d AND \u201cAS AVAILABLE\u201d, WITHOUT WARRANTIES OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING MERCHANTABILITY, FITNESS FOR A PARTICULAR P':
        'KECUALI DINYATAKAN SECARA TEGAS, LAYANAN DAN PRODUK DISEDIAKAN \u201cAS IS\u201d DAN \u201cAS AVAILABLE\u201d, TANPA JAMINAN APAPUN, TERSURAT MAUPUN TERSIRAT, TERMASUK MERCHANTABILITY, KESESUAIAN UNTUK TUJUAN TERTENTU',
    'TO THE MAXIMUM EXTENT PERMITTED BY LAW, SURIOTA\u2019S TOTAL CUMULATIVE LIABILITY ARISING OUT OF OR RELATED TO THESE TERMS OR ANY ENGAGEMENT SHALL NOT EXCEED THE AMOUNT PAID BY YOU TO SURIOTA UNDER THE APP':
        'SEJAUH MAKSIMUM YANG DIIZINKAN HUKUM, TOTAL LIABILITAS KUMULATIF SURIOTA YANG TIMBUL DARI ATAU TERKAIT KETENTUAN INI ATAU ENGAGEMENT APAPUN TIDAK MELEBIHI JUMLAH YANG ANDA BAYAR KE SURIOTA DI BAWAH ENGAGEMENT',
    'IN NO EVENT SHALL SURIOTA BE LIABLE FOR INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, OR FOR LOSS OF PROFITS, REVENUE, DATA, OR USE - EVEN IF ADVISED OF THE POSSIBILITY.':
        'DALAM SITUASI APAPUN SURIOTA TIDAK BERTANGGUNG JAWAB ATAS KERUGIAN TIDAK LANGSUNG, INSIDENTAL, KHUSUS, KONSEKUENSIAL, ATAU PUNITIF, ATAU KEHILANGAN KEUNTUNGAN, REVENUE, DATA, ATAU PENGGUNAAN - BAHKAN JIKA DIBERITAHU TENTANG KEMUNGKINANNYA.',
    'IN NO EVENT SHALL SURIOTA BE LIABLE FOR INDIRECT, INCIDENTAL, SPECIAL, CONSEQUENTIAL, OR PUNITIVE DAMAGES, OR FOR LOSS OF PROFITS, REVENUE, DATA, OR USE \u2014 EVEN IF ADVISED OF THE POSSIBILITY.':
        'DALAM SITUASI APAPUN SURIOTA TIDAK BERTANGGUNG JAWAB ATAS KERUGIAN TIDAK LANGSUNG, INSIDENTAL, KHUSUS, KONSEKUENSIAL, ATAU PUNITIF, ATAU KEHILANGAN KEUNTUNGAN, REVENUE, DATA, ATAU PENGGUNAAN - BAHKAN JIKA DIBERITAHU TENTANG KEMUNGKINANNYA.',
    'These Terms remain in effect while you use the Services. Either party may terminate an Engagement with thirty (30) days\u2019 written notice, or immediately for material breach not cured within fifteen (15':
        'Ketentuan ini tetap berlaku selama Anda menggunakan Layanan. Salah satu pihak dapat mengakhiri Engagement dengan pemberitahuan tertulis tiga puluh (30) hari, atau segera untuk pelanggaran material yang tidak diperbaiki dalam lima belas (15',
    'Entire Agreement - these Terms (together with any Engagement and our Kebijakan Privasi) constitute the entire agreement.':
        'Perjanjian Lengkap - Ketentuan ini (bersama Engagement apapun dan Kebijakan Privasi kami) merupakan perjanjian lengkap.',
    'Entire Agreement \u2014 these Terms (together with any Engagement and our Kebijakan Privasi) constitute the entire agreement.':
        'Perjanjian Lengkap - Ketentuan ini (bersama Engagement apapun dan Kebijakan Privasi kami) merupakan perjanjian lengkap.',
    'Severability - if any provision is held unenforceable, the remainder remains in effect.':
        'Severabilitas - jika ada ketentuan yang tidak dapat ditegakkan, sisanya tetap berlaku.',
    'Severability \u2014 if any provision is held unenforceable, the remainder remains in effect.':
        'Severabilitas - jika ada ketentuan yang tidak dapat ditegakkan, sisanya tetap berlaku.',
    'Assignment - you may not assign these Terms without our written consent; SURIOTA may assign to an affiliate or successor.':
        'Pengalihan - Anda tidak boleh mengalihkan Ketentuan ini tanpa persetujuan tertulis kami; SURIOTA dapat mengalihkan ke afiliasi atau penerus.',
    'Assignment \u2014 you may not assign these Terms without our written consent; SURIOTA may assign to an affiliate or successor.':
        'Pengalihan - Anda tidak boleh mengalihkan Ketentuan ini tanpa persetujuan tertulis kami; SURIOTA dapat mengalihkan ke afiliasi atau penerus.',
    'Force Majeure - neither party is liable for delays caused by events beyond reasonable control (natural disasters, war, pandemic, government action).':
        'Force Majeure - tidak ada pihak yang bertanggung jawab atas keterlambatan akibat kejadian di luar kontrol wajar (bencana alam, perang, pandemi, tindakan pemerintah).',
    'Force Majeure \u2014 neither party is liable for delays caused by events beyond reasonable control (natural disasters, war, pandemic, government action).':
        'Force Majeure - tidak ada pihak yang bertanggung jawab atas keterlambatan akibat kejadian di luar kontrol wajar (bencana alam, perang, pandemi, tindakan pemerintah).',
    'Notices - written notices to admin@suriota.com for SURIOTA, or to the address you provided.':
        'Pemberitahuan - pemberitahuan tertulis ke admin@suriota.com untuk SURIOTA, atau ke alamat yang Anda berikan.',
    'Notices \u2014 written notices to admin@suriota.com for SURIOTA, or to the address you provided.':
        'Pemberitahuan - pemberitahuan tertulis ke admin@suriota.com untuk SURIOTA, atau ke alamat yang Anda berikan.',
    'Questions about these Terms? We are happy to clarify before you commit.':
        'Pertanyaan tentang Ketentuan ini? Kami senang mengklarifikasi sebelum Anda commit.',

    # ===== AI page =====
    'Production-grade AI for industrial use cases. Predictive maintenance, computer vision QC, anomaly detection - built on your data, deployed on your terms.':
        'AI grade produksi untuk use case industri. Predictive maintenance, computer vision QC, deteksi anomali - dibangun di atas data Anda, di-deploy sesuai term Anda.',
    'Production-grade AI for industrial use cases. Predictive maintenance, computer vision QC, anomaly detection \u2014 built on your data, deployed on your terms.':
        'AI grade produksi untuk use case industri. Predictive maintenance, computer vision QC, deteksi anomali - dibangun di atas data Anda, di-deploy sesuai term Anda.',
    'Many industrial AI proyek die in POC. SURIOTA treats AI like any other engineering discipline - with version control, observability, model registries, and SLA. We pick high-ROI use cases, train on you':
        'Banyak proyek AI industri mati di POC. SURIOTA memperlakukan AI seperti disiplin engineering lainnya - dengan version control, observability, model registry, dan SLA. Kami pilih use case ROI-tinggi, train pada',
    'Many industrial AI proyek die in POC. SURIOTA treats AI like any other engineering discipline \u2014 with version control, observability, model registries, and SLA. We pick high-ROI use cases, train on you':
        'Banyak proyek AI industri mati di POC. SURIOTA memperlakukan AI seperti disiplin engineering lainnya - dengan version control, observability, model registry, dan SLA. Kami pilih use case ROI-tinggi, train pada',
    'Edge-capable, retrainable, and governed - we build AI you can audit and trust.':
        'Edge-capable, retrainable, dan ter-governance - kami build AI yang bisa Anda audit dan percaya.',
    'Edge-capable, retrainable, and governed \u2014 we build AI you can audit and trust.':
        'Edge-capable, retrainable, dan ter-governance - kami build AI yang bisa Anda audit dan percaya.',
    'Free initial consultation - share your data and use case, our ML team responds within 24 hours with a feasibility check termasuk data sufficiency, baseline, and target metrics.':
        'Konsultasi awal gratis - bagikan data dan use case Anda, tim ML kami merespon dalam 24 jam dengan feasibility check termasuk kecukupan data, baseline, dan target metrik.',
    'Free initial consultation \u2014 share your data and use case, our ML team responds within 24 hours with a feasibility check termasuk data sufficiency, baseline, and target metrics.':
        'Konsultasi awal gratis - bagikan data dan use case Anda, tim ML kami merespon dalam 24 jam dengan feasibility check termasuk kecukupan data, baseline, dan target metrik.',

    # ===== SysInt =====
    'Most industrial operations run a patchwork of vendor systems: PLCs from one brand, SCADA from another, an ERP that does not talk to either. SURIOTA designs integration architectures - data buses, APIs':
        'Sebagian besar operasi industri menjalankan campuran sistem vendor: PLC dari satu brand, SCADA dari brand lain, ERP yang tidak terhubung keduanya. SURIOTA merancang arsitektur integrasi - data bus, API',
    'Most industrial operations run a patchwork of vendor systems: PLCs from one brand, SCADA from another, an ERP that does not talk to either. SURIOTA designs integration architectures \u2014 data buses, APIs':
        'Sebagian besar operasi industri menjalankan campuran sistem vendor: PLC dari satu brand, SCADA dari brand lain, ERP yang tidak terhubung keduanya. SURIOTA merancang arsitektur integrasi - data bus, API',
    'Free initial consultation - share your stack, our engineering team responds within 24 hours with a phased integration plan that minimises operational risk.':
        'Konsultasi awal gratis - bagikan stack Anda, tim engineer kami merespon dalam 24 jam dengan rencana integrasi berfase yang meminimalkan risiko operasional.',
    'Free initial consultation \u2014 share your stack, our engineering team responds within 24 hours with a phased integration plan that minimises operational risk.':
        'Konsultasi awal gratis - bagikan stack Anda, tim engineer kami merespon dalam 24 jam dengan rencana integrasi berfase yang meminimalkan risiko operasional.',
}

PAGES = [5379, 5380, 5381, 5382]  # Privacy, Terms, AI, SysInt
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
    for en, idt in FINAL.items():
        if en in new_ed:
            new_ed = new_ed.replace(en, idt)
            changes += 1
    content_raw = d.get('content', {}).get('raw', '')
    new_content = content_raw
    for en, idt in FINAL.items():
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
$log = $upload['basedir']."/purge-legal-final.txt";
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
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=json.dumps({'code':purge, 'active':True, 'name':'SX: legal final'}).encode(), method='POST', headers=HDRS), timeout=60).read()
time.sleep(3)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/id/kebijakan-privasi/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print('Purged')
