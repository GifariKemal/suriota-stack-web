"""Playwright check: mobile portrait + desktop-mode-on-mobile + desktop, snap back-to-top behaviour."""
import asyncio
from playwright.async_api import async_playwright
import os, sys

URL = "https://suriota.com/setup-genset-dse-5520/"
OUT = "C:/Users/Administrator/Music/Website Suriota"

async def measure(page, label):
    """Return key layout metrics + screenshot."""
    # Wait for v3 JS to inject hero
    await page.wait_for_selector(".sxa-hero", timeout=10000)
    await page.wait_for_timeout(800)

    vp = page.viewport_size
    metrics = await page.evaluate("""() => {
        const pc = document.querySelector('.page-content');
        const main = document.querySelector('.sxa-main');
        const hero = document.querySelector('.sxa-hero');
        const cta  = document.querySelector('.sxa-cta-final');
        const bt   = document.querySelector('.sxa-back-top');
        const sm   = document.querySelector('main.site-main, #content.site-main');
        const r = el => el ? el.getBoundingClientRect() : null;
        const cs = el => el ? getComputedStyle(el) : null;
        return {
            viewport: { w: window.innerWidth, h: window.innerHeight, devicePixelRatio: window.devicePixelRatio },
            documentWidth: document.documentElement.scrollWidth,
            site_main: sm ? { width: r(sm).width, padL: cs(sm).paddingLeft, padR: cs(sm).paddingRight, maxW: cs(sm).maxWidth } : null,
            page_content: pc ? { width: r(pc).width, left: r(pc).left, right: r(pc).right, padL: cs(pc).paddingLeft, padR: cs(pc).paddingRight, maxW: cs(pc).maxWidth, display: cs(pc).display } : null,
            sxa_main: main ? { width: r(main).width, left: r(main).left, padL: cs(main).paddingLeft, padR: cs(main).paddingRight } : null,
            hero: hero ? { width: r(hero).width, left: r(hero).left, padL: cs(hero).paddingLeft } : null,
            cta:  cta  ? { width: r(cta).width, left: r(cta).left, padL: cs(cta).paddingLeft } : null,
            backtop: bt ? { display: cs(bt).display, position: cs(bt).position, left: cs(bt).left, right: cs(bt).right, bottom: cs(bt).bottom, zIndex: cs(bt).zIndex, opacity: cs(bt).opacity, visibility: cs(bt).visibility, exists: true } : { exists: false }
        };
    }""")
    print(f"\n=== [{label}] viewport {vp} ===")
    import json
    print(json.dumps(metrics, indent=2))

    # Snap initial
    await page.screenshot(path=f"{OUT}/_check_{label}_top.png", full_page=False)

    # Scroll to trigger back-to-top
    await page.evaluate("window.scrollTo(0, 1200)")
    await page.wait_for_timeout(600)
    back_state = await page.evaluate("""() => {
        const bt = document.querySelector('.sxa-back-top');
        if(!bt) return {exists:false};
        const r = bt.getBoundingClientRect();
        const cs = getComputedStyle(bt);
        return {
            inView: r.width>0 && r.height>0 && r.top<window.innerHeight && r.left<window.innerWidth,
            hasShow: bt.classList.contains('show'),
            rect: {top:r.top,left:r.left,right:r.right,bottom:r.bottom,width:r.width,height:r.height},
            opacity: cs.opacity, visibility: cs.visibility, display: cs.display
        };
    }""")
    print(f"After scroll y=1200, back-to-top:", back_state)
    await page.screenshot(path=f"{OUT}/_check_{label}_scrolled.png", full_page=False)
    return metrics, back_state


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # ============ 1) REAL MOBILE PORTRAIT ============
        ctx_m = await browser.new_context(
            viewport={"width": 390, "height": 844},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1",
            device_scale_factor=3,
            is_mobile=True,
            has_touch=True
        )
        page_m = await ctx_m.new_page()
        await page_m.goto(URL, wait_until="networkidle", timeout=45000)
        await measure(page_m, "mobile-real-390")
        await ctx_m.close()

        # ============ 2) DESKTOP MODE ON MOBILE (Chrome Android style: 980 viewport, desktop UA) ============
        ctx_dm = await browser.new_context(
            viewport={"width": 980, "height": 1700},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36",
            device_scale_factor=1,
            is_mobile=False,
        )
        page_dm = await ctx_dm.new_page()
        await page_dm.goto(URL, wait_until="networkidle", timeout=45000)
        await measure(page_dm, "desktop-mode-980")
        await ctx_dm.close()

        # ============ 3) REAL DESKTOP ============
        ctx_d = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            device_scale_factor=1,
            is_mobile=False
        )
        page_d = await ctx_d.new_page()
        await page_d.goto(URL, wait_until="networkidle", timeout=45000)
        await measure(page_d, "desktop-1440")
        await ctx_d.close()

        await browser.close()

asyncio.run(main())
