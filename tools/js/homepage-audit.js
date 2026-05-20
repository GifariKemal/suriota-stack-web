#!/usr/bin/env node
/**
 * Homepage Visual Audit — Puppeteer
 * Checks: entry title, buttons, product images, layouts, footer, headings
 */
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function auditHomepage() {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  
  // Desktop viewport
  await page.setViewport({ width: 1920, height: 1080 });
  
  console.log('Navigating to https://suriota.com ...');
  await page.goto('https://suriota.com', { waitUntil: 'networkidle2', timeout: 60000 });
  await new Promise(r => setTimeout(r, 3000)); // let lazy images / animations settle
  
  const results = await page.evaluate(() => {
    const findings = [];
    
    function log(issue, detail, severity = 'info') {
      findings.push({ issue, detail, severity });
    }
    
    // ── 1. Entry title hidden? ──
    const entryTitle = document.querySelector('.entry-title');
    if (!entryTitle) {
      log('Entry title', 'No .entry-title element found on page', 'warning');
    } else {
      const style = window.getComputedStyle(entryTitle);
      const hidden = style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0';
      log('Entry title', hidden 
        ? '.entry-title is hidden (display:none / visibility:hidden / opacity:0) ✅'
        : `.entry-title is VISIBLE — ${style.display}, visibility:${style.visibility}, opacity:${style.opacity} ❌`,
        hidden ? 'success' : 'warning');
    }
    
    // Also check h1.entry-title specifically
    const h1Entry = document.querySelector('h1.entry-title');
    if (h1Entry) {
      const style = window.getComputedStyle(h1Entry);
      const hidden = style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0';
      log('H1 Entry Title', hidden
        ? 'h1.entry-title is hidden ✅'
        : `h1.entry-title is VISIBLE — display:${style.display} ❌`,
        hidden ? 'success' : 'warning');
    }
    
    // ── 2. Buttons: pill-shaped or normal? ──
    const buttons = Array.from(document.querySelectorAll('a.elementor-button, .elementor-button, button.elementor-button, .btn, a.btn'));
    const buttonStats = { pill: 0, normal: 0, unknown: 0 };
    buttons.forEach((btn, i) => {
      const style = window.getComputedStyle(btn);
      const radius = parseFloat(style.borderRadius);
      const height = btn.getBoundingClientRect().height;
      const isPill = radius >= height / 2;
      if (isPill) buttonStats.pill++;
      else if (radius > 0) buttonStats.normal++;
      else buttonStats.unknown++;
    });
    log('Button shapes', `Found ${buttons.length} buttons — Pill: ${buttonStats.pill}, Normal/rounded: ${buttonStats.normal}, Unknown: ${buttonStats.unknown}`, 'info');
    
    // ── 3. Product images visible & sized? ──
    const images = Array.from(document.querySelectorAll('img'));
    let visibleImages = 0;
    let zeroSizeImages = 0;
    let hiddenImages = 0;
    let productImages = [];
    
    images.forEach(img => {
      const rect = img.getBoundingClientRect();
      const style = window.getComputedStyle(img);
      const isVisible = style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
      
      if (isVisible) visibleImages++;
      else if (style.display === 'none' || style.visibility === 'hidden') hiddenImages++;
      else if (rect.width === 0 || rect.height === 0) zeroSizeImages++;
      
      // Check if it's likely a product/service image
      const src = (img.src || '').toLowerCase();
      const alt = (img.alt || '').toLowerCase();
      const parentClasses = (img.parentElement?.className || '').toLowerCase();
      const isProductLike = src.includes('product') || src.includes('service') || alt.includes('product') || 
                           alt.includes('service') || parentClasses.includes('product') || parentClasses.includes('service') ||
                           parentClasses.includes('portfolio') || parentClasses.includes('item');
      
      if (isProductLike || rect.width > 100) {
        productImages.push({
          src: img.src.substring(0, 100),
          alt: img.alt,
          width: rect.width,
          height: rect.height,
          naturalWidth: img.naturalWidth,
          naturalHeight: img.naturalHeight,
          visible: isVisible,
          parentClass: img.parentElement?.className?.substring(0, 80) || 'none'
        });
      }
    });
    
    log('Image audit', `Total images: ${images.length}, Visible: ${visibleImages}, Hidden: ${hiddenImages}, Zero-size: ${zeroSizeImages}`, 'info');
    
    // List product-like images
    productImages.slice(0, 15).forEach(pi => {
      const ratio = pi.naturalWidth > 0 ? (pi.width / pi.naturalWidth).toFixed(2) : 'N/A';
      const issue = !pi.visible ? 'HIDDEN' : (pi.width < 50 || pi.height < 50 ? 'VERY SMALL' : 'OK');
      log(`Image: ${pi.alt || 'no-alt'}`, `${pi.width}x${pi.height} (natural ${pi.naturalWidth}x${pi.naturalHeight}, ratio ${ratio}) — ${issue}`, 
        issue === 'OK' ? 'success' : 'warning');
    });
    
    // ── 4. Broken layouts / overlapping / missing ──
    // Check for elements with negative margins causing overlap
    const allElements = Array.from(document.querySelectorAll('body *'));
    let overlapSuspects = 0;
    let negativeMarginElements = 0;
    
    allElements.forEach(el => {
      const style = window.getComputedStyle(el);
      const marginTop = parseFloat(style.marginTop);
      const marginBottom = parseFloat(style.marginBottom);
      if (marginTop < -20 || marginBottom < -20) {
        negativeMarginElements++;
        if (negativeMarginElements <= 5) {
          log('Negative margin', `${el.tagName}${el.className ? '.'+el.className.split(' ').slice(0,3).join('.') : ''} marginTop:${marginTop}px marginBottom:${marginBottom}px`, 'warning');
        }
      }
    });
    
    if (negativeMarginElements > 5) {
      log('Negative margins', `Total ${negativeMarginElements} elements with large negative margins (>20px)`, 'warning');
    }
    
    // Check for overflow / horizontal scroll
    const bodyWidth = document.body.scrollWidth;
    const vw = window.innerWidth;
    if (bodyWidth > vw + 5) {
      log('Horizontal overflow', `body.scrollWidth (${bodyWidth}px) > viewport (${vw}px) — possible horizontal scroll ❌`, 'warning');
    } else {
      log('Horizontal overflow', `No horizontal overflow detected ✅`, 'success');
    }
    
    // Check for empty sections (common Elementor issue)
    const sections = Array.from(document.querySelectorAll('.elementor-section'));
    let emptySections = 0;
    sections.forEach((sec, i) => {
      const rect = sec.getBoundingClientRect();
      const hasContent = sec.innerText.trim().length > 0 || sec.querySelector('img, video, iframe, canvas, svg');
      if (!hasContent && rect.height < 10) {
        emptySections++;
      }
    });
    if (emptySections > 0) {
      log('Empty sections', `${emptySections} near-empty sections found`, 'warning');
    }
    
    // ── 5. Footer sections ──
    const footer = document.querySelector('footer') || document.querySelector('.elementor-footer') || 
                   document.querySelector('#footer') || document.querySelector('.site-footer');
    if (!footer) {
      // Try to find footer-like element
      const possibleFooters = Array.from(document.querySelectorAll('section')).filter(s => {
        const text = s.innerText.toLowerCase();
        return text.includes('copyright') || text.includes('©') || text.includes('all rights');
      });
      if (possibleFooters.length > 0) {
        log('Footer', `No <footer> tag, but found ${possibleFooters.length} section(s) with copyright text`, 'info');
      } else {
        log('Footer', 'No footer element or copyright section found ❌', 'warning');
      }
    } else {
      const footerRect = footer.getBoundingClientRect();
      const footerLinks = footer.querySelectorAll('a').length;
      const footerText = footer.innerText.substring(0, 200);
      log('Footer', `Found <footer> — height:${Math.round(footerRect.height)}px, links:${footerLinks}`, 'success');
      log('Footer preview', footerText, 'info');
    }
    
    // ── 6. Heading fonts ──
    const headings = Array.from(document.querySelectorAll('h1, h2, h3, h4, h5, h6'));
    const fontMap = {};
    headings.forEach(h => {
      const style = window.getComputedStyle(h);
      const fontFamily = style.fontFamily;
      const fontSize = style.fontSize;
      const fontWeight = style.fontWeight;
      const key = `${fontFamily} / ${fontSize} / ${fontWeight}`;
      if (!fontMap[key]) fontMap[key] = [];
      if (fontMap[key].length < 3) fontMap[key].push(h.innerText.substring(0, 60));
    });
    
    Object.entries(fontMap).forEach(([key, texts]) => {
      log('Heading font', `${key} — examples: ${texts.join(' | ')}`, 'info');
    });
    
    // Check for heading hierarchy issues
    const h1s = document.querySelectorAll('h1');
    if (h1s.length > 1) {
      log('H1 count', `Multiple H1s found: ${h1s.length} — ${Array.from(h1s).map(h => h.innerText.substring(0,40)).join(' | ')}`, 'warning');
    } else if (h1s.length === 1) {
      log('H1 count', `Single H1: "${h1s[0].innerText.substring(0,60)}" ✅`, 'success');
    } else {
      log('H1 count', 'No H1 found ❌', 'warning');
    }
    
    // ── Bonus: viewport scroll height ──
    log('Page height', `Total scroll height: ${document.body.scrollHeight}px`, 'info');
    
    return findings;
  });
  
  await browser.close();
  return results;
}

auditHomepage()
  .then(results => {
    console.log('\n' + '='.repeat(70));
    console.log('HOMEPAGE VISUAL AUDIT REPORT — https://suriota.com');
    console.log('='.repeat(70) + '\n');
    
    results.forEach(r => {
      const icon = r.severity === 'success' ? '✅' : r.severity === 'warning' ? '⚠️' : 'ℹ️';
      console.log(`${icon} [${r.issue}]`);
      console.log(`   ${r.detail}\n`);
    });
    
    const warnings = results.filter(r => r.severity === 'warning').length;
    const successes = results.filter(r => r.severity === 'success').length;
    console.log('='.repeat(70));
    console.log(`SUMMARY: ${successes} passed, ${warnings} warnings/issues`);
    console.log('='.repeat(70));
  })
  .catch(err => {
    console.error('Audit failed:', err);
    process.exit(1);
  });
