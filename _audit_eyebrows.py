"""Audit all .sx-eyebrow content across pages — find non-label content."""
import asyncio, sys, io, time, json
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
]

async def main():
    suspicious = []
    all_eyebrows = []
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        for url, lbl in PAGES:
            page = await b.new_page()
            try:
                resp = await page.goto(url + '?nc='+str(time.time()), wait_until='domcontentloaded', timeout=30000)
                if resp and resp.status >= 400:
                    await page.close(); continue
                await page.wait_for_timeout(1500)
                eyebrows = await page.evaluate('''
                    (() => {
                        const arr=[];
                        document.querySelectorAll('.sx-eyebrow, .sxa-eyebrow').forEach(el => {
                            const text = (el.innerText||'').trim();
                            if (text) arr.push({text, html: el.outerHTML.slice(0,200)});
                        });
                        return arr;
                    })()
                ''')
                for e in eyebrows:
                    all_eyebrows.append({'page': lbl, 'text': e['text']})
                    # Heuristics for suspicious eyebrow:
                    # - Contains proper noun pattern (PT, SURIOTA company name)
                    # - More than 5 words
                    # - Contains lowercase letters (mixed case content)
                    text = e['text']
                    words = text.split()
                    is_pt = 'PT' in text and 'SURYA' in text.upper()
                    is_long = len(words) > 5
                    has_lower = any(c.islower() for c in text)
                    has_sentence = '.' in text or ',' in text
                    if is_pt or is_long or has_sentence:
                        suspicious.append({'page': lbl, 'text': text, 'reason':
                            ('company-name' if is_pt else '') +
                            (' long' if is_long else '') +
                            (' sentence' if has_sentence else '')})
            except Exception as e:
                print(f'[{lbl}] ERR {str(e)[:80]}')
            await page.close()
        await b.close()

    # Frequency of unique eyebrow texts
    from collections import Counter
    counter = Counter(e['text'] for e in all_eyebrows)
    print('=== ALL UNIQUE EYEBROW TEXTS (with frequency) ===')
    for txt, cnt in sorted(counter.items(), key=lambda x: -x[1]):
        flag = '⚠️' if cnt >= 1 and (
            'PT' in txt and 'SURYA' in txt.upper() or
            len(txt.split()) > 5 or
            ',' in txt or '.' in txt
        ) else '  '
        print(f"  {flag} ({cnt:2d}x) \"{txt[:100]}\"")

    print(f'\n=== SUSPICIOUS EYEBROWS ({len(suspicious)}) ===')
    by_text = {}
    for s in suspicious:
        by_text.setdefault(s['text'], []).append(s['page'])
    for text, pages in by_text.items():
        print(f"  \"{text[:100]}\" — on: {','.join(pages)}")

asyncio.run(main())
