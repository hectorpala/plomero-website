/**
 * auto-index.mjs — Indexing API automático post-push
 *
 * Detecta qué páginas HTML cambiaron en el último commit,
 * filtra las que tienen noindex, y manda las demás a Google.
 *
 * Uso manual:   node mcp-local-seo/auto-index.mjs
 * Uso con rango: node mcp-local-seo/auto-index.mjs HEAD~3..HEAD
 */

import { execSync } from 'child_process';
import { readFileSync, existsSync } from 'fs';
import { indexUrls } from './search-console.js';

const BASE_URL = 'https://plomeroculiacanpro.mx';
const BASE_DIR = '/Users/openclaw/Documents/Mis Apps/Sitios Web/Plomero Culiacán';
const MAX_URLS = 50; // límite conservador (API permite 200/día)

const range = process.argv[2] || 'HEAD~1..HEAD';

// 1. Detectar archivos HTML modificados en el rango de commits
let changedFiles;
try {
  changedFiles = execSync(
    `git -C "${BASE_DIR}" diff --name-only --diff-filter=ACM ${range}`,
    { encoding: 'utf-8' }
  ).trim().split('\n').filter(f => f.endsWith('index.html'));
} catch {
  console.log('⚠️  No se pudieron obtener archivos del diff. Usando último commit.');
  changedFiles = execSync(
    `git -C "${BASE_DIR}" show --name-only --format="" HEAD`,
    { encoding: 'utf-8' }
  ).trim().split('\n').filter(f => f.endsWith('index.html'));
}

if (!changedFiles.length || (changedFiles.length === 1 && !changedFiles[0])) {
  console.log('✅ No hay páginas HTML que indexar en este push.');
  process.exit(0);
}

// 2. Filtrar páginas noindex y convertir a URLs
const urls = [];
for (const file of changedFiles) {
  const fullPath = `${BASE_DIR}/${file}`;
  if (!existsSync(fullPath)) continue;

  const html = readFileSync(fullPath, 'utf-8');
  if (html.includes('noindex') || html.includes('http-equiv="refresh"')) continue;

  // Convertir ruta a URL: servicios/foo/index.html → /servicios/foo/
  const urlPath = file.replace('index.html', '');
  urls.push(`${BASE_URL}/${urlPath}`);
}

if (!urls.length) {
  console.log('✅ Todas las páginas modificadas tienen noindex — nada que indexar.');
  process.exit(0);
}

// Limitar a MAX_URLS
const toIndex = urls.slice(0, MAX_URLS);
const skipped = urls.length - toIndex.length;

console.log(`\n📡 Auto-indexación post-push`);
console.log(`   Páginas detectadas: ${urls.length}${skipped ? ` (enviando ${MAX_URLS}, omitiendo ${skipped})` : ''}\n`);

// 3. Enviar a Google Indexing API
const result = await indexUrls({ urls: toIndex });

let ok = 0, err = 0;
result.results.forEach(r => {
  const path = r.url.replace(BASE_URL, '');
  if (r.status.includes('✅')) {
    console.log(`  ✅ ${path}`);
    ok++;
  } else {
    console.log(`  ❌ ${path} → ${r.error}`);
    err++;
  }
});

console.log(`\n  Resultado: ${ok} enviadas · ${err} errores\n`);
