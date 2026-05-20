// Capture the full pageerror stack from suriota.com
'use strict';
const puppeteer = require('C:/Users/Administrator/AppData/Local/Temp/node_modules/puppeteer');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';

(async () => {
  const browser = await puppeteer.launch({ executablePath: CHROME, headless: 'new', args:['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });
  const errs = [];
  page.on('pageerror', e => errs.push({ msg: e.message, stack: e.stack }));
  // Also hook the CDP layer for uncaught exceptions
  const cdp = await page.target().createCDPSession();
  await cdp.send('Runtime.enable');
  const cdpErrs = [];
  cdp.on('Runtime.exceptionThrown', evt => cdpErrs.push(evt.exceptionDetails));
  await page.goto('https://suriota.com/', { waitUntil: 'networkidle2', timeout: 60000 });
  await new Promise(r => setTimeout(r, 4000));
  console.log('PAGEERRORS:', JSON.stringify(errs, null, 2));
  console.log('--- CDP EXCEPTIONS (first 5) ---');
  cdpErrs.slice(0,5).forEach((e,i) => {
    console.log('#'+i, e.text, '|', e.exception && e.exception.description ? e.exception.description.slice(0,800) : JSON.stringify(e).slice(0,800));
  });
  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
