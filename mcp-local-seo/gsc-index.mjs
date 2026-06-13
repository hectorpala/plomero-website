import { readFileSync } from 'fs';
import { google } from 'googleapis';

const DIR = '/Users/openclaw/Sitios Web/Plomero Culiacán/mcp-local-seo';
const TOKEN_FILE = `${DIR}/gsc-token.json`;
const CLIENT_SECRET_FILE = `${DIR}/client_secret.json`;
const SITE_URL = 'sc-domain:plomeroculiacanpro.mx';
const SITE_URL_HTTP = 'https://plomeroculiacanpro.mx/';

async function getAuth() {
  const creds = JSON.parse(readFileSync(CLIENT_SECRET_FILE, 'utf-8'));
  const { client_id, client_secret } = creds.installed || creds.web || {};
  const oauth2 = new google.auth.OAuth2(client_id, client_secret, 'http://localhost:3847/oauth2callback');
  oauth2.setCredentials(JSON.parse(readFileSync(TOKEN_FILE, 'utf-8')));
  return oauth2;
}

// 1. Ping sitemap
const sitemapUrl = 'https://plomeroculiacanpro.mx/sitemaps/main_sitemap.xml';
console.log('=== 1. Ping sitemap ===');
try {
  const res = await fetch(`https://www.google.com/ping?sitemap=${encodeURIComponent(sitemapUrl)}`);
  console.log(`HTTP ${res.status} ${res.status === 200 ? '✅' : '⚠️'}`);
} catch(e) { console.log('Error:', e.message); }

// 2. Submit sitemap vía GSC API
console.log('\n=== 2. Submit sitemap vía API ===');
try {
  const auth = await getAuth();
  const wm = google.webmasters({ version: 'v3', auth });
  await wm.sitemaps.submit({ siteUrl: SITE_URL, feedpath: sitemapUrl });
  console.log('✅ Sitemap enviado');
} catch(e) { console.log('Error:', e.message); }

// 3. URL Inspection de páginas clave
console.log('\n=== 3. Estado de indexación — páginas clave ===');
const urls = [
  'https://plomeroculiacanpro.mx/servicios/',
  'https://plomeroculiacanpro.mx/servicios/emergencia-24-7/',
  'https://plomeroculiacanpro.mx/servicios/correccion-baja-presion/',
  'https://plomeroculiacanpro.mx/servicios/tecnico-de-gas-culiacan/',
  'https://plomeroculiacanpro.mx/blog/baja-presion-agua-causas-soluciones/',
  'https://plomeroculiacanpro.mx/blog/desatascar-wc-metodos-profesionales/',
  'https://plomeroculiacanpro.mx/blog/drenaje-tapado-senales-prevencion/',
];

try {
  const auth = await getAuth();
  const sc = google.searchconsole({ version: 'v1', auth });
  for (const url of urls) {
    try {
      const res = await sc.urlInspection.index.inspect({
        requestBody: { inspectionUrl: url, siteUrl: SITE_URL_HTTP, languageCode: 'es' }
      });
      const r = res.data?.inspectionResult?.indexStatusResult;
      const verdict = r?.verdict || '?';
      const state = r?.coverageState || 'desconocido';
      const lastCrawl = r?.lastCrawlTime ? r.lastCrawlTime.substring(0,10) : 'nunca';
      const icon = verdict === 'PASS' ? '✅' : verdict === 'NEUTRAL' ? '🔄' : '❌';
      console.log(`${icon} ${url.replace('https://plomeroculiacanpro.mx',''||'/')}`);
      console.log(`   Estado: ${state} · Último crawl: ${lastCrawl}`);
    } catch(e) {
      console.log(`⚠️  ${url.replace('https://plomeroculiacanpro.mx','')} → ${e.message.substring(0,80)}`);
    }
    await new Promise(r => setTimeout(r, 600));
  }
} catch(e) { console.log('Error general:', e.message); }
