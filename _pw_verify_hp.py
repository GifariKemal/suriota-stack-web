"""Verify homepage changes: 5 service cards no Learn More, Capabilities boxed."""
import asyncio, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context(viewport={'width': 1440, 'height': 900})
        page = await ctx.new_page()
        await page.goto('https://suriota.com/?cb=verify', wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(2500)

        data = await page.evaluate('''() => {
            // 1) Service cards check
            const services = document.querySelectorAll('.about-service-card-link');
            const serviceData = Array.from(services).map(s => {
                const card = s.querySelector('article');
                const text = (card?.textContent || '').trim();
                const hasLearnMore = text.includes('Learn More') || text.includes('LEARN MORE');
                const hasContact = text.includes('Contact') && (text.includes('CONTACT') || /Contact\\s*→/.test(text));
                const desc = card?.querySelector('p')?.textContent || '';
                return {
                    href: s.href,
                    title: card?.querySelector('h3')?.textContent || '',
                    descLen: desc.length,
                    descSample: desc.slice(0, 80),
                    hasLearnMore,
                    hasContact
                };
            });

            // 2) Capabilities boxed check
            const capWidget = document.querySelector('[data-id="50680e6"]');
            const capInner = capWidget?.querySelector('div[style*="background"]');
            const capSection = document.querySelector('[data-id="49b2d08"]');
            const capData = capWidget ? {
                widget_width: Math.round(capWidget.getBoundingClientRect().width),
                widget_left: Math.round(capWidget.getBoundingClientRect().left),
                inner_bg: capInner ? getComputedStyle(capInner).backgroundColor : 'N/A',
                inner_width: capInner ? Math.round(capInner.getBoundingClientRect().width) : 0,
                inner_radius: capInner ? getComputedStyle(capInner).borderRadius : 'N/A',
                section_bg: capSection ? getComputedStyle(capSection).backgroundColor : 'N/A',
                section_width: capSection ? Math.round(capSection.getBoundingClientRect().width) : 0
            } : null;

            return { serviceData, capData };
        }''')

        print('=== 5 Service Cards ===')
        for s in data['serviceData']:
            tag = 'OK' if (not s['hasLearnMore'] and not s['hasContact']) else 'FAIL'
            print(f"  [{tag}] {s['title']:35} | desc {s['descLen']}c | learn-more={s['hasLearnMore']} contact={s['hasContact']}")
            print(f"         desc: {s['descSample']}...")

        print(f"\n=== Capabilities section ===")
        c = data['capData']
        if c:
            print(f"  widget        : {c['widget_width']}px wide, left {c['widget_left']}")
            print(f"  inner bg      : {c['inner_bg']}")
            print(f"  inner width   : {c['inner_width']}px (target ~1100)")
            print(f"  inner radius  : {c['inner_radius']}")
            print(f"  section bg    : {c['section_bg']} (target transparent)")
            print(f"  section width : {c['section_width']}px")

        # Screenshot 5 cards + capabilities area
        cards = await page.evaluate('document.querySelector(".about-service-card-link")?.getBoundingClientRect()')
        if cards:
            await page.evaluate(f"window.scrollTo(0, {cards['top'] - 50})")
            await page.wait_for_timeout(500)
            await page.screenshot(path='_hp_after_services.png', clip={'x': 0, 'y': 0, 'width': 1440, 'height': 600})
            print('\nScreenshot 5 cards -> _hp_after_services.png')

        capRect = await page.evaluate('document.querySelector("[data-id=\\"49b2d08\\"]")?.getBoundingClientRect()')
        if capRect:
            await page.evaluate(f"window.scrollTo(0, {capRect['top'] - 30})")
            await page.wait_for_timeout(500)
            await page.screenshot(path='_hp_after_cap.png', clip={'x': 0, 'y': 0, 'width': 1440, 'height': 350})
            print('Screenshot capabilities -> _hp_after_cap.png')

        await b.close()

asyncio.run(main())
