"""Sample all 14 MED pages — dump unique English content for translation."""
import asyncio, sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

MED_PAGES = [
    ('https://suriota.com/id/magang-srt-team/', 'Internship'),
    ('https://suriota.com/id/water-treatment-id/', 'WT'),
    ('https://suriota.com/id/saas-id/', 'SaaS'),
    ('https://suriota.com/id/electrical-id/', 'Electrical'),
    ('https://suriota.com/id/automation-id/', 'Automation'),
    ('https://suriota.com/id/renewable-energy-id/', 'RE'),
    ('https://suriota.com/id/internet-of-things-id/', 'IoT'),
    ('https://suriota.com/id/digital-consulting-id/', 'DC'),
    ('https://suriota.com/id/surge-energy-mapping-id/', 'SURGE-E'),
    ('https://suriota.com/id/surge-vessel-tracking-id/', 'SURGE-V'),
    ('https://suriota.com/id/iso-m485-series-id/', 'ISO-M485'),
    ('https://suriota.com/id/pm1611-wd-id/', 'PM1611'),
    ('https://suriota.com/id/rs-485-surge-protector-id/', 'SPD-T485'),
    ('https://suriota.com/id/waste-water-logger-id/', 'WW'),
]

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        for url, lbl in MED_PAGES:
            page = await b.new_page()
            await page.goto(url + '?cb=' + str(time.time()), wait_until='domcontentloaded', timeout=20000)
            await page.wait_for_timeout(800)
            txt = await page.evaluate('document.body.innerText')
            # Find lines with significant English content
            import re
            lines = [l.strip() for l in txt.split('\n') if l.strip()]
            en_lines = []
            for l in lines:
                if len(l) < 15: continue
                # Count English words
                en_count = sum(1 for w in [' the ', ' and ', ' for ', ' with ', ' from ', ' our ', ' we ', ' you ', ' is ', ' are ', ' have ', ' to ', ' on ', ' in ', 'engineering team'] if w in l.lower())
                if en_count >= 2:
                    en_lines.append(l)
            print(f'\n========== {lbl} ({len(en_lines)} EN-heavy lines) ==========')
            for l in en_lines[:20]:
                print(f'  - {l[:140]}')
            await page.close()
        await b.close()

asyncio.run(main())
