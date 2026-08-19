# Oportunidades GSC — 2026-08-18

Periodo: 28 días. Rendimiento: 583 clics, 59,603 impresiones, CTR 0.98%, posición media 6.6. Los sitemaps reportan 0 errores y 0 advertencias.

| # | oportunidad | dimensión | impacto | esfuerzo | riesgo doorway | acción |
|---|---|---|---|---|---|---|
| 1 | “tabla de precios de plomería”: 444 impresiones, pos. 6.8, 1 clic | GSC/CTR | alto | bajo | nulo | Conservar `/precios/`: ya tiene title, H1 y meta alineados exactamente con la consulta; no sobreoptimizar sin una prueba CTR posterior |
| 2 | “lista de precios de plomería en México”: 272 impresiones, pos. 8.1, 1 clic | GSC/CTR | alto | medio | nulo | Enriquecer solo si NEGOCIO.md permite alcance nacional; hoy la página declara Culiacán y no se inventa cobertura nacional |
| 3 | consultas de baño tapado: 587 impresiones en la principal y varias variantes con CTR bajo | GSC/contenido | alto | bajo | nulo | Conservar y medir `/blog/desatascar-wc-metodos-profesionales/`: el title ya responde “cómo destapar un baño muy tapado” y la meta explica métodos y límites |
| 4 | consultas de tinaco lleno sin presión: 120/106/87 impresiones, posiciones 5–6 | GSC/contenido | medio | bajo | nulo | Enriquecer la página existente, no crear otra: `/blog/baja-presion-agua-causas-soluciones/` ya concentra la intención |
| 5 | “bombas de agua en Sinaloa”: 30 impresiones, pos. 8, 0 clics | GSC/servicio | bajo | medio | alto | No crear: búsqueda ambigua de producto/venta; el sitio ofrece corrección de presión, no se deriva que venda bombas |

## Decisión del panel

```json
{"decisiones":[{"accion":"enriquecer","objetivo":"/precios/","tipo":"ctr-fix","riesgo":"bajo","demanda":"444 impresiones para tabla de precios; 272 para lista de precios en México","porque":"DEV: la intención ya tiene página dedicada y el snippet actual coincide; no crear duplicado. MAESTRO: mantener el enfoque local y los precios canónicos, sin prometer cobertura nacional."},{"accion":"enriquecer","objetivo":"/blog/desatascar-wc-metodos-profesionales/","tipo":"ctr-fix","riesgo":"bajo","demanda":"587 impresiones para cómo destapar un baño muy tapado y 172 impresiones/cero clics para una variante","porque":"Ambos expertos: la consulta ya está cubierta por una guía específica; medir el title/meta actual antes de reescribir otra vez."},{"accion":"enriquecer","objetivo":"/blog/baja-presion-agua-causas-soluciones/","tipo":"enriquecer","riesgo":"bajo","demanda":"múltiples variantes de 76–120 impresiones en posiciones 5–7","porque":"Ambos expertos: es el mismo diagnóstico de tinaco/presión, por lo que una página nueva sería duplicada."},{"accion":"humano","objetivo":"bombas-de-agua-en-sinaloa","tipo":"pagina-nueva","riesgo":"alto","demanda":"30 impresiones, posición 8, cero clics","porque":"DEV: la intención puede ser venta de producto. MAESTRO: NEGOCIO.md no autoriza inventar que se venden bombas; gana la decisión conservadora."}]}
```

Resultado del loop: backlog autoejecutable vacío en dos consultas; 0 páginas nuevas porque toda demanda válida ya tiene destino propio y los snippets principales ya responden a la consulta.
