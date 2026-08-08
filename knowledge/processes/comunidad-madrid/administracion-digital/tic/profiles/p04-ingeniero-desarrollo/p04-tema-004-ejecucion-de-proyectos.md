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
  - "gemini"
  - "perplexity"
needs_human_review: true
---

# Tema 4. Ejecución de proyectos

## 1. Formas de Organización de los Proyectos

Como ingeniero de desarrollo, saber cómo está estructurado el poder en tu proyecto te ahorra muchos quebraderos de cabeza. En el test, suelen preguntar por el tipo de estructura organizativa. Hay tres patrones clásicos:

**Patrón Lógico - Tipos de Organización:**
1.  **Organización Funcional (Clásica):** Agrupación por especialidad (ej. todos los programadores en el "Departamento de Desarrollo", los de redes en "Sistemas"). El Jefe de Proyecto **apenas tiene autoridad**; manda el jefe del departamento funcional.
2.  **Organización Orientada a Proyectos:** Todo el equipo trabaja a tiempo completo en el proyecto y responden *exclusivamente* al Jefe de Proyecto. Éste tiene **autoridad total**.
3.  **Organización Matricial (La más común):** Mezcla las dos anteriores. El técnico de bases de datos tiene un jefe "funcional" (el de bases de datos) pero está asignado a un proyecto donde responde también a un Jefe de Proyecto (estructura "matricial"). Puede ser *débil* (el Jefe de Proyecto manda poco) o *fuerte* (el Jefe de Proyecto manda más).

Dentro de la organización matricial conviene distinguir un tercer punto intermedio que suele aparecer como distractor: la **matricial equilibrada**, donde el Jefe de Proyecto y el jefe funcional comparten el poder de forma similar, sin que ninguno predomine claramente sobre el otro. Así, el espectro completo de autoridad del Jefe de Proyecto, de menor a mayor, es: Funcional → Matricial débil → Matricial equilibrada → Matricial fuerte → Orientada a proyectos.

Un matiz adicional examinable es el de la **organización compuesta o híbrida**: en la práctica, muchas organizaciones combinan varias estructuras simultáneamente (ej. mantienen departamentos funcionales estables pero crean una PMO directiva para determinados proyectos estratégicos), por lo que el modelo puro rara vez se da al 100%.

---

## 2. Roles y Responsabilidades Clave

Los tribunales adoran preguntar por "quién hace qué". En el documento de Métrica v3 que usamos como referencia, hay perfiles muy bien delimitados.

**Patrón Lógico - Los 3 roles principales de Métrica v3:**
*   **Comité de Dirección:** Son los "jefazos". Ellos promueven los recursos iniciales y son los únicos que **aprueban los procesos formalmente** (ej. dan luz verde a iniciar el proyecto en la fase PSI y aprueban el paso a producción).
*   **Comité de Seguimiento:** Su misión es el seguimiento "político" y la resolución de bloqueos importantes. Si hay un **cambio grave en los requisitos**, el Jefe de Proyecto lo propone, pero quien lo **aprueba** es el Comité de Seguimiento.
*   **Jefe de Proyecto:** El gestor real. Estima el esfuerzo, elabora la planificación (Gantt, PERT), asigna tareas, registra y analiza el impacto de las **incidencias**, y hace informes de seguimiento. En Métrica v3 es quien "archiva la documentación de gestión" cuando termina el proyecto.

*(Nota Ágil - Scrum): Recuerda que en metodologías ágiles estos roles cambian. El Scrum Master actúa como facilitador eliminando impedimentos técnicos del día a día, y el Product Owner es quien prioriza los requisitos de negocio.*

### 2.1  Ampliación de roles bajo PRINCE2

PRINCE2 estructura la gobernanza del proyecto en torno al **Project Board (Comité de Proyecto)**, que representa a nivel gerencial los tres intereses del proyecto: negocio, usuario y proveedor. Está formado por tres roles obligatorios:

*   **Executive (Ejecutivo):** el máximo responsable individual del proyecto; es propietario del Business Case, asegura la relación calidad-precio de la inversión y equilibra las necesidades de negocio, usuarios y proveedores. Tiene la última palabra en la toma de decisiones del Project Board.
*   **Senior User (Usuario Principal):** representa a quienes usarán los productos del proyecto; especifica las necesidades de los usuarios y los beneficios esperados, y responde de que la solución final satisfaga esas necesidades.
*   **Senior Supplier (Proveedor Principal):** representa a quienes diseñan, desarrollan, facilitan, adquieren e implementan los productos del proyecto; responde de la integridad técnica del proyecto y de la calidad de los entregables.

> **PRINCE2**: equivalente al Comité de Dirección/Seguimiento de Métrica v3

*    **Project Manager**:  gestiona el día a día, equivalente funcional al Jefe de Proyecto de Métrica v3.
*    **Team Manager**: dirige la producción de los entregables asignados a su equipo.
*    **Project Assurance**: garantiza de forma independiente que el proyecto se gestiona correctamente, en nombre del Project Board.
*    **Project Support**: apoyo administrativo, gestión documental y de herramientas.

---

## 3. Gestión por Excepción

"Gestión por excepción" está íntimamente ligada a metodologías como **PRINCE2**.

**Patrón Lógico - ¿Qué significa "Por Excepción"?:**
*   **Regla general:** El Jefe de Proyecto tiene delegada cierta autoridad y unas tolerancias (ej. puede pasarse del presupuesto un 5% o retrasarse 2 días sin tener que pedir permiso arriba). Mientras el proyecto se mantenga dentro de esas tolerancias, el trabajo sigue normal.
*   **La Excepción:** Si surge una incidencia que va a superar esas tolerancias (ej. un retraso previsto de 10 días), se considera una "excepción". El Jefe de Proyecto debe detenerse, escalar el problema al Comité y proponer una solución.
*   **En el test:** Si el enunciado habla de "fijar tolerancias" y "solo informar o pedir permiso a la dirección cuando se van a superar esos límites", la respuesta correcta siempre se asocia a la **Gestión por excepción** y a metodologías estructuradas (PRINCE2).

La Gestión por Excepción es, de hecho, uno de los **7 principios oficiales de PRINCE2** (los otros seis son: Justificación Comercial Continua, Aprender de la Experiencia, Roles y Responsabilidades definidos, Gestión por Fases, Enfoque en los Productos y Adaptación al entorno del proyecto — precisamente los conceptos que estructuran este mismo tema). Las **tolerancias** en PRINCE2 se fijan sobre seis parámetros distintos, no solo tiempo y coste: alcance, plazo, coste, calidad, riesgo y beneficios. Cuando se prevé que una tolerancia se va a exceder, el rol responsable de generar el aviso formal se llama **Informe de Excepción** (*Exception Report*), y da lugar a un **Plan de Excepción** (*Exception Plan*) que sustituye al plan de la fase o del proyecto en curso, sometido de nuevo a aprobación del Project Board.

Esta forma de gestión encaja con el concepto genérico de **dirección por objetivos y delegación**: cada nivel de gestión delega autoridad en el nivel inferior fijando tolerancias, y solo interviene activamente cuando el nivel inferior "escala" un problema que él mismo no puede resolver con la autoridad delegada. Es la lógica opuesta a la microgestión o supervisión constante.

---

## 4. Gestión de Dominios o Ámbitos y de Procesos en los Proyectos

Este es un bloque nuevo respecto a los conceptos clásicos de "producto vs. proceso", y responde a cómo los estándares actuales organizan el trabajo de dirección de proyectos en bloques temáticos manejables.

**Bajo PMBOK (6ª edición) — Áreas de Conocimiento:** el enfoque clásico agrupaba la gestión de proyectos en 10 áreas o "dominios" temáticos: Integración, Alcance, Cronograma, Costes, Calidad, Recursos, Comunicaciones, Riesgos, Adquisiciones e Interesados. Cada área se gestiona a través de procesos agrupados en los 5 Grupos de Procesos (Inicio, Planificación, Ejecución, Monitoreo y Control, Cierre), de forma que cada proceso pertenece simultáneamente a un área de conocimiento y a un grupo de procesos (la clásica "matriz de procesos" del PMBOK 6).

**Bajo PMBOK (7ª edición) — Dominios de Desempeño:** sustituye las áreas de conocimiento por **8 Dominios de Desempeño** (*Performance Domains*), entendidos como grupos de actividades interrelacionadas y esenciales para la entrega efectiva de los resultados del proyecto:

1.  **Interesados** (*Stakeholders*).
2.  **Equipo** (*Team*).
3.  **Enfoque de Desarrollo y Ciclo de Vida** (*Development Approach and Life Cycle*).
4.  **Planificación** (*Planning*).
5.  **Trabajo del Proyecto** (*Project Work*).
6.  **Entrega** (*Delivery*).
7.  **Medición** (*Measurement*).
8.  **Incertidumbre** (*Uncertainty*).

**Bajo PRINCE2 — Los 7 Temas:** son el equivalente funcional de las áreas de conocimiento del PMBOK, aspectos de la dirección de proyectos que deben abordarse de manera continua: **Business Case, Organización, Calidad, Planes, Riesgo, Cambio y Progreso**. A diferencia de PMBOK, PRINCE2 vincula cada tema directamente con uno de sus 7 principios (ej. el tema "Organización" desarrolla el principio "Roles y Responsabilidades definidos").

**Bajo PRINCE2 — Los 7 Procesos:** son la secuencia temporal de actividades de gestión que se ejecutan a lo largo del proyecto: Puesta en Marcha (SU), Dirección de un Proyecto (DP), Inicio de un Proyecto (IP), Control de una Fase (CS), Gestión de la Entrega de Productos (MP), Gestión de los Límites de Fase (SB) y Cierre de un Proyecto (CP). La relación entre temas y procesos es análoga a la relación PMBOK entre áreas de conocimiento y grupos de procesos: los temas son el "qué" transversal, los procesos son el "cuándo" secuencial.

Para el examen, la trampa habitual consiste en confundir "área de conocimiento/dominio" (algo transversal que aplica durante todo el proyecto) con "fase o proceso" (algo que ocurre en un momento temporal concreto). Si el enunciado habla de gestionar riesgos, calidad o comunicaciones "a lo largo de todo el proyecto", es un dominio/tema; si habla de "arrancar el proyecto" o "cerrar una fase", es un proceso o grupo de procesos.

---

## 5. Enfoque en Productos y Gestión de Proyectos

Es fundamental distinguir qué estamos construyendo (el producto) y cómo lo estamos construyendo (el proyecto).

**Patrón Lógico de Enfoques:**

*   **Enfoque en el Producto:** Se centra en la calidad y especificaciones de lo que vas a entregar. Por ejemplo, en Métrica v3, el aseguramiento de la calidad verifica los *productos intermedios* que van saliendo para ver si cumplen la norma (ej. revisar un esquema de base de datos).
*   **Enfoque en el Proyecto (Proceso):** Se centra en la maquinaria organizativa: cumplir plazos, medir el esfuerzo gastado, gestionar los riesgos y controlar el presupuesto.

El "Enfoque en los Productos" es, además, uno de los 7 principios formales de PRINCE2, y merece detalle porque suele preguntarse de forma literal: PRINCE2 define la planificación como orientada a **resultados (productos)** y no a actividades. Antes de planificar el trabajo a realizar, se define con precisión qué productos se van a entregar, con qué características de calidad (mediante las llamadas **Descripciones de Producto**, que detallan propósito, composición, derivación, formato, criterios de calidad y método de comprobación de cada entregable). Solo después se identifican las actividades necesarias para producir esos entregables. Esta secuencia ("primero defino el qué, después planifico el cómo") es la esencia del enfoque en productos y contrasta con la planificación tradicional centrada primero en listar tareas.

**Adaptación al entorno (Sastrería / Tailoring):**
Ni Métrica v3 ni PMBOK son camisas de fuerza. La adaptación significa que, dependiendo de la magnitud del proyecto, el Jefe de Proyecto seleccionará el ciclo de vida y decidirá qué actividades o tareas son obligatorias y cuáles se pueden omitir o simplificar. Métrica v3 dice explícitamente que sus perfiles deben "adaptarse y dimensionarse" según las características particulares de cada proyecto.

---

## 6. Adaptación al Entorno del Proyecto

La **Adaptación** (*Tailoring*) es también uno de los 7 principios formales de PRINCE2, y en PMBOK 7 aparece como uno de los 12 principios rectores bajo el nombre "Adaptar (Tailoring) según el contexto". La idea común a ambos marcos es que ningún estándar se aplica "de fábrica" sin ajuste: se debe adaptar en función de factores como el tamaño del proyecto, la complejidad, el nivel de riesgo, las restricciones de tiempo/coste y la madurez de la organización.

En PRINCE2, la adaptación se materializa formalmente al inicio del proyecto documentando, en el Plan de Inicio del Proyecto, qué elementos de la metodología se aplicarán tal cual, cuáles se simplificarán y cuáles no aplican, siempre justificando la decisión (nunca se "salta" un principio, pero sí se puede ajustar el nivel de formalidad de temas y procesos). En PMBOK 7, el dominio de desempeño "Enfoque de Desarrollo y Ciclo de Vida" es precisamente el que orienta esta decisión, ayudando a elegir entre un enfoque predictivo, adaptativo (ágil) o híbrido según las características del proyecto y del producto a entregar.

Un matiz muy examinable: adaptar **no** significa eliminar principios (los 7 principios de PRINCE2 son "universales, de aplicación obligatoria, y auto-validantes": si un proyecto no los cumple, no puede considerarse gestionado bajo PRINCE2). Lo que se adapta es el **grado de formalidad y detalle** con el que se aplican los temas y procesos, nunca los principios en sí.

---

## 7. Ejemplo Real (Sin analogías)

Estás trabajando en un proyecto para lanzar una nueva App móvil del ayuntamiento para el pago de impuestos.

*   **Organización:** Trabajas en una "Organización Matricial". Tu jefe de departamento de desarrollo te evalúa anualmente, pero estás asignado al "Proyecto App Ayuntamiento" y recibes tareas del Jefe de Proyecto. Si además existe un Comité con Ejecutivo, Usuario Principal (el concejal de Hacienda) y Proveedor Principal (el jefe del departamento TIC), estás ante la estructura de un Project Board tipo PRINCE2.
*   **El Producto vs. El Proyecto:** El código en Java que haces, la interfaz gráfica y los manuales de usuario son el **Producto**. El cronograma de entregas, la gestión de la sala de reuniones para las presentaciones y la solicitud de licencias de software para tu equipo, son parte del **Proyecto**. Antes de empezar a codificar, el equipo redacta una Descripción de Producto para la "Pasarela de pago", especificando sus criterios de calidad (ej. cumplimiento PCI-DSS, tiempo de respuesta máximo).
*   **Gestión por Excepción:** El Jefe de Proyecto tiene margen para absorber retrasos menores a una semana. Un día te das cuenta de que integrar la pasarela de pagos del banco va a retrasar todo 3 semanas. El Jefe de Proyecto "levanta la mano" por **excepción** y escala el problema al Comité de Seguimiento mediante un Informe de Excepción, para ver si se retrasa la salida a producción o si se contrata temporalmente a un especialista.
*   **Adaptación:** Al ser un proyecto de tamaño medio, el ayuntamiento decide no exigir todos los formularios e informes que PRINCE2 recomendaría para un proyecto de gran envergadura, simplificando el tema "Planes" a un único cronograma consolidado en lugar de planes de fase separados.

---

## 8. Resumen

| Concepto | Palabra Chivata en el Test |
| :--- | :--- |
| **Organización Matricial** | "Dos jefes", "Gerente funcional + Gerente de proyecto", "Combinación". |
| **Matricial fuerte vs. débil** | Fuerte = "mayor autoridad del JP"; débil = "predomina el jefe funcional". |
| **Comité de Dirección (Métrica v3)** | "Autoridad final", "Aprueba proceso de desarrollo", "Paso a producción". |
| **Comité de Seguimiento (Métrica v3)** | "Resuelve contingencias", "Aprueba cambios de requisitos propuestos por el Jefe de Proyecto". |
| **Executive (PRINCE2)** | "Máximo responsable", "Propietario del Business Case", "Última palabra". |
| **Senior User (PRINCE2)** | "Especifica necesidades de usuario", "Beneficios esperados". |
| **Senior Supplier (PRINCE2)** | "Integridad técnica", "Calidad de los entregables". |
| **Gestión por Excepción (PRINCE2)** | "Tolerancias", "Límites fijados", "Solo reportar si se superan", "Delegación de autoridad", "Informe/Plan de Excepción". |
| **7 Temas PRINCE2** | "Business Case, Organización, Calidad, Planes, Riesgo, Cambio, Progreso". |
| **7 Procesos PRINCE2** | "SU-DP-IP-CS-MP-SB-CP", "Secuencia temporal". |
| **Dominios de Desempeño PMBOK7** | "8 dominios", "Sustituyen áreas de conocimiento", "Interesados, Equipo, Enfoque de desarrollo...". |
| **Enfoque en los Productos** | "Orientado a resultados no a actividades", "Descripción de Producto", "Primero el qué, después el cómo". |
| **Adaptación / Tailoring** | "Ajustar la metodología", "Dimensionar los perfiles según magnitud", "No todas las tareas son obligatorias", "No elimina principios". |

### 8.1. Simulacro de Test

**Pregunta:**
*Durante el desarrollo de un nuevo sistema de información en un ministerio siguiendo la metodología Métrica v3, surge un cambio importante en la legislación que obliga a modificar una funcionalidad troncal del sistema. Una vez analizado el impacto y propuestos los cambios, ¿qué órgano o rol tiene la responsabilidad de aprobar esta petición de cambio de requisitos?*
a) El Comité de Dirección, ya que es el máximo órgano.
b) El Comité de Seguimiento.
c) El Jefe de Proyecto, como responsable técnico.
d) El Analista principal del proyecto.

**Razonamiento Estructurado:**
1.  **Busca la palabra chivata:** El enunciado pregunta expresamente "quién tiene la responsabilidad de aprobar una petición de cambio de requisitos" en Métrica v3.
2.  **Aplica tu patrón lógico de roles:**
    *   (C) El Jefe de Proyecto es el que gestiona el día a día. Si hay un cambio, él propone la solución, calcula el esfuerzo y se lo *presenta* a un comité, pero no tiene potestad para autorizar cambios graves que afectan a presupuesto o alcance. Falsa.
    *   (D) El Analista principal se encarga del trabajo técnico (diseñar el nuevo modelo), no de la gestión presupuestaria o aprobaciones de alcance. Falsa.
    *   (A) El Comité de Dirección se encarga de los grandes hitos y aprobaciones *a nivel de proceso* general (como iniciar el proyecto en PSI o dar el visto bueno final al paso a producción en IAS).
    *   (B) **El Comité de Seguimiento**. Nuestro patrón nos indica que, según Métrica v3, si hay un cambio de requisitos, se somete a la aprobación del Comité de Seguimiento, previo análisis del impacto en la planificación por parte del Jefe de Proyecto.
3.  **Respuesta correcta:** B.


**Pregunta:**
*Dentro del Project Board de PRINCE2, ¿qué rol es responsable de garantizar la integridad técnica del proyecto y la calidad de los productos entregados por el equipo de desarrollo?*
a) El Executive.
b) El Senior User.
c) El Senior Supplier.
d) El Project Manager.

**Razonamiento Estructurado:**
1.  El Executive (A) responde del Business Case y de la relación calidad-precio de la inversión, no de la integridad técnica en sí. El Senior User (B) representa a quienes usarán los productos, no a quienes los construyen. El Project Manager (D) no forma parte del Project Board; gestiona el día a día.
2.  El **Senior Supplier** representa a quienes diseñan, desarrollan y proveen los recursos técnicos, por lo que es responsable directo de la integridad técnica y de la calidad de los entregables.
3.  **Respuesta correcta:** C.

**Pregunta:**
*Un proyecto adapta la aplicación de PRINCE2 a su tamaño reduciendo la formalidad de varios de sus temas. ¿Cuál de las siguientes afirmaciones sobre la adaptación (Tailoring) en PRINCE2 es correcta?*
a) La adaptación permite eliminar cualquiera de los 7 principios si el proyecto es pequeño.
b) La adaptación afecta al grado de formalidad de temas y procesos, pero nunca elimina los principios.
c) Solo los proyectos ágiles pueden adaptar PRINCE2.
d) La adaptación es opcional y no se documenta formalmente.

**Razonamiento Estructurado:**
1.  Los 7 principios de PRINCE2 son universales y de aplicación obligatoria; si no se cumplen, el proyecto no está gestionado bajo PRINCE2. Por eso (A) es falsa. (C) es falsa porque cualquier proyecto, no solo los ágiles, debe adaptar PRINCE2 a su contexto. (D) es falsa porque la adaptación se documenta en el Plan de Inicio del Proyecto.
2.  Lo correcto es que se ajusta el nivel de detalle y formalidad de temas y procesos, manteniendo intactos los principios.
3.  **Respuesta correcta:** B.
