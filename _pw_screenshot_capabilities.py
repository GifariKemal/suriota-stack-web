"""Screenshot capabilities + neighbouring sections to visualize background width issue."""
import asyncio, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context(viewport={'width': 1440, 'height': 900})
        page = await ctx.new_page()
        await page.goto('https://suriota.com/?cb=cap', wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(2000)

        # Find capabilities widget bounding + its parent container
        info = await page.evaluate('''() => {
            const w = document.querySelector('[data-id="50680e6"]');
            if (!w) return { found: false };
            const r = w.getBoundingClientRect();
            // Walk up parents to inspect each
            let n = w, chain = [];
            while (n && n !== document.body) {
                const cs = getComputedStyle(n);
                const br = n.getBoundingClientRect();
                chain.push({
                    tag: n.tagName,
                    cls: (n.className || '').slice(0, 80),
                    id: n.id || n.dataset?.id || '',
                    width: Math.round(br.width),
                    left: Math.round(br.left),
                    right: Math.round(window.innerWidth - br.right),
                    bg: cs.backgroundColor,
                    bgImg: cs.backgroundImage.slice(0, 50),
                    padL: cs.paddingLeft,
                    padR: cs.paddingRight,
                    mL: cs.marginLeft,
                    mR: cs.marginRight
                });
                n = n.parentElement;
                if (chain.length > 8) break;
            }
            return { found: true, top: r.top, height: r.height, chain };
        }''')

        if not info['found']:
            print('Capabilities widget not found')
            return

        print(f"Capabilities widget top: {info['top']}, height: {info['height']}")
        print('\nDOM chain (widget to body):')
        for i, c in enumerate(info['chain']):
            print(f"  [{i}] {c['tag']}.{c['cls'][:40]:40} | id={c['id']:10} | w={c['width']:5} l={c['left']:4} r={c['right']:4} | bg={c['bg'][:25]:25} | pad={c['padL']}/{c['padR']}")

        # Screenshot around capabilities section
        await page.evaluate(f"window.scrollTo(0, {info['top'] - 50})")
        await page.wait_for_timeout(500)
        await page.screenshot(path='_cap_section.png', clip={'x': 0, 'y': 0, 'width': 1440, 'height': min(900, info['height'] + 100)})
        print('\nScreenshot -> _cap_section.png')
        await b.close()

asyncio.run(main())
