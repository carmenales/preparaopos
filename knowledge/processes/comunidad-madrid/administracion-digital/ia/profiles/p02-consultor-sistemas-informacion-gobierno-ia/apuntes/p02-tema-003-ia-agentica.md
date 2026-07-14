---
id: "cm-ad-ia-p02-tema-003-ia-agentica"
title: "IA Agéntica"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/ia"
profiles:
  - "p02-consultor-sistemas-informacion-ia"
official_profile: "P02 - Consultor de Sistemas de Información - Especialista en Gobierno de IA"
official_topic: "Tema 3. IA Agentica"
source_ids: []
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

# IA Agéntica

## Encaje en la convocatoria

Este tema corresponde al **Tema 3 del Anexo 3** de la Resolución 352/2026 (BOCM 11/06/2026)[cite: 1]. Para el perfil **P02 (Consultor de Sistemas de Información especialista en Gobierno de IA)**, el enfoque de este tema difiere sustancialmente del perfil de desarrollo (P01).

Aquí, la IA Agéntica no se estudia desde cómo programar una llamada a una API, sino desde **cómo controlar la autonomía, auditar la trayectoria de decisiones, gestionar los riesgos de seguridad (OWASP) y garantizar el cumplimiento normativo (AI Act y ENS)**. En un examen tipo test, es crucial distinguir entre la "observabilidad" técnica de *AgentOps* y el "registro de eventos" (*logging*) como obligación legal. Se debe diferenciar claramente un *Prompt* como instrucción de código frente a un *Prompt* como mecanismo de control lógico (*Guardrail*).

## Ideas clave

1.  **Agente vs. LLM:** Un LLM genera salidas estadísticas. Un **Agente de IA** es una arquitectura de software que *usa* el LLM como motor de razonamiento para perseguir objetivos, invocar herramientas y modificar su entorno de forma autónoma.
2.  **Riesgo y Autonomía:** A mayor autonomía y capacidad de uso de herramientas externas (ej. consultar un expediente real), mayor es la superficie de ataque y la necesidad de **mínimo privilegio (ABAC/RBAC)**, trazabilidad y supervisión humana (*Human-in-the-loop*).
3.  **Observabilidad (Trazabilidad Estructural):** En sistemas agénticos, no basta con monitorizar si el servidor está encendido. La observabilidad se basa en **Trazas (*Traces*)** y **Tramos (*Spans*)** que documentan paso a paso el razonamiento (*Thought*) y la acción (*Action*) del agente.
4.  **Cumplimiento Legal (Art. 12 AI Act):** Para sistemas de alto riesgo, la observabilidad es la implementación técnica del **registro automático de acontecimientos (*logging*)** exigido por el Reglamento (UE) 2024/1689.
5.  **Prompt Engineering en Gobierno:** No es "hablar con la IA". Es la disciplina de inyectar reglas inmutables (*System Prompt*) que actúan como barreras de seguridad, definiendo qué herramientas puede usar el agente y bajo qué condiciones debe detenerse o escalar al humano.
6.  **Inyección Indirecta de Prompts:** Es la vulnerabilidad más crítica en IA Agéntica (OWASP Top 10 LLMs). Ocurre cuando el agente, usando sus herramientas, lee un documento externo infectado con comandos ocultos que subvierten sus reglas operativas originales.
7.  **AgentOps:** Es la extensión de MLOps/LLMOps. Se centra operativamente en la gobernanza de las trayectorias de decisión, el control de bucles infinitos, la evaluación dinámica (Tasa de éxito de tareas) y la gestión del coste por interacciones complejas.

## Desarrollo

### 1. Concepto de agente: tipos, componentes e integración

**Agente de IA:** Sistema que percibe su contexto, razona utilizando un modelo fundacional (LLM) y ejecuta acciones secuenciales de forma autónoma o semiautónoma mediante el uso de herramientas externas para alcanzar un objetivo definido.

#### 1.1. Tipos de Arquitecturas (Perspectiva de Gobierno)

*   **Agente Único (*Single-Agent*):** Un solo modelo orquesta la planificación y las herramientas. *Riesgo:* Desviación del objetivo (*Prompt Drift*) en tareas largas y dificultad para aplicar el principio de segregación de funciones.
*   **Sistemas Multi-Agente (*Multi-Agent Systems - MAS*):** Múltiples agentes con *System Prompts* aislados y roles especializados que colaboran (ej. un agente redacta, un agente auditor revisa normativamente, un agente orquestador dirige).
    *   *Ventaja:* Mejora el control y la modularidad.
    *   *Riesgo:* **Colusión de agentes** (cooperación anómala para eludir seguridad), aumento de latencia, coste y propagación en cascada de errores.

#### 1.2. Componentes Críticos (Foco de Auditoría)

1.  **Modelo (*Brain*):** El LLM base que razona.
2.  **Memoria:**
    *   *A corto plazo:* El contexto inmediato de la sesión.
    *   *A largo plazo:* Bases de datos vectoriales. *Implicación (RGPD):* Almacenar datos personales de ciudadanos en la memoria de un agente exige políticas estrictas de retención, minimización y mecanismos para el **Derecho de Supresión (Art. 17 RGPD)**.
3.  **Herramientas (*Tools / Function Calling*):** Interfaces a sistemas externos (APIs). Constituyen el mayor vector de riesgo. Exigen arquitecturas *Zero Trust*: el agente debe usar una Identidad de Máquina con privilegios mínimos, y la validación final de los parámetros la ejecuta el orquestador (código tradicional), no el LLM.
4.  **Planificación (*Planning*):** Capacidad de descomponer tareas y autocorregirse (*Reflexion*).
5.  **Orquestación:** El marco de control lógico (ej. LangGraph) que rige el flujo, aplica *timeouts* y define cuándo detener el bucle o requerir aprobación humana (*HITL*).

#### 1.3. Integración y Protocolos

*   **MCP (*Model Context Protocol*):** Estándar abierto para conectar de forma segura agentes con fuentes de datos y herramientas, estandarizando la exposición de recursos.
*   **A2A (*Agent2Agent Protocol*):** Orientado a la interoperabilidad y comunicación entre distintos agentes, útil en despliegues distribuidos.

### 2. Observabilidad en agentes

En software clásico (APM), la ruta del código está predefinida. En IA Agéntica, el flujo de control es probabilístico y lo decide el LLM en tiempo real. La observabilidad es esencial para auditar *por qué* el agente tomó una decisión.

#### 2.1. Telemetría y Estandarización (OpenTelemetry)

*   **Trazas (*Traces*):** Reconstrucción del recorrido completo de una petición del usuario de extremo a extremo.
*   **Tramos (*Spans*):** Subdivisiones atómicas de la traza. Capturan:
    1.  El estado del *prompt* enviado.
    2.  El razonamiento intermedio.
    3.  La invocación de la herramienta (parámetros).
    4.  La respuesta de la herramienta (*Observation*).

#### 2.2. Diferenciación Conceptual de Examen

| Concepto | Finalidad | Pregunta que responde |
| :--- | :--- | :--- |
| **Monitorización** | Vigilar estado y alertas (Latencia, caídas). | ¿Está fallando el sistema? |
| **Observabilidad** | Telemetría profunda (Trazas, *Spans*). | ¿Por qué el sistema tomó esta ruta? |
| **Auditoría (Art. 12 AI Act)** | Revisión formal con evidencias de los logs. | ¿Cumplió las políticas y responsabilidades legales? |

#### 2.3. Métricas Específicas de Agentes

*   **Consumo de Tokens / Coste:** Los agentes iteran en bucle, el coste se multiplica exponencialmente por cada paso de razonamiento.
*   **Tasa de uso de herramientas y Tasa de fallo de herramientas.**
*   **Detección de Bucles Infinitos (*Infinite Tool Loop*):** El agente llama repetidamente a la misma herramienta sin lograr avanzar. Requiere mecanismos de corte (*Circuit Breakers* / *Timeouts*).

### 3. Ingeniería de prompts (*Prompt Engineering*)

Para el perfil de Gobierno (P02), el *Prompt Engineering* no es optimizar respuestas, es **diseñar instrucciones operativas como un mecanismo de control de seguridad (Guardrails)**. Un *prompt* en producción debe versionarse y tratarse como código fuente crítico.

#### 3.1. Arquitectura de Prompts en Agentes

*   **System Prompt:** Instrucciones persistentes de alto nivel con máxima prioridad de atención en el modelo. Fija las reglas inmutables de seguridad y el marco de actuación.
*   **User Prompt:** La entrada del ciudadano/usuario, que nunca debe tener precedencia sobre el *System Prompt*.
*   **Técnicas Clave:**
    *   **Chain-of-Thought (CoT):** Obliga al modelo a desglosar el razonamiento paso a paso. *Valor en P02:* Proporciona **explicabilidad** a la decisión para auditorías posteriores.
    *   **ReAct (*Reasoning and Acting*):** Interrumpe la inferencia pura y estructura el bucle en `Pensamiento -> Acción (Llamada a Herramienta) -> Observación`. Es la base operativa del comportamiento agéntico.

#### 3.2. Riesgos de Seguridad Críticos (OWASP Top 10 LLMs)

*   **Inyección de Prompts Directa (*Jailbreak*):** El usuario introduce comandos para eludir los *Guardrails*.
*   **Inyección de Prompts Indirecta (*Indirect Prompt Injection*):** El mayor riesgo en la Administración. El atacante esconde instrucciones maliciosas en un PDF o web externa. El agente autónomo consulta el PDF (herramienta de lectura), el LLM asimila el texto oculto como una instrucción legítima y ejecuta acciones no autorizadas (ej. extraer datos de otros expedientes).

### 4. AgentOps

**AgentOps** es la evolución operativa. Combina MLOps (modelos), LLMOps (prompts/generación) y DevOps, centrándose en gobernar el **ciclo de vida de las trayectorias de decisión autónomas**.

#### 4.1. Funciones de Gobernanza en AgentOps

*   **Gestión del Cambio y Versionado:** Un cambio en el *System Prompt* o la adición de una nueva herramienta altera radicalmente el perfil de riesgo del agente. Requiere *pipelines* de CI/CD con evaluaciones automatizadas.
*   **Evaluación Dinámica (*Agent Evaluation*):** A diferencia de un LLM que se evalúa por similitud de texto (*BLEU/ROUGE*), un agente se evalúa por:
    *   *Task Success Rate:* ¿Consiguió el objetivo final?
    *   *Trajectory Score:* ¿Fueron los pasos elegidos lógicos, óptimos y seguros?
*   **Control de Autonomía y Supervisión (HITL):** Implementación técnica de puntos de control donde el agente se detiene y exige aprobación humana (*Human-in-the-loop*) antes de ejecutar una acción destructiva o con impacto legal (ej. enviar una notificación formal).
*   **Prevención de Denegación de Cartera (*Denial of Wallet*):** Mecanismos para detener a un agente si sus llamadas a APIs de pago o consumo de tokens exceden el presupuesto asignado por error o por un ataque adversario.

## Conceptos que suelen preguntarse

| Concepto a distinguir | Realidad Técnica y Operativa | Distractor Típico en Examen |
| :--- | :--- | :--- |
| **Agente vs. Chatbot** | El agente decide y ejecuta acciones. El chatbot solo conversa. | "Un chatbot basado en LLM es automáticamente un agente de IA". |
| **Memoria vs. Ventana de Contexto** | Memoria (ej. BBDD Vectorial) retiene datos entre sesiones. Ventana de Contexto es el límite de tokens por llamada. | "Ampliar la ventana de contexto crea una memoria semántica persistente infinita". |
| **CoT vs. ReAct** | CoT es razonamiento interno en texto. ReAct interrumpe para interactuar con herramientas externas. | "CoT y ReAct son sinónimos técnicos y siempre llaman a APIs". |
| **Inyección Indirecta de Prompts** | El ataque proviene de los datos ingeridos (documentos, webs) leídos por el agente de forma autónoma. | "La inyección indirecta solo ocurre cuando el administrador teclea mal el prompt". |
| **Trazas vs. Logs** | Las Trazas reconstruyen la relación causal del flujo completo (*Spans*). Los logs son eventos discretos estáticos. | "Guardar un fichero plano de logs garantiza el 100% de la explicabilidad del modelo". |

## Posibles preguntas tipo test

**Pregunta 1.** Desde la perspectiva del gobierno de la IA, ¿por qué la vulnerabilidad conocida como "Inyección Indirecta de Prompts" (*Indirect Prompt Injection*) representa un riesgo crítico de seguridad operativo específico para los agentes de IA?
A. Porque altera físicamente los pesos sinápticos del modelo fundacional durante el entrenamiento.
B. Porque explota la capacidad autónoma del agente de leer y asimilar información de fuentes externas (ej. documentos web o correos), que contienen comandos ocultos diseñados para subvertir las políticas del sistema.
C. Porque requiere que el atacante posea credenciales de administrador de la plataforma cloud.
D. Porque eleva la temperatura estocástica del modelo, obligándolo a generar salidas deterministas.
**Respuesta correcta: B.** (La inyección indirecta utiliza las propias herramientas de lectura del agente en contra de las políticas de su orquestador).

**Pregunta 2.** De acuerdo con el Reglamento (UE) 2024/1689 (Ley de IA), los sistemas de alto riesgo deben garantizar la trazabilidad de su funcionamiento a lo largo de su ciclo de vida. En el marco de la disciplina emergente 'AgentOps', ¿qué mecanismo técnico proporciona la instrumentación adecuada para cumplir este requisito registrando el razonamiento y las llamadas a herramientas?
A. La reducción de la dimensionalidad de los Embeddings.
B. La implementación exclusiva de métricas de uso de CPU y RAM del servidor.
C. La telemetría estructurada mediante Trazas (*Traces*) y Tramos (*Spans*), capturando el estado del prompt, el pensamiento y las acciones paso a paso.
D. El uso de validadores sintácticos de bases de datos relacionales tradicionales.
**Respuesta correcta: C.** (La observabilidad profunda mediante trazas desglosa el comportamiento de "caja negra" en eventos secuenciales auditables).

**Pregunta 3.** Al diseñar la gobernanza y los límites de actuación de un agente de IA en una Administración Pública, la incorporación del patrón técnico HITL (*Human-in-the-loop*) en el flujo de orquestación tiene como finalidad principal:
A. Reentrenar el modelo de lenguaje en tiempo real utilizando las respuestas corregidas por el usuario final.
B. Eliminar el coste económico de los tokens al derivar la inferencia al operador humano.
C. Establecer una validación y aprobación humana explícita antes de que el sistema autónomo ejecute una acción irreversible, con impacto jurídico o alto riesgo operativo.
D. Mejorar exclusivamente la métrica de Perplejidad del modelo base.
**Respuesta correcta: C.** (HITL es el control clave para acotar la autonomía en procesos sensibles).

**Pregunta 4.** ¿Cuál de las siguientes afirmaciones describe con mayor precisión la diferencia conceptual entre la "Observabilidad" de un agente de IA y la "Monitorización" clásica de la infraestructura subyacente?
A. No existe diferencia funcional en entornos multiagente descentralizados.
B. La Monitorización se centra en alertar sobre el estado de los componentes (ej. caídas, saturación); la Observabilidad permite investigar las causas profundas y reconstruir el "por qué" de una trayectoria de decisiones del sistema probabilístico.
C. La Observabilidad se utiliza exclusivamente para facturar los costes de las licencias SaaS; la Monitorización para el control de la red.
D. La Monitorización es un requisito de AgentOps, mientras que la Observabilidad solo se exige en bases de datos SQL tradicionales.
**Respuesta correcta: B.** (La observabilidad aporta el contexto causal del comportamiento estocástico del agente).

**Pregunta 5.** En la evaluación dinámica de agentes autónomos (*AgentOps*), a diferencia de las métricas puramente lingüísticas empleadas en la evaluación de LLMs estáticos, se introducen métricas que evalúan la calidad de la planificación. ¿Cuál es un indicador clave para medir la pertinencia de las decisiones tomadas por el agente?
A. La evaluación de la trayectoria (*Trajectory Score*), que analiza si los pasos y herramientas elegidas fueron lógicos y seguros para alcanzar la meta.
B. El cálculo de la Complejidad Ciclomática del código fuente del orquestador Python.
C. La comprobación del hash criptográfico de la imagen Docker desplegada en Kubernetes.
D. El conteo total del vocabulario del tokenizador (Byte-Pair Encoding).
**Respuesta correcta: A.** (En agentes importa tanto el resultado final como los medios empleados para llegar a él).

## Normativa o fuentes relacionadas

*   **Reglamento (UE) 2024/1689 (Ley de IA):** Artículos relativos a definiciones de sistemas de IA, obligaciones de registro automático de acontecimientos (*logging*) en sistemas de alto riesgo (Art. 12) y requisitos de supervisión humana (Art. 14).
*   **Esquema Nacional de Seguridad (RD 311/2022):** Principios básicos de protección, gestión de riesgos, registro de actividad y mínimo privilegio, esenciales para el diseño seguro de herramientas agénticas en el sector público.
*   **OWASP Top 10 for LLM Applications:** Documentación técnica referente para la ciberseguridad en IA, detallando amenazas críticas como la inyección indirecta de prompts (LLM01) y el diseño inseguro de *plugins*/herramientas (LLM07).
*   **NIST AI RMF 1.0 y NIST AI 600-1 (Generative AI Profile):** Marcos voluntarios de gestión de riesgos de IA, útiles para estructurar el gobierno y la confianza en sistemas generativos.
*   **OpenTelemetry Documentation:** Estándar y convenciones semánticas para la instrumentación de trazas, métricas y logs en aplicaciones de IA generativa.

## Dudas o puntos pendientes

*   **Estatus Normativo de "AgentOps":** Es vital recordar que *AgentOps* es una disciplina de ingeniería y operación emergente de la industria, **no una norma ISO/IEC oficial ni un estándar legal**. El AI Act regula el riesgo del "Sistema de IA", independientemente de si la industria lo etiqueta comercialmente como "agente", "workflow" o "chatbot".
*   **MCP y A2A:** El *Model Context Protocol* y los protocolos *Agent-to-Agent* son especificaciones técnicas abiertas impulsadas por fabricantes en rápida evolución. Deben estudiarse como patrones de integración, asumiendo que su adopción no exime de cumplir las políticas corporativas tradicionales de IAM (Gestión de Identidad y Accesos) y seguridad de red de la Administración.