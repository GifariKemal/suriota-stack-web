// Probe the Elementor image-carousel (widget e396a55) at suriota.com
// to find why autoplay/drag works on mobile but not desktop.
'use strict';

const path = require('path');
const fs = require('fs');

const PUPPETEER_PATH = 'C:/Users/Administrator/AppData/Local/Temp/node_modules/puppeteer';
const CHROME_PATH = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const URL = 'https://suriota.com/';
const WIDGET_ID = 'e396a55';
const OUT_JSON = 'C:/Users/Administrator/Music/Website Suriota/audit/carousel_desktop_probe.json';

const puppeteer = require(PUPPETEER_PATH);

async function probe(viewport, label) {
  const result = {
    label,
    viewport,
    url: URL,
    timestamp: new Date().toISOString(),
    pageErrors: [],
    consoleMessages: [],
    failedRequests: [],
    requests: [],
    inPageProbe: null,
  };

  const browser = await puppeteer.launch({
    executablePath: CHROME_PATH,
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage'],
  });

  try {
    const page = await browser.newPage();
    await page.setViewport(viewport);

    page.on('pageerror', e => result.pageErrors.push(String(e && e.message ? e.message : e)));
    page.on('console', msg => {
      try {
        result.consoleMessages.push({ type: msg.type(), text: msg.text() });
      } catch (_) {}
    });
    page.on('requestfailed', req => {
      try {
        result.failedRequests.push({
          url: req.url(),
          method: req.method(),
          failure: req.failure() ? req.failure().errorText : null,
          resourceType: req.resourceType(),
        });
      } catch (_) {}
    });
    page.on('requestfinished', req => {
      const u = req.url();
      if (/bundle\.js|image-carousel|swiper|177\.|wpo-minify|elementor.*\.js/i.test(u)) {
        result.requests.push({
          url: u,
          status: req.response() ? req.response().status() : null,
          resourceType: req.resourceType(),
        });
      }
    });

    await page.goto(URL, { waitUntil: 'networkidle2', timeout: 60000 });

    // Wait for the widget element
    await page.waitForSelector(`.elementor-element-${WIDGET_ID}`, { timeout: 30000 }).catch(() => {});
    // Give Elementor's lazy webpack chunks a chance to load.
    await new Promise(r => setTimeout(r, 4000));

    // Scroll the carousel into view in case it's lazy-init on intersect.
    await page.evaluate((id) => {
      const el = document.querySelector('.elementor-element-' + id);
      if (el) el.scrollIntoView({ behavior: 'instant', block: 'center' });
    }, WIDGET_ID);
    await new Promise(r => setTimeout(r, 3000));

    result.inPageProbe = await page.evaluate((id) => {
      function summarizeStyle(el, props) {
        if (!el) return null;
        const cs = getComputedStyle(el);
        const out = {};
        for (const p of props) out[p] = cs.getPropertyValue(p);
        return out;
      }

      const widget = document.querySelector('.elementor-element-' + id);
      if (!widget) return { error: 'widget not found' };

      const swiperEl = widget.querySelector('.swiper, .swiper-container');
      const wrapper = widget.querySelector('.swiper-wrapper');
      const slides = widget.querySelectorAll('.swiper-slide');
      const firstSlide = slides[0] || null;

      const swiperClasses = swiperEl ? Array.from(swiperEl.classList) : null;
      const swiperApi = (swiperEl && swiperEl.swiper) ? swiperEl.swiper : null;

      let swiperParams = null;
      let autoplayState = null;
      if (swiperApi) {
        try {
          swiperParams = {
            autoplay: swiperApi.params && swiperApi.params.autoplay,
            allowTouchMove: swiperApi.params && swiperApi.params.allowTouchMove,
            simulateTouch: swiperApi.params && swiperApi.params.simulateTouch,
            slidesPerView: swiperApi.params && swiperApi.params.slidesPerView,
            loop: swiperApi.params && swiperApi.params.loop,
            speed: swiperApi.params && swiperApi.params.speed,
            enabled: swiperApi.enabled,
            initialized: swiperApi.initialized,
            destroyed: swiperApi.destroyed,
            isLocked: swiperApi.isLocked,
            mouseEvents: swiperApi.mouse ? Object.keys(swiperApi.mouse) : null,
          };
          if (swiperApi.autoplay) {
            autoplayState = {
              running: swiperApi.autoplay.running,
              paused: swiperApi.autoplay.paused,
            };
          }
        } catch (e) {
          swiperParams = { error: String(e) };
        }
      }

      const widgetRect = widget.getBoundingClientRect();
      const cx = Math.floor(widgetRect.left + widgetRect.width / 2);
      const cy = Math.floor(widgetRect.top + widgetRect.height / 2);
      let elemAtPoint = null;
      try {
        const hit = document.elementFromPoint(cx, cy);
        if (hit) {
          elemAtPoint = {
            tag: hit.tagName,
            id: hit.id,
            className: hit.className && hit.className.toString ? hit.className.toString() : null,
            isInsideWidget: widget.contains(hit),
            outerHTMLstart: (hit.outerHTML || '').slice(0, 220),
          };
        }
      } catch (_) {}

      const cssProps = [
        'pointer-events','touch-action','user-select','transform',
        'overflow','overflow-x','overflow-y','width','height',
        'visibility','display','cursor','position','z-index'
      ];

      const wrapperInlineTransform = wrapper ? wrapper.style.transform : null;
      const wrapperInlineTransition = wrapper ? wrapper.style.transitionDuration : null;

      // Collect rules from stylesheets matching the widget id selector
      const matchingRules = [];
      try {
        for (const sheet of document.styleSheets) {
          let rules = null;
          try { rules = sheet.cssRules || sheet.rules; } catch (_) { continue; }
          if (!rules) continue;
          for (const rule of rules) {
            const sel = rule.selectorText;
            if (!sel) continue;
            if (
              sel.includes('elementor-element-' + id) ||
              sel.includes('image-carousel') ||
              /swiper(-wrapper|-slide)?[\s,>{:]?/.test(sel) && (sel.includes(id) || sel.includes('image-carousel'))
            ) {
              matchingRules.push({
                href: sheet.href || '(inline)',
                selector: sel,
                cssText: rule.cssText.slice(0, 400),
              });
              if (matchingRules.length > 60) break;
            }
          }
          if (matchingRules.length > 60) break;
        }
      } catch (e) {
        matchingRules.push({ error: String(e) });
      }

      // Also scan inline <style> blocks for the widget id, regardless of stylesheet rules
      const inlineStyleHits = [];
      try {
        const styles = document.querySelectorAll('style');
        styles.forEach((s, i) => {
          const txt = s.textContent || '';
          if (txt.includes(id) || txt.includes('image-carousel')) {
            inlineStyleHits.push({
              index: i,
              dataAttrs: Array.from(s.attributes).map(a => a.name + '=' + a.value),
              snippet: txt.slice(0, 400),
              length: txt.length,
            });
          }
        });
      } catch (_) {}

      // Check whether Elementor's image-carousel handler has been registered.
      const elementorFrontend = window.elementorFrontend || null;
      let handlerInfo = null;
      try {
        if (elementorFrontend && elementorFrontend.elementsHandler) {
          const handlers = elementorFrontend.elementsHandler.elementsHandlers || {};
          handlerInfo = {
            keys: Object.keys(handlers),
            hasImageCarousel: !!handlers['image-carousel.default'] || !!handlers['image-carousel'],
          };
        }
      } catch (e) { handlerInfo = { error: String(e) }; }

      // Swiper global presence
      const swiperGlobals = {
        windowSwiper: typeof window.Swiper,
        elementorSwiper: !!(elementorFrontend && elementorFrontend.utils && elementorFrontend.utils.swiper),
      };

      return {
        widget: {
          dataSettings: widget.getAttribute('data-settings'),
          classes: Array.from(widget.classList),
          rect: widgetRect.toJSON ? widgetRect.toJSON() : {
            x: widgetRect.x, y: widgetRect.y, width: widgetRect.width, height: widgetRect.height,
          },
        },
        swiperEl: swiperEl ? {
          classes: swiperClasses,
          hasInitializedClass: swiperClasses ? swiperClasses.includes('swiper-initialized') : false,
          hasContainerInitClass: swiperClasses ? swiperClasses.includes('swiper-container-initialized') : false,
          tag: swiperEl.tagName,
        } : null,
        swiperApi: !!swiperApi,
        swiperParams,
        autoplayState,
        slidesCount: slides.length,
        wrapperInline: { transform: wrapperInlineTransform, transitionDuration: wrapperInlineTransition },
        firstSlideInline: firstSlide ? { transform: firstSlide.style.transform, width: firstSlide.style.width } : null,
        computed: {
          widget: summarizeStyle(widget, cssProps),
          swiperEl: summarizeStyle(swiperEl, cssProps),
          wrapper: summarizeStyle(wrapper, cssProps),
          firstSlide: summarizeStyle(firstSlide, cssProps),
        },
        elementFromPointAtCenter: elemAtPoint,
        matchingStylesheetRules: matchingRules,
        inlineStyleHits,
        handlerInfo,
        swiperGlobals,
        viewport: { width: window.innerWidth, height: window.innerHeight },
        userAgent: navigator.userAgent,
        readyState: document.readyState,
      };
    }, WIDGET_ID);
  } catch (e) {
    result.fatal = String(e && e.stack ? e.stack : e);
  } finally {
    await browser.close().catch(() => {});
  }

  return result;
}

(async () => {
  const out = {};
  out.desktop = await probe({ width: 1440, height: 900, deviceScaleFactor: 1, isMobile: false, hasTouch: false }, 'desktop-1440x900');
  out.mobile = await probe({ width: 390, height: 844, deviceScaleFactor: 3, isMobile: true, hasTouch: true }, 'mobile-iphone12');

  fs.writeFileSync(OUT_JSON, JSON.stringify(out, null, 2), 'utf8');
  console.log('WROTE', OUT_JSON);
  console.log('DESKTOP swiper-initialized?', out.desktop.inPageProbe && out.desktop.inPageProbe.swiperEl && out.desktop.inPageProbe.swiperEl.hasInitializedClass);
  console.log('MOBILE  swiper-initialized?', out.mobile.inPageProbe && out.mobile.inPageProbe.swiperEl && out.mobile.inPageProbe.swiperEl.hasInitializedClass);
})().catch(e => { console.error('FATAL', e); process.exit(1); });
