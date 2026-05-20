const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const PAGES = [
  { name: 'portfolio', url: 'https://suriota.com/portfolio/', post_id: 839 },
  { name: 'internship', url: 'https://suriota.com/internship/', post_id: 1127 }
];

const OUT_DIR = path.join(__dirname, '..', 'screenshots', 'audit-cluster4');
if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });

async function auditPage(page, p) {
  const results = {
    name: p.name,
    url: p.url,
    post_id: p.post_id,
    desktop_screenshot: path.join(OUT_DIR, `audit-cluster4-${p.name}-desktop.png`),
    mobile_screenshot: path.join(OUT_DIR, `audit-cluster4-${p.name}-mobile.png`),
    headings: [],
    missing_alt: [],
    console_errors: 0,
    lcp_candidate: null,
    load_time_ms: 0,
    viewport_data: {}
  };

  // Track console errors
  const consoleMessages = [];
  page.on('console', msg => {
    if (msg.type() === 'error') consoleMessages.push(msg.text());
  });

  // Measure load time
  const start = Date.now();
  await page.goto(p.url, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(3000); // let JS settle
  results.load_time_ms = Date.now() - start;

  // Desktop screenshot (1440x900)
  await page.setViewportSize({ width: 1440, height: 900 });
  await page.waitForTimeout(1000);
  await page.screenshot({ path: results.desktop_screenshot, fullPage: false });

  // Mobile screenshot (375x812)
  await page.setViewportSize({ width: 375, height: 812 });
  await page.waitForTimeout(1000);
  await page.screenshot({ path: results.mobile_screenshot, fullPage: false });

  // Extract data
  const data = await page.evaluate(() => {
    // Headings
    const headings = [];
    document.querySelectorAll('h1, h2, h3, h4, h5, h6').forEach(el => {
      headings.push({
        tag: el.tagName,
        text: el.innerText.trim().replace(/\s+/g, ' ').substring(0, 200),
        class: el.className
      });
    });

    // Images without alt
    const missingAlt = [];
    document.querySelectorAll('img').forEach(img => {
      const alt = img.getAttribute('alt');
      if (!alt || alt.trim() === '') {
        missingAlt.push({
          src: img.src.substring(0, 200),
          class: img.className
        });
      }
    });

    // LCP candidate (largest visible image or text block)
    let lcpCandidate = null;
    const largestImg = Array.from(document.querySelectorAll('img')).reduce((largest, img) => {
      const rect = img.getBoundingClientRect();
      const area = rect.width * rect.height;
      return area > (largest?.area || 0) && rect.top < window.innerHeight ? { el: img, area } : largest;
    }, null);

    if (largestImg) {
      lcpCandidate = {
        type: 'image',
        src: largestImg.el.src.substring(0, 200),
        area: Math.round(largestImg.area)
      };
    }

    // Viewport-specific data
    const viewportData = {
      width: window.innerWidth,
      height: window.innerHeight,
      scrollWidth: document.documentElement.scrollWidth,
      scrollHeight: document.documentElement.scrollHeight,
      hasHorizontalScroll: document.documentElement.scrollWidth > window.innerWidth,
      elementorWidgets: Array.from(new Set(
        Array.from(document.querySelectorAll('[data-widget_type]')).map(el => el.dataset.widget_type)
      )),
      touchTargets: (() => {
        const small = [];
        document.querySelectorAll('a, button, input, textarea, select, [role="button"]').forEach(el => {
          const rect = el.getBoundingClientRect();
          if (rect.width < 44 || rect.height < 44) {
            small.push({ tag: el.tagName, text: el.innerText?.trim()?.substring(0, 30), w: Math.round(rect.width), h: Math.round(rect.height) });
          }
        });
        return small.slice(0, 20);
      })()
    };

    return { headings, missingAlt, lcpCandidate, viewportData };
  });

  results.headings = data.headings;
  results.missing_alt = data.missingAlt;
  results.lcp_candidate = data.lcpCandidate;
  results.viewport_data = data.viewportData;
  results.console_errors = consoleMessages.length;

  return results;
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  const allResults = [];
  for (const p of PAGES) {
    try {
      console.log(`Auditing ${p.name}...`);
      const result = await auditPage(page, p);
      allResults.push(result);
      console.log(`✅ ${p.name} done`);
    } catch (e) {
      console.error(`❌ ${p.name}: ${e.message}`);
      allResults.push({ name: p.name, error: e.message });
    }
  }

  await browser.close();

  const outPath = path.join(OUT_DIR, 'audit-results.json');
  fs.writeFileSync(outPath, JSON.stringify(allResults, null, 2));
  console.log(`Results saved to ${outPath}`);
})();
