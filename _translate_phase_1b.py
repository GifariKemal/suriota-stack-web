"""Phase 1B — translate 15 remaining pages: 6 services + 9 products."""
import json, urllib.request, urllib.error, base64, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization': f'Basic {AUTH}', 'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

PAGES = [
    # === 6 SERVICE PAGES ===
    {
        'en_id': 37, 'slug': 'electrical-id',
        'title': 'Layanan Industrial Electrical Engineering Batam | SURIOTA',
        'meta_title': 'Industrial Electrical Engineering Batam | SURIOTA',
        'meta_desc': 'Instalasi panel listrik, distribusi daya, commissioning sesuai SNI, IEC, PUIL 2011 untuk industri oil & gas, shipyard, manufaktur di Batam. SURIOTA turnkey.',
        'hero_h1': 'Layanan Industrial Electrical', 'hero_eyebrow': 'LAYANAN',
        'intro': 'SURIOTA menyediakan layanan <strong>instalasi panel listrik, distribusi daya, dan commissioning</strong> sesuai standar <strong>SNI, IEC, PUIL 2011</strong>. Turnkey engineering untuk sektor oil & gas, shipyard, manufaktur, dan commercial buildings di Indonesia.',
        'cta_text': 'Diskusi Proyek Anda', 'cta_url': 'https://wa.me/6285835672476',
        'view_en': 'https://suriota.com/electrical/'
    },
    {
        'en_id': 35, 'slug': 'automation-id',
        'title': 'Layanan Industrial Automation, PLC & SCADA | SURIOTA',
        'meta_title': 'Industrial Automation, PLC & SCADA | SURIOTA',
        'meta_desc': 'Integrasi PLC, SCADA, IIoT, gateway Modbus & platform SURGE untuk manufaktur Industry 4.0, oil & gas, shipyard. SURIOTA layani otomasi industri di seluruh Indonesia.',
        'hero_h1': 'Industrial Automation & SCADA', 'hero_eyebrow': 'LAYANAN',
        'intro': 'SURIOTA mengintegrasikan <strong>PLC, SCADA, IIoT</strong> dengan gateway Modbus dan platform SURGE untuk <strong>Industry 4.0</strong>. Vendor-agnostic — kami otomatisasi pabrik manufaktur, oil & gas, dan shipyard di seluruh Indonesia.',
        'cta_text': 'Konsultasi Otomasi', 'cta_url': 'https://wa.me/6285835672476',
        'view_en': 'https://suriota.com/automation/'
    },
    {
        'en_id': 39, 'slug': 'renewable-energy-id',
        'title': 'Layanan Solar PV PLTS & Renewable Energy | SURIOTA',
        'meta_title': 'Solar PV PLTS & Renewable Energy | SURIOTA Indonesia',
        'meta_desc': 'PLTS, hybrid PLTS-PLTB, smart street light (PJU) & monitoring energi IoT. Feasibility study, desain, instalasi. SURIOTA layani industri di seluruh Indonesia.',
        'hero_h1': 'Solar PV PLTS & Renewable Energy', 'hero_eyebrow': 'LAYANAN',
        'intro': 'SURIOTA merancang dan memasang <strong>Solar PV PLTS, sistem hybrid PLTS-PLTB</strong>, dan <strong>smart street light (PJU)</strong> dengan monitoring energi IoT real-time. Feasibility study, desain teknis, dan instalasi turnkey untuk industri & commercial buildings.',
        'cta_text': 'Konsultasi PLTS', 'cta_url': 'https://wa.me/6285835672476',
        'view_en': 'https://suriota.com/renewable-energy/'
    },
    {
        'en_id': 5029, 'slug': 'internet-of-things-id',
        'title': 'IoT & Integrasi Sistem — Modbus, MQTT, AWS IoT | SURIOTA',
        'meta_title': 'IoT & Integrasi Sistem Batam | SURIOTA',
        'meta_desc': 'IoT industri & integrasi sistem: gateway Modbus, MQTT, AWS IoT Core, edge computing untuk manufaktur, oil & gas, shipyard. SURIOTA Batam — 64+ proyek.',
        'hero_h1': 'Industrial IoT & Integrasi Sistem', 'hero_eyebrow': 'LAYANAN',
        'intro': 'SURIOTA mengintegrasikan <strong>Industrial IoT end-to-end</strong> — dari gateway Modbus & MQTT, edge computing, hingga AWS IoT Core dan SURGE cloud dashboard. Kami melayani manufaktur, oil & gas, shipyard, water utilities, dan renewable energy di seluruh Indonesia.',
        'cta_text': 'Konsultasi IoT Gratis', 'cta_url': 'https://wa.me/6285835672476',
        'view_en': 'https://suriota.com/internet-of-things/'
    },
    {
        'en_id': 5037, 'slug': 'data-analytics-id',
        'title': 'AI & Data Analytics Industri — Predictive Maintenance | SURIOTA',
        'meta_title': 'AI & Data Analytics Industri | SURIOTA',
        'meta_desc': 'Analitik AI industri: predictive maintenance, OEE dashboard, optimasi energi, real-time monitoring untuk manufaktur & utilities. SURIOTA layani Indonesia.',
        'hero_h1': 'AI & Data Analytics Industri', 'hero_eyebrow': 'LAYANAN',
        'intro': 'SURIOTA mengubah data mesin menjadi keputusan operasional — <strong>predictive maintenance, OEE dashboard, computer-vision QC, optimasi energi</strong>, dan intelligence real-time untuk plant manufaktur, oil & gas, mining, water utilities, dan logistics.',
        'cta_text': 'Konsultasi Analytics', 'cta_url': 'https://wa.me/6285835672476',
        'view_en': 'https://suriota.com/data-analytics/'
    },
    {
        'en_id': 5033, 'slug': 'digital-consulting-id',
        'title': 'Industrial Digital Transformation Consulting | SURIOTA',
        'meta_title': 'Industrial Digital Transformation Consulting | SURIOTA',
        'meta_desc': 'Konsultan transformasi digital industri: roadmap Industry 4.0, konvergensi OT/IT, audit IIoT, modernisasi SCADA. SURIOTA layani manufaktur Indonesia.',
        'hero_h1': 'Digital Transformation Consulting', 'hero_eyebrow': 'LAYANAN',
        'intro': 'SURIOTA membantu manufaktur Indonesia merancang <strong>roadmap Industry 4.0</strong> — assessment konvergensi <strong>OT/IT</strong>, audit kesiapan <strong>IIoT</strong>, strategi modernisasi <strong>SCADA</strong>, dan migrasi cloud step-by-step.',
        'cta_text': 'Konsultasi Strategi', 'cta_url': 'https://wa.me/6285835672476',
        'view_en': 'https://suriota.com/digital-consulting/'
    },
    # === 9 PRODUCT PAGES ===
    {
        'en_id': 934, 'slug': 'suriota-modbus-gateway-id',
        'title': 'SRT-MGATE-1210 Modbus Gateway IIoT | SURIOTA Batam',
        'meta_title': 'SRT-MGATE-1210 Modbus Gateway IIoT | SURIOTA',
        'meta_desc': 'SRT-MGATE-1210 — Modbus RTU/TCP ke MQTT gateway dengan BLE config, WiFi auto-failover & RTC backup. Gateway IoT industri buatan Indonesia oleh SURIOTA.',
        'hero_h1': 'SRT-MGATE-1210 — Modbus Gateway IIoT', 'hero_eyebrow': 'PRODUK',
        'intro': '<strong>SRT-MGATE-1210</strong> adalah gateway IoT industri yang mengonversi <strong>Modbus RTU/TCP ke MQTT</strong>. Fitur unggulan: konfigurasi via <strong>BLE smartphone</strong> (no laptop needed!), auto-failover WiFi, RTC battery backup. Buatan Indonesia oleh SURIOTA, Batam.',
        'cta_text': 'Beli di Tokopedia', 'cta_url': 'https://www.tokopedia.com/suriota',
        'view_en': 'https://suriota.com/suriota-modbus-gateway/'
    },
    {
        'en_id': 1542, 'slug': 'surge-energy-mapping-id',
        'title': 'SURGE Energy Mapping — Monitoring kWh SaaS | SURIOTA',
        'meta_title': 'SURGE Energy Mapping — kWh Monitoring SaaS | SURIOTA',
        'meta_desc': 'SaaS monitoring energi multi-lokasi — kWh real-time, power factor, demand. SURGE menggantikan EMS mahal untuk pabrik & gedung. Platform SURIOTA.',
        'hero_h1': 'SURGE Energy Mapping', 'hero_eyebrow': 'PLATFORM',
        'intro': '<strong>SURGE Energy Mapping</strong> — platform SaaS multi-tenant SURIOTA untuk monitoring energi listrik <strong>real-time kWh, power factor, demand</strong> dari banyak lokasi. Pengganti EMS mahal untuk pabrik manufaktur, building management, dan utilities.',
        'cta_text': 'Demo SURGE Energy', 'cta_url': 'https://wa.me/6285835672476',
        'view_en': 'https://suriota.com/surge-energy-mapping/'
    },
    {
        'en_id': 1546, 'slug': 'surge-vessel-tracking-id',
        'title': 'SURGE Vessel Tracking — Pelacakan Armada | SURIOTA',
        'meta_title': 'SURGE Vessel Tracking — Fleet & Fuel Monitoring | SURIOTA',
        'meta_desc': 'SaaS maritim IoT: pelacakan GPS kapal, monitoring RPM & konsumsi bahan bakar untuk shipyard & fleet operator. SURGE Vessel by SURIOTA, Batam.',
        'hero_h1': 'SURGE Vessel Tracking', 'hero_eyebrow': 'PLATFORM',
        'intro': '<strong>SURGE Vessel Tracking</strong> — SaaS IoT maritim untuk operator armada & shipyard di Indonesia. <strong>Pelacakan GPS real-time, monitoring RPM mesin, konsumsi bahan bakar</strong>, dan dashboard armada. Buatan SURIOTA, Batam — pusat industri maritim Indonesia.',
        'cta_text': 'Konsultasi Vessel IoT', 'cta_url': 'https://wa.me/6285835672476',
        'view_en': 'https://suriota.com/surge-vessel-tracking/'
    },
    {
        'en_id': 1547, 'slug': 'surge-water-analytic-id',
        'title': 'SURGE Water Analytics — Monitoring SPARING KLHK | SURIOTA',
        'meta_title': 'SURGE Water Analytics — KLHK SPARING Monitoring | SURIOTA',
        'meta_desc': 'SaaS kualitas air real-time — monitoring pH, COD, TSS, NH3 dengan compliance SPARING KLHK untuk IPAL, WTP, PDAM. SURGE Water by SURIOTA.',
        'hero_h1': 'SURGE Water Analytics', 'hero_eyebrow': 'PLATFORM',
        'intro': '<strong>SURGE Water Analytics</strong> — SaaS monitoring kualitas air real-time untuk compliance <strong>SPARING KLHK</strong>. Sensor pH, COD, TSS, NH3 → dashboard cloud → notifikasi otomatis. Dipakai oleh <strong>PDAM Tirta Kepri</strong>, IPAL industri, dan WTP.',
        'cta_text': 'Demo SURGE Water', 'cta_url': 'https://wa.me/6285835672476',
        'view_en': 'https://suriota.com/surge-water-analytic/'
    },
    {
        'en_id': 1740, 'slug': 'iso-m485-series-id',
        'title': 'ISO-M485 Isolated RS-485 Repeater | SURIOTA Indonesia',
        'meta_title': 'ISO-M485 Isolated RS-485 Repeater | SURIOTA',
        'meta_desc': 'Isolator & repeater RS-485 industrial dengan proteksi surge. ISO-M485 melindungi jaringan Modbus di pabrik & shipyard. Produk SURIOTA, Batam.',
        'hero_h1': 'ISO-M485 Isolated RS-485', 'hero_eyebrow': 'PRODUK',
        'intro': '<strong>ISO-M485</strong> adalah <strong>isolator & repeater RS-485 industri</strong> dengan proteksi surge built-in. Melindungi jaringan Modbus dari ground loop, noise listrik, dan petir induksi di pabrik manufaktur, shipyard, dan plant otomatis.',
        'cta_text': 'Order via Tokopedia', 'cta_url': 'https://www.tokopedia.com/suriota',
        'view_en': 'https://suriota.com/iso-m485-series/'
    },
    {
        'en_id': 1741, 'slug': 'thm-30md-id',
        'title': 'THM-30MD Sensor Suhu & Kelembaban Modbus | SURIOTA',
        'meta_title': 'THM-30MD Temperature & Humidity Modbus Sensor | SURIOTA',
        'meta_desc': 'Sensor industrial suhu & kelembaban dengan output Modbus RTU. THM-30MD untuk warehouse, HVAC, cold chain monitoring. SURIOTA Indonesia.',
        'hero_h1': 'THM-30MD — Sensor Suhu & Kelembaban', 'hero_eyebrow': 'PRODUK',
        'intro': '<strong>THM-30MD</strong> adalah sensor industri untuk monitoring <strong>suhu & kelembaban</strong> dengan output Modbus RTU. Akurasi tinggi, casing tahan industri, plug-and-play dengan SCADA atau SURGE platform. Cocok untuk warehouse, HVAC, cold chain, dan greenhouse monitoring.',
        'cta_text': 'Order via Tokopedia', 'cta_url': 'https://www.tokopedia.com/suriota',
        'view_en': 'https://suriota.com/thm-30md/'
    },
    {
        'en_id': 1742, 'slug': 'pm1611-wd-id',
        'title': 'PM1611-WD Smart Prepaid Energy Meter IoT | SURIOTA',
        'meta_title': 'PM1611-WD Smart Prepaid Energy Meter | SURIOTA',
        'meta_desc': 'Smart meter prabayar dengan WiFi/Modbus untuk rumah sewa, pabrik. Integrasi MQTT ke platform SURGE. PM1611-WD oleh SURIOTA.',
        'hero_h1': 'PM1611-WD — Smart Prepaid Energy Meter', 'hero_eyebrow': 'PRODUK',
        'intro': '<strong>PM1611-WD</strong> — <strong>smart prepaid energy meter</strong> dengan koneksi WiFi & Modbus. Cocok untuk rumah sewa, kos-kosan, dan pabrik dengan tenant terpisah. Integrasi langsung dengan SURGE Energy Mapping untuk billing & monitoring real-time.',
        'cta_text': 'Order via Tokopedia', 'cta_url': 'https://www.tokopedia.com/suriota',
        'view_en': 'https://suriota.com/pm1611-wd/'
    },
    {
        'en_id': 1765, 'slug': 'rs-485-surge-protector-id',
        'title': 'RS-485 Surge Protector SPD-T485-105 | SURIOTA',
        'meta_title': 'RS-485 Surge Protector SPD-T485-105 | SURIOTA',
        'meta_desc': 'Surge protector RS-485 / RS-422 / Profibus / CAN untuk jalur komunikasi industri. SPD-T485-105 buatan Indonesia oleh SURIOTA.',
        'hero_h1': 'SPD-T485-105 — RS-485 Surge Protector', 'hero_eyebrow': 'PRODUK',
        'intro': '<strong>SPD-T485-105</strong> — <strong>Surge Protective Device</strong> untuk jalur komunikasi industri: RS-485, RS-422, Profibus, dan CAN. Melindungi PLC, sensor, dan inverter dari petir induksi & lonjakan tegangan. Dirancang & diproduksi di Indonesia oleh SURIOTA.',
        'cta_text': 'Order via Tokopedia', 'cta_url': 'https://www.tokopedia.com/suriota',
        'view_en': 'https://suriota.com/rs-485-surge-protector-spd-t485-105/'
    },
    {
        'en_id': 929, 'slug': 'waste-water-logger-id',
        'title': 'Wastewater Data Logger IPAL IoT Monitoring | SURIOTA',
        'meta_title': 'Wastewater Data Logger — IPAL IoT Monitoring | SURIOTA',
        'meta_desc': 'Data logger IoT untuk monitoring air limbah (pH, COD, TSS, NH3) dengan compliance SPARING KLHK. Wastewater Logger SURIOTA, Batam.',
        'hero_h1': 'Wastewater Data Logger', 'hero_eyebrow': 'PRODUK',
        'intro': '<strong>Wastewater Logger</strong> — data logger IoT khusus monitoring <strong>air limbah industri & IPAL</strong>. Sensor multi-parameter: pH, COD, TSS, NH3. Output ke SURGE Water Analytics dengan compliance <strong>SPARING KLHK</strong>. Buatan SURIOTA, Batam.',
        'cta_text': 'Konsultasi SPARING', 'cta_url': 'https://wa.me/6285835672476',
        'view_en': 'https://suriota.com/waste-water-logger/'
    },
]


def build_id_content(p):
    return f'''<!-- wp:html -->
<div class="sx-id-page" style="max-width:1080px;margin:48px auto;padding:0 clamp(16px,3vw,32px);font-family:'Plus Jakarta Sans',sans-serif;color:#0E3942;">
  <p class="sx-eyebrow" style="font:600 12px/1 'IBM Plex Mono',monospace;letter-spacing:0.16em;text-transform:uppercase;color:#C8851F;margin-bottom:12px;">{p['hero_eyebrow']}</p>
  <h1 style="font:700 clamp(32px,5vw,48px)/1.15 'Plus Jakarta Sans',sans-serif;letter-spacing:-0.025em;margin:0 0 20px;color:#0E3942;">{p['hero_h1']}</h1>
  <div style="font:400 17px/1.65 'Plus Jakarta Sans',sans-serif;color:#1F2D33;margin-bottom:32px;max-width:780px;">{p['intro']}</div>
  <div style="display:flex;gap:14px;flex-wrap:wrap;margin-bottom:48px;">
    <a href="{p['cta_url']}" style="display:inline-flex;align-items:center;gap:8px;padding:14px 28px;background:#205B69;color:#fff;text-decoration:none;border-radius:6px;font:600 14px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:0.04em;">{p['cta_text']} <span>&rarr;</span></a>
    <a href="{p['view_en']}" style="display:inline-flex;align-items:center;gap:8px;padding:14px 28px;background:transparent;color:#205B69;text-decoration:none;border:1px solid #E5E9EB;border-radius:6px;font:600 14px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:0.04em;">Versi Lengkap (English) &rarr;</a>
  </div>
  <hr style="border:none;border-top:1px solid #E5E9EB;margin:32px 0;">
  <p style="font:400 14px/1.6 'Plus Jakarta Sans',sans-serif;color:#5B6F75;background:#FAFBFC;padding:16px 20px;border-left:3px solid #C8851F;border-radius:4px;">
    <strong>Catatan:</strong> Spesifikasi teknis lengkap, gambar produk, dan studi kasus tersedia di versi Bahasa Inggris. Tim engineer SURIOTA siap berkomunikasi dalam Bahasa Indonesia via WhatsApp atau email.
  </p>
</div>
<!-- /wp:html -->'''


def link_translation(en_id, id_id):
    payload = json.dumps({'en_id': en_id, 'id_id': id_id}).encode()
    req = urllib.request.Request('https://suriota.com/wp-json/sx/v1/link-translation', data=payload, method='POST', headers=HDRS)
    try:
        return json.loads(urllib.request.urlopen(req, timeout=30).read())
    except urllib.error.HTTPError as e:
        return {'error': f'HTTP {e.code}: {e.read().decode()[:200]}'}


def create_id_page(p):
    payload = {'title': p['title'], 'content': build_id_content(p), 'slug': p['slug'], 'status': 'publish'}
    req = urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages?lang=id', data=json.dumps(payload).encode(), method='POST', headers=HDRS)
    try:
        return json.loads(urllib.request.urlopen(req, timeout=30).read())
    except urllib.error.HTTPError as e:
        return {'error': f'HTTP {e.code}: {e.read().decode()[:300]}'}


results = []
for p in PAGES:
    print(f"\n=== EN {p['en_id']} → /id/{p['slug']}/ ===")
    created = create_id_page(p)
    if 'error' in created:
        print(f"  CREATE FAIL: {created['error']}")
        results.append({'en_id': p['en_id'], 'status': 'create_fail'})
        continue
    id_id = created['id']
    print(f"  Created id={id_id}")
    link = link_translation(p['en_id'], id_id)
    if 'error' in link:
        print(f"  LINK FAIL: {link['error']}")
        results.append({'en_id': p['en_id'], 'id_id': id_id, 'status': 'link_fail'})
        continue
    print(f"  Linked")
    results.append({'en_id': p['en_id'], 'id_id': id_id, 'slug': p['slug'], 'meta_title': p['meta_title'], 'meta_desc': p['meta_desc'], 'status': 'ok'})

with open('_id_pages_phase1b.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

ok = [r for r in results if r['status'] == 'ok']
print(f'\n=== SUMMARY ===')
print(f'Successful: {len(ok)}/{len(PAGES)}')
for r in ok:
    print(f"  EN {r['en_id']} ↔ ID {r['id_id']}  /id/{r['slug']}/")
