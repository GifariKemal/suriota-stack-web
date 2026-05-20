"""Comprehensive English-content audit on all 27 ID pages."""
import asyncio, sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

PAGES = [
    ('https://suriota.com/id/beranda/', 'Homepage'),
    ('https://suriota.com/id/tentang-kami/', 'About'),
    ('https://suriota.com/id/portfolio-id/', 'Portfolio'),
    ('https://suriota.com/id/magang-srt-team/', 'Internship'),
    ('https://suriota.com/id/water-treatment-id/', 'WT'),
    ('https://suriota.com/id/saas-id/', 'SaaS'),
    ('https://suriota.com/id/artikel-id/', 'Artikel'),
    ('https://suriota.com/id/electrical-id/', 'Electrical'),
    ('https://suriota.com/id/automation-id/', 'Automation'),
    ('https://suriota.com/id/renewable-energy-id/', 'RE'),
    ('https://suriota.com/id/internet-of-things-id/', 'IoT'),
    ('https://suriota.com/id/data-analytics-id/', 'DA'),
    ('https://suriota.com/id/digital-consulting-id/', 'DC'),
    ('https://suriota.com/id/suriota-modbus-gateway-id/', 'MGATE'),
    ('https://suriota.com/id/surge-energy-mapping-id/', 'SURGE-E'),
    ('https://suriota.com/id/surge-vessel-tracking-id/', 'SURGE-V'),
    ('https://suriota.com/id/surge-water-analytic-id/', 'SURGE-W'),
    ('https://suriota.com/id/iso-m485-series-id/', 'ISO-M485'),
    ('https://suriota.com/id/thm-30md-id/', 'THM-30MD'),
    ('https://suriota.com/id/pm1611-wd-id/', 'PM1611'),
    ('https://suriota.com/id/rs-485-surge-protector-id/', 'SPD-T485'),
    ('https://suriota.com/id/waste-water-logger-id/', 'WW'),
    ('https://suriota.com/id/kontak/', 'Contact'),
    ('https://suriota.com/id/kebijakan-privasi/', 'Privacy'),
    ('https://suriota.com/id/syarat-layanan/', 'Terms'),
    ('https://suriota.com/id/artificial-intelligence-id/', 'AI'),
    ('https://suriota.com/id/system-integration-id/', 'SysInt'),
]

# Strong English indicators (words that indicate clearly English sentences)
EN_STRONG = [' the ', ' and ', ' for ', ' with ', ' from ', ' you ', ' is ', ' are ', ' to ', ' on ', ' in ', ' your ', ' our ', ' we ', ' have ', ' that ', ' this ', ' will ', ' has ', ' can ']

async def main():
    output = []
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context(viewport={'width':1440,'height':900})
        for url, lbl in PAGES:
            page = await ctx.new_page()
            try:
                await page.goto(url + '?cb=' + str(time.time()), wait_until='domcontentloaded', timeout=20000)
                await page.wait_for_timeout(800)
                txt = await page.evaluate('document.body.innerText')
                lines = [l.strip() for l in txt.split('\n') if len(l.strip()) > 25]
                en_lines = []
                for l in lines:
                    en_count = sum(1 for w in EN_STRONG if w in l.lower())
                    if en_count >= 2:
                        en_lines.append(l)
                output.append(f'\n========== {lbl} ({len(en_lines)} English lines) ==========')
                for ln in en_lines[:25]:
                    output.append(f'  > {ln[:200]}')
            except Exception as e:
                output.append(f'\n[{lbl}] ERR {str(e)[:60]}')
            await page.close()
        await b.close()

    full = '\n'.join(output)
    print(full)
    with open('_audit_id_pages.txt', 'w', encoding='utf-8') as f:
        f.write(full)

asyncio.run(main())
