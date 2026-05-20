const puppeteer = require('puppeteer');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
(async () => {
  const browser = await puppeteer.launch({ headless: 'new', executablePath: CHROME, args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });
  await page.emulateMediaFeatures([{ name: 'prefers-reduced-motion', value: 'reduce' }]);

  await page.goto('https://suriota.com/?cb=' + Date.now(), { waitUntil: 'networkidle2', timeout: 60000 });
  await page.waitForSelector('.elementor-element-e396a55 .swiper');

  // Wait 5s for snippet to kick in
  await new Promise(r => setTimeout(r, 5000));

  const before = await page.evaluate(() => {
    const el = document.querySelector('.elementor-element-e396a55 .swiper');
    if (!el || !el.swiper) return null;
    const wrapper = el.querySelector('.swiper-wrapper');
    return {
      autoplay_enabled: el.swiper.autoplay && el.swiper.autoplay.enabled,
      autoplay_running: el.swiper.autoplay && el.swiper.autoplay.running,
      speed: el.swiper.params.speed,
      transform: wrapper ? wrapper.style.transform : null
    };
  });

  await new Promise(r => setTimeout(r, 5000));

  const after = await page.evaluate(() => {
    const el = document.querySelector('.elementor-element-e396a55 .swiper');
    if (!el || !el.swiper) return null;
    const wrapper = el.querySelector('.swiper-wrapper');
    return {
      transform: wrapper ? wrapper.style.transform : null
    };
  });

  console.log('=== After 5s wait (reduce-motion=reduce, desktop 1440x900) ===');
  console.log(JSON.stringify(before, null, 2));
  console.log('\n=== After +5s more (transform should have advanced) ===');
  console.log('transform:', after.transform);
  console.log('\nTransform changed (autoplay actually moving)?', before.transform !== after.transform);

  await browser.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });
