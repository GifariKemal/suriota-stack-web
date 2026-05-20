"""Audit color and spacing inconsistencies across pages."""
import asyncio, sys, io, time, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright
from collections import Counter, defaultdict

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
    ('https://suriota.com/iso-m485-series/', 'ISO-M485'),
    ('https://suriota.com/id/beranda/', 'ID-Home'),
    ('https://suriota.com/id/kebijakan-privasi/', 'ID-Privacy'),
]

# Element selectors to inspect
SELECTORS_COLOR = [
    ('body', ['color', 'background-color']),
    ('h1, .sx-hero-h1', ['color']),
    ('h2', ['color']),
    ('h3', ['color']),
    ('p', ['color']),
    ('a:not(.elementor-button):not(.sx-cta-btn)', ['color']),
    ('.elementor-button, .sx-cta-btn', ['background-color', 'color']),
    ('.sx-eyebrow', ['color']),
    ('header, .sx-header', ['background-color', 'color']),
    ('footer, .sx-footer', ['background-color', 'color']),
    ('section', ['background-color']),
    ('.sx-whyus-card, .sx-trust-card, .sx-card, .sx-service-card, .sx-industries-card', ['background-color', 'border-color']),
    ('.sx-callout, .sx-cta-final', ['background-color']),
    ('.sx-hero, section.sx-hero', ['background-color']),
    ('strong', ['color']),
]

SELECTORS_SPACING = [
    ('section', ['padding-top', 'padding-bottom']),
    ('.sx-section, .sx-whyus, .sx-industries, .sx-cta-final', ['padding-top', 'padding-bottom']),
    ('.sx-inner, .sx-whyus-inner, .sx-industries-inner', ['padding-left', 'padding-right', 'max-width']),
    ('h1, .sx-hero-h1', ['margin-bottom']),
    ('h2', ['margin-bottom', 'margin-top']),
    ('h3, .sx-whyus-h3', ['margin-bottom']),
    ('p', ['margin-bottom']),
    ('.sx-whyus-grid, .sx-card-grid', ['gap']),
]

async def main():
    color_usage = defaultdict(set)  # color -> set of (sel, prop, page)
    spacing_usage = defaultdict(set)  # value -> set of (sel, prop, page)

    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context(viewport={'width':1440,'height':900})
        for url, lbl in PAGES:
            page = await ctx.new_page()
            try:
                resp = await page.goto(url + '?nc='+str(time.time()), wait_until='domcontentloaded', timeout=30000)
                if resp and resp.status >= 400:
                    await page.close(); continue
                await page.wait_for_timeout(1500)

                for sel, props in SELECTORS_COLOR:
                    data = await page.evaluate(f'''
                        Array.from(document.querySelectorAll({json.dumps(sel)}))
                            .slice(0, 5)
                            .map(el => {{
                                const cs = getComputedStyle(el);
                                return {{ {", ".join([f'{p.replace("-","_")}: cs.getPropertyValue({json.dumps(p)})' for p in props])} }};
                            }})
                    ''')
                    for d in data:
                        for prop in props:
                            val = d.get(prop.replace('-','_'),'')
                            if val and val not in ('rgba(0, 0, 0, 0)', 'transparent', ''):
                                color_usage[val].add((sel, prop, lbl))

                for sel, props in SELECTORS_SPACING:
                    data = await page.evaluate(f'''
                        Array.from(document.querySelectorAll({json.dumps(sel)}))
                            .slice(0, 3)
                            .map(el => {{
                                const cs = getComputedStyle(el);
                                return {{ {", ".join([f'{p.replace("-","_")}: cs.getPropertyValue({json.dumps(p)})' for p in props])} }};
                            }})
                    ''')
                    for d in data:
                        for prop in props:
                            val = d.get(prop.replace('-','_'),'')
                            if val and val not in ('0px', '0', 'normal', ''):
                                spacing_usage[(sel, prop, val)].add(lbl)
            except Exception as e:
                print(f'[{lbl}] ERR {str(e)[:80]}')
            await page.close()
        await b.close()

    # Analyze: cluster similar colors
    def parse_rgb(c):
        m = re.match(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', c)
        if m: return (int(m.group(1)), int(m.group(2)), int(m.group(3)))
        return None

    print('========== UNIQUE COLORS FOUND ==========\n')
    # Group colors by close similarity (Euclidean dist < 10 in RGB)
    colors_list = list(color_usage.keys())
    rgbs = [(c, parse_rgb(c)) for c in colors_list]
    rgbs = [(c, rgb) for c, rgb in rgbs if rgb]

    clusters = []
    used = set()
    for i, (c, rgb) in enumerate(rgbs):
        if c in used: continue
        cluster = [c]
        used.add(c)
        for j, (c2, rgb2) in enumerate(rgbs):
            if c2 in used: continue
            if abs(rgb[0]-rgb2[0]) + abs(rgb[1]-rgb2[1]) + abs(rgb[2]-rgb2[2]) < 25:
                cluster.append(c2)
                used.add(c2)
        clusters.append(cluster)

    # Show clusters with >1 color (these are inconsistencies)
    print('=== COLOR CLUSTERS (near-duplicates that may be inconsistent) ===\n')
    inconsistent_clusters = [c for c in clusters if len(c) > 1]
    for cluster in sorted(inconsistent_clusters, key=lambda x: -len(x)):
        print(f'Cluster ({len(cluster)} variants):')
        for c in cluster:
            usages = color_usage[c]
            pages = set(u[2] for u in usages)
            sels = set(f"{u[0]}:{u[1]}" for u in usages)
            print(f'  {c}  used in {len(pages)} pages, selectors: {list(sels)[:3]}')
        print()

    # Spacing inconsistencies
    print('========== SPACING INCONSISTENCIES ==========\n')
    spacing_by_sel_prop = defaultdict(list)
    for (sel, prop, val), pages in spacing_usage.items():
        spacing_by_sel_prop[(sel, prop)].append((val, len(pages), pages))

    for (sel, prop), variants in spacing_by_sel_prop.items():
        if len(variants) > 1:
            # Only flag if values differ significantly
            print(f'\n--- {sel} / {prop} — {len(variants)} variants ---')
            for val, cnt, pages in sorted(variants, key=lambda x: -x[1]):
                print(f'  {val:10s}  ({cnt:2d} pages) {sorted(pages)[:5]}')

asyncio.run(main())
