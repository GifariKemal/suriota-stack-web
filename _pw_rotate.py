import asyncio
from playwright.async_api import async_playwright

async def check_related(page, url, label):
    page.on("pageerror", lambda err: print(f"[{label} ERR] {err}"))
    await page.goto(url, wait_until="networkidle", timeout=30000)
    await page.wait_for_timeout(2500)
    titles = await page.evaluate("""() => {
        return [...document.querySelectorAll('.sxa-rel-title')].map(el => el.textContent.trim());
    }""")
    print(f"\n[{label}] {url}")
    print(f"  Related count: {len(titles)}")
    for t in titles: print(f"  - {t[:70]}")
    return titles

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # Test 3 different posts
        urls = [
            ("post-1474-electrical", "https://suriota.com/setup-genset-dse-5520/"),
            ("post-1462-iot", "https://suriota.com/sistem-pakan-ikan-control-monitoring-pakan-ikan-berbasis-iot/"),
            ("post-1454-water", "https://suriota.com/maintenance-sparing-wwtp/"),
        ]
        results = {}
        for label, url in urls:
            page = await browser.new_page(viewport={"width":1280,"height":900})
            titles = await check_related(page, url, label)
            results[label] = titles
            await page.close()

        # Check if related articles differ between posts
        print("\n=== ROTATION CHECK ===")
        all_titles = [tuple(v) for v in results.values()]
        unique = len(set(all_titles))
        print(f"Unique title sets: {unique}/{len(all_titles)} {'GOOD' if unique > 1 else 'BAD (all same)'}")
        await browser.close()

asyncio.run(main())
