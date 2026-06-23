# Oportunidades GSC — 2026-06-22 (corrida auto-diario)

GSC MCP vivo (gsc_list_sites OK). Rendimiento 28d: **361 clics (+19%) · 28,332 impr (+27%) · pos 6.8**. Sitio en crecimiento sano.

## Decisión de crecimiento: 0 páginas nuevas (sin hueco de demanda sin canibalizar)
Todos los clusters con demanda real YA tienen página dedicada. No hay query de plomería con demanda que carezca de página → no se inventan doorways.

| Cluster (query top) | Impr | Pos | CTR | Página que rankea | Disposición |
|---|---|---|---|---|---|
| drenaje tapado (+variantes) | 151+110+90 | 6-8 | 0% | /blog/drenaje-tapado-senales-prevencion/ | ranking/SERP-features (gsc-212/214), no snippet — no churn |
| como destapar un baño/inodoro | 203+79+37 | 3-7 | ~0% | /blog/desatascar-wc-metodos-profesionales/ | tiene blog + servicio dedicado; ranking, no snippet |
| baja presión de agua | 31+19 | 8.8 | 0% | /blog/baja-presion-agua-causas-soluciones/ | tiene blog + servicio dedicado |
| **bombas de agua en culiacan** | 28 | 4.7 | 0% | /servicios/correccion-baja-presion/ (VIEJA) | **ENLAZADO** → ver abajo |
| plomero culiacan / plomero | 130+134 | 5-9.7 | bajo | / (home) | head terms, autoridad (gsc-209) |

## Optimización ejecutada: enlazado interno a la página nueva de bombas
- **Problema:** `/servicios/reparacion-de-bombas-de-agua/` (creada 2026-06-21) está "Google no reconoce esta URL — nunca rastreada"; solo 1 enlace entrante (home). La demanda real de "bombas de agua en culiacan" (pos 4.7) la sigue capturando la página VIEJA `correccion-baja-presion` (mismatch de intención gsc-207/211).
- **Acción:** enlace contextual desde `correccion-baja-presion` (38 menciones de "bomba", autoridad temática) → página dedicada de bombas, con anchor "reparación de bombas de agua" ruteando la intención de *reparar/instalar bomba*. La página nueva pasa de 1 → 2 enlaces entrantes. Indexación solicitada por MCP tras publicar.

## Diferido (no hoy, por candado de 18 páginas)
- bk-64bed7fd (a11y): `aria-hidden` en `<header class=article-header>` de 8 blogs oculta la fecha al lector de pantalla. Confirmado de nuevo hoy por el lote rotativo (problemas-comunes). 8 páginas → con las 15 del breadcrumb excede el candado; corrida dedicada.
- bk-6a3a1bcc (imagen): foto real para destape-de-bano-inodoro (hoy muestra tinaco).
