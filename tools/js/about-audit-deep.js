#!/usr/bin/env node
/**
 * Deep About Us Audit — precise selectors
 */
const { chromium } = require('playwright');

const URL = 'https://suriota.com/about-us/';

async function audit() {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1920, height: 1080 });
  await page.goto(URL, { waitUntil: 'networkidle' });
  await page.waitForTimeout(3000);

  // Screenshot full page
  const fs = require('fs');
  const path = require('path');
  const outDir = path.join(__dirname, '..', 'screenshots', '2026-05-14-audit');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
  await page.screenshot({ path: path.join(outDir, 'about-desktop.png'), fullPage: true });

  const r = await page.evaluate(() => {
    const out = {
      entryTitle: null,
      buttons: [],
      stats: null,
      visionMission: null,
      fourFocus: null,
      maknaLogo: null,
      cta: null,
      headingFonts: {},
      cards: [],
      layoutIssues: []
    };

    // 1. Entry title
    const et = document.querySelector('.entry-title');
    out.entryTitle = et ? {
      display: getComputedStyle(et).display,
      hidden: getComputedStyle(et).display === 'none'
    } : 'missing';

    // 2. All buttons with computed styles
    document.querySelectorAll('a, button').forEach(el => {
      const txt = el.innerText.trim();
      if (!txt || txt.length > 60) return;
      const cs = getComputedStyle(el);
      // Only include if looks like a button (has bg color or border or role)
      const isBtn = el.tagName === 'BUTTON' || el.getAttribute('role') === 'button' ||
        cs.backgroundColor !== 'rgba(0, 0, 0, 0)' || el.classList.contains('elementor-button');
      if (!isBtn) return;
      const h = parseFloat(cs.height);
      const br = parseFloat(cs.borderRadius);
      out.buttons.push({
        text: txt.slice(0, 40),
        borderRadius: cs.borderRadius,
        height: cs.height,
        pillShaped: br >= h / 2 && h > 0,
        bg: cs.backgroundColor,
        color: cs.color,
        class: el.className.slice(0, 60)
      });
    });

    // 3. Stats — look for numbers / counters / "+" / "Tahun" / "Project"
    const allSections = Array.from(document.querySelectorAll('.elementor-section, section'));
    const statsSec = allSections.find(s => /\d+\s*\+|Tahun|Project|Klien|Client|Beroperasi/.test(s.innerText));
    if (statsSec) {
      out.stats = {
        text: statsSec.innerText.replace(/\s+/g, ' ').trim().slice(0, 250),
        childCount: statsSec.children.length,
        columns: statsSec.querySelectorAll('.elementor-column').length
      };
    }

    // 4. Vision / Mission
    const vm = allSections.find(s => /VISI KAMI|MISI KAMI|Vision|Mission/i.test(s.innerText));
    if (vm) {
      out.visionMission = {
        text: vm.innerText.replace(/\s+/g, ' ').trim().slice(0, 300),
        headingCount: vm.querySelectorAll('h1,h2,h3').length
      };
    }

    // 5. 4 Bidang Fokus
    const ff = allSections.find(s => /4 Bidang Fokus|Elektrikal.*Otomasi.*Water Treatment.*Energi Terbarukan/s.test(s.innerText.replace(/\s+/g, ' ')));
    if (ff) {
      const cards = ff.querySelectorAll('.elementor-column, [class*="card"]');
      out.fourFocus = {
        text: ff.innerText.replace(/\s+/g, ' ').trim().slice(0, 300),
        cardCount: cards.length,
        cards: Array.from(cards).map(c => {
          const cs = getComputedStyle(c);
          return {
            bg: cs.backgroundColor,
            radius: cs.borderRadius,
            shadow: cs.boxShadow !== 'none' ? 'yes' : 'no',
            padding: cs.padding
          };
        }).slice(0, 6)
      };
    }

    // 6. Makna Logo
    const ml = allSections.find(s => /Makna Logo|Surya|Inovasi|Prioritas|Teknologi/s.test(s.innerText.replace(/\s+/g, ' ')));
    if (ml) {
      const cards = ml.querySelectorAll('.elementor-column, [class*="card"]');
      out.maknaLogo = {
        text: ml.innerText.replace(/\s+/g, ' ').trim().slice(0, 300),
        cardCount: cards.length,
        cards: Array.from(cards).map(c => {
          const cs = getComputedStyle(c);
          return {
            bg: cs.backgroundColor,
            radius: cs.borderRadius,
            shadow: cs.boxShadow !== 'none' ? 'yes' : 'no'
          };
        }).slice(0, 6)
      };
    }

    // 7. CTA Section
    const cta = allSections.find(s => /Siap Berkolaborasi|Hubungi|Consulting Engineering/i.test(s.innerText));
    if (cta) {
      out.cta = {
        text: cta.innerText.replace(/\s+/g, ' ').trim().slice(0, 200),
        bg: getComputedStyle(cta).backgroundColor
      };
    }

    // 8. Heading font families
    document.querySelectorAll('h1, h2, h3').forEach(h => {
      const fam = getComputedStyle(h).fontFamily;
      const tag = h.tagName;
      if (!out.headingFonts[tag]) out.headingFonts[tag] = {};
      out.headingFonts[tag][fam] = (out.headingFonts[tag][fam] || 0) + 1;
    });

    // 9. All white-background cards with radius/shadow
    document.querySelectorAll('.elementor-column, .elementor-widget-wrap, .elementor-widget-container, div').forEach(el => {
      const cs = getComputedStyle(el);
      const bg = cs.backgroundColor;
      const isWhite = bg === 'rgb(255, 255, 255)' || bg === 'rgba(255, 255, 255, 1)';
      const r = parseFloat(cs.borderRadius);
      const hasShadow = cs.boxShadow && cs.boxShadow !== 'none';
      if (isWhite && (r > 4 || hasShadow)) {
        // Only keep if it looks like a content card (has some padding, reasonable size)
        const rect = el.getBoundingClientRect();
        if (rect.width > 80 && rect.height > 40) {
          out.cards.push({
            tag: el.tagName,
            class: el.className.slice(0, 80),
            bg,
            radius: cs.borderRadius,
            shadow: hasShadow ? cs.boxShadow.slice(0, 40) : 'none',
            width: Math.round(rect.width),
            height: Math.round(rect.height)
          });
        }
      }
    });

    // 10. Overlap / overflow check
    const bodyW = document.body.scrollWidth;
    if (bodyW > window.innerWidth) {
      out.layoutIssues.push(`Body scrollWidth (${bodyW}px) exceeds viewport (${window.innerWidth}px)`);
    }

    return out;
  });

  // Mobile screenshot
  await page.setViewportSize({ width: 375, height: 812 });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: path.join(outDir, 'about-mobile.png'), fullPage: true });

  const mobile = await page.evaluate(() => {
    const issues = [];
    const bodyW = document.body.scrollWidth;
    if (bodyW > window.innerWidth) {
      issues.push(`Body scrollWidth (${bodyW}px) exceeds viewport (${window.innerWidth}px)`);
    }
    document.querySelectorAll('img').forEach(img => {
      if (img.naturalWidth > 0 && img.width > window.innerWidth) {
        issues.push(`Image overflows: ${img.src.split('/').pop()} width=${img.width}px`);
      }
    });
    return { overflowIssues: issues.slice(0, 5), entryTitleHidden: (() => {
      const et = document.querySelector('.entry-title');
      return et ? getComputedStyle(et).display === 'none' : 'missing';
    })() };
  });

  await browser.close();
  return { desktop: r, mobile, screenshots: outDir };
}

audit().then(r => {
  console.log(JSON.stringify(r, null, 2));
}).catch(console.error);
