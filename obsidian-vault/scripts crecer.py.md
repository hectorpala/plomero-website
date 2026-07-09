# scripts crecer.py

Ruta: `scripts/crecer.py`

## Para que sirve

Orquestador de crecimiento del sitio. Es un punto de entrada para estado, servicios, colonias, gates, sitemap, service worker y publicacion.

## Comandos importantes

```bash
python3 scripts/crecer.py estado
python3 scripts/crecer.py gate ruta/a/index.html
python3 scripts/crecer.py publicar "mensaje"
```

## Riesgo

Toca muchas piezas: sitemap, enlaces internos, [[sw.js]], gates, git y publicacion.

## Relacionado

- [[Manual operativo]]
- [[Pipeline de publicacion]]
- [[Sitemap]]
- [[gate-pagina.py]]
- [[sw.js]]

#script #orquestador
