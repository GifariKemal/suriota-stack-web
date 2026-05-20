import asyncio
from playwright.async_api import async_playwright

URLS = [
    "https://suriota.com/data-analytics/",
    "https://suriota.com/digital-consulting/",
    "https://suriota.com/software-as-a-service/",
    "https://suriota.com/internet-of-things/",
]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": 1280, "height": 900})
        for url in URLS:
            page = await ctx.new_page()
            try:
                await page.goto(url, wait_until="networkidle", timeout=30000)
                await page.wait_for_timeout(1500)
                m = await page.evaluate("""() => {
                    const hero = document.querySelector('.sx-hero, .sx-hero-dark');
                    const card = document.querySelector('.sx-why-card, .sx-svc-card');
                    const cs = el => el ? getComputedStyle(el) : null;
                    return {
                        heroBg: cs(hero)?.backgroundColor,
                        heroBgImage: cs(hero)?.backgroundImage,
                        heroPadding: cs(hero)?.padding,
                        cardBg: cs(card)?.backgroundColor,
                        cardBorder: cs(card)?.border,
                        cardPadding: cs(card)?.padding,
                        bodyFont: cs(document.body)?.fontFamily,
                    };
                }""")
                slug = url.rstrip('/').split('/')[-1]
                await page.screenshot(path=f"C:/Users/Administrator/Music/Website Suriota/_svc_{slug}.png", full_page=False)
                print(f"\n[{slug}]")
                for k,v in m.items():
                    if v: print(f"  {k}: {v[:80] if isinstance(v,str) else v}")
            except Exception as e:
                print(f"ERROR {url}: {e}")
            await page.close()
        await browser.close()

asyncio.run(main())
