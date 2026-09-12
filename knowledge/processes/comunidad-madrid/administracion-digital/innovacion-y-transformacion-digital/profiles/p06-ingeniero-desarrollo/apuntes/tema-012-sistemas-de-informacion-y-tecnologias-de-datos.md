---
id: "cm-ad-innovacion-y-transformacion-digital-tema-012-sistemas-de-informacion-y-tecnologias-de-datos"
title: "Sistemas de información y tecnologías de datos"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/innovacion-y-transformacion-digital"
profiles:
  - "p06-ingeniero-desarrollo"
official_profiles:
  - "P06 - Ingeniero de Desarrollo"
official_topic: "Tema 12. Sistemas de información y tecnologías de datos"
source_ids: []
tags:
  - "sistemas-de-informacion"
  - "tecnologias-de-datos"
  - "gestion-del-dato"
  - "api"
  - "servicios-de-integracion"
  - "bi"
  - "herramientas-bi"
  - "tendencias-tecnologicas"
  - "teorema-cap"
  - "rfc-9110"
created_at: "2026-09-03"
last_reviewed: "2026-09-12"
ai_generated: true
ai_sources:
  - "perplexity"
  - "chatgpt"
  - "gemini"
needs_human_review: true
---

# Tema 12. Sistemas de información y tecnologías de datos

## 1. Sistemas de información y gestión del dato

Un **Sistema de Información (SI)** es un conjunto de componentes interrelacionados (hardware, software, datos, personas y procesos) que recopilan, procesan, almacenan y distribuyen información para apoyar la toma de decisiones y el control en una organización.

La **Gestión del Dato (Data Management)** comprende el desarrollo, ejecución y supervisión de planes, políticas, programas y prácticas que entregan, controlan, protegen y aumentan el valor de los datos y la información. El estándar de referencia en la industria es el marco **DAMA-DMBOK**, el cual establece las siguientes áreas de conocimiento principales:

*   **Gobernanza de Datos:** Ejercicio de autoridad, control y toma de decisiones compartida sobre la gestión de los activos de datos. Establece roles (Data Owner, Data Steward).
*   **Arquitectura de Datos:** Define las necesidades de datos de la empresa y diseña los planos para satisfacerlas.
*   **Gestión de Datos Maestros y de Referencia (MDM):** Control sobre los datos críticos de la organización (entidades clave como ciudadanos, empleados, infraestructuras) para proporcionar una "única versión de la verdad" (*Golden Record*).
*   **Calidad de Datos:** Procesos para medir, monitorizar y mejorar la precisión, completitud, coherencia y actualidad de los datos.
*   **Seguridad de los Datos:** Garantía de la privacidad, confidencialidad y acceso adecuado. En la Administración Pública Española, esto se rige de forma estricta por el Esquema Nacional de Seguridad (ENS, Real Decreto 311/2022) y el Reglamento General de Protección de Datos (RGPD) junto con la LOPDGDD.

**Clasificación de los Sistemas de Información según su nivel organizativo**
Complementando la definición general de SI, la literatura clásica de sistemas de información distingue distintos tipos según el nivel jerárquico y la función que desempeñan en la organización, clasificación que suele aparecer en preguntas de identificación:

*   **Sistemas de Procesamiento de Transacciones (TPS - Transaction Processing Systems):** gestionan las operaciones rutinarias y repetitivas del día a día (nóminas, facturación, registro de expedientes), constituyendo la base operativa sobre la que se apoyan el resto de sistemas.
*   **Sistemas de Información de Gestión (MIS - Management Information Systems):** generan informes periódicos y estructurados a partir de los datos de los TPS, dirigidos a la gestión de nivel medio para el control operativo.
*   **Sistemas de Apoyo a la Decisión (DSS - Decision Support Systems):** herramientas analíticas e interactivas que ayudan a la toma de decisiones semiestructuradas mediante modelos de simulación, análisis de escenarios y proyecciones.
*   **Sistemas de Información Ejecutiva (EIS - Executive Information Systems):** proporcionan a la alta dirección una visión sintética y estratégica del estado de la organización, habitualmente mediante cuadros de mando de alto nivel.

## 2. Bases de datos y almacenamiento

Las bases de datos son el núcleo del almacenamiento estructurado y no estructurado en los sistemas de información, dividiéndose principalmente en dos grandes paradigmas:

### 2.1 Bases de Datos Relacionales (RDBMS)
Almacenan la información en tablas (filas y columnas) fuertemente tipadas y normalizadas. Utilizan SQL (*Structured Query Language*).
*   **Propiedades ACID:** Garantizan transacciones fiables mediante Atomicidad, Consistencia, Aislamiento (*Isolation*) y Durabilidad.
*   **Uso:** Sistemas transaccionales (OLTP), aplicaciones de gestión financiera, registros administrativos críticos.
*   **Ejemplos:** Oracle, PostgreSQL, MySQL, SQL Server.

### 2.2 Bases de Datos NoSQL
Diseñadas para modelos de datos específicos, esquemas flexibles y alta escalabilidad horizontal. Se basan en el **Teorema CAP** (Consistencia, Disponibilidad, Tolerancia a Particiones), priorizando generalmente la disponibilidad y la tolerancia a particiones frente a la consistencia estricta (propiedades BASE: *Basically Available, Soft state, Eventual consistency*).
*   **Clave-Valor:** Optimizadas para lecturas rápidas mediante diccionarios (ej. Redis, DynamoDB).
*   **Documentales:** Almacenan datos en formatos semiestructurados como JSON o BSON (ej. MongoDB, Couchbase).
*   **Columnares:** Almacenan datos por columnas, ideales para analítica de grandes volúmenes y series temporales (ej. Apache Cassandra, HBase).
*   **Grafos:** Estructuras de nodos y aristas para modelar relaciones complejas (ej. Neo4j).

**El Teorema CAP en detalle**
El Teorema CAP fue formulado inicialmente como conjetura por Eric Brewer en una conferencia (PODC 2000) y demostrado formalmente en 2002 por Seth Gilbert y Nancy Lynch, del MIT, en su publicación académica *"Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services"*. El teorema demuestra que, en un sistema distribuido de almacenamiento de datos, resulta imposible garantizar simultáneamente las tres propiedades siguientes, pudiendo satisfacerse como máximo dos de ellas a la vez:

*   **Consistencia (Consistency):** todos los nodos ven exactamente los mismos datos al mismo tiempo; cualquier lectura posterior a una escritura debe devolver ese valor actualizado (o uno posterior) en todos los nodos.
*   **Disponibilidad (Availability):** toda solicitud recibida por un nodo que no haya fallado debe generar una respuesta, sin excepción, aunque parte del sistema esté caído.
*   **Tolerancia a particiones (Partition tolerance):** el sistema debe seguir funcionando aunque se produzcan fallos de comunicación (pérdida o retraso de mensajes) entre los nodos que lo componen.

Dado que las particiones de red son inevitables en cualquier sistema distribuido real, en la práctica la decisión de diseño se reduce a elegir entre **Consistencia** y **Disponibilidad** cuando se produce una partición: los sistemas **CP** (Consistencia + tolerancia a Particiones) rechazan responder si no pueden garantizar el dato más reciente, mientras que los sistemas **AP** (Disponibilidad + tolerancia a Particiones) siempre responden, aunque el dato devuelto pueda estar desactualizado hasta que se resincronicen los nodos (consistencia eventual). Esta decisión de diseño explica por qué la mayoría de las bases NoSQL orientadas a escalabilidad masiva (como Cassandra o DynamoDB) priorizan el modelo AP frente al modelo CP típico de los RDBMS tradicionales.

### 2.3 Tecnologías de Almacenamiento a nivel de infraestructura
*   **DAS (Direct Attached Storage):** Almacenamiento conectado directamente al servidor.
*   **NAS (Network Attached Storage):** Dispositivos de almacenamiento accesibles a través de protocolos de red (NFS, SMB/CIFS). Operan a nivel de sistema de archivos.
*   **SAN (Storage Area Network):** Red dedicada de alta velocidad que proporciona acceso a almacenamiento a nivel de bloque (Fibre Channel, iSCSI).
*   **Object Storage (Almacenamiento de Objetos):** Almacena datos como objetos discretos con metadatos asociados y un identificador único, altamente escalable, estándar en la nube (ej. Amazon S3, Azure Blob Storage).

## 3. APIs y servicios de integración

La interoperabilidad y la comunicación entre sistemas desacoplados se sustentan en Interfaces de Programación de Aplicaciones (APIs) y patrones de integración.

### 3.1 Estilos Arquitectónicos de APIs
*   **REST (Representational State Transfer):** Estilo arquitectónico basado en la web. Utiliza los métodos estándar de HTTP (GET, POST, PUT, DELETE) y se basa en recursos (URIs). Es *stateless* (sin estado) y la representación de datos más común es JSON.
*   **SOAP (Simple Object Access Protocol):** Protocolo estándar basado en XML. Utiliza contratos estrictos definidos en WSDL (*Web Services Description Language*). Destaca por su alta extensibilidad en seguridad (WS-Security) y transaccionalidad (WS-Transaction), siendo frecuente en entornos institucionales y bancarios heredados.
*   **GraphQL:** Lenguaje de consulta para APIs desarrollado por Facebook que permite a los clientes solicitar exactamente los datos que necesitan en una sola petición, resolviendo problemas de *over-fetching* (sobre-obtención de datos) y *under-fetching*.
*   **gRPC:** Marco de llamada a procedimiento remoto (RPC) de alto rendimiento desarrollado por Google. Utiliza HTTP/2 y Protocol Buffers (Protobuf) para la serialización binaria, ideal para microservicios internos.

**Semántica de los métodos HTTP según el RFC 9110**
El estándar de referencia que define formalmente la semántica de los métodos HTTP utilizados por las APIs REST es el **RFC 9110, "HTTP Semantics"**, publicado por el IETF (Internet Engineering Task Force) en junio de 2022, que consolida y sustituye a especificaciones anteriores dispersas (RFC 7230-7235), elevándose a Estándar de Internet (STD 97). El RFC 9110 caracteriza cada método según dos propiedades clave, muy examinables por su precisión técnica:

*   **Métodos seguros (safe):** no deberían tener ningún efecto significativo distinto de la recuperación de información; es el caso del método **GET**, que solicita la transferencia de una representación del recurso sin modificarlo, lo que permite que sus respuestas puedan almacenarse en caché y precargarse.
*   **Métodos idempotentes:** el efecto de realizar la misma petición varias veces es idéntico al de realizarla una sola vez. **GET**, **PUT** y **DELETE** son idempotentes: repetir un PUT reemplaza el recurso con el mismo estado final, y repetir un DELETE sobre un recurso ya eliminado deja el resultado igual (eliminado). **POST**, en cambio, **no es seguro ni idempotente**: enviar la misma petición POST dos veces puede crear dos recursos distintos (por ejemplo, dos pedidos duplicados), ya que su propósito es procesar el contenido enviado según la semántica específica del recurso de destino.

Esta distinción safe/idempotente es una trampa de examen habitual: no debe confundirse "idempotente" con "sin efectos" (PUT y DELETE tienen efectos pero son idempotentes) ni asumir que todos los métodos HTTP comparten las mismas garantías de repetición.

### 3.2 Servicios de Integración
*   **API Gateway:** Punto de entrada único para un conjunto de microservicios. Proporciona enrutamiento, composición de APIs, limitación de tasa (*rate limiting*), autenticación, y terminación SSL.
*   **ESB (Enterprise Service Bus):** Componente centralizado de la arquitectura SOA (Arquitectura Orientada a Servicios) que gestiona la comunicación, transformación de mensajes y enrutamiento entre servicios dispares.
*   **Arquitectura de Microservicios:** Paradigma donde las aplicaciones se componen de servicios pequeños, independientes y débilmente acoplados, que se comunican entre sí a través de APIs ligeras o buses de eventos (ej. Kafka, RabbitMQ).

## 4. Herramientas de Business Intelligence

El *Business Intelligence* (BI) abarca las estrategias y tecnologías utilizadas por las organizaciones para el análisis de datos de información empresarial, transformando datos en bruto en conocimiento accionable.

### 4.1 Componentes de una Arquitectura BI
*   **Data Warehouse / Data Mart:** Repositorios de datos modelados dimensionalmente (modelos en estrella o copo de nieve) para el análisis histórico.
*   **Procesos ETL/ELT:** Integración de datos que Extrae, Transforma y Carga información desde los sistemas operacionales hacia el Data Warehouse.
*   **OLAP (Online Analytical Processing):** Tecnología que permite el análisis multidimensional de datos a alta velocidad (Cubos OLAP) mediante operaciones como *drill-down*, *roll-up* y *slice-and-dice*.

**Operaciones OLAP y modelado dimensional**
Conviene precisar el significado exacto de las operaciones OLAP más citadas, ya que suelen confundirse entre sí:
*   **Drill-down (desagregación):** navega desde un nivel de agregación alto hacia un nivel de mayor detalle (por ejemplo, de ventas anuales a ventas mensuales).
*   **Roll-up (agregación):** operación inversa al drill-down, consolida datos de un nivel de detalle hacia un nivel más agregado.
*   **Slice:** selecciona un subconjunto del cubo fijando el valor de una única dimensión (por ejemplo, ver solo los datos del año 2025).
*   **Dice:** selecciona un subcubo fijando valores concretos en varias dimensiones simultáneamente.
*   **Pivot (rotación):** reorienta la vista del cubo intercambiando filas y columnas para observar los datos desde otra perspectiva.

En cuanto al modelo dimensional, el **esquema en estrella (star schema)** organiza una tabla de hechos central (con las métricas cuantitativas) rodeada de tablas de dimensiones desnormalizadas conectadas directamente a ella, priorizando la velocidad de consulta. El **esquema en copo de nieve (snowflake schema)** normaliza además las propias tablas de dimensiones en subtablas relacionadas jerárquicamente, reduciendo la redundancia de datos a costa de consultas con más uniones (joins) y, por tanto, algo más lentas.

### 4.2 Categorías de Herramientas BI
*   **Cuadros de mando (Dashboards):** Herramientas de visualización interactiva que consolidan KPIs y métricas críticas en una única pantalla (ej. Power BI, Tableau, Qlik Sense).
*   **Reporting Empresarial:** Generación de informes estáticos, altamente formateados y paginados (ej. SQL Server Reporting Services).
*   **Data Discovery y Self-Service BI:** Plataformas que permiten a los usuarios de negocio, sin profundos conocimientos técnicos, explorar datos, crear modelos y generar sus propias visualizaciones de forma autónoma.

## 5. Tendencias tecnológicas en gestión del dato

El ecosistema de gestión de datos está en constante evolución, impulsado por el volumen de información y la necesidad de agilidad en la Inteligencia Artificial.

*   **Data Fabric (Tejido de Datos):** Arquitectura de gestión de datos que integra y conecta datos a través de plataformas dispares (on-premise, cloud, edge) mediante un acceso continuo. Utiliza la automatización impulsada por IA para el descubrimiento y orquestación de datos y metadatos.
*   **Data Mesh (Malla de Datos):** Paradigma organizativo y arquitectónico descentralizado. Trata a los datos como un "producto", donde los equipos de dominio específicos son propietarios de sus datos y los exponen a través de interfaces estandarizadas, rompiendo el modelo monolítico del Data Lake central.
*   **Augmented Analytics (Analítica Aumentada):** Integración de Machine Learning y Procesamiento de Lenguaje Natural (NLP) en las plataformas de BI para automatizar la preparación de datos, el descubrimiento de patrones (insights) y la generación de narrativas, democratizando el análisis complejo.
*   **Gobernanza de Datos para IA (AI Governance):** Con la irrupción del Reglamento (UE) 2024/1689 de Inteligencia Artificial, se exige una trazabilidad exhaustiva, control de sesgos (*bias detection*) y calidad demostrable en los conjuntos de datos de entrenamiento, validación y prueba para sistemas de IA de alto riesgo.
*   **Real-time Stream Processing:** Transición de los procesos por lotes (batch) al análisis de datos en movimiento. Tecnologías como Apache Kafka, Apache Flink y Spark Streaming permiten ingerir y analizar eventos en tiempo real, habilitando respuestas instantáneas del sistema ante anomalías operativas o de seguridad.

**Data Mesh: los cuatro principios fundacionales**
El paradigma Data Mesh, formulado originalmente por Zhamak Dehghani, se articula en torno a cuatro principios que conviene diferenciar con precisión porque suelen preguntarse de forma aislada:
1.  **Propiedad de datos orientada al dominio (Domain-oriented ownership):** cada dominio de negocio es responsable de sus propios datos, en lugar de centralizar esa responsabilidad en un equipo único de datos.
2.  **Datos como producto (Data as a product):** cada conjunto de datos expuesto por un dominio debe tratarse con los mismos estándares de calidad, documentación y facilidad de descubrimiento que un producto de software dirigido a usuarios (internos o externos).
3.  **Infraestructura de datos como plataforma de autoservicio (Self-serve data platform):** una infraestructura común y transversal que permite a cada dominio publicar y consumir datos de forma autónoma, sin depender de un equipo central para cada tarea técnica.
4.  **Gobernanza federada y computacional (Federated computational governance):** un modelo de gobernanza que combina estándares globales comunes (interoperabilidad, seguridad, cumplimiento normativo) con autonomía local de cada dominio, automatizando en la medida de lo posible el cumplimiento de dichos estándares mediante políticas ejecutables por la propia plataforma.

## Referencias técnicas

*   Gilbert, S. y Lynch, N., *"Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services"*, ACM SIGACT News, 2002 (demostración formal del Teorema CAP conjeturado por Eric Brewer en PODC 2000).
*   IETF, RFC 9110, *"HTTP Semantics"*, junio de 2022 (Estándar de Internet STD 97).
*   DAMA International, *DAMA-DMBOK: Data Management Body of Knowledge*, 2ª edición.
*   Real Decreto 311/2022, de 3 de mayo, por el que se regula el Esquema Nacional de Seguridad.
*   Reglamento (UE) 2016/679 (RGPD) y Ley Orgánica 3/2018 (LOPDGDD).
*   Reglamento (UE) 2024/1689, por el que se establecen normas armonizadas en materia de inteligencia artificial.
