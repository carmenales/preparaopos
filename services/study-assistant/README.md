# Study Assistant — Servicio de Visor de Apuntes

Servicio FastAPI que reemplaza al Study Assistant PHP (`apps/studyassistant/`), implementado con estructura DDD (Domain-Driven Design).

## Funcionalidades (Fase 0 — Solo Lectura)

- **Dashboard** con KPIs globales, Process Hub y catálogo de apuntes filtrable
- **Visor de apuntes** con renderizado Markdown enriquecido (LaTeX, Mermaid, Quiz Cards, tablas GFM, callouts)
- **TOC jerárquico** colapsable con navegación por anclas
- **Búsqueda semántica** vectorial (proxy al servicio `embeddings` existente)
- **Servidor de assets** seguro con protección contra Path Traversal
- **Navegación secuencial** (anterior/siguiente) con barra de progreso
- **Enlace a práctica** en Preparador TAI

## Estructura

```
services/study-assistant/
├── main.py                     # Entrypoint FastAPI
├── config.py                   # Configuración (rutas, puertos, URLs)
├── presentation/               # Capa de presentación
│   ├── routes/                 # Endpoints HTTP
│   ├── templates/              # Plantillas Jinja2
│   └── static/                 # CSS y JS
├── domain/                     # Capa de dominio (lógica de negocio pura)
│   ├── notes/                  # Modelos y servicio de notas
│   └── markdown/               # Renderizador Markdown
└── infrastructure/             # Capa de infraestructura
    ├── knowledge_fs/           # Acceso al sistema de ficheros
    └── embeddings/             # Cliente HTTP al servicio de embeddings
```

## Ejecución Local

```powershell
cd services/study-assistant
pip install -r requirements.txt
python main.py
```

El servicio arranca en `http://localhost:8095`.

## Requisitos Previos

1. **Índice de notas generado**: Ejecutar `scripts/build_knowledge_index.py` para generar `apps/studyassistant/data/knowledge_index.json`.
2. **Búsqueda semántica** (opcional): El servicio `embeddings` debe estar corriendo en el puerto 8091 para que la búsqueda semántica funcione.

## Variables de Entorno

| Variable | Default | Descripción |
| :--- | :--- | :--- |
| `KNOWLEDGE_BASE_PATH` | `../../knowledge` | Ruta al directorio de apuntes Markdown |
| `KNOWLEDGE_INDEX_PATH` | `../../apps/studyassistant/data/knowledge_index.json` | Ruta al índice pregenerado |
| `EMBEDDINGS_SERVICE_URL` | `http://localhost:8091` | URL del servicio de embeddings |
| `PREPARADORTAI_BASE_URL` | `http://localhost:8080` | URL del Preparador TAI |
| `SA_HOST` | `0.0.0.0` | Host de escucha |
| `SA_PORT` | `8095` | Puerto de escucha |

## Docker

```powershell
docker build -t study-assistant .
docker run -p 8095:8000 -v ../../knowledge:/app/knowledge:ro study-assistant
```

