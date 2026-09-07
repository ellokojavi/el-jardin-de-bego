#!/usr/bin/env python3
"""Genera la versión web de cada guía a partir de su fuente Markdown.

Una página HTML por documento, con el estilo de "El jardín de Bego", el
solucionario plegado tras un botón y un control de descarga del .docx.

Uso:  python3 scripts/build-web.py            (todas)
      python3 scripts/build-web.py 01-Matematicas.md
"""
import html as _html
import re
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

# clase de color, etiqueta y descripción corta por documento
GUIAS = {
    "00-Plan-de-estudio":    ("g-plan", "Antes de empezar"),
    "01-Matematicas":        ("g-mate", "Guía 1"),
    "02-Lenguaje":           ("g-leng", "Guía 2"),
    "03-Ciencias":           ("g-cien", "Guía 3"),
    "04-Historia":           ("g-hist", "Guía 4"),
    "05-Ingles":             ("g-ingl", "Guía 5"),
    "06-Evaluacion-final":   ("g-eval", "Cierre · Semana 3"),
}

CORTE = re.compile(r"```\{=openxml\}.*?```\s*", re.S)

ICONO_DESCARGA = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<path d="M12 3v12"/><path d="m7 11 5 5 5-5"/><path d="M4 20h16"/></svg>'
)
FLECHA = (
    '<svg class="flecha" width="18" height="18" viewBox="0 0 24 24" fill="none" '
    'stroke="currentColor" stroke-width="2.4" stroke-linecap="round" '
    'stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>'
)


def md_a_html(md: str) -> str:
    if not md.strip():
        return ""
    r = subprocess.run(
        ["pandoc", "--from", "markdown", "--to", "html5"],
        input=md, capture_output=True, text=True, check=True,
    )
    return r.stdout


def envolver_tablas(h: str) -> str:
    return re.sub(r"(<table[\s\S]*?</table>)", r'<div class="tabla-envoltura">\1</div>', h)


def envolver_ahora(h: str) -> str:
    # el marcador universal es el lápiz: "Ahora tú" en español, "Now you try" en inglés
    pat = re.compile(r"<h3[^>]*>[^<]*\u270f[^<]*</h3>", re.I)
    partes, pos = [], 0
    for m in pat.finditer(h):
        partes.append(h[pos:m.start()])
        sig = re.search(r"<h[123][\s>]", h[m.end():])
        fin = m.end() + (sig.start() if sig else len(h) - m.end())
        bloque = h[m.start():fin].rstrip()
        bloque = re.sub(r"<hr\s*/?>\s*$", "", bloque).rstrip()
        partes.append('<section class="ahora">' + bloque + "</section>\n")
        pos = fin
    partes.append(h[pos:])
    return "".join(partes)


def procesar(h: str) -> str:
    return envolver_ahora(envolver_tablas(h))


def separar_portada(md: str):
    """Extrae título, lema y crédito de las primeras líneas y devuelve el resto."""
    lineas = md.split("\n")
    titulo = lema = credito = ""
    i = 0
    while i < len(lineas):
        l = lineas[i].strip()
        i += 1
        if not l:
            continue
        if not titulo and l.startswith("# "):
            titulo = l[2:].strip()
            continue
        if titulo and not lema and l.startswith("**") and l.endswith("**"):
            lema = l.strip("*").strip()
            continue
        if titulo and not credito and l.startswith("Bego"):
            credito = l
            continue
        i -= 1
        break
    return titulo, lema, credito, "\n".join(lineas[i:])


PREFIJO_DESCARGA = "El jardin de Bego - "  # contexto en el nombre del archivo bajado

PLANTILLA = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{titulo_tab} · El jardín de Bego</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700;9..144,900&family=Nunito:wght@400;600;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="./guia.css">
</head>
<body class="{clase}">

<header class="barra">
  <div class="envoltura">
    <a class="volver" href="./index.html">&larr; El jardín de Bego</a>
    <a class="descargar" href="./{docx}" download="{descarga}">{icono} Descargar .docx</a>
  </div>
</header>

<main class="envoltura">
  <div class="encabezado">
    <div class="num">{etiqueta}</div>
    <h1>{titulo}</h1>
    {lema_html}
    {credito_html}
  </div>

  <article class="contenido">
{cuerpo}
  </article>

{solucionario}
  <div class="pie">
    <p><a class="volver" href="./index.html">&larr; Volver al jardín</a></p>
    <a class="descargar" href="./{docx}" download="{descarga}">{icono} Descargar .docx</a>
  </div>
</main>

</body>
</html>
"""

BLOQUE_SOLUCIONARIO = """  <details class="solucionario">
    <summary>
      <span>Solucionario · para el adulto
        <span class="aviso">Contiene todas las respuestas. Conviene abrirlo solo al corregir.</span>
      </span>
      {flecha}
    </summary>
    <div class="cuerpo">
{cuerpo}
    </div>
  </details>

"""


def construir(ruta_md: Path) -> Path:
    stem = ruta_md.stem
    clase, etiqueta = GUIAS[stem]
    md = ruta_md.read_text(encoding="utf-8")

    partes = CORTE.split(md, maxsplit=1)
    cuerpo_md = partes[0]
    solucion_md = partes[1] if len(partes) > 1 else ""

    titulo, lema, credito, resto = separar_portada(cuerpo_md)
    titulo = re.sub(r"^Gu[ií]a\s*\d+\s*·\s*", "", titulo)

    cuerpo = procesar(md_a_html(resto))
    if solucion_md.strip():
        sol = BLOQUE_SOLUCIONARIO.format(
            flecha=FLECHA, cuerpo=procesar(md_a_html(solucion_md))
        )
    else:
        sol = ""

    salida = ruta_md.with_suffix(".html")
    salida.write_text(
        PLANTILLA.format(
            lang="en" if stem == "05-Ingles" else "es-CL",
            clase=clase,
            etiqueta=_html.escape(etiqueta),
            titulo=_html.escape(titulo),
            titulo_tab=_html.escape(titulo),
            lema_html=f'<p class="lema">{_html.escape(lema)}</p>' if lema else "",
            credito_html=f'<p class="credito">{_html.escape(credito)}</p>' if credito else "",
            cuerpo=cuerpo,
            solucionario=sol,
            docx=stem + ".docx",
            descarga=PREFIJO_DESCARGA + stem + ".docx",
            icono=ICONO_DESCARGA,
        ),
        encoding="utf-8",
    )
    return salida


def main(args):
    objetivos = [Path(a) for a in args] or sorted(RAIZ.glob("[0-9][0-9]-*.md"))
    for md in objetivos:
        md = (RAIZ / md).resolve()
        if md.stem not in GUIAS:
            print(f"omitido (no es una guía): {md.name}")
            continue
        salida = construir(md)
        print(f"→ {salida.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
