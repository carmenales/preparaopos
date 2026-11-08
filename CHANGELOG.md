# Changelog

Cambios notables de PreparaOpos. Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y versionado [SemVer](https://semver.org/lang/es/). El detalle de cada rama está en `docs/ESTADO.md`.

## [Sin publicar] — candidata a 1.0.0

Primera versión del sistema nuevo: sustituye a preparadortai (PHP), studyassistant (PHP) y PreparaTIC V3
(ver `docs/MIGRACION.md`).

### Añadido
- **Gateway** Nginx en :8080: apuntes en `/` (study-assistant) y tests en `/tests/` (test-engine).
- **Banco de preguntas unificado** en test-engine (18.820 preguntas, 65 exámenes): PreparaTIC A1 con año y
  marca de examen oficial, TAI, AGE A2 GSI 2024, Ayto. Madrid Aux. TIC, Majadahonda, Comunidad de Madrid y
  UC3M; historial de MariaDB importado.
- **Tests**: exámenes (simulacro y práctica), tests fijos como PreparaTIC (Aleatorios, Relevancia, Bloques,
  Temas y Años) y generador por temario, bloque, tema, año, solo oficiales, falladas, dudosas y ponderado por
  frecuencia en los exámenes oficiales.
- **Pantalla de test** de PreparaTIC: todas las preguntas en una página, cronómetro pausable, Ocultar Tiempo,
  Corregir en cualquier momento, Filtrar, Modo Entrenamiento, corregir al responder, dudosas, ver respuesta,
  nota en vivo, índice y continuar otro día. Apunte enlazado al corregir.
- **Mi Progreso**: historial con borrado y estadísticas de preparadortai (diagnóstico rápido, gráficos de
  evolución, resultados y acierto por bloque, progreso por examen, fallos recurrentes y áreas débiles).
- **Banco de preguntas**: alta, edición, anulación y borrado de preguntas y cuestionarios, y edición de los
  apuntes enlazados.
- **Apuntes** (study-assistant): portada con filtros, apunte con índice, búsqueda semántica, practicar desde
  el apunte, ingesta de PDF con revisión y refinado con Ollama (knowledge-service) y borrado.
- **Inicio** con la explicación de la app, interfaz de PreparaTIC en claro y oscuro, y móvil.
- **CI** en GitHub Actions: tests de la raíz y de cada servicio y comprobación de rutas por el gateway.

### Retirado (pendiente, al cerrar la validación)
- preparadortai y studyassistant (PHP), MariaDB y phpMyAdmin.
