#!/usr/bin/env node
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  const outDir = path.join(__dirname, '..', 'screenshots', '2026-05-14-verify');
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
  
  await page.setViewport({ width: 1920, height: 1080 });
  await page.goto('https://suriota.com', { waitUntil: 'networkidle2', timeout: 60000 });
  await new Promise(r => setTimeout(r, 3000));
  await page.screenshot({ path: path.join(outDir, 'homepage-desktop-audit.png'), fullPage: true });
  
  await page.setViewport({ width: 375, height: 812 });
  await new Promise(r => setTimeout(r, 1000));
  await page.screenshot({ path: path.join(outDir, 'homepage-mobile-audit.png'), fullPage: true });
  
  await browser.close();
  console.log(`Screenshots saved to ${outDir}`);
})();
