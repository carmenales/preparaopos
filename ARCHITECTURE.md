# Arquitectura General del Sistema Preparaopos

Documento técnico de arquitectura global del repositorio **preparaopos**, una plataforma integral diseñada para la preparación de oposiciones tecnológicas mediante aplicaciones interactivas, bases de conocimiento estructuradas en Markdown, modelos locales de inteligencia artificial y búsqueda semántica vectorial.

---

## 1. Principios de Diseño y Filosofía del Sistema

El ecosistema **preparaopos** se rige por cuatro principios fundamentales:

1. **Local-First y Cero Costes de Nube (Zero-Cloud-Cost):**
   Tanto los modelos de embeddings (`sentence-transformers`) como los modelos generativos de lenguaje (LLMs vía Ollama) se ejecutan 100% en infraestructura local (CPU/GPU local). No existen suscripciones externas, costes por token ni exposición de datos privados a APIs de terceros.
2. **Git como Única Fuente de Verdad para el Conocimiento:**
   Los apuntes teóricos no se almacenan como blobs en una base de datos relacional, sino como archivos Markdown (`knowledge/**/*.md`) versionados en Git con metadatos estructurados en YAML frontmatter. Esto permite control de versiones diff, edición colaborativa y legibilidad humana universal.
3. **Desacoplamiento Funcional en Monorepo:**
   El repositorio agrupa aplicaciones web especializadas, microservicios de IA, scripts de procesamiento y esquemas de base de datos en un único monorepo coordinado, comunicados mediante contratos ligeros de URLs y APIs REST internas.
4. **Resiliencia Operativa:**
   Las aplicaciones web cliente (`preparadortai` y `studyassistant`) son completamente funcionales de forma autónoma. Si los microservicios de IA o búsqueda semántica están detenidos, las aplicaciones degradan su funcionalidad de forma elegante sin interrumpir el estudio.

---

## 2. Mapa Global de la Arquitectura

```mermaid
flowchart TD
    subgraph Cliente["Capa Cliente (Navegador Web)"]
        User["Opositor / Estudiante"]
        BrowserUI["Interfaz Web (HTML5 / Bootstrap 5 / CSS Moderno)"]
        ClientLibs["MathJax v3 (LaTeX) · Mermaid.js v10 · Fetch API"]
    end

    subgraph Frontends["Capa de Aplicaciones Web (apps/)"]
        TAI_App["apps/preparadortai (Puerto 8080)<br>PHP 8.2 / Apache<br>Tests, Simulacros, Métricas y Exámenes"]
        Study_App["apps/studyassistant (Puerto 8090)<br>PHP 8.2<br>Visor Markdown, TOC Anidado y Búsqueda"]
        Shared_Lib["apps/shared (Volumen Compartido)<br>Configuración de Rutas y Helpers de Enlace"]
    end

    subgraph Microservicios["Capa de Servicios de Inteligencia Artificial (services/)"]
        Embeddings_Svc["services/embeddings (Puerto 8091:8000)<br>FastAPI / Python 3.11<br>Modelo MiniLM L12 v2 (CPU)"]
        Knowledge_Svc["services/knowledge (Puerto 8100:8000)<br>FastAPI / Python 3.11<br>Generador RAG Asistido"]
        Ollama_Host["Ollama en Host (Puerto 11434)<br>Modelos: llama3.1, etc."]
    end

    subgraph Almacenamiento["Capa de Almacenamiento y Persistencia"]
        DB_MariaDB[(MariaDB 10.4: preparadortai<br>Puerto 3307:3306<br>Preguntas, Intentos, Sesiones, Reglas)]
        PMA["phpMyAdmin (Puerto 8081)<br>Gestión Visual de Base de Datos"]
        FS_Knowledge["knowledge/**/*.md<br>Apuntes Teóricos con Frontmatter"]
        FS_Data["apps/studyassistant/data/<br>Índices JSON y Matriz de Embeddings .npy"]
    end

    subgraph Pipelines["Capa de Pipelines de Procesamiento (scripts/)"]
        Ingestion["Ingesta y Extracción (batch_extract.py, PyMuPDF, PPTX)"]
        CleanRefine["Normalización y Refinado (normalize_markdown.py, LLM)"]
        NLP_Tags["Enriquecimiento NLP (extract_tags.py con spaCy)"]
        Indexers["Indexación (build_knowledge_index.py, build_semantic_index.py)"]
        Linkers["Enlace Semántico (suggest_topic_links.py)"]
    end

    %% Relaciones Cliente
    User --> BrowserUI
    BrowserUI --> ClientLibs
    BrowserUI -->|HTTP 8080| TAI_App
    BrowserUI -->|HTTP 8090| Study_App
    BrowserUI -->|HTTP 8081| PMA

    %% Relaciones Frontends
    TAI_App -->|mysqli TCP 3306| DB_MariaDB
    TAI_App -->|require_once| Shared_Lib
    Study_App -->|require_once| Shared_Lib
    Study_App -->|Lectura directa :ro| FS_Knowledge
    Study_App -->|Lectura directa| FS_Data
    Study_App -->|Proxy HTTP /search| Embeddings_Svc

    %% Interoperabilidad entre Apps
    Study_App -.->|"Enlace canónico: Ponerme a prueba"| TAI_App
    TAI_App -.->|"Enlace canónico: Repasar apunte"| Study_App

    %% Relaciones Microservicios
    Embeddings_Svc -->|Carga en memoria| FS_Data
    Knowledge_Svc -->|Consulta vectorial /search| Embeddings_Svc
    Knowledge_Svc -->|Generación vía API /api/generate| Ollama_Host
    PMA -->|TCP 3306| DB_MariaDB

    %% Relaciones Pipelines
    Ingestion --> CleanRefine
    CleanRefine --> NLP_Tags
    NLP_Tags --> FS_Knowledge
    FS_Knowledge --> Indexers
    Indexers --> FS_Data
    Linkers -->|Consulta semántica| Embeddings_Svc
    Linkers -->|Lectura/Escritura enlaces| DB_MariaDB
```

---

## 3. Topología de Contenedores y Red (`docker-compose.yml`)

El entorno de ejecución completo se orquesta mediante **Docker Compose**:

| Servicio | Contenedor | Imagen / Dockerfile | Puerto Host | Puerto Red Docker | Propósito y Responsabilidad |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`web`** | `preparaopos-preparadortai-web` | `infra/docker/php/Dockerfile` (PHP 8.2 + Apache) | `8080` | `80` | Servidor web de la aplicación interactiva de exámenes **Preparador TAI**. |
| **`studyassistant`** | `preparaopos-studyassistant-web` | `infra/docker/php/Dockerfile` (PHP 8.2 integrado) | `8090` | `8080` | Servidor web del visor de apuntes y catálogo **Study Assistant**. |
| **`embeddings`** | `preparaopos-embeddings` | `infra/docker/embeddings/Dockerfile` (Python 3.11) | `8091` | `8000` | Microservicio FastAPI de búsqueda semántica vectorial en local. |
| **`knowledge-service`** | `preparaopos-knowledge-service` | `services/knowledge/Dockerfile` (Python 3.11) | `8100` | `8000` | Microservicio RAG para generación asistida de contenido con Ollama. |
| **`db`** | `preparaopos-preparadortai-db` | `mariadb:10.4` | `3307` | `3306` | Base de datos relacional del banco de preguntas y sesiones. |
| **`phpmyadmin`** | `preparaopos-preparadortai-phpmyadmin` | `phpmyadmin:5` | `8081` | `80` | Interfaz web de administración de la base de datos MariaDB. |

### Medidas de Seguridad y Aislamiento de Volúmenes:
* **Volúmenes de sólo lectura (`:ro`):**
  * `knowledge/` se monta estrictamente como `:ro` en `studyassistant` y en `embeddings`, evitando cualquier posibilidad de sobreescritura accidental o maliciosa desde la web.
  * `apps/shared/` se monta como `:ro` en ambas aplicaciones web para asegurar un contrato inmutable en tiempo de ejecución.
* **Privilegios de Contenedor:**
  * El contenedor `studyassistant` opera bajo el usuario sin privilegios `www-data` y con la directiva de seguridad `security_opt: no-new-privileges:true`.
* **Conexión con el Host:**
  * El contenedor `knowledge-service` se comunica con el servidor Ollama que corre en la máquina anfitrión a través de `host.docker.internal:11434` mediante la directiva `extra_hosts`.

---

## 4. Estructura de Directorios del Monorepo

```text
preparaopos/
├── apps/                          # Aplicaciones de usuario final
│   ├── preparadortai/             # Plataforma de tests y exámenes (PHP + MariaDB)
│   ├── studyassistant/            # Visor y buscador de apuntes Markdown (PHP + JS)
│   └── shared/                    # Configuración común y generadores de URLs canónicas
│
├── services/                      # Microservicios auxiliares contenerizados
│   ├── embeddings/                # API FastAPI de búsqueda vectorial (Sentence-Transformers)
│   └── knowledge/                 # Servicio RAG de generación y explotación de conocimiento
│
├── knowledge/                     # Base de conocimiento central en Markdown
│   ├── _template/                 # Plantillas formales de apuntes
│   ├── processes/                 # Apuntes organizados por proceso / perfil / apuntes
│   └── sources/                   # Fuentes de origen (PDFs de leyes, manuales, etc.)
│
├── scripts/                       # Pipelines de ingesta, NLP, indexación y mantenimiento
├── db/                            # Base de datos relacional
│   ├── migrations/                # Migraciones SQL versionadas
│   └── local/                     # Dumps de inicialización local (ignorados en Git)
│
├── infra/                         # Dockerfiles de soporte
│   └── docker/
│       ├── php/                   # Entorno PHP 8.2 con extensiones PDO y MySQLi
│       └── embeddings/            # Entorno Python 3.11 con PyTorch y Transformers
│
├── docker-compose.yml             # Orquestación de contenedores y redes
└── ARCHITECTURE.md                # Este documento de arquitectura global
```

---

## 5. Descripción de los Subsistemas Principales

### 5.1. Preparador TAI (`apps/preparadortai`)
* **Rol:** Sistema de evaluación, entrenamiento y administración del banco de preguntas.
* **Capacidades:**
  * Tests aleatorios, tests por bloque/tema, exámenes de convocatorias oficiales con temporizador, práctica de preguntas falladas (*banco de errores*) y relación de conceptos.
  * Persistencia asíncrona de intentos en MariaDB (`test_attempts` y `test_sessions`).
  * Panel estadístico avanzado con soporte para reglas de puntuación oficiales parametrizables (`scoring_rules`).
* **Documentación específica:** [`apps/preparadortai/ARCHITECTURE.md`](file:///c:/repositories/preparaopos/apps/preparadortai/ARCHITECTURE.md).

### 5.2. Study Assistant (`apps/studyassistant`)
* **Rol:** Visor interactivo y catálogo de la base de conocimiento teórico.
* **Capacidades:**
  * Catálogo de apuntes con filtrado rápido en memoria sobre `knowledge_index.json` (por texto, etiqueta, proceso y estado).
  * Renderizador Markdown propio ultraligero que soporta fórmulas matemáticas $\LaTeX$ (MathJax), diagramas Mermaid.js, tarjetas interactivas de cuestionarios tipo test y callouts.
  * Tabla de contenidos (TOC) multinivel y colapsable (`h2` a `h4`).
  * Búsqueda semántica interactiva en lenguaje natural conectada al microservicio de embeddings.
* **Documentación específica:** [`apps/studyassistant/ARCHITECTURE.md`](file:///c:/repositories/preparaopos/apps/studyassistant/ARCHITECTURE.md).

### 5.3. Capa de Interoperabilidad (`apps/shared`)
* **Rol:** Puente de comunicación desacoplado entre las aplicaciones web.
* **Capacidades:**
  * Centralización de puertos y dominios en `config/apps.php`.
  * Helpers canónicos en `helpers/url.php` para generar enlaces parametrizados entre el estudio teórico y la práctica de tests.
* **Documentación específica:** [`apps/shared/ARCHITECTURE.md`](file:///c:/repositories/preparaopos/apps/shared/ARCHITECTURE.md).

### 5.4. Microservicio de Embeddings (`services/embeddings`)
* **Rol:** Inferencia vectorial y cálculo de similitud para búsqueda por significado.
* **Capacidades:**
  * Utiliza el modelo multilingüe `paraphrase-multilingual-MiniLM-L12-v2` (384 dimensiones).
  * Carga en el arranque los fragmentos (`semantic_chunks.json`) y la matriz densa normalizada (`semantic_embeddings.npy`).
  * Computa similitud coseno en microsegundos mediante multiplicación matricial NumPy en CPU: $\text{scores} = \mathbf{E} \cdot \mathbf{q}$.

### 5.5. Microservicio de Generación RAG (`services/knowledge`)
* **Rol:** Generación asistida de nuevos apuntes de estudio y síntesis de contenidos.
* **Capacidades:**
  * Combina búsqueda vectorial sobre el microservicio `embeddings` con inferencia de modelos LLM locales a través de Ollama.
  * Recupera fragmentos relevantes (`TopicRetriever`), redacta el borrador del apunte (`NoteGenerator`) y genera el frontmatter YAML estandarizado de forma determinista (`FrontmatterGenerator`).

### 5.6. Pipelines y Scripts (`scripts/`)
* **Rol:** Cadena de procesamiento de datos por lotes e indexación.
* **Capacidades:**
  * Ingesta y conversión de PDFs y PPTX a Markdown limpio (`batch_extract.py`, `extract_pdf_text.py`, `extract_pptx_text.py`, `normalize_markdown.py`).
  * Refinado ortotipográfico con LLM local y caché SHA-256 (`refine_markdown_llm.py`).
  * Extracción de etiquetas por NLP con spaCy (`extract_tags.py`).
  * Generación de índices léxicos y semánticos (`build_knowledge_index.py`, `build_semantic_index.py`).
  * Enlace inteligente entre preguntas y apuntes (`suggest_topic_links.py`).
* **Documentación específica:** [`scripts/README.md`](file:///c:/repositories/preparaopos/scripts/README.md).

---

## 6. Flujos de Datos Transversales End-to-End

### 6.1. Ciclo de Vida del Conocimiento: De PDF a Consulta Semántica

```mermaid
sequenceDiagram
    autonumber
    actor Admin as Administrador / Opositor
    participant Batch as scripts/batch_extract.py
    participant Normalize as scripts/normalize_markdown.py
    participant Ollama as Ollama Local (LLM)
    participant KnowledgeRepo as knowledge/**/*.md
    participant Indexer as scripts/build_semantic_index.py
    participant EmbeddingsSvc as services/embeddings
    participant StudyUI as Study Assistant (Web)

    Admin->>Batch: Ejecuta extracción sobre temarios en PDF
    Batch->>Normalize: Convierte a texto plano y normaliza tablas/siglas
    Normalize->>Ollama: Refina sintaxis y repara párrafos (vía LLM)
    Ollama-->>Normalize: Markdown estructurado
    Normalize->>KnowledgeRepo: Almacena apunte final con Frontmatter YAML
    Admin->>Indexer: Ejecuta indexación semántica en contenedor
    Indexer->>Indexer: Trocea por headings y genera vectores (MiniLM)
    Indexer-->>EmbeddingsSvc: Actualiza semantic_chunks.json y semantic_embeddings.npy
    EmbeddingsSvc->>EmbeddingsSvc: Recarga matriz y normaliza en memoria
    Admin->>StudyUI: Busca "arquitectura lambda vs kappa"
    StudyUI->>EmbeddingsSvc: Consulta HTTP /search
    EmbeddingsSvc-->>StudyUI: Resultados con % de similitud y anclas directas
```

### 6.2. Ciclo de Aprendizaje Activo: Estudio $\leftrightarrow$ Práctica de Examen

```mermaid
sequenceDiagram
    autonumber
    actor Alumno as Opositor
    participant Study as Study Assistant (note.php)
    participant Shared as apps/shared/helpers/url.php
    participant TAI as Preparador TAI (practica_tematica.php)
    participant DB as MariaDB (test_attempts)

    Alumno->>Study: Lee apunte "Tema 11: Arquitectura de Datos"
    Study->>Shared: build_preparadortai_topic_practice_url(["Tema 11"])
    Shared-->>Study: URL "practica_tematica.php?topics=Tema+11&source=studyassistant"
    Study-->>Alumno: Muestra botón "📝 Ponerme a prueba"
    Alumno->>TAI: Clic en el botón
    TAI->>DB: Carga preguntas vinculadas a la categoría y tema
    TAI-->>Alumno: Inicia examen temático focalizado
    Alumno->>TAI: Responde preguntas y concluye sesión
    TAI->>DB: Guarda métricas de acierto/fallo y tiempo
    TAI-->>Alumno: Presenta resultados con opción de relectura del apunte
```

---

## 7. Índice de Documentación de Arquitectura

Para consultar los detalles técnicos de bajo nivel de cada componente, recurra a los documentos específicos del repositorio:

* 📄 **Preparador TAI:** [`apps/preparadortai/ARCHITECTURE.md`](file:///c:/repositories/preparaopos/apps/preparadortai/ARCHITECTURE.md)
* 📄 **Study Assistant:** [`apps/studyassistant/ARCHITECTURE.md`](file:///c:/repositories/preparaopos/apps/studyassistant/ARCHITECTURE.md)
* 📄 **Capa Compartida:** [`apps/shared/ARCHITECTURE.md`](file:///c:/repositories/preparaopos/apps/shared/ARCHITECTURE.md)
* 📄 **Scripts y Pipelines:** [`scripts/README.md`](file:///c:/repositories/preparaopos/scripts/README.md)
* 📄 **Base de Datos y Configuración:** [`docs/database.md`](file:///c:/repositories/preparaopos/docs/database.md)

