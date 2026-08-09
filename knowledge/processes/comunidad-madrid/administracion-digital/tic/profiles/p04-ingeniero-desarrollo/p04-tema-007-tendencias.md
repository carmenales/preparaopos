---
id: "cm-ad-tic-p04-tema-007-tendencias-gestion"
title: "Tendencias en la Gestión de Proyectos"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/tic"
profiles:
  - "p04-ingeniero-desarrollo"
official_profile: "P04 - Ingeniero de Desarrollo"
official_topic: "Tema 7. Tendencias en la Gestión de Proyectos"
source_ids:
  - "A2_Bloque_III.pdf"
  - "A2_Bloque_IV.pdf"
tags:
  - "hibridacion"
  - "stakeholders"
  - "ia"
  - "ciberseguridad"
  - "soft-skills"
  - "sostenibilidad"
  - "pmi-talent-triangle"
created_at: "2026-08-08"
last_reviewed: "2026-08-08"
ai_generated: true
ai_sources:
  - "gemini"
  - "perplexity"
needs_human_review: true
---

# Tema 7. Tendencias en la Gestión de Proyectos

Este tema cubre los enfoques modernos que complementan la gestión tradicional. Como ingeniero, debes ver esto como la capa de optimización y gobernanza sobre el proceso técnico, alineando la entrega de valor con los marcos regulatorios y tecnológicos actuales.

## 1. Hibridación de Metodologías (Predictivo + Agile)

La tendencia actual no es elegir entre "predictivo" (cascada) y "agile", sino **hibridar**.
*   **Predictivo:** Se mantiene para el control de alto nivel (gestión de presupuestos, cumplimiento normativo, plazos fijos, gestión de riesgos de nivel ejecutivo).
*   **Agile:** Se utiliza en la ejecución (sprints, desarrollo continuo, integración de valor).
*   **Patrón:** El PMBOK 7ª y 8ª edición y el enfoque corporativo proponen marcos donde los **hitos de negocio son predictivos** (fecha de lanzamiento comercial) y la **ejecución es ágil**.

Esta hibridación se sustenta formalmente en el dominio de desempeño "Enfoque de Desarrollo y Ciclo de Vida" del PMBOK 7/8, que reconoce explícitamente un espectro continuo entre predictivo puro y adaptativo puro, con múltiples combinaciones híbridas intermedias. Un patrón habitual de hibridación en la Administración Pública es el llamado **"agile-fall" o cascada con sprints internos**: el proyecto mantiene fases contractuales y de gobierno predictivas (viabilidad, contratación, aceptación formal, cumplimiento normativo) exigidas por la normativa de contratación pública, mientras que dentro de la fase de desarrollo el equipo trabaja con Scrum o Kanban. La decisión de cuánto hibridar depende de factores de adaptación (Tailoring) como el nivel de incertidumbre de los requisitos, la criticidad regulatoria, el tamaño del equipo y la cultura de la organización.

**Marcos Oficiales Híbridos (Muy examinables):**
*   **PRINCE2 Agile:** Extensión oficial de AXELOS que combina la gobernanza, justificación comercial y control de PRINCE2 con marcos de entrega ágil (Scrum, Kanban). Define qué, por qué y cuándo (PRINCE2), dejando el "cómo" a la agilidad.
*   **Disciplined Agile (DA):** Adquirido por el PMI, es un kit de herramientas que ayuda a las organizaciones a elegir su "forma de trabajar" (*Way of Working - WoW*) en función del contexto del equipo, ofreciendo una guía para hibridar con éxito.
*   **Bimodal IT (Gartner):** Tendencia organizativa que divide la gestión en dos modos: Modo 1 (Predictivo, enfocado en la estabilidad, seguridad y sistemas core o *legacy*) y Modo 2 (Ágil, enfocado en la innovación, exploración y *time-to-market* rápido).

## 2. Automatización y Herramientas Digitales

La gestión de proyectos ha dejado de depender de hojas de cálculo manuales para integrarse en ecosistemas digitales interconectados conocidos como **PMIS** (*Project Management Information Systems*).

*   **PMIS (Sistemas de Información para la Dirección de Proyectos):** Herramientas como Jira, Microsoft Project Server, Asana o Trello, que centralizan el cronograma, la asignación de recursos y el seguimiento de incidencias, proporcionando la "fuente única de la verdad" (*Single Source of Truth*).
*   **Automatización RPA en la Gobernanza:** La *Robotic Process Automation* (RPA) no solo se aplica a los procesos de negocio (como vimos en el Plan de Digitalización de la AGE), sino a la propia gestión del proyecto. Ejemplos: generación y envío automático de informes de estado EVM los viernes a las 15:00, actualización automática del registro de riesgos al detectar un ticket crítico, o el cálculo automatizado de la línea base.
*   **Kanban Digital y Flujos de Trabajo:** La automatización de las transiciones de estado (ej. al pasar una tarea a "Hecho" en Jira, se lanza automáticamente un pipeline de integración continua CI/CD o se notifica al usuario clave para su validación).

## 3. Gestión de Interesados en el Proyecto (Stakeholders)

Es la identificación y gestión de las expectativas de todas las personas/organizaciones afectadas por el proyecto.
*   **Matriz de Poder/Interés (Mendelow):**
    *   **Alto Poder/Alto Interés:** Gestionar estrechamente (aliados clave).
    *   **Alto Poder/Bajo Interés:** Mantener satisfechos (evitar que se vuelvan detractores).
    *   **Bajo Poder/Alto Interés:** Mantener informados (pueden ser buenos evangelizadores).
    *   **Bajo Poder/Bajo Interés:** Monitorizar (sin dedicar excesivos recursos).

Según el PMBOK, la gestión de interesados se articula en **4 procesos secuenciales** que conviene memorizar porque es habitual que el examen pregunte por su orden o por el entregable de cada uno:
1.  **Identificar a los Interesados:** se reconocen todas las personas, grupos u organizaciones que pueden afectar o verse afectados por el proyecto. Entregable clave: el **Registro de Interesados** (nombre, rol, organización, ubicación, requisitos, expectativas, nivel de poder/interés/influencia y clasificación interno/externo, favorable/neutral/opositor).
2.  **Planificar el Involucramiento de los Interesados:** se desarrollan enfoques para involucrar eficazmente a cada interesado según sus necesidades, expectativas e impacto potencial. Entregable clave: el **Plan de Involucramiento/Compromiso de los Interesados** (*Stakeholder Engagement Plan*).
3.  **Gestionar el Involucramiento de los Interesados:** se comunica y trabaja con los interesados para satisfacer sus necesidades y expectativas, abordar incidentes y fomentar su participación adecuada durante todo el ciclo de vida del proyecto.
4.  **Monitorear el Involucramiento de los Interesados:** se hace seguimiento de las relaciones con los interesados y se ajustan las estrategias y planes para involucrarlos, adaptándose a cambios en su nivel de poder, interés o posición frente al proyecto.

Además de la matriz de Mendelow, existen otros modelos de clasificación de interesados que pueden aparecer como distractor o alternativa en examen:
*   **Modelo de Prominencia (Salience Model):** Clasifica a los interesados basándose en tres variables: **Poder** (capacidad para imponer su voluntad), **Legitimidad** (si su involucramiento es apropiado) y **Urgencia** (necesidad de atención inmediata). La intersección de las tres crea el *Interesado Definitivo* (Definitive Stakeholder), que requiere máxima atención.
*   **Dirección de influencia:** Ascendente (alta dirección); Descendente (el equipo); Horizontal (pares del jefe de proyecto); Externa (proveedores, reguladores, sociedad).

## 4. Ciberseguridad y Cumplimiento Normativo en Proyectos

*   **Security by Design:** La seguridad debe ser un requisito desde la fase de análisis inicial.
*   **DevSecOps:** Evolución del tradicional DevOps. Es la tendencia que integra las prácticas y herramientas de seguridad en el ciclo de vida del desarrollo ágil desde el primer sprint, rompiendo el silo de auditar la seguridad solo al final del proyecto.

En proyectos TIC de la Administración Pública española, el cumplimiento normativo no es un anexo opcional sino un conjunto de restricciones que condicionan el alcance y la planificación desde el Acta de Constitución:
*   **Esquema Nacional de Seguridad (ENS - RD 311/2022):** Obliga a categorizar el sistema (Básico, Medio, Alto) en la fase de iniciación y a aplicar las medidas de seguridad correspondientes desde el diseño. El proyecto debe generar entregables específicos como la **Declaración de Aplicabilidad**.
*   **RGPD y LOPDGDD:** Exigen Privacidad desde el Diseño y por Defecto (art. 25 RGPD) y, en tratamientos de alto riesgo o uso de nuevas tecnologías, la ejecución de una **Evaluación de Impacto en la Protección de Datos (EIPD / DPIA)** como hito bloqueante del proyecto.
*   **Esquema Nacional de Interoperabilidad (ENI):** Condiciona el diseño de sistemas que deban intercambiar información entre Administraciones, forzando el uso de estándares abiertos.
La gestión de proyectos moderna integra estos requisitos como parte del **Plan de Gestión de Riesgos y de Calidad**, no como una fase separada de auditoría final.

## 5. Gestión de Proyectos en el ámbito de la IA y Gestión Basada en Datos (Data-Driven)

*   Uso de **IA para predecir** desviaciones de plazos (EVM predictivo).
*   Automatización de informes y dashboards en tiempo real (evitando el reporting manual).
*   Gestión de la calidad del dato: El éxito de la IA en proyectos depende de la fiabilidad de los datos alimentados (GIGO - *Garbage In, Garbage Out*).

Ampliando los casos de uso concretos de IA en dirección de proyectos, que cada vez aparecen más en manuales actualizados (PMBOK 8ª edición incorpora contenido explícito sobre IA):
*   **IA Generativa en Documentación:** Uso de modelos de lenguaje (LLM) integrados en el PMIS para redactar borradores del Acta de Constitución, historias de usuario, actas de reunión o generar el Registro de Riesgos preliminar a partir de las notas del equipo.
*   **Análisis Predictivo (Machine Learning):** Modelos que, entrenados con datos históricos de proyectos similares, estiman la probabilidad de retraso o sobrecoste antes de que ocurra, complementando al EVM tradicional (que es descriptivo, no predictivo).
*   **Optimización de Recursos:** Algoritmos que sugieren la mejor distribución del equipo entre tareas según carga de trabajo, competencias y disponibilidad.
*   **Chatbots y Asistentes Virtuales:** Para resolver dudas frecuentes de los *stakeholders* o automatizar el triaje de incidencias (Service Desk de Nivel 0).

El concepto **GIGO** se complementa con el de **Gobernanza del Dato** (*Data Governance*): antes de automatizar decisiones con IA, el proyecto debe garantizar la trazabilidad, calidad y origen legítimo de los datos usados. Esto conecta directamente con la nueva normativa europea (**IA Act / Reglamento UE 2024/1689**), que exige a los proyectos de IA clasificados como "de alto riesgo" estrictos sistemas de gestión de calidad, evaluación de sesgos y supervisión humana.

## 6. Sostenibilidad y Responsabilidad Social en los Proyectos

*   **Sostenibilidad (ESG):** Los proyectos (tanto públicos como privados) deben evaluar su huella de carbono y su impacto social (criterios ESG: *Environmental, Social, and Governance*). Ya no es una opción, es una métrica clave del proyecto y un factor de evaluación en los pliegos de contratación pública.
*   **Green Project Management (GPM):** Metodologías como **PRiSM** (*Projects integrating Sustainable Methods*) que extienden el enfoque del proyecto para medir el ciclo de vida completo del producto creado, garantizando la reducción del impacto ambiental.
*   **Green IT:** Aplicado a las TIC públicas, incluye el diseño de arquitecturas eficientes energéticamente, la consolidación en la nube para reducir la huella de carbono del CPD, y la economía circular en la adquisición de hardware.

La propia norma **ISO 21502:2020** reconoce que los objetivos de sostenibilidad deben considerarse durante todo el ciclo de vida del proyecto, alineándose con marcos como los **Objetivos de Desarrollo Sostenible (ODS - Agenda 2030)** de Naciones Unidas. En la práctica, esto se traduce en indicadores de proyecto tan concretos como el PUE (*Power Usage Effectiveness*) de la infraestructura desplegada, la accesibilidad digital obligatoria de las soluciones (Real Decreto 1112/2018 para garantizar la inclusión social) y el impacto social del proyecto sobre la brecha digital.

## 7. Habilidades Blandas (Soft Skills) en la Gestión de Proyectos

Indispensables para el perfil TIC (especialmente A2/A1) para conectar la ejecución del código con la estrategia del negocio.
*   **Inteligencia Emocional:** Gestión del estrés en hitos de entrega críticos y empatía con las presiones de los *stakeholders*.
*   **Negociación:** Fundamental para gestionar el alcance (Scope Creep) cuando el cliente quiere "añadir una funcionalidad más" a mitad del proyecto sin ampliar el presupuesto.
*   **Gestión de Conflictos:** Capacidad de arbitrar entre el equipo técnico y las demandas del negocio.
*   **Liderazgo Siervo (Servant Leadership):** Enfoque clave en los marcos ágiles (ej. Scrum Master) y adoptado por PMBOK 7. El líder no manda desde arriba, sino que se pone "al servicio del equipo" para eliminar impedimentos (*blockers*), facilitar recursos, protegerlos de interrupciones y fomentar su auto-organización.

El PMI formaliza estas competencias en el **Talent Triangle (Triángulo del Talento)**, marco de referencia oficial para la formación continua de sus certificados, actualizado recientemente con esta terminología:
1.  **Ways of Working (Formas de Trabajar)**, antes llamado "Gestión de Proyectos Técnica": competencias metodológicas como saber aplicar marcos predictivos, ágiles, híbridos, técnicas EVM, y gestión del alcance.
2.  **Power Skills (Habilidades de Poder)**, antes llamado "Liderazgo": las habilidades blandas propiamente dichas — liderazgo colaborativo (siervo/transformacional), escucha activa, comunicación, adaptabilidad, gestión de conflictos e inteligencia emocional.
3.  **Business Acumen (Visión de Negocio)**, antes llamado "Gestión Estratégica y de Negocio": comprensión del sector, gestión de beneficios, cumplimiento normativo (ENS, RGPD) y alineación con los objetivos estratégicos.

Este marco es relevante para el examen porque consolida la visión de que el éxito de un proyecto no depende solo del dominio técnico ("Ways of Working"), sino de una combinación equilibrada de las tres dimensiones.

---

## 8. Resumen

| Concepto | Palabra Chivata |
| :--- | :--- |
| **Hibridación** | "Adaptación", "Tailoring", "Agile-fall", "PRINCE2 Agile", "Bimodal IT". |
| **Stakeholders (Mendelow)** | "Matriz Poder/Interés", "Mantener satisfecho (Alto Poder/Bajo Interés)". |
| **Modelo de Prominencia** | "Poder, Legitimidad y Urgencia", "Interesado Definitivo". |
| **Procesos Interesados (PMBOK)**| "Identificar → Planificar → Gestionar → Monitorear". |
| **Ciberseguridad y Cumplimiento**| "Security by Design", "DevSecOps", "ENS (Categorización/DA)", "EIPD". |
| **IA y Data-Driven** | "Predicción", "GIGO", "AI Act", "Automatización de informes". |
| **Sostenibilidad/ESG** | "Ambiental, Social, Gobernanza", "PRiSM", "Green IT", "ODS". |
| **PMI Talent Triangle** | "Ways of Working + Power Skills + Business Acumen". |
| **Liderazgo Siervo** | "Servant Leadership", "Eliminar impedimentos", "Líder como facilitador". |

### 8.1. Simulacro de Test

**Pregunta 1:**
*En un proyecto híbrido, si un Stakeholder tiene alto poder de decisión pero poco interés en los detalles técnicos del desarrollo diario, ¿cuál es la estrategia recomendada según la matriz de Mendelow?*
a) Gestionar estrechamente y convocarle a reuniones diarias.
b) Mantenerle satisfecho con resúmenes ejecutivos.
c) Informarle puntualmente solo cuando haya fallos.
d) Ignorarle, ya que no tiene interés.

**Razonamiento Estructurado:**
1.  **Busca el patrón:** Stakeholder = Alto Poder / Bajo Interés.
2.  **Desmontando:**
    *   (A) Gestionar estrechamente es para quien tiene alto poder Y alto interés.
    *   (D) Ignorar a alguien con alto poder es un error crítico.
    *   (C) Informar solo de fallos es reactivo y peligroso.
    *   (B) **Mantenerle satisfecho** (con reportes ejecutivos que le den seguridad sin aburrirle) es la respuesta de libro de Mendelow.
3.  **Respuesta correcta: B.**

**Pregunta 2:**
*Según el enfoque de gestión de interesados del PMBOK, ¿en qué proceso se elabora por primera vez el documento que clasifica si la postura de un interesado es favorable, neutral u opositora frente al proyecto?*
a) Planificar el Involucramiento de los Interesados.
b) Identificar a los Interesados.
c) Gestionar el Involucramiento de los Interesados.
d) Monitorear el Involucramiento de los Interesados.

**Razonamiento Estructurado:**
1.  Esta clasificación forma parte del "Registro de Interesados", que documenta quiénes son, su rol, poder y actitud inicial frente al proyecto.
2.  El Registro de Interesados es el entregable principal y exclusivo del primer proceso: "Identificar a los Interesados". Los procesos de planificar (A), gestionar (C) y monitorear (D) utilizan y actualizan ese registro, pero no lo crean por primera vez.
3.  **Respuesta correcta: B.**

**Pregunta 3:**
*¿Cómo se denomina la filosofía de liderazgo, fuertemente adoptada por los enfoques ágiles y reconocida dentro de las 'Power Skills' del PMI, en la que el Director de Proyecto enfoca su esfuerzo en eliminar obstáculos, proveer recursos y proteger al equipo de interrupciones externas en lugar de impartir órdenes directivas?*
a) Liderazgo Transaccional.
b) Microgestión (Micromanagement).
c) Liderazgo Laissez-Faire.
d) Liderazgo Siervo (Servant Leadership).

**Razonamiento Estructurado:**
1.  **Busca el patrón:** "Eliminar obstáculos", "proteger al equipo", "en lugar de impartir órdenes".
2.  **Desmontando:**
    *   (A) Transaccional se basa en recompensas y castigos.
    *   (B) Microgestión es el extremo opuesto a la auto-organización ágil.
    *   (C) Laissez-Faire es una ausencia de liderazgo o intervención nula, lo cual no encaja con la actitud proactiva de "eliminar obstáculos".
    *   (D) El Liderazgo Siervo (*Servant Leadership*) es exactamente la definición descrita, característica principal del rol del Scrum Master y muy valorado en el nuevo PMBOK.
3.  **Respuesta correcta: D.**

**Pregunta 4:**
*Un proyecto de desarrollo software en la Administración adopta un enfoque en el que la seguridad no se evalúa en una fase final de auditoría, sino que las pruebas de vulnerabilidad, análisis de código estático (SAST) y cumplimiento del ENS se automatizan y ejecutan continuamente dentro de las iteraciones ágiles de desarrollo y despliegue. ¿A qué tendencia tecnológica se refiere esta práctica?*
a) Agile-fall.
b) DevSecOps.
c) Bimodal IT.
d) Data-Driven Management.

**Razonamiento Estructurado:**
1.  **Busca el patrón:** "Seguridad no se evalúa al final", "pruebas automatizadas dentro de iteraciones continuas".
2.  **Desmontando:**
    *   (A) Agile-fall es hibridar fases cascada con ejecución ágil, pero no especifica la integración de seguridad técnica continua.
    *   (C) Bimodal IT es tener dos velocidades/modos de gestión en la organización (Gartner).
    *   (D) Data-Driven se refiere al uso de IA y métricas, no a pruebas de seguridad.
    *   (B) DevSecOps (Development, Security, Operations) es la metodología que integra de forma automatizada y temprana ("Shift Left") las prácticas de seguridad dentro del pipeline de integración/entrega continua.
3.  **Respuesta correcta: B.**