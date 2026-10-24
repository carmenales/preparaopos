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
- `scripts/backup_test_engine.py` (API de backup, `integrity_check`, retención 14, en `backups/`, ignorada por git) y `scripts/purge_test_sessions.py` (simulación por defecto, solo sesiones del smoke test salvo `--all`, `--before`, copia previa obligatoria).

## Antes de mergear a `develop`
1. ~~Smoke del gateway~~: OK al 100 % el 2026-10-19. Ojo: los pasos 5 y 6 crean sesiones reales en la BD.
2. Purgar las sesiones que dejaron smoke tests antiguos: `docker compose stop test-engine` → `python scripts/purge_test_sessions.py --apply` → `docker compose start test-engine`. Por defecto solo selecciona las del smoke test (no toca el historial importado ni el uso real) y hace antes una copia verificada en `backups/test-engine/`.

## Pendiente menor
- `docker-compose.dev.yml` está vacío (0 bytes): rellenar u eliminar.
- ✅ Smoke test: ya borra al terminar las sesiones que crea (rama `feature/smoke-cleanup`).
- `GET /sessions/{id}/result` de una sesión que no existe devuelve 500 en vez de 404.
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

## Orden y borrado de apuntes (rama `feature/notes-order-and-archive`)
- **Orden**: `sort_by_topic` (study-assistant `domain/notes/service.py`) interpreta bloque, tema y subparte del tema oficial o, si no se puede, del id: «I.05_Estructura» y «Tema I.05 …» ocupan el mismo sitio, «I.06.I» va antes que «I.06.II» y «Tema 10» después de «Tema 9». Los temas de un perfil (`p01`, `p04`…) van seguidos y se colocan donde empieza su numeración. Los apuntes sin numeración van al final, en orden alfabético. Lo usan el catálogo, la navegación anterior/siguiente y la posición «N de M».
- **Borrar** (sin archivado, decisión de Carmen): «🗑️ Borrar apunte» en el visor → página de confirmación (borrado definitivo, preguntas enlazadas, ids repetidos) → knowledge-service `POST /notes/delete` borra el `.md` (solo dentro de `knowledge/`) y regenera el índice → study-assistant recarga el índice y linking-service `DELETE /links/by-note/{id}` borra sus enlaces. Se identifica por id **y ruta**, porque hay un id repetido (`cm-ad-innovacion-y-transformacion-digital-tema-016`, ficheros `tema-016-…-ia.md` y `tema-016-…-ia-ampliado.md`); si queda otro apunte con el mismo id, sus enlaces no se tocan. Las imágenes no se borran (pueden ser compartidas).
- Si knowledge-service no responde, no se borra nada; si no responde linking-service, se borra el apunte y se avisa de que sus enlaces quedan.
- Tests: study-assistant 25, linking-service 8, `tests/test_ingest_service.py` 19. Probado también de extremo a extremo con knowledge-service y linking-service reales sobre una copia de `knowledge/`.
- ⚠️ **`knowledge/processes/age/a2-gsi/apuntes/` (65 apuntes) no está en git**, igual que otras carpetas de apuntes: borrar uno de ellos no tiene vuelta atrás.
- ⚠️ El `knowledge_index.json` actual (2026-10-19) incluye `Introducción.md` y `agenda 2030.md`, que ya no existen en disco. La próxima publicación o el próximo borrado regeneran el índice y desaparecen del catálogo (114 apuntes en vez de 116).

## Limpieza del smoke test (rama `feature/smoke-cleanup`)
- `scripts/smoke_gateway.py` espera hasta 30 s (`--wait`) a que `/healthz`, `/` y `/tests/` dejen de dar 502/503/504: justo tras un `docker compose up` test-engine tarda unos segundos en aceptar peticiones.
- Al terminar borra sus dos sesiones (simulacro y práctica por apunte) con el borrado del historial (`POST /tests/history/{id}/delete`) y comprueba que ya no aparecen; `--keep-sessions` las conserva para depurar. Ya no alimenta el historial, las estadísticas ni el refuerzo de falladas.
- `scripts/purge_test_sessions.py` borraba **todas** las sesiones (también las 11 importadas de preparadortai). Ahora por defecto solo selecciona las del smoke test: simulacro del examen 53 con como mucho una respuesta más la práctica sin respuestas de `tema-i-01-derecho-constitucional` en los 10 s siguientes. `--all` para todas. Fija los ids antes de borrar (si no, SQLite reevalúa el emparejamiento durante el `DELETE` y deja las prácticas).
- En la BD actual selecciona 30 sesiones (15 pares, 15 respuestas) y deja las 11 de preparadortai (332 respuestas) y los 2 tests generados (comprobado sobre una copia).
- Tests: `tests/test_purge_test_sessions.py` (unittest). Smoke probado contra los servicios reales detrás de un proxy local, arrancando test-engine 5 s más tarde.

## Generador ponderado por frecuencia histórica (rama `feature/weighted-generator`)
- Opción «Ponderar por frecuencia en exámenes oficiales» en `/generator/`, combinable con el resto de filtros. Se guarda en `source_ref` (`weighted=1`) y el historial la muestra («ponderado por frecuencia»).
- Peso de un tema: sus preguntas de examen oficial (no anuladas) en el temario. Peso de una pregunta: el de su tema entre las preguntas disponibles de ese tema (como `PreguntaTest.getPeso()` del generador Java de PreparaTIC, que usaba pesos puestos a mano en una hoja de cálculo; aquí salen de los datos). Muestreo sin repetición proporcional al peso (Efraimidis-Spirakis); si no bastan las de peso positivo, se completa al azar.
- Solo hay base para **PreparaTIC A1** (8.152 preguntas oficiales en 133 temas, 2002-2026; de 3 a 294 por tema). En los demás temarios la opción sale desactivada.
- Efecto medido con la BD real en el 10 % de temas que más caen: 27,4 % de las preguntas oficiales históricas, ≈26 % en tests ponderados y 22,8 % en aleatorios. La diferencia es moderada porque la mitad del banco de PreparaTIC ya son preguntas oficiales: lo que corrige sobre todo es el peso de los temas con muchas preguntas no oficiales.
- ⚠️ Datos: las 101 preguntas de AGE GSI 2024 (`age-gsi-official`) tienen `is_official_exam = 0` aunque son del examen oficial, así que tampoco salen con «Solo preguntas de examen oficial». Con un único examen no darían una frecuencia útil, pero el filtro sí debería incluirlas.
- **Números del formulario condicionados** (detectado por Carmen al probar): los números de cada opción se calculaban sobre todo el temario, así que con «B3 · Tema 107» elegido los años seguían mostrando las preguntas de todos los temas (p. ej. 2004 (323)) y «Solo oficiales» 8.152, mientras el recuento daba 0. Ahora cada número cuenta con los demás filtros elegidos (no el suyo), el formulario se recalcula entero con htmx al cambiar cualquier campo (`GET /generator/fields`), las opciones en 0 se ocultan y lo elegido se mantiene aunque se quede en 0. Ejemplo real: B3 · 107 tiene 34 preguntas (2026: 9, 2024: 2, 2023: 23), 8 oficiales.
- Tests: test-engine 77 en local (9 nuevos); en un clon sin datos se saltan los que usan la BD.

## CI (rama `feature/ci-fixes`)
- Antes: el job de Docker comprobaba preparadortai en el 8080 (ahora es el gateway; preparadortai está en el 8082 y necesita el volcado de MariaDB, que no está en git) y los tests de `services/*` no se ejecutaban.
- Jobs de `.github/workflows/ci.yml`:
  - `php-syntax`: sin cambios, hasta retirar las apps PHP.
  - `python-tests`: `unittest discover -s tests` y generación del índice. Ya no instala `services/embeddings/requirements.txt` (arrastraba torch y ningún test lo usa); `numpy` y `requests`, que importan los scripts, pasan a `scripts/requirements.txt`.
  - `service-tests`: pytest de study-assistant, test-engine y linking-service (matriz, Python 3.11 como sus Dockerfile).
  - `gateway`: levanta gateway, study-assistant, test-engine y linking-service con la BD vacía y el índice de los apuntes versionados, y comprueba las rutas por el 8080 (con reintentos mientras arrancan).
- **Datos que no están en git** (BD de test-engine, `imports/`, apuntes sin revisar, índice): los tests que los necesitan se saltan en CI y lo dicen (`-rs`); en local se ejecutan todos.
  - test-engine: `tests/conftest.py` salta los tests que usan la BD (fixtures `client`, `db`, `db_session`, `session_service`, `svc` o marca `real_db`) si no existe `data/test_engine.sqlite`. En CI corren 15 de 68: **la lógica que depende de los datos (generador, sesiones, gestión) no se comprueba en CI**. Para cubrirla haría falta una BD de prueba sintética y reescribir los tests que cuentan preguntas reales (96, 269…).
  - study-assistant: `tests/conftest.py` crea un índice y unos apuntes de prueba en un directorio temporal; los 25 tests ya no dependen de los apuntes reales y corren igual en CI y en local.
  - `tests/test_import_local_exams.py`: se saltan las 6 pruebas que leen `imports/`.
- Comprobado en un clon limpio (`git archive`) con un entorno nuevo: raíz 145 tests (6 saltados), study-assistant 25, test-engine 15 (53 saltados), linking-service 8, y las rutas del job `gateway` contra los servicios reales con la BD vacía. En local, con los datos, todo sigue igual (test-engine 68, study-assistant 25).

## Después
La migración no está completa: ver `docs/MIGRACION.md` (datos sin importar, funcionalidades de las apps PHP sin equivalente y criterios para etiquetar la versión).

1. Simulacro completo manual por :8080. Luego tag/release y usar el sistema unos días.
2. Backlog: Alembic; catálogo histórico de exámenes y selector por bloque/tema; rediseño UI/UX; 1.267 preguntas TAI pendientes (necesitan apuntes `c1-tai`/`a1-sti`); linking para otros temarios; revisión de apuntes en borrador (#42); UX de enlaces 1-a-varios; `lifespan` en vez de `on_event`; proveedores de IA opcionales (Gemini/Obsidian/Notion).
