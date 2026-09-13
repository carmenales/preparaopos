# Microservicio de Generación de Conocimiento RAG (`services/knowledge`)

Microservicio FastAPI que implementa la generación asistida de apuntes teóricos de oposición a partir de fragmentos de referencia recuperados vectorialmente, orquestando llamadas al modelo LLM local ejecutado en Ollama.

---

## 1. Características Técnicas

* **Framework:** FastAPI / Uvicorn sobre Python 3.11.
* **Diseño Ligero:** No instala librerías pesadas de ML (`torch` o `transformers`). Se comunica con `services/embeddings` vía HTTP para la recuperación vectorial y con Ollama para la síntesis textual.
* **Seguridad:** Contenedor ejecutado bajo usuario sin privilegios (`appuser`).
* **Determinismo de Metadatos:** El frontmatter YAML es generado mediante código estructurado (`frontmatter_generator.py`), impidiendo que el LLM modifique metadatos críticos o alucine identificadores.
* **Puerto interno Docker:** `8000`.
* **Puerto mapeado en host:** `8100`.

---

## 2. Endpoints de la API

### `GET /health`
Comprueba que el microservicio está en funcionamiento.

**Respuesta:**
```json
{
  "status": "ok",
  "service": "knowledge-service"
}
```

### `POST /notes/generate`
Genera una **vista previa** de un apunte completo estructurado. No escribe directamente a disco.

**Cuerpo de la petición (JSON):**
```json
{
  "process_slug": "comunidad-madrid/administracion-digital/tic",
  "topic": "Arquitecturas de Streaming y Procesamiento en Tiempo Real",
  "description": "Comparativa entre Apache Kafka, Apache Flink y conceptos de procesamiento distribuido.",
  "top_k": 20,
  "min_score": 0.35
}
```

**Flujo interno ejecutado:**
1. `TopicRetriever` consulta a `http://embeddings:8000/search` con el tema y la descripción.
2. Filtra fragmentos con similitud inferior a `min_score` y elimina redundancias.
3. `NoteGenerator` construye el prompt estricto con los fragmentos de evidencia (`prompts/note_generation.txt`) y solicita al modelo LLM (`llama3.1:latest`) la redacción del cuerpo del apunte en Markdown.
4. `FrontmatterGenerator` construye de forma determinista el bloque YAML completo (ID, título, proceso, tags agregadas, marcas de revisión humana).
5. Devuelve el objeto `GenerateNotePreview`.

**Respuesta (JSON):**
```json
{
  "frontmatter": {
    "id": "cm-ad-tic-arquitecturas-de-streaming-y-procesamiento-en-tiempo-real",
    "title": "Arquitecturas de Streaming y Procesamiento en Tiempo Real",
    "official_topic": "Arquitecturas de Streaming y Procesamiento en Tiempo Real",
    "processes": [
      "comunidad-madrid/administracion-digital/tic"
    ],
    "status": "draft",
    "created_at": "2026-09-13",
    "ai_generated": true,
    "needs_human_review": true,
    "source_ids": [
      "tema-011-arquitectura-de-datos-y-plataformas"
    ],
    "generator_model": "llama3.1:latest",
    "fragment_count": 6
  },
  "markdown_body": "## Conceptos de Procesamiento en Streaming\n\n...",
  "full_markdown": "---\nid: ...\n---\n\n## Conceptos...",
  "fragments_used": [ ... ],
  "warnings": []
}
```

---

## 3. Variables de Entorno y Configuración

| Variable | Valor por Defecto | Descripción |
| :--- | :--- | :--- |
| `SEARCH_SERVICE_URL` | `http://embeddings:8000` | URL interna de red Docker hacia el microservicio de búsqueda vectorial. |
| `OLLAMA_URL` | `http://host.docker.internal:11434` | Dirección para conectar con el servidor Ollama instalado en la máquina anfitrión. |
| `OLLAMA_MODEL` | `llama3.1:latest` | Modelo de lenguaje local utilizado para la redacción. |
| `OLLAMA_READ_TIMEOUT_SECONDS` | `600.0` | Tiempo de espera máximo para respuestas de texto extensas. |
| `NOTE_GENERATION_TOP_K` | `20` | Cantidad máxima de fragmentos a recuperar como contexto. |
| `NOTE_GENERATION_MIN_SCORE` | `0.35` | Puntuación mínima de similitud coseno para incorporar un fragmento. |

---

## 4. Documentación Relacionada

* 📄 **[Arquitectura de Servicios](../ARCHITECTURE.md)**: Flujos RAG, modelos Pydantic y diagramas de secuencia.
* 📄 **[Microservicio de Embeddings](../embeddings/README.md)**: Proveedor de la búsqueda vectorial.
* 📄 **[Arquitectura General del Repositorio](../../ARCHITECTURE.md)**: Visión global del ecosistema.

