"""Detailed size audit - print all issues with categorization."""
import asyncio, sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

PAGES = [
    ('https://suriota.com/', 'Home'),
    ('https://suriota.com/about/', 'About'),
    ('https://suriota.com/portfolio/', 'Portfolio'),
    ('https://suriota.com/contact/', 'Contact'),
    ('https://suriota.com/automation/', 'Automation'),
    ('https://suriota.com/electrical/', 'Electrical'),
    ('https://suriota.com/renewable-energy/', 'RE'),
    ('https://suriota.com/internet-of-things/', 'IoT'),
    ('https://suriota.com/water-treatment/', 'WT'),
    ('https://suriota.com/data-analytics/', 'DA'),
    ('https://suriota.com/digital-consulting/', 'DC'),
    ('https://suriota.com/artificial-intelligence/', 'AI'),
    ('https://suriota.com/system-integration/', 'SysInt'),
    ('https://suriota.com/saas/', 'SaaS'),
    ('https://suriota.com/surge-energy-mapping/', 'SURGE-E'),
    ('https://suriota.com/surge-vessel-tracking/', 'SURGE-V'),
    ('https://suriota.com/surge-water-analytic/', 'SURGE-W'),
    ('https://suriota.com/suriota-modbus-gateway/', 'MGATE'),
    ('https://suriota.com/iso-m485-series/', 'ISO-M485'),
    ('https://suriota.com/pm1611-wd/', 'PM1611'),
    ('https://suriota.com/thm-30md/', 'THM-30MD'),
    ('https://suriota.com/rs-485-surge-protector/', 'SPD-T485'),
    ('https://suriota.com/waste-water-logger/', 'WW'),
    ('https://suriota.com/privacy-policy/', 'Privacy'),
    ('https://suriota.com/terms-of-service/', 'Terms'),
    ('https://suriota.com/id/beranda/', 'ID-Home'),
    ('https://suriota.com/id/tentang-kami/', 'ID-About'),
    ('https://suriota.com/id/portfolio-id/', 'ID-Portfolio'),
    ('https://suriota.com/id/kontak/', 'ID-Contact'),
    ('https://suriota.com/id/kebijakan-privasi/', 'ID-Privacy'),
    ('https://suriota.com/id/syarat-layanan/', 'ID-Terms'),
    ('https://suriota.com/id/artikel-id/', 'ID-Artikel'),
]

SAMPLES = ['body', 'h1', 'h2', 'h3', 'h4', 'p', 'a', 'li', 'small', 'span',
           '.elementor-button', '.elementor-heading-title', '.elementor-widget-text-editor',
           'nav', 'header', 'footer', '.elementor-nav-menu a', 'input', 'button',
           'td', 'th', 'blockquote']

SIZE_RANGES = {
    'body': (14, 18), 'p': (14, 18), 'a': (12, 18),
    'h1': (28, 80), 'h2': (22, 56), 'h3': (18, 40), 'h4': (16, 28),
    'li': (12, 18), 'small': (10, 14),
    'td': (12, 18), 'th': (12, 18),
    '.elementor-button': (12, 20),
    '.elementor-heading-title': (16, 80),
    '.elementor-widget-text-editor': (12, 20),
    '.elementor-nav-menu a': (12, 20),
    'blockquote': (14, 24),
    'nav': (12, 20), 'header': (12, 24), 'footer': (10, 18),
    'input': (12, 18), 'button': (12, 18),
}

async def main():
    issues = []
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context(viewport={'width':1440,'height':900})
        for url, lbl in PAGES:
            page = await ctx.new_page()
            try:
                resp = await page.goto(url + '?nc=' + str(time.time()), wait_until='domcontentloaded', timeout=30000)
                if resp and resp.status >= 400:
                    await page.close(); continue
                await page.wait_for_timeout(1500)
                for sel in SAMPLES:
                    try:
                        data = await page.evaluate(f"""
                            (() => {{
                                const el = document.querySelector("{sel.replace('"','\\"')}");
                                if (!el) return null;
                                const cs = getComputedStyle(el);
                                return {{
                                    size: parseFloat(cs.fontSize),
                                    weight: cs.fontWeight,
                                    text: (el.innerText || el.textContent || '').trim().slice(0, 40)
                                }};
                            }})()
                        """)
                        if not data: continue
                        size = data['size']
                        if sel in SIZE_RANGES:
                            lo, hi = SIZE_RANGES[sel]
                            if size < lo:
                                issues.append((lbl, sel, size, 'TOO SMALL', lo, hi, data['text']))
                            elif size > hi:
                                issues.append((lbl, sel, size, 'TOO BIG', lo, hi, data['text']))
                    except Exception:
                        pass
            except Exception as e:
                pass
            await page.close()
        await b.close()

    # Group by selector and issue type
    by_sel = {}
    for lbl, sel, size, kind, lo, hi, text in issues:
        key = (sel, kind)
        if key not in by_sel: by_sel[key] = []
        by_sel[key].append((lbl, size, text))

    print(f'Total flagged: {len(issues)}\n')
    for (sel, kind), lst in sorted(by_sel.items()):
        ex = lst[0]
        print(f'=== {sel} {kind} ({len(lst)} pages) — recommend in range —')
        for lbl, size, text in lst[:20]:
            print(f'  {lbl:14s} {size:5.1f}px "{text}"')

asyncio.run(main())
