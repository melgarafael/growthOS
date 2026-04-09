#!/usr/bin/env node
/**
 * export-carousel.mjs — HTML → PNG batch exporter
 *
 * Usage:
 *   node export-carousel.mjs <path-to-carousels-vN.html> [--out <dir>] [--carousel <cid>]
 *
 * Default behavior:
 *   - Opens the HTML with Playwright (Chromium headless)
 *   - Screenshots each .slide element at 1080x1080 (native size, no scaling)
 *   - Saves to growthOS/output/carousels/{file-stem}/slides/{cid}-{sNN}.png
 *
 * Options:
 *   --out <dir>        custom output directory
 *   --carousel <cid>   export only 1 carousel (e.g., --carousel c04)
 *   --parallel <n>     number of parallel screenshots (default 4)
 *
 * Relies on: Playwright (reuse from ~/.claude/skills/playwright or global install)
 */

import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import { dirname, resolve, basename, extname } from 'path';
import { mkdirSync, existsSync } from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const REPO_ROOT = resolve(__dirname, '..', '..');
const GROWTHOS = resolve(REPO_ROOT, 'growthOS');

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = { parallel: 4, out: null, carousel: null };
  let html = null;
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === '--out') opts.out = args[++i];
    else if (a === '--carousel') opts.carousel = args[++i];
    else if (a === '--parallel') opts.parallel = parseInt(args[++i], 10);
    else html = a;
  }
  if (!html) {
    console.error('usage: export-carousel.mjs <path-to-html> [--out dir] [--carousel cid] [--parallel n]');
    process.exit(1);
  }
  return { html: resolve(html), ...opts };
}

async function main() {
  const { html, out, carousel, parallel } = parseArgs();
  if (!existsSync(html)) {
    console.error(`❌ not found: ${html}`);
    process.exit(1);
  }

  const stem = basename(html, extname(html));
  const outDir = out || resolve(GROWTHOS, 'output', 'carousels', stem);
  mkdirSync(outDir, { recursive: true });

  console.log(`🎬 exporting ${basename(html)} → ${outDir}`);
  if (carousel) console.log(`   filter: only carousel ${carousel}`);

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    // Viewport tall enough to fit both legacy 1080x1080 and new 1080x1350 slides
    viewport: { width: 1600, height: 1500 },
    deviceScaleFactor: 2, // retina-quality PNGs
  });
  const page = await context.newPage();
  await page.goto(`file://${html}`, { waitUntil: 'networkidle' });

  // Find all sections (each section = 1 carousel)
  const sections = await page.$$('section[data-carousel], section.carousel, section[id^="c"]');
  console.log(`   found ${sections.length} carousel section(s)`);

  let totalExported = 0;

  for (const section of sections) {
    const cid = await section.getAttribute('data-carousel')
      || await section.getAttribute('id')
      || `c${totalExported.toString().padStart(2, '0')}`;
    if (carousel && !cid.includes(carousel)) continue;

    const slidesDir = resolve(outDir, cid, 'slides');
    mkdirSync(slidesDir, { recursive: true });

    // Find slide elements inside this section
    const slides = await section.$$('.slide, [data-slide]');
    if (slides.length === 0) {
      // Fallback: top-level .slide elements (v1 structure)
      console.log(`   ⚠ no .slide inside section ${cid}, skipping`);
      continue;
    }

    console.log(`   📸 ${cid}: exporting ${slides.length} slides (parallel=${parallel})`);

    // Process in batches of `parallel`
    const batches = [];
    for (let i = 0; i < slides.length; i += parallel) {
      batches.push(slides.slice(i, i + parallel));
    }

    for (const batch of batches) {
      await Promise.all(batch.map(async (slide, idx) => {
        const slideNum = (batches.indexOf(batch) * parallel + idx + 1).toString().padStart(2, '0');
        const fname = `${cid}-s${slideNum}.png`;
        const fpath = resolve(slidesDir, fname);

        // Temporarily un-scale the slide (remove transform:scale) for native 1080x1080 capture
        await slide.evaluate((el) => {
          el.dataset._originalTransform = el.style.transform;
          el.style.transform = 'none';
        });

        await slide.screenshot({ path: fpath, omitBackground: false });

        // Restore original transform
        await slide.evaluate((el) => {
          el.style.transform = el.dataset._originalTransform || '';
        });
      }));
    }

    totalExported += slides.length;
  }

  await browser.close();
  console.log(`\n✅ exported ${totalExported} slides total`);
  console.log(`📂 output: ${outDir}`);
}

main().catch((err) => {
  console.error('❌ export failed:', err);
  process.exit(1);
});
