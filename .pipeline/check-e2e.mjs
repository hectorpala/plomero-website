#!/usr/bin/env node
// Checker E2E FUNCIONAL para plomeroculiacanpro.mx (puppeteer + Chrome, mismo stack
// que check-produccion/tracking). Prueba los FLUJOS de usuario reales, no solo el HTML:
//  1. MENÚ HAMBURGUESA (viewport móvil): clic en .mobile-menu-btn -> #nav-menu visible.
//  2. FORMULARIO (/contacto/): rellena y envía, pero ABORTA el POST (NO se manda lead
//     real a Netlify) y confirma que el envío SÍ se disparó al endpoint correcto.
//  3. WhatsApp: el enlace wa.me del DOM renderizado tiene el número correcto 526673922273.
//  4. FORMULARIO #contact-form en TODAS las páginas donde vive (descubiertas recorriendo el
//     repo, NO hardcodeadas): cero mensajes visibles al cargar, 4 campos visibles con ancho
//     razonable, VALIDACIÓN VIVA (clase .valid/.invalid + el mensaje correcto visible) y el
//     botón de envío que arranca deshabilitado y se habilita al completar. Nunca envía.
//
// POR QUÉ EXISTE EL PUNTO 4 (bug 2026: 258 días ciego): el commit a5198bbd borró de
// styles.min.css el bloque .form-field/.error-message{display:none}/.success-message y los 8
// mensajes quedaron visibles a la vez bajo cada campo en /, /servicios/emergencia-24-7/ y
// /servicios/plomero-colonias-culiacan/. Nadie lo vio porque este checker (y check-produccion)
// solo probaban /contacto/, que usa OTRO markup (#lead-form, con <label>, sin .form-field) —
// la única página que NO podía exhibir el fallo. El descubrimiento del punto 4 es DINÁMICO a
// propósito: una lista escrita a mano reintroduce exactamente ese punto ciego.
//
// Solo REPORTA. Emite a stdout SOLO el JSON común:
//   {"hallazgos":[{id,archivo,linea,severidad,categoria,descripcion,fix_sugerido}], "analizadas":N}
// categoria = "e2e".
//
// Overrides solo-autoprueba (igual que PUPPETEER_EXECUTABLE_PATH): E2E_BASE.

import puppeteer from "puppeteer";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
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

// ------------------------------------------- 4. formulario #contact-form en TODAS sus páginas
// Directorios que NUNCA son páginas servidas del sitio (mismo criterio que
// check-plantilla.py / check-indexabilidad.py: SKIP_DIRS).
const SKIP_DIRS = new Set([
  "node_modules", ".git", "partials", "docs", ".netlify", "reivision de sitio",
  "site-check", "keyword-volume-tool", "mcp-local-seo", "scripts", "graphify-plomero",
  ".pipeline",
]);

// Descubrimiento DINÁMICO: recorre el repo y devuelve la ruta URL de cada HTML publicable
// que contenga id="contact-form". Hardcodear la lista es justo lo que dejó el bug 258 días
// invisible, así que si mañana hay más (o menos) páginas con el formulario, se prueban solas.
function descubrirPaginasContactForm() {
  const encontradas = [];
  const walk = (dir) => {
    let entradas;
    try { entradas = fs.readdirSync(dir, { withFileTypes: true }); } catch (_) { return; }
    for (const e of entradas) {
      const full = path.join(dir, e.name);
      if (e.isDirectory()) {
        if (SKIP_DIRS.has(e.name) || e.name.startsWith(".")) continue;
        walk(full);
      } else if (e.isFile() && e.name.endsWith(".html")) {
        if (e.name.endsWith(".min.html") || e.name.includes(".backup") || e.name.endsWith(".bak")) continue;
        let html;
        try { html = fs.readFileSync(full, "utf8"); } catch (_) { continue; }
        if (!/id=["']contact-form["']/.test(html)) continue;
        const rel = path.relative(ROOT, full).split(path.sep).join("/");
        const url = rel === "index.html" ? "/"
          : rel.endsWith("/index.html") ? "/" + rel.slice(0, -"index.html".length)
          : "/" + rel;
        encontradas.push({ url, archivo: rel });
      }
    }
  };
  walk(ROOT);
  encontradas.sort((a, b) => a.url.localeCompare(b.url));
  return encontradas;
}

const VALIDOS = {
  nombre: "Prueba QA Pipeline",
  telefono: "6670000000",
  email: "qa-pipeline@ejemplo.com",
  mensaje: "Mensaje de prueba automática del pipeline, no enviar.",
};

async function escribir(page, sel, valor) {
  // typing real (dispara los listeners 'input' de main.js), luego blur explícito.
  await page.focus(sel);
  await page.evaluate((s) => { const e = document.querySelector(s); if (e) e.value = ""; }, sel);
  await page.type(sel, valor, { delay: 5 });
  await page.evaluate((s) => { const e = document.querySelector(s); if (e) e.blur(); }, sel);
  await new Promise((r) => setTimeout(r, 250));
}

// Estado del campo TAL COMO LO VE EL USUARIO: la clase del wrapper y si cada mensaje se
// pinta o no (offsetParent === null => no ocupa espacio => invisible). Mide el CSS aplicado,
// no el HTML crudo: es la diferencia entre "el markup existe" y "el formulario funciona".
async function estadoCampo(page, id) {
  return page.evaluate((fid) => {
    const inp = document.getElementById(fid);
    if (!inp) return null;
    const w = inp.closest(".form-field");
    if (!w) return { sinWrapper: true };
    const vis = (el) => !!el && el.offsetParent !== null;
    return {
      clases: w.className,
      valid: w.classList.contains("valid"),
      invalid: w.classList.contains("invalid"),
      errorVisible: vis(w.querySelector(".error-message")),
      exitoVisible: vis(w.querySelector(".success-message")),
      hayError: !!w.querySelector(".error-message"),
      hayExito: !!w.querySelector(".success-message"),
    };
  }, id);
}

async function checkContactForm(browser, pagina) {
  const { url, archivo } = pagina;
  const ctx = await newCtx(browser);
  const page = await ctx.newPage();
  await page.setUserAgent(UA);
  await page.setViewport({ width: 1280, height: 900 });
  await bypassSW(page);

  // NUNCA se manda un lead real: cualquier POST hacia el dominio se aborta (aquí ni siquiera
  // pulsamos "Enviar" — solo medimos el cableado —, pero el candado va por si acaso).
  let postAbortado = null;
  await page.setRequestInterception(true);
  page.on("request", (req) => {
    try {
      if (req.method() === "POST" && req.url().startsWith(BASE)) {
        postAbortado = req.url();
        req.abort();
        return;
      }
    } catch (_) {}
    try { req.continue(); } catch (_) {}
  });

  try {
    await page.goto(BASE + url, { waitUntil: "networkidle2", timeout: 60000 });
  } catch (e) {
    add("media", archivo, `E2E: no se pudo cargar ${BASE}${url} para probar #contact-form (${e.message})`,
      `Revisar disponibilidad de ${url}`);
    await ctx.close();
    return false;
  }

  const existe = await page.evaluate(() => !!document.getElementById("contact-form"));
  if (!existe) {
    add("alta", archivo,
      `E2E: ${url} trae id="contact-form" en el HTML del repo pero NO existe en el DOM renderizado`,
      "Revisar que el formulario no lo esté borrando/reemplazando algún JS");
    await ctx.close();
    return true;
  }

  // (a) EL CHEQUEO QUE HABRÍA CAZADO EL BUG: al cargar, CERO mensajes visibles.
  const alCargar = await page.evaluate(() => {
    const todos = Array.from(document.querySelectorAll(".error-message,.success-message"));
    const vis = todos.filter((e) => e.offsetParent !== null);
    return { total: todos.length, visibles: vis.length, textos: vis.slice(0, 4).map((e) => (e.textContent || "").trim().slice(0, 48)) };
  });
  if (alCargar.total === 0) {
    add("media", archivo,
      `E2E: ${url} no tiene ningún .error-message/.success-message en el DOM — la validación visible del formulario desapareció del markup`,
      "Restaurar los mensajes de error/éxito de cada .form-field (el usuario se queda sin feedback)");
  } else if (alCargar.visibles > 0) {
    add("alta", archivo,
      `E2E: ${url} muestra ${alCargar.visibles} de ${alCargar.total} mensajes de validación VISIBLES nada más cargar (sin que el usuario escriba nada): ${alCargar.textos.join(" | ")}`,
      "Restaurar en styles.min.css el bloque .error-message{display:none} / .success-message{display:none} " +
      "(+ .form-field.valid .success-message{display:block} y .form-field.invalid .error-message{display:block}); " +
      "así se veía el bug del commit a5198bbd: los 8 mensajes a la vez bajo cada campo");
  }

  // (b) los 4 campos existen, son visibles y no están colapsados
  const campos = await page.evaluate(() => {
    const ids = ["nombre", "telefono", "email", "mensaje"];
    return ids.map((id) => {
      const e = document.getElementById(id);
      if (!e) return { id, falta: true };
      const r = e.getBoundingClientRect();
      const cs = getComputedStyle(e);
      return {
        id,
        visible: r.width > 0 && r.height > 0 && cs.display !== "none" && cs.visibility !== "hidden",
        ancho: Math.round(r.width),
        alto: Math.round(r.height),
      };
    });
  });
  const faltantes = campos.filter((c) => c.falta).map((c) => c.id);
  if (faltantes.length) {
    add("alta", archivo, `E2E: ${url} — faltan campos del formulario en el DOM: ${faltantes.join(", ")}`,
      "Restaurar los 4 campos (nombre, telefono, email, mensaje) del #contact-form");
  }
  const invisibles = campos.filter((c) => !c.falta && !c.visible).map((c) => c.id);
  if (invisibles.length) {
    add("alta", archivo, `E2E: ${url} — campos presentes pero NO visibles para el usuario: ${invisibles.join(", ")}`,
      "Revisar el CSS del formulario (display/visibility/tamaño): un campo invisible es un lead perdido");
  }
  const colapsados = campos.filter((c) => !c.falta && c.visible && c.ancho < 120)
    .map((c) => `${c.id}=${c.ancho}px`);
  if (colapsados.length) {
    add("alta", archivo, `E2E: ${url} — campos con ancho colapsado (<120px): ${colapsados.join(", ")}`,
      "Restaurar .form-field input/textarea{width:100%} en styles.min.css");
  }

  // (c) el botón arranca DESHABILITADO
  const btnInicial = await page.evaluate(() => {
    const b = document.querySelector("#contact-form button[type='submit']");
    return b ? { hay: true, disabled: b.disabled } : { hay: false };
  });
  if (!btnInicial.hay) {
    add("alta", archivo, `E2E: ${url} — el #contact-form no tiene botón [type=submit]`,
      "Restaurar el botón de envío del formulario");
  } else if (!btnInicial.disabled) {
    add("media", archivo,
      `E2E: ${url} — el botón de envío arranca HABILITADO con el formulario vacío (debería estar disabled hasta completarlo)`,
      "Revisar updateSubmitButton() en main.js y el atributo disabled del botón en el HTML");
  }

  // (d) VALIDACIÓN VIVA — nombre con valor VÁLIDO -> .valid + SOLO el mensaje de éxito
  if (!faltantes.includes("nombre")) {
    await escribir(page, "#nombre", VALIDOS.nombre);
    const st = await estadoCampo(page, "nombre");
    if (st && st.sinWrapper) {
      add("alta", archivo, `E2E: ${url} — el campo #nombre no está dentro de un .form-field; la validación visual no puede funcionar`,
        "Envolver cada campo en <div class=\"form-field\"> (main.js usa field.closest('.form-field'))");
    } else if (st) {
      if (!st.valid) {
        add("alta", archivo,
          `E2E: ${url} — tras escribir un nombre VÁLIDO y quitar el foco, el .form-field NO tomó la clase 'valid' (clases: "${st.clases}") — la validación en vivo está muerta`,
          "Revisar el bloque de validación de main.js (listeners input/blur + validateField)");
      } else if (!st.exitoVisible || st.errorVisible) {
        add("alta", archivo,
          `E2E: ${url} — el campo nombre tomó la clase 'valid' pero el feedback NO se pinta (éxito visible: ${st.exitoVisible}, error visible: ${st.errorVisible}) — el CSS de validación no se está aplicando`,
          "Restaurar en styles.min.css .form-field.valid .success-message{display:block} y .error-message{display:none} (bloque borrado por a5198bbd)");
      }
    }
  }

  // (e) VALIDACIÓN VIVA — teléfono INVÁLIDO (pocos dígitos) -> .invalid + SOLO el error
  if (!faltantes.includes("telefono")) {
    await escribir(page, "#telefono", "123");
    const st = await estadoCampo(page, "telefono");
    if (st && st.sinWrapper) {
      add("alta", archivo, `E2E: ${url} — el campo #telefono no está dentro de un .form-field`,
        "Envolver cada campo en <div class=\"form-field\">");
    } else if (st) {
      if (!st.invalid) {
        add("alta", archivo,
          `E2E: ${url} — tras escribir un teléfono INVÁLIDO ("123") y quitar el foco, el .form-field NO tomó la clase 'invalid' (clases: "${st.clases}") — el formulario acepta basura sin avisar`,
          "Revisar el validador de teléfono en main.js (/^[0-9]{10}$/)");
      } else if (!st.errorVisible || st.exitoVisible) {
        add("alta", archivo,
          `E2E: ${url} — el campo teléfono tomó la clase 'invalid' pero el feedback NO se pinta (error visible: ${st.errorVisible}, éxito visible: ${st.exitoVisible}) — el CSS de validación no se está aplicando`,
          "Restaurar en styles.min.css .form-field.invalid .error-message{display:block} y .success-message{display:none} (bloque borrado por a5198bbd)");
      }
    }
  }

  // (f) con los 4 campos VÁLIDOS el botón se habilita (sin pulsarlo: no se manda lead)
  if (btnInicial.hay && !faltantes.length) {
    await escribir(page, "#nombre", VALIDOS.nombre);
    await escribir(page, "#telefono", VALIDOS.telefono);
    await escribir(page, "#email", VALIDOS.email);
    await escribir(page, "#mensaje", VALIDOS.mensaje);
    const btnFinal = await page.evaluate(() => {
      const b = document.querySelector("#contact-form button[type='submit']");
      return b ? b.disabled : null;
    });
    if (btnFinal !== false) {
      add("alta", archivo,
        `E2E: ${url} — con los 4 campos llenos y VÁLIDOS el botón de envío sigue deshabilitado: nadie puede mandar el formulario`,
        "Revisar isFormValid()/updateSubmitButton() en main.js y que los ids de los campos coincidan con los validadores");
    }
  }

  if (postAbortado) {
    add("media", archivo, `E2E: ${url} — se abortó un POST inesperado hacia ${postAbortado} durante la prueba (no se envió nada)`,
      "Revisar por qué el formulario intenta enviarse sin que el usuario pulse el botón");
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
  let paginasForm = [];
  try {
    paginasForm = descubrirPaginasContactForm();
  } catch (e) {
    add("alta", ".pipeline/check-e2e.mjs",
      `verificación ciega: falló el descubrimiento de páginas con #contact-form (${e.message}); el formulario de la home y los servicios NO se probó`,
      "Revisar el recorrido del repo en descubrirPaginasContactForm()");
  }
  try {
    if (await checkMenu(browser)) ran += 1;
    if (await checkForm(browser)) ran += 1;
    if (await checkWhatsapp(browser)) ran += 1;
    if (!paginasForm.length) {
      // Sin páginas descubiertas no hay nada que probar: NO es un pase, es una ceguera
      // (el bug a5198bbd vivió 258 días justo porque nadie miraba estas páginas).
      add("alta", "(repo)",
        "verificación ciega: no se encontró ninguna página con id=\"contact-form\" en el repo; el formulario principal del sitio quedó SIN probar",
        "Verificar que la home y las landings de servicios sigan trayendo el #contact-form (o ajustar el descubrimiento si el markup cambió)");
    }
    for (const p of paginasForm) {
      if (await checkContactForm(browser, p)) ran += 1;
    }
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
