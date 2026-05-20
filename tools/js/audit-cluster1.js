#!/usr/bin/env node
/**
 * Cluster 1 Audit — Homepage, About Us, Tentang
 * Screenshots + DOM evaluation + performance metrics
 */
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const PAGES = [
  { name: 'homepage', post_id: 12, url: 'https://suriota.com/' },
  { name: 'about-us', post_id: 29, url: 'https://suriota.com/about-us/' },
  { name: 'tentang', post_id: 376, url: 'https://suriota.com/tentang/' }
];

const OUT_DIR = path.join(__dirname, '..', 'screenshots', 'audit-2026-05-18');

async function auditPage(browser, pageInfo) {
  const page = await browser.newPage();
  const results = {
    name: pageInfo.name,
    url: pageInfo.url,
    post_id: pageInfo.post_id,
    desktopScreenshot: path.join(OUT_DIR, `audit-cluster1-${pageInfo.name}-desktop.png`),
    mobileScreenshot: path.join(OUT_DIR, `audit-cluster1-${pageInfo.name}-mobile.png`),
    headings: [],
    missingAlt: [],
    consoleErrors: [],
    lcp: null,
    loadTime: null,
    performance: {}
  };

  // Capture console errors
  page.on('console', msg => {
    if (msg.type() === 'error') {
      results.consoleErrors.push(msg.text());
    }
  });

  // Desktop
  await page.setViewport({ width: 1440, height: 900 });
  const startTime = Date.now();
  await page.goto(pageInfo.url, { waitUntil: 'networkidle2', timeout: 60000 });
  await new Promise(r => setTimeout(r, 3000));
  results.loadTime = Date.now() - startTime;

  await page.screenshot({ path: results.desktopScreenshot, fullPage: true });

  // DOM Evaluation
  const domData = await page.evaluate(() => {
    // Headings
    const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6')).map(h => ({
      tag: h.tagName,
      text: h.innerText.trim().substring(0, 200),
      id: h.id || null,
      class: h.className.substring(0, 100) || null
    }));

    // Images without alt
    const images = Array.from(document.querySelectorAll('img'));
    const missingAlt = images
      .filter(img => !img.alt || img.alt.trim() === '')
      .map(img => ({
        src: (img.src || '').substring(0, 150),
        width: img.naturalWidth,
        height: img.naturalHeight,
        visible: img.getBoundingClientRect().width > 0 && img.getBoundingClientRect().height > 0
      }));

    // LCP candidate (largest visible image or text block in viewport)
    const viewportH = window.innerHeight;
    let lcpEl = null;
    let maxArea = 0;
    const candidates = Array.from(document.querySelectorAll('img, h1, h2, video, [role="img"]'));
    candidates.forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.top < viewportH && rect.bottom > 0 && rect.width > 0 && rect.height > 0) {
        const area = rect.width * rect.height;
        if (area > maxArea) {
          maxArea = area;
          lcpEl = {
            tag: el.tagName,
            text: el.innerText ? el.innerText.trim().substring(0, 100) : null,
            src: el.src ? el.src.substring(0, 100) : null,
            width: Math.round(rect.width),
            height: Math.round(rect.height),
            area: Math.round(area)
          };
        }
      }
    });

    // Horizontal scroll check
    const hasHorizontalScroll = document.documentElement.scrollWidth > window.innerWidth + 5;

    // Touch target sizes (mobile-relevant but check on desktop too)
    const smallTouchTargets = Array.from(document.querySelectorAll('a, button, [role="button"]')).filter(el => {
      const rect = el.getBoundingClientRect();
      return rect.width > 0 && rect.height > 0 && (rect.width < 44 || rect.height < 44);
    }).length;

    // Elementor widget count (rough)
    const widgetCount = document.querySelectorAll('[data-element_type="widget"]').length;
    const sectionCount = document.querySelectorAll('[data-element_type="section"]').length;

    // Check for Elementor structure data
    const elementorData = document.querySelector('script#elementor-frontend-js-before');
    const hasElementorConfig = !!elementorData;

    // Check for emergency header/footer indicators
    const hasEmergencyHeader = document.querySelector('[data-emergency-header]') !== null || document.querySelector('.sx-emergency-header') !== null;
    const hasEmergencyFooter = document.querySelector('[data-emergency-footer]') !== null || document.querySelector('.sx-emergency-footer') !== null;

    // Font families used
    const bodyFont = window.getComputedStyle(document.body).fontFamily;
    const h1Font = document.querySelector('h1') ? window.getComputedStyle(document.querySelector('h1')).fontFamily : null;

    // Check meta viewport
    const viewportMeta = document.querySelector('meta[name="viewport"]')?.content || null;

    return {
      headings,
      missingAlt,
      lcpCandidate: lcpEl,
      hasHorizontalScroll,
      smallTouchTargets,
      widgetCount,
      sectionCount,
      hasElementorConfig,
      hasEmergencyHeader,
      hasEmergencyFooter,
      bodyFont,
      h1Font,
      viewportMeta
    };
  });

  Object.assign(results, domData);

  // Mobile screenshot
  await page.setViewport({ width: 375, height: 812 });
  await new Promise(r => setTimeout(r, 1500));
  await page.screenshot({ path: results.mobileScreenshot, fullPage: true });

  await page.close();
  return results;
}

async function run() {
  if (!fs.existsSync(OUT_DIR)) fs.mkdirSync(OUT_DIR, { recursive: true });

  const browser = await puppeteer.launch({ headless: true });
  const allResults = [];

  for (const p of PAGES) {
    try {
      console.log(`Auditing ${p.name}...`);
      const res = await auditPage(browser, p);
      allResults.push(res);
      console.log(`  ✅ ${p.name} — ${res.headings.length} headings, ${res.missingAlt.length} missing alt, ${res.consoleErrors.length} console errors`);
    } catch (e) {
      console.error(`  ❌ ${p.name}: ${e.message}`);
      allResults.push({ name: p.name, error: e.message });
    }
  }

  await browser.close();

  // Save raw results
  fs.writeFileSync(path.join(OUT_DIR, 'audit-cluster1-raw.json'), JSON.stringify(allResults, null, 2));

  // Print structured report
  console.log('\n' + '='.repeat(80));
  console.log('AUDIT REPORT — CLUSTER 1 (Homepage, About Us, Tentang)');
  console.log('='.repeat(80));

  for (const r of allResults) {
    if (r.error) {
      console.log(`\n❌ ${r.name}: ERROR — ${r.error}`);
      continue;
    }

    console.log(`\n📄 ${r.name.toUpperCase()}`);
    console.log(`   URL: ${r.url}`);
    console.log(`   Screenshots: ${r.desktopScreenshot}, ${r.mobileScreenshot}`);
    console.log(`   Load time: ${r.loadTime}ms`);
    console.log(`   Console errors: ${r.consoleErrors.length}`);
    console.log(`   Widgets/Sections: ${r.widgetCount}/${r.sectionCount}`);
    console.log(`   LCP candidate: ${r.lcpCandidate ? `${r.lcpCandidate.tag} (${r.lcpCandidate.width}x${r.lcpCandidate.height}, area ${r.lcpCandidate.area})` : 'none'}`);
    console.log(`   Headings (${r.headings.length}):`);
    r.headings.forEach(h => console.log(`      ${h.tag}: "${h.text}"`));
    console.log(`   Missing alt: ${r.missingAlt.length} images`);
    r.missingAlt.forEach(img => console.log(`      - ${img.src.substring(0, 80)}`));
    console.log(`   Horizontal scroll: ${r.hasHorizontalScroll ? 'YES ❌' : 'No ✅'}`);
    console.log(`   Small touch targets: ${r.smallTouchTargets}`);
    console.log(`   Body font: ${r.bodyFont}`);
    console.log(`   H1 font: ${r.h1Font}`);
  }
}

run().catch(console.error);
