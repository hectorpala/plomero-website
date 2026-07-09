#!/usr/bin/env node
// registrar-costo.mjs — Suma los TOKENS de todos los transcripts de una corrida (sesión
// principal + sidechains de los subagentes revisores) y anexa una línea al ledger de uso.
// No toca la corrida: se ejecuta DESPUÉS, y si algo falla solo deja "uso n/d" en el log.
//
// IMPORTANTE: este sistema corre por SUSCRIPCIÓN (Max), NO por API. El dato que importa son los
// TOKENS, como consumo de la CUOTA de suscripción (límites por ventana de 5h y tope semanal) —
// NO dólares facturados. El campo `usd_equiv_api_ref` es solo una referencia hipotética "si esto
// fuera API"; NO es lo que se paga. Sirve para dimensionar y cazar corridas anómalas.
//
// BASE DE PRECIOS (cambiada el 2026-07-08): antes se cotizaba TODO a precios Opus, aunque la
// corrida es MULTI-MODELO (orquestador en Sonnet + revisores en Haiku/Sonnet/Opus). Eso inflaba
// la referencia ~5x y volvía inútil el tripwire de presupuesto. Ahora cada mensaje se cotiza con
// SU modelo (`message.model` del transcript) y se emite el desglose `por_modelo`.
// OJO: las filas del ledger ANTERIORES a esa fecha están en base Opus y NO son comparables en
// `usd_equiv_api_ref` (sí lo son en tokens, que no dependen del modelo).
//
// Uso:  node registrar-costo.mjs <dir-transcripts> <epoch-inicio> <ledger.jsonl> [etiqueta]
//
// Atribución por VENTANA DE TIEMPO en dos niveles: (1) archivos con mtime >= inicio (filtro
// grueso) y (2) DENTRO de cada archivo, solo las líneas cuyo timestamp cae en la ventana.
// Antes se sumaba el archivo ENTERO: una sesión interactiva vieja retomada durante la corrida
// contabilizaba todo su pasado al auto-agente (ledger inflado + falso positivo runaway).

import { readdirSync, statSync, readFileSync, appendFileSync } from 'fs';
import { join } from 'path';

const [, , DIR, startStr, LEDGER, LABEL = ''] = process.argv;
if (!DIR || !startStr || !LEDGER) {
  console.error('uso: registrar-costo.mjs <dir-transcripts> <epoch-inicio> <ledger.jsonl> [etiqueta]');
  process.exit(2);
}
const startMs = Number(startStr) * 1000;

// Precios USD por 1M tokens, POR FAMILIA de modelo. El patrón es estable: out = 5x in,
// cacheW = 1.25x in, cacheR = 0.1x in. Un modelo desconocido se cotiza como opus (conservador:
// nunca subestima) y se reporta en `modelos_desconocidos` para que se note y se agregue aquí.
const PRECIOS = {
  opus:   { in: 15, out: 75, cw: 18.75, cr: 1.5  },
  sonnet: { in: 3,  out: 15, cw: 3.75,  cr: 0.3  },
  haiku:  { in: 1,  out: 5,  cw: 1.25,  cr: 0.1  },
  sintetico: { in: 0, out: 0, cw: 0, cr: 0 },   // '<synthetic>': mensajes locales, no consumen API
};

// De 'claude-sonnet-5' / 'claude-opus-4-8' / 'claude-haiku-4-5-20251001' a la familia.
function familiaDe(model) {
  if (!model) return 'desconocido';
  if (model === '<synthetic>') return 'sintetico';
  if (model.includes('opus')) return 'opus';
  if (model.includes('sonnet')) return 'sonnet';
  if (model.includes('haiku')) return 'haiku';
  return 'desconocido';
}
const precioDe = (fam) => PRECIOS[fam] ?? PRECIOS.opus;   // desconocido -> opus (conservador)

function* walk(d) {
  let ents;
  try { ents = readdirSync(d, { withFileTypes: true }); } catch { return; }
  for (const e of ents) {
    const p = join(d, e.name);
    if (e.isDirectory()) yield* walk(p);
    else if (e.isFile() && e.name.endsWith('.jsonl')) yield p;
  }
}

let inTok = 0, outTok = 0, cw = 0, cr = 0, files = 0, mensajes = 0;
const porModelo = {};                 // familia -> {mensajes, input, output, cache_write, cache_read, usd}
const desconocidos = new Set();       // ids de modelo sin precio conocido (se cotizan como opus)
const acum = (fam) => (porModelo[fam] ??= { mensajes: 0, input: 0, output: 0, cache_write: 0, cache_read: 0, usd: 0 });
for (const f of walk(DIR)) {
  let st;
  try { st = statSync(f); } catch { continue; }
  if (st.mtimeMs < startMs) continue;          // fuera de la ventana de esta corrida
  files++;
  let txt;
  try { txt = readFileSync(f, 'utf-8'); } catch { continue; }
  for (const ln of txt.split('\n')) {
    if (!ln.includes('"usage"')) continue;
    let o;
    try { o = JSON.parse(ln); } catch { continue; }
    // Solo mensajes DE ESTA corrida: si la línea trae timestamp y es anterior al
    // inicio, es historia de otra sesión dentro del mismo archivo — no se cuenta.
    if (o?.timestamp) {
      const t = Date.parse(o.timestamp);
      if (!Number.isNaN(t) && t < startMs) continue;
    }
    const u = o?.message?.usage || o?.usage;
    if (!u) continue;
    const i = u.input_tokens || 0, ou = u.output_tokens || 0;
    const w = u.cache_creation_input_tokens || 0, r = u.cache_read_input_tokens || 0;
    inTok += i; outTok += ou; cw += w; cr += r; mensajes++;

    // Cotización POR MODELO: cada mensaje con el suyo (`message.model`), no todo a Opus.
    const modelo = o?.message?.model;
    const fam = familiaDe(modelo);
    if (fam === 'desconocido' && modelo) desconocidos.add(modelo);
    const p = precioDe(fam);
    const a = acum(fam);
    a.mensajes++; a.input += i; a.output += ou; a.cache_write += w; a.cache_read += r;
    a.usd += i / 1e6 * p.in + ou / 1e6 * p.out + w / 1e6 * p.cw + r / 1e6 * p.cr;
  }
}

const usd = Object.values(porModelo).reduce((s, a) => s + a.usd, 0);
// Redondeo del desglose (2 decimales) para que el ledger sea legible.
for (const a of Object.values(porModelo)) a.usd = Math.round(a.usd * 100) / 100;
const rec = {
  // Fecha LOCAL (Mazatlán), no UTC: toISOString fechaba las corridas de las 18:25
  // en el día siguiente (UTC-7) y todo análisis por día quedaba corrido.
  fecha: new Date(startMs || Date.now()).toLocaleDateString('sv-SE', { timeZone: 'America/Mazatlan' }),
  inicio_epoch: Number(startStr),
  etiqueta: LABEL,
  transcripts: files,
  mensajes,
  input_tokens: inTok,
  output_tokens: outTok,
  cache_write_tokens: cw,
  cache_read_tokens: cr,
  total_tokens: inTok + outTok + cw + cr,
  usd_equiv_api_ref: Math.round(usd * 100) / 100,   // referencia hipotética "si fuera API"; NO se paga (corre por suscripción)
  base_precios: "por-modelo",                       // filas viejas: base "opus" (no comparables en USD)
  por_modelo: porModelo,                            // desglose real: quién gastó qué
  ...(desconocidos.size ? { modelos_desconocidos: [...desconocidos] } : {}),
};

try {
  appendFileSync(LEDGER, JSON.stringify(rec) + '\n');
} catch (e) {
  console.error('⚠️  no pude escribir el ledger de uso:', e.message);
}
// Desglose "sonnet 12.4M/$3.1 · haiku 0.9M/$0.1": deja ver de un vistazo si el orquestador
// se subió a Opus por accidente (el gasto se dispara sin que cambien los tokens).
const desglose = Object.entries(porModelo)
  .filter(([f]) => f !== 'sintetico')
  .sort((a, b) => b[1].usd - a[1].usd)
  .map(([f, a]) => `${f} ${((a.input + a.output + a.cache_write + a.cache_read) / 1e6).toFixed(1)}M/$${a.usd}`)
  .join(' · ');
console.log(
  `📊 Uso de la corrida (cuota de suscripción): ${(rec.total_tokens / 1e6).toFixed(2)}M tokens ` +
  `(in ${inTok} · out ${outTok} · cacheW ${cw} · cacheR ${cr}) · ${files} transcripts, ${mensajes} mensajes` +
  `  ·  ≈ $${rec.usd_equiv_api_ref} equiv-API (referencia, NO facturado)` +
  (desglose ? `  ·  [${desglose}]` : '') +
  (desconocidos.size ? `  ·  ⚠️ modelo(s) sin precio: ${[...desconocidos].join(',')} (cotizados como opus)` : '')
);
