"""Final verification of A-F fixes."""
import asyncio, sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

PAGES = [
    ('https://suriota.com/',                            'Homepage'),
    ('https://suriota.com/about-us/',                   'About'),
    ('https://suriota.com/suriota-modbus-gateway/',     'SRT-MGATE'),
    ('https://suriota.com/surge-water-analytic/',       'SURGE-Water'),
    ('https://suriota.com/water-treatment/',            'WT'),
]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(user_agent='Mozilla/5.0 Chrome/120.0')
        for url, lbl in PAGES:
            page = await ctx.new_page()
            await page.goto(url + '?cb=v6', wait_until='domcontentloaded', timeout=30000)
            await page.wait_for_timeout(1500)
            data = await page.evaluate('''() => {
                const get = (sel, a='content') => document.querySelector(sel)?.getAttribute(a);
                const ldScripts = Array.from(document.querySelectorAll('script[type="application/ld+json"]'));
                const parsed = [], invalid = [];
                ldScripts.forEach((s, i) => {
                    try {
                        const d = JSON.parse(s.textContent);
                        parsed.push(d['@type'] || (d['@graph'] ? 'graph' : 'unknown'));
                    } catch(e) { invalid.push(i); }
                });
                const imgs = Array.from(document.querySelectorAll('img'));
                return {
                    lang: document.documentElement.lang,
                    og_title: get('meta[property="og:title"]'),
                    og_image: get('meta[property="og:image"]'),
                    schemas: parsed,
                    invalid_count: invalid.length,
                    has_WebSite: parsed.includes('WebSite'),
                    has_Organization: parsed.includes('Organization'),
                    imgs_total: imgs.length,
                    imgs_no_alt: imgs.filter(i => !i.alt || i.alt.trim() === '').length,
                    title: document.title
                };
            }''')
            await page.close()
            print(f'\n[{lbl}] {url}')
            print(f"  lang        : {data['lang']}  {'OK' if data['lang']=='en' else 'BAD'}")
            print(f"  title       : {data['title'][:75]}")
            print(f"  og:title    : {data['og_title']}")
            print(f"  schemas     : {data['schemas']}")
            print(f"  WebSite     : {'OK' if data['has_WebSite'] else 'MISSING'}")
            print(f"  Organization: {'OK' if data['has_Organization'] else 'MISSING'}")
            print(f"  INVALID JSON-LD: {data['invalid_count']}  {'OK' if data['invalid_count']==0 else 'BAD'}")
            print(f"  imgs        : {data['imgs_total']} total, {data['imgs_no_alt']} no-alt")
        await browser.close()

asyncio.run(main())
