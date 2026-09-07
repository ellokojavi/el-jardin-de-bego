# Scripts

- `build.sh` — Markdown → docx con pandoc (todos los `NN-*.md`, o los que se indiquen)
- `verify.sh` — docx → PDF → JPEG por página en `_verificacion/`, para revisar el
  formato con los ojos antes de dar por bueno un documento
- `fix_versos.py` — agrega el salto duro (` \`) a los versos en blockquote, que en
  Word se colapsan en un solo párrafo

Recordatorios de formato (ver `../CLAUDE.md`):

- Salto de página duro: bloque ```` ```{=openxml} ```` con
  `<w:p><w:r><w:br w:type="page"/></w:r></w:p>`
- Nada de LaTeX `$$...$$`: no renderiza en docx vía pandoc
