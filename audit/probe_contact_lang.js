const puppeteer = require('C:/Users/Administrator/AppData/Local/Temp/node_modules/puppeteer');
(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    headless: 'new',
    args: ['--no-sandbox'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });
  await page.goto('https://suriota.com/contact/', { waitUntil: 'networkidle2', timeout: 45000 });
  await new Promise(r => setTimeout(r, 1500));
  const info = await page.evaluate(() => {
    const forms = Array.from(document.querySelectorAll('form'));
    const formData = forms.map(f => ({
      id: f.id, cls: f.className,
      action: f.getAttribute('action'),
      method: f.getAttribute('method'),
      inputs: Array.from(f.querySelectorAll('input,textarea,select')).map(i => ({ name: i.name, type: i.type })),
      hasRecaptcha: !!f.querySelector('.g-recaptcha, [data-sitekey]') || !!document.querySelector('.grecaptcha-badge'),
    }));
    const candidates = [];
    document.querySelectorAll('a[hreflang], .lang-item, [class*="polylang"], [class*="pll-"], [class*="language"], .wpml-ls a').forEach(el => {
      candidates.push({ tag: el.tagName, cls: el.className, href: el.href || (el.querySelector && el.querySelector('a') ? el.querySelector('a').href : null) });
    });
    return { formData, langCandidates: candidates.slice(0, 20) };
  });
  console.log(JSON.stringify(info, null, 2));
  await browser.close();
})();
