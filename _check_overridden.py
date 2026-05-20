"""Check for overridden Geist rules — find elements where Geist is declared but not winning."""
import asyncio, sys, io, time, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

PAGES = [
    ('https://suriota.com/', 'Home'),
    ('https://suriota.com/about/', 'About'),
    ('https://suriota.com/portfolio/', 'Portfolio'),
    ('https://suriota.com/automation/', 'Automation'),
    ('https://suriota.com/iso-m485-series/', 'ISO-M485'),
    ('https://suriota.com/suriota-modbus-gateway/', 'MGATE'),
    ('https://suriota.com/surge-energy-mapping/', 'SURGE-E'),
    ('https://suriota.com/contact/', 'Contact'),
    ('https://suriota.com/privacy-policy/', 'Privacy'),
    ('https://suriota.com/id/beranda/', 'ID-Home'),
    ('https://suriota.com/id/portfolio-id/', 'ID-Portfolio'),
    ('https://suriota.com/id/kebijakan-privasi/', 'ID-Privacy'),
    ('https://suriota.com/jasa-maintenance-webmail-webmail-maintenance-pt-hijrah-travel/', 'Post-Maint'),
    ('https://suriota.com/survey-setup-vfd/', 'Post-VFD'),
]

# Selectors that SHOULD show Geist or Geist Mono (or be overridden but we'll detect)
SELECTORS_MONO = [
    '.sx-mono', '[class*="mono"]', '.sxa-rel-meta', 'code', 'pre', 'kbd', 'samp',
    '.sx-eyebrow', '.elementor-widget-code'
]

SELECTORS_SANS = [
    'body', 'h1', 'h2', 'h3', 'h4', 'h5', 'p', 'a', 'li', 'span', 'small',
    '.elementor-button', '.elementor-heading-title', '.elementor-widget-text-editor',
    'nav', 'header', 'footer', '.elementor-nav-menu a',
    'input', 'button', 'textarea', 'select',
    'td', 'th', 'blockquote',
    '.sx-hero-title', '.sx-hero-subtitle', '.sx-stat-num', '.sx-stat-label',
    '.sx-card-title', '.sx-card-body', '.sx-callout',
    '.sx-whyus-h3', '.sx-whyus-desc', '.sx-whyus-title',
    '.about-service-card h3', '.about-service-card p',
    '.sxa-h1', '.sxa-main', '.sxa-cta-h2', '.sxa-cta-sub', '.sxa-cta-btn',
    '.sxa-related-title', '.sxa-rel-title',
    '.elementor-icon-list-text', '.elementor-icon-box-description',
    '.elementor-cta__title', '.elementor-cta__description',
    '.elementor-testimonial__name', '.elementor-testimonial__title',
    '.elementor-accordion-title', '.elementor-tab-title',
    'figcaption',
]

async def main():
    overridden_issues = []  # rule declares Geist but computed is something else
    rule_inspections = []

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

                # For each selector, find elements and check rule cascade
                inspection = await page.evaluate('''
                    (() => {
                        const sansSelectors = ''' + json.dumps(SELECTORS_SANS) + ''';
                        const monoSelectors = ''' + json.dumps(SELECTORS_MONO) + ''';
                        const issues = [];
                        const allSel = sansSelectors.concat(monoSelectors).map(s => ({sel: s, isMono: monoSelectors.includes(s)}));

                        for (const {sel, isMono} of allSel) {
                            let elements;
                            try { elements = document.querySelectorAll(sel); } catch(e) { continue; }
                            if (!elements.length) continue;
                            const el = elements[0];
                            const cs = getComputedStyle(el);
                            const computedFamily = cs.fontFamily;
                            const primary = computedFamily.split(',')[0].replace(/['"]/g, '').trim();

                            // Find ALL CSS rules that match this element AND set font-family
                            const matchedFontFamilyRules = [];
                            for (const sheet of document.styleSheets) {
                                let rules;
                                try { rules = sheet.cssRules; } catch(e) { continue; }
                                if (!rules) continue;
                                for (const r of rules) {
                                    try {
                                        if (!r.selectorText) continue;
                                        if (!el.matches(r.selectorText)) continue;
                                        const ff = r.style.getPropertyValue('font-family');
                                        const fSh = r.style.getPropertyValue('font');
                                        if (!ff && !fSh) continue;
                                        const imp = r.style.getPropertyPriority('font-family') === 'important' ||
                                                    r.style.getPropertyPriority('font') === 'important';
                                        matchedFontFamilyRules.push({
                                            selector: r.selectorText.slice(0, 100),
                                            fontFamily: ff || fSh,
                                            important: imp,
                                            sheet: (sheet.href || 'inline').split('/').pop().slice(0, 50)
                                        });
                                    } catch(e) {}
                                }
                            }

                            // Also inline styles
                            const inlineFF = el.style.fontFamily;
                            if (inlineFF) {
                                matchedFontFamilyRules.push({selector: '[inline]', fontFamily: inlineFF, important: true, sheet: 'inline'});
                            }

                            // Check if Geist is being overridden
                            const hasGeistRule = matchedFontFamilyRules.some(r => /Geist/.test(r.fontFamily));
                            const usingGeist = /Geist/.test(primary);
                            const expectedFont = isMono ? 'Geist Mono' : 'Geist';
                            const usingExpectedFont = primary === expectedFont || (isMono && /Geist Mono/.test(computedFamily.split(',')[0]));

                            if (hasGeistRule && !usingGeist) {
                                issues.push({
                                    sel, primary, computed: computedFamily.slice(0, 120),
                                    rules: matchedFontFamilyRules.slice(-5)
                                });
                            }
                            // Also flag if mono selector but using sans Geist (vs Geist Mono)
                            if (isMono && usingGeist && !/Geist Mono/.test(primary)) {
                                issues.push({
                                    sel: sel + ' (mono expected)',
                                    primary, computed: computedFamily.slice(0, 120),
                                    rules: matchedFontFamilyRules.slice(-5)
                                });
                            }
                        }
                        return issues;
                    })()
                ''')

                for issue in inspection:
                    overridden_issues.append({'lbl': lbl, **issue})
            except Exception as e:
                print(f'[{lbl}] ERR {str(e)[:80]}')
            await page.close()
        await b.close()

    print(f'\n========== OVERRIDDEN GEIST RULES ({len(overridden_issues)} cases) ==========\n')
    if not overridden_issues:
        print('  No overrides found — Geist wins everywhere ✓')
        return

    # Group by selector
    by_sel = {}
    for i in overridden_issues:
        by_sel.setdefault(i['sel'], []).append(i)

    for sel, lst in by_sel.items():
        pages = ','.join(set(x['lbl'] for x in lst))
        ex = lst[0]
        print(f'=== {sel} ===')
        print(f'  Pages: {pages}')
        print(f'  Computed primary: {ex["primary"]}')
        print(f'  Full computed: {ex["computed"]}')
        print(f'  Last 5 matched rules (in cascade order):')
        for r in ex['rules']:
            imp = ' !important' if r['important'] else ''
            print(f"    {r['selector']:60s} → font-family: {r['fontFamily']}{imp} [from {r['sheet']}]")
        print()

asyncio.run(main())
