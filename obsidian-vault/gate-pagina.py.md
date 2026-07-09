# gate-pagina.py

Ruta: `.pipeline/gate-pagina.py`

## Para que sirve

Candado para paginas nuevas o modificadas antes de publicar.

## Que revisa

- Anti-fuga: evita palabras o IDs de otro sitio.
- Validacion de landing cuando aplica.
- [[ci-gate.py]].
- Anti-doorway por similitud de contenido visible.

## Riesgo

Si se relaja demasiado, puede publicar paginas duplicadas o fugas de marca. Si se endurece demasiado, puede bloquear paginas validas.

## Validacion

```bash
python3 .pipeline/gate-pagina.py ruta/a/index.html
```

## Relacionado

- [[Scripts delicados]]
- [[Pipeline de publicacion]]
- [[SEO]]
- [[Guia plomeria URL]]

#script #gate #doorway
