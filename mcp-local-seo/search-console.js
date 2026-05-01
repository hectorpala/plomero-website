import { google } from 'googleapis';
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { createServer } from 'http';

const __dirname = dirname(fileURLToPath(import.meta.url));
const TOKEN_FILE = join(__dirname, 'gsc-token.json');
const CLIENT_SECRET_FILE = join(__dirname, 'client_secret.json');
const CACHE_FILE = join(__dirname, 'cache-search-console.json');
const CACHE_TTL_HOURS = 24;
const SITE_URL = 'sc-domain:plomeroculiacanpro.mx';

function loadCache() {
  if (!existsSync(CACHE_FILE)) return {};
  try {
    return JSON.parse(readFileSync(CACHE_FILE, 'utf-8'));
  } catch {
    return {};
  }
}

function saveCache(cache) {
  writeFileSync(CACHE_FILE, JSON.stringify(cache, null, 2), 'utf-8');
}

function isCacheValid(entry) {
  if (!entry || !entry.timestamp) return false;
  const age = Date.now() - entry.timestamp;
  return age < CACHE_TTL_HOURS * 60 * 60 * 1000;
}

async function getAuthClient() {
  if (!existsSync(CLIENT_SECRET_FILE)) {
    return {
      error: 'No se encontró client_secret.json. Descárgalo de Google Cloud Console > Credentials > OAuth2 Client > Download JSON y colócalo en mcp-local-seo/client_secret.json'
    };
  }

  const credentials = JSON.parse(readFileSync(CLIENT_SECRET_FILE, 'utf-8'));
  const { client_id, client_secret } = credentials.installed || credentials.web || {};

  if (!client_id || !client_secret) {
    return { error: 'client_secret.json no tiene el formato correcto. Debe ser de tipo "Desktop app".' };
  }

  const oauth2Client = new google.auth.OAuth2(
    client_id,
    client_secret,
    'http://localhost:3847/oauth2callback'
  );

  if (existsSync(TOKEN_FILE)) {
    const token = JSON.parse(readFileSync(TOKEN_FILE, 'utf-8'));
    oauth2Client.setCredentials(token);

    if (token.expiry_date && token.expiry_date < Date.now()) {
      try {
        const { credentials: newToken } = await oauth2Client.refreshAccessToken();
        oauth2Client.setCredentials(newToken);
        writeFileSync(TOKEN_FILE, JSON.stringify(newToken, null, 2));
      } catch {
        return { error: 'Token expirado y no se pudo renovar. Elimina gsc-token.json y vuelve a autenticar.' };
      }
    }

    return oauth2Client;
  }

  return {
    error: 'No hay token de Search Console. Ejecuta: node mcp-local-seo/auth-setup.js para autenticarte con Google.',
    needsAuth: true
  };
}

export async function searchKeywords({ query, pageFilter, days = 28, limit = 50 }) {
  const cache = loadCache();
  const cacheKey = `keywords_${query || 'all'}_${pageFilter || 'all'}_${days}_${limit}`;

  if (cache[cacheKey] && isCacheValid(cache[cacheKey])) {
    return { ...cache[cacheKey].data, source: 'cache' };
  }

  const auth = await getAuthClient();
  if (auth.error) return auth;

  const searchconsole = google.searchconsole({ version: 'v1', auth });

  const endDate = new Date();
  const startDate = new Date();
  startDate.setDate(startDate.getDate() - days);

  const requestBody = {
    startDate: startDate.toISOString().split('T')[0],
    endDate: endDate.toISOString().split('T')[0],
    dimensions: ['query'],
    rowLimit: limit,
    dimensionFilterGroups: []
  };

  if (query) {
    requestBody.dimensionFilterGroups.push({
      filters: [{
        dimension: 'query',
        operator: 'contains',
        expression: query
      }]
    });
  }

  if (pageFilter) {
    requestBody.dimensionFilterGroups.push({
      filters: [{
        dimension: 'page',
        operator: 'contains',
        expression: pageFilter
      }]
    });
  }

  try {
    const res = await searchconsole.searchanalytics.query({
      siteUrl: SITE_URL,
      requestBody
    });

    const result = {
      period: `${requestBody.startDate} a ${requestBody.endDate}`,
      total_keywords: res.data.rows?.length || 0,
      keywords: (res.data.rows || []).map(row => ({
        keyword: row.keys[0],
        clicks: row.clicks,
        impressions: row.impressions,
        ctr: `${(row.ctr * 100).toFixed(1)}%`,
        position: parseFloat(row.position.toFixed(1))
      }))
    };

    cache[cacheKey] = { data: result, timestamp: Date.now() };
    saveCache(cache);

    return { ...result, source: 'search_console_api' };
  } catch (err) {
    return { error: `Error al consultar Search Console: ${err.message}` };
  }
}

export async function findOpportunities({ minPosition = 5, maxPosition = 20, minImpressions = 10, days = 28 }) {
  const cache = loadCache();
  const cacheKey = `opportunities_${minPosition}_${maxPosition}_${minImpressions}_${days}`;

  if (cache[cacheKey] && isCacheValid(cache[cacheKey])) {
    return { ...cache[cacheKey].data, source: 'cache' };
  }

  const auth = await getAuthClient();
  if (auth.error) return auth;

  const searchconsole = google.searchconsole({ version: 'v1', auth });

  const endDate = new Date();
  const startDate = new Date();
  startDate.setDate(startDate.getDate() - days);

  try {
    const res = await searchconsole.searchanalytics.query({
      siteUrl: SITE_URL,
      requestBody: {
        startDate: startDate.toISOString().split('T')[0],
        endDate: endDate.toISOString().split('T')[0],
        dimensions: ['query', 'page'],
        rowLimit: 500
      }
    });

    const rows = res.data.rows || [];

    const quickWins = rows
      .filter(r => r.position >= minPosition && r.position <= maxPosition && r.impressions >= minImpressions)
      .sort((a, b) => b.impressions - a.impressions)
      .slice(0, 30)
      .map(r => ({
        keyword: r.keys[0],
        page: r.keys[1],
        clicks: r.clicks,
        impressions: r.impressions,
        position: parseFloat(r.position.toFixed(1)),
        potential: r.clicks === 0 ? 'alto' : 'medio'
      }));

    const zeroClicks = rows
      .filter(r => r.clicks === 0 && r.impressions >= 20 && r.position <= 10)
      .sort((a, b) => b.impressions - a.impressions)
      .slice(0, 20)
      .map(r => ({
        keyword: r.keys[0],
        page: r.keys[1],
        impressions: r.impressions,
        position: parseFloat(r.position.toFixed(1)),
        action: 'Mejorar titulo y meta description para atraer clics'
      }));

    const result = {
      period: `${startDate.toISOString().split('T')[0]} a ${endDate.toISOString().split('T')[0]}`,
      quick_wins: {
        description: `Keywords en posición ${minPosition}-${maxPosition} con ${minImpressions}+ impresiones. Un push SEO las sube a página 1.`,
        count: quickWins.length,
        keywords: quickWins
      },
      zero_clicks: {
        description: 'Keywords en top 10 con 0 clics. El snippet no atrae. Mejorar title/description.',
        count: zeroClicks.length,
        keywords: zeroClicks
      }
    };

    cache[cacheKey] = { data: result, timestamp: Date.now() };
    saveCache(cache);

    return { ...result, source: 'search_console_api' };
  } catch (err) {
    return { error: `Error al consultar Search Console: ${err.message}` };
  }
}
