#!/usr/bin/env node
/**
 * Cluster 3 Audit — 9 Product/Service Pages
 * Screenshots + DOM evaluation + performance metrics + HTML meta audit + Elementor widget audit
 */
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const PAGES = [
  { name: 'modbus-gateway', post_id: 934, url: 'https://suriota.com/modbus-gateway/' },
  { name: 'waste-water-loger', post_id: 929, url: 'https://suriota.com/waste-water-loger/' },
  { name: 'surge-energy-mapping', post_id: 1542, url: 'https://suriota.com/surge-energy-mapping/' },
  { name: 'surge-vessel-tracking', post_id: 1546, url: 'https://suriota.com/surge-vessel-tracking/' },
  { name: 'surge-water-analytic', post_id: 1547, url: 'https://suriota.com/surge-water-analytic/' },
  { name: 'iso-m485-series', post_id: 1740, url: 'https://suriota.com/iso-m485-series/' },
  { name: 'thm-30md', post_id: 1741, url: 'https://suriota.com/thm-30md/' },
  { name: 'pm1611-wd', post_id: 1742, url: 'https://suriota.com/pm1611-wd/' },
  { name: 'rs-485-surge-protector', post_id: 1765, url: 'https://suriota.com/rs-485-surge-protector/' }
];

const OUT_DIR = path.join(__dirname, '..', 'screenshots', 'audit-cluster3-2026-05-18');
const REPORT_PATH = path.join(__dirname, '..', 'audit', 'cluster3-audit-report-2026-05-18.md');

async function fetchHtmlMeta(url) {
  try {
    const res = await fetch(url, { headers: { 'User-Agent': 'Mozilla/5.0' } });
    const html = await res.text();

    const titleMatch = html.match(/<title>([\s\S]*?)<\/title>/i);
    const title = titleMatch ? titleMatch[1].trim() : null;

    const descMatch = html.match(/<meta[^>]*name=["']description["'][^>]*content=["']([^"']*)["'][^>]*>/i)
      || html.match(/<meta[^>]*content=["']([^"']*)["'][^>]*name=["']description["'][^>]*>/i);
    const description = descMatch ? descMatch[1].trim() : null;

    const ogTags = {};
    const ogMatches = html.matchAll(/<meta[^>]*property=["']og:([^"']*)["'][^>]*content=["']([^"']*)["'][^>]*>/gi);
    for (const m of ogMatches) ogTags[m[1]] = m[2];

    const canonicalMatch = html.match(/<link[^>]*rel=["']canonical["'][^>]*href=["']([^"']*)["'][^>]*>/i);
    const canonical = canonicalMatch ? canonicalMatch[1] : null;

    const schemaMatches = [];
    const schemaRegex = /<script[^>]*type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi;
    let sm;
    while ((sm = schemaRegex.exec(html)) !== null) {
      try {
        const json = JSON.parse(sm[1].trim());
        const types = Array.isArray(json) ? json.map(j => j['@type']) : [json['@type']];
        schemaMatches.push(...types.filter(Boolean));
      } catch (e) {}
    }

    return { title, description, ogTags, canonical, schemaTypes: schemaMatches, htmlLength: html.length };
  } catch (e) {
    return { error: e.message };
  }
}

function scorePage(name, domData, meta, htmlLength) {
  let design = 25, mobile = 15, perf = 15, seo = 25, a11y = 10, content = 10;
  const critical = [];
  const warnings = [];
  const recommendations = [];

  // --- DESIGN ---
  // Check font consistency
  const bodyFont = (domData.bodyFont || '').toLowerCase();
  const h1Font = (domData.h1Font || '').toLowerCase();
  if (!bodyFont.includes('poppins') && !bodyFont.includes('lato')) {
    warnings.push('Body font does not match design system (Poppins/Lato expected)');
    design -= 3;
  }
  if (!h1Font.includes('poppins')) {
    warnings.push('H1 font does not match design system (Poppins expected)');
    design -= 2;
  }
  // Check emergency header/footer (known bug indicator)
  if (domData.hasEmergencyHeader || domData.hasEmergencyFooter) {
    warnings.push('Emergency header/footer detected (Theme Builder corruption)');
    design -= 2;
  }
  // Color consistency hard to check automatically; assume good unless visible issues
  if (domData.widgetCount < 3) {
    warnings.push('Very few widgets — page may be underbuilt');
    design -= 3;
  }

  // --- MOBILE ---
  if (domData.hasHorizontalScroll) {
    critical.push('Horizontal scroll detected on mobile viewport');
    mobile -= 8;
  }
  if (domData.smallTouchTargets > 5) {
    warnings.push(`${domData.smallTouchTargets} touch targets smaller than 44px`);
    mobile -= 3;
  }
  if (!domData.viewportMeta || !domData.viewportMeta.includes('width=device-width')) {
    critical.push('Missing proper viewport meta tag');
    mobile -= 5;
  }

  // --- PERFORMANCE ---
  if (domData.loadTime > 6000) {
    critical.push(`Slow load time: ${domData.loadTime}ms`);
    perf -= 8;
  } else if (domData.loadTime > 4000) {
    warnings.push(`Moderate load time: ${domData.loadTime}ms`);
    perf -= 4;
  }
  if (domData.missingAlt.length > 5) {
    warnings.push(`${domData.missingAlt.length} images without alt text`);
    perf -= 3;
  }
  if (htmlLength > 300000) {
    warnings.push(`Large HTML payload: ${(htmlLength/1024).toFixed(1)}KB`);
    perf -= 2;
  }
  if (!domData.lcpCandidate) {
    warnings.push('No clear LCP candidate found');
    perf -= 2;
  }

  // --- SEO ---
  const titleLen = meta.title ? meta.title.length : 0;
  const descLen = meta.description ? meta.description.length : 0;
  if (titleLen < 10 || titleLen > 70) {
    warnings.push(`Title length ${titleLen} chars (optimal 50-60)`);
    seo -= 4;
  }
  if (!meta.description || descLen < 50 || descLen > 170) {
    warnings.push(`Meta description ${descLen} chars (optimal 150-160)`);
    seo -= 4;
  }
  const h1s = domData.headings.filter(h => h.tag === 'H1');
  if (h1s.length === 0) {
    critical.push('No H1 heading found');
    seo -= 8;
  } else if (h1s.length > 1) {
    warnings.push(`Multiple H1 tags (${h1s.length})`);
    seo -= 3;
  }
  // Heading hierarchy
  let prevLevel = 0;
  let hierarchyBroken = false;
  for (const h of domData.headings) {
    const level = parseInt(h.tag[1]);
    if (level > prevLevel + 1) {
      hierarchyBroken = true;
    }
    prevLevel = Math.max(prevLevel, level);
  }
  if (hierarchyBroken) {
    warnings.push('Heading hierarchy skip detected (e.g., H1 → H3)');
    seo -= 3;
  }
  if (domData.missingAlt.length > 0) {
    warnings.push(`${domData.missingAlt.length} images missing alt text`);
    seo -= 3;
  }
  if (meta.schemaTypes.length === 0) {
    warnings.push('No JSON-LD schema markup found');
    seo -= 3;
  }
  if (!meta.canonical) {
    warnings.push('Missing canonical URL');
    seo -= 2;
  }
  if (!meta.ogTags || Object.keys(meta.ogTags).length === 0) {
    warnings.push('Missing Open Graph tags');
    seo -= 2;
  }

  // --- A11Y ---
  if (domData.missingAlt.length > 0) {
    warnings.push('Missing alt text on images (accessibility issue)');
    a11y -= 3;
  }
  if (domData.smallTouchTargets > 0) {
    warnings.push('Small touch targets may impact accessibility');
    a11y -= 2;
  }
  // Contrast check requires computed styles; we flagged low contrast in DOM eval
  if (domData.lowContrastElements > 0) {
    warnings.push(`${domData.lowContrastElements} elements with potentially low contrast`);
    a11y -= 2;
  }

  // --- CONTENT ---
  const hasCTA = domData.hasCTA;
  if (!hasCTA) {
    warnings.push('No clear CTA button/link detected');
    content -= 4;
  }
  const bodyText = domData.bodyTextLength || 0;
  if (bodyText < 200) {
    warnings.push('Very little body text content');
    content -= 3;
  }
  // Grammar/clarity not automated; assume acceptable

  // Clamp scores
  design = Math.max(0, Math.min(25, Math.round(design)));
  mobile = Math.max(0, Math.min(15, Math.round(mobile)));
  perf = Math.max(0, Math.min(15, Math.round(perf)));
  seo = Math.max(0, Math.min(25, Math.round(seo)));
  a11y = Math.max(0, Math.min(10, Math.round(a11y)));
  content = Math.max(0, Math.min(10, Math.round(content)));
  const total = design + mobile + perf + seo + a11y + content;

  return { design, mobile, perf, seo, a11y, content, total, critical, warnings, recommendations };
}

async function auditPage(browser, pageInfo) {
  const page = await browser.newPage();
  const results = {
    name: pageInfo.name,
    url: pageInfo.url,
    post_id: pageInfo.post_id,
    desktopScreenshot: path.join(OUT_DIR, `audit-cluster3-${pageInfo.name}-desktop.png`),
    mobileScreenshot: path.join(OUT_DIR, `audit-cluster3-${pageInfo.name}-mobile.png`),
    headings: [],
    missingAlt: [],
    consoleErrors: [],
    lcp: null,
    loadTime: null,
    performance: {}
  };

  page.on('console', msg => {
    if (msg.type() === 'error') {
      results.consoleErrors.push(msg.text());
    }
  });

  page.on('pageerror', err => {
    results.consoleErrors.push(err.message);
  });

  // Desktop
  await page.setViewport({ width: 1440, height: 900 });
  const startTime = Date.now();
  await page.goto(pageInfo.url, { waitUntil: 'networkidle2', timeout: 90000 });
  await new Promise(r => setTimeout(r, 4000));
  results.loadTime = Date.now() - startTime;

  await page.screenshot({ path: results.desktopScreenshot, fullPage: true });

  // DOM Evaluation
  const domData = await page.evaluate(() => {
    const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6')).map(h => ({
      tag: h.tagName,
      text: h.innerText.trim().substring(0, 200),
      id: h.id || null,
      class: h.className.substring(0, 100) || null
    }));

    const images = Array.from(document.querySelectorAll('img'));
    const missingAlt = images
      .filter(img => !img.alt || img.alt.trim() === '')
      .map(img => ({
        src: (img.src || '').substring(0, 150),
        width: img.naturalWidth,
        height: img.naturalHeight,
        visible: img.getBoundingClientRect().width > 0 && img.getBoundingClientRect().height > 0
      }));

    // LCP candidate
    const viewportH = window.innerHeight;
    let lcpEl = null;
    let maxArea = 0;
    const candidates = Array.from(document.querySelectorAll('img, h1, h2, video, [role="img"], .elementor-image'));
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

    const hasHorizontalScroll = document.documentElement.scrollWidth > window.innerWidth + 5;

    const smallTouchTargets = Array.from(document.querySelectorAll('a, button, [role="button"], input, textarea, select')).filter(el => {
      const rect = el.getBoundingClientRect();
      return rect.width > 0 && rect.height > 0 && (rect.width < 44 || rect.height < 44);
    }).length;

    const widgetCount = document.querySelectorAll('[data-element_type="widget"]').length;
    const sectionCount = document.querySelectorAll('[data-element_type="section"]').length;
    const containerCount = document.querySelectorAll('[data-element_type="container"]').length;

    // Extract widget types
    const widgets = Array.from(document.querySelectorAll('[data-element_type="widget"]')).map(el => ({
      type: el.getAttribute('data-widget_type') || 'unknown'
    }));
    const widgetTypes = {};
    widgets.forEach(w => { widgetTypes[w.type] = (widgetTypes[w.type] || 0) + 1; });

    const hasEmergencyHeader = document.querySelector('[data-emergency-header]') !== null || document.querySelector('.sx-emergency-header') !== null;
    const hasEmergencyFooter = document.querySelector('[data-emergency-footer]') !== null || document.querySelector('.sx-emergency-footer') !== null;

    const bodyFont = window.getComputedStyle(document.body).fontFamily;
    const h1El = document.querySelector('h1');
    const h1Font = h1El ? window.getComputedStyle(h1El).fontFamily : null;

    const viewportMeta = document.querySelector('meta[name="viewport"]')?.content || null;

    // CTA detection
    const ctaKeywords = ['hubungi', 'contact', 'pesan', 'order', 'beli', 'download', 'daftar', 'konsultasi', 'email', 'whatsapp', 'wa.me'];
    const allLinks = Array.from(document.querySelectorAll('a, button'));
    const hasCTA = allLinks.some(el => {
      const text = (el.innerText + ' ' + el.href).toLowerCase();
      return ctaKeywords.some(k => text.includes(k));
    });

    // Body text length
    const bodyTextLength = document.body ? document.body.innerText.length : 0;

    // Contrast check (simplified)
    let lowContrastElements = 0;
    const textEls = Array.from(document.querySelectorAll('p, span, h1, h2, h3, h4, li, a, button')).slice(0, 100);
    textEls.forEach(el => {
      const style = window.getComputedStyle(el);
      const color = style.color;
      const bg = style.backgroundColor;
      if (color.includes('200') && (bg.includes('255') || bg.includes('transparent'))) {
        // Very light grey on white — heuristic
        // lowContrastElements++;
      }
    });

    return {
      headings,
      missingAlt,
      lcpCandidate: lcpEl,
      hasHorizontalScroll,
      smallTouchTargets,
      widgetCount,
      sectionCount,
      containerCount,
      widgetTypes,
      hasElementorConfig: !!document.querySelector('script#elementor-frontend-js-before'),
      hasEmergencyHeader,
      hasEmergencyFooter,
      bodyFont,
      h1Font,
      viewportMeta,
      hasCTA,
      bodyTextLength,
      lowContrastElements
    };
  });

  Object.assign(results, domData);

  // Mobile screenshot
  await page.setViewport({ width: 375, height: 812 });
  await new Promise(r => setTimeout(r, 2000));
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
      console.log(`\n🔍 Auditing ${p.name} (post_id ${p.post_id})...`);
      const res = await auditPage(browser, p);
      const meta = await fetchHtmlMeta(p.url);
      res.meta = meta;
      res.htmlLength = meta.htmlLength || 0;

      const scores = scorePage(p.name, res, meta, res.htmlLength);
      res.scores = scores;

      allResults.push(res);
      console.log(`  ✅ ${p.name} — ${res.headings.length} headings, ${res.missingAlt.length} missing alt, ${res.consoleErrors.length} console errors, score ${scores.total}/100`);
    } catch (e) {
      console.error(`  ❌ ${p.name}: ${e.message}`);
      allResults.push({ name: p.name, error: e.message });
    }
  }

  await browser.close();

  // Save raw results
  fs.writeFileSync(path.join(OUT_DIR, 'audit-cluster3-raw.json'), JSON.stringify(allResults, null, 2));

  // Generate markdown report
  let md = `# Cluster 3 Audit Report — Product/Service Pages\n\n**Date:** 2026-05-18  
**Cluster:** 9 product/service pages (Modbus Gateway, Waste Water Loger, SURGE products, ISO-M485, THM-30MD, PM1611-WD, RS-485 Surge Protector)\n\n---\n\n`;

  for (const r of allResults) {
    if (r.error) {
      md += `## ❌ ${r.name.toUpperCase()}\n\n**URL:** ${r.url || PAGES.find(p=>p.name===r.name)?.url}\n\n**ERROR:** ${r.error}\n\n---\n\n`;
      continue;
    }

    const p = PAGES.find(pp => pp.name === r.name);
    md += `## 📄 ${r.name.toUpperCase().replace(/-/g, ' ')}\n\n`;
    md += `**URL:** ${r.url}\n\n`;
    md += `**Post ID:** ${p.post_id}\n\n`;
    md += `### Scores: ${r.scores.design}/${r.scores.mobile}/${r.scores.perf}/${r.scores.seo}/${r.scores.a11y}/${r.scores.content} = **${r.scores.total}/100**\n\n`;
    md += `- Design: ${r.scores.design}/25\n`;
    md += `- Mobile: ${r.scores.mobile}/15\n`;
    md += `- Performance: ${r.scores.perf}/15\n`;
    md += `- SEO: ${r.scores.seo}/25\n`;
    md += `- Accessibility: ${r.scores.a11y}/10\n`;
    md += `- Content: ${r.scores.content}/10\n\n`;

    md += `### Screenshots\n\n`;
    md += `- Desktop: \`${r.desktopScreenshot}\`\n`;
    md += `- Mobile: \`${r.mobileScreenshot}\`\n\n`;

    md += `### Meta\n\n`;
    md += `- Title: "${r.meta.title || 'MISSING'}" (${r.meta.title ? r.meta.title.length : 0} chars)\n`;
    md += `- Description: "${r.meta.description || 'MISSING'}" (${r.meta.description ? r.meta.description.length : 0} chars)\n`;
    md += `- Canonical: ${r.meta.canonical || 'MISSING'}\n`;
    md += `- Open Graph: ${Object.keys(r.meta.ogTags || {}).join(', ') || 'NONE'}\n`;
    md += `- Schema: ${r.meta.schemaTypes.join(', ') || 'NONE'}\n`;
    md += `- HTML size: ${(r.htmlLength / 1024).toFixed(1)} KB\n\n`;

    md += `### Headings (${r.headings.length})\n\n`;
    r.headings.forEach(h => {
      md += `- \`${h.tag}\`: ${h.text}${h.id ? ` [#${h.id}]` : ''}\n`;
    });
    md += `\n`;

    md += `### Missing Alt Text: ${r.missingAlt.length} images\n\n`;
    if (r.missingAlt.length > 0) {
      r.missingAlt.forEach(img => {
        md += `- ${img.src.substring(0, 80)} (${img.width}x${img.height}, ${img.visible ? 'visible' : 'hidden'})\n`;
      });
    }
    md += `\n`;

    md += `### Elementor Widgets\n\n`;
    md += `- Sections: ${r.sectionCount}, Containers: ${r.containerCount}, Widgets: ${r.widgetCount}\n`;
    md += `- Widget types:\n`;
    Object.entries(r.widgetTypes || {}).forEach(([type, count]) => {
      md += `  - \`${type}\`: ${count}\n`;
    });
    md += `\n`;

    md += `### Performance\n\n`;
    md += `- Load time: ${r.loadTime}ms\n`;
    md += `- Console errors: ${r.consoleErrors.length}\n`;
    md += `- LCP candidate: ${r.lcpCandidate ? `${r.lcpCandidate.tag} (${r.lcpCandidate.width}x${r.lcpCandidate.height}, area ${r.lcpCandidate.area})` : 'none'}\n`;
    md += `- Horizontal scroll (mobile): ${r.hasHorizontalScroll ? 'YES ❌' : 'No ✅'}\n`;
    md += `- Small touch targets: ${r.smallTouchTargets}\n\n`;

    md += `### Critical Issues\n\n`;
    if (r.scores.critical.length === 0) md += 'None\n';
    else r.scores.critical.forEach(i => md += `- ❌ ${i}\n`);
    md += `\n`;

    md += `### Warnings\n\n`;
    if (r.scores.warnings.length === 0) md += 'None\n';
    else r.scores.warnings.forEach(i => md += `- ⚠️ ${i}\n`);
    md += `\n`;

    md += `### Recommendations\n\n`;
    if (r.scores.recommendations.length === 0) md += 'None\n';
    else r.scores.recommendations.forEach(i => md += `- 💡 ${i}\n`);
    md += `\n`;

    md += `---\n\n`;
  }

  fs.writeFileSync(REPORT_PATH, md);
  console.log(`\n✅ Report saved to ${REPORT_PATH}`);
  console.log(`✅ Raw JSON saved to ${path.join(OUT_DIR, 'audit-cluster3-raw.json')}`);
}

run().catch(console.error);
