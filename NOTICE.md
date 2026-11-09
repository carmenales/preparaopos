# Créditos y licencias de terceros

PreparaOpos es un proyecto personal de estudio. Usa o se basa en el trabajo de otras personas, que se
reconoce aquí. Las licencias completas están en los enlaces o en las carpetas indicadas.

## PreparaTIC
**Grupo de Preparación para las oposiciones TIC de la Administración del Estado.** Publica su aplicación de
tests con licencia **Apache 2.0** (ver «Licencia de uso» en la propia aplicación y
`apps/tests_preparatic/generator/LICENSE`).

De PreparaTIC se usan:
- El **banco de preguntas A1 TIC** (16.680 preguntas, con su bloque, tema, año y marca de examen oficial),
  extraído de su aplicación V3 (`scripts/etl/preparatic_bundle_extracted.json`, `scripts/etl/import_preparatic.py`)
  y los nombres de bloques y temas (`scripts/etl/preparatic_catalog.json`, `services/test-engine/syllabi/`).
- Las **aplicaciones originales** V2 y V3, el generador en Java y sus datos, en `apps/tests_preparatic/`
  (se conservan como referencia).
- Su **diseño y su lógica de test** como modelo de test-engine: colores, pantalla de test (cronómetro, Corregir,
  Filtrar, Modo Entrenamiento), tests por colección (Aleatorios, Relevancia, Bloques, Temas, Años) y el peso por
  frecuencia en los exámenes oficiales. Es una reimplementación propia en Python y Jinja, no una copia de su código.

Cambios respecto al original (sección 4 de la licencia Apache 2.0): las preguntas se guardan en la base de datos
de test-engine y se pueden corregir, anular o enlazar con apuntes desde la aplicación.

## Exámenes oficiales
Las preguntas de los exámenes de AGE A2 GSI 2024, Ayuntamiento de Madrid, Ayuntamiento de Majadahonda,
Comunidad de Madrid y UC3M son las publicadas por cada convocatoria, con sus plantillas de respuestas.
Las de TAI vienen de preparadortai, la aplicación anterior de este proyecto.

## Bibliotecas que se cargan en el navegador
| Biblioteca | Licencia | Uso |
|---|---|---|
| [Apache ECharts](https://echarts.apache.org/) 5.5.1 | Apache 2.0 | Gráficos de Estadísticas (desde jsDelivr) |
| [htmx](https://htmx.org/) 1.9.12 | BSD 2-Clause | Interacción de test-engine sin recargar (desde unpkg) |
| [Heroicons](https://heroicons.com/) | MIT | Trazos de los iconos de test-engine (`services/test-engine/presentation/icons.py`) |

Las dependencias de Python de cada servicio están en su `requirements.txt`, cada una con su propia licencia.
