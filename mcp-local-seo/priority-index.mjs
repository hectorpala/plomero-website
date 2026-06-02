import { submitSitemap } from '/Users/openclaw/Documents/Mis Apps/Sitios Web/Plomero Culiacán/mcp-local-seo/search-console.js';
import { writeFileSync } from 'fs';
import { google } from 'googleapis';
import { readFileSync } from 'fs';

const DIR = '/Users/openclaw/Documents/Mis Apps/Sitios Web/Plomero Culiacán/mcp-local-seo';
const SITE_URL = 'sc-domain:plomeroculiacanpro.mx';

async function getAuth() {
  const creds = JSON.parse(readFileSync(`${DIR}/client_secret.json`, 'utf-8'));
  const { client_id, client_secret } = creds.installed || creds.web || {};
  const oauth2 = new google.auth.OAuth2(client_id, client_secret, 'http://localhost:3847/oauth2callback');
  oauth2.setCredentials(JSON.parse(readFileSync(`${DIR}/gsc-token.json`, 'utf-8')));
  return oauth2;
}

// Crear sitemap temporal con solo las páginas nuevas/cambiadas
const urgentUrls = [
  'https://plomeroculiacanpro.mx/servicios/',
  'https://plomeroculiacanpro.mx/servicios/emergencia-24-7/',
  'https://plomeroculiacanpro.mx/servicios/correccion-baja-presion/',
  'https://plomeroculiacanpro.mx/servicios/tecnico-de-gas-culiacan/',
  'https://plomeroculiacanpro.mx/blog/desatascar-wc-metodos-profesionales/',
  'https://plomeroculiacanpro.mx/blog/drenaje-tapado-senales-prevencion/',
];

const now = new Date().toISOString();
const miniSitemap = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urgentUrls.map(url => `  <url>
    <loc>${url}</loc>
    <lastmod>${now}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>`).join('\n')}
</urlset>`;

const miniPath = '/Users/openclaw/Documents/Mis Apps/Sitios Web/Plomero Culiacán/sitemaps/priority_sitemap.xml';
writeFileSync(miniPath, miniSitemap);
console.log('Sitemap de prioridad creado con', urgentUrls.length, 'URLs');

// Enviar el sitemap de prioridad
const auth = await getAuth();
const wm = google.webmasters({ version: 'v3', auth });

try {
  await wm.sitemaps.submit({
    siteUrl: SITE_URL,
    feedpath: 'https://plomeroculiacanpro.mx/sitemaps/priority_sitemap.xml'
  });
  console.log('✅ Sitemap de prioridad enviado a Google');
} catch(e) {
  console.log('Error:', e.message);
}

// También reenviar el main sitemap
try {
  await wm.sitemaps.submit({
    siteUrl: SITE_URL,
    feedpath: 'https://plomeroculiacanpro.mx/sitemaps/main_sitemap.xml'
  });
  console.log('✅ Main sitemap reenviado');
} catch(e) {
  console.log('Error main:', e.message);
}

// Verificar sitemaps activos
try {
  const list = await wm.sitemaps.list({ siteUrl: SITE_URL });
  console.log('\n=== Sitemaps registrados en GSC ===');
  (list.data.sitemap || []).forEach(s => {
    console.log(`  ${s.path} → ${s.lastDownloaded?.substring(0,10) || 'nunca'} (${s.warnings || 0} warn, ${s.errors || 0} err)`);
  });
} catch(e) {
  console.log('Error listing:', e.message);
}
