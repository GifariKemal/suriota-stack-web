"""Check computed font-family on key elements across pages."""
import asyncio, sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

PAGES = [
    ('https://suriota.com/', 'Home'),
    ('https://suriota.com/id/beranda/', 'ID-Home'),
    ('https://suriota.com/automation/', 'Automation'),
    ('https://suriota.com/portfolio/', 'Portfolio'),
    ('https://suriota.com/surge-energy-mapping/', 'SURGE-E'),
    ('https://suriota.com/id/kebijakan-privasi/', 'ID-Privacy'),
]

SELECTORS = [
    'body',
    'h1', 'h2', 'h3',
    'p',
    'a',
    '.elementor-button',
    '.elementor-heading-title',
    '.elementor-widget-text-editor',
    'nav, .elementor-nav-menu, header',
    'footer',
    'li',
    'table, td, th',
    '.sx-stat-num, .sx-hero-title, .sx-card-title',
]

async def main():
    issues = []
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context(viewport={'width':1440,'height':900})
        for url, lbl in PAGES:
            page = await ctx.new_page()
            try:
                await page.goto(url + '?nc=' + str(time.time()), wait_until='domcontentloaded', timeout=25000)
                await page.wait_for_timeout(1200)
                results = {}
                for sel in SELECTORS:
                    try:
                        family = await page.evaluate(f"""
                            (() => {{
                                const el = document.querySelector("{sel.replace('"','\\"')}");
                                if (!el) return null;
                                const cs = getComputedStyle(el);
                                return cs.fontFamily;
                            }})()
                        """)
                        if family:
                            primary = family.split(',')[0].strip().strip("\"'")
                            results[sel] = primary
                            if 'Plus Jakarta' in family or 'Lato' in family or 'Poppins' in family or 'IBM Plex' in family:
                                if 'Geist' not in family.split(',')[0]:
                                    issues.append(f'{lbl}|{sel}|{family[:80]}')
                    except Exception as e:
                        pass
                print(f'\\n=== {lbl} ({url}) ===')
                for sel, fam in results.items():
                    flag = '✓' if 'Geist' in fam else '✗'
                    print(f'  {flag} {sel:50s} → {fam}')
            except Exception as e:
                print(f'\\n[{lbl}] ERR {str(e)[:80]}')
            await page.close()
        await b.close()

    print('\\n\\n===== ISSUES (non-Geist as primary font) =====')
    if issues:
        for i in issues:
            print('  ', i)
    else:
        print('  None — Geist is primary on all checked elements ✓')

asyncio.run(main())
