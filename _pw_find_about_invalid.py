import asyncio, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://suriota.com/about-us/', wait_until='domcontentloaded', timeout=30000)
        out = await page.evaluate('''() => {
            const scripts = Array.from(document.querySelectorAll('script[type="application/ld+json"]'));
            return scripts.map((s, idx) => {
                let error = null, type = null;
                try { const d = JSON.parse(s.textContent); type = d['@type'] || (d['@graph'] && 'graph'); }
                catch(e) { error = e.message; }
                return { idx, length: s.textContent.length, type, error, head: s.textContent.slice(0, 250), id: s.id || '(no id)' };
            });
        }''')
        await browser.close()

        print(f'Total scripts: {len(out)}')
        for o in out:
            print(f"\n[{o['idx']}] id='{o['id']}' type={o['type']} len={o['length']}")
            if o['error']:
                print(f"  ERROR: {o['error']}")
                print(f"  HEAD: {o['head'][:250]}")

asyncio.run(main())
