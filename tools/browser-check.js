// Load every chapters/ page on GitHub in a real browser engine and check that all math rendered.
//
// Usage:
//   (cd tools && npm install && npx playwright install chromium webkit)
//   node tools/browser-check.js [chromium|webkit] [branch]
//
// For each page this reports how many <math-renderer> expressions GitHub produced, how many
// MathJax rendered, how many failed ("Unable to render expression", disallowed macros), and
// how many inline expressions are clipped with a scrollbar (the Safari table-cell issue), and
// how many MathML features Chrome cannot render (<mlabeledtr> from \tag; mathvariant fonts), and
// how many expressions are laid out out of order (Chrome's stretchy-fence bug).
const { chromium, webkit } = require('playwright');
const fs = require('fs');
const path = require('path');

const engine = process.argv[2] === 'webkit' ? webkit : chromium;
const branch = process.argv[3] || 'main';
const repo = 'robominds/navigation-filter-best-practices';
const dir = path.join(__dirname, '..', 'chapters');

(async () => {
  const browser = await engine.launch();
  let failures = 0;
  for (const f of fs.readdirSync(dir).filter((n) => /^\d.*\.md$/.test(n)).sort()) {
    const page = await browser.newPage({ viewport: { width: 1300, height: 1000 } });
    for (let attempt = 1; ; attempt++) {  // GitHub occasionally stalls; retry slow loads
      try {
        await page.goto(`https://github.com/${repo}/blob/${branch}/chapters/${f}`, { waitUntil: 'networkidle', timeout: 90000 });
        break;
      } catch (err) {
        if (attempt === 3) throw err;
      }
    }
    for (let i = 0; i < 80; i++) { await page.mouse.wheel(0, 2500); await page.waitForTimeout(120); }
    await page.waitForTimeout(4000);
    const r = await page.evaluate(() => {
      const els = [...document.querySelectorAll('math-renderer')];
      let ok = 0, bad = 0, clipped = 0, misordered = 0, first = '';
      // Chrome's native MathML cannot lay out <mlabeledtr> (\tag) and ignores mathvariant (\mathbf etc.).
      const chromeUnsupported = document.querySelectorAll('math-renderer mlabeledtr, math-renderer [mathvariant]:not([mathvariant="normal"])').length;
      for (const e of els) {
        const t = e.innerText || '';
        if (/Unable to render|not allowed/.test(t)) { bad++; first = first || t.slice(0, 100); }
        else if (e.querySelector('mjx-container, svg, math')) ok++;
        if (e.classList.contains('js-inline-math') && e.scrollWidth > e.clientWidth + 1) clipped++;
        // Out-of-order layout: children of an <mrow> drawn right-to-left (a Chrome MathML bug).
        for (const row of e.querySelectorAll('mrow, math')) {
          const boxes = [...row.children].map((k) => k.getBoundingClientRect()).filter((b) => b.width > 0);
          if (boxes.some((b, i) => i > 0 && b.left < boxes[i - 1].left - 2)) { misordered++; break; }
        }
      }
      return { total: els.length, ok, bad, clipped, misordered, chromeUnsupported, first };
    });
    const pass = r.ok === r.total && r.bad === 0 && r.clipped === 0 && r.misordered === 0 && r.chromeUnsupported === 0;
    failures += !pass;
    console.log(`${pass ? 'ok  ' : 'FAIL'} ${f}: ${r.ok}/${r.total} rendered, ${r.bad} failed, ${r.clipped} clipped, ${r.misordered} misordered, ${r.chromeUnsupported} Chrome-unsupported MathML ${r.first}`);
    await page.close();
  }
  await browser.close();
  process.exit(failures ? 1 : 0);
})();
