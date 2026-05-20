'use strict';
const puppeteer = require('C:/Users/Administrator/AppData/Local/Temp/node_modules/puppeteer');
(async () => {
  const browser = await puppeteer.launch({ executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe', headless:'new', args:['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });

  await page.evaluateOnNewDocument(() => {
    window.__inits = [];
    // Patch window.Swiper as a getter/setter so we wrap whatever assigns to it.
    let realSwiper = null;
    let wrapped = null;
    function makeWrapped(orig) {
      const W = function(el, opts){
        try {
          window.__inits.push({
            source: 'window.Swiper',
            ts: Date.now(),
            elClass: el && (el.className || (el[0] && el[0].className) || null),
            opts: opts ? JSON.parse(JSON.stringify(opts, (k,v) => typeof v === 'function' ? '[fn]' : v)) : null,
            stack: (new Error()).stack.split('\n').slice(0,10).join(' | '),
          });
        } catch(_) {}
        return new orig(el, opts);
      };
      W.prototype = orig.prototype;
      // Copy static props
      for (const k of Object.getOwnPropertyNames(orig)) {
        if (k !== 'length' && k !== 'name' && k !== 'prototype') {
          try { W[k] = orig[k]; } catch(_) {}
        }
      }
      W.__wrapped = true;
      return W;
    }
    Object.defineProperty(window, 'Swiper', {
      configurable: true,
      get() { return wrapped; },
      set(v) {
        if (v && !v.__wrapped) {
          realSwiper = v;
          wrapped = makeWrapped(v);
        } else {
          wrapped = v;
        }
      },
    });

    // Also patch elementorFrontend.utils.swiper later
    const poll = setInterval(() => {
      try {
        if (window.elementorFrontend && window.elementorFrontend.utils && window.elementorFrontend.utils.swiper) {
          const orig = window.elementorFrontend.utils.swiper;
          if (!orig.__patched) {
            const Wrapped = function(el, opts) {
              try {
                window.__inits.push({
                  source: 'elementorFrontend.utils.swiper',
                  ts: Date.now(),
                  elClass: el && (el.className || (el[0] && el[0].className) || (el.get && el.get(0) && el.get(0).className)) || null,
                  opts: opts ? JSON.parse(JSON.stringify(opts, (k,v) => typeof v === 'function' ? '[fn]' : v)) : null,
                  stack: (new Error()).stack.split('\n').slice(0,10).join(' | '),
                });
              } catch (_) {}
              return new orig(el, opts);
            };
            Wrapped.prototype = orig.prototype;
            Wrapped.__patched = true;
            window.elementorFrontend.utils.swiper = Wrapped;
          }
        }
      } catch (_) {}
    }, 30);
    setTimeout(() => clearInterval(poll), 8000);
  });

  await page.goto('https://suriota.com/', { waitUntil:'networkidle2', timeout: 60000 });
  await new Promise(r=>setTimeout(r,6000));

  const inits = await page.evaluate(() => window.__inits || []);
  console.log('TOTAL SWIPER CALLS:', inits.length);
  inits.forEach((i, n) => {
    console.log('---#'+n+' SRC:'+i.source+' EL:'+i.elClass);
    console.log('  speed:', i.opts && i.opts.speed, 'autoplay:', JSON.stringify(i.opts && i.opts.autoplay), 'slidesPerView:', i.opts && i.opts.slidesPerView);
    console.log('  stack:', i.stack);
  });

  // Now check live state
  const live = await page.evaluate(() => {
    const w = document.querySelector('.elementor-element-e396a55 .swiper');
    if (!w || !w.swiper) return null;
    return {
      speed: w.swiper.params.speed,
      autoplay: w.swiper.params.autoplay,
      destroyed: w.swiper.destroyed,
    };
  });
  console.log('LIVE STATE:', JSON.stringify(live));

  await browser.close();
})().catch(e=>{console.error(e);process.exit(1);});
