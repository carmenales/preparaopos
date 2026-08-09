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
  - "A2_Bloque_III.pdf"
  - "A2_Bloque_IV.pdf"
  - "gemini"
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
A nivel de operación de servicios, el cambio se define como “la adición, modificación o eliminación de cualquier cosa que pueda tener un efecto directo o indirecto en los servicios”[cite: 5]. ITIL especifica tres tipos de cambios[cite: 5]:
1.  **Cambios Estándar:** Son cambios frecuentes, directos, documentados y de riesgo bajo que están preaprobados (ej. ampliación de memoria, cambio de tóner)[cite: 5].
2.  **Cambios Normales:** No tienen un proceso preaprobado. Implican un riesgo medio-alto y deben seguir un proceso de programación, evaluación de riesgo y autorización[cite: 5]. Requieren un **Plan de back-out** (plan B en caso de imprevistos) y deben ser aprobados por el **CAC (Comité Asesor de Cambios)**[cite: 5].
3.  **Cambios Urgentes/Emergencia:** Necesitan evaluación rápida para resolver incidentes graves o fallos críticos de seguridad; el CAC es más flexible o existe un CAC de Emergencia (eCAB)[cite: 5].

### 2.3. Gestión de la Configuración y Versiones
La Gestión de la Configuración garantiza que la información de los activos requeridos (sus estados, relaciones y atributos) esté controlada y precisa[cite: 5].
*   **CIs (Configuration Items / Elementos de Configuración):** Son los componentes que deben ser gestionados para la prestación del servicio[cite: 5].
*   **CMDB (Configuration Management Database):** Es el repositorio central donde se administran y relacionan todos los CIs de la organización[cite: 5].

**Control de Versiones:**
Para el código y la documentación, se utilizan Sistemas de Control de Versiones (VCS) como Git, Subversion o Mercurial[cite: 5]. Los conceptos clave para examen incluyen[cite: 5]:
*   **Repositorio:** Lugar de almacenamiento de elementos e históricos[cite: 5].
*   **Línea base (Baseline):** Revisión aprobada de un elemento desde la que parten los cambios[cite: 5].
*   **Rama (Branching):** Bifurcación independiente de un elemento[cite: 5].
*   **Integración (Merge) / Commit:** Fusión de cambios y su consolidación en el repositorio[cite: 5].

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

**Patrones rápidos para el test:**
*   Si **EV > PV**, vas por delante del cronograma (SPI > 1).
*   Si **EV > AC**, estás ahorrando dinero (CPI > 1).

## 4. Herramientas Colaborativas e Informes

En la gestión de proyectos y servicios TIC, se utilizan diferentes herramientas de colaboración, ticketing y cuadros de mando.

### 4.1. Seguimiento de Incidentes e Informes
Un sistema de seguimiento de incidentes (ticketing o *bugtracker*) permite administrar, actualizar y resolver problemas reportados[cite: 5]. 
*   **Herramientas conocidas:** GLPI, Jira, OTRS (Open-source Ticket Request System), y BMC Helix (anteriormente Remedy)[cite: 5].
*   **Métricas de informe y seguimiento operativo:** Los SLA (Acuerdos de Nivel de Servicio) rigen la gobernanza. Para los informes de rendimiento se miden variables críticas como el **MTTR** (Mean Time to Recovery/Repair - Tiempo medio de reparación)[cite: 5] y el **MTBF** (Mean Time Between Failures - Tiempo medio entre fallos)[cite: 5].

## 5. Patrones de Examen y "Palabras Chivatas"

| Concepto | Palabra Chivata |
| :--- | :--- |
| **WBS (EDT)** | "Descomposición jerárquica", "Árbol", "Entregables", "Regla del 100%", "Paquete de trabajo". |
| **PERT** | "Probabilístico", "Tres estimaciones", "Ruta crítica", "Holgura", "Grafo". |
| **Ruta Crítica (CPM)** | "Holgura cero", "Camino más largo", "Determina la duración del proyecto". |
| **Gantt** | "Diagrama de barras", "Visualización temporal". |
| **EVM (Valor Ganado)** | "Línea base", "Desviación de coste/plazo", "$CPI$", "$SPI$". |
| **Comité de Seguimiento (Métrica v3)** | "Aprueba los cambios de requisitos" (el Jefe de Proyecto solo analiza). |
| **CMDB y CIs (ITIL)** | "Base de datos de configuración", "Elementos de configuración", "Relaciones de servicios"[cite: 5]. |
| **CAC / CAB (ITIL)** | "Comité Asesor de Cambios", "Aprueba cambios normales"[cite: 5]. |
| **Plan de Back-out (ITIL)**| "Plan de marcha atrás", "Cambios normales", "Contingencia"[cite: 5]. |

### 5.1. Simulacro de Test: Desmontando trampas

**Pregunta 1:**
*En el contexto de la Gestión del Valor Ganado (EVM), si el índice de rendimiento de costes (CPI) es 0,8, ¿qué significa?*
a) El proyecto está costando un 20% menos de lo planificado.
b) El proyecto está costando un 80% más de lo planificado.
c) Por cada euro invertido, solo estamos obteniendo 0,80 euros de valor.
d) El proyecto va un 20% retrasado.

**Razonamiento Estructurado:**
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

**Razonamiento Estructurado:**
1.  **Busca el patrón:** Las migraciones a la nube y los cambios que implican un riesgo, pero no solucionan un incidente crítico de forma inmediata, no son estándar ni de emergencia[cite: 5].
2.  **Desmontando:**
    *   (A) Falsa. Los cambios estándar son de bajo riesgo y frecuentes (ej. cambiar un cartucho de impresora)[cite: 5].
    *   (C) Falsa. Un cambio urgente se usa para restaurar un servicio caído por un incidente grave[cite: 5].
    *   (D) Falsa. La CMDB registra los elementos, pero la acción es un cambio.
    *   (B) Correcta. Migrar a la nube es el ejemplo de libro de un Cambio Normal, y requiere evaluación de riesgos, aprobación del CAC y plan de back-out[cite: 5].
3.  **Respuesta correcta: B.**