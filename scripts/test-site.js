#!/usr/bin/env node
// Pre-delivery site check. Usage: node scripts/test-site.js <url> [client-slug]
// Tests: load, console errors, broken links, mobile overflow, forms, basic SEO.
// With a client slug, saves report and screenshots to projects/<slug>/02-work/test-report/.
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const url = process.argv[2];
const slug = process.argv[3];
if (!url || !/^https?:\/\//.test(url)) {
  console.error('Usage: node scripts/test-site.js <https://url> [client-slug]');
  process.exit(1);
}

const outDir = slug
  ? path.join(__dirname, '..', 'projects', slug, '02-work', 'test-report')
  : path.join(process.cwd(), 'test-report');

(async () => {
  fs.mkdirSync(outDir, { recursive: true });
  const browser = await chromium.launch();
  const rows = [];
  const add = (check, ok, detail) => rows.push({ check, ok, detail });

  const consoleErrors = [];
  const failedRequests = [];
  const ctx = await browser.newContext({ viewport: { width: 1366, height: 800 } });
  const page = await ctx.newPage();
  page.on('console', (m) => m.type() === 'error' && consoleErrors.push(m.text().slice(0, 160)));
  page.on('requestfailed', (r) => failedRequests.push(`${r.url().slice(0, 100)} (${r.failure()?.errorText})`));

  const t0 = Date.now();
  let resp;
  try {
    resp = await page.goto(url, { waitUntil: 'load', timeout: 45000 });
  } catch (e) {
    add('Page loads', false, e.message.split('\n')[0]);
  }
  const loadMs = Date.now() - t0;
  if (resp) {
    add('Page loads', resp.ok(), `HTTP ${resp.status()}`);
    add('Load speed under 3s', loadMs < 3000, `${(loadMs / 1000).toFixed(1)}s`);
    add('Uses HTTPS', page.url().startsWith('https://'), page.url());
    await page.screenshot({ path: path.join(outDir, 'desktop.png'), fullPage: true });

    const info = await page.evaluate(() => ({
      title: document.title,
      desc: document.querySelector('meta[name=description]')?.content || '',
      h1: document.querySelectorAll('h1').length,
      viewport: !!document.querySelector('meta[name=viewport]'),
      noAlt: [...document.images].filter((i) => !i.alt).length,
      forms: [...document.forms].map((f) => ({
        action: f.action,
        fields: f.querySelectorAll('input:not([type=hidden]),textarea,select').length,
        submit: !!f.querySelector('[type=submit],button'),
      })),
      links: [...new Set([...document.querySelectorAll('a[href]')].map((a) => a.href))].filter((h) => /^https?:/.test(h)),
    }));
    add('Page title set', !!info.title, info.title || 'missing');
    add('Meta description set', !!info.desc, info.desc ? `${info.desc.length} chars` : 'missing (hurts SEO)');
    add('Exactly one H1', info.h1 === 1, `${info.h1} found`);
    add('Mobile viewport tag', info.viewport, info.viewport ? 'ok' : 'missing');
    add('Images have alt text', info.noAlt === 0, `${info.noAlt} without alt`);
    add('Console errors', consoleErrors.length === 0, consoleErrors.length ? consoleErrors.slice(0, 3).join(' | ') : 'none');
    add('Failed requests', failedRequests.length === 0, failedRequests.length ? failedRequests.slice(0, 3).join(' | ') : 'none');
    info.forms.forEach((f, i) =>
      add(`Form ${i + 1} has fields and submit button`, f.fields > 0 && f.submit, `${f.fields} fields, action ${f.action || 'none'}. Submit it by hand once.`)
    );
    if (!info.forms.length) add('Forms found', true, 'none on this page');

    // Broken links (first 40)
    const broken = [];
    for (const link of info.links.slice(0, 40)) {
      try {
        let r = await ctx.request.head(link, { timeout: 10000, failOnStatusCode: false });
        if (r.status() >= 400) r = await ctx.request.get(link, { timeout: 10000, failOnStatusCode: false });
        if (r.status() >= 400 && ![401, 403, 429, 999].includes(r.status())) broken.push(`${link} (${r.status()})`);
      } catch (e) {
        broken.push(`${link} (no response)`);
      }
    }
    add(`Broken links (checked ${Math.min(info.links.length, 40)} of ${info.links.length})`, broken.length === 0, broken.length ? broken.join(' | ') : 'none');

    // Mobile
    const mctx = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
    const mp = await mctx.newPage();
    await mp.goto(url, { waitUntil: 'load', timeout: 45000 }).catch(() => {});
    const overflow = await mp.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
    add('Mobile: no sideways scroll', overflow <= 1, overflow > 1 ? `${overflow}px too wide` : 'ok');
    await mp.screenshot({ path: path.join(outDir, 'mobile.png'), fullPage: true });
  }
  await browser.close();

  const pass = rows.filter((r) => r.ok).length;
  const lines = [
    `# Site test: ${url}`,
    `Run: ${new Date().toISOString().slice(0, 10)}. Result: ${pass} of ${rows.length} checks passed.`,
    '',
    '| Check | Result | Detail |',
    '|---|---|---|',
    ...rows.map((r) => `| ${r.check} | ${r.ok ? 'PASS' : 'FAIL'} | ${r.detail.replace(/\|/g, '/')} |`),
    '',
    'Screenshots: desktop.png, mobile.png in this folder.',
    'Not tested automatically: payments, logins, automations, email delivery. Test those by hand.',
  ];
  fs.writeFileSync(path.join(outDir, 'report.md'), lines.join('\n') + '\n');
  console.log(lines.join('\n'));
  console.log(`\nSaved to ${outDir}`);
})();
