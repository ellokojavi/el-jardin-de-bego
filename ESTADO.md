# Estado del proyecto

Última actualización: 2026-09-09

## Completado

Las siete piezas están producidas y convertidas a `.docx`:

- `00-Plan-de-estudio` — calendario de 15 sesiones y recomendaciones para el adulto
- `01-Matematicas`, `02-Lenguaje`, `03-Ciencias`, `04-Historia`, `05-Ingles`
- `06-Evaluacion-final` — evaluación integrada de 55 puntos con solucionario
- `index.html` — sitio hub con plan por semanas y tracker de sesiones
- Empaquetado como repositorio git con `.gitattributes`, `.gitignore`, `.nojekyll`,
  LICENSE (CC BY-NC-SA 4.0) y README

El 2026-09-07 el repositorio se instaló como proyecto local de Cowork en
`~/Documents/Claude/Projects/Plan de Estudios Bego - Quinto Basico`, conservando su
historial git.

### Flashcards (2026-09-09)

Mazos de pregunta y respuesta para Lenguaje (14 tarjetas), Ciencias (17) e Historia (21),
en dos formatos generados desde `scripts/flashcards.json` por `scripts/build-flashcards.py`:
la página para estudiar en pantalla y el PDF para recortar y doblar. Enlazados desde la
caja de cada guía en `index.html`. Matemáticas e Inglés todavía no tienen mazo.

## Publicado

- Repositorio público: https://github.com/ellokojavi/el-jardin-de-bego
- Sitio en vivo: https://ellokojavi.github.io/el-jardin-de-bego/
- **El sitio lleva `<meta name="robots" content="noindex, nofollow">` a propósito.**
  La URL es pública y funciona para cualquiera que tenga el enlace, pero el sitio no
  aparece en buscadores. No quitar ese meta tag: es una decisión, no un descuido.
- El `robots.txt` de la raíz del repo es complementario y en la práctica no lo leen
  los crawlers (en una página de proyecto solo consultan
  `https://ellokojavi.github.io/robots.txt`). El meta tag es el que hace el trabajo.
- Los commits usan la dirección `noreply` de GitHub, no el correo personal.

## Pendiente

- **Empezar el plan con Bego** — 15 sesiones, tres semanas.
- Opcional: completar `referencia/curriculum-mineduc.md` con los OA textuales por
  asignatura, para poder trazar cada guía contra su objetivo curricular.
