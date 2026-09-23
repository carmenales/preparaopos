# Tests PreparaTIC (Plataforma de Tests Integrada)

Plataforma de generación y realización de exámenes de test para oposiciones TIC de la AGE (A1 TIC y A2 GSI), desarrollada y mantenida históricamente por la comunidad de **PreparaTIC** (promociones XXIV a XXVIII).

Esta carpeta integra el banco de preguntas completo (+10.300 preguntas oficiales y revisadas) y los dos motores web históricos para su uso y evaluación previa a la migración a la nueva arquitectura.

---

## 1. Estructura del Módulo

| Directorio / Fichero | Descripción |
| :--- | :--- |
| **`index.html`** / **`v3/index.html`** | **Versión V3 (Principal)**: SPA moderna y autónoma desarrollada en **Vue 3 + Vite + Tailwind CSS + ECharts**, que incluye en su interior el banco completo de preguntas, algoritmos de ponderación y motor de estadísticas locales en IndexedDB. |
| **`v2/`** | **Versión V2 (Histórica)**: Interfaz web clásica basada en la plantilla *Gentelella Admin* (Bootstrap, jQuery, DataTables). |
| **`data/`** | Datasets maestros en formato CSV/Excel: `Excel_revision_preparatic24.xlsx` (banco de preguntas con enunciado, 4 opciones, solución y justificación), temas, bloques y temáticas. |
| **`generator/`** | Herramienta original en Java (`TestGenerator.java`) con dependencias Maven (`pom.xml`) y plantillas de generación StringTemplate (`.st`). |
| **`scriptsDB/`** | Esquema SQL de la base de datos relacional original (`CreateDBSchema.sql`). |
| **`run_local.py`** | Servidor HTTP local en Python para ejecutar la aplicación en el navegador sin restricciones CORS locales. |
| **`start_tests.bat`** | Acceso directo ejecutable para iniciar el servidor con doble clic en Windows. |

---

## 2. Cómo Ejecutar la Aplicación

Para iniciar el servidor local y abrir la aplicación automáticamente en tu navegador:

### Opción A: Desde la consola (PowerShell / CMD)
```powershell
python apps/tests_preparatic/run_local.py
```

### Opción B: Doble clic en Windows
Haz doble clic sobre el archivo [`start_tests.bat`](file:///c:/repositories/preparaopos/apps/tests_preparatic/start_tests.bat).

Por defecto, se levantará en:
- **V3 (SPA Principal):** [http://localhost:8080/](http://localhost:8080/)
- **V2 (Versión Gentelella):** [http://localhost:8080/v2/index.html](http://localhost:8080/v2/index.html)

---

## 3. Funcionalidades de la Versión V3

La aplicación V3 incluye rutas internas navegables mediante Vue Router:

- **Modos de Examen y Test:**
  - `/test/random`: Test con preguntas aleatorias mezclando bloques generales y específicos.
  - `/test/weighted`: Test ponderado por frecuencia histórica de aparición en convocatorias oficiales.
  - `/test/block`: Tests específicos por bloques temáticos (Bloque I a Bloque IV).
  - `/test/topic`: Tests por temas específicos del temario oficial.
  - `/test/year`: Preguntas agrupadas por año de convocatoria.
  - `/test/exam`: Simulacro de exámenes oficiales íntegros.
- **Progreso y Estadísticas:**
  - `/progress/history`: Histórico de tests realizados guardados en el almacenamiento del navegador.
  - `/progress/stats`: Cuadro de mandos con gráficos interactivos ECharts (evolución de notas, aciertos por bloque/tema, tasa de error).

