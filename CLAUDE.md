# El jardín de Bego — repaso de 5° básico

Materiales de repaso para Bego (11 años), alineados a las Bases Curriculares del
Ministerio de Educación de Chile para 5° básico. Cubren lo que su curso pasó entre
**marzo y septiembre de 2026** en cinco asignaturas, en un plan de **tres semanas /
15 sesiones / ~20 horas**.

`index.html` es la guía principal del sitio: enlaza las cinco guías, muestra el plan
por semanas y lleva la cuenta de las sesiones.

## Archivos

Estructura plana, a propósito: `index.html` enlaza los `.docx` con rutas relativas,
así que funciona igual publicado en GitHub Pages o abriendo la carpeta local. **No
mover los documentos a subcarpetas sin actualizar los enlaces del `index.html`.**

| Archivo | Asignatura | Contenidos | Horas |
|---|---|---|---|
| `00-Plan-de-estudio` | — | Calendario de las 15 sesiones y recomendaciones para el adulto | — |
| `01-Matematicas` | Matemáticas | Números hasta el millón, multiplicación y división, fracciones, decimales | 5 |
| `02-Lenguaje` | Lenguaje y Comunicación | Textos literarios, el poema y sus elementos, lenguaje figurado | 4 |
| `03-Ciencias` | Ciencias Naturales | Hábitos saludables, sellos ALTO EN, menú saludable, efectos del cigarrillo | 4 |
| `04-Historia` | Historia y Geografía | Descubrimiento y Conquista de América y de Chile | 4 |
| `05-Ingles` | Inglés | Food vocabulary, likes and dislikes, there is / there are, healthy habits | 3 |
| `06-Evaluacion-final` | Todas | Evaluación integrada de 55 puntos con solucionario | — |

Cada uno existe como `.md` (**fuente, se edita**) y `.docx` (**generado, no se edita
a mano**). Después de tocar un `.md` hay que regenerar su `.docx`.

Además: `referencia/` (bases curriculares y fuentes), `scripts/` (conversión y
verificación), `LICENSE` (CC BY-NC-SA 4.0), `.nojekyll` (para GitHub Pages).

## Estructura de cada guía

1. Diagnóstico de entrada
2. Cuatro secciones de contenido, cada una con ejercicios «✏️ Ahora tú»
3. Práctica graduada en tres niveles
4. Una actividad central de aplicación
5. Evaluación integradora
6. Solucionario, **después de un salto de página**, con tabla de remediación

El solucionario va siempre en páginas aparte para poder imprimir solo la parte de la
estudiante.

## Reglas de contenido

- Español de Chile, natural para una niña de 11 años, sin infantilizar. La guía de
  Inglés es la excepción: su contenido va en inglés.
- Los textos literarios son **composiciones originales**, no obras con derechos.
- **Conexiones entre asignaturas** deliberadas, y vale la pena mantenerlas al editar:
  el menú saludable de Ciencias se traduce en la guía de Inglés; las fracciones de
  Matemáticas reaparecen en el plato saludable de Ciencias; los viajes de Colón se
  trabajan con números grandes en Matemáticas; el poema «Barco de papel» de Lenguaje
  conversa con los viajes de exploración de Historia.
- **Consistencia retroactiva**: cuando se identifica una mejora estructural, se
  aplica hacia atrás a todas las guías ya terminadas.

## Versión web de las guías

Cada documento existe también como página: `01-Matematicas.html`, etc., generadas por
`scripts/build-web.py` a partir del mismo `.md`. **No se editan a mano**, igual que los
`.docx`.

- El estilo compartido está en `guia.css`. Tocarlo cambia las siete páginas.
- Cada página lleva el `noindex`, un enlace de vuelta al índice y un botón de descarga
  del `.docx` arriba y abajo.
- El **solucionario va plegado** dentro de un `<details>` con la advertencia "para el
  adulto". El script lo separa cortando el Markdown en el bloque ```` ```{=openxml} ````
  del salto de página, así que ese marcador cumple dos funciones: salto de página en el
  `.docx` y frontera del solucionario en la web. No quitarlo.
- Los bloques "✏️ Ahora tú" (y "✏️ Now you try" en Inglés) se detectan por el lápiz y se
  destacan con un recuadro. Si se renombran, conservar el emoji.
- Las guías web son **solo de lectura**: los ejercicios se responden en el `.docx`
  impreso o en el cuaderno.

Después de editar cualquier `.md` hay que regenerar **ambos** formatos:

```bash
scripts/build.sh 01-Matematicas.md      # .docx
python3 scripts/build-web.py 01-Matematicas.md   # .html
```

## Toolchain

Todo está instalado en este Mac (`pandoc`, `soffice`, `pdftoppm`, `git`).

- **Markdown → docx**: `pandoc 01-Matematicas.md -o 01-Matematicas.docx --standalone`
  (o `scripts/build.sh` para todos)
- **Salto de página duro en docx**: en el Markdown, un bloque ```` ```{=openxml} ````
  con `<w:p><w:r><w:br w:type="page"/></w:r></w:p>`
- **Versos**: líneas consecutivas de blockquote (`> `) se colapsan en Word salvo que
  cada línea, excepto la última, termine en ` \`. Arreglo: `scripts/fix_versos.py`
- **Matemáticas**: LaTeX (`$$...$$`) **no** renderiza en docx vía pandoc — usar
  equivalentes en texto plano.
- **Verificación visual**: `scripts/verify.sh 01-Matematicas.docx` genera JPEGs por
  página en `_verificacion/` para revisar el formato con los ojos. Hacerlo siempre
  después de regenerar un documento.
- **Sitio**: pruebas de interactividad con Playwright.

## Sitio hub

Metáfora de jardín (cada asignatura es una planta): SVG animado —el sol gira y respira,
la abeja vuela y aletea, todo detenido si el sistema pide movimiento reducido—, tarjetas
que abren la guía web con descarga `.docx` aparte, sección con el plan de tres semanas y
el marcador de las 15 sesiones.

**El marcador es de solo lectura.** El avance vive en `progreso.js`, que declara
`window.PROGRESO = { actualizado, sesiones }`. Nadie puede marcar sesiones desde el
navegador: para actualizar el progreso se edita ese archivo y se hace push. Dentro del
propio archivo está la tabla de qué sesión corresponde a cada guía. Se carga con
`<script src>` y no con `fetch`, para que la página siga funcionando abierta desde el
disco.

Ojo: el repositorio es público, así que `progreso.js` es legible por cualquiera que
tenga la URL. Es privado en el sentido de que no se edita desde la página, no en el
sentido de secreto.

## Publicación

Publicado el 2026-09-07 en GitHub Pages, desde `main` / raíz:

- Repositorio público: https://github.com/ellokojavi/el-jardin-de-bego
- Sitio: https://ellokojavi.github.io/el-jardin-de-bego/

El sitio lleva `<meta name="robots" content="noindex, nofollow">` **a propósito**: la
URL es pública y se puede compartir con quien sea, pero el sitio queda fuera de los
buscadores, porque los documentos están dirigidos a una niña por su nombre. No quitar
ese meta tag. El `robots.txt` es complementario y no lo leen los crawlers en una
página de proyecto; el meta tag es el que sirve.

Los documentos incluyen los solucionarios completos y el repositorio es público: eso
fue una decisión consciente.

Después de cambiar cualquier `.md`, regenerar su `.docx` (`scripts/build.sh`),
verificar (`scripts/verify.sh`) y hacer push — el sitio se reconstruye solo.
