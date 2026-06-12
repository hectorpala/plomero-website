# ESTADO del pipeline de agentes

```json
{
  "ultima_corrida": {
    "fecha": "2026-06-12",
    "rama": "mantenimiento/altos-20260612",
    "modo": "arreglo de severidad ALTA",
    "hallazgos_altos_detectados": 11,
    "arreglados": 10,
    "verificados": 10,
    "pendientes": 1
  },
  "pendientes": [
    {
      "id": "seo-002",
      "categoria": "seo",
      "descripcion": "56 paginas de colonia siguen siendo plantillas casi identicas (doorway). Consolidar en paginas de zona con 301 o reescribir con contenido unico.",
      "razon_no_tocado": "decision estrategica, fuera del alcance del arreglo automatico",
      "severidad": "alta"
    }
  ],
  "baseline": {
    "fecha": "2026-06-12",
    "hallazgos_totales_diagnostico": 41,
    "por_categoria": {"seo": 10, "movil": 9, "a11y": 7, "perf": 11, "links": 4}
  },
  "aprobados": [
    "movil-001", "movil-002", "movil-003",
    "a11y-001", "a11y-002",
    "perf-001",
    "links-002", "links-003", "links-004",
    "seo-001"
  ]
}
```

## Resumen de la corrida 2026-06-12 (rama mantenimiento/altos-20260612)

- **Arreglados y verificados (10 altos):** movil-001, movil-002, movil-003, a11y-001, a11y-002, perf-001, links-002, links-003, links-004, seo-001.
- **Pendiente (1):** seo-002 — consolidación/reescritura de las 56 colonias (decisión estratégica, no automatizable).
- **Reglas actualizadas:** CACHÉ (ahora cubre JS/main.js, no solo CSS) y MÓVIL/tablas (patrón table-wrapper). Sin duplicar.
- **Sin push.** Cambios solo en la rama de mantenimiento.
