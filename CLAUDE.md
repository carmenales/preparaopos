# PreparaOpos — contexto para asistentes de IA

Lee primero `docs/ESTADO.md` (estado actual y próximos pasos) y `docs/adr/0001-arquitectura-nueva-generacion.md` (arquitectura).

## Reglas de trabajo
- Idioma: español en docs y UI; mensajes de commit en inglés (Conventional Commits).
- GitFlow: `feature/*` desde `develop`; `hotfix/*` solo para bugs de release. Merge a `develop` con `--no-ff`.
- **Antes del primer cambio en ficheros, la rama `feature/*` tiene que existir y estar activa.** Nunca se edita en `develop` ni en `main`: si no hay rama, se crea (o se pide a Carmen) antes de tocar nada.
- Cada propuesta de commits debe cubrir todos los ficheros cambiados; se comprueba con `git status -s` antes de darla.
- **Los commits los hace Carmen con su usuario.** Ninguna IA hace commits ni añade trailers `Co-Authored-By`, IDs de sesión ni otra marca de IA. Las IA proponen el mensaje de commit.
- No matar procesos por PID sin inspeccionarlos antes. No hacer merge, push ni borrar ramas sin petición explícita.
- Las clasificaciones semánticas (pregunta↔tema, pregunta↔apunte) nunca se aplican por umbral: CSV con columna `confirmar` → revisión manual → `apply`.
- Verificar con datos reales (consultas, tests, recuentos) antes de dar algo por hecho.

## Arquitectura (resumen)
Tres servicios FastAPI en capas (presentation / domain / infrastructure), cada uno con su SQLite:
| Servicio | Puerto | Ruta en gateway | BD |
|---|---|---|---|
| study-assistant | 8095 | `/` | índices JSON de `knowledge/` |
| test-engine | 8096 | `/tests/` (`ROOT_PATH=/tests`) | `services/test-engine/data/test_engine.sqlite` |
| linking-service | 8097 | no expuesto | `services/linking-service/data/linking.sqlite` |
Gateway Nginx en :8080 (`infra/gateway/`). Las apps PHP (`apps/studyassistant`, `apps/preparadortai`) siguen vivas hasta verificar los reemplazos (strangler fig).

## Comandos
- Suite completa: `docker compose up -d --build` → http://localhost:8080
- Tests por servicio: `cd services/<servicio> && python -m pytest -q`
- Smoke del gateway: `python scripts/smoke_gateway.py`
- En Docker sobre bind mount de Windows: `SQLITE_JOURNAL_MODE=DELETE` (WAL falla).
