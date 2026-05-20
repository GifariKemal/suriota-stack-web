"""Full audit — switcher + Bahasa% + em-dash for all 22 ID + 22 EN pages."""
import asyncio, sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

EN_PAGES = [
    ('https://suriota.com/', 'Homepage'),
    ('https://suriota.com/about-us/', 'About'),
    ('https://suriota.com/portfolio/', 'Portfolio'),
    ('https://suriota.com/internship/', 'Internship'),
    ('https://suriota.com/water-treatment/', 'WT'),
    ('https://suriota.com/software-as-a-service/', 'SaaS'),
    ('https://suriota.com/artikel/', 'Artikel'),
    ('https://suriota.com/electrical/', 'Electrical'),
    ('https://suriota.com/automation/', 'Automation'),
    ('https://suriota.com/renewable-energy/', 'RE'),
    ('https://suriota.com/internet-of-things/', 'IoT'),
    ('https://suriota.com/data-analytics/', 'DA'),
    ('https://suriota.com/digital-consulting/', 'DC'),
    ('https://suriota.com/suriota-modbus-gateway/', 'MGATE'),
    ('https://suriota.com/surge-energy-mapping/', 'SURGE-E'),
    ('https://suriota.com/surge-vessel-tracking/', 'SURGE-V'),
    ('https://suriota.com/surge-water-analytic/', 'SURGE-W'),
    ('https://suriota.com/iso-m485-series/', 'ISO-M485'),
    ('https://suriota.com/thm-30md/', 'THM-30MD'),
    ('https://suriota.com/pm1611-wd/', 'PM1611'),
    ('https://suriota.com/rs-485-surge-protector-spd-t485-105/', 'SPD-T485'),
    ('https://suriota.com/waste-water-logger/', 'WW'),
]

ID_PAGES = [
    ('https://suriota.com/id/beranda/', 'ID Homepage'),
    ('https://suriota.com/id/tentang-kami/', 'ID About'),
    ('https://suriota.com/id/portfolio-id/', 'ID Portfolio'),
    ('https://suriota.com/id/magang-srt-team/', 'ID Internship'),
    ('https://suriota.com/id/water-treatment-id/', 'ID WT'),
    ('https://suriota.com/id/saas-id/', 'ID SaaS'),
    ('https://suriota.com/id/artikel-id/', 'ID Artikel'),
    ('https://suriota.com/id/electrical-id/', 'ID Electrical'),
    ('https://suriota.com/id/automation-id/', 'ID Automation'),
    ('https://suriota.com/id/renewable-energy-id/', 'ID RE'),
    ('https://suriota.com/id/internet-of-things-id/', 'ID IoT'),
    ('https://suriota.com/id/data-analytics-id/', 'ID DA'),
    ('https://suriota.com/id/digital-consulting-id/', 'ID DC'),
    ('https://suriota.com/id/suriota-modbus-gateway-id/', 'ID MGATE'),
    ('https://suriota.com/id/surge-energy-mapping-id/', 'ID SURGE-E'),
    ('https://suriota.com/id/surge-vessel-tracking-id/', 'ID SURGE-V'),
    ('https://suriota.com/id/surge-water-analytic-id/', 'ID SURGE-W'),
    ('https://suriota.com/id/iso-m485-series-id/', 'ID ISO-M485'),
    ('https://suriota.com/id/thm-30md-id/', 'ID THM-30MD'),
    ('https://suriota.com/id/pm1611-wd-id/', 'ID PM1611'),
    ('https://suriota.com/id/rs-485-surge-protector-id/', 'ID SPD-T485'),
    ('https://suriota.com/id/waste-water-logger-id/', 'ID WW'),
]

ID_WORDS = ['adalah','dan','untuk','dari','yang','akan','dengan','pada','kami','Sistem','Layanan','Industri','dalam','Anda','tim','proyek','dapat','sesuai','telah','seperti','itu','ini','seluruh','memiliki','antara','siap','tanpa','setiap','melalui','tersebut','sebagai','membantu','digunakan']
EN_WORDS = ['the ',' and ',' for ',' from ',' with ',' our ',' we ',' you ',' is ',' are ',' will ',' have ','engineering team','reduce','provides','enables']


async def audit_page(ctx, url, lbl):
    page = await ctx.new_page()
    result = {'lbl': lbl, 'url': url, 'http': 0, 'switcher_ok': False, 'bahasa_pct': 0, 'em_html': 0, 'em_text': 0}
    try:
        resp = await page.goto(url + '?cb=' + str(time.time()), wait_until='domcontentloaded', timeout=20000)
        result['http'] = resp.status if resp else 0
        await page.wait_for_timeout(800)

        data = await page.evaluate('''() => {
            const lang = document.querySelector('.sx-hf-v5-lang');
            const btn = lang ? lang.querySelector('.sx-hf-v5-dropbtn') : null;
            const items = lang ? Array.from(lang.querySelectorAll('.sx-hf-v5-lang-content a, .sx-hf-v5-lang-content .sx-lang-disabled')) : [];
            const txt = document.body.innerText;
            const html = document.documentElement.outerHTML;
            return {
                switcher_present: !!lang,
                btn_text: btn ? btn.textContent.trim() : null,
                items_count: items.length,
                has_cn_coming: items.some(i => /CN.*Coming/i.test(i.textContent)),
                body_text: txt,
                em_in_text: (txt.match(/\\u2014/g) || []).length,
                em_in_html: (html.match(/\\u2014/g) || []).length
            };
        }''')

        result['switcher_ok'] = data['switcher_present'] and data['btn_text'] and data['items_count'] >= 2 and data['has_cn_coming']
        result['btn_text'] = data['btn_text']
        result['em_html'] = data['em_in_html']
        result['em_text'] = data['em_in_text']

        # Bahasa% only for ID pages
        if 'ID ' in lbl:
            txt = data['body_text']
            idh = sum(txt.count(w) for w in ID_WORDS)
            enh = sum(txt.count(w) for w in EN_WORDS)
            result['bahasa_pct'] = round(idh / max(idh + enh, 1) * 100)
    except Exception as e:
        result['error'] = str(e)[:60]
    await page.close()
    return result


async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context(viewport={'width':1440,'height':900})

        # === EN pages ===
        print('=== 22 EN PAGES ===')
        en_results = []
        for url, lbl in EN_PAGES:
            r = await audit_page(ctx, url, lbl)
            en_results.append(r)
            switch = 'OK' if r['switcher_ok'] else 'MISS'
            em_tag = '' if r['em_html'] == 0 else f' [emdash:{r["em_html"]}]'
            http = r['http']
            print(f"  {lbl:14} HTTP={http} switch={switch} btn='{r.get('btn_text', '')}'{em_tag}")

        # === ID pages ===
        print('\n=== 22 ID PAGES ===')
        id_results = []
        for url, lbl in ID_PAGES:
            r = await audit_page(ctx, url, lbl)
            id_results.append(r)
            switch = 'OK' if r['switcher_ok'] else 'MISS'
            em_tag = '' if r['em_html'] == 0 else f' [emdash:{r["em_html"]}]'
            tier = 'GOOD' if r['bahasa_pct'] >= 70 else ('MED' if r['bahasa_pct'] >= 40 else 'LOW')
            print(f"  {lbl:14} HTTP={r['http']} switch={switch} {tier}={r['bahasa_pct']}% btn='{r.get('btn_text','')}'{em_tag}")

        # Summary
        all_results = en_results + id_results
        http_ok = sum(1 for r in all_results if r['http'] == 200)
        switch_ok = sum(1 for r in all_results if r['switcher_ok'])
        em_dirty = [r['lbl'] for r in all_results if r['em_html'] > 0]
        id_good = sum(1 for r in id_results if r['bahasa_pct'] >= 70)
        id_med = sum(1 for r in id_results if 40 <= r['bahasa_pct'] < 70)
        id_low = sum(1 for r in id_results if r['bahasa_pct'] < 40)

        print('\n' + '=' * 60)
        print('FINAL SUMMARY')
        print('=' * 60)
        print(f"HTTP 200       : {http_ok}/44")
        print(f"Switcher OK    : {switch_ok}/44")
        print(f"Em-dash dirty  : {len(em_dirty)} pages — {em_dirty if em_dirty else 'NONE'}")
        print(f"ID Bahasa GOOD : {id_good}/22 (>=70%)")
        print(f"ID Bahasa MED  : {id_med}/22 (40-69%)")
        print(f"ID Bahasa LOW  : {id_low}/22 (<40%)")

        await b.close()

asyncio.run(main())
