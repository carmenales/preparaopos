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

## Paso 3 de la migración: generador de tests (rama `feature/test-generator`)
- Origen de sesión `generated` (`domain/sessions/generator.py`) con filtros de temario, bloque/tema, año, solo examen oficial y solo falladas (último intento incorrecto), de 10 a 100 preguntas en la interfaz (máximo 200). Excluye anuladas.
- Modo examen: 60 s por pregunta. Puntuación: la regla común de los exámenes del temario si es única; si no, A−F/3.
- Pantalla `/generator` (enlazada desde la cabecera y el catálogo) con recuento en vivo de preguntas disponibles (htmx).
- Ojo: el smoke test responde preguntas en la BD real, así que también alimenta el refuerzo (la 18012 aparece como fallada). Se suma a la tarea pendiente de que el smoke marque o limpie sus sesiones.

## Paso 7 de la migración: historial de preparadortai (rama `feature/session-history`)
- `scripts/etl/import_mariadb_history.py`: 11 sesiones y 332 intentos de MariaDB (junio y julio) como sesiones cerradas `legacy`, con su nota según la regla del examen. Simulación por defecto, copia previa, todo o nada e idempotente.
- Corregidos dos bugs: la regla de puntuación por defecto calculaba sobre 100 (ahora sobre 10), y 1.147 preguntas de TAI no tenían etiqueta de temario y no aparecían en el generador (`scripts/etl/fix_tai_syllabus_tags.py`).
- `import_tai_mariadb.py` omite ya las categorías de exámenes locales (AYTO, CM, UC3M) que también están en `ptype`, para no duplicarlas como TAI.

## Paso 4 de la migración: historial y estadísticas (rama `feature/history-and-stats`)
- `/history/`: todas las sesiones con su descripción (examen, filtros del generador, apunte o preparadortai), modo, aciertos, fallos y blancos, y nota. Se puede ver el resultado, continuar las abiertas y borrar (con confirmación; borra también los intentos).
- `/stats/`: por temario, acierto, respuestas y sesiones, cobertura de preguntas vistas, falladas pendientes (misma definición que el refuerzo), acierto por bloque y tema con los más flojos primero y enlace «Repasar» al generador ya filtrado, y evolución de la nota.
- Las sesiones del smoke test aparecen en el historial; ahora se pueden borrar desde ahí.

## Paso 5 de la migración: gestión de preguntas y cuestionarios (rama `feature/question-management`)
- `/manage/questions/`: búsqueda por enunciado, temario y cuestionario (50 por página); alta y edición con 2-6 opciones, correcta, justificaciones, temario/bloque/tema, año, examen oficial, anulación con motivo y añadir a un cuestionario. Las preguntas nuevas llevan `source = 'manual'`.
- Protección del historial: las opciones se editan sobre la misma fila (los intentos apuntan a su id), no se puede quitar una opción ya elegida ni borrar una pregunta con respuestas (se anula). Cambiar la correcta no reescribe los aciertos ya guardados.
- `/manage/exams/`: alta y edición de cuestionarios (temario, año, convocatoria, regla de puntuación y duración), lista de sus preguntas con «Quitar» y borrado si no tiene sesiones.
- Fuera de alcance: crear temarios nuevos y reordenar preguntas dentro de un cuestionario.

## Paso 6 de la migración: asistente de ingesta (rama `feature/ingest-assistant`)
- `services/knowledge/pdf_extractor.py` y `markdown_normalizer.py` **nunca se habían commiteado**: `ingest_service.py` (commit `f7429cd5`) ya los importaba, pero estaban como ficheros sin seguimiento en `stash@{1}` (`feature/knowledge-source-ui`). Sin ellos knowledge-service no arrancaba. Recuperados del stash tal cual (el stash no se ha tocado); pasan los 16 tests de `tests/test_ingest_service.py`.
- study-assistant `/ingest/`: subir PDF (proceso existente u otro nuevo, origen, limpieza) → revisión con título, tema, etiquetas, estado, editor Markdown con vista previa en vivo (htmx) y «Refinar con Ollama» → publicar. Tras publicar se recarga el índice en memoria y se abre el apunte, sin reiniciar el contenedor.
- Si knowledge-service u Ollama no responden, se muestra un aviso y no se pierde el texto.
- `docker-compose.yml`: `KNOWLEDGE_SERVICE_INTERNAL_URL` para study-assistant.
- Gateway: `location /ingest/` con `client_max_body_size 50m` y `proxy_read_timeout 1000s` (por defecto Nginx rechaza más de 1 MB con 413 y corta a los 60 s, menos de lo que tarda el refinado con Ollama).

## Correcciones de la migración (rama `feature/migration-fixes`)
- Pie de página del PDF en 9 opciones de GSI 2024 y aviso «N de M pedidas» en el generador (ya commiteados y aplicados).
- **Edición manual de enlaces pregunta↔apunte** (los automáticos los generó una IA y algunos no tienen sentido). En `/manage/questions/{id}/edit`, sección «Apuntes enlazados»: lista con título, tema y origen (a mano / automático por tema con su confianza), «Quitar» en cada uno y un desplegable con todos los apuntes de study-assistant agrupados por proceso para enlazar otro. Una pregunta puede tener varios.
  - linking-service: `POST /links` (manual, confianza 1,0, comprueba que el apunte existe) y `DELETE /links/{question_id}/{note_id}`. Quitar deja una lápida (`source='removed'`) que las lecturas ignoran, para que `resolve_links.py` no lo vuelva a crear; la resolución automática tampoco rebaja un enlace manual. Si study-assistant no responde, `POST /links` devuelve 404 con el motivo en vez de 500.
  - test-engine: si linking-service o study-assistant no responden, la página de edición se sigue mostrando con un aviso. Cambiar el bloque o el tema de una pregunta no cambia sus enlaces.
- **Frontmatter de la ingesta**: `ai_cleaned` solo es `true` si el texto se ha refinado con Ollama, y `needs_human_review` lo marca el usuario con una casilla al publicar (antes eran siempre `true` y `false`).
- Tests: test-engine 68, linking-service 7, study-assistant 14 y `tests/test_ingest_service.py`. Probado también de extremo a extremo con linking-service real.

## CI (fuera de alcance; anotado)
- `ci.yml` hace `curl localhost:8080/assets/css/style.css` esperando preparadortai, pero ahora el 8080 es el gateway Nginx (preparadortai está en el 8082).
- La CI solo ejecuta `unittest discover -s tests`; los tests de `services/*` (pytest) no corren en CI.

## Después
La migración no está completa: ver `docs/MIGRACION.md` (datos sin importar, funcionalidades de las apps PHP sin equivalente y criterios para etiquetar la versión).

1. Simulacro completo manual por :8080. Luego tag/release y usar el sistema unos días.
2. Backlog: Alembic; catálogo histórico de exámenes y selector por bloque/tema; rediseño UI/UX; 1.267 preguntas TAI pendientes (necesitan apuntes `c1-tai`/`a1-sti`); linking para otros temarios; revisión de apuntes en borrador (#42); UX de enlaces 1-a-varios; `lifespan` en vez de `on_event`; proveedores de IA opcionales (Gemini/Obsidian/Notion).
