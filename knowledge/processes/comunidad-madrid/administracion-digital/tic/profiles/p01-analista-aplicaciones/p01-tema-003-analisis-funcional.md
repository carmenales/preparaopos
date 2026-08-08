---
id: "cm-ad-tic-p01-tema-003-analisis-funcional-diseño"
title: "Análisis funcional/diseño"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/tic"
profiles:
  - "p01-analista-aplicaciones"
official_profile: "P01 - Analista de Aplicaciones"
official_topic: "Tema 3. Análisis funcional/diseño"
source_ids:
tags:
  - "analisis-funcional"
  - "casos-de-uso"
  - "historias-de-usuario"
  - "scrum"
  - "kanban"
  - "dsdm"
  - "cmmi"
  - "tdd"
  - "bdd"
  - "iso-29148"
created_at: "2026-08-08"
last_reviewed: "2026-08-08"
ai_generated: true
ai_sources:
  - "gemini"
  - "perplexity"
needs_human_review: true
---

# Tema 3. Análisis funcional/diseño

## 1. Análisis Funcional y de Requisitos

El análisis funcional es la fase donde definimos **qué** debe hacer el sistema, sin entrar todavía en **cómo** lo va a hacer técnicamente a nivel de código. La base de esto es la Ingeniería de Requerimientos.

### 1.1. Ingeniería de Requerimientos
Su tarea principal es generar especificaciones correctas, claras y sin ambigüedades sobre el comportamiento del sistema.

> **Norma de referencia:** El estándar internacional que regula formalmente la Ingeniería de Requisitos es la **ISO/IEC/IEEE 29148:2018** *"Systems and software engineering — Life cycle processes — Requirements engineering"*, que sustituyó a los antiguos IEEE 830, IEEE 1233 e IEEE 1362. Define el **proceso de elicitación de requisitos** (*requirements elicitation*) como el proceso mediante el cual el adquirente y los proveedores del sistema descubren, revisan, articulan, entienden y documentan los requisitos del sistema y sus procesos de ciclo de vida.

**Técnicas principales de obtención de requisitos:**
*   **Entrevistas:** Encuentros "cara a cara" con los usuarios. Requieren preparación previa, envío de un guion y elaboración de un acta final.
*   **Reuniones JAD (Joint Application Design):** Sesiones de trabajo largas y preparadas para conseguir consenso rápido. Reúnen a usuarios, desarrolladores y un moderador. El objetivo es reducir el tiempo de desarrollo manteniendo la calidad.
*   **Reuniones JRP (Joint Requirement Planning):** Similares a las JAD, pero enfocadas a la Alta Dirección para tomar decisiones estratégicas.
*   **Cuestionarios/encuestas:** útiles cuando el número de usuarios afectados es muy grande y no es viable entrevistar a todos.
*   **Observación directa (*Job shadowing*):** el analista observa al usuario realizar su trabajo real, útil para detectar requisitos implícitos que el usuario no verbaliza.
*   **Tormenta de ideas (*brainstorming*) y talleres de trabajo:** generación creativa de requisitos en grupo.
*   **Prototipado:** construcción de una versión preliminar (maqueta o prototipo funcional) del sistema para validar requisitos con el usuario antes de construir la solución final.
*   **Análisis de documentación existente:** manuales, normativa, procedimientos y sistemas legados como fuente de requisitos.
*   **Técnicas de grupo nominal y Delphi:** para llegar a consenso entre expertos de forma estructurada, minimizando sesgos de grupo.

### 1.2. Tipos de requisitos y sus atributos de calidad

**Clasificación de requisitos:**

*   **Requisitos funcionales (RF):** describen **qué** debe hacer el sistema; una acción o comportamiento concreto ante una entrada.
*   **Requisitos no funcionales (RNF):** describen **cómo** debe comportarse el sistema en términos de calidad (rendimiento, seguridad, usabilidad, disponibilidad, mantenibilidad, portabilidad, etc.), sin especificar una función concreta.
*   **Requisitos de negocio, de usuario, de sistema y de diseño/implementación:** distintos niveles de abstracción según la ISO/IEC/IEEE 29148, desde la necesidad de negocio hasta el requisito técnico concreto que implementa el desarrollador.

El estándar **ISO/IEC 25010** (modelo de calidad de producto software, sucesor de ISO/IEC 9126) es la referencia oficial para clasificar los **requisitos no funcionales** en 8 características: *Functional suitability* (idoneidad funcional), *Performance efficiency* (eficiencia de desempeño), *Compatibility*, *Usability*, *Reliability*, *Security*, *Maintainability* y *Portability*.

**Atributos de un buen requisito (ISO/IEC/IEEE 29148):** necesario, no ambiguo, completo, singular (atómico), factible, verificable, correcto y conforme (con estándares aplicables).

**Trazabilidad de requisitos:** capacidad de seguir la vida de un requisito desde su origen (necesidad de negocio) hasta su implementación y prueba, en ambas direcciones (hacia atrás y hacia adelante). Es clave para la gestión del cambio y para la auditoría en procesos certificados bajo CMMI o ISO 9001.

**Validación vs. Verificación de requisitos:**

*   **Verificación:** ¿estamos construyendo el sistema correctamente? (¿el producto cumple la especificación?).
*   **Validación:** ¿estamos construyendo el sistema correcto? (¿la especificación satisface la necesidad real del usuario?).

### 1.3. Casos de Uso e Historias de Usuario

Son las dos herramientas principales para documentar requisitos, dependiendo de si usamos metodologías tradicionales o ágiles.

*   **Historias de Usuario (Metodologías Ágiles - XP/Scrum):**
    *   Son tarjetas de papel donde el cliente describe brevemente una característica que el sistema debe tener.
    *   Se descomponen luego en tareas de programación.
    *   **Estructura patrón:** "Como [Rol], quiero [Funcionalidad], para [Beneficio/Objetivo]". Ejemplo real: "Como ciudadano, quiero un botón de descarga en PDF para guardar mi certificado de empadronamiento".

*   **Casos de Uso (Metodologías Tradicionales/UML - Métrica v3):**
    *   Definen la interacción exacta entre un "Actor" (un usuario u otro sistema) y el sistema.
    *   Especifican el comportamiento del sistema.
    *   Tienen un flujo principal (lo que pasa si todo va bien) y flujos alternativos (excepciones).

**Anatomía completa de un Caso de Uso (UML/ISO 29148):**
*   **Nombre:** verbo + sustantivo (ej. "Solicitar certificado").
*   **Actor principal:** quien inicia la interacción (puede ser humano u otro sistema).
*   **Actores secundarios:** los que participan pero no inician.
*   **Precondiciones:** estado del sistema necesario antes de ejecutar el caso de uso.
*   **Postcondiciones (garantías de éxito):** estado del sistema tras completarse con éxito.
*   **Flujo principal (camino feliz):** secuencia numerada de pasos sin errores.
*   **Flujos alternativos:** variaciones válidas del flujo principal.
*   **Flujos de excepción:** gestión de errores.
*   **Relaciones entre casos de uso (UML):**
    *   **Include** (`<<include>>`): un caso de uso *siempre* incluye la ejecución de otro (obligatorio, ej. "Realizar pedido" incluye "Verificar stock").
    *   **Extend** (`<<extend>>`): un caso de uso *opcionalmente* extiende a otro en ciertas condiciones (ej. "Pagar con tarjeta" extiende a "Realizar pedido").
    *   **Generalización:** un actor o caso de uso especializa a otro más general.
**Historias de Usuario, criterio INVEST y criterios de aceptación:**
Una buena historia de usuario debe cumplir el acrónimo **INVEST**:
*   **I**ndependiente: puede desarrollarse sin depender estrictamente de otra.
*   **N**egociable: no es un contrato cerrado, se puede discutir con el cliente.
*   **V**aliosa: aporta valor de negocio al usuario final.
*   **E**stimable: el equipo puede estimar su esfuerzo.
*   **S**mall (pequeña): cabe en un sprint.
*   **T**estable: existen criterios claros para comprobar que está terminada.
Las historias de usuario se acompañan de **criterios de aceptación**: condiciones concretas que deben cumplirse para considerar la historia "terminada" (*Done*). Frecuentemente se redactan en formato Gherkin (Dado/Cuando/Entonces), enlazando con BDD (ver apartado 3.2).

Jerarquía habitual en ágil: **Épica** (gran bloque de valor, varias historias) → **Historia de usuario** → **Tareas** (unidades técnicas de trabajo del equipo).

**Cuándo usar cada técnica:**

| Aspecto | Casos de Uso | Historias de Usuario |
| :--- | :--- | :--- |
| Metodología típica | Tradicional/UML (Métrica v3, RUP) | Ágil (Scrum, XP) |
| Nivel de detalle | Alto, formal, exhaustivo | Bajo, conversacional |
| Foco | Interacción actor-sistema | Valor de negocio para el usuario |
| Cuándo se completa el detalle | Al inicio (documento cerrado) | Progresivamente, justo a tiempo |
| Verificación | Flujos alternativos/excepción | Criterios de aceptación |

---

## 2. Metodologías Ágiles de Desarrollo

Las metodologías ágiles valoran la adaptación al cambio, las entregas tempranas y la interacción de los individuos por encima de los procesos rígidos y la documentación exhaustiva.

**Manifiesto Ágil (2001):** origen formal de la filosofía ágil. Establece 4 valores:

1. Individuos e interacciones sobre procesos y herramientas.
2. Software funcionando sobre documentación extensiva.
3. Colaboración con el cliente sobre negociación contractual.
4. Respuesta ante el cambio sobre seguimiento de un plan.

Y 12 principios, entre los que destacan (muy preguntados): satisfacer al cliente mediante entrega temprana y continua de software con valor; aceptar los cambios de requisitos incluso en fases avanzadas; entregar software funcionando frecuentemente (semanas, no meses); la simplicidad es esencial; los equipos auto-organizados producen las mejores arquitecturas y diseños.

### 2.1. Scrum
Es un marco de trabajo iterativo e incremental para proyectos en entornos complejos.

**Base normativa:** Scrum se define formalmente en la **Scrum Guide** (Ken Schwaber y Jeff Sutherland), documento de referencia oficial y gratuito, actualizado por última vez en 2020. Scrum se define allí como un **marco de trabajo ligero** (no una metodología, no un proceso ni una técnica) que ayuda a las personas, equipos y organizaciones a generar valor a través de soluciones adaptativas a problemas complejos.

Scrum se fundamenta en el **empirismo** (el conocimiento procede de la experiencia y de tomar decisiones basadas en lo observado) y en la teoría de control de procesos **Lean**, apoyándose en **3 pilares**: **Transparencia, Inspección y Adaptación**.

**Valores de Scrum (5):** Compromiso, Foco, Apertura, Respeto y Coraje.

**Patrón Lógico - Los Roles:**

**Terminología oficial actualizada (Scrum Guide 2020):** desde 2020 no se habla de "3 roles" separados sino de un único **Scrum Team**, compuesto por 10 o menos personas, que incluye tres tipos de **responsabilidades (accountabilities)**:

1.  **Product Owner (El cliente):** Escribe las historias de usuario y prioriza el trabajo (Product Backlog) basándose en el valor de negocio.
    > Es el **único responsable** de gestionar el Product Backlog, incluyendo redactar los elementos, ordenarlos por valor y asegurar que sean transparentes y comprendidos por el equipo.
2.  **Scrum Master (El facilitador):** Mantiene el proceso, elimina obstáculos (impedimentos) y protege al equipo de interrupciones externas. No es un jefe, es un facilitador.
    > Es responsable de establecer Scrum tal y como se define en la Guía Scrum, ayudando a todos a entender la teoría y práctica de Scrum, tanto dentro del Scrum Team como en la organización.
3.  **Team (El equipo de desarrollo):** Equipo autoorganizado (de 4 a 9 personas) que construye el software.
    > Terminología 2020: **Developers**, los profesionales del Scrum Team comprometidos con crear cualquier aspecto de un Incremento utilizable en cada Sprint. Son **auto-gestionados** (deciden internamente quién hace qué, cuándo y cómo), característica que sustituye al término "autoorganizado".

**Patrón Lógico - Los Artefactos y Eventos:**
*   **Sprint:** Iteración de 1 a 4 semanas. Durante el Sprint, los requisitos están congelados.
    > Cada Sprint puede considerarse un proyecto corto y tiene una duración máxima de **un mes**; cuanto más largo es el Sprint, más riesgo de que cambie la definición de "hecho", el valor se reduzca o la complejidad aumente. Los Sprints permiten la **previsibilidad** al asegurar inspección y adaptación al menos cada mes.
*   **Product Backlog:** Lista completa y priorizada de todo lo que el sistema necesita.
*   **Sprint Backlog:** Subconjunto del Product Backlog que el equipo se compromete a hacer en el Sprint actual.
    > Está compuesto por el objetivo del Sprint (*Sprint Goal*), los elementos del Product Backlog seleccionados para el Sprint y un plan de acción para entregar el Incremento.
*   **Incremento:** *(artefacto no citado en el apunte original y clave en examen)* es un peldaño concreto hacia la Visión u objetivo del producto; cada Incremento se suma a los anteriores y se verifica exhaustivamente, garantizando que todos los Incrementos funcionan juntos.
*   **Daily Scrum:** Reunión diaria de 15 minutos, de pie, para sincronizar el trabajo.
    > La realizan únicamente los **Developers**; es un evento para inspeccionar el progreso hacia el Sprint Goal y adaptar el Sprint Backlog si es necesario.
*   **Sprint Planning:** *(evento no citado en el apunte original)* inicia el Sprint; en ella se decide qué se puede conseguir en el Sprint (Sprint Goal) y cómo se llevará a cabo el trabajo elegido.
*   **Sprint Review:** Reunión al final del Sprint para mostrar el software funcionando a los interesados (Stakeholders).
    > Su propósito es inspeccionar el resultado del Sprint y determinar futuras adaptaciones.
*   **Sprint Retrospective:** Reunión interna del equipo para analizar qué ha ido bien y qué mejorar en sus procesos.
    > Cierra el Sprint; el Scrum Team inspecciona cómo fue el último Sprint en cuanto a individuos, interacciones, procesos, herramientas y su Definición de Terminado.

**Definición de Terminado (*Definition of Done*, DoD):** descripción formal del estado del Incremento cuando cumple las medidas de calidad requeridas para el producto. En cuanto un elemento del Product Backlog cumple la DoD, nace un Incremento. Es un concepto muy preguntado porque garantiza transparencia y calidad homogénea.

### 2.2. Kanban
Método para gestionar el flujo de trabajo con énfasis en la entrega "justo a tiempo".

> **Origen y principios:** Kanban (palabra japonesa: "tarjeta visual") proviene del sistema de producción de Toyota (Lean Manufacturing) y fue adaptado al desarrollo software por David J. Anderson. A diferencia de Scrum, **no exige roles ni eventos fijos**, no trabaja en Sprints con duración fija, y puede aplicarse como capa de mejora continua sobre cualquier proceso existente (incluido Scrum, dando lugar a "Scrumban").

**Los 4 principios básicos de Kanban:**
1. Empezar con lo que se hace ahora (no exige rediseñar el proceso desde cero).
2. Acordar realizar cambios incrementales y evolutivos.
3. Respetar inicialmente los roles, responsabilidades y cargos actuales.
4. Fomentar el liderazgo en todos los niveles.

**Patrón Lógico y Reglas Clave:**
1.  **Mostrar el proceso:** Uso de un tablero visual con columnas (Ej: Cola, Análisis, Desarrollo, Pruebas).
2.  **Limitar el Trabajo en Curso (WIP - Work In Progress):** Regla fundamental. Se fija un límite máximo de tareas por columna para evitar cuellos de botella.
3.  **Optimizar el flujo (Cycle Time / Lead Time):** Se mide el tiempo desde que una tarea entra al tablero hasta que sale.
    > **Matiz examinable:** el **Lead Time** mide desde que la tarea se *solicita* hasta que se *entrega*; el **Cycle Time** mide desde que el equipo *empieza a trabajar* en ella hasta que se completa. Son métricas distintas, y confundirlas es una trampa habitual de test.
4.  **Gestionar el flujo explícitamente:** definir y comunicar políticas claras de cómo se mueven las tareas entre columnas.
5.  **Mejora colaborativa mediante modelos y método científico:** uso de métricas (como el diagrama de flujo acumulado) para detectar cuellos de botella y mejorar continuamente.

### 2.3. DSDM (Dynamic Systems Development Method)
Enfoque iterativo e incremental basado en el desarrollo rápido de aplicaciones (RAD).

**Patrón Lógico de DSDM:**
*   **Fijo:** El tiempo (plazos) y el presupuesto están fijados estrictamente desde el principio.
*   **Variable:** Los requisitos son variables y se negocian para asegurar que se cumple el plazo.

**Los 8 Principios de DSDM (DSDM Agile Project Framework, oficial):**

1. Centrarse en la necesidad del negocio (*Focus on the business need*).
2. Entregar a tiempo (*Deliver on time*).
3. Colaborar (*Collaborate*).
4. No comprometer nunca la calidad (*Never compromise quality*).
5. Construir incrementalmente sobre cimientos firmes (*Build incrementally from firm foundations*).
6. Desarrollar iterativamente (*Develop iteratively*).
7. Comunicarse de forma continua y clara (*Communicate continuously and clearly*).
8. Demostrar control (*Demonstrate control*).

**Priorización MoSCoW:** técnica de priorización de requisitos característica de DSDM (aunque usada también en otras metodologías), que clasifica cada requisito en:
*   **M**ust have (imprescindible).
*   **S**hould have (importante pero no crítico).
*   **C**ould have (deseable si hay tiempo).
*   **W**on't have this time (aplazado a una futura iteración).

**Ciclo de vida DSDM:** Pre-proyecto → Viabilidad → Fundamentos → Desarrollo iterativo evolutivo → Despliegue → Post-proyecto.

**Relación con RAD:** DSDM nació en 1994 como una respuesta estructurada al RAD (*Rapid Application Development*), aportando disciplina y gobernanza al desarrollo rápido, algo que el RAD original no garantizaba.

> **Cuadro comparativo Scrum vs. Kanban vs. DSDM (muy útil para examen):**

| Característica | Scrum | Kanban | DSDM |
| :--- | :--- | :--- | :--- |
| Iteraciones | Sprints de duración fija (1-4 semanas) | Flujo continuo, sin iteraciones fijas | Timeboxes, con plazo y presupuesto fijos |
| Roles definidos | Sí (PO, SM, Developers) | No exige roles nuevos | Sí (varios roles formales: Business Sponsor, Business Visionary, Technical Coordinator, etc.) |
| Qué es fijo | El calendario del Sprint | El límite WIP | Tiempo y presupuesto |
| Qué es variable | El alcance dentro del Sprint | El orden/prioridad de tareas | El alcance/requisitos (vía MoSCoW) |
| Métrica clave | Velocidad del equipo | Lead Time / Cycle Time | Cumplimiento de plazo con calidad |

---

## 3. Pruebas Funcionales y Metodologías Dirigidas por Pruebas

**Tipos y niveles de prueba (marco general, examinable):**
*   **Pruebas unitarias:** verifican el correcto funcionamiento de una unidad mínima de código (función, método) de forma aislada.
*   **Pruebas de integración:** comprueban la correcta comunicación entre varios módulos o componentes.
*   **Pruebas de sistema:** validan el sistema completo frente a los requisitos funcionales especificados.
*   **Pruebas de aceptación (UAT — User Acceptance Testing):** las realiza el usuario/cliente final para confirmar que el sistema cumple sus necesidades reales; son las que dan el visto bueno final antes de producción.
*   **Pruebas de regresión:** se repiten tras cada cambio para verificar que no se han introducido nuevos errores.
*   **Pruebas funcionales vs. no funcionales:** las funcionales verifican *qué hace* el sistema (entradas/salidas esperadas); las no funcionales verifican *cómo lo hace* (rendimiento, carga, seguridad, usabilidad).

### 3.1. TDD (Test Driven Development - Desarrollo Guiado por Pruebas)
Metodología donde **primero se escribe la prueba** antes de escribir el código fuente.
*   **Ciclo patrón:**
    1. Escribir una prueba que falla (porque el código no existe).
    2. Escribir el código más simple posible (KISS) para que la prueba pase.
    3. Refactorizar (limpiar y optimizar el código eliminando duplicidades).

Este ciclo se conoce popularmente como **Red-Green-Refactor** (rojo: la prueba falla; verde: la prueba pasa; refactor: se mejora el código sin romper la prueba). Fue popularizado por Kent Beck en el contexto de Extreme Programming (XP). Su beneficio principal es que el diseño del código emerge de las propias pruebas, favoreciendo bajo acoplamiento y alta cohesión.

### 3.2. BDD (Behavior Driven Development - Desarrollo Orientado al Comportamiento)
Evolución del TDD que fomenta la colaboración entre desarrolladores, probadores y clientes. Se usan lenguajes naturales estructurados (como Gherkin: `Dado que... Cuando... Entonces...`) para definir el comportamiento del sistema de forma que el cliente lo entienda fácilmente.

BDD nació de la mano de Dan North como refinamiento de TDD, trasladando el foco desde "probar unidades de código" hacia "describir comportamientos de negocio". Herramientas típicas asociadas: **Cucumber**, **SpecFlow**, **JBehave**. La estructura Gherkin (`Given / When / Then`) permite que los criterios de aceptación de una historia de usuario se conviertan directamente en pruebas automatizables, cerrando el círculo entre requisitos ágiles (historias de usuario) y pruebas funcionales.

**ATDD (Acceptance Test Driven Development):** enfoque hermano de TDD y BDD donde los criterios de aceptación se escriben de forma colaborativa (cliente, desarrollador, tester) *antes* de codificar, y se convierten directamente en las pruebas de aceptación del sistema.

---

## 4. Enfoque CMMI (Capability Maturity Model Integration)

CMMI es un modelo para evaluar la madurez de los procesos de desarrollo de software de una organización. Identifica 5 niveles de madurez:
1.  **Inicial:** Procesos impredecibles, reactivos y caóticos. Depende del heroísmo individual.
2.  **Gestionado (Managed):** Proyectos planificados, medidos y controlados a nivel básico.
3.  **Definido:** Procesos estandarizados y documentados a nivel de toda la organización.
4.  **Gestionado Cuantitativamente:** Se usan métricas estadísticas para controlar el rendimiento.
5.  **En Optimización:** Mejora continua de los procesos.

**Origen y titularidad:** CMMI fue desarrollado originalmente por el **Software Engineering Institute (SEI)** de la Universidad Carnegie Mellon, y actualmente su mantenimiento corresponde al **CMMI Institute** (integrado en ISACA). Es un modelo de referencia para la mejora de procesos, aplicable a desarrollo (CMMI-DEV), adquisición (CMMI-ACQ) y servicios (CMMI-SVC).

**Dos representaciones posibles de CMMI (distinción muy preguntada):**
*   **Representación por Etapas (*Staged*):** la organización avanza por los 5 **niveles de madurez** de forma secuencial y global (los descritos arriba). Es la más citada en oposición.
*   **Representación Continua (*Continuous*):** la organización mejora **áreas de proceso individuales**, cada una con su propio **nivel de capacidad** (0 a 3: Incompleto, Realizado, Gestionado, Definido), sin necesidad de seguir un orden global.

**Áreas de proceso (Process Areas) relacionadas directamente con el análisis funcional (CMMI-DEV):**
*   **Requirements Management (REQM)** — Gestión de Requisitos: área de **Nivel de madurez 2**. Su propósito es gestionar los requisitos del proyecto y sus productos, e identificar inconsistencias entre esos requisitos y los planes/productos de trabajo del proyecto.
*   **Requirements Development (RD)** — Desarrollo de Requisitos: área de **Nivel de madurez 3**. Su propósito es **elicitar, analizar y establecer** los requisitos de cliente, producto y componentes de producto, mediante tres metas específicas: 1) Desarrollar los Requisitos del Cliente, 2) Desarrollar los Requisitos del Producto, y 3) Analizar y Validar los Requisitos.
*   *(Nota: en CMMI v2.0, ambas áreas se han unificado conceptualmente en la práctica **Requirements Development and Management — RDM**.)*

**Relación CMMI ↔ Ágil:** aunque tradicionalmente se percibían como incompatibles (CMMI = documentación exhaustiva vs. Ágil = documentación mínima), el propio SEI reconoce que se pueden combinar: los niveles de madurez CMMI valoran *qué* procesos deben existir y ser medibles, no *cómo* se ejecutan; Scrum o XP pueden ser el "cómo" que satisface las metas de REQM/RD exigidas por CMMI (enfoque conocido como "Agile + CMMI" o, en investigación académica, propuestas como "xScrum").

---

## 5. Metodologías Ágiles: cuadro-resumen normativo

> **Tabla síntesis final (repaso rápido antes de examen):**

| Metodología | Tipo de enfoque | Qué es fijo | Qué es variable | Documento/fuente oficial |
| :--- | :--- | :--- | :--- | :--- |
| Scrum | Marco de trabajo empírico, iterativo-incremental | Duración del Sprint | Alcance dentro del Sprint | Scrum Guide (Schwaber & Sutherland, 2020) |
| Kanban | Método de gestión de flujo continuo | Límite WIP por columna | Orden y ritmo de entrada de tareas | Origen: Toyota Production System / D.J. Anderson |
| DSDM | Framework ágil de gestión de proyectos (extensión de RAD) | Tiempo y presupuesto | Requisitos/alcance (vía MoSCoW) | DSDM Agile Project Framework |
| TDD | Práctica de desarrollo dirigida por pruebas | El ciclo Red-Green-Refactor | El diseño interno del código | Kent Beck / Extreme Programming |
| BDD | Práctica de especificación de comportamiento | El lenguaje Gherkin (Given/When/Then) | La granularidad del escenario | Dan North |

---

## 6. Patrones de Examen y "Palabras Chivatas"

| Concepto | Palabra Chivata en el Test |
| :--- | :--- |
| **Scrum** | "Marco de trabajo", "Iterativo e incremental", "Autoorganizado/auto-gestionado", "Sprints", "Empirismo", "Transparencia-Inspección-Adaptación". |
| **Product Owner** | "Voz del cliente", "Prioriza el Backlog", "Maximiza el valor", "Único responsable del Product Backlog". |
| **Scrum Master** | "Elimina impedimentos/obstáculos", "Facilitador", "No es un jefe". |
| **Developers/Equipo** | "Auto-gestionado", "Construye el Incremento", "10 o menos personas". |
| **Kanban** | "Límites WIP", "Tablero visual", "Flujo continuo", "Just in time", "No exige roles ni Sprints". |
| **DSDM** | "Presupuestos y plazos estrictos/fijos", "Extensión de RAD", "MoSCoW", "8 principios". |
| **JAD (Joint Application Design)** | "Reuniones largas estructuradas", "Usuarios y desarrolladores", "Prototipos". |
| **JRP (Joint Requirement Planning)** | "Alta Dirección", "decisiones estratégicas". |
| **TDD** | "Prueba antes que el código", "Refactorización", "Red-Green-Refactor". |
| **BDD** | "Dado/Cuando/Entonces", "Gherkin", "Comportamiento", "Colaboración cliente-dev-tester". |
| **CMMI** | "5 niveles de madurez", "Requirements Management = Nivel 2", "Requirements Development = Nivel 3", "SEI/CMMI Institute". |
| **Casos de uso** | "Actor", "flujo principal/alternativo/excepción", "include/extend". |
| **Historias de usuario** | "Como... quiero... para...", "INVEST", "criterios de aceptación". |

### 6.1. Simulacro de Test: Desmontando trampas

**Pregunta:**
*En el marco de trabajo Scrum, ¿quién es el único responsable de decidir qué elementos del Product Backlog tienen mayor prioridad para el negocio y, por tanto, deben desarrollarse primero?*
a) El Scrum Master, ya que gestiona el proceso.
b) El Director del Proyecto.
c) El Product Owner.
d) El Equipo de Desarrollo de forma consensuada.

**Razonamiento Estructurado:**
1.  **Busca la palabra chivata:** El enunciado pregunta por el "único responsable de decidir qué elementos tienen mayor prioridad para el negocio" en Scrum.
2.  **Aplica el patrón:**
    *   El equipo de desarrollo (D) construye.
    *   El Scrum Master (A) facilita y quita estorbos, no decide prioridades de negocio.
    *   El Director de Proyecto (B) es un rol de metodologías clásicas (como Métrica v3), pero en Scrum puro **no existe** la figura del Director de Proyecto como tal que dicte prioridades de negocio.
    *   El **Product Owner** (C) es literalmente "la voz del cliente" y el dueño del producto. Su única función clave es ordenar el Backlog.
3.  **Respuesta correcta:** C.

**Pregunta:**
*Según CMMI-DEV, ¿en qué nivel de madurez se sitúa el área de proceso "Requirements Development" (Desarrollo de Requisitos)?*
a) Nivel 1 (Inicial).
b) Nivel 2 (Gestionado).
c) Nivel 3 (Definido).
d) Nivel 5 (En Optimización).

**Razonamiento Estructurado:**
1.  **Distingue REQM de RD:** "Requirements **Management**" (gestionar inconsistencias entre requisitos y planes) es Nivel 2; "Requirements **Development**" (elicitar, analizar y establecer los requisitos) es Nivel 3.
2.  **Respuesta correcta:** C.

**Pregunta:**
*¿Cuál de las siguientes NO es uno de los 8 principios oficiales de DSDM?*
a) Centrarse en la necesidad del negocio.
b) Nunca comprometer la calidad.
c) Priorizar siempre el coste sobre el plazo.
d) Comunicarse de forma continua y clara.

**Razonamiento Estructurado:**
1.  Los 8 principios de DSDM giran en torno a negocio, plazo, colaboración, calidad, construcción incremental, iteración, comunicación y control; en ningún caso se prioriza "el coste sobre el plazo" como principio explícito.
2.  **Respuesta correcta:** C.
