// usage: node test/run_headless.cjs <full|empty|error> <out.json>   (serve the repo root on :8766 first)  — isolated headless run of the office harness
const { chromium } = require(process.env.PLAYWRIGHT_PATH || 'playwright');
(async () => {
  const mode = process.argv[2] || 'full', out = process.argv[3];
  const browser = await chromium.launch({ headless: true, executablePath: process.env.CHROME_PATH || undefined });
  const page = await browser.newPage({ viewport: { width: 1240, height: 900 } });
  const errs = [];
  page.on('pageerror', (e) => errs.push('pageerror: ' + e.message));
  page.on('console', (m) => { if (m.type() === 'error') errs.push('console: ' + m.text()); });
  await page.goto('http://127.0.0.1:8766/test/harness.html?scenario=' + mode + '&r=' + Date.now());
  await page.waitForFunction(() => !!window.__OFFICE_RESULTS__, null, { timeout: 900000, polling: 500 }).catch(async () => { const partial = await page.evaluate(() => Array.from(document.querySelectorAll('#results li, #results div')).slice(-6).map((x) => x.textContent.slice(0, 200))); console.log('TIMEOUT; last lines:', JSON.stringify(partial, null, 1)); console.log('errs', JSON.stringify(errs)); await browser.close(); process.exit(2); });
  const r = await page.evaluate(() => ({ search: location.search, pass: window.__OFFICE_RESULTS__.pass, fail: window.__OFFICE_RESULTS__.fail, lines: window.__OFFICE_RESULTS__.lines, consoleErrors: (window.__consoleErrors__ || []).length, z4dbg: window.__z4dbg || null, trace: window.__z4trace || null }));
  r.pageErrors = errs;
  require('fs').writeFileSync(out, JSON.stringify(r, null, 1));
  console.log(mode, 'pass', r.pass, 'fail', r.fail, 'console', r.consoleErrors, 'pageErrors', errs.length);
  r.lines.filter((l) => /\(z|✘/.test(l)).forEach((l) => console.log(l.slice(0, 300)));
  if (r.z4dbg) console.log(JSON.stringify(r.z4dbg));
  await browser.close();
})().catch((e) => { console.error('RUNNER ERROR', e.message); process.exit(1); });
