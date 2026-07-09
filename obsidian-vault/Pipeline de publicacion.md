# Pipeline de publicacion

Mapa operativo de como una generacion termina publicada.

```text
launchd
  -> autoagente / catchup / meta
  -> crecer-diario.sh
  -> scripts/crecer.py
  -> ci-gate.py
  -> gate-pagina.py
  -> pre-push
  -> GitHub
  -> Netlify
```

## Nodos relacionados

- [[Automatizacion]]
- [[Scripts delicados]]
- [[SEO]]
- [[Grafo de invocacion real]]
- [[Bitacora]]
- [[Manual operativo]]
- [[ci-gate.py]]
- [[gate-pagina.py]]
- [[scripts crecer.py]]
- [[Sitemap]]
- [[CHANGELOG]]

## Riesgo

Cambios en checkers, gates o hooks pueden bloquear publicaciones o dejar pasar paginas malas.

#pipeline #publicacion
