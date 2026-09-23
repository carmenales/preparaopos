---
title: OWASP MCP Top 10 (Model Context Protocol)
---

# OWASP MCP Top 10

El **OWASP MCP Top 10** es un marco de seguridad creado por la comunidad para abordar los desafíos únicos que surgen al utilizar el **Model Context Protocol (MCP)**. El MCP es un estándar abierto que permite a los asistentes de IA (clientes) conectarse de forma segura con fuentes de datos y herramientas externas (servidores MCP).


## Objetivo

A medida que las organizaciones conectan sus LLMs y agentes a bases de datos, repositorios de código y sistemas internos mediante MCP, la superficie de ataque cambia drásticamente. El objetivo de esta guía es proporcionar a desarrolladores y arquitectos las mejores prácticas para asegurar estas conexiones bidireccionales, evitando que un servidor MCP se convierta en una puerta trasera hacia la infraestructura crítica.


## Las 10 Vulnerabilidades Críticas en MCP

### MCP01: Mala Gestión de Tokens y Exposición de Secretos (Token Mismanagement & Secret Exposure)

Ocurre cuando las credenciales necesarias para que el servidor MCP acceda a sistemas backend se gestionan de forma insegura y quedan expuestas a través de la memoria del modelo o logs.

#### Riesgos
* Presencia de **credenciales hardcodeadas** o tokens de larga duración en la configuración del servidor MCP.
* El LLM o agente recupera **secretos de forma no intencionada** a través de la manipulación de prompts o trazas de depuración (*debug traces*).
* Exposición de variables de entorno al cliente MCP.

#### Mitigaciones
* Utilizar **credenciales de corta duración** y con alcance limitado (scoped).
* Integrar **controles de escaneo de secretos** y utilizar gestores de secretos (Vaults).
* Filtrar agresivamente las respuestas del servidor MCP para enmascarar cualquier API Key antes de enviarla al modelo.

### MCP02: Escalada de Privilegios por Ampliación de Alcance (Privilege Escalation via Scope Creep)

Se produce cuando a los servidores MCP se les otorgan permisos genéricos o excesivos que, con el tiempo, permiten a los agentes realizar acciones destructivas no previstas.

#### Riesgos
* Un agente diseñado solo para leer código termina utilizando el servidor MCP para **modificar repositorios** o exfiltrar datos.
* Permisos temporales que **nunca se revocan** y se acumulan.
* Falta de separación de roles entre diferentes servidores MCP.

#### Mitigaciones
* Enforzar un diseño de **mínimo privilegio absoluto** (solo lectura si no necesita escritura).
* Configurar la **expiración automática de alcances (*scopes*)**.
* Realizar revisiones de acceso estrictas sobre los servidores MCP periódicamente.

### MCP03: Envenenamiento de Herramientas (Tool Poisoning)

Surge cuando un adversario compromete las herramientas o plugins subyacentes de los que depende el modelo para interactuar con su entorno.

#### Riesgos
* **Ataques de "Rug Pull"**: Actualizaciones maliciosas a herramientas previamente confiables.
* **Envenenamiento de esquema (*Schema Poisoning*)**: Corromper las definiciones de las interfaces de las herramientas para engañar al modelo y que actúe de forma errónea.
* **Tool shadowing**: Introducir herramientas duplicadas o falsas para interceptar las llamadas legítimas del agente.

#### Mitigaciones
* **Validar estrictamente los esquemas** de entrada y salida de cada herramienta.
* Monitorear los registros de cambios en las dependencias de los plugins.
* Asegurar las vías de distribución de las herramientas internas.

### MCP04: Ataques a la Cadena de Suministro y Manipulación de Dependencias (Software Supply Chain Attacks & Dependency Tampering)

Los ecosistemas MCP dependen de una multitud de conectores open-source y plugins del lado del modelo que pueden estar comprometidos.

#### Riesgos
* Descargar un **servidor MCP de la comunidad** que contiene un backdoor o componente malicioso.
* Un atacante altera el comportamiento del agente mediante **dependencias envenenadas**.

#### Mitigaciones
* Exigir el uso de **componentes firmados digitalmente**.
* Implementar **monitoreo de dependencias (SCA)**.
* Mantener un seguimiento de la procedencia (Provenance tracking) para todos los módulos MCP.

### MCP05: Inyección y Ejecución de Comandos (Command Injection & Execution)

Sucede cuando los datos procesados por el servidor MCP (provenientes del cliente de IA) se pasan directamente a la terminal o al sistema sin la sanitización adecuada.

#### Riesgos
* Un prompt malicioso engaña al LLM para que envíe un **argumento con comandos del SO** (ej. `; rm -rf /`) a la herramienta del servidor MCP.
* Lograr **Ejecución Remota de Código (RCE)** explotando binarios del sistema (como `git` o herramientas CLI).

#### Mitigaciones
* **Nunca concatenar** la entrada generada por la IA directamente en comandos de shell.
* Validar los argumentos de las herramientas contra **listas blancas estrictas**.
* Ejecutar el servidor MCP en contenedores sin privilegios.

### MCP06:2025 - Subversión del Flujo de Intención (Intent Flow Subversion)

Ocurre cuando instrucciones maliciosas se incrustan dentro del contexto recuperado (documentos, esquemas o salidas de herramientas), alterando la ruta crítica donde el agente traduce la petición del usuario en acciones. 

> A diferencia de una inyección directa, esto sucede "en flujo": el modelo lee un recurso externo con instrucciones ocultas que anulan y secuestran el objetivo original.

#### Riesgos
* **Secuestro del Objetivo (*Goal Hijacking*):** El agente persigue un objetivo totalmente distinto al del usuario (ej. en lugar de "resumir logs", decide "exfiltrar logs" a un servidor externo).
* **Acciones Autónomas No Autorizadas:** El agente utiliza sus herramientas MCP conectadas para realizar acciones destructivas (ej. borrar repositorios o modificar configuraciones en la nube).
* **Persistencia Sigilosa:** Los atacantes inyectan "meta-instrucciones" en contextos MCP de larga duración que alteran el comportamiento del agente a lo largo de múltiples sesiones desconectadas.

#### Mitigaciones
* **Integridad del Flujo y Anclaje Semántico:** "Anclar" explícitamente el objetivo original del usuario en el prompt del sistema y requerir que el modelo evalúe si su siguiente acción es coherente con dicho objetivo (usando un Punto de Decisión de Políticas o PDP).
* **Verificación Independiente (*The Checker Pattern*):** Utilizar un modelo "Guardrail" (barrera de seguridad) separado e independiente que solo evalúe la *Intención del Usuario* frente a la *Acción Propuesta*, manteniéndolo completamente aislado del contexto MCP potencialmente envenenado.
* **Sanitización y Etiquetado Estricto de Contexto:** Tratar todo el texto proveniente de recursos MCP como no confiable por defecto. Usar etiquetas de metadatos (como `[UNTRUSTED_CONTEXT]`) para instruir al modelo a tratar ese contenido exclusivamente como datos pasivos, nunca como comandos ejecutables.
* **Detección Activa de Deriva (*Drift Detection*):** Monitorizar la "deriva de intención" a lo largo del tiempo. Si el plan del agente se desvía del objetivo original, pausar automáticamente la sesión y requerir validación humana (*Human-in-the-Loop*).

### MCP07: Autenticación y Autorización Insuficientes (Insufficient Authentication & Authorization)

Aparece cuando los servidores MCP se exponen en la red local o en la nube sin controles de identidad fuertes, asumiendo erróneamente que solo el cliente de IA legítimo los consumirá.

#### Riesgos
* Atacantes en la misma red **suplantan al cliente de IA** y realizan consultas directamente al servidor MCP.
* Falta de controles de autorización granulares (el servidor MCP no verifica qué usuario humano inició la petición).

#### Mitigaciones
* Implementar **autenticación fuerte** entre el cliente y el servidor MCP (ej. tokens criptográficos o mTLS).
* Asegurar que el contexto del **usuario humano se propague** hasta el servidor MCP para validar sus permisos reales.

### MCP08: Falta de Auditoría y Telemetría (Lack of Audit and Telemetry)

Se da cuando los sistemas MCP operan en "caja negra", sin dejar rastro de qué información se transmitió o qué herramientas se invocaron.

#### Riesgos
* Incapacidad para realizar **análisis forense** tras un incidente de exfiltración de datos.
* Los atacantes abusan de las herramientas conectadas de forma silenciosa sin disparar ninguna alarma.

#### Mitigaciones
* Implementar un **registro estandarizado (logging)** de todas las llamadas a herramientas y cargas útiles del contexto (cuidando de no registrar PII).
* Monitorear y generar **alertas de seguridad (SIEM)** sobre patrones de acceso anómalos o volúmenes de datos inusuales.

### MCP09: Servidores MCP en la Sombra (Shadow MCP Servers)

Surge cuando los empleados y desarrolladores despliegan sus propios conectores MCP (locales o en la nube) para conectar herramientas de IA corporativas a sus flujos de trabajo sin la aprobación de TI.

#### Riesgos
* Exposición de bases de datos internas a través de **servidores no securizados**.
* Pérdida total del **gobierno de los datos (Data Governance)**.
* Vulnerabilidades sistémicas introducidas por configuraciones "caseras" sin parchear.

#### Mitigaciones
* Implementar descubrimiento y **monitorización de red** para detectar tráfico de protocolos MCP no autorizados.
* Utilizar **listas blancas (allow-listing)** en los clientes corporativos de IA para restringir las conexiones solo a servidores MCP aprobados.

### MCP10: Inyección de Contexto y Sobre-Compartición (Context Injection & Over-Sharing)

Se produce cuando un servidor MCP devuelve más información de la estrictamente necesaria, contaminando el contexto del LLM con datos irrelevantes, PII o información confidencial cruzada.

#### Riesgos
* El LLM ingiere información de múltiples inquilinos (multitenancy) o de recursos de otros usuarios, provocando **fugas de datos en sus respuestas**.
* Aumento de la superficie de ataque, ya que el modelo tiene "demasiado contexto" que puede ser manipulado.

#### Mitigaciones
* Implementar el principio de **necesidad de conocer (Need-to-Know)** en las respuestas del servidor MCP.
* Aplicar **filtrado de salida (*egress filtering*)** para sanitizar o redactar PII, números de tarjetas y contraseñas antes de empaquetar el contexto hacia el cliente de IA.


## Tabla Resumen (MCP Top 10)

| ID | Riesgo (Categoría) | Palabra Clave / Concepto | Defensa / Mitigación Principal |
|:---|:---|:---|:---|
| **MCP01** | Mala Gestión de Tokens | Credenciales hardcodeadas, fuga en memoria. | Tokens cortos, Vaults, enmascaramiento de APIs. |
| **MCP02** | Escalada de Privilegios | Scope creep, permisos que se acumulan. | Mínimo privilegio, expiración de scopes. |
| **MCP03** | Envenenamiento de Herramientas | Rug pulls, schema poisoning, shadow tools. | Validación de esquemas, asegurar herramientas. |
| **MCP04** | Cadena de Suministro | Conectores MCP maliciosos, dependencias. | Firmas digitales, SBOM, rastreo de procedencia. |
| **MCP05** | Inyección de Comandos | RCE a través de herramientas, ejecución CLI. | No concatenar shell, listas blancas de argumentos. |
| **MCP06** | Subversión del Flujo de Intención | Goal Hijacking, inyección en flujo (contexto). | Anclaje semántico, Checker Pattern (Guardrail), etiquetas de contexto. |
| **MCP07** | Autenticación Insuficiente | Servidor MCP expuesto a clientes no autorizados. | mTLS, propagación de identidad del usuario. |
| **MCP08** | Falta de Auditoría | Visibilidad nula (Caja negra), falta de logs. | Logs estandarizados sin PII, integración con SIEM. |
| **MCP09** | Servidores MCP en la Sombra | Conectores "caseros" locales (Shadow AI). | Monitorización de red, listas blancas (Allow-list). |
| **MCP10** | Sobre-Compartición de Contexto | Devolver PII o datos excesivos al LLM. | Egress filtering, principio "Need-to-Know". |


## Bibliografía
* [OWASP MCP Top 10](https://owasp.org/www-project-mcp-top-10/)
