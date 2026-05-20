#!/usr/bin/env node
/**
 * Homepage Visual Audit v2 — Desktop + Mobile + Detailed Overlap Check
 */
const puppeteer = require('puppeteer');

async function audit(viewport) {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.setViewport(viewport);
  
  await page.goto('https://suriota.com', { waitUntil: 'networkidle2', timeout: 60000 });
  await new Promise(r => setTimeout(r, 3000));
  
  const results = await page.evaluate((vpName) => {
    const findings = [];
    function log(issue, detail, severity = 'info') { findings.push({ issue, detail, severity, viewport: vpName }); }
    
    // 1. Entry title
    const entryTitle = document.querySelector('.entry-title');
    if (entryTitle) {
      const s = window.getComputedStyle(entryTitle);
      const hidden = s.display === 'none' || s.visibility === 'hidden' || s.opacity === '0';
      log('Entry title', hidden ? 'Hidden ✅' : `VISIBLE (${s.display}, ${s.visibility}, ${s.opacity}) ❌`, hidden ? 'success' : 'warning');
    } else {
      log('Entry title', 'Element not found', 'warning');
    }
    
    // 2. Button shapes
    const btns = Array.from(document.querySelectorAll('a.elementor-button, .elementor-button, button.elementor-button'));
    const stats = { pill:0, normal:0, square:0 };
    btns.forEach(b => {
      const s = window.getComputedStyle(b);
      const r = parseFloat(s.borderRadius);
      const h = b.getBoundingClientRect().height;
      if (r >= h/2) stats.pill++;
      else if (r > 4) stats.normal++;
      else stats.square++;
    });
    log('Buttons', `${btns.length} total — Pill: ${stats.pill}, Rounded: ${stats.normal}, Square: ${stats.square}`);
    
    // 3. Product images
    const imgs = Array.from(document.querySelectorAll('img'));
    let visible = 0, hidden = 0, zero = 0;
    imgs.forEach(img => {
      const r = img.getBoundingClientRect();
      const s = window.getComputedStyle(img);
      if (s.display === 'none' || s.visibility === 'hidden') hidden++;
      else if (r.width === 0 || r.height === 0) zero++;
      else visible++;
    });
    log('Images', `Total ${imgs.length} — Visible: ${visible}, Hidden: ${hidden}, Zero-size: ${zero}`, visible === imgs.length ? 'success' : 'warning');
    
    // 4. Overlap detection (simplified bounding-box intersection)
    const sections = Array.from(document.querySelectorAll('.elementor-section, .elementor-container'));
    let overlaps = 0;
    for (let i = 0; i < sections.length; i++) {
      const r1 = sections[i].getBoundingClientRect();
      if (r1.height < 5) continue;
      for (let j = i+1; j < sections.length; j++) {
        const r2 = sections[j].getBoundingClientRect();
        if (r2.height < 5) continue;
        const intersect = !(r2.left > r1.right || r2.right < r1.left || r2.top > r1.bottom || r2.bottom < r1.top);
        if (intersect && Math.abs(r1.top - r2.top) < 5 && r1.height > 50 && r2.height > 50) {
          overlaps++;
          if (overlaps <= 3) log('Overlap', `Section ${i} and ${j} may overlap at Y≈${Math.round(r1.top)}`, 'warning');
        }
      }
    }
    if (overlaps > 3) log('Overlaps', `${overlaps} potential overlaps detected`, 'warning');
    else if (overlaps === 0) log('Overlaps', 'No obvious section overlaps ✅', 'success');
    
    // Horizontal overflow
    const overflow = document.documentElement.scrollWidth > window.innerWidth + 2;
    log('Overflow', overflow ? `Scroll ${document.documentElement.scrollWidth} > viewport ${window.innerWidth} ❌` : 'No horizontal overflow ✅', overflow ? 'warning' : 'success');
    
    // 5. Footer
    const footer = document.querySelector('footer, .elementor-footer, #footer, .site-footer');
    if (footer) {
      const rect = footer.getBoundingClientRect();
      log('Footer', `<footer> found — height ${Math.round(rect.height)}px, links: ${footer.querySelectorAll('a').length}`, 'success');
    } else {
      const copyright = Array.from(document.querySelectorAll('section, div')).find(el => /©|copyright|all rights/i.test(el.innerText));
      log('Footer', copyright ? `No <footer> tag; copyright text in ${copyright.tagName}` : 'No footer or copyright found ❌', copyright ? 'info' : 'warning');
    }
    
    // 6. Heading fonts
    const h1s = document.querySelectorAll('h1');
    if (h1s.length === 1) log('H1', `Single H1: "${h1s[0].innerText.trim().substring(0,50)}" ✅`, 'success');
    else log('H1', `${h1s.length} H1 elements — ${Array.from(h1s).map(h=>h.innerText.trim().substring(0,30)).join(' | ')} ❌`, 'warning');
    
    const h2s = Array.from(document.querySelectorAll('h2')).slice(0, 5);
    h2s.forEach(h => {
      const s = window.getComputedStyle(h);
      log('H2 font', `"${h.innerText.trim().substring(0,40)}" — ${s.fontFamily.split(',')[0]}, ${s.fontSize}, weight ${s.fontWeight}`);
    });
    
    // Check for text truncation / clipping
    const headings = Array.from(document.querySelectorAll('h1, h2, h3'));
    let clipped = 0;
    headings.forEach(h => {
      const r = h.getBoundingClientRect();
      const s = window.getComputedStyle(h);
      if (s.overflow === 'hidden' && h.scrollHeight > r.height + 2) {
        clipped++;
        if (clipped <= 2) log('Clipped text', `"${h.innerText.substring(0,40)}" scrollHeight ${h.scrollHeight} > rect ${r.height}`, 'warning');
      }
    });
    if (clipped > 2) log('Clipped text', `${clipped} headings may be clipped`, 'warning');
    
    return findings;
  }, viewport.label);
  
  await browser.close();
  return results;
}

(async () => {
  const desktop = await audit({ width: 1920, height: 1080, label: 'Desktop' });
  const mobile = await audit({ width: 375, height: 812, label: 'Mobile' });
  const all = [...desktop, ...mobile];
  
  console.log('\n' + '='.repeat(70));
  console.log('  HOMEPAGE AUDIT — https://suriota.com');
  console.log('='.repeat(70) + '\n');
  
  all.forEach(r => {
    const icon = r.severity === 'success' ? '✅' : r.severity === 'warning' ? '⚠️' : 'ℹ️';
    console.log(`${icon} [${r.viewport}] ${r.issue}`);
    console.log(`   ${r.detail}\n`);
  });
  
  const warnings = all.filter(r => r.severity === 'warning').length;
  const success = all.filter(r => r.severity === 'success').length;
  console.log('='.repeat(70));
  console.log(`SUMMARY: ${success} checks passed, ${warnings} warnings`);
  console.log('='.repeat(70));
})();
