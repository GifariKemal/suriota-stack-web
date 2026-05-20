"""Full 3-language comparison for all 25 pages."""
import asyncio, sys, time
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except: pass
from playwright.async_api import async_playwright

# (en_url, id_url, zh_url, label)
ALL_PAGES = [
    ('https://suriota.com/', 'https://suriota.com/id/beranda/', 'https://suriota.com/shouye/', 'home'),
    ('https://suriota.com/about-us/', 'https://suriota.com/id/tentang-kami/', 'https://suriota.com/guanyu-women/', 'about'),
    ('https://suriota.com/portfolio/', 'https://suriota.com/id/portfolio-id/', 'https://suriota.com/anli/', 'portfolio'),
    ('https://suriota.com/contact/', 'https://suriota.com/id/kontak/', 'https://suriota.com/lianxi/', 'contact'),
    ('https://suriota.com/automation/', 'https://suriota.com/id/automation-id/', 'https://suriota.com/zidonghua/', 'automation'),
    ('https://suriota.com/electrical/', 'https://suriota.com/id/electrical-id/', 'https://suriota.com/dianqi-gongcheng/', 'electrical'),
    ('https://suriota.com/renewable-energy/', 'https://suriota.com/id/renewable-energy-id/', 'https://suriota.com/kezaisheng-nengyuan/', 'renewable'),
    ('https://suriota.com/internet-of-things/', 'https://suriota.com/id/internet-of-things-id/', 'https://suriota.com/iot/', 'iot'),
    ('https://suriota.com/water-treatment/', 'https://suriota.com/id/water-treatment-id/', 'https://suriota.com/shuichuli/', 'wt'),
    ('https://suriota.com/data-analytics/', 'https://suriota.com/id/data-analytics-id/', 'https://suriota.com/shujufenxi/', 'da'),
    ('https://suriota.com/digital-consulting/', 'https://suriota.com/id/digital-consulting-id/', 'https://suriota.com/shuzihua-zixun/', 'dc'),
    ('https://suriota.com/artificial-intelligence/', 'https://suriota.com/id/artificial-intelligence-id/', 'https://suriota.com/rengong-zhineng/', 'ai'),
    ('https://suriota.com/system-integration/', 'https://suriota.com/id/system-integration-id/', 'https://suriota.com/xitong-jicheng/', 'sysint'),
    ('https://suriota.com/software-as-a-service/', 'https://suriota.com/id/saas-id/', 'https://suriota.com/saas/', 'saas'),
    ('https://suriota.com/surge-energy-mapping/', 'https://suriota.com/id/surge-energy-mapping-id/', 'https://suriota.com/surge-energy-mapping-2/', 'surge_e'),
    ('https://suriota.com/surge-vessel-tracking/', 'https://suriota.com/id/surge-vessel-tracking-id/', 'https://suriota.com/surge-vessel-tracking-2/', 'surge_v'),
    ('https://suriota.com/surge-water-analytic/', 'https://suriota.com/id/surge-water-analytic-id/', 'https://suriota.com/surge-water-analytic-2/', 'surge_w'),
    ('https://suriota.com/suriota-modbus-gateway/', 'https://suriota.com/id/suriota-modbus-gateway-id/', 'https://suriota.com/modbus-gateway/', 'mgate'),
    ('https://suriota.com/iso-m485-series/', 'https://suriota.com/id/iso-m485-series-id/', 'https://suriota.com/iso-m485/', 'iso_m485'),
    ('https://suriota.com/thm-30md/', 'https://suriota.com/id/thm-30md-id/', 'https://suriota.com/thm-30md-2/', 'thm30md'),
    ('https://suriota.com/pm1611-wd/', 'https://suriota.com/id/pm1611-wd-id/', 'https://suriota.com/pm1611-wd-2/', 'pm1611'),
    ('https://suriota.com/rs-485-surge-protector-spd-t485-105/', 'https://suriota.com/id/rs-485-surge-protector-id/', 'https://suriota.com/rs-485-spd/', 'spd_t485'),
    ('https://suriota.com/waste-water-logger/', 'https://suriota.com/id/waste-water-logger-id/', 'https://suriota.com/wastewater-logger/', 'ww_logger'),
    ('https://suriota.com/privacy-policy/', 'https://suriota.com/id/kebijakan-privasi/', 'https://suriota.com/yinsi-zhengce/', 'privacy'),
    ('https://suriota.com/terms-of-service/', 'https://suriota.com/id/syarat-layanan/', 'https://suriota.com/fuwu-tiaokuan/', 'terms'),
]

async def get_stats(page, url):
    try:
        await page.goto(url+'?nc='+str(time.time()), wait_until='domcontentloaded', timeout=30000)
        await page.wait_for_timeout(2500)
        return await page.evaluate('''(() => ({
            sections: document.querySelectorAll("section").length,
            h1: (document.querySelector("h1") || {}).innerText || "",
            h2: document.querySelectorAll("h2").length,
            h3: document.querySelectorAll("h3").length,
            eyebrows: document.querySelectorAll(".sx-eyebrow").length,
            buttons: document.querySelectorAll(".elementor-button, .sx-cta-btn, .sx-btn").length,
            body_h: document.body.scrollHeight
        }))()''')
    except Exception as e:
        return {'error': str(e)[:50]}

async def main():
    diffs = []
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context(viewport={'width':1440,'height':900})
        for en, id_, zh, lbl in ALL_PAGES:
            print(f'\n=== {lbl} ===')
            row = {}
            for url, lang in [(en,'en'),(id_,'id'),(zh,'zh')]:
                page = await ctx.new_page()
                row[lang] = await get_stats(page, url)
                await page.close()
            for lang in ('en','id','zh'):
                r = row[lang]
                if 'error' in r:
                    print(f'  {lang}: ERROR {r["error"]}')
                else:
                    print(f"  {lang}: sec={r['sections']} h1='{r['h1'][:40]}' h2={r['h2']} h3={r['h3']} eb={r['eyebrows']} btn={r['buttons']} h={r['body_h']}")
            en_r, id_r, zh_r = row['en'], row['id'], row['zh']
            if all('error' not in x for x in [en_r, id_r, zh_r]):
                for f in ('sections','h2','h3','eyebrows','buttons'):
                    if en_r[f] != zh_r[f] or id_r[f] != zh_r[f]:
                        diffs.append(f'{lbl}.{f}: EN={en_r[f]} ID={id_r[f]} ZH={zh_r[f]}')
                # body height significantly different (>30% diff)
                e_h = en_r['body_h']; z_h = zh_r['body_h']
                if e_h > 0 and abs(e_h - z_h) / e_h > 0.30:
                    diffs.append(f'{lbl}.body_h: EN={e_h}px ZH={z_h}px ({100*(z_h-e_h)/e_h:+.0f}%)')
        await b.close()

    print('\n========== DIFFERENCES ==========')
    if diffs:
        for d in diffs: print(f'  {d}')
    else:
        print('  ✅ No structural differences detected')

asyncio.run(main())
