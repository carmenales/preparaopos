---
title: OWASP Top 10 para Aplicaciones LLM
---

# 🧠 OWASP Top 10 para LLMs

El **OWASP Top 10 para Aplicaciones LLM** es el estándar de seguridad diseñado específicamente para abordar los riesgos únicos que surgen al integrar modelos de lenguaje masivo (como GPT, Claude o Llama) en aplicaciones corporativas.

## Objetivo

Ayudar a desarrolladores, científicos de datos y equipos de seguridad a identificar y mitigar las vulnerabilidades críticas en el ciclo de vida de la IA Generativa, desde la ingesta de datos y el entrenamiento, hasta la interacción del modelo con los usuarios y los sistemas de backend.


## Las 10 Vulnerabilidades Críticas en LLMs

### LLM01:2025 - Inyección de Prompts (Prompt Injection)

Ocurre cuando un atacante manipula las entradas del LLM mediante instrucciones engañosas para saltarse los filtros de seguridad o alterar el comportamiento previsto.

#### Riesgos
* **Inyección Directa (*Jailbreak*):** El usuario introduce un prompt diseñado para sobrescribir las instrucciones del sistema.
* **Inyección Indirecta:** El LLM ingiere contenido malicioso de fuentes externas (ej. resume una web que contiene instrucciones ocultas).

#### Mitigaciones
* Separar estrictamente las instrucciones del sistema del contenido del usuario.
* Aplicar **filtros de entrada/salida** (moderación de contenido).
* Tratar las respuestas del LLM como **datos no confiables**.

### LLM02:2025 - Divulgación de Información Sensible (Sensitive Information Disclosure)

El LLM revela involuntariamente datos confidenciales, secretos corporativos o información personal (PII) a través de sus respuestas.

#### Riesgos
* **Memorización de datos:** El modelo aprendió contraseñas o PII durante el entrenamiento y las repite ante ciertos estímulos.
* Devolución de **datos cruzados** entre usuarios en arquitecturas multi-tenant sin filtros adecuados.

#### Mitigaciones
* **Sanitizar/Redactar** exhaustivamente los datos antes de introducirlos en el entrenamiento o en el prompt.
* Implementar **políticas de filtrado a la salida** para detectar y bloquear la fuga de PII/secretos.

### LLM03:2025 - Cadena de Suministro (Supply Chain)

Deriva de la dependencia de componentes de terceros, incluyendo modelos preentrenados, conjuntos de datos (*datasets*) o plugins comprometidos.

#### Riesgos
* Descargar un modelo open-source desde plataformas públicas (ej. Hugging Face) que contiene **código malicioso oculto**.
* Filtraciones de datos o vulnerabilidades al usar plugins de proveedores no confiables.

#### Mitigaciones
* Exigir la **Lista de Materiales de Software para IA (AI-SBOM)** y firmar criptográficamente los modelos.
* Utilizar exclusivamente modelos, plugins y conjuntos de datos de **proveedores confiables y verificados**.

### LLM04:2025 - Envenenamiento de Datos y del Modelo (Data and Model Poisoning)

Consiste en la manipulación de los datos o procesos de entrenamiento (o fine-tuning) del modelo para introducir vulnerabilidades, sesgos o puertas traseras.

#### Riesgos
* Atacantes inyectan **ejemplos tóxicos o sesgados** en los datos de entrenamiento.
* El modelo aprende a emitir información falsa o maliciosa bajo ciertos estímulos ocultos (backdoors).

#### Mitigaciones
* Validar rigurosamente la **procedencia e integridad de las fuentes de datos** de entrenamiento.
* Utilizar técnicas de **limpieza de datos** (*data sanitization*) y monitorizar el comportamiento del modelo continuamente.

### LLM05:2025 - Manejo Inadecuado de Salidas (Improper Output Handling)

Se produce cuando un componente o sistema *downstream* confía ciegamente en la salida generada por el LLM sin validarla ni sanearla.

#### Riesgos
* Ejecución de código remoto (**RCE**), Cross-Site Scripting (**XSS**) o Server-Side Request Forgery (**SSRF**).
* Elevación de privilegios si el LLM interactúa directamente con una terminal, navegador web o base de datos.

#### Mitigaciones
* Aplicar el modelo de **confianza cero (*Zero Trust*)** a todas las salidas del modelo.
* Validar, sanear y escapar rigurosamente el contenido generado antes de su ejecución o renderizado.

### LLM06:2025 - Agencia Excesiva (Excessive Agency)

Se produce cuando se otorga al LLM una capacidad de decisión y ejecución (funcionalidad, permisos o autonomía) que excede lo estrictamente necesario.

#### Riesgos
* El modelo toma decisiones destructivas (como borrar archivos o enviar correos en nombre del usuario) tras una alucinación o una inyección de prompts.
* **Impacto devastador** al combinar autonomía total con herramientas sobreprivilegiadas.

#### Mitigaciones
* Aplicar el **principio de mínimo privilegio** a las acciones que el modelo puede realizar (limitar el alcance de los plugins).
* Requerir **aprobación humana (*Human-in-the-Loop*)** para las operaciones de alto impacto antes de su ejecución.

### LLM07:2025 - Fuga del Prompt de Sistema (System Prompt Leakage)

Ocurre cuando los atacantes logran extraer las instrucciones fundamentales, directrices de comportamiento o contexto confidencial inyectado por los desarrolladores en el "System Prompt".

#### Riesgos
* **Robo de Propiedad Intelectual:** Revelar la lógica de negocio de la aplicación.
* Utilizar el conocimiento del prompt de sistema para diseñar ataques de *Jailbreak* mucho más precisos y efectivos.

#### Mitigaciones
* Implementar barreras (guardrails) específicas para **bloquear consultas de extracción** de instrucciones.
* Asumir que **el prompt de sistema no es un secreto** y no almacenar información confidencial o credenciales dentro de él.

### LLM08:2025 - Debilidades en Vectores y Embeddings (Vector and Embedding Weaknesses)

Involucra la manipulación o el acceso inseguro a las bases de datos vectoriales y a los modelos de embeddings, pilares fundamentales en las arquitecturas RAG (Generación Aumentada por Recuperación).

#### Riesgos
* Atacantes alteran los vectores para que búsquedas legítimas devuelvan **contextos maliciosos o envenenados**.
* Exposición de datos confidenciales si la base de datos vectorial no tiene controles de acceso granulares por usuario.

#### Mitigaciones
* Proteger el acceso a la base de datos vectorial con **autenticación y controles de acceso (RBAC) estrictos**.
* Validar y auditar el contenido antes de convertirlo en embeddings y almacenarlo.

### LLM09:2025 - Desinformación (Misinformation)

Se da cuando el modelo genera y difunde información falsa, alucinada o manipulada, y los usuarios confían ciegamente en ella.

>*Evolución de la antigua categoría "Overreliance"*. 

#### Riesgos
* Generación de **alucinaciones** (información falsa presentada como hecho) que perjudican la reputación de la empresa o causan daños a los usuarios.
* Producción de **código fuente inseguro** o vulnerable que los desarrolladores integran en producción sin revisar.

#### Mitigaciones
* Implementar mecanismos de **anclaje de datos (Grounding)** utilizando arquitecturas RAG fiables.
* Comunicar claramente a los usuarios las **limitaciones de la IA**, incluir avisos de advertencia y fomentar la validación cruzada.

### LLM10:2025 - Consumo Ilimitado (Unbounded Consumption)

Sucede cuando la infraestructura no restringe adecuadamente el uso del modelo, permitiendo el agotamiento de recursos.

> *Evolución de la antigua "Denegación de Servicio"*. 

#### Riesgos
* Peticiones inusualmente largas o complejas que saturan el servidor de inferencia (**Denegación de Servicio - DoS**).
* **Impacto financiero masivo** al agotar cuotas de APIs de pago por uso (ataques de denegación de billetera / *Denial of Wallet*).

#### Mitigaciones
* Implementar **límites de velocidad (*rate limiting*)** y restricción de recursos por usuario/IP.
* Establecer **topes estrictos** en el tamaño de las entradas (prompts) y en la cantidad máxima de tokens generados.


## Tabla Resumen (LLM Top 10 - 2025)

| ID | Riesgo (Categoría) | Palabra Clave / Concepto | Defensa / Mitigación Principal |
|:---|:---|:---|:---|
| **LLM01** | Inyección de Prompts | Jailbreak, inyección indirecta (contexto). | Separar instrucciones, filtros, tratar datos como no confiables. |
| **LLM02** | Fuga de Datos Sensibles | IA revela PII, memorización de contraseñas. | Sanitizar datos de entrada, filtrado estricto a la salida. |
| **LLM03** | Cadena de Suministro | Modelos/plugins de terceros comprometidos. | AI-SBOM, usar repositorios y proveedores verificados. |
| **LLM04** | Envenenamiento de Datos y Modelo | Backdoors en IA, manipulación de datasets. | Validar fuentes de origen, limpieza de datos (Sanitization). |
| **LLM05** | Manejo Inadecuado de Salidas | RCE o XSS por confiar en la salida de la IA. | Zero Trust, validación/sanitización en sistemas downstream. |
| **LLM06** | Agencia Excesiva | Dar autonomía y permisos destructivos al modelo. | Mínimo privilegio, aprobación humana (Human-in-the-loop). |
| **LLM07** | Fuga del Prompt de Sistema | Robo de IP, extracción de instrucciones base. | Bloquear queries de extracción, no guardar secretos en el prompt. |
| **LLM08** | Debilidades en Vectores (Embeddings)| Manipulación de BBDD vectoriales en arquitecturas RAG. | Controles de acceso estrictos (RBAC) en BBDD, auditar entradas. |
| **LLM09** | Desinformación | Alucinaciones, confianza ciega (overreliance). | Grounding (RAG), advertir al usuario, validación cruzada. |
| **LLM10** | Consumo Ilimitado | Denegación de servicio (DoS), facturas masivas. | Rate limiting, topes estrictos de tokens (entrada/salida). |

## Bibliografía
* [OWASP 2025 Top 10 Risk & Mitigations for LLMs and Gen AI Apps](https://genai.owasp.org/llm-top-10/)