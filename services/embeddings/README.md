# Microservicio de Embeddings y Búsqueda Semántica (`services/embeddings`)

Microservicio FastAPI que carga el modelo multilingüe de representación vectorial densa y ofrece búsqueda semántica sobre los apuntes de `knowledge/` sin depender de GPUs dedicadas ni de APIs de pago externas.

---

## 1. Características Técnicas

* **Framework:** FastAPI / Uvicorn sobre Python 3.11.
* **Modelo NLP:** `paraphrase-multilingual-MiniLM-L12-v2` (Sentence-Transformers).
* **Dimensiones del embedding:** 384 dimensiones.
* **Inferencia y Similitud:**
  * Inferencia local optimizada para CPU.
  * Carga estática de fragmentos precomputados (`apps/studyassistant/data/semantic_chunks.json`) y matriz normalizada (`apps/studyassistant/data/semantic_embeddings.npy`).
  * Similitud coseno calculada mediante multiplicación matricial NumPy de alta velocidad: $\text{scores} = \mathbf{E} \cdot \mathbf{q}$.
* **Puerto interno Docker:** `8000`.
* **Puerto mapeado en host:** `8091`.

---

## 2. Endpoints de la API

### `GET /health`
Devuelve el estado de disponibilidad del servicio y la cantidad de fragmentos actualmente cargados en memoria.

**Respuesta:**
```json
{
  "status": "ok",
  "model": "paraphrase-multilingual-MiniLM-L12-v2",
  "indexed_chunks": 1420
}
```

### `GET /search?q={query}&top_k={top_k}`
Realiza la búsqueda semántica vectorial para la cadena de texto `q`.

**Parámetros:**
* `q` (requerido, string): Texto o pregunta de búsqueda en lenguaje natural.
* `top_k` (opcional, entero de 1 a 50, por defecto 8): Número máximo de resultados a retornar.

**Respuesta:**
```json
{
  "query": "cifrado simetrico vs asimetrico",
  "results": [
    {
      "note_id": "tema-008-criptografia",
      "note_title": "Criptografía",
      "heading": "Tipos de Cifrado",
      "anchor": "tipos-de-cifrado",
      "text_preview": "En el cifrado simétrico se usa una clave compartida...",
      "score": 0.8123,
      "chunk_id": "tema-008-criptografia::002",
      "source_id": "tema-008-criptografia",
      "content": "...",
      "tags": ["seguridad", "criptografia"]
    }
  ]
}
```

---

## 3. Regenerar el Índice Semántico

Cuando se actualicen los apuntes en `knowledge/`, se debe reconstruir el índice de vectores:

```powershell
# Ejecutar dentro del contenedor embeddings (tiene sentence-transformers instalado):
docker compose exec embeddings python scripts/build_semantic_index.py

# Reiniciar el contenedor para recargar la memoria:
docker compose restart embeddings
```

---

## 4. Documentación Relacionada

* 📄 **[Arquitectura de Servicios](../ARCHITECTURE.md)**: Flujos de datos y diseño global.
* 📄 **[Study Assistant](../../apps/studyassistant/ARCHITECTURE.md)**: Aplicación web cliente que consume este servicio a través de `search.php`.

