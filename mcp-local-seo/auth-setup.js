#!/usr/bin/env node

/**
 * Script para autenticarse con Google Search Console.
 *
 * Uso:
 *   node mcp-local-seo/auth-setup.js
 *
 * Requisitos:
 *   1. Tener client_secret.json en mcp-local-seo/
 *      (Descargar de Google Cloud Console > Credentials > OAuth2 Client)
 *   2. Tener acceso a Google Search Console para plomeroculiacanpro.mx
 */

import { google } from 'googleapis';
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { createServer } from 'http';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { exec } from 'child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));
const CLIENT_SECRET_FILE = join(__dirname, 'client_secret.json');
const TOKEN_FILE = join(__dirname, 'gsc-token.json');

const SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly'];

async function main() {
  if (!existsSync(CLIENT_SECRET_FILE)) {
    console.error('\n❌ No se encontró client_secret.json');
    console.error('');
    console.error('Para obtenerlo:');
    console.error('1. Ve a https://console.cloud.google.com/apis/credentials');
    console.error('2. Click en tu OAuth2 Client');
    console.error('3. Click en "Download JSON"');
    console.error('4. Renombra el archivo a client_secret.json');
    console.error(`5. Colócalo en: ${__dirname}/`);
    process.exit(1);
  }

  const credentials = JSON.parse(readFileSync(CLIENT_SECRET_FILE, 'utf-8'));
  const { client_id, client_secret } = credentials.installed || credentials.web || {};

  const oauth2Client = new google.auth.OAuth2(
    client_id,
    client_secret,
    'http://localhost:3847/oauth2callback'
  );

  const authUrl = oauth2Client.generateAuthUrl({
    access_type: 'offline',
    scope: SCOPES,
    prompt: 'consent'
  });

  console.log('\n🔐 Autenticación de Google Search Console');
  console.log('==========================================');
  console.log('\nSe abrirá tu navegador para autorizar el acceso...\n');

  // Open browser
  const openCmd = process.platform === 'darwin' ? 'open' : process.platform === 'win32' ? 'start' : 'xdg-open';
  exec(`${openCmd} "${authUrl}"`);

  // Start local server to catch the callback
  return new Promise((resolve, reject) => {
    const httpServer = createServer(async (req, res) => {
      if (!req.url.startsWith('/oauth2callback')) return;

      const url = new URL(req.url, 'http://localhost:3847');
      const code = url.searchParams.get('code');

      if (!code) {
        res.writeHead(400);
        res.end('Error: no se recibió código de autorización');
        httpServer.close();
        reject(new Error('No auth code'));
        return;
      }

      try {
        const { tokens } = await oauth2Client.getToken(code);
        writeFileSync(TOKEN_FILE, JSON.stringify(tokens, null, 2));

        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(`
          <html><body style="font-family:sans-serif;text-align:center;padding:50px;">
            <h1>✅ Autenticación exitosa</h1>
            <p>Token guardado. Ya puedes cerrar esta ventana.</p>
            <p>El MCP de Search Console está listo para usarse.</p>
          </body></html>
        `);

        console.log('✅ Token guardado en gsc-token.json');
        console.log('✅ El MCP de Search Console está listo.\n');

        httpServer.close();
        resolve();
      } catch (err) {
        res.writeHead(500);
        res.end(`Error: ${err.message}`);
        httpServer.close();
        reject(err);
      }
    });

    httpServer.listen(3847, () => {
      console.log('Esperando autorización en http://localhost:3847 ...');
    });

    // Timeout after 2 minutes
    setTimeout(() => {
      httpServer.close();
      reject(new Error('Timeout: no se completó la autorización en 2 minutos'));
    }, 120000);
  });
}

main().catch(err => {
  console.error(`\n❌ Error: ${err.message}\n`);
  process.exit(1);
});
