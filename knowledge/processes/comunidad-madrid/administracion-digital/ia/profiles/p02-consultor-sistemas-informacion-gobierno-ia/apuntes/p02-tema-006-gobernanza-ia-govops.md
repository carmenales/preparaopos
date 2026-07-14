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

Este tema corresponde al **Tema 6 del Anexo 3** de la Resolución 352/2026 (BOCM 11/06/2026) exclusivo para el perfil **P02: Consultor de Sistemas de Información especialista en Gobierno de IA** de la Agencia para la Administración Digital de la Comunidad de Madrid. 

Tras estudiar en el Tema 5 la norma legal pura (*AI Act*, RGPD, ISO 42001), este Tema 6 evalúa la **implementación organizativa y técnica** de dicha norma en la Administración Pública. En un examen tipo test con penalización, el tribunal buscará que el opositor discrimine rigurosamente entre *Gobierno* (dirigir y evaluar) y *Gestión* (construir y operar), que conozca la estructura del **NIST AI RMF 1.0** y que distinga las fases de ataque a la IA según las taxonomías de **ENISA** (Data Poisoning vs. Evasión). Asimismo, debe entenderse el concepto emergente de **GovOps**: la traducción de la ética y la ley en código ejecutable (*Policy-as-Code*) dentro de los *pipelines* de MLOps/LLMOps.

## Ideas clave

1.  **Gobierno vs. Gestión (ISO/IEC 38507 / COBIT):** El **Gobierno** evalúa, dirige y monitoriza (EDM) asegurando la alineación con la estrategia y la legalidad. La **Gestión** planifica, construye, ejecuta y controla. El gobierno recae en la alta dirección/comités; la gestión en los equipos técnicos.
2.  **Sistema de Gestión de Riesgos (Art. 9 AI Act):** Es una obligación legal para sistemas de alto riesgo. No es un documento estático, sino un **proceso iterativo continuo** a lo largo de todo el ciclo de vida del sistema. La responsabilidad recae en el **Proveedor** (aunque el Responsable del Despliegue deba vigilarlo).
3.  **NIST AI RMF 1.0:** Marco voluntario estructurado en cuatro funciones principales. La función **GOVERN** es transversal y fundacional; las funciones **MAP**, **MEASURE** y **MANAGE** se aplican de forma iterativa al ciclo de vida.
4.  **GovOps (Governance Operations):** Operacionalización del gobierno mediante la automatización. Su pilar es **Policy-as-Code** (Políticas como Código): traducir límites éticos o normativos en reglas que bloquean automáticamente el despliegue de un modelo si no las cumple.
5.  **Gobierno del Dato como Prerrequisito:** No hay IA fiable sin datos fiables. La trazabilidad completa (Linaje de datos) es esencial para cumplir con el Art. 10 de la Ley de IA.
6.  **Amenazas Específicas de IA (ENISA):** Distinción crítica de examen:
    *   Fase de Entrenamiento $\rightarrow$ **Envenenamiento de datos (*Data Poisoning*)**.
    *   Fase de Inferencia $\rightarrow$ **Ataques de Evasión / Ejemplos Adversarios**.
    *   Modelos de Caja Negra $\rightarrow$ Inferencia de Membresía e Inversión del Modelo.

## Desarrollo

### 1. Concepto de Gobierno de la IA

Según estándares como la **ISO/IEC 38507:2022** (Implicaciones de gobernanza del uso de IA), el Gobierno de la IA es el sistema mediante el cual se dirige y controla el uso actual y futuro de la IA por parte de la organización.
*   **Finalidad:** Garantizar tres resultados clave (Cumplimiento normativo, Confianza/Explicabilidad y Eficiencia).
*   **Pilares:** Control (permisos y límites), Trazabilidad (registro auditable), Supervisión Humana y Cumplimiento.

#### 1.1. Modelos de Gobernanza en Organizaciones Públicas
Las AAPP no solo buscan eficiencia, sino que están atadas al principio de legalidad, la prohibición de la arbitrariedad y el interés general.
*   **Apetito al Riesgo:** Debe definirse explícita y cuantitativamente (Riesgo = Impacto × Probabilidad). Ej. Un sistema de priorización de prestaciones sociales exige un apetito al riesgo de sesgo cercano a cero.
*   **Modelo Organizativo (Líneas de Defensa):**
    *   *1ª Línea:* Equipos de desarrollo/operación (Operan el riesgo).
    *   *2ª Línea:* Oficinas de Gobierno de IA, DPO, Ciberseguridad (Supervisan y definen políticas).
    *   *3ª Línea:* Auditoría Interna / Intervención (Verificación independiente).

### 2. Integración con el gobierno de TI (GovOps) y del dato

La IA no es un silo; debe integrarse en las estructuras corporativas existentes.

#### 2.1. Integración con Gobierno del Dato (DAMA-DMBOK)
El Art. 10 de la Ley de IA (Gobernanza de Datos) exige conjuntos de datos pertinentes y representativos. Esto requiere conectar la IA con catálogos de datos corporativos, definiendo claramente a los *Data Owners* y garantizando el **Linaje de los Datos** (origen y transformaciones hasta su ingesta por el algoritmo).

#### 2.2. Integración con Gobierno TI (COBIT) y MLOps
La IA introduce nuevos riesgos (Caja Negra, degradación o *Drift*). Los procesos tradicionales de Gestión de Cambios (ITIL) deben adaptarse.
*   **GovOps (Governance Operations):** Disciplina que integra el cumplimiento regulatorio directamente en las operaciones (MLOps/LLMOps).
*   **Policy-as-Code:** Automatiza la gobernanza. Por ejemplo, en lugar de un "acta de aprobación" manual en Word para un nuevo modelo, un *script* en el pipeline CI/CD verifica automáticamente que el modelo ha superado las pruebas de equidad y no tiene vulnerabilidades críticas conocidas (CVEs) antes de permitir su despliegue a producción.

### 3. Gestión de riesgos en sistemas de IA

La gestión de riesgos de IA difiere del software clásico por su naturaleza probabilística y su capacidad de aprender (y desviarse) con nuevos datos.

#### 3.1. Marco Normativo (Art. 9 AI Act - Sistema de Gestión de Riesgos)
*   **Sujeto Obligado:** El **Proveedor** de un sistema de alto riesgo (no el Responsable del Despliegue, aunque deba vigilarlo).
*   **Naturaleza:** Proceso **continuo e iterativo** a lo largo de todo el ciclo de vida (no un simple PDF ex-ante).
*   **Etapas Literales (Art. 9.2):**
    1.  Identificación y análisis de riesgos previsibles.
    2.  Evaluación de riesgos por uso previsto y *uso indebido razonablemente previsible*.
    3.  Evaluación de otros riesgos detectados en la vigilancia poscomercialización (Art. 72).
    4.  Adopción de medidas de gestión.
*   **Jerarquía de Mitigación (Orden estricto de examen):** 1º Eliminar por diseño $\rightarrow$ 2º Medidas de mitigación/control $\rightarrow$ 3º Información y formación a los responsables del despliegue.

#### 3.2. Marco Técnico Voluntario: NIST AI RMF 1.0
Estándar global estructurado en cuatro funciones principales (*Core Functions*):
1.  **GOVERN (Gobernar):** Función **transversal** y fundacional. Cultiva la cultura de riesgo, alinea la IA con los valores organizativos y establece políticas.
2.  **MAP (Mapear):** Contextualiza el sistema. Qué se va a construir, para qué, y a quién afecta.
3.  **MEASURE (Medir):** Análisis cuantitativo/cualitativo de los riesgos detectados (ej. pruebas de sesgo por subgrupos poblacionales).
4.  **MANAGE (Gestionar):** Priorización y respuesta al riesgo (Aceptar, Mitigar, Transferir o Evitar - *Go/No-Go*).

### 4. Principios de seguridad en el ciclo de vida de sistemas de IA

La seguridad en la IA ("Security" y "Safety") abarca todo el ciclo de vida, integrándose con el **Esquema Nacional de Seguridad (ENS - RD 311/2022)** para el sector público (seguridad como proceso integral, mínimo privilegio, líneas de defensa).

#### 4.1. Taxonomía de Amenazas Específicas de IA (ENISA)
Foco crítico de examen para distinguir en qué fase del ciclo de vida ocurre el ataque:

*   **Fase de Entrenamiento (*Training Phase*):**
    *   **Envenenamiento de Datos (*Data Poisoning*):** El atacante altera el conjunto de datos de entrenamiento (inyectando datos maliciosos o cambiando etiquetas) para corromper el modelo desde su origen, creando "puertas traseras" (*backdoors*).
*   **Fase de Inferencia (*Inference / Production Phase*):** El modelo ya está entrenado e inmutable.
    *   **Ataques de Evasión / Ejemplos Adversarios (*Adversarial Examples*):** El atacante altera sutilmente los datos de entrada (añadiendo "ruido" invisible al ojo humano) para engañar al modelo y forzar un error de clasificación.
*   **Riesgos de Modelos "Caja Negra" (Ataques a la Confidencialidad):**
    *   **Inferencia de Membresía (*Membership Inference*):** Analizando las salidas del modelo, el atacante deduce si un dato concreto (ej. información de salud de una persona) formó parte del conjunto de datos de entrenamiento.
    *   **Inversión del Modelo (*Model Inversion*):** El atacante reconstruye datos de entrenamiento o extrae los parámetros/pesos del propio modelo a base de realizar peticiones masivas a la API.

## Conceptos que suelen preguntarse

| Concepto a distinguir | Realidad Técnica / Normativa | Trampa de examen |
| :--- | :--- | :--- |
| **Gobierno vs. Gestión** | Gobierno (Alta Dirección): Evalúa, Dirige, Monitoriza (EDM). Gestión (Equipos): Planifica, Construye, Ejecuta. | "El Gobierno de IA es el encargado de programar los scripts de MLOps diarios." |
| **Envenenamiento vs. Evasión** | Envenenamiento = Ataca los datos de **Entrenamiento**. Evasión = Ataca la **Inferencia** en producción. | "Un ataque de evasión ocurre cuando se inyectan etiquetas falsas en el dataset original." |
| **NIST AI RMF (GOVERN)** | Función transversal que abarca todo el ciclo de vida y dicta la cultura de riesgos. | "GOVERN es la última fase que se aplica solo tras medir los riesgos." |
| **Jerarquía de Mitigación AI Act** | 1º Diseño $\rightarrow$ 2º Control $\rightarrow$ 3º Información. | "La primera opción legal para tratar un riesgo es informar al usuario en el manual." |
| **GovOps vs. DevSecOps** | DevSecOps integra ciberseguridad. GovOps integra cumplimiento legal, ética y auditoría (*Policy-as-Code*). | "GovOps es simplemente un escáner de vulnerabilidades de código fuente SAST." |

## Posibles preguntas tipo test

**Pregunta 1.** De acuerdo con el marco NIST AI RMF 1.0 para la gestión de riesgos en Inteligencia Artificial, ¿cuál de las siguientes funciones (*Core Functions*) actúa como el pilar transversal diseñado para cultivar una cultura de riesgo, establecer políticas y asignar la rendición de cuentas organizativa, informando al resto de funciones?
A. MAP (Mapear).
B. MEASURE (Medir).
C. MANAGE (Gestionar).
D. GOVERN (Gobernar).
**Respuesta correcta: D.** (Govern es la función fundacional que rodea y guía a Map, Measure y Manage).

**Pregunta 2.** En el contexto de la ciberseguridad específica para sistemas de aprendizaje automático (según las clasificaciones de agencias como ENISA), si un atacante altera sutilmente los píxeles de una imagen de entrada en producción para engañar al modelo y forzar una clasificación incorrecta, sin haber modificado el conjunto de datos de entrenamiento histórico, ¿qué tipo de ataque está realizando?
A. Ataque de envenenamiento de datos (*Data Poisoning*).
B. Ataque de evasión / ejemplos adversarios (*Evasion / Adversarial Attack*).
C. Inversión de modelo (*Model Inversion*).
D. Inferencia de membresía (*Membership Inference*).
**Respuesta correcta: B.** (Como el modelo ya está entrenado y la alteración (ruido) se produce en la entrada durante el tiempo de inferencia, se trata de evasión adversarial. Si atacara el dataset, sería envenenamiento).

**Pregunta 3.** Según el artículo 9 del Reglamento (UE) 2024/1689 (Ley de IA), relativo al "Sistema de gestión de riesgos" para sistemas de IA de alto riesgo, ¿cuál es el orden de prioridad estipulado normativamente (Jerarquía de Mitigación) para hacer frente a los riesgos detectados?
A. Proveer información y formación a los responsables del despliegue en primer lugar, y si no es suficiente, rediseñar el sistema.
B. Eliminar o reducir los riesgos mediante un diseño y desarrollo adecuados; si no es posible, implantar medidas de mitigación y control; y finalmente proporcionar la información requerida a los responsables del despliegue.
C. Transferir el riesgo mediante la contratación de pólizas de seguro de responsabilidad civil algorítmica.
D. Aceptar el riesgo documentándolo en la Evaluación de Impacto de Protección de Datos (EIPD), sin necesidad de rediseño.
**Respuesta correcta: B.** (El Art. 9.5 exige estrictamente este orden, priorizando la mitigación por diseño ("*Safety by Design*") frente a la mera provisión de manuales de uso).

**Pregunta 4.** ¿Cómo se denomina el paradigma técnico y organizativo que facilita la Operacionalización del Gobierno (GovOps) mediante la traducción de requisitos normativos, éticos y límites de riesgo en scripts automatizados que evalúan y bloquean despliegues en el *pipeline* de MLOps si no se cumplen dichas reglas?
A. Model Drift Monitoring.
B. Shadow IT Authorization.
C. Policy-as-Code (Políticas como Código).
D. Continuous Integration (CI).
**Respuesta correcta: C.** (*Policy-as-Code* permite que las reglas de gobernanza —ej. no superar un umbral X de sesgo demográfico— se evalúen automáticamente mediante código, materializando el concepto de GovOps).

**Pregunta 5.** Bajo los estándares internacionales de Gobierno Corporativo de TI (como la familia ISO/IEC 38507 o COBIT), ¿cuál de las siguientes afirmaciones define correctamente la diferencia estructural entre el "Gobierno de la IA" y la "Gestión de la IA"?
A. El Gobierno de IA ejecuta las operaciones de MLOps diarias, mientras la Gestión audita los resultados semestralmente.
B. No existe diferencia técnica, ambos términos son sinónimos absolutos en el Esquema Nacional de Seguridad.
C. El Gobierno evalúa, dirige y monitoriza el uso de la IA alineado con los objetivos estratégicos (EDM), mientras que la Gestión planifica, construye, ejecuta y controla las actividades técnicas para alcanzar esos objetivos.
D. El Gobierno se aplica exclusivamente al hardware de la red y la infraestructura Cloud, mientras que la Gestión se aplica al ajuste fino (*Fine-Tuning*) de los modelos fundacionales.
**Respuesta correcta: C.** (Definición canónica de estándares internacionales: Governance = Evaluar, Dirigir, Monitorizar. Management = Planificar, Construir, Ejecutar, Controlar).

## Normativa o fuentes relacionadas

*   **Reglamento (UE) 2024/1689 (Ley de IA):** Art. 9 (Sistema de gestión de riesgos). 
*   **NIST AI 100-1 (AI RMF 1.0):** *Artificial Intelligence Risk Management Framework*. Funciones: Govern, Map, Measure, Manage.
*   **ISO/IEC 38507:2022:** *Information technology — Governance of implications of the use of artificial intelligence by organizations*.
*   **ENISA:** *Securing Machine Learning Algorithms*. Clasificación canónica de amenazas (Poisoning vs. Evasion).
*   **Real Decreto 311/2022 (Esquema Nacional de Seguridad - ENS):** En particular el Art. 6 (Seguridad como proceso integral) y Art. 11 (Diferenciación de responsabilidades entre seguridad y explotación).

## Dudas o puntos pendientes

*   **Madurez del término "GovOps":** Aunque el concepto "GovOps" se exige en el temario, no es un término con una única definición certificada por ISO a fecha de la convocatoria (a diferencia de DevOps o MLOps). En el sector, a menudo se engloba dentro de las prácticas de *AI Governance as Code* o se subsume en las evaluaciones automatizadas de LLMOps. Para el examen, su núcleo definitorio es la **automatización técnica del cumplimiento normativo**.