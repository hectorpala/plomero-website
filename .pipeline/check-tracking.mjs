#!/usr/bin/env node
// Checker de TRACKING (GTM/GA) para plomeroculiacanpro.mx.
// Envuelve la lógica de verificar-tracking.js (que era un snippet manual de consola)
// en puppeteer, reusando el MISMO stack de Chrome headless que check-produccion.mjs.
// Carga las páginas clave en producción y confirma que el tracking REALMENTE funciona,
// no solo que el snippet esté en el HTML.
//
// Solo REPORTA. Emite a stdout SOLO el JSON común de hallazgos:
//   {"hallazgos":[{id,archivo,linea,severidad,categoria,descripcion,fix_sugerido}], "analizadas":N}
// categoria = "tracking".
//
// Por cada página clave:
//  1. ¿el HTML referencia GTM (snippet/gtm.js, id GTM-…)?  (htmlHasGTM)
//  2. window.dataLayer existe y es array                    (dataLayerOk)
//  3. el contenedor GTM CARGA (window.google_tag_manager)   (gtmLoaded)
//  4. se dispara la request a GA (network: …/g/collect)     (gaFired)
// Reglas:
//  - HTML con GTM pero dataLayer ausente            -> ALTA
//  - HTML con GTM pero el contenedor NO carga       -> ALTA  (gtm.js 404/bloqueado/id malo)
//  - GTM carga pero NO dispara request a GA         -> ALTA  (page_view no llegó: tag/consent roto)
//  - página clave SIN GTM en el HTML                -> media (cobertura incompleta)
// Si Chrome no lanza o no se cargó ninguna página -> verificación ciega (ALTA).
//
// Overrides solo-autoprueba (igual que PUPPETEER_EXECUTABLE_PATH): TRACK_BASE, TRACK_URLS.

import puppeteer from "puppeteer";
import fs from "fs";

const BASE = process.env.TRACK_BASE || "https://plomeroculiacanpro.mx";
const URLS = (process.env.TRACK_URLS || "/,/precios/,/contacto/,/servicios/reparacion-de-fugas/,/blog/")
  .split(",").map((s) => s.trim()).filter(Boolean);
const UA = "Mozilla/5.0 (revisor-tracking; +pipeline-mantenimiento)";
// El sitio DIFIERE GTM a propósito (protege el LCP): lo carga en la primera
// interacción ['scroll','click','touchstart','keydown'] o, como fallback, a los 12s
// (ver index.html). Por eso el checker SIMULA una interacción y luego espera el
// beacon, en vez de asumir que GTM carga solo al cargar la página (eso daría falsos
// positivos: un visitante real interactúa).
const POLL_MS = 8000;   // tiempo máx. de espera tras la interacción
const STEP_MS = 500;

const hallazgos = [];
let seq = 0;
function add(sev, archivo, desc, fix, linea = 0) {
  seq += 1;
  hallazgos.push({
    id: "trk-" + String(seq).padStart(3, "0"),
    archivo, linea, severidad: sev, categoria: "tracking",
    descripcion: desc, fix_sugerido: fix,
  });
}
function out(analizadas) { process.stdout.write(JSON.stringify({ hallazgos, analizadas }, null, 2) + "\n"); }

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

const isGtmJs = (u) => /googletagmanager\.com\/gtm\.js/i.test(u);
const isGtagJs = (u) => /googletagmanager\.com\/gtag\/js/i.test(u) || /google-analytics\.com\/analytics\.js/i.test(u);
function isGaHit(u) {
  const gaHost = /(google-analytics\.com|analytics\.google\.com)/i.test(u);
  const collect = /\/(g\/)?collect(\?|$)/i.test(u);
  return gaHost && collect;
}

async function main() {
  let browser;
  try {
    browser = await puppeteer.launch({ headless: "new", executablePath: resolveChrome(),
      args: ["--no-sandbox", "--disable-setuid-sandbox"] });
  } catch (e) {
    add("alta", "(entorno)",
      `verificación ciega: no se pudo lanzar Chrome headless (${e.message}); el tracking NO se verificó`,
      "Instalar Chrome o ajustar PUPPETEER_EXECUTABLE_PATH para el pipeline");
    out(0);
    return;
  }

  let loadedCount = 0;
  try {
    for (const path of URLS) {
      const page = await browser.newPage();
      await page.setUserAgent(UA);
      let gtmJs = false, gaFired = false, gtagJs = false;
      page.on("request", (r) => {
        const u = r.url();
        if (isGtmJs(u)) gtmJs = true;
        if (isGtagJs(u)) gtagJs = true;
        if (isGaHit(u)) gaFired = true;
      });

      let loaded = true;
      try {
        await page.goto(BASE + path, { waitUntil: "networkidle2", timeout: 60000 });
      } catch (e) {
        loaded = false;
        add("media", path,
          `TRACKING: no se pudo cargar ${BASE}${path} en headless (${e.message}); no se verificó su tracking`,
          "Revisar disponibilidad/render de la página (puede solaparse con revisor-produccion)");
      }
      if (loaded) {
        loadedCount += 1;
        // SIMULAR primera interacción (el sitio difiere GTM hasta entonces).
        try {
          await page.evaluate(() => {
            window.scrollTo(0, 400);
            ["scroll", "click", "touchstart", "keydown"].forEach((e) => window.dispatchEvent(new Event(e)));
          });
          await page.mouse.move(200, 200);
        } catch (_) {}
        // Poll: esperar a que el contenedor cargue y dispare GA (hasta POLL_MS).
        let st = { htmlHasGTM: false, dataLayerOk: false, gtmLoaded: false, gtmAjenos: [] };
        for (let waited = 0; waited <= POLL_MS; waited += STEP_MS) {
          st = await page.evaluate(() => ({
            // El contenedor debe ser EL DEL PLOMERO (GTM-W75CRTX5): el patrón pelado
            // /GTM-[A-Z0-9]+/ aceptaba CUALQUIER contenedor, incluido el del
            // electricista (GTM-5Z2QRZ5Q) → "tracking sano" ante una fuga del hermano.
            htmlHasGTM: document.documentElement.innerHTML.includes("GTM-W75CRTX5") ||
                        !!document.querySelector('script[src*="googletagmanager.com/gtm.js?id=GTM-W75CRTX5"]'),
            gtmAjenos: (document.documentElement.innerHTML.match(/GTM-[A-Z0-9]{6,}/g) || [])
              .filter((id) => id !== "GTM-W75CRTX5")
              .filter((id, i, a) => a.indexOf(id) === i),
            dataLayerOk: Array.isArray(window.dataLayer),
            gtmLoaded: typeof window.google_tag_manager !== "undefined",
            gaIds: typeof window.google_tag_manager !== "undefined"
              ? Object.keys(window.google_tag_manager).filter((k) => /^G-/.test(k)) : [],
          }));
          if (st.gtmLoaded && gaFired) break;
          await new Promise((r) => setTimeout(r, STEP_MS));
        }
        if (st.gtmAjenos && st.gtmAjenos.length) {
          add("alta", path,
            `TRACKING/FUGA: la página ${BASE}${path} contiene contenedor(es) GTM AJENO(S): ${st.gtmAjenos.join(", ")} (el del sitio es GTM-W75CRTX5)`,
            "Eliminar el contenedor ajeno (contaminación del sitio hermano); los eventos se están yendo a otra cuenta");
        }
        const ga4Present = gtagJs || (st.gaIds && st.gaIds.length > 0);

        if (!st.htmlHasGTM) {
          add("media", path,
            `TRACKING: la página clave ${BASE}${path} NO referencia GTM en el HTML (cobertura de tracking incompleta)`,
            "Añadir el snippet de GTM (GTM-W75CRTX5) a la página, como en el resto del sitio");
        } else {
          if (!st.dataLayerOk) {
            add("alta", path,
              `TRACKING: ${BASE}${path} tiene GTM en el HTML pero window.dataLayer NO existe (el snippet no se ejecutó)`,
              "Revisar el snippet de GTM (debe crear window.dataLayer antes de cargar gtm.js); ¿JS roto en la página? (ver REGLAS.md wa.me/minificación)");
          } else if (!st.gtmLoaded) {
            add("alta", path,
              `TRACKING: ${BASE}${path} tiene GTM en el HTML pero el CONTENEDOR no carga (window.google_tag_manager ausente${gtmJs ? "; gtm.js se pidió pero no inicializó" : "; gtm.js ni siquiera se solicitó tras simular interacción"})`,
              "Verificar el id del contenedor (GTM-W75CRTX5), que gtm.js no esté bloqueado/404 y que no haya error JS que aborte la carga");
          } else if (!ga4Present) {
            add("alta", path,
              `TRACKING: ${BASE}${path} carga GTM pero NO hay GA4 configurado (no se cargó gtag/js ni hay measurement id G-… en el contenedor); no se está midiendo nada`,
              "Configurar la etiqueta de GA4 dentro del contenedor GTM-W75CRTX5 (sin ella el tráfico no llega a Analytics)");
          } else if (!gaFired) {
            add("media", path,
              `TRACKING: ${BASE}${path} carga GTM y GA4 (${(st.gaIds || []).join(",") || "gtag/js"}) pero NO se observó beacon …/g/collect tras ${POLL_MS}ms + simular interacción; causa probable: Consent Mode denegado por defecto (un visitante real que ACEPTA sí lo dispararía) o trigger page_view condicionado`,
              "Verificar en GA4 Realtime con un navegador real/consentido si llegan hits; si el Consent Mode bloquea por defecto es ESPERADO. Si no, revisar el trigger page_view de la etiqueta GA4 en GTM. (No es necesariamente un bug: headless no acepta consentimiento)");
          }
        }
      }
      await page.close();
    }
  } finally {
    await browser.close();
  }

  if (loadedCount === 0) {
    add("alta", "(entorno)",
      "verificación ciega: no se cargó ninguna página clave; el tracking NO se verificó",
      "Revisar disponibilidad de producción / entorno headless");
  }
  out(loadedCount);
}

main().catch((e) => {
  add("alta", ".pipeline/check-tracking.mjs",
    `verificación ciega: fallo inesperado del checker de tracking: ${e.message}`,
    "Revisar/reparar .pipeline/check-tracking.mjs");
  out(0);
});
