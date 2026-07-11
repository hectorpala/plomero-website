# Oportunidades GSC — 2026-07-10

Fuente: `mcp__local-seo__find_opportunities` / `search_keywords` (Search Console API real, 28 días: 2026-06-13 a 2026-07-11). No se pudo obtener el agregado de tendencia (clics/impresiones vs periodo anterior) porque `gsc_performance`/`gsc_list_sites` no estaban en el set de tools cargado por el subagente esa corrida; el desglose por keyword/página sí es dato real de GSC.

| # | Query | Impresiones | Posición | CTR | Página que ya cubre | Acción |
|---|-------|--------------|----------|-----|----------------------|--------|
| 1 | como destapar un baño muy tapado | 141 | 6.7 | 0% | blog/desatascar-wc-metodos-profesionales/ | **ctr-fix HECHO** (title/meta/JSON-LD espejan "muy tapado" + gancho local) |
| 2 | baños tapados | 56 | 7.2 | 0% | blog/desatascar-wc-metodos-profesionales/ | Observar (probable arrastre del fix #1) |
| 3 | lista de precios de plomería en méxico 2026 | 157 | 7.2 | 0.6% | /precios/ | Observar — intención NACIONAL, no local; tocar el snippet rozaría la regla dura de precios en meta |
| 4 | plomero / plomero cerca de mi (home vs servicios/plomero-cerca-de-mi/) | 158+27 / 80+18 | 10.4/6.3 vs 12.7/7.4 | — | ambas | Observar — posible canibalización, requiere decisión de arquitectura (redirects/consolidación), no es ctr-fix de hoy |
| — | cluster "baja presión de agua" (~50 variantes long-tail) | vario | 5-10 | ~0% | blog/baja-presion-agua-causas-soluciones/ | Ya cubierto, sin acción |
| — | cluster "tinaco" (costo/instalación) | vario | 1-10 | vario | servicios/instalacion-de-tinaco/ | Ya bien posicionado, sin acción |

**Páginas nuevas: 0.** Ninguna query con demanda real cae fuera del catálogo existente (servicios/ + blog/); toda la demanda mapea a páginas ya creadas. Total quick-wins detectados (pos 5-20, 10+ impr): 30 keywords, todas en páginas existentes — 12 con CTR 0% en top-10.

Decisión tomada por el panel `decisor-negocio` (dev senior + experto del mercado de Culiacán): priorizar #1 por mejor ratio impacto/esfuerzo/riesgo; #2-#4 quedan en observación explícita para la próxima corrida.
