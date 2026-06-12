# Plomero Culiacán — Instrucciones del proyecto

## Memoria (LEER SIEMPRE antes de trabajar)
- ANTES de hacer cualquier cambio, lee REGLAS.md (errores ya cometidos que NO debes repetir).
- Registra hallazgos nuevos en HISTORIAL.jsonl (una línea JSON por hallazgo).
- El estado de la última corrida está en ESTADO.md.

## Reglas de trabajo (estilo Anthropic)
- VERIFICA tu trabajo antes de darlo por hecho: corre el sitio y compruébalo, no asumas que "se ve bien".
- HEALTH CHECK primero: antes de tocar nada, revisa que lo existente no esté roto.
- UNA mejora por sesión. No abarques de más.
- JAMÁS borres ni edites tests para "hacer pasar" algo. Eso oculta funcionalidad rota.
- Cambios mínimos. No refactorices fuera del alcance pedido.
- Muestra EVIDENCIA (salida de comando, captura) en vez de afirmar éxito.

## Reglas duras del sitio (resumen — el detalle está en REGLAS.md)
- CSS: al cambiar estilos, versionar URL (?v=AAAAMMDD) Y subir versión del service worker (sw.js). Aplicar el fix en los TRES archivos CSS (styles.css, styles.min.css y el .hash.css servido).
- MÓVIL: tablas con scroll horizontal; imágenes con max-width:100%; grids con auto-fit minmax, no columnas fijas; tap targets ~44px.
- SEO: nada de doorways (páginas casi idénticas); coordenadas GPS reales y únicas; sin aggregateRating self-serving en blog; og:image/twitter:image deben existir; al borrar páginas, cero enlaces rotos + actualizar sitemap.
- JS: tras minificar, verificar que las URLs wa.me no queden truncadas (rompe todo el sitio).
- CONTACTO: el email correcto es info@plomeroculiacanpro.mx

## Comandos útiles
- git log --oneline -30  (ver historia reciente)
- Servidor local para probar: (usar el que ya use el proyecto)
