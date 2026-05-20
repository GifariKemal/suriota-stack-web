import asyncio, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context(
            viewport={'width': 390, 'height': 844},
            device_scale_factor=3,
            is_mobile=True,
            has_touch=True,
            user_agent='Mozilla/5.0 (iPhone) Mobile'
        )
        page = await ctx.new_page()
        await page.goto('https://suriota.com/?cb=fabf', wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(3000)
        # Scroll to middle for clean view
        await page.evaluate('window.scrollTo(0, 300)')
        await page.wait_for_timeout(1000)
        # Full viewport screenshot showing bottom area
        await page.screenshot(path='_mob_fab_final.png', clip={'x': 0, 'y': 700, 'width': 390, 'height': 144})
        print('Saved _mob_fab_final.png')

        fab = await page.evaluate('''() => {
            const f = document.querySelector('.sx-wa-fab');
            if (!f) return null;
            const r = f.getBoundingClientRect();
            return {
                left: Math.round(r.left),
                bottom: Math.round(window.innerHeight - r.bottom),
                w: Math.round(r.width),
                h: Math.round(r.height)
            };
        }''')
        print(f'FAB position: {fab}')
        await b.close()

asyncio.run(main())
