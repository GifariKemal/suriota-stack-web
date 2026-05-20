'use strict';
const puppeteer = require('C:/Users/Administrator/AppData/Local/Temp/node_modules/puppeteer');
const fs = require('fs');
(async () => {
  const browser = await puppeteer.launch({ executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe', headless:'new', args:['--no-sandbox'] });
  const page = await browser.newPage();
  await page.goto('https://suriota.com/', { waitUntil:'domcontentloaded' });
  const txt = await page.evaluate(async () => {
    const r = await fetch('/wp-content/cache/wpo-minify/1779207331/assets/wpo-minify-footer-0667255a.min.js');
    return r.text();
  });
  fs.writeFileSync('C:/Users/Administrator/Music/Website Suriota/audit/wpo_footer_0667255a.js', txt, 'utf8');
  console.log('LEN', txt.length);
  // Find SwiperHandler class
  const needles = ['SwiperHandler','createSwiperInstance','new Swiper(','class SwiperHandler'];
  for (const n of needles) {
    let i = -1;
    while ((i = txt.indexOf(n, i+1)) !== -1) {
      console.log('FOUND', n, 'at', i);
      console.log(txt.slice(Math.max(0,i-30), i + 500).replace(/\n/g,' '));
      console.log('---');
    }
  }
  await browser.close();
})().catch(e=>{console.error(e);process.exit(1);});
