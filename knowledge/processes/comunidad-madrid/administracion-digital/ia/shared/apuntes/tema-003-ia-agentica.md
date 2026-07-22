---
id: "cm-ad-ia-tema-003-ia-agentica"
title: "IA Agéntica"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/ia"
profiles:
  - "p01-consultor-sistemas-informacion-ia"
  - "p02-consultor-sistemas-informacion-gobierno-ia"
official_profiles:
  - "P01 - Consultor de Sistemas de Información - IA Aplicada al Ciclo de Vida del Software"
  - "P02 - Consultor de Sistemas de Información - Gobierno de IA"
official_topic: "Tema 3. IA Agéntica"
source_ids:
tags:
  - "inteligencia-artificial"
  - "ia-generativa"
  - "ia-agentica"
  - "agentes-ia"
  - "gobierno-ia"
  - "observabilidad"
  - "prompt-engineering"
  - "agentops"
  - "trazabilidad"
  - "seguridad-ia"
created_at: "2026-07-17"
last_reviewed: null
ai_generated: true
ai_sources:
  - "chatgpt"
  - "perplexity"
  - "gemini"
needs_human_review: true
---

# IA Agéntica

## Encaje en la convocatoria

Este tema corresponde al **Tema 3 del Anexo 3** de la Resolución 352/2026 (BOCM 11/06/2026), dentro de las áreas de conocimiento del Bloque 1 de la Fase 1 de oposición, común a los perfiles **P01: Consultor de Sistemas de Información - IA Aplicada al Ciclo de Vida del Software** y **P02: Consultor de Sistemas de Información - Especialista en Gobierno de IA** de la Agencia para la Administración Digital de la Comunidad de Madrid.

Aunque la “IA agéntica” no aparece como categoría explícita en el Reglamento (UE) 2024/1689 (Ley de IA), los sistemas agénticos se consideran **sistemas de IA** y, cuando son de alto riesgo, están sujetos a obligaciones de gestión de riesgos, supervisión humana significativa, registro de eventos y trazabilidad (Arts. 9, 12 y 14), además de los principios del Esquema Nacional de Seguridad (ENS) en España. Es importante distinguir en examen entre la **observabilidad técnica** de AgentOps y el **registro de eventos** exigido legalmente, así como diferenciar el *prompt* como artefacto de configuración y control (*System Prompt*) frente a simples entradas de usuario.

## Ideas clave

1. **Agente de IA vs LLM:** Un LLM genera texto, código u otras salidas estadísticas. Un **agente de IA** es una arquitectura de software que usa el LLM como motor de razonamiento dentro de un bucle de percepción, planificación y ejecución de acciones mediante herramientas, para perseguir objetivos y modificar su entorno.
2. **ReAct Framework:** Paradigma fundamental que unifica razonamiento (*Chain‑of‑Thought*) con acción (*Function Calling*) mediante la secuencia iterativa **Thought → Action → Observation**, base de muchas arquitecturas agénticas modernas.
3. **Ejecución de herramientas (Function Calling):** El LLM no ejecuta código ni APIs; emite una salida estructurada (normalmente JSON) donde decide qué herramienta usar y con qué parámetros, y el orquestador (código tradicional) valida y ejecuta la llamada.
4. **Riesgo y autonomía:** Cuanta más autonomía y más herramientas externas puede usar el agente (APIs, RAG, bases de datos), mayor es la superficie de ataque y más críticas son la gestión de identidades y privilegios, arquitecturas *Zero Trust*, trazabilidad y supervisión humana.
5. **Observabilidad (trazabilidad estructural):** En sistemas agénticos, la observabilidad se basa en **traces y spans** siguiendo convenciones de OpenTelemetry, registrando el razonamiento, las acciones y las observaciones paso a paso; esto va más allá de la monitorización clásica de estado.
6. **Cumplimiento legal (Art. 12 AI Act):** Para sistemas de alto riesgo, la observabilidad es la implementación técnica del registro automático de acontecimientos exigido por el AI Act, y se vincula con la supervisión humana del Art. 14.
7. **Prompt engineering en gobierno:** Diseñar y versionar el *System Prompt* como código fuente crítico que actúa como **guardrail**, definiendo el rol del agente, qué puede hacer, qué herramientas puede usar y cuándo debe escalar al humano.
8. **Inyección indirecta de prompts:** Vulnerabilidad crítica (OWASP LLM01/Top 10 Agentic) donde el agente, a través de sus herramientas, lee contenido externo infectado con comandos ocultos que subvierten sus reglas operativas.
9. **AgentOps:** Extensión operativa de MLOps/LLMOps centrada en gobernar el ciclo de vida de las trayectorias de decisión de agentes, control de bucles, evaluación dinámica (Task Success Rate, Trajectory Score), costes por interacción y supervisión humana.

## Desarrollo

### 1. Concepto de agente: tipos, componentes e integración

Un **agente de IA** es un sistema que percibe su contexto (inputs, memoria, entorno), razona utilizando un modelo fundacional (LLM u otros) y ejecuta acciones secuenciales de forma autónoma o semiautónoma mediante herramientas externas, para alcanzar un objetivo definido y reevaluar el estado tras cada acción.

#### 1.1. Chatbot, RAG y agente

- **Chatbot:** interfaz conversacional reactiva; responde a entradas de usuario sin planificar acciones externas ni mantener objetivos a largo plazo.
- **RAG:** patrón que recupera información de una base de conocimiento y la inyecta en el contexto para generar respuestas más fundamentadas, pero sin ejecutar acciones en sistemas externos.
- **Agente de IA:** decide qué pasos dar, invoca herramientas (APIs, RAG, bases de datos, servicios de ticketing) y reevalúa el estado tras cada acción, pudiendo interactuar con múltiples sistemas corporativos.

#### 1.2. Arquitecturas: agente único y sistemas multi‑agente

- **Agente único (single‑agent):** un solo agente central con un System Prompt que orquesta planificación y herramientas dentro de un mismo bucle de contexto. Riesgos: desviación de objetivo (*prompt drift*), acoplamiento de responsabilidades y dificultad para aplicar segregación de funciones.
- **Sistemas multi‑agente (MAS):** varios agentes con System Prompts diferenciados y roles especializados (supervisor, redactor, auditor, ejecutor) que colaboran o delegan tareas.
  - Ventajas: modularidad, separación de responsabilidades, posibilidad de que un agente audite a otro.
  - Riesgos: colusión entre agentes, latencias mayores, costes y complejidad de observabilidad, propagación en cascada de errores (relacionado con OWASP Agentic “Cascading Failures”).

#### 1.3. Componentes críticos

1. **Modelo (brain/core):** LLM u otro modelo fundacional que genera razonamientos, planes y decisiones.
2. **Memoria:**
   - **Corto plazo:** historial de conversación y razones dentro de la ventana de contexto; se destruye al cerrar sesión.
   - **Largo plazo:** almacenamiento persistente (bases vectoriales, BBDD) que conserva datos de casos, decisiones y estados pasados; exige políticas RGPD (minimización, retención, derecho de supresión).
3. **Herramientas (tools/plugins):**
   - Interfaces hacia sistemas externos (APIs, RAG, servicios de correo, bases de datos), definidas mediante esquemas (JSON Schema u otros).
   - Vector de riesgo principal (Identity & Privilege Abuse, OWASP AS103): requieren identidad de máquina, mínimo privilegio, segmentación y validación de parámetros por el orquestador.
4. **Planificación:**
   - Descomposición del objetivo en subtareas.
   - Reflexión sobre resultados (Reflexion) para corregir estrategias y adaptarse.
5. **Orquestador / harness:**
   - Código que gestiona el ciclo de vida del agente: inicialización, llamadas al modelo, llamadas a herramientas, gestión de errores, timeouts, límites de pasos y puntos HITL.

#### 1.4. Protocolos emergentes (MCP, Agent‑to‑Agent)

- **MCP (Model Context Protocol):** protocolo para describir y exponer herramientas, datos y capacidades disponibles a un modelo o agente de forma estándar, permitiendo descubrir y consumir recursos locales y remotos de forma segura.
- **Agent‑to‑Agent (A2A):** patrones de comunicación y coordinación entre agentes, relevantes en ecosistemas multi‑agente donde se delegan tareas o se coordina información.

### 2. Observabilidad en agentes

La ejecución de un agente no es un flujo de código determinista, sino una secuencia de decisiones estadísticamente guiadas por el modelo. La **observabilidad** busca reconstruir qué hizo el agente y por qué, a través de trazas de telemetría estructuradas.

#### 2.1. Traces y spans (OpenTelemetry)

OpenTelemetry define convenciones semánticas para instrumentar aplicaciones, incluida IA generativa y agéntica:

- **Trace (traza):** representa el recorrido completo de una solicitud o tarea end‑to‑end (por ejemplo, una interacción completa con un asistente agéntico).
- **Span (tramo):** unidad de trabajo dentro de la traza (llamada al LLM, invocación a una herramienta, paso de pipeline) con sus propias etiquetas (prompt, parámetros, respuesta).

Todos los spans asociados a una misma ejecución comparten el mismo trace_id y pueden organizarse en jerarquía padre‑hijo, permitiendo reconstruir el árbol de decisiones del agente.

#### 2.2. Monitorización, observabilidad y auditoría

| Concepto         | Finalidad                                                          |
| :--------------- | :----------------------------------------------------------------- |
| Monitorización   | Vigilar métricas y alertas (latencia, errores, consumo recursos).  |
| Observabilidad   | Entender flujos internos y decisiones vía traces/spans.           |
| Auditoría        | Revisar y documentar cumplimiento normativo a partir de registros.|

Monitorizar responde a “¿está funcionando?”, observabilidad a “¿qué hizo y por qué?”, auditoría a “¿cumplió las políticas y obligaciones legales?”.

#### 2.3. Métricas específicas

- Consumo total de tokens por tarea y por agente.
- Latencia por llamada y latencia end‑to‑end.
- Tasa de uso y fallo de herramientas (por ejemplo, porcentaje de llamadas que generan errores o resultados inválidos).
- Detección de bucles infinitos de herramientas (tool loops), con mecanismos de corte (timeouts, límites de pasos).

#### 2.4. Exigencia normativa

El **Art. 12 del AI Act** exige que los sistemas de alto riesgo dispongan de registro automático de acontecimientos para garantizar trazabilidad, lo que en arquitecturas agénticas se implementa mediante telemetría estructurada (traces, spans, logs enriquecidos) integrada en sistemas de registro y auditoría.

### 3. Prompt engineering en agentes y gobierno

El **prompt engineering** deja de ser simplemente “pedir bien las cosas” y pasa a ser diseño de artefactos de configuración críticos:

- El **System Prompt** define el rol del agente, sus límites, sus herramientas, sus obligaciones normativas y su relación con el usuario.
- Debe versionarse, revisarse y auditarse como código fuente, porque un cambio en el System Prompt puede alterar radicalmente el perfil de riesgo.

#### 3.1. Estructura de prompts

- **System Prompt:** instrucciones persistentes de máxima prioridad (rol, tono, políticas de seguridad, requisitos de cita de fuentes, reglas de escalado a humano).
- **User Prompt:** entrada del usuario, que debe ser subordinada al System Prompt (no puede sobreescribirlo).

#### 3.2. Técnicas

- Zero‑shot / Few‑shot: incluir ejemplos de tareas y salidas correctas antes de la consulta.
- Chain‑of‑Thought (CoT): pedir razonamiento paso a paso para ganar explicabilidad.
- ReAct: estructurar el bucle en Thought → Action → Observation, explicitando las decisiones del agente.

#### 3.3. Prompt injection

- **Directa (jailbreaking):** instrucciones maliciosas en el prompt de usuario que intentan ignorar el System Prompt.
- **Indirecta:** el agente usa una herramienta para leer contenido externo (web, PDF, email, repositorio) que contiene comandos ocultos y los trata como instrucciones legítimas.

OWASP LLM01 identifica la *prompt injection* como riesgo crítico en aplicaciones LLM, y OWASP Top 10 Agentic extiende este riesgo a ecosistemas de agentes, enfatizando el peligro de instrucciones ocultas en datos de entrada.

### 4. AgentOps

**AgentOps** es la disciplina que aplica principios de MLOps y LLMOps a sistemas agénticos, gestionando su ciclo de vida operativo (configuración, despliegue, monitorización, evaluación, supervisión humana y seguridad).

#### 4.1. Comparación con MLOps y LLMOps

- **MLOps:** reentrenamiento, despliegue y monitorización de modelos ML supervisados/no supervisados, centrado en métricas como Accuracy y F1.
- **LLMOps:** gestión de modelos fundacionales, prompting, RAG, evaluación de toxicidad, groundedness y coste por token.
- **AgentOps:** añade gestión de bucles de decisión, permisos de herramientas, puntos HITL, límites de consumo y evaluación de trayectorias.

#### 4.2. Funciones principales

- Versionado de System Prompts, herramientas y configuraciones de agente.
- Evaluación dinámica:
  - **Task Success Rate:** porcentaje de tareas en que el agente alcanza el objetivo correcto.
  - **Trajectory Score:** calidad de los pasos intermedios (seguridad, eficiencia, cumplimiento de políticas).
- Gestión de autonomía:
  - Control del **action space** (conjunto de herramientas y permisos).
  - Configuración de niveles de autonomía supervisada, semiautónoma y autónoma.
- Supervisión humana (HITL y HOTA – Human‑Over‑The‑Agent):
  - Puntos de control donde el agente requiere aprobación humana para acciones sensibles.
  - Métricas como override rate (tasa de correcciones humanas) para medir efectividad de la supervisión.

#### 4.3. Controles de seguridad

- Guardrails de entrada y salida.
- Identity & Privilege Management (IAM) específico para agentes (evitar “vacío de atribución” descrito por OWASP Agentic AS103).
- Observabilidad avanzada (traces/spans).
- Gestión de límites de consumo (tokens, llamadas a API, costes).

## Conceptos que suelen preguntarse (Trampas comunes)

| Concepto                         | Realidad técnica / jurídica                                                 | Distractor típico en examen                                |
| :------------------------------- | :--------------------------------------------------------------------------- | :--------------------------------------------------------- |
| Agente vs chatbot                | El agente decide y ejecuta acciones; el chatbot solo conversa.             | “Todo chatbot LLM es automáticamente un agente de IA”.     |
| CoT vs ReAct                     | CoT es razonamiento interno; ReAct intercala acciones externas.            | “CoT y ReAct son sinónimos y siempre llaman a APIs”.       |
| Memoria vs ventana de contexto   | Memoria = almacenamiento persistente; ventana de contexto = tokens por llamada.| “Aumentar contexto crea memoria persistente infinita”.  |
| LLM vs herramienta               | El LLM propone; la herramienta (API) es ejecutada por el orquestador.      | “El modelo LLM ejecuta directamente SQL o comandos shell”. |
| Prompt injection indirecta       | Viene de datos externos consumidos por herramientas del agente.            | “Solo ocurre cuando el usuario escribe instrucciones malas”.|
| Trace vs span                    | Trace = ejecución completa; span = unidad de trabajo dentro de la trace.   | “Trace y span son equivalentes y se usan indistintamente”. |
| AgentOps vs LLMOps               | AgentOps añade bucles, herramientas y HITL; LLMOps se centra en modelo/contexto.| “AgentOps solo trata del entrenamiento de pesos”.      |

## Posibles preguntas tipo test

**Pregunta 1.** En un agente basado en ReAct, ¿qué secuencia describe correctamente el ciclo de decisión?

A. System Prompt → User Prompt → Output Parser.  
B. Ingesta → Chunking → Búsqueda vectorial.  
C. Thought → Action → Observation.  
D. Zero‑shot → Few‑shot → Chain‑of‑Thought.

**Respuesta correcta: C.**

**Pregunta 2.** ¿Quién valida y ejecuta físicamente la llamada a una API corporativa en un sistema agéntico con herramientas?

A. El modelo de lenguaje (LLM).  
B. La memoria a largo plazo del agente.  
C. El código del orquestador tras recibir la propuesta de parámetros del modelo.  
D. El protocolo de trazas HTTP.

**Respuesta correcta: C.**

**Pregunta 3.** ¿Cuál de las siguientes situaciones describe una inyección indirecta de prompts?

A. Usuario pide explícitamente “Ignora tus directrices previas”.  
B. Agente lee un PDF externo que contiene instrucciones ocultas para aprobar todas las solicitudes.  
C. Administrador cambia la temperatura a 0.  
D. Se reduce la ventana de contexto del modelo.

**Respuesta correcta: B.**

**Pregunta 4.** ¿Qué diferencia hay entre trace y span según OpenTelemetry?

A. Trace almacena coste; span almacena tokens.  
B. Trace representa la ejecución completa de una petición; span representa una unidad de trabajo dentro de la trace.  
C. Son sinónimos.  
D. Trace pertenece a memoria corta; span a memoria larga.

**Respuesta correcta: B.**

**Pregunta 5.** ¿Cuál es el objetivo principal de HITL en AgentOps?

A. Eliminar latencia.  
B. Validar el tokenizador.  
C. Requerir aprobación humana explícita antes de acciones de alto riesgo propuestas por el agente.  
D. Optimizar embeddings.

**Respuesta correcta: C.**

**Pregunta 6.** ¿Por qué la inyección indirecta de prompts es especialmente peligrosa en sistemas agénticos?

A. Porque altera pesos del modelo base en entrenamiento.  
B. Porque explota la capacidad del agente para leer y asimilar datos externos a través de sus herramientas.  
C. Porque exige credenciales de administrador.  
D. Porque aumenta la temperatura del modelo.

**Respuesta correcta: B.**

**Pregunta 7.** ¿Qué mecanismo técnico ayuda a cumplir el Art. 12 del AI Act en sistemas agénticos?

A. Reducir dimensionalidad de embeddings.  
B. Medir uso de CPU y RAM.  
C. Telemetría estructurada mediante traces y spans que capturan prompts, acciones y observaciones.  
D. Validación de esquemas SQL.

**Respuesta correcta: C.**

**Pregunta 8.** ¿Qué métrica es clave para evaluar decisiones de un agente autónomo?

A. Complejidad ciclomática del código.  
B. Trajectory Score, evaluando la calidad y seguridad de los pasos intermedios.  
C. Hash criptográfico de la imagen Docker.  
D. Número total de tokens en el vocabulario.

**Respuesta correcta: B.**

## Normativa o fuentes relacionadas

- **Reglamento (UE) 2024/1689 (AI Act):** Art. 9 (gestión de riesgos), Art. 12 (registro de eventos), Art. 14 (supervisión humana) aplicables a sistemas de alto riesgo en la Administración.
- **Real Decreto 311/2022 (ENS):** principios básicos y requisitos mínimos de seguridad (procesos integrales, gestión basada en riesgos, registro de actividad, control de acceso, mínimo privilegio).  
- **OWASP Top 10 for LLM Applications 2025 y OWASP Top 10 for Agentic Applications:** catálogos de riesgos y mitigaciones para aplicaciones LLM y agénticas (Prompt Injection, Sensitive Information Disclosure, Identity & Privilege Abuse, Cascading Failures, Excessive Agency).
- **NIST AI RMF 1.0 y NIST AI 600‑1 (Generative AI Profile):** marco de gestión de riesgos de IA, con perfil específico para IA generativa y agentes.
- **OpenTelemetry Semantic Conventions for GenAI/Agentic:** estándar de facto para instrumentación de trazas, spans y métricas en aplicaciones de IA.

## Dudas o puntos pendientes

- La terminología “IA agéntica”, “AgentOps”, “ReAct”, “MCP”, “A2A” pertenece a la práctica industrial y no está fijada en normas ISO/IEC; el AI Act regula sistemas de IA en función de su **uso y riesgo**, independientemente de etiquetas comerciales.
- La integración de agentes en arquitecturas ENS exige aplicar principios de seguridad integral, prevención, detección, respuesta y conservación, aunque el ENS no mencione explícitamente “prompts” o “agentes”; los controles de validación de entrada, registro de actividad y control de acceso son la base técnica para mitigar riesgos agénticos.