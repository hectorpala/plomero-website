# Medir LEADS (WhatsApp + Llamadas) en GA4 — receta exacta

**Problema:** GA4 marca **0 conversiones**. Los clics a WhatsApp (`wa.me`) y a llamar (`tel:`) no se
cuentan como leads. Sin esto no sabes qué páginas/cambios generan llamadas.

**Estado actual del código:** `main.js` solo trackea los botones con id `cta-whatsapp`/`cta-llamar`
(los flotantes del home). NO trackea: los CTA del hero ("Cotización por WhatsApp"/"Llamar Ahora"),
los `wa.me`/`tel:` inline del contenido, ni los flotantes de las páginas de servicio. Por eso GA4 ve casi nada.

**Detalle clave (por qué importa el orden):** el sitio carga GTM DIFERIDO para proteger el LCP. Si GTM
cargara recién con el clic, se perdería ese primer clic (el listener aún no existe). Por eso la vía
confiable es **empujar el evento a `dataLayer` desde el código en el momento del clic** (queda en la cola)
y que GTM lo procese al cargar — NO un disparador de clic propio de GTM (que llegaría tarde).

---

## Parte A — CÓDIGO (lo hace el dev): cobertura total del clic
Añadir a `main.js` UN listener delegado que cace TODO `wa.me`/`tel:` de cualquier página y empuje
`generate_lead` a `dataLayer`. (Requiere versionar `main.js?v=` en todas las páginas + bump de `sw.js` —
el proceso estándar de las REGLAS; ojo con no truncar las URLs `wa.me` al minificar.)

```js
// Lead tracking universal: cualquier clic a WhatsApp o teléfono, en cualquier página.
document.addEventListener('click', function (e) {
  var a = e.target.closest && e.target.closest('a[href]');
  if (!a) return;
  var href = a.getAttribute('href') || '';
  var metodo = href.indexOf('wa.me') !== -1 || href.indexOf('whatsapp') !== -1 ? 'whatsapp'
             : href.indexOf('tel:') === 0 ? 'llamada' : null;
  if (!metodo) return;
  try {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({ event: 'generate_lead', metodo: metodo, page: location.pathname });
  } catch (err) {}
}, true);
```

## Parte B — GTM (lo haces tú en gtm.google.com, contenedor GTM-W75CRTX5) — ~5 min
1. **Disparador** → Nuevo → tipo **"Evento personalizado"** (Custom Event):
   - Nombre del evento: `generate_lead`  · Se activa en: Todos los eventos personalizados.
   - Nómbralo `CE - generate_lead`.
2. **Variable** (para el método) → Nuevo → "Variable de capa de datos":
   - Nombre de la variable de la capa de datos: `metodo`  · Nómbrala `dlv - metodo`.
3. **Etiqueta** → Nuevo → **"Google Analytics: evento de GA4"**:
   - Etiqueta de configuración: tu GA4 (la que ya envía datos a la propiedad 518719778).
   - Nombre del evento: `generate_lead`
   - Parámetros del evento: `method` = `{{dlv - metodo}}`
   - Activador: `CE - generate_lead`. Nómbrala `GA4 - generate_lead`.
4. **Vista previa** (Preview): abre el sitio, haz clic en un botón de WhatsApp y en uno de Llamar;
   confirma que la etiqueta `GA4 - generate_lead` se dispara y que el evento llega a GA4 → DebugView.
5. **Enviar / Publicar** el contenedor.

## Parte C — GA4 (lo haces tú en analytics.google.com, propiedad 518719778)
6. Administrar → **Eventos clave** (Key events) → **Nuevo evento clave** → nombre `generate_lead`.
   (En GA4 nuevo, las "conversiones" se llaman "eventos clave".) Listo: cada clic a WhatsApp/llamar
   se cuenta como lead. Opcional: crea uno por método si quieres separar WhatsApp vs llamadas.

---

**Verificar después:** en GA4 → Informes → Interacción → Eventos, debe aparecer `generate_lead` con
conteo > 0 tras unas horas. Y en Eventos clave, el número de leads del día.

> Nota: la sub-medición de SESIONES (GSC 363 clics vs GA4 40 sesiones) es OTRO tema (el GTM diferido
> pierde a quien rebota antes de interactuar). Eso es un trade-off con el LCP; se trata aparte.
