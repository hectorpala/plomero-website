import { google } from 'googleapis';
import { readFileSync } from 'fs';

const DIR = '/Users/openclaw/Sitios Web/Plomero Culiacán/mcp-local-seo';
const SITE_URL = 'sc-domain:plomeroculiacanpro.mx';

const creds = JSON.parse(readFileSync(`${DIR}/client_secret.json`, 'utf-8'));
const { client_id, client_secret } = creds.installed || creds.web || {};
const oauth2 = new google.auth.OAuth2(client_id, client_secret, 'http://localhost:3847/oauth2callback');
oauth2.setCredentials(JSON.parse(readFileSync(`${DIR}/gsc-token.json`, 'utf-8')));

const wm = google.webmasters({ version: 'v3', auth: oauth2 });
const res = await wm.sitemaps.get({
  siteUrl: SITE_URL,
  feedpath: 'https://plomeroculiacanpro.mx/sitemaps/main_sitemap.xml'
});
console.log(JSON.stringify(res.data, null, 2));
