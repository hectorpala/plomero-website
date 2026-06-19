#!/usr/bin/env node
// Checker DEAD-MAN'S SWITCH del pipeline de mantenimiento. CORRE PRIMERO.
// No verifica el SITIO; verifica que los SENSORES del pipeline funcionan. Si un
// sensor está ciego (cron parado, GSC sin token, un checker reventado, corpus
// vacío, producción caída) grita ALTA en vez de dejar pasar una corrida "sana"
// que en realidad no miró nada. Repite la lección de gsc-215 a nivel pipeline.
//
// Solo REPORTA. Emite a stdout SOLO el JSON común de hallazgos:
//   {"hallazgos":[{id,archivo,linea,severidad,categoria,descripcion,fix_sugerido}]}
// categoria = "infra". Salida con ORDEN ESTABLE (a → b → c-por-archivo → d).
//
// Chequeos:
//  (a) FRESCURA DEL CRON: el log run-*.log más reciente en
//      ~/Library/Logs/mantener-sitio/ debe tener <26h. Sin logs o demasiado viejo
//      → ALTA "cron parado" (la automatización dejó de correr y nadie lo sabía).
//  (b) GSC VIVO: llamada barata webmasters.sites.list con el token de mcp-local-seo.
//      Token ausente / 401 / error / lista vacía → ALTA "GSC ciego" (repite gsc-215).
//  (c) CHECKERS SANOS (verificación ciega a nivel pipeline):
//      - LOCALES deterministas (todo .pipeline/check-*.{py,mjs} salvo este, los
//        pesados y check-secretos.sh): se ejecutan completos; exigen exit 0 + JSON
//        parseable con array "hallazgos" + sin clave "error" + (si exponen el campo
//        opcional "analizadas") analizadas>0. Crash / JSON inválido / 0 analizadas
//        → ALTA "verificación ciega: <checker> no devolvió datos".
//      - PESADOS/RED (produccion, perf, tracking, e2e): SMOKE = `node --check`
//        (sintaxis) + que puppeteer resuelva. Correrlos completos aquí duplicaría
//        trabajo caro: cada uno corre como su propio revisor en el pipeline.
//      - SANIDAD DE CORPUS independiente: el sitemap tiene >0 <loc> y hay >0 .html
//        servidos. Si el corpus quedó en 0, un checker "pasaría en vacío" sin error.
//      NOTA: los 3 checkers existentes (indexabilidad/plantilla/produccion) NO se
//      modifican (regla: no tocar los 9 revisores actuales); el campo "analizadas"
//      es opcional y solo lo exponen los checkers nuevos.
//  (d) PRODUCCIÓN 200: GET https://plomeroculiacanpro.mx/ debe responder 200.

import { execFileSync } from "child_process";
import fs from "fs";
import os from "os";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.dirname(__dirname);
// Overrides solo para AUTOPRUEBAS del dead-man's switch (igual que
// PUPPETEER_EXECUTABLE_PATH en check-produccion). En producción nunca se setean.
const BASE = process.env.INFRA_BASE || "https://plomeroculiacanpro.mx";
const MCP_DIR = path.join(ROOT, "mcp-local-seo");
const LOG_DIR = process.env.INFRA_LOG_DIR || path.join(os.homedir(), "Library", "Logs", "mantener-sitio");
const NODE = fs.existsSync("/usr/local/bin/node") ? "/usr/local/bin/node" : process.execPath;
const CRON_MAX_HOURS = process.env.INFRA_CRON_MAX_HOURS ? Number(process.env.INFRA_CRON_MAX_HOURS) : 26;

// Checkers pesados/red: solo smoke (no se corren completos aquí).
const HEAVY = new Set(["check-produccion.mjs", "check-perf.mjs", "check-tracking.mjs", "check-e2e.mjs"]);
// No son checkers de páginas con el contrato JSON estándar (se excluyen del barrido local).
// check-parte.py (valida un parte concreto; requiere argumento) y check-reglas.py (utilidad de
// presupuesto de REGLAS.md) NO emiten {"hallazgos":[...]} — no son sensores de página.
// Solo el NÚCLEO va aquí. Las utilidades (check-parte.py, check-reglas.py, …) se auto-excluyen
// declarando `infra:utilidad-no-sensor` en su cabecera (ver esUtilidadDeclarada) — evita infra-003.
const NOT_PAGE_CHECKERS = new Set(["check-infra.mjs", "check-secretos.sh"]);

const SKIP_DIRS = ["/node_modules/", "/.git/", "/partials/", "/docs/", "/.netlify/",
  "/reivision de sitio/", "/site-check/", "/keyword-volume-tool/", "/mcp-local-seo/", "/scripts/"];

const hallazgos = [];
let seq = 0;
function add(sev, archivo, desc, fix, linea = 0) {
  seq += 1;
  hallazgos.push({
    id: "infra-" + String(seq).padStart(3, "0"),
    archivo, linea, severidad: sev, categoria: "infra",
    descripcion: desc, fix_sugerido: fix,
  });
}
function out() { process.stdout.write(JSON.stringify({ hallazgos }, null, 2) + "\n"); }

// ---------------------------------------------------------------- (a) cron fresco
function checkCron() {
  let entries = [];
  try {
    entries = fs.readdirSync(LOG_DIR).filter((f) => /^run-.*\.log$/.test(f));
  } catch (_) {
    add("alta", LOG_DIR,
      `INFRA: no existe el directorio de logs del cron (${LOG_DIR}); el mantenimiento automático nunca corrió o el launchd no está cargado`,
      "Verificar que el LaunchAgent/cron de mantener-diario.sh esté cargado y escribiendo logs en ~/Library/Logs/mantener-sitio/");
    return;
  }
  if (entries.length === 0) {
    add("alta", LOG_DIR,
      "INFRA: no hay ningún log run-*.log del cron; la corrida diaria de las 20:00 no está dejando rastro",
      "Verificar el LaunchAgent de mantener-diario.sh (que corre y escribe en ~/Library/Logs/mantener-sitio/)");
    return;
  }
  let newest = null, newestM = 0;
  for (const f of entries) {
    const m = fs.statSync(path.join(LOG_DIR, f)).mtimeMs;
    if (m > newestM) { newestM = m; newest = f; }
  }
  const ageH = (Date.now() - newestM) / 3.6e6;
  if (ageH > CRON_MAX_HOURS) {
    add("alta", path.join(LOG_DIR, newest),
      `INFRA: el log de cron más reciente (${newest}) supera el umbral de frescura de ${CRON_MAX_HOURS}h — el mantenimiento automático parece DETENIDO (dead-man's switch)`,
      "Revisar el LaunchAgent/launchd de mantener-diario.sh: que esté cargado, sin errores en launchd.err.log, y corriendo a las 20:00");
  }
}

// ---------------------------------------------------------------- (b) GSC vivo
function checkGsc() {
  const script = [
    "import {readFileSync} from 'fs';",
    "import {google} from 'googleapis';",
    `const D=${JSON.stringify(MCP_DIR)};`,
    "const c=JSON.parse(readFileSync(D+'/client_secret.json','utf-8'));",
    "const {client_id,client_secret}=c.installed||c.web||{};",
    "const o=new google.auth.OAuth2(client_id,client_secret,'http://localhost:3847/oauth2callback');",
    "o.setCredentials(JSON.parse(readFileSync(D+'/gsc-token.json','utf-8')));",
    "const wm=google.webmasters({version:'v3',auth:o});",
    "const r=await wm.sites.list();",
    "const n=(r.data.siteEntry||[]).length;",
    "console.log(n>0?('GSC_OK '+n):'GSC_EMPTY');",
  ].join("\n");
  let res;
  try {
    res = execFileSync(NODE, ["--input-type=module", "-e", script],
      { cwd: MCP_DIR, timeout: 45000, encoding: "utf-8", stdio: ["ignore", "pipe", "pipe"] }).trim();
  } catch (e) {
    const msg = (e.stderr || e.message || "").toString().split("\n").find((l) => l.trim()) || String(e.message);
    add("alta", "mcp-local-seo/gsc-token.json",
      `INFRA: GSC ciego — la llamada barata webmasters.sites.list falló (${msg.slice(0, 200)}). Indexación/cobertura SIN vigilancia (repite gsc-215)`,
      "Reautenticar/renovar el token (mcp-local-seo/auth-setup.js) o revisar la propiedad sc-domain; mientras tanto el revisor-gsc no puede leer datos reales");
    return;
  }
  if (res !== null && res.startsWith("GSC_OK")) return; // sano
  add("alta", "mcp-local-seo/gsc-token.json",
    `INFRA: GSC ciego — webmasters.sites.list no devolvió sitios (${res || "salida vacía"}); el token puede estar vivo pero sin propiedades, o la cuenta perdió acceso`,
    "Revisar que la cuenta autenticada posea la propiedad sc-domain:plomeroculiacanpro.mx y reautenticar si hace falta");
}

// ---------------------------------------------------------------- (c) checkers sanos
// Una utilidad (no-sensor de página) puede auto-excluirse SIN tocar este archivo declarando el
// marcador `infra:utilidad-no-sensor` en su cabecera. Evita la regresión infra-003 (añadir un
// check-*.py utilitario y olvidar NOT_PAGE_CHECKERS -> ALTA falsa de "verificación ciega").
function esUtilidadDeclarada(f) {
  try {
    return fs.readFileSync(`${__dirname}/${f}`, "utf8").slice(0, 800).includes("infra:utilidad-no-sensor");
  } catch (_) { return false; }
}
function listPageCheckers() {
  return fs.readdirSync(__dirname)
    .filter((f) => /^check-.*\.(py|mjs)$/.test(f) && !NOT_PAGE_CHECKERS.has(f) && !esUtilidadDeclarada(f))
    .sort();
}
function corpusSanity() {
  // sitemap <loc>
  let locs = 0;
  const sm = path.join(ROOT, "sitemaps", "main_sitemap.xml");
  if (fs.existsSync(sm)) locs = (fs.readFileSync(sm, "utf-8").match(/<loc>/g) || []).length;
  if (locs === 0) {
    add("alta", "sitemaps/main_sitemap.xml",
      "INFRA: el sitemap principal tiene 0 <loc> (o no existe); cualquier checker que recorra el sitemap 'pasaría en vacío' sin error",
      "Restaurar sitemaps/main_sitemap.xml; sin URLs en el sitemap la verificación de indexabilidad es ciega");
  }
  // .html servidos
  let html = 0;
  (function walk(dir) {
    let items = [];
    try { items = fs.readdirSync(dir, { withFileTypes: true }); } catch (_) { return; }
    for (const it of items) {
      const p = path.join(dir, it.name);
      const rel = "/" + path.relative(ROOT, p).split(path.sep).join("/") + (it.isDirectory() ? "/" : "");
      if (it.isDirectory()) {
        if (SKIP_DIRS.some((s) => rel.includes(s))) continue;
        walk(p);
      } else if (it.name.endsWith(".html") && !it.name.includes(".backup") &&
                 !it.name.endsWith(".min.html") && it.name !== "404.html") {
        html += 1;
      }
    }
  })(ROOT);
  if (html === 0) {
    add("alta", ".",
      "INFRA: 0 archivos .html servidos detectados en el repo; el corpus de páginas está vacío y los checkers de plantilla/contenido no tienen qué mirar",
      "Verificar el árbol del repo: deberían existir decenas de index.html servidos");
  }
}
function checkCheckers() {
  // smoke de puppeteer (lo usan los pesados)
  let puppeteerOk = true;
  try { execFileSync(process.execPath, ["--input-type=module", "-e", "await import('puppeteer')"],
    { cwd: ROOT, timeout: 30000, stdio: "ignore" }); } catch (_) { puppeteerOk = false; }

  for (const f of listPageCheckers()) {
    const full = path.join(__dirname, f);
    if (HEAVY.has(f)) {
      // SMOKE: sintaxis + dependencias
      try {
        execFileSync(process.execPath, ["--check", full], { timeout: 20000, stdio: "ignore" });
      } catch (e) {
        add("alta", path.join(".pipeline", f),
          `INFRA: el checker pesado ${f} no pasa 'node --check' (error de sintaxis); no podría correr en el pipeline`,
          `Reparar la sintaxis de .pipeline/${f}`);
        continue;
      }
      if (!puppeteerOk) {
        add("alta", path.join(".pipeline", f),
          `INFRA: el checker ${f} depende de puppeteer pero 'import puppeteer' no resuelve; correría ciego`,
          "Reinstalar puppeteer (npm i) en la raíz del repo");
      }
      continue;
    }
    // LOCAL determinista: corre completo y valida el JSON
    const runner = f.endsWith(".py") ? "python3" : process.execPath;
    let stdout;
    try {
      stdout = execFileSync(runner, [full], { cwd: ROOT, timeout: 90000, encoding: "utf-8",
        stdio: ["ignore", "pipe", "pipe"] });
    } catch (e) {
      add("alta", path.join(".pipeline", f),
        `INFRA: verificación ciega — el checker determinista ${f} salió con error (${(e.message || "").split("\n")[0].slice(0, 160)})`,
        `Reparar .pipeline/${f}; mientras falle, su revisión NO se está ejecutando`);
      continue;
    }
    let data;
    try { data = JSON.parse(stdout); } catch (_) {
      add("alta", path.join(".pipeline", f),
        `INFRA: verificación ciega — el checker ${f} no imprimió JSON parseable por stdout`,
        `Revisar que .pipeline/${f} emita solo el JSON común {"hallazgos":[...]}`);
      continue;
    }
    if (!Array.isArray(data.hallazgos)) {
      add("alta", path.join(".pipeline", f),
        `INFRA: verificación ciega — el checker ${f} no devolvió un array "hallazgos"`,
        `Revisar el contrato de salida de .pipeline/${f}`);
      continue;
    }
    if (data.error) {
      add("alta", path.join(".pipeline", f),
        `INFRA: verificación ciega — el checker ${f} reportó un error interno: ${String(data.error).slice(0, 160)}`,
        `Reparar la causa del error en .pipeline/${f}`);
    }
    if (typeof data.analizadas === "number" && data.analizadas === 0) {
      add("alta", path.join(".pipeline", f),
        `INFRA: verificación ciega — el checker ${f} analizó 0 páginas/URLs (0 anómalo: no pudo acceder a sus datos)`,
        `Revisar por qué .pipeline/${f} no encontró nada que analizar (¿corpus movido? ¿ruta rota?)`);
    }
  }
  corpusSanity();
}

// ---------------------------------------------------------------- (d) producción 200
async function checkProd() {
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), 20000);
  try {
    const r = await fetch(BASE + "/", { method: "GET", redirect: "manual",
      headers: { "User-Agent": "Mozilla/5.0 (check-infra; +pipeline)" }, signal: ctrl.signal });
    try { await r.arrayBuffer(); } catch (_) {}
    if (r.status !== 200) {
      add("alta", "/",
        `INFRA: producción ${BASE}/ devolvió HTTP ${r.status} (se espera 200); el sitio puede estar caído o mal desplegado`,
        "Revisar el deploy en Netlify y los redirects; confirmar que la home sirva 200");
    }
  } catch (e) {
    add("alta", "/",
      `INFRA: producción ${BASE}/ no responde (${e.name === "AbortError" ? "timeout" : e.message})`,
      "Confirmar si producción está caída o es un fallo de red transitorio; reintentar");
  } finally {
    clearTimeout(t);
  }
}

async function main() {
  checkCron();      // (a)
  checkGsc();       // (b)
  checkCheckers();  // (c)
  await checkProd(); // (d)
  out();
}

main().catch((e) => {
  add("alta", ".pipeline/check-infra.mjs",
    `INFRA: fallo inesperado del propio dead-man's switch: ${e.message}`,
    "Revisar/reparar .pipeline/check-infra.mjs");
  out();
});
