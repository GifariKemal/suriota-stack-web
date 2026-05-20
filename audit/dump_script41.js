'use strict';
const puppeteer = require('C:/Users/Administrator/AppData/Local/Temp/node_modules/puppeteer');
const fs = require('fs');
(async () => {
  const browser = await puppeteer.launch({ executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe', headless:'new', args:['--no-sandbox']});
  const page = await browser.newPage();
  await page.goto('https://suriota.com/', { waitUntil:'domcontentloaded' });
  const html = await page.content();
  fs.writeFileSync('C:/Users/Administrator/Music/Website Suriota/audit/suriota_home.html', html, 'utf8');
  const lines = html.split('\n');
  console.log('TOTAL LINES:', lines.length);
  for (let i = 38; i < 46 && i < lines.length; i++) {
    console.log('--- LINE ' + (i+1) + ' (len=' + lines[i].length + ') ---');
    console.log(lines[i].slice(0, 1500));
  }
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
