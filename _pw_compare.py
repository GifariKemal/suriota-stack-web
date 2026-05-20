import asyncio
from playwright.async_api import async_playwright

URLS = [
    ("electrical", "https://suriota.com/electrical/"),
    ("automation", "https://suriota.com/automation/"),
    ("water-treatment", "https://suriota.com/water-treatment/"),
    ("internet-of-things", "https://suriota.com/internet-of-things/"),
    ("renewable-energy", "https://suriota.com/renewable-energy/"),
]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(viewport={"width": 1280, "height": 900})
        for name, url in URLS:
            page = await ctx.new_page()
            try:
                await page.goto(url, wait_until="networkidle", timeout=30000)
                await page.wait_for_timeout(1500)
                # Get key visual metrics
                m = await page.evaluate("""() => {
                    const body = document.body;
                    const main = document.querySelector('main, .elementor-section-wrap, [data-elementor-type]');
                    const headerH1 = document.querySelector('h1');
                    const sections = document.querySelectorAll('[data-elementor-type=\"wp-page\"] section, .elementor-section');
                    const widgets = document.querySelectorAll('.elementor-widget');
                    const r = el => el ? el.getBoundingClientRect() : null;
                    const cs = el => el ? getComputedStyle(el) : null;
                    return {
                        bodyClass: body.className,
                        documentScrollHeight: document.documentElement.scrollHeight,
                        h1: headerH1 ? headerH1.textContent.trim().slice(0,80) : null,
                        sectionCount: sections.length,
                        widgetCount: widgets.length,
                        bodyBg: cs(body)?.backgroundColor,
                        firstSectionWidth: sections[0] ? r(sections[0]).width : null,
                        siteMainWidth: r(document.querySelector('.site-main'))?.width,
                    };
                }""")
                await page.screenshot(path=f"C:/Users/Administrator/Music/Website Suriota/_cmp_{name}.png", full_page=False)
                print(f"\n[{name}] {url}")
                for k, v in m.items(): print(f"  {k}: {v}")
            except Exception as e:
                print(f"[{name}] ERROR: {e}")
            await page.close()
        await browser.close()

asyncio.run(main())
