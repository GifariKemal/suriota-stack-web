"""Visual + content verify of synced ID About page."""
import asyncio, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context(viewport={'width': 1440, 'height': 900})

        # Side-by-side: EN vs ID
        for url, lbl in [('https://suriota.com/about-us/?cb=verif', 'EN'),
                         ('https://suriota.com/id/tentang-kami/?cb=verif', 'ID')]:
            page = await ctx.new_page()
            await page.goto(url, wait_until='networkidle', timeout=30000)
            await page.wait_for_timeout(2000)
            data = await page.evaluate('''() => {
                return {
                    h1: Array.from(document.querySelectorAll('h1')).filter(e => getComputedStyle(e).display !== 'none').map(e => e.textContent.trim()),
                    h2: Array.from(document.querySelectorAll('h2')).filter(e => getComputedStyle(e).display !== 'none').map(e => e.textContent.trim().slice(0, 80)),
                    h3: Array.from(document.querySelectorAll('h3')).filter(e => getComputedStyle(e).display !== 'none').map(e => e.textContent.trim().slice(0, 80)),
                    text_length: document.body.innerText.length,
                    cards: document.querySelectorAll('article').length
                };
            }''')
            print(f'\n[{lbl}] {url}')
            print(f"  H1: {data['h1']}")
            print(f"  H2 ({len(data['h2'])}): {data['h2']}")
            print(f"  H3 ({len(data['h3'])}): {data['h3'][:6]}")
            print(f"  Article cards: {data['cards']}")
            print(f"  Total text: {data['text_length']} chars")

            slug_part = 'id' if 'id' in url else 'en'
            await page.screenshot(path=f'_about_{slug_part}.png', full_page=True)
            print(f'  Screenshot saved -> _about_{slug_part}.png')
            await page.close()

        await b.close()

asyncio.run(main())
