#!/usr/bin/env bash
# Checker DETERMINISTA de SECRETOS para plomeroculiacanpro.mx.
# Solo REPORTA (no arregla). Emite a stdout SOLO el JSON común de hallazgos:
#   {"hallazgos":[{id,archivo,linea,severidad,categoria,descripcion,fix_sugerido}], "analizadas":N}
# categoria = "secretos". Salida con ORDEN ESTABLE (se ordena antes de emitir).
#
# Tres barridos:
#  1. WORKING TREE (alta): patrones de secreto sobre los archivos versionables
#     (git ls-files + untracked NO ignorados). Un secreto aquí está a un commit de
#     filtrarse. -> exit 2 (candado: NO publicar).
#  2. GITIGNORE vs ÍNDICE (alta): ningún archivo TRACKEADO debe coincidir con un
#     patrón de secretos de .gitignore (.env, client_secret.json, gsc-token.json…).
#     git ls-files --ignored --cached. -> exit 2 (candado: NO publicar).
#  3. HISTORIAL (alta, NO bloquea): los mismos patrones sobre `git log -p`. Un
#     secreto en el historial sigue expuesto aunque ya no esté en el árbol; exige
#     ROTAR la credencial. No flipa el exit code (bloquear sería inútil: el pasado
#     es inmutable; lo accionable es revocar, no "no publicar").
#
# Usa gitleaks si está instalado (mejor cobertura); si no, regex. gitleaks se suma
# como señal extra; el regex es la línea base y siempre corre.
#
# CANDADO DE PUBLICACIÓN: exit 0 = sin secretos actuales (publicable);
# exit 2 = hay secreto en working tree o archivo de secreto trackeado (NO publicar);
# exit 1 = error del propio checker. (El JSON siempre se imprime en stdout.)
#
# PROPUESTA (no instalada): un hook pre-commit que corra este checker y aborte el
# commit si exit==2. Ver .pipeline/progreso-revisores.md (no se instala sin tu OK).
set -uo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT" || { echo '{"hallazgos":[{"id":"sec-001","archivo":".pipeline/check-secretos.sh","linea":0,"severidad":"alta","categoria":"secretos","descripcion":"verificación ciega: no se pudo acceder a la raíz del repo","fix_sugerido":"Revisar el checker"}],"analizadas":0}'; exit 1; }

SELF=".pipeline/check-secretos.sh"
TSV="$(mktemp)"            # scope \t sev \t archivo \t linea \t rule
trap 'rm -f "$TSV"' EXIT

# Reglas: nombre|ERE. client_secret/refresh_token SOLO como valor asignado
# (la palabra suelta aparece en código legítimo -> falso positivo).
RULES=(
  "openai-key|sk-[A-Za-z0-9]{20,}"
  "google-api-key|AIza[0-9A-Za-z_-]{20,}"
  "github-token|gh[opsu]_[A-Za-z0-9]{20,}"
  "private-key-block|-----BEGIN [A-Z ]*PRIVATE KEY-----[^A-Za-z0-9+/]{0,4}[A-Za-z0-9+/]{30,}"
  # Con y SIN comillas, y clave en cualquier case (el estilo .env `GOOGLE_CLIENT_SECRET=...`
  # sin comillas y en MAYÚSCULAS no matcheaba nada → secreto real pasaba en verde).
  "client-secret-value|[Cc][Ll][Ii][Ee][Nn][Tt]_[Ss][Ee][Cc][Rr][Ee][Tt][A-Z_]*[\"']?[[:space:]]*[:=][[:space:]]*[\"']?[A-Za-z0-9_-]{12,}"
  "refresh-token-value|[Rr][Ee][Ff][Rr][Ee][Ss][Hh]_[Tt][Oo][Kk][Ee][Nn][A-Z_]*[\"']?[[:space:]]*[:=][[:space:]]*[\"']?[A-Za-z0-9_/-]{12,}"
  # Formato ACTUAL de client secret de Google (el que está expuesto en R-01 usa este prefijo).
  "google-client-secret-gocspx|GOCSPX-[A-Za-z0-9_-]{16,}"
)

# --- conjunto de archivos del working tree (versionables, sin ignorados ni el propio checker)
FILES_NUL="$(mktemp)"; trap 'rm -f "$TSV" "$FILES_NUL"' EXIT
{ git ls-files -z; git ls-files -z --others --exclude-standard; } 2>/dev/null \
  | LC_ALL=C sort -z -u > "$FILES_NUL"
ANALIZADAS=$(tr -cd '\0' < "$FILES_NUL" | wc -c | tr -d ' ')
# VERIFICACIÓN CIEGA: 0 archivos barridos = git falló (errores suprimidos arriba), no un
# repo sin archivos. Sin esto el checker imprimía "sin secretos" con barrido vacío y
# NINGÚN sensor lo validaba (está excluido del contrato por ser bash).
if [ "${ANALIZADAS:-0}" -eq 0 ]; then
  printf '{"hallazgos":[{"id":"sec-000","archivo":".pipeline/check-secretos.sh","linea":0,"severidad":"alta","categoria":"secretos","descripcion":"verificación ciega: git ls-files devolvió 0 archivos — el barrido de secretos NO corrió (git roto o fuera del repo)","fix_sugerido":"Correr desde la raíz del repo con git sano; mientras tanto los secretos NO se están vigilando"}],"analizadas":0}\n'
  exit 2
fi

# --- BARRIDO 1: working tree
for rule in "${RULES[@]}"; do
  name="${rule%%|*}"; re="${rule#*|}"
  while IFS= read -r line; do
    f="${line%%:*}"; rest="${line#*:}"; ln="${rest%%:*}"
    [ "$f" = "$SELF" ] && continue
    # Excluir REFERENCIAS a archivos de secreto (no son el secreto):
    # p.ej. CLIENT_SECRET_FILE = "client_secret.json".
    case "$line" in
      *client_secret.json*|*CLIENT_SECRET_FILE*|*token.json*|*TOKEN_FILE*) continue ;;
    esac
    printf 'tree\talta\t%s\t%s\t%s\n' "$f" "$ln" "$name" >> "$TSV"
  done < <(xargs -0 grep -nIEH -e "$re" -- < "$FILES_NUL" 2>/dev/null)
done

# --- BARRIDO 2: archivos de secreto TRACKEADOS (coinciden con .gitignore)
while IFS= read -r f; do
  [ -z "$f" ] && continue
  if printf '%s\n' "$f" | grep -qiE '(secret|token|credential|(^|/)\.env)'; then
    printf 'gitignore\talta\t%s\t0\tarchivo-secreto-trackeado\n' "$f" >> "$TSV"
  fi
done < <(git ls-files --cached --ignored --exclude-standard 2>/dev/null)

# --- BARRIDO 3: historial (git log -p) — reporta, NO bloquea
HIST="$(git log -p --no-color 2>/dev/null)"
for rule in "${RULES[@]}"; do
  name="${rule%%|*}"; re="${rule#*|}"
  n="$(printf '%s' "$HIST" | grep -cIE "^\+.*$re" 2>/dev/null || true)"
  if [ "${n:-0}" -gt 0 ]; then
    printf 'history\talta\t(historial git)\t0\t%s::%s\n' "$name" "$n" >> "$TSV"
  fi
done

# --- gitleaks (si existe): señal extra
if command -v gitleaks >/dev/null 2>&1; then
  GL="$(mktemp)"
  if gitleaks detect --source "$ROOT" --no-banner --redact -f json -r "$GL" >/dev/null 2>&1; then :; fi
  if [ -s "$GL" ]; then
    python3 - "$GL" "$TSV" <<'PY' 2>/dev/null || true
import json,sys
gl,tsv=sys.argv[1],sys.argv[2]
try: data=json.load(open(gl))
except Exception: data=[]
with open(tsv,"a") as o:
    for d in data if isinstance(data,list) else []:
        f=d.get("File","(gitleaks)"); ln=d.get("StartLine",0); rid=d.get("RuleID","gitleaks")
        o.write(f"tree\talta\t{f}\t{ln}\tgitleaks:{rid}\n")
PY
  fi
  rm -f "$GL"
fi

# --- emitir JSON común (ordenado -> determinista) y fijar exit code
LC_ALL=C sort -u "$TSV" -o "$TSV"
BLOCK=$(grep -cE '^(tree|gitignore)' "$TSV" 2>/dev/null) || true
BLOCK=${BLOCK:-0}

python3 - "$TSV" "$ANALIZADAS" <<'PY'
import json,sys
tsv,analizadas=sys.argv[1],int(sys.argv[2])
rows=[]
try:
    for raw in open(tsv,encoding="utf-8"):
        raw=raw.rstrip("\n")
        if not raw: continue
        parts=raw.split("\t")
        if len(parts)<5: continue
        rows.append(parts[:5])
except FileNotFoundError:
    pass
rows.sort(key=lambda r:(r[0],r[2],r[4],r[3]))
hall=[]
for i,(scope,sev,arch,ln,rule) in enumerate(rows,1):
    try: linea=int(ln)
    except ValueError: linea=0
    if scope=="tree":
        desc=f"SECRETO: posible {rule} en un archivo versionable del working tree (línea {linea}); un secreto aquí está a un commit de filtrarse"
        fix="Quitar el secreto del archivo y ROTARLO (asúmelo comprometido); moverlo a variable de entorno o archivo gitignored. CANDADO: no publicar hasta resolverlo"
    elif scope=="gitignore":
        desc=f"SECRETO: el archivo '{arch}' está TRACKEADO pese a coincidir con un patrón de secretos de .gitignore; no debe versionarse"
        fix=f"git rm --cached '{arch}', confirmar que .gitignore lo cubre y ROTAR el secreto. CANDADO: no publicar hasta resolverlo"
    else:  # history
        name,_,cnt=rule.partition("::")
        desc=f"SECRETO EN HISTORIAL: el patrón {name} aparece en {cnt} línea(s) añadida(s) del historial (git log -p); sigue expuesto aunque ya no esté en el árbol actual"
        fix="ROTAR/REVOCAR la credencial YA; opcionalmente purgar el historial (git filter-repo). No bloquea la publicación (el pasado es inmutable), pero exige rotación humana"
    hall.append({"id":"sec-%03d"%i,"archivo":arch,"linea":linea,"severidad":sev,
                 "categoria":"secretos","descripcion":desc,"fix_sugerido":fix})
print(json.dumps({"hallazgos":hall,"analizadas":analizadas},ensure_ascii=False,indent=2))
PY

[ "${BLOCK:-0}" -gt 0 ] && exit 2
exit 0
