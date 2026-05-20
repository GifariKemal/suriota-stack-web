const puppeteer = require('C:/Users/Administrator/AppData/Local/Temp/node_modules/puppeteer');
(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new',
    args: ['--no-sandbox'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });
  await page.goto('https://suriota.com/', { waitUntil: 'networkidle2', timeout: 45000 });
  await new Promise(r => setTimeout(r, 1500));
  const info = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('form')).map(f => ({
      id: f.id, cls: f.className,
      action: f.getAttribute('action'),
      method: f.getAttribute('method'),
      inputCount: f.querySelectorAll('input,textarea,select').length,
      inputNames: Array.from(f.querySelectorAll('input,textarea,select')).map(i => i.name + ':' + i.type),
    }));
  });
  console.log(JSON.stringify(info, null, 2));
  await browser.close();
})();
