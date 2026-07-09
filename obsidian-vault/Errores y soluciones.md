# Errores y soluciones

Registro de fallas, sintomas, causa y solucion.

## 2026-07-08 - Obsidian abria un vault vacio

Sintoma:
Obsidian se abria, pero el usuario no veia las notas ni el mapa del proyecto. Parecia estar en blanco.

Causa:
Obsidian estaba registrado para abrir `/Users/openclaw/Documents/Obsidian Vault`, no el vault real del proyecto.

Solucion:
Se registro el vault correcto:

`/Users/openclaw/Sitios Web/Plomero Culiacan/obsidian-vault`

Tambien se agrego `INICIO - ABRE ESTO.md` y un `workspace.json` para abrir el mapa con Graph view.

Validacion:
Los archivos `.md` existen dentro de `obsidian-vault/` y estan conectados con enlaces internos. El mapa debe mostrar [[Manual operativo]], [[Pipeline de publicacion]], [[Scripts delicados]], [[SEO]] y [[Tareas]].

Relacionado:
- [[Manual operativo]]
- [[Tareas]]
- [[Pipeline de publicacion]]
- [[Scripts delicados]]
- [[Bitacora]]

## Plantilla

```md
## YYYY-MM-DD - Titulo del problema

Sintoma:

Causa:

Solucion:

Validacion:

Relacionado:
- [[Pipeline de publicacion]]
- [[Scripts delicados]]
```

## Relacionado

- [[Manual operativo]]
- [[Scripts delicados]]
- [[Pipeline de publicacion]]
- [[Bitacora]]
- [[Tareas]]

#errores #soluciones
