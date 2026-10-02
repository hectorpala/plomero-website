---
name: checa-pagina
description: Reporte completo de cómo va plomeroculiacanpro.mx (Google Search Console + Analytics + contactos de WhatsApp/llamada/formulario + comportamiento + velocidad real + salud técnica) en formato fijo para Héctor. Usar cuando diga "chécame la página", "cómo va la página", "cómo va el plomero", "dame el reporte" o /checa-pagina. Solo lectura.
---

# Reporte "chécame la página cómo va"

Solo lectura: este reporte **no edita nada** del sitio. Si encuentras algo que arreglar, lo
recomiendas al final y esperas a que Héctor diga que sí.

Periodo por defecto: **últimos 28 días** comparado con los 28 anteriores. Si Héctor dice
"esta semana" usa 7, "este mes" usa 30, "hoy" usa 1.

## 1. Juntar los datos (todo en paralelo)

**Google Search Console** (`mcp__gsc__*`, site `plomeroculiacanpro.mx`):
- `gsc_performance` (periodo) → clics, impresiones, CTR, posición, cambio vs anterior.
- `gsc_keywords` orderBy clicks, limit 15 · y orderBy impressions, limit 15.
- `gsc_opportunities` → casi top 3, página 2, top 10 con 0 clics.
- `gsc_sitemaps` → errores.
- `gsc_inspect` → `/`, `/precios/`, `/servicios/destape-de-drenajes/`,
  `/blog/desatascar-wc-metodos-profesionales/`, `/servicios/plomero-cerca-de-mi/`.
- Búsquedas de dinero a seguir siempre: `plomero culiacan`, `plomeros culiacan`,
  `plomero cerca de mi`, `plomeros a domicilio culiacán`, `plomero` (sácalas de gsc_keywords;
  si no salen en el top, dilo).

**Analytics** (propiedad buena **503992062**, `G-NSV2K9N2ZD`) — pasa SIEMPRE `dominio: "plomeroculiacanpro.mx"`
en `ga4_report` y `ga4_eventos`: hasta el 1-oct-2026 el sitio de Mazatlán mandaba sus visitas a esta
misma propiedad (usaba el contenedor GTM-W75CRTX5).
- `ga4_report` con dimension `sessionDefaultChannelGroup`, `pagePath`, `deviceCategory`,
  `country`, `sessionSource`.
- `ga4_eventos`:
  - `generate_lead` × [`metodo`] · [`ubicacion`] · [`pagina`] · [`dia_semana`, `hora`] ·
    [`fuente`] · [`dispositivo`] · [`ciudad`]
  - `faq_open` × [`pregunta`]
  - `web_vital` × [`metrica`, `rating`] · [`metrica`, `dispositivo`]
  - `scroll_depth` × [`pagina`, `profundidad`]
  - `internal_link_click` × [`pagina`, `enlace`]
  - `evento: "todos"` (para exit_intent_*, page_time_milestone, nav_click)
  - Si `ga4_eventos` no existe en la sesión: el servidor gsc es viejo → pide a Héctor
    `/mcp` → reconectar **gsc** y sigue con lo demás.

**Salud técnica** (en `~/Sitios Web/Plomero Culiacán`):
- `python3 .pipeline/check-plantilla.py`, `check-contenido.py`, `check-linking.py`,
  `check-indexabilidad.py` → cuenta hallazgos (ignora `estudio/`).
- `node .pipeline/check-tracking.mjs` → ¿llega la visita a Analytics en las páginas clave?
- `node .pipeline/check-e2e.mjs` → ¿funciona el formulario?
- `curl` a las URLs de los sitemaps → todas 200.

**Reporte anterior**: el más reciente de `reportes-privados/` para comparar.

## 2. Reglas para leer los datos (no te equivoques)

- **Visitas desde Google = clics de Search Console.** Es el número oficial. Analytics subcontó
  ~1 de cada 15 visitas hasta el **1-oct-2026** (cargador de GTM roto, ya arreglado): no
  compares Analytics de antes de esa fecha contra después como si fuera crecimiento.
- **Robots**: visitas "directas" de computadora con 0–3 s y de países fuera de México
  (India, China, Holanda, EE. UU.…) son robots. Repórtalas aparte y **no** las cuentes como
  personas.
- **Contactos**: los eventos `generate_lead`, `faq_open`, `web_vital`, `ubicacion`, etc.
  existen **desde el 1-oct-2026** (no hay historia antes). Analytics tarda 24–48 h.
- Un clic a WhatsApp **no es** un mensaje enviado. Dilo así: "clics a WhatsApp".
- **Tasa de contacto** = contactos ÷ visitas reales de personas (Search Console o Analytics sin
  robots, di cuál usaste).
- `valor` de web_vital: LCP e INP en milisegundos, CLS sin unidad. Bueno: LCP ≤ 2500,
  INP ≤ 200, CLS ≤ 0.1.
- Pocos datos (< 30 visitas o < 5 contactos) → dilo: "todavía poco volumen para concluir".
- **No inventes**: si un dato no salió, escribe "sin datos" y por qué.
- Microsoft Clarity (grabaciones/mapas de calor) **no** está conectado: recuérdale que lo vea
  en clarity.microsoft.com si quiere ver grabaciones.

## 3. Formato de salida (exactamente así, en español, sin jerga)

```
# 🔧 Plomero Culiacán Pro — Cómo va la página
Periodo: <fecha inicio> – <fecha fin> (vs <periodo anterior>)

## En 5 líneas
🟢/🟡/🔴 Visitas desde Google: <n> (<±%>)
🟢/🟡/🔴 Contactos: <n> (<x> WhatsApp · <y> llamadas · <z> formularios)
🟢/🟡/🔴 "plomero culiacan": posición <n> (<antes>)
🟢/🟡/🔴 Velocidad en celular: <bueno/mejorable/malo>
🟢/🟡/🔴 Salud del sitio: <n> problemas

## 1. Cómo te encuentran en Google
| | Este periodo | Anterior | Cambio |  (clics, impresiones, % de clic, posición)
Búsquedas que más te traen (tabla: búsqueda · clics · posición)
Búsquedas de dinero (tabla fija: plomero culiacan, plomeros culiacan, plomero cerca de mi,
  plomeros a domicilio culiacán, plomero)
Oportunidades: 3 búsquedas casi en top 3 o en página 2, con qué página

## 2. Quién visitó la página
Personas reales vs robots · de dónde llegaron (Google, directo, ChatGPT, ficha de Google,
  Facebook) · celular vs computadora · ciudades · se quedaron (%) y tiempo promedio ·
  páginas más vistas (tabla)

## 3. Contactos (WhatsApp, llamada, formulario)
Total y tasa de contacto
Por medio (tabla) · por botón (flotante/portada/artículo/menú/pie) · por página (top 5) ·
  por día y hora (cuándo escribe más la gente) · por fuente · por dispositivo

## 4. Qué hace la gente en la página
Hasta dónde leen (25/50/75/90 % por página) · preguntas frecuentes más abiertas ·
  del blog pasan a servicios (clics internos) · ventana de salida (vista/cerrada/contactó)

## 5. Velocidad real
| Métrica | Promedio | % bueno | Celular | Computadora |  (LCP, CLS, INP)

## 6. Salud técnica
Revisores · Analytics recibe visitas · formulario funciona · páginas caídas · sitemaps ·
  indexación de páginas clave

## 7. Comparado con el reporte anterior (<fecha>)
3–5 cambios importantes (subió/bajó y por qué)

## 8. Lo que yo haría (máx. 3, con el dato que lo justifica)

## 9. Pendientes tuyos
(ficha de Google, marcar generate_lead como evento clave, etc. — solo los que sigan abiertos)
```

Semáforo: 🟢 mejoró o está bien · 🟡 igual o poco volumen · 🔴 empeoró o está mal.

## 4. Guardar

Guarda el reporte tal cual en `reportes-privados/AAAA-MM-DD.md` (carpeta ignorada por git: el
repo es **público**, los números del negocio no se suben). Si ya existe uno de hoy, agrégale
la hora al nombre.

## Pendientes conocidos (actualiza esta lista cuando se cierren)
- Ficha de Google: no existe (kit en `docs/FICHA-GOOGLE.md`).
- `generate_lead` como evento clave en GA4: marcarlo con la estrella cuando aparezca en
  Administrar → Eventos → Eventos recientes.
- Medir el CTR del blog `/blog/desatascar-wc-metodos-profesionales/` (título nuevo 1-oct-2026;
  antes 0.7 % en "como destapar un baño").
