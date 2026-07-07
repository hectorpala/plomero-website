#!/usr/bin/env python3
"""fix-colonia-eta.py — sana 2 defectos sistémicos de la diferenciación de colonias:
 (1) hero-eta-badge con ETA que CONTRADICE el cuerpo (meta+benefit-h3+cobertura, 3 fuentes).
     Solo corrige el badge cuando las 3 fuentes del cuerpo COINCIDEN y el badge difiere (deriva, no inventa).
 (2) meta description (y og:description) truncada a mitad de palabra antes de ' · Llegada' -> recorta
     el fragmento colgante al ultimo borde de clausula completo (no inventa texto).
Uso: python3 .pipeline/fix-colonia-eta.py [--apply]   (sin --apply = dry-run)
infra:utilidad-no-sensor (no es checker de pagina; corre con args)"""
import re, glob, os, sys, html
APPLY = "--apply" in sys.argv
# ROOT absoluto: el glob relativo dependía del cwd — corrido desde otro directorio daba
# "0 colonias" con exit 0 (éxito falso, clase infra-006/007).
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
changed=[]
_files = sorted(glob.glob(os.path.join(ROOT, "servicios/plomero-colonias-culiacan/*/index.html")))
if not _files:
    print("❌ 0 colonias encontradas bajo %s — ruta rota, no un sitio sin colonias." % ROOT)
    sys.exit(1)
for f in _files:
    c=os.path.basename(os.path.dirname(f))
    h=open(f,encoding="utf-8").read(); orig=h
    def g(pat,s):
        x=re.search(pat,s); return x.group(1) if x else None
    meta_eta = g(r'<meta name="description" content="[^"]*?([0-9]{2}-[0-9]{2}) min',h)
    badge_full = re.search(r'(hero-eta-badge[^>]*>(?:<[^>]+>)*\s*<span>Llegamos en )([0-9]{2}-[0-9]{2})( min a [^<]+</span>)',h)
    benefit = g(r'<h3>Llegada (?:en|R[aá]pida)[^<]*?([0-9]{2}-[0-9]{2}) min',h) or g(r'Llegada R[aá]pida</h3><p>([0-9]{2}-[0-9]{2}) min',h)
    cob = g(r'Cobertura.*?Llegamos en ([0-9]{2}-[0-9]{2}) min',h)
    notes=[]
    # (1) badge fix — solo si las 3 fuentes del cuerpo existen, coinciden, y el badge difiere
    body=[v for v in (meta_eta,benefit,cob) if v]
    if badge_full and len(body)==3 and len(set(body))==1 and badge_full.group(2)!=body[0]:
        target=body[0]
        h=h[:badge_full.start()] + badge_full.group(1)+target+badge_full.group(3) + h[badge_full.end():]
        notes.append("badge %s->%s"%(badge_full.group(2),target))
    # (2) meta/og description truncada
    def fix_desc(m):
        d=m.group(2)
        parts=d.split(' · Llegada')
        if len(parts)<2: return m.group(0)
        head=parts[0]; rest=' · Llegada'+parts[1]
        # ¿la 1a parte termina en fragmento (<=3 letras minus, o coma)?
        toks=head.rstrip().split(' ')
        last=toks[-1] if toks else ''
        if re.fullmatch(r'[a-záéíóúñ]{1,3},?',last) or head.rstrip().endswith(','):
            # recorta al ultimo ' · ' (clausula completa) o quita la ultima clausula tras la ultima coma
            if ' · ' in head:
                segs=head.split(' · ')
                # quita el ultimo segmento (la clausula truncada) si tiene una coma interna o frag
                lastseg=segs[-1]
                if ',' in lastseg:
                    lastseg=lastseg.rsplit(',',1)[0].rstrip()  # corta la sub-clausula truncada
                    segs[-1]=lastseg
                else:
                    segs=segs[:-1]
                head=' · '.join(segs).rstrip(' ,·')
            new=m.group(1)+head+rest+m.group(3)
            notes.append("meta-trim")
            return new
        return m.group(0)
    h=re.sub(r'(<meta name="description" content=")([^"]*)(">)',fix_desc,h,count=1)
    h=re.sub(r'(<meta property="og:description" content=")([^"]*)(">)',fix_desc,h,count=1)
    if h!=orig:
        changed.append((c,"; ".join(sorted(set(notes)))))
        if APPLY: open(f,"w",encoding="utf-8").write(h)
print(("APLICADO" if APPLY else "DRY-RUN")+" — %d colonias"%len(changed))
for c,n in changed: print("  %-22s %s"%(c,n))
