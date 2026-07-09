# Manual operativo

Manual vivo para operar el proyecto [[Plomero Culiacan]] sin depender de memoria.

## Flujo base

1. Revisar estado del sitio con [[scripts crecer.py]].
2. Crear o modificar contenido segun [[SEO]] y [[Guia plomeria URL]].
3. Validar la pagina con [[gate-pagina.py]].
4. Correr [[ci-gate.py]] si el cambio toca estructura, indexabilidad o plantilla.
5. Revisar [[Sitemap]] si se agregaron URLs.
6. Publicar solo si los candados pasan.
7. Registrar cambios importantes en [[Bitacora]] y [[CHANGELOG]].

## Antes de publicar

- Confirmar que no hay fugas de otro sitio o marca.
- Confirmar que paginas nuevas no son doorway.
- Confirmar que el sitemap incluye URLs nuevas.
- Confirmar que [[sw.js]] se actualizo si hubo cambios que pueden quedar cacheados.
- Evitar tocar [[Scripts delicados]] sin correr validaciones.

## Si algo falla

1. Guardar el error en [[Errores y soluciones]].
2. Ubicar si el problema esta en [[Pipeline de publicacion]], [[SEO]], [[Automatizacion]] o [[Scripts delicados]].
3. No publicar hasta entender si el error es de contenido, infraestructura o cache.
4. Si queda pendiente, anotarlo en [[Tareas]].

## Relacionado

- [[Pipeline de publicacion]]
- [[Scripts delicados]]
- [[Grafo de invocacion real]]
- [[Docs existentes]]
- [[Graphify]]
- [[Tareas]]
- [[Archivos por revisar]]

#manual #operacion #publicacion
