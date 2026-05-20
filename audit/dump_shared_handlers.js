'use strict';
const puppeteer = require('C:/Users/Administrator/AppData/Local/Temp/node_modules/puppeteer');
const fs = require('fs');
(async () => {
  const browser = await puppeteer.launch({ executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe', headless:'new', args:['--no-sandbox'] });
  const page = await browser.newPage();
  await page.goto('https://suriota.com/', { waitUntil:'domcontentloaded' });
  const out = await page.evaluate(async () => {
    const r = await fetch('/wp-content/plugins/elementor/assets/js/shared-frontend-handlers.03caa53373b56d3bab67.bundle.min.js');
    return r.text();
  });
  fs.writeFileSync('C:/Users/Administrator/Music/Website Suriota/audit/shared_handlers.js', out, 'utf8');
  // Find autoplay-related substrings
  const hits = [];
  const needles = ['getSwiperSettings','autoplay','autoplay_speed','autoplay:"yes"','"yes"','disableOnInteraction','pauseOnHover','pause_on_hover','pause_on_interaction'];
  for (const n of needles) {
    let i = -1;
    while ((i = out.indexOf(n, i+1)) !== -1) hits.push({ needle: n, at: i, snippet: out.slice(Math.max(0,i-80), i+200).replace(/\n/g,' ') });
    if (hits.length > 60) break;
  }
  console.log('LEN:', out.length);
  hits.forEach(h => console.log(h.at, h.needle, '||', h.snippet));
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
