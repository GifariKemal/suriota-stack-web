const puppeteer = require('puppeteer');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
(async () => {
  const browser = await puppeteer.launch({ headless: 'new', executablePath: CHROME, args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });
  await page.emulateMediaFeatures([{ name: 'prefers-reduced-motion', value: 'reduce' }]);
  await page.goto('https://suriota.com/?cb=' + Date.now(), { waitUntil: 'networkidle2', timeout: 60000 });
  await page.waitForSelector('.elementor-element-e396a55 .swiper');

  const samples = [];
  for (let i = 0; i < 8; i++) {
    await new Promise(r => setTimeout(r, 2000));
    const t = await page.evaluate(() => {
      const el = document.querySelector('.elementor-element-e396a55 .swiper');
      return el && el.swiper ? { idx: el.swiper.activeIndex, real: el.swiper.realIndex, prog: +el.swiper.progress.toFixed(3) } : null;
    });
    samples.push(t);
    console.log(`t=${(i+1)*2}s  idx=${t.idx}  real=${t.real}  progress=${t.prog}`);
  }
  const moved = new Set(samples.map(s => s.idx)).size > 1;
  console.log(`\nCarousel moving over 16s? ${moved ? 'YES ✓' : 'NO ✗'}`);
  await browser.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });
