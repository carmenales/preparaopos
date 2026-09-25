# Topología de Datos y Persistencia

**Última actualización:** 25 de septiembre de 2026  
**Estado:** Inventario del sistema actual (As-Is) — previo a migración

Este documento cataloga todos los almacenes de datos del ecosistema PreparaOpos, sus esquemas, formatos y ubicaciones. Se actualizará conforme avance la migración a la nueva arquitectura (ver `docs/adr/0001-arquitectura-nueva-generacion.md`).

---

## Índice

- [Topología de Datos y Persistencia](#topología-de-datos-y-persistencia)
  - [Índice](#índice)
  - [1. Resumen de Motores de Almacenamiento](#1-resumen-de-motores-de-almacenamiento)
  - [2. MariaDB Relacional (Preparador TAI)](#2-mariadb-relacional-preparador-tai)
    - [Conexión](#conexión)
    - [2.1. Diagrama ER Completo](#21-diagrama-er-completo)
    - [2.2. Descripción de Tablas](#22-descripción-de-tablas)
    - [2.3. Exportación y Gestión del Dump Local](#23-exportación-y-gestión-del-dump-local)
  - [3. IndexedDB (PreparaTIC V3)](#3-indexeddb-preparatic-v3)
  - [4. Ficheros Markdown (Knowledge Base)](#4-ficheros-markdown-knowledge-base)
  - [5. Estructuras Vectoriales e Índices (Study Assistant)](#5-estructuras-vectoriales-e-índices-study-assistant)
  - [6. CSVs de PreparaTIC (Banco de Preguntas)](#6-csvs-de-preparatic-banco-de-preguntas)
  - [7. SQL de Exámenes Oficiales Importados](#7-sql-de-exámenes-oficiales-importados)
  - [8. Reglas de Git para Datos](#8-reglas-de-git-para-datos)
  - [9. Estado Objetivo (To-Be)](#9-estado-objetivo-to-be)

---

## 1. Resumen de Motores de Almacenamiento

El estado de los datos se encuentra actualmente **fragmentado en 4 motores de almacenamiento** más 2 fuentes de datos en ficheros planos pendientes de integración:

| # | Motor / Formato | Ubicación | Aplicación que lo consume | Volumen aproximado |
| :--- | :--- | :--- | :--- | :--- |
| 1 | **MariaDB 10.4** | Contenedor Docker / XAMPP local | `apps/preparadortai` (PHP) | 7 tablas, ~1.500 preguntas |
| 2 | **IndexedDB** (navegador) | Almacenamiento local del navegador | `apps/tests_preparatic` (V3 SPA) | +10.300 preguntas + intentos |
| 3 | **Ficheros Markdown** | `knowledge/**/*.md` | `apps/studyassistant` (PHP) | ~200 ficheros, 4 administraciones |
| 4 | **JSON + NumPy** | `apps/studyassistant/data/` | `services/embeddings` (Python) | 3 ficheros (índice + chunks + vectores dim. 384) |
| 5 | **CSV** (ficheros planos) | `apps/tests_preparatic/data/` | No integrado en app; fuente de datos | 10.308 filas, 22 columnas |
| 6 | **SQL generado** | `imports/age_a2_gsi/generated/` | No integrado; requiere import manual | 180 preguntas AGE GSI 2024 |

---

## 2. MariaDB Relacional (Preparador TAI)

### Conexión

| Parámetro | Docker | XAMPP Local |
| :--- | :--- | :--- |
| Host | `localhost` | `localhost` / `127.0.0.1` |
| Puerto | `3307` | `3306` |
| Base de datos | `preparadortai` | `preparadortai` |
| Usuario app | `preparaopos` | `root` |
| Contraseña app | `preparaopos` | *(sin contraseña o la configurada)* |

### 2.1. Diagrama ER Completo

```mermaid
erDiagram
    ptype ||--o{ incorrectas : "tiene opciones falsas"
    ptype ||--o{ test_attempts : "recibe respuestas"
    question_sets ||--o{ test_attempts : "agrupa intentos"
    question_sets }o--|| scoring_rules : "aplica regla de corrección"
    test_sessions ||--o{ test_attempts : "contiene intentos individuales"
    question_topic_links }o--|| ptype : "asocia categoría-bloque-tema"

    ptype {
        int id PK "Identificador único de pregunta"
        text pregunta "Enunciado de la pregunta"
        text respuesta "Texto de la respuesta correcta"
        varchar img_path "Ruta opcional a imagen incrustada"
        text justif "Justificación y explicación razonada"
        varchar categoria "Identificador de categoría/proceso"
        int bloque "Número de bloque temático"
        int tema "Número de tema oficial"
        int anio "Año de convocatoria si aplica"
    }

    incorrectas {
        int id PK "Identificador de opción errónea"
        int id_pregunta FK "Referencia a ptype.id"
        text texto "Texto de la opción incorrecta"
    }

    rtype {
        int id PK "Identificador de ejercicio de relación"
        varchar categoria "Categoría o proceso"
        text concepto_a "Concepto o término de columna A"
        text concepto_b "Definición o pareja de columna B"
    }

    test_sessions {
        varchar test_session_id PK "UUID/identificador único de sesión"
        datetime started_at "Fecha y hora de inicio"
        datetime finished_at "Fecha y hora de conclusión"
        varchar mode "Modo de examen (oficial, tematico, refuerzo)"
        varchar categoria "Categoría evaluada"
    }

    test_attempts {
        int id PK "Identificador de respuesta"
        varchar test_session_id FK "Referencia a sesión"
        int question_id FK "Referencia a ptype.id"
        tinyint is_correct "1 si fue correcta, 0 si incorrecta"
        text selected_answer "Opción elegida por el usuario"
        datetime created_at "Marca de tiempo de la respuesta"
        varchar categoria "Categoría en el momento del test"
        int bloque "Bloque evaluado"
        int tema "Tema evaluado"
    }

    question_sets {
        int id PK "Identificador de conjunto/convocatoria"
        varchar categoria "Nombre clave de categoría"
        varchar organismo "Organismo convocante (AGE, Ayto, etc.)"
        varchar proceso_selectivo "Nombre oficial del proceso"
        int convocatoria_year "Año de la convocatoria"
        varchar turno "Turno (libre, promoción interna)"
        varchar tipo "Tipo (Examen oficial, Práctica)"
        int scoring_rule_id FK "Referencia a scoring_rules"
    }

    scoring_rules {
        int id PK "Identificador de regla"
        varchar code UK "Código de regla (ej: ayto_madrid_aux_tic)"
        varchar name "Nombre descriptivo de la fórmula"
        decimal correct_score "Puntuación otorgada por acierto"
        decimal wrong_penalty "Penalización restada por error"
        decimal blank_score "Puntuación por respuesta en blanco"
        decimal score_scale "Escala final (10, 20, 100)"
        tinyint min_score_zero "1 para truncar a 0 si la nota es negativa"
    }

    question_topic_links {
        varchar categoria "Categoría del examen"
        int bloque "Bloque temático"
        int tema "Tema oficial"
        varchar knowledge_note_id "ID del apunte en knowledge/"
    }
```

### 2.2. Descripción de Tablas

| Tabla | Propósito | Claves / Relaciones |
| :--- | :--- | :--- |
| `ptype` | Tabla principal de preguntas tipo test. Almacena enunciado, respuesta correcta, justificación, imagen opcional, categoría, bloque, tema y año. | PK: `id` |
| `incorrectas` | Opciones de respuesta falsas vinculadas a una pregunta. Número variable de opciones por pregunta. | FK: `id_pregunta` → `ptype.id` |
| `rtype` | Ejercicios de emparejar conceptos (columna A ↔ columna B). Independiente de las preguntas tipo test. | PK: `id` |
| `test_sessions` | Cabecera de cada sesión de examen realizada por el usuario. Registra inicio, fin, modo y categoría. | PK: `test_session_id` (UUID) |
| `test_attempts` | Detalle transaccional: cada respuesta emitida por el usuario durante un test, registrada en tiempo real. | FK: `test_session_id`, `question_id` → `ptype.id` |
| `question_sets` | Definición de convocatorias y conjuntos de examen con su organismo, año, turno y regla de corrección. | FK: `scoring_rule_id` → `scoring_rules.id` |
| `scoring_rules` | Parámetros de corrección: puntuación por acierto, penalización por fallo, escala y truncamiento. | UK: `code` |
| `question_topic_links` | Mapeo relacional de preguntas con bloques y temas teóricos de `knowledge/`. | Compuesta: `categoria` + `bloque` + `tema` |

### 2.3. Exportación y Gestión del Dump Local

El dump real de la base de datos **no se versiona en Git**. Se genera localmente desde la instancia XAMPP/MariaDB y se coloca en:

```text
db/local/001_preparadortai_dump.sql
```

**Comando de exportación** (desde la raíz del repositorio):

```powershell
# Sin contraseña en root:
& "C:\xampp\mysql\bin\mysqldump.exe" -u root --default-character-set=utf8mb4 --databases preparadortai --result-file=".\db\local\001_preparadortai_dump.sql"

# Con contraseña:
& "C:\xampp\mysql\bin\mysqldump.exe" -u root -p --default-character-set=utf8mb4 --databases preparadortai --result-file=".\db\local\001_preparadortai_dump.sql"
```

> [!WARNING]
> No usar redirección con `>` en PowerShell para generar el dump. Windows PowerShell puede escribir el fichero en UTF-16, causando errores `ASCII '\0' appeared in the statement` al importar en Docker.

**Verificación del dump:**

```powershell
Get-Content .\db\local\001_preparadortai_dump.sql -TotalCount 20
```

**Docker — servicios de base de datos:**

| Servicio | URL / Puerto |
| :--- | :--- |
| App PHP legacy | `http://localhost:8080` |
| phpMyAdmin | `http://localhost:8081` |
| MariaDB | `localhost:3307` |

**Reinicialización del volumen Docker** (MariaDB solo importa de `/docker-entrypoint-initdb.d` cuando el volumen está vacío):

```powershell
docker compose down -v
docker compose up --build -d
```

---

## 3. IndexedDB (PreparaTIC V3)

La SPA Vue 3 en `apps/tests_preparatic/v3/index.html` (86.4 MB) contiene **todas las preguntas compiladas como objetos JavaScript inline**. El almacenamiento en el navegador se usa para:

- Intentos de examen realizados por el usuario.
- Estadísticas de rendimiento (evolución temporal, gráfico de radar por bloques).
- Configuración local de preferencias.

> [!NOTE]
> Estos datos son **locales al navegador** y no tienen mecanismo de exportación ni sincronización con MariaDB ni con ningún otro almacén. El historial de intentos en IndexedDB es independiente del historial en `test_attempts` de MariaDB.

---

## 4. Ficheros Markdown (Knowledge Base)

**Ubicación:** `knowledge/**/*.md`

Archivos de texto estructurados organizados jerárquicamente por administración y proceso selectivo:

```text
knowledge/
├── processes/
│   ├── age/
│   │   ├── a1-sti/          # AGE A1 TIC (Sistemas y Tecnologías de la Información)
│   │   └── a2-gsi/          # AGE A2 GSI (Gestión de Sistemas e Informática)
│   │       ├── bloques/     # Bloques I-IV (91 temas)
│   │       ├── supuesto-practico/
│   │       ├── convocatorias/
│   │       └── repaso/
│   ├── comunidad-madrid/
│   │   └── administracion-digital/  # Perfiles P01, P04, P06
│   └── ayto-majadahonda/
├── sources/
│   ├── normativa/           # 54 leyes BOE en JSON estructurado
│   └── glosarios/           # Siglas TIC, CCN-STIC, algoritmos, patrones
└── assets/                  # Imágenes y esquemas referenciados
```

Cada fichero `.md` incluye **frontmatter YAML** con metadatos:

```yaml
---
title: "Tema 12: Contratación Pública Electrónica"
process: age-a2-gsi
official_topic: 12
block: III
tags: [LCSP, contratación, licitación electrónica]
status: reviewed
---
```

Los metadatos son parseados en tiempo de ejecución por `NoteRepository` (PHP) para la navegación facetada y el dashboard de KPIs.

---

## 5. Estructuras Vectoriales e Índices (Study Assistant)

**Ubicación:** `apps/studyassistant/data/`

| Fichero | Formato | Contenido | Tamaño aprox. |
| :--- | :--- | :--- | :--- |
| `knowledge_index.json` | JSON | Índice léxico estructurado de todos los apuntes: ruta, título, proceso, bloque, tags. | ~500 KB |
| `semantic_chunks.json` | JSON | Segmentos textuales divididos por encabezados Markdown. Cada chunk incluye texto, título del apunte y encabezado de sección. | ~5 MB |
| `semantic_embeddings.npy` | NumPy binario | Matriz densa de vectores (dimensión 384) generados con `paraphrase-multilingual-MiniLM-L12-v2`. Una fila por chunk. | ~10 MB |

**Flujo de generación:**

```text
knowledge/**/*.md
    → scripts/build_indexes.py → knowledge_index.json
    → services/embeddings/     → semantic_chunks.json + semantic_embeddings.npy
```

**Consumo en runtime:** El servicio `embeddings` (puerto 8091) carga los 3 ficheros en memoria al arrancar y realiza búsqueda por similitud coseno con producto escalar matricial optimizado en NumPy (< 150 ms en CPU doméstica).

---

## 6. CSVs de PreparaTIC (Banco de Preguntas)

**Ubicación:** `apps/tests_preparatic/data/`

| Fichero | Filas | Descripción |
| :--- | :--- | :--- |
| `Excel_revision_preparatic24.xlsx - Excel_revision_preparatic24.csv` | 10.308 | Banco principal de preguntas PreparaTIC con 22 columnas |
| `Bloques, Temas y temáticas - PROVISIONAL - Bloques.csv` | 8 | Mapeo de bloques A1-A4 y B1-B4 del temario A1 TIC |
| `Bloques, Temas y temáticas - PROVISIONAL - Temas.csv` | Variable | Listado de temas por bloque |
| `Bloques, Temas y temáticas - PROVISIONAL - Tematicas.csv` | Variable | Temáticas transversales |
| `Excel_preguntas_nuevas_preparatic24.xlsx - *.csv` | Variable | Preguntas adicionales de exámenes de años anteriores |

**Esquema del CSV principal** (columnas clave):

| Columna | Tipo | Descripción |
| :--- | :--- | :--- |
| `ID` | Entero | Identificador original en PreparaTIC |
| `PREGUNTA` | Texto | Enunciado de la pregunta |
| `RESPUESTA_A` a `RESPUESTA_D` | Texto | Las 4 opciones de respuesta |
| `RESPUESTA_CORRECTA` | Letra (A-D) | Indicador de la opción correcta |
| `BLOQUE` | Código (A1-B4) | Bloque del temario A1 TIC |
| `TEMAS` | Texto | Puede ser multi-valor separado por comas (ej. `"36,45"`) |
| `EXAMEN` | Texto | Nombre de la convocatoria de origen |
| `ESTADO` | Texto | Estado de revisión |
| `OBSERVACIONES` | Texto | Notas y erratas |
| `AUTOR` | Texto | Autor de la pregunta |
| `PROMOCION` | Texto | Promoción de PreparaTIC |

**Bloques del temario A1 TIC:**

| Código | Rango de temas | Nombre del bloque |
| :--- | :--- | :--- |
| A1 | 1-5 | Organización del Estado y Administración Electrónica |
| A2 | 6-12 | Tecnología básica |
| A3 | 13-18 | Desarrollo de sistemas |
| A4 | 19-23 | Sistemas y comunicaciones |
| B1 | 24-55 | Específicos grupo 1 |
| B2 | 56-80 | Específicos grupo 2 |
| B3 | 81-105 | Específicos grupo 3 |
| B4 | 106-125+ | Específicos grupo 4 |

> [!IMPORTANT]
> Los números de bloque y tema del temario **A1 TIC** (PreparaTIC) son **incompatibles** con los de **TAI** (MariaDB) y con los de **A2 GSI** (AGE). El tema 12 de A1 TIC no es el tema 12 de TAI ni el tema 12 de A2 GSI. Esta incompatibilidad se resuelve en la arquitectura nueva con la tabla `question_syllabus_tags` (ver §9).

---

## 7. SQL de Exámenes Oficiales Importados

**Ubicación:** `imports/age_a2_gsi/generated/`

| Fichero | Preguntas | Descripción |
| :--- | :--- | :--- |
| `import_age_gsi_2024.sql` | ~180 | Examen AGE A2 GSI Libre 2024 — extraído por OCR desde PDF oficial |

**Formato:** INSERTs en el esquema MariaDB de `ptype`:

```sql
INSERT INTO ptype (pregunta, respuesta, justif, img_path, categoria, bloque, tema, anio)
VALUES ('...', '...', '...', NULL, 'AGE A2 GSI LIBRE 2024', 0, 0, 2024);
```

> [!NOTE]
> `bloque=0` y `tema=0` porque las preguntas del examen AGE GSI 2024 **no están categorizadas** por tema del temario. La categorización se hará durante la migración a la nueva arquitectura.

**Pipeline de extracción:** `imports/age_a2_gsi/extractor/extractor.py` usa `pdfplumber` + `pytesseract` para parsear cuadernillos de examen PDF y plantillas de soluciones definitivas, identificando preguntas anuladas.

---

## 8. Reglas de Git para Datos

Los siguientes ficheros **no deben versionarse** en Git:

```text
db/local/*.sql
*.sql
*.dump
*.bak
*.backup
*.sqlite
*.db
```

El directorio `db/local/` se mantiene con un `.gitkeep` para preservar la estructura.

---

## 9. Estado Objetivo (To-Be)

> [!IMPORTANT]
> Pendiente de actualización conforme avance la migración (ver ADR-0001).

La arquitectura nueva (ADR-0001) sustituye los 4 motores de almacenamiento actuales + 2 fuentes de datos por **SQLite (WAL) + sqlite-vec**, con una base de datos independiente por servicio:

| Servicio | Base de datos | Contenido |
| :--- | :--- | :--- |
| `study-assistant` | `study_assistant.sqlite` | Metadatos de notas + embeddings vectoriales (sqlite-vec) |
| `test-engine` | `test_engine.sqlite` | Preguntas unificadas (`questions`, `question_options`, `question_syllabus_tags`, `exams`, `exam_questions`), sesiones e intentos |
| `linking-service` | `linking.sqlite` | Tabla `question_topic_links` |

El esquema normalizado multi-taxonómico del banco de preguntas se detalla en `docs/architecture/ESPECIFICACION_REQUISITOS_Y_ARQUITECTURA.md` §7.4.

---

*Este documento se actualizará conforme avance la migración, documentando el estado Before/After de cada fase.*
