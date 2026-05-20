"""Comprehensive font + size audit across all pages."""
import asyncio, sys, io, time, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

# All key pages EN + ID
PAGES = [
    # EN
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
    # ID
    ('https://suriota.com/id/beranda/', 'ID-Home'),
    ('https://suriota.com/id/tentang-kami/', 'ID-About'),
    ('https://suriota.com/id/portfolio-id/', 'ID-Portfolio'),
    ('https://suriota.com/id/kontak/', 'ID-Contact'),
    ('https://suriota.com/id/kebijakan-privasi/', 'ID-Privacy'),
    ('https://suriota.com/id/syarat-layanan/', 'ID-Terms'),
    ('https://suriota.com/id/artikel-id/', 'ID-Artikel'),
    # Article sample
    ('https://suriota.com/peran-iot-industri-keberlanjutan-bisnis/', 'EN-Article'),
]

# Selectors to check — covers all main typography classes
SAMPLES = [
    'body', 'h1', 'h2', 'h3', 'h4', 'p', 'a',
    'li', 'td', 'th', 'span',
    '.elementor-button',
    '.elementor-heading-title',
    '.elementor-widget-text-editor',
    'nav', 'header', 'footer',
    '.elementor-nav-menu a',
    'small',
    'blockquote',
    'code', 'pre',
    'input', 'button', 'textarea',
]

# Reasonable size ranges (px) for B2B web — flag if outside
SIZE_RANGES = {
    'body': (14, 18),
    'p': (14, 18),
    'a': (12, 18),
    'h1': (28, 80),
    'h2': (22, 56),
    'h3': (18, 40),
    'h4': (16, 28),
    'li': (12, 18),
    'small': (10, 14),
    'span': (10, 22),
    'td': (12, 18),
    'th': (12, 18),
    'input': (12, 18),
    'button': (12, 18),
    'textarea': (12, 18),
    '.elementor-button': (12, 20),
    '.elementor-heading-title': (16, 80),
    '.elementor-widget-text-editor': (12, 20),
    'nav': (12, 20),
    'header': (12, 24),
    'footer': (10, 18),
    '.elementor-nav-menu a': (12, 20),
    'blockquote': (14, 24),
    'code': (10, 16),
    'pre': (10, 16),
}

async def main():
    issues_font = []   # non-Geist font found
    issues_size = []   # font size out of range
    summary = {}       # per page stats
    fonts_seen = set()

    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context(viewport={'width':1440,'height':900})
        for url, lbl in PAGES:
            page = await ctx.new_page()
            try:
                resp = await page.goto(url + '?nc=' + str(time.time()), wait_until='domcontentloaded', timeout=30000)
                if resp and resp.status >= 400:
                    print(f'\n[{lbl}] HTTP {resp.status} - skipping')
                    summary[lbl] = {'error': f'HTTP {resp.status}'}
                    await page.close()
                    continue
                await page.wait_for_timeout(1500)
                page_issues_font = 0
                page_issues_size = 0
                results = []
                for sel in SAMPLES:
                    try:
                        data = await page.evaluate(f"""
                            (() => {{
                                const el = document.querySelector("{sel.replace('"','\\"')}");
                                if (!el) return null;
                                const cs = getComputedStyle(el);
                                return {{
                                    family: cs.fontFamily,
                                    size: parseFloat(cs.fontSize),
                                    weight: cs.fontWeight,
                                    text: (el.innerText || el.textContent || '').trim().slice(0, 30)
                                }};
                            }})()
                        """)
                        if not data:
                            continue
                        primary = data['family'].split(',')[0].strip().strip("\"'")
                        fonts_seen.add(primary)
                        size = data['size']
                        results.append((sel, primary, size, data['weight']))
                        # Flag non-Geist
                        if 'Geist' not in primary and primary not in ('Font Awesome 6 Free','Font Awesome 6 Brands','eicons','dashicons','Material Icons','inherit','initial','unset'):
                            issues_font.append(f'{lbl} | {sel} | {primary} | size={size}px')
                            page_issues_font += 1
                        # Flag size out of range
                        if sel in SIZE_RANGES:
                            lo, hi = SIZE_RANGES[sel]
                            if size < lo or size > hi:
                                issues_size.append(f'{lbl} | {sel} | size={size}px (range {lo}-{hi}px) | "{data["text"]}"')
                                page_issues_size += 1
                    except Exception:
                        pass
                summary[lbl] = {'font_issues': page_issues_font, 'size_issues': page_issues_size, 'samples': len(results)}
            except Exception as e:
                print(f'\n[{lbl}] ERR {str(e)[:80]}')
                summary[lbl] = {'error': str(e)[:80]}
            await page.close()
        await b.close()

    # Output
    print('\n========== SUMMARY ==========')
    print(f'{"Page":15s} {"Samples":>8s} {"FontIssue":>10s} {"SizeIssue":>10s}')
    for lbl, s in summary.items():
        if 'error' in s:
            print(f'{lbl:15s} ERROR: {s["error"]}')
        else:
            print(f'{lbl:15s} {s["samples"]:>8d} {s["font_issues"]:>10d} {s["size_issues"]:>10d}')

    print('\n========== UNIQUE FONTS SEEN ==========')
    for f in sorted(fonts_seen):
        flag = '✓' if 'Geist' in f or f in ('Font Awesome 6 Free','Font Awesome 6 Brands','eicons','dashicons','Material Icons') else '✗'
        print(f'  {flag} {f}')

    print('\n========== FONT ISSUES (non-Geist) ==========')
    if issues_font:
        # Dedup by combination
        seen = set()
        for i in issues_font:
            parts = i.split('|')
            key = (parts[1].strip(), parts[2].strip())  # sel+font
            if key in seen: continue
            seen.add(key)
            print(' ', i)
        print(f'\n  Total raw issues: {len(issues_font)}, unique sel+font combos: {len(seen)}')
    else:
        print('  None ✓')

    print('\n========== SIZE ISSUES ==========')
    if issues_size:
        seen = set()
        for i in issues_size[:60]:
            parts = i.split('|')
            key = (parts[1].strip(), parts[2].strip())
            if key in seen: continue
            seen.add(key)
            print(' ', i)
        if len(issues_size) > 60:
            print(f'  ... and {len(issues_size)-60} more')
    else:
        print('  None ✓')

asyncio.run(main())
