# Estado de la migración al sistema nuevo

_Inventario del 2026-10-19 sobre `develop` (`9afaab23`). La migración se da por terminada cuando se cumplan todos los criterios de §4; entonces se etiqueta la primera versión y se retiran las apps PHP y MariaDB._

## 1. Datos

| Fuente | Preguntas | En test-engine | Estado |
|---|---:|---:|---|
| PreparaTIC (bundle V3) | 16.680 | 16.680 | ✅ Con `year` e `is_official_exam` (8.152 de examen oficial) desde el paso 1 (`scripts/etl/backfill_preparatic_metadata.py`). |
| TAI (MariaDB `ptype`) | 1.331 | 1.331 | ✅ 52 cuestionarios. 1.267 pendientes de clasificar por tema. |
| AGE A2 GSI 2024 | 101 | 101 | ✅ Clasificado y enlazado con apuntes. |
| Ayto. Madrid Aux. TIC 2021/2024 (`imports/ayto_madrid_aux_tic`) | 294 | 294 | ✅ Paso 2. 6 cuestionarios, 3 opciones, A−F/3. |
| Ayto. Majadahonda Técnico Informático (`imports/ayto_majadahonda`) | 44 | 44 | ✅ Paso 2. ⚠️ Baremo no consta: sin regla (test-engine aplica A−F/3 por defecto). |
| Comunidad de Madrid P01/P02 IA (`imports/cm_madrid_digital`) | 100 | 100 | ✅ Paso 2. A−F/3. |
| Comunidad de Madrid TIC P01 Analista (`_template`) | 44 | 0 | ⏸️ Excluido: sin plantilla oficial (`[PENDIENTE DE PLANTILLA OFICIAL]`). Importar cuando se publique. |
| UC3M A2 GSI 2021/2024 (`imports/uc3m_gsi`) | 270 | 270 | ✅ Paso 2. 3 exámenes, A−F/4 (regla nueva `oficial-cuarto`). |
| Historial de tests en MariaDB (`test_sessions`, `test_attempts`) | 332 intentos | 332 | ✅ Paso 7. 11 sesiones de práctica (17-jun a 22-jul) con `source = 'legacy'`, desde `backups/mariadb/*.tsv` (`scripts/etl/import_mariadb_history.py`). Todos los intentos casan de forma exacta. |
| Historial de PreparaTIC V3 (IndexedDB del navegador) | — | 0 | ➖ Se queda en el navegador; no se migra. |

**Lo que no se puede recuperar:** los exámenes completos de PreparaTIC. Las preguntas marcadas como de examen se mezclan dentro de cada año (p. ej. 2023 tiene 1.171, de varias convocatorias) y no hay nada que las separe por examen. Sí se pueden ofrecer tests por año y solo con preguntas de examen oficial.

### Comprobación en MariaDB (hecha el 2026-10-19)
Con la suite levantada, en PowerShell:
```powershell
docker exec preparaopos-preparadortai-db mariadb -uroot -p -e "
  SELECT categoria, COUNT(*) FROM ptype GROUP BY categoria ORDER BY categoria;
  SELECT COUNT(*) AS sesiones FROM test_sessions;
  SELECT COUNT(*) AS intentos, MIN(answered_at), MAX(answered_at) FROM test_attempts;" <nombre_bd>
```
- Si aparecen categorías AYTO/CM/UC3M/MAJADAHONDA, esos SQL se cargaron después de la importación a test-engine.
- Si hay intentos con fechas de estudio real, hay que migrar el historial.

### Incidencias de datos detectadas
- ✅ **Opción correcta siempre en primera posición en TAI (1.331) y AGE GSI 2024 (101)** (corregido en `feature/fix-option-order`). GSI 2024 recupera el orden oficial A-D, comprobado contra el JSON del examen. TAI no conserva el orden original en ninguna fuente: se baraja de forma determinista por pregunta, y en 3 preguntas cuya explicación cita la letra («opción C») la correcta se coloca en esa letra. Los importadores generan ya este mismo orden.
- Ayto. Madrid 2024 práctico, pregunta 16, opción C: el texto lleva un resto de la extracción del PDF («…aún no es oficial. economía, innovación 8»). Revisar en origen.
- Ayto. Madrid: el SQL `_fixed` corrige tres textos frente a `review_questions.csv` (RD 193/2023, WCAG 2.2 2023 y 2.1 actualizada en 2025). Se importa el texto del SQL.

### Pendientes detectados al probar el generador (2026-10-19)
1. **Pie de página del PDF en opciones de GSI 2024:** 9 opciones terminan en «2024 - GSI-L Página N de 10» (siempre el mismo patrón y solo en esa fuente). Limpiar en la BD, en `import_age_gsi_2024.py` y en el JSON del examen.
2. **Enlaces pregunta→apunte:** hoy significan «apuntes del mismo tema oficial» (clasificación semántica revisada a mano → todos los apuntes de ese tema; confianza 1,0 si hay uno y 0,8 si hay varios), no «el apunte contiene la respuesta». Solo existen para GSI 2024 (118 enlaces, 100 preguntas, 51 apuntes). Primero, etiquetarlos en la interfaz como «Apuntes del tema». Después, enlace a nivel de sección: fragmento más parecido por embeddings, ancla al apartado y aviso de «sin cobertura en tus apuntes» por debajo de un umbral.
3. **Generador: menos preguntas de las pedidas sin avisar** (se pidieron 10 y salieron 6). Avisar o limitar el número al disponible antes de crear el test y mostrar «N de M pedidas» en la sesión.
5. ✅ **Regla de puntuación por defecto sobre 100** (corregido: ahora sobre 10): `DEFAULT_AGE_SCORING_RULE` (`domain/sessions/service.py`) tiene `score_scale = 100`, pero la hoja de resultados pinta «/ 10». Afecta a cualquier sesión sin regla propia (p. ej. Majadahonda). Aún no hay ninguna sesión cerrada con ella.
6. ✅ **1.147 preguntas de TAI sin etiqueta de temario** (corregido: el importador etiqueta siempre y `scripts/etl/fix_tai_syllabus_tags.py` repara la BD existente): `import_tai_mariadb.py` solo etiqueta las que tienen bloque y tema, y el generador busca por etiqueta, así que esas preguntas no aparecen ni en «todo el temario» ni en el refuerzo (TAI muestra 184 preguntas y 7 falladas en vez de 1.331 y 48). Las demás fuentes crean la etiqueta con bloque y tema vacíos.
4. **UX de test-engine escasa:** el rediseño ya estaba en el backlog y sube de prioridad (formularios, recuento visible, navegación de la sesión).

## 2. Funcionalidad

### preparadortai (PHP) → test-engine
| Página antigua | Qué hace | En test-engine |
|---|---|---|
| `examenes.php` | Catálogo de exámenes y simulacro | ✅ Catálogo, simulacro y práctica |
| `temas.php`, `practica_tematica.php` | Test por tema o bloque | ✅ Generador (`/generator`) |
| `practica.php` | Ejercicios por categoría | ⚠️ Cubierto por los cuestionarios del catálogo |
| `refuerzo.php` | Test con preguntas falladas | ✅ Generador: «solo las que fallé la última vez» |
| `historial_sesiones.php`, `detalle_sesion.php`, `delete_test_session.php` | Historial de tests | ✅ `/history/` (ver, continuar y borrar sesiones) |
| `estadisticas.php`, `progreso_cuestionarios.php` | Estadísticas y progreso | ✅ `/stats/` (acierto, cobertura, falladas pendientes, bloque/tema y evolución) |
| `gestionar.php`, `agregar.php`, `editar.php` | Alta y edición de preguntas | ✅ `/manage/questions/` (buscar, alta, edición, anular, borrar si no tiene respuestas) |
| `categorias.php`, `nueva_categoria.php`, `editar_cuestionario.php` | Gestión de cuestionarios | ✅ `/manage/exams/` (alta, edición, quitar preguntas, borrar si no tiene sesiones) |
| `relacionar.php` | Repaso pregunta↔tema | ⚠️ El enlace con apuntes lo da linking-service |
| `changelog.php` | Novedades | ➖ No se migra |

### PreparaTIC V3 (Vue) → test-engine
| Modo | En test-engine |
|---|---|
| Aleatorio | ✅ Generador (todo el temario) |
| Ponderado por frecuencia histórica | ❌ Pendiente: no estaba en el paso 3; ya hay datos (`year`, `is_official_exam`) para hacerlo |
| Por bloque / por tema | ✅ Generador |
| Por año de convocatoria | ✅ Generador (+ «solo examen oficial») |
| Examen oficial íntegro | ➖ No reconstruible (§1) |
| Historial y estadísticas con gráficos | ✅ `/history/` y `/stats/` (barras simples; sin gráficos interactivos) |

### studyassistant (PHP) → study-assistant
| Página antigua | En study-assistant |
|---|---|
| `index.php` (panel, filtros, chips, métricas) | ✅ |
| `note.php` (TOC, anterior/siguiente, Mermaid, MathJax) | ✅ + práctica desde el apunte |
| `search.php` (búsqueda semántica) | ✅ `/api/search` → embeddings |
| `asset.php` | ✅ |
| `ingest.php` (asistente PDF → apunte con knowledge-service y Ollama) | ❌ |

### Servicios Python que se quedan
`services/embeddings` (lo usa study-assistant) y `services/knowledge` (lo usará el asistente de ingesta).

## 3. Plan propuesto (por orden)
1. ✅ **Metadatos de PreparaTIC**: columnas `questions.year` e `is_official_exam`. Reimportar solo esos campos desde `preparatic_bundle_extracted.json`, sin tocar ids ni etiquetas.
2. ✅ **Importar las preguntas de `imports/`** (708; las 44 del `_template` quedan fuera): un importador que lea los `.sql` directamente (sin pasar por MariaDB), con un temario por proceso (`ayto-madrid/aux-tic`, `majadahonda/tecnico-informatico`, `comunidad-madrid/...`, `uc3m/a2-gsi`) y un examen por cuestionario, respetando las anuladas.
3. ✅ **Generador de tests**: por bloque o tema, por año, aleatorio, solo preguntas de examen oficial y falladas (refuerzo). Esto cubre `temas`, `practica_tematica`, `refuerzo` y los modos de V3.
4. ✅ **Historial y estadísticas**: lista de sesiones con borrado y aciertos por bloque/tema (sustituye a `historial_sesiones`, `estadisticas` y `progreso`).
5. ✅ **Gestión de preguntas**: alta, edición y anulación (sustituye a `gestionar`, `agregar`, `editar` y `categorias`).
6. **Asistente de ingesta** en study-assistant (sustituye a `ingest.php`).
7. ✅ **Historial de MariaDB**: 332 intentos reales de junio y julio (ver §1).

## 4. Criterios para dar la migración por terminada
- [ ] Todas las preguntas de §1 están en test-engine, con su origen, año y anuladas.
- [ ] Cada página de §2 marcada ❌ tiene equivalente o se decide explícitamente no migrarla.
- [ ] Simulacro completo hecho a mano por :8080 sin incidencias.
- [ ] Una semana de uso real sin volver a las apps PHP.
- [ ] Se retiran de `docker-compose.yml` `preparadortai-web`, `studyassistant-web`, MariaDB y phpMyAdmin, con un volcado final de MariaDB guardado en `backups/`.
- [ ] Etiqueta `v1.0.0`.
