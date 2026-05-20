"""Audit broader inconsistencies: buttons, h2 titles, mixed-language, colors."""
import asyncio, sys, io, time, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

PAGES = [
    ('https://suriota.com/', 'Home', 'en'),
    ('https://suriota.com/about/', 'About', 'en'),
    ('https://suriota.com/portfolio/', 'Portfolio', 'en'),
    ('https://suriota.com/contact/', 'Contact', 'en'),
    ('https://suriota.com/automation/', 'Automation', 'en'),
    ('https://suriota.com/electrical/', 'Electrical', 'en'),
    ('https://suriota.com/renewable-energy/', 'RE', 'en'),
    ('https://suriota.com/internet-of-things/', 'IoT', 'en'),
    ('https://suriota.com/water-treatment/', 'WT', 'en'),
    ('https://suriota.com/data-analytics/', 'DA', 'en'),
    ('https://suriota.com/digital-consulting/', 'DC', 'en'),
    ('https://suriota.com/artificial-intelligence/', 'AI', 'en'),
    ('https://suriota.com/system-integration/', 'SysInt', 'en'),
    ('https://suriota.com/saas/', 'SaaS', 'en'),
    ('https://suriota.com/surge-energy-mapping/', 'SURGE-E', 'en'),
    ('https://suriota.com/surge-vessel-tracking/', 'SURGE-V', 'en'),
    ('https://suriota.com/surge-water-analytic/', 'SURGE-W', 'en'),
    ('https://suriota.com/suriota-modbus-gateway/', 'MGATE', 'en'),
    ('https://suriota.com/iso-m485-series/', 'ISO-M485', 'en'),
    ('https://suriota.com/pm1611-wd/', 'PM1611', 'en'),
    ('https://suriota.com/thm-30md/', 'THM-30MD', 'en'),
    ('https://suriota.com/rs-485-surge-protector/', 'SPD-T485', 'en'),
    ('https://suriota.com/waste-water-logger/', 'WW', 'en'),
    ('https://suriota.com/privacy-policy/', 'Privacy', 'en'),
    ('https://suriota.com/terms-of-service/', 'Terms', 'en'),
    ('https://suriota.com/id/beranda/', 'ID-Home', 'id'),
    ('https://suriota.com/id/tentang-kami/', 'ID-About', 'id'),
    ('https://suriota.com/id/portfolio-id/', 'ID-Portfolio', 'id'),
    ('https://suriota.com/id/kontak/', 'ID-Contact', 'id'),
    ('https://suriota.com/id/automation-id/', 'ID-Automation', 'id'),
    ('https://suriota.com/id/electrical-id/', 'ID-Electrical', 'id'),
    ('https://suriota.com/id/water-treatment-id/', 'ID-WT', 'id'),
    ('https://suriota.com/id/iso-m485-series-id/', 'ID-ISO-M485', 'id'),
    ('https://suriota.com/id/surge-energy-mapping-id/', 'ID-SURGE-E', 'id'),
    ('https://suriota.com/id/kebijakan-privasi/', 'ID-Privacy', 'id'),
    ('https://suriota.com/id/syarat-layanan/', 'ID-Terms', 'id'),
]

# Strong English markers (full English phrases unlikely in proper Bahasa)
EN_PHRASES = [
    'Why choose', 'Built for', 'Get started', 'Learn more', 'Read more', 'See more',
    'Contact us', 'Get in touch', 'Schedule a demo', 'Book a call', 'Request a',
    'Free consultation', 'No obligation', 'within 24 hours', 'Talk to', 'Reach out',
    'Click here', 'View all', 'Explore our', 'Discover our', 'Find out more',
    'Coming soon', 'Stay tuned', 'Sign up', 'Subscribe',
]

# Bahasa markers (English shouldn't have these)
ID_PHRASES = [
    'Kami menyediakan', 'Pelajari lebih', 'Lihat selengkapnya', 'Hubungi kami',
    'Dapatkan', 'Pesan demo', 'Konsultasi gratis', 'Tanpa kewajiban',
    'Tentang kami', 'Layanan kami', 'Produk kami',
]

async def main():
    button_texts = {}  # text -> set of pages
    h2_texts = {}
    mixed_lang_issues = []  # English on ID pages
    cta_buttons_per_page = {}

    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        ctx = await b.new_context(viewport={'width':1440,'height':900})
        for url, lbl, lang in PAGES:
            page = await ctx.new_page()
            try:
                resp = await page.goto(url + '?nc='+str(time.time()), wait_until='domcontentloaded', timeout=30000)
                if resp and resp.status >= 400:
                    await page.close(); continue
                await page.wait_for_timeout(1500)

                # Get all button-like text
                btns = await page.evaluate('''
                    Array.from(document.querySelectorAll('a.elementor-button, .elementor-button, button:not([aria-label*="close"]), .sx-cta-btn, .sxa-cta-btn, a[class*="cta"], a[class*="button"]')).map(el => {
                        const t = (el.innerText||'').trim();
                        return t;
                    }).filter(t => t && t.length < 50)
                ''')
                cta_buttons_per_page[lbl] = btns
                for t in btns:
                    button_texts.setdefault(t, set()).add(lbl)

                # Get all h2 text
                h2s = await page.evaluate('''
                    Array.from(document.querySelectorAll('h2, .sx-hero-h1, .sx-section-title, .sx-whyus-title, .sx-industries-title, .sxa-h1, .sxa-cta-h2')).map(el => (el.innerText||'').trim()).filter(t => t && t.length < 200)
                ''')
                for t in h2s:
                    h2_texts.setdefault(t, set()).add(lbl)

                # Check for English content on ID pages
                if lang == 'id':
                    body_text = await page.evaluate('''
                        document.body.innerText.split('\\n').filter(l => l.trim().length > 20).join('\\n')
                    ''')
                    for phrase in EN_PHRASES:
                        if phrase.lower() in body_text.lower():
                            # show first occurrence with context
                            pos = body_text.lower().find(phrase.lower())
                            mixed_lang_issues.append({
                                'page': lbl,
                                'phrase': phrase,
                                'context': body_text[max(0,pos-30):pos+80]
                            })
                # Check for Bahasa content on EN pages
                if lang == 'en':
                    body_text = await page.evaluate('''
                        document.body.innerText.split('\\n').filter(l => l.trim().length > 20).join('\\n')
                    ''')
                    for phrase in ID_PHRASES:
                        if phrase.lower() in body_text.lower():
                            pos = body_text.lower().find(phrase.lower())
                            mixed_lang_issues.append({
                                'page': lbl,
                                'phrase': phrase,
                                'context': body_text[max(0,pos-30):pos+80]
                            })
            except Exception as e:
                print(f'[{lbl}] ERR {str(e)[:80]}')
            await page.close()
        await b.close()

    # Report: Button text taxonomy
    print('========== BUTTON / CTA TEXT TAXONOMY ==========\n')
    print(f'Total unique button texts: {len(button_texts)}')
    print()
    # Show those appearing multiple times (common CTAs) + flag inconsistencies
    common = sorted(button_texts.items(), key=lambda x: -len(x[1]))
    for txt, pages in common[:40]:
        marker = ''
        if 'Hubungi' in txt and 'Hubungi Kami' != txt: marker = ' ⚠️'
        print(f'  ({len(pages):3d} pages) "{txt}"{marker}')

    # Cluster similar buttons (CTA patterns)
    print('\n========== CTA PATTERN CLUSTERS (similar-meaning, different text) ==========\n')
    patterns = {
        'CONTACT/DEMO (EN)': ['Hubungi','Contact','Talk to','Get in touch','Reach out','Book','Schedule'],
        'CONSULT/CONSULTATION': ['Konsultasi','Consultation','Free consultation'],
        'WHATSAPP': ['WhatsApp','WA','Chat'],
        'DEMO': ['Demo','demo','Request demo','Live demo'],
        'LEARN/SELENGKAPNYA': ['Selengkapnya','Pelajari','Lihat','Learn more','See more','Read more','Explore','View'],
        'GET STARTED': ['Get Started','Mulai','Start'],
    }
    for pname, keywords in patterns.items():
        matches = []
        for txt, pages in button_texts.items():
            if any(kw.lower() in txt.lower() for kw in keywords):
                matches.append((txt, len(pages)))
        if matches:
            print(f'  {pname}:')
            for t, c in sorted(matches, key=lambda x: -x[1]):
                print(f'    ({c:3d}) "{t}"')
            print()

    # Mixed language on ID pages
    print('========== MIXED LANGUAGE ISSUES ==========\n')
    by_page = {}
    for i in mixed_lang_issues:
        by_page.setdefault(i['page'], []).append(i)
    for page, lst in by_page.items():
        if not lst: continue
        print(f'  {page}: {len(lst)} issues')
        seen = set()
        for i in lst[:5]:
            if i['phrase'] in seen: continue
            seen.add(i['phrase'])
            print(f'    - "{i["phrase"]}" in: "...{i["context"].strip()}..."')
        if len(lst) > 5:
            print(f'    ... +{len(lst)-5} more')
        print()

asyncio.run(main())
