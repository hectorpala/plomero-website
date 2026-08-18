#!/usr/bin/env node
// Registra el consumo de una corrida de Codex a partir del JSONL emitido por `codex exec --json`.
// Codex corre con la suscripción de ChatGPT: se registran tokens para detectar corridas anómalas,
// pero no se inventa un costo API equivalente cuando el modelo/tarifa no viene en el evento.

import { appendFileSync, readFileSync, statSync } from 'fs';

const [, , LOG, startStr, LEDGER, LABEL = ''] = process.argv;
if (!LOG || !startStr || !LEDGER) {
  console.error('uso: registrar-costo.mjs <log-jsonl> <epoch-inicio> <ledger.jsonl> [etiqueta]');
  process.exit(2);
}

let text = '';
try {
  if (statSync(LOG).isFile()) text = readFileSync(LOG, 'utf8');
} catch (error) {
  console.error(`⚠️ no pude leer el log de Codex: ${error.message}`);
}

let input = 0;
let output = 0;
let cachedInput = 0;
let cacheWrite = 0;
let reasoningOutput = 0;
let turns = 0;
let completedItems = 0;

for (const line of text.split('\n')) {
  let event;
  try { event = JSON.parse(line); } catch { continue; }
  if (event?.type === 'item.completed') completedItems += 1;
  if (event?.type !== 'turn.completed' || !event?.usage) continue;
  const usage = event.usage;
  input += Number(usage.input_tokens || 0);
  output += Number(usage.output_tokens || 0);
  cachedInput += Number(usage.cached_input_tokens || 0);
  cacheWrite += Number(usage.cache_write_input_tokens || 0);
  reasoningOutput += Number(usage.reasoning_output_tokens || 0);
  turns += 1;
}

const startMs = Number(startStr) * 1000;
const rec = {
  fecha: new Date(startMs || Date.now()).toLocaleDateString('sv-SE', { timeZone: 'America/Mazatlan' }),
  inicio_epoch: Number(startStr),
  etiqueta: LABEL,
  proveedor: 'codex',
  transcripts: text ? 1 : 0,
  mensajes: completedItems,
  turnos_completados: turns,
  input_tokens: input,
  output_tokens: output,
  cache_write_tokens: cacheWrite,
  cache_read_tokens: cachedInput,
  reasoning_output_tokens: reasoningOutput,
  // cached_input_tokens y reasoning_output_tokens ya son subconjuntos; no se suman dos veces.
  total_tokens: input + output,
  usd_equiv_api_ref: 0,
  base_precios: 'codex-suscripcion-sin-precio',
};

try {
  appendFileSync(LEDGER, JSON.stringify(rec) + '\n');
} catch (error) {
  console.error(`⚠️ no pude escribir el ledger de uso: ${error.message}`);
  process.exit(1);
}

console.log(
  `📊 Uso de la corrida Codex (suscripción): ${(rec.total_tokens / 1e6).toFixed(2)}M tokens ` +
  `(in ${input} · out ${output} · cacheR ${cachedInput} · reasoning ${reasoningOutput}) · ` +
  `${turns} turno(s), ${completedItems} ítems completados · costo API no calculado`
);
