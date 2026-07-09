# check-infra.mjs

Ruta: `.pipeline/check-infra.mjs`

## Para que sirve

Dead-man switch del pipeline. No revisa solo paginas; revisa que los sensores del sistema esten vivos.

## Que cuida

- Frescura del cron/logs.
- GSC vivo.
- Checkers sanos.
- Corpus no vacio.
- Produccion disponible.

## Riesgo

Es uno de los nodos mas delicados: si falla mal, puede avisar demasiado o dejar ciego el mantenimiento.

## Validacion

```bash
node .pipeline/check-infra.mjs
```

## Relacionado

- [[Scripts delicados]]
- [[Automatizacion]]
- [[Pipeline de publicacion]]
- [[Grafo de invocacion real]]

#script #infra #checker
