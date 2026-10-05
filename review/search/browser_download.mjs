// Browser pass (Playwright + pre-installed Chromium): for OA papers still missing, open each OA landing page,
// capture any PDF response, or follow the first PDF-looking link. Keeps only real PDFs (%PDF magic).
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PW_PATH || 'playwright');
import fs from 'fs';

const oa = JSON.parse(fs.readFileSync('data/oa_status.json', 'utf8'));
const log = Object.fromEntries(JSON.parse(fs.readFileSync('data/download_log.json', 'utf8')).map(r => [r.n, r]));
const isPdf = b => b && b.length > 4 && b.subarray(0, 4).toString() === '%PDF';
const pad = n => String(n).padStart(2, '0');

const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome', args: ['--no-sandbox'] })
  .catch(() => chromium.launch({ args: ['--no-sandbox'] }));
const ctx = await browser.newContext({ acceptDownloads: true, ignoreHTTPSErrors: false,
  userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0 Safari/537.36' });

async function tryUrl(url, fn) {
  const page = await ctx.newPage();
  let got = null;
  page.on('response', async r => {
    try { if (!got && (r.headers()['content-type'] || '').includes('pdf')) { const b = await r.body(); if (isPdf(b)) got = b; } } catch {}
  });
  const dl = page.waitForEvent('download', { timeout: 40000 }).then(async d => { const p = await d.path(); const b = fs.readFileSync(p); if (isPdf(b)) got = b; }).catch(() => {});
  try { await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 }); } catch {}
  if (!got) {  // look for a PDF link on the landing page
    const href = await page.evaluate(() => {
      const a = [...document.querySelectorAll('a[href]')].map(x => x.href)
        .find(h => /\.pdf($|\?)|\/pdf\/?$|\/download\/|ndownloader|bitstream/i.test(h));
      const meta = document.querySelector('meta[name="citation_pdf_url"]');
      return (meta && meta.content) || a || null;
    }).catch(() => null);
    if (href) { try { await page.goto(href, { waitUntil: 'networkidle', timeout: 45000 }); } catch {} }
  }
  await Promise.race([dl, new Promise(r => setTimeout(r, 4000))]);
  await page.close();
  if (got) { fs.writeFileSync(fn, got); return true; }
  return false;
}

for (const o of oa) {
  const r = log[o.n];
  if (r.file || !o.is_oa) continue;
  const fn = `fulltext/${pad(o.n)}.pdf`;
  const urls = [...new Set(o.locations.flatMap(l => [l.url, l.pdf]).filter(Boolean))];
  for (const u of urls) {
    const ok = await tryUrl(u, fn);
    r.tried.push([u, 'browser', ok]);
    if (ok) { r.file = fn; break; }
  }
  console.log(o.n, o.oa_status, r.file ? 'OK' : '--');
}
fs.writeFileSync('data/download_log.json', JSON.stringify(Object.values(log), null, 1));
await browser.close();
console.log('downloaded', Object.values(log).filter(r => r.file).length);
