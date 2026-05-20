'use strict';
const puppeteer = require('C:/Users/Administrator/AppData/Local/Temp/node_modules/puppeteer');
(async () => {
  const browser = await puppeteer.launch({ executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe', headless:'new', args:['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });
  await page.goto('https://suriota.com/', { waitUntil:'networkidle2', timeout: 60000 });
  await new Promise(r=>setTimeout(r,4000));
  const out = await page.evaluate(() => {
    const widget = document.querySelector('.elementor-element-e396a55');
    const ef = window.elementorFrontend;
    const $ = window.jQuery;
    const $w = $(widget);
    const handlersOnEl = $w.data('elementorElementType') || null;

    // Look at all stored data keys with values
    const allData = $w.data() || {};
    const summary = {};
    for (const k of Object.keys(allData)) {
      const v = allData[k];
      if (v && typeof v === 'object' && v.constructor === Object) summary[k] = v;
      else if (typeof v !== 'object') summary[k] = v;
      else summary[k] = '[' + (v && v.constructor && v.constructor.name) + ']';
    }

    // Locate the actual handler instance: elementorFrontend.elementsHandler.elementsHandlers
    const eh = ef.elementsHandler;
    let handlerInstanceFound = null;
    let allRunningInstances = [];
    try {
      // Try iterating $w jquery data for our handler
      for (const k of Object.keys(allData)) {
        const v = allData[k];
        if (v && typeof v === 'object' && v.constructor && v.constructor.name && /Carousel/i.test(v.constructor.name)) {
          allRunningInstances.push({
            dataKey: k,
            className: v.constructor.name,
            elementSettings: v.getElementSettings ? v.getElementSettings() : null,
            swiperSettings: v.getSwiperSettings ? (function(){ try { return v.getSwiperSettings(); } catch(e){ return {err:String(e)}; } })() : null,
          });
        }
      }
    } catch (e) {
      allRunningInstances.push({ err: String(e) });
    }

    return {
      dataKeys: Object.keys(allData),
      summary,
      runningCarouselHandlers: allRunningInstances,
    };
  });
  console.log(JSON.stringify(out, null, 2));
  await browser.close();
})().catch(e=>{console.error(e);process.exit(1);});
