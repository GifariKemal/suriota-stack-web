"""Mobile responsive audit + link verification on homepage + key pages."""
import asyncio, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

PAGES = [
    ('https://suriota.com/',                'Homepage'),
    ('https://suriota.com/internet-of-things/', 'IoT'),
    ('https://suriota.com/artikel/',        'Artikel'),
    ('https://suriota.com/water-treatment/', 'WT'),
]

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        # iPhone 13 viewport
        ctx = await b.new_context(
            viewport={'width': 390, 'height': 844},
            device_scale_factor=3,
            is_mobile=True,
            has_touch=True,
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
        )
        for url, lbl in PAGES:
            page = await ctx.new_page()
            print(f'\n========== {lbl} - MOBILE ==========')
            await page.goto(url + '?cb=mob', wait_until='networkidle', timeout=30000)
            await page.wait_for_timeout(2000)

            # General mobile health
            data = await page.evaluate('''() => {
                const vp = window.innerWidth;
                const scrollW = document.documentElement.scrollWidth;
                const hasHScroll = scrollW > vp;

                // Find any element wider than viewport (horizontal overflow culprits)
                const overflowers = [];
                document.querySelectorAll('*').forEach(el => {
                    const r = el.getBoundingClientRect();
                    if (r.right > vp + 5 || r.left < -5) {
                        const cls = (el.className || '').toString().slice(0, 40);
                        const id = el.dataset?.id || el.id || '';
                        if (cls || id) {
                            overflowers.push({ tag: el.tagName, cls, id, right: Math.round(r.right), left: Math.round(r.left), w: Math.round(r.width) });
                        }
                    }
                });

                // Touch target audit (links/buttons < 44x44 are bad)
                const smallTouch = [];
                document.querySelectorAll('a, button').forEach(el => {
                    const r = el.getBoundingClientRect();
                    if (r.width > 0 && r.height > 0 && (r.width < 32 || r.height < 32)) {
                        smallTouch.push({
                            text: (el.textContent || el.ariaLabel || '').trim().slice(0, 30),
                            w: Math.round(r.width),
                            h: Math.round(r.height)
                        });
                    }
                });

                // Font size audit (< 12px hard to read on mobile)
                const tinyFonts = new Set();
                document.querySelectorAll('p, span, div, li').forEach(el => {
                    if (!el.textContent.trim()) return;
                    const fs = parseFloat(getComputedStyle(el).fontSize);
                    if (fs > 0 && fs < 12) {
                        tinyFonts.add(`${el.tagName}.${(el.className||'').toString().slice(0,30)} ${fs}px`);
                    }
                });

                return {
                    viewport: vp,
                    scrollWidth: scrollW,
                    hasHScroll,
                    overflowCount: overflowers.length,
                    overflowSample: overflowers.slice(0, 5),
                    smallTouchCount: smallTouch.length,
                    smallTouchSample: smallTouch.slice(0, 10),
                    tinyFontCount: tinyFonts.size,
                    tinyFontSample: Array.from(tinyFonts).slice(0, 5)
                };
            }''')

            print(f"  viewport={data['viewport']} scrollW={data['scrollWidth']} h-scroll={data['hasHScroll']}")
            print(f"  Overflowing elements: {data['overflowCount']}")
            for o in data['overflowSample']:
                print(f"    - {o['tag']}.{o['cls']:30} id={o['id']:10} | w={o['w']} l={o['left']} r={o['right']}")
            print(f"  Touch targets <32x32px: {data['smallTouchCount']}")
            for t in data['smallTouchSample'][:5]:
                print(f"    - {t['text']:30} {t['w']}x{t['h']}")
            print(f"  Tiny fonts (<12px): {data['tinyFontCount']}")
            for f in data['tinyFontSample']:
                print(f"    - {f}")

            # Homepage-specific: verify 5 service card links + capability boxed
            if 'Homepage' in lbl:
                hp = await page.evaluate('''() => {
                    const cards = Array.from(document.querySelectorAll('.about-service-card-link')).map(c => {
                        const r = c.getBoundingClientRect();
                        return {
                            href: c.href,
                            title: c.querySelector('h3')?.textContent?.trim(),
                            w: Math.round(r.width),
                            stacked: r.left < 50  // close to left edge means stacked single col
                        };
                    });
                    const cap = document.querySelector('[data-id="50680e6"] > div');
                    const capR = cap?.getBoundingClientRect();
                    return {
                        cards,
                        capWidth: capR ? Math.round(capR.width) : 0,
                        capRadius: cap ? getComputedStyle(cap).borderRadius : 'N/A'
                    };
                }''')
                print(f"\n  --- HOMEPAGE SPECIFIC ---")
                print(f"  5 cards:")
                for c in hp['cards']:
                    print(f"    {c['title']:35} | w={c['w']} stacked={c['stacked']} | -> {c['href'][-40:]}")
                print(f"  Capabilities box: w={hp['capWidth']}px radius={hp['capRadius']}")

                # Screenshot
                await page.locator('[data-id="50680e6"]').screenshot(path='_hp_mob_cap.png')
                # Scroll to top + screenshot service cards
                await page.evaluate('window.scrollTo(0,0)')
                await page.wait_for_timeout(500)
                await page.locator('.about-service-card-link').first.scroll_into_view_if_needed()
                await page.wait_for_timeout(500)
                await page.screenshot(path='_hp_mob_services.png', clip={'x': 0, 'y': 0, 'width': 390, 'height': 844})
                print('  Screenshots -> _hp_mob_cap.png, _hp_mob_services.png')

            await page.close()
        await b.close()

asyncio.run(main())
