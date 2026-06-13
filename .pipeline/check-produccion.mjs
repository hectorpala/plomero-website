#!/usr/bin/env node
// Checker de PRODUCCIÓN EN VIVO para plomeroculiacanpro.mx.
// Usa la infra de Chrome headless ya existente en el proyecto (puppeteer, ver
// scripts/automation/media-audit/*.mjs y REGLAS.md movil-201) + fetch para HTTP.
// NO es local: golpea https://plomeroculiacanpro.mx para detectar fallos de
// deploy/runtime que los revisores de archivos no ven.
//
// Emite a stdout SOLO el JSON común de hallazgos:
//   {"hallazgos":[{"id","archivo","linea","severidad","categoria","descripcion","fix_sugerido"}]}
//
// Chequeos:
//  1. Errores de consola JS en producción (pageerror = ALTA; console.error = media)
//     en /, /precios/, /contacto/ + wa.me del DOM con número completo 526673922273.
//  2. Uptime: cada URL clave debe dar 200 (no 3xx/4xx/5xx) en producción.
//  3. Headers de seguridad (HSTS, X-Content-Type-Options, Referrer-Policy) + mixed content (http://).
//  4. Formulario de /contacto/: action válido + endpoint 2xx (sin enviar lead real).

import puppeteer from "puppeteer";
import fs from "fs";

const BASE = "https://plomeroculiacanpro.mx";
const WA_NUMBER = "526673922273";
const UA = "Mozilla/5.0 (revisor-produccion; +pipeline-mantenimiento)";

const CONSOLE_PAGES = ["/", "/precios/", "/contacto/"];
const KEY_URLS = [
  "/", "/servicios/", "/precios/", "/contacto/", "/blog/",
  "/servicios/plomero-a-domicilio/", "/servicios/emergencia-24-7/",
  "/servicios/reparacion-de-fugas/",
];
const SEC_HEADERS = [
  ["strict-transport-security", "Strict-Transport-Security (HSTS)"],
  ["x-content-type-options", "X-Content-Type-Options"],
  ["referrer-policy", "Referrer-Policy"],
];

const hallazgos = [];
let seq = 0;
function add(sev, archivo, desc, fix, linea = 0) {
  seq += 1;
  hallazgos.push({
    id: "prod-" + String(seq).padStart(3, "0"),
    archivo, linea, severidad: sev, categoria: "produccion",
    descripcion: desc, fix_sugerido: fix,
  });
}

function resolveChrome() {
  const cands = [
    process.env.PUPPETEER_EXECUTABLE_PATH,
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
  ];
  for (const c of cands) {
    if (c && fs.existsSync(c)) return c;
  }
  return undefined; // deja que puppeteer use su Chrome empaquetado si está
}

async function main() {
  // ---------- CHECK 2: uptime + CHECK 3a: headers de seguridad (sobre "/")
  let rootHeaders = null;
  for (const url of KEY_URLS) {
    try {
      const r = await fetch(BASE + url, {
        method: "GET", redirect: "manual",
        headers: { "User-Agent": UA },
      });
      if (url === "/") rootHeaders = r.headers;
      if (r.status !== 200) {
        add("alta", url,
          `PRODUCCIÓN: ${BASE}${url} devolvió HTTP ${r.status} (se espera 200; un 3xx/4xx/5xx en una URL clave indica fallo de deploy/Netlify o redirect inesperado)`,
          "PENDIENTE HUMANO: revisar deploy/Netlify y redirects; confirmar que la URL clave sirva 200");
      }
      // consumir cuerpo para liberar el socket
      try { await r.arrayBuffer(); } catch (_) {}
    } catch (e) {
      add("alta", url,
        `PRODUCCIÓN: ${BASE}${url} no responde (error de red: ${e.message})`,
        "PENDIENTE HUMANO: confirmar si producción está caída o es un fallo de red transitorio; reintentar");
    }
  }
  if (rootHeaders) {
    for (const [h, label] of SEC_HEADERS) {
      if (!rootHeaders.get(h)) {
        add("media", "netlify.toml",
          `PRODUCCIÓN: falta el header de seguridad ${label} en la respuesta de ${BASE}/`,
          `PENDIENTE HUMANO (requiere aprobación, cambio de config no puramente mecánico): añadir ${label} a [[headers]] for="/*" en netlify.toml`);
      }
    }
  } else {
    add("alta", "/",
      `PRODUCCIÓN: no se pudieron leer los headers de ${BASE}/ (la home no respondió); no se pudo verificar HSTS/X-Content-Type-Options/Referrer-Policy`,
      "PENDIENTE HUMANO: verificar disponibilidad de la home en producción");
  }

  // ---------- CHECKS 1 y 4 con Chrome headless
  let browser;
  try {
    browser = await puppeteer.launch({
      headless: "new",
      executablePath: resolveChrome(),
      args: ["--no-sandbox", "--disable-setuid-sandbox"],
    });
  } catch (e) {
    add("alta", "(entorno)",
      `No se pudo lanzar Chrome headless (puppeteer): ${e.message}. No se ejecutaron los checks de consola JS, wa.me, mixed-content ni formulario`,
      "PENDIENTE HUMANO/INFRA: instalar Chrome o ajustar PUPPETEER_EXECUTABLE_PATH para el pipeline");
    print();
    return;
  }

  try {
    for (const path of CONSOLE_PAGES) {
      const page = await browser.newPage();
      await page.setUserAgent(UA);
      const pageErrors = [];
      const consoleErrors = [];
      page.on("pageerror", (err) => pageErrors.push(err));
      page.on("console", (msg) => { if (msg.type() === "error") consoleErrors.push(msg.text()); });

      let loaded = true;
      try {
        await page.goto(BASE + path, { waitUntil: "networkidle2", timeout: 60000 });
      } catch (e) {
        loaded = false;
        add("alta", path,
          `PRODUCCIÓN: no se pudo cargar ${BASE}${path} en headless (${e.message})`,
          "PENDIENTE HUMANO: revisar disponibilidad/render de la página en producción");
      }

      if (loaded) {
        // 1: excepciones JS NO capturadas -> ALTA (esto habría atrapado el incidente wa.me)
        for (const err of pageErrors) {
          const loc = (err.stack || "").split("\n")[1]?.trim() || "";
          add("alta", path,
            `PRODUCCIÓN: excepción JS NO capturada en ${BASE}${path}: ${err.message}${loc ? " @ " + loc : ""}`,
            "PENDIENTE HUMANO: corregir el error JS en el código fuente (no auto-arreglable a ciegas; el JS afecta menú/formularios/tracking de todo el sitio — ver REGLAS.md regla wa.me/minificación)");
        }
        // 1: console.error -> media (puede ser ruido de terceros; se reporta)
        for (const txt of [...new Set(consoleErrors)]) {
          add("media", path,
            `PRODUCCIÓN: console.error en ${BASE}${path}: ${txt}`,
            "PENDIENTE HUMANO: revisar si es error propio o ruido de terceros (GTM/analytics); si es propio, corregir");
        }

        // 1: wa.me del DOM renderizado con número completo
        const wa = await page.evaluate(() =>
          Array.from(document.querySelectorAll('a[href*="wa.me"], a[href*="api.whatsapp.com"]'))
            .map((a) => a.getAttribute("href") || ""));
        const malos = wa.filter((h) => !h.includes(WA_NUMBER));
        if (malos.length) {
          add("alta", path,
            `PRODUCCIÓN: ${malos.length} enlace(s) wa.me en ${BASE}${path} NO contienen el número completo ${WA_NUMBER} (posible URL truncada): ${malos.slice(0, 3).map((m) => m.slice(0, 80)).join(" | ")}`,
            `Corregir el href para que sea https://wa.me/${WA_NUMBER}... (mecánico en el HTML/JS fuente; ver REGLAS.md: una URL wa.me truncada rompe todo el sitio)`);
        }

        // 3b: mixed content — recursos http:// activos en página https
        const mixed = await page.evaluate(() => {
          const out = [];
          const grab = (sel, attr) => document.querySelectorAll(sel).forEach((el) => {
            const v = el.getAttribute(attr);
            if (v && /^http:\/\//i.test(v)) out.push(el.tagName.toLowerCase() + " " + attr + "=" + v);
          });
          grab("script[src]", "src"); grab('link[rel="stylesheet"]', "href");
          grab("img[src]", "src"); grab("iframe[src]", "src");
          return out;
        });
        for (const m of mixed) {
          add("alta", path,
            `PRODUCCIÓN: recurso http:// (mixed content activo) cargado en página https ${BASE}${path}: ${m}`,
            "Cambiar el recurso a https:// en el HTML fuente (mecánico)");
        }

        // 4: formulario de contacto (sin enviar lead real)
        if (path === "/contacto/") {
          const form = await page.evaluate(() => {
            const f = document.querySelector("form#lead-form") ||
                      document.querySelector('form[data-netlify], form[name], form');
            if (!f) return { exists: false };
            return { exists: true, action: f.getAttribute("action"), method: f.getAttribute("method"), netlify: f.hasAttribute("data-netlify") };
          });
          if (!form.exists) {
            add("alta", path, `PRODUCCIÓN: no se encontró ningún <form> en ${BASE}/contacto/`,
              "PENDIENTE HUMANO: el formulario de captación de leads desapareció del render — revisar plantilla/contenido");
          } else if (!form.action) {
            add("alta", path, `PRODUCCIÓN: el formulario de /contacto/ no tiene atributo action`,
              "PENDIENTE HUMANO: añadir action válido al form (o confirmar manejo por Netlify Forms)");
          } else {
            const actionUrl = new URL(form.action, BASE).href;
            try {
              const fr = await fetch(actionUrl, { method: "GET", redirect: "follow", headers: { "User-Agent": UA } });
              if (!(fr.status >= 200 && fr.status < 300)) {
                add("alta", path,
                  `PRODUCCIÓN: el endpoint del formulario (${actionUrl}) respondió HTTP ${fr.status} (se espera 2xx)`,
                  "PENDIENTE HUMANO: revisar la página/endpoint destino del form (action) en producción");
              }
              try { await fr.arrayBuffer(); } catch (_) {}
            } catch (e) {
              add("alta", path,
                `PRODUCCIÓN: no se pudo alcanzar el endpoint del formulario (${actionUrl}): ${e.message}`,
                "PENDIENTE HUMANO: verificar el endpoint del formulario");
            }
          }
        }
      }
      await page.close();
    }
  } finally {
    await browser.close();
  }
  print();
}

function print() {
  process.stdout.write(JSON.stringify({ hallazgos }, null, 2) + "\n");
}

main().catch((e) => {
  // Nunca reventar sin JSON: reporta el fallo como evidencia operativa.
  add("alta", "(entorno)", `Fallo inesperado del checker de producción: ${e.message}`,
    "PENDIENTE HUMANO/INFRA: revisar el checker .pipeline/check-produccion.mjs");
  print();
});
