# Ficha de Google (Perfil de Empresa) — kit listo para copiar

Creado el 1-oct-2026. Hoy NO existe ficha: "plomero culiacan" lleva 3 meses en la posición 11
y Google enseña primero el mapa con fichas. Todo lo de abajo sale de
`~/gsc-mcp/datos-negocio-plomero.json` y `docs/NEGOCIO.md` (nada inventado).

## Paso a paso (lo hace Héctor, ~20 min + verificación)

1. Entra a **business.google.com** con hector.palazuelos@gmail.com → "Agregar empresa".
2. Copia los datos de abajo, sección por sección.
3. Tipo de negocio: **"Negocio de área de servicio"** (vas a domicilio). Marca **NO** mostrar
   dirección: así tu casa no aparece en el mapa.
4. Verificación: Google suele pedir un **video** (camioneta/herramienta con rotulación, una
   reparación, el letrero o el teléfono del negocio). Sin trucos: tiene que ser real.
5. Cuando esté verificada, pásale a Claude el enlace de la ficha (`https://g.page/r/...`). Él
   lo agrega al sitio (`sameAs` del JSON-LD).

## Datos

| Campo | Valor |
|---|---|
| Nombre | `Plomero Culiacán Pro` (exacto, sin agregar palabras: Google suspende fichas con nombres rellenos) |
| Categoría principal | `Plomero` |
| Categorías extra | `Servicio de destape de cañerías` · `Servicio de reparación de calentadores de agua` · `Servicio de detección de fugas de agua` · `Contratista de gas` |
| Teléfono | `667 392 2273` |
| WhatsApp (chat) | `+52 667 392 2273` |
| Sitio web | `https://plomeroculiacanpro.mx/?utm_source=google&utm_medium=organic&utm_campaign=ficha-google` (con esto Analytics separa las visitas que vienen de la ficha) |
| Horario | Abierto 24 horas, los 7 días (solo si de verdad contestas de noche) |
| Área de servicio | Culiacán, Sinaloa · Costa Rica (Sinaloa) · Eldorado (solo si de verdad vas) |
| Fecha de apertura | la real (no inventar) |

## Descripción (pegar tal cual, 639 de 750 caracteres)

```
Plomería residencial y comercial en Culiacán, Sinaloa, con servicio de emergencia las 24 horas. Destapamos baños y drenajes, detectamos y reparamos fugas de agua, instalamos y reparamos boilers, tinacos, cisternas, bombas, sanitarios, llaves y mezcladoras, y atendemos instalaciones y fugas de gas. Primero diagnosticamos y te damos una cotización clara por escrito, sin costo; no empezamos hasta que la autorices. Todas las reparaciones llevan garantía escrita de 6 meses en mano de obra y materiales. Llegada típica de 30 a 60 minutos en Culiacán. Puedes mandarnos fotos o video del problema por WhatsApp para darte una idea antes de ir.
```

## Servicios (sección "Servicios" de la ficha)

Agrega cada uno con su descripción corta. **Sin precios** (misma regla que el sitio).

- Destape de drenajes y baños — sonda e hidrojet; diagnóstico antes de cotizar.
- Desazolve y limpieza de drenajes
- Detección de fugas de agua — geófono y termografía, sin romper de más.
- Reparación de fugas
- Cambio de tuberías — cobre, PVC, CPVC y PEX.
- Corrección de baja presión de agua
- Instalación de boiler
- Reparación y mantenimiento de boiler
- Instalación de tinaco
- Instalación de cisternas
- Instalación de sanitarios
- Reparación de llaves y mezcladoras
- Plomería comercial
- Plomero urgente 24 horas
- Técnico de gas — instalación de líneas y detección de fugas.

## Fotos (lo que más mueve la ficha)

Solo fotos **reales y tuyas**. Mínimo para arrancar:
- Logo (cuadrado) y portada.
- 3 de la camioneta/herramienta.
- 10 de trabajos: antes y después de destapes, fugas, boilers, tinacos.
- 2–3 tuyas o del equipo trabajando (genera confianza).
Después: 2–3 fotos nuevas por semana de trabajos reales.

## Reseñas (reales, nunca compradas ni inventadas)

Después de cada trabajo terminado, manda por WhatsApp (cambia `ENLACE` por el enlace de reseñas
que da la ficha en "Pedir reseñas"):

```
¡Gracias por confiar en Plomero Culiacán Pro! Si quedaste contento con el servicio, ¿nos ayudas con una reseña? Nos toma 1 minuto y ayuda muchísimo a que otros vecinos nos encuentren: ENLACE
```

Reglas de Google: no ofrecer descuentos a cambio de reseñas, no pedirlas a familiares
haciéndose pasar por clientes, contestar todas (buenas y malas) en menos de 48 h.

## Cuando ya tengas reseñas reales

Avísale a Claude para:
- Agregar el enlace de la ficha al sitio (`sameAs` en el JSON-LD del negocio).
- Poner un botón "Ver reseñas en Google" que lleve a la ficha real.
- **No** volver a escribir calificaciones a mano en el sitio: `check-plantilla.py` check 28 lo
  bloquea. Se muestran solo si vienen de la ficha real.
