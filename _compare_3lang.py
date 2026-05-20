"""Side-by-side comparison EN/ID/ZH for key pages — find inconsistencies."""
import asyncio, sys, time, os, re
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except: pass
from playwright.async_api import async_playwright

# Map: (EN URL, ID URL, ZH URL, label)
PAGES = [
    ('https://suriota.com/', 'https://suriota.com/id/beranda/', 'https://suriota.com/shouye/', 'home'),
    ('https://suriota.com/about-us/', 'https://suriota.com/id/tentang-kami/', 'https://suriota.com/guanyu-women/', 'about'),
    ('https://suriota.com/portfolio/', 'https://suriota.com/id/portfolio-id/', 'https://suriota.com/anli/', 'portfolio'),
    ('https://suriota.com/contact/', 'https://suriota.com/id/kontak/', 'https://suriota.com/lianxi/', 'contact'),
    ('https://suriota.com/automation/', 'https://suriota.com/id/automation-id/', 'https://suriota.com/zidonghua/', 'automation'),
    ('https://suriota.com/iso-m485-series/', 'https://suriota.com/id/iso-m485-series-id/', 'https://suriota.com/iso-m485/', 'iso_m485'),
    ('https://suriota.com/surge-energy-mapping/', 'https://suriota.com/id/surge-energy-mapping-id/', 'https://suriota.com/surge-energy-mapping-2/', 'surge_e'),
]

os.makedirs('_screenshots/compare', exist_ok=True)
EN_WORDS = [' the ', ' and ', ' for ', ' with ', ' from ', ' you ', ' will ', ' our ', ' we ', ' is ', ' are ', ' that ', ' this ', ' to ', ' of ']

async def main():
    issues = []
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context(viewport={'width':1440,'height':900})
        for en_url, id_url, zh_url, lbl in PAGES:
            row = {'page': lbl}
            for url, lang in [(en_url,'en'),(id_url,'id'),(zh_url,'zh')]:
                page = await ctx.new_page()
                try:
                    resp = await page.goto(url+'?nc='+str(time.time()), wait_until='networkidle', timeout=45000)
                    await page.wait_for_timeout(2500)
                    # Stats
                    body_h = await page.evaluate('document.body.scrollHeight')
                    sections = await page.evaluate('document.querySelectorAll("section").length')
                    h1 = await page.evaluate('(document.querySelector("h1") || {}).innerText || ""')
                    h2_count = await page.evaluate('document.querySelectorAll("h2").length')
                    h3_count = await page.evaluate('document.querySelectorAll("h3").length')
                    eyebrows = await page.evaluate('document.querySelectorAll(".sx-eyebrow").length')
                    buttons = await page.evaluate('document.querySelectorAll(".elementor-button, .sx-cta-btn, .sx-btn").length')
                    images = await page.evaluate('document.querySelectorAll("img").length')
                    # EN word count in body
                    body_text = await page.evaluate('document.body.innerText')
                    lines = [l for l in body_text.split('\n') if len(l.strip()) > 30]
                    en_lines = [l for l in lines if sum(1 for w in EN_WORDS if w in l.lower()) >= 4]
                    await page.screenshot(path=f'_screenshots/compare/{lbl}_{lang}.png', full_page=False)
                    row[lang] = {
                        'h1': h1[:60], 'h2': h2_count, 'h3': h3_count,
                        'sections': sections, 'body_h': body_h,
                        'eyebrows': eyebrows, 'buttons': buttons, 'images': images,
                        'en_lines_count': len(en_lines),
                        'en_sample': en_lines[0][:120] if en_lines else ''
                    }
                except Exception as e:
                    row[lang] = {'error': str(e)[:60]}
                await page.close()

            # Compare
            print(f'\n=== {lbl.upper()} ===')
            for lang in ('en','id','zh'):
                r = row.get(lang, {})
                if 'error' in r:
                    print(f'  {lang}: ERROR {r["error"]}')
                else:
                    print(f"  {lang}: h1='{r['h1']}' sections={r['sections']} h2={r['h2']} h3={r['h3']} eyebrows={r['eyebrows']} buttons={r['buttons']} body_h={r['body_h']}px en_lines={r['en_lines_count']}")
                    if r['en_sample']:
                        print(f"       EN sample: {r['en_sample']}")
            # Find inconsistencies
            en, id_, zh = row.get('en',{}), row.get('id',{}), row.get('zh',{})
            if all(isinstance(x, dict) and 'error' not in x for x in [en, id_, zh]):
                # Structural differences
                for field in ('sections','h2','h3','eyebrows','buttons'):
                    e = en.get(field,0); i = id_.get(field,0); z = zh.get(field,0)
                    if e != z or i != z:
                        issues.append(f'{lbl}: {field} EN={e} ID={i} ZH={z}')

    print('\n========== STRUCTURAL DIFFERENCES ==========')
    for i in issues:
        print(f'  {i}')

asyncio.run(main())
