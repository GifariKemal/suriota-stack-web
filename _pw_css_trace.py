import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for slug in ['data-analytics', 'internet-of-things']:
            page = await browser.new_page()
            css_urls = []
            page.on("response", lambda r: css_urls.append(r.url) if r.url.endswith('.css') or '/elementor/' in r.url.lower() and 'css' in r.url else None)
            await page.goto(f'https://suriota.com/{slug}/', wait_until="networkidle", timeout=30000)
            await page.wait_for_timeout(1500)
            # Get all stylesheets loaded
            sheets = await page.evaluate("""() => {
                return Array.from(document.styleSheets).map(s => ({
                    href: s.href || '(inline)',
                    rules: s.cssRules ? s.cssRules.length : 'CORS',
                    hasService: (s.cssRules && Array.from(s.cssRules).some(r => r.selectorText && r.selectorText.includes('sx-page-service')))
                }));
            }""")
            print(f'\n=== /{slug}/ ===')
            print(f'Total stylesheets: {len(sheets)}')
            for s in sheets:
                marker = ' <- has .sx-page-service!' if s['hasService'] else ''
                print(f'  href: {s["href"][:90]} | rules: {s["rules"]}{marker}')
            await page.close()
        await browser.close()

asyncio.run(main())
