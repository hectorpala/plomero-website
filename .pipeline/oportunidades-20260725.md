# Oportunidades GSC — 2026-07-25

Rendimiento 28 días: 579 clics (+45%), 57,301 impresiones (+67%), posición media 6.3.

## Resultado: 0 páginas nuevas, 0 ctr-fix nuevos

Backlog auto-ejecutable (`gestor-backlog.py stats`): **0 auto-ejecutables** (14 tareas totales,
11 hechas, 1 requiere_humano, 1 descartada, 1 pendiente de riesgo alto). `check-plantilla.py`:
**0 hallazgos** — el mismatch FAQPage-vs-visible (backlog desde 2026-07-21) quedó en 0 páginas
tras el trabajo de las corridas 07-23/07-24.

Todas las oportunidades de `gsc_opportunities` (striking distance, página 2, zero-clicks-top10)
mapean a páginas YA EXISTENTES, mismo panorama que los días previos:

| Keyword | Pos | Impr | Página |
|---|---|---|---|
| como destapar un baño muy tapado | 6.6 | 399 | /blog/desatascar-wc-metodos-profesionales/ |
| lista de precios de plomería en méxico (2026) | 7.4-7.5 | 496 | /precios/ |
| porque no sale/baja agua tinaco lleno (variantes) | 5.3-7.5 | ~470 | /blog/baja-presion-agua-causas-soluciones/ |
| plomero / plomero culiacan | 4.2-10.5 | 276 | / |
| drenaje tapado (variantes) | 5.5-6.7 | 246 | /blog/drenaje-tapado-senales-prevencion/ |
| gas a domicilio culiacán 24 horas | 10.4 | 80 | /servicios/tecnico-de-gas-culiacan/ |
| bombas de agua en culiacan | 3.6 | 35 | /servicios/correccion-baja-presion/ |
| cuanto cuesta instalar un tinaco | 7.9 | 34 | /servicios/instalacion-de-tinaco/ |
| plomero(s) culiacan (zona poniente) | 9.6-10.3 | 105 | /servicios/plomero-zona-poniente-culiacan/ |

Candidatos de CTR-fix ya analizados en corridas previas, decisión vigente de NO re-tocar:
- `desatascar-wc-metodos-profesionales`: SERP-features reconfirmado (06-26/07-08/07-14).
- `bombas de agua en culiacan` / correccion-baja-presion: decisor-negocio cerró este análisis
  2026-07-13 (se venía re-escalando cada corrida sin necesidad real).

## Foco real del día: retomar y verificar la rama huérfana de 2 días

La rama `auto/diario-20260723-0903` traía 85 archivos ya trabajados (FASE 3-6 del 07-23,
interrumpida antes de FASE 7-10) y dos intentos de respaldo (Codex, 07-23/07-24) que no pudieron
avanzarla por bloqueos de SU sandbox (ninguno reproducible en este entorno). Hoy: confirmado que
los bloqueos de Codex no aplican aquí; FASE 7 (verificador) encontró y se corrigió UNA regresión
real (contraste ilegible en el footer de 2 páginas al convertir `<h4>`→`<h3>` para el fix de
jerarquía de encabezados); 2ª pasada del verificador dio ok=true. Publicado hoy.
