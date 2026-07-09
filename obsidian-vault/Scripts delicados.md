# Scripts delicados

Scripts que no conviene tocar a la ligera porque afectan publicacion, validacion, cache o automatizacion.

## Alto riesgo

- `.pipeline/check-infra.mjs`
- `ci-gate.py`
- `gate-pagina.py`
- `check-pagina-nueva.py`
- `check-contrato-checkers.mjs`
- `scripts/crecer.py`
- `sw.js`

## Notas especificas

- [[check-infra.mjs]]
- [[ci-gate.py]]
- [[gate-pagina.py]]
- [[check-pagina-nueva.py]]
- [[check-contrato-checkers.mjs]]
- [[scripts crecer.py]]
- [[sw.js]]

## Regla practica

Si cambia alguno de estos, correr el pipeline/checkers relevantes antes de publicar.

## Relacionado

- [[Pipeline de publicacion]]
- [[Grafo de invocacion real]]
- [[Automatizacion]]
- [[Bitacora]]
- [[Manual operativo]]
- [[Errores y soluciones]]

#riesgo #scripts
