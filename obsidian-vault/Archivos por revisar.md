# Archivos por revisar

Lista inicial basada en [[Graphify]] y en el [[Grafo de invocacion real]].

## Estado de la evidencia

- Reporte Graphify: `~/graphify-plomero/graphify-out/GRAPH_REPORT.md`
- Grafo visual: `~/graphify-plomero/graphify-out/graph.html`
- Grafo real: `~/graphify-plomero/graphify-out/invocacion-real.json`
- Commit del grafo: `a56c0e4f`
- HEAD actual revisado: `65b6441`

Conclusion: esta lista es **evidencia inicial**, no orden de borrar. Antes de eliminar algo hay que confirmar referencias y proposito.

## Regla de decision

- **No tocar**: aparece conectado al pipeline, a gates, a deploy, a cache o a GSC.
- **Revisar**: grado 0 en grafo real o no aparece invocado, pero podria ser herramienta manual.
- **Posible limpieza**: reportes viejos, scripts duplicados o herramientas reemplazadas.
- **Borrar solo con prueba**: despues de confirmar sin referencias, sin uso manual y con commit separado.

## Candidatos inmediatos

### `scripts/add_breadcrumbs.py`

Estado: revisar.

Evidencia:
- Aparece con grado 0 en `invocacion-real.json`.
- `rg` no encontro llamadas directas a `add_breadcrumbs.py`.
- Existe otro script parecido: `scripts/add_visual_breadcrumbs.py`.

Riesgo:
- Puede ser script manual antiguo para colonias. No borrar sin comparar contra [[Schemas]] y [[SEO]].

Siguiente accion:
- Comparar con `scripts/add_visual_breadcrumbs.py`.
- Confirmar si ya no se usa para breadcrumbs JSON-LD.

Relacionado:
- [[SEO]]
- [[Schemas]]
- [[Scripts delicados]]

### `reivision de sitio/check.sh`

Estado: revisar.

Evidencia:
- Parece herramienta manual de Lighthouse.
- Guarda reportes en `reivision de sitio/logs/`.
- No aparece en el grafo real como parte del pipeline principal.

Riesgo:
- Puede ser reporte historico/manual, no necesariamente basura.

Siguiente accion:
- Decidir si se conserva como herramienta manual, se mueve a docs, o se reemplaza por checkers actuales de `.pipeline`.

Relacionado:
- [[Pipeline de publicacion]]
- [[check-infra.mjs]]
- [[Manual operativo]]

## Grado 0 en grafo real - revisar por grupos

### Checkers o pipeline

- `.pipeline/check-contenido.py`
- `.pipeline/check-linking.py`
- `.pipeline/check-nap.py`
- `.pipeline/check-pagina-nueva.py`
- `.pipeline/gestor-backlog.py`
- `.pipeline/hooks/install.sh`
- `.pipeline/meta-semanal.sh`
- `.pipeline/recolecta-señales.py`
- `.pipeline/selector-revisores.py`

Nota: grado 0 no significa inutil. Algunos pueden ser llamados por humanos, por Claude, por launchd o por convenciones que Graphify no ve.

### Scripts de mantenimiento

- `scripts/actualizar-colonias-botones.py`
- `scripts/actualizar-colonias-favicon.py`
- `scripts/actualizar-cta-floating.py`
- `scripts/add_complete_schemas_colonias.py`
- `scripts/add_internal_links.py`
- `scripts/add_local_business_schema.py`
- `scripts/add_localbusiness_schemas_all_colonias.py`
- `scripts/add_review_schemas.py`
- `scripts/add_visual_breadcrumbs.py`
- `scripts/agregar-badge-rating-colonias.py`
- `scripts/agregar-rating-colonias.py`
- `scripts/estandarizar-favicons-colonias.py`
- `scripts/fix-badge-colonias-antiguas.py`
- `scripts/fix-favicons-colonias-antiguas.py`
- `scripts/fix-rating-colonias-antiguas.py`
- `scripts/fix-remaining-colonias.py`
- `scripts/generar_colonias.py`
- `scripts/generar-colonias.py`
- `scripts/generate-sitemap.py`
- `scripts/inject_zona_content.py`
- `scripts/update_sitemap_breadcrumbs.py`
- `scripts/update_sitemap_colonias_fixed.py`
- `scripts/update_sitemap_colonias.py`
- `scripts/update_sitemap_internal_links.py`
- `scripts/update_sitemap_servicios.py`

Patron probable:
- Muchos parecen scripts de migracion o reparacion masiva.
- Conviene clasificarlos como `activo`, `manual`, `historico` o `reemplazado`.

## No tocar sin pruebas

- [[ci-gate.py]]
- [[gate-pagina.py]]
- [[check-infra.mjs]]
- [[scripts crecer.py]]
- [[sw.js]]
- `.pipeline/check-plantilla.py`
- `.pipeline/check-indexabilidad.py`
- `.pipeline/check-produccion.mjs`
- `.pipeline/check-contrato-checkers.mjs`

## Siguiente paso

1. Actualizar Graphify contra HEAD actual.
2. Para cada candidato, correr `rg` por basename y funcion principal.
3. Mover cada archivo a una categoria:
   - conservar
   - documentar como manual
   - deprecado
   - candidato a borrar
4. Registrar decisiones en [[Bitacora]] y errores en [[Errores y soluciones]].

#graphify #limpieza #archivos
