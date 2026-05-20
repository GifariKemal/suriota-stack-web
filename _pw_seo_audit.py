"""Comprehensive SEO audit beyond meta titles/descriptions.
Checks: OG/Twitter meta, canonical, H1 count, image alt coverage, schema variety, robots.txt, sitemap.
"""
import asyncio, json, sys, io, urllib.request
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

PAGES = [
    'https://suriota.com/',
    'https://suriota.com/about-us/',
    'https://suriota.com/portfolio/',
    'https://suriota.com/internet-of-things/',
    'https://suriota.com/water-treatment/',
    'https://suriota.com/suriota-modbus-gateway/',
    'https://suriota.com/surge-water-analytic/',
    'https://suriota.com/artikel/',
]

async def audit_page(page, url):
    await page.goto(url, wait_until='domcontentloaded', timeout=30000)
    return await page.evaluate('''() => {
        const get = (sel, attr='content') => {
            const el = document.querySelector(sel);
            return el ? (attr === 'text' ? el.textContent.trim() : el.getAttribute(attr)) : null;
        };
        const all = (sel) => Array.from(document.querySelectorAll(sel));
        const schemas = all('script[type="application/ld+json"]').map(s => {
            try {
                const d = JSON.parse(s.textContent);
                if (Array.isArray(d)) return d.map(x => x['@type']);
                if (d['@graph']) return d['@graph'].map(x => x['@type']);
                return [d['@type']];
            } catch(e) { return ['INVALID']; }
        }).flat();
        const images = all('img');
        const noAlt = images.filter(i => !i.alt || i.alt.trim() === '').length;
        const h1s = all('h1').map(h => h.textContent.trim().slice(0, 80));
        const h2s = all('h2').length;
        return {
            canonical: get('link[rel="canonical"]', 'href'),
            og_title: get('meta[property="og:title"]'),
            og_desc: get('meta[property="og:description"]'),
            og_image: get('meta[property="og:image"]'),
            og_type: get('meta[property="og:type"]'),
            twitter_card: get('meta[name="twitter:card"]'),
            twitter_title: get('meta[name="twitter:title"]'),
            twitter_image: get('meta[name="twitter:image"]'),
            robots: get('meta[name="robots"]'),
            viewport: get('meta[name="viewport"]'),
            h1_count: h1s.length,
            h1_texts: h1s,
            h2_count: h2s,
            schemas: schemas,
            schema_unique: [...new Set(schemas)],
            images_total: images.length,
            images_no_alt: noAlt,
            lang: document.documentElement.lang
        };
    }''')

async def main():
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(user_agent='Mozilla/5.0 (Windows NT 10.0) Chrome/120.0')
        for url in PAGES:
            page = await ctx.new_page()
            try:
                r = await audit_page(page, url)
                r['url'] = url
                results.append(r)
            except Exception as e:
                results.append({'url': url, 'error': str(e)[:200]})
            await page.close()
        await browser.close()

    # Report
    print('\n' + '=' * 100)
    print('TECHNICAL SEO AUDIT — 8 sample pages')
    print('=' * 100)
    for r in results:
        if 'error' in r:
            print(f"\n{r['url']}: ERROR {r['error']}")
            continue
        print(f"\n{r['url']}")
        print(f"  canonical    : {r['canonical']}")
        print(f"  og:title     : {(r['og_title'] or 'MISSING')[:80]}")
        print(f"  og:image     : {(r['og_image'] or 'MISSING')[:80]}")
        print(f"  twitter:card : {r['twitter_card'] or 'MISSING'}")
        print(f"  twitter:image: {(r['twitter_image'] or 'MISSING')[:80]}")
        print(f"  H1 count     : {r['h1_count']} - {r['h1_texts']}")
        print(f"  H2 count     : {r['h2_count']}")
        print(f"  schemas      : {r['schema_unique']}")
        print(f"  images       : {r['images_total']} total, {r['images_no_alt']} missing alt")
        print(f"  lang         : {r['lang']}")

    # Check robots + sitemap
    print('\n' + '=' * 100)
    print('ROBOTS + SITEMAP')
    print('=' * 100)
    for path in ['/robots.txt', '/sitemap.xml', '/sitemap_index.xml', '/sitemap.aioseo.xml']:
        try:
            req = urllib.request.Request('https://suriota.com' + path, headers={'User-Agent': 'Mozilla/5.0'})
            resp = urllib.request.urlopen(req, timeout=10)
            body = resp.read().decode('utf-8', errors='replace')
            print(f'{path}: HTTP {resp.status}, {len(body)} bytes')
            if path == '/robots.txt':
                print('  ' + body.replace('\n', '\n  ')[:400])
        except Exception as e:
            print(f'{path}: ERROR {e}')

    with open('_pw_seo_audit_report.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print('\nJSON → _pw_seo_audit_report.json')

asyncio.run(main())
