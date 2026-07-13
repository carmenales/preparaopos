---
id: "tema-003-ia-agentica"
title: "IA Agéntica"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital"
official_topic: "Tema 3. IA Agéntica"
source_ids: []
tags:
  - inteligencia-artificial
  - ia-generativa
  - ia-agentica
  - agentes-ia
  - observabilidad
  - prompt-engineering
  - agentops
created_at: "2026-07-09"
last_reviewed: null
ai_generated: true
ai_sources:
  - "chatgpt"
  - "perplexity"
  - "gemini"
  - "base-apunte"
needs_human_review: true
---

# Fundamentos de Inteligencia Artificial

## Encaje en la convocatoria

Este tema corresponde al **Tema 3. IA Agéntica** del Anexo 3 de la Resolución 352/2026 (BOCM 11/06/2026), dentro de las áreas de conocimiento del Bloque 1 para los perfiles **P01 (IA aplicada al ciclo de vida del software)** y **P02 (Gobierno de IA)** de la Agencia para la Administración Digital de la Comunidad de Madrid. 

La prueba consta de **45 preguntas tipo test (+5 de reserva)**, con **penalización de -0,25 puntos por error**. El estudio debe enfocarse en la precisión técnica de las arquitecturas de software autónomo, componentes lógicos de los agentes (memoria, herramientas, planificación), gobernanza operativa (*AgentOps*) y telemetría, evitando el enfoque puramente divulgativo. 

A nivel normativo, aunque la "IA Agéntica" no es una categoría estricta en el Reglamento (UE) 2024/1689 (Ley de IA), los sistemas agénticos están sujetos a las obligaciones de trazabilidad, gestión de riesgos, supervisión humana (HITL) y registro de logs (Art. 12), especialmente en casos de alto riesgo.

## Ideas clave

- **Agente de IA vs. LLM:** Un LLM es un modelo estadístico que genera salidas (texto, código). Un Agente es una arquitectura de software que utiliza el LLM como motor de razonamiento dentro de un bucle de percepción, planificación y ejecución de acciones mediante herramientas.
- **ReAct Framework:** Paradigma fundamental en IA agéntica que unifica el razonamiento lógico (*Chain-of-Thought*) con la acción práctica (*Function Calling*) mediante la secuencia iterativa: *Thought $\rightarrow$ Action $\rightarrow$ Observation*.
- **Ejecución de herramientas (Function Calling):** El LLM **no ejecuta** código ni herramientas externas. El LLM emite una salida estructurada (típicamente JSON) decidiendo qué herramienta usar y con qué parámetros. El *framework* subyacente (orquestador) es quien invoca la API y devuelve la observación al modelo.
- **AgentOps vs. Observabilidad:** La observabilidad se centra en la telemetría técnica de la ejecución distribuida (trazas, *spans*, latencia, coste). AgentOps abarca el ciclo de vida operacional completo: gobernanza, validación de *prompts*, control de bucles infinitos y evaluación (Tasa de Éxito de Tareas).
- **Vulnerabilidad Crítica:** La **Inyección Indirecta de Prompts (Indirect Prompt Injection)** es el mayor vector de ataque en agentes (OWASP Top 10 LLM01), ocurriendo cuando el agente asimila instrucciones maliciosas desde fuentes de datos externas consultadas mediante sus herramientas.

## Desarrollo

### 1. Concepto de agente: tipos, componentes e integración

Un **Agente de IA** es un sistema que percibe su contexto, razona sobre los datos disponibles y ejecuta acciones de forma autónoma o semiautónoma para alcanzar un objetivo definido, apoyándose en un modelo fundacional. 
#### 1.1. Diferencia entre Chatbot, RAG y Agente
* **Chatbot:** Interacción conversacional reactiva. Baja autonomía.
* **RAG (Generación Aumentada por Recuperación):** Recupera información y la aporta al contexto. No planifica acciones ni modifica su entorno.
* **Agente IA:** Decide interactivamente qué pasos dar, invoca herramientas (APIs, bases de datos) y reevalúa el estado tras cada acción.

#### 1.2. Tipos de Arquitecturas
* **Agente Único (*Single-Agent*):** Un modelo ejecuta todo el flujo de planificación y uso de herramientas en un mismo bucle de contexto. Riesgo de *Prompt Drift* (desvío del objetivo) en tareas complejas.
* **Sistemas Multi-Agente (*Multi-Agent Systems - MAS*):** Colaboración o delegación entre agentes lógicos especializados (ej. patrón Supervisor o *Manager-Worker*). Mejora la modularidad pero incrementa la latencia, el coste y la complejidad de la observabilidad.

#### 1.3. Componentes Críticos del Agente
1. **Modelo (*Brain/Core*):** LLM con capacidad de razonamiento estructurado.
2. **Memoria:**
   * **A corto plazo (*Short-term Memory*):** El historial acumulado dentro de la *ventana de contexto* en una sesión activa (*In-Context Learning*). Desaparece al finalizar la sesión.
   * **A largo plazo (*Long-term Memory*):** Almacenamiento persistente externo (ej. Bases de Datos Vectoriales) que permite al agente recuperar contextos históricos de ejecuciones pasadas por similitud semántica.
3. **Herramientas (*Tools/Plugins*):** Interfaces hacia sistemas externos (APIs, RAG, *sandboxes* de código). Definidas analíticamente mediante esquemas (JSON Schema). **Nota de seguridad (OWASP LLM07):** Requieren principios de mínimo privilegio; la validación de sus parámetros recae en el orquestador, no en el modelo.
4. **Planificación (*Planning*):**
   * **Descomposición:** Partir un problema en subtareas lógicas.
   * **Reflexión (*Reflexion*):** Autocrítica tras observar el resultado de una acción para iterar o corregir la estrategia.

#### 1.4. Integración (Protocolos Emergentes)
* **MCP (Model Context Protocol):** Estándar abierto para conectar de forma segura modelos/agentes con fuentes de datos externas y herramientas locales.
* **A2A (Agent2Agent Protocol):** Protocolos orientados a la interoperabilidad, descubrimiento y delegación de tareas entre distintos agentes.

### 2. Observabilidad en agentes

La naturaleza no determinista de los LLMs impide la depuración de software tradicional. El flujo de control lo decide el modelo en tiempo de ejecución, no un código condicional estricto escrito por un humano. 
#### 2.1. Trazas y Tramos (*Traces and Spans*)
Basado en las convenciones semánticas de **OpenTelemetry para IA Generativa**:
* **Traza (*Trace*):** Representa el flujo completo para resolver una solicitud del usuario (ej. `solicitud-123`).
* **Tramo (*Span*):** Subdivisión temporal de una unidad de trabajo discreta dentro de la traza (ej. llamada de inferencia al LLM, invocación de la API de creación de tickets, búsqueda vectorial).

#### 2.2. Métricas y Anomalías Específicas
* **Consumo de Tokens y Coste por Tarea:** Monitoreo exhaustivo debido al coste recursivo de los agentes.
* **Latencia por Invocación vs. Latencia *End-to-End*:** Un agente puede hacer 10 invocaciones al modelo para 1 sola respuesta al usuario.
* **Infinite Tool Loop (Bucle Infinito):** Anomalía donde el agente entra en un estado cíclico invocando reiteradamente una herramienta sin lograr la condición de parada. Requiere control de *timeouts* y límites de pasos en el orquestador.

#### 2.3. Exigencia Normativa
El **Art. 12 del Reglamento (UE) 2024/1689** exige que los sistemas de alto riesgo incorporen capacidades de registro automático de eventos (*logging*) a lo largo de su ciclo de vida, lo cual hace que la observabilidad detallada sea un imperativo legal para el gobierno de la IA.

### 3. Ingeniería de prompts (Prompt Engineering)

Disciplina de diseño iterativo de instrucciones de entrada para optimizar la fiabilidad del modelo, gestionando el formato de salida y mitigando alucinaciones.

#### 3.1. Técnicas Estructurales
* **Zero-shot / Few-shot:** Inclusión de cero o varios pares de ejemplos "entrada-salida" para adiestrar al modelo mediante aprendizaje en contexto.
* **Chain-of-Thought (CoT - Cadena de Pensamiento):** Inducir al modelo a generar pasos de razonamiento intermedios lógicos antes de la respuesta final. Reduce errores matemáticos y lógicos.

#### 3.2. El framework ReAct (Reasoning and Acting)
Es la técnica de prompt más crítica en IA agéntica. Combina CoT con interacción externa forzando al modelo a ciclar en tres pasos estructurados:
1. **Thought (Pensamiento):** Razonamiento interno sobre el estado actual.
2. **Action (Acción):** Especificación de la herramienta a usar y sus argumentos.
3. **Observation (Observación):** Resultado inyectado de vuelta al prompt tras la ejecución real de la herramienta por el sistema.

#### 3.3. Prompt Injection (Vulnerabilidad OWASP LLM01)
Técnica de ataque donde el comportamiento del agente es manipulado mediante instrucciones adversarias.
* **Directa (Jailbreak):** El usuario ingresa la instrucción (ej. "Ignora tus directrices previas").
* **Indirecta:** Crítica en agentes. El agente utiliza una herramienta para leer un entorno externo (web, PDF, correo de terceros) que contiene instrucciones maliciosas ocultas. El modelo las asimila y ejecuta acciones dañinas (ej. borrar base de datos) creyendo que son legítimas.

### 4. AgentOps

**AgentOps** es la extensión de LLMOps adaptada al ciclo de vida de los sistemas autónomos, abarcando flujos multi-paso, integración de herramientas y gestión de la memoria adaptativa.

#### 4.1. Diferencias operativas
* **MLOps:** Optimiza modelos matemáticos (drift, exactitud, reentrenamiento).
* **LLMOps:** Optimiza el uso de un modelo fundacional estático (RAG, evaluación de prompts, mitigación de toxicidad).
* **AgentOps:** Gestiona el bucle de ejecución, permisos de herramientas, validación de esquemas JSON, límites de concurrencia y protocolos de supervisión humana.

#### 4.2. Controles Críticos de Seguridad
* **Guardrails (Cortafuegos Lógicos):** Reglas validadoras en la entrada y la salida para sanitizar textos, evitar fugas de información (PII) o bloquear JSON malformados.
* **HITL (Human-in-the-Loop):** Aprobación explícita requerida antes de que el orquestador ejecute una acción irreversible (ej. envíos de correos, transacciones financieras) propuesta por el agente.
* **Evaluación Dinámica:** Transición desde métricas estáticas (Perplejidad, BLEU) hacia la simulación de entornos para medir la **Tasa de Éxito de Tareas (*Task Success Rate*)**.

## Conceptos que suelen preguntarse

| Concepto | Realidad técnica | Distractor típico en examen |
| :--- | :--- | :--- |
| **CoT vs. ReAct** | **CoT** es razonamiento interno lineal. **ReAct** incluye llamadas iterativas a herramientas externas (*Action/Observation*). | "CoT y ReAct son sinónimos absolutos y ambos invocan APIs". |
| **Memoria vs. Contexto** | **Memoria** (largo plazo) es persistente (BBDD vectoriales). **Contexto** (corto plazo) se destruye al cerrar la sesión. | "Aumentar la ventana de contexto de un LLM equivale a memoria persistente". |
| **Ejecución de Herramientas** | El LLM emite una propuesta (ej. JSON). El **Orquestador** valida permisos y ejecuta la API. | "El modelo LLM se conecta directamente a la base de datos y ejecuta el comando". |
| **Observabilidad vs. APM** | La observabilidad en agentes rastrea **decisiones estocásticas** (spans, prompts); el APM sigue código predecible determinista. | "El APM tradicional es suficiente para depurar sistemas multi-agente". |
| **AgentOps vs. LLMOps** | AgentOps añade la gestión del bucle autónomo, estado, HITL y herramientas externas a LLMOps. | "AgentOps se enfoca exclusivamente en entrenar los pesos del modelo neuronal". |

## Posibles preguntas tipo test

**Pregunta 1.** En el diseño de una arquitectura de agente de IA basada en el patrón ReAct, la estructura del bucle de decisión se define obligatoriamente por la siguiente secuencia:
A. System Prompt $\rightarrow$ User Prompt $\rightarrow$ Output Parser.
B. Ingesta $\rightarrow$ Chunking $\rightarrow$ Búsqueda Vectorial.
C. Thought (Pensamiento) $\rightarrow$ Action (Acción) $\rightarrow$ Observation (Observación).
D. Zero-shot $\rightarrow$ Few-shot $\rightarrow$ Chain-of-Thought.
**Respuesta correcta: C.** (Es la tríada fundacional del framework ReAct para agentes autónomos).

**Pregunta 2.** En el contexto de un sistema agéntico que integra invocación a herramientas externas (*Tool Calling*), ¿quién es el responsable técnico de validar los parámetros de entrada y ejecutar físicamente la llamada a la API corporativa?
A. El modelo de lenguaje (LLM), utilizando su red neuronal interna.
B. La Memoria a Largo Plazo del agente.
C. El código de la aplicación subyacente (Orquestador/Framework) tras recibir la respuesta estructurada del modelo.
D. El protocolo W3C Trace Context de forma automática.
**Respuesta correcta: C.** (El LLM propone los argumentos, típicamente en JSON; el framework orquestador ejecuta la acción y asegura los permisos, clave de seguridad OWASP LLM07).

**Pregunta 3.** ¿Cuál de las siguientes situaciones describe con precisión una vulnerabilidad de **Inyección Indirecta de Prompts (Indirect Prompt Injection)** en un agente de soporte público?
A. El modelo es reentrenado (*Fine-Tuning*) por un desarrollador con un dataset corrupto (Data Poisoning).
B. Un ciudadano envía una consulta y el agente, utilizando su herramienta de búsqueda web autorizada, escanea una página de terceros que contiene texto malicioso oculto que altera el comportamiento del agente.
C. Un usuario autorizado reduce la temperatura del LLM a cero para forzar respuestas codiciosas.
D. La ventana de contexto sobrepasa el límite máximo permitido por el proveedor, truncando las instrucciones de seguridad.
**Respuesta correcta: B.** (La inyección indirecta proviene de datos asimilados en tiempo de ejecución a través de las herramientas del agente, no de la interacción directa del usuario en el chat).

**Pregunta 4.** Dentro del marco de observabilidad de aplicaciones de IA Generativa (siguiendo convenciones de OpenTelemetry), ¿cuál es la diferencia exacta entre una Traza (*Trace*) y un Tramo (*Span*)?
A. Un *Trace* almacena el coste económico; un *Span* almacena los tokens consumidos.
B. Una *Trace* representa el flujo completo para resolver una solicitud del usuario; el *Span* representa una unidad de trabajo discreta dentro de dicha traza (ej. la invocación a una base de datos vectorial).
C. Son conceptos idénticos e intercambiables en sistemas multi-agente.
D. El *Trace* pertenece a la memoria a corto plazo, el *Span* a la memoria a largo plazo.
**Respuesta correcta: B.**

**Pregunta 5.** La incorporación del patrón HITL (*Human-in-the-Loop*) en el ámbito de las operaciones de agentes (*AgentOps*) busca principalmente:
A. Eliminar completamente la latencia de la inferencia.
B. Validar manualmente el tokenizador subword empleado por el LLM.
C. Introducir una validación y aprobación humana explícita antes de que el agente orquestador ejecute una acción irreversible o de alto riesgo propuesta por el modelo.
D. Optimizar la actualización de los embeddings en la memoria semántica.
**Respuesta correcta: C.** (Es un control crítico de gobierno para prevenir ejecuciones autónomas descontroladas).

## Normativa o fuentes relacionadas

* **Fuentes Normativas:** * **Reglamento (UE) 2024/1689 (Ley de IA):** Art. 12 (obligación de registro de acontecimientos o *logging* a lo largo del ciclo de vida para sistemas de alto riesgo), Art. 14 (Supervisión humana / HITL).
  * **Real Decreto 311/2022 (Esquema Nacional de Seguridad):** Requisitos de trazabilidad, gestión de incidentes y control de acceso.
* **Estándares y Marcos Técnicos Institucionales:**
  * **NIST AI RMF 1.0 (Artificial Intelligence Risk Management Framework):** Para el gobierno y tolerancia al riesgo en la autonomía.
  * **NIST AI 600-1 (Generative AI Profile):** Riesgos propios de modelos generativos, mitigación de inyecciones y fiabilidad.
  * **OWASP Top 10 for LLM Applications:** Documentación técnica de ciberseguridad primaria (LLM01: Prompt Injection, LLM07: Insecure Plugin Design, LLM08: Excessive Agency).
  * **OpenTelemetry - Semantic Conventions for GenAI:** Estándar técnico abierto de facto para instrumentación de trazas (*traces*) y tramos (*spans*) en llamadas LLM.

## Dudas o puntos pendientes

* **Ausencia de un estándar oficial ISO/IEC consolidado para "AgentOps" o "Agente de IA":** La definición de agente, los frameworks como ReAct o los protocolos emergentes MCP (*Model Context Protocol*) y A2A (*Agent2Agent Protocol*) se presentan como conocimiento técnico avanzado de la industria (provenientes de documentación de fabricantes y especificaciones abiertas), pero no constituyen terminología normativamente fijada en el momento de la convocatoria.
* **Inyección de Prompts en el Esquema Nacional de Seguridad:** El ENS no nombra literalmente la inyección de prompts, pero sus controles sobre validación de entradas de datos, sanitización e integridad de las interfaces externas son los fundamentos obligatorios aplicables para mitigar estas vulnerabilidades en la Administración Pública.