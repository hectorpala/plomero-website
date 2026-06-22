# NEGOCIO.md — Fuente única de verdad del negocio

Este archivo existe para que el Auto Agente **derive** las decisiones de negocio en vez de
preguntarte cada corrida. Tú lo curas de vez en cuando (servicios, precios, políticas); la
computadora lo ejecuta continuamente. **Si algo cambia, edítalo AQUÍ y queda autónomo para
siempre.** Lo lee en la FASE 0 y lo aplica en la FASE 6 (qué crear) y en la FASE 5 (contenido).

> Regla madre: **"deriva, no inventes".** Si una decisión se puede resolver con ESTE archivo +
> los datos (repo/GSC), la máquina decide sola. Si NO, va a humano (cola `requiere_humano`).

## Giro
Plomería **residencial y comercial** en Culiacán, Sinaloa. Todo lo que sea PLOMERÍA cae en el giro.

## Servicios que SÍ ofreces — auto-creables si hay DEMANDA real en GSC
(derivados de las páginas existentes en `servicios/`)
- Destapes y desazolve (baños, inodoros, drenajes)
- Detección y reparación de fugas (incl. fugas de agua)
- Tuberías: cambio e instalación
- Corrección de baja presión de agua
- Boilers: instalación, reparación, mantenimiento
- Tinacos, cisternas y **bombas de agua** (instalación y reparación)
- Sanitarios, llaves y mezcladoras (instalación y reparación)
- Plomería de **emergencia 24/7**
- **Plomería comercial**
- **Técnico de gas** (instalación y detección de fugas de gas)

## Decisión de PÁGINA NUEVA  ("auto si es plomería")
1. Query de GSC con demanda real (≥ UMBRAL_DEMANDA) que cae CLARAMENTE en plomería (lista de
   arriba o un vecino directo del giro, p.ej. "fluxómetro", "calentador de paso") →
   **CREAR sola**: encólala riesgo **medio** (auto-drena en FASE 6). Pasa por todos los candados.
2. Query FUERA de plomería (electricidad, aire acondicionado, albañilería, impermeabilización,
   jardinería, cerrajería…) o **ambigua** → **NO crear**: encólala riesgo **alto**
   (`requiere_humano`) y menciónala en el parte para que el dueño decida.
3. Ante la duda de si algo "es plomería" → trátalo como ambiguo (riesgo alto), nunca lo fuerces.

## Servicios que NO ofreces  (jamás crear; si hay demanda, va a humano)
<!-- Curado por el dueño. Agrega aquí lo que NO haces aunque la gente lo busque. Vacío = todo
     lo de plomería se auto-crea; lo no-plomería ya se escala solo por la regla de arriba. -->
- (ninguno declarado todavía)

## Precios
- **NUNCA** precio visible en el cuerpo (regla dura, la caza `check-pagina-nueva.py`). Lenguaje:
  "cotización sin costo / cotización clara". Las cifras solo en JSON-LD (priceRange/offers).
- No inventar precios. Si un precio solo lo sabe el dueño y no se puede derivar → no lo pongas.

## Contenido / año
- Unificar el año visible al **año actual** es seguro por defecto (freshness), SIEMPRE que no
  implique afirmar precios nuevos. `datePublished` NO se toca; `dateModified` = hoy si editas.
- Si subir el año daría a entender precios de "este año" sin confirmación del dueño, deja el año
  consistente con la última edición real y NO insinúes precios nuevos.

## Datos fijos (derivados, no inventar)
- Contacto: WhatsApp/tel **667 392 2273** · email **info@plomeroculiacanpro.mx**.
- Anti-doorway: Jaccard < 0.80 (lo bloquea `gate-pagina.py`).
- Cobertura: Culiacán y colonias (ver `servicios/plomero-colonias-culiacan/`).
