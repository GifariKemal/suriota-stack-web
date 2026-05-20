const puppeteer = require('puppeteer');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
(async () => {
  const browser = await puppeteer.launch({ headless: 'new', executablePath: CHROME, args: ['--no-sandbox'] });
  const urls = ['https://suriota.com/', 'https://suriota.com/id/', 'https://suriota.com/shouye/', 'https://suriota.com/about-us/', 'https://suriota.com/contact/'];
  for (const url of urls) {
    const page = await browser.newPage();
    const errs = [];
    page.on('pageerror', e => errs.push(e.message.slice(0,160)));
    page.on('console', m => { if (m.type()==='error') errs.push('CONSOLE: '+m.text().slice(0,160)); });
    try {
      await page.goto(url + '?cb=' + Date.now(), { waitUntil: 'networkidle2', timeout: 45000 });
    } catch(e){ errs.push('NAV-FAIL: '+e.message.slice(0,100)); }
    console.log(`${url}  →  ${errs.length} errors`);
    errs.forEach(e => console.log('  - ' + e));
    await page.close();
  }
  await browser.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });
