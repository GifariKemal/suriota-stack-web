import asyncio, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context(viewport={'width': 1440, 'height': 900})

        pages = [
            ('https://suriota.com/', 'EN Home'),
            ('https://suriota.com/id/beranda/', 'ID Beranda'),
            ('https://suriota.com/about-us/', 'EN About'),
            ('https://suriota.com/id/tentang-kami/', 'ID Tentang'),
        ]

        for url, lbl in pages:
            page = await ctx.new_page()
            await page.goto(url + '?cb=p', wait_until='networkidle', timeout=30000)
            await page.wait_for_timeout(2000)

            data = await page.evaluate('''() => {
                const hl = Array.from(document.querySelectorAll('link[rel="alternate"][hreflang]')).map(l => ({ h: l.hreflang, href: l.href }));
                const sw = document.querySelector('.sx-lang-switcher');
                const swData = sw ? {
                    visible: getComputedStyle(sw).display !== 'none',
                    links: Array.from(sw.querySelectorAll('a')).map(a => ({ text: a.textContent.trim(), href: a.href, active: a.classList.contains('active') })),
                    pos: { top: getComputedStyle(sw).top, right: getComputedStyle(sw).right, bottom: getComputedStyle(sw).bottom, left: getComputedStyle(sw).left }
                } : null;
                return {
                    lang: document.documentElement.lang,
                    title: document.title,
                    hreflang: hl,
                    switcher: swData
                };
            }''')
            print(f'\n[{lbl}] {url}')
            print(f"  lang attr     : {data['lang']}")
            print(f"  title         : {data['title']}")
            print(f"  hreflang ({len(data['hreflang'])}):")
            for h in data['hreflang']:
                print(f"    {h['h']:10} -> {h['href']}")
            print(f"  switcher      : {data['switcher']}")
            await page.close()

        # Mobile test
        ctx2 = await b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, user_agent='Mozilla/5.0 (iPhone)')
        page = await ctx2.new_page()
        await page.goto('https://suriota.com/?cb=mob', wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(2000)
        await page.locator('.sx-lang-switcher').screenshot(path='_lang_switcher_mob.png')
        print('\n_lang_switcher_mob.png saved')

        await b.close()

asyncio.run(main())
