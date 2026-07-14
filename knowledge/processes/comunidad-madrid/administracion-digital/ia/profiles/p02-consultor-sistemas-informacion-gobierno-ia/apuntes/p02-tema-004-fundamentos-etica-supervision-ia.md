---
id: "cm-ad-ia-p02-tema-004-fundamentos-etica-supervision-ia"
title: "Fundamentos de Ética y supervisión de sistemas de IA"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/ia"
profiles:
  - "p02-consultor-sistemas-informacion-ia"
official_profile: "P02 - Consultor de Sistemas de Información - Especialista en Gobierno de IA"
official_topic: "Tema 4. Fundamentos de Ética y supervisión de sistemas de IA"
source_ids: []
tags:
  - "etica-ia"
  - "sesgos"
  - "privacidad-por-diseno"
  - "ley-ia"
  - "ai-act"
  - "ocde"
  - "unesco"
  - "derechos-fundamentales"
  - "auditoria-algoritmica"
created_at: "2026-07-14"
last_reviewed: null
ai_generated: true
ai_sources:
  - "perplexity"
  - "chatgpt"
  - "gemini"
  - "base-apunte"
  - "eur-lex"
needs_human_review: true
---

# Fundamentos de Ética y supervisión de sistemas de IA

## Encaje en la convocatoria

Este tema es el núcleo fundacional del perfil **P02: Consultor de Sistemas de Información especialista en Gobierno de IA**, correspondiente al Tema 4 del Anexo 3 de la Resolución 352/2026 (BOCM 11/06/2026)[cite: 1]. 

A diferencia de los temas anteriores puramente arquitectónicos, el tribunal evalúa aquí la capacidad de traducir **principios éticos abstractos en obligaciones jurídicas y controles auditables**. En un examen tipo test con penalización, es crucial discriminar los distintos marcos internacionales (la OCDE y la UNESCO son *soft law*; el Reglamento de IA es *hard law*) y no confundir herramientas legales limítrofes (la EIPD del RGPD frente a la FRIA de la Ley de IA). Especial atención merece la excepción legal del Art. 10.5 de la Ley de IA, que permite, de forma contraintuitiva pero estrictamente regulada, el tratamiento de datos personales sensibles para detectar sesgos.

## Ideas clave

1.  **De la Ética al Derecho (Los 4 Pilares):** Equidad, Transparencia, Responsabilidad y Explicabilidad no son meras recomendaciones. El AI Act las materializa en obligaciones normativas concretas (ej. Art. 10 para sesgos/equidad, Art. 13 para transparencia)[cite: 2].
2.  **Excepción de Datos Sensibles (Art. 10.5 Ley IA):** Para mitigar sesgos algorítmicos, la ley permite excepcionalmente procesar categorías especiales de datos personales (Art. 9 RGPD) bajo estrictas garantías, si la corrección no puede lograrse con datos sintéticos[cite: 2].
3.  **Privacidad desde el Diseño (Art. 25 RGPD):** *Privacy by Design* no es una revisión final de seguridad. Es una obligación legal que exige integrar medidas técnicas (como la seudonimización) desde el momento mismo de la concepción de la arquitectura del sistema[cite: 2].
4.  **FRIA vs. EIPD:** La Evaluación de Impacto en los Derechos Fundamentales (FRIA, Art. 27 Ley IA) aplica a entidades públicas que desplieguen IA de alto riesgo. **Complementa, pero no sustituye**, a la Evaluación de Impacto de Protección de Datos (EIPD, Art. 35 RGPD)[cite: 2].
5.  **Marcos Internacionales (Diferenciación de test):** 
    *   **UE (HLEG, 2019):** Define los "7 requisitos clave para una IA fiable".
    *   **OCDE (2019):** Primer estándar intergubernamental basado en valores democráticos[cite: 2].
    *   **UNESCO (2021):** Primer instrumento normativo mundial. Destaca por prohibir expresamente la vigilancia masiva y el *Social Scoring*[cite: 2].
6.  **Supervisión Humana (Art. 14 Ley IA):** Exige mitigar normativamente el "sesgo de automatización". Establece la "regla de los cuatro ojos" (doble verificación humana separada) para sistemas biométricos de alto riesgo[cite: 2].

## Desarrollo

### 1. Principios éticos en IA: equidad, transparencia, responsabilidad y explicabilidad

La base ética europea fue establecida por el Grupo de Expertos de Alto Nivel sobre IA (HLEG) en sus "Directrices éticas para una IA fiable" (2019). Estos principios informan la base de la Ley de IA:

*   **Equidad (*Fairness*):** Exige que el sistema no genere impactos desproporcionados o discriminatorios. En el Reglamento (UE) 2024/1689 se operacionaliza a través del Artículo 10 (Gobernanza de Datos), exigiendo el examen activo de los conjuntos de datos en busca de posibles sesgos que afecten a la salud, seguridad o derechos fundamentales (Art. 10.2.f)[cite: 2].
*   **Transparencia:** Comprende la obligación de revelar que se está interactuando con una IA. En sistemas de alto riesgo (Art. 13 Ley IA), exige un diseño lo suficientemente transparente para que los usuarios (desplegadores) puedan interpretar los resultados, apoyado en instrucciones de uso detalladas[cite: 2].
*   **Responsabilidad (*Accountability*):** Principio que exige que exista un sujeto humano o jurídico que rinda cuentas por las decisiones del sistema. Implica auditoría y asunción de consecuencias legales, evitando que "la máquina" sirva como escudo de irresponsabilidad.
*   **Explicabilidad:** Es una dimensión profunda de la transparencia. Mientras la transparencia es general, la explicabilidad es la capacidad de justificar *por qué* el modelo tomó una decisión específica en un caso concreto (esencial para evitar la indefensión en actos administrativos automatizados). El Art. 13.3.b de la Ley de IA exige documentar las capacidades técnicas para proporcionar esta información[cite: 2].
    *   *Interpretabilidad vs. Explicabilidad:* La interpretabilidad es comprender matemáticamente el modelo (ej. un árbol de decisión). La explicabilidad es dar una razón comprensible a un usuario final.

### 2. Gestión de sesgos y privacidad

#### 2.1. Gestión de Sesgos (Art. 10 Ley IA)
El Artículo 10 de la Ley de Inteligencia Artificial ("Datos y gobernanza de datos") es crítico. Exige que los conjuntos de datos de entrenamiento, validación y prueba cumplan criterios de calidad:
*   Deben ser pertinentes, suficientemente representativos, estar exentos de errores y completos (Art. 10.3)[cite: 2].
*   Obliga a detectar, prevenir y mitigar los sesgos (Art. 10.2.g)[cite: 2].
*   **La excepción crítica (Art. 10.5):** Constituye un supuesto legal altamente preguntable. Se permite el tratamiento de categorías especiales de datos personales (raza, opiniones políticas, etc.) con el propósito **exclusivo y estricto** de detectar y corregir sesgos algorítmicos, siempre que se eliminen posteriormente y existan salvaguardas técnicas como la seudonimización o el cifrado[cite: 2].

#### 2.2. Tipología de Sesgos (NIST SP 1270)
*   **Sesgo Estadístico / Computacional:** Fallos en el muestreo o datos desbalanceados.
*   **Sesgo Sistémico / Histórico:** El algoritmo aprende correctamente de los datos, pero los datos reflejan desigualdades sociales estructurales.
*   **Sesgo Humano:** Prejuicios de los desarrolladores o el "Sesgo de automatización" (el operario confía ciegamente en el output de la IA).

#### 2.3. Privacidad desde el Diseño (*Privacy by Design*)
*   **Base Legal:** Artículo 25 del RGPD[cite: 2].
*   **Concepto Operativo:** Exige al responsable del tratamiento integrar medidas técnicas (ej. minimización de datos) **desde el momento en que se determinan los medios de tratamiento** (diseño original de la arquitectura), no como una capa de seguridad superpuesta al final del desarrollo[cite: 2]. *Privacy by Default* (por defecto) exige que la configuración inicial solo trate los datos estrictamente necesarios.

### 3. Marcos internacionales de ética en IA

En un examen tipo test, es esencial discriminar la naturaleza jurídica y el autor de cada marco:

| Marco | Autor y Fecha | Naturaleza Jurídica y Foco |
| :--- | :--- | :--- |
| **Directrices Éticas para una IA Fiable** | Comisión Europea (HLEG), 2019 | *Soft law*. Definen los "7 requisitos clave para una IA fiable" (acción humana, solidez, privacidad, transparencia, diversidad, bienestar social y rendición de cuentas). |
| **Principios sobre IA** | OCDE, 2019 (Actualizado 2024) | *Soft law*. Primer estándar intergubernamental. Enfoque en crecimiento inclusivo y valores democráticos[cite: 2]. |
| **Recomendación sobre la Ética de la IA** | UNESCO, 2021 | *Soft law* (193 Estados). Fuerte enfoque en derechos humanos y sostenibilidad climática. **Prohíbe expresamente la vigilancia masiva y el *Social Scoring***[cite: 2]. |
| **Reglamento (UE) 2024/1689 (Ley de IA / AI Act)** | Unión Europea, 2024 | **Hard law (Vinculante).** Traduce los principios en obligaciones legales auditables basadas en niveles de riesgo[cite: 2]. |

### 4. Auditoría, control y supervisión continua

#### 4.1. Seguimiento Poscomercialización (Art. 72 Ley IA)
*   **Concepto:** Los proveedores de sistemas de IA de alto riesgo deben mantener un sistema de vigilancia poscomercialización para recopilar y analizar de forma "activa y sistemática" los datos sobre el funcionamiento real del sistema durante toda su vida útil, detectando derivas o nuevos riesgos[cite: 2].
*   **Diferencia de test:** No es una evaluación de conformidad puntual previa al despliegue, es un **control continuo** en el tiempo[cite: 2].

#### 4.2. Supervisión Humana (Art. 14 Ley IA)
Diseño de la interfaz para prevenir la automatización ciega. Modalidades:
*   **HITL (*Human-in-the-loop*):** El sistema no actúa sin la aprobación expresa del humano. (Ej. Redactar una resolución sancionadora).
*   **HOTL (*Human-on-the-loop*):** El sistema opera autónomamente, pero el humano monitoriza con capacidad de abortar (*Kill Switch*).
*   **Exigencia excepcional (Art. 14.5):** En sistemas de identificación biométrica remota de alto riesgo, **ninguna decisión puede tomarse sin verificación separada por al menos dos personas físicas**[cite: 2].

### 5. Evaluación de derechos fundamentales y de impacto algorítmico

#### 5.1. Evaluación de Impacto sobre los Derechos Fundamentales (FRIA - Art. 27 Ley IA)
*   **Obligatoriedad:** Exigida a los responsables del despliegue (*Deployers*) que sean organismos de Derecho público (como la Administración de la C. de Madrid), así como a ciertas entidades privadas (banca/seguros), antes de desplegar un sistema de alto riesgo[cite: 2].
*   **Contenido Mínimo (Art. 27.1):** Descripción de procesos, frecuencia de uso, categorías de personas afectadas, riesgos específicos, medidas de supervisión humana implementadas y gobernanza interna de denuncia[cite: 2].

#### 5.2. FRIA vs. EIPD (RGPD)
*   La FRIA (Ley de IA) evalúa el impacto sobre el catálogo completo de la Carta de Derechos Fundamentales de la UE (derecho a la tutela judicial, no discriminación, dignidad).
*   La EIPD o DPIA (Art. 35 RGPD) evalúa específicamente los riesgos para la privacidad y libertades emanados del tratamiento de datos personales[cite: 2].
*   **Regla de compatibilidad (Foco de Test - Art. 27.4 Ley IA):** Si las obligaciones de la FRIA ya se cumplen en una EIPD del RGPD, la FRIA **complementará** a dicha EIPD. No se sustituyen ni se excluyen mutuamente[cite: 2].

## Conceptos que suelen preguntarse

| Concepto a distinguir | Realidad Jurídico/Técnica | Trampa de examen |
| :--- | :--- | :--- |
| **FRIA vs. DPIA/EIPD** | La FRIA evalúa Derechos Fundamentales (Ley IA). La DPIA evalúa Protección de Datos (RGPD). Son complementarias (Art. 27.4)[cite: 2]. | "La FRIA exime y sustituye a la DPIA para evitar burocracia duplicada". |
| **Tratamiento de Datos Sensibles (Art. 10.5 Ley IA)** | Se permite excepcionalmente solo para detectar y mitigar sesgos algorítmicos[cite: 2]. | "Está absolutamente prohibido tratar el origen racial por el Art. 9 del RGPD bajo cualquier circunstancia". |
| **Naturaleza de Marcos Internacionales** | OCDE y UNESCO son *Soft law* (Recomendaciones no vinculantes)[cite: 2]. El Reglamento UE de IA es *Hard law*[cite: 2]. | "La UNESCO emitió un reglamento de obligado cumplimiento sobre Social Scoring". |
| **Transparencia vs. Explicabilidad** | Transparencia = Saber que hay IA y su propósito general. Explicabilidad = Saber *por qué* el modelo arrojó este resultado. | "La explicabilidad requiere publicar siempre el código fuente y los pesos del modelo en internet". |
| **Seguimiento Poscomercialización** | Es una obligación continua durante toda la vida útil del sistema (Art. 72)[cite: 2]. | "Es un trámite que se realiza únicamente en los primeros 30 días tras el despliegue". |

## Posibles preguntas tipo test

**Pregunta 1.** Según el Reglamento (UE) 2024/1689 (Ley de IA), ¿está permitido el tratamiento de categorías especiales de datos personales (tales como el origen racial o étnico) por parte del proveedor de un sistema de IA de alto riesgo?
A. En ningún caso, debido a la prohibición expresa y absoluta del Reglamento General de Protección de Datos (RGPD).
B. Sí, excepcionalmente, en la estricta medida en que sea necesario para garantizar el examen y la detección de sesgos en relación con los sistemas de IA de alto riesgo.
C. Sí, siempre que dichos datos se publiquen en un registro abierto para facilitar las auditorías externas.
D. Sí, pero únicamente si el sistema opera bajo un paradigma "Human-out-of-the-loop".
**Respuesta correcta: B.** (Es la excepción crítica del Artículo 10.5 de la Ley de IA, muy contraintuitiva frente a la normativa general de protección de datos)[cite: 2].

**Pregunta 2.** En el contexto de los marcos internacionales sobre la ética en la Inteligencia Artificial, ¿qué instrumento internacional fue el primer estándar normativo mundial adoptado, destacando por su prohibición explícita de los sistemas de puntuación social (*social scoring*) y vigilancia masiva?
A. El Reglamento (UE) 2024/1689 (AI Act).
B. Las Directrices Éticas para una IA Fiable del HLEG de la Comisión Europea.
C. La Recomendación sobre la Ética de la Inteligencia Artificial de la UNESCO (2021).
D. La Recomendación del Consejo sobre Inteligencia Artificial de la OCDE (2019).
**Respuesta correcta: C.** (La UNESCO marcó un hito global al introducir estas prohibiciones expresas en 2021, antes que el AI Act)[cite: 2].

**Pregunta 3.** Si la Agencia para la Administración Digital va a desplegar un sistema de IA de alto riesgo para la priorización de inspecciones, y realiza la Evaluación de Impacto sobre los Derechos Fundamentales (FRIA) exigida por el artículo 27 de la Ley de IA, ¿qué ocurre si la Administración ya está obligada a realizar una Evaluación de Impacto de Protección de Datos (EIPD) por el artículo 35 del RGPD?
A. La FRIA sustituye y anula la necesidad de realizar la EIPD.
B. La EIPD sustituye a la FRIA, eximiendo a la Administración de esa obligación de la Ley de IA.
C. La FRIA se integrará y complementará a dicha Evaluación de Impacto de Protección de Datos (EIPD).
D. Debe elegirse solo una de ellas a criterio del Delegado de Protección de Datos.
**Respuesta correcta: C.** (La Ley de IA establece en el Art. 27.4 la complementariedad de ambas evaluaciones, evitando la exención total o el solapamiento ciego)[cite: 2].

**Pregunta 4.** El principio de Privacidad desde el Diseño (*Privacy by Design*), regulado en el Artículo 25 del RGPD, impone al responsable del tratamiento la obligación de aplicar medidas técnicas y organizativas apropiadas:
A. Únicamente en el momento del despliegue a producción.
B. Solo si se produce una brecha de seguridad notificada a la AEPD.
C. Desde el momento en que se determinan los medios de tratamiento y en el propio tratamiento.
D. Exclusivamente a requerimiento expreso del Comité Europeo de Protección de Datos.
**Respuesta correcta: C.** (Es la definición literal de diseñar la privacidad en las fases tempranas de la arquitectura)[cite: 2].

**Pregunta 5.** De acuerdo con el Artículo 14 del Reglamento (UE) 2024/1689, ¿qué exigencia excepcional de supervisión humana aplica a las decisiones adoptadas por sistemas de IA de alto riesgo de identificación biométrica remota?
A. Deben operar bajo supervisión asíncrona anual.
B. Ninguna decisión puede tomarse sin verificación y confirmación separada por al menos dos personas físicas competentes.
C. Requieren el visto bueno de la Agencia Española de Protección de Datos en cada inferencia.
D. Están exentos de supervisión si la confianza algorítmica supera el 99%.
**Respuesta correcta: B.** (Es la "regla de los cuatro ojos" o doble validación humana exigida en el Art. 14.5)[cite: 2].

## Normativa o fuentes relacionadas

*   **Reglamento (UE) 2024/1689 (Ley de IA):**
    *   Art. 10 (Gobernanza de datos e identificación de sesgos)[cite: 2].
    *   Art. 13 (Transparencia)[cite: 2].
    *   Art. 14 (Supervisión humana)[cite: 2].
    *   Art. 27 (Evaluación de impacto sobre los derechos fundamentales - FRIA)[cite: 2].
    *   Art. 72 (Seguimiento poscomercialización)[cite: 2].
*   **Reglamento (UE) 2016/679 (RGPD):**
    *   Art. 25 (Protección de datos desde el diseño y por defecto)[cite: 2].
    *   Art. 35 (Evaluación de impacto de protección de datos - EIPD/DPIA)[cite: 2].
*   **Recomendación de la OCDE sobre Inteligencia Artificial (2019 / 2024):** Marco de *soft law* fundamentado en valores democráticos y crecimiento inclusivo[cite: 2].
*   **Recomendación sobre la Ética de la Inteligencia Artificial (UNESCO, 2021):** Instrumento mundial con prohibición expresa de *Social Scoring* y enfoque en sostenibilidad[cite: 2].

## Dudas o puntos pendientes

*   **Metodología y Plantilla de la FRIA:** El artículo 27.5 de la Ley de IA establece que la Oficina Europea de Inteligencia Artificial debe desarrollar un modelo de cuestionario (plantilla) para facilitar el cumplimiento de la FRIA por parte de los desplegadores. A fecha de estudio, el formato técnico de este formulario puede encontrarse en fase de redacción. Para el examen, lo exigible es conocer el contenido mínimo obligatorio regulado en el Art. 27.1 (Descripción de procesos, categorías afectadas, riesgos, supervisión, mecanismos de denuncia)[cite: 2].