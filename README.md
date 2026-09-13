# preparaopos

Laboratorio/plataforma para preparación de oposiciones y modernización técnica de bancos de preguntas.

## Aplicaciones

- `apps/preparadortai`: aplicación interactiva para tests, simulacros y banco de preguntas ([Arquitectura](apps/preparadortai/ARCHITECTURE.md)).
- `apps/studyassistant`: aplicación para consultar, estudiar y realizar búsquedas semánticas sobre los apuntes Markdown ([Arquitectura](apps/studyassistant/ARCHITECTURE.md)).
- `apps/shared`: librería compartida de configuración y generadores de URLs canónicas inter-aplicación ([Arquitectura](apps/shared/ARCHITECTURE.md)).

## Servicios Backend (IA y NLP)

- `services/embeddings`: microservicio de búsqueda semántica vectorial local con `Sentence-Transformers` ([README](services/embeddings/README.md)).
- `services/knowledge`: microservicio RAG para generación asistida de apuntes con Ollama ([README](services/knowledge/README.md)).
- Guía y arquitectura: [Catálogo de Servicios](services/README.md) · [Arquitectura de Servicios](services/ARCHITECTURE.md).

## Documentación

- [Arquitectura General del Sistema](ARCHITECTURE.md)
- [Arquitectura de Preparador TAI](apps/preparadortai/ARCHITECTURE.md)
- [Arquitectura de Study Assistant](apps/studyassistant/ARCHITECTURE.md)
- [Arquitectura de Apps Shared](apps/shared/ARCHITECTURE.md)
- [Arquitectura de Microservicios (services/)](services/ARCHITECTURE.md)
- [Catálogo de Microservicios](services/README.md)
- [Catálogo de Scripts y Pipelines](scripts/README.md)
- [Database setup](docs/database.md)

## Comprobación del entorno Docker

Con los contenedores levantados:

```powershell
.\scripts\check-docker-stack.ps1
```

Si PowerShell bloquea la ejecución de scripts:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\check-docker-stack.ps1
```