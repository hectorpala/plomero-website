#!/usr/bin/env node
// registrar-costo.mjs — Suma los TOKENS de todos los transcripts de una corrida (sesión
// principal + sidechains de los subagentes revisores) y anexa una línea al ledger de uso.
// No toca la corrida: se ejecuta DESPUÉS, y si algo falla solo deja "uso n/d" en el log.
//
// IMPORTANTE: este sistema corre por SUSCRIPCIÓN (Max), NO por API. El dato que importa son los
// TOKENS, como consumo de la CUOTA de suscripción (límites por ventana de 5h y tope semanal) —
// NO dólares facturados. El campo `usd_equiv_api_ref` es solo una referencia hipotética "si esto
// fuera API a precios Opus 4.x"; NO es lo que se paga. Sirve para dimensionar y cazar corridas
// anómalas (un loop que dispara el consumo), no para contabilidad.
//
// Uso:  node registrar-costo.mjs <dir-transcripts> <epoch-inicio> <ledger.jsonl> [etiqueta]
//
// Atribución por VENTANA DE TIEMPO: cuenta los .jsonl del proyecto con mtime >= inicio de la
// corrida. Caveat: si hubo una sesión interactiva en el MISMO proyecto durante la corrida,
// sus tokens se sumarían (sobre-estima). Para una corrida desatendida normal no ocurre.

import { readdirSync, statSync, readFileSync, appendFileSync } from 'fs';
import { join } from 'path';

const [, , DIR, startStr, LEDGER, LABEL = ''] = process.argv;
if (!DIR || !startStr || !LEDGER) {
  console.error('uso: registrar-costo.mjs <dir-transcripts> <epoch-inicio> <ledger.jsonl> [etiqueta]');
  process.exit(2);
}
const startMs = Number(startStr) * 1000;

// Precios estimados Opus 4.x — USD por 1M tokens. Ajustables por entorno si cambia el modelo/tarifa.
const P_IN = Number(process.env.PRECIO_IN ?? 15);
const P_OUT = Number(process.env.PRECIO_OUT ?? 75);
const P_CW = Number(process.env.PRECIO_CACHE_W ?? 18.75);
const P_CR = Number(process.env.PRECIO_CACHE_R ?? 1.5);

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
    const u = o?.message?.usage || o?.usage;
    if (!u) continue;
    inTok += u.input_tokens || 0;
    outTok += u.output_tokens || 0;
    cw += u.cache_creation_input_tokens || 0;
    cr += u.cache_read_input_tokens || 0;
    mensajes++;
  }
}

const usd = inTok / 1e6 * P_IN + outTok / 1e6 * P_OUT + cw / 1e6 * P_CW + cr / 1e6 * P_CR;
const rec = {
  fecha: new Date(startMs || Date.now()).toISOString().slice(0, 10),
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
};

try {
  appendFileSync(LEDGER, JSON.stringify(rec) + '\n');
} catch (e) {
  console.error('⚠️  no pude escribir el ledger de uso:', e.message);
}
console.log(
  `📊 Uso de la corrida (cuota de suscripción): ${(rec.total_tokens / 1e6).toFixed(2)}M tokens ` +
  `(in ${inTok} · out ${outTok} · cacheW ${cw} · cacheR ${cr}) · ${files} transcripts, ${mensajes} mensajes` +
  `  ·  ≈ $${rec.usd_equiv_api_ref} equiv-API (referencia, NO facturado)`
);
