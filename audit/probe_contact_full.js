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
    // Look for contact-form-7, gravity, wpforms, elementor, fluent
    const cf7 = !!document.querySelector('.wpcf7-form, .wpcf7');
    const grav = !!document.querySelector('.gform_wrapper, .gform_form');
    const wp  = !!document.querySelector('.wpforms-form');
    const ele = !!document.querySelector('.elementor-form');
    const fluent = !!document.querySelector('.fluentform');
    const ninja = !!document.querySelector('.nf-form-cont');
    // mailto / phone links
    const mailto = Array.from(document.querySelectorAll('a[href^="mailto:"]')).map(a => a.href);
    const tel    = Array.from(document.querySelectorAll('a[href^="tel:"], a[href*="wa.me"], a[href*="api.whatsapp"]')).map(a => a.href);
    // Headlines
    const h1 = Array.from(document.querySelectorAll('h1')).map(h => h.innerText.trim()).slice(0,5);
    // text body length
    const bodyText = document.body.innerText.length;
    // language switcher (broader)
    const langs = Array.from(document.querySelectorAll('a[hreflang]')).map(a => ({ href: a.href, lang: a.getAttribute('hreflang'), text: a.innerText.trim() }));
    // hreflang links in <head>
    const hreflangsHead = Array.from(document.querySelectorAll('link[rel="alternate"][hreflang]')).map(l => ({ href: l.href, lang: l.getAttribute('hreflang') }));
    return { cf7, grav, wp, ele, fluent, ninja, mailto, tel, h1, bodyText, langs, hreflangsHead };
  });
  console.log(JSON.stringify(info, null, 2));
  await browser.close();
})();
