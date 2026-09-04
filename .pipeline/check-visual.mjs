#!/usr/bin/env node
// Checker de REGRESIÓN VISUAL para plomeroculiacanpro.mx (puppeteer + Chrome, mismo
// stack que check-e2e / check-perf / check-produccion).
//
// POR QUÉ EXISTE
// -------------
// El formulario de la portada estuvo VISUALMENTE ROTO 258 días y 77 corridas diarias
// sin que nadie lo viera: el commit a5198bbd (19-dic-2025) borró el bloque de CSS de
// validación y los 8 mensajes de error del formulario quedaron visibles TODOS a la vez,
// amontonados, en la home. El sistema tenía 19 revisores y 24 detectores y NINGUNO lo
// cazó, porque ninguno MIRA la página: verifican estructura HTML, etiquetas, JSON-LD,
// enlaces y códigos HTTP. Un cambio de CSS que destroza el render no toca nada de eso.
// Este checker es la red barata que lo habría cazado en diciembre: una COMPARACIÓN
// VISUAL (píxeles) contra una línea base, una vez por corrida.
//
// CÓMO COMPARA SIN LIBRERÍAS DE IMÁGENES
// --------------------------------------
// Sin dependencias nuevas (solo `puppeteer`, ya en el repo, y stdlib de Node). Todo el
// trabajo de imagen se hace DENTRO del propio Chrome: las capturas se cargan como data
// URI en <img>, se pintan en <canvas> al MISMO ancho reducido (320 px, alto
// proporcional) y se leen ambos getImageData para contar el porcentaje de píxeles cuya
// diferencia por canal supera una tolerancia. No hace falta decodificar PNG en Node y
// es exacto para lo que importa: un bloque de texto que aparece de la nada mueve
// muchísimos píxeles. Si las dos imágenes tienen distinto alto (contenido que aparece
// o desaparece), se compara sobre el alto MAYOR rellenando el sobrante.
//
// POR QUÉ NO SE USA `fullPage: true`  (medido el 2026-09-04, NO tocar sin releer esto)
// ------------------------------------------------------------------------------------
// La home mide ~28 000 px de alto en móvil. A esa altura `page.screenshot({fullPage})`
// TRUNCA en silencio: devuelve un PNG de 28 033 px cuyo contenido se corta a media
// tarjeta y NUNCA llega al footer... ni al formulario de contacto, que vive al final.
// O sea: la versión "obvia" de este checker medía 0.00 % de diferencia con el CSS de
// validación borrado — habría vuelto a NO ver el bug histórico. Por eso la captura se
// hace por BANDAS: se scrollea de viewport en viewport (390x844, el tamaño real), se
// captura cada pantalla y se van pegando en el canvas reducido. Determinista y sin
// límite de altura. La barra de navegación fija y los botones flotantes se ocultan a
// partir de la segunda banda (si no, se repetirían en las ~34 bandas de la home y
// taparían el contenido real).
//
// SOLO REPORTA. Emite a stdout SOLO el JSON común de hallazgos:
//   {"hallazgos":[{id,archivo,linea,severidad,categoria,descripcion,fix_sugerido}], "analizadas":N}
// categoria = "visual".  (El diagnóstico y los % medidos van por stderr.)
//
// LÍNEAS BASE: .pipeline/visual-baseline/<slug>.png. Si falta la de una URL NO es un
// fallo: es la primera vez — se guarda y se emite un hallazgo BAJA informativo.
// Se regeneran con `node .pipeline/check-visual.mjs --update-baseline` (igual que
// check-perf.mjs), que es también la forma de ACEPTAR un rediseño legítimo.
//
// PESO EN DISCO (las líneas base van a git): lo que se guarda NO es la captura cruda
// (4 MB solo la home) sino ya la imagen reducida que se compara: 320 px de ancho, en
// gris y cuantizada a 16 niveles (los 4 bits altos). No se pierde nada de lo que el
// checker mira, porque la captura actual pasa por EXACTAMENTE la misma reducción antes
// de compararse (dos corridas iguales dan 0.00 %). El precio: un cambio SOLO de color
// (mismo layout, misma luminancia) no se ve — eso ya lo cubre check-plantilla.py
// (check 12, color off-brand) + el auto-fixer `color-off-brand`.
//
// UMBRAL: 1.5 % de píxeles distintos (env VISUAL_UMBRAL). Por qué 1.5: con la
// estabilización de abajo, dos corridas seguidas de la misma página dan 0.00 % EXACTO,
// así que el suelo de ruido es CERO; y un destrozo de layout real (el bloque de
// mensajes de validación) mide varios puntos. 1.5 deja margen para un retoque menor
// (un botón, una línea de texto) sin gritar, y caza cualquier rotura de bloque.
// Severidad MEDIA: el checker AVISA, no bloquea — un rediseño intencional también
// dispara, y el modo de fallo que más daño ha hecho en este proyecto es el checker que
// grita todos los días hasta que nadie lo lee.
//
// RUIDO: antes de capturar se desactivan animaciones/transiciones/caret, se espera a
// networkidle2 y a document.fonts.ready, y se recorre la página para forzar el
// lazy-loading. Sin eso el checker sería ruido diario.
//
// Overrides solo-autoprueba (igual que PUPPETEER_EXECUTABLE_PATH): VISUAL_BASE
// (servidor local), VISUAL_URLS, VISUAL_UMBRAL, VISUAL_TOLERANCIA, VISUAL_ANCHO,
// VISUAL_BASELINE_DIR.

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.dirname(__dirname);

const BASE = process.env.VISUAL_BASE || "https://plomeroculiacanpro.mx";
const URLS = (process.env.VISUAL_URLS || "/,/servicios/emergencia-24-7/,/contacto/")
  .split(",").map((s) => s.trim()).filter(Boolean);
const BASELINE_DIR = process.env.VISUAL_BASELINE_DIR || path.join(__dirname, "visual-baseline");
const UPDATE = process.argv.includes("--update-baseline");

function numEnv(name, def) {
  const v = Number(process.env[name]);
  return Number.isFinite(v) && v > 0 ? v : def;
}
const UMBRAL = numEnv("VISUAL_UMBRAL", 1.5);        // % de píxeles distintos que dispara
const TOLERANCIA = numEnv("VISUAL_TOLERANCIA", 12); // diferencia por canal (0-255) que cuenta
const ANCHO_DIFF = numEnv("VISUAL_ANCHO", 320);     // ancho al que se normalizan las capturas
const BLANCO_Q = 248;                               // el blanco (255) tras cuantizar a 4 bits
const MAX_ALTO = 80000;                             // tope de seguridad para páginas patológicas
const VIEWPORT = { width: 390, height: 844, deviceScaleFactor: 1, isMobile: true, hasTouch: true };
const UA = "Mozilla/5.0 (revisor-visual; +pipeline-mantenimiento)";

const hallazgos = [];
let seq = 0;
function add(sev, archivo, desc, fix, linea = 0) {
  seq += 1;
  hallazgos.push({
    id: "visual-" + String(seq).padStart(3, "0"),
    archivo, linea, severidad: sev, categoria: "visual",
    descripcion: desc, fix_sugerido: fix,
  });
}
function out(analizadas) {
  process.stdout.write(JSON.stringify({ hallazgos, analizadas }, null, 2) + "\n");
}

function slugDe(u) {
  const p = (() => { try { return new URL(u, BASE).pathname; } catch (_) { return u; } })();
  const s = p.replace(/^\/+|\/+$/g, "").replace(/[^a-zA-Z0-9._-]+/g, "-").toLowerCase();
  return s || "home";
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

// CSS de estabilización: sin esto la captura cambia entre corridas por animaciones en
// vuelo, transiciones a medio camino, scroll suave y el cursor parpadeante de los inputs.
const CSS_ESTABLE = "*,*::before,*::after{animation:none!important;transition:none!important;" +
  "caret-color:transparent!important;scroll-behavior:auto!important}" +
  "html{scroll-behavior:auto!important}";

// ---------------------------------------------------------------- lienzo de trabajo
// Una sola página about:blank hace TODO el trabajo de imagen: componer las bandas en el
// canvas reducido, cuantizar y comparar contra la línea base.
async function abrirLienzo(browser) {
  const page = await browser.newPage();
  await page.goto("about:blank");

  const iniciar = (alto, anchoVp) => page.evaluate((alto, anchoVp, ancho) => {
    const escala = ancho / anchoVp;
    const c = document.createElement("canvas");
    c.width = ancho;
    c.height = Math.max(1, Math.round(alto * escala));
    const g = c.getContext("2d", { willReadFrequently: true });
    g.fillStyle = "#ffffff";
    g.fillRect(0, 0, c.width, c.height);
    window.__vc = { c: c, g: g, escala: escala };
    return { w: c.width, h: c.height };
  }, alto, anchoVp, ANCHO_DIFF);

  // Pega una banda (captura de un viewport) en su sitio dentro del canvas reducido.
  const pegar = (b64, y, altoVp) => page.evaluate(async (b64, y, altoVp) => {
    const img = await new Promise((res, rej) => {
      const i = new Image();
      i.onload = () => res(i);
      i.onerror = () => rej(new Error("banda PNG no decodificable"));
      i.src = "data:image/png;base64," + b64;
    });
    const s = window.__vc;
    s.g.drawImage(img, 0, y * s.escala, s.c.width, altoVp * s.escala);
    return true;
  }, b64, y, altoVp);

  // Cierra la composición: gris + cuantización a 16 niveles -> PNG base64.
  const finalizar = () => page.evaluate(() => {
    const s = window.__vc;
    if (!s) return null;
    const d = s.g.getImageData(0, 0, s.c.width, s.c.height), a = d.data;
    for (let i = 0; i < a.length; i += 4) {
      const v = ((((a[i] * 77 + a[i + 1] * 151 + a[i + 2] * 28) >> 8) & 0xF0) | 8);
      a[i] = a[i + 1] = a[i + 2] = v; a[i + 3] = 255;
    }
    s.g.putImageData(d, 0, 0);
    const b64 = s.c.toDataURL("image/png").split(",")[1];
    window.__vc = null;
    return { b64: b64, w: s.c.width, h: s.c.height };
  });

  // Diff de dos PNG YA reducidos y cuantizados.
  const diff = (a, b) => page.evaluate(async (a, b, ancho, tol, blanco) => {
    const carga = (x) => new Promise((res, rej) => {
      const i = new Image();
      i.onload = () => res(i);
      i.onerror = () => rej(new Error("PNG no decodificable"));
      i.src = "data:image/png;base64," + x;
    });
    const dos = await Promise.all([carga(a), carga(b)]);
    const ia = dos[0], ib = dos[1];
    const alto = Math.max(ia.height, ib.height);
    const pinta = (img) => {
      const c = document.createElement("canvas");
      c.width = ancho; c.height = alto;
      const g = c.getContext("2d", { willReadFrequently: true });
      // Relleno con el blanco YA cuantizado: si una imagen es más corta, el sobrante se
      // compara contra el contenido real de la otra y cuenta como diferencia (que es lo
      // que queremos), pero dos páginas que solo difieren en blanco al final no gritan.
      g.fillStyle = "rgb(" + blanco + "," + blanco + "," + blanco + ")";
      g.fillRect(0, 0, ancho, alto);
      g.drawImage(img, 0, 0);
      return g.getImageData(0, 0, ancho, alto).data;
    };
    const da = pinta(ia), db = pinta(ib);
    let distintos = 0;
    for (let i = 0; i < da.length; i += 4) {
      if (Math.abs(da[i] - db[i]) > tol ||
          Math.abs(da[i + 1] - db[i + 1]) > tol ||
          Math.abs(da[i + 2] - db[i + 2]) > tol) distintos++;
    }
    return { pct: (distintos / (ancho * alto)) * 100, altoA: ia.height, altoB: ib.height };
  }, a, b, ANCHO_DIFF, TOLERANCIA, BLANCO_Q);

  return {
    iniciar: iniciar, pegar: pegar, finalizar: finalizar, diff: diff,
    cerrar: async () => { try { await page.close(); } catch (_) {} },
  };
}

// ---------------------------------------------------------------- captura por bandas
async function capturar(browser, lienzo, ruta) {
  const ctx = browser.createBrowserContext
    ? await browser.createBrowserContext()
    : await browser.createIncognitoBrowserContext();
  const page = await ctx.newPage();
  try {
    await page.setUserAgent(UA);
    await page.setViewport(VIEWPORT);
    // El sitio es PWA: el service worker puede servir una versión cacheada y hacer que
    // la captura no refleje el CSS/HTML del deploy actual.
    try {
      const c = await page.target().createCDPSession();
      await c.send("Network.setBypassServiceWorker", { bypass: true });
    } catch (_) {}
    await page.evaluateOnNewDocument((css) => {
      const poner = () => {
        const st = document.createElement("style");
        st.setAttribute("data-visual-estable", "1");
        st.textContent = css;
        (document.head || document.documentElement).appendChild(st);
      };
      if (document.head) poner();
      else document.addEventListener("DOMContentLoaded", poner, { once: true });
    }, CSS_ESTABLE);

    await page.goto(new URL(ruta, BASE).href, { waitUntil: "networkidle2", timeout: 60000 });
    // Fuentes: capturar antes de que carguen pinta el texto con la fallback y TODO el
    // bloque de texto sale distinto -> falso positivo enorme.
    await page.evaluate(() => (document.fonts && document.fonts.ready) ? document.fonts.ready : null);
    await page.evaluate(() => new Promise((r) => setTimeout(r, 600)));
    // Recorrer la página fuerza el lazy-loading ANTES de medir el alto definitivo.
    await page.evaluate(async () => {
      const alto = () => Math.max(document.documentElement.scrollHeight, document.body.scrollHeight);
      for (let y = 0; y < alto(); y += 800) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 40)); }
      window.scrollTo(0, 0);
      await new Promise((r) => setTimeout(r, 400));
    });

    const H = await page.evaluate(() =>
      Math.max(document.documentElement.scrollHeight, document.body.scrollHeight));
    const alto = Math.min(H, MAX_ALTO);
    const vh = VIEWPORT.height;
    await lienzo.iniciar(alto, VIEWPORT.width);

    // Bandas: scroll real + captura del viewport. `fullPage` trunca en páginas largas
    // (ver cabecera); esto no.
    let bandas = 0;
    for (let y = 0; y < alto; y += vh) {
      const real = await page.evaluate((y, primera) => {
        window.scrollTo(0, y);
        // A partir de la 2ª banda se oculta lo que va FIJO en pantalla (nav, botones
        // flotantes): si no, se repetiría en cada banda y taparía el contenido real.
        // visibility:hidden no altera el layout, así que el alto de la página no cambia.
        if (!primera) {
          const todos = document.querySelectorAll("body *");
          for (let i = 0; i < todos.length; i++) {
            const p = getComputedStyle(todos[i]).position;
            if (p === "fixed" || p === "sticky") todos[i].style.visibility = "hidden";
          }
        }
        return window.scrollY;
      }, y, y === 0);
      await page.evaluate(() => new Promise((r) => setTimeout(r, 60)));
      const b64 = await page.screenshot({ type: "png", encoding: "base64" });
      await lienzo.pegar(b64, real, vh);
      bandas += 1;
      if (real + vh >= alto) break; // el scroll ya topó con el final de la página
    }

    const red = await lienzo.finalizar();
    return { ok: true, b64: red.b64, w: red.w, h: red.h, altoReal: H, bandas: bandas };
  } catch (e) {
    try { await lienzo.finalizar(); } catch (_) {} // no dejar el canvas a medias
    return { ok: false, error: e.message };
  } finally {
    try { await ctx.close(); } catch (_) {}
  }
}

// ---------------------------------------------------------------- main
async function main() {
  let puppeteer;
  try { puppeteer = (await import("puppeteer")).default; }
  catch (e) {
    add("alta", ".pipeline/check-visual.mjs",
      `verificación ciega: no se pudo cargar puppeteer (${e.message}); NADIE está mirando cómo se ve el sitio`,
      "Instalar/reparar puppeteer (`npm i`) para que la comparación visual vuelva a correr");
    out(0); return;
  }

  let browser;
  try {
    browser = await puppeteer.launch({
      headless: "new",
      executablePath: resolveChrome(),
      args: ["--no-sandbox", "--disable-setuid-sandbox", "--hide-scrollbars", "--force-device-scale-factor=1"],
    });
  } catch (e) {
    add("alta", ".pipeline/check-visual.mjs",
      `verificación ciega: Chrome no lanzó para la comparación visual (${e.message}); NADIE está mirando cómo se ve el sitio`,
      "Revisar PUPPETEER_EXECUTABLE_PATH / instalación de Chrome; mientras tanto una rotura visual (como el formulario roto 258 días) pasaría inadvertida");
    out(0); return;
  }

  let analizadas = 0;
  let lienzo;
  try {
    fs.mkdirSync(BASELINE_DIR, { recursive: true });
    lienzo = await abrirLienzo(browser);

    for (const ruta of URLS) {
      const slug = slugDe(ruta);
      const archivoBase = path.join(BASELINE_DIR, slug + ".png");
      const relBase = path.relative(ROOT, archivoBase);

      const cap = await capturar(browser, lienzo, ruta);
      if (!cap.ok) {
        add("media", ruta,
          `VISUAL: no se pudo capturar ${new URL(ruta, BASE).href} (${cap.error}); esta página quedó SIN comparación visual`,
          "Revisar disponibilidad de la página; si el 404/timeout es real, arreglarlo o quitar la URL de VISUAL_URLS");
        continue;
      }
      analizadas += 1;
      process.stderr.write(`visual ${ruta}: ${cap.bandas} bandas, ${cap.altoReal}px de alto real -> ${cap.w}x${cap.h}\n`);

      const existe = fs.existsSync(archivoBase);
      if (UPDATE || !existe) {
        fs.writeFileSync(archivoBase, Buffer.from(cap.b64, "base64"));
        if (!UPDATE) {
          add("baja", relBase,
            `VISUAL: no había línea base para ${ruta}; se estableció ahora (${relBase}, ${Math.round(Buffer.byteLength(cap.b64, "base64") / 1024)} KB). Desde la próxima corrida sí se compara`,
            "Ninguna acción: revisar de reojo que la página se vea bien hoy y commitear la línea base junto al resto del cambio");
        }
        continue;
      }

      const b64Base = fs.readFileSync(archivoBase).toString("base64");
      let d;
      try { d = await lienzo.diff(cap.b64, b64Base); }
      catch (e) {
        add("media", relBase,
          `VISUAL: falló la comparación de píxeles de ${ruta} (${e.message}); esta página quedó SIN verificar`,
          "Revisar que la línea base no esté corrupta; regenerarla con `node .pipeline/check-visual.mjs --update-baseline`");
        continue;
      }

      // Diagnóstico por stderr (stdout es SOLO el JSON del contrato): deja ver el margen
      // real contra el umbral aunque no haya hallazgo.
      process.stderr.write(`visual ${ruta}: ${d.pct.toFixed(2)} % distinto (umbral ${UMBRAL} %, base ${d.altoB}px vs ahora ${d.altoA}px)\n`);

      if (d.pct > UMBRAL) {
        const alturas = d.altoA !== d.altoB
          ? ` La página cambió de ALTO (base ${d.altoB}px vs ahora ${d.altoA}px, medido a ${ANCHO_DIFF}px de ancho): apareció o desapareció contenido.`
          : "";
        add("media", ruta,
          `VISUAL: ${ruta} se ve distinta a su línea base: ${d.pct.toFixed(2)} % de píxeles cambiados (umbral ${UMBRAL} %).${alturas} Precedente: el formulario de la home estuvo roto 258 días porque ningún checker MIRABA la página`,
          `Abrir ${new URL(ruta, BASE).href} en móvil (390x844) y compararla con ${relBase}. Si el cambio es una ROTURA, arreglarla; si es un rediseño intencional, ACEPTARLO regenerando la base con \`node .pipeline/check-visual.mjs --update-baseline\` y commitear los PNG`);
      }
    }
  } finally {
    if (lienzo) await lienzo.cerrar();
    try { await browser.close(); } catch (_) {}
  }

  if (UPDATE) process.stderr.write(`líneas base visuales actualizadas para ${analizadas} URL(s): ${BASELINE_DIR}\n`);
  out(analizadas);
}

main().catch((e) => {
  add("alta", ".pipeline/check-visual.mjs",
    `verificación ciega: fallo inesperado del checker visual: ${e.message}`,
    "Revisar/reparar .pipeline/check-visual.mjs");
  out(0);
});
