#!/usr/bin/env node
/**
 * generate-cover.mjs — renderiza a capa do Boletim dos Magos como PNG 840x300.
 *
 * Uso:
 *   node generate-cover.mjs --edicao 12 \
 *     --titulo "Agentes saem do laboratório" \
 *     --sub "Claude Managed Agents + MCP no WhatsApp + GPT-5.4 computer use" \
 *     --data "09 abr 2026" \
 *     --tags "Managed Agents|MCP|Computer Use" \
 *     --out /path/to/cover-12.png
 *
 * Tamanho: 840 × 300 (padrão Circle post cover — fonte: help.circle.so)
 */

import { chromium } from 'playwright';
import { fileURLToPath } from 'url';
import { dirname, resolve } from 'path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const TEMPLATE = resolve(__dirname, '..', 'cover-template.html');

function parseArgs(argv) {
  const out = {};
  for (let i = 2; i < argv.length; i += 2) {
    const k = argv[i].replace(/^--/, '');
    out[k] = argv[i + 1];
  }
  return out;
}

const args = parseArgs(process.argv);
const required = ['edicao', 'titulo', 'data', 'out'];
for (const r of required) {
  if (!args[r]) {
    console.error(`Faltando --${r}`);
    process.exit(1);
  }
}

const qs = new URLSearchParams({
  edicao: args.edicao,
  titulo: args.titulo,
  sub: args.sub || '',
  data: args.data,
  tags: args.tags || '',
}).toString();

const url = `file://${TEMPLATE}?${qs}`;

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({
    viewport: { width: 840, height: 300 },
    deviceScaleFactor: 2, // @2x pra capa nítida em Retina
  });
  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.waitForTimeout(150); // deixa fontes renderizarem
  await page.screenshot({
    path: args.out,
    omitBackground: false,
    type: 'png',
    fullPage: false,
    clip: { x: 0, y: 0, width: 840, height: 300 },
  });
  await browser.close();
  console.log(`✓ capa gerada: ${args.out}`);
})().catch(err => {
  console.error('ERRO:', err);
  process.exit(1);
});
