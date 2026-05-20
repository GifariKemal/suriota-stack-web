#!/usr/bin/env node
/**
 * About Us Page Audit — computed styles & layout check
 */
const { chromium } = require('playwright');

const URL = 'https://suriota.com/about-us/';

async function audit() {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1920, height: 1080 });
  await page.goto(URL, { waitUntil: 'networkidle' });
  await page.waitForTimeout(3000);

  const results = await page.evaluate(() => {
    const r = {
      entryTitle: {},
      buttons: [],
      headings: [],
      statsSection: {},
      visionMission: {},
      servicesSection: {},
      v4Cards: [],
      layoutIssues: [],
      missing: []
    };

    // 1. Entry title hidden?
    const entryTitle = document.querySelector('.entry-title');
    if (!entryTitle) {
      r.missing.push('.entry-title element not found in DOM');
    } else {
      const cs = getComputedStyle(entryTitle);
      r.entryTitle = {
        display: cs.display,
        visibility: cs.visibility,
        opacity: cs.opacity,
        height: cs.height,
        hidden: cs.display === 'none' || cs.visibility === 'hidden' || cs.opacity === '0'
      };
    }

    // 2. Buttons shape
    const allBtns = document.querySelectorAll('.elementor-button, button, .btn, a[role="button"]');
    allBtns.forEach((b, i) => {
      if (i > 20) return;
      const cs = getComputedStyle(b);
      const br = parseFloat(cs.borderRadius);
      const h = parseFloat(cs.height);
      r.buttons.push({
        text: b.innerText.trim().slice(0, 40),
        borderRadius: cs.borderRadius,
        height: cs.height,
        pillShaped: br >= h / 2 && h > 0,
        backgroundColor: cs.backgroundColor,
        color: cs.color
      });
    });

    // 3. Check for overlaps / broken layout (simplified: elements with negative margins or extremely large z-index conflicts)
    // Also check if any section has 0 height
    document.querySelectorAll('section, .elementor-section').forEach((sec, idx) => {
      const rect = sec.getBoundingClientRect();
      const cs = getComputedStyle(sec);
      if (rect.height < 5 && rect.width > 100) {
        r.layoutIssues.push(`Section #${idx} near y=${Math.round(rect.top)} has near-zero height (${Math.round(rect.height)}px)`);
      }
    });

    // 4a. Stats section
    const statsSec = document.querySelector('.elementor-section:has(.elementor-counter), .elementor-section:has([class*="stat"])') ||
                     Array.from(document.querySelectorAll('.elementor-section')).find(s => s.innerText.includes('Tahun') && s.innerText.includes('Project'));
    if (statsSec) {
      const counters = statsSec.querySelectorAll('.elementor-counter, .elementor-heading-title');
      r.statsSection = {
        found: true,
        textPreview: statsSec.innerText.replace(/\s+/g, ' ').trim().slice(0, 200),
        counterCount: counters.length
      };
    } else {
      r.statsSection = { found: false };
      r.missing.push('Stats section not found');
    }

    // 4b. Vision / Mission
    const vm = Array.from(document.querySelectorAll('.elementor-section')).find(s =>
      /vision|misi|visi/i.test(s.innerText)
    );
    if (vm) {
      r.visionMission = {
        found: true,
        textPreview: vm.innerText.replace(/\s+/g, ' ').trim().slice(0, 200)
      };
    } else {
      r.visionMission = { found: false };
      r.missing.push('Vision/Mission section not found');
    }

    // 4c. Services / 4 Bidang Fokus
    const svc = Array.from(document.querySelectorAll('.elementor-section')).find(s =>
      /bidang|fokus|layanan|service/i.test(s.innerText)
    );
    if (svc) {
      r.servicesSection = {
        found: true,
        textPreview: svc.innerText.replace(/\s+/g, ' ').trim().slice(0, 300),
        cardCount: svc.querySelectorAll('.elementor-column').length
      };
    } else {
      r.servicesSection = { found: false };
      r.missing.push('Services/4 Bidang section not found');
    }

    // 5. Heading fonts
    document.querySelectorAll('h1, h2, h3').forEach((h, i) => {
      if (i > 15) return;
      const cs = getComputedStyle(h);
      r.headings.push({
        tag: h.tagName,
        text: h.innerText.trim().slice(0, 50),
        fontFamily: cs.fontFamily,
        fontSize: cs.fontSize,
        fontWeight: cs.fontWeight,
        lineHeight: cs.lineHeight,
        color: cs.color
      });
    });

    // 6. V4 leftover cards: white bg + rounded corners + shadows
    document.querySelectorAll('.elementor-column, .elementor-widget-wrap, .elementor-widget-container').forEach((el, i) => {
      if (i > 100) return;
      const cs = getComputedStyle(el);
      const bg = cs.backgroundColor;
      const hasWhiteBg = bg === 'rgb(255, 255, 255)' || bg === 'rgba(255, 255, 255, 1)';
      const hasRadius = parseFloat(cs.borderRadius) > 8;
      const hasShadow = cs.boxShadow && cs.boxShadow !== 'none';
      if (hasWhiteBg && (hasRadius || hasShadow)) {
        r.v4Cards.push({
          tag: el.tagName,
          class: el.className.slice(0, 80),
          backgroundColor: bg,
          borderRadius: cs.borderRadius,
          boxShadow: cs.boxShadow.slice(0, 60)
        });
      }
    });

    return r;
  });

  // Mobile check
  await page.setViewportSize({ width: 375, height: 812 });
  await page.waitForTimeout(1500);

  const mobile = await page.evaluate(() => {
    const issues = [];
    document.querySelectorAll('.elementor-section').forEach((sec, idx) => {
      const rect = sec.getBoundingClientRect();
      if (rect.width > 400) {
        issues.push(`Section #${idx} overflows viewport: width=${Math.round(rect.width)}px`);
      }
    });
    // Check entry title on mobile
    const et = document.querySelector('.entry-title');
    return {
      entryTitleHidden: et ? (getComputedStyle(et).display === 'none' || getComputedStyle(et).visibility === 'hidden') : 'not found',
      overflowIssues: issues.slice(0, 5)
    };
  });

  await browser.close();
  return { desktop: results, mobile };
}

audit().then(r => {
  console.log(JSON.stringify(r, null, 2));
}).catch(console.error);
