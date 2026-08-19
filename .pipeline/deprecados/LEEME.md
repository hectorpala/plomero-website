# Deprecados (archivados 2026-07-07, auditoría del auto-agente)

- **mantener-diario.sh** + **com.plomeroculiacan.mantener.plist** — reemplazados por
  `crecer-diario.sh` (que incluye el mantenimiento) desde jun-2026. Se archivan porque
  eran un footgun: el script tomaba el lock compartido SIN escribir `pid`, así que
  cualquier otro driver lo trataba como huérfano y se lo robaba mientras seguía vivo;
  además su plist compartía el horario 18:25.
  El LaunchAgent `com.plomeroculiacan.mantener` NO está instalado (verificado 2026-07-07).
  Desde 2026-08-17, ejecutar por accidente el script archivado solo delega al driver
  vigente de Codex; ya no contiene una ruta alternativa ni una llamada a otro proveedor.
