const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  for (const url of ['https://suriota.com/', 'https://suriota.com/about-us/']) {
    await page.goto(url, {waitUntil:'networkidle2'});
    const el = await page.$('.entry-title');
    if (el) {
      const style = await page.evaluate(e => window.getComputedStyle(e).display, el);
      const text = await page.evaluate(e => e.innerText, el);
      console.log(url + ' .entry-title display: ' + style + ' text: "' + text + '"');
    } else {
      console.log(url + ' no .entry-title');
    }
  }
  await browser.close();
})();
