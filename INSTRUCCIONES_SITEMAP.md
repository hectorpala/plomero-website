# Instrucciones para Actualizar el Sitemap

## 🎯 Propósito

El script `update-sitemap.sh` automatiza la actualización del sitemap con fechas reales de modificación de archivos y configuraciones de `changefreq` optimizadas para SEO.

## 📋 Cuándo Usar el Script

Ejecuta el script cada vez que:
- ✅ Actualices contenido en cualquier página (homepage, servicios, blog)
- ✅ Agregues nuevos artículos de blog
- ✅ Modifiques páginas de servicios
- ✅ Hagas cambios importantes en el sitio
- ✅ Antes de hacer deploy a producción

## 🚀 Cómo Usar

```bash
# Desde la raíz del proyecto
./update-sitemap.sh
```

## 🔧 Qué Hace el Script

1. **Lee la fecha de modificación real** de cada archivo HTML
2. **Asigna `changefreq` inteligente** según el tipo de página:
   - `weekly`: Homepage, Blog index (contenido dinámico)
   - `monthly`: Servicios, Artículos de blog (contenido estable)
   - `yearly`: Contacto (raramente cambia)
3. **Mantiene las prioridades** correctas para SEO
4. **Genera sitemap válido** en `sitemaps/main_sitemap.xml`

## 📊 Configuración de Changefreq

| Tipo de Página | Changefreq | Razón |
|----------------|------------|-------|
| Homepage | weekly | Se actualiza frecuentemente con nuevo contenido |
| Blog Index | weekly | Se agrega nuevo contenido regularmente |
| Páginas de Servicio | monthly | Contenido estable, cambios ocasionales |
| Artículos de Blog | monthly | Contenido evergreen, raramente se modifica |
| Página de Contacto | yearly | Información estática |

## 🔄 Agregar Nuevas URLs

Si agregas nuevas páginas al sitio:

1. Abre `update-sitemap.sh`
2. Agrega una nueva línea en la sección "Procesar todas las URLs":

```bash
process_url "https://plomeroculiacanpro.mx/nueva-pagina/" "0.X"
```

3. Ajusta la prioridad (0.1 a 1.0) según la importancia de la página

## 🎯 Prioridades Recomendadas

- **1.0**: Homepage
- **0.9**: Servicios principales, páginas de alta conversión
- **0.8**: Servicios secundarios, categorías importantes
- **0.7**: Artículos de blog, páginas de soporte
- **0.6**: Contenido complementario

## 📝 Actualizar Meta Tag x-build

Después de ejecutar el script, actualiza el meta tag en `index.html`:

```html
<meta name="x-build" content="YYYY-MM-DDTHH:MM:SSZ" />
```

O ejecuta:
```bash
# El script muestra la fecha actual que puedes copiar
```

## ✅ Verificar el Sitemap

Después de ejecutar el script:

1. Revisa `sitemaps/main_sitemap.xml`
2. Verifica que las fechas sean actuales
3. Confirma que todas las URLs estén presentes
4. Valida en: https://www.xml-sitemaps.com/validate-xml-sitemap.html

## 🚨 Importante

- El script **NO** hace commit automático
- **Revisa** los cambios antes de hacer commit
- **Ejecuta** antes de cada deploy importante
- **Mantén sincronizado** el meta tag x-build con las fechas del sitemap

## 🔗 Beneficios SEO

✅ **Señales de frescura**: Google ve fechas actualizadas reales
✅ **Crawl budget optimizado**: `changefreq` ayuda a Google a priorizar
✅ **Indexación rápida**: Nuevas páginas se descubren más rápido
✅ **Consistencia**: Meta tags alineados con sitemap
