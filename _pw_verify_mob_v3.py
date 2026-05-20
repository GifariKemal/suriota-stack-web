"""Verify mobile a11y fix + WhatsApp FAB visible."""
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
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0) AppleWebKit/605.1.15 Mobile/15E148'
        )
        page = await ctx.new_page()
        await page.goto('https://suriota.com/?cb=mob3', wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(2500)

        # 1) WhatsApp FAB check
        fab = await page.evaluate('''() => {
            const f = document.querySelector('.sx-wa-fab');
            if (!f) return null;
            const r = f.getBoundingClientRect();
            const cs = getComputedStyle(f);
            return {
                visible: cs.display !== 'none' && cs.visibility !== 'hidden',
                width: Math.round(r.width),
                height: Math.round(r.height),
                position: cs.position,
                right: cs.right,
                bottom: cs.bottom,
                bg: cs.backgroundColor,
                zIndex: cs.zIndex,
                href: f.href
            };
        }''')
        print('=== WhatsApp FAB ===')
        print(f'  {fab}')

        # 2) Touch target audit after fix
        # Open hamburger
        try:
            await page.locator('.sx-hf-v5-toggle').click(timeout=5000)
            await page.wait_for_timeout(800)
            # Expand "Our Services" dropdown
            try:
                await page.locator('text=Our Services').first.click(timeout=3000)
                await page.wait_for_timeout(600)
            except: pass

            menu = await page.evaluate('''() => {
                const visible = Array.from(document.querySelectorAll('header.sx-hf-v5 a, header.sx-hf-v5 button')).filter(a => {
                    const r = a.getBoundingClientRect();
                    const cs = getComputedStyle(a);
                    return r.width > 0 && r.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden';
                }).map(a => ({
                    text: (a.textContent || '').trim().slice(0, 30),
                    h: Math.round(a.getBoundingClientRect().height),
                    w: Math.round(a.getBoundingClientRect().width)
                })).filter(a => a.text.length > 1);
                const small = visible.filter(a => a.h < 44);
                return { total: visible.length, small_count: small.length, small_items: small.slice(0, 10), all_sample: visible.slice(0, 12) };
            }''')
            print(f'\n=== Menu touch targets ===')
            print(f"  Total visible links: {menu['total']}")
            print(f"  Items < 44px tall: {menu['small_count']}")
            print('  Sample (first 12):')
            for m in menu['all_sample']:
                ok = 'OK' if m['h'] >= 44 else 'SMALL'
                print(f"    [{ok}] h={m['h']:3} w={m['w']:3} | {m['text']}")
        except Exception as e:
            print(f'menu check fail: {e}')

        # 3) Screenshot FAB
        await page.goto('https://suriota.com/?cb=ss', wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(2000)
        # Close any chat widgets / cookie if blocking
        try:
            await page.locator('.sx-wa-fab').screenshot(path='_mob_fab.png')
            print('\n_mob_fab.png saved')
        except Exception as e:
            print(f'fab screenshot fail: {e}')

        await b.close()

asyncio.run(main())
