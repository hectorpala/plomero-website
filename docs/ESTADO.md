## 2026-09-03 — Auditoría externa: 3 ALTAS cerradas y pipeline desbloqueado

Sesión de revisión pedida por Héctor (4 revisores + los checkers del pipeline). Publicado en
main `d261dbad`, deploy Netlify `6a9a0f18`, guardia-deploy limpio.

- **A1 (alta)** El commit `a5198bbd` (19-dic-2025) había borrado el CSS de validación del
  formulario; en producción se veían los 8 mensajes a la vez en home, emergencia-24-7 y
  plomero-colonias. Restaurado con paleta de marca (#C2410C / #075E54). Verificado headless.
- **A2 (alta)** 11 días sin publicar (16 commits) por 3 bloqueos falsos. Arreglados: piso de
  ruido por red en check-perf, baseline re-medida contra prod, el verificador ya solo bloquea
  por ALTA / regresión / verificación ciega, y PUPPETEER_EXECUTABLE_PATH en el driver.
- **A3 (alta)** 277 archivos internos se servían en el dominio. 14 reglas 404! + .bak fuera del repo.
- **M1** WhatsApp post-envío ya no lo bloquea el navegador (pestaña abierta antes del await).
- **M5/M6** og:url roto del post de la marcha y 61 tel: sin +52.
- Hook pre-push reinstalado desde .pipeline/hooks/ (el vivo estaba desfasado).

PENDIENTE HUMANO: rotar el client secret OAuth del proyecto odsappi (commit `3edd5afe`).
Deuda conocida que NO bloquea: 56 páginas con precios visibles, ESTADO.md sobre presupuesto
de contexto, sitemaps con lastmod contradictorio, JSON-LD de /contacto/ sin address.

# ESTADO del pipeline de agentes

## 2026-09-03 — auto/diario-20260903-1826 — PUBLICADA

- Health local: `/`, `/contacto/`, `/servicios/` y `/blog/` respondieron 200. Piso determinista: infra, plantilla, indexabilidad, NAP (73), conversión (68), enlazado (68), E2E (3), rendimiento (2) y producción limpios; tracking midió 5 páginas y mantuvo 4 medias preexistentes por beacon ausente sin consentimiento. Secretos: árbol actual publicable; dos credenciales históricas siguen pendientes de rotación.
- Lote rotativo: corrección de baja presión, detección de fugas, plomería comercial, zona centro y reparación de bombas. Se retiraron cifras visibles no respaldadas de las primeras cuatro; `check-contenido.py` bajó la deuda site-wide de 56 a 52 páginas. Cuatro gates OK (Jaccard 0.25–0.31) y Chrome local confirmó 4/4 HTTP 200, JSON-LD válido, canonical/og/twitter iguales, cero enlaces rotos, overflow o errores JS.
- GSC vivo: 518 clics, 54,791 impresiones, CTR 0.95%, posición 6.7; sitemaps con 0 errores/advertencias. Toda oportunidad con demanda ya tiene destino; backlog `[]` dos veces y 0 páginas nuevas. Reporte `.pipeline/oportunidades-20260903.md`.
- Verificador solo-lectura: `ok=true`, 0 problemas de la corrida; diff de 4 HTML + 1 reporte, 0 tests y 0 borrados. Publicado por `scripts/crecer.py publicar`: merge `aa408b47`, push seguro a `origin/main`, 4 URL enviadas a GSC. Producción devolvió HTTP/2 200 en las cuatro.

## 2026-09-02 — auto/diario-20260818-1825 retomada — NO PUBLICADA

- Health local: `/`, `/contacto/`, `/servicios/` y `/blog/` respondieron 200. Piso: infra, plantilla, indexabilidad, NAP (73), conversión (68), enlazado (68), E2E (3) y producción limpios; secretos actuales publicables, con dos credenciales históricas pendientes de rotación.
- Seis artículos heredados pasan `gate-pagina.py` (Jaccard máximo 0.27), responden 200, parsean JSON-LD y mantienen canonical/og:url/twitter:url iguales. Lote rotativo de cinco colonias: gates OK, Jaccard máximo 0.68. `ci-gate.py` terminó con 0 ALTA; 0 tests, 0 borrados y 6 HTML modificados.
- `check-contenido.py` mantiene la deuda conocida de precios visibles en 56/73 páginas. GSC vivo: 527 clics, 54,987 impresiones, CTR 0.96%, posición 6.7; sitemaps con 0 errores/advertencias. Toda demanda fuerte tiene destino; backlog `[]` dos veces y 0 páginas nuevas. Reporte `.pipeline/oportunidades-20260902.md` (`6829d68a`).
- Verificador solo-lectura: `ok=false`. Tracking no imprimió JSON ni código de salida; rendimiento midió home LCP 1,024 ms vs baseline 180 ms e INP 152 ms vs 72 ms. No se ejecutó merge, push ni indexación.

## 2026-09-01 — auto/diario-20260818-1825 retomada — NO PUBLICADA

- Health local: `/`, `/contacto/`, `/servicios/` y `/blog/` respondieron 200. Piso local: plantilla, indexabilidad, NAP (73), conversión (68), enlazado (68), E2E (3) y producción limpios; secretos actuales publicables, con dos credenciales históricas pendientes de rotación.
- Seis artículos heredados pasan `gate-pagina.py` (Jaccard máximo 0.27), responden 200, parsean JSON-LD y mantienen canonical/og:url/twitter:url iguales. `ci-gate.py` terminó con 0 ALTA; 0 tests y 0 borrados.
- Contenido mantiene la deuda conocida de precios visibles en 56 páginas. GSC vivo: 531 clics, 55,464 impresiones, CTR 0.96%, posición 6.7; sitemaps con 0 errores/advertencias. No hay hueco sin destino ni backlog autoejecutable; 0 páginas nuevas. Reporte `.pipeline/oportunidades-20260901.md` (`3aecf5e6`).
- Verificador solo-lectura: `ok=false`. Tracking terminó sin JSON aun fuera del sandbox; rendimiento midió home LCP 1,120 ms vs 180 ms e INP 176 ms vs 72 ms, y reparación de fugas INP 168 ms vs 56 ms. No se ejecutó merge, push ni indexación.

## 2026-08-31 — auto/diario-20260818-1825 retomada — NO PUBLICADA

- Health local: `/`, `/contacto/`, `/servicios/` y `/blog/` respondieron 200. Piso local limpio: infra, plantilla, indexabilidad, NAP (73), conversión (68), enlazado (68), E2E (3) y producción; secretos actuales publicables, con dos credenciales históricas pendientes de rotación.
- Contenido: seis artículos heredados pasan `gate-pagina.py` (Jaccard máximo 0.27) y `ci-gate.py` terminó con 0 ALTA. `check-contenido.py` mantiene la deuda conocida de precios visibles en 56 páginas.
- GSC vivo: 548 clics, 55,931 impresiones, CTR 0.98%, posición 6.6; sitemaps con 0 errores/advertencias. Toda demanda fuerte tiene destino; backlog `[]` dos veces, 0 páginas nuevas. Reporte `.pipeline/oportunidades-20260831.md` (`934a8b50`).
- Verificador solo-lectura: `ok=false`. Rendimiento midió home LCP 1,048 ms vs 180 ms e INP aproximado 224 ms; reparación de fugas INP 168 ms vs 56 ms. Tracking cargó GTM/GA4 pero no observó beacon en 4 páginas sin consentimiento. No se ejecutó merge, push ni indexación.

## 2026-08-30 — auto/diario-20260818-1825 retomada — NO PUBLICADA

- Health local: `/`, `/contacto/`, `/servicios/` y `/blog/` respondieron 200; las seis páginas heredadas respondieron 200, parsearon JSON-LD y mantuvieron canonical/og:url/twitter:url iguales.
- Piso: infra, plantilla, indexabilidad, NAP (73), conversión (68), enlazado (68), E2E (3) y producción sin hallazgos; `ci-gate.py` 0 ALTA y seis `gate-pagina.py` OK. Secretos: árbol actual publicable, dos credenciales históricas pendientes de rotación.
- Hallazgos vinculantes: `check-contenido.py` mantiene 56 páginas con precios visibles; rendimiento midió LCP home 516 ms vs baseline 180 ms; tracking analizó 5 páginas y en 4 cargó GTM/GA4 sin observar beacon tras interacción sin consentimiento.
- GSC vivo: 555 clics, 56,476 impresiones, CTR 0.98%, posición 6.6; sitemaps 0 errores/advertencias. Toda demanda fuerte ya tiene destino; backlog `[]` dos veces, 0 páginas nuevas. Reporte `.pipeline/oportunidades-20260830.md` (`558fcec2`).
- Verificador solo-lectura: `ok=false`. No se ejecutó merge, push ni indexación.

## 2026-08-26 — auto/diario-20260818-1825 retomada — NO PUBLICADA

- Health local: `/`, `/contacto/`, `/servicios/` y `/blog/` respondieron 200. Piso válido: infra, plantilla, indexabilidad, NAP 73, conversión 68, enlazado 68, E2E 3, rendimiento 2 y producción sin hallazgos; secretos exit 0 con dos credenciales históricas pendientes.
- Arreglos: cinco artículos quedaron sin tarifas/porcentajes comerciales ni testimonios no verificables (`7ea38947`); el artículo de WC se alineó a más de 1,100 impresiones GSC agregadas y quedó sin cifras no respaldadas (`fa182f7e`). Seis gates OK; headless 375px con HTTP 200, JSON-LD válido, 0 overflow y 0 errores JS.
- GSC: 582 clics, 57,206 impresiones, CTR 1.02%, posición 6.6; sitemaps 0 errores/advertencias. Cero páginas nuevas: toda demanda fuerte tiene destino; backlog autoejecutable `[]` dos veces. Reporte `.pipeline/oportunidades-20260826.md`.
- Aprendizaje: `check-contenido.py` ahora detecta precios visibles en páginas indexables y reveló deuda heredada en 56/73 páginas (`16ee2c50`). `check-reglas.py` pasó con 54 reglas y ~3,981 tokens.
- Verificador solo-lectura: `ok=false`. `ci-gate.py` y seis gates pasaron, pero tracking terminó otra vez sin JSON y quedan 56 páginas con precios visibles. No se ejecutó merge, push ni indexación.

## 2026-08-25 — auto/diario-20260818-1825 retomada — NO PUBLICADA

- Health local: `/`, `/contacto/`, `/servicios/` y `/blog/` respondieron 200. Se retomó la rama del 18 de agosto; no se abrió otra.
- Piso con datos reales: plantilla e indexabilidad limpias; NAP 73, conversión 68, enlazado 68, E2E 3, rendimiento 2 y producción sin hallazgos. `ci-gate.py`: 0 ALTA. Secretos: árbol actual publicable (`exit 0`), pero dos credenciales antiguas siguen pendientes de rotación.
- Tracking bloqueó de nuevo: Chrome revisó 5 páginas; las 5 solicitaron `gtm.js`, pero `window.google_tag_manager` no se inicializó. Veredicto final: `ok=false`; ante este candado no se ejecutó merge ni push.
- GSC vivo: 583 clics, 57,477 impresiones, CTR 1.01%, posición 6.6; sitemaps con 0 errores/advertencias. Toda demanda fuerte ya tiene página propia; backlog autoejecutable `[]` dos veces y 0 páginas nuevas. Reporte: `.pipeline/oportunidades-20260825.md`.

---

## Histórico

Las corridas anteriores al 2026-08-28 están en [`docs/archivo/ESTADO-historico.md`](archivo/ESTADO-historico.md). Se archivaron el 2026-09-04 porque este archivo se relee en cada llamada del agente y pesaba 5× su presupuesto de contexto. El detalle de cada incidente sigue en `data/HISTORIAL.jsonl`.
