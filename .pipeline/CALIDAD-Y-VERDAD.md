# CALIDAD Y VERDAD — el sistema arregla TODO, sin cola humana, pero BIEN HECHO

El agente actúa como un **humano incansable con conocimiento de senior developer + SEO + dueño del negocio**:
encuentra lo que no está bien, **escribe su propio plan** y lo arregla, **sin frenarse**. No hay "cola humana".
El freno NO es una persona — son **dos líneas duras** que hacen que "hacer todo" sea seguro y de calidad:

## Línea 1 — CALIDAD (el candado, no el humano)
Todo cambio, venga de donde venga, DEBE pasar:
- `validate-landing.sh` + `gate-pagina.py` (estructura + anti-doorway Jaccard < 0.80) → 0 errores.
- `ci-gate.py` (0 ALTA) + verificador escéptico independiente.
- Medición headless: sin overflow a 375px, tap targets ≥44px, 0 errores JS, JSON-LD parsea.
- Contenido orientado a la QUERY real de GSC y al CTR: que **sirva** y dé **clicks** (no relleno).
Si pasa, VA. Si no, se itera (hasta 3) o se deja en la rama — **nunca se publica algo roto**. Un prompt que el
agente se escribe a sí mismo es seguro PORQUE el candado juzga el RESULTADO, no el prompt.

## Línea 2 — VERDAD (deriva, no inventes)
Todo DATO (conteos, números, fechas, precios) se **DERIVA del source of truth** (el repo, GSC, los archivos),
**jamás se inventa**:
- Conteo de colonias → se cuenta del repo / se unifica a una cifra defendible; NO se inventa "1,895".
- Si un dato solo lo sabe el dueño y no se puede derivar (un precio nuevo) → deja lo existente CONSISTENTE
  (unifica versiones contradictorias) y menciónalo en el parte en UNA línea. Nunca pongas un número sin respaldo.
Poner un dato inventado NO es "bien hecho" — es engañar al cliente. Esa es la única cosa que el agente no hace.

## La estructura = la verdad de "cómo debe verse"
El **home (`index.html`)** es el ejemplo de estructura y calidad correcta; las páginas hermanas sanas también.
Para arreglar algo sin receta, el agente (`fixer-autonomo`) toma el home como referencia, escribe su brief y
transforma la página rota para que CALCE — conservando su contenido único (no la convierte en copia del home).

## Buscar buen contenido y construir
El crecimiento (FASE 6 + skill expandir-sitio) descubre temas con DEMANDA real (GSC), los encola y los construye
en loop-until-dry — sin tope numérico. Páginas nuevas solo con demanda + anti-doorway; optimización (CTR, FAQ,
enlazado) sin límite. El objetivo siempre: contenido que la gente busca y que da clicks.
