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
- `scripts/backup_test_engine.py` (API de backup, `integrity_check`, retención 14, en `backups/`, ignorada por git) y `scripts/purge_test_sessions.py` (simulación por defecto, `--before`, copia previa obligatoria).

## Antes de mergear a `develop`
1. ~~Smoke del gateway~~: OK al 100 % el 2026-10-19. Ojo: los pasos 5 y 6 crean sesiones reales en la BD.
2. Purgar las sesiones creadas por tests y por el smoke: `docker compose stop test-engine` → `python scripts/purge_test_sessions.py --apply` → `docker compose start test-engine`. La purga hace antes una copia verificada en `backups/test-engine/`.

## Pendiente menor
- `docker-compose.dev.yml` está vacío (0 bytes): rellenar u eliminar.
- Smoke test: marcar sus sesiones (p. ej. `source_ref='smoke'`) o limpiarlas al terminar, para que no se mezclen con el uso real.
- Ficheros sueltos: `ultimos_commits.txt`, `…/02_Metodologia_Proyecto copy.md`.
- Untracked de `knowledge/` (a1-sti, a2-gsi/apuntes, mapping, majadahonda, p06): decidir qué se versiona (el repo es privado).

## Paso 1 de la migración (rama `feature/preparatic-year-metadata`)
- `questions.year` y `questions.is_official_exam`. `init_schema` añade las columnas que falten en BD existentes (`ensure_additive_columns`, solo aditivo).
- `scripts/etl/backfill_preparatic_metadata.py` rellena las 16.680 preguntas de PreparaTIC desde el bundle (simulación por defecto y copia previa). Probado sobre una copia de la BD real: el resto de tablas y columnas no cambia.
- `import_preparatic.py` guarda ya ambos campos en importaciones nuevas.

## Paso 2 de la migración (rama `feature/import-local-exams`)
- `scripts/etl/mysql_dump_parser.py`: lector de los SQL de MariaDB de `imports/` (sin ejecutarlos).
- `scripts/etl/import_local_exams.py`: 708 preguntas en 12 exámenes y 4 temarios nuevos, con el orden original de las opciones, año y marca de examen oficial, pendientes de clasificar. Validación por defecto, copia previa, todo o nada e idempotente. Probado sobre una copia de la BD real: los datos existentes no cambian y la app abre y puntúa los exámenes nuevos.
- Bug detectado, fuera de este paso: en TAI y en GSI 2024 la opción correcta es siempre la primera (ver `docs/MIGRACION.md`, «Incidencias de datos»).

## Corrección del orden de opciones (rama `feature/fix-option-order`)
- `scripts/etl/option_order.py`: orden oficial a partir de las letras de las justificaciones, o barajado determinista cuando no hay orden original.
- `scripts/etl/fix_option_order.py`: corrige la BD existente (solo `display_order` de GSI 2024 y TAI). Simulación por defecto, copia previa, verificación contra el JSON oficial e idempotente. Los intentos no se ven afectados porque guardan el id de la opción, no su posición.
- `import_age_gsi_2024.py` e `import_tai_mariadb.py` insertan ya ese mismo orden (verificado: 101/101 y 1.331/1.331).

## CI (fuera de alcance; anotado)
- `ci.yml` hace `curl localhost:8080/assets/css/style.css` esperando preparadortai, pero ahora el 8080 es el gateway Nginx (preparadortai está en el 8082).
- La CI solo ejecuta `unittest discover -s tests`; los tests de `services/*` (pytest) no corren en CI.

## Después
La migración no está completa: ver `docs/MIGRACION.md` (datos sin importar, funcionalidades de las apps PHP sin equivalente y criterios para etiquetar la versión).

1. Simulacro completo manual por :8080. Luego tag/release y usar el sistema unos días.
2. Backlog: Alembic; catálogo histórico de exámenes y selector por bloque/tema; rediseño UI/UX; 1.267 preguntas TAI pendientes (necesitan apuntes `c1-tai`/`a1-sti`); linking para otros temarios; revisión de apuntes en borrador (#42); UX de enlaces 1-a-varios; `lifespan` en vez de `on_event`; proveedores de IA opcionales (Gemini/Obsidian/Notion).
