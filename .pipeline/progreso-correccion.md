# Progreso — corrección autónoma del sistema de mantenimiento

Sesión de corrección en ramas (NO push, NO merge a main). Actualizado en vivo.
Punto de partida: `main` @ `4a0b2034` (3 ramas en vuelo ya integradas + checker-plantilla completado, sin push). origin/main en `62168bf2`.

## Cola AUTO

### RAMA `fix/pipeline-robustez` ✅ commit `8466e43f` (mantener-prompt.txt + SKILL.md + 4 revisores deterministas)
- [x] **A1 [candado]** Candado de publicación bajado a ≤15 archivos (prompt paso 8 + SKILL paso 12). Verificado: "máximo 15 archivos" en ambos, 0 ocurrencias de "200 archivos".
- [x] **A2 [verificación ciega]** Los 4 revisores DETERMINISTAS (indexabilidad, produccion, plantilla, gsc) emiten hallazgo ALTA "verificación ciega: <tool> no devolvió datos" si su tool falla o devuelve vacío anómalo. Instrucción en prompt paso 3 + SKILL paso 4 + 1 línea en cada `.md` (con id `<prefijo>-ciega`). Verificado: presente en los 6 archivos; ningún revisor mantiene el viejo `{"hallazgos":[]}` silencioso.
- [x] **A3 [dedup por id]** Dedup firma por regla canónica estable (archivo+categoria+clave-de-regla) en prompt paso 4 + SKILL paso 6. Verificado en ambos.
- Evidencia: `git diff --stat main` = 6 archivos, frontmatter de revisores intacto.

### RAMA `fix/monitor-dedup` ✅ commit `ccfa7a5d`
- [x] **A4 [H-11]** `site-monitor.yml`: dedup de Issues (etiqueta `monitor-automatico`: si ya hay uno abierto, comenta en vez de abrir otro cada 6h) + bloque `permissions` (contents:read, issues:write). Mismo patrón que `seo-check.yml`. Verificado: YAML válido (`yaml.safe_load` OK), listForRepo+createComment+create presentes.

### RAMA `feat/ensenar-genera-test` ✅ commit `553501fd` (base main; checker-plantilla ya en main)
- [x] **A5 [aprendizaje]** `ensenar/SKILL.md`: clasifica mecánico↔subjetivo. Mecánico → assert determinista en `check-plantilla.py` (patrón `add()`/`check_*`, actualiza docstring, verifica que el test falla ante el bug + md5 estable); subjetivo → línea al revisor LLM. Verificado: todos los símbolos referenciados (add, check_page, attr, imgs, resolve_to_disk, has_noindex, check_css_parity) existen con esa firma.

### RAMA `fix/stubs-noindex` ✅ commit `5f89e64b`
- [x] **A6 [seo-004]** `<meta name="robots" content="noindex">` en los 6 redirect-stubs `servicios/plomero/*`. Insertado tras el meta-refresh con la indentación de cada archivo. Verificado: diff = +6 líneas (1/archivo), noindex/refresh/canonical=1 en los 6; el checker ignora stubs (sin ruido).

## Movido a COLA HUMANA
- **A7 [H-06] rollback-post-push** → PENDIENTES-HUMANO.md con propuesta de diseño. Razón: no hay señal fiable de fin de deploy Netlify sin API/token (el propio fix/seo-check-workflow eliminó el trigger push por esto); un `git revert`+push autónomo sobre esa señal es demasiado riesgoso sin supervisión.

## Estado — COLA AUTO VACÍA ✅ (2026-06-14)
Todos los items AUTO implementados en ramas (A1–A6) o movidos a humano con justificación (A7).
PENDIENTES-HUMANO.md completo. Ninguna rama pusheada ni mergeada — pendiente revisión + push/merge por Héctor.

| Rama | Commit | Items | Verificación |
|------|--------|-------|--------------|
| `fix/pipeline-robustez` | `8466e43f` | A1, A2, A3 | candado 15 en prompt+SKILL (0 "200"); "verificación ciega" en prompt+SKILL+4 revisores; firma canónica en ambos; frontmatter intacto |
| `fix/monitor-dedup` | `ccfa7a5d` | A4 | YAML válido (`yaml.safe_load`); listForRepo+createComment+create; permissions añadido |
| `feat/ensenar-genera-test` | `553501fd` | A5 | símbolos de check-plantilla.py referenciados existen con su firma; frontmatter intacto |
| `fix/stubs-noindex` | `5f89e64b` | A6 | diff +6 líneas (1/stub); noindex/refresh/canonical=1 en los 6 |

**Orden de merge recomendado:** las 4 son independientes (archivos disjuntos) y parten de `main` @ `4a0b2034` → mergeables en cualquier orden, sin conflictos entre sí. (fix/pipeline-robustez y feat/ensenar-genera-test ambos conceptualmente sobre el sistema de checker, pero tocan archivos distintos.)

**Movido a humano:** A7 (H-06 rollback-post-push) → PENDIENTES-HUMANO.md, por señal de deploy Netlify no fiable sin API/token (mismo motivo por el que fix/seo-check-workflow quitó el trigger push).

**Artefactos sin trackear (intencionales, no commiteados):** `.pipeline/progreso-correccion.md` (este archivo) y `.pipeline/PENDIENTES-HUMANO.md`.
