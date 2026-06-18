# Routing de modelos por revisor — política (decidir bien SIN restar efectividad)

Cada revisor declara su `model:` en el frontmatter. La regla NO es "lo barato a Haiku": es
**el modelo justo según dónde vive la inteligencia de la tarea**. Bajar de modelo solo donde el
modelo NO cambia el resultado; mantener el fuerte donde su juicio ES el producto.

## El principio (3 preguntas)

1. **¿La verdad la produce un checker determinista y el agente solo lo corre y relaya el JSON?**
   → **haiku.** Haiku ejecuta el comando y devuelve el JSON igual que Opus. Cero pérdida de efectividad.
2. **¿Hay juicio ligero, medición headless, o es sensible (seguridad) pero mecánico?**
   → **sonnet.** Capaz, pero sin pagar Opus donde no hace falta.
3. **¿El JUICIO del modelo ES el entregable (calidad de copy, thin content, doorway, meta-crítica)?**
   → **opus.** Aquí un error es caro; no se degrada.

## Asignación actual

| Modelo | Revisores | Por qué |
|---|---|---|
| **haiku** (10) | conversion · e2e-funcional · enlazado-interno · indexabilidad · infra-salud · nap · perf-real · plantilla · produccion · tracking | Cada uno corre un checker (`check-*.py`/`.mjs`); el JSON del checker es la verdad. El modelo solo lo invoca. |
| **sonnet** (7) | gsc · a11y · movil · perf · seo · links · secretos | Juicio ligero / medición headless / patrón sensible. No arriesgar Haiku, no malgastar Opus. |
| **opus** (2) | contenido · critico-completitud | El juicio subjetivo ES el producto (ortografía/thin content/duplicado; detectar huecos ciegos del pipeline). |

## Roles que NO se tocan (heredan el modelo de sesión = Opus)
- El **builder/fixer** (escribe contenido/código), el **verificador adversarial** (FASE 7) y el
  **bibliotecario** (FASE 9, escribe reglas/checkers): quality-critical → se quedan en Opus.

## Cómo decidir para un revisor NUEVO
Si su `description` dice "Solo checks locales y mecánicos" y corre un `check-*`, es **haiku**.
Si pide juzgar calidad/intención/duplicado, es **opus**. Si está en medio, **sonnet**.
Ante la duda, sube un escalón: el ahorro no vale perder efectividad.
