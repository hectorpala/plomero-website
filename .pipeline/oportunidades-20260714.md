# Oportunidades GSC — 2026-07-14

Rendimiento 28d: 463 clics (+19%), 46,565 impresiones (+63%), posición 6.4.

## Striking distance / zero-click revisadas
Todas las queries de `gsc_opportunities` (striking_distance, pagina_2, zero_clicks_top10)
mapean a páginas YA EXISTENTES. Ninguna representa un hueco de demanda sin página propia.

- **"como destapar un baño muy tapado"** (218 impr, pos 6.6, 0 clics) → `/blog/desatascar-wc-metodos-profesionales/`.
  Ya tiene title/meta con match exacto fuerte (bk-6fd0a475, ctr-fix hecho en corrida previa).
  Decisión (reconfirmada, ya tomada 2026-06-26 y 2026-07-07): 0-clic es por SERP-features/PAA,
  no snippet débil — reescribir sería cambio-por-cambio. NO se toca de nuevo hoy.
- **"bombas de agua en culiacan"** (32 impr, pos 3.3, 0 clics) → `/servicios/correccion-baja-presion/`.
  Coincide con el mismatch de tema ya detectado por el revisor SEO del lote rotativo de hoy
  (seo-title-tema-desalineado-correccion-baja-presion-20260714): el `<title>` decía "Bombas de
  Agua" pese a que el H1/canonical es "Corrección de Baja Presión" — canibalizaba con
  `/servicios/reparacion-de-bombas-de-agua/`. Ya corregido hoy en FASE 5 (alineado al tema real).
- **"lista de precios de plomería en méxico[ 2026]"** (191+171 impr, pos 7.3, /precios/) →
  query de alcance NACIONAL contra una página explícitamente de Culiacán. El bajo CTR puede ser
  auto-filtrado sano (usuarios fuera de Culiacán descartan el resultado al ver "Culiacán" en el
  snippet) — no es necesariamente un defecto. Tocar el title implicaría alcance nacional que el
  negocio no ofrece (NEGOCIO.md: giro es Culiacán, Sinaloa). NO se toca — riesgo de sobre-prometer
  cobertura geográfica que no existe.
- **"plomero" / "plomero culiacán"** (head terms, pos 9.5/5) → ya conocidos (gsc-209), requieren
  autoridad/enlazado interno de fondo, no un cambio puntual de copy.

## Páginas nuevas
0 páginas nuevas hoy. Ninguna query de GSC representa un servicio de plomería sin página propia
(todas las de la lista de arriba ya tienen página dedicada). Backlog auto-ejecutable (`gestor-backlog.py
next --riesgo-max medio`) vacío.

## Colonias
Las 24 colonias existentes ya están todas indexables (0 noindex). Sin promoción pendiente.
