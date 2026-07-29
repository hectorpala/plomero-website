# Meta-pase del Crítico-Sistema — 2026-07-29

Dejé **2 propuestas nuevas**, con su DRAFT ya escrito y verificado en vivo contra el repo real, arriba de
`docs/PROPUESTAS.md` (quedan **15 pendientes en total**, sumando las de pases anteriores — ninguna de las
11 previas se resolvió sola en estos 5 días, siguen esperando tu aprobación). Yo no apliqué nada — tú
apruebas.

## Top 3 por impacto

1. **(A, nueva) La rama con el trabajo de los últimos 3 días está bloqueada por el cap de 18 páginas y
   TÚ NO LO VES en ningún lado — ni yo lo vi en el brief, tuve que ir a buscarlo a mano.** Desde el
   2026-07-26, `auto/diario-20260726-1826` acumula 48 páginas con cambio real (CLS de logo en 24
   colonias, FAQPage-vs-visible, reconciliación de precios, testimonios, hub de colonias reescrito) y el
   verificador FASE 7 YA CONFIRMÓ `ok=true` — 0 ALTA, 0 electricista/GTM ajeno, 0 enlaces rotos. Lo único
   que falta es que decidas `CAP_OK=1` o pidas recortar el lote. El problema de fondo: `recolecta-señales.py`
   (mi propia materia prima) no mira `git branch` — así que ni yo ni tú nos enteramos de esto leyendo el
   brief, solo grepeando `HISTORIAL.jsonl` línea por línea. El draft agrega una sección al brief que lista
   toda rama `auto/*` sin publicar con su edad y marca ⚠️ATASCADA a los 2 días — ya la probé en vivo y
   detecta el bloqueo correctamente.
2. **(M, nueva, relacionada) Ese mismo bloqueo ya dejó DOS ramas con el mismo trabajo, una vieja y una
   nueva, y es fácil publicar la vieja por error.** `scripts/crecer.py publicar` crea una rama
   `auto/crecer-*` nueva CADA VEZ que se llama, aunque ya estés parado en una rama `auto/diario-*`.
   Verifiqué que `auto/crecer-20260727-183544` (del intento de publicar del 07-27) le faltan 4 commits
   del 07-28, incluido el fix de `docs/ESTADO.md` — si algún día haces `CAP_OK=1` sobre la rama
   equivocada, publicarías contenido viejo sin darte cuenta. El draft hace que reuse la rama actual en
   vez de crear otra.
3. **(A, de pases anteriores, sigue sin merge) La clase de bug de enlaces a redirect-stubs sigue viva
   HOY** (propuesta de más arriba en el archivo, verificada de nuevo indirectamente: sigue apareciendo en
   `HISTORIAL.jsonl` el 2026-07-26 un caso nuevo — `seo-enlace-redirect-stub-cuanto-cuesta-bano-20260726`
   — exactamente la clase que el draft pendiente ya cierra). Cada semana que pasa sin merge es una
   página nueva que puede reincidir en lo mismo.

**Cómo lo verifiqué:** corrí `.pipeline/recolecta-señales.py` (297 entradas de historial, 38 corridas de
costo, 14 tareas de backlog, REGLAS.md 13 tokens sobre presupuesto — marginal, ya se marca solo). El brief
no mencionó el bloqueo de 3 días, así que leí `data/HISTORIAL.jsonl` desde 2026-07-24 a mano y encontré
`sistema-cap-18-excedido-48-paginas-no-publicado-20260727/28`. Confirmé en vivo con `git branch
--no-merged main` y `git log main..<rama> --format=%ai` que la rama lleva 3 días sin fusionar. Confirmé
con `git merge-base --is-ancestor` que la segunda rama (`auto/crecer-*`) es un ANCESTRO obsoleto de la
primera. Probé el draft de `sec_ramas_atascadas()` ejecutándolo de verdad contra este repo — imprime
ambas ramas atascadas con su edad correcta. Revisé `data/BACKLOG.jsonl`: solo 1 tarea fuera de
`hecho`/`descartado` (la doorway `plomero-a-domicilio` vs `plomero-cerca-de-mi`, ahora 40 días esperando
decisión — ya hay un draft pendiente de un pase anterior para mostrar su edad en el brief).

**Estado del sistema:** el hueco nuevo real de hoy es que el propio sistema de vigilancia (mi brief) no
mira el estado de git, así que un bloqueo de 3 días con trabajo YA verificado puede quedar invisible
indefinidamente. Todo lo demás sigue siendo la misma cola de 11 propuestas anteriores esperando tu
decisión — ninguna se aplicó sola porque el sistema está diseñado para que nada se aplique sin ti.
