const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'] });
  
  // DESKTOP WITH HOVER
  const page1 = await browser.newPage();
  await page1.setViewport({ width: 1440, height: 900 });
  await page1.goto('https://suriota.com', { waitUntil: 'networkidle2', timeout: 30000 });
  await new Promise(r => setTimeout(r, 3000));
  
  await page1.screenshot({ path: 'screenshots/check-desktop-before-hover.png', fullPage: false });
  
  // Hover over Our Services
  await page1.hover('button.sx-hf-dropbtn');
  await new Promise(r => setTimeout(r, 800));
  await page1.screenshot({ path: 'screenshots/check-desktop-services-hover.png', fullPage: false });
  
  // Hover over Product
  const dropdowns = await page1.$$('button.sx-hf-dropbtn');
  if (dropdowns.length > 1) {
    await dropdowns[1].hover();
    await new Promise(r => setTimeout(r, 800));
    await page1.screenshot({ path: 'screenshots/check-desktop-product-hover.png', fullPage: false });
  }
  
  // Scroll to footer
  await page1.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await new Promise(r => setTimeout(r, 1000));
  await page1.screenshot({ path: 'screenshots/check-desktop-footer.png', fullPage: false });
  
  // MOBILE
  const page2 = await browser.newPage();
  await page2.setViewport({ width: 375, height: 812 });
  await page2.goto('https://suriota.com', { waitUntil: 'networkidle2', timeout: 30000 });
  await new Promise(r => setTimeout(r, 3000));
  await page2.screenshot({ path: 'screenshots/check-mobile-initial.png', fullPage: false });
  
  // Click hamburger
  await page2.click('#sx-hf-toggle');
  await new Promise(r => setTimeout(r, 800));
  await page2.screenshot({ path: 'screenshots/check-mobile-menu-open.png', fullPage: false });
  
  // Click Our Services
  await page2.evaluate(() => {
    const links = document.querySelectorAll('button.sx-hf-dropbtn');
    if (links[0]) {
      links[0].click();
      links[0].parentElement.classList.add('open');
    }
  });
  await new Promise(r => setTimeout(r, 800));
  await page2.screenshot({ path: 'screenshots/check-mobile-services-click.png', fullPage: false });
  
  // Scroll to footer
  await page2.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await new Promise(r => setTimeout(r, 1000));
  await page2.screenshot({ path: 'screenshots/check-mobile-footer.png', fullPage: false });
  
  await browser.close();
  console.log('All screenshots saved!');
})();
