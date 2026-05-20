#!/usr/bin/env node
/**
 * Batch Backup Script for Suriota Website
 * Usage: node scripts/backup-all.js
 */
const https = require('https');
const fs = require('fs');
const path = require('path');

const CONFIG = {
  site: 'https://suriota.com',
  user: 'admin',
  pass: 'hCYK JqF1 khdB WDzI LQdQ WEBr',
  backupDir: path.join(__dirname, '..', 'backups')
};

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
}

function fetchJson(urlPath) {
  return new Promise((resolve, reject) => {
    const url = new URL(urlPath, CONFIG.site);
    const auth = Buffer.from(`${CONFIG.user}:${CONFIG.pass}`).toString('base64');
    const options = {
      hostname: url.hostname,
      port: url.port || 443,
      path: url.pathname + url.search,
      method: 'GET',
      headers: { 'Authorization': `Basic ${auth}`, 'Content-Type': 'application/json' }
    };
    https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); } catch(e) { resolve(data); }
      });
    }).on('error', reject).end();
  });
}

async function backup() {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const dir = path.join(CONFIG.backupDir, timestamp);
  ensureDir(dir);

  console.log(`[${timestamp}] Starting backup to ${dir}...`);

  // Pages
  const pages = await fetchJson('/wp-json/wp/v2/pages?per_page=100');
  fs.writeFileSync(path.join(dir, 'pages.json'), JSON.stringify(pages, null, 2));
  console.log(`  Pages: ${pages.length}`);

  // Posts
  const posts = await fetchJson('/wp-json/wp/v2/posts?per_page=100');
  fs.writeFileSync(path.join(dir, 'posts.json'), JSON.stringify(posts, null, 2));
  console.log(`  Posts: ${posts.length}`);

  // Media
  const media = await fetchJson('/wp-json/wp/v2/media?per_page=100');
  fs.writeFileSync(path.join(dir, 'media.json'), JSON.stringify(media, null, 2));
  console.log(`  Media: ${media.length}`);

  // Elementor globals
  try {
    const globals = await fetchJson('/wp-json/elementor/v1/globals');
    fs.writeFileSync(path.join(dir, 'elementor_globals.json'), JSON.stringify(globals, null, 2));
    console.log('  Elementor globals: OK');
  } catch(e) { console.log('  Elementor globals: FAILED'); }

  // Templates
  try {
    const templates = await fetchJson('/wp-json/wp/v2/elementor_library?per_page=100');
    fs.writeFileSync(path.join(dir, 'elementor_templates.json'), JSON.stringify(templates, null, 2));
    console.log(`  Templates: ${templates.length}`);
  } catch(e) { console.log('  Templates: FAILED'); }

  // Site info
  const info = await fetchJson('/wp-json/');
  fs.writeFileSync(path.join(dir, 'site_info.json'), JSON.stringify(info, null, 2));

  console.log(`Backup complete: ${dir}`);
  return { dir, pages: pages.length, posts: posts.length, media: media.length };
}

backup().catch(console.error);
