# Meta-pase del Crítico-Sistema — 2026-07-10

Dejé **4 propuestas nuevas**, todas con su DRAFT ya escrito y probado en vivo contra el sitio real,
listas para merge en `docs/PROPUESTAS.md` (las nuevas van arriba). Yo no apliqué nada — tú apruebas.

## Top 3 por impacto
1. **(A) 6 páginas de zona/colonia usan la coordenada GPS GENÉRICA del centro de Culiacán, no la real.**
   La regla existe desde el 11 de junio ("cada página local debe tener coordenadas reales y únicas —
   la genérica es señal de doorway para Google") pero es de las pocas reglas que JAMÁS se mecanizó en un
   checker, y ya reincidió 3 veces. Lo comprobé hoy en vivo: las 4 páginas de zona (norte/sur/oriente/poniente)
   + centro comparten la MISMA coordenada, y la colonia "Barrio Estación" también la usa (sus 24 hermanas
   sí tienen coordenadas reales y distintas). El draft añade el checker que lo cierra para siempre.
2. **(A) El checker de `twitter:url` solo revisa que la etiqueta EXISTA, nunca que apunte al lugar correcto.**
   Ese hueco dejó que el mismo bug (la tarjeta de X/Twitter enlazando al HOME en vez de a la página) reincidiera
   3 veces — la última, dos páginas a la vez, el 9 de julio. Ahora mismo el sitio está limpio (ya lo arreglaron
   a mano), pero sin este draft el bug vuelve a aparecer la próxima vez que alguien edite una página a mano.
3. **(M) La garantía se puede contradecir dentro de la MISMA página y nadie lo revisa.** La regla de julio
   agrupa "garantía, precio o rating" bajo un solo checker, pero ese checker (el que ya existe) solo mira el
   rating — la garantía se quedó fuera pese a estar nombrada. Probé el draft contra las 86 páginas del sitio
   HOY: 5 tienen dos duraciones de garantía distintas en el mismo texto (p. ej. "30 días" y "3 meses" en
   /precios/). Lo dejé en severidad BAJA a propósito — avisa, no autocorrige, porque puede haber garantías
   legítimamente distintas por línea de servicio y eso necesita ojo humano, no un fixer ciego.

La 4ª (B, esfuerzo mínimo): una tarea del backlog (`bk-12b83ae9`, "reautenticar el token de GSC") sigue
marcada `requiere_humano` desde hace 18 días, pero el problema real se resolvió el 26 de junio por otra vía
(sin re-login). Es ruido puro en cada corrida — el draft es un solo comando para cerrarla.

**Cómo verifiqué los drafts:** no me quedé en "debería funcionar" — pegué las 3 funciones nuevas en una copia
de `check-plantilla.py`, la corrí contra el sitio real (86 páginas, 0.76s, sin errores) y confirmé que
los hallazgos de arriba (6 geo, 0 twitter:url, 5 garantía) coinciden con lo que reporta. La copia de prueba
ya está borrada — no toqué el checker real.

**Estado del sistema:** el pipeline sigue sano en general (0 corridas perdidas, backlog casi vacío salvo la
tarea zombie de arriba). El patrón de esta semana es que hay reglas ESCRITAS en REGLAS.md que nunca se
tradujeron a un checker — las propuestas 1 y 3 cierran ese tipo de hueco puntual; la 2 cierra una regresión
ya reincidente. Todas están listas para merge en `docs/PROPUESTAS.md`.
