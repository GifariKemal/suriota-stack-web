"""Verify navbar language dropdown — desktop + mobile."""
import asyncio, sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)

        # Desktop EN page
        print('=== Desktop EN page ===')
        ctx = await b.new_context(viewport={'width':1440,'height':900})
        page = await ctx.new_page()
        await page.goto('https://suriota.com/?cb=' + str(time.time()), wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(2000)
        data = await page.evaluate('''() => {
            const lang = document.querySelector('.sx-hf-v5-lang');
            if (!lang) return { found: false };
            const btn = lang.querySelector('.sx-hf-v5-dropbtn');
            const items = Array.from(lang.querySelectorAll('.sx-hf-v5-lang-content a, .sx-hf-v5-lang-content .sx-lang-disabled'));
            const floating = document.querySelector('.sx-lang-switcher');
            return {
                found: true,
                btn_text: btn ? btn.textContent.trim() : null,
                items: items.map(i => ({ text: i.textContent.trim(), href: i.href, disabled: i.classList.contains('sx-lang-disabled') })),
                pos: btn ? { top: Math.round(btn.getBoundingClientRect().top), right: Math.round(window.innerWidth - btn.getBoundingClientRect().right) } : null,
                floating_present: !!floating
            };
        }''')
        print(f"  Lang in navbar: {data['found']}")
        print(f"  Button text: {data['btn_text']}")
        print(f"  Items in dropdown:")
        for i in data['items']:
            print(f"    - {i['text']} (disabled={i['disabled']}) -> {i['href'][-40:] if i['href'] else 'no link'}")
        print(f"  Old floating switcher present: {data['floating_present']}")
        print(f"  Button position: {data['pos']}")

        # Click dropdown to verify expansion
        try:
            await page.locator('.sx-hf-v5-lang .sx-hf-v5-dropbtn').click(timeout=3000)
            await page.wait_for_timeout(500)
            expanded = await page.evaluate('document.querySelector(".sx-hf-v5-lang").classList.contains("open")')
            print(f"  Click expansion: {expanded}")
        except Exception as e:
            print(f"  click err: {e}")

        # Screenshot navbar
        try:
            await page.locator('header.sx-hf-v5').screenshot(path='_lang_navbar_desktop.png')
            print('  Saved _lang_navbar_desktop.png')
        except Exception as e:
            print(f'  screenshot err: {e}')

        await page.close()

        # Desktop ID page
        print('\n=== Desktop ID page ===')
        page = await ctx.new_page()
        await page.goto('https://suriota.com/id/beranda/?cb=' + str(time.time()), wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(2000)
        data2 = await page.evaluate('''() => {
            const lang = document.querySelector('.sx-hf-v5-lang');
            const btn = lang ? lang.querySelector('.sx-hf-v5-dropbtn') : null;
            const items = lang ? Array.from(lang.querySelectorAll('.sx-hf-v5-lang-content a, .sx-hf-v5-lang-content .sx-lang-disabled')) : [];
            return {
                btn_text: btn ? btn.textContent.trim() : null,
                items: items.map(i => ({ text: i.textContent.trim(), href: i.href, disabled: i.classList.contains('sx-lang-disabled') })),
            };
        }''')
        print(f"  Button text: {data2['btn_text']}")
        for i in data2['items']:
            print(f"    - {i['text']} (disabled={i['disabled']}) -> {i['href'][-40:] if i['href'] else 'no link'}")
        await page.close()

        # Mobile EN
        print('\n=== Mobile EN ===')
        ctx_m = await b.new_context(viewport={'width':390,'height':844}, is_mobile=True, has_touch=True, user_agent='Mozilla/5.0 (iPhone)')
        page = await ctx_m.new_page()
        await page.goto('https://suriota.com/?cb=' + str(time.time()), wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(2000)
        try:
            await page.locator('.sx-hf-v5-toggle').click(timeout=3000)
            await page.wait_for_timeout(800)
            await page.screenshot(path='_lang_navbar_mobile.png', clip={'x':0,'y':0,'width':390,'height':700})
            print('  Saved _lang_navbar_mobile.png')
        except Exception as e:
            print(f'  mobile err: {e}')

        await b.close()

asyncio.run(main())
