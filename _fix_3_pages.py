"""Fix remaining inconsistencies on ID-Portfolio, ID-Contact, ID-Terms."""
import sys, io, json, urllib.request, base64, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

FIXES = {
    # ID-Portfolio: TAHUNS → TAHUN
    5275: [
        ('>Tahuns<', '>Tahun<'),
    ],
    # ID-Contact: hero h1, breadcrumb, card labels, section h2
    5378: [
        ('Hubungi Kami with SURIOTA', 'Hubungi Kami dengan SURIOTA'),
        ('>Home<', '>Beranda<'),
        ('Fastest response \\u00b7 Direct chat', 'Respons tercepat \\u00b7 Chat langsung'),
        ('Tell us about your proyek', 'Ceritakan tentang proyek Anda'),
        # Also fix possible Mon-Fri English label if exists
        ('Mon-Fri \\u00b7', 'Sen-Jum \\u00b7'),
        ('Mon&#8211;Fri \\u00b7', 'Sen&#8211;Jum \\u00b7'),
    ],
    # ID-Terms: subtitle typo + TOC translations
    5380: [
        # Subtitle typo + English
        ('Mohon bacaead carefully.', 'Mohon baca dengan teliti.'),
        # TOC items
        ('>1. Acceptance of Terms<', '>1. Penerimaan Syarat<'),
        ('>2. Definitions<', '>2. Definisi<'),
        ('>3. Services Description<', '>3. Deskripsi Layanan<'),
        ('>4. Accounts &amp; Registration<', '>4. Akun &amp; Registrasi<'),
        ('>5. Acceptable Use<', '>5. Penggunaan yang Dapat Diterima<'),
        ('>6. Intellectual Property<', '>6. Kekayaan Intelektual<'),
        ('>7. Fees &amp; Payment<', '>7. Biaya &amp; Pembayaran<'),
        ('>8. Confidentiality<', '>8. Kerahasiaan<'),
        ('>9. Warranties &amp; Disclaimers<', '>9. Garansi &amp; Disclaimer<'),
        # Main h2 (h2 inside section) — same texts so will be matched too
        ('<h2>1. Acceptance of Terms</h2>', '<h2>1. Penerimaan Syarat</h2>'),
        ('<h2>2. Definitions</h2>', '<h2>2. Definisi</h2>'),
        ('<h2>3. Services Description</h2>', '<h2>3. Deskripsi Layanan</h2>'),
        ('<h2>4. Accounts &amp; Registration</h2>', '<h2>4. Akun &amp; Registrasi</h2>'),
        ('<h2>5. Acceptable Use</h2>', '<h2>5. Penggunaan yang Dapat Diterima</h2>'),
        ('<h2>6. Intellectual Property</h2>', '<h2>6. Kekayaan Intelektual</h2>'),
        ('<h2>7. Fees &amp; Payment</h2>', '<h2>7. Biaya &amp; Pembayaran</h2>'),
        ('<h2>8. Confidentiality</h2>', '<h2>8. Kerahasiaan</h2>'),
        ('<h2>9. Warranties &amp; Disclaimers</h2>', '<h2>9. Garansi &amp; Disclaimer</h2>'),
        # Same as escaped form
        ('<h2>1. Acceptance of Terms<\\/h2>', '<h2>1. Penerimaan Syarat<\\/h2>'),
        ('<h2>2. Definitions<\\/h2>', '<h2>2. Definisi<\\/h2>'),
        ('<h2>3. Services Description<\\/h2>', '<h2>3. Deskripsi Layanan<\\/h2>'),
        ('<h2>4. Accounts &amp; Registration<\\/h2>', '<h2>4. Akun &amp; Registrasi<\\/h2>'),
        ('<h2>5. Acceptable Use<\\/h2>', '<h2>5. Penggunaan yang Dapat Diterima<\\/h2>'),
        ('<h2>6. Intellectual Property<\\/h2>', '<h2>6. Kekayaan Intelektual<\\/h2>'),
        ('<h2>7. Fees &amp; Payment<\\/h2>', '<h2>7. Biaya &amp; Pembayaran<\\/h2>'),
        ('<h2>8. Confidentiality<\\/h2>', '<h2>8. Kerahasiaan<\\/h2>'),
        ('<h2>9. Warranties &amp; Disclaimers<\\/h2>', '<h2>9. Garansi &amp; Disclaimer<\\/h2>'),
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
        else:
            miss.append((pid, old[:60]))
    if new_ed != ed:
        payload = json.dumps({'meta': {'_elementor_data': new_ed}}).encode()
        urllib.request.urlopen(urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}', data=payload, method='POST', headers=HDRS), timeout=30).read()
        print(f'  {pid}: +{page_changes}')
        total += page_changes

print(f'\nTotal: {total}')
if miss:
    print(f'\nMisses ({len(miss)}):')
    for pid, t in miss[:15]:
        print(f'  {pid}: "{t}"')

urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/elementor/v1/cache', method='DELETE', headers=HDRS), timeout=30).read()
time.sleep(2)
for url in ['https://suriota.com/id/portfolio-id/', 'https://suriota.com/id/kontak/', 'https://suriota.com/id/syarat-layanan/']:
    urllib.request.urlopen(urllib.request.Request(url+'?nc='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=30).read()
print('Done')
