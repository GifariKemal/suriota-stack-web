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
    const navLinks = Array.from(document.querySelectorAll('header a[href], nav a[href]'))
      .map(a => ({ href: a.href, text: a.innerText.trim().slice(0,40) }))
      .filter(l => l.href && !l.href.startsWith('javascript:'));
    return navLinks;
  });
  console.log(JSON.stringify(info, null, 2));
  await browser.close();
})();
