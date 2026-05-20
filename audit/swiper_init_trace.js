'use strict';
const puppeteer = require('C:/Users/Administrator/AppData/Local/Temp/node_modules/puppeteer');
(async () => {
  const browser = await puppeteer.launch({ executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe', headless:'new', args:['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });

  // Inject a Swiper constructor proxy BEFORE Elementor's modules run.
  await page.evaluateOnNewDocument(() => {
    window.__swiperInits = [];
    // Wait for Swiper to be defined then wrap
    let realSwiper = null;
    let wrapped = false;
    Object.defineProperty(window, 'Swiper', {
      configurable: true,
      get() { return realSwiper && wrappedCtor; },
      set(v) {
        realSwiper = v;
      },
    });
    function wrappedCtor() { /* placeholder */ }
    // Easier: poll
    const poll = setInterval(() => {
      try {
        if (window.elementorFrontend && window.elementorFrontend.utils && window.elementorFrontend.utils.swiper) {
          const orig = window.elementorFrontend.utils.swiper;
          if (!orig.__patched) {
            const Wrapped = function(el, opts) {
              try {
                window.__swiperInits.push({
                  ts: Date.now(),
                  elClass: el && (el.className || (el[0] && el[0].className) || (el.get && el.get(0) && el.get(0).className)) || null,
                  opts: opts ? JSON.parse(JSON.stringify(opts, (k,v) => typeof v === 'function' ? '[fn]' : v)) : null,
                  stack: (new Error()).stack,
                });
              } catch (e) { window.__swiperInits.push({ err:String(e) }); }
              return new orig(el, opts);
            };
            Wrapped.prototype = orig.prototype;
            Wrapped.__patched = true;
            window.elementorFrontend.utils.swiper = Wrapped;
          }
          clearInterval(poll);
        }
      } catch (_) {}
    }, 30);
    setTimeout(() => clearInterval(poll), 8000);
  });

  await page.goto('https://suriota.com/', { waitUntil:'networkidle2', timeout: 60000 });
  await new Promise(r=>setTimeout(r,5000));
  const inits = await page.evaluate(() => window.__swiperInits || []);
  console.log('SWIPER INITS via elementorFrontend.utils.swiper:', inits.length);
  inits.forEach((i, n) => {
    console.log('--- #' + n + ' elClass:', i.elClass);
    console.log('opts keys:', i.opts ? Object.keys(i.opts) : null);
    if (i.opts) {
      console.log('  speed:', i.opts.speed, 'autoplay:', JSON.stringify(i.opts.autoplay), 'slidesPerView:', i.opts.slidesPerView, 'loop:', i.opts.loop);
      console.log('  full:', JSON.stringify(i.opts).slice(0, 1200));
    }
    if (i.stack) console.log('  stack:', i.stack.split('\n').slice(0,5).join(' | '));
  });
  await browser.close();
})().catch(e=>{console.error(e);process.exit(1);});
