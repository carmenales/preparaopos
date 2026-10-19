# Estado de la migración al sistema nuevo

_Inventario del 2026-10-19 sobre `develop` (`9afaab23`). La migración se da por terminada cuando se cumplan todos los criterios de §4; entonces se etiqueta la primera versión y se retiran las apps PHP y MariaDB._

## 1. Datos

| Fuente | Preguntas | En test-engine | Estado |
|---|---:|---:|---|
| PreparaTIC (bundle V3) | 16.680 | 16.680 | ✅ Con `year` e `is_official_exam` (8.152 de examen oficial) desde el paso 1 (`scripts/etl/backfill_preparatic_metadata.py`). |
| TAI (MariaDB `ptype`) | 1.331 | 1.331 | ✅ 52 cuestionarios. 1.267 pendientes de clasificar por tema. |
| AGE A2 GSI 2024 | 101 | 101 | ✅ Clasificado y enlazado con apuntes. |
| Ayto. Madrid Aux. TIC 2023/2025 (`imports/ayto_madrid_aux_tic`) | 294 | 0 | ❌ Solo existe como SQL para MariaDB (6 cuestionarios). |
| Ayto. Majadahonda Técnico Informático (`imports/ayto_majadahonda`) | 44 | 0 | ❌ Ídem. |
| Comunidad de Madrid P01/P02 IA y P01 TIC (`imports/cm_madrid_digital`) | 144 | 0 | ❌ Ídem. El de TIC P01 se llama `_template`: confirmar que es real. |
| UC3M A2 GSI 2021/2024 (`imports/uc3m_gsi`) | 270 | 0 | ❌ Ídem (3 exámenes). |
| Historial de tests en MariaDB (`test_sessions`, `test_attempts`, `question_sets`) | — | 0 | ❓ Sin comprobar si hay uso real que conservar. |
| Historial de PreparaTIC V3 (IndexedDB del navegador) | — | 0 | ➖ Se queda en el navegador; no se migra. |

**Lo que no se puede recuperar:** los exámenes completos de PreparaTIC. Las preguntas marcadas como de examen se mezclan dentro de cada año (p. ej. 2023 tiene 1.171, de varias convocatorias) y no hay nada que las separe por examen. Sí se pueden ofrecer tests por año y solo con preguntas de examen oficial.

### Comprobación pendiente en MariaDB
Con la suite levantada, en PowerShell:
```powershell
docker exec preparaopos-preparadortai-db mariadb -uroot -p -e "
  SELECT categoria, COUNT(*) FROM ptype GROUP BY categoria ORDER BY categoria;
  SELECT COUNT(*) AS sesiones FROM test_sessions;
  SELECT COUNT(*) AS intentos, MIN(answered_at), MAX(answered_at) FROM test_attempts;" <nombre_bd>
```
- Si aparecen categorías AYTO/CM/UC3M/MAJADAHONDA, esos SQL se cargaron después de la importación a test-engine.
- Si hay intentos con fechas de estudio real, hay que migrar el historial.

## 2. Funcionalidad

### preparadortai (PHP) → test-engine
| Página antigua | Qué hace | En test-engine |
|---|---|---|
| `examenes.php` | Catálogo de exámenes y simulacro | ✅ Catálogo, simulacro y práctica |
| `temas.php`, `practica_tematica.php` | Test por tema o bloque | ❌ (solo hay práctica desde un apunte) |
| `practica.php` | Ejercicios por categoría | ⚠️ Cubierto por los cuestionarios del catálogo |
| `refuerzo.php` | Test con preguntas falladas | ❌ |
| `historial_sesiones.php`, `detalle_sesion.php`, `delete_test_session.php` | Historial de tests | ❌ (solo la hoja de resultados de cada sesión) |
| `estadisticas.php`, `progreso_cuestionarios.php` | Estadísticas y progreso | ❌ |
| `gestionar.php`, `agregar.php`, `editar.php` | Alta y edición de preguntas | ❌ |
| `categorias.php`, `nueva_categoria.php`, `editar_cuestionario.php` | Gestión de cuestionarios | ❌ |
| `relacionar.php` | Repaso pregunta↔tema | ⚠️ El enlace con apuntes lo da linking-service |
| `changelog.php` | Novedades | ➖ No se migra |

### PreparaTIC V3 (Vue) → test-engine
| Modo | En test-engine |
|---|---|
| Aleatorio | ❌ |
| Ponderado por frecuencia histórica | ❌ (necesita `year`) |
| Por bloque / por tema | ❌ |
| Por año de convocatoria | ❌ (necesita `year`) |
| Examen oficial íntegro | ➖ No reconstruible (§1) |
| Historial y estadísticas con gráficos | ❌ |

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
2. **Importar las 752 preguntas de `imports/`**: un importador que lea los `.sql` directamente (sin pasar por MariaDB), con un temario por proceso (`ayto-madrid/aux-tic`, `majadahonda/tecnico-informatico`, `comunidad-madrid/...`, `uc3m/a2-gsi`) y un examen por cuestionario, respetando las anuladas.
3. **Generador de tests**: por bloque o tema, por año, aleatorio, solo preguntas de examen oficial y falladas (refuerzo). Esto cubre `temas`, `practica_tematica`, `refuerzo` y los modos de V3.
4. **Historial y estadísticas**: lista de sesiones con borrado y aciertos por bloque/tema (sustituye a `historial_sesiones`, `estadisticas` y `progreso`).
5. **Gestión de preguntas**: alta, edición y anulación (sustituye a `gestionar`, `agregar`, `editar` y `categorias`).
6. **Asistente de ingesta** en study-assistant (sustituye a `ingest.php`).
7. **Historial de MariaDB**, solo si la comprobación de §1 muestra uso real.

## 4. Criterios para dar la migración por terminada
- [ ] Todas las preguntas de §1 están en test-engine, con su origen, año y anuladas.
- [ ] Cada página de §2 marcada ❌ tiene equivalente o se decide explícitamente no migrarla.
- [ ] Simulacro completo hecho a mano por :8080 sin incidencias.
- [ ] Una semana de uso real sin volver a las apps PHP.
- [ ] Se retiran de `docker-compose.yml` `preparadortai-web`, `studyassistant-web`, MariaDB y phpMyAdmin, con un volcado final de MariaDB guardado en `backups/`.
- [ ] Etiqueta `v1.0.0`.
