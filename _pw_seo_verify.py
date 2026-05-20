"""Playwright SEO verification across 22 pages.
Checks: title, meta description, Organization JSON-LD presence, hero subtitle keyword density (service pages).
"""
import asyncio, json, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

PAGES = [
    # (url, label, expected_title_fragment, expected_desc_fragment, hero_keywords_to_check)
    ('https://suriota.com/',                                          'Homepage',         'Industrial IoT & System Integration Batam', 'Modbus Gateway',           None),
    ('https://suriota.com/about-us/',                                 'About',            'About SURIOTA',                              'Industrial IoT',          None),
    ('https://suriota.com/portfolio/',                                'Portfolio',        '64+ Industrial IoT Projects',                'PDAM Tirta Kepri',        None),
    ('https://suriota.com/internship/',                               'Internship',       'Internship Industrial IoT',                  'R&D, DevOps',             None),
    ('https://suriota.com/artikel/',                                  'Artikel',          'Industrial IoT Articles',                    'KLHK SPARING',            None),
    # 4 v4.5 service pages
    ('https://suriota.com/electrical/',                               'Electrical',       'Industrial Electrical Engineering',          'SNI, IEC, PUIL',          ['oil & gas','shipyard','manufacturing']),
    ('https://suriota.com/automation/',                               'Automation',       'Industrial Automation, PLC & SCADA',         'Modbus gateway',          ['Modbus gateway','manufacturing','shipyard']),
    ('https://suriota.com/water-treatment/',                          'Water Treatment',  'KLHK SPARING Monitoring',                    'pH, COD, TSS, NH3',       ['KLHK SPARING','IPAL','pH, COD, TSS, NH3']),
    ('https://suriota.com/renewable-energy/',                         'Renewable Energy', 'Solar PV PLTS',                              'PLTS-PLTB',               ['PLTS-PLTB','smart street light','PJU']),
    # 4 v3 raw-HTML service pages
    ('https://suriota.com/internet-of-things/',                       'IoT',              'IoT & System Integration Services',          'AWS IoT Core',            ['Modbus','MQTT','AWS IoT Core','oil & gas']),
    ('https://suriota.com/data-analytics/',                           'Data Analytics',   'AI & Industrial Data Analytics',             'predictive maintenance',  ['predictive maintenance','OEE','mining']),
    ('https://suriota.com/digital-consulting/',                       'Digital Consulting','Digital Transformation Consulting',         'Industry 4.0',            ['Industry 4.0','OT/IT convergence','SCADA']),
    ('https://suriota.com/software-as-a-service/',                    'SaaS SURGE',       'SURGE SaaS',                                 'KLHK SPARING',            ['KLHK SPARING','ThingsBoard','multi-tenant']),
    # 9 product pages
    ('https://suriota.com/suriota-modbus-gateway/',                   'SRT-MGATE',        'SRT-MGATE-1210 Modbus Gateway',              'BLE config',              None),
    ('https://suriota.com/surge-energy-mapping/',                     'SURGE-Energy',     'SURGE Energy Mapping',                       'kWh',                     None),
    ('https://suriota.com/surge-vessel-tracking/',                    'SURGE-Vessel',     'SURGE Vessel Tracking',                      'Maritime IoT',            None),
    ('https://suriota.com/surge-water-analytic/',                     'SURGE-Water',      'SURGE Water Analytics',                      'KLHK SPARING',            None),
    ('https://suriota.com/iso-m485-series/',                          'ISO-M485',         'ISO-M485 Isolated RS-485',                   'isolated RS-485',         None),
    ('https://suriota.com/thm-30md/',                                 'THM-30MD',         'THM-30MD Temperature',                       'Modbus RTU',              None),
    ('https://suriota.com/pm1611-wd/',                                'PM1611-WD',        'PM1611-WD Prepaid Energy',                   'prepaid energy meter',    None),
    ('https://suriota.com/rs-485-surge-protector-spd-t485-105/',      'SPD-T485',         'RS-485 Surge Protector SPD-T485-105',        'Profibus',                None),
    ('https://suriota.com/waste-water-logger/',                       'WW Logger',        'Wastewater Data Logger',                     'IPAL',                    None),
]

OK = 'OK'
FAIL = 'X '

async def main():
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            viewport={'width': 1280, 'height': 900},
            user_agent='Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        for url, label, exp_title, exp_desc, hero_kws in PAGES:
            page = await ctx.new_page()
            row = {'label': label, 'url': url, 'status': 'ok', 'issues': []}
            try:
                resp = await page.goto(url, wait_until='domcontentloaded', timeout=30000)
                code = resp.status if resp else 0
                if code != 200:
                    row['status'] = 'fail'
                    row['issues'].append(f'HTTP {code}')
                    results.append(row); await page.close(); continue

                # Title
                title = await page.title()
                row['title'] = title
                if exp_title.lower() not in title.lower():
                    row['issues'].append(f'title missing "{exp_title}"')

                # Meta description
                desc = await page.evaluate('document.querySelector("meta[name=\'description\']")?.content || ""')
                row['desc'] = desc[:180]
                if exp_desc.lower() not in desc.lower():
                    row['issues'].append(f'desc missing "{exp_desc}"')

                # Organization JSON-LD presence + content
                org_check = await page.evaluate('''() => {
                    const scripts = Array.from(document.querySelectorAll('script[type="application/ld+json"]'));
                    for (const s of scripts) {
                        try {
                            const d = JSON.parse(s.textContent);
                            if (d['@type'] === 'Organization' && d.name === 'SURIOTA') {
                                return {
                                    found: true,
                                    services: (d.hasOfferCatalog?.itemListElement || []).length,
                                    products: (d.makesOffer || []).length,
                                    knowsAbout: (d.knowsAbout || []).length,
                                    slogan: d.slogan,
                                    sameAs: (d.sameAs || []).length
                                };
                            }
                        } catch(e) {}
                    }
                    return {found: false};
                }''')
                row['org'] = org_check
                if not org_check.get('found'):
                    row['issues'].append('Org JSON-LD missing')

                # Hero subtitle keyword check (service pages only)
                if hero_kws:
                    body_text = await page.evaluate('document.body.innerText')
                    missing = [k for k in hero_kws if k.lower() not in body_text.lower()]
                    row['hero_missing'] = missing
                    if missing:
                        row['issues'].append(f'hero kw missing: {missing}')

                if row['issues']:
                    row['status'] = 'partial'
            except Exception as e:
                row['status'] = 'error'
                row['issues'].append(f'exc: {str(e)[:120]}')

            results.append(row)
            await page.close()
        await browser.close()

    # Report
    print('\n' + '=' * 90)
    print(f'{"PAGE":<22} {"STATUS":<8} {"ORG":<6} {"ISSUES"}')
    print('=' * 90)
    ok_count = 0
    for r in results:
        org = ''
        if r.get('org', {}).get('found'):
            o = r['org']
            org = f"{o['services']}s/{o['products']}p"
        status_icon = OK if r['status'] == 'ok' else FAIL
        if r['status'] == 'ok': ok_count += 1
        issues = '; '.join(r['issues']) if r['issues'] else '-'
        print(f"{r['label']:<22} {status_icon} {r['status']:<6} {org:<6} {issues[:60]}")
    print('=' * 90)
    print(f'TOTAL: {ok_count}/{len(results)} fully ok')
    print('\nFull JSON dump → _pw_seo_report.json')
    with open('_pw_seo_report.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

asyncio.run(main())
