# Progreso — Revisores faltantes (9 nuevos: 9 → 18)

Rama: `feat/revisores-faltantes` (desde main). UN commit por revisor. NO push / NO merge.
Patrón por revisor: checker `.pipeline/check-<x>.{py|mjs|sh}` (solo REPORTA, JSON común,
determinista) + agente `.claude/agents/revisor-<x>.md` + registro en
`.pipeline/mantener-prompt.txt` (paso 3) y `.claude/skills/mantener-sitio/SKILL.md` (FASE 1) +
evidencia (sintaxis, corrida real, PRUEBA NEGATIVA, determinismo md5) + commit.

JSON común: `{"hallazgos":[{id,archivo,linea,severidad,categoria,descripcion,fix_sugerido}]}`

Umbrales acordados con Héctor (2026-06-14):
- "Página clave" con formulario obligatorio (ALTA): **/contacto/ y home** únicamente (hoy ambas
  tienen `<form>` → 0 falsos positivos). `tel:` (667 392 2273 / 526673922273) + `wa.me` + CTA
  antes del fold se exigen en TODA página indexable. "Form en cada servicio" queda como posible
  mejora futura, NO hallazgo ALTA.
- Core Web Vitals: Google "good" → LCP<2.5s, CLS<0.1, INP<200ms + regresión vs baseline
  (mediana de 3 corridas).

Leyenda estado: ⬜ pendiente · 🔄 en curso · ✅ hecho+commit · 🧑 cola humana (con pregunta)

---

## FASE 1 — confianza en los sensores + seguridad
- [x] ✅ #1 revisor-infra-salud → `.pipeline/check-infra.mjs` (dead-man's switch, corre PRIMERO)
- [ ] #2 revisor-secretos → `.pipeline/check-secretos.sh` (+ candado de publicación)

## FASE 2 — conectar lo que ya existe
- [ ] #3 revisor-perf-real → baseline + presupuesto CWV (puede tocar site-monitor.yml → push SSH)
- [ ] #4 revisor-tracking → `verificar-tracking.js` envuelto (dataLayer/GTM/GA)

## FASE 3 — ofensiva / negocio
- [ ] #5 revisor-conversion → `.pipeline/check-conversion.py`
- [ ] #6 revisor-nap → teléfono/email/nombre idénticos en todas las páginas

## FASE 4 — profundidad
- [ ] #7 revisor-enlazado-interno → `.pipeline/check-linking.py` (huérfanas, profundidad >3)
- [ ] #8 revisor-contenido → parte mecánica (regex restos plantilla); subjetivo → LLM
- [ ] #9 revisor-e2e-funcional → `.pipeline/check-e2e.mjs` (puppeteer)

---

## Bitácora de diseño y evidencia

### #1 revisor-infra-salud — ✅ HECHO (commit en esta rama)
**Qué valida:** dead-man's switch del pipeline (no el sitio, los SENSORES). (a) frescura del
cron: log run-*.log más reciente en ~/Library/Logs/mantener-sitio/ <26h; (b) GSC vivo:
`webmasters.sites.list` con el token de mcp-local-seo (401/vacío → ALTA "GSC ciego"); (c)
checkers sanos: los deterministas LOCALES (indexabilidad, plantilla, + nuevos) se corren
completos y deben dar exit 0 + JSON con `hallazgos` + sin `error` + `analizadas`>0 si lo
exponen; los PESADOS (produccion, perf, tracking, e2e) reciben smoke (`node --check` +
puppeteer resuelve); + sanidad de corpus (sitemap >0 `<loc>`, >0 .html servidos); (d)
producción 200. Corre PRIMERO en el pipeline.
**Decisiones:** no se modifican los 3 checkers existentes → `analizadas` es campo opcional;
los pesados solo smoke para no duplicar trabajo caro (cada uno corre como su revisor).
Overrides solo-para-autopruebas vía env (INFRA_LOG_DIR / INFRA_CRON_MAX_HOURS / INFRA_BASE),
nunca seteados en producción (mismo patrón que PUPPETEER_EXECUTABLE_PATH en check-produccion).
**Determinista:** SÍ. Caso sano → `{"hallazgos":[]}`; descripciones sin timestamps/edades
volátiles. 2 corridas back-to-back → md5 idéntico (382b13bc...).
**Prueba negativa (6 ramas, todas detectan, repo restaurado idéntico):**
- (a) cron viejo: `INFRA_CRON_MAX_HOURS=0.0001` → ALTA "el log de cron más reciente ... supera el umbral".
- (b) GSC ciego: token movido a /tmp → ALTA "GSC ciego — webmasters.sites.list falló"; token restaurado.
- (c) local analizadas:0: scratch `check-zzscratchA.py` → ALTA "analizó 0 páginas/URLs"; borrado.
- (c) local JSON inválido: scratch `check-zzscratchB.py` → ALTA "no imprimió JSON parseable"; borrado.
- (c) heavy sintaxis rota: scratch `check-tracking.mjs` roto → ALTA "no pasa 'node --check'"; borrado.
- (d) prod caída: `INFRA_BASE=http://127.0.0.1:9` → ALTA "producción ... no responde (fetch failed)".
**Corrida real sobre el repo:** `{"hallazgos":[]}` (todos los sensores vivos: cron fresco,
token GSC válido, indexabilidad+plantilla limpios, prod 200).
