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

Metáfora de jardín (cada asignatura es una planta): SVG animado, tarjetas de
asignatura que enlazan a los `.docx`, sección con el plan de tres semanas y un tracker
de las 15 sesiones. El tracker persiste en `localStorage` con sincronización entre
pestañas, indicador de estado de guardado y fallback si el almacenamiento está
bloqueado. El texto de introducción usa tercera persona plural: «todo lo que pasaron
en quinto año en Chile».

El progreso vive en el navegador y el equipo donde se marque: no se sincroniza entre
dispositivos ni se guarda en el repositorio.

## Publicación

GitHub Pages: **Settings → Pages**, *Deploy from a branch*, rama `main`, carpeta
`/ (root)`.

Decisión pendiente antes de publicar: los documentos incluyen los solucionarios
completos. Repositorio público = solucionarios públicos. GitHub Pages sobre
repositorio privado requiere plan de pago; la alternativa es dejarlo privado y usar
los archivos localmente.
