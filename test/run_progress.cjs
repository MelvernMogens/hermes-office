// progress-tracing runner (v5.7 debug): prints results line count + last line every 10s
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');
(async () => {
  const mode = process.argv[2] || 'full', lim = +(process.argv[3] || 300);
  const browser = await chromium.launch({ headless: true, executablePath: process.env.CHROME_PATH || undefined });
  const page = await browser.newPage({ viewport: { width: 1240, height: 900 } });
  page.on('pageerror', (e) => console.log('PAGEERR', e.message));
  page.on('console', (m) => { if (m.type() === 'error') console.log('CONSOLEERR', m.text().slice(0, 300)); });
  await page.goto('http://127.0.0.1:8766/test/harness.html?scenario=' + mode + '&r=' + Date.now());
  const t0 = Date.now(); let last = '';
  while ((Date.now() - t0) / 1000 < lim) {
    await page.waitForTimeout(5000);
    const s = await page.evaluate(() => { const r = window.__OFFICE_RESULTS__; const ls = (window.__OFFICE_T__ && window.__OFFICE_T__.lines) || []; return { done: !!r, pass: r && r.pass, fail: r && r.fail, n: ls.length, last: ls.length ? ls[ls.length - 1].slice(0, 160) : '' }; });
    const k = s.n + '|' + s.last; if (k !== last) { console.log(Math.round((Date.now() - t0) / 1000) + 's', JSON.stringify(s)); last = k; }
    if (s.done) { const lines = await page.evaluate(() => window.__OFFICE_RESULTS__.lines.filter((l) => /✘|\(t\d/.test(l))); lines.forEach((l) => console.log(l.slice(0, 400))); break; }
  }
  await browser.close();
})();
