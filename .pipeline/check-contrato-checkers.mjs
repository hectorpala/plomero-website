#!/usr/bin/env node
// infra:utilidad-no-sensor  (utilidad de pre-push exit-0/1, NO emite {hallazgos} — que
//   check-infra.mjs no la trate como sensor de página, o daría una ALTA falsa infra-003).
// Gate PROACTIVO del contrato de checkers (clase regresión infra-003/005).
// Corre cada .pipeline/check-*.{py,mjs} que sea SENSOR DE PÁGINA (no NOT_PAGE_CHECKERS ni
// utilidad declarada) y verifica que imprima un JSON con array "hallazgos". exit 1 si alguno
// no cumple — pensado para pre-push, para que un checker roto no llegue a la corrida diaria
// (donde hoy dispara una ALTA falsa de "verificación ciega" un ciclo después).
import { spawnSync } from "child_process";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
const dir = path.dirname(fileURLToPath(import.meta.url));
const NOT_PAGE = new Set(["check-infra.mjs", "check-secretos.sh", "check-contrato-checkers.mjs"]);
const HEAVY = new Set(["check-produccion.mjs", "check-perf.mjs", "check-tracking.mjs", "check-e2e.mjs"]); // tocan red: omitir en pre-push
const esUtilidad = (f) => {
  try { return fs.readFileSync(`${dir}/${f}`, "utf8").slice(0, 800).includes("infra:utilidad-no-sensor"); }
  catch { return false; }
};
const checkers = fs.readdirSync(dir)
  .filter((f) => /^check-.*\.(py|mjs)$/.test(f) && !NOT_PAGE.has(f) && !HEAVY.has(f) && !esUtilidad(f))
  .sort();
let fallos = 0;
for (const f of checkers) {
  const runner = f.endsWith(".py") ? "python3" : process.execPath;
  let ok = false, motivo = "";
  try {
    const r = spawnSync(runner, [`${dir}/${f}`], { encoding: "utf8", timeout: 60000 });
    if (r.status !== 0) { motivo = `exit ${r.status}: ${(r.stderr || "").slice(0, 160)}`; }
    else {
      const data = JSON.parse(r.stdout);
      if (Array.isArray(data.hallazgos)) ok = true;
      else motivo = "el JSON no tiene array \"hallazgos\"";
    }
  } catch (e) { motivo = `no devolvió JSON parseable (${String(e).slice(0, 120)})`; }
  if (!ok) { fallos++; console.error(`❌ ${f}: ${motivo}`); }
}
if (fallos) {
  console.error(`\n${fallos} checker(s) NO emiten el contrato {hallazgos}. Si es una UTILIDAD, ` +
    `declara \`infra:utilidad-no-sensor\` en su cabecera; si es un sensor, arregla su salida.`);
  process.exit(1);
}
console.log(`✅ ${checkers.length} checkers emiten el contrato {hallazgos}.`);
