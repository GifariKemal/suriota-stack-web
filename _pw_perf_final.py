"""Final perf check + switcher mobile + responsive interaction test."""
import asyncio, sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)

        # 1) Desktop perf — fresh (no waiting for all images)
        print('=== DESKTOP — initial paint (DOMContentLoaded) ===')
        ctx = await b.new_context(viewport={'width': 1440, 'height': 900})
        page = await ctx.new_page()
        t0 = time.time()
        await page.goto('https://suriota.com/?fresh=' + str(int(time.time())), wait_until='domcontentloaded', timeout=60000)
        t_dom = round((time.time() - t0) * 1000)
        # Check loading="lazy" count
        lazy_data = await page.evaluate('''() => {
            const imgs = Array.from(document.querySelectorAll('img'));
            return {
                total: imgs.length,
                with_lazy: imgs.filter(i => i.loading === 'lazy').length,
                with_eager: imgs.filter(i => i.loading === 'eager').length,
                no_attr: imgs.filter(i => !i.loading).length,
                switcher_visible: !!document.querySelector('.sx-lang-switcher'),
                switcher_in_html: document.documentElement.outerHTML.includes('<div class="sx-lang-switcher"')
            };
        }''')
        print(f'  DOMContentLoaded wall: {t_dom}ms')
        print(f"  Images: total={lazy_data['total']} lazy={lazy_data['with_lazy']} eager={lazy_data['with_eager']} no-attr={lazy_data['no_attr']}")
        print(f"  Switcher visible at DOMContentLoaded: {lazy_data['switcher_visible']}")
        print(f"  Switcher in HTML source: {lazy_data['switcher_in_html']}")
        await page.close()

        # 2) Mobile switcher
        print('\n=== MOBILE switcher ===')
        ctx_mob = await b.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, user_agent='Mozilla/5.0 (iPhone)')
        page = await ctx_mob.new_page()
        await page.goto('https://suriota.com/?cb=mob', wait_until='domcontentloaded', timeout=30000)
        await page.wait_for_timeout(1500)
        sw = await page.evaluate('''() => {
            const s = document.querySelector('.sx-lang-switcher');
            if (!s) return null;
            const r = s.getBoundingClientRect();
            const cs = getComputedStyle(s);
            return {
                visible: cs.display !== 'none',
                pos: { top: cs.top, bottom: cs.bottom, left: cs.left, right: cs.right },
                rect: { top: Math.round(r.top), left: Math.round(r.left), w: Math.round(r.width), h: Math.round(r.height) },
                zIndex: cs.zIndex,
                links: Array.from(s.querySelectorAll('a')).map(a => ({ text: a.textContent, h: Math.round(a.getBoundingClientRect().height), active: a.classList.contains('active') }))
            };
        }''')
        print(f'  Mobile switcher: {sw}')
        # Test click on ID
        if sw:
            try:
                await page.locator('.sx-lang-switcher a:not(.active)').click(timeout=5000)
                await page.wait_for_timeout(1500)
                url_after = page.url
                print(f'  After clicking ID: {url_after}')
            except Exception as e:
                print(f'  click test failed: {e}')

        await page.locator('.sx-lang-switcher').screenshot(path='_switcher_mob_final.png')
        print('  Saved _switcher_mob_final.png')
        await page.close()

        # 3) ID page mobile
        print('\n=== Mobile ID page switcher ===')
        page = await ctx_mob.new_page()
        await page.goto('https://suriota.com/id/beranda/?cb=mob', wait_until='domcontentloaded', timeout=30000)
        await page.wait_for_timeout(1500)
        sw2 = await page.evaluate('''() => {
            const s = document.querySelector('.sx-lang-switcher');
            if (!s) return null;
            return {
                visible: getComputedStyle(s).display !== 'none',
                active_lang: Array.from(s.querySelectorAll('a.active')).map(a => a.textContent.trim()).join(',')
            };
        }''')
        print(f'  ID page switcher: {sw2}')
        await page.close()

        await b.close()

asyncio.run(main())
