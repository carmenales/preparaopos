# preparaopos

Laboratorio/plataforma para preparación de oposiciones y modernización técnica de bancos de preguntas.

## Aplicaciones

- `apps/preparadortai`: aplicación PHP legacy para tests y preguntas de relación.
- `apps/studyassistant`: aplicación para consultar, estudiar y realizar búsquedas semánticas sobre los apuntes Markdown ([Arquitectura](apps/studyassistant/ARCHITECTURE.md)).

## Documentación

- [Database setup](docs/database.md)
- [Catálogo de Scripts y Pipelines](scripts/README.md)
- [Arquitectura de Study Assistant](apps/studyassistant/ARCHITECTURE.md)

## Comprobación del entorno Docker

Con los contenedores levantados:

```powershell
.\scripts\check-docker-stack.ps1
```

Si PowerShell bloquea la ejecución de scripts:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\check-docker-stack.ps1
```