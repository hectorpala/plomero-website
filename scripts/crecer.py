#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""crecer.py — ORQUESTADOR de crecimiento del sitio (un solo punto de entrada).

Une todas las herramientas en un flujo automatizado y agrega el "plomería" que
antes se hacía a mano: sitemap, enlace entrante, bump del service worker,
publicar (rama+merge+push) y stats.

  python3 scripts/crecer.py estado                 # dashboard del sitio
  python3 scripts/crecer.py servicio spec.json     # crear servicio + sitemap + enlace + sw + gate
  python3 scripts/crecer.py colonia  spec.json     # promover colonia + sitemap + gate
  python3 scripts/crecer.py gate <ruta/index.html> # candado (atajo)
  python3 scripts/crecer.py publicar "mensaje"     # rama + commit + merge --no-ff + push (auto-indexa)

Specs: `python3 scripts/crear-servicio.py --ejemplo`  /  `diferenciar-colonia.py --ejemplo`
Quedan SOLO la auditoría con datos GSC y la indexación por MCP en el skill /expandir-sitio
(necesitan el MCP). Todo lo demás (determinista) lo hace este CLI.
"""
import json, os, re, subprocess, sys, datetime, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://plomeroculiacanpro.mx"
# El sitemap.xml raíz es un sitemapindex; las URLs de páginas viven en el hijo:
SITEMAP_CHILD = "sitemaps/main_sitemap.xml"
COLONIAS_DIR = "servicios/plomero-colonias-culiacan"
PY = sys.executable


def sh(cmd, **kw):
    # errors="replace": el pre-push hook puede emitir bytes no-utf8 (emoji/acentos de la
    # auto-indexación); sin esto, decodificar la salida revienta y aborta `publicar` (infra-004).
    kw.setdefault("errors", "replace")
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, **kw)


def _read(p): return open(os.path.join(ROOT, p), encoding="utf-8").read()
def _write(p, h): open(os.path.join(ROOT, p), "w", encoding="utf-8").write(h)


def _snapshot(paths):
    """Guarda los bytes EXACTOS de archivos existentes para poder revertir (atomicidad)."""
    return {p: _read(p) for p in paths if os.path.isfile(os.path.join(ROOT, p))}


def _restore(snap):
    for p, h in snap.items():
        _write(p, h)


_SLUG_RE = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")


def _valid_slug(slug):
    """Un slug seguro: solo minúsculas/números/guiones, ≤80 car. Bloquea vacío, '/', '..'."""
    return isinstance(slug, str) and 0 < len(slug) <= 80 and bool(_SLUG_RE.match(slug))


def _rm_page_dir(parent_rel, slug):
    """Borra <parent_rel>/<slug>/ SOLO si el slug es válido y la ruta queda DENTRO de
    parent_rel (defensa en profundidad contra rm -rf de rutas computadas)."""
    if not _valid_slug(slug):
        print("  ⚠️ rollback: slug inválido %r — NO borro nada por seguridad." % slug); return
    base = os.path.realpath(os.path.join(ROOT, parent_rel))
    target = os.path.realpath(os.path.join(base, slug))
    if target != os.path.join(base, slug) or not target.startswith(base + os.sep):
        print("  ⚠️ rollback: ruta fuera de %s — NO borro nada." % parent_rel); return
    if os.path.isdir(target):
        sh(["rm", "-rf", target])


# ───────────────────────── herramientas de "plomería" ─────────────────────────
def sitemap_add(loc, priority):
    sm = _read(SITEMAP_CHILD)
    if loc in sm:
        print("  • sitemap: ya estaba"); return
    today = datetime.date.today().isoformat()
    entry = '  <url><loc>%s</loc><lastmod>%s</lastmod><changefreq>monthly</changefreq><priority>%s</priority></url>\n' % (loc, today, priority)
    _write(SITEMAP_CHILD, sm.replace("</urlset>", entry + "</urlset>", 1))
    print("  • sitemap: +1 (%s)" % loc)


def home_link_add(slug, label):
    """Añade <li><a> a la lista de servicios de la home (justo antes de la sección
    social-proof). Devuelve True si la página quedó enlazada (o ya lo estaba); False si
    NO se pudo enlazar — en ese caso la página sería HUÉRFANA y la operación debe FALLAR
    (no dejar páginas sin enlaces entrantes en una corrida autónoma)."""
    h = _read("index.html")
    href = "/servicios/%s/" % slug
    if href in h:
        print("  • enlace home: ya estaba"); return True
    anchor = '</a></li></ul></div></section><section class="social-proof">'
    if anchor not in h:
        print("  ❌ enlace home: no encontré la lista de servicios — la página quedaría HUÉRFANA")
        return False
    li = '</a></li><li><a href="%s">%s</a></li></ul></div></section><section class="social-proof">' % (href, label)
    _write("index.html", h.replace(anchor, li, 1))
    print("  • enlace home: +1 (%s)" % label)
    return True


def sw_bump():
    """Sube el número de versión de CACHE_NAME del service worker. Devuelve True si lo
    logró; False si no encontró el patrón (no publicar sin bump → CSS viejo cacheado)."""
    sw = _read("sw.js")
    m = re.search(r"const CACHE_NAME = 'plomero-culiacan-v(\d+)';", sw)
    if not m:
        print("  ❌ sw: no encontré CACHE_NAME — NO puedo versionar el cache (no publicar así)")
        return False
    n = int(m.group(1)); new = "plomero-culiacan-v%d" % (n + 1)
    _write("sw.js", sw.replace(m.group(0), "const CACHE_NAME = '%s';" % new, 1))
    print("  • sw: v%s -> v%d" % (m.group(1), n + 1))
    return True


def gate(paths):
    r = sh([PY, ".pipeline/gate-pagina.py"] + paths)
    print(r.stdout.rstrip())
    return r.returncode == 0


# ───────────────────────── subcomandos ─────────────────────────
def cmd_estado(_):
    serv = [d for d in glob.glob(os.path.join(ROOT, "servicios/*/")) if "colonias" not in d]
    coldir = os.path.join(ROOT, COLONIAS_DIR)
    cols = glob.glob(os.path.join(coldir, "*/index.html"))
    idx = sum(1 for c in cols if "noindex" not in open(c, encoding="utf-8").read())
    blogs = glob.glob(os.path.join(ROOT, "blog/*/index.html"))
    sm = _read(SITEMAP_CHILD).count("<url>") if os.path.isfile(os.path.join(ROOT, SITEMAP_CHILD)) else 0
    last = sh(["git", "log", "--oneline", "-1"]).stdout.strip()
    swm = re.search(r"plomero-culiacan-v\d+", _read('sw.js'))
    print("══════ ESTADO DEL SITIO ══════")
    print("  Servicios (páginas):     %d" % len(serv))
    print("  Colonias:                %d total · %d indexables · %d noindex" % (len(cols), idx, len(cols) - idx))
    print("  Blog (posts):            %d" % len(blogs))
    print("  URLs en %s: %d" % (SITEMAP_CHILD, sm))
    print("  Service worker:          %s" % (swm.group(0) if swm else "?"))
    print("  Último commit:           %s" % last)
    print("\n  Candados:")
    cg = sh([PY, ".pipeline/ci-gate.py"])
    for ln in cg.stdout.strip().splitlines():
        if "▶" in ln or "Gate" in ln: print("   ", ln.strip())


def cmd_servicio(args):
    spec = args[0]
    z = json.load(open(spec, encoding="utf-8"))
    slug = z["slug"]
    if not _valid_slug(slug):
        sys.exit("❌ slug inválido: %r (solo minúsculas, números y guiones; nada de '/', '..' ni vacío)" % slug)
    page = "servicios/%s/index.html" % slug
    print("── crear-servicio: %s ──" % slug)
    r = sh([PY, "scripts/crear-servicio.py", spec])
    print(r.stdout.rstrip())
    if r.returncode != 0:
        sys.exit("❌ falló crear-servicio (no se cableó ni tocó nada).")
    # Snapshot de los archivos rastreados que vamos a mutar -> rollback atómico.
    snap = _snapshot([SITEMAP_CHILD, "index.html", "sw.js"])
    print("── wiring automático ──")
    sitemap_add("%s/servicios/%s/" % (SITE, slug), "0.8")
    linked = home_link_add(slug, z.get("bc", slug))
    bumped = sw_bump()
    print("── candado ──")
    ok = gate([page]) and linked and bumped
    if not ok:
        print("\n↩️  FALLÓ el candado o el enlace en home — revirtiendo para dejar el árbol LIMPIO…")
        _restore(snap)
        _rm_page_dir("servicios", slug)
        print("   revertido: %s, index.html, sw.js · eliminada servicios/%s/" % (SITEMAP_CHILD, slug))
        print("❌ NO se publica. Corrige el spec (%s) y reintenta. Motivo arriba." % spec)
        sys.exit(1)
    print("\n✅ LISTO. Revisa, luego:  python3 scripts/crecer.py publicar \"feat: %s\"" % slug)


def cmd_colonia(args):
    spec = args[0]
    z = json.load(open(spec, encoding="utf-8"))
    slug = z["slug"]
    if not _valid_slug(slug):
        sys.exit("❌ slug inválido: %r (solo minúsculas, números y guiones)" % slug)
    page = "%s/%s/index.html" % (COLONIAS_DIR, slug)
    # La colonia YA existe (noindex) y diferenciar-colonia la edita en sitio.
    # Snapshot ANTES de editar para poder restaurarla (NO borrarla) si algo falla.
    snap = _snapshot([page, SITEMAP_CHILD])
    print("── diferenciar-colonia: %s ──" % slug)
    r = sh([PY, "scripts/diferenciar-colonia.py", spec])
    print(r.stdout.rstrip())
    if r.returncode != 0:
        _restore(snap)
        sys.exit("❌ falló diferenciar-colonia (revertido; la colonia quedó como estaba).")
    print("── wiring automático ──")
    sitemap_add("%s/%s/%s/" % (SITE, COLONIAS_DIR, slug), "0.6")
    print("── candado ──")
    ok = gate([page])
    if not ok:
        print("\n↩️  FALLÓ el candado — revirtiendo (la colonia vuelve a noindex como estaba)…")
        _restore(snap)
        print("   revertido: %s + %s" % (page, SITEMAP_CHILD))
        print("❌ NO se publica. Hazla más única en el spec y reintenta.")
        sys.exit(1)
    print("\n✅ LISTO. Revisa, luego: publicar")


def cmd_gate(args):
    sys.exit(0 if gate(list(args)) else 1)


def cmd_publicar(args):
    if not args:
        sys.exit("uso: crecer.py publicar \"mensaje del commit\"")
    msg = args[0]
    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    branch = "auto/crecer-%s" % stamp
    st = sh(["git", "status", "--short"]).stdout.strip()
    if not st:
        sys.exit("nada que publicar (working tree limpio)")
    print("Cambios:\n" + st)
    # Purga ramas auto/* YA fusionadas (git branch -d solo borra las mergeadas; las no
    # fusionadas se conservan porque tienen trabajo pendiente de revisión humana).
    for b in sh(["git", "branch", "--merged", "main"]).stdout.splitlines():
        b = b.strip().lstrip("*").strip()
        if b.startswith("auto/"):
            sh(["git", "branch", "-d", b])
    cob = sh(["git", "checkout", "-b", branch])
    if cob.returncode != 0:
        print("❌ no pude crear la rama %s (%s). Aborté sin commitear." % (branch, (cob.stderr or "").strip()[:80]))
        sys.exit(1)
    sh(["git", "add", "-A"])
    full = msg + "\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <noreply@anthropic.com>"
    c = sh(["git", "commit", "-m", full])
    print(c.stdout.rstrip() + c.stderr.rstrip())
    if "BLOQUEADO" in (c.stdout + c.stderr) or c.returncode != 0:
        print("❌ commit bloqueado por el hook — revisa; quedó en la rama %s" % branch); sys.exit(1)

    env = dict(os.environ); env["PATH"] = "/usr/local/bin:" + env.get("PATH", "")

    def git(*a):
        # errors="replace": `git push` arrastra la salida del pre-push hook (auto-indexación),
        # que puede traer bytes no-utf8; sin esto, decodificar revienta y aborta el push (infra-004).
        return subprocess.run(["git", *a], cwd=ROOT, text=True, capture_output=True, env=env,
                              errors="replace")

    # Publicación SEGURA: sincroniza con el remoto antes de mergear; NUNCA --force.
    sh(["git", "checkout", "main"])
    git("fetch", "origin")
    ff = git("merge", "--ff-only", "origin/main")
    if ff.returncode != 0:
        print("❌ publicación detenida: la main local divergió de origin/main.")
        print("   La rama %s queda SIN fusionar para revisión humana. (No se forzó nada.)" % branch)
        sys.exit(1)
    mg = git("merge", "--no-ff", branch, "-m", "Merge: " + msg)
    if mg.returncode != 0:
        git("merge", "--abort")
        print("❌ publicación detenida: el merge tuvo CONFLICTOS (rama y main tocaron lo mismo).")
        print("   Aborté el merge; la rama %s queda intacta para revisión humana. (No se pusheó nada.)" % branch)
        sys.exit(1)
    p = git("push", "origin", "main")
    out = (p.stdout + p.stderr).strip()
    print(out[-600:])
    if p.returncode != 0:
        # Reintegra UNA sola vez y reintenta; si vuelve a fallar, ABORTA (sin force).
        print("↻ push rechazado — reintegro con el remoto y reintento UNA vez (sin rebase ni force)…")
        git("fetch", "origin")
        rs = git("reset", "--hard", "origin/main")
        mg2 = git("merge", "--no-ff", branch, "-m", "Merge: " + msg)
        if rs.returncode != 0 or mg2.returncode != 0:
            git("merge", "--abort")
            print("❌ publicación detenida: no pude reintegrar limpio. Rama %s sin publicar; revísalo a mano." % branch)
            sys.exit(1)
        p2 = git("push", "origin", "main")
        print((p2.stdout + p2.stderr).strip()[-600:])
        if p2.returncode != 0:
            print("❌ publicación detenida: push rechazado tras el reintento. Rama %s sin publicar." % branch)
            sys.exit(1)
    sh(["git", "branch", "-d", branch])
    print("\n✅ Publicado. (El pre-push ya encoló la indexación en GSC.)")
    print("   Refuerza la indexación por MCP desde /expandir-sitio si quieres acelerar.")


CMDS = {"estado": cmd_estado, "servicio": cmd_servicio, "colonia": cmd_colonia,
        "gate": cmd_gate, "publicar": cmd_publicar}


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help") or sys.argv[1] not in CMDS:
        print(__doc__); sys.exit(0 if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help") else 1)
    CMDS[sys.argv[1]](sys.argv[2:])


if __name__ == "__main__":
    main()
