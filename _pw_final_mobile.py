import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Mobile viewport
        ctx = await browser.new_context(
            viewport={"width": 390, "height": 844},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0) AppleWebKit/605.1.15 Mobile/15E148",
            device_scale_factor=3,
            is_mobile=True,
            has_touch=True
        )
        for url in [
            ("article-mobile", "https://suriota.com/setup-genset-dse-5520/"),
            ("artikel-page-mobile", "https://suriota.com/artikel/"),
            ("iot-service-mobile", "https://suriota.com/internet-of-things/"),
        ]:
            page = await ctx.new_page()
            label, u = url
            await page.goto(u, wait_until="networkidle", timeout=30000)
            await page.wait_for_timeout(2500)
            # Scroll for back-to-top
            await page.evaluate("window.scrollTo(0,1200)")
            await page.wait_for_timeout(500)
            m = await page.evaluate("""() => {
                const bt = document.querySelector('.sxa-back-top');
                const main = document.querySelector('.sxa-main, .sxa-art-grid, .sx-hero');
                const cs = el => el ? getComputedStyle(el) : null;
                const r = el => el ? el.getBoundingClientRect() : null;
                return {
                    vp: {w:window.innerWidth},
                    bt: bt ? {visible: cs(bt).opacity!='0' && cs(bt).visibility!='hidden', pos:cs(bt).position, left:cs(bt).left, bottom:cs(bt).bottom, z:cs(bt).zIndex} : 'NONE',
                    main: main ? {tag:main.tagName.toLowerCase(), width:r(main).width, padL:cs(main).paddingLeft} : 'NONE'
                };
            }""")
            print(f"\n[{label}] {u}")
            for k,v in m.items(): print(f"  {k}: {v}")
            await page.close()
        await browser.close()

asyncio.run(main())
