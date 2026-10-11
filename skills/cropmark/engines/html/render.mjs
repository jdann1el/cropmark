// cropmark HTML engine (MIT). Usage: node render.mjs page.html outDir [scale]
// Every <section class="frame" id="..."> becomes one PNG. Frames with data-slices="N"
// (a wide panorama, e.g. width 5400px for 5 slides) are cut into N equal PNGs.
// All bundled fonts are injected as @font-face: family = file stem (e.g. "Anton-Regular", "InstrumentSerif-Italic").
import { chromium } from 'playwright';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { mkdirSync, readdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';
const here = path.dirname(fileURLToPath(import.meta.url));
const fontsDir = path.resolve(here, '../../fonts');
const [html, out = 'out', scale = '1'] = process.argv.slice(2);
if (!html) { console.error('usage: node render.mjs page.html outDir [scale]'); process.exit(1); }
mkdirSync(out, { recursive: true });
const css = readdirSync(fontsDir).filter(f => /\.(ttf|otf|woff2?)$/.test(f))
  .map(f => `@font-face{font-family:"${f.replace(/\.[^.]+$/, '')}";src:url("${pathToFileURL(path.join(fontsDir, f)).href}")}`).join('\n');
// CHROME_PATH: use an already-installed Chromium/headless_shell when `npx playwright install` is not possible.
import { existsSync } from 'node:fs';
import os from 'node:os';
async function launch() {
  if (process.env.CHROME_PATH) return chromium.launch({ executablePath: process.env.CHROME_PATH });
  try { return await chromium.launch(); } catch (e) {
    // fallback: any browser already in the Playwright cache (version mismatch after npm i is common)
    const cache = process.env.PLAYWRIGHT_BROWSERS_PATH || path.join(os.homedir(), process.platform === 'darwin' ? 'Library/Caches/ms-playwright' : '.cache/ms-playwright');
    const cands = existsSync(cache) ? readdirSync(cache).sort().reverse().flatMap(d => [
      path.join(cache, d, 'chrome-linux', 'headless_shell'), path.join(cache, d, 'chrome-headless-shell-linux64', 'chrome-headless-shell'),
      path.join(cache, d, 'chrome-linux', 'chrome'), path.join(cache, d, 'chrome-mac', 'headless_shell'),
      path.join(cache, d, 'chrome-headless-shell-mac-arm64', 'chrome-headless-shell')]) : [];
    for (const c of cands) if (existsSync(c)) { try { console.warn('using cached browser ' + c); return await chromium.launch({ executablePath: c }); } catch {} }
    throw e;
  }
}
const browser = await launch();
const page = await browser.newPage({ viewport: { width: 1400, height: 1600 }, deviceScaleFactor: +scale });
await page.goto(pathToFileURL(path.resolve(html)).href, { waitUntil: 'networkidle' });
await page.addStyleTag({ content: css });
await page.evaluate(async () => {
  await document.fonts.ready;
  await Promise.all([...document.fonts].filter(f => f.status === 'unloaded').map(f => f.load().catch(() => {})));
  await document.fonts.ready;
  const bad = [...document.fonts].filter(f => f.status === 'error');
  if (bad.length) throw new Error('font failed: ' + bad.map(f => f.family).join(', '));
  await Promise.all([...document.images].map(i => i.decode().catch(() => {})));
});
const report = [];
const frames = await page.$$('.frame');
let n = 0;
for (const [i, el] of frames.entries()) {
  const id = (await el.getAttribute('id')) ?? `frame-${i + 1}`;
  const info = await el.evaluate(node => {
    const r = node.getBoundingClientRect();
    // overflow only matters for text: flag text nodes that end outside the frame (bleed images are fine)
    const tw = document.createTreeWalker(node, NodeFilter.SHOW_TEXT);
    const boxes = []; let over = false; let t;
    while ((t = tw.nextNode())) {
      if (!t.textContent.trim()) continue;
      const el = t.parentElement; const cs = getComputedStyle(el);
      if (cs.visibility === 'hidden' || cs.display === 'none' || +cs.opacity === 0) continue;
      const rg = document.createRange(); rg.selectNodeContents(t);
      const rs = [...rg.getClientRects()]; if (!rs.length) continue;  // tight glyph-line boxes, not the element box
      const x0 = Math.min(...rs.map(q => q.left)), y0 = Math.min(...rs.map(q => q.top)), x1 = Math.max(...rs.map(q => q.right)), y1 = Math.max(...rs.map(q => q.bottom));
      const role = el.closest('[data-role]')?.dataset.role || 'text';
      const b = [x0 - r.left, y0 - r.top, x1 - r.left, y1 - r.top].map(Math.round);
      if (role !== 'bleed' && (b[0] < -1 || b[1] < -1 || b[2] > r.width + 1 || b[3] > r.height + 1)) over = true;
      let bgEl = el, bg = null;  // nearest opaque background colour, used by QA as the true background when present
      while (bgEl && bgEl !== node.parentElement) { const c = getComputedStyle(bgEl).backgroundColor; if (c && !c.endsWith(', 0)') && c !== 'transparent' && !getComputedStyle(bgEl).backgroundImage.includes('url')) { bg = c; break; } if (getComputedStyle(bgEl).backgroundImage !== 'none') break; bgEl = bgEl.parentElement; }
      boxes.push({ text: t.textContent.trim().slice(0, 60), box: b, color: cs.color, bg, size: parseFloat(cs.fontSize), role });
    }
    return { w: r.width, h: r.height, over, boxes, slices: +(node.dataset.slices || 1) };
  });
  if (info.over) console.warn(`WARN frame ${id}: some text ends outside the frame (mark intentional bleed with data-role="bleed")`);
  const box = await el.boundingBox();
  const sw = box.width / info.slices;
  for (let s = 0; s < info.slices; s++) {
    n++;
    const name = info.slices > 1 ? `${id}-${s + 1}` : id;
    const file = `${out}/${String(n).padStart(2, '0')}-${name}.png`;
    await page.screenshot({ path: file, clip: { x: box.x + s * sw, y: box.y, width: sw, height: box.height }, fullPage: true });
    const bx = info.boxes.filter(b => b.box[2] > s * sw && b.box[0] < (s + 1) * sw)
      .map(b => ({ ...b, box: [b.box[0] - s * sw, b.box[1], b.box[2] - s * sw, b.box[3]] }));
    writeFileSync(file + '.boxes.json', JSON.stringify({ size: [sw * +scale, box.height * +scale], boxes: bx }, null, 1));
    report.push(file);
  }
}
await browser.close();
console.log(`rendered ${report.length} png -> ${out}/`);
