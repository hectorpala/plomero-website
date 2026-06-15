#!/usr/bin/env node
// Checker E2E FUNCIONAL para plomeroculiacanpro.mx (puppeteer + Chrome, mismo stack
// que check-produccion/tracking). Prueba los FLUJOS de usuario reales, no solo el HTML:
//  1. MENÚ HAMBURGUESA (viewport móvil): clic en .mobile-menu-btn -> #nav-menu visible.
//  2. FORMULARIO (/contacto/): rellena y envía, pero ABORTA el POST (NO se manda lead
//     real a Netlify) y confirma que el envío SÍ se disparó al endpoint correcto.
//  3. WhatsApp: el enlace wa.me del DOM renderizado tiene el número correcto 526673922273.
//
// Solo REPORTA. Emite a stdout SOLO el JSON común:
//   {"hallazgos":[{id,archivo,linea,severidad,categoria,descripcion,fix_sugerido}], "analizadas":N}
// categoria = "e2e".
//
// Overrides solo-autoprueba (igual que PUPPETEER_EXECUTABLE_PATH): E2E_BASE.

import puppeteer from "puppeteer";
import fs from "fs";

const BASE = process.env.E2E_BASE || "https://plomeroculiacanpro.mx";
const WA_NUMBER = "526673922273";
const UA = "Mozilla/5.0 (revisor-e2e; +pipeline-mantenimiento)";

const hallazgos = [];
let seq = 0;
function add(sev, archivo, desc, fix, linea = 0) {
  seq += 1;
  hallazgos.push({
    id: "e2e-" + String(seq).padStart(3, "0"),
    archivo, linea, severidad: sev, categoria: "e2e",
    descripcion: desc, fix_sugerido: fix,
  });
}
function out(analizadas) { process.stdout.write(JSON.stringify({ hallazgos, analizadas }, null, 2) + "\n"); }

// El sitio tiene service worker (PWA); cuando está activo puede manejar la
// navegación/POST del form y ocultarlo de la interceptación. Lo bypasseamos para
// medir el cableado REAL del formulario (los SW no cachean POST igualmente).
async function newCtx(browser) {
  return browser.createBrowserContext
    ? await browser.createBrowserContext()
    : await browser.createIncognitoBrowserContext();
}
async function bypassSW(page) {
  try {
    const c = await page.target().createCDPSession();
    await c.send("Network.setBypassServiceWorker", { bypass: true });
  } catch (_) {}
}

function resolveChrome() {
  const cands = [
    process.env.PUPPETEER_EXECUTABLE_PATH,
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
  ];
  for (const c of cands) if (c && fs.existsSync(c)) return c;
  return undefined;
}

// ---------------------------------------------------------------- 1. menú hamburguesa
async function checkMenu(browser) {
  const ctx = await newCtx(browser);
  const page = await ctx.newPage();
  await page.setUserAgent(UA);
  await page.setViewport({ width: 390, height: 844, isMobile: true, hasTouch: true });
  await bypassSW(page);
  try {
    await page.goto(BASE + "/", { waitUntil: "networkidle2", timeout: 60000 });
  } catch (e) {
    add("media", "/", `E2E: no se pudo cargar ${BASE}/ para probar el menú (${e.message})`,
      "Revisar disponibilidad de la home");
    await ctx.close();
    return false;
  }
  const btn = await page.$(".mobile-menu-btn, .menu-toggle, .hamburger, .nav-toggle, [aria-label*='men']");
  if (!btn) {
    add("alta", "/", "E2E: no se encontró el botón de menú móvil (.mobile-menu-btn) en la home",
      "Restaurar el botón de menú hamburguesa (la navegación móvil depende de él)");
    await ctx.close();
    return true;
  }
  const visible = () => page.evaluate(() => {
    const el = document.querySelector("#nav-menu, .nav-menu");
    if (!el) return null;
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    return r.height > 0 && r.width > 0 && cs.display !== "none" && cs.visibility !== "hidden" && cs.opacity !== "0";
  });
  const before = await visible();
  await btn.click();
  await new Promise((r) => setTimeout(r, 600));
  const after = await visible();
  if (after === null) {
    add("alta", "/", "E2E: tras clicar el menú no existe el panel #nav-menu/.nav-menu en el DOM",
      "Verificar que el botón de menú muestre el contenedor de navegación correcto");
  } else if (!after) {
    add("alta", "/",
      `E2E: el menú hamburguesa NO se abre — tras clicar .mobile-menu-btn el panel sigue oculto (antes:${before}, después:${after})`,
      "Revisar el JS del menú móvil (toggle de clase/display); sin esto la navegación móvil no funciona (ver REGLAS.md: un JS roto rompe el menú)");
  }
  await ctx.close();
  return true;
}

// ---------------------------------------------------------------- 2. formulario (sin lead real)
async function checkForm(browser) {
  const ctx = await newCtx(browser);
  const page = await ctx.newPage();
  await page.setUserAgent(UA);
  let armed = false, formPost = null;
  await bypassSW(page);
  await page.setRequestInterception(true);
  page.on("request", (req) => {
    try {
      const u = req.url();
      // Solo el POST del formulario (mismo origen) se ABORTA para no mandar lead real.
      if (armed && req.method() === "POST" && u.startsWith(BASE)) {
        formPost = u;
        req.abort();
        return;
      }
    } catch (_) {}
    try { req.continue(); } catch (_) {}
  });

  try {
    await page.goto(BASE + "/contacto/", { waitUntil: "networkidle2", timeout: 60000 });
  } catch (e) {
    add("media", "/contacto/", `E2E: no se pudo cargar ${BASE}/contacto/ para probar el formulario (${e.message})`,
      "Revisar disponibilidad de /contacto/");
    await ctx.close();
    return false;
  }

  // Resolver el lead-form por PRIORIDAD (querySelector con lista mezcla orden de
  // documento y podría devolver otro form; aquí el orden es explícito).
  const hasForm = await page.evaluate(() =>
    !!(document.querySelector("#lead-form") || document.querySelector("form[data-netlify]") || document.querySelector("form")));
  if (!hasForm) {
    add("alta", "/contacto/", "E2E: no se encontró el formulario (#lead-form) en /contacto/",
      "Restaurar el formulario de captación de leads");
    await ctx.close();
    return true;
  }
  // rellenar campos requeridos con datos de prueba válidos
  try {
    await page.evaluate(() => {
      const set = (sel, val) => { const e = document.querySelector(sel); if (e) { e.value = val; e.dispatchEvent(new Event("input", { bubbles: true })); } };
      set("#lf-nombre, input[name='nombre']", "Prueba QA Pipeline");
      set("#lf-telefono, input[name='telefono']", "6670000000");
      set("#lf-colonia, input[name='colonia']", "Las Quintas");
      set("textarea[name='mensaje'], #lf-mensaje", "Mensaje de prueba automática (no enviar).");
    });
  } catch (_) {}

  armed = true;
  try {
    await page.evaluate(() => {
      const f = document.querySelector("#lead-form") || document.querySelector("form[data-netlify]") || document.querySelector("form");
      if (f) { if (typeof f.requestSubmit === "function") f.requestSubmit(); else f.submit(); }
    });
  } catch (_) {}
  for (let waited = 0; waited < 6000 && !formPost; waited += 300) {
    await new Promise((r) => setTimeout(r, 300));
  }
  armed = false;

  if (!formPost) {
    add("alta", "/contacto/",
      "E2E: el formulario de /contacto/ NO disparó ningún envío (POST) al rellenarlo y enviarlo — el submit puede estar roto (validación/JS) o sin action",
      "Verificar que el form envíe (action válido, sin JS que bloquee el submit); REGLAS.md: un JS roto mata el formulario");
  }
  await ctx.close();
  return true;
}

// ---------------------------------------------------------------- 3. wa.me
async function checkWhatsapp(browser) {
  const ctx = await newCtx(browser);
  const page = await ctx.newPage();
  await page.setUserAgent(UA);
  await bypassSW(page);
  try {
    await page.goto(BASE + "/", { waitUntil: "networkidle2", timeout: 60000 });
  } catch (e) {
    add("media", "/", `E2E: no se pudo cargar ${BASE}/ para probar wa.me (${e.message})`,
      "Revisar disponibilidad de la home");
    await ctx.close();
    return false;
  }
  const hrefs = await page.evaluate(() =>
    Array.from(document.querySelectorAll('a[href*="wa.me"], a[href*="api.whatsapp.com"]'))
      .map((a) => a.getAttribute("href") || ""));
  if (!hrefs.length) {
    add("alta", "/", "E2E: no hay ningún enlace wa.me/WhatsApp en el DOM renderizado de la home",
      "Añadir el CTA de WhatsApp (https://wa.me/" + WA_NUMBER + ")");
  } else {
    const malos = hrefs.filter((h) => !h.includes(WA_NUMBER));
    if (malos.length) {
      add("alta", "/",
        `E2E: ${malos.length} enlace(s) wa.me en la home NO tienen el número correcto ${WA_NUMBER} (posible URL truncada): ${malos.slice(0, 3).map((m) => m.slice(0, 70)).join(" | ")}`,
        "Corregir el href a https://wa.me/" + WA_NUMBER + " (REGLAS.md: una URL wa.me truncada rompe el sitio)");
    }
  }
  await ctx.close();
  return true;
}

async function main() {
  let browser;
  try {
    browser = await puppeteer.launch({ headless: "new", executablePath: resolveChrome(),
      args: ["--no-sandbox", "--disable-setuid-sandbox"] });
  } catch (e) {
    add("alta", "(entorno)",
      `verificación ciega: no se pudo lanzar Chrome headless (${e.message}); los flujos E2E NO se probaron`,
      "Instalar Chrome o ajustar PUPPETEER_EXECUTABLE_PATH");
    out(0);
    return;
  }
  let ran = 0;
  try {
    if (await checkMenu(browser)) ran += 1;
    if (await checkForm(browser)) ran += 1;
    if (await checkWhatsapp(browser)) ran += 1;
  } finally {
    await browser.close();
  }
  if (ran === 0) {
    add("alta", "(entorno)", "verificación ciega: no se ejecutó ningún flujo E2E",
      "Revisar entorno/headless y disponibilidad del sitio");
  }
  out(ran);
}

main().catch((e) => {
  add("alta", ".pipeline/check-e2e.mjs", `verificación ciega: fallo inesperado del checker E2E: ${e.message}`,
    "Revisar/reparar .pipeline/check-e2e.mjs");
  out(0);
});
