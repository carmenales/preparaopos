---
id: "cm-ad-tic-p04-tema-006-herramientas-tecnicas"
title: "Herramientas y Técnicas de Gestión"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/tic"
profiles:
  - "p04-ingeniero-desarrollo"
official_profile: "P04 - Ingeniero de Desarrollo"
official_topic: "Tema 6. Herramientas y Técnicas"
source_ids:
  - "A2_Bloque_III.pdf"
  - "A2_Bloque_IV.pdf"
tags:
  - "wbs"
  - "pert"
  - "gantt"
  - "riesgos"
  - "evm"
  - "metrica-v3"
  - "itil"
  - "cmdb"
created_at: "2026-08-08"
last_reviewed: null
ai_generated: true
ai_sources:
  - "chatgpt"
  - "gemini"
  - "perplexity"
needs_human_review: true
---

# Tema 6. Herramientas y Técnicas

Este tema es el núcleo operativo de Métrica v3 (Interfaz de Gestión de Proyectos - GP) y de estándares como el PMBOK o marcos de servicio como ITIL v4. Como ingeniero, esto es "código de gestión": reglas claras para construir la estructura del proyecto y asegurar su correcta operación técnica y gobernanza.

## 1. Planificación: WBS, Cronogramas y Estimación

La planificación transforma la idea en tareas ejecutables, estableciendo las líneas base del proyecto.

*   **WBS (Work Breakdown Structure / Estructura de Desglose del Trabajo - EDT):** Es el **árbol jerárquico** que descompone el proyecto en entregables manejables (fases -> actividades -> tareas). Es la base para cualquier estimación. 
    *   *Regla del 100%:* La WBS debe incluir el 100% del trabajo definido por el alcance del proyecto.
    *   *Paquete de trabajo (Work Package):* Es el nivel más bajo de la WBS, donde el coste y la duración pueden ser estimados y gestionados con fiabilidad.
    *   *Diccionario de la WBS:* Documento de respaldo que proporciona información detallada (descripción, responsable, criterios de aceptación) sobre cada componente de la WBS.
*   **Estimación:**
    *   **Puntos Función (Albrecht / Mark II):** Técnica empírica e independiente del lenguaje. Mide la complejidad de la funcionalidad basándose en las entradas, salidas, consultas, archivos lógicos internos y archivos de interfaz externos.
    *   **Staffing Size:** Específico para **Orientación a Objetos**. Se basa en estimar el número de clases clave y secundarias para determinar el esfuerzo en días/persona.
    *   **COCOMO (Constructive Cost Model):** Modelo matemático de Barry Boehm basado en líneas de código (KLOC) y multiplicadores de esfuerzo.
    *   **Técnica Delphi / Delphi de banda ancha:** Método cualitativo basado en el consenso de un panel de expertos anónimos.
*   **Cronogramas y Secuenciación:**
    *   **Método de la Ruta Crítica (CPM):** Algoritmo para predecir la duración del proyecto. La ruta crítica es la secuencia de actividades con **holgura cero**; cualquier retraso en ella retrasa el proyecto.
    *   **PERT (Program Evaluation and Review Technique):** Grafo de redes (nodos/flechas) probabilístico. Usa tres estimaciones (Optimista, Pesimista, Más probable) para calcular la duración esperada: $E = \frac{O + 4M + P}{6}$. Permite calcular la **Ruta Crítica** (la secuencia de tareas sin holgura).
    *   **Holgura (Float):** *Holgura Total* es el tiempo que una actividad puede retrasarse sin retrasar el proyecto; *Holgura Libre* es el tiempo que puede retrasarse sin afectar a las actividades sucesoras.
    *   **Gantt:** El diagrama de barras clásico para visualizar plazos y superposición de tareas en el tiempo.

### 1.1. WBS y planificación del alcance

La **WBS/EDT** organiza jerárquicamente el alcance total del proyecto mediante entregables y componentes de trabajo. El nivel inferior de la descomposición puede corresponder a **paquetes de trabajo**, que permiten planificar y controlar coste, duración y recursos con un nivel de detalle adecuado.

La WBS constituye una referencia para desarrollar el cronograma, estimar costes y asignar responsabilidades. La descomposición debe ser suficiente para planificar y controlar el trabajo, evitando niveles de detalle innecesarios.

La **regla del 100 %** establece que la WBS debe recoger todo el trabajo necesario para completar el alcance definido, incluyendo el trabajo de dirección y gestión del proyecto cuando forme parte del alcance.

El **diccionario de la WBS** complementa la representación gráfica mediante información detallada de sus componentes, como descripción, responsables, criterios de aceptación, supuestos y restricciones.

### 1.2. Cronogramas y relaciones entre actividades

El cronograma representa la planificación temporal del trabajo. Para construirlo es necesario identificar y secuenciar actividades y determinar su duración y dependencias.

Las relaciones de precedencia más habituales son:

* **Fin a inicio (FS):** la actividad sucesora comienza cuando termina la predecesora.
* **Fin a fin (FF):** la actividad sucesora termina cuando termina la predecesora.
* **Inicio a inicio (SS):** la actividad sucesora comienza cuando comienza la predecesora.
* **Inicio a fin (SF):** la actividad sucesora termina cuando comienza la predecesora.

El cronograma puede representarse mediante diagramas de red y diagramas de Gantt. El uso de relaciones de precedencia permite identificar dependencias y determinar posibles ajustes de secuencia.

### 1.3. Ruta crítica y holguras

El **método de la ruta crítica (CPM)** determina la secuencia de actividades que condiciona la duración mínima del proyecto. Las actividades de la ruta crítica presentan, en el modelo básico, **holgura total cero**.

La **holgura total** es el tiempo que una actividad puede retrasarse sin retrasar la fecha de finalización del proyecto. La **holgura libre** es el tiempo que puede retrasarse una actividad sin retrasar el comienzo más temprano de una actividad sucesora.

Una actividad fuera de la ruta crítica puede convertirse en crítica si su holgura se consume como consecuencia de retrasos o cambios de planificación.

### 1.4. Estimación de duración y esfuerzo

La estimación debe expresar sus supuestos y el grado de incertidumbre asociado.

Entre las técnicas pueden utilizarse:

* **Estimación análoga:** utiliza información histórica de proyectos o actividades similares.
* **Estimación paramétrica:** aplica relaciones estadísticas entre variables históricas y parámetros del trabajo.
* **Estimación ascendente (bottom-up):** estima componentes detallados y agrega sus resultados.
* **Estimación de tres puntos:** utiliza valores optimista, más probable y pesimista.
* **Juicio de expertos:** incorpora conocimiento especializado cuando existe información suficiente.
* **Estimación por consenso:** combina estimaciones independientes para reducir sesgos individuales.

### 1.5. PERT y estimación de tres puntos

En la formulación PERT clásica, la duración esperada se obtiene mediante:

**E = (O + 4M + P) / 6**

donde **O** es la estimación optimista, **M** la más probable y **P** la pesimista.

La misma técnica puede utilizarse para representar la incertidumbre del esfuerzo o duración de una actividad. La estimación de tres puntos no elimina la incertidumbre, sino que la incorpora explícitamente al cálculo.

### 1.6. Líneas base

Una **línea base** es una versión aprobada de un elemento o conjunto de elementos utilizada como referencia para medir el desempeño y controlar los cambios.

En la dirección de proyectos pueden establecerse, entre otras, líneas base de alcance, cronograma y coste. Las desviaciones se analizan comparando la situación real con las referencias aprobadas.

Las líneas base no son inmutables: pueden modificarse mediante el proceso de control de cambios establecido por el proyecto.

## 2. Gestión de Riesgos y Cambios

En Métrica v3, la gestión de incidencias y cambios se hace en la fase **GPS (Seguimiento y Control)**. A nivel de servicio y operaciones (ITIL), se sistematiza rigurosamente la configuración.

### 2.1. Gestión de Riesgos
Los riesgos son eventos inciertos que, de ocurrir, tienen un efecto positivo (oportunidad) o negativo (amenaza) en los objetivos del proyecto.
*   Deben identificarse, analizarse cualitativamente (Matriz de Probabilidad x Impacto) y cuantificarse (p. ej., simulación de Monte Carlo o Valor Monetario Esperado).
*   **Estrategias frente a Amenazas:** Evitar (eliminar la causa), Transferir (seguros, externalizar), Mitigar (reducir probabilidad/impacto), Aceptar.
*   **Riesgo Residual:** El riesgo que permanece después de aplicar las respuestas.
*   **Riesgo Secundario:** Un nuevo riesgo que surge como consecuencia directa de la implementación de una respuesta al riesgo.

### 2.2. Control de Cambios
Cuando un usuario pide cambiar un requisito, el Jefe de Proyecto realiza un **Análisis de Impacto** (¿cuánto tiempo/dinero extra supone?). El cambio se registra formalmente, pero **solo lo aprueba el Comité de Seguimiento**.

**Integración con ITIL v4 (Change Enablement):**
A nivel de operación de servicios, el cambio se define como “la adición, modificación o eliminación de cualquier cosa que pueda tener un efecto directo o indirecto en los servicios”. ITIL especifica tres tipos de cambios:
1.  **Cambios Estándar:** Son cambios frecuentes, directos, documentados y de riesgo bajo que están preaprobados (ej. ampliación de memoria, cambio de tóner).
2.  **Cambios Normales:** No tienen un proceso preaprobado. Implican un riesgo medio-alto y deben seguir un proceso de programación, evaluación de riesgo y autorización. Requieren un **Plan de back-out** (plan B en caso de imprevistos) y deben ser aprobados por el **CAC (Comité Asesor de Cambios)**.
3.  **Cambios Urgentes/Emergencia:** Necesitan evaluación rápida para resolver incidentes graves o fallos críticos de seguridad; el CAC es más flexible o existe un CAC de Emergencia (eCAB).

### 2.3. Gestión de la Configuración y Versiones
La Gestión de la Configuración garantiza que la información de los activos requeridos (sus estados, relaciones y atributos) esté controlada y precisa.
*   **CIs (Configuration Items / Elementos de Configuración):** Son los componentes que deben ser gestionados para la prestación del servicio.
*   **CMDB (Configuration Management Database):** Es el repositorio central donde se administran y relacionan todos los CIs de la organización.

**Control de Versiones:**
Para el código y la documentación, se utilizan Sistemas de Control de Versiones (VCS) como Git, Subversion o Mercurial. Los conceptos clave para examen incluyen:
*   **Repositorio:** Lugar de almacenamiento de elementos e históricos.
*   **Línea base (Baseline):** Revisión aprobada de un elemento desde la que parten los cambios.
*   **Rama (Branching):** Bifurcación independiente de un elemento.
*   **Integración (Merge) / Commit:** Fusión de cambios y su consolidación en el repositorio.

### 2.4. Gestión del riesgo durante el ciclo de vida

La gestión de riesgos es continua. La identificación inicial debe complementarse con la revisión periódica del registro de riesgos y de la eficacia de las respuestas adoptadas.

Debe distinguirse entre:

* **Riesgo inherente:** exposición antes de considerar las respuestas.
* **Riesgo residual:** exposición que permanece después de aplicar una respuesta.
* **Riesgo secundario:** nuevo riesgo que aparece como consecuencia directa de una respuesta.

También pueden identificarse **riesgos emergentes**, derivados de circunstancias que no estaban previstas inicialmente o que no podían analizarse adecuadamente al comienzo.

### 2.5. Análisis cualitativo y cuantitativo

El análisis cualitativo prioriza los riesgos según criterios como probabilidad, impacto, proximidad y urgencia.

El análisis cuantitativo asigna valores numéricos a los efectos de la incertidumbre sobre objetivos del proyecto. Puede apoyarse en simulaciones, análisis de escenarios, árboles de decisión y Valor Monetario Esperado.

### 2.6. Respuestas a riesgos y oportunidades

Para las amenazas pueden emplearse estrategias como **evitar, transferir, mitigar y aceptar**. Dependiendo del contexto pueden existir estrategias adicionales, como escalar cuando la respuesta requiere una autoridad externa al proyecto.

Para las oportunidades pueden emplearse estrategias como **explotar, compartir, mejorar y aceptar**.

Cada respuesta debe tener un responsable y debe supervisarse su ejecución y eficacia.

### 2.7. Control integrado de cambios

Una solicitud de cambio debe analizarse considerando su impacto sobre alcance, cronograma, coste, calidad, recursos, riesgos, contratos y beneficios.

El control integrado de cambios permite evaluar las modificaciones de forma conjunta y evitar que una decisión local produzca desviaciones no controladas en otros objetivos del proyecto.

Una **solicitud de cambio** no equivale automáticamente a un cambio aprobado. Debe seguir el procedimiento de evaluación, decisión, actualización de las líneas base cuando proceda e información a las partes afectadas.

### 2.8. Gestión de configuración

La gestión de configuración identifica y controla los elementos que constituyen el producto o los productos del proyecto y sus versiones.

Comprende actividades como identificación de elementos de configuración, control de cambios, registro del estado de configuración y auditoría de configuración.

Los elementos de configuración pueden incluir código fuente, documentación, ejecutables, infraestructura, scripts, modelos, especificaciones y otros componentes sujetos a control.

### 2.9. Control de versiones

Los sistemas de control de versiones permiten mantener el historial de cambios y recuperar estados anteriores.

Conceptos habituales son:

* **Repositorio:** almacenamiento de versiones e historial.
* **Commit:** registro de un conjunto de cambios.
* **Branch:** línea independiente de desarrollo.
* **Merge:** integración de cambios procedentes de distintas ramas.
* **Tag:** referencia identificativa de una versión concreta.
* **Baseline:** referencia aprobada utilizada como punto de control.

En proyectos TIC, el control de versiones debe integrarse con los procedimientos de gestión de cambios y configuración.

## 3. Métricas: Valor Ganado (EVM)

El *Earned Value Management* (EVM) es la técnica estrella para integrar alcance, cronograma y recursos para evaluar el desempeño y avance del proyecto. Se basa en tres valores clave:
*   **PV (Valor Planificado / Planned Value):** El presupuesto autorizado asignado al trabajo que *debíamos* haber hecho a día de hoy.
*   **EV (Valor Ganado / Earned Value):** El valor real (presupuestado) del trabajo físicamente *finalizado* a día de hoy.
*   **AC (Coste Real / Actual Cost):** Lo que hemos gastado *realmente* por el trabajo ejecutado hasta hoy.

**Fórmulas Esenciales (Variables de Variación e Índices):**
*   **Variación de Coste (CV):** $CV = EV - AC$. (Si CV > 0, estamos por debajo del presupuesto).
*   **Variación del Cronograma (SV):** $SV = EV - PV$. (Si SV > 0, vamos adelantados).
*   **Índice de Rendimiento de Costes (CPI):** $CPI = \frac{EV}{AC}$. (Si CPI > 1, eficiencia de coste alta).
*   **Índice de Rendimiento del Cronograma (SPI):** $SPI = \frac{EV}{PV}$. (Si SPI > 1, eficiencia de tiempo alta).

**Interpretación de indicadores:**
*   Si **EV > PV**, vas por delante del cronograma (SPI > 1).
*   Si **EV > AC**, estás ahorrando dinero (CPI > 1).

### 3.1. EVM: valores de referencia

El **Valor Ganado (EVM)** integra información de alcance, cronograma y coste mediante tres variables:

* **PV (Planned Value):** valor presupuestado del trabajo planificado hasta una fecha de referencia.
* **EV (Earned Value):** valor presupuestado del trabajo realmente completado hasta esa fecha.
* **AC (Actual Cost):** coste real incurrido para realizar el trabajo completado.

Estas magnitudes deben expresarse con una misma base monetaria o unidad de medida compatible.

### 3.2. Variaciones de coste y cronograma

* **CV = EV − AC**. Un valor positivo indica que el valor ganado supera el coste real.
* **SV = EV − PV**. Un valor positivo indica que el valor ganado supera el valor planificado.

### 3.3. Índices de desempeño

* **CPI = EV / AC**. Un valor superior a 1 indica eficiencia favorable de costes; un valor inferior a 1 indica rendimiento desfavorable.
* **SPI = EV / PV**. Un valor superior a 1 indica progreso superior al planificado; un valor inferior a 1 indica progreso inferior al planificado.

Los indicadores deben interpretarse conjuntamente con las condiciones del proyecto y no de forma aislada.

### 3.4. Previsiones de coste

EVM también permite realizar previsiones:

* **ETC (Estimate to Complete):** coste estimado necesario para completar el trabajo restante.
* **EAC (Estimate at Completion):** coste estimado total al finalizar el proyecto.
* **VAC (Variance at Completion):** diferencia entre el presupuesto al finalizar y el coste estimado final.

Una formulación sencilla, cuando se supone que el rendimiento actual de costes continuará, es:

**EAC = BAC / CPI**

donde **BAC** es el presupuesto al finalizar (*Budget at Completion*).

La elección de la fórmula de previsión depende de las hipótesis sobre el comportamiento futuro del proyecto.

### 3.5. EVM y líneas base

La aplicación de EVM requiere una referencia aprobada contra la que comparar el desempeño. Por ello, las líneas base de alcance, cronograma y coste deben mantenerse bajo control de cambios.

La calidad de los resultados de EVM depende de la calidad de la medición del avance físico y de la correcta imputación de costes.

## 4. Herramientas Colaborativas e Informes

En la gestión de proyectos y servicios TIC, se utilizan diferentes herramientas de colaboración, ticketing y cuadros de mando.

### 4.1. Seguimiento de incidentes e informes
Un sistema de seguimiento de incidentes (ticketing o *bugtracker*) permite administrar, actualizar y resolver problemas reportados. 
*   **Herramientas conocidas:** GLPI, Jira, OTRS (Open-source Ticket Request System), y BMC Helix (anteriormente Remedy).
*   **Métricas de informe y seguimiento operativo:** Los SLA (Acuerdos de Nivel de Servicio) rigen la gobernanza. Para los informes de rendimiento se miden variables críticas como el **MTTR** (Mean Time to Recovery/Repair - Tiempo medio de reparación) y el **MTBF** (Mean Time Between Failures - Tiempo medio entre fallos).

### 4.2. Herramientas colaborativas

Las herramientas colaborativas de gestión de proyectos pueden proporcionar funciones como:

* gestión de tareas y responsables;
* planificación y visualización de cronogramas;
* gestión documental y control de versiones;
* comunicación y reuniones;
* seguimiento de incidencias;
* paneles y cuadros de mando;
* registro de decisiones y cambios;
* gestión de flujos de aprobación;
* integración con repositorios de código y sistemas de automatización.

La herramienta debe seleccionarse atendiendo a las necesidades del proyecto, requisitos de seguridad, trazabilidad, integración, control de acceso, disponibilidad y protección de la información.

### 4.3. Informes de proyecto

Los informes de seguimiento deben proporcionar información suficiente para conocer el estado del proyecto y facilitar la toma de decisiones.

Pueden incluir:

* estado del alcance;
* avance del cronograma;
* ejecución presupuestaria;
* desempeño EVM;
* riesgos y oportunidades;
* cuestiones e incidencias;
* cambios;
* calidad y defectos;
* recursos;
* decisiones pendientes;
* hitos alcanzados y próximos hitos;
* previsiones y desviaciones.

### 4.4. Cuadros de mando y niveles de información

Los cuadros de mando permiten presentar indicadores agregados y facilitar la detección de desviaciones.

La información debe adaptarse al nivel de gestión. La dirección necesita información consolidada sobre objetivos, riesgos, coste, plazo y decisiones; los responsables operativos necesitan mayor detalle sobre tareas, incidencias y entregables.

### 4.5. Seguimiento y escalado

El seguimiento no consiste únicamente en registrar datos, sino en comparar el desempeño con las referencias aprobadas, identificar desviaciones, analizar sus causas y adoptar las medidas oportunas.

Cuando una desviación supera la autoridad delegada o las tolerancias establecidas, debe escalarse al nivel de gobierno correspondiente.

### 4.6. Herramientas de seguimiento de incidencias

Los sistemas de gestión de incidencias permiten registrar la descripción del problema, prioridad, responsable, estado, fechas, evidencias, acciones y resolución.

La información de incidencias debe mantenerse trazable y relacionada, cuando proceda, con requisitos, cambios, elementos de configuración, versiones y entregables.
## 5. Síntesis de conceptos

| Concepto | Palabra Chivata |
| :--- | :--- |
| **WBS (EDT)** | "Descomposición jerárquica", "Árbol", "Entregables", "Regla del 100%", "Paquete de trabajo". |
| **PERT** | "Probabilístico", "Tres estimaciones", "Ruta crítica", "Holgura", "Grafo". |
| **Ruta Crítica (CPM)** | "Holgura cero", "Camino más largo", "Determina la duración del proyecto". |
| **Gantt** | "Diagrama de barras", "Visualización temporal". |
| **EVM (Valor Ganado)** | "Línea base", "Desviación de coste/plazo", "$CPI$", "$SPI$". |
| **Comité de Seguimiento (Métrica v3)** | "Aprueba los cambios de requisitos" (el Jefe de Proyecto solo analiza). |
| **CMDB y CIs (ITIL)** | "Base de datos de configuración", "Elementos de configuración", "Relaciones de servicios". |
| **CAC / CAB (ITIL)** | "Comité Asesor de Cambios", "Aprueba cambios normales". |
| **Plan de Back-out (ITIL)**| "Plan de marcha atrás", "Cambios normales", "Contingencia". |


## 6. Referencias normativas y técnicas

* **ISO 21511:2018**, *Work breakdown structures for project and programme management*.
* **ISO 21508:2026**, *Project, programme and portfolio management — Earned value management*.
* **ISO 21512:2024**, *Project, programme and portfolio management — Earned value management implementation guidance*.
* **PMI**, *A Guide to the Project Management Body of Knowledge (PMBOK® Guide) — Eighth Edition*, 2025.
* **PMI**, publicaciones y guías de referencia sobre Earned Value Management.
* **ITIL 4**, prácticas de Change Enablement y Service Configuration Management, PeopleCert.
* **MÉTRICA v3**, Interfaz de Gestión de Proyectos (GP), Administración Pública española.

### 7. Simulacro de Test: Ejercicios de aplicación

**Pregunta 1:**
*En el contexto de la Gestión del Valor Ganado (EVM), si el índice de rendimiento de costes (CPI) es 0,8, ¿qué significa?*
a) El proyecto está costando un 20% menos de lo planificado.
b) El proyecto está costando un 80% más de lo planificado.
c) Por cada euro invertido, solo estamos obteniendo 0,80 euros de valor.
d) El proyecto va un 20% retrasado.

**Razonamiento:**
1.  **Busca el patrón:** $CPI = \frac{EV}{AC}$. Si CPI < 1, significa que gastamos más de lo que ganamos (ineficiencia).
2.  **Desmontando:**
    *   (A) Imposible, el CPI sería > 1.
    *   (B) Si el CPI fuera 0,8, es una ineficiencia, pero no implica un 80% extra de coste, sino una relación 1:0,8.
    *   (D) El SPI mide el tiempo, el CPI mide el coste. Falsa.
3.  **Respuesta correcta: C.** La definición técnica de CPI es la eficiencia de costes. Un valor de 0,8 indica que por cada unidad monetaria real (AC) aplicada, solo se genera 0,8 unidades de valor ganado (EV).

**Pregunta 2:**
*Un proyecto de migración a la nube para un ministerio está en fase de despliegue. Esta acción implica cierto nivel de riesgo y parada de los sistemas productivos durante el fin de semana. Según los fundamentos de la gestión de cambios de ITIL v4, ¿cómo debe tramitarse este despliegue?*
a) Como un Cambio Estándar, pues las migraciones a la nube son una práctica común de la industria.
b) Como un Cambio Normal, el cual requiere programación, autorización del CAC y un plan de back-out.
c) Como un Cambio Urgente/de Emergencia debido a la parada del fin de semana.
d) Como un elemento de la CMDB sin necesidad de aprobación.

**Razonamiento:**
1.  **Busca el patrón:** Las migraciones a la nube y los cambios que implican un riesgo, pero no solucionan un incidente crítico de forma inmediata, no son estándar ni de emergencia.
2.  **Desmontando:**
    *   (A) Falsa. Los cambios estándar son de bajo riesgo y frecuentes (ej. cambiar un cartucho de impresora).
    *   (C) Falsa. Un cambio urgente se usa para restaurar un servicio caído por un incidente grave.
    *   (D) Falsa. La CMDB registra los elementos, pero la acción es un cambio.
    *   (B) Correcta. Migrar a la nube es el ejemplo de libro de un Cambio Normal, y requiere evaluación de riesgos, aprobación del CAC y plan de back-out.
3.  **Respuesta correcta: B.**