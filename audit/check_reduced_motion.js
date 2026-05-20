'use strict';
const puppeteer = require('C:/Users/Administrator/AppData/Local/Temp/node_modules/puppeteer');
(async () => {
  const browser = await puppeteer.launch({ executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe', headless:'new', args:['--no-sandbox'] });
  // Test 1: default (Puppeteer headless often reports reduce)
  let page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });
  await page.goto('https://suriota.com/', { waitUntil: 'domcontentloaded' });
  const r1 = await page.evaluate(() => ({
    reduce: window.matchMedia('(prefers-reduced-motion: reduce)').matches,
    noPref: window.matchMedia('(prefers-reduced-motion: no-preference)').matches,
  }));
  console.log('DEFAULT headless:', r1);

  // Test 2: emulate "no-preference"
  await page.emulateMediaFeatures([{ name: 'prefers-reduced-motion', value: 'no-preference' }]);
  await page.reload({ waitUntil: 'networkidle2' });
  await new Promise(r => setTimeout(r, 4500));
  const r2 = await page.evaluate(() => {
    const w = document.querySelector('.elementor-element-e396a55 .swiper');
    return {
      reduceMatches: window.matchMedia('(prefers-reduced-motion: reduce)').matches,
      noPrefMatches: window.matchMedia('(prefers-reduced-motion: no-preference)').matches,
      swiperSpeed: w && w.swiper && w.swiper.params.speed,
      autoplayEnabled: w && w.swiper && w.swiper.params.autoplay && w.swiper.params.autoplay.enabled,
      autoplayRunning: w && w.swiper && w.swiper.autoplay && w.swiper.autoplay.running,
    };
  });
  console.log('EMULATED no-preference + reload:', r2);

  // Wait and check if wrapper actually moves now
  const before = await page.evaluate(() => document.querySelector('.elementor-element-e396a55 .swiper-wrapper').style.transform);
  await new Promise(r => setTimeout(r, 5500));
  const after = await page.evaluate(() => document.querySelector('.elementor-element-e396a55 .swiper-wrapper').style.transform);
  console.log('TRANSFORM before/after 5s:', before, '|', after);

  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
