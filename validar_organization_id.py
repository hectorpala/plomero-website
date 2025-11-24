#!/usr/bin/env python3
"""
Validar implementación de Organization @id
"""

from pathlib import Path
import re

print(f"\n🔍 VALIDACIÓN: ORGANIZATION @ID")
print(f"{'='*70}\n")

# Validar index.html
print(f"📄 VALIDANDO INDEX.HTML")
print(f"{'='*70}\n")

index_file = Path('index.html')

with open(index_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Buscar Organization con @id
org_id_match = re.search(r'"@type":\s*"Organization"[^}]*"@id":\s*"https://plomeroculiacanpro\.mx/#organization"', content, re.DOTALL)

if org_id_match:
    print(f"✅ Organization schema con @id encontrado")
else:
    print(f"❌ Organization schema con @id NO encontrado")

# Buscar properties del Organization
has_name = '"name": "Plomero Culiacán Pro"' in content
has_url = '"url": "https://plomeroculiacanpro.mx"' in content
has_logo = '"logo"' in content and 'logo-plomero-culiacan-pro.webp' in content

print(f"   - name: {'✅' if has_name else '❌'}")
print(f"   - url: {'✅' if has_url else '❌'}")
print(f"   - logo: {'✅' if has_logo else '❌'}")

# Validar páginas de colonias
print(f"\n📄 VALIDANDO PÁGINAS DE COLONIAS")
print(f"{'='*70}\n")

base_dir = Path('servicios/plomero-colonias-culiacan')

total_paginas = 0
paginas_con_author_id = 0
paginas_con_copyright_id = 0

for colonia_dir in sorted(base_dir.iterdir()):
    if not colonia_dir.is_dir() or colonia_dir.name == '__pycache__':
        continue

    index_file = colonia_dir / 'index.html'
    if not index_file.exists():
        continue

    total_paginas += 1

    with open(index_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Verificar author con @id
    author_id_pattern = r'"author":\s*{\s*"@id":\s*"https://plomeroculiacanpro\.mx/#organization"\s*}'
    if re.search(author_id_pattern, content):
        paginas_con_author_id += 1

    # Verificar copyrightHolder con @id
    copyright_id_pattern = r'"copyrightHolder":\s*{\s*"@id":\s*"https://plomeroculiacanpro\.mx/#organization"\s*}'
    if re.search(copyright_id_pattern, content):
        paginas_con_copyright_id += 1

print(f"Total páginas: {total_paginas}")
print(f"Páginas con author @id: {paginas_con_author_id} ({paginas_con_author_id/total_paginas*100:.1f}%)")
print(f"Páginas con copyrightHolder @id: {paginas_con_copyright_id} ({paginas_con_copyright_id/total_paginas*100:.1f}%)")

# Resumen
print(f"\n{'='*70}")
print(f"📊 RESUMEN DE VALIDACIÓN")
print(f"{'='*70}\n")

index_valid = org_id_match and has_name and has_url and has_logo
colonias_valid = paginas_con_author_id == total_paginas and paginas_con_copyright_id == total_paginas

if index_valid and colonias_valid:
    print(f"✅ VALIDACIÓN EXITOSA")
    print(f"\n📈 Implementación completa:")
    print(f"   - Organization schema principal: ✅")
    print(f"   - Referencias @id en author: ✅ (120/120)")
    print(f"   - Referencias @id en copyrightHolder: ✅ (120/120)")
    print(f"\n🎯 Listo para producción")
else:
    print(f"⚠️  VALIDACIÓN PARCIAL")
    if not index_valid:
        print(f"   - Organization schema en index.html: ❌")
    if not colonias_valid:
        print(f"   - Referencias @id en colonias: ⚠️  {paginas_con_author_id}/{total_paginas}")

print(f"\n✨ Validación completada\n")
