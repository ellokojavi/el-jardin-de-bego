#!/usr/bin/env bash
# Convierte las fuentes .md a .docx en la raíz del proyecto.
# Uso: scripts/build.sh [archivo.md ...]   (sin argumentos: convierte todos)
set -euo pipefail
cd "$(dirname "$0")/.."
files=("$@")
if [ ${#files[@]} -eq 0 ]; then
  while IFS= read -r f; do files+=("$f"); done < <(ls -1 [0-9][0-9]-*.md | sort)
fi
for f in "${files[@]}"; do
  out="${f%.md}.docx"
  echo "→ $f  ->  $out"
  pandoc "$f" -o "$out" --standalone
done
