---
id: "cm-ad-ia-p02-tema-007-gobierno-sistemas-agenticos"
title: "Gobierno de los Sistemas Agénticos"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/ia"
profiles:
  - "p02-consultor-sistemas-informacion-ia"
official_profile: "P02 - Consultor de Sistemas de Información - Especialista en Gobierno de IA"
official_topic: "Tema 7. Gobierno de los Sistemas Agénticos"
source_ids: []
tags:
  - "gobierno-ia"
  - "ia-agentica"
  - "agentes-ia"
  - "supervision-humana"
  - "hitl"
  - "trazabilidad"
  - "seguridad"
  - "multi-agente"
  - "ai-act"
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

# Gobierno de los Sistemas Agénticos

## Encaje en la convocatoria

Este tema corresponde al **Tema 7 del Anexo 3** de la Resolución 352/2026 (BOCM 11/06/2026)[cite: 1], exclusivo para el perfil **P02 (Consultor de Sistemas de Información especialista en Gobierno de IA)** de la Agencia para la Administración Digital de la Comunidad de Madrid.

Es la continuación lógica del Tema 6 (GovOps) y la aplicación jurídico-operativa de los conceptos técnicos del Tema 3 (IA Agéntica). En este perfil, el foco no está en *cómo se programa* un agente, sino en **cómo se acota su autonomía, cómo se auditan sus decisiones, cómo se aseguran sus credenciales (M2M) y cómo se implementa la supervisión humana legalmente exigida**. 

En un examen tipo test con penalización, el tribunal evaluará la capacidad del opositor para cruzar los conceptos técnicos (arquitecturas multi-agente, *prompt injection*) con las obligaciones del **Reglamento (UE) 2024/1689 (Ley de IA)** (Arts. 12 y 14) y del **Esquema Nacional de Seguridad (ENS - RD 311/2022)**. Es fundamental distinguir entre las modalidades de supervisión (HITL, HOTL, HOOTL) y no confundir la "observabilidad" técnica con la "auditoría" formal.

## Ideas clave

1.  **Diferencia Agente vs. Modelo (Brecha de Autonomía):** Un modelo de IA responde a una entrada (salida única). Un **agente de IA** percibe, planifica, invoca herramientas y ejecuta acciones múltiples sin que un humano inicie cada paso. Esta autonomía exige controles de seguridad en tiempo real.
2.  **Paradigma *Zero Trust* y Mínimo Privilegio:** Un agente no debe heredar los permisos del usuario humano. Debe operar bajo identidades técnicas (Cuentas de Servicio) con Control de Acceso Basado en Atributos (ABAC) y permisos estrictamente acotados a su función (evitando la "Agencia Excesiva", OWASP LLM08).
3.  **Trazabilidad Estructural (Art. 12 Ley IA):** El registro de actividad (*logging*) es obligatorio. En agentes, esto implica documentar cada ciclo completo: el contexto, el razonamiento (*Thought*), la llamada a la herramienta (*Action*) y el resultado (*Observation*).
4.  **Supervisión Humana Efectiva (Art. 14 Ley IA):** Obligación normativa para mitigar riesgos. Se implementa operativamente mediante **HITL** (Human-in-the-loop: el sistema requiere aprobación antes de actuar) o **HOTL** (Human-on-the-loop: el sistema actúa, pero el humano monitoriza con capacidad de parada o *Kill Switch*).
5.  **Riesgos Emergentes en Sistemas Multi-Agente:** La seguridad no escala linealmente. Múltiples agentes cooperando introducen vulnerabilidades sistémicas: colusión de agentes, cascadas de alucinaciones y herencia indebida de permisos.
6.  **Inyección Indirecta de Prompts:** El vector de ataque más crítico. Ocurre cuando el agente usa sus herramientas para leer un entorno externo (ej. un PDF) que contiene comandos maliciosos ocultos destinados a subvertir las políticas del sistema.

## Desarrollo

### 1. Fundamentos de la gobernanza de Agentes IA

La gobernanza de sistemas agénticos es el conjunto de políticas, controles técnicos (AgentOps) y mecanismos de rendición de cuentas para asegurar que los agentes autónomos operen de forma segura, trazable y alineada con la legalidad y los objetivos públicos.

*   **Actuación Administrativa Automatizada (AAA):** En España, si un agente genera actos con efectos jurídicos sin revisión humana, la Ley 40/2015 (Art. 41) exige una resolución previa que defina el sistema y el órgano responsable de su auditoría e impugnación.
*   **Las 4 Dimensiones de la Gobernanza Agéntica:**
    1.  **Control de acceso y autorización:** Principio de mínimo privilegio (RBAC/ABAC).
    2.  **Límites de comportamiento (Autonomía):** Qué puede hacer solo y qué requiere aprobación (*Guardrails*).
    3.  **Auditabilidad y trazabilidad:** Registro inmutable de la cadena de razonamiento y acción.
    4.  **Integración de datos:** Respeto a las políticas de privacidad y clasificación corporativas.

### 2. Límites de autonomía, gestión de accesos y trazabilidad

El riesgo de un agente no es solo que "se equivoque", sino que **se equivoque actuando** con impacto en el mundo real.

#### 2.1. Perímetro de Autonomía y *Guardrails*
Se deben establecer barreras lógicas:
*   **Filtros de contenido:** Sanitización de entradas y salidas.
*   **Restricción de herramientas (*Tool Gating*):** Restringir a endpoints tipificados. Aislar entornos (*Sandboxing*) cuando el agente ejecuta código o interactúa con datos externos no confiables.

#### 2.2. Gestión de Accesos (Alineación con el ENS)
*   **Identidades de Máquina:** El agente debe autenticarse de forma independiente, no con los tokens de sesión del ciudadano o funcionario.
*   **Separación Lectura/Escritura:** Las herramientas que modifican estado (escritura) requieren niveles de autorización y supervisión radicalmente distintos a las de solo lectura.

#### 2.3. Trazabilidad y Registro (Art. 12 Ley IA)
*   **Obligación:** Los sistemas de alto riesgo deben integrar registro automático desde el diseño (proveedores, Art. 12) y conservar esos registros (responsables del despliegue, Art. 26.6).
*   **Instrumentación (OpenTelemetry):** Se requiere el registro de **Trazas (*Traces*)** y **Tramos (*Spans*)** que reconstruyan la decisión: intención original, herramientas invocadas, parámetros enviados, respuesta obtenida y razonamiento intermedio.

### 3. Supervisión humana: HITL, HOTL y HOOTL

El **Artículo 14 del Reglamento (UE) 2024/1689** exige que los sistemas de IA de alto riesgo permitan una supervisión humana efectiva, dotando al operador de la capacidad de comprender, anular o detener el sistema (*Kill Switch*), mitigando el riesgo de **sesgo de automatización** (*Automation Bias*).

| Modalidad | Intervención | Nivel de Autonomía / Riesgo Adecuado | Caso de Uso en Administración |
| :--- | :--- | :--- | :--- |
| **HITL** (*Human-in-the-loop*) | Síncrona. La inacción humana detiene el proceso. Se requiere validación previa a la acción. | Riesgo Alto. Acciones irreversibles o con impacto jurídico. | El agente redacta una resolución; el funcionario la revisa, firma y envía. |
| **HOTL** (*Human-on-the-loop*) | Asíncrona. El sistema avanza, el humano vigila y puede abortar o corregir (*Override*). | Riesgo Medio. Tareas masivas bajo umbrales de seguridad. | Clasificación preliminar de alertas de red o incidencias. |
| **HOOTL** (*Human-out-of-the-loop*) | Nula en operación ordinaria. Solo auditoría *ex-post*. | Riesgo Bajo. Acciones triviales, reversibles y acotadas. | Etiquetado automático de documentos internos para el buscador. |

*   **Falsa Supervisión (Riesgo de Examen):** Una supervisión donde el humano se limita a hacer clic en "Aceptar" por falta de tiempo, formación o interfaz opaca, no cumple la exigencia de "supervisión efectiva" del AI Act.

### 4. Alineación y seguridad en sistemas multi-agente

Los Sistemas Multi-Agente (MAS) introducen complejidades sistémicas donde los riesgos no se suman, sino que interactúan y emergen.

#### 4.1. Riesgos Específicos de la Coordinación Agéntica
*   **Colusión de Agentes:** Dos agentes (ej. un generador y un auditor) cooperan anómalamente para eludir las reglas de seguridad o dar por válida una alucinación (Falso Consenso).
*   **Herencia de Permisos / Escalada de Privilegios:** Un agente con bajos permisos delega una tarea en un subagente con permisos críticos de forma no autorizada (*Confused Deputy*).
*   **Cascada de Errores:** Un error factual o alucinación de un agente inicial se asume como "verdad absoluta" por los siguientes agentes de la cadena.
*   **Propagación de Datos (Fuga):** Datos confidenciales manejados por el Agente A se filtran al Agente B, que los expone o almacena indebidamente.

#### 4.2. Controles Multi-Agente
*   **Orquestación Gobernada:** Un componente central aplica las políticas de control; la coordinación no se deja enteramente al criterio de los LLMs.
*   **Compartimentación de Memoria y Contexto:** Aplicación del principio de *Need-to-Know*.
*   **Contratos de Interacción (A2A):** Definición estricta de qué puede pedir cada agente a otro y en qué formato.

### 5. Vulnerabilidades Críticas de Seguridad (OWASP Top 10 LLMs)

Para el gobierno de agentes, dos vulnerabilidades destacan sobre el resto:
1.  **Agencia Excesiva (LLM08 - *Excessive Agency*):** Otorgar a un agente autonomía, herramientas o permisos que exceden lo estrictamente necesario (violación del mínimo privilegio).
2.  **Inyección Indirecta de Prompts (*Indirect Prompt Injection*):** El vector de ataque principal. Ocurre cuando el agente consume fuentes externas no confiables (una web, un PDF de un ciudadano). El atacante esconde comandos en ese documento; el agente los lee, los asimila como instrucciones legítimas (debido a la dificultad del LLM para separar datos de instrucciones) y ejecuta acciones maliciosas usando sus herramientas. *Mitigación:* Sandboxing, sanitización estricta, y HITL para acciones derivadas de datos externos.

## Conceptos que suelen preguntarse

| Concepto a distinguir | Realidad Técnica y de Gobierno | Trampa de examen |
| :--- | :--- | :--- |
| **Observabilidad vs. Monitorización** | Monitorización vigila (alertas, CPU). Observabilidad entiende causas (trazas, razonamiento de caja negra). | "Tener un dashboard de CPU garantiza la observabilidad del agente". |
| **HITL vs. HOTL** | HITL: Intervención *antes* de la acción. HOTL: Monitorización *durante* (capacidad de parada). | "En HOTL, el sistema no avanza si el humano no aprueba cada paso". |
| **Herramienta (Tool Calling) vs. Acción** | Herramienta es la capacidad (API). Acción es su ejecución. El orquestador (código) valida y ejecuta, no el LLM directamente. | "El LLM ejecuta comandos SQL directamente en la base de datos". |
| **Inyección Indirecta de Prompts** | El ataque entra por los datos leídos por las herramientas del agente (ej. un PDF escaneado). | "Solo ocurre cuando el administrador escribe mal el System Prompt". |
| **Supervisión Humana vs. Logs** | Art. 14 (Supervisión) es intervención humana. Art. 12 (Logs) es trazabilidad técnica. | "Guardar logs en disco sustituye la obligación legal de supervisión humana". |

## Posibles preguntas tipo test

**Pregunta 1.** Desde la perspectiva del gobierno de la IA, si la Agencia para la Administración Digital despliega un agente autónomo encargado de tramitar expedientes, ¿cuál de las siguientes vulnerabilidades operativas (clasificadas en OWASP) representa el riesgo de que el agente lea un documento adjunto por un ciudadano que contiene instrucciones ocultas diseñadas para tomar el control del flujo de decisiones del sistema?
A. Evasión de modelo (*Model Evasion*).
B. Agencia Excesiva (*Excessive Agency*).
C. Inyección indirecta de prompts (*Indirect Prompt Injection*).
D. Envenenamiento de datos de entrenamiento (*Data Poisoning*).
**Respuesta correcta: C.** (La inyección indirecta explota la capacidad del agente de interactuar con el entorno y consumir datos externos no confiables).

**Pregunta 2.** De acuerdo con el Reglamento (UE) 2024/1689 (Ley de IA), ¿qué objetivo primordial justifica la imposición del requisito de "Supervisión Humana" (Art. 14) en los sistemas de IA de alto riesgo?
A. Reducir los costes operativos de almacenamiento de logs en el proveedor cloud.
B. Reemplazar la necesidad de elaborar documentación técnica exigida por el Marcado CE.
C. Prevenir o reducir al mínimo los riesgos para la salud, la seguridad o los derechos fundamentales mediante la intervención efectiva y proporcionada de personas físicas.
D. Asegurar el reentrenamiento automático del modelo (*Continuous Training*) basado en el *feedback* implícito del usuario.
**Respuesta correcta: C.** (Literalidad del Art. 14, orientado a la mitigación del riesgo residual y prevención del daño).

**Pregunta 3.** Al diseñar la gobernanza de un sistema multi-agente en una Administración Pública, se decide que el agente no ejecutará ninguna notificación formal con efectos jurídicos hasta que un empleado público haya revisado el borrador, validado las fuentes y pulsado explícitamente el botón de "Aprobar y Enviar", deteniéndose el flujo hasta que esto ocurra. Este modelo de supervisión se denomina:
A. Human-out-of-the-loop (HOOTL).
B. Human-on-the-loop (HOTL).
C. Human-in-the-loop (HITL).
D. Role-Based Access Control (RBAC).
**Respuesta correcta: C.** (La intervención síncrona que condiciona y precede a la ejecución de la acción define el paradigma HITL).

**Pregunta 4.** En relación con el control de accesos y la seguridad de un agente de IA que interactúa con bases de datos del sector público, ¿cuál de las siguientes prácticas representa una violación del principio de "mínimo privilegio" y un riesgo grave de gobernanza?
A. Exigir que las acciones irreversibles requieran la validación por un segundo factor o supervisor.
B. Aislar las herramientas de ejecución de código en entornos restringidos (*Sandboxing*).
C. Permitir que el agente herede dinámicamente todos los permisos del usuario logueado o utilice credenciales genéricas de administrador para facilitar sus conexiones API.
D. Restringir la disponibilidad de las herramientas en función de la tarea específica planificada por el orquestador.
**Respuesta correcta: C.** (El agente debe operar con una identidad técnica propia y permisos estrictamente acotados; heredar privilegios globales favorece ataques de *Confused Deputy* o escalada de privilegios).

**Pregunta 5.** El Artículo 12 de la Ley de Inteligencia Artificial exige que los sistemas de alto riesgo garanticen capacidades técnicas de registro de eventos (*logging*). En la arquitectura de sistemas agénticos, ¿qué mecanismo técnico proporciona la profundidad necesaria para reconstruir el razonamiento algorítmico y auditar el cumplimiento legal?
A. El ajuste de la métrica de Perplejidad del modelo base.
B. El truncamiento morfológico (*Stemming*) de los archivos de base de datos.
C. La monitorización exclusiva del uso de CPU y memoria RAM del clúster de Kubernetes.
D. La instrumentación de telemetría estructurada en Trazas (*Traces*) y Tramos (*Spans*), capturando el estado del prompt, las herramientas invocadas y el razonamiento intermedio en cada iteración.
**Respuesta correcta: D.** (Las trazas distribuidas son la materialización de la observabilidad y auditabilidad exigida normativamente a los sistemas de caja negra que toman decisiones secuenciales).

## Normativa o fuentes relacionadas

*   **Reglamento (UE) 2024/1689 (Ley de IA):**
    *   Art. 12: Conservación de registros (Trazabilidad estructural).
    *   Art. 14: Supervisión humana (HITL, prevención del sesgo de automatización).
    *   Art. 26: Obligaciones de los responsables del despliegue (Retención de logs por mínimo 6 meses).
*   **Real Decreto 311/2022 (Esquema Nacional de Seguridad):** Medidas de control de acceso (mínimo privilegio), segregación de funciones e identidad técnica para sistemas automatizados.
*   **Ley 40/2015, de Régimen Jurídico del Sector Público:** Art. 41 (Actuación administrativa automatizada), fundamental para enmarcar la legalidad de la autonomía agéntica.
*   **NIST AI 600-1 (Generative AI Profile):** Extensión del AI RMF enfocada a riesgos de modelos generativos, autonomía y ataques (Inyecciones).
*   **OWASP Top 10 for LLM Applications:** Vulnerabilidades críticas como LLM01 (*Prompt Injection* indirecta) y LLM08 (*Excessive Agency*).

## Dudas o puntos pendientes

*   **"IA Agéntica" vs. "Sistema de IA" (Reglamentación):** Es importante recordar que el AI Act no reconoce la "IA Agéntica" como una categoría jurídica especial con artículos propios. Legalmente es un "Sistema de IA". Las exigencias de trazabilidad, gobernanza y supervisión humana del Reglamento se aplican en función de su **clasificación de riesgo (ej. Alto Riesgo)**, impacto y contexto de uso, no por el hecho tecnológico de estar etiquetado comercialmente como "agente".