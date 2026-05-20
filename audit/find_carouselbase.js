'use strict';
const puppeteer = require('C:/Users/Administrator/AppData/Local/Temp/node_modules/puppeteer');
(async () => {
  const browser = await puppeteer.launch({ executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe', headless:'new', args:['--no-sandbox'] });
  const page = await browser.newPage();
  await page.goto('https://suriota.com/', { waitUntil:'networkidle2', timeout: 60000 });
  await new Promise(r=>setTimeout(r,4000));
  const out = await page.evaluate(() => {
    const CB = window.elementorModules && elementorModules.frontend && elementorModules.frontend.handlers && elementorModules.frontend.handlers.CarouselBase;
    if (!CB) return { found:false };
    // CarouselBase methods we need to inspect: getSwiperSettings (sometimes called buildSwiperConfig in newer versions)
    const proto = CB.prototype;
    const methods = Object.getOwnPropertyNames(proto);
    const result = { found:true, methods };
    for (const m of methods) {
      try {
        const fn = proto[m];
        if (typeof fn === 'function') {
          const src = fn.toString();
          if (src.length < 4000 && /autoplay|speed|swiper|getSwiperSettings|buildSwiperConfig/i.test(src)) {
            result[m] = src.slice(0, 3500);
          }
        }
      } catch (_) {}
    }
    return result;
  });
  console.log(JSON.stringify(out, null, 2));
  await browser.close();
})().catch(e=>{console.error(e);process.exit(1);});
