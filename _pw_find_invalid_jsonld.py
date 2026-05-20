"""Find which JSON-LD script tag is INVALID — try parsing each individually."""
import asyncio, sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://suriota.com/', wait_until='domcontentloaded', timeout=30000)
        out = await page.evaluate('''() => {
            const scripts = Array.from(document.querySelectorAll('script[type="application/ld+json"]'));
            return scripts.map((s, idx) => {
                const text = s.textContent;
                let parsed = null, error = null, type = null;
                try {
                    parsed = JSON.parse(text);
                    type = parsed['@type'] || (parsed['@graph'] && 'graph') || 'unknown';
                } catch(e) { error = e.message; }
                return {
                    idx,
                    length: text.length,
                    head: text.slice(0, 200).replace(/\\s+/g, ' '),
                    tail: text.slice(-150).replace(/\\s+/g, ' '),
                    parsed_type: type,
                    error: error
                };
            });
        }''')
        await browser.close()

        print(f'Total JSON-LD blocks: {len(out)}')
        for o in out:
            status = 'OK' if not o['error'] else 'INVALID'
            print(f"\n[{o['idx']}] {status} type={o['parsed_type']} len={o['length']}")
            if o['error']:
                print(f"  ERROR: {o['error']}")
                print(f"  HEAD: {o['head']}")
                print(f"  TAIL: {o['tail']}")
            else:
                print(f"  head: {o['head'][:100]}")

asyncio.run(main())
