# Grafo de invocacion real

Este mapa representa las llamadas reales entre scripts, comandos, launchd, subprocess y hooks.

## Por que importa

El proyecto tiene pocas dependencias por imports, pero muchas dependencias operativas por ejecucion.

## Ejemplo mental

```text
launchd
  -> crecer-diario.sh
  -> claude
  -> scripts/crecer.py
  -> ci-gate.py
  -> checkers
  -> git push
  -> pre-push
  -> Netlify
```

## Relacionado

- [[Graphify]]
- [[Pipeline de publicacion]]
- [[Scripts delicados]]
- [[Arquitectura]]

#grafo #invocaciones
