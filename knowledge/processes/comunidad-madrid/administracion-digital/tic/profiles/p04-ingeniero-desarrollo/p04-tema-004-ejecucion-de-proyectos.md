---
id: "cm-ad-tic-p04-tema-004-ejecucion-proyectos"
title: "Ejecución de proyectos"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/tic"
profiles:
  - "p04-ingeniero-desarrollo"
official_profile: "P04 - Ingeniero de Desarrollo"
official_topic: "Tema 4. Ejecución de proyectos"
source_ids:
  - "A2_Bloque_III.pdf"
  - "A2_Bloque_IV.pdf"
tags:
  - "ejecucion-proyectos"
  - "roles"
  - "organizacion"
  - "metrica-v3"
  - "scrum"
  - "prince2"
  - "pmbok"
created_at: "2026-08-08"
last_reviewed: "2026-08-08"
ai_generated: true
ai_sources:
  - "chatgpt"
  - "gemini"
  - "perplexity"
needs_human_review: true
---

# Tema 4. Ejecución de proyectos

## 1. Formas de Organización de los Proyectos

Como ingeniero de desarrollo, saber cómo está estructurado el poder en tu proyecto te ahorra muchos quebraderos de cabeza. En el test, suelen preguntar por el tipo de estructura organizativa y el grado de autoridad del Jefe de Proyecto según el PMBOK.

**Tipos de organización:**
1.  **Organización Funcional (Clásica):** Agrupación por especialidad (ej. todos los programadores en el "Departamento de Desarrollo", los de redes en "Sistemas"). El Jefe de Proyecto **apenas tiene autoridad**; manda el jefe del departamento funcional.
2.  **Organización Orientada a Proyectos (Proyectizada):** Todo el equipo trabaja a tiempo completo en el proyecto y responden *exclusivamente* al Jefe de Proyecto. Éste tiene **autoridad total** sobre el presupuesto y los recursos.
3.  **Organización Matricial (La más común):** Mezcla las dos anteriores. El técnico tiene un jefe "funcional" pero está asignado a un proyecto donde responde también a un Jefe de Proyecto. 

Dentro de la organización matricial distinguimos tres niveles clave en función de quién tiene el poder:
*   **Matricial Débil:** El Jefe de Proyecto actúa más como un *coordinador* o *expedidor*. El poder real lo tiene el gerente funcional.
*   **Matricial Equilibrada:** El Jefe de Proyecto y el jefe funcional comparten el poder y las decisiones presupuestarias de forma similar.
*   **Matricial Fuerte:** El Jefe de Proyecto tiene mayor autoridad que el gerente funcional y controla el presupuesto del proyecto.

**Tabla Resumen de Autoridad (Resumen de autoridad):**

| Estructura | Autoridad del Jefe de Proyecto | Control del Presupuesto | Rol del Jefe de Proyecto |
| :--- | :--- | :--- | :--- |
| **Funcional** | Poca o Ninguna | Gerente Funcional | Media jornada |
| **Matricial Débil** | Limitada | Gerente Funcional | Media jornada (Coordinador) |
| **Matricial Equilibrada** | De baja a moderada | Mixto | Jornada completa |
| **Matricial Fuerte** | De moderada a alta | Jefe de Proyecto | Jornada completa |
| **Proyectizada** | Alta a Casi Total | Jefe de Proyecto | Jornada completa |

*Nota:* Un matiz adicional examinable es el de la **organización compuesta o híbrida**: en la práctica, muchas organizaciones combinan varias estructuras simultáneamente (ej. mantienen departamentos funcionales estables pero crean una PMO directiva para determinados proyectos estratégicos).

---

### 1.1. Estructuras organizativas y autoridad

La estructura organizativa condiciona la disponibilidad de recursos, la autoridad del director del proyecto, los mecanismos de comunicación y la asignación de responsabilidades.

En una estructura funcional, la autoridad sobre los recursos se concentra en los responsables funcionales. En las estructuras matriciales, la autoridad se comparte en distinto grado entre responsables funcionales y de proyecto. En una estructura proyectizada, el director del proyecto dispone de una autoridad considerablemente mayor sobre el equipo y los recursos asignados.

La estructura organizativa debe distinguirse de la estructura de gobernanza específica del proyecto. Una organización puede mantener departamentos funcionales y, simultáneamente, establecer una estructura de gobierno para un proyecto concreto.

### 1.2. Organización del equipo y comunicación

La organización del proyecto debe definir canales de comunicación, responsabilidades, mecanismos de coordinación y procedimientos para resolver conflictos o escalar decisiones.

En proyectos TIC con equipos multidisciplinares pueden coexistir perfiles de negocio, análisis, arquitectura, desarrollo, pruebas, seguridad, operaciones y proveedores externos. La claridad en las responsabilidades reduce duplicidades y facilita la gestión de dependencias.

### 1.3. PMO y estructuras organizativas

Una PMO puede actuar como estructura de apoyo, control o dirección en función de su mandato. Su relación con los proyectos debe estar definida para evitar conflictos de autoridad y establecer claramente qué decisiones permanecen en el director del proyecto, cuáles corresponden a la dirección y cuáles se delegan en otros niveles.

## 2. Roles y Responsabilidades Clave

Los tribunales adoran preguntar por "quién hace qué". Es vital distinguir entre los roles de Métrica v3 y los roles de PRINCE2.

### 2.1. Roles en Métrica v3

*   **Comité de Dirección:** Son los "jefazos" o promotores. Promueven los recursos iniciales y son los únicos que **aprueban los procesos formalmente** (ej. dan luz verde a iniciar el proyecto en la fase PSI y aprueban el paso a producción).
*   **Comité de Seguimiento:** Su misión es el seguimiento "político" y la resolución de bloqueos importantes. Si hay un **cambio grave en los requisitos**, el Jefe de Proyecto lo propone, pero quien lo **aprueba** es el Comité de Seguimiento.
*   **Jefe de Proyecto:** El gestor real. Estima el esfuerzo, elabora la planificación (Gantt, PERT), asigna tareas, registra y analiza el impacto de las **incidencias**, y hace informes de seguimiento. En Métrica v3 es quien "archiva la documentación de gestión" cuando termina el proyecto.
*   **Directores de los Usuarios:** Representan a los usuarios finales y son clave en la validación de requisitos y en la aprobación de las pruebas de aceptación.

### 2.2. Roles bajo PRINCE2

PRINCE2 estructura la gobernanza del proyecto en torno al **Project Board (Comité de Proyecto)**, que representa a nivel gerencial los tres intereses principales. Está formado por tres roles obligatorios:

*   **Executive (Ejecutivo):** El máximo responsable individual del proyecto; es propietario del *Business Case*, asegura la relación calidad-precio de la inversión y tiene la última palabra en la toma de decisiones del Project Board.
*   **Senior User (Usuario Principal):** Representa a quienes usarán los productos del proyecto; especifica las necesidades de los usuarios, los beneficios esperados y responde de que la solución final satisfaga esas necesidades.
*   **Senior Supplier (Proveedor Principal):** Representa a quienes diseñan, desarrollan, facilitan o implementan los productos; responde de la **integridad técnica** del proyecto y de la calidad de los entregables.

*Otros roles en PRINCE2:*
*   **Project Manager:** Gestiona el día a día. Es el equivalente funcional al Jefe de Proyecto de Métrica v3.
*   **Team Manager:** Dirige la producción técnica de los entregables asignados a su equipo.
*   **Project Assurance (Garantía del Proyecto):** Garantiza de forma independiente que el proyecto se gestiona correctamente (suele ser delegado por el Project Board).
*   **Project Support:** Apoyo administrativo, gestión documental y de herramientas.

*(Nota Ágil): En Scrum los roles cambian: el **Scrum Master** actúa como facilitador eliminando impedimentos, el **Product Owner** prioriza el valor de negocio en el Product Backlog, y los **Developers** construyen el incremento.*

---

### 2.1. Responsabilidades y delegación

La dirección de proyectos requiere distribuir la autoridad de forma que cada nivel de gestión pueda tomar decisiones dentro de unos límites previamente definidos.

La delegación no elimina la responsabilidad del nivel superior sobre el resultado global. Cada nivel debe disponer de información suficiente para controlar el proyecto y elevar únicamente las cuestiones que requieran decisión superior.

### 2.2. Gobernanza y escalado

La gobernanza establece quién tiene autoridad para iniciar, modificar, supervisar y cerrar un proyecto o una fase.

Los mecanismos de escalado deben permitir que los asuntos que superen la autoridad delegada lleguen al nivel competente con información suficiente sobre su impacto, alternativas y recomendación de actuación.

## 3. Gestión por Excepción

"Gestión por excepción" es uno de los **7 principios fundamentales de PRINCE2**.

**Significado de la gestión por excepción:**
*   **La Regla general:** Cada nivel de gestión delega autoridad al nivel inferior estableciendo unos límites o **tolerancias**. Mientras el proyecto se mantenga dentro de esas tolerancias, el trabajo sigue sin necesidad de reuniones continuas ni microgestión.
*   **La Excepción:** Si surge una incidencia que va a superar esas tolerancias (ej. un retraso previsto mayor al límite), se considera una "excepción". El Project Manager debe detenerse y **escalar el problema** al Project Board mediante un documento formal.
*   **Documentos clave:** El aviso se hace mediante un **Informe de Excepción** (*Exception Report*), y la solución propuesta se presenta como un **Plan de Excepción** (*Exception Plan*), que, si se aprueba, sustituye al plan original.

**Las 6 Tolerancias de PRINCE2 (Concepto muy examinable):**
Para que la gestión por excepción funcione, PRINCE2 define tolerancias en 6 áreas de desempeño, no solo en tiempo y coste:
1.  **Tiempo:** Límite de retraso o adelanto permitido.
2.  **Coste:** Desviación presupuestaria permitida.
3.  **Calidad:** Límites aceptables para que un producto cumpla su propósito (ej. tolerar pequeños defectos estéticos pero no funcionales).
4.  **Alcance:** Variación permitida en los requisitos o productos a entregar (ej. funcionalidades MoSCoW: Must, Should, Could, Won't).
5.  **Beneficio:** Desviación permitida frente a los beneficios económicos/estratégicos proyectados en el Business Case.
6.  **Riesgo:** Límites en el nivel de exposición al riesgo que la organización está dispuesta a asumir.

---

### 3.1. Tolerancias y gestión por excepción

En PRINCE2, la **gestión por excepción** delega autoridad mediante la definición de tolerancias. Mientras las previsiones del proyecto permanezcan dentro de dichas tolerancias, el nivel de gestión responsable puede continuar el trabajo sin elevar cada desviación al nivel superior.

Las tolerancias se establecen respecto del **tiempo, coste, alcance, calidad, beneficio y riesgo**.

Cuando se prevé que una tolerancia sea rebasada, se produce una excepción y la decisión se escala al nivel correspondiente. La finalidad es evitar la microgestión y concentrar la intervención de la dirección en las situaciones que requieren una decisión fuera de la autoridad delegada.

### 3.2. Gestión de una excepción

Ante una posible superación de tolerancias, el responsable debe informar de la situación y de sus consecuencias. En PRINCE2, el **Exception Report** informa al nivel de dirección correspondiente de la previsión de superar la tolerancia.

Cuando resulte necesario modificar la forma de gestionar el proyecto, puede elaborarse un **Exception Plan** para sustituir o revisar el plan que ha dejado de ser válido. El plan de excepción debe seguir el procedimiento de autorización establecido por el nivel de gobierno competente.

### 3.3. Gestión por excepción y niveles de gestión

La gestión por excepción se aplica a los diferentes niveles del sistema de gestión de PRINCE2. Cada nivel recibe una delegación de autoridad, establece tolerancias y escala únicamente las desviaciones que exceden esos límites.

Este mecanismo permite combinar control y autonomía: los responsables de los niveles inferiores disponen de margen para gestionar el trabajo dentro de sus límites y la dirección conserva el control sobre las decisiones relevantes.

## 4. Gestión de Dominios o Ámbitos y de Procesos en los Proyectos

Este bloque responde a cómo los estándares actuales organizan el trabajo de dirección de proyectos. Es fundamental no mezclar las versiones del PMBOK.

**Bajo PMBOK (6ª edición) — Áreas de Conocimiento y Grupos de Procesos:**
El enfoque clásico agrupaba la gestión en **10 Áreas de Conocimiento** (Integración, Alcance, Cronograma, Costes, Calidad, Recursos, Comunicaciones, Riesgos, Adquisiciones e Interesados). Estas áreas se gestionaban de forma matricial a través de **5 Grupos de Procesos**: Inicio, Planificación, Ejecución, Monitoreo y Control, y Cierre.

**Bajo PMBOK (7ª edición) — Los 8 Dominios de Desempeño:**
El estándar ha evolucionado para ser aplicable a entornos ágiles, predictivos e híbridos, sustituyendo las áreas de conocimiento por **8 Dominios de Desempeño** (*Performance Domains*):
1.  **Interesados** (*Stakeholders*).
2.  **Equipo** (*Team*).
3.  **Enfoque de Desarrollo y Ciclo de Vida** (*Development Approach and Life Cycle*).
4.  **Planificación** (*Planning*).
5.  **Trabajo del Proyecto** (*Project Work*).
6.  **Entrega** (*Delivery*).
7.  **Medición** (*Measurement*).
8.  **Incertidumbre** (*Uncertainty*).

**Bajo PRINCE2 — 7 Temas y 7 Procesos:**
*   **Los 7 Temas (El "Qué"):** Aspectos transversales que deben abordarse continuamente: Business Case, Organización, Calidad, Planes, Riesgo, Cambio y Progreso.
*   **Los 7 Procesos (El "Cuándo"):** La secuencia temporal del proyecto: Puesta en Marcha (SU), Dirección de un Proyecto (DP), Inicio de un Proyecto (IP), Control de una Fase (CS), Gestión de la Entrega de Productos (MP), Gestión de los Límites de Fase (SB) y Cierre de un Proyecto (CP).

---

### 4.1. Dominios de desempeño y procesos de gestión

La dirección de proyectos comprende actividades relacionadas con la gobernanza, el alcance, cronograma, finanzas, interesados, recursos y riesgos. La forma concreta de organizar estas actividades depende del estándar o método utilizado.

En **PMBOK 8**, PMI mantiene los principios y dominios de desempeño como base y presenta siete dominios: Gobernanza, Alcance, Cronograma, Finanzas, Interesados, Recursos y Riesgo. La guía también incorpora orientación sobre procesos de manera no prescriptiva.

En **ISO 21502:2020**, la gestión se plantea mediante prácticas aplicables a diferentes enfoques de entrega, incluidos predictivo, incremental, iterativo, adaptativo e híbrido. La norma se aplica a proyectos públicos y privados y no prescribe una única metodología.

En **PRINCE2 7**, las prácticas y procesos proporcionan el marco de gobierno y gestión del proyecto.

### 4.2. Gestión de procesos durante la ejecución

Durante la ejecución deben gestionarse y controlarse, según corresponda, el trabajo del proyecto, los recursos, las comunicaciones, los riesgos, las cuestiones, la calidad, los cambios y los entregables.

Los procesos de gestión deben aportar información suficiente para comparar el desempeño real con las previsiones, identificar desviaciones y adoptar decisiones. La ejecución no debe considerarse un proceso aislado: interactúa con la planificación, el seguimiento y control y el cierre.

## 5. Enfoque en Productos y Gestión de Proyectos

Es fundamental distinguir qué estamos construyendo (el producto) y cómo lo estamos construyendo (el proyecto).

*   **Enfoque en el Producto:** Se centra en las especificaciones, la funcionalidad y la calidad de lo que se va a entregar. PRINCE2 tiene un principio específico llamado "Enfoque en los Productos".
*   **Enfoque en el Proyecto (Proceso):** Se centra en la maquinaria organizativa: cumplir plazos, medir el esfuerzo gastado, gestionar los riesgos y controlar el presupuesto.

**Planificación Basada en Productos (PRINCE2):**
A diferencia de la planificación tradicional que empieza listando tareas, PRINCE2 exige que primero se identifiquen y definan los productos (entregables) mediante **Descripciones de Producto**. Cada descripción detalla el propósito, formato y *criterios de calidad*. Solo cuando se sabe exactamente *qué* se va a construir (PBS - *Product Breakdown Structure*), se deducen las actividades necesarias para lograrlo. 

---

### 5.1. Enfoque basado en productos

El principio de **enfoque en los productos** de PRINCE2 orienta la gestión hacia los productos que deben entregarse y hacia los criterios que permiten determinar si son aceptables.

La planificación basada en productos comienza identificando los productos que deben generarse, sus relaciones y sus características. A partir de ellos se determina el trabajo necesario para producirlos y comprobar su aceptación.

La **Product Breakdown Structure (PBS)** representa la descomposición jerárquica de los productos. Las **Product Descriptions** definen, entre otros aspectos, el propósito del producto, su composición, criterios de calidad, tolerancias y método de aceptación.

### 5.2. Calidad y aceptación

El enfoque en productos relaciona directamente alcance y calidad. Cada producto debe disponer de criterios de calidad suficientemente precisos para determinar si cumple su propósito.

La aceptación debe basarse en criterios previamente definidos. De este modo se reduce la ambigüedad sobre lo que debe considerarse terminado y se facilita la verificación de los entregables.

### 5.3. Enfoque en productos frente a enfoque en actividades

Un enfoque centrado exclusivamente en actividades puede llevar a ejecutar muchas tareas sin demostrar que se ha obtenido el resultado requerido.

El enfoque basado en productos parte de lo que debe entregarse y utiliza los productos para derivar el trabajo, las actividades, los recursos y las comprobaciones necesarias. No elimina la planificación de actividades, sino que proporciona una base para relacionarlas con resultados concretos.

## 6. Adaptación al Entorno del Proyecto

La **Adaptación** (*Tailoring*) es un principio fundamental tanto en PRINCE2 como en PMBOK 7. Significa que ninguna metodología se aplica como una "camisa de fuerza" ni de forma burocrática ciega.

*   **En PRINCE2:** La metodología DEBE adaptarse a la escala, riesgo, complejidad e importancia del proyecto. Esta adaptación se documenta formalmente en el *Project Initiation Document (PID)*.  **Adaptar no significa eliminar principios**. Los 7 principios de PRINCE2 son universales y obligatorios; lo que se adapta (simplifica o fusiona) son los roles, los documentos de gestión (temas) y la formalidad de los procesos.
*   **En PMBOK 7:** Se denomina "Tailoring". Incluye elegir el ciclo de vida adecuado (predictivo, iterativo, ágil o híbrido), seleccionar los procesos, herramientas y métodos que aporten valor y descartar el papeleo innecesario.
*   **En Métrica v3:** Sus manuales indican explícitamente que las tareas y perfiles deben "adaptarse y dimensionarse" a las características del sistema de información concreto.

---

### 6.1. Adaptación al contexto organizativo

La adaptación o **tailoring** consiste en ajustar el enfoque de gestión a las características del proyecto y al contexto de la organización.

La adaptación puede afectar a la selección del enfoque de desarrollo, nivel de detalle, mecanismos de gobierno, documentación, roles, herramientas, técnicas, controles y frecuencia de seguimiento.

### 6.2. Factores que condicionan la adaptación

Entre los factores que deben considerarse se encuentran:

* tamaño y duración del proyecto;
* complejidad técnica y organizativa;
* criticidad del sistema o servicio;
* nivel de riesgo;
* requisitos legales y reglamentarios;
* número y diversidad de interesados;
* distribución geográfica de los equipos;
* modelo de contratación y relación con proveedores;
* restricciones presupuestarias y de recursos;
* cultura y capacidad de la organización;
* enfoque de desarrollo adoptado.

La adaptación no debe utilizarse para eliminar controles exigidos por la normativa o por el modelo de gobierno aplicable.

### 6.3. Tailoring en PMBOK y PRINCE2

PMI establece explícitamente la necesidad de adaptar el enfoque, prácticas, herramientas y técnicas al contexto.

PRINCE2 7 refuerza la flexibilidad y la personalización del método. La adaptación permite ajustar el método al proyecto manteniendo sus elementos fundamentales y evitando una aplicación burocrática que no aporte valor. citeturn155725search3turn155725search8

### 6.4. Adaptación y cumplimiento

La adaptación metodológica no equivale a eliminar obligaciones legales, contractuales, de seguridad, protección de datos, calidad o auditoría.

Cuando existan requisitos externos de obligado cumplimiento, estos constituyen restricciones del proyecto y deben integrarse en el diseño de la gobernanza, procesos y productos.

## 8. Referencias normativas y técnicas

* **Project Management Institute (PMI), A Guide to the Project Management Body of Knowledge (PMBOK® Guide) — Eighth Edition**, 2025. citeturn155725search3
* **ISO 21502:2020**, *Project, programme and portfolio management — Guidance on project management*. citeturn155725search0
* **PRINCE2 Project Management (Version 7)**, PeopleCert. citeturn155725search8

## 9. Ejemplo Real (Sin analogías)

Estás trabajando en un proyecto para lanzar una nueva App móvil del ayuntamiento para el pago de impuestos.

*   **Organización:** Trabajas en una "Organización Matricial Fuerte". Tu jefe de departamento de desarrollo te evalúa, pero estás asignado a tiempo completo al "Proyecto App" y el Jefe de Proyecto gestiona tu tiempo y el presupuesto. 
*   **Roles PRINCE2:** El concejal de Hacienda actúa como *Senior User* y el jefe de infraestructura del ayuntamiento actúa como *Senior Supplier* en el Project Board.
*   **Enfoque en Productos:** Antes de codificar, se crea una *Descripción de Producto* para el "Módulo de Pago con Tarjeta", detallando que debe cumplir con la normativa PCI-DSS (criterio de calidad).
*   **Gestión por Excepción:** El Project Board te ha dado una tolerancia de +/- 10.000€. Al detectar que la pasarela de pago bancaria requerirá licencias extra por 15.000€, superas tu tolerancia de coste. Redactas un *Exception Report* para que el Board decida si amplía el presupuesto o cancela la funcionalidad.
*   **Adaptación (Tailoring):** Como es un proyecto rápido de 3 meses, el equipo decide unificar la fase de inicio y planificación en un solo documento consolidado, en lugar de generar toda la burocracia de un megaproyecto.

---

## 10. Resumen

| Concepto | Concepto clave |
| :--- | :--- |
| **Matricial Fuerte vs. Débil** | Fuerte = "Control del presupuesto y autoridad del JP"; Débil = "JP como coordinador, manda el jefe funcional". |
| **Comité de Dirección (Métrica v3)** | "Promotor", "Autoridad final", "Aprueba paso a producción". |
| **Comité de Seguimiento (Métrica v3)** | "Resuelve contingencias graves", "Aprueba cambios de requisitos". |
| **Executive (PRINCE2)** | "Máximo responsable", "Propietario del Business Case", "Última palabra". |
| **Senior User (PRINCE2)** | "Especifica necesidades", "Valida los beneficios esperados". |
| **Senior Supplier (PRINCE2)** | "Proporciona recursos técnicos", "Asegura la integridad técnica". |
| **Gestión por Excepción (PRINCE2)** | "Tolerancias (6)", "Límites de autoridad", "Exception Report". |
| **Dominios de Desempeño (PMBOK7)** | "8 dominios", "Sustituyen áreas de conocimiento", "Interesados, Equipo...". |
| **Enfoque en los Productos** | "Product-based planning", "PBS", "Descripción del producto y sus criterios de calidad". |
| **Adaptación / Tailoring** | "Ajustar al tamaño/riesgo", "No se eliminan los principios", "Evitar burocracia ciega". |

### 10.1. Simulacro de Test

**Pregunta 1:**
*Durante el desarrollo de un nuevo sistema en un ministerio siguiendo Métrica v3, surge un cambio legislativo que obliga a modificar una funcionalidad troncal del sistema. Una vez analizado el impacto por el Jefe de Proyecto, ¿qué órgano tiene la responsabilidad de aprobar esta petición de cambio de requisitos?*
a) El Comité de Dirección, ya que es el máximo órgano.
b) El Comité de Seguimiento.
c) El Jefe de Proyecto, como responsable de la ejecución.
d) El Director de Usuarios.

**Razonamiento:**
*   (A) El Comité de Dirección aprueba hitos de fase (procesos globales) como el paso a producción, no los cambios de requisitos técnicos del día a día.
*   (C) El Jefe de Proyecto analiza el impacto pero no tiene autoridad para aprobar desvíos graves del alcance.
*   (B) En Métrica v3, el **Comité de Seguimiento** es explícitamente el órgano encargado de aprobar o rechazar las peticiones de cambio de requisitos.
**Respuesta correcta: B.**

**Pregunta 2:**
*Según la metodología PRINCE2, ¿cuál de los siguientes parámetros NO es una de las 6 áreas de tolerancia utilizadas para aplicar el principio de "Gestión por excepción"?*
a) Riesgo.
b) Beneficio.
c) Calidad.
d) Recursos Humanos.

**Razonamiento:**
*   Las 6 áreas de tolerancia en PRINCE2 son: Tiempo, Coste, Calidad, Alcance, Riesgo y Beneficio. 
*   La gestión de "Recursos Humanos" forma parte de la planificación, pero las tolerancias se fijan sobre restricciones de control directivo.
**Respuesta correcta: D.**

**Pregunta 3:**
*Una organización ha decidido adoptar PRINCE2 para un proyecto interno pequeño y de bajo riesgo. El Project Manager decide eliminar el principio de "Justificación Comercial Continua" porque considera que el Business Case es obvio. Según las normas de adaptación (Tailoring) de PRINCE2, ¿es correcta esta decisión?*
a) Sí, la adaptación permite eliminar principios si el proyecto es pequeño.
b) No, la adaptación ajusta la formalidad de los temas y procesos, pero los principios son de aplicación obligatoria.
c) Sí, siempre y cuando el Project Board firme el documento de excepción.
d) No, PRINCE2 no permite ningún tipo de adaptación o simplificación documental.

**Razonamiento:**
*   La trampa clásica del examen: la adaptación (Tailoring) permite unir documentos, saltar la burocracia de ciertos roles combinándolos o relajar procesos, pero **nunca** permite eliminar uno de los 7 principios, ya que son la esencia de la metodología.
**Respuesta correcta: B.**