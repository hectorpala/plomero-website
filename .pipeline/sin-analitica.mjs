// sin-analitica.mjs — que los checkers que abren PRODUCCIÓN en Chrome NO cuenten como visitas.
//
// Por qué: check-produccion/visual/perf/e2e cargan https://plomeroculiacanpro.mx con GTM vivo y
// GA4 los registraba como gente real (2-oct-2026: 11 sesiones "Querétaro / desktop / directo",
// una por página revisada, = el doble del tráfico real de ese día). check-e2e además toca los
// botones de WhatsApp → podía meter generate_lead falsos.
//
// Cómo: dominio CDP Fetch con patrones SOLO de analítica; Chrome detiene esas peticiones y se
// responden vacías (200 sin cuerpo) antes de salir. No usa setRequestInterception de puppeteer,
// así que no desactiva la caché (check-perf mide igual) ni genera console.error
// ERR_BLOCKED_BY_CLIENT (check-produccion lo reportaría como hallazgo).
//
//   await sinAnalitica(page)                     → GTM, GA4 y Clarity ni siquiera cargan
//   await sinAnalitica(page, { soloEnvios: true }) → GTM/gtag cargan y "disparan" (check-tracking
//                                                    necesita verlos), pero el envío /collect
//                                                    nunca llega a Google

const TODO = [
  "*googletagmanager.com/*",
  "*google-analytics.com/*",
  "*analytics.google.com/*",
  "*clarity.ms/*",
  "*doubleclick.net/*",
];
const ENVIOS = [
  "*google-analytics.com/*collect*",
  "*analytics.google.com/*collect*",
  "*clarity.ms/collect*",
  "*doubleclick.net/*",
];

export async function sinAnalitica(page, { soloEnvios = false } = {}) {
  try {
    const cdp = await page.target().createCDPSession();
    cdp.on("Fetch.requestPaused", ({ requestId }) => {
      cdp.send("Fetch.fulfillRequest", {
        requestId,
        responseCode: 200,
        responseHeaders: [{ name: "Content-Type", value: "application/javascript" }],
        body: "",
      }).catch(() => {});
    });
    await cdp.send("Fetch.enable", {
      patterns: (soloEnvios ? ENVIOS : TODO).map((urlPattern) => ({ urlPattern })),
    });
  } catch (_) {
    // Sin CDP no se bloquea, pero el checker sigue: medir importa más que no ensuciar GA4.
  }
}
