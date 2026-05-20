"""Full ZH page audit — screenshot + check fonts, eyebrows, English remnants, sizes."""
import asyncio, sys, time, json, os
try: sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except: pass
from playwright.async_api import async_playwright

ZH_PAGES = [
    ('https://suriota.com/shouye/', '01_home', 5448, '首页'),
    ('https://suriota.com/guanyu-women/', '02_about', 5450, '关于 SURIOTA'),
    ('https://suriota.com/anli/', '03_portfolio', 5454, '项目案例'),
    ('https://suriota.com/lianxi/', '04_contact', 5465, '联系我们'),
    ('https://suriota.com/zidonghua/', '05_automation', 5451, '自动化'),
    ('https://suriota.com/dianqi-gongcheng/', '06_electrical', 5452, '电气工程'),
    ('https://suriota.com/kezaisheng-nengyuan/', '07_renewable', 5453, '可再生能源'),
    ('https://suriota.com/iot/', '08_iot', 5468, '物联网'),
    ('https://suriota.com/shuichuli/', '09_wt', 5457, '水处理'),
    ('https://suriota.com/shujufenxi/', '10_data_analytics', 5472, '数据分析'),
    ('https://suriota.com/shuzihua-zixun/', '11_consulting', 5470, '数字化咨询'),
    ('https://suriota.com/rengong-zhineng/', '12_ai', 5471, '人工智能'),
    ('https://suriota.com/xitong-jicheng/', '13_sysint', 5469, '系统集成'),
    ('https://suriota.com/saas/', '14_saas', 5473, '软件即服务'),
    ('https://suriota.com/surge-energy-mapping-2/', '15_surge_energy', 5458, 'SURGE-E'),
    ('https://suriota.com/surge-vessel-tracking-2/', '16_surge_vessel', 5459, 'SURGE-V'),
    ('https://suriota.com/surge-water-analytic-2/', '17_surge_water', 5460, 'SURGE-W'),
    ('https://suriota.com/modbus-gateway/', '18_mgate', 5456, 'Modbus网关'),
    ('https://suriota.com/iso-m485/', '19_iso_m485', 5461, 'ISO-M485'),
    ('https://suriota.com/pm1611-wd-2/', '20_pm1611', 5463, 'PM1611-WD'),
    ('https://suriota.com/thm-30md-2/', '21_thm30md', 5462, 'THM-30MD'),
    ('https://suriota.com/rs-485-spd/', '22_spd_t485', 5464, 'SPD-T485'),
    ('https://suriota.com/wastewater-logger/', '23_ww_logger', 5455, 'WW Logger'),
    ('https://suriota.com/yinsi-zhengce/', '24_privacy', 5466, '隐私政策'),
    ('https://suriota.com/fuwu-tiaokuan/', '25_terms', 5467, '服务条款'),
]

EN_MARKERS = [' the ', ' and ', ' for ', ' with ', ' from ', ' you ', ' will ', ' our ', ' we ', ' is ', ' are ', ' that ', ' this ', ' to ', ' by ', ' of ', ' in ']

os.makedirs('_screenshots/zh', exist_ok=True)

async def main():
    results = []
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context(viewport={'width':1440,'height':900})
        for url, name, pid, title in ZH_PAGES:
            page = await ctx.new_page()
            try:
                resp = await page.goto(url+'?nc='+str(time.time()), wait_until='domcontentloaded', timeout=30000)
                await page.wait_for_timeout(2000)
                code = resp.status if resp else 0
                # font
                font = await page.evaluate('getComputedStyle(document.body).fontFamily.split(",")[0].trim()')
                # check nav state
                nav = await page.evaluate('''(() => {
                    var btn = document.querySelector('.sx-hf-v5-lang .sx-hf-v5-dropbtn');
                    return btn ? btn.innerText.trim().replace(/\\n/g, ' ') : 'no btn';
                })()''')
                # count EN words in body
                body = await page.evaluate('document.body.innerText')
                # Take long sentences (>40 chars)
                lines = [l.strip() for l in body.split('\n') if len(l.strip()) > 40]
                en_lines = []
                for ln in lines:
                    en_count = sum(1 for w in EN_MARKERS if w in ln.lower())
                    if en_count >= 4:
                        en_lines.append(ln[:150])
                # Find any pure English eyebrow (uppercase short labels)
                en_eyebrows = await page.evaluate('''(() => {
                    var arr = [];
                    document.querySelectorAll('.sx-eyebrow').forEach(el => {
                        var t = (el.innerText||'').trim();
                        if (t && /^[A-Z][A-Z0-9 \\&\\-\\.]+$/.test(t) && t.length < 40 && t !== 'FAQ' && t !== 'SAAS' && !/^SURGE/.test(t) && !/^RS-485/.test(t) && !/^SAAS/.test(t)) {
                            arr.push(t);
                        }
                    });
                    return arr;
                })()''')
                await page.screenshot(path=f'_screenshots/zh/{name}.png', full_page=False)
                results.append({
                    'name': name, 'pid': pid, 'url': url, 'code': code, 'font': font, 'nav': nav,
                    'en_lines_count': len(en_lines), 'en_lines': en_lines[:3],
                    'en_eyebrows': en_eyebrows
                })
                print(f'  ✓ {name} ({pid}): {code} font={font} nav={nav} en_lines={len(en_lines)} eyebrows_EN={len(en_eyebrows)}')
            except Exception as e:
                print(f'  ✗ {name}: {str(e)[:80]}')
                results.append({'name':name, 'error': str(e)[:80]})
            await page.close()
        await b.close()

    # Report
    print('\n========== ZH AUDIT REPORT ==========')
    fonts_seen = set()
    bad_pages = []
    for r in results:
        if 'error' in r: continue
        fonts_seen.add(r['font'])
        flag = '⚠️' if r['en_lines_count'] > 0 or r['en_eyebrows'] else '✓'
        print(f"{flag} {r['name']:25s} {r['code']} nav={r['nav']:10s} EN_lines={r['en_lines_count']:2d} EN_eyebrows={r['en_eyebrows']}")
        if r['en_lines_count'] > 0:
            for ln in r['en_lines']:
                print(f"      > {ln}")
            bad_pages.append(r['name'])

    print(f'\nFonts seen: {fonts_seen}')
    print(f'Pages with EN residual: {len(bad_pages)}')

asyncio.run(main())
