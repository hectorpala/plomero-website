---
name: mantener-sitio
description: Pipeline de mantenimiento autónomo del sitio — health check, revisión, arreglo, verificación y aprendizaje. Invocar con /mantener-sitio.
---

# Pipeline de mantenimiento autónomo

Ejecuta este ciclo en orden. Muestra EVIDENCIA en cada fase, no solo afirmaciones.

## FASE 0 — Memoria
1. Lee REGLAS.md (errores que NO debes repetir), ESTADO.md (estado anterior) y las últimas líneas de HISTORIAL.jsonl.

## FASE 0.5 — Health Check (ANTES de tocar nada)
2. Levanta un servidor local estático (ej: `python3 -m http.server 8080` en background) sobre la raíz del sitio.
3. Comprueba que la home y 2-3 páginas clave (/precios/, /contacto/) responden 200 con `curl -sI`. Si algo está roto YA, anótalo como hallazgo de severidad alta.

## FASE 1 — Revisión (en paralelo)
4. Son 14 subagentes revisores. **PRIMERO**, como compuerta, corre **revisor-infra-salud** (dead-man's switch, DETERMINISTA, `node .pipeline/check-infra.mjs`): verifica que los SENSORES del pipeline funcionan (frescura del cron <26h, token GSC vivo, los checkers deterministas corren sin error y sobre corpus no vacío, producción 200). Si grita ALTA, la corrida es sospechosa: prioriza esa señal antes de confiar en el resto. Luego lanza con la herramienta Task, en paralelo (un solo mensaje, varias llamadas), los 13 restantes: revisor-seo, revisor-movil, revisor-a11y, revisor-perf, revisor-links, revisor-gsc, revisor-indexabilidad, revisor-produccion, revisor-plantilla, revisor-secretos, revisor-perf-real, revisor-tracking, revisor-conversion. **revisor-conversion** es DETERMINISTA (`python3 .pipeline/check-conversion.py`): por página indexable asegura tel:/wa.me con el número correcto, CTA antes del fold y formulario en las páginas clave. **revisor-secretos** es DETERMINISTA (`bash .pipeline/check-secretos.sh`): busca claves/tokens en el working tree y en `git log -p` y que ningún archivo de secreto esté trackeado; su EXIT CODE es candado de publicación (FASE 5). **revisor-perf-real** (`node .pipeline/check-perf.mjs`) MIDE Core Web Vitals (mediana de 3) contra presupuesto (LCP<2.5s/CLS<0.1/INP<200ms) + regresión vs baseline, reusando los reportes Lighthouse de site-monitor.yml o midiendo con puppeteer. **revisor-tracking** (`node .pipeline/check-tracking.mjs`, puppeteer) carga páginas clave, simula la primera interacción (el sitio difiere GTM para el LCP) y confirma dataLayer + contenedor GTM + request a GA. Los 5 primeros (seo, movil, a11y, perf, links) son LLM y cubren lo SUBJETIVO (calidad de copy, intención de búsqueda, similitud de doorways, contraste). revisor-plantilla es DETERMINISTA (corre `python3 .pipeline/check-plantilla.py`) y garantiza las reglas MECÁNICAS de REGLAS.md (enlaces/og:image inexistentes, popup sin ARIA, fetchpriority/CLS, paridad CSS, table-wrapper, theme-color) — para que no dependan de que el LLM "recuerde leer REGLAS.md".
   **Verificación ciega (obligatorio):** los revisores DETERMINISTAS (revisor-infra-salud, revisor-indexabilidad, revisor-produccion, revisor-plantilla, revisor-gsc, revisor-secretos, revisor-conversion) NUNCA pueden "pasar callando". Si la herramienta de uno falla, no imprime JSON parseable, sale con error, o devuelve un vacío ANÓMALO por no poder acceder a sus datos (recorrió 0 páginas/0 URLs, o auth/cuota caída en GSC), ese revisor debe emitir un hallazgo de severidad **ALTA** `"verificación ciega: <tool> no devolvió datos (<motivo>)"` — NO un resultado vacío que parezca sano. (Una corrida exitosa con 0 hallazgos sobre datos reales sí es sana; lo prohibido es confundir "no pude mirar" con "está limpio". Evita repetir gsc-215, que dejó la indexación ciega varios días.)
5. Junta todos sus hallazgos JSON en una sola lista.

## FASE 2 — Deduplicar contra memoria
6. Para cada hallazgo, genera una FIRMA CANÓNICA ESTABLE = `archivo` + `categoria` + CLAVE DE REGLA (el tipo de defecto, NO la descripción en texto libre, que es frágil porque incluye rutas/conteos variables). Para hallazgos de los checkers deterministas, la clave es la regla de la que provienen (p.ej. "links-rotos", "og-image-inexistente", "breadcrumb-3-niveles", "exit-popup-aria", "paridad-css", "theme-color"); para hallazgos de revisores LLM, el invariante del problema (categoria + patrón estable del defecto), no la frase exacta. Búscala en HISTORIAL.jsonl:
   - Si NUNCA se vio: es nuevo.
   - Si ya se vio y se marcó arreglado pero reaparece: márcalo como REGRESIÓN (prioridad alta) — significa que falta una regla.
   - Si ya se vio y sigue pendiente: no lo repitas, solo cuéntalo.
7. Añade los hallazgos nuevos y regresiones a HISTORIAL.jsonl (una línea JSON por hallazgo, con fecha de hoy).

## FASE 3 — Arreglar (solo severidad alta y media)
8. Arregla SOLO hallazgos mecánicos de severidad alta y media, UNO POR UNO, con cambios MÍNIMOS, respetando TODAS las reglas de REGLAS.md (ej: versionar CSS + subir SW, aplicar fix en los 3 archivos CSS, etc.). No arregles severidad baja en modo automático.
9. NUNCA hagas en automático: consolidar/fusionar/borrar/reescribir páginas; cambios de contenido, copy o precios; decisiones de estrategia SEO; borrar o editar tests; cualquier cambio que borre más de 5 archivos completos. Anótalo como pendiente humano.

## FASE 4 — Verificar (escéptico, con el sitio corriendo)
10. Por cada arreglo, vuelve a comprobar en el sitio corriendo que el problema YA NO está. Asume que NO se arregló salvo prueba clara. Si sigue roto, vuelve a intentar (máximo 2 veces) y si no, revierte ese arreglo y márcalo como pendiente.

## FASE 5 — Gate de publicación
11. Auto-revisa el diff contra main: confirma que nada quedó fuera de alcance, que HTML/JSON-LD siguen válidos, y que no se tocaron tests ni contenido estratégico.
12. Solo publica si se cumplen TODOS los candados: auto-revisión limpia, diff de máximo 15 archivos (una corrida normal toca 1–5; en un sitio de ~100 páginas, >15 archivos es señal de que algo se salió de alcance y debe revisarlo un humano antes de publicar), cero borrados estructurales inesperados y **candado de secretos**: `bash .pipeline/check-secretos.sh` termina con exit 0 (exit 2 = secreto en working tree o archivo de secreto trackeado → NO publicar; exit 1 = verificación ciega → tampoco). Si cualquier candado falla, NO hagas merge ni push; deja la rama, escribe en ESTADO.md por qué se detuvo y termina.
13. Si todo pasa, PUBLICA sincronizando ANTES con el remoto. `git push --force` (o `-f`) está PROHIBIDO en cualquier circunstancia. Sigue exactamente este orden:
    a. `git checkout main`.
    b. SINCRONIZA con el remoto antes de mergear: `git fetch origin` y luego `git merge --ff-only origin/main`. Esto adelanta la main local al remoto (que otro escritor pudo haber movido). Si el `--ff-only` FALLA (la main local divergió del remoto), NO fuerces ni hagas un merge normal: ABORTA la publicación, deja la rama de la corrida sin fusionar, escribe el motivo en ESTADO.md ("publicación detenida: main local divergió de origin/main") y termina.
    c. Mergea la rama de la corrida: `git merge --no-ff <rama> -m "fix: mantenimiento auto YYYY-MM-DD — N hallazgos"`.
    d. `git push` (dispara la indexación en Google, deja que corra).
    e. SI el push es RECHAZADO (non-fast-forward u otro error): NO uses `--force`. Reintegra y reintenta UNA sola vez: `git fetch origin && git rebase origin/main && git push`. Si ese segundo push también falla: ABORTA, deja la rama, escribe el motivo en ESTADO.md ("publicación detenida: push rechazado tras reintento") y termina sin publicar.
    f. SOLO si el push tuvo éxito: borra la rama fusionada.

## FASE 6 — Aprender
14. Si algún error fue una REGRESIÓN o reveló un patrón nuevo, añade/actualiza una regla en REGLAS.md (formato: "- [FECHA] CATEGORÍA: regla — por qué. Severidad: X"). CONSOLIDA, no dupliques. Solo crea regla de un error ya verificado.
15. Actualiza ESTADO.md con: fecha de esta corrida, qué se arregló, qué quedó pendiente y si se publicó o no.

## FASE 7 — Reporte
16. Apaga el servidor local y escribe .pipeline/ultima-corrida.md. Muéstrame un resumen: hallazgos encontrados / arreglados / pendientes / regresiones / reglas nuevas / publicado o detenido.
