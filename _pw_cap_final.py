import asyncio, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context(viewport={'width': 1440, 'height': 900})
        page = await ctx.new_page()
        await page.goto('https://suriota.com/?cb=final', wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(2500)
        # Use locator to scroll element into view
        await page.locator('[data-id="49b2d08"]').scroll_into_view_if_needed()
        await page.wait_for_timeout(500)
        await page.locator('[data-id="49b2d08"]').screenshot(path='_hp_cap_final.png')
        print('Saved -> _hp_cap_final.png')
        await b.close()

asyncio.run(main())
