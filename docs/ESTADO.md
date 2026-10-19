# Estado del proyecto

_Última revisión: 2026-10-19 · rama `feature/cross-navigation-in-ui` (`c7d76832`), 14 commits por delante de `develop`._

## Hecho y verificado
- **test-engine**: 18.112 preguntas (PreparaTIC A1 16.680, TAI legacy, AGE GSI 2024 con 101). 1.268 pendientes de clasificar (1.267 TAI + la 18110 de reserva GSI). ScoringService (Decimal, A−F/3, 2 decimales ROUND_HALF_UP, anuladas fuera del denominador), sesiones práctica/simulacro con expiración en servidor, práctica por apunte (`source="note"`).
- **linking-service**: enlaces apunte↔pregunta para el piloto GSI 2024 (confianza 1.0 un match / 0.8 varios). Degradación elegante si no responde.
- **Navegación cruzada** study-assistant ↔ test-engine y **gateway Nginx** :8080.
- Tests (2026-10-19): test-engine 26/26, linking-service 5/5, study-assistant 4/4. La BD real de test-engine no cambia al ejecutarlos (MD5 idéntico antes y después).

## Corregido el 2026-10-19 (pendiente de commit)
- `tests/conftest.py` de test-engine estaba vacío en git: los tests escribían en la BD real. Ahora copia la BD (con sus `-journal`/`-wal`/`-shm`) a un directorio temporal antes de importar `config`, y un fixture comprueba que no se usa la BD real.
- `engine.py`: el fallo o la discrepancia de `journal_mode` se registra como WARNING con el modo pedido y el efectivo.
- Enlaces entre servicios en la barra superior: ya no se escriben a mano (`/` y `/tests/`); salen de `STUDY_ASSISTANT_PUBLIC_URL` y `TEST_ENGINE_PUBLIC_URL`. Antes, test-engine ejecutándose solo en :8096 enviaba «Volver a Apuntes» a su propio catálogo.
- `.gitattributes` (LF) y `*.sqlite-journal` en `.gitignore`.

## Antes de mergear a `develop`
1. Ejecutar `python scripts/smoke_gateway.py` con `docker compose up -d --build`.
2. Limpiar las sesiones y los intentos creados por tests en `test_engine.sqlite`: 441 sesiones y 2.496 intentos desde el 3-oct. Antes, hacer copia con la API de backup. El `.bak` del 16-oct también está contaminado.

## Pendiente menor
- `docker-compose.dev.yml` está vacío (0 bytes): rellenar u eliminar.
- `scripts/backup_test_engine.py`: API de backup de SQLite, carpeta `backups/` ignorada y fuera del bind mount, retención 14, `PRAGMA integrity_check` tras copiar.
- Ficheros sueltos: `ultimos_commits.txt`, `…/02_Metodologia_Proyecto copy.md`.
- Untracked de `knowledge/` (a1-sti, a2-gsi/apuntes, mapping, majadahonda, p06): decidir qué se versiona (el repo es privado).

## Después
1. Simulacro completo manual por :8080. Luego tag/release y usar el sistema unos días.
2. Backlog: Alembic; catálogo histórico de exámenes y selector por bloque/tema; rediseño UI/UX; 1.267 preguntas TAI pendientes (necesitan apuntes `c1-tai`/`a1-sti`); linking para otros temarios; revisión de apuntes en borrador (#42); UX de enlaces 1-a-varios; `lifespan` en vez de `on_event`; proveedores de IA opcionales (Gemini/Obsidian/Notion).
