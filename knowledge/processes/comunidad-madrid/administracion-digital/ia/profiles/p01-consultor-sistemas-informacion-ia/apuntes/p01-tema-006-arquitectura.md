---
id: "cm-ad-ia-p01-tema-006-arquitectura"
title: "Arquitectura"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/ia"
profiles:
  - "p01-consultor-sistemas-informacion-ia"
official_profile: "P01 - Consultor de Sistemas de Información - IA Aplicada al Ciclo de Vida del Software"
official_topic: "Tema 6. Arquitectura"
source_ids:
tags:
  - "arquitectura"
  - "integracion"
  - "apis"
  - "eventos"
  - "microservicios"
  - "kubernetes"
  - "cloud-hibrida"
  - "arquitectura-datos"
  - "ia-gateway"
created_at: "2026-07-10"
last_reviewed: null
ai_generated: true
ai_sources:
  - "perplexity"
  - "chatgpt"
  - "gemini"
needs_human_review: true
---

# Arquitectura

## Encaje en la convocatoria

Este tema corresponde al **Tema 6 del Anexo 3** de la Resolución 352/2026 (BOCM 11/06/2026) para el perfil **P01 – IA aplicada al ciclo de vida del software** de la Agencia para la Administración Digital de la Comunidad de Madrid.  

El enunciado abarca cinco grandes bloques de ingeniería de sistemas moderna: **arquitecturas de integración** (APIs, ESB, eventos), **microservicios sobre Kubernetes**, **modelos de cloud híbrida**, **arquitectura de datos** (pipelines, calidad, ontologías, data fabric) y **IA Gateway como middleware especializado**, con preguntas tipo test que explotan diferencias finas entre conceptos.

## Ideas clave

- **De ESB/SOA a microservicios y EDA:** Se ha pasado del modelo SOA con **Enterprise Service Bus (ESB)** (“tuberías inteligentes, extremos tontos”) al modelo de **microservicios y Event‑Driven Architecture (EDA)** (“tuberías tontas, extremos inteligentes”).  
- **Integración síncrona vs asíncrona:** Síncrona (REST, gRPC) implica acoplamiento temporal y respuesta inmediata; asíncrona (Pub/Sub, Kafka) desacopla productores y consumidores mediante eventos que representan hechos ya ocurridos.  
- **Kubernetes y unidad mínima:** Kubernetes (K8s), promovido por la CNCF, orquesta contenedores donde la unidad mínima desplegable es el **Pod**, que puede contener varios contenedores compartiendo IP y volúmenes, no el contenedor individual.  
- **Cloud híbrida vs multicloud:** La **nube híbrida** conecta infraestructura local (on‑premises) con la nube pública; el modelo **multicloud** usa varios proveedores de nube pública sin requerir necesariamente infraestructura propia.  
- **ETL vs ELT y Data Fabric:** En **ETL** la transformación se realiza antes de cargar en destino; en **ELT** se cargan datos en bruto y se transforman aprovechando la capacidad del repositorio Cloud; **Data Fabric** proporciona una capa unificada de acceso e integración de datos distribuidos basada en metadatos y automatización.  
- **Calidad del dato y ontologías:** La calidad del dato se evalúa con marcos como **ISO 8000‑8** (calidad sintáctica, semántica, pragmática) y **DAMA‑DMBOK** (exactitud, completitud, consistencia, unicidad); las ontologías W3C (RDF, OWL, SPARQL) añaden semántica formal e interoperabilidad.  
- **IA Gateway vs API Gateway:** El **IA Gateway** gobierna prompts, tokens y modelos (caché semántico, routing, DLP, cuotas de consumo), mientras que un API Gateway tradicional se centra en tráfico HTTP, rate limiting por petición y cabeceras.

## Desarrollo

### 1. Arquitectura de integración

#### 1.1. Integración síncrona basada en APIs

La integración síncrona sigue el patrón petición‑respuesta (Request/Reply), donde el consumidor queda bloqueado esperando la respuesta del proveedor, generando **acoplamiento temporal**.  

- **REST (Representational State Transfer):**  
  Arquitectura sobre HTTP (típicamente HTTP/1.1) que trata recursos identificados por URLs, usando métodos como `GET`, `POST`, `PUT`, `DELETE` y formatos ligeros como JSON; es *stateless* y ampliamente utilizada en integración norte‑sur.  
- **gRPC:**  
  Framework de Google sobre **HTTP/2** y **Protocol Buffers (Protobuf)**, con contratos fuertemente tipados y comunicación binaria, muy eficiente para comunicaciones internas entre microservicios (tráfico este‑oeste).  
- **API Gateway:**  
  Patrón que define un **punto de entrada único** (reverse proxy) para tráfico externo hacia los servicios internos; gestiona enrutamiento, terminación TLS, autenticación/autorización (OAuth 2.0, JWT), limitación de tasa (rate limiting) y transformación básica de peticiones.  

En las preguntas de examen se enfatiza que el API Gateway opera en el **plano de red** y HTTP, mientras que el IA Gateway opera en el plano de tokens y prompts.

#### 1.2. Modelo SOA con Bus Empresarial (ESB)

Las arquitecturas orientadas a servicios (SOA) tradicionales introducen un **Enterprise Service Bus (ESB)** como middleware central.  

El ESB se encarga de:

- Mediar entre servicios, transformando mensajes (por ejemplo, de SOAP/XML a REST/JSON).  
- Orquestar flujos complejos (workflow) y aplicar reglas de negocio centralizadas.  
- Traducir protocolos y formatos, convirtiéndose en el punto donde se concentran muchas responsabilidades técnicas y funcionales.  

El problema arquitectónico es que el ESB tiende a convertirse en cuello de botella y único punto de fallo, con “tuberías inteligentes” y extremos relativamente tontos, generando alto acoplamiento entre servicios.

#### 1.3. Arquitectura orientada a eventos (EDA) y Pub/Sub

La **Event‑Driven Architecture (EDA)** usa comunicación asíncrona basada en eventos que describen cambios de estado ya producidos (por ejemplo, `ExpedienteRegistrado`).  

- **Productores (Producers):** Emisión de eventos a un broker sin conocer quién los consumirá.  
- **Brokers (ej. Apache Kafka):** Canales de publicación/suscripción (topics) donde varios consumidores pueden reaccionar al mismo evento de forma independiente.  
- **Consumidores (Consumers):** Microservicios que suscriben a topics y ejecutan su lógica de negocio en reacción a eventos.  

La filosofía **“Dumb pipes, smart endpoints”** indica que las tuberías (broker, bus de mensajes) deben ser simples y rápidas, mientras que la lógica inteligente reside en los endpoints (microservicios).  

En esta transición desde ESB a EDA se busca menor acoplamiento, mayor escalabilidad y evitar que el bus central aglutine lógica de negocio.

### 2. Arquitectura de microservicios sobre Kubernetes (K8s)

**Kubernetes (K8s)** es el orquestador estándar de contenedores respaldado por la **Cloud Native Computing Foundation (CNCF)**.

#### 2.1. Arquitectura del clúster

Se distingue entre **Control Plane** (plano de control) y **Worker Nodes** (nodos de trabajo).  

- **Control Plane:**
  - `kube-apiserver`: Servicio frontal que expone la API de Kubernetes y todas las operaciones de gestión del clúster.
  - `etcd`: Base de datos distribuida clave‑valor de alta disponibilidad que almacena el estado deseado y real del clúster; es la **única fuente de verdad persistente**.
  - `kube-scheduler`: Asigna Pods nuevos a nodos disponibles según recursos y afinidades.
  - `kube-controller-manager`: Ejecuta bucles de control (controllers) que aseguran que el estado actual converge al estado deseado.
- **Worker Nodes:**
  - `kubelet`: Agente local que garantiza que los contenedores de los Pods asignados al nodo se ejecutan como se declara.
  - `kube-proxy`: Gestiona reglas de red y balanceo de carga a nivel de servicios.
  - Runtime de contenedores (containerd, CRI‑O), responsable de lanzar y gestionar contenedores.

Una pregunta típica de examen identifica `etcd` como el componente del Control Plane encargado de almacenar el estado del clúster.

#### 2.2. Objetos fundamentales de Kubernetes

- **Pod:**  
  Unidad mínima desplegable; agrupa uno o varios contenedores que comparten **IP, espacio de nombres de red y volúmenes**, lo que permite patrones como el **sidecar container** (logging, proxy, sincronización).  
- **Deployment:**  
  Recurso declarativo que gestiona **ReplicaSets** para mantener un número fijo de Pods y aplicar actualizaciones mediante estrategias como `RollingUpdate`, que actualiza Pods progresivamente manteniendo disponibilidad del servicio en aplicaciones stateless.  
- **Service:**  
  Abstracción de red estable (IP y nombre DNS) que expone un conjunto de Pods dinámicos (por ejemplo, `ClusterIP`, `NodePort`, `LoadBalancer`).  
- **Ingress / Gateway API:**  
  Recurso que controla el tráfico HTTP/HTTPS entrante hacia servicios internos (nivel L7), gestionando rutas, TLS y reglas de entrada; su evolución moderna es **Gateway API**.  
- **Service Mesh (Istio, Linkerd):**  
  Capa adicional que inyecta proxies sidecar en cada Pod para aplicar mTLS, circuit breakers, reintentos y observabilidad detallada del tráfico este‑oeste.

#### 2.3. Asignación de nodos y sidecar containers

- **nodeSelector:**  
  Mecanismo sencillo de scheduling que vincula Pods a nodos con etiquetas concretas mediante coincidencias de clave‑valor, sin expresiones avanzadas; se pregunta explícitamente en exámenes como “coincidencia simple clave‑valor”.  
- **Sidecar containers:**  
  Se usan para tareas auxiliares junto al contenedor principal, como logging, proxy de red, métricas o sincronización de ficheros dentro del mismo Pod, no para sustituir al contenedor principal si falla.

### 3. Arquitectura híbrida on‑premises / cloud y Landing Zone

La **arquitectura híbrida** combina centros de datos propios (*on‑premises*) con recursos de nubes públicas (IaaS, PaaS, SaaS), conectados por redes seguras para garantizar soberanía de datos y cumplimiento normativo.

#### 3.1. Conectividad y ENS

Los modelos habituales de conexión son:

- **VPN IPsec sobre Internet público:**  
  Menores costes, más latencia y exposición a internet (mitigada mediante cifrado y medidas ENS).  
- **Enlaces dedicados privados (ExpressRoute, Direct Connect):**  
  Conexión punto a punto con baja latencia y no exposición directa a internet, adecuados para sistemas clasificados como ENS Medio/Alto.

El **Esquema Nacional de Seguridad (RD 311/2022)** exige principios básicos como seguridad como proceso integral, existencia de líneas de defensa y diferenciación de responsabilidades, aplicables tanto a infraestructura on‑prem como cloud.

#### 3.2. Hub‑and‑Spoke y Landing Zone

Los proveedores cloud suelen recomendar un modelo **Hub‑and‑Spoke** para redes híbridas.

- **Hub:**  
  VNET/VPC central que concentra conectividad con on‑premises y políticas comunes de seguridad, routing y monitorización.  
- **Spokes:**  
  Redes “satélite” donde residen cargas de trabajo individuales, conectadas al hub.  

La **Landing Zone** es la implementación inicial del entorno cloud donde se definen:

- La **conectividad centralizada con on‑premises desde el hub**, aplicando políticas de red y seguridad comunes a todos los spokes.  
- La estructura de suscripciones/proyectos, cuentas, dominios, y estándares de identidad, logging y cumplimiento.  

En las preguntas tipo test se destaca que la Landing Zone no es el punto de entrada de datos (eso suele corresponder al **data landing zone** dentro del hub de datos), sino la arquitectura base que centraliza la conectividad y las políticas.

#### 3.3. Workload placement y cloud bursting

La decisión de dónde ubicar cada carga de trabajo (workload placement) se basa en:

- Latencia requerida, coste de transferencia (egress), requisitos de soberanía y clasificación ENS (Bajo/Medio/Alto).  
- Madurez de la organización para operar servicios cloud y on‑prem de forma integrada.  

**Cloud bursting** describe escenarios en los que sistemas on‑prem escalan temporalmente hacia la nube pública para absorber picos de demanda, manteniendo la base de operación local.

### 4. Arquitectura de datos: pipelines, calidad, ontologías y Data Fabric

#### 4.1. Pipelines de datos: ETL vs ELT

Los pipelines de datos conectan fuentes operacionales con repositorios analíticos (data warehouses, data lakes, lakehouses).

- **ETL (Extract, Transform, Load):**  
  Se extraen datos desde fuentes, se transforman en un motor intermedio (middleware, servidor ETL) y se cargan ya transformados en el almacén destino; tradicionalmente usado en data warehouses locales.  
- **ELT (Extract, Load, Transform):**  
  Se extraen datos en bruto, se cargan directamente en el repositorio escalable cloud (data lake/lakehouse) y la transformación se ejecuta posteriormente aprovechando la capacidad de cómputo del propio destino.  

Una pregunta típica describe un caso en el que la Administración usa BigQuery/Snowflake para hacer limpieza y transformación sobre datos “raw”; la respuesta correcta es que se trata de **ELT**, porque la T ocurre en el sistema destino.

#### 4.2. Calidad del dato: DAMA y ISO 8000

Se evalúa la calidad bajo dos perspectivas complementarias:

- **DAMA‑DMBOK (industria):**  
  Dimensiones como exactitud (datos correctos), completitud (ausencia de campos clave vacíos), consistencia (coherencia entre sistemas) y unicidad (no duplicidad).  
- **ISO 8000‑8 (normativa):**  
  - **Calidad sintáctica:** el dato cumple formato y esquema (tipos, longitudes, patrones).  
  - **Calidad semántica:** el dato representa el significado correcto según diccionarios de metadatos y estándares sectoriales.  
  - **Calidad pragmática:** el dato es adecuado para el uso de negocio concreto (por ejemplo, resolución suficiente para la decisión).  

Las preguntas de examen tienden a pedir que se identifique la **calidad semántica** como la que evalúa la corrección del significado técnico del dato.

#### 4.3. Ontologías y Web Semántica (W3C)

Para dotar de semántica formal e interoperabilidad entre sistemas se utilizan estándares de la Web Semántica del **W3C**:

- **RDF (Resource Description Framework):**  
  Modelo basado en grafos que representa conocimiento mediante tripletas **Sujeto–Predicado–Objeto**, constituyendo la estructura fundamental de datos semánticos.  
- **OWL (Web Ontology Language):**  
  Lenguaje para definir ontologías con clases, propiedades, axiomas (equivalencias, disjointness, transitividad) y reglas lógicas que permiten razonamiento automático.  
- **SPARQL:**  
  Lenguaje de consulta estandarizado para grafos RDF, similar al papel de SQL sobre bases relacionales.  

Una cuestión frecuente pregunta qué estándar utiliza tripletas Sujeto‑Predicado‑Objeto: la respuesta correcta es **RDF**.

#### 4.4. Data Warehouse, Data Mart, Delta Lake y Data Fabric

- **Data Warehouse:**  
  Almacén centralizado de datos estructurados integrados para análisis empresarial.  
- **Data Mart:**  
  Subconjunto temático del Data Warehouse, orientado a un área de negocio específica.  
- **Delta Lake / Lakehouse:**  
  Capa de gestión transaccional (ACID) sobre data lakes, permitiendo versiones, esquema evolutivo y consultas eficientes.  
- **Data Fabric:**  
  Enfoque arquitectónico que proporciona una **capa unificada de acceso e integración de datos distribuidos**, basada en metadatos y automatización, permitiendo consumir datos sin necesidad de centralizarlos físicamente.  

La pregunta de oposición que define Data Fabric se centra precisamente en esta capacidad de integración lógica sin centralización física de datos.

### 5. Arquitectura middleware: IA Gateway

El **IA Gateway** (AI Gateway) es un componente middleware emergente que intermedia entre aplicaciones corporativas (incluyendo agentes) y modelos de lenguaje (LLMs) y otros servicios de IA.

#### 5.1. Diferencias con API Gateway

A diferencia del **API Gateway** clásico centrado en tráfico HTTP/IP (peticiones, cabeceras, direcciones IP), el IA Gateway opera en el plano de **prompts, tokens e inferencias**.  

Funciones típicas:

- **Model routing y fallback:**  
  Enrutamiento inteligente de solicitudes hacia diferentes modelos según criterios de coste, latencia y complejidad; posibilidad de fall‑back automático a otros proveedores si falla el primario.  
- **Guardrails y políticas:**  
  Implementación de controles técnicos sobre prompts y respuestas (por ejemplo, filtros de contenido, límites de longitud, restricciones de uso) antes/depués de llamar al modelo.  
- **Control de consumo:**  
  Limitación de uso en función de **tokens consumidos y número de llamadas**, aplicando políticas de FinOps y cuotas por unidad organizativa.  

En preguntas se indica que IA Gateway permite routing de modelos, guardrails y control de consumo, pero no orquesta por sí mismo todas las comunicaciones agent‑to‑agent (eso entra más en funciones de orquestador o plataforma de agentes).

#### 5.2. Caché semántico y protección de datos (DLP)

Una característica diferenciadora es la **caché semántica (semantic caching)**:

- El IA Gateway genera embeddings de los prompts y guarda respuestas asociadas; si una nueva pregunta es semánticamente muy similar (distancia vectorial baja), puede devolver la respuesta cacheada sin invocar de nuevo al modelo, reduciendo costes y latencia.  
- No se basa en coincidencias exactas de texto como una caché HTTP tradicional, sino en similitud semántica.  

En cuanto a protección de datos:

- Implementa funciones de **Data Loss Prevention (DLP)** y anonimización, enmascarando PII (DNI, números de tarjeta sanitaria, etc.) antes de que los prompts salgan del perímetro corporativo hacia servicios externos de IA.  

Es importante distinguir que el IA Gateway **no es un motor RAG** por sí mismo (no indexa documentos ni realiza retrieval sobre bases vectoriales), sino un proxy de gobierno para el consumo de modelos.

### 6. Kafka y política de particiones

En el contexto de EDA, **Apache Kafka** aparece como broker de eventos de referencia.

- **cleanup.policy=compact:**  
  Indica que Kafka realizará compactación de log manteniendo solo el **último valor por clave (key)** y eliminando versiones anteriores de la misma clave, útil para topics de tipo “tabla de estado”.  
- **Redistribución de mensajes al aumentar particiones:**  
  Añadir nuevas particiones a un topic existente (pasar de 5 a 6) **no redistribuye automáticamente** los mensajes ya escritos; la operación estándar solo afecta a nuevos mensajes, salvo que se haga una reasignación manual específica (reassign partitions), algo que suele presentarse en examen como “no posible de forma automática”.

## Conceptos que suelen preguntarse (trampas típicas)

| Concepto a distinguir        | Qué es realmente                                                                                                         | Trampa habitual en exámenes                                                        |
| :--------------------------- | :------------------------------------------------------------------------------------------------------------------------ | :--------------------------------------------------------------------------------- |
| ESB vs EDA                  | ESB centraliza lógica y transformación (smart pipes); EDA usa brokers simples y extremos inteligentes desacoplados. | “ESB y EDA son el mismo patrón de integración asíncrona.”               |
| Pod vs contenedor           | El Pod es la unidad mínima en K8s, puede contener varios contenedores que comparten IP y volúmenes.      | “La unidad atómica en K8s es el contenedor.”                             |
| `etcd` en Kubernetes        | Base clave‑valor distribuida que guarda el estado del clúster (Control Plane).                         | “`etcd` es donde se ejecuta el código de usuario.”                      |
| Híbrida vs multicloud       | Híbrida = on‑prem + cloud; multicloud = varias clouds públicas, sin requerir CPD propio.               | “Multicloud requiere necesariamente infraestructura on‑prem.”           |
| ETL vs ELT                  | Diferencia en dónde se hace la transformación: ETL antes de cargar; ELT después, en el destino.        | “ELT transforma los datos antes de guardarlos por seguridad.”           |
| Calidad semántica (ISO 8000)| Evalúa si el dato codifica correctamente su significado técnico según metadatos.                        | “Se refiere al formato del dato” (eso es sintáctica).                   |
| RDF vs otros formatos       | RDF representa conocimiento en tripletas Sujeto‑Predicado‑Objeto.                                      | “JSON‑LD o OpenAPI usan tripletas RDF.”                                  |
| IA Gateway                  | Proxy IA que implementa caché semántico, routing de modelos, DLP y control por tokens.                | “El IA Gateway es el motor RAG que almacena documentos.”                |
| Sidecar container           | Contenedor auxiliar para logging, proxy, métricas, etc., en el mismo Pod.                               | “Sustituye al contenedor principal cuando falla.”                       |
| RollingUpdate               | Actualiza Pods progresivamente manteniendo disponibilidad.                                            | “Elimina todos los Pods a la vez y luego crea los nuevos.”              |
| nodeSelector                | Coincidencia simple clave‑valor para elegir nodos.                                                               | “Admite expresiones complejas tipo In, Exists” (eso es node affinity).  |
| Data Fabric                 | Capa unificada de acceso e integración de datos distribuidos sin centralización física.                          | “Es un nuevo tipo de Data Warehouse centralizado.”                      |

## Posibles preguntas tipo test

**Pregunta 1.** Según la arquitectura de Kubernetes, ¿qué componente del plano de control actúa como almacén clave‑valor de alta disponibilidad responsable de guardar el estado del clúster?

A. `kube-proxy`.  
B. `kubelet`.  
C. `etcd`.  
D. `kube-scheduler`.  

**Respuesta correcta: C.** (`etcd` es la única fuente de verdad persistente del estado del clúster).

---

**Pregunta 2.** Al evolucionar desde un ESB corporativo hacia una arquitectura orientada a eventos con brokers como Kafka, el cambio de paradigma se basa en:

A. Consolidar el ESB como Service Mesh en todos los contenedores de Kubernetes.  
B. Transicionar hacia “tuberías tontas y extremos inteligentes”, eliminando el cuello de botella central de la lógica de transformación.  
C. Abandonar el patrón asíncrono e implementar gRPC obligatorio.  
D. Requerir que el productor conozca siempre la identidad de todos los consumidores.  

**Respuesta correcta: B.** (La EDA disocia la lógica del bus central y la reparte entre microservicios).

---

**Pregunta 3.** Si la Administración decide cargar datos “en crudo” en BigQuery o Snowflake y realizar allí mismo la transformación aprovechando su capacidad de cómputo, está aplicando un pipeline:

A. ETL (Extract, Transform, Load).  
B. ELT (Extract, Load, Transform).  
C. Pub/Sub orientado a eventos.  
D. Caché semántico.  

**Respuesta correcta: B.** (En ELT, los datos se cargan sin transformar y se procesan posteriormente en el destino).

---

**Pregunta 4.** Dentro del marco ISO 8000, ¿qué dimensión de calidad evalúa si un dato codifica correctamente su significado técnico esperado?

A. Calidad pragmática.  
B. Calidad sintáctica.  
C. Calidad semántica.  
D. Calidad de ocultación (DLP).  

**Respuesta correcta: C.** (Sintáctica = formato, semántica = significado, pragmática = adecuación al uso).

---

**Pregunta 5.** Para la Web Semántica, ¿qué estándar W3C representa conocimiento en forma de tripletas (Sujeto, Predicado, Objeto)?

A. JSON‑LD.  
B. gRPC.  
C. RDF (Resource Description Framework).  
D. OpenAPI.  

**Respuesta correcta: C.** (RDF es la base del modelo de grafos semánticos).

---

**Pregunta 6.** Se despliega un IA Gateway para gobernar el uso corporativo de LLMs. ¿Qué característica fundamental lo distingue de un API Gateway tradicional?

A. El IA Gateway almacena bases de datos relacionales para ejecutar SQL.  
B. Implementa caché semántico usando embeddings para responder a preguntas similares aunque se formulen diferente.  
C. Limita tráfico midiendo paquetes UDP en lugar de peticiones HTTP.  
D. Realiza fine‑tuning automático en tiempo real.  

**Respuesta correcta: B.** (Su función núcleo es gobernar prompts y tokens con capacidades semánticas).

---

**Pregunta 7.** En Kubernetes, ¿para qué se usa típicamente un contenedor sidecar dentro de un Pod?

A. Para sustituir al contenedor principal cuando falla.  
B. Para desplegar automáticamente nuevos nodos del clúster.  
C. Para almacenamiento permanente sin volúmenes.  
D. Para ejecutar tareas auxiliares (logging, proxy, sincronización de ficheros) junto al contenedor principal.  

**Respuesta correcta: D.** (El patrón sidecar añade funcionalidad de apoyo dentro del mismo Pod).

---

**Pregunta 8.** En Apache Kafka, ¿qué implica la configuración `cleanup.policy=compact` en un topic?

A. Borrar mensajes mayores que `retention.bytes`.  
B. Comprimir mensajes por antigüedad (`retention.ms`).  
C. Mantener solo el último valor por clave, eliminando versiones anteriores de esa clave.  
D. Borrar mensajes antiguos según `retention.ms`.  

**Respuesta correcta: C.** (La compactación conserva la última versión de cada key).

---

**Pregunta 9.** ¿Qué descripción refleja correctamente el concepto **Data Fabric** en arquitectura de datos?

A. Nuevo tipo de Data Warehouse centralizado.  
B. Enfoque que proporciona una capa unificada de acceso e integración de datos distribuidos, basada en metadatos y automatización, sin necesidad de centralizarlos físicamente.  
C. Sistema de ficheros distribuido de baja latencia.  
D. Subconjunto temático del Data Warehouse.  

**Respuesta correcta: B.** (Data Fabric se centra en integración lógica distribuida).

---

**Pregunta 10.** En un modelo Hub‑and‑Spoke para arquitectura híbrida on‑premises/cloud, ¿qué papel desempeña la Landing Zone?

A. Permitir que los spokes se comuniquen directamente entre sí evitando el hub.  
B. Centralizar la conectividad con on‑premises en el hub y aplicar políticas de red y seguridad comunes a todos los spokes.  
C. Ser el punto de entrada de datos raw dentro del hub.  
D. Actuar como data lake para historificación de logs.  

**Respuesta correcta: B.** (La Landing Zone define la arquitectura base y la conectividad híbrida común).

## Normativa o fuentes relacionadas

- **ISO 8000‑8:** *Data quality – Part 8: Concepts and measuring*, para dimensiones de calidad sintáctica, semántica y pragmática.  
- **DAMA‑DMBOK:** Referencia industrial en gestión de datos y calidad (exactitud, completitud, consistencia, unicidad).  
- **CNCF – Kubernetes documentation:** Descripción oficial de Control Plane, etcd, Pods, Deployments, Services y Service Mesh.  
- **W3C – RDF, OWL, SPARQL:** Estándares de la Web Semántica y ontologías.  
- **Real Decreto 311/2022 (ENS):** Principios básicos y requisitos mínimos de seguridad aplicables a arquitecturas híbridas y cloud.

## Dudas o puntos pendientes

- **IA Gateway como patrón emergente:** No existe todavía una norma ISO específica para IA Gateways; se trata de un patrón de mercado (Cloudflare, Kong, Azure AI Gateway) centrado en gobierno de consumo de modelos, prompts y tokens, más que en integración de datos.  
- **ETL vs ELT en contextos legacy:** Aunque ELT domina en plataformas cloud, en entornos locales con capacidad de cómputo limitada en destino, ETL sigue siendo válido; la clave en examen es diferenciar **“dónde ocurre la transformación”**.  
- **Gateway API vs Ingress en Kubernetes:** Gateway API es el estándar moderno para tráfico L7; muchas referencias y exámenes siguen mencionando Ingress como recurso clásico, pero conceptualmente ambos cubren entrada de tráfico HTTP/HTTPS al clúster.