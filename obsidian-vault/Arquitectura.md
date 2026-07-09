# Arquitectura

La arquitectura real del proyecto combina sitio estatico, scripts de generacion, checkers, automatizaciones y despliegue.

## Relacionado

- [[Plomero Culiacan]]
- [[Pipeline de publicacion]]
- [[Automatizacion]]
- [[Scripts delicados]]
- [[Graphify]]
- [[Grafo de invocacion real]]

## Idea clave

El codigo no se conecta principalmente por imports. Muchas relaciones viven en llamadas por shell, subprocess, launchd y hooks.

#arquitectura
