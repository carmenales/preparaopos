# preparaopos

Laboratorio/plataforma para preparación de oposiciones y modernización técnica de bancos de preguntas.

## Aplicaciones

- `apps/preparadortai`: aplicación PHP legacy para tests y preguntas de relación.

## Documentación

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