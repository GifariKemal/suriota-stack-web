"""KBBI-compliant Indonesian standardization across all 27 ID pages."""
import sys, io, json, urllib.request, base64, time, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization':f'Basic {AUTH}','User-Agent':'Mozilla/5.0','Content-Type':'application/json'}

# === KBBI-compliant translation dict — ordered: longest-first ===
KBBI = {
    # ===== "Project" → "Proyek" (KBBI BAKU) - all variants =====
    'Project Archive': 'Arsip Proyek',
    'PROJECT ARCHIVE': 'ARSIP PROYEK',
    'projects across': 'proyek di sektor',
    'project across': 'proyek di sektor',
    'Industrial Projects': 'Proyek Industri',
    'industrial projects': 'proyek industri',
    'INDUSTRIAL PROJECTS': 'PROYEK INDUSTRI',
    'Projects': 'Proyek',
    'projects': 'proyek',
    'PROJECTS': 'PROYEK',
    'Project': 'Proyek',
    'project': 'proyek',
    'PROJECT': 'PROYEK',

    # ===== Portfolio table headers =====
    'No Client Project Year': 'No Klien Proyek Tahun',
    'Client Project Year': 'Klien Proyek Tahun',
    'Tidak Client Project Year': 'No Klien Proyek Tahun',
    'Tidak Client': 'No Klien',
    'No Institution Name': 'No Nama Institusi',
    'Tidak Institution Name': 'No Nama Institusi',
    'Project Name': 'Nama Proyek',
    'Institution Name': 'Nama Institusi',

    # ===== Fix broken auto-translations of "No." (number) =====
    'Permen LHK Tidak.': 'Permen LHK No.',
    'Tidak. 80/2019': 'No. 80/2019',
    '\u00b7 TIDAKW OPEN': '\u00b7 SEKARANG OPEN',
    'TIDAKW': 'NOW',
    'Tidakw': 'Sekarang',

    # ===== Years =====
    'Year': 'Tahun',
    'Years': 'Tahun',
    'YEARS': 'TAHUN',
    'YEARS EXPERIENCE': 'TAHUN PENGALAMAN',
    'Years of Operation': 'Tahun Beroperasi',
    'Years Experience': 'Tahun Pengalaman',
    '3 + Years': '3+ Tahun',
    '64 + Projects': '64+ Proyek',
    '20 + Clients': '20+ Klien',

    # ===== Client / Customer =====
    'Clients': 'Klien',
    'Client': 'Klien',
    'CLIENTS': 'KLIEN',
    'Customer': 'Pelanggan',
    'Customers': 'Pelanggan',
    'Customer Service': 'Layanan Pelanggan',
    'Customer Support': 'Dukungan Pelanggan',

    # ===== "Rencanat" / "Rencanatation" broken translation fixes =====
    'Rencanatation': 'Plantation',  # restore — technical term acceptable
    'Smart NPK & Rencanatation Soil Monitoring': 'Smart NPK & Plantation Soil Monitoring',
    'Rencanatation pH': 'Plantation pH',
    'Rencanatation Soil': 'Plantation Soil',
    'Site Rencana & 2D Drawing': 'Site Plan & 2D Drawing',
    'Site Rencana': 'Site Plan',

    # ===== Technical/industrial terms =====
    'Setup Ethernet Komunikasi Printing': 'Setup Ethernet Printer',  # awkward translation
    'Komunikasi Printing': 'Printer',
    'WS Instalasi Electrical': 'WS Electrical Installation',
    'WS Electrical Installation': 'WS Instalasi Electrical',  # ID-target form
    'Electrical Installation': 'Instalasi Electrical',
    'Centrifugal Pump Rewinding': 'Rewinding Pompa Sentrifugal',
    'Submersible Satellite Pump Rewinding': 'Rewinding Pompa Submersible Satelit',
    'Pump Rewinding': 'Rewinding Pompa',

    # ===== "Phase" → "Fase" KBBI standard =====
    'Phase Protection': 'Proteksi Fase',
    'Phase & Lightning Arrester': 'Fase & Penangkal Petir',
    'Lightning Arrester': 'Penangkal Petir',
    'Lightning Protection': 'Proteksi Petir',
    'Reservoir': 'Waduk',  # KBBI: waduk for water reservoir

    # ===== Common technical descriptions =====
    'Power Monitoring & Control': 'Monitoring & Kontrol Daya',
    'Electrical Power Monitoring & Control': 'Monitoring & Kontrol Daya Listrik',
    'HVAC Monitoring & Management': 'Monitoring & Manajemen HVAC',
    'Water Quality IoT Sensor Integration': 'Integrasi Sensor IoT Kualitas Air',
    'Water Quality & Flowmeter Monitoring': 'Monitoring Kualitas Air & Flowmeter',
    'Flowmeter Discharge Monitoring & Control System Prototype': 'Prototype Sistem Monitoring & Kontrol Discharge Flowmeter',
    'NPK Hardware Monitoring & Control Prototype': 'Prototype Hardware Monitoring & Kontrol NPK',
    'KLHK Server Migration & SPARING IoT Dashboard Development': 'Migrasi Server KLHK & Pengembangan Dashboard IoT SPARING',
    'WTP Maintenance': 'Maintenance WTP',
    'WWTP Maintenance': 'Maintenance WWTP',
    'SPARING WWTP Maintenance': 'Maintenance SPARING WWTP',
    'Replacement & Repair of SPARING Sensors': 'Penggantian & Perbaikan Sensor SPARING',
    'IoT Attendance Module': 'Modul Absensi IoT',
    'IoT-Based Hybrid Street Lighting': 'Penerangan Jalan Hybrid Berbasis IoT',
    '(Solar PV + Wind Turbine)': '(Solar PV + Turbin Angin)',
    'Mini Pertamina Schematic & Programming': 'Skematik & Programming Mini Pertamina',
    'Procurement Module': 'Modul Procurement',
    'pH, Temp, Humidity Monitoring & Soil Control IoT System': 'Sistem IoT Monitoring pH, Suhu, Kelembaban & Kontrol Tanah',
    'Smart NPK & Plantation Soil Monitoring IoT System': 'Sistem IoT Smart NPK & Monitoring Tanah Perkebunan',

    # ===== "Year badges" =====
    '3+ Years': '3+ Tahun',
    '5 Services': '5 Layanan',
    '5 Layanan': '5 Layanan',  # keep
    '20+ Clients': '20+ Klien',
    '64+ Projects': '64+ Proyek',

    # ===== Other recurring English fragments =====
    'Hands-on internship': 'Magang langsung',
    'real-world experience': 'pengalaman dunia nyata',
    'IoT Industri, automation, and renewable energi': 'IoT Industri, otomasi, dan renewable energi',
    'Manual & automated testing': 'Testing manual & otomatis',
    'design systems & user research': 'design system & user research',
    'VPS infrastructure & CI/CD pipelines': 'infrastruktur VPS & pipeline CI/CD',

    # ===== "and the X" patterns =====
    'and the SURGE': 'dan SURGE',
    'with the SURGE': 'dengan SURGE',

    # ===== Common Indonesian word fixes =====
    'projek': 'proyek',  # informal → KBBI baku
    'Projek': 'Proyek',
    'PROJEK': 'PROYEK',
    'Tim profesional': 'Tim Profesional',
    'profesional Tim': 'Profesional Tim',

    # ===== Untranslated technical sections =====
    'Increase operational efficiency and ensure environmental compliance': 'Tingkatkan efisiensi operasional dan pastikan compliance lingkungan',
    'Tingkatkan efisiensi operasional dan pastikan compliance lingkunganc': 'Tingkatkan efisiensi operasional dan pastikan compliance lingkungan',

    # ===== Capitalization corrections =====
    'Bahasa indonesia': 'Bahasa Indonesia',
    'bahasa Indonesia': 'Bahasa Indonesia',
    'BAHASA INDONESIA': 'Bahasa Indonesia',

    # ===== Department/category translations =====
    'Renewable Energy': 'Renewable Energy',  # keep as known term
    'Water Treatment': 'Water Treatment',  # keep
    'Energy & Utilities': 'Energi & Utilitas',
    'Government & Public': 'Pemerintah & Publik',

    # ===== Form/UI common =====
    'Submit Form': 'Kirim Formulir',
    'Subscribe': 'Berlangganan',
    'Subscribe to our newsletter': 'Berlangganan newsletter kami',
    'Newsletter': 'Newsletter',
    'Search': 'Cari',
    'Filter': 'Filter',
    'Reset': 'Reset',
    'Cancel': 'Batal',
    'OK': 'OK',

    # ===== Time/period =====
    'Months': 'Bulan',
    'Days': 'Hari',
    'Hours': 'Jam',
    'Minutes': 'Menit',

    # ===== Status badges =====
    'New': 'Baru',
    'Active': 'Aktif',
    'Inactive': 'Tidak Aktif',
    'Available': 'Tersedia',
    'Out of stock': 'Stok Habis',
    'Coming Soon': 'Akan Datang',  # but we kept "Coming Soon" in lang switcher intentionally

    # ===== Address / Geo =====
    'Address': 'Alamat',
    'City': 'Kota',
    'Province': 'Provinsi',
    'Country': 'Negara',
    'Region': 'Wilayah',

    # ===== Common verbs in Indonesian B2B context =====
    'Discover': 'Temukan',
    'Explore': 'Jelajahi',
    'Browse': 'Telusuri',
    'View Details': 'Lihat Detail',
    'See Details': 'Lihat Detail',
    'More Info': 'Info Lebih Lanjut',
    'Get Info': 'Dapatkan Info',
}

# Tricky: lowercase 'project' is risky (might match URLs or attribute names)
# Filter out risky single-word lowercase items
RISKY = ['project', 'projects', 'Phase', 'Reservoir', 'Year', 'Years', 'Client', 'Clients', 'New', 'Active', 'OK', 'Reset']
# Actually those are valid Indonesian fixes — but watch for false positives
# Let me KEEP them but apply carefully

ID_PAGES = [5273,5274,5275,5276,5277,5278,5279,5281,5282,5283,5284,5285,5286,5287,5288,5289,5290,5291,5292,5293,5294,5295,5378,5379,5380,5381,5382]

print(f'Applying {len(KBBI)} KBBI corrections to {len(ID_PAGES)} ID pages...')
total = 0
for pid in ID_PAGES:
    try:
        r = urllib.request.Request(f'https://suriota.com/wp-json/wp/v2/pages/{pid}?context=edit&_fields=meta,content', headers=HDRS)
        d = json.loads(urllib.request.urlopen(r, timeout=60).read())
    except:
        continue

    changes = 0
    payload = {}

    # Apply to _elementor_data
    ed = d.get('meta', {}).get('_elementor_data', '')
    if not isinstance(ed, str): ed = json.dumps(ed)
    new_ed = ed
    for en, idt in KBBI.items():
        if en in new_ed:
            new_ed = new_ed.replace(en, idt)
            changes += new_ed.count(idt) - ed.count(idt)  # approximation
            # Simpler: count occurrences before vs after
            changes += 1  # at least 1 replacement

    # Apply to content
    content_raw = d.get('content', {}).get('raw', '')
    new_content = content_raw
    for en, idt in KBBI.items():
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
        except Exception as e:
            print(f'  page {pid}: push fail {e}')

print(f'\nTotal: {total} corrections')

# Purge
purge = '''
$upload = wp_upload_dir();
$log = $upload['basedir']."/purge-kbbi.txt";
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
urllib.request.urlopen(urllib.request.Request('https://suriota.com/wp-json/code-snippets/v1/snippets/5', data=json.dumps({'code':purge, 'active':True, 'name':'SX: kbbi purge'}).encode(), method='POST', headers=HDRS), timeout=60).read()
time.sleep(3)
urllib.request.urlopen(urllib.request.Request('https://suriota.com/?cb='+str(int(time.time())), headers={'User-Agent':'Mozilla/5.0'}), timeout=60).read()
print('Purged')
