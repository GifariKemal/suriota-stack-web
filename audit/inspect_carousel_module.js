'use strict';
const puppeteer = require('C:/Users/Administrator/AppData/Local/Temp/node_modules/puppeteer');
const fs = require('fs');
(async () => {
  const browser = await puppeteer.launch({ executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe', headless:'new', args:['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });

  await page.goto('https://suriota.com/', { waitUntil:'networkidle2', timeout: 60000 });
  await new Promise(r => setTimeout(r, 4000));

  // 1. Pull the carousel's full module instance via Elementor's elementsHandler
  const inspect = await page.evaluate(() => {
    const widget = document.querySelector('.elementor-element-e396a55');
    if (!widget) return { error:'no widget' };

    // Try to grab the module instance the Elementor frontend keeps for the widget
    const ef = window.elementorFrontend;
    let handlerInstance = null;
    try {
      // jQuery data is where Elementor stashes handler refs in older versions; newer uses Backbone-style
      const $ = window.jQuery;
      if ($) {
        const $w = $(widget);
        // Get all data keys
        handlerInstance = {
          dataKeys: Object.keys($w.data() || {}),
          dataSettings: $w.data('settings'),
          elementorSettings: $w.data('elementor-settings'),
        };
      }
    } catch (e) {
      handlerInstance = { jqErr: String(e) };
    }

    const swiperEl = widget.querySelector('.swiper');
    const api = swiperEl && swiperEl.swiper;
    let allParams = null;
    if (api) {
      // capture full params object — what was actually passed to Swiper constructor
      try {
        const p = api.params;
        const flat = {};
        for (const k of Object.keys(p)) {
          const v = p[k];
          if (v === null || typeof v !== 'object') flat[k] = v;
          else if (Array.isArray(v)) flat[k] = '[array:'+v.length+']';
          else flat[k] = (function(){ const o={}; for (const kk of Object.keys(v)) { const vv=v[kk]; if (vv===null||typeof vv!=='object') o[kk]=vv; else o[kk]='[obj]'; } return o; })();
        }
        allParams = flat;
      } catch (e) { allParams = { err:String(e) }; }
    }

    // Try to start autoplay manually and see if it sticks
    let manualStart = null;
    if (api && api.autoplay) {
      try {
        const before = { running: api.autoplay.running, paused: api.autoplay.paused, enabled: api.params.autoplay && api.params.autoplay.enabled };
        api.params.autoplay = Object.assign({}, api.params.autoplay, { enabled:true, delay: 3000, disableOnInteraction:false });
        api.params.speed = 800;
        if (typeof api.autoplay.start === 'function') api.autoplay.start();
        manualStart = { before, after: { running: api.autoplay.running, paused: api.autoplay.paused, enabled: api.params.autoplay && api.params.autoplay.enabled }, speed: api.params.speed };
      } catch (e) { manualStart = { err: String(e) }; }
    }

    return {
      handlerData: handlerInstance,
      allParams,
      manualStart,
      slideToBefore: api ? api.realIndex : null,
    };
  });

  // 2. Wait 6 seconds, see if manual autoplay actually moves the wrapper
  await new Promise(r => setTimeout(r, 6500));
  const after = await page.evaluate(() => {
    const swiperEl = document.querySelector('.elementor-element-e396a55 .swiper');
    const api = swiperEl && swiperEl.swiper;
    const wrapper = document.querySelector('.elementor-element-e396a55 .swiper-wrapper');
    return {
      realIndex: api && api.realIndex,
      transform: wrapper && wrapper.style.transform,
      autoplayRunning: api && api.autoplay && api.autoplay.running,
    };
  });

  // 3. Fetch the carousel bundle and look at how settings are mapped
  const carouselBundle = await page.evaluate(async () => {
    const r = await fetch('/wp-content/plugins/elementor/assets/js/image-carousel.6167d20b95b33386757b.bundle.min.js');
    const txt = await r.text();
    return { len: txt.length, snippet: txt.slice(0, 3500) };
  });

  console.log(JSON.stringify({ inspect, after, carouselBundleLen: carouselBundle.len }, null, 2));
  fs.writeFileSync('C:/Users/Administrator/Music/Website Suriota/audit/carousel_bundle_snippet.js', carouselBundle.snippet, 'utf8');

  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
