const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });
  
  const url = 'https://suriota.com/hybrid-pju-menggunakan-plts-dan-pltb-berbasis-iot/';
  await page.goto(url, { waitUntil: 'networkidle2' });
  
  const outputDir = path.join(__dirname, 'screenshots', '2026-05-18-portfolio-post');
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });
  
  // Get page height
  const pageHeight = await page.evaluate(() => document.body.scrollHeight);
  console.log('Page height:', pageHeight);
  
  // Take screenshots at different scroll positions
  const layers = [
    { name: 'layer-01-hero', scroll: 0 },
    { name: 'layer-02-intro-toc', scroll: 850 },
    { name: 'layer-03-content-1', scroll: 2400 },
    { name: 'layer-04-content-2', scroll: 4200 },
    { name: 'layer-05-content-3', scroll: 6000 },
    { name: 'layer-06-content-4', scroll: 7800 },
    { name: 'layer-07-cta-comment', scroll: 9600 },
    { name: 'layer-08-footer', scroll: pageHeight - 900 }
  ];
  
  for (const layer of layers) {
    await page.evaluate((scrollY) => window.scrollTo(0, scrollY), layer.scroll);
    await new Promise(r => setTimeout(r, 500));
    const filePath = path.join(outputDir, `${layer.name}.png`);
    await page.screenshot({ path: filePath, fullPage: false });
    console.log(`Saved: ${filePath}`);
  }
  
  await browser.close();
  console.log('All screenshots saved!');
})();
