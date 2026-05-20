"""Inspect homepage: find Core Services CTA buttons + Capabilities width issue."""
import asyncio, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context(viewport={'width': 1440, 'height': 900})
        page = await ctx.new_page()
        await page.goto('https://suriota.com/?cb=insp', wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(2000)

        # Look for Our 5 Core Services + Capabilities sections + buttons
        data = await page.evaluate('''() => {
            const text = document.body.innerText;
            const hasCore = text.includes('Core Services') || text.includes('5 Core');
            const hasCap = text.toLowerCase().includes('capabilit');

            // Find Learn More + Contact buttons
            const buttons = Array.from(document.querySelectorAll('a, button')).filter(b => {
                const t = b.textContent.trim().toLowerCase();
                return t === 'learn more' || t === 'contact' || t.includes('learn more') || t === 'contact us';
            }).map(b => ({
                text: b.textContent.trim(),
                href: b.href || '(button)',
                parent_id: b.closest('[data-id]')?.dataset?.id || '',
                parent_class: b.parentElement?.className?.slice(0, 60) || ''
            }));

            // Find Capabilities section bounding
            const capSection = Array.from(document.querySelectorAll('section, .elementor-section, .elementor-top-section')).find(s =>
                s.textContent.toLowerCase().includes('capabilit')
            );
            const capInfo = capSection ? {
                width: capSection.getBoundingClientRect().width,
                left: capSection.getBoundingClientRect().left,
                bg: getComputedStyle(capSection).backgroundColor,
                padL: getComputedStyle(capSection).paddingLeft,
                padR: getComputedStyle(capSection).paddingRight,
                id: capSection.dataset?.id || capSection.id || '(none)'
            } : null;

            // Compare to neighbor sections widths
            const allSections = Array.from(document.querySelectorAll('section.elementor-top-section')).map(s => ({
                id: s.dataset?.id || s.id || '',
                width: Math.round(s.getBoundingClientRect().width),
                left: Math.round(s.getBoundingClientRect().left),
                right: Math.round(window.innerWidth - s.getBoundingClientRect().right),
                bgColor: getComputedStyle(s).backgroundColor,
                bgImg: getComputedStyle(s).backgroundImage.slice(0, 60),
                hasText: (s.textContent || '').trim().slice(0, 50)
            }));

            return { hasCore, hasCap, buttons, capInfo, allSections, viewport: window.innerWidth };
        }''')

        print(f'Viewport: {data["viewport"]}px')
        print(f'\nHas "Core Services": {data["hasCore"]}')
        print(f'Has "Capabilit": {data["hasCap"]}')

        print(f'\n=== Learn More / Contact buttons ===')
        for btn in data['buttons']:
            print(f'  "{btn["text"]}" -> {btn["href"][:60]}  parent_id={btn["parent_id"]}')

        print(f'\n=== Capabilities section info ===')
        if data['capInfo']:
            print(f'  {data["capInfo"]}')

        print(f'\n=== ALL Top sections (looking for width inconsistency) ===')
        for s in data['allSections']:
            txt = s['hasText'].replace('\n', ' ')
            print(f"  id={s['id']:10} width={s['width']:5} left={s['left']:4} right={s['right']:4} bg={s['bgColor'][:25]:25} txt='{txt}'")

        await page.screenshot(path='_hp_full.png', full_page=True)
        print('\nFull screenshot -> _hp_full.png')
        await b.close()

asyncio.run(main())
