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
  - "conocimiento-experto"
  - "perplexity"
needs_human_review: true
---

# Tema 7. Tendencias en la Gestión de Proyectos

Este tema cubre los enfoques modernos que complementan la gestión tradicional. Como ingeniero, debes ver esto como la capa de optimización y gobernanza sobre el proceso técnico.

## 1. Hibridación de Metodologías

La tendencia actual no es elegir entre "predictivo" (cascada) y "agile", sino **hibridar**.
*   **Predictivo:** Se mantiene para el control de alto nivel (gestión de presupuestos, cumplimiento normativo, plazos fijos, gestión de riesgos de nivel ejecutivo).
*   **Agile:** Se utiliza en la ejecución (sprints, desarrollo continuo, integración de valor).
*   **Patrón:** El PMBOK 7ª y 8ª edición y el enfoque corporativo proponen marcos donde los **hitos de negocio son predictivos** (fecha de lanzamiento comercial) y la **ejecución es ágil**.

Esta hibridación se sustenta formalmente en el dominio de desempeño "Enfoque de Desarrollo y Ciclo de Vida" del PMBOK 7/8, que reconoce explícitamente un espectro continuo entre predictivo puro y adaptativo puro, con múltiples combinaciones híbridas intermedias. Un patrón habitual de hibridación en la Administración Pública es el llamado **"agile-fall" o cascada con sprints internos**: el proyecto mantiene fases contractuales y de gobierno predictivas (viabilidad, contratación, aceptación formal, cumplimiento normativo) exigidas por la normativa de contratación pública, mientras que dentro de la fase de desarrollo el equipo trabaja con Scrum o Kanban. La decisión de cuánto hibridar depende de factores de adaptación (Tailoring) como el nivel de incertidumbre de los requisitos, la criticidad regulatoria, el tamaño del equipo y la cultura de la organización.

## 2. Gestión de Interesados (Stakeholders)

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

Además de la matriz de Mendelow, existen otros modelos de clasificación de interesados que pueden aparecer como distractor o alternativa en examen: el **Modelo de Prominencia (Poder-Legitimidad-Urgencia)**, que valora si el interesado tiene poder para imponer su voluntad, si su relación es legítima, y si su reclamación requiere atención inmediata; y la clasificación simple por **dirección de influencia** (ascendente: alta dirección; descendente: el equipo; horizontal: pares del jefe de proyecto; externa: proveedores, reguladores, sociedad).

## 3. Ciberseguridad, Cumplimiento y Sostenibilidad

*   **Security by Design:** La seguridad debe ser un requisito desde la fase de análisis (cumplimiento del ENS - Esquema Nacional de Seguridad).
*   **Sostenibilidad (ESG):** Los proyectos públicos deben evaluar su huella de carbono y su impacto social (Sostenibilidad Ambiental, Social y de Gobernanza). Ya no es una opción, es una métrica de proyecto.

En proyectos TIC de la Administración Pública española, el cumplimiento normativo no es un anexo opcional sino un conjunto de restricciones que condicionan el alcance y la planificación desde el Acta de Constitución: el **Esquema Nacional de Seguridad (RD 311/2022)** obliga a categorizar el sistema y aplicar las medidas de seguridad correspondientes desde el diseño; el **RGPD y la LOPDGDD** exigen Privacidad desde el Diseño y por Defecto (art. 25 RGPD) y, en tratamientos de alto riesgo, una Evaluación de Impacto (EIPD); y el **Esquema Nacional de Interoperabilidad (ENI)** condiciona el diseño de sistemas que deban intercambiar información entre Administraciones. La gestión de proyectos moderna integra estos requisitos como parte del **Plan de Gestión de Riesgos y de Calidad**, no como una fase separada de auditoría final.

Sobre sostenibilidad, la propia norma **ISO 21502:2020** reconoce que los objetivos de sostenibilidad (ambiental, social y económica) deben considerarse durante todo el ciclo de vida del proyecto, alineándose con marcos como los **Objetivos de Desarrollo Sostenible (ODS)** de Naciones Unidas y los criterios **ESG** (*Environmental, Social, Governance*). En la práctica esto se traduce en indicadores de proyecto tan concretos como la huella de carbono de la infraestructura desplegada (relevante en proyectos de nube o centros de datos), la accesibilidad digital de las soluciones desarrolladas (cumplimiento de la normativa de accesibilidad web, ej. Real Decreto 1112/2018) y el impacto social del proyecto sobre los colectivos afectados.

## 4. IA y Gestión Basada en Datos (Data-Driven)

*   Uso de **IA para predecir** desviaciones de plazos (EVM predictivo).
*   Automatización de informes y dashboards en tiempo real (evitando el reporting manual).
*   Gestión de la calidad del dato: El éxito de la IA en proyectos depende de la fiabilidad de los datos alimentados (GIGO - *Garbage In, Garbage Out*).

Ampliando los casos de uso concretos de IA en dirección de proyectos, que cada vez aparecen más en manuales actualizados (PMBOK 8ª edición incorpora contenido explícito sobre IA):
*   **Generación automática de contenidos de gestión:** borradores de actas de reunión, informes de estado o resúmenes ejecutivos a partir de las notas del equipo.
*   **Análisis predictivo de riesgos:** modelos que, entrenados con datos históricos de proyectos similares, estiman la probabilidad de retraso o sobrecoste antes de que ocurra, complementando al EVM tradicional (que es descriptivo, no predictivo).
*   **Optimización de la asignación de recursos:** algoritmos que sugieren la mejor distribución del equipo entre tareas según carga de trabajo, competencias y disponibilidad.
*   **Chatbots y asistentes virtuales de proyecto:** para resolver dudas frecuentes de los interesados o automatizar el triaje de incidencias.

El concepto **GIGO** se complementa con el de **gobernanza del dato** (*Data Governance*): antes de automatizar decisiones con IA, el proyecto debe garantizar la trazabilidad, calidad y origen legítimo de los datos usados, y evaluar sesgos algorítmicos, especialmente relevante en el sector público donde las decisiones automatizadas pueden afectar a derechos de los ciudadanos (conectando este tema con los principios de **IA fiable y ética** que promueve el Reglamento Europeo de IA, AI Act).

## 5. Habilidades Blandas (Soft Skills)

Indispensables para el perfil P04 para conectar el código con el negocio.
*   **Inteligencia Emocional:** Gestión del estrés en hitos de entrega críticos.
*   **Negociación:** Fundamental para gestionar el alcance cuando el cliente quiere "añadir una funcionalidad más" a mitad del sprint.
*   **Gestión de Conflictos:** Capacidad de arbitrar entre el equipo técnico y el negocio.

El PMI formaliza estas competencias en el **Talent Triangle (Triángulo del Talento)**, marco de referencia oficial para la formación continua de sus certificados, actualizado recientemente con esta terminología:
*   **Ways of Working (Formas de Trabajar)**, antes llamado "Gestión de Proyectos Técnica": competencias metodológicas como gestión ágil e híbrida, EVM, gestión de riesgos, alcance y cronograma.
*   **Power Skills (Habilidades de Poder)**, antes llamado "Liderazgo": las habilidades blandas propiamente dichas — liderazgo colaborativo, escucha activa, comunicación, adaptabilidad, gestión de conflictos, inteligencia emocional, negociación, influencia y trabajo en equipo.
*   **Business Acumen (Visión de Negocio)**, antes llamado "Gestión Estratégica y de Negocio": comprensión del sector, gestión de beneficios, análisis competitivo, cumplimiento legal y normativo, y alineación estratégica.

Este marco es relevante para el examen porque desplaza el peso de "gestionar un proyecto" desde lo puramente técnico hacia una combinación equilibrada de las tres dimensiones, reflejando que un buen Jefe de Proyecto necesita tanto dominio metodológico como habilidades interpersonales y comprensión del negocio.

---

## 6. Resumen

| Concepto | Palabra Chivata |
| :--- | :--- |
| **Hibridación** | "Adaptación", "Tailoring", "Predictivo para negocio, ágil para ejecución", "Agile-fall". |
| **Stakeholders** | "Matriz Poder/Interés", "Gestión de expectativas", "Registro de interesados". |
| **4 procesos de gestión de interesados** | "Identificar → Planificar → Gestionar → Monitorear". |
| **Data-Driven** | "Predicción", "Métricas en tiempo real", "Toma de decisiones basada en hechos". |
| **Security by Design** | "Seguridad desde el inicio", "No es una capa externa", "ENS". |
| **Sostenibilidad/ESG** | "Ambiental, Social y de Gobernanza", "ISO 21502 lo integra en el ciclo de vida". |
| **GIGO** | "Garbage In, Garbage Out", "Calidad del dato condiciona la IA". |
| **PMI Talent Triangle** | "Ways of Working + Power Skills + Business Acumen". |

### 6.1. Simulacro de Test

**Pregunta:**
*En un proyecto híbrido, si un Stakeholder tiene alto poder de decisión pero poco interés en los detalles técnicos del desarrollo diario, ¿cuál es la estrategia recomendada?*
a) Gestionar estrechamente y reuniones diarias.
b) Mantenerle satisfecho con resúmenes ejecutivos.
c) Informarle puntualmente solo cuando haya fallos.
d) Ignorarle, ya que no tiene interés.

**Razonamiento Estructurado:**
1.  **Busca el patrón:** Stakeholder = Alto Poder / Bajo Interés.
2.  **Desmontando:**
    *   (A) Gestionar estrechamente es para quien tiene alto poder Y alto interés.
    *   (D) Ignorar a alguien con alto poder es suicidio profesional en gestión.
    *   (C) Informar solo de fallos es reactivo y peligroso.
    *   (B) **Mantenerle satisfecho** (con reportes de nivel ejecutivo que le den seguridad sin aburrirle con detalles técnicos) es la clave de la matriz de Mendelow.
3.  **Respuesta correcta: B.**

**Pregunta:**
*Según el enfoque de gestión de interesados del PMBOK, ¿en qué proceso se elabora por primera vez el Registro de Interesados?*
a) Planificar el Involucramiento de los Interesados.
b) Identificar a los Interesados.
c) Gestionar el Involucramiento de los Interesados.
d) Monitorear el Involucramiento de los Interesados.

**Razonamiento Estructurado:**
1.  El Registro de Interesados es el entregable que documenta por primera vez quiénes son los interesados, su rol, su poder y su interés; esto ocurre en el primer proceso del ciclo, antes de poder planificar nada sobre ellos.
2.  Los procesos posteriores (b, c, d en el enunciado original) actualizan o utilizan ese registro, pero no lo crean por primera vez.
3.  **Respuesta correcta:** B.

**Pregunta:**
*Según el PMI Talent Triangle actualizado, ¿en cuál de sus tres dimensiones se incluyen específicamente competencias como la inteligencia emocional, la negociación y la gestión de conflictos?*
a) Ways of Working.
b) Power Skills.
c) Business Acumen.
d) Technical Project Management (denominación original sin cambios).

**Razonamiento Estructurado:**
1.  "Ways of Working" (A) agrupa competencias metodológicas (ágil, EVM, riesgos). "Business Acumen" (C) agrupa comprensión de negocio y cumplimiento normativo. (D) es la denominación antigua que ya no se usa tras la actualización.
2.  Las habilidades interpersonales como inteligencia emocional, negociación y gestión de conflictos se agrupan explícitamente en "Power Skills".
3.  **Respuesta correcta:** B.
