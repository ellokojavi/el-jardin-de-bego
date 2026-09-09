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

## Vocabulario: los bloques "📖 Palabras nuevas"

Bego se traba con palabras que las guías daban por sabidas ("sedentarismo", "nicotina",
"encomienda", "hablante lírico"). Por eso cada sección lleva un bloque de vocabulario.

- En el Markdown es un encabezado `#### 📖 Palabras nuevas` seguido de una definición
  por párrafo, con la palabra en negrita y punto: `**Sedentarismo.** Pasar casi todo el
  día sentada…`
- **Dónde va:** justo antes del `### ✏️ Ahora tú` de esa sección, para que lea el
  contenido, aclare las palabras y recién después practique. En las secciones sin
  ejercicios (evaluaciones, actividad central) va inmediatamente después del encabezado
  de sección.
- **Nunca dentro del solucionario.** Es material para Bego, no para el adulto.
- En la web, `scripts/build-web.py` agrupa cada bloque en una caja azul (`.palabras`).
  En el `.docx` sale como subtítulo más definiciones. No hay que hacer nada extra.
- Criterio para incluir una palabra: término técnico de la asignatura, palabra de
  español general poco frecuente a los 11 años, o palabra en inglés nueva (en ese caso
  la definición da el significado y la pronunciación aproximada a la chilena). Se
  excluye lo que el propio texto ya explica en el momento. Entre 2 y 5 por sección.
- Al agregar contenido nuevo a una guía, revisar si necesita palabras nuevas en su
  bloque.

## Imágenes

Las fotos y láminas viven en `imagenes/`, dentro del repositorio, no enlazadas a un sitio
externo. Se insertan en el `.md`, así que salen en la página **y** en el `.docx`.

```markdown
![Pie de foto que explica qué se ve y para qué sirve. Foto de Autor, Licencia.](imagenes/carabelas.jpg)
```

- **Dónde va:** al final de la subsección `###` que ilustra, no al principio de la sección.
- **El pie de foto enseña.** No describe la imagen: dice qué mirar y por qué importa. En
  el caso del desembarco de Colón, además advierte que es una pintura del siglo XIX y no
  un registro fiel — sirve para que Bego aprenda a mirar una fuente con criterio.
- **El crédito va al final del propio pie**, en la misma frase: autor y licencia. Los
  datos completos quedan en `imagenes/creditos.json`, que el script llena solo.
- **Origen:** Wikimedia Commons, priorizando dominio público. `scripts/imagenes.py buscar
  "consulta"` lista candidatas con su licencia; `scripts/imagenes.py bajar "File:X.jpg"
  nombre` descarga, recomprime y anota el crédito. El script va despacio a propósito:
  Commons responde 429 si uno insiste.
- **Techo de tamaño: 760 × 440 px.** No es capricho — pandoc dimensiona las imágenes del
  `.docx` según sus píxeles, y una foto vertical más alta se come una página entera del
  documento impreso.
- Los sellos ALTO EN son un dibujo propio hecho con PIL, no una imagen bajada: son
  octógonos negros simples y así no dependemos de nadie.

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
- Los enlaces de descarga llevan `download="El jardin de Bego - <archivo>.docx"`, así que
  el archivo llega al computador con ese nombre aunque en el repositorio se llame
  `01-Matematicas.docx`. El prefijo se define en `PREFIJO_DESCARGA`, dentro de
  `scripts/build-web.py`, y en los enlaces del `index.html`.
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

## Flashcards

Lenguaje, Ciencias e Historia tienen un mazo de tarjetas cada uno, en dos formatos que
salen del **mismo archivo**: `flashcards-02-Lenguaje.html` (y sus equivalentes) es la
página para estudiar en pantalla y lleva adentro, oculta con `display:none`, la hoja
`.imprimible` que solo aparece al imprimir. El PDF se genera imprimiendo esa misma
página con Chrome sin ventana, así que nunca se desincronizan.

- **Fuente:** `scripts/flashcards.json` — una entrada por guía, con `stem`, `clase`
  (la de `guia.css`), títulos y la lista de tarjetas (`tema`, `p`, `r`). Es lo único
  que se edita a mano; las páginas y los PDF son generados.
- **Generador:** `python3 scripts/build-flashcards.py [stem]`. Sin argumentos rehace
  los tres mazos. Si no encuentra Chrome, deja el HTML y avisa.
- **Estilo:** `flashcards.css`, cargado después de `guia.css` y apoyado en sus tokens.
- **Papel:** cada tarjeta se imprime como una tira de 57 mm con la pregunta a la
  izquierda y la respuesta a la derecha, cuatro por hoja A4. Se corta por el borde
  entero y se dobla por la línea punteada del medio: impresión por una sola cara, sin
  reversos que calzar. Las respuestas de más de 240 caracteres bajan de cuerpo solas
  (clase `apretada`); si una respuesta se sale de la tira, hay que acortarla en el JSON.
- **Criterio de contenido:** las tarjetas repasan lo esencial de la guía, con las mismas
  palabras y ejemplos que usa el documento. No introducen materia nueva. Si se edita una
  guía, revisar si su mazo quedó desactualizado.
- Los enlaces a los dos formatos van en la caja de la guía en `index.html`, en la fila
  `.extras`.

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
