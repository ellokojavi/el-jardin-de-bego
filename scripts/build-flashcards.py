#!/usr/bin/env python3
"""Genera las flashcards de "El jardín de Bego".

Lee `scripts/flashcards.json` y escribe, para cada guía listada ahí:

  flashcards-<stem>.html   la versión en línea (mazo interactivo) que además
                           lleva adentro, oculta en pantalla, la hoja para
                           imprimir; Ctrl+P sobre la página imprime las tarjetas
  flashcards-<stem>.pdf    la misma hoja, ya paginada, lista para imprimir

El PDF se saca imprimiendo la propia página con Chrome/Chromium sin ventana, así
que hay una sola fuente para las dos versiones. Si no hay Chrome a mano, el
script deja las páginas HTML y avisa: el PDF se puede regenerar después.

    python3 scripts/build-flashcards.py            # todas las guías
    python3 scripts/build-flashcards.py 04-Historia
"""

from __future__ import annotations

import html
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATOS = Path(__file__).resolve().parent / "flashcards.json"
PREFIJO_DESCARGA = "El jardin de Bego - "  # mismo criterio que build-web.py

CANDIDATOS_CHROME = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/opt/pw-browsers/chromium",
]


def buscar_chrome() -> str | None:
    for nombre in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        ruta = shutil.which(nombre)
        if ruta:
            return ruta
    for ruta in CANDIDATOS_CHROME:
        if os.path.exists(ruta):
            return ruta
    return None


def e(texto: str) -> str:
    return html.escape(texto, quote=False)


# --------------------------------------------------------------------------- #
# plantilla
# --------------------------------------------------------------------------- #

PAGINA = """<!DOCTYPE html>
<html lang="es-CL">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Flashcards de {asignatura} · El jardín de Bego</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22%3E%3Ctext y=%22.9em%22 font-size=%2290%22%3E🌷%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700;9..144,900&family=Nunito:wght@400;600;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="./guia.css">
<link rel="stylesheet" href="./flashcards.css">
</head>
<body class="{clase} cuerpo-tarjetas">

<header class="barra">
  <div class="envoltura">
    <a class="volver" href="./index.html">&larr; El jardín de Bego</a>
    <span class="acciones-barra">
      <a class="descargar" href="./{stem}.html">Ver la guía</a>
      <a class="descargar" href="./flashcards-{stem}.pdf" download="{descarga_pdf}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3v12"/><path d="m7 11 5 5 5-5"/><path d="M4 20h16"/></svg> Imprimibles</a>
    </span>
  </div>
</header>

<main class="envoltura">
  <div class="encabezado">
    <div class="num">{num} · Flashcards</div>
    <h1>{titulo}</h1>
    <p class="lema">{subtitulo}</p>
    <p class="credito">{n} tarjetas · Bego · 5° básico · Repaso 2026</p>
  </div>

  <section class="mazo" aria-label="Mazo de tarjetas">
    <div class="mazo-datos">
      <span id="posicion">Tarjeta 1 de {n}</span>
      <span id="marcador" class="marcador-mazo"></span>
    </div>
    <div class="progreso"><i id="avance"></i></div>

    <div class="tarjeta" id="tarjeta" tabindex="0" role="button" aria-live="polite"
         aria-label="Tarjeta. Toca o aprieta la barra espaciadora para darla vuelta.">
      <div class="giro" id="giro">
        <div class="lado frente">
          <span class="etiqueta" id="tema-frente"></span>
          <p class="texto" id="pregunta"></p>
          <span class="pista">Toca la tarjeta para ver la respuesta</span>
        </div>
        <div class="lado reverso">
          <span class="etiqueta">Respuesta</span>
          <p class="texto respuesta" id="respuesta"></p>
        </div>
      </div>
    </div>

    <div class="juicio" id="juicio" hidden>
      <button type="button" class="boton bien" id="btn-bien">La sabía</button>
      <button type="button" class="boton mal" id="btn-mal">A repasar</button>
    </div>

    <div class="controles">
      <button type="button" class="boton" id="btn-antes" aria-label="Tarjeta anterior">&larr; Antes</button>
      <button type="button" class="boton principal" id="btn-voltear">Dar vuelta</button>
      <button type="button" class="boton" id="btn-sigue" aria-label="Tarjeta siguiente">Después &rarr;</button>
    </div>

    <div class="extras-mazo">
      <button type="button" class="boton chico" id="btn-barajar">Barajar</button>
      <button type="button" class="boton chico" id="btn-reiniciar">Empezar de nuevo</button>
    </div>

    <div class="resumen" id="resumen" hidden>
      <h2 id="resumen-titulo"></h2>
      <p id="resumen-texto"></p>
      <div class="extras-mazo">
        <button type="button" class="boton principal" id="btn-repasar" hidden>Repasar las que fallé</button>
        <button type="button" class="boton" id="btn-otra-vez">Pasar todas de nuevo</button>
      </div>
    </div>
  </section>

  <section class="instrucciones">
    <h2>Cómo se usan</h2>
    <p><strong>En pantalla.</strong> Lee la pregunta, respóndela en voz alta y recién ahí da vuelta la
    tarjeta. Marca «la sabía» o «a repasar» con honestidad: al final el mazo te deja pasar de nuevo
    solo las que fallaste. «Barajar» las desordena, que es como conviene estudiar la segunda vuelta.</p>
    <p><strong>En papel.</strong> El botón <em>Imprimibles</em> baja un PDF con las {n} tarjetas ya
    escritas. Imprime las hojas por un solo lado, recorta por la línea entera y dobla por la línea
    punteada: te queda la pregunta por delante y la respuesta por detrás.</p>
    <p class="volver-guia"><a href="./{stem}.html">Volver a la {num_min}</a> · <a href="./index.html">Índice del jardín</a></p>
  </section>
</main>

<footer class="cierre">
  <p>El jardín de Bego · Flashcards de {asignatura}</p>
</footer>

<!-- Hoja para imprimir: invisible en pantalla, es la que sale en el PDF y en Ctrl+P -->
<div class="imprimible" aria-hidden="true">
  <div class="cabecera-impresa">
    <strong>Flashcards · {titulo}</strong>
    <span>{subtitulo} · Bego · 5° básico</span>
    <span class="modo">Recorta por la línea entera y dobla por la punteada: la pregunta queda delante y la respuesta detrás.</span>
  </div>
{tiras}
</div>

<script>
const TARJETAS = {json_tarjetas};
const ASIGNATURA = {json_asignatura};
{script}
</script>
</body>
</html>
"""

SCRIPT = r"""
(function () {
  const $ = (id) => document.getElementById(id);
  const tarjeta = $("tarjeta"), giro = $("giro");
  const elPregunta = $("pregunta"), elRespuesta = $("respuesta"), elTema = $("tema-frente");
  const elPos = $("posicion"), elMarcador = $("marcador"), elAvance = $("avance");
  const juicio = $("juicio"), resumen = $("resumen"), mazo = document.querySelector(".mazo");

  let orden = [], i = 0, vuelta = false, sabidas = new Set(), fallidas = new Set();

  const barajar = (a) => { for (let k = a.length - 1; k > 0; k--) { const j = Math.floor(Math.random() * (k + 1)); [a[k], a[j]] = [a[j], a[k]]; } return a; };

  function arrancar(indices, mezclar) {
    orden = mezclar ? barajar(indices.slice()) : indices.slice();
    i = 0; vuelta = false; sabidas = new Set(); fallidas = new Set();
    resumen.hidden = true;
    mazo.classList.remove("terminado");
    pintar();
  }

  function pintar() {
    const t = TARJETAS[orden[i]];
    giro.classList.remove("volteada");
    vuelta = false;
    elTema.textContent = t.tema || ASIGNATURA;
    elPregunta.textContent = t.p;
    elRespuesta.textContent = t.r;
    elPos.textContent = "Tarjeta " + (i + 1) + " de " + orden.length;
    elMarcador.textContent = sabidas.size ? sabidas.size + " sabidas · " + fallidas.size + " a repasar" : "";
    elAvance.style.width = ((i) / orden.length * 100) + "%";
    juicio.hidden = true;
    $("btn-voltear").textContent = "Dar vuelta";
    tarjeta.setAttribute("aria-label", "Pregunta: " + t.p);
  }

  function voltear() {
    vuelta = !vuelta;
    giro.classList.toggle("volteada", vuelta);
    juicio.hidden = !vuelta;
    $("btn-voltear").textContent = vuelta ? "Ver la pregunta" : "Dar vuelta";
    if (vuelta) tarjeta.setAttribute("aria-label", "Respuesta: " + TARJETAS[orden[i]].r);
  }

  function avanzar(paso) {
    const siguiente = i + paso;
    if (siguiente < 0) return;
    if (siguiente >= orden.length) { terminar(); return; }
    i = siguiente; pintar();
  }

  function juzgar(bien) {
    const id = orden[i];
    if (bien) { sabidas.add(id); fallidas.delete(id); } else { fallidas.add(id); sabidas.delete(id); }
    avanzar(1);
  }

  function terminar() {
    mazo.classList.add("terminado");
    resumen.hidden = false;
    elAvance.style.width = "100%";
    elPos.textContent = "Mazo terminado";
    elMarcador.textContent = "";
    const total = orden.length, bien = sabidas.size, mal = fallidas.size;
    $("resumen-titulo").textContent = mal === 0 && bien > 0 ? "¡Te las sabías todas!" : "Fin del mazo";
    $("resumen-texto").textContent = bien + " de " + total + " marcadas como sabidas" +
      (mal ? " y " + mal + " para repasar." : ".") +
      (bien + mal < total ? " Las que no marcaste quedaron sin puntuar." : "");
    $("btn-repasar").hidden = mal === 0;
    resumen.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  tarjeta.addEventListener("click", voltear);
  tarjeta.addEventListener("keydown", (ev) => {
    if (ev.key === " " || ev.key === "Enter") { ev.preventDefault(); voltear(); }
  });
  $("btn-voltear").addEventListener("click", voltear);
  $("btn-antes").addEventListener("click", () => avanzar(-1));
  $("btn-sigue").addEventListener("click", () => avanzar(1));
  $("btn-bien").addEventListener("click", () => juzgar(true));
  $("btn-mal").addEventListener("click", () => juzgar(false));
  $("btn-barajar").addEventListener("click", () => arrancar(TARJETAS.map((_, k) => k), true));
  $("btn-reiniciar").addEventListener("click", () => arrancar(TARJETAS.map((_, k) => k), false));
  $("btn-otra-vez").addEventListener("click", () => arrancar(TARJETAS.map((_, k) => k), true));
  $("btn-repasar").addEventListener("click", () => arrancar(Array.from(fallidas), true));

  document.addEventListener("keydown", (ev) => {
    if (ev.target.tagName === "BUTTON" && ev.key === " ") return;
    if (ev.key === "ArrowRight") avanzar(1);
    else if (ev.key === "ArrowLeft") avanzar(-1);
    else if (ev.key === " " && ev.target === document.body) { ev.preventDefault(); voltear(); }
  });

  arrancar(TARJETAS.map((_, k) => k), false);
})();
"""


def tira(n: int, total: int, asignatura: str, t: dict) -> str:
    largo = len(t["r"])
    clase = " apretada" if largo > 240 else ""
    return f"""  <div class="tira">
    <div class="cara pregunta">
      <span class="rotulo">{e(asignatura)} · tarjeta {n} de {total}</span>
      <p class="linea">{e(t['p'])}</p>
      <span class="tema-impreso">{e(t.get('tema', ''))}</span>
    </div>
    <div class="cara respuesta{clase}">
      <span class="rotulo">Respuesta {n}</span>
      <p class="linea">{e(t['r'])}</p>
    </div>
  </div>"""


def construir(guia: dict) -> Path:
    stem = guia["stem"]
    tarjetas = guia["tarjetas"]
    total = len(tarjetas)
    tiras = "\n".join(
        tira(k + 1, total, guia["asignatura"], t) for k, t in enumerate(tarjetas)
    )
    pagina = PAGINA.format(
        clase=guia["clase"],
        stem=stem,
        num=guia["num"],
        num_min=guia["num"].lower(),
        titulo=e(guia["titulo"]),
        subtitulo=e(guia["subtitulo"]),
        asignatura=e(guia["asignatura"]),
        n=total,
        tiras=tiras,
        descarga_pdf=f"{PREFIJO_DESCARGA}Flashcards {guia['asignatura']}.pdf",
        json_tarjetas=json.dumps(tarjetas, ensure_ascii=False),
        json_asignatura=json.dumps(guia["asignatura"], ensure_ascii=False),
        script=SCRIPT,
    )
    destino = RAIZ / f"flashcards-{stem}.html"
    destino.write_text(pagina, encoding="utf-8")
    return destino


def a_pdf(pagina: Path, chrome: str) -> bool:
    salida = pagina.with_suffix(".pdf")
    with tempfile.TemporaryDirectory() as perfil:
        orden = [
            chrome,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            f"--user-data-dir={perfil}",
            "--no-pdf-header-footer",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=6000",
            f"--print-to-pdf={salida}",
            pagina.as_uri(),
        ]
        res = subprocess.run(orden, capture_output=True, text=True)
    if res.returncode != 0 or not salida.exists():
        print(f"  ! No se pudo generar {salida.name}: {res.stderr.strip()[:200]}")
        return False
    return True


def main() -> int:
    datos = json.loads(DATOS.read_text(encoding="utf-8"))
    pedidas = sys.argv[1:]
    guias = [g for g in datos["guias"] if not pedidas or g["stem"] in pedidas]
    if not guias:
        print("No hay guías que coincidan. Disponibles:",
              ", ".join(g["stem"] for g in datos["guias"]))
        return 1

    chrome = buscar_chrome()
    if not chrome:
        print("Aviso: no encontré Chrome ni Chromium; genero solo el HTML.")

    for guia in guias:
        pagina = construir(guia)
        print(f"✓ {pagina.name} ({len(guia['tarjetas'])} tarjetas)")
        if chrome and a_pdf(pagina, chrome):
            print(f"✓ {pagina.with_suffix('.pdf').name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
