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

La prueba consta de **45 preguntas tipo test (+5 de reserva)**, con **penalización de -0,25 puntos por error**. El contenido base (arquitecturas de agentes, componentes, observabilidad, prompt engineering y AgentOps) es común, pero el enfoque de estudio difiere: para **P01** el énfasis recae en la precisión técnica de la implementación (ReAct, *Function Calling*, tipos de memoria), mientras que para **P02** el estudio se traslada a **cómo controlar la autonomía, auditar la trayectoria de decisiones, gestionar los riesgos de seguridad (OWASP) y garantizar el cumplimiento normativo (AI Act y ENS)**.

A nivel normativo, aunque la "IA Agéntica" no es una categoría estricta en el Reglamento (UE) 2024/1689 (Ley de IA), los sistemas agénticos están sujetos a las obligaciones de trazabilidad, gestión de riesgos, supervisión humana (HITL) y registro de logs (Art. 12), especialmente en casos de alto riesgo. En un examen tipo test, es crucial distinguir entre la "observabilidad" técnica de *AgentOps* y el "registro de eventos" (*logging*) como obligación legal, así como diferenciar un *Prompt* como instrucción de código frente a un *Prompt* como mecanismo de control lógico (*Guardrail*).

## Ideas clave

1. **Agente de IA vs. LLM:** Un LLM genera salidas estadísticas (texto, código). Un **Agente de IA** es una arquitectura de software que *usa* el LLM como motor de razonamiento dentro de un bucle de percepción, planificación y ejecución de acciones autónomas mediante herramientas, para perseguir objetivos y modificar su entorno.
2. **ReAct Framework:** Paradigma fundamental en IA agéntica que unifica el razonamiento lógico (*Chain-of-Thought*) con la acción práctica (*Function Calling*) mediante la secuencia iterativa: *Thought → Action → Observation*.
3. **Ejecución de herramientas (Function Calling):** El LLM **no ejecuta** código ni herramientas externas; emite una salida estructurada (típicamente JSON) decidiendo qué herramienta usar y con qué parámetros. El *framework* subyacente (orquestador, código tradicional) es quien invoca la API, valida los parámetros y devuelve la observación al modelo.
4. **Riesgo y Autonomía:** A mayor autonomía y capacidad de uso de herramientas externas (ej. consultar un expediente real), mayor es la superficie de ataque y la necesidad de **mínimo privilegio (ABAC/RBAC)**, arquitecturas *Zero Trust*, trazabilidad y supervisión humana (*Human-in-the-loop*).
5. **Observabilidad (Trazabilidad Estructural):** En sistemas agénticos, la observabilidad se basa en **Trazas (Traces)** y **Tramos (Spans)**, siguiendo las convenciones de OpenTelemetry, que documentan paso a paso el razonamiento (*Thought*) y la acción (*Action*) del agente. Es distinta de la Monitorización clásica (vigilar estado y alertas) y de la Auditoría legal (revisión formal con evidencias).
6. **Cumplimiento Legal (Art. 12 AI Act):** Para sistemas de alto riesgo, la observabilidad es la implementación técnica del **registro automático de acontecimientos (logging)** exigido por el Reglamento (UE) 2024/1689, junto con la supervisión humana del Art. 14.
7. **Prompt Engineering en Gobierno:** No es "hablar con la IA". Es la disciplina de diseñar y versionar instrucciones (*System Prompt*) como código fuente crítico, que actúan como barreras de seguridad (*Guardrails*), definiendo qué herramientas puede usar el agente y bajo qué condiciones debe detenerse o escalar al humano.
8. **Inyección Indirecta de Prompts:** Es la vulnerabilidad más crítica en IA Agéntica (OWASP Top 10 LLM, LLM01). Ocurre cuando el agente, usando sus herramientas, lee un documento o fuente externa infectada con comandos ocultos que subvierten sus reglas operativas originales.
9. **AgentOps:** Es la extensión operativa de MLOps/LLMOps. Se centra en gobernar el ciclo de vida de las trayectorias de decisión autónomas: control de bucles infinitos, evaluación dinámica (Tasa de éxito de tareas, *Trajectory Score*), gestión del coste por interacciones complejas y supervisión humana (HITL).

## Desarrollo

### 1. Concepto de agente: tipos, componentes e integración

**Agente de IA:** Sistema que percibe su contexto, razona utilizando un modelo fundacional (LLM) y ejecuta acciones secuenciales de forma autónoma o semiautónoma mediante el uso de herramientas externas para alcanzar un objetivo definido, reevaluando el estado tras cada acción.

#### 1.1. Diferencia entre Chatbot, RAG y Agente

* **Chatbot:** Interacción conversacional reactiva. Baja autonomía.
* **RAG (Generación Aumentada por Recuperación):** Recupera información y la aporta al contexto. No planifica acciones ni modifica su entorno.
* **Agente IA:** Decide interactivamente qué pasos dar, invoca herramientas (APIs, bases de datos) y reevalúa el estado tras cada acción.

#### 1.2. Tipos de Arquitecturas (Perspectiva técnica y de Gobierno)

* **Agente Único (Single-Agent):** Un solo modelo orquesta la planificación y las herramientas en un mismo bucle de contexto. *Riesgo:* desviación del objetivo (*Prompt Drift*) en tareas largas y dificultad para aplicar el principio de segregación de funciones.
* **Sistemas Multi-Agente (Multi-Agent Systems - MAS):** Múltiples agentes con *System Prompts* aislados y roles especializados que colaboran o delegan (ej. patrón Supervisor o Manager-Worker; un agente redacta, un agente auditor revisa normativamente, un agente orquestador dirige).
  * *Ventaja:* Mejora el control y la modularidad.
  * *Riesgo:* **Colusión de agentes** (cooperación anómala para eludir seguridad), aumento de latencia, coste, complejidad de la observabilidad y propagación en cascada de errores.

#### 1.3. Componentes Críticos (Foco de Auditoría)

1. **Modelo (Brain/Core):** El LLM base con capacidad de razonamiento estructurado.
2. **Memoria:**
   * *A corto plazo (Short-term Memory):* El historial acumulado dentro de la ventana de contexto en una sesión activa (*In-Context Learning*); desaparece al finalizar la sesión.
   * *A largo plazo (Long-term Memory):* Almacenamiento persistente externo (ej. bases de datos vectoriales) que permite recuperar contextos históricos por similitud semántica. *Implicación RGPD:* almacenar datos personales de ciudadanos en la memoria de un agente exige políticas estrictas de retención, minimización y mecanismos para el **Derecho de Supresión (Art. 17 RGPD)**.
3. **Herramientas (Tools/Plugins/Function Calling):** Interfaces hacia sistemas externos (APIs, RAG, *sandboxes* de código), definidas mediante esquemas (JSON Schema). Constituyen el mayor vector de riesgo (OWASP LLM07): exigen arquitecturas *Zero Trust*, identidad de máquina con privilegios mínimos, y la validación final de los parámetros la ejecuta el orquestador (código tradicional), nunca el LLM.
4. **Planificación (Planning):**
   * *Descomposición:* partir un problema en subtareas lógicas.
   * *Reflexión (Reflexion):* autocrítica tras observar el resultado de una acción, para iterar o corregir la estrategia.
5. **Orquestación:** El marco de control lógico (ej. LangGraph) que rige el flujo, aplica *timeouts* y define cuándo detener el bucle o requerir aprobación humana (HITL).

#### 1.4. Integración y Protocolos Emergentes

* **MCP (Model Context Protocol):** Estándar abierto para conectar de forma segura agentes/modelos con fuentes de datos externas y herramientas locales, estandarizando la exposición de recursos.
* **A2A (Agent2Agent Protocol):** Orientado a la interoperabilidad, descubrimiento, comunicación y delegación de tareas entre distintos agentes, útil en despliegues distribuidos.

### 2. Observabilidad en agentes

La naturaleza no determinista de los LLMs impide la depuración de software tradicional (APM), donde la ruta del código está predefinida. En IA Agéntica, el flujo de control es probabilístico y lo decide el LLM en tiempo real. La observabilidad es esencial para auditar *por qué* el agente tomó una decisión.

#### 2.1. Trazas y Tramos (Traces and Spans) — Telemetría y OpenTelemetry

Basado en las convenciones semánticas de **OpenTelemetry para IA Generativa**:
* **Traza (Trace):** Reconstrucción del recorrido completo de una petición del usuario de extremo a extremo (ej. `solicitud-123`).
* **Tramo (Span):** Subdivisión atómica/temporal de una unidad de trabajo discreta dentro de la traza (ej. llamada de inferencia al LLM, invocación de la API de creación de tickets, búsqueda vectorial). Captura: el estado del prompt enviado, el razonamiento intermedio, la invocación de la herramienta (parámetros) y la respuesta de la herramienta (*Observation*).

#### 2.2. Diferenciación Conceptual de Examen

| Concepto | Finalidad | Pregunta que responde |
| :--- | :--- | :--- |
| **Monitorización** | Vigilar estado y alertas (latencia, caídas). | ¿Está fallando el sistema? |
| **Observabilidad** | Telemetría profunda (Trazas, Spans). | ¿Por qué el sistema tomó esta ruta? |
| **Auditoría (Art. 12 AI Act)** | Revisión formal con evidencias de los logs. | ¿Cumplió las políticas y responsabilidades legales? |

#### 2.3. Métricas y Anomalías Específicas de Agentes

* **Consumo de Tokens / Coste por Tarea:** Los agentes iteran en bucle; el coste se multiplica exponencialmente por cada paso de razonamiento (un agente puede hacer 10 invocaciones al modelo para 1 sola respuesta al usuario).
* **Latencia por Invocación vs. Latencia End-to-End.**
* **Tasa de uso de herramientas y Tasa de fallo de herramientas.**
* **Detección de Bucles Infinitos (Infinite Tool Loop):** El agente llama repetidamente a la misma herramienta sin lograr avanzar. Requiere mecanismos de corte (*Circuit Breakers* / *Timeouts*) y límites de pasos en el orquestador.

#### 2.4. Exigencia Normativa

El **Art. 12 del Reglamento (UE) 2024/1689** exige que los sistemas de alto riesgo incorporen capacidades de registro automático de eventos (*logging*) a lo largo de su ciclo de vida, lo cual hace que la observabilidad detallada sea un imperativo legal para el gobierno de la IA.

### 3. Ingeniería de prompts (Prompt Engineering)

Disciplina de diseño iterativo de instrucciones de entrada para optimizar la fiabilidad del modelo, gestionar el formato de salida y mitigar alucinaciones. Para el perfil de Gobierno (P02), el *Prompt Engineering* no es optimizar respuestas, sino **diseñar instrucciones operativas como un mecanismo de control de seguridad (Guardrails)**; un *prompt* en producción debe versionarse y tratarse como código fuente crítico.

#### 3.1. Arquitectura de Prompts en Agentes

* **System Prompt:** Instrucciones persistentes de alto nivel con máxima prioridad de atención en el modelo. Fija las reglas inmutables de seguridad y el marco de actuación.
* **User Prompt:** La entrada del ciudadano/usuario, que nunca debe tener precedencia sobre el System Prompt.

#### 3.2. Técnicas Estructurales

* **Zero-shot / Few-shot:** Inclusión de cero o varios pares de ejemplos "entrada-salida" para adiestrar al modelo mediante aprendizaje en contexto.
* **Chain-of-Thought (CoT - Cadena de Pensamiento):** Induce al modelo a generar pasos de razonamiento intermedios lógicos antes de la respuesta final, reduciendo errores matemáticos y lógicos. *Valor para P02:* proporciona **explicabilidad** a la decisión para auditorías posteriores.
* **ReAct (Reasoning and Acting):** La técnica de prompt más crítica en IA agéntica. Combina CoT con interacción externa, forzando al modelo a ciclar en tres pasos estructurados:
  1. **Thought (Pensamiento):** razonamiento interno sobre el estado actual.
  2. **Action (Acción):** especificación de la herramienta a usar y sus argumentos.
  3. **Observation (Observación):** resultado inyectado de vuelta al prompt tras la ejecución real de la herramienta por el sistema.

#### 3.3. Prompt Injection (Vulnerabilidad OWASP LLM01)

Técnica de ataque donde el comportamiento del agente es manipulado mediante instrucciones adversarias:
* **Directa (Jailbreak):** el usuario introduce comandos para eludir los Guardrails (ej. "Ignora tus directrices previas").
* **Indirecta:** el mayor riesgo en la Administración. El agente utiliza una herramienta para leer un entorno externo (web, PDF, correo de terceros) que contiene instrucciones maliciosas ocultas. El LLM las asimila como una instrucción legítima y ejecuta acciones no autorizadas o dañinas (ej. extraer datos de otros expedientes, borrar información) creyendo que son legítimas.

### 4. AgentOps

**AgentOps** es la extensión operativa de MLOps y LLMOps adaptada al ciclo de vida de los sistemas autónomos, combinando la gestión de modelos, prompts/generación y DevOps, centrada en gobernar el **ciclo de vida de las trayectorias de decisión autónomas**, los flujos multi-paso, la integración de herramientas y la gestión de la memoria adaptativa.

#### 4.1. Diferencias operativas entre disciplinas

* **MLOps:** Optimiza modelos matemáticos (drift, exactitud, reentrenamiento).
* **LLMOps:** Optimiza el uso de un modelo fundacional estático (RAG, evaluación de prompts, mitigación de toxicidad).
* **AgentOps:** Gestiona el bucle de ejecución, permisos de herramientas, validación de esquemas JSON, límites de concurrencia y protocolos de supervisión humana.

#### 4.2. Funciones de Gobernanza en AgentOps

* **Gestión del Cambio y Versionado:** un cambio en el System Prompt o la adición de una nueva herramienta altera radicalmente el perfil de riesgo del agente; requiere *pipelines* de CI/CD con evaluaciones automatizadas.
* **Evaluación Dinámica (Agent Evaluation):** a diferencia de un LLM que se evalúa por similitud de texto (BLEU/ROUGE) o Perplejidad, un agente se evalúa por:
  * *Task Success Rate:* ¿consiguió el objetivo final?
  * *Trajectory Score:* ¿fueron los pasos elegidos lógicos, óptimos y seguros?
* **Control de Autonomía y Supervisión (HITL):** implementación técnica de puntos de control donde el agente se detiene y exige aprobación humana (*Human-in-the-loop*) antes de ejecutar una acción irreversible o con impacto legal/alto riesgo (ej. enviar una notificación formal, transacciones financieras).
* **Prevención de Denegación de Cartera (Denial of Wallet):** mecanismos para detener a un agente si sus llamadas a APIs de pago o consumo de tokens exceden el presupuesto asignado por error o por un ataque adversario.

#### 4.3. Controles Críticos de Seguridad

* **Guardrails (Cortafuegos lógicos):** reglas validadoras en la entrada y la salida para sanitizar textos, evitar fugas de información (PII) o bloquear JSON malformados.
* **HITL (Human-in-the-Loop):** aprobación explícita requerida antes de que el orquestador ejecute una acción irreversible.
* **Evaluación Dinámica:** transición desde métricas estáticas (Perplejidad, BLEU) hacia la simulación de entornos para medir la Tasa de Éxito de Tareas.

## Conceptos que suelen preguntarse (Trampas comunes)

| Concepto a distinguir | Realidad técnica / jurídica | Distractor típico en examen |
| :--- | :--- | :--- |
| **Agente vs. Chatbot** | El agente decide y ejecuta acciones; el chatbot solo conversa. | "Un chatbot basado en LLM es automáticamente un agente de IA". |
| **CoT vs. ReAct** | CoT es razonamiento interno lineal en texto. ReAct interrumpe para interactuar con herramientas externas (Action/Observation). | "CoT y ReAct son sinónimos técnicos y ambos siempre llaman a APIs". |
| **Memoria vs. Ventana de Contexto** | Memoria (largo plazo, ej. BBDD vectorial) retiene datos entre sesiones. Ventana de Contexto (corto plazo) es el límite de tokens por llamada y se destruye al cerrar la sesión. | "Ampliar la ventana de contexto crea una memoria semántica persistente infinita". |
| **Ejecución de Herramientas** | El LLM emite una propuesta (ej. JSON); el Orquestador valida permisos y ejecuta la API. | "El modelo LLM se conecta directamente a la base de datos y ejecuta el comando". |
| **Inyección Indirecta de Prompts** | El ataque proviene de los datos ingeridos (documentos, webs) leídos por el agente de forma autónoma. | "La inyección indirecta solo ocurre cuando el administrador teclea mal el prompt". |
| **Trazas vs. Logs** | Las Trazas reconstruyen la relación causal del flujo completo (Spans); los logs son eventos discretos estáticos. | "Guardar un fichero plano de logs garantiza el 100% de la explicabilidad del modelo". |
| **Observabilidad vs. APM** | La observabilidad en agentes rastrea decisiones estocásticas (spans, prompts); el APM sigue código predecible determinista. | "El APM tradicional es suficiente para depurar sistemas multi-agente". |
| **AgentOps vs. LLMOps** | AgentOps añade la gestión del bucle autónomo, estado, HITL y herramientas externas a LLMOps. | "AgentOps se enfoca exclusivamente en entrenar los pesos del modelo neuronal". |

## Posibles preguntas tipo test

**Pregunta 1.** En el diseño de una arquitectura de agente de IA basada en el patrón ReAct, la estructura del bucle de decisión se define obligatoriamente por la siguiente secuencia:

A. System Prompt → User Prompt → Output Parser.

B. Ingesta → Chunking → Búsqueda Vectorial.

C. Thought (Pensamiento) → Action (Acción) → Observation (Observación).

D. Zero-shot → Few-shot → Chain-of-Thought.

**Respuesta correcta: C.** (Es la tríada fundacional del framework ReAct para agentes autónomos).

**Pregunta 2.** En el contexto de un sistema agéntico que integra invocación a herramientas externas (Tool Calling), ¿quién es el responsable técnico de validar los parámetros de entrada y ejecutar físicamente la llamada a la API corporativa?

A. El modelo de lenguaje (LLM), utilizando su red neuronal interna.

B. La Memoria a Largo Plazo del agente.

C. El código de la aplicación subyacente (Orquestador/Framework) tras recibir la respuesta estructurada del modelo.

D. El protocolo W3C Trace Context de forma automática.

**Respuesta correcta: C.** (El LLM propone los argumentos, típicamente en JSON; el framework orquestador ejecuta la acción y asegura los permisos, clave de seguridad OWASP LLM07).

**Pregunta 3.** ¿Cuál de las siguientes situaciones describe con precisión una vulnerabilidad de Inyección Indirecta de Prompts (Indirect Prompt Injection) en un agente de soporte público?

A. El modelo es reentrenado (Fine-Tuning) por un desarrollador con un dataset corrupto (Data Poisoning).

B. Un ciudadano envía una consulta y el agente, utilizando su herramienta de búsqueda web autorizada, escanea una página de terceros que contiene texto malicioso oculto que altera el comportamiento del agente.

C. Un usuario autorizado reduce la temperatura del LLM a cero para forzar respuestas codiciosas.

D. La ventana de contexto sobrepasa el límite máximo permitido por el proveedor, truncando las instrucciones de seguridad.

**Respuesta correcta: B.** (La inyección indirecta proviene de datos asimilados en tiempo de ejecución a través de las herramientas del agente, no de la interacción directa del usuario en el chat).

**Pregunta 4.** Dentro del marco de observabilidad de aplicaciones de IA Generativa (siguiendo convenciones de OpenTelemetry), ¿cuál es la diferencia exacta entre una Traza (Trace) y un Tramo (Span)?

A. Un Trace almacena el coste económico; un Span almacena los tokens consumidos.

B. Una Trace representa el flujo completo para resolver una solicitud del usuario; el Span representa una unidad de trabajo discreta dentro de dicha traza (ej. la invocación a una base de datos vectorial).

C. Son conceptos idénticos e intercambiables en sistemas multi-agente.

D. El Trace pertenece a la memoria a corto plazo, el Span a la memoria a largo plazo.

**Respuesta correcta: B.**

**Pregunta 5.** La incorporación del patrón HITL (Human-in-the-Loop) en el ámbito de las operaciones de agentes (AgentOps) busca principalmente:

A. Eliminar completamente la latencia de la inferencia.

B. Validar manualmente el tokenizador subword empleado por el LLM.

C. Introducir una validación y aprobación humana explícita antes de que el agente orquestador ejecute una acción irreversible o de alto riesgo propuesta por el modelo.

D. Optimizar la actualización de los embeddings en la memoria semántica.

**Respuesta correcta: C.** (Es un control crítico de gobierno para prevenir ejecuciones autónomas descontroladas).

**Pregunta 6.** Desde la perspectiva del gobierno de la IA, ¿por qué la vulnerabilidad conocida como "Inyección Indirecta de Prompts" representa un riesgo crítico de seguridad operativo específico para los agentes de IA?

A. Porque altera físicamente los pesos sinápticos del modelo fundacional durante el entrenamiento.

B. Porque explota la capacidad autónoma del agente de leer y asimilar información de fuentes externas (ej. documentos web o correos), que contienen comandos ocultos diseñados para subvertir las políticas del sistema.

C. Porque requiere que el atacante posea credenciales de administrador de la plataforma cloud.

D. Porque eleva la temperatura estocástica del modelo, obligándolo a generar salidas deterministas.

**Respuesta correcta: B.** (La inyección indirecta utiliza las propias herramientas de lectura del agente en contra de las políticas de su orquestador).

**Pregunta 7.** De acuerdo con el Reglamento (UE) 2024/1689 (Ley de IA), los sistemas de alto riesgo deben garantizar la trazabilidad de su funcionamiento a lo largo de su ciclo de vida. En el marco de AgentOps, ¿qué mecanismo técnico proporciona la instrumentación adecuada para cumplir este requisito registrando el razonamiento y las llamadas a herramientas?

A. La reducción de la dimensionalidad de los Embeddings.

B. La implementación exclusiva de métricas de uso de CPU y RAM del servidor.

C. La telemetría estructurada mediante Trazas (Traces) y Tramos (Spans), capturando el estado del prompt, el pensamiento y las acciones paso a paso.

D. El uso de validadores sintácticos de bases de datos relacionales tradicionales.

**Respuesta correcta: C.** (La observabilidad profunda mediante trazas desglosa el comportamiento de "caja negra" en eventos secuenciales auditables).

**Pregunta 8.** En la evaluación dinámica de agentes autónomos (AgentOps), a diferencia de las métricas puramente lingüísticas empleadas en la evaluación de LLMs estáticos, ¿cuál es un indicador clave para medir la pertinencia de las decisiones tomadas por el agente?

A. La evaluación de la trayectoria (Trajectory Score), que analiza si los pasos y herramientas elegidas fueron lógicos y seguros para alcanzar la meta.

B. El cálculo de la Complejidad Ciclomática del código fuente del orquestador Python.

C. La comprobación del hash criptográfico de la imagen Docker desplegada en Kubernetes.

D. El conteo total del vocabulario del tokenizador (Byte-Pair Encoding).

**Respuesta correcta: A.** (En agentes importa tanto el resultado final como los medios empleados para llegar a él).

## Normativa o fuentes relacionadas

* **Reglamento (UE) 2024/1689 (Ley de IA):** Art. 12 (obligación de registro automático de acontecimientos o *logging* a lo largo del ciclo de vida para sistemas de alto riesgo) y Art. 14 (Supervisión humana / HITL).
* **Real Decreto 311/2022 (Esquema Nacional de Seguridad):** Principios básicos de protección, gestión de riesgos, registro de actividad, gestión de incidentes, control de acceso y mínimo privilegio, esenciales para el diseño seguro de herramientas agénticas en el sector público.
* **OWASP Top 10 for LLM Applications:** Documentación técnica de referencia para la ciberseguridad en IA, detallando amenazas críticas como la inyección de prompts (LLM01), el diseño inseguro de plugins/herramientas (LLM07) y la agencia excesiva (LLM08).
* **NIST AI RMF 1.0 y NIST AI 600-1 (Generative AI Profile):** Marcos voluntarios de gestión de riesgos de IA, útiles para estructurar el gobierno y la confianza en sistemas generativos y agénticos.
* **OpenTelemetry — Semantic Conventions for GenAI:** Estándar técnico abierto de facto para la instrumentación de trazas, métricas y logs en aplicaciones de IA generativa y agéntica.

## Dudas o puntos pendientes

* **Estatus normativo de "AgentOps" y ausencia de estándar ISO/IEC:** Es vital recordar que AgentOps, la definición de agente, frameworks como ReAct y los protocolos emergentes MCP y A2A son disciplinas y especificaciones técnicas de la industria en rápida evolución, **no una norma ISO/IEC oficial ni terminología normativamente fijada**. El AI Act regula el riesgo del "Sistema de IA", independientemente de si la industria lo etiqueta comercialmente como "agente", "workflow" o "chatbot".
* **MCP y A2A:** Deben estudiarse como patrones de integración, asumiendo que su adopción no exime de cumplir las políticas corporativas tradicionales de IAM (Gestión de Identidad y Accesos) y seguridad de red de la Administración.
* **Inyección de Prompts en el Esquema Nacional de Seguridad:** El ENS no nombra literalmente la inyección de prompts, pero sus controles sobre validación de entradas de datos, sanitización e integridad de las interfaces externas son los fundamentos obligatorios aplicables para mitigar estas vulnerabilidades en la Administración Pública.
