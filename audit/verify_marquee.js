const puppeteer = require('puppeteer');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
(async () => {
  const browser = await puppeteer.launch({ headless: 'new', executablePath: CHROME, args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });
  await page.emulateMediaFeatures([{ name: 'prefers-reduced-motion', value: 'reduce' }]);
  await page.goto('https://suriota.com/?cb=' + Date.now(), { waitUntil: 'networkidle2', timeout: 60000 });
  await page.waitForSelector('.elementor-element-e396a55');
  await new Promise(r => setTimeout(r, 4000));

  const probe = await page.evaluate(() => {
    const w = document.querySelector('.elementor-element-e396a55');
    const wrap = w ? w.querySelector('.swiper-wrapper') : null;
    if (!w || !wrap) return { error: 'not found' };
    const cs = getComputedStyle(wrap);
    return {
      marquee_applied: w.dataset.sxMarquee === '1',
      slide_count: wrap.querySelectorAll('.swiper-slide').length,
      animation: cs.animationName + ' ' + cs.animationDuration + ' ' + cs.animationTimingFunction + ' ' + cs.animationIterationCount,
      transform_at_0s: cs.transform
    };
  });
  console.log('AT t=0s:', JSON.stringify(probe, null, 2));

  await new Promise(r => setTimeout(r, 3000));
  const after = await page.evaluate(() => {
    const wrap = document.querySelector('.elementor-element-e396a55 .swiper-wrapper');
    return getComputedStyle(wrap).transform;
  });
  console.log('\nAT t=3s, transform:', after);
  console.log('Transform changed?', probe.transform_at_0s !== after);

  await browser.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });
