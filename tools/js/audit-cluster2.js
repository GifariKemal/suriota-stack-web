#!/usr/bin/env node
/**
 * Cluster 2 Audit — 6 Service Pages
 * Desain Grafis (33), Automation (35), Electrical (37),
 * Renewable Energy (39), Teknologi Informasi (41), Water Treatment (945)
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const PAGES = [
  { name: 'desain-grafis', url: 'https://suriota.com/desain-grafis/', postId: 33 },
  { name: 'automation', url: 'https://suriota.com/automation/', postId: 35 },
  { name: 'electrical', url: 'https://suriota.com/electrical/', postId: 37 },
  { name: 'renewable-energy', url: 'https://suriota.com/renewable-energy/', postId: 39 },
  { name: 'teknologi-informasi', url: 'https://suriota.com/teknologi-informasi/', postId: 41 },
  { name: 'water-treatment', url: 'https://suriota.com/water-treatment/', postId: 945 },
];

const outDir = path.join(__dirname, '..', 'screenshots', 'audit-cluster2-' + new Date().toISOString().split('T')[0]);
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

async function fetchRawHtml(url) {
  try {
    const html = execSync(`curl -sL -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" "${url}" --max-time 15`, { encoding: 'utf-8', maxBuffer: 5 * 1024 * 1024 });
    return html;
  } catch (e) {
    return '';
  }
}

async function fetchElementorStructure(postId) {
  try {
    // Try WordPress REST API for page content
    const json = execSync(`curl -sL "https://suriota.com/wp-json/wp/v2/pages/${postId}?_fields=content,title,meta&_embed" --max-time 10`, { encoding: 'utf-8' });
    const data = JSON.parse(json);
    return data;
  } catch (e) {
    return null;
  }
}

function parseMeta(html) {
  const titleMatch = html.match(/<title>([^<]*)<\/title>/i);
  const descMatch = html.match(/<meta[^>]*name=["']description["'][^>]*content=["']([^"']*)["'][^>]*>/i) || html.match(/<meta[^>]*content=["']([^"']*)["'][^>]*name=["']description["'][^>]*>/i);
  const ogTitle = html.match(/<meta[^>]*property=["']og:title["'][^>]*content=["']([^"']*)["'][^>]*>/i);
  const ogDesc = html.match(/<meta[^>]*property=["']og:description["'][^>]*content=["']([^"']*)["'][^>]*>/i);
  const ogImage = html.match(/<meta[^>]*property=["']og:image["'][^>]*content=["']([^"']*)["'][^>]*>/i);
  const ogUrl = html.match(/<meta[^>]*property=["']og:url["'][^>]*content=["']([^"']*)["'][^>]*>/i);
  const canonical = html.match(/<link[^>]*rel=["']canonical["'][^>]*href=["']([^"']*)["'][^>]*>/i);
  const schemaMatches = [...html.matchAll(/<script[^>]*type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi)];
  const schemas = schemaMatches.map(m => {
    try { return JSON.parse(m[1]); } catch (e) { return { _raw: m[1].substring(0,200) }; }
  });
  return {
    title: titleMatch ? titleMatch[1].trim() : '',
    titleLen: titleMatch ? titleMatch[1].trim().length : 0,
    description: descMatch ? descMatch[1].trim() : '',
    descLen: descMatch ? descMatch[1].trim().length : 0,
    ogTitle: ogTitle ? ogTitle[1] : '',
    ogDesc: ogDesc ? ogDesc[1] : '',
    ogImage: ogImage ? ogImage[1] : '',
    ogUrl: ogUrl ? ogUrl[1] : '',
    canonical: canonical ? canonical[1] : '',
    schemas,
  };
}

function parseElementorWidgets(html) {
  const widgets = [];
  const widgetMatches = [...html.matchAll(/data-widget_type=["']([^"']*)["']/g)];
  const counts = {};
  widgetMatches.forEach(m => {
    const type = m[1];
    counts[type] = (counts[type] || 0) + 1;
  });
  return counts;
}

async function auditPage(pageInfo) {
  console.log(`\n🔍 Auditing: ${pageInfo.name}`);
  const results = {
    name: pageInfo.name,
    url: pageInfo.url,
    postId: pageInfo.postId,
    screenshots: {},
    headings: [],
    missingAlt: 0,
    totalImages: 0,
    consoleErrors: 0,
    lcpCandidate: '',
    loadTime: 0,
    meta: {},
    elementorWidgets: {},
    wpData: null,
    findings: { desktop: [], mobile: [] },
  };

  // Fetch raw HTML + meta
  const html = await fetchRawHtml(pageInfo.url);
  results.meta = parseMeta(html);
  results.elementorWidgets = parseElementorWidgets(html);

  // Fetch WP structure
  results.wpData = await fetchElementorStructure(pageInfo.postId);

  const browser = await chromium.launch();

  for (const vp of [
    { label: 'desktop', width: 1440, height: 900 },
    { label: 'mobile', width: 375, height: 812 },
  ]) {
    const context = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
    const page = await context.newPage();
    const consoleMsgs = [];
    page.on('console', msg => { if (msg.type() === 'error') consoleMsgs.push(msg.text()); });

    const start = Date.now();
    try {
      await page.goto(pageInfo.url, { waitUntil: 'networkidle', timeout: 45000 });
      await page.waitForTimeout(2500);
    } catch (e) {
      console.log(`  ⚠️ Load timeout/error for ${pageInfo.name} ${vp.label}`);
    }
    results.loadTime = Date.now() - start;

    const ssPath = path.join(outDir, `audit-cluster2-${pageInfo.name}-${vp.label}.png`);
    await page.screenshot({ path: ssPath, fullPage: true });
    results.screenshots[vp.label] = ssPath;

    const data = await page.evaluate(() => {
      const headings = [];
      for (let i = 1; i <= 6; i++) {
        document.querySelectorAll(`h${i}`).forEach(h => {
          headings.push({ tag: `H${i}`, text: h.innerText.trim().substring(0, 120) });
        });
      }

      const imgs = Array.from(document.querySelectorAll('img'));
      let missingAlt = 0;
      imgs.forEach(img => {
        const alt = img.getAttribute('alt');
        if (!alt || alt.trim() === '' || alt.trim() === 'image') missingAlt++;
      });

      // LCP candidate: largest visible image or text block
      let lcp = { type: 'unknown', text: '' };
      const largestImg = imgs
        .filter(img => {
          const r = img.getBoundingClientRect();
          const s = window.getComputedStyle(img);
          return r.width > 100 && r.height > 100 && s.display !== 'none' && s.visibility !== 'hidden';
        })
        .sort((a, b) => {
          const ra = a.getBoundingClientRect();
          const rb = b.getBoundingClientRect();
          return (rb.width * rb.height) - (ra.width * ra.height);
        })[0];

      if (largestImg) {
        lcp = { type: 'image', src: largestImg.src.substring(0, 120), alt: largestImg.alt || '', w: largestImg.getBoundingClientRect().width, h: largestImg.getBoundingClientRect().height };
      } else {
        const h1 = document.querySelector('h1');
        if (h1) lcp = { type: 'text', text: h1.innerText.trim().substring(0, 100) };
      }

      // Check horizontal overflow
      const overflow = document.documentElement.scrollWidth > window.innerWidth + 2;

      // Check tap targets
      const btns = Array.from(document.querySelectorAll('a, button'));
      let smallTap = 0;
      btns.forEach(b => {
        const r = b.getBoundingClientRect();
        if (r.width > 0 && r.height > 0 && (r.width < 44 || r.height < 44)) smallTap++;
      });

      // Contrast check (basic)
      const allText = Array.from(document.querySelectorAll('p, span, a, h1, h2, h3, h4, li'));
      let lowContrast = 0;
      allText.slice(0, 30).forEach(el => {
        const s = window.getComputedStyle(el);
        const color = s.color;
        const bg = s.backgroundColor;
        if (color.includes('rgb(200') || color.includes('rgb(255') || color.includes('rgba(0, 0, 0, 0.')) {
          if (bg === 'rgba(0, 0, 0, 0)' || bg.includes('255')) lowContrast++;
        }
      });

      // CTA presence
      const ctaWords = ['hubungi', 'konsultasi', 'pesan', 'order', 'daftar', 'contact', 'wa.me', 'whatsapp', 'telp', 'telepon', 'email', 'get started', 'learn more'];
      const bodyText = document.body.innerText.toLowerCase();
      const hasCta = ctaWords.some(w => bodyText.includes(w));

      // ARIA labels on nav/menu
      const navMissingAria = Array.from(document.querySelectorAll('nav, [role="navigation"]')).filter(n => !n.getAttribute('aria-label')).length;

      // Brand color check
      const elements = Array.from(document.querySelectorAll('section, div, a, button'));
      let brandColors = 0;
      elements.slice(0, 50).forEach(el => {
        const s = window.getComputedStyle(el);
        const bg = s.backgroundColor;
        const c = s.color;
        if (bg.includes('205B69') || bg.includes('200, 133, 31') || bg.includes('14, 57, 66') ||
            c.includes('205B69') || c.includes('200, 133, 31') || c.includes('14, 57, 66')) {
          brandColors++;
        }
      });

      return {
        headings,
        totalImages: imgs.length,
        missingAlt,
        lcp,
        overflow,
        smallTapTargets: smallTap,
        lowContrastCount: lowContrast,
        hasCta,
        navMissingAria,
        brandColors,
        bodyTextLen: document.body.innerText.length,
      };
    });

    results.findings[vp.label] = data;
    results.consoleErrors = consoleMsgs.length;
    results.lcpCandidate = data.lcp;
    results.totalImages = data.totalImages;
    results.missingAlt = data.missingAlt;

    if (vp.label === 'desktop') {
      results.headings = data.headings;
    }

    await context.close();
  }

  await browser.close();
  return results;
}

async function main() {
  const allResults = [];
  for (const p of PAGES) {
    const r = await auditPage(p);
    allResults.push(r);
  }

  // Write raw JSON
  fs.writeFileSync(path.join(outDir, 'audit-cluster2-raw.json'), JSON.stringify(allResults, null, 2));

  // Score and output
  console.log('\n' + '='.repeat(80));
  console.log('CLUSTER 2 AUDIT REPORT');
  console.log('='.repeat(80));

  for (const r of allResults) {
    const headings = r.headings;
    const h1s = headings.filter(h => h.tag === 'H1');
    const h1Unique = h1s.length === 1;
    const headingHierarchy = headings.every((h, i) => {
      if (i === 0) return true;
      const prev = parseInt(headings[i-1].tag[1]);
      const curr = parseInt(h.tag[1]);
      return curr <= prev + 1;
    });

    const d = r.findings.desktop;
    const m = r.findings.mobile;

    // SCORING
    let design = 0;
    // Visual hierarchy, color consistency, typography, spacing, brand alignment
    if (d.brandColors > 0) design += 8;
    if (headings.length >= 3) design += 5;
    if (!d.overflow) design += 5;
    if (d.lowContrastCount < 5) design += 4;
    else design += 2;
    if (r.totalImages > 0) design += 3;
    design = Math.min(25, design);

    let mobile = 0;
    if (!m.overflow) mobile += 5;
    if (m.smallTapTargets < 10) mobile += 5;
    else if (m.smallTapTargets < 20) mobile += 3;
    if (d.headings.length === m.headings.length) mobile += 3;
    if (m.totalImages > 0) mobile += 2;
    mobile = Math.min(15, mobile);

    let perf = 0;
    if (r.loadTime < 3000) perf += 8;
    else if (r.loadTime < 5000) perf += 5;
    else perf += 2;
    if (r.consoleErrors === 0) perf += 4;
    else if (r.consoleErrors < 3) perf += 2;
    if (r.missingAlt < r.totalImages * 0.3) perf += 3;
    else perf += 1;
    perf = Math.min(15, perf);

    let seo = 0;
    const t = r.meta;
    if (t.titleLen >= 50 && t.titleLen <= 60) seo += 5;
    else if (t.titleLen > 30 && t.titleLen < 70) seo += 3;
    else seo += 1;
    if (t.descLen >= 150 && t.descLen <= 160) seo += 5;
    else if (t.descLen > 100 && t.descLen < 180) seo += 3;
    else seo += 1;
    if (h1Unique) seo += 5;
    else seo += 1;
    if (headingHierarchy) seo += 4;
    else seo += 2;
    if (r.missingAlt === 0) seo += 3;
    else if (r.missingAlt <= 2) seo += 2;
    else seo += 0;
    if (t.schemas.length > 0) seo += 2;
    if (t.canonical) seo += 1;
    if (t.ogTitle && t.ogUrl) seo += 1;
    seo = Math.min(25, seo);

    let a11y = 0;
    if (r.missingAlt === 0) a11y += 3;
    else if (r.missingAlt <= 3) a11y += 1;
    if (d.lowContrastCount < 5) a11y += 3;
    else a11y += 1;
    if (d.navMissingAria === 0) a11y += 2;
    else a11y += 1;
    if (!d.overflow) a11y += 2;
    a11y = Math.min(10, a11y);

    let content = 0;
    if (d.hasCta) content += 4;
    if (d.bodyTextLen > 800) content += 3;
    else if (d.bodyTextLen > 400) content += 2;
    if (headings.length >= 3) content += 3;
    content = Math.min(10, content);

    const total = design + mobile + perf + seo + a11y + content;

    // Issues
    const critical = [];
    const warnings = [];
    const recommendations = [];

    if (!h1Unique) critical.push(`H1 issue: ${h1s.length} H1 element(s)`);
    if (t.titleLen < 10 || t.titleLen > 70) critical.push(`Title length ${t.titleLen} chars (optimal 50-60)`);
    if (t.descLen < 50 || t.descLen > 170) warnings.push(`Meta description ${t.descLen} chars (optimal 150-160)`);
    if (r.missingAlt > 0) warnings.push(`${r.missingAlt} image(s) missing alt text`);
    if (d.overflow) critical.push('Horizontal overflow on desktop');
    if (m.overflow) critical.push('Horizontal overflow on mobile');
    if (r.consoleErrors > 0) warnings.push(`${r.consoleErrors} console error(s)`);
    if (r.loadTime > 5000) warnings.push(`Load time ${r.loadTime}ms > 5s`);
    if (!headingHierarchy) warnings.push('Heading hierarchy has jumps');
    if (!t.canonical) warnings.push('Missing canonical URL');
    if (t.schemas.length === 0) warnings.push('No schema markup found');
    if (!d.hasCta) warnings.push('No clear CTA detected');
    if (m.smallTapTargets > 10) warnings.push(`${m.smallTapTargets} small tap targets on mobile`);
    if (d.navMissingAria > 0) warnings.push(`${d.navMissingAria} nav elements missing aria-label`);

    recommendations.push('Review heading hierarchy (H1→H2→H3)');
    if (r.missingAlt > 0) recommendations.push('Add descriptive alt text to all images');
    if (!t.ogImage) recommendations.push('Add Open Graph image tag');
    if (t.schemas.length === 0) recommendations.push('Add JSON-LD schema (Organization, Service, WebPage)');
    recommendations.push('Ensure consistent Industrial Editorial design tokens');
    if (r.loadTime > 3000) recommendations.push('Optimize images and reduce render-blocking assets');
    recommendations.push('Add visible CTA button (Hubungi/WA) if not present');

    const schemaTypes = t.schemas.map(s => s['@type'] || (Array.isArray(s['@graph']) ? s['@graph'].map(x => x['@type']).join(',') : 'unknown')).join(' | ');

    console.log(`\nPage: ${r.name}`);
    console.log(`URL: ${r.url}`);
    console.log(`Scores: ${design}/${mobile}/${perf}/${seo}/${a11y}/${content} = ${total}/100`);
    console.log(`Screenshots: ${r.screenshots.desktop}, ${r.screenshots.mobile}`);
    console.log(`Headings:`);
    headings.forEach(h => console.log(`  ${h.tag}: "${h.text}"`));
    console.log(`Missing Alt: ${r.missingAlt} images (of ${r.totalImages})`);
    console.log(`Meta: Title=${t.titleLen} chars, Desc=${t.descLen} chars`);
    console.log(`Schema: ${schemaTypes || 'none'}`);
    console.log(`Critical Issues: ${critical.join('; ') || 'none'}`);
    console.log(`Warnings: ${warnings.join('; ') || 'none'}`);
    console.log(`Recommendations: ${recommendations.join('; ')}`);
    console.log(`Elementor Widgets: ${JSON.stringify(r.elementorWidgets)}`);
    console.log('-'.repeat(80));
  }

  console.log(`\nScreenshots saved to: ${outDir}`);
  console.log(`Raw JSON saved to: ${path.join(outDir, 'audit-cluster2-raw.json')}`);
}

main().catch(console.error);
