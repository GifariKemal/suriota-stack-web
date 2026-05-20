"""Find which images lack alt text on key pages."""
import asyncio, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

PAGES = [
    'https://suriota.com/',
    'https://suriota.com/suriota-modbus-gateway/',
    'https://suriota.com/surge-water-analytic/',
]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        for url in PAGES:
            await page.goto(url, wait_until='domcontentloaded', timeout=30000)
            await page.wait_for_timeout(1500)
            imgs = await page.evaluate('''() => {
                return Array.from(document.querySelectorAll('img')).map(i => ({
                    src: i.src,
                    alt: i.alt,
                    class: i.className,
                    parent: i.parentElement?.tagName,
                    parent_class: i.parentElement?.className
                }));
            }''')
            print(f'\n=== {url} ===')
            no_alt = [i for i in imgs if not i['alt'] or i['alt'].strip() == '']
            print(f'Total: {len(imgs)}, Missing alt: {len(no_alt)}')
            for i in no_alt:
                src = i['src'].rsplit('/', 1)[-1].split('?')[0][:60]
                print(f"  - src={src} cls='{i['class'][:40]}' parent={i['parent']}.{(i['parent_class'] or '')[:40]}")
        await browser.close()

asyncio.run(main())
