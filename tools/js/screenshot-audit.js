#!/usr/bin/env node
/**
 * Visual Audit Script — Screenshot all key pages
 * Usage: node scripts/screenshot-audit.js
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const PAGES = [
  { name: 'homepage', url: 'https://suriota.com/' },
  { name: 'about', url: 'https://suriota.com/about-us/' },
  { name: 'portfolio', url: 'https://suriota.com/portfolio/' },
  { name: 'automation', url: 'https://suriota.com/automation/' },
  { name: 'electrical', url: 'https://suriota.com/electrical/' },
  { name: 'renewable', url: 'https://suriota.com/renewable-energy/' },
  { name: 'water-treatment', url: 'https://suriota.com/water-treatment/' },
  { name: 'modbus-gateway', url: 'https://suriota.com/suriota-modbus-gateway/' },
  { name: 'internship', url: 'https://suriota.com/internship/' }
];

async function run() {
  const outDir = path.join(__dirname, '..', 'screenshots', new Date().toISOString().split('T')[0]);
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  const browser = await chromium.launch();
  const page = await browser.newPage();

  for (const p of PAGES) {
    try {
      await page.setViewportSize({ width: 1920, height: 1080 });
      await page.goto(p.url, { waitUntil: 'networkidle' });
      await page.waitForTimeout(2500);
      await page.screenshot({ path: path.join(outDir, `${p.name}-desktop.png`), fullPage: true });

      await page.setViewportSize({ width: 375, height: 812 });
      await page.waitForTimeout(1000);
      await page.screenshot({ path: path.join(outDir, `${p.name}-mobile.png`), fullPage: true });

      console.log(`✅ ${p.name}`);
    } catch (e) {
      console.log(`❌ ${p.name}: ${e.message}`);
    }
  }

  await browser.close();
  console.log(`Screenshots saved to: ${outDir}`);
}

run().catch(console.error);
