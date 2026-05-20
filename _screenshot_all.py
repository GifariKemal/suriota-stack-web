"""Capture viewport screenshots of all key pages."""
import asyncio, sys, io, time, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

PAGES = [
    ('https://suriota.com/', '01_home_en'),
    ('https://suriota.com/id/beranda/', '02_home_id'),
    ('https://suriota.com/about/', '03_about_en'),
    ('https://suriota.com/id/tentang-kami/', '04_about_id'),
    ('https://suriota.com/portfolio/', '05_portfolio_en'),
    ('https://suriota.com/id/portfolio-id/', '06_portfolio_id'),
    ('https://suriota.com/contact/', '07_contact_en'),
    ('https://suriota.com/id/kontak/', '08_contact_id'),
    ('https://suriota.com/automation/', '09_automation'),
    ('https://suriota.com/electrical/', '10_electrical'),
    ('https://suriota.com/renewable-energy/', '11_renewable'),
    ('https://suriota.com/internet-of-things/', '12_iot'),
    ('https://suriota.com/water-treatment/', '13_water'),
    ('https://suriota.com/data-analytics/', '14_data_analytics'),
    ('https://suriota.com/digital-consulting/', '15_consulting'),
    ('https://suriota.com/artificial-intelligence/', '16_ai'),
    ('https://suriota.com/system-integration/', '17_sysint'),
    ('https://suriota.com/saas/', '18_saas'),
    ('https://suriota.com/surge-energy-mapping/', '19_surge_energy'),
    ('https://suriota.com/surge-vessel-tracking/', '20_surge_vessel'),
    ('https://suriota.com/surge-water-analytic/', '21_surge_water'),
    ('https://suriota.com/suriota-modbus-gateway/', '22_mgate'),
    ('https://suriota.com/iso-m485-series/', '23_iso_m485'),
    ('https://suriota.com/pm1611-wd/', '24_pm1611'),
    ('https://suriota.com/thm-30md/', '25_thm30md'),
    ('https://suriota.com/rs-485-surge-protector/', '26_spd_t485'),
    ('https://suriota.com/waste-water-logger/', '27_ww_logger'),
    ('https://suriota.com/privacy-policy/', '28_privacy_en'),
    ('https://suriota.com/terms-of-service/', '29_terms_en'),
    ('https://suriota.com/id/kebijakan-privasi/', '30_privacy_id'),
    ('https://suriota.com/id/syarat-layanan/', '31_terms_id'),
]

OUT_DIR = '_screenshots'
os.makedirs(OUT_DIR, exist_ok=True)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context(viewport={'width':1440,'height':900})
        for url, name in PAGES:
            page = await ctx.new_page()
            try:
                resp = await page.goto(url + '?nc='+str(time.time()), wait_until='domcontentloaded', timeout=30000)
                if resp and resp.status >= 400:
                    print(f'{name} HTTP {resp.status}')
                    await page.close(); continue
                await page.wait_for_timeout(2000)
                # Viewport only (no fullpage to keep files manageable)
                await page.screenshot(path=f'{OUT_DIR}/{name}.png', full_page=False)
                print(f'✓ {name}')
            except Exception as e:
                print(f'✗ {name}: {str(e)[:60]}')
            await page.close()
        await b.close()

asyncio.run(main())
print('All done')
