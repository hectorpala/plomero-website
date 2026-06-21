#!/bin/bash
# Instala los git-hooks rastreados en .git/hooks (que NO está versionado).
# Corre esto tras clonar el repo para activar el gate pre-push.
set -e
DIR="$(cd "$(dirname "$0")" && pwd)"
REPO="$(git -C "$DIR" rev-parse --show-toplevel)"
cp "$DIR/pre-push" "$REPO/.git/hooks/pre-push"
chmod +x "$REPO/.git/hooks/pre-push"
echo "✅ pre-push instalado en .git/hooks/"
