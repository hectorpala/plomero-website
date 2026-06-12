# Última corrida — 2026-06-12 noche (AUTÓNOMA)

**Rama:** auto/mantenimiento-20260612-noche → merge 6688d219 a main → push OK → rama borrada.
**Publicado: SÍ.** Candados 3/3: auto-revisión limpia, 106 archivos ≤ 200, 0 borrados.

## Qué se arregló (8 hallazgos mecánicos, todos verificados con el sitio corriendo)

| ID | Qué | Verificación |
|----|-----|--------------|
| seo-201 (=links-202) | JSON-LD de plomero-economico con URLs sin `/servicios/` (404) | grep 0 malas, JSON-LD 4/4 válido, curl 200 |
| seo-202 (=links-201) | og:url + breadcrumb de desazolve sin `/servicios/` (404) | 3/3 URLs correctas servidas |
| perf-201 | hero de tecnico-de-gas declaraba 1200x800, imagen real 800x800 (CLS) | sips + HTML servido |
| perf-202/203/204 | 2-3 `fetchpriority=high` por página en 3 servicios; bajo-el-fold a `loading=lazy` | conteo de high servido = preloads+hero exacto |
| perf-205 | preload de emergencia-24-7 sin imagesrcset (doble descarga en desktop) | atributo servido |
| movil-201 | CTAs de texto tel:/wa.me con tap target 17-27px | regla en los 3 CSS (paridad 1/1/1), Chrome headless: 44-52px a 375px, 0 overflow en 10 páginas, .hero-phone-link sigue oculto en desktop, botones excluidos |

Bump CSS `?v=20260612c` (102 páginas) + sw.js CACHE_NAME v24 (regla de caché cumplida).

## Qué quedó pendiente para humano (nuevos)

1. **gsc-201 (ALTA):** /precios/ jamás indexada — canibalizada por /servicios/plomero-precios/ (sí indexada, title casi igual). Decidir consolidación (301 o canonical).
2. **gsc-202 (ALTA):** hub /servicios/ "Google no reconoce esta URL" — solo 2 enlaces internos; la home usa el ancla #servicios. Añadir enlace real en nav/footer.
3. **gsc-203 (1 minuto):** reenviar sitemap.xml y sitemaps/main_sitemap.xml en GSC (copia de Google del 06-03/06-04, anterior a la consolidación).
4. **gsc-204:** titles/metas con CTR 0 pese a ~430 impresiones (drenaje-tapado) y pos 1.9 (desatascar-wc) — copy.
5. **a11y-201:** verde "Disponibles ahora" 2.0:1; recomendado #15803d (~4.7:1) en inline de index.html + 3 CSS.

Bajas registradas sin tocar: seo-203/204 (og:url a la home), seo-205 (typo año, página noindex), movil-202 (link Términos 65x19), perf-206 (dims de logo).

## Notas

- 0 regresiones de la corrida de la tarde (los 6 revisores verificaron los fixes previos).
- El hook de indexación del push agotó la cuota diaria (consumida por la corrida de la tarde): 2 enviadas, 98 con error de cuota. Se renueva mañana; no afecta el deploy.
- Aprendizaje clave: una regla CSS añadida al final casi anula el `display:none` de `.hero-phone-link` en desktop (misma especificidad, orden gana). Cazado antes de publicar; regla nueva CSS/CASCADA en REGLAS.md.
- GSC rendimiento 28d: 336 clics (+26%), 23,801 impresiones (+23%) — al alza, sin caídas.
