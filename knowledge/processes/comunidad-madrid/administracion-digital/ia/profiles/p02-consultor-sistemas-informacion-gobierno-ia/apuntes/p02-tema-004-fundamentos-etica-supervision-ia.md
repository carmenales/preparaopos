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
  - "iso-42001"
  - "aesia"
  - "fria"
  - "rgpd"
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

Este tema es el núcleo fundacional del perfil **P02: Consultor de Sistemas de Información especialista en Gobierno de IA**, correspondiente al **Tema 4 del Anexo 3** de la Resolución 352/2026 (BOCM 11/06/2026).

En las preguntas de bloque P02 se exploran tanto los principios éticos clásicos (equidad, transparencia, responsabilidad, explicabilidad) como su traducción en obligaciones normativas concretas en el **Reglamento (UE) 2024/1689 (Ley de IA)**, el **RGPD**, las guías de la **AEPD/AESIA** y la norma **ISO/IEC 42001** sobre sistemas de gestión de IA.

## Ideas clave

1. **De la ética al derecho (4 pilares):** Equidad, transparencia, responsabilidad y explicabilidad pasan de ser recomendaciones a convertirse en obligaciones legales auditables en la Ley de IA (por ejemplo, gobernanza de datos en el artículo 10 y transparencia en el artículo 13). 
2. **Excepción de datos sensibles (art. 10.5 Ley de IA):** Se permite, con fuertes garantías, tratar categorías especiales de datos personales (art. 9 RGPD) exclusivamente para detectar y corregir sesgos en sistemas de alto riesgo, si no es posible hacerlo con datos sintéticos. 
3. **Privacidad desde el diseño (art. 25 RGPD):** La protección de datos por diseño exige incorporar medidas técnicas y organizativas (minimización, seudonimización, configuración por defecto mínima) desde la concepción de la arquitectura, no como parche final. 
4. **FRIA vs. EIPD:** La **Evaluación de Impacto sobre los Derechos Fundamentales (FRIA)** regulada en la Ley de IA complementa, pero no sustituye, la **Evaluación de Impacto en Protección de Datos (EIPD/DPIA)** del art. 35 RGPD para tratamientos de alto riesgo. 
5. **Marcos internacionales:** Las directrices de la **UE (HLEG)**, la recomendación de la **OCDE** y la recomendación de la **UNESCO** son instrumentos de *soft law*, mientras que la Ley de IA es *hard law* vinculante y basada en niveles de riesgo; UNESCO destaca por prohibir explícitamente vigilancia masiva y *social scoring*. 
6. **Supervisión humana significativa (art. 14 Ley de IA):** Se exige mitigar el sesgo de automatización y, en ciertos sistemas biométricos de alto riesgo, aplicar la “regla de los cuatro ojos”, es decir, doble verificación humana independiente antes de tomar decisiones. 
7. **Transparencia y explicabilidad:** La transparencia incluye informar del uso de IA y sus capacidades y limitaciones; la explicabilidad exige aportar razones comprensibles de decisiones concretas, asociada a técnicas de interpretabilidad y “caja negra/blanca”. 
8. **ISO/IEC 42001 (SGIA):** La política de IA establece objetivos y apetito de riesgo y sirve de referencia para evaluar riesgos identificados en todas las etapas del ciclo de vida del sistema.  

---

## 1. Principios éticos en IA: equidad, transparencia, responsabilidad y explicabilidad

La base ética europea se consolida con las **“Directrices éticas para una IA fiable”** del Grupo de Expertos de Alto Nivel sobre IA (HLEG) de la Comisión Europea (2019), que articulan siete requisitos (acción humana, robustez, privacidad y gestión de datos, transparencia, diversidad/no discriminación, bienestar social y rendición de cuentas).

### 1.1. Equidad (Fairness)

La equidad exige que los sistemas de IA no generen impactos discriminatorios o desproporcionados sobre ciertos grupos. 

En la Ley de IA, este principio se concreta en el **artículo 10 (Datos y gobernanza de datos)**:

- Los conjuntos de datos de entrenamiento, validación y prueba deben ser pertinentes, representativos, suficientemente amplios y libres de errores significativos. 
- Se exige examen activo para identificar y mitigar sesgos capaces de afectar a la salud, la seguridad o los derechos fundamentales.

La equidad tiene una doble dimensión en la UE: **sustantiva** (resultado material no discriminatorio) y **procedimental** (garantías en cómo se toman las decisiones), que aparece en preguntas de examen sobre la noción de “Fairness” en el marco europeo.

### 1.2. Transparencia

La transparencia implica que:

- El usuario o afectado sabe que interactúa con un sistema de IA, en particular en sistemas donde la persona podría confundirse sobre la naturaleza humana o artificial del interlocutor. 
- Los sistemas de alto riesgo deben proporcionar suficiente información para que el desplegador pueda comprender correctamente el funcionamiento y las limitaciones del sistema y utilizarlo de manera apropiada (art. 13 Ley de IA).

La **Guía de Transparencia de AESIA** define transparencia como la cualidad de que el sistema sea comprensible para quienes lo diseñan, desarrollan y usan, ligada estrechamente a técnicas de **explicabilidad** e **interpretabilidad**.

### 1.3. Responsabilidad (Accountability)

El principio de responsabilidad exige identificar claramente quién responde por las decisiones del sistema de IA:

- Proveedor del modelo base.  
- Proveedor del sistema de IA (quien lo desarrolla y comercializa).  
- Desplegador (organización que lo usa en un contexto concreto).

El **“problema de las muchas manos” (many hands problem)** describe precisamente la dificultad de atribuir responsabilidades en cadenas complejas con muchos actores, y es central en la gobernanza de IA agéntica y sistemas distribuidos.

### 1.4. Explicabilidad

La explicabilidad es una forma de transparencia centrada en responder **por qué** se ha producido un resultado concreto:

- Es esencial en actos administrativos automatizados para evitar indefensión y permitir la impugnación informada. 
- El art. 13.3.b de la Ley de IA exige documentar las capacidades técnicas para proporcionar explicaciones significativas de los resultados y errores del sistema.

Se diferencia de la **interpretabilidad**, que se enfoca más en comprender internamente el modelo (estructura, pesos, reglas) desde un punto de vista técnico. 

La AESIA insiste en combinar análisis de **“caja blanca”** (auditando código, flujos de datos y orquestadores) con **“caja negra”** (golden tests, evaluación de salidas) para lograr explicabilidad práctica.

---

## 2. Gestión de sesgos y privacidad

### 2.1. Gestión de sesgos (art. 10 Ley de IA)

El artículo 10 de la Ley de IA regula los requisitos de datos y gobernanza:

- Calidad: pertinencia, representatividad, ausencia de errores y completitud razonable. 
- Mitigación de sesgos: el proveedor debe identificar y reducir sesgos que puedan provocar discriminaciones o impactos desproporcionados.

**Excepción crítica (art. 10.5):**  
La Ley permite tratar **categorías especiales de datos personales** (origen racial, opiniones políticas, convicciones religiosas, etc.), normalmente prohibidas por el art. 9 RGPD, de forma excepcional y bajo estrictas salvaguardas, **únicamente para detectar, prevenir o corregir sesgos** en sistemas de alto riesgo, y siempre que dichos datos se eliminen después.

En el examen se plantea esta excepción contraintuitiva: aunque en principio esos datos están prohibidos, el AI Act los autoriza bajo controles estrictos en el contexto de sesgos.

### 2.2. Tipología de sesgos (NIST SP 1270)

El informe **NIST SP 1270** distingue varias fuentes de sesgo:

- **Estadístico/computacional:** Muestras no representativas, desbalance de clases, errores en datos.  
- **Sistémico/histórico:** El modelo refleja fielmente desigualdades existentes en la sociedad o en los datos históricos (por ejemplo, discriminación laboral previa).  
- **Humano:** Prejuicios de diseñadores, operadores o supervisores; incluye el **sesgo de automatización**, donde el humano confía excesivamente en las recomendaciones de la IA.

### 2.3. Privacidad por diseño y por defecto (art. 25 RGPD)

El artículo 25 RGPD introduce dos obligaciones:

- **Protección de datos desde el diseño:** aplicar medidas técnicas y organizativas apropiadas **desde el momento de determinar los medios del tratamiento**, es decir, en el diseño de la arquitectura, y durante todo el tratamiento. 
- **Protección de datos por defecto:** la configuración inicial del sistema debe limitar el tratamiento a los datos estrictamente necesarios para cada finalidad.

En los test se subraya que no es una revisión puntual al final, sino una exigencia temprana en el diseño.

---

## 3. Marcos internacionales de ética en IA

En preguntas tipo test se pide diferenciar naturaleza jurídica y foco de cada marco.

| Marco                                            | Autor / Fecha                          | Naturaleza jurídica y foco principal                                                                 |
| :---------------------------------------------- | :------------------------------------- | :---------------------------------------------------------------------------------------------------- |
| Directrices éticas para una IA fiable           | Comisión Europea (HLEG, 2019)          | *Soft law*. Define 7 requisitos para IA fiable (acción humana, robustez, privacidad, transparencia, etc.).|
| Recomendación sobre IA                          | OCDE, 2019 (actualización 2024)        | *Soft law*. Primer estándar intergubernamental, basado en valores democráticos y crecimiento inclusivo.|
| Recomendación sobre Ética de la IA             | UNESCO, 2021                           | *Soft law* global. Enfatiza derechos humanos y sostenibilidad; prohíbe vigilancia masiva y *social scoring*.|
| Reglamento (UE) 2024/1689 (Ley de IA)           | Unión Europea, 2024                    | **Ley vinculante (hard law)**. Traduce principios éticos en obligaciones legales basadas en niveles de riesgo.|

En los exámenes se identifica la recomendación de **UNESCO 2021** como el primer instrumento normativo mundial que prohíbe expresamente sistemas de puntuación social y vigilancia masiva.

---

## 4. Auditoría, seguimiento y supervisión humana

### 4.1. Seguimiento poscomercialización (art. 72 Ley de IA)

La Ley de IA exige que los proveedores de sistemas de alto riesgo establezcan un sistema de **vigilancia poscomercialización**:

- Recolección y análisis sistemático de datos de operación durante toda la vida útil del sistema. 
- Objetivo: detectar derivas, nuevos riesgos, fallos recurrentes y situaciones no previstas inicialmente.

No es un control puntual tras el despliegue, sino una obligación continua a largo plazo.

### 4.2. Supervisión humana (art. 14 Ley de IA)

El artículo 14 regula la supervisión humana significativa, conectada con el sesgo de automatización.

Modalidades típicas:

- **Human‑in‑the‑loop (HITL):** El sistema propone, pero el humano decide y aprueba cada acción crítica (por ejemplo, resolución sancionadora). 
- **Human‑on‑the‑loop (HOTL):** El sistema opera con cierto grado de autonomía, pero existe monitorización humana con posibilidad de intervención, corrección o parada (“kill switch”).

**Regla de los cuatro ojos (art. 14.5):**  
Para sistemas de identificación biométrica remota de alto riesgo, la Ley exige que ninguna decisión se tome sin verificación y confirmación separada por **al menos dos personas físicas competentes**, lo que en examen se presenta como doble validación humana.

En el contexto de IA agéntica, las guías recomiendan además monitorizar:

- **Override rates:** frecuencia con la que el humano corrige o rechaza decisiones del agente.  
- Tiempo de respuesta en la supervisión, para evitar aprobaciones automáticas e irreflexivas.

---

## 5. Evaluaciones de impacto: FRIA y EIPD

### 5.1. FRIA (Evaluación de Impacto sobre Derechos Fundamentales)

La **FRIA** está regulada en el **art. 27 de la Ley de IA**:

- Es obligatoria para desplegadores que son organismos de Derecho público (Administración) y para ciertas entidades privadas, cuando vayan a usar sistemas de alto riesgo en ámbitos regulados. 
- Debe realizarse **antes** del despliegue del sistema.

Contenido mínimo (art. 27.1) incluye:

- Descripción del sistema, finalidad prevista y procesos afectados.  
- Frecuencia de uso y categorías de personas afectadas. 
- Identificación de riesgos específicos sobre derechos fundamentales.  
- Medidas de mitigación, supervisión humana y mecanismos internos de denuncia.

La Ley prevé que la **Oficina Europea de IA** elabore una plantilla estructurada para FRIA, pero lo relevante para el examen es conocer estos contenidos mínimos.

### 5.2. EIPD/DPIA (Evaluación de Impacto en Protección de Datos)

El **art. 35 RGPD** exige una evaluación de impacto en protección de datos cuando el tratamiento entrañe un **alto riesgo** para los derechos y libertades de las personas (por ejemplo, vigilancia sistemática, procesamiento a gran escala de datos sensibles).

La **AEPD** recuerda que deben revisarse las EIPD cuando cambian significativamente los riesgos o el contexto de tratamiento (por ejemplo, introducción de IA generativa en procesos ya existentes).

### 5.3. Complementariedad FRIA–EIPD (art. 27.4 Ley de IA)

La Ley de IA aclara que:

- FRIA evalúa impacto sobre el catálogo completo de derechos fundamentales (dignidad, no discriminación, tutela judicial, etc.). 
- EIPD se centra en riesgos derivados del tratamiento de datos personales.

Si la organización ya ha realizado una EIPD que cubre aspectos exigidos por FRIA, **la FRIA complementa, pero no sustituye, la EIPD**.

En el examen se pregunta explícitamente esta relación: la respuesta correcta es que ambas evaluaciones son complementarias.

---

## 6. Clasificación de sistemas de IA de alto riesgo y finalidad prevista

Las **“Draft Commission Guidelines on the Classification of High‑Risk AI Systems”** interpretan el Anexo III de la Ley de IA y sus criterios de clasificación.

### 6.1. Combinación de sistemas y reclasificación

Un sistema de IA que inicialmente no está en una categoría de alto riesgo puede convertirse en alto riesgo cuando:

- Se integra con otros sistemas de IA o aplicaciones de tal forma que **contribuye sustancialmente** a un proceso incluido en el Anexo III (por ejemplo, decisión sobre acceso a servicios esenciales, empleo, educación).

En un test se plantea que si un sistema se combina con otros y afecta a un ámbito de alto riesgo, pasa a considerarse de alto riesgo.

### 6.2. Finalidad prevista y usos razonablemente previsibles

La **finalidad prevista** del sistema (declarada por el proveedor) es importante, pero no es el único criterio:

- Si los materiales promocionales muestran usos de alto riesgo razonablemente previsibles, aunque los términos de servicio los prohiban, las directrices indican que el sistema debe clasificarse según esos usos previsibles.  
- En el examen se plantea que si el marketing sugiere usos de alto riesgo, el sistema se considera de alto riesgo aun cuando el contrato diga lo contrario.

---

## 7. Identificación biométrica remota (RBI) y participación activa

La clasificación de **sistemas de identificación biométrica remota (RBI)** distingue entre:

- Escenarios de participación activa: la persona coopera explícitamente, por ejemplo, colocándose en una zona marcada y mirando a un sensor para autenticarse.  
- Escenarios de vigilancia remota sin participación activa: cámaras fijas en espacios públicos o estaciones que escanean rostros sin acciones específicas del usuario.

Las directrices de la Comisión aclaran que ciertos sistemas con fuerte participación activa se considerarán fuera del ámbito de RBI remota masiva; esto aparece en preguntas tipo test que diferencian un acceso controlado frente a vigilancia no solicitada.

---

## 8. ISO/IEC 42001: Sistemas de gestión de IA (SGIA)

La norma **ISO/IEC 42001** establece un Sistema de Gestión de IA (SGIA) siguiendo la estructura de alto nivel (HLS), similar a ISO 27001.

### 8.1. Política de IA y evaluación de riesgos

Relación fundamental:

- La **política de IA** define objetivos, principios y **tolerancia al riesgo (risk appetite)** de la organización.  
- La **evaluación de riesgos** utiliza estos criterios de tolerancia como referencia para decidir si los riesgos identificados son aceptables o requieren mitigación.

En el examen se plantea que la política de IA **no es estática y decorativa**, sino el marco contra el que se evalúan riesgos en todas las etapas del ciclo de vida.

### 8.2. Gestión de riesgos y apetito de riesgo

Cuando el riesgo calculado supera el apetito de riesgo:

- Deben implementarse controles para reducir probabilidad o impacto hasta que el riesgo residual quede por debajo del umbral.  
- Una vez se alcanza un nivel compatible con el apetito de riesgo, la organización puede aceptar ese riesgo residual, documentándolo.

No se considera buena práctica simplemente elevar el apetito para acomodar riesgos altos sin controles, ni limitarse a transferirlos mediante seguros.

### 8.3. Ciclo de mejora continua y riesgos del ciclo de vida

El SGIA exige **mejora continua** basada en:

- Monitorización de resultados y aparición de riesgos emergentes.  
- Retroalimentación de estos hallazgos hacia fases de diseño y desarrollo para ajustar controles.

En las preguntas se destaca el riesgo asociado a la **fase de reutilización (Reuse)**: usar un sistema de IA en un contexto distinto para el que fue diseñado originalmente, con requisitos de precisión o garantías diferentes, lo que puede generar resultados inadecuados.

---

## 9. Transparencia y documentación (AESIA, ISO/IEC 42001)

La **Guía de Transparencia de AESIA** y el Anexo A de ISO/IEC 42001 coinciden en que la organización debe proporcionar información apropiada sobre el sistema de IA a las partes interesadas.

Esta información incluye:

- Capacidades y limitaciones del sistema.  
- Modos de fallo previsibles.  
- Métricas de rendimiento (precisión, tasas de error, incertidumbre).

No se exige publicar el código fuente ni todos los datos de entrenamiento; la transparencia se centra en hacer comprensible el funcionamiento y riesgos, apoyando la explicabilidad.

La guía menciona el **“golden data set”** como conjunto de datos de referencia de alta calidad usado para validar y evaluar el sistema, clave en estrategias de explicabilidad y control interno.

---

## 10. AEPD, EIPD y políticas de uso de IA generativa

Las guías de la **AEPD** sobre IA generativa y tratamiento de datos insisten en:

- Realizar o revisar una **EIPD** cuando el tratamiento entrañe alto riesgo para derechos y libertades, lo cual incluye muchos casos de uso de IA generativa sobre datos personales.  
- Definir políticas internas que impidan inclusión accidental de datos personales en prompts, mediante herramientas técnicas (DLP, filtros) y formación.

En preguntas se resalta que deben existir mecanismos para **impedir** el pegado accidental de datos personales en prompts, no simplemente confiar en que el usuario use VPN corporativa.

---

## 11. Oficina de IA y supervisión de modelos de uso general

El Reglamento de IA crea una **Oficina de IA** en la Comisión Europea con competencias específicas:

- Supervisar a proveedores de **modelos de uso general** (foundation models y modelos GPAI) en cuanto a cumplimiento de obligaciones de transparencia, documentación y gestión de riesgos sistémicos.  
- Coordinar autoridades nacionales y contribuir a elaboración de directrices y plantillas (por ejemplo, para FRIA).

---

## 12. Otros aspectos técnicos relevantes para ética y supervisión

### 12.1. RLHF vs. RLAIF

- **RLHF (Reinforcement Learning from Human Feedback):** aprendizaje por refuerzo usando evaluadores humanos que puntúan respuestas o preferencias.  
- **RLAIF (Reinforcement Learning from AI Feedback):** similar, pero las puntuaciones o comparaciones de calidad las genera otro modelo de IA, reduciendo coste humano pero introduciendo nuevos sesgos potenciales.

### 12.2. Cifrado homomórfico

El cifrado homomórfico permite realizar operaciones matemáticas directamente sobre datos cifrados, devolviendo resultados que, al descifrarse, coinciden con el cálculo sobre texto en claro.

En un entorno corporativo de IA:

- Contribuye a la **confidencialidad durante el procesamiento**, al no exponer datos sensibles en claro ni claves privadas en el servidor.

---

## 13. Régimen transitorio y Reglamento Ómnibus Digital

El Reglamento de IA establece una fecha límite para cumplir obligaciones de alto riesgo del Anexo III:

- En las preguntas se indica **02 de diciembre de 2027** como fecha clave para el pleno cumplimiento de obligaciones de riesgo alto.

La **Propuesta de Reglamento Ómnibus Digital sobre IA (COM(2025) 836 final)** tiene como objetivo:

- Ajustar el AI Act y otros reglamentos digitales para permitir, con salvaguardas, el uso de categorías especiales de datos personales para detectar y corregir sesgos.  
- No autoriza venta libre de datos sensibles ni elimina el RGPD; al contrario, refuerza la gobernanza de datos en el contexto de IA.

---

## Conceptos que suelen preguntarse

| Concepto a distinguir                  | Realidad jurídico/técnica                                                                                      | Trampa de examen                                                                                 |
| :------------------------------------- | :------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------- |
| FRIA vs. DPIA/EIPD                     | FRIA (Ley de IA) evalúa derechos fundamentales; DPIA (RGPD) evalúa protección de datos; son complementarias.| “La FRIA sustituye la DPIA para evitar burocracia duplicada.”                         |
| Tratamiento de datos sensibles (10.5)  | Permitido excepcionalmente para detectar/mitigar sesgos en sistemas de alto riesgo, con salvaguardas y eliminación posterior.| “Siempre está prohibido tratar origen racial bajo cualquier circunstancia.”           |
| Naturaleza de OCDE/UNESCO vs AI Act   | OCDE/UNESCO = *soft law*; AI Act = *hard law* vinculante.                                           | “UNESCO promulgó un reglamento obligatorio sobre social scoring.”                     |
| Transparencia vs. explicabilidad       | Transparencia = saber que hay IA y límites; explicabilidad = entender por qué un resultado concreto.| “Explicabilidad implica publicar pesos y código fuente siempre.”                      |
| Seguimiento poscomercialización        | Obligación continua de vigilancia durante toda la vida útil del sistema (art. 72).                 | “Solo se realiza en los primeros días tras el despliegue.”                            |
| FRIA–EIPD relación                     | FRIA complementa a EIPD; no exime ni sustituye.                                           | “Si haces EIPD ya no necesitas FRIA.”                                                 |
| ISO/IEC 42001 política–riesgo          | Política de IA fija apetito de riesgo; evaluación lo compara con riesgos en todo el ciclo de vida.  | “La política es decorativa y la evaluación de riesgos es independiente del SGIA.”    |
| Oficina de IA                          | Órgano de la Comisión que supervisa proveedores de modelos de uso general.                           | “Cada Estado miembro tiene su propia oficina exclusiva para foundation models.”       |
| Transparencia (AESIA)                  | Cualidad ligada a interpretabilidad/explicabilidad; informar capacidades, límites y métricas.       | “Transparencia obliga a publicar todo el código y datos.”                             |
| Golden data set                        | Conjunto de datos de referencia para validar y evaluar funcionamiento.                               | “Es un almacén de incidentes o contraseñas.”                                          |

---

## Posibles preguntas tipo test

**Pregunta 1.** Según la Ley de IA, ¿está permitido el tratamiento de categorías especiales de datos personales (como el origen racial o étnico) por parte del proveedor de un sistema de IA de alto riesgo?

A. En ningún caso, por la prohibición absoluta del RGPD.  
B. Sí, de forma excepcional, únicamente para garantizar el examen y detección de sesgos en sistemas de alto riesgo, con salvaguardas estrictas.  
C. Sí, siempre que los datos se publiquen en un registro abierto.  
D. Sí, pero solo si el sistema opera en modo “Human‑out‑of‑the‑loop”.  

**Respuesta correcta: B.** (corresponde a la excepción del art. 10.5 AI Act).

---

**Pregunta 2.** ¿Qué instrumento internacional fue el primer estándar normativo mundial que prohíbe explícitamente sistemas de puntuación social y vigilancia masiva?

A. Reglamento (UE) 2024/1689 (AI Act).  
B. Directrices del HLEG de la Comisión Europea.  
C. Recomendación sobre Ética de la IA de la UNESCO (2021).  
D. Recomendación sobre IA de la OCDE (2019).  

**Respuesta correcta: C.**.

---

**Pregunta 3.** Si la Agencia para la Administración Digital despliega un sistema de IA de alto riesgo y realiza una FRIA (art. 27 Ley de IA) estando ya obligada a una EIPD (art. 35 RGPD), ¿cuál es la relación correcta entre ambas evaluaciones?

A. La FRIA sustituye la EIPD.  
B. La EIPD sustituye a la FRIA.  
C. La FRIA se integra y **complementa** la EIPD.  
D. Debe elegirse sólo una de ellas.  

**Respuesta correcta: C.**.

---

**Pregunta 4.** ¿Qué exige el principio de privacidad desde el diseño del art. 25 RGPD?

A. Solo aplicar medidas técnicas al desplegar el sistema en producción.  
B. Reaccionar únicamente cuando se produce una brecha notificada.  
C. Integrar medidas técnicas y organizativas apropiadas desde la determinación de los medios de tratamiento y durante el propio tratamiento.  
D. Actuar solo si lo requiere el Comité Europeo de Protección de Datos.  

**Respuesta correcta: C.**.

---

**Pregunta 5.** Según el art. 14 de la Ley de IA, ¿qué exigencia excepcional se aplica a decisiones adoptadas por sistemas de identificación biométrica remota de alto riesgo?

A. Supervisión anual diferida.  
B. Verificación y confirmación separada por al menos dos personas físicas competentes (regla de los cuatro ojos).  
C. Visto bueno de la AEPD en cada inferencia.  
D. Exención de supervisión si la confianza algorítmica supera el 99 %.  

**Respuesta correcta: B.**.

---

**Pregunta 6.** ¿Cuál es la relación fundamental entre la política de IA y la evaluación de riesgos según ISO/IEC 42001?

A. La evaluación se realiza sólo antes del desarrollo y la política se delega al proveedor del modelo.  
B. La evaluación de riesgos es únicamente cualitativa para no frenar la innovación.  
C. La política define objetivos y apetito de riesgo y sirve como criterio frente al que se comparan los riesgos en todas las etapas del ciclo de vida.  
D. La política es estática y la evaluación de riesgos se limita a la fase de desmantelamiento.  

**Respuesta correcta: C.**.

---

**Pregunta 7.** ¿Qué órgano tiene competencia exclusiva para supervisar a proveedores de modelos de IA de uso general según la Ley de IA?

A. Banco Central Europeo.  
B. Oficinas de IA de cada Estado miembro.  
C. Comisión Europea, a través de la Oficina de IA.  
D. Autoridades de protección de datos nacionales.  

**Respuesta correcta: C.**.

---

## Normativa o fuentes relacionadas

- **Reglamento (UE) 2024/1689 (Ley de IA):**  
  - Art. 10 (Datos y gobernanza de datos).  
  - Art. 13 (Transparencia).  
  - Art. 14 (Supervisión humana).  
  - Art. 27 (FRIA).  
  - Art. 72 (Seguimiento poscomercialización).
- **Reglamento (UE) 2016/679 (RGPD):**  
  - Art. 25 (Privacidad por diseño y por defecto).  
  - Art. 35 (EIPD/DPIA).
- **Recomendación OCDE sobre IA (2019/2024).** Marco de valores democráticos y crecimiento inclusivo. 
- **Recomendación UNESCO sobre Ética de la IA (2021).** Prohibición explícita de social scoring y vigilancia masiva. 
- **ISO/IEC 42001 – Sistemas de gestión de IA.** Política, evaluación de riesgos y mejora continua.  
- **Guías AEPD/AESIA sobre IA generativa, transparencia y EIPD.**

---

## Dudas o puntos pendientes

- **Plantilla FRIA:** La Oficina de IA debe elaborar un cuestionario estándar para FRIA; a efectos de examen, lo clave es el contenido mínimo del art. 27.1. 
- **Fecha exacta de aplicación plena de obligaciones de alto riesgo:** Los borradores de directrices mencionan diciembre de 2027 como horizonte para plena aplicación; conviene verificar siempre la versión consolidada del AI Act.