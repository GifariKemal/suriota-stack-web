// Sitewide audit for suriota.com
// Runs each URL at 1440x900 + 375x812, captures errors/network/visual diagnostics

const path = require('path');
const fs = require('fs');

const puppeteer = require('C:/Users/Administrator/AppData/Local/Temp/node_modules/puppeteer');

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const OUT = 'C:/Users/Administrator/Music/Website Suriota/audit/sitewide_audit.json';

const PAGES = [
  // Tier 1
  { url: 'https://suriota.com/',                              name: 'EN-home',     tier: 1 },
  { url: 'https://suriota.com/id/',                           name: 'ID-home',     tier: 1 },
  { url: 'https://suriota.com/shouye/',                       name: 'ZH-home',     tier: 1 },
  { url: 'https://suriota.com/about-us/',                     name: 'About',       tier: 1 },
  { url: 'https://suriota.com/portfolio/',                    name: 'Portfolio',   tier: 1 },
  { url: 'https://suriota.com/contact/',                      name: 'Contact',     tier: 1 },
  // Tier 2
  { url: 'https://suriota.com/electrical-services/',          name: 'Electrical',  tier: 2 },
  { url: 'https://suriota.com/automation-services/',          name: 'Automation',  tier: 2 },
  { url: 'https://suriota.com/renewable-energy-services/',    name: 'Renewable',   tier: 2 },
  { url: 'https://suriota.com/water-treatment-services/',     name: 'WaterTreat',  tier: 2 },
  // Tier 3
  { url: 'https://suriota.com/suriota-modbus-gateway/',       name: 'ModbusGW',    tier: 3 },
  { url: 'https://suriota.com/iso-m485-series/',              name: 'ISO-M485',    tier: 3 },
  { url: 'https://suriota.com/thm-30md/',                     name: 'THM-30MD',    tier: 3 },
  { url: 'https://suriota.com/pm1611-wd/',                    name: 'PM1611-WD',   tier: 3 },
  { url: 'https://suriota.com/rs-485-surge-protector-spd-t485-105/', name: 'SPD-T485', tier: 3 },
  { url: 'https://suriota.com/waste-water-loger/',            name: 'WasteLogger', tier: 3 },
  // Tier 4
  { url: 'https://suriota.com/surge-energy-mapping/',         name: 'SURGE-Energy', tier: 4 },
  { url: 'https://suriota.com/surge-vessel-tracking/',        name: 'SURGE-Vessel', tier: 4 },
  { url: 'https://suriota.com/surge-water-analytic/',         name: 'SURGE-Water',  tier: 4 },
];

const VIEWPORTS = [
  { name: 'desktop', width: 1440, height: 900 },
  { name: 'mobile',  width: 375,  height: 812, isMobile: true, hasTouch: true },
];

async function auditPage(browser, target) {
  const result = {
    name: target.name,
    url: target.url,
    tier: target.tier,
    status: null,
    title: null,
    pageErrors: [],
    consoleErrors: [],
    requestFailed: [],
    forms: 0,
    submitButtons: 0,
    visibleLinks: 0,
    brokenHrefStubs: 0,
    brokenImages: 0,
    brokenImageList: [],
    hasCarouselWidget: false,
    reduceMotionActive: null,
    bodyOverflowX: { desktop: false, mobile: false },
    langSwitcherCount: 0,
    langSwitcherLinks: [],
    // contact-specific
    contactForm: null,
  };

  for (const vp of VIEWPORTS) {
    const page = await browser.newPage();
    await page.setViewport({ width: vp.width, height: vp.height, isMobile: !!vp.isMobile, hasTouch: !!vp.hasTouch });
    if (vp.isMobile) {
      await page.setUserAgent('Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1');
    }

    page.on('pageerror', e => result.pageErrors.push(`[${vp.name}] ${e.message}`));
    page.on('console', m => { if (m.type() === 'error') result.consoleErrors.push(`[${vp.name}] ${m.text().slice(0,300)}`); });
    page.on('requestfailed', r => {
      const f = r.failure();
      result.requestFailed.push(`[${vp.name}] ${r.url()} :: ${f ? f.errorText : 'unknown'}`);
    });

    let response = null;
    try {
      response = await page.goto(target.url, { waitUntil: 'networkidle2', timeout: 45000 });
    } catch (e) {
      result.pageErrors.push(`[${vp.name}] NAV: ${e.message}`);
    }

    if (vp.name === 'desktop' && response) {
      result.status = response.status();
    }

    // Wait a moment for lazy/swiper init
    await new Promise(r => setTimeout(r, 1500));

    // Probe DOM
    let probe = null;
    try {
      probe = await page.evaluate(() => {
        const out = {};
        out.title = document.title;
        out.forms = document.querySelectorAll('form').length;
        out.submitButtons = document.querySelectorAll('form button[type=submit], form input[type=submit]').length;
        const links = Array.from(document.querySelectorAll('a[href]'));
        out.visibleLinks = links.filter(a => a.offsetParent !== null).length;
        out.brokenHrefStubs = links.filter(a => {
          const h = (a.getAttribute('href') || '').trim();
          return h === '' || h === '#';
        }).length;

        const imgs = Array.from(document.querySelectorAll('img'));
        const broken = imgs.filter(i => i.complete && i.naturalWidth === 0).map(i => (i.currentSrc || i.src || '').slice(-120));
        out.brokenImages = broken.length;
        out.brokenImageList = broken.slice(0, 6);

        out.hasCarouselWidget = !!document.querySelector('.elementor-widget-image-carousel, .swiper');
        out.reduceMotionActive = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        const html = document.documentElement;
        const body = document.body;
        out.overflowX = (body.scrollWidth - body.clientWidth) > 2 || (html.scrollWidth - html.clientWidth) > 2;

        // language switcher: Polylang renders .lang-item or .pll-switcher
        const langs = Array.from(document.querySelectorAll('.lang-item a, .pll-switcher a, ul.lang-switcher a, .pll-parent-menu-item a'));
        out.langSwitcherCount = langs.length;
        out.langSwitcherLinks = langs.slice(0, 5).map(a => a.href);

        // contact form info
        const cf = document.querySelector('form.wpcf7-form, form.elementor-form, form#contact-form, form');
        if (cf) {
          out.contactForm = {
            action: cf.getAttribute('action') || '(no action attr)',
            method: cf.getAttribute('method') || 'get',
            hasRecaptcha: !!document.querySelector('.g-recaptcha, .grecaptcha-badge, [data-sitekey]'),
            hasHoneypot: !!cf.querySelector('input[name*="honeypot"], input[name*="_honey"]'),
            inputCount: cf.querySelectorAll('input,textarea,select').length,
          };
        }
        return out;
      });
    } catch (e) {
      result.pageErrors.push(`[${vp.name}] PROBE: ${e.message}`);
    }

    if (probe) {
      if (vp.name === 'desktop') {
        result.title = probe.title;
        result.forms = probe.forms;
        result.submitButtons = probe.submitButtons;
        result.visibleLinks = probe.visibleLinks;
        result.brokenHrefStubs = probe.brokenHrefStubs;
        result.brokenImages = probe.brokenImages;
        result.brokenImageList = probe.brokenImageList;
        result.hasCarouselWidget = probe.hasCarouselWidget;
        result.reduceMotionActive = probe.reduceMotionActive;
        result.langSwitcherCount = probe.langSwitcherCount;
        result.langSwitcherLinks = probe.langSwitcherLinks;
        if (probe.contactForm) result.contactForm = probe.contactForm;
      }
      result.bodyOverflowX[vp.name] = probe.overflowX;
    }

    await page.close();
  }

  return result;
}

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: 'new',
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu'],
  });

  const results = [];
  for (const t of PAGES) {
    process.stdout.write(`Scanning ${t.name} ... `);
    const start = Date.now();
    try {
      const r = await auditPage(browser, t);
      results.push(r);
      console.log(`OK ${Date.now()-start}ms  errs=${r.pageErrors.length} reqFail=${r.requestFailed.length} brokenImg=${r.brokenImages}`);
    } catch (e) {
      results.push({ name: t.name, url: t.url, tier: t.tier, fatal: e.message });
      console.log(`FAIL ${e.message}`);
    }
  }

  await browser.close();
  fs.writeFileSync(OUT, JSON.stringify(results, null, 2));
  console.log('Saved to', OUT);
})();
