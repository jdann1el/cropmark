// cropmark HTML engine (MIT). Usage: node render.mjs page.html outDir [scale]
import { chromium } from 'playwright';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { mkdirSync, readdirSync, readFileSync, writeFileSync } from 'node:fs';
import path from 'node:path';
const here = path.dirname(fileURLToPath(import.meta.url));
const fontsDir = path.resolve(here, '../../fonts');
const [html, out = 'out', scaleArg = '1'] = process.argv.slice(2);
const scale = Number(scaleArg);
let browser;
try {
  if (!html) throw new Error('usage: node render.mjs page.html outDir [scale]');
  if (!Number.isFinite(scale) || scale <= 0) throw new Error('scale must be positive and finite');
  const css = readdirSync(fontsDir).filter(f => /\.(ttf|otf|woff2?)$/i.test(f))
    .map(f => `@font-face{font-family:${JSON.stringify(f.replace(/\.[^.]+$/, ''))};src:url(${JSON.stringify(pathToFileURL(path.join(fontsDir, f)).href)})}`).join('\n');
  browser = await chromium.launch(process.env.CHROME_PATH ? { executablePath: process.env.CHROME_PATH } : {});
  const page = await browser.newPage({ viewport: { width: 1400, height: 1600 }, deviceScaleFactor: scale });
  await page.goto(pathToFileURL(path.resolve(html)).href, { waitUntil: 'networkidle' });
  await page.addStyleTag({ content: css });
  // This reserved attribute is only a temporary bridge to Chromium's font report.
  await page.evaluate(() => document.querySelectorAll('[data-cropmark-font-probe]').forEach(el => el.removeAttribute('data-cropmark-font-probe')));
  const frames = await page.$$('.frame');
  if (!frames.length) throw new Error('no .frame elements found');
  await page.evaluate(async () => {
    // Images outside output frames do not affect the exported composition.
    await Promise.all([...document.querySelectorAll('.frame img')].map(async img => {
      try {
        // Eager loading also makes off-screen panorama images ready before capture.
        img.loading = 'eager';
        await img.decode();
        if (!img.naturalWidth || !img.naturalHeight) throw new Error('empty image');
      } catch (error) { throw new Error(`image failed to load/decode: ${img.currentSrc || img.src || '(empty src)'} (${error.message})`); }
    }));
    const backgrounds = new Set();
    for (const el of document.querySelectorAll('.frame, .frame *')) {
      for (const match of getComputedStyle(el).backgroundImage.matchAll(/url\((?:"([^"]*)"|'([^']*)'|([^)]*))\)/g)) {
        backgrounds.add(match[1] ?? match[2] ?? match[3]);
      }
    }
    await Promise.all([...backgrounds].map(async src => {
      const img = new Image(); img.src = src;
      try { await img.decode(); }
      catch (error) { throw new Error(`background image failed to load/decode: ${src} (${error.message})`); }
    }));
    await document.fonts.ready;
  });
  const infos = [];
  const ids = new Set();
  for (const [index, frame] of frames.entries()) {
    const id = (await frame.getAttribute('id')) || `frame-${index + 1}`;
    if (!/^[A-Za-z0-9][A-Za-z0-9_-]*$/.test(id)) throw new Error(`unsafe frame id: ${JSON.stringify(id)} (use letters, digits, _ or -)`);
    if (ids.has(id)) throw new Error(`duplicate frame id: ${id}`);
    ids.add(id);
    const info = await frame.evaluate(async node => {
      const slices = node.hasAttribute('data-slices') ? Number(node.dataset.slices) : 1;
      if (!Number.isSafeInteger(slices) || slices <= 0) throw new Error('data-slices must be a positive integer');
      const r = node.getBoundingClientRect();
      if (![r.x, r.y, r.width, r.height].every(Number.isFinite) || r.x < 0 || r.y < 0 || r.width <= 0 || r.height <= 0) throw new Error('frame must have positive finite dimensions and nonnegative position');
      const walker = document.createTreeWalker(node, NodeFilter.SHOW_TEXT);
      const boxes = []; let over = false; let text;
      const generics = new Set(['serif', 'sans-serif', 'monospace', 'cursive', 'fantasy', 'system-ui', 'ui-serif', 'ui-sans-serif', 'ui-monospace', 'ui-rounded', 'math']);
      const available = new Map();
      const canvas = document.createElement('canvas').getContext('2d');
      function familyAvailable(family) {
        if (generics.has(family.toLowerCase())) return true;
        if (available.has(family)) return available.get(family);
        const face = [...document.fonts].some(f => f.family.replace(/^['"]|['"]$/g, '') === family && f.status === 'loaded');
        // FontFaceSet.check alone returns true for unknown system families.
        const probe = 'mmmmmmmmmmWWWWiiii0123456789';
        const distinct = ['monospace', 'serif', 'sans-serif'].some(base => {
          canvas.font = `72px ${base}`; const fallback = canvas.measureText(probe).width;
          canvas.font = `72px ${JSON.stringify(family)}, ${base}`;
          return canvas.measureText(probe).width !== fallback;
        });
        available.set(family, face || distinct);
        return face || distinct;
      }
      while ((text = walker.nextNode())) {
        if (!text.textContent.trim()) continue;
        const el = text.parentElement;
        if (!el.checkVisibility({ checkOpacity: true, checkVisibilityCSS: true })) continue;
        const cs = getComputedStyle(el);
        await document.fonts.load(`${cs.fontStyle} ${cs.fontWeight} ${cs.fontSize} ${cs.fontFamily}`, text.textContent);
        const families = cs.fontFamily.split(',').map(f => f.trim().replace(/^['"]|['"]$/g, ''));
        // A fallback stack is allowed, but its first requested family must exist.
        if (!familyAvailable(families[0])) throw new Error(`unavailable requested font family: ${families[0]}`);
        const range = document.createRange(); range.selectNodeContents(text);
        const rects = [...range.getClientRects()]; if (!rects.length) continue;
        const stroke = parseFloat(cs.webkitTextStrokeWidth) || 0;
        const expansion = stroke / 2;
        const b = [Math.min(...rects.map(q => q.left)) - r.left - expansion,
          Math.min(...rects.map(q => q.top)) - r.top - expansion,
          Math.max(...rects.map(q => q.right)) - r.left + expansion,
          Math.max(...rects.map(q => q.bottom)) - r.top + expansion];
        const role = el.closest('[data-role]')?.dataset.role || 'text';
        if (role !== 'bleed' && (b[0] < -1 || b[1] < -1 || b[2] > r.width + 1 || b[3] > r.height + 1)) over = true;
        const ancestors = [];
        for (let ancestor = el; ancestor; ancestor = ancestor.parentElement) ancestors.push(getComputedStyle(ancestor));
        const opacity = ancestors.reduce((value, style) => value * Number(style.opacity), 1);
        // Opacity groups, gradients, filters and blends need a raster estimate. For
        // ordinary solid layers, composite the whole stack over the PNG's white canvas.
        const simpleBackground = ancestors.every(style => Number(style.opacity) === 1 &&
          style.backgroundImage === 'none' && style.filter === 'none' && style.backdropFilter === 'none' &&
          style.mixBlendMode === 'normal' && !style.backgroundClip.includes('text'));
        let bg = null;
        if (simpleBackground) {
          bg = [255, 255, 255];
          for (const style of [...ancestors].reverse()) {
            canvas.clearRect(0, 0, 1, 1);
            canvas.fillStyle = style.backgroundColor;
            canvas.fillRect(0, 0, 1, 1);
            const rgba = canvas.getImageData(0, 0, 1, 1).data;
            const alpha = rgba[3] / 255;
            bg = bg.map((channel, i) => rgba[i] * alpha + channel * (1 - alpha));
          }
        }
        // Retain the DOM location for Chromium's actual rendered-font report.
        if (!el.hasAttribute('data-cropmark-font-probe')) el.setAttribute('data-cropmark-font-probe', String(document.querySelectorAll('[data-cropmark-font-probe]').length));
        boxes.push({ text: text.textContent.trim().slice(0, 60), box: b, color: cs.color, bg, bgSource: simpleBackground ? 'composited-solid-stack' : 'raster-estimate-required', opacity, stroke_fill: cs.webkitTextStrokeColor, size: parseFloat(cs.fontSize), role,
          fontFamily: cs.fontFamily, fontStyle: cs.fontStyle, fontWeight: cs.fontWeight,
          strokeWidth: stroke, boundsKind: 'css-range-with-stroke-expansion', probe: el.getAttribute('data-cropmark-font-probe') });
      }
      return { w: r.width, h: r.height, slices, over, boxes, textFree: node.dataset.textFree === 'true' };
    });
    if (info.over) throw new Error(`frame ${id}: text bounds extend outside the frame (mark intentional bleed with data-role="bleed")`);
    infos.push({ frame, id, info });
  }
  const session = await page.context().newCDPSession(page);
  await session.send('DOM.enable'); await session.send('CSS.enable');
  const { root } = await session.send('DOM.getDocument');
  const fontReports = new Map();
  for (const { info } of infos) for (const b of info.boxes) {
    if (!fontReports.has(b.probe)) {
      const { nodeId } = await session.send('DOM.querySelector', { nodeId: root.nodeId, selector: `[data-cropmark-font-probe="${b.probe}"]` });
      const { fonts } = await session.send('CSS.getPlatformFontsForNode', { nodeId });
      fontReports.set(b.probe, fonts);
    }
    b.effectiveFonts = fontReports.get(b.probe);
    delete b.probe;
  }
  mkdirSync(out, { recursive: true });
  let count = 0;
  for (const { frame, id, info } of infos) {
    const box = await frame.boundingBox();
    const sw = box.width / info.slices;
    for (let s = 0; s < info.slices; s++) {
      const name = info.slices > 1 ? `${id}-${s + 1}` : id;
      const file = path.join(out, `${String(++count).padStart(2, '0')}-${name}.png`);
      await page.screenshot({ path: file, clip: { x: box.x + s * sw, y: box.y, width: sw, height: box.height }, fullPage: true });
      const boxes = info.boxes.filter(b => b.box[2] > s * sw && b.box[0] < (s + 1) * sw).map(b => ({ ...b,
        size: b.size * scale, strokeWidth: b.strokeWidth * scale,
        box: [(b.box[0] - s * sw) * scale, b.box[1] * scale, (b.box[2] - s * sw) * scale, b.box[3] * scale].map((v, i) => i < 2 ? Math.floor(v) : Math.ceil(v)) }));
      // Read actual PNG dimensions, including Chromium's rounding of fractional scales.
      const png = readFileSync(file);
      writeFileSync(file + '.boxes.json', JSON.stringify({ size: [png.readUInt32BE(16), png.readUInt32BE(20)], coordinateSpace: 'physical-pixels', ...(info.textFree ? { text_free: true } : {}),
        boundsNote: 'CSS text range plus half the text stroke width; not an exact raster ink mask. Shadows, transforms, and glyph overhang can exceed these bounds. effectiveFonts describes the parent element including descendants.', boxes }, null, 1));
    }
  }
  console.log(`rendered ${count} png -> ${out}/`);
} catch (error) {
  console.error(`ERROR cropmark HTML: ${error.message}`);
  process.exitCode = 1;
} finally {
  await browser?.close();
}
