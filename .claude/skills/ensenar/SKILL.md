---
name: ensenar
description: Enseña al pipeline a detectar un error que se le escapó. Agrega la regla a REGLAS.md y actualiza el revisor correspondiente para que lo cace siempre. Uso /ensenar <descripción del error>
disable-model-invocation: true
---
El humano detectó un error que el pipeline no atrapó. Tu trabajo es que NO vuelva a escaparse. El error es: $ARGUMENTS

Pasos:
1. Entiende el error: qué es, en qué archivo/tipo de página aparece, y por qué es un problema. Si falta info, pregúntame con AskUserQuestion antes de seguir.
2. Decide a qué categoría pertenece (seo, movil, a11y, perf, links, gsc) y por tanto qué revisor debe aprender a detectarlo.
3. Agrega una regla nueva a REGLAS.md, consolidando si ya existe una parecida (no dupliques). Formato: "- [FECHA] CATEGORÍA: regla concreta — por qué. Severidad: alta/media/baja".
4. Actualiza el archivo del revisor correspondiente (.claude/agents/revisor-X.md) para que SIEMPRE busque este tipo de problema de ahora en adelante: añade una línea concreta a su lista de qué revisar.
5. Registra en HISTORIAL.jsonl una línea indicando que se enseñó esta detección (con fecha, categoria, "tipo":"aprendizaje_humano").
6. Muéstrame: la regla que agregaste, qué revisor actualizaste y cómo, y confirma que quedó. Haz commit con mensaje "learn: enseñar al pipeline a detectar <resumen>" — sin push.

NO arregles el error del sitio ahora; este comando solo ENSEÑA a detectarlo. El arreglo lo hará la próxima corrida del pipeline.
