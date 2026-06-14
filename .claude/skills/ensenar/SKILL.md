---
name: ensenar
description: Enseña al pipeline a detectar un error que se le escapó. Agrega la regla a REGLAS.md y, si es mecánico, un assert determinista a check-plantilla.py (aprender = test que falla); si es subjetivo, una línea al revisor LLM. Uso /ensenar <descripción del error>
disable-model-invocation: true
---
El humano detectó un error que el pipeline no atrapó. Tu trabajo es que NO vuelva a escaparse. El error es: $ARGUMENTS

Pasos:
1. Entiende el error: qué es, en qué archivo/tipo de página aparece, y por qué es un problema. Si falta info, pregúntame con AskUserQuestion antes de seguir.
2. Decide a qué categoría pertenece (seo, movil, a11y, perf, links, gsc) y CLASIFÍCALO:
   - **MECÁNICO** = se puede detectar parseando/grepeando el HTML o los archivos del repo, sin juicio (presencia/ausencia de un atributo, tag, valor, archivo, patrón). Ej: og:image a archivo inexistente, popup sin `role="dialog"`, breadcrumb sin 3 niveles, `<img>` sin width/height, enlace roto.
   - **SUBJETIVO** = requiere criterio (calidad de copy, intención de búsqueda, similitud visual de doorways, percepción de contraste, decisión editorial/estratégica).
   Si es ambiguo, trátalo como subjetivo (no metas en el checker algo que dé falsos positivos).
3. Agrega una regla nueva a REGLAS.md, consolidando si ya existe una parecida (no dupliques). Formato: "- [FECHA] CATEGORÍA: regla concreta — por qué. Severidad: alta/media/baja".
4. Haz que el pipeline lo DETECTE SIEMPRE, según la clasificación del paso 2:
   - **Si es MECÁNICO → añade un assert determinista a `.pipeline/check-plantilla.py`** (aprender = un test que falla, no un párrafo que el LLM debe recordar). Sigue el patrón ya existente del archivo:
     a. Para una regla por-página, añade un bloque check dentro de `check_page(fpath, t, noindex, redirects)` (numéralo como los demás: `# --- N. <descripción> (severidad, categoria)`), parseando con los helpers existentes (`attr`, `imgs`, `re`, `resolve_to_disk`, `has_noindex`…) y emitiendo el hallazgo con `add(severidad, r, categoria, descripcion, fix_sugerido)`. Para una regla global (todo el sitio, p.ej. paridad entre archivos), añade una función `check_*()` y llámala desde `main()` como `check_css_parity()`.
     b. Respeta las invariantes del checker: solo LEE disco (sin red, sin servidor), salida DETERMINISTA (no dependas de orden de `os.walk`; el `add()` ya se ordena al final), `categoria` ∈ seo/movil/a11y/perf/links, y NO marques como roto lo que un redirect cubre.
     c. Actualiza el bloque docstring de cabecera (la lista numerada de "Reglas mecanicas") con la regla nueva.
     d. VERIFICA que el test realmente falla ante el bug: corre `python3 .pipeline/check-plantilla.py` y confirma que AHORA reporta un hallazgo para la página/archivo con el error (que antes no salía). Confirma también que NO dispara sobre una página sana (cero falsos positivos) y que la salida sigue siendo determinista (dos corridas idénticas: `python3 .pipeline/check-plantilla.py | md5` dos veces). Como el revisor-plantilla ya corre este checker, no hace falta tocar su `.md`.
   - **Si es SUBJETIVO → actualiza el revisor LLM correspondiente** (`.claude/agents/revisor-X.md`): añade una línea concreta a su lista de qué revisar, para que SIEMPRE busque este tipo de problema. (No lo metas en el checker: daría falsos positivos.)
5. Registra en HISTORIAL.jsonl una línea indicando que se enseñó esta detección (con fecha, categoria, "tipo":"aprendizaje_humano", y si fue "mecanico":true/false).
6. Muéstrame: la regla que agregaste, si fue assert mecánico (con la EVIDENCIA del paso 4.d: el hallazgo nuevo + las dos corridas con el mismo md5) o línea en el revisor LLM, y confirma que quedó. Haz commit con mensaje "learn: enseñar al pipeline a detectar <resumen>" — sin push.

NO arregles el error del sitio ahora; este comando solo ENSEÑA a detectarlo. El arreglo lo hará la próxima corrida del pipeline.
