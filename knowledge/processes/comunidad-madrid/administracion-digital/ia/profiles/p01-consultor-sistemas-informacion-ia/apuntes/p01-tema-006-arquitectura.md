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

Este tema corresponde al **Tema 6 del Anexo 3** de la Resolución 352/2026 (BOCM 11/06/2026), específico para el perfil **P01 (IA aplicada al ciclo de vida del software)** de la Agencia para la Administración Digital de la Comunidad de Madrid. 

*(Aviso para opositores: En el perfil P02, el Tema 6 es distinto: "Gobernanza de la IA", por lo que este apunte es exclusivo para P01).*

El tema abarca cinco grandes bloques de la ingeniería de sistemas moderna: **arquitecturas de integración** (APIs, ESB, Eventos), **microservicios con Kubernetes**, **modelos cloud híbridos**, **arquitectura de datos** (pipelines, calidad, ontologías) e **IA Gateway**. El examen, al ser tipo test con penalización, no busca definiciones divulgativas, sino discriminar fronteras técnicas muy finas: diferencias entre ETL y ELT, componentes específicos del *Control Plane* de Kubernetes, dimensiones de calidad del dato según estándares (ISO 8000 vs. DAMA), y diferencias entre el tráfico que gestiona un API Gateway frente a un IA Gateway.

## Ideas clave

- **Evolución de la integración:** Del modelo SOA clásico basado en **ESB** ("Tuberías inteligentes, extremos tontos", alto acoplamiento) al modelo de **Microservicios y EDA** ("Tuberías tontas, extremos inteligentes", bajo acoplamiento).
- **Integración Síncrona vs. Asíncrona:** Síncrona (APIs/REST/gRPC) implica acoplamiento temporal y respuesta inmediata. Asíncrona (EDA/Pub-Sub) desacopla productores de consumidores mediante eventos que describen hechos pasados.
- **Kubernetes (K8s):** Un orquestador de contenedores donde la unidad mínima desplegable es el **Pod** (que puede albergar varios contenedores compartiendo IP y volumen), no el contenedor individual.
- **Cloud Híbrida vs. Multicloud:** La nube híbrida conecta infraestructura local (*on-premises*) con la nube pública. El modelo *multicloud* implica usar varios proveedores de nube pública simultáneamente (no exigen *on-premises*).
- **Arquitectura de Datos (ETL vs. ELT):** En **ETL**, la transformación computacional recae sobre un middleware intermedio. En **ELT**, los datos se cargan "crudos" y la transformación aprovecha el cómputo del almacén destino (ej. *Data Warehouse* Cloud).
- **Calidad del Dato:** Se evalúa a través de marcos internacionales como la familia **ISO 8000** (calidad sintáctica, semántica y pragmática) y marcos de la industria como **DAMA-DMBOK** (exactitud, completitud, unicidad).
- **Ontologías (Estándares W3C):** Superan a los esquemas de bases de datos añadiendo semántica formal, usando la tripleta **RDF** (Sujeto-Predicado-Objeto) y el lenguaje lógico **OWL**.
- **IA Gateway:** Middleware especializado. A diferencia del API Gateway (que limita peticiones/IPs), el IA Gateway intercepta prompts, enruta por modelos, protege datos sensibles (DLP) y aplica caché semántico, limitando por **tokens** consumidos.

## Desarrollo

### 1. Arquitectura de integración

#### 1.1. Modelo Síncrono basado en APIs
La comunicación se basa en el patrón petición-respuesta (*Request-Reply*). El consumidor queda bloqueado a la espera del proveedor, generando **acoplamiento temporal**.
* **REST (Representational State Transfer):** Arquitectura *stateless* sobre HTTP/1.1 (típicamente) usando verbos (GET, POST, PUT, DELETE) y formatos ligeros como JSON.
* **gRPC:** Framework de Google basado en **HTTP/2** y **Protocol Buffers (Protobuf)**. Utiliza contratos fuertemente tipados y comunicación binaria, siendo muy superior en rendimiento para la comunicación interna síncrona entre microservicios (tráfico Este-Oeste).
* **API Gateway:** Patrón de diseño. Punto de entrada único para tráfico externo (Norte-Sur). Ejerce funciones transversales: enrutamiento, terminación TLS, *rate limiting*, autenticación (OAuth2/JWT) y transformación básica.

#### 1.2. Modelo basado en Bus Empresarial (ESB)
Propio de las arquitecturas Orientadas a Servicios (SOA). El **Enterprise Service Bus (ESB)** es un middleware pesado que centraliza la mediación, traducción de protocolos (ej. SOAP a REST), transformación (XML a JSON) y la orquestación.
* **Problema Arquitectónico:** Aglutina demasiada lógica de negocio ("Smart pipes"), convirtiéndose en un cuello de botella, un único punto de fallo (SPOF) organizativo/técnico y generando un alto grado de acoplamiento.

#### 1.3. Modelo de Integración Orientada a Eventos (EDA)
Comunicación asíncrona mediante mensajes. Un **Productor** emite un evento indicando un cambio de estado (ej. `ExpedienteRegistrado`), y un intermediario (*Broker*) lo distribuye.
* **Pub/Sub (Publicación/Suscripción):** Los eventos se publican en *topics* (canales). Varios **Consumidores** reaccionan al mismo evento independientemente (ej. Apache Kafka).
* **Filosofía:** "Dumb pipes, smart endpoints" (Tuberías tontas, extremos inteligentes). El *broker* solo enruta bytes rápido; la lógica recae en los microservicios.

### 2. Arquitectura de microservicios Kubernetes (K8s)

**Kubernetes** es el estándar *de facto* promovido por la CNCF para la orquestación de contenedores. 

#### 2.1. Arquitectura del Clúster
* **Control Plane (Plano de Control):** Toma las decisiones globales.
  * `kube-apiserver`: Interfaz de comunicación (frontend) de K8s.
  * `etcd`: Almacén de datos clave-valor de alta disponibilidad. Es la única fuente de verdad persistente del clúster.
  * `kube-scheduler`: Asigna nuevos Pods a los Nodos disponibles.
  * `kube-controller-manager`: Gestiona los bucles de control (mantiene el estado deseado).
* **Worker Nodes (Nodos de Trabajo):** Máquinas de cómputo.
  * `kubelet`: Agente local que asegura que los contenedores del Pod se están ejecutando.
  * `kube-proxy`: Mantiene las reglas de red para la comunicación.
  * *Container Runtime*: Motor de ejecución (containerd, CRI-O).

#### 2.2. Objetos / Componentes Fundamentales
* **Pod:** Unidad atómica. Encapsula contenedores que comparten volúmenes y red (localhost).
* **Deployment:** Objeto declarativo que gestiona *ReplicaSets* para asegurar un número de réplicas corriendo y gestionar actualizaciones sin caída (*Rolling Updates*).
* **Service:** Provee una abstracción de red estable (IP/DNS estático) para acceder a un conjunto de Pods (que son efímeros).
* **Ingress:** Gestiona tráfico HTTP/HTTPS externo hacia los Services del clúster. (Su evolución actual es el estándar *Gateway API*).
* **Service Mesh:** Infraestructura añadida (ej. Istio, Linkerd) que intercepta todo el tráfico interno mediante *sidecars* (proxies en cada Pod) para aportar mTLS, *circuit breaking*, reintentos y observabilidad extrema (tráfico Este-Oeste).

### 3. Modelo de arquitectura híbrida on premises-cloud

Combina centros de datos propios o corporativos (*On-Premises*) con recursos de nubes públicas, unidos por una red que permite la portabilidad de datos y servicios.

* **Conectividad:** * *VPN IPsec* (barata, sobre internet público, mayor latencia) vs. *Enlaces dedicados privados* como Azure ExpressRoute o AWS Direct Connect (sin tocar internet público, baja latencia, integraciones ENS Alto).
* **Casos de Uso Comunes:**
  * **Soberanía y Compliance:** Datos altamente sensibles se procesan *On-Prem* (cumpliendo niveles altos del ENS), mientras los frontends y recursos escalables residen en la nube.
  * **Cloud Bursting (Desbordamiento):** La aplicación base vive localmente, pero en picos estacionales de demanda levanta recursos en la nube pública.
* **Workload Placement (Ubicación de Cargas):** Criterios de decisión que incluyen latencia de red, coste de transferencia (Egress), legalidad del dato y grado de madurez tecnológica.

### 4. Arquitectura de datos: pipelines, calidad y ontologías

#### 4.1. Pipelines de Datos (ETL vs. ELT)
* **ETL (Extract, Transform, Load):** Extracción desde fuentes, transformación en un motor centralizado en memoria, y carga al destino. Histórico de los *Data Warehouses* clásicos.
* **ELT (Extract, Load, Transform):** Los datos en bruto (*Raw*) se extraen y se vuelcan directamente en el destino escalable cloud (ej. un *Data Lake* o *Lakehouse*). Las transformaciones se ejecutan después utilizando la inmensa capacidad de cómputo del propio repositorio destino.

#### 4.2. Calidad del Dato
Se audita bajo dos prismas complementarios preguntables en oposición:
* **Prisma DAMA-DMBOK:** Mide exactitud (*Accuracy*), completitud (sin campos vacíos clave), consistencia (datos coherentes entre sistemas) y unicidad.
* **Prisma Normativo ISO 8000-8:** * *Calidad Sintáctica:* Cumple el formato/esquema.
  * *Calidad Semántica:* El valor representa el significado correcto.
  * *Calidad Pragmática:* El dato es adecuado para el uso de negocio concreto de su consumidor.

#### 4.3. Ontologías (Web Semántica)
A diferencia de los esquemas relacionales, las ontologías son representaciones formales que definen conceptos, relaciones y lógica deductiva para la interoperabilidad de máquinas. Usan el *stack* del **W3C**:
* **RDF (Resource Description Framework):** Estructura los datos en grafos mediante la tripleta base **Sujeto - Predicado - Objeto**.
* **OWL (Web Ontology Language):** Añade axiomas y reglas lógicas (clases equivalentes, disjuntas, transitividad) que permiten a motores semánticos deducir conocimiento no explícito.
* **SPARQL:** El lenguaje de consulta estandarizado para consultar grafos de conocimiento RDF.

### 5. Arquitectura middleware: IA Gateway

El **AI Gateway** es una nueva capa *middleware* diseñada para intermediar entre las aplicaciones corporativas (y agentes) y los Modelos de Lenguaje Grandes (LLMs).

* **Diferencia de paradigma:** Mientras el API Gateway gestiona peticiones IP/HTTP, el IA Gateway gestiona y audita **tokens**, *prompts* e inferencias.
* **Capacidades fundamentales (Foco de Test):**
  * **Caché Semántico (*Semantic Caching*):** No exige coincidencias de texto exacto como un caché HTTP. Transforma la consulta en un vector (*embedding*) y, si la distancia matemática con una consulta previa es muy corta (ej. "¿Cómo solicitar beca?" vs. "¿Pasos para beca?"), devuelve la respuesta en caché sin pagar inferencia al LLM.
  * **Model Routing / Fallback:** Enruta *prompts* al modelo más barato/rápido según su complejidad. Si falla el proveedor primario, conmuta de forma transparente al proveedor de contingencia (*Fallback*).
  * **DLP (Data Loss Prevention) y Anonimización:** Intercepta *prompts* y enmascara PII (DNI, tarjetas sanitarias) antes de abandonar la red local hacia el proveedor LLM.
  * **Limitación por Coste/Token:** Aplica *rate limiting* y cuotas de presupuesto (FinOps) no por llamadas de red, sino midiendo el tamaño real (tokens) consumido por cada unidad de negocio.
* **Aclaración Arquitectónica:** El IA Gateway no hace "RAG" (no indexa documentos PDF ni enriquece contexto por defecto), simplemente gobierna la política de acceso y telemetría de las inferencias.

## Conceptos que suelen preguntarse

| Concepto a distinguir | Qué es realmente | Trampa habitual en exámenes |
| :--- | :--- | :--- |
| **ESB vs EDA** | ESB centraliza lógica ("Smart pipes"); EDA desacopla productores/consumidores ("Dumb pipes"). | "ESB y Event-Driven son el mismo patrón asíncrono." |
| **Pod vs Contenedor** | El Pod es la unidad mínima en K8s. Puede contener varios contenedores compartiendo IP y volumen. | "En Kubernetes, la unidad atómica de asignación es el Contenedor." |
| **etcd en Kubernetes** | Base de datos clave-valor distribuida. Es la única fuente de estado del *Control Plane*. | "`etcd` es el nodo donde se ejecuta el código del usuario." |
| **Híbrida vs Multicloud** | Híbrida: Infraestructura propia (On-Premises) + Cloud. Multicloud: Uso de múltiples Clouds públicos. | "Multicloud requiere siempre poseer un CPD físico propio." |
| **ETL vs ELT** | Diferencia en el orden computacional: ELT transforma *después* de volcar en el sistema destino. | "ELT transforma los datos antes de guardarlos por motivos de seguridad." |
| **RDF y OWL** | Stack semántico W3C. RDF usa tripletas (Sujeto-Predicado-Objeto). OWL aporta capacidad deductiva formal. | "RDF es el lenguaje oficial para bases de datos relacionales SQL." |
| **IA Gateway** | Proxy especializado en el plano de control (Tokens, DLP en prompts, caché semántico). | "El IA Gateway es el encargado de almacenar documentos indexados para RAG." |

## Posibles preguntas tipo test

**Pregunta 1.** Según la arquitectura de Kubernetes, ¿qué componente del plano de control (*Control Plane*) funciona como almacén de datos clave-valor de alta disponibilidad responsable de guardar el estado deseado y real de todo el clúster?
A. El `kube-proxy`.
B. El `kubelet`.
C. El `etcd`.
D. El `kube-scheduler`.
**Respuesta correcta: C.** (`etcd` es la única fuente de verdad persistente del *Control Plane*).

**Pregunta 2.** Al evolucionar una arquitectura de integración desde un Enterprise Service Bus (ESB) corporativo tradicional hacia una arquitectura orientada a eventos (EDA) con brokers de mensajería (ej. Kafka), se busca un cambio de paradigma basado en:
A. Transicionar hacia "tuberías tontas y extremos inteligentes" (*Dumb pipes, smart endpoints*), eliminando el cuello de botella central de la lógica de transformación.
B. Consolidar el ESB como *Service Mesh* en todos los contenedores de Kubernetes.
C. Abandonar el patrón asíncrono e implementar gRPC de forma obligatoria.
D. Requerir que el productor del evento conozca siempre la identidad y protocolo exacto de todos sus consumidores.
**Respuesta correcta: A.** (La orquestación centralizada del ESB da paso a la coreografía distribuida de los eventos).

**Pregunta 3.** Si la Agencia de Administración Digital decide utilizar la potencia de procesamiento analítico masivo de un repositorio de datos Cloud (ej. BigQuery/Snowflake) para realizar allí mismo la limpieza y transformación de los datos que llegan "en crudo" desde los sistemas legados, está implementando una arquitectura de *pipeline*:
A. ETL (Extract, Transform, Load).
B. ELT (Extract, Load, Transform).
C. Pub/Sub con enrutamiento de modelos.
D. Cacheo semántico.
**Respuesta correcta: B.** (En ELT, los datos se cargan sin transformar (Load) y la T (Transform) ocurre dentro del almacén destino).

**Pregunta 4.** Dentro del marco normativo internacional ISO 8000 para la calidad del dato, ¿qué dimensión evalúa si un dato codifica correctamente su significado técnico esperado, apoyándose habitualmente en diccionarios de metadatos o estándares sectoriales?
A. Calidad Pragmática.
B. Calidad Sintáctica.
C. Calidad Semántica.
D. Calidad de Ocultación (DLP).
**Respuesta correcta: C.** (Sintáctica = Formato, Semántica = Significado/Metadata, Pragmática = Adecuación al uso del negocio).

**Pregunta 5.** Para implementar la interoperabilidad de la Web Semántica y construir Ontologías, el W3C ha estandarizado un formato subyacente que representa todo el conocimiento en forma de tripletas lógicas (Sujeto, Predicado, Objeto). ¿A qué estándar corresponde?
A. JSON-LD.
B. gRPC.
C. RDF (Resource Description Framework).
D. OpenAPI.
**Respuesta correcta: C.**

**Pregunta 6.** Se implementa un **IA Gateway** como componente de arquitectura *middleware* para el consumo corporativo de Modelos Fundacionales. ¿Qué característica fundamental lo distingue de un API Gateway tradicional (como un proxy inverso estándar)?
A. Que el IA Gateway almacena bases de datos relacionales en su interior para resolver consultas SQL directamente.
B. Que implementa Caché Semántico usando vectores matemáticos (*embeddings*) para devolver respuestas cacheadas a preguntas similares aunque estén redactadas de manera diferente.
C. Que limita el tráfico de red midiendo el número de paquetes UDP en lugar de peticiones HTTP.
D. Que realiza entrenamientos *Fine-Tuning* automáticos en tiempo real.
**Respuesta correcta: B.** (La interceptación y análisis semántico del tráfico/prompts es la función *core* de un AI Gateway frente al API Gateway clásico).

## Normativa o fuentes relacionadas

* **ISO 8000 Series (Data Quality):** Especialmente ISO 8000-8 (*Concepts and measuring*), definiendo calidad sintáctica, semántica y pragmática.
* **CNCF (Cloud Native Computing Foundation):** Estándares de arquitectura *Cloud Native* y Kubernetes. Documentación oficial de componentes (`etcd`, Nodos, Control Plane).
* **W3C (World Wide Web Consortium):** Estándares de Web Semántica: **RDF** (Resource Description Framework), **OWL** (Web Ontology Language), y **SPARQL**.
* **DAMA-DMBOK:** Base de conocimientos de gestión de datos, referencia fundamental para las dimensiones de calidad del dato (Exactitud, Completitud, Consistencia, Unicidad).
* **Real Decreto 311/2022 (Esquema Nacional de Seguridad):** Relevante para las arquitecturas Híbridas (interconexiones seguras y segregación de recursos).
* **IETF / W3C (Protocolos base):** Documentación sobre REST, HTTP/1.1 vs HTTP/2, y OpenAPI.

## Dudas o puntos pendientes

* **IA Gateway (Falta de estándar normativo puro):** A fecha de publicación de la convocatoria, el término "IA Gateway" no está sujeto a una norma ISO/IETF estricta, sino que es un patrón arquitectónico de infraestructura emergente (adoptado por Kong, Cloudflare, Azure, etc.). Las preguntas de test sobre este concepto se orientarán al paradigma de negocio (Caché Semántico, Control de Coste por Tokens, *Fallback* de LLMs).
* **ETL frente a ELT:** Aunque ELT es la tendencia actual por el auge del Data Warehousing moderno, en bases de datos locales o limitadas, el paradigma clásico ETL sigue siendo válido para no sobrecargar el repositorio destino. Deben diferenciarse con base en **dónde** ocurre el cómputo de la transformación de los datos.
* **K8s Ingress vs. Gateway API:** Históricamente el objeto `Ingress` se usaba en Kubernetes para la entrada de tráfico Norte-Sur. Actualmente la CNCF promueve `Gateway API` como su evolución lógica y estandarizada; en preguntas genéricas de oposición, a menudo ambos términos aparecen como correctos funcionalmente para la entrada del tráfico L7.
