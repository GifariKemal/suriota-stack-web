"""Translate legal boilerplate on ID-Terms + ID-Privacy."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

FIXES = {
    # ID-Terms (5380)
    5380: [
        # Section 1 intro (with escaped quotes)
        (r'These Syarat Layanan (\u201c<strong>Terms<\/strong>\u201d) form a binding agreement between you (\u201cyou\u201d or \u201cKlien\u201d) and PT Surya Inovasi Prioritas (\u201c<strong>SURIOTA<\/strong>\u201d, \u201cwe\u201d, \u201cus\u201d, or \u201cour\u201d). By accessing our website, purchasing our products, or using our services, you agree to be bound by these Terms together with our',
         r'Syarat Layanan ini (\u201c<strong>Syarat<\/strong>\u201d) merupakan perjanjian mengikat antara Anda (\u201cAnda\u201d atau \u201cKlien\u201d) dan PT Surya Inovasi Prioritas (\u201c<strong>SURIOTA<\/strong>\u201d, \u201ckami\u201d). Dengan mengakses website kami, membeli produk kami, atau menggunakan layanan kami, Anda menyetujui untuk terikat oleh Syarat ini bersama'),

        # Section 3 broken auto-translation
        ('manajemen energiergipping, vessel tracking, and water analytics. Specific scope, deliverables, timelines, and acceptance criteria are defined in the applicable Statement of Work or service plan.',
         'manajemen energi, vessel tracking, dan water analytics. Scope spesifik, deliverables, timeline, dan acceptance criteria ditentukan dalam Statement of Work atau service plan yang berlaku.'),

        # Section 6.1 license grant
        ('We grant you a non-exclusive, non-transferable licence to use the Products and Services solely for their intended business purpose.',
         'Kami memberikan Anda lisensi non-eksklusif dan tidak dapat dialihkan untuk menggunakan Produk dan Layanan semata-mata untuk tujuan bisnis yang dimaksud.'),

        # Section 11 indemnification (broken "wajarnable")
        ('termasuk biaya wajarnable legal fees) arising from: (a) your breach of these Terms; (b) your misuse of the Services or Products; (c) your violation of any law or third-party right; or (d) materials you provided to us.',
         'termasuk biaya legal yang wajar) yang timbul dari: (a) pelanggaran Anda atas Syarat ini; (b) penyalahgunaan Layanan atau Produk oleh Anda; (c) pelanggaran hukum atau hak pihak ketiga oleh Anda; atau (d) materi yang Anda berikan kepada kami.'),

        # Section 14 arbitration
        ('sengketa akan diajukan ke bindingg arbitration administered by the Indonesian National Arbitration Board (BANI) in Jakarta, in the English language. The arbitral award akan final and binding. Nothing in this section prevents either party from seeking injunctive relief in court for IP or confidentiality breaches.',
         'sengketa akan diajukan ke arbitrase mengikat yang diadministrasikan oleh Badan Arbitrase Nasional Indonesia (BANI) di Jakarta, dalam bahasa Inggris. Putusan arbitrase bersifat final dan mengikat. Tidak ada dalam pasal ini yang menghalangi pihak manapun untuk mencari upaya hukum injungtif di pengadilan untuk pelanggaran IP atau kerahasiaan.'),

        # Section 6.2 h3
        (r'<h3>6.2 Klien Materials<\/h3>', r'<h3>6.2 Materi Klien<\/h3>'),
        # Section 6.3 h3
        (r'<h3>6.3 Deliverables<\/h3>', r'<h3>6.3 Deliverables<\/h3>'),  # keep as legal term

        # Definitions list (Section 2)
        ('<strong>Services<\\/strong> - engineering, integrasi, konsultasi, dan penawaran SaaS yang disediakan oleh SURIOTA, termasuk platform SURGE.',
         '<strong>Layanan<\\/strong> - engineering, integrasi, konsultasi, dan penawaran SaaS yang disediakan oleh SURIOTA, termasuk platform SURGE.'),
        ('<strong>Products<\\/strong> - hardware manufactured or distributed by SURIOTA',
         '<strong>Produk<\\/strong> - hardware yang diproduksi atau didistribusikan oleh SURIOTA'),
        (', and successors).', ', dan penerusnya).'),
        ('<strong>Engagement<\\/strong> - a proyek, support contract, or subscription agreed in writing (Statement of Work, Purchase Order, or service plan).',
         '<strong>Engagement<\\/strong> - proyek, kontrak support, atau langganan yang disepakati tertulis (Statement of Work, Purchase Order, atau service plan).'),
        ('<strong>Deliverables<\\/strong> - documents, designs, code, configurations, reports, or installed equipment produced under an Engagement.',
         '<strong>Deliverables<\\/strong> - dokumen, desain, kode, konfigurasi, laporan, atau peralatan terpasang yang dihasilkan dalam suatu Engagement.'),
        ('<strong>Confidential Information<\\/strong> - any non-public information disclosed by either party that should reasonably be understood to be confidential.',
         '<strong>Informasi Rahasia<\\/strong> - informasi non-publik apapun yang diungkapkan oleh salah satu pihak yang sepatutnya dipahami sebagai rahasia.'),
    ],

    # ID-Privacy (5379)
    5379: [
        # Section 9 security (broken "stafining")
        ('training stafining. While we strive to safeguard your data, no method of transmission or storage is 100% secure; we will notify you and the relevant authority within 72 hours of becoming aware of a personal-data breach that materially affects your rights.',
         'training staf. Meskipun kami berupaya melindungi data Anda, tidak ada metode transmisi atau penyimpanan yang 100% aman; kami akan memberitahu Anda dan otoritas terkait dalam 72 jam setelah mengetahui pelanggaran data pribadi yang secara material mempengaruhi hak Anda.'),
        # Section 10 h2 if still English
        (r'<h2>10. International Data Transfers<\/h2>', r'<h2>10. Transfer Data Internasional<\/h2>'),
    ],
}

total = 0
miss = []
for pid, pairs in FIXES.items():
    r = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}?context=edit&_fields=meta', headers=HDRS)
    d = json.loads(urllib.request.urlopen(r, timeout=30).read())
    ed = d.get('meta',{}).get('_elementor_data','')
    if isinstance(ed, list): ed = json.dumps(ed)
    if not isinstance(ed, str): continue
    new_ed = ed
    page_changes = 0
    for old, new in pairs:
        c = new_ed.count(old)
        if c > 0:
            new_ed = new_ed.replace(old, new)
            page_changes += c
            print(f'  {pid}: +{c} "{old[:60]}..."')
        else:
            miss.append((pid, old[:80]))
    if new_ed != ed:
        payload = json.dumps({'meta': {'_elementor_data': new_ed}}).encode()
        urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}', data=payload, method='POST', headers=HDRS), timeout=30).read()
        print(f'  ✓ {pid} updated: +{page_changes}')
        total += page_changes

print(f'\nTotal: {total}')
if miss:
    print(f'Misses ({len(miss)}):')
    for pid, t in miss:
        print(f'  {pid}: {t}')

urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/elementor/v1/cache', method='DELETE', headers=HDRS), timeout=30).read()
time.sleep(2)
for url in ['https://suriota.com/id/syarat-layanan/', 'https://suriota.com/id/kebijakan-privasi/']:
    urllib.request.urlopen(urllib.request.Request(url+'?nc='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read()
print('Done')
