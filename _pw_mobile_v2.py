"""Focused mobile audit — homepage screenshots + capability radius check."""
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
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148'
        )
        page = await ctx.new_page()
        await page.goto('https://suriota.com/?cb=v2', wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(2500)

        # Find the actual styled inner div using better selector
        data = await page.evaluate('''() => {
            const widget = document.querySelector('[data-id="50680e6"]');
            // Find the DEEPEST div with background-color set (our custom inner)
            let found = null;
            widget?.querySelectorAll('div').forEach(d => {
                const bg = getComputedStyle(d).backgroundColor;
                if (bg === 'rgb(32, 91, 105)') found = d;
            });
            const r = found?.getBoundingClientRect();
            return found ? {
                width: Math.round(r.width),
                radius: getComputedStyle(found).borderRadius,
                padL: getComputedStyle(found).paddingLeft,
                padR: getComputedStyle(found).paddingRight,
                padT: getComputedStyle(found).paddingTop,
                shadow: getComputedStyle(found).boxShadow
            } : null;
        }''')
        print(f'Capabilities inner box (mobile): {data}')

        # Screenshot 4 zones
        # 1) Service cards
        await page.evaluate('window.scrollTo(0,0)')
        await page.wait_for_timeout(500)
        try:
            await page.locator('.about-service-card-link').first.scroll_into_view_if_needed(timeout=5000)
            await page.wait_for_timeout(500)
            await page.screenshot(path='_mob_services.png')
            print('Saved -> _mob_services.png')
        except Exception as e:
            print(f'service screenshot fail: {e}')

        # 2) Capabilities
        try:
            await page.locator('[data-id="50680e6"]').scroll_into_view_if_needed(timeout=5000)
            await page.wait_for_timeout(500)
            await page.screenshot(path='_mob_cap.png')
            print('Saved -> _mob_cap.png')
        except Exception as e:
            print(f'cap screenshot fail: {e}')

        # 3) Open hamburger and inspect mobile menu touch targets
        await page.evaluate('window.scrollTo(0,0)')
        await page.wait_for_timeout(500)
        # Find hamburger
        ham = await page.evaluate('''() => {
            const all = Array.from(document.querySelectorAll('button, a, span'));
            const h = all.find(el => el.textContent.trim() === '☰' || el.getAttribute('aria-label')?.includes('menu') || el.className.includes('hamburger') || el.className.includes('toggle'));
            return h ? { tag: h.tagName, cls: h.className, text: h.textContent.trim().slice(0,20) } : null;
        }''')
        print(f'Hamburger: {ham}')

        # Click hamburger and inspect menu
        try:
            hamBtn = page.locator('text=☰').first
            await hamBtn.click(timeout=5000)
            await page.wait_for_timeout(1000)
            await page.screenshot(path='_mob_menu_open.png')
            print('Saved -> _mob_menu_open.png')

            # Audit visible menu items
            menu_data = await page.evaluate('''() => {
                const visible = Array.from(document.querySelectorAll('a')).filter(a => {
                    const r = a.getBoundingClientRect();
                    const cs = getComputedStyle(a);
                    return r.width > 0 && r.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden';
                }).map(a => ({
                    text: a.textContent.trim().slice(0, 30),
                    h: Math.round(a.getBoundingClientRect().height),
                    href: (a.href || '').slice(-40)
                }));
                return visible.filter(a => a.h < 40 && a.text.length > 3).slice(0, 15);
            }''')
            print('\nMobile menu items with height <40px:')
            for m in menu_data:
                print(f"  h={m['h']:3} | {m['text']:30} | {m['href']}")
        except Exception as e:
            print(f'menu open fail: {e}')

        await b.close()

asyncio.run(main())
