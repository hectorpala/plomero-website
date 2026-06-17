# PENDIENTE — Consolidar canibalización de precios (301)

**Decisión (2026-06-14):** URL canónica de precios = **`/precios/`** (la más fuerte: en el
nav, 29 enlaces internos, 3 tablas de precios, schema FAQ/Service/Offer, title con "2026").
La débil `/servicios/plomero-precios/` (0 tablas, sin schema) se consolida hacia ella.

## ⚠️ NO activar todavía
Activar SOLO cuando `/precios/` esté **indexada y rankeando** en Google
(verificar con `gsc_inspect` → estado "Enviada e indexada"). Hoy `/precios/` está
"Descubierta, sin indexar, nunca rastreada"; redirigir tráfico vivo a una página aún no
indexada abriría un hueco. Orden correcto:

1. Push de indexación de `/precios/` (Indexing API) — NO empujar `/servicios/plomero-precios/`.
2. Confirmar `/precios/` indexada con `gsc_inspect`.
3. **Recién entonces** activar el 301 de abajo + sacar `/servicios/plomero-precios/` del sitemap.

## Regla a añadir al final de `_redirects` (paso 3)
```
# 301: consolidar precios en la canónica /precios/ (decisión 2026-06-14)
/servicios/plomero-precios   /precios/ 301
/servicios/plomero-precios/  /precios/ 301
```

## Además en el paso 3
- Quitar la entrada `/servicios/plomero-precios/` de `sitemaps/main_sitemap.xml`.
- (Opcional) cambiar el canonical de `servicios/plomero-precios/index.html` a
  `https://plomeroculiacanpro.mx/precios/` por si el 301 tarda en propagar.
