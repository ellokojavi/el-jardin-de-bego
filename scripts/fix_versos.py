#!/usr/bin/env python3
"""Arregla el colapso de versos en docx generado por pandoc.

En Word, las líneas consecutivas de un blockquote (`> `) se colapsan en un solo
párrafo. La solución es terminar cada línea, salvo la última del bloque, con un
espacio y una barra invertida (salto duro de Markdown).

Uso: python3 scripts/fix_versos.py materiales/**/*.md
"""
import re
import sys
from pathlib import Path


def fix(text: str) -> str:
    lines = text.split("\n")
    out = []
    for i, line in enumerate(lines):
        is_quote = line.lstrip().startswith(">")
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        next_is_quote = nxt.lstrip().startswith(">") and nxt.strip() != ">"
        if is_quote and next_is_quote and not line.rstrip().endswith("\\"):
            line = line.rstrip() + " \\"
        out.append(line)
    return "\n".join(out)


def main(paths):
    if not paths:
        print(__doc__)
        return 1
    for p in paths:
        path = Path(p)
        original = path.read_text(encoding="utf-8")
        fixed = fix(original)
        if fixed != original:
            path.write_text(fixed, encoding="utf-8")
            print(f"arreglado: {path}")
        else:
            print(f"sin cambios: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
