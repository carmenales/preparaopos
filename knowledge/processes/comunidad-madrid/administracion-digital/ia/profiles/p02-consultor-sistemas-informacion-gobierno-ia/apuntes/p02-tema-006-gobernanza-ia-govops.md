---
id: "cm-ad-ia-p02-tema-006-gobernanza-ia-govops"
title: "Gobernanza de la IA y Operacionalización del Gobierno (GovOps)"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/ia"
profiles:
  - "p02-consultor-sistemas-informacion-ia"
official_profile: "P02 - Consultor de Sistemas de Información - Especialista en Gobierno de IA"
official_topic: "Tema 6. Gobernanza de la IA Operacionalización del Gobierno (GovOps)"
source_ids: []
tags:
  - "gobierno-ia"
  - "govops"
  - "gestion-riesgos"
  - "gobierno-ti"
  - "gobierno-dato"
  - "ai-act"
  - "nist-ai-rmf"
  - "iso-iec-38507"
  - "enisa"
created_at: "2026-07-14"
last_reviewed: null
ai_generated: true
ai_sources:
  - "chatgpt"
  - "perplexity"
  - "gemini"
  - "base-apunte"
needs_human_review: true
---

# Gobernanza de la IA y Operacionalización del Gobierno (GovOps)

## Encaje en la convocatoria

Este tema corresponde al **Tema 6 del Anexo 3** de la Resolución 352/2026 (BOCM 11/06/2026) para el perfil **P02: Consultor de Sistemas de Información especialista en Gobierno de IA** de la Agencia para la Administración Digital de la Comunidad de Madrid.  

Completa los temas 4 y 5: aquí el foco es cómo **poner en práctica** la gobernanza y la gestión de riesgos de la IA (AI Act, NIST AI RMF, ENS, ISO/IEC 38507), incluyendo la integración con gobierno TI y del dato y la operacionalización mediante **GovOps / Policy‑as‑Code**.

## Ideas clave

1. **Gobierno vs gestión (ISO/IEC 38507 / COBIT):** El **gobierno** evalúa, dirige y monitoriza (EDM) el uso de la IA alineado con estrategia, legalidad y valores; la **gestión** planifica, construye, ejecuta y controla las actividades técnicas.  
2. **Sistema de gestión de riesgos (art. 9 AI Act):** Obligación legal para proveedores de sistemas de alto riesgo; es un proceso **continuo e iterativo** durante todo el ciclo de vida, no un documento estático.  
3. **Jerarquía de mitigación (art. 9.5 AI Act):** Primero eliminar o reducir riesgos por diseño; después medidas de mitigación y control; por último información y formación a los desplegadores.  
4. **NIST AI RMF 1.0:** Marco voluntario articulado en cuatro funciones: **GOVERN** (transversal y fundacional), **MAP**, **MEASURE** y **MANAGE**, aplicadas iterativamente al ciclo de vida. 
5. **GovOps y Policy‑as‑Code:** GovOps es la operacionalización del gobierno de IA integrando cumplimiento normativo y políticas en los pipelines de MLOps/LLMOps mediante **políticas como código**.  
6. **Gobierno del dato como prerrequisito:** El art. 10 AI Act exige gobernanza de datos (calidad, representatividad, documentación); sin buen gobierno del dato no hay IA fiable ni cumplimiento de sesgos. 
7. **Amenazas específicas de IA (ENISA):** Envenenamiento de datos en entrenamiento, ataques de evasión/adversarios en inferencia y ataques a modelos de caja negra (inferencia de membresía, inversión de modelo).

---

## 1. Concepto de gobierno de la IA

La **ISO/IEC 38507:2022** define el gobierno de la IA como el sistema mediante el cual una organización dirige y controla el uso actual y futuro de la IA.  

Objetivos esenciales en el sector público:

- Garantizar **cumplimiento normativo** (AI Act, RGPD, ENS, LOPDGDD).  
- Generar **confianza** y explicabilidad (evitar arbitrariedad, facilitar impugnación).  
- Asegurar **eficiencia y alineamiento** con la estrategia y el interés general (no sólo eficiencia económica).

Pilares prácticos:

- **Control:** definición de permisos, límites de acción y apetito de riesgo.  
- **Trazabilidad:** registros auditables de decisiones, datos y modelos (logs, linaje).  
- **Supervisión humana significativa:** evitar el sesgo de automatización mediante controles y métricas (override rates).  
- **Cumplimiento:** integración con políticas corporativas, auditoría y sistemas de gestión (SGIA, SGSI).

---

## 2. Gobierno vs gestión y modelo de tres líneas

### 2.1. Diferencia gobierno–gestión (COBIT / ISO 38507)

Los estándares de gobierno TI (COBIT, ISO/IEC 38507) distinguen:

- **Gobierno de la IA:**  
  - Lo ejerce la alta dirección, comités de gobierno de IA, órganos colegiados.  
  - Funciones **EDM**: **Evaluar** necesidades y riesgos, **Dirigir** con políticas y objetivos, **Monitorizar** desempeño y cumplimiento.  
- **Gestión de la IA:**  
  - La realizan equipos técnicos (datos, ML, operaciones, seguridad).  
  - Funciones: **Planificar, construir, ejecutar y controlar** casos de uso y sistemas concretos.

En examen aparece literalmente que el gobierno no “programa scripts diarios de MLOps”, sino que marca dirección, políticas y criterios; la gestión ejecuta las actividades técnicas.

### 2.2. Modelo de tres líneas de defensa

Aplicando el modelo de **tres líneas de defensa** en AAPP:

- **1ª línea:** equipos de desarrollo y operación de IA (MLOps/LLMOps), que **asumen y gestionan** riesgos en el día a día.  
- **2ª línea:** oficinas de gobierno de IA, DPO, seguridad TI; definen políticas, controles y supervisan.  
- **3ª línea:** auditoría interna/intervención, que verifica de forma independiente la eficacia del gobierno y el cumplimiento.

El **apetito de riesgo** (risk appetite) se define en el nivel de gobierno y sirve como referencia para evaluar riesgos identificados en el SGIA (ISO/IEC 42001).

---

## 3. Sistema de gestión de riesgos en el AI Act (art. 9)

El **artículo 9 AI Act** exige que los proveedores de sistemas de alto riesgo establezcan, implementen, documenten y mantengan un **sistema de gestión de riesgos** asociado al sistema.

### 3.1. Naturaleza del sistema

El riesgo se gestiona como un proceso:

- **Continuo e iterativo** a lo largo de todo el ciclo de vida del sistema de IA de alto riesgo.  
- Con **revisiones sistemáticas y actualizaciones regulares**.  
- Integrable con otros sistemas de gestión de riesgos obligatorios por normativa sectorial (aviación, sanidad, etc.).

### 3.2. Etapas literales (art. 9.2)

El art. 9.2 establece cuatro pasos:

1. **Identificación y análisis** de riesgos conocidos y razonablemente previsibles para salud, seguridad y derechos fundamentales cuando se usa conforme a la finalidad prevista.  
2. **Estimación y evaluación** de riesgos cuando el sistema se usa conforme a su finalidad, incluyendo **uso indebido razonablemente previsible**.  
3. **Evaluación de otros riesgos** que puedan surgir a partir de datos del sistema de vigilancia poscomercialización (art. 72 AI Act).  
4. **Adopción de medidas de gestión de riesgos** apropiadas y dirigidas a los riesgos identificados.

Los riesgos objeto de este artículo son sólo aquellos que pueden mitigarse o eliminarse mediante diseño, desarrollo o información técnica adecuada.

### 3.3. Jerarquía de mitigación (art. 9.5)

El art. 9.5 define un orden de prioridad jurídico:

1. **Eliminación o reducción de riesgos por diseño y desarrollo** del sistema en la medida técnicamente posible (Safety by Design).  
2. **Medidas de mitigación y control** para riesgos que no pueden eliminarse.  
3. **Información y formación** proporcionada al desplegador (art. 13), teniendo en cuenta su conocimiento, experiencia, educación y el contexto de uso.

En preguntas de examen se plantea explícitamente este orden: primero diseño, luego controles, finalmente información; no al revés.

### 3.4. Testing y grupos vulnerables

El sistema de gestión de riesgos incluye:

- **Pruebas (testing)** para identificar medidas de riesgo más apropiadas; pueden incluir test en condiciones reales (art. 60 AI Act).  
- Evaluación de impacto sobre **menores de 18 años** y otros grupos vulnerables.

---

## 4. Marcos de referencia: NIST AI RMF y ENS

### 4.1. NIST AI RMF 1.0 – funciones Govern, Map, Measure, Manage

El **NIST AI Risk Management Framework (AI RMF 1.0)** es un marco voluntario que organiza la gestión de riesgos de IA en cuatro funciones: **GOVERN, MAP, MEASURE y MANAGE**.

- **GOVERN:** función transversal y fundacional. Establece cultura de riesgo, roles, responsabilidades, políticas y procesos de gobernanza; rodea y guía a las demás funciones. 
- **MAP:** caracteriza el contexto y el sistema, identificando propósito, actores, datos, posibles impactos y dependencias.  
- **MEASURE:** evalúa y cuantifica riesgos e impactos utilizando métricas y pruebas apropiadas.  
- **MANAGE:** decide respuestas al riesgo (aceptar, mitigar, transferir, evitar), prioriza acciones y realiza seguimiento.

El **Playbook de NIST** proporciona acciones sugeridas y guías para materializar estas funciones en organizaciones.

### 4.2. Integración con el Esquema Nacional de Seguridad (ENS)

En la Administración española, la gobernanza de IA se integra con el **Esquema Nacional de Seguridad (ENS, RD 311/2022)**, que fija principios como:

- **Seguridad como proceso integral:** incluye todos los elementos humanos, materiales, técnicos, jurídicos y organizativos del sistema de información; se evita que la ignorancia u organización deficiente sean fuente de riesgo.  
- **Prevención, detección, respuesta y conservación:** la seguridad debe contemplar medidas en las cuatro fases para minimizar vulnerabilidades y gestionar incidentes.  
- **Líneas de defensa y diferenciación de responsabilidades:** separación de funciones de explotación y seguridad, con niveles de supervisión.

Estos principios se aplican también a sistemas de IA, en coherencia con la lógica del art. 9 AI Act y NIST AI RMF.

---

## 5. GovOps y Policy‑as‑Code

### 5.1. Concepto de GovOps

**GovOps (Governance Operations)** designa la disciplina que integra el gobierno de IA en las operaciones técnicas (MLOps/LLMOps): en lugar de aprobar modelos sólo mediante actas o comités, se incorporan controles de gobernanza directamente en pipelines y herramientas.

Relación con otros enfoques:

- **DevSecOps:** integra seguridad en desarrollo y operación.  
- **GovOps:** integra **cumplimiento normativo, ética y auditoría** en los pipelines y entornos de ejecución.

### 5.2. Policy‑as‑Code (políticas como código)

El pilar técnico de GovOps es **Policy‑as‑Code**, que consiste en traducir políticas y límites de riesgo en **reglas automatizadas evaluadas por código**:

- Un script del pipeline CI/CD comprueba que el modelo ha superado pruebas de sesgo (por ejemplo, métricas de equidad por subgrupos) y no presenta vulnerabilidades críticas antes de permitir su despliegue.  
- Las reglas pueden codificar requisitos del AI Act (por ejemplo, prohibición de determinados usos, necesidad de FRIA completa) y controles internos de SGIA (ISO/IEC 42001).

Esto materializa el enfoque **Govern–Map–Measure–Manage** de NIST en procesos repetibles y auditables.

---

## 6. Gobierno del dato como prerrequisito

El **art. 10 AI Act** exige gobernanza de datos para sistemas de alto riesgo: calidad, pertinencia, representatividad y ausencia de errores significativos.

Dependencias principales:

- **Gobierno del dato (DAMA‑DMBOK):**  
  - Definir **data owners**, responsabilidades sobre calidad y acceso.  
  - Mantener **catálogos de datos corporativos** y políticas de uso.  
- **Linaje de datos (data lineage):** trazabilidad desde origen y transformaciones hasta su ingesta por el modelo; imprescindible para auditar sesgos y errores.  
- **Golden data set:** conjunto de datos de referencia de alta calidad usado para evaluar y validar el funcionamiento del sistema de IA; mencionado por AEPD en políticas de explicabilidad.

Sin gobierno del dato, es difícil demostrar que se cumplen las obligaciones de sesgo y calidad de datos del AI Act y las expectativas de transparencia de AEPD/AESIA.

---

## 7. Amenazas específicas de IA según ENISA

El informe **“Securing Machine Learning Algorithms”** de ENISA clasifica amenazas específicas para sistemas de aprendizaje automático.

### 7.1. Ataques en la fase de entrenamiento – Data Poisoning

En la **fase de entrenamiento**, el modelo aprende a partir de datos históricos.

- **Envenenamiento de datos (Data Poisoning):** el atacante altera el conjunto de entrenamiento (inyectando ejemplos maliciosos o cambiando etiquetas) para corromper el modelo desde su origen, creando errores sistemáticos o backdoors.
- Impacto: el modelo se comporta mal en producción de forma consistente, pudiendo discriminar o aceptar entradas maliciosas específicas.

### 7.2. Ataques en inferencia – Evasion / Adversarial Examples

En la **fase de inferencia**, el modelo ya está entrenado e inmutable.

- **Ataques de evasión / ejemplos adversarios (Evasion / Adversarial Examples):** el atacante introduce pequeñas perturbaciones en la entrada (ruido imperceptible) para engañar al modelo y forzar clasificaciones incorrectas.
- No se modifican los datos de entrenamiento; el ataque ocurre sobre las entradas en producción.

En examen suele preguntarse esta diferencia: envenenamiento afecta al entrenamiento, evasión a la inferencia.

### 7.3. Ataques a modelos de caja negra – confidencialidad

ENISA describe también amenazas sobre modelos accesibles vía API:

- **Inferencia de membresía (Membership Inference):** a partir de respuestas del modelo, el atacante deduce si un registro concreto estuvo en el conjunto de entrenamiento.  
- **Inversión del modelo (Model Inversion):** el atacante reconstruye datos de entrenamiento o extrae parámetros mediante consultas repetidas y análisis estadístico.

Estas amenazas conectan con obligaciones del AI Act sobre confidencialidad, robustez y gestión de riesgos, y con controles de seguridad del ENS.

---

## Conceptos que suelen preguntarse

| Concepto a distinguir                    | Realidad técnica / normativa                                                                                   | Trampa de examen                                                                                     |
| :-------------------------------------- | :------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------- |
| **Gobierno vs gestión**                | Gobierno (alta dirección): Evalúa, Dirige, Monitoriza (EDM). Gestión (equipos): Planifica, Construye, Ejecuta, Controla. | “El gobierno de IA es el que programa los scripts MLOps diarios.”                         |
| **Envenenamiento vs evasión (ENISA)**  | Envenenamiento = ataque a datos de **entrenamiento**; evasión = ataque a entradas en **inferencias** de producción. | “Un ataque de evasión consiste en inyectar etiquetas falsas en el dataset original.”      |
| **NIST AI RMF – GOVERN**              | Función transversal que cultiva cultura de riesgo y establece políticas; enmarca MAP, MEASURE y MANAGE.| “GOVERN es la última fase y sólo se aplica después de medir riesgos.”                     |
| **Jerarquía de mitigación (AI Act)**   | 1) Diseño adecuado; 2) Medidas de mitigación y control; 3) Información y formación al desplegador. | “La primera opción legal para tratar un riesgo es informar al usuario en el manual.”      |
| **GovOps vs DevSecOps**               | DevSecOps integra seguridad; GovOps integra cumplimiento normativo, ética y auditoría en pipelines (Policy‑as‑Code). | “GovOps es sólo un escáner de vulnerabilidades SAST.”                                     |
| **Golden data set (AEPD)**            | Conjunto de datos de alta calidad usado como referencia para evaluar y validar el sistema.           | “Es un almacén de contraseñas o de incidentes.”                                           |
| **Apetito de riesgo y SGIA**          | La política de IA fija tolerancia al riesgo; la evaluación de riesgos la usa como criterio en todo el ciclo de vida.| “La evaluación de riesgos se hace sólo al final y sin referencia al apetito definido.”    |

---

## Posibles preguntas tipo test

**Pregunta 1.** De acuerdo con el marco NIST AI RMF 1.0, ¿qué función actúa como pilar transversal para cultivar cultura de riesgo, establecer políticas y asignar responsabilidades, informando al resto de funciones?

A. MAP (Mapear).  
B. MEASURE (Medir).  
C. MANAGE (Gestionar).  
D. GOVERN (Gobernar).  

**Respuesta correcta: D.**.

---

**Pregunta 2.** Según ENISA, si un atacante altera sutilmente los píxeles de una imagen de entrada en producción para engañar al modelo y forzar una clasificación incorrecta, sin modificar el conjunto de entrenamiento, ¿qué tipo de ataque está realizando?

A. Envenenamiento de datos (Data Poisoning).  
B. Ataque de evasión / ejemplos adversarios (Evasion / Adversarial Attack).  
C. Inversión de modelo (Model Inversion).  
D. Inferencia de membresía (Membership Inference).  

**Respuesta correcta: B.**.

---

**Pregunta 3.** Según el art. 9 del Reglamento (UE) 2024/1689, ¿cuál es el orden de prioridad (jerarquía de mitigación) para tratar los riesgos identificados en sistemas de alto riesgo?

A. Proporcionar información y formación primero; rediseñar sólo si no es suficiente.  
B. Eliminar o reducir riesgos mediante diseño y desarrollo; si no es posible, implementar medidas de mitigación/control; finalmente, proporcionar la información requerida y formación al desplegador.  
C. Transferir el riesgo mediante pólizas de seguro.  
D. Aceptar el riesgo documentándolo sin necesidad de rediseño.  

**Respuesta correcta: B.**.

---

**Pregunta 4.** ¿Cómo se denomina el paradigma que operacionaliza el gobierno (GovOps) traduciendo requisitos normativos y límites de riesgo en scripts que bloquean despliegues en el pipeline de MLOps si no se cumplen?

A. Model Drift Monitoring.  
B. Shadow IT Authorization.  
C. Policy‑as‑Code (Políticas como Código).  
D. Continuous Integration (CI).  

**Respuesta correcta: C.**.

---

**Pregunta 5.** Bajo estándares de gobierno corporativo de TI (ISO/IEC 38507, COBIT), ¿qué afirmación define correctamente la diferencia estructural entre “Gobierno de la IA” y “Gestión de la IA”?

A. El gobierno ejecuta MLOps diarios, mientras la gestión audita resultados.  
B. No existe diferencia técnica; son sinónimos en el ENS.  
C. El gobierno evalúa, dirige y monitoriza el uso de la IA alineado con objetivos estratégicos (EDM); la gestión planifica, construye, ejecuta y controla actividades técnicas para alcanzarlos.  
D. El gobierno se aplica sólo al hardware, la gestión al fine‑tuning de modelos.  

**Respuesta correcta: C.**.

---

## Normativa o fuentes relacionadas

- **Reglamento (UE) 2024/1689 (Ley de IA):** art. 9 (sistema de gestión de riesgos), art. 10 (datos y gobernanza de datos), art. 72 (seguimiento poscomercialización). 
- **NIST AI RMF 1.0 (NIST AI 100‑1):** funciones Govern, Map, Measure, Manage, y AI RMF Playbook.
- **ISO/IEC 38507:2022:** *Governance of implications of the use of artificial intelligence by organizations*.  
- **ENISA – Securing Machine Learning Algorithms:** taxonomía de amenazas de ML (data poisoning, adversarial attacks, data exfiltration, etc.).
- **Real Decreto 311/2022 (ENS):** seguridad como proceso integral, principios de prevención–detección–respuesta–conservación y diferenciación de responsabilidades.

## Dudas o puntos pendientes

- **Madurez del término “GovOps”:** No existe definición única estandarizada por ISO; en la práctica se utiliza para describir la automatización de controles de gobernanza (AI Act, NIST AI RMF, ISO/IEC 42001) mediante Policy‑as‑Code en pipelines de MLOps/LLMOps. 
- **Estandarización detallada de métricas de sesgo y equidad:** El AI Act remite a normas armonizadas y guías de organismos (NIST, ENISA, AEPD, AESIA), que seguirán actualizándose; conviene revisar versiones consolidadas en el momento de la oposición.