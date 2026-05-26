from playwright.sync_api import sync_playwright
from pathlib import Path

TARGETS = {
    5556: ('p3-en', 'https://suriota.com/digital-transformation-consulting/'),
    5557: ('p4-en', 'https://suriota.com/industrial-engineering-automation/'),
    5558: ('p5-en', 'https://suriota.com/surge-saas-platform/'),
    5566: ('p1-id', 'https://suriota.com/id/iot-industri-integrasi-sistem/'),
    5573: ('p3-zh', 'https://suriota.com/zh/shuzihua-zhuanxing-zixun/'),
}

OUT = Path(r'C:\Users\Administrator\Music\Website Suriota\audit\pillar-v2-snapshots\_tmp')
OUT.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch()
    for pid, (label, url) in TARGETS.items():
        ctx = b.new_context(viewport={'width':1440,'height':900}, device_scale_factor=2)
        page = ctx.new_page()
        try:
            page.goto(url, wait_until='networkidle', timeout=45000)
        except Exception as e:
            print(f'{pid} {label}: NAV ERROR {e}')
            ctx.close()
            continue

        page.evaluate("document.querySelectorAll('.sxp-reveal').forEach(el=>el.classList.add('is-visible'))")
        page.wait_for_timeout(400)

        em_count = page.evaluate("""() => {
          const main = document.querySelector('main');
          return main ? (main.innerText.match(/\\u2014/g) || []).length : 0;
        }""")

        try:
            faq_btn = page.locator('.sxp-faq__btn').first
            faq_btn.scroll_into_view_if_needed()
            faq_btn.click()
            page.wait_for_timeout(400)
        except Exception as e:
            print(f'{pid} {label}: FAQ click error {e}')

        open_bg = page.evaluate("""() => {
          const el = document.querySelector('.sxp-faq__item:has(.sxp-faq__btn[aria-expanded="true"])');
          return el ? getComputedStyle(el).backgroundColor : 'none';
        }""")

        try:
            faq_section = page.locator('.sxp-faq').first
            faq_section.screenshot(path=str(OUT / f'verify-faq-{label}.png'))
        except Exception as e:
            print(f'{pid} {label}: FAQ snap error {e}')

        try:
            cta = page.locator('.sxp-cta-block').first
            cta.scroll_into_view_if_needed()
            page.wait_for_timeout(400)
            cta.screenshot(path=str(OUT / f'verify-cta-{label}.png'))
        except Exception as e:
            print(f'{pid} {label}: CTA snap error {e}')

        wa_svg = page.evaluate("""() => {
          const path = document.querySelector('.sxp-cta-block__wa svg path');
          return path ? path.getAttribute('d').length : 0;
        }""")

        try:
            hero = page.locator('.sxp-hero').first
            hero.screenshot(path=str(OUT / f'verify-hero-{label}.png'))
        except Exception as e:
            print(f'{pid} {label}: HERO snap error {e}')

        print(f'{pid} {label}:')
        print(f'   em_dash_in_main_text: {em_count}')
        print(f'   faq_open_bg: {open_bg}')
        print(f'   wa_svg_path_length: {wa_svg}')
        ctx.close()
    b.close()
