# Microservicios de Inteligencia Artificial (services/)

Esta carpeta contiene los microservicios backend contenerizados que proporcionan capacidades de procesamiento de lenguaje natural (NLP), búsqueda semántica vectorial y generación asistida por RAG al ecosistema **preparaopos**.

Para una descripción técnica profunda de los patrones de diseño y flujo de datos, consulta el **[Documento de Arquitectura de Servicios](ARCHITECTURE.md)**.

---

## 1. Catálogo de Servicios

| Directorio | Servicio Docker | Puerto Host | Puerto Interno | Función Principal |
| :--- | :--- | :--- | :--- | :--- |
| **[`embeddings/`](embeddings/)** | `embeddings` | `8091` | `8000` | Búsqueda semántica vectorial local con `Sentence-Transformers` (`MiniLM-L12-v2`) sobre fragmentos de apuntes. |
| **[`knowledge/`](knowledge/)** | `knowledge-service` | `8100` | `8000` | Servicio RAG para la generación asistida de apuntes teóricos a partir de fragmentos y un modelo LLM local en Ollama. |

---

## 2. Arranque y Despliegue con Docker

Ambos servicios se encuentran integrados en el `docker-compose.yml` de la raíz del proyecto.

### Levantar los servicios:
```powershell
# Levantar el servicio de embeddings:
docker compose up -d embeddings

# Levantar el servicio generador de conocimiento:
docker compose up -d knowledge-service

# O levantar toda la pila del repositorio:
docker compose up -d
```

### Comprobación de estado (Healthcheck):

```powershell
# Comprobar servicio de embeddings:
curl http://localhost:8091/health

# Comprobar servicio de generación de conocimiento:
curl http://localhost:8100/health
```

Respuesta esperada de `embeddings`:
```json
{
  "status": "ok",
  "model": "paraphrase-multilingual-MiniLM-L12-v2",
  "indexed_chunks": 1420
}
```

Respuesta esperada de `knowledge-service`:
```json
{
  "status": "ok",
  "service": "knowledge-service"
}
```

---

## 3. Guía Rápida de Uso de los Endpoints

### 3.1. Búsqueda Semántica Vectorial (`embeddings:8000`)

Permite realizar búsquedas por significado en lenguaje natural.

```powershell
curl "http://localhost:8091/search?q=algoritmos+de+cifrado+asimetrico&top_k=3"
```

Estructura de respuesta:
```json
{
  "query": "algoritmos de cifrado asimetrico",
  "results": [
    {
      "note_id": "tema-008-criptografia",
      "note_title": "Criptografía y Seguridad",
      "heading": "Cifrado Asimétrico y Clave Pública",
      "anchor": "cifrado-asimetrico-y-clave-publica",
      "text_preview": "El cifrado asimétrico emplea un par de claves: una pública y otra privada...",
      "score": 0.8421,
      "chunk_id": "tema-008-criptografia::004",
      "tags": ["seguridad", "criptografia", "rsa"]
    }
  ]
}
```

---

### 3.2. Generación Asistida de Apuntes RAG (`knowledge-service:8000`)

Genera un borrador completo de apunte en Markdown con frontmatter YAML garantizado y trazabilidad de los fragmentos utilizados como evidencia.

> [!NOTE]
> Requiere que el servidor Ollama esté ejecutándose en la máquina anfitrión con el modelo `llama3.1:latest` disponible.

```powershell
curl -X POST "http://localhost:8100/notes/generate" `
  -H "Content-Type: application/json" `
  -d '{
    "process_slug": "comunidad-madrid/administracion-digital/tic",
    "topic": "Arquitectura de Datos y Plataformas Big Data",
    "description": "Diferencias clave entre arquitecturas Lambda y Kappa en procesamiento streaming.",
    "top_k": 15,
    "min_score": 0.40
  }'
```

Estructura de respuesta:
```json
{
  "frontmatter": {
    "id": "cm-ad-tic-arquitectura-de-datos-y-plataformas-big-data",
    "title": "Arquitectura de Datos y Plataformas Big Data",
    "official_topic": "Arquitectura de Datos y Plataformas Big Data",
    "processes": ["comunidad-madrid/administracion-digital/tic"],
    "status": "draft",
    "ai_generated": true,
    "needs_human_review": true,
    "source_ids": ["tema-011-arquitectura-de-datos-y-plataformas"],
    "generator_model": "llama3.1:latest",
    "fragment_count": 8
  },
  "markdown_body": "## Arquitectura Lambda vs Kappa\n\n...",
  "full_markdown": "---\nid: ...\n---\n\n## Arquitectura Lambda...",
  "fragments_used": [ ... ],
  "warnings": []
}
```

---

## 4. Reindexación de Vectores

Cada vez que se añadan, modifiquen o reorganicen apuntes en `knowledge/**/*.md`, debe actualizarse el índice de fragmentos y vectores:

```powershell
# 1. Ejecutar el script de indexación dentro del contenedor embeddings
docker compose exec embeddings python scripts/build_semantic_index.py

# 2. Reiniciar el contenedor para recargar la matriz en memoria
docker compose restart embeddings
```

---

## 5. Índice de Documentación de Servicios

* 📄 **[Documento de Arquitectura de Servicios](ARCHITECTURE.md)**: Flujos RAG, modelos Pydantic, inferencia en CPU y diagramas Mermaid.
* 📄 **[`embeddings/README.md`](embeddings/README.md)**: Documentación específica del microservicio vectorial.
* 📄 **[`knowledge/README.md`](knowledge/README.md)**: Documentación específica del servicio de generación de apuntes.

