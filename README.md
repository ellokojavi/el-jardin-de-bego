# El jardín de Bego

Materiales de repaso para 5° básico, alineados a las Bases Curriculares del Ministerio de Educación de Chile. Cubren lo pasado entre marzo y septiembre de 2026 en cinco asignaturas, organizados en un plan de tres semanas y unas 20 horas de estudio.

**Sitio en vivo:** https://ellokojavi.github.io/el-jardin-de-bego/

`index.html` es la guía principal: enlaza las cinco guías, muestra el plan por semanas y lleva la cuenta de las quince sesiones.

## Contenido

| Archivo | Asignatura | Contenidos | Horas |
|---|---|---|---|
| `00-Plan-de-estudio.docx` | — | Calendario de las 15 sesiones y recomendaciones para el adulto | — |
| `01-Matematicas.docx` | Matemáticas | Números hasta el millón, multiplicación y división, fracciones, decimales | 5 |
| `02-Lenguaje.docx` | Lenguaje y Comunicación | Textos literarios, el poema y sus elementos, lenguaje figurado | 4 |
| `03-Ciencias.docx` | Ciencias Naturales | Hábitos saludables, sellos ALTO EN, menú saludable, efectos del cigarrillo | 4 |
| `04-Historia.docx` | Historia y Geografía | Descubrimiento y Conquista de América y de Chile | 4 |
| `05-Ingles.docx` | Inglés | Food vocabulary, likes and dislikes, there is / there are, healthy habits | 3 |
| `06-Evaluacion-final.docx` | Todas | Evaluación integrada de 55 puntos con solucionario | — |

Los archivos `.md` son las fuentes de cada documento. Para regenerar un `.docx` después de editar su fuente:

```bash
pandoc 01-Matematicas.md -o 01-Matematicas.docx --standalone
```

## Estructura de cada guía

1. Diagnóstico de entrada
2. Cuatro secciones de contenido, cada una con ejercicios «✏️ Ahora tú»
3. Práctica graduada en tres niveles
4. Una actividad central de aplicación
5. Evaluación integradora
6. Solucionario, después de un salto de página, con tabla de remediación

El solucionario va siempre en páginas aparte para poder imprimir solo la parte del estudiante.

## Publicar en GitHub Pages

En **Settings → Pages**, elegir *Deploy from a branch*, rama `main` y carpeta `/ (root)`. La página queda en `https://USUARIO.github.io/REPOSITORIO/` en un par de minutos.

Los enlaces a las guías son relativos, así que funcionan tanto en la web publicada como al descargar la carpeta completa y abrir `index.html` localmente.

**Antes de publicar**, vale la pena decidir si el repositorio será público. Los documentos incluyen los solucionarios completos. Si prefieres mantenerlo privado, GitHub Pages sobre repositorios privados requiere un plan de pago; la alternativa es dejar el repositorio privado y usar los archivos de forma local.

## Progreso guardado

El marcador de sesiones usa el almacenamiento local del navegador. El avance se conserva al cerrar la página, pero vive en ese navegador y ese equipo: no se sincroniza entre dispositivos ni se guarda en el repositorio.

## Licencia

Contenidos originales bajo [Creative Commons BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.es). Se pueden compartir y adaptar con fines no comerciales, citando la fuente y manteniendo la misma licencia.
