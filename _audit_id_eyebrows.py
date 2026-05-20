"""Audit eyebrows ONLY on ID pages — find English text that should be Bahasa."""
import asyncio, sys, io, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

ID_PAGES = [
    ('https://suriota.com/id/beranda/', 'ID-Home'),
    ('https://suriota.com/id/tentang-kami/', 'ID-About'),
    ('https://suriota.com/id/portfolio-id/', 'ID-Portfolio'),
    ('https://suriota.com/id/kontak/', 'ID-Contact'),
    ('https://suriota.com/id/magang-srt-team/', 'ID-Internship'),
    ('https://suriota.com/id/water-treatment-id/', 'ID-WT'),
    ('https://suriota.com/id/saas-id/', 'ID-SaaS'),
    ('https://suriota.com/id/artikel-id/', 'ID-Artikel'),
    ('https://suriota.com/id/electrical-id/', 'ID-Electrical'),
    ('https://suriota.com/id/automation-id/', 'ID-Automation'),
    ('https://suriota.com/id/renewable-energy-id/', 'ID-RE'),
    ('https://suriota.com/id/internet-of-things-id/', 'ID-IoT'),
    ('https://suriota.com/id/data-analytics-id/', 'ID-DA'),
    ('https://suriota.com/id/digital-consulting-id/', 'ID-DC'),
    ('https://suriota.com/id/artificial-intelligence-id/', 'ID-AI'),
    ('https://suriota.com/id/system-integration-id/', 'ID-SysInt'),
    ('https://suriota.com/id/suriota-modbus-gateway-id/', 'ID-MGATE'),
    ('https://suriota.com/id/surge-energy-mapping-id/', 'ID-SURGE-E'),
    ('https://suriota.com/id/surge-vessel-tracking-id/', 'ID-SURGE-V'),
    ('https://suriota.com/id/surge-water-analytic-id/', 'ID-SURGE-W'),
    ('https://suriota.com/id/iso-m485-series-id/', 'ID-ISO-M485'),
    ('https://suriota.com/id/thm-30md-id/', 'ID-THM-30MD'),
    ('https://suriota.com/id/pm1611-wd-id/', 'ID-PM1611'),
    ('https://suriota.com/id/rs-485-surge-protector-id/', 'ID-SPD-T485'),
    ('https://suriota.com/id/waste-water-logger-id/', 'ID-WW'),
    ('https://suriota.com/id/kebijakan-privasi/', 'ID-Privacy'),
    ('https://suriota.com/id/syarat-layanan/', 'ID-Terms'),
]

# English words that should NOT appear in ID eyebrows
ENGLISH_PATTERNS = [
    'KEY FEATURES', 'BUILT FOR', 'WHY SURIOTA', 'WHY CHOOSE SURIOTA', 'WHAT WE DELIVER',
    'HOW WE WORK', 'APPLICATIONS', 'INDUSTRIES WE SERVE', 'INDUSTRIES WE AUTOMATE',
    'INDUSTRIES WE POWER', 'WHY SURGE', 'CONTACT', 'START A CONVERSATION',
    'WHAT HAPPENS NEXT', 'READY TO START?', 'ABOUT US', 'LEGAL', 'FAQ'
]

async def main():
    all_id_eyebrows = []
    issues = []
    async with async_playwright() as p:
        b = await p.chromium.launch(headless=True)
        for url, lbl in ID_PAGES:
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
                            if (text) arr.push(text);
                        });
                        return arr;
                    })()
                ''')
                for txt in eyebrows:
                    all_id_eyebrows.append({'page': lbl, 'text': txt})
                    if txt in ENGLISH_PATTERNS:
                        issues.append({'page': lbl, 'text': txt})
            except Exception as e:
                print(f'[{lbl}] ERR {str(e)[:80]}')
            await page.close()
        await b.close()

    from collections import Counter
    counter = Counter(e['text'] for e in all_id_eyebrows)
    print('=== ALL ID PAGE EYEBROW TEXTS ===')
    for txt, cnt in sorted(counter.items(), key=lambda x: -x[1]):
        flag = '⚠️ EN' if txt in ENGLISH_PATTERNS else '   '
        # also check if text contains common English words
        english_words = ['the','and','for','our','we','your','you','of','in','on','with','by']
        contains_en = any(' '+w+' ' in ' '+txt.lower()+' ' or txt.lower().startswith(w+' ') for w in english_words)
        if contains_en and not txt in ENGLISH_PATTERNS:
            flag = '⚠️ en?'
        print(f"  {flag} ({cnt:2d}x) \"{txt}\"")

    print(f'\n=== ENGLISH EYEBROWS ON ID PAGES ({len(issues)} cases) ===')
    by_text = {}
    for s in issues:
        by_text.setdefault(s['text'], []).append(s['page'])
    for text, pages in by_text.items():
        print(f"  EN eyebrow \"{text}\" → on: {', '.join(pages)}")

asyncio.run(main())
