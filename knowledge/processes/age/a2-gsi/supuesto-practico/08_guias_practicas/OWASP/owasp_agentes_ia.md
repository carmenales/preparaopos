---
title: OWASP Top 10 Aplicaciones Agénticas
---

# 🤖 OWASP Top 10 para Aplicaciones Agénticas (2026)

El **OWASP Top 10 for Agentic Applications 2026** es un marco de seguridad creado por el Proyecto GenAI Security de OWASP. Surge como evolución directa del ecosistema LLM, centrándose específicamente en los riesgos que aparecen cuando dotamos a los modelos de IA de autonomía, acceso a herramientas, memoria y capacidad de interactuar con otros sistemas.

## Objetivo

Proporcionar a los desarrolladores, equipos de seguridad y líderes de IA un lenguaje común y una guía práctica para proteger los flujos de trabajo autónomos (sistemas multi-agente). Su meta es pasar de asegurar simples cajas de texto (prompts) a asegurar agentes que pueden planificar, delegar y ejecutar acciones en nombre del usuario.


## Las 10 Vulnerabilidades Críticas en Agentes (ASI)

### ASI01: Secuestro del Objetivo del Agente (Agent Goal Hijack)

Ocurre cuando un atacante manipula o engaña al agente de IA para que cambie su objetivo principal, desvíe su toma de decisiones o siga instrucciones maliciosas ocultas.

#### Riesgos
* **Alteración de los objetivos** a través de inyecciones de instrucciones (indirect prompt injection) ocultas en documentos, correos electrónicos o webs externas.
* Ejecución de **acciones no deseadas** que desvían la planificación y el comportamiento autónomo original del agente.
* Exfiltración de datos al convencer al agente de que su "nueva misión" es enviar información a un servidor externo.

#### Mitigaciones
* Tratar **todo el lenguaje natural como no confiable** y aplicar filtros estrictos de validación de entrada/salida.
* Requerir **aprobación humana (*Human-in-the-loop*)** para cualquier acción de alto impacto o cambio de objetivo.
* Usar patrones como la **"Cápsula de Intención" (*Intent Capsule*)**, un envoltorio inmutable que obliga al agente a recordar su mandato original en cada ciclo de ejecución.

### ASI02: Uso Indebido y Explotación de Herramientas (Tool Misuse & Exploitation)

Se produce cuando un agente emplea las herramientas legítimas a su disposición (acceso a bases de datos, APIs externas, envío de emails) de forma insegura o no prevista, provocando daños.

#### Riesgos
* Realizar llamadas a herramientas con **parámetros destructivos** (ej. borrar registros) debido a instrucciones ambiguas del usuario o manipulación externa.
* Encadenar herramientas en **secuencias inesperadas** que culminan en la pérdida de información o exposición de secretos.
* Uso de herramientas sobreprivilegiadas en entornos de producción.

#### Mitigaciones
* Aplicar un **alcance estricto de permisos (*scoping*)** y el principio de "Mínima Agencia" para cada herramienta.
* Ejecutar las herramientas en **entornos aislados (*sandboxing*)**.
* Implementar **validación de argumentos** y controles de políticas de seguridad en cada invocación de la herramienta.

### ASI03: Abuso de Identidad y Privilegios (Identity & Privilege Abuse)

Sucede cuando un agente asume permisos excesivos o utiliza credenciales de forma inadecuada para realizar acciones que superan su nivel de autorización estricto.

#### Riesgos
* Un agente "toma prestados" **permisos de un usuario administrador** para ejecutar tareas de lectura/escritura que no debería poder hacer por sí solo.
* **Escalada de privilegios** dentro de un ecosistema donde múltiples agentes colaboran.
* Uso de tokens obsoletos o compartidos entre diferentes sesiones.

#### Mitigaciones
* Adoptar el principio de **Mínima Agencia (*Least Agency*)** y mínimo privilegio.
* Asignar **identidades distintas y trazables** a cada agente de forma independiente al usuario humano que los invoca.
* Monitorizar la **herencia de credenciales** a lo largo de los flujos de trabajo multi-agente.

### ASI04: Vulnerabilidades en la Cadena de Suministro Agéntica (Agentic Supply Chain Vulnerabilities)

Surge de los riesgos introducidos por depender de agentes de terceros, herramientas externas, modelos bases o plantillas que pueden ser maliciosos o estar comprometidos.

#### Riesgos
* Uso de **plugins o servidores MCP (Model Context Protocol)** de fuentes externas no confiables o envenenadas.
* Inserción de código malicioso o alteración de los flujos de trabajo agénticos en tiempo de ejecución.
* Heredar vulnerabilidades de repositorios de "habilidades" (skills) públicas de agentes.

#### Mitigaciones
* Validar la **integridad y el comportamiento** de todos los componentes cargados dinámicamente.
* Llevar un inventario exhaustivo o **Lista de Materiales de Software (SBOM)** adaptada al flujo agéntico.
* Verificar **firmas digitales y manifiestos** de plugins, herramientas y modelos antes de su uso.

### ASI05: Ejecución de Código Inesperada (Unexpected Code Execution - RCE)

Ocurre cuando la capacidad del agente para generar y ejecutar código (por ejemplo, para resolver un problema de análisis de datos o desarrollo) es explotada para ejecutar comandos hostiles.

#### Riesgos
* **Inyección directa** de comandos del sistema operativo (RCE) procesados por el agente como instrucciones legítimas.
* El agente genera comandos de consola de forma autónoma (ej. *vibe coding runaway*) que accidentalmente **borran o alteran entornos de producción**.

#### Mitigaciones
* Confinar la ejecución de código generado por IA a **entornos altamente restringidos (contenedores efímeros o máquinas virtuales sin red)**.
* Aplicar **evaluación y revisión estricta (*Human-in-the-loop*)** antes de la ejecución de comandos que afecten al sistema subyacente.

### ASI06: Envenenamiento de Memoria y Contexto (Memory & Context Poisoning)

Se da cuando se introduce información maliciosa, sesgada o falsa en la memoria a corto o largo plazo del agente (como en sus bases de datos vectoriales - RAG), afectando sus decisiones futuras.

#### Riesgos
* El agente toma **decisiones peligrosas o sesgadas** basándose en un contexto que ha sido manipulado previamente por un atacante.
* "Plantado" de datos (*data planting*) para comprometer interacciones futuras de otros usuarios que consultan la misma base de conocimiento.

#### Mitigaciones
* Rastrear y validar todas las **operaciones de escritura en la memoria** del agente con atribución clara de origen.
* Aislar o **segmentar la memoria y las bases vectoriales** por usuario y sesión para evitar la contaminación cruzada entre contextos.

### ASI07: Comunicación Insegura entre Agentes (Insecure Inter-Agent Communication)

Radica en la falta de autenticación o cifrado cuando múltiples agentes autónomos intercambian información, negocian o se delegan tareas entre sí en una red (*Multi-Agent Systems*).

#### Riesgos
* **Suplantación de identidad (*spoofing*)** de un agente hacia otro (hacerse pasar por el "Agente Financiero" para obtener datos).
* **Intercepción o alteración de mensajes** en flujos donde los agentes colaboran para resolver un problema complejo.

#### Mitigaciones
* Implementar **autenticación y cifrado riguroso (ej. mTLS)** en todas las comunicaciones y APIs entre agentes.
* **Validar de forma cruzada el origen y la integridad** de los datos o instrucciones delegadas por otros agentes.

### ASI08: Fallos en Cascada (Cascading Failures)

Se produce cuando un único error o comportamiento anómalo se propaga y amplifica rápidamente a través de una red de agentes interconectados, causando un colapso sistémico.

#### Riesgos
* **Bucles infinitos (*self-looping*)** donde los agentes intentan corregirse a sí mismos sin éxito tras un fallo, consumiendo cuotas de API y memoria.
* Errores iniciales de un agente que generan **consecuencias destructivas en cadena** en otros sistemas posteriores de la arquitectura.

#### Mitigaciones
* Analizar los flujos de ejecución y telemetría para habilitar la **detección de bucles (*self-looping detection*)**.
* Implementar **cortacircuitos (*circuit breakers*)** y límites de ejecución (cuotas/tiempos máximos) para detener la propagación del fallo.

### ASI09: Explotación de la Confianza Humano-Agente (Human-Agent Trust Exploitation)

Involucra el uso de la naturaleza persuasiva, conversacional y antropomórfica de los agentes de IA para manipular a los usuarios humanos hacia la realización de acciones inseguras.

#### Riesgos
* Uso del agente como vehículo para realizar **ingeniería social o phishing altamente personalizado** contra el propio usuario.
* El agente da recomendaciones maliciosas presentadas con un "tono de autoridad", provocando que **el usuario confíe ciegamente** en datos perjudiciales.

#### Mitigaciones
* Evaluar y filtrar sistemáticamente las respuestas de la IA para detectar **lenguaje manipulador o intentos de persuasión**.
* Implementar **indicadores visuales claros** de que el usuario está interactuando con IA y no asumir la veracidad de la salida sin cruzarla con las políticas de riesgo de la organización.

### ASI10: Agentes Rebeldes o Comprometidos (Rogue Agents)

Describe situaciones donde un agente, debido a un compromiso externo o a una desviación prolongada de su modelo ("drift"), actúa de manera perjudicial o persigue metas engañosas fuera de su alcance original.

#### Riesgos
* El agente **persiste en el sistema de forma oculta**, exfiltrando datos corporativos de manera gradual sin levantar sospechas.
* Comportamientos maliciosos que emergen debido a la **deriva de comportamiento (*behavioral drift*)** no controlada a lo largo de interacciones sostenidas.

#### Mitigaciones
* Implementar **barreras de seguridad (*guardrails*) en tiempo de ejecución** para evaluar la respuesta y bloquear patrones de acción fuera de la política predefinida.
* Analizar las trazas de ejecución en busca de anomalías para **detectar desviaciones de comportamiento** a lo largo del tiempo antes de que actúen.



## Tabla Resumen (Agentic Top 10 2026)

| ID | Riesgo (Categoría) | Palabra Clave / Concepto | Defensa / Mitigación Principal |
|:---|:---|:---|:---|
| **ASI01** | Secuestro del Objetivo | Prompt injection indirecto, desvío de meta. | Cápsula de intención, Human-in-the-loop. |
| **ASI02** | Uso Indebido de Herramientas | Parámetros destructivos en llamadas a APIs. | Scoping de herramientas, validación, Sandboxing. |
| **ASI03** | Abuso de Identidad y Privilegios | Escalada de permisos, robo de credenciales. | Mínima Agencia, identidades separadas para agentes. |
| **ASI04** | Vuln. en Cadena de Suministro | Plugins maliciosos, servidores MCP comprometidos. | Componentes firmados, SBOM de IA. |
| **ASI05** | Ejecución de Código Inesperada | RCE, Vibe coding runaway, comandos de OS. | Ejecución en entornos asilados/contenedores efímeros. |
| **ASI06** | Envenenamiento de Memoria | Manipulación de bases de datos vectoriales / RAG. | Segmentación de memoria por sesión/usuario. |
| **ASI07** | Comunicación Inter-Agente Insegura | Spoofing entre agentes, falta de cifrado. | Cifrado mTLS, validación cruzada de identidad. |
| **ASI08** | Fallos en Cascada | Self-looping, colapso sistémico amplificado. | Circuit breakers (cortacircuitos), detección de bucles. |
| **ASI09** | Explotación de Confianza Humana | Ingeniería social vía IA, antropomorfismo. | Filtrado de persuasión, alertas de riesgo para el usuario. |
| **ASI10** | Agentes Rebeldes (Rogue) | Persistencia no detectada, behavioral drift. | Guardrails en tiempo de ejecución, monitorización de deriva. |

## Bibliografía
* [OWASP Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)