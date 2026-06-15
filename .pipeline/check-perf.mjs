#!/usr/bin/env node
// Checker de RENDIMIENTO REAL (Core Web Vitals) para plomeroculiacanpro.mx.
// Conecta lo que site-monitor.yml ya medía pero TIRABA: en vez de quedarse solo
// con el "score" de Lighthouse y descartar el JSON, persiste una BASELINE y compara
// LCP/CLS/INP contra (a) un PRESUPUESTO absoluto y (b) regresión vs la baseline.
// Usa la MEDIANA de varias corridas para no disparar por ruido.
//
// Solo REPORTA. Emite a stdout SOLO el JSON común de hallazgos:
//   {"hallazgos":[{id,archivo,linea,severidad,categoria,descripcion,fix_sugerido}], "analizadas":N}
// categoria = "perf".
//
// FUENTES DE MÉTRICAS (en orden de preferencia):
//  1. Reportes Lighthouse JSON (lo que produce site-monitor.yml en CI): vía
//     env PERF_REPORTS="r1.json,r2.json,..." o, si no, los .pipeline/lighthouse-run-*.json
//     presentes. Se agrupan por finalUrl y se toma la MEDIANA por métrica.
//  2. Medición local con puppeteer + Chrome (mismo stack que check-produccion): 3
//     cargas por URL clave, mediana de LCP/CLS y un INP aproximado por interacción.
//     (Se usa cuando no hay reportes Lighthouse — p.ej. la corrida local del pipeline.)
//  Si NINGUNA fuente da datos → verificación ciega (ALTA): no se pudo MEDIR.
//
// BASELINE: .pipeline/perf-baseline.json ({url:{lcp,cls,inp}}). Se ESCRIBE solo con
// `--update-baseline` (el checker normal solo REPORTA, no toca la baseline). Si no
// existe baseline, igual se valida el presupuesto absoluto y se avisa (baja) que
// falta establecerla.
//
// PRESUPUESTO (acordado con Héctor — Google "good"): LCP<2500ms, CLS<0.1, INP<200ms.
// REGRESIÓN vs baseline: empeora >20% Y supera un piso de ruido (LCP +200ms, CLS
// +0.02, INP +50ms). Debe superar AMBOS para contar (evita falsos positivos de ruido).

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.dirname(__dirname);
const BASE = process.env.PERF_BASE || "https://plomeroculiacanpro.mx";
const BASELINE_FILE = process.env.PERF_BASELINE || path.join(__dirname, "perf-baseline.json");
const UPDATE = process.argv.includes("--update-baseline");

const BUDGET = { lcp: 2500, cls: 0.1, inp: 200 };          // unidades: ms, unitless, ms
const REL = 0.20;                                          // regresión relativa mínima
const FLOOR = { lcp: 200, cls: 0.02, inp: 50 };            // piso de ruido absoluto
const UNIT = { lcp: "ms", cls: "", inp: "ms" };
const DEFAULT_URLS = (process.env.PERF_URLS || "/,/servicios/reparacion-de-fugas/").split(",").map((s) => s.trim()).filter(Boolean);

const hallazgos = [];
let seq = 0;
function add(sev, archivo, desc, fix, linea = 0) {
  seq += 1;
  hallazgos.push({
    id: "perf-" + String(seq).padStart(3, "0"),
    archivo, linea, severidad: sev, categoria: "perf",
    descripcion: desc, fix_sugerido: fix,
  });
}
function out(analizadas) {
  process.stdout.write(JSON.stringify({ hallazgos, analizadas }, null, 2) + "\n");
}
function median(xs) {
  const a = xs.filter((x) => typeof x === "number" && !Number.isNaN(x)).sort((p, q) => p - q);
  if (!a.length) return null;
  const m = Math.floor(a.length / 2);
  return a.length % 2 ? a[m] : (a[m - 1] + a[m]) / 2;
}
function urlPath(u) {
  try { return new URL(u, BASE).pathname; } catch (_) { return u; }
}
function round(metric, v) { return metric === "cls" ? Math.round(v * 1000) / 1000 : Math.round(v); }

// ---------------------------------------------------------------- fuente 1: Lighthouse JSON
function lighthouseReports() {
  let files = [];
  if (process.env.PERF_REPORTS) {
    files = process.env.PERF_REPORTS.split(",").map((s) => s.trim()).filter(Boolean);
  } else {
    try {
      files = fs.readdirSync(__dirname)
        .filter((f) => /^lighthouse-run-.*\.json$/.test(f))
        .map((f) => path.join(__dirname, f));
    } catch (_) { files = []; }
  }
  const byUrl = {}; // url -> {lcp:[],cls:[],inp:[], inpSrc}
  for (const f of files) {
    let rep;
    try { rep = JSON.parse(fs.readFileSync(f, "utf-8")); } catch (_) { continue; }
    const url = urlPath(rep.finalUrl || rep.requestedUrl || rep.finalDisplayedUrl || "/");
    const A = rep.audits || {};
    const lcp = A["largest-contentful-paint"]?.numericValue;
    const cls = A["cumulative-layout-shift"]?.numericValue;
    // Lighthouse "lab" no mide INP (es métrica de campo). Si existe el audit, úsalo;
    // si no, TBT como PROXY documentado.
    let inp = A["interaction-to-next-paint"]?.numericValue;
    let inpSrc = "lighthouse:inp";
    if (typeof inp !== "number") { inp = A["total-blocking-time"]?.numericValue; inpSrc = "lighthouse:tbt(proxy)"; }
    const e = (byUrl[url] = byUrl[url] || { lcp: [], cls: [], inp: [], inpSrc });
    if (typeof lcp === "number") e.lcp.push(lcp);
    if (typeof cls === "number") e.cls.push(cls);
    if (typeof inp === "number") { e.inp.push(inp); e.inpSrc = inpSrc; }
  }
  return byUrl;
}

// ---------------------------------------------------------------- fuente 2: puppeteer
async function puppeteerMeasure() {
  let puppeteer;
  try { puppeteer = (await import("puppeteer")).default; } catch (_) { return null; }
  const cands = [
    process.env.PUPPETEER_EXECUTABLE_PATH,
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
  ].filter((c) => c && fs.existsSync(c));
  let browser;
  try {
    browser = await puppeteer.launch({ headless: "new", executablePath: cands[0],
      args: ["--no-sandbox", "--disable-setuid-sandbox"] });
  } catch (_) { return null; }
  const byUrl = {};
  try {
    for (const u of DEFAULT_URLS) {
      const full = new URL(u, BASE).href;
      const e = { lcp: [], cls: [], inp: [], inpSrc: "puppeteer:event(aprox)" };
      for (let i = 0; i < 3; i++) {
        const page = await browser.newPage();
        try {
          await page.evaluateOnNewDocument(() => {
            window.__cls = 0; window.__lcp = 0; window.__inp = 0;
            new PerformanceObserver((l) => { for (const en of l.getEntries())
              if (!en.hadRecentInput) window.__cls += en.value; }).observe({ type: "layout-shift", buffered: true });
            new PerformanceObserver((l) => { const es = l.getEntries();
              window.__lcp = es[es.length - 1].renderTime || es[es.length - 1].loadTime || window.__lcp;
            }).observe({ type: "largest-contentful-paint", buffered: true });
            new PerformanceObserver((l) => { for (const en of l.getEntries())
              window.__inp = Math.max(window.__inp, en.duration); }).observe({ type: "event", buffered: true, durationThreshold: 16 });
          });
          await page.goto(full, { waitUntil: "networkidle2", timeout: 60000 });
          // provocar una interacción para alimentar INP aproximado
          try { await page.mouse.click(10, 10); await page.evaluate(() => new Promise((r) => setTimeout(r, 300))); } catch (_) {}
          const m = await page.evaluate(() => ({ lcp: window.__lcp, cls: window.__cls, inp: window.__inp }));
          if (typeof m.lcp === "number" && m.lcp > 0) e.lcp.push(m.lcp);
          if (typeof m.cls === "number") e.cls.push(m.cls);
          if (typeof m.inp === "number" && m.inp > 0) e.inp.push(m.inp);
        } catch (_) { /* una carga falló; las otras dos siguen */ }
        await page.close();
      }
      byUrl[urlPath(u)] = e;
    }
  } finally {
    await browser.close();
  }
  return byUrl;
}

// ---------------------------------------------------------------- comparación
function loadBaseline() {
  try { return JSON.parse(fs.readFileSync(BASELINE_FILE, "utf-8")); } catch (_) { return null; }
}

async function main() {
  // fuente
  let byUrl = lighthouseReports();
  let fuente = "lighthouse";
  if (Object.keys(byUrl).length === 0) {
    const p = await puppeteerMeasure();
    if (p && Object.keys(p).length) { byUrl = p; fuente = "puppeteer"; }
  }

  // medianas
  const medians = {}; // url -> {lcp,cls,inp,inpSrc}
  for (const [url, e] of Object.entries(byUrl)) {
    const med = { lcp: median(e.lcp), cls: median(e.cls), inp: median(e.inp), inpSrc: e.inpSrc };
    if (med.lcp == null && med.cls == null && med.inp == null) continue;
    medians[url] = med;
  }
  const urls = Object.keys(medians).sort();
  const analizadas = urls.length;

  if (analizadas === 0) {
    add("alta", ".pipeline/check-perf.mjs",
      "verificación ciega: no se pudieron MEDIR Core Web Vitals (ni reportes Lighthouse en PERF_REPORTS/.pipeline/lighthouse-run-*.json, ni puppeteer/Chrome disponible)",
      "En CI: que site-monitor.yml corra Lighthouse y deje los JSON; en local: que puppeteer+Chrome estén instalados. Mientras tanto el rendimiento NO se está midiendo");
    out(0);
    return;
  }

  // modo --update-baseline: escribe y termina (no es un hallazgo)
  if (UPDATE) {
    const bl = {};
    for (const u of urls) bl[u] = { lcp: round("lcp", medians[u].lcp ?? 0), cls: round("cls", medians[u].cls ?? 0),
      inp: round("inp", medians[u].inp ?? 0), inpSrc: medians[u].inpSrc, fuente };
    fs.writeFileSync(BASELINE_FILE, JSON.stringify(bl, null, 2) + "\n");
    process.stderr.write(`baseline actualizada (${fuente}) para ${urls.length} URL(s): ${BASELINE_FILE}\n`);
    out(analizadas);
    return;
  }

  const baseline = loadBaseline();
  if (!baseline) {
    add("baja", path.relative(ROOT, BASELINE_FILE),
      `PERF: no hay baseline de Core Web Vitals (${path.relative(ROOT, BASELINE_FILE)}); se valida el presupuesto absoluto pero NO la regresión`,
      "Establecer la baseline con `node .pipeline/check-perf.mjs --update-baseline` (idealmente desde site-monitor.yml en CI con Lighthouse)");
  }

  for (const url of urls) {
    const m = medians[url];
    // presupuesto absoluto
    for (const metric of ["lcp", "cls", "inp"]) {
      const v = m[metric];
      if (v == null) continue;
      const isProxy = metric === "inp" && m.inpSrc && m.inpSrc.includes("proxy");
      if (v > BUDGET[metric]) {
        add(metric === "cls" || metric === "lcp" ? "alta" : (isProxy ? "media" : "alta"), url,
          `PERF: ${url} ${metric.toUpperCase()} mediana ${round(metric, v)}${UNIT[metric]} supera el presupuesto ${BUDGET[metric]}${UNIT[metric]}${isProxy ? " (INP medido por proxy TBT — el lab no da INP)" : ""} [fuente:${m.inpSrc && metric === "inp" ? m.inpSrc : fuente}]`,
          metric === "lcp" ? "Optimizar el LCP: imagen hero con fetchpriority=high y dimensiones, menos bloqueo de render, preconnect"
            : metric === "cls" ? "Reservar espacio (width/height en imágenes, evitar inserciones tardías) para bajar el CLS"
            : "Reducir el trabajo del hilo principal (menos JS bloqueante, dividir tareas largas) para bajar INP/TBT");
      }
    }
    // regresión vs baseline
    const b = baseline && baseline[url];
    if (b) {
      for (const metric of ["lcp", "cls", "inp"]) {
        const v = m[metric], bv = b[metric];
        if (v == null || typeof bv !== "number" || bv <= 0) continue;
        const delta = v - bv;
        if (delta > FLOOR[metric] && delta > bv * REL) {
          add("media", url,
            `PERF/REGRESIÓN: ${url} ${metric.toUpperCase()} subió de ${round(metric, bv)}${UNIT[metric]} (baseline) a ${round(metric, v)}${UNIT[metric]} (+${Math.round((delta / bv) * 100)}%), supera +20% y el piso de ruido`,
            "Revisar qué cambio reciente degradó esta métrica; comparar con el último diff. Si la regresión es intencional y aceptada, re-baseline con --update-baseline");
        }
      }
    }
  }
  out(analizadas);
}

main().catch((e) => {
  add("alta", ".pipeline/check-perf.mjs",
    `verificación ciega: fallo inesperado del checker de perf: ${e.message}`,
    "Revisar/reparar .pipeline/check-perf.mjs");
  out(0);
});
