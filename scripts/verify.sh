#!/usr/bin/env bash
# Verificación visual: docx -> pdf -> JPEGs por página, en _verificacion/
# Uso: scripts/verify.sh 01-Matematicas.docx [...]
set -euo pipefail
cd "$(dirname "$0")/.."
out=_verificacion
mkdir -p "$out"
for f in "$@"; do
  base="$(basename "${f%.docx}")"
  soffice --headless --convert-to pdf --outdir "$out" "$f" >/dev/null
  pdftoppm -jpeg -r 60 "$out/$base.pdf" "$out/page-$base"
  echo "→ $out/page-$base-*.jpg"
done
