"""Phase 1A — Create Indonesian translations of 7 strategic pages.
For each: create ID page with translated title + hero + brief intro + AIOSEO meta + link to EN.
"""
import json, urllib.request, urllib.error, base64, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

AUTH = base64.b64encode(b'admin:hCYK JqF1 khdB WDzI LQdQ WEBr').decode()
HDRS = {'Authorization': f'Basic {AUTH}', 'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}

# Strategic page translations: en_id -> ID copy + meta
PAGES = [
    {
        'en_id': 12,
        'slug': 'beranda',
        'title': 'Beranda — SURIOTA Mitra Industri Generasi Baru',
        'meta_title': 'IoT Industri & Integrasi Sistem Batam | SURIOTA',
        'meta_desc': 'SURIOTA — Solusi IoT industri, gateway Modbus, monitoring SaaS, otomasi SCADA di Batam. 64+ proyek industri di sektor manufaktur, maritim, oil & gas, water treatment.',
        'hero_h1': 'Mitra Industri Generasi Baru',
        'hero_eyebrow': 'PT SURYA INOVASI PRIORITAS',
        'intro': '<strong>SURIOTA</strong> adalah perusahaan teknologi spesialis <strong>IoT Industri & Integrasi Sistem</strong> yang berbasis di Batam, Kepulauan Riau. Sejak Januari 2023, kami telah menyelesaikan <strong>64+ proyek industri</strong> — mulai dari gateway Modbus hingga platform IoT lengkap untuk sektor manufaktur, energi, logistik, dan maritim.',
        'cta_text': 'Konsultasi Gratis',
        'cta_url': 'https://wa.me/6285835672476'
    },
    {
        'en_id': 29,
        'slug': 'tentang-kami',
        'title': 'Tentang SURIOTA — Mitra Industrial IoT Batam Indonesia',
        'meta_title': 'Tentang SURIOTA — Mitra IoT Industri Batam Indonesia',
        'meta_desc': 'PT Surya Inovasi Prioritas (SURIOTA) — perusahaan teknologi spesialis IoT industri, otomasi & integrasi sistem di Batam. 64+ proyek, 6 produk in-house, 25+ engineer.',
        'hero_h1': 'Tentang SURIOTA',
        'hero_eyebrow': 'TENTANG KAMI',
        'intro': '<strong>PT Surya Inovasi Prioritas (SURIOTA)</strong> adalah perusahaan teknologi yang berfokus pada <strong>Industrial IoT dan Integrasi Sistem</strong>, berkantor pusat di Batam Centre, Kepulauan Riau. Kami merancang dan memproduksi solusi konektivitas industri — dari gateway Modbus hingga platform IoT terintegrasi.',
        'cta_text': 'Hubungi Tim Engineer',
        'cta_url': 'https://wa.me/6285835672476'
    },
    {
        'en_id': 839,
        'slug': 'portfolio-id',
        'title': 'Portfolio — 64+ Proyek IoT Industri SURIOTA Batam',
        'meta_title': 'Portfolio — 64+ Proyek IoT Industri | SURIOTA Batam',
        'meta_desc': 'Jelajahi 64+ proyek SURIOTA: PDAM Tirta Kepri SPARING, gateway Modbus, hybrid PLTS, SCADA, oil & gas IoT di seluruh Indonesia, manufaktur & maritim.',
        'hero_h1': 'Portfolio Proyek SURIOTA',
        'hero_eyebrow': 'PORTFOLIO',
        'intro': 'Jelajahi <strong>64+ proyek industri SURIOTA</strong> yang telah selesai sejak 2023 — termasuk PDAM Tirta Kepri (SPARING), gateway Modbus IIoT, sistem hybrid PLTS-PLTB, SCADA modernization, dan IoT oil & gas. Tersebar di Sumatra, Jawa, dan Kalimantan.',
        'cta_text': 'Diskusikan Proyek Anda',
        'cta_url': 'https://wa.me/6285835672476'
    },
    {
        'en_id': 1127,
        'slug': 'magang-srt-team',
        'title': 'Program Magang IoT Industri & Engineering | SURIOTA Batam',
        'meta_title': 'Magang IoT Industri & Engineering | SURIOTA Batam',
        'meta_desc': 'Bergabung program magang SURIOTA di Batam: R&D, DevOps, QA, UI/UX dengan proyek nyata IoT industri, Modbus gateway & SCADA. Pengalaman engineering langsung.',
        'hero_h1': 'Program Magang Batch 3 — SRT Team',
        'hero_eyebrow': 'KARIER',
        'intro': 'Bergabunglah dengan <strong>Program Magang SURIOTA</strong> di Batam. Kami membuka posisi <strong>R&D App Developer, DevOps, QA, UI/UX</strong> untuk berkontribusi pada proyek nyata IoT industri, gateway Modbus, dan sistem SCADA. Pengalaman engineering langsung di sektor industri Indonesia.',
        'cta_text': 'Lamar Sekarang',
        'cta_url': 'mailto:admin@suriota.com?subject=Lamaran%20Magang%20SURIOTA'
    },
    {
        'en_id': 945,
        'slug': 'water-treatment-id',
        'title': 'Water Treatment, WTP & Monitoring SPARING KLHK | SURIOTA',
        'meta_title': 'WTP, WWTP & Monitoring SPARING KLHK IoT | SURIOTA',
        'meta_desc': 'Desain WTP, WWTP, IPAL dengan compliance SPARING KLHK & monitoring real-time pH, COD, TSS, NH3 via SURGE Water Analytics. SURIOTA layani PDAM Tirta Kepri.',
        'hero_h1': 'Layanan Water Treatment & Monitoring SPARING',
        'hero_eyebrow': 'LAYANAN',
        'intro': 'SURIOTA menyediakan layanan <strong>desain WTP, WWTP, IPAL</strong> lengkap dengan compliance <strong>SPARING KLHK</strong> dan monitoring real-time kualitas air (pH, COD, TSS, NH3) melalui platform SURGE Water Analytics. Sudah dipercaya oleh PDAM Tirta Kepri & industri manufaktur.',
        'cta_text': 'Konsultasi Compliance KLHK',
        'cta_url': 'https://wa.me/6285835672476'
    },
    {
        'en_id': 5039,
        'slug': 'saas-id',
        'title': 'SURGE SaaS — Platform Monitoring IoT Industri | SURIOTA',
        'meta_title': 'SURGE SaaS — Platform Monitoring IoT Industri | SURIOTA',
        'meta_desc': 'Platform SaaS SURGE — monitoring IoT multi-tenant untuk energi, air (compliance SPARING KLHK), pelacakan kapal. 70% lebih murah dari ThingsBoard. Buatan Indonesia.',
        'hero_h1': 'SURGE — Platform SaaS IoT Industri',
        'hero_eyebrow': 'PLATFORM',
        'intro': '<strong>SURGE</strong> adalah platform <strong>SaaS multi-tenant</strong> SURIOTA untuk monitoring IoT industri: <strong>Energy Mapping</strong> (kWh, power factor), <strong>Water Analytic</strong> (compliance SPARING KLHK), dan <strong>Vessel Tracking</strong> (pelacakan armada + monitoring bahan bakar). 70% lebih murah dari ThingsBoard.',
        'cta_text': 'Coba Demo Gratis',
        'cta_url': 'https://wa.me/6285835672476'
    },
    {
        'en_id': 5260,
        'slug': 'artikel-id',
        'title': 'Artikel IoT Industri & Wawasan Engineering | SURIOTA',
        'meta_title': 'Artikel IoT Industri & Wawasan Engineering | SURIOTA',
        'meta_desc': 'Baca wawasan SURIOTA tentang IoT industri, otomasi, water treatment, compliance KLHK SPARING, PLTS hybrid & 64+ studi kasus portfolio di Indonesia.',
        'hero_h1': 'Artikel & Wawasan Industrial IoT',
        'hero_eyebrow': 'WAWASAN SURIOTA',
        'intro': 'Pelajari studi kasus engineering, dokumentasi teknis, dan wawasan dari tim SURIOTA — Industrial IoT, otomasi, electrical, water treatment, dan renewable energy di Indonesia.',
        'cta_text': 'Lihat Versi English →',
        'cta_url': 'https://suriota.com/artikel/'
    },
]


def build_id_content(p):
    """Build minimal but useful Indonesian page content (English page remains the canonical source)."""
    return f'''<!-- wp:html -->
<div class="sx-id-page" style="max-width:1080px;margin:48px auto;padding:0 clamp(16px,3vw,32px);font-family:'Plus Jakarta Sans',sans-serif;color:#0E3942;">
  <p class="sx-eyebrow" style="font:600 12px/1 'IBM Plex Mono',monospace;letter-spacing:0.16em;text-transform:uppercase;color:#C8851F;margin-bottom:12px;">{p['hero_eyebrow']}</p>
  <h1 style="font:700 clamp(32px,5vw,48px)/1.15 'Plus Jakarta Sans',sans-serif;letter-spacing:-0.025em;margin:0 0 20px;color:#0E3942;">{p['hero_h1']}</h1>
  <div style="font:400 17px/1.65 'Plus Jakarta Sans',sans-serif;color:#1F2D33;margin-bottom:32px;max-width:780px;">{p['intro']}</div>
  <div style="display:flex;gap:14px;flex-wrap:wrap;margin-bottom:48px;">
    <a href="{p['cta_url']}" style="display:inline-flex;align-items:center;gap:8px;padding:14px 28px;background:#205B69;color:#fff;text-decoration:none;border-radius:6px;font:600 14px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:0.04em;">{p['cta_text']} <span>&rarr;</span></a>
    <a href="https://suriota.com/{p['slug'].replace('-id', '').replace('beranda', '').replace('tentang-kami', 'about-us').replace('magang-srt-team', 'internship').replace('portfolio-id', 'portfolio').replace('saas-id', 'software-as-a-service').replace('artikel-id', 'artikel').replace('water-treatment-id', 'water-treatment')}/" style="display:inline-flex;align-items:center;gap:8px;padding:14px 28px;background:transparent;color:#205B69;text-decoration:none;border:1px solid #E5E9EB;border-radius:6px;font:600 14px/1 'Plus Jakarta Sans',sans-serif;letter-spacing:0.04em;">View in English &rarr;</a>
  </div>
  <hr style="border:none;border-top:1px solid #E5E9EB;margin:32px 0;">
  <p style="font:400 14px/1.6 'Plus Jakarta Sans',sans-serif;color:#5B6F75;background:#FAFBFC;padding:16px 20px;border-left:3px solid #C8851F;border-radius:4px;">
    <strong>Catatan:</strong> Versi Bahasa Indonesia lengkap dari halaman ini sedang dalam tahap pengembangan. Untuk konten teknis lengkap, kunjungi versi bahasa Inggris. Tim engineer SURIOTA siap melayani dalam Bahasa Indonesia via WhatsApp atau email.
  </p>
</div>
<!-- /wp:html -->'''


def update_aioseo_meta(post_id, title, desc):
    """Update AIOSEO meta via direct REST + the existing wp_aioseo_posts pattern."""
    # We use the slot-5 PHP pattern that already works
    pass


def link_translation(en_id, id_id):
    """Use our custom sx/v1/link-translation endpoint."""
    payload = json.dumps({'en_id': en_id, 'id_id': id_id}).encode()
    req = urllib.request.Request('https://suriota.com/wp-json/sx/v1/link-translation', data=payload, method='POST', headers=HDRS)
    try:
        resp = json.loads(urllib.request.urlopen(req, timeout=30).read())
        return resp
    except urllib.error.HTTPError as e:
        return {'error': f'HTTP {e.code}: {e.read().decode()[:200]}'}


def create_id_page(p):
    payload = {
        'title': p['title'],
        'content': build_id_content(p),
        'slug': p['slug'],
        'status': 'publish',
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request('https://suriota.com/wp-json/wp/v2/pages?lang=id', data=data, method='POST', headers=HDRS)
    try:
        resp = json.loads(urllib.request.urlopen(req, timeout=30).read())
        return resp
    except urllib.error.HTTPError as e:
        return {'error': f'HTTP {e.code}: {e.read().decode()[:300]}'}


results = []
for p in PAGES:
    print(f"\n=== Translating EN page {p['en_id']} → ID slug '{p['slug']}' ===")
    created = create_id_page(p)
    if 'error' in created:
        print(f"  CREATE FAIL: {created['error']}")
        results.append({'en_id': p['en_id'], 'status': 'create_fail', 'error': created['error']})
        continue
    id_id = created['id']
    id_link = created.get('link', '?')
    print(f"  Created ID page id={id_id} link={id_link}")

    # Link as translation
    link = link_translation(p['en_id'], id_id)
    if 'error' in link:
        print(f"  LINK FAIL: {link['error']}")
        results.append({'en_id': p['en_id'], 'id_id': id_id, 'status': 'link_fail', 'error': link['error']})
        continue
    print(f"  Linked: {link.get('translations')}")
    results.append({'en_id': p['en_id'], 'id_id': id_id, 'status': 'ok', 'link': id_link, 'meta_title': p['meta_title'], 'meta_desc': p['meta_desc']})

# Save mapping for AIOSEO meta update step
with open('_id_pages_mapping.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print('\n=== SUMMARY ===')
ok = [r for r in results if r['status'] == 'ok']
print(f'Successful: {len(ok)}/{len(PAGES)}')
for r in ok:
    print(f"  EN {r['en_id']} ↔ ID {r['id_id']}  {r['link']}")
