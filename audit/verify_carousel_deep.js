const puppeteer = require('puppeteer');
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
(async () => {
  const browser = await puppeteer.launch({ headless: 'new', executablePath: CHROME, args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });
  await page.emulateMediaFeatures([{ name: 'prefers-reduced-motion', value: 'reduce' }]);

  await page.goto('https://suriota.com/?cb=' + Date.now(), { waitUntil: 'networkidle2', timeout: 60000 });
  await page.waitForSelector('.elementor-element-e396a55 .swiper');

  // Wait long enough for snippets to register
  await new Promise(r => setTimeout(r, 4000));

  const probe = await page.evaluate(() => {
    const el = document.querySelector('.elementor-element-e396a55 .swiper');
    if (!el) return { error: 'no .swiper found' };
    const s = el.swiper;
    return {
      snippet_5513_present: !!document.getElementById('sx-carousel-manual-marquee'),
      snippet_5512_present: !!document.getElementById('sx-carousel-motion-optout'),
      snippet_5511_present: !!document.getElementById('sx-document-body-guard'),
      timer_attached: !!el._sxTimer,
      swiper_exists: !!s,
      slideNext_exists: s && typeof s.slideNext === 'function',
      slideNext_locked: s ? s.allowSlideNext : null,
      progress: s ? s.progress : null,
      activeIndex: s ? s.activeIndex : null,
      params_speed: s ? s.params.speed : null,
      params_autoplay_enabled: s && s.params.autoplay ? s.params.autoplay.enabled : null,
      autoplay_running: s && s.autoplay ? s.autoplay.running : null
    };
  });
  console.log('PROBE:', JSON.stringify(probe, null, 2));

  // Manually call slideNext to see if it works at all
  const manualResult = await page.evaluate(() => {
    const el = document.querySelector('.elementor-element-e396a55 .swiper');
    const wrapperBefore = el.querySelector('.swiper-wrapper').style.transform;
    el.swiper.slideNext();
    return new Promise(resolve => {
      setTimeout(() => {
        const wrapperAfter = el.querySelector('.swiper-wrapper').style.transform;
        resolve({ before: wrapperBefore, after: wrapperAfter, changed: wrapperBefore !== wrapperAfter });
      }, 1500);
    });
  });
  console.log('\nManual slideNext result:', JSON.stringify(manualResult, null, 2));

  await browser.close();
})().catch(e => { console.error('FATAL', e.message); process.exit(1); });
