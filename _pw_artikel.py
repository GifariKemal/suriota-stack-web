import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 900})

        # Capture console + network errors
        page.on("console", lambda msg: print(f"[{msg.type}] {msg.text}"))
        page.on("pageerror", lambda err: print(f"[PAGEERROR] {err}"))
        page.on("response", lambda r: print(f"[NET {r.status}] {r.url[:120]}") if r.status >= 400 or '/wp-json/' in r.url else None)

        print("=== Loading /artikel/ ===")
        await page.goto("https://suriota.com/artikel/", wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(2500)

        # Check grid content
        grid_html = await page.evaluate("""() => {
            const g = document.getElementById('sxa-art-grid');
            return g ? g.innerHTML.slice(0, 500) : 'NOT FOUND';
        }""")
        print("\n=== Grid HTML (first 500 chars) ===")
        print(grid_html)

        all_count = await page.evaluate("""() => {
            return document.querySelectorAll('.sxa-art-card').length;
        }""")
        print(f"\n=== Cards rendered: {all_count} ===")

        # Get count text
        count_text = await page.evaluate("""() => {
            return document.getElementById('sxa-art-count')?.textContent;
        }""")
        print(f"Counter: {count_text}")

        await browser.close()

asyncio.run(main())
