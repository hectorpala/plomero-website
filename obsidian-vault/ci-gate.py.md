# ci-gate.py

Ruta: `.pipeline/ci-gate.py`

## Para que sirve

Gate determinista para CI y pre-commit. Corre checkers locales de disco y bloquea si hay hallazgos de severidad alta.

## Checkers que coordina

- `check-plantilla.py`
- `check-indexabilidad.py`
- `check-estructura-sitio.py`
- `check-rutas-pipeline.py`

## Riesgo

Si se rompe, puede bloquear commits buenos o dejar pasar errores graves.

## Validacion

```bash
python3 .pipeline/ci-gate.py
```

## Relacionado

- [[Scripts delicados]]
- [[Pipeline de publicacion]]
- [[gate-pagina.py]]
- [[check-infra.mjs]]

#script #gate #ci
