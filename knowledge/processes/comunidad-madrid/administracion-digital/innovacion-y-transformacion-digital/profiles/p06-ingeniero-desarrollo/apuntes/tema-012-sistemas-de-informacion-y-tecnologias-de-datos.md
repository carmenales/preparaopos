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
  - "data-lake"
  - "data-lakehouse"
  - "bases-de-datos-vectoriales"
  - "dataops"
created_at: "2026-09-03"
last_reviewed: "2026-09-13"
ai_generated: true
ai_sources:
  - "perplexity"
  - "chatgpt"
  - "gemini"
  - "claude"
needs_human_review: true
---

# Tema 12. Sistemas de información y tecnologías de datos

## 1. Sistemas de información y gestión del dato

Un **Sistema de Información (SI)** es un conjunto de componentes interrelacionados (hardware, software, datos, personas y procesos) que recopilan, procesan, almacenan y distribuyen información para apoyar la toma de decisiones, la coordinación y el control en una organización. Además de respaldar la toma de decisiones, los SI también ayudan a los gestores y trabajadores a analizar problemas, visualizar asuntos complejos y crear nuevos productos o servicios.

La **Gestión del Dato (Data Management)** comprende el desarrollo, ejecución y supervisión de planes, políticas, programas y prácticas que entregan, controlan, protegen y aumentan el valor de los datos y la información a lo largo de todo su ciclo de vida. El estándar de referencia en la industria es el marco **DAMA-DMBOK** (Data Management Body of Knowledge), el cual establece las siguientes áreas de conocimiento principales:

*   **Gobernanza de Datos:** Ejercicio de autoridad, control y toma de decisiones compartida sobre la gestión de los activos de datos. Establece el marco operativo y roles fundamentales como el *Data Owner* (responsable de negocio del dato) y el *Data Steward* (gestor operativo del dato).
*   **Arquitectura de Datos:** Define las necesidades de datos de la empresa y diseña los planos lógicos y físicos para satisfacerlas, asegurando la alineación con la arquitectura empresarial.
*   **Gestión de Datos Maestros y de Referencia (MDM):** Control sobre los datos críticos de la organización (entidades clave como ciudadanos, empleados, infraestructuras, nomenclátores) para proporcionar una "única versión de la verdad" (*Golden Record*) en toda la entidad.
*   **Gestión de Metadatos:** Creación, control y soporte al acceso de los metadatos (datos sobre los datos), fundamentales para los diccionarios de datos, catálogos y la trazabilidad (linaje del dato).
*   **Calidad de Datos:** Procesos para medir, monitorizar y mejorar dimensiones de calidad como la precisión, completitud, coherencia, integridad y actualidad de los datos.
*   **Seguridad de los Datos:** Garantía de la privacidad, confidencialidad y acceso adecuado. En la Administración Pública Española, la seguridad de la información está regulada de forma estricta por el Esquema Nacional de Seguridad (ENS, regulado en el Real Decreto 311/2022) y el marco de privacidad definido por el Reglamento General de Protección de Datos (RGPD) y la Ley Orgánica 3/2018 (LOPDGDD).

**Clasificación de los Sistemas de Información según su nivel organizativo**
La literatura clásica de sistemas de información distingue diferentes tipologías según el nivel jerárquico y la función que desempeñan en la organización:

*   **Sistemas de Procesamiento de Transacciones (TPS - Transaction Processing Systems):** Gestionan las operaciones rutinarias y repetitivas del día a día (nóminas, facturación, registro de entrada/salida de expedientes). Tienen un alto volumen de entrada y salida, requiriendo alta disponibilidad y constituyendo la base operativa sobre la que se apoyan el resto de sistemas.
*   **Sistemas de Información de Gestión (MIS - Management Information Systems):** Generan informes periódicos y estructurados a partir de los datos consolidados de los TPS. Están dirigidos a la gestión de nivel medio para la planificación, el control operativo y la toma de decisiones estructuradas.
*   **Sistemas de Apoyo a la Decisión (DSS - Decision Support Systems):** Herramientas analíticas e interactivas que ayudan a la toma de decisiones semiestructuradas o no estructuradas mediante modelos de simulación, análisis estadístico, escenarios ("what-if") y proyecciones.
*   **Sistemas de Información Ejecutiva (EIS - Executive Information Systems):** Proporcionan a la alta dirección una visión sintética y estratégica del estado de la organización, habitualmente mediante cuadros de mando (dashboards) de alto nivel, permitiendo el *drill-down* (navegación hacia el detalle).

Adicionalmente, las arquitecturas modernas contemplan sistemas transversales de integración institucional:
*   **ERP (Enterprise Resource Planning):** Sistemas integrados de gestión empresarial que unifican procesos de finanzas, recursos humanos, compras y logística en una base de datos centralizada.
*   **CRM (Customer Relationship Management):** Orientados a la gestión de las relaciones con los clientes o ciudadanos, centralizando la información de contacto y el historial de interacciones.
*   **BPM (Business Process Management):** Sistemas orientados a la automatización, orquestación y monitorización de procesos de negocio complejos.

## 2. Bases de datos y almacenamiento

Las bases de datos son el núcleo del almacenamiento estructurado, semiestructurado y no estructurado en los sistemas de información, dividiéndose principalmente en dos grandes paradigmas:

### 2.1 Bases de Datos Relacionales (RDBMS)
Almacenan la información en tablas (relaciones conformadas por filas/tuplas y columnas/atributos) fuertemente tipadas y basadas en el álgebra relacional. Utilizan **SQL** (*Structured Query Language*).

*   **Propiedades ACID:** Garantizan la fiabilidad de las transacciones en los RDBMS:
    *   *Atomicidad (Atomicity):* Una transacción se ejecuta completamente o no se ejecuta en absoluto ("todo o nada").
    *   *Consistencia (Consistency):* Cualquier transacción llevará a la base de datos de un estado válido a otro estado válido, cumpliendo todas las restricciones de integridad definidas.
    *   *Aislamiento (Isolation):* La ejecución concurrente de transacciones produce el mismo estado que si se ejecutaran de forma secuencial.
    *   *Durabilidad (Durability):* Una vez que una transacción ha sido confirmada (*committed*), persistirá incluso en caso de fallo del sistema.
*   **Normalización:** Proceso de diseño para minimizar la redundancia y evitar anomalías de actualización. Las formas normales más habituales son la Primera Forma Normal (1FN), Segunda Forma Normal (2FN), Tercera Forma Normal (3FN) y la Forma Normal de Boyce-Codd (BCNF).
*   **Uso y ejemplos:** Sistemas transaccionales críticos (OLTP), registros administrativos, contabilidad. Ejemplos: Oracle, PostgreSQL, MySQL, Microsoft SQL Server.

### 2.2 Bases de Datos NoSQL
Diseñadas para modelos de datos específicos, esquemas flexibles (schema-less o schema-on-read) y alta escalabilidad horizontal. Se fundamentan en el **Teorema CAP** y adoptan frecuentemente el modelo de consistencia **BASE** (*Basically Available, Soft state, Eventual consistency*), que relaja las garantías ACID para favorecer el rendimiento y la tolerancia a fallos.

*   **Clave-Valor:** Almacenan pares de clave única y su valor asociado. Optimizadas para lecturas extremadamente rápidas mediante diccionarios o tablas hash (ej. Redis, Amazon DynamoDB, Memcached).
*   **Documentales:** Almacenan datos en formatos semiestructurados como JSON, BSON o XML. Permiten indexación sobre el contenido del documento y estructuras jerárquicas complejas (ej. MongoDB, CouchDB).
*   **Columnares (Wide-column stores):** Almacenan datos en familias de columnas en lugar de filas. Ideales para analítica de grandes volúmenes de datos distribuidos y escalabilidad masiva (ej. Apache Cassandra, HBase).
*   **Grafos:** Utilizan estructuras de nodos, aristas (relaciones) y propiedades para representar y consultar redes de información interconectada altamente compleja, utilizando lenguajes específicos como Cypher o Gremlin (ej. Neo4j, Amazon Neptune).
*   **Vectoriales:** Categoría de bases de datos NoSQL especializada en el almacenamiento e indexación de *embeddings* (vectores numéricos de alta dimensión que representan el significado semántico de textos, imágenes u otros contenidos). A diferencia de una consulta relacional por coincidencia exacta, resuelven consultas por **similitud semántica**, calculada mediante métricas de distancia (coseno, euclídea o producto escalar) sobre índices especializados (como HNSW o IVFFlat). Constituyen la pieza de infraestructura central de las arquitecturas RAG (*Retrieval-Augmented Generation*) y de los motores de búsqueda y recomendación semántica. Se distingue entre bases de datos vectoriales dedicadas (Pinecone, Milvus, Weaviate, Qdrant) y extensiones vectoriales incorporadas a motores relacionales ya existentes, como **pgvector** para PostgreSQL.

**El Teorema CAP y la extensión PACELC**
El Teorema CAP fue formulado inicialmente por Eric Brewer y demostrado formalmente en 2002 por Seth Gilbert y Nancy Lynch en la publicación *"Brewer's Conjecture and the Feasibility of Consistent, Available, Partition-Tolerant Web Services"*. Demuestra que, en un sistema informático distribuido, resulta imposible garantizar simultáneamente las tres propiedades siguientes:

*   **Consistencia (Consistency):** Todos los nodos ven exactamente los mismos datos al mismo tiempo. Una lectura siempre devuelve la escritura más reciente o un error.
*   **Disponibilidad (Availability):** Toda solicitud recibida por un nodo operativo del sistema genera una respuesta no errónea, sin garantía de que contenga la información más reciente.
*   **Tolerancia a particiones (Partition tolerance):** El sistema continúa funcionando a pesar de la pérdida arbitraria de mensajes o fallos de red entre nodos.

Dado que las particiones de red son inevitables en un sistema distribuido, un sistema de estas características debe elegir obligatoriamente entre **Consistencia (CP)** o **Disponibilidad (AP)** frente a un fallo de red.

Posteriormente, el **Teorema PACELC** (formulado por Daniel Abadi) extendió el Teorema CAP. PACELC establece que, si hay una partición (P), el sistema debe elegir entre Disponibilidad (A) y Consistencia (C); pero de lo contrario (E - *Else*), cuando el sistema funciona normalmente sin particiones, debe elegir entre Latencia (L - *Latency*) y Consistencia (C).

### 2.3 Tecnologías de Almacenamiento a nivel de infraestructura
*   **DAS (Direct Attached Storage):** Almacenamiento físico conectado directamente al bus del servidor. Alto rendimiento local pero nula compartición a nivel de red.
*   **NAS (Network Attached Storage):** Dispositivos de almacenamiento accesibles a través de redes TCP/IP utilizando protocolos de nivel de archivo (NFS, SMB/CIFS, AFP). Operan a nivel de sistema de ficheros.
*   **SAN (Storage Area Network):** Red dedicada de alta velocidad que proporciona acceso a almacenamiento a nivel de bloque, visible para los sistemas operativos como si fueran discos duros locales. Utiliza protocolos específicos como Fibre Channel, FCoE o iSCSI.
*   **Object Storage (Almacenamiento de Objetos):** Almacena datos como objetos discretos agrupados en contenedores (buckets), acompañados de metadatos detallados y un identificador único (URI). Presenta un espacio de nombres plano, es altamente escalable horizontalmente y constituye el estándar de almacenamiento masivo en plataformas cloud (ej. Amazon S3, Azure Blob Storage).

## 3. APIs y servicios de integración

La interoperabilidad y la comunicación entre sistemas desacoplados se sustentan en Interfaces de Programación de Aplicaciones (APIs) y patrones de integración estandarizados.

### 3.1 Estilos Arquitectónicos y Protocolos de APIs
*   **REST (Representational State Transfer):** Estilo arquitectónico basado en los estándares de la Web. Se apoya en recursos identificados por URIs y métodos HTTP. Es estricto respecto a su naturaleza *stateless* (sin estado en el servidor). La madurez de un servicio REST se clasifica mediante el **Modelo de Madurez de Richardson** (Nivel 0: pantano del POX; Nivel 1: recursos; Nivel 2: verbos HTTP; Nivel 3: controles hipermedia o **HATEOAS** - *Hypermedia As The Engine Of Application State*).
*   **SOAP (Simple Object Access Protocol):** Protocolo estándar de intercambio de mensajes basado en XML. Utiliza contratos estrictos y legibles por máquina definidos en WSDL (*Web Services Description Language*). Destaca por su alta extensibilidad formalizada en los estándares WS-* (como WS-Security para autenticación/firma y WS-ReliableMessaging para entrega garantizada).
*   **GraphQL:** Lenguaje de consulta e inserción para APIs desarrollado por Facebook. Permite a los clientes solicitar exactamente la estructura de datos que necesitan en una sola petición a un único punto de acceso (endpoint), resolviendo ineficiencias clásicas de REST como el *over-fetching* (obtención de datos excesivos) y el *under-fetching* (obtención insuficiente que obliga a múltiples peticiones).
*   **gRPC:** Marco de llamada a procedimiento remoto (RPC) de alto rendimiento, de código abierto, desarrollado inicialmente por Google. Utiliza HTTP/2 como transporte y **Protocol Buffers (Protobuf)** como lenguaje de descripción de interfaz y serialización binaria, proporcionando una comunicación extremadamente rápida, ideal para microservicios internos.

**Semántica de los métodos HTTP según el RFC 9110**
El estándar que define formalmente la semántica de los métodos HTTP utilizados por las APIs REST es el **RFC 9110, "HTTP Semantics"** (Estándar de Internet STD 97 del IETF). El documento caracteriza los métodos según tres propiedades fundamentales:

*   **Métodos seguros (Safe):** No deben tener el propósito de producir efectos secundarios en el servidor; son de solo lectura. Ejemplo: **GET**, **HEAD**, **OPTIONS**, **TRACE**.
*   **Métodos idempotentes (Idempotent):** El efecto de realizar la misma petición de manera sucesiva múltiples veces es idéntico al de realizarla una sola vez. Todo método seguro es idempotente. Además, **PUT** y **DELETE** son idempotentes (repetir un PUT sobrescribe el recurso con el mismo estado, y repetir un DELETE sobre un recurso inexistente deja el sistema en el mismo estado).
*   **Cachables (Cacheable):** Respuestas que pueden ser almacenadas y reutilizadas posteriormente. Las respuestas a peticiones **GET**, **HEAD** y en ciertos casos **POST** pueden ser cacheadas.
*   **El método POST:** El método **POST** está diseñado para procesar la representación adjunta de acuerdo con la semántica del recurso destino. **No es seguro ni es idempotente**: enviar la misma petición POST varias veces puede resultar en la creación de múltiples recursos diferenciados.

### 3.2 Servicios y Patrones de Integración
*   **API Gateway:** Punto de entrada único (Single Point of Entry) que expone servicios de backend a clientes externos. Actúa como proxy inverso y centraliza funciones de corte transversal como el enrutamiento (routing), composición de APIs, limitación de tasa (*rate limiting* o *throttling*), autenticación, autorización, validación de cuotas, y terminación SSL. En arquitecturas modernas se complementa con el patrón **BFF (Backend For Frontend)**.
*   **ESB (Enterprise Service Bus):** Componente centralizado propio de la Arquitectura Orientada a Servicios (SOA). Gestiona la comunicación entre aplicaciones heterogéneas implementando mediación, enrutamiento inteligente basado en contenido y transformación de mensajes.
*   **Arquitectura de Microservicios:** Paradigma de diseño donde una aplicación se estructura como un conjunto de servicios pequeños, funcionalmente independientes y débilmente acoplados. Favorecen patrones de comunicación asíncrona (coreografía de eventos a través de *message brokers* como Apache Kafka o RabbitMQ) frente a la comunicación síncrona (orquestación).

## 4. Herramientas de Business Intelligence

El *Business Intelligence* (BI) abarca las estrategias y tecnologías utilizadas por las organizaciones para la integración y análisis de la información, transformando datos operacionales en bruto en conocimiento accionable y soporte a la toma de decisiones.

### 4.1 Arquitectura y Modelado BI
*   **Data Warehouse (Almacén de Datos):** Repositorio central corporativo orientado a consultas analíticas. Tradicionalmente se diseña bajo dos enfoques principales:
    *   *Enfoque Top-Down (Bill Inmon):* Se construye un Almacén de Datos Corporativo (EDW) central normalizado (3FN), a partir del cual se derivan Data Marts departamentales dependientes.
    *   *Enfoque Bottom-Up (Ralph Kimball):* Se construyen primero los Data Marts individuales modelados dimensionalmente, y el Data Warehouse corporativo surge de la unión de estos mediante el uso de dimensiones conformadas (Bus de Arquitectura Empresarial).
*   **Data Lake (Lago de Datos):** Repositorio centralizado, cuyo término fue acuñado en 2010 por James Dixon (entonces CTO de Pentaho), que almacena grandes volúmenes de datos estructurados, semiestructurados y no estructurados en su formato nativo u original, sin necesidad de transformarlos ni definir un esquema previo (*schema-on-read*), habitualmente sobre almacenamiento de objetos de bajo coste (como Hadoop HDFS o Amazon S3). Frente a la rigidez del esquema predefinido del Data Warehouse (*schema-on-write*), el Data Lake ofrece mayor flexibilidad y libertad de exploración a analistas y científicos de datos, a costa de un mayor riesgo de degradar su calidad y gobernanza si no se gestiona adecuadamente (fenómeno conocido informalmente como *data swamp* o "pantano de datos").
*   **Data Lakehouse:** Arquitectura de convergencia, popularizada comercialmente por Databricks a partir de 2020, que combina el almacenamiento de bajo coste y la flexibilidad del Data Lake con las garantías transaccionales, el control de esquema y el rendimiento analítico propios del Data Warehouse. Esta convergencia se hace posible mediante los denominados **formatos de tabla abiertos** (*open table formats*), una capa de metadatos que se sitúa sobre los ficheros del Data Lake (habitualmente en formato Parquet) y les añade transacciones ACID, evolución y validación de esquemas, y capacidades de *time travel* (consulta de versiones anteriores de los datos). Los tres formatos de tabla abiertos de referencia son **Delta Lake** (desarrollado por Databricks), **Apache Iceberg** y **Apache Hudi**.

*   **Modelado Dimensional:** Técnica de diseño de bases de datos orientada a la recuperación de información, compuesta por:
    *   *Tabla de Hechos (Fact Table):* Almacena las métricas cuantitativas del negocio (ej. importes, cantidades) y las claves foráneas a las dimensiones.
    *   *Tablas de Dimensiones (Dimension Tables):* Contienen los atributos descriptivos que dan contexto a los hechos (ej. tiempo, cliente, producto).
    *   *Dimensiones Lentamente Cambiantes (SCD - Slowly Changing Dimensions):* Técnicas para gestionar modificaciones históricas. Destacan el Tipo 1 (sobrescritura del valor), Tipo 2 (creación de nueva fila con rango de fechas) y Tipo 3 (añadir nueva columna para el valor anterior).
*   **Esquemas:**
    *   *Estrella (Star Schema):* Una tabla de hechos central rodeada por dimensiones totalmente desnormalizadas.
    *   *Copo de Nieve (Snowflake Schema):* Variación donde las tablas de dimensiones están normalizadas en múltiples jerarquías, reduciendo el espacio pero incrementando la complejidad (joins).

**Procesos de Integración: ETL vs. ELT**
*   **ETL (Extract, Transform, Load):** El motor de integración extrae los datos, los transforma en un servidor de paso intermedio (limpieza, normalización, cruce) y posteriormente los carga en el almacén destino. Óptimo cuando el destino tiene poca capacidad de cómputo o existen fuertes requisitos de enmascaramiento previo.
*   **ELT (Extract, Load, Transform):** Los datos se extraen y cargan crudos (*raw*) directamente en la plataforma de destino. La transformación se realiza internamente ejecutando consultas nativas que aprovechan la capacidad de Procesamiento Masivo Paralelo (MPP) de las modernas bases de datos analíticas.

**OLAP (Online Analytical Processing)**
Tecnología para análisis rápido y multidimensional (cubos OLAP) mediante operaciones clásicas:
*   *Drill-down* (bajar al detalle) y *Roll-up* (agregación).
*   *Slice* (filtrar por un solo valor dimensional) y *Dice* (filtrar un subcubo seleccionando valores en varias dimensiones).
*   *Pivot* (rotar ejes).
Las arquitecturas físicas OLAP se clasifican en:
*   **MOLAP (Multidimensional OLAP):** Los datos pre-calculados se almacenan físicamente en estructuras de matriz multidimensional propietarias.
*   **ROLAP (Relational OLAP):** Los datos y agrupaciones permanecen en el motor relacional, resolviendo las consultas mediante SQL complejo en tiempo de ejecución.
*   **HOLAP (Hybrid OLAP):** Combina el almacenamiento de detalle en el modelo relacional (ROLAP) y los agregados pre-calculados en cubos multidimensionales (MOLAP).

### 4.2 Categorías de Herramientas BI
*   **Cuadros de mando (Dashboards):** Visualización interactiva orientada a la consolidación y monitorización de KPIs (Indicadores Clave de Rendimiento).
*   **Reporting Empresarial:** Generación de informes preformateados, estáticos, parametrizables y paginados, diseñados habitualmente para impresión o exportación (ej. JasperReports, SQL Server Reporting Services).
*   **Self-Service BI y Data Discovery:** Plataformas que permiten a los analistas de negocio explorar modelos de datos semánticos sin intervención continua de los departamentos de TI (ej. Microsoft Power BI, Qlik Sense, Tableau).

## 5. Tendencias tecnológicas en gestión del dato

El ecosistema analítico evoluciona hacia modelos distribuidos, gobernados en tiempo real y asistidos por aprendizaje automático.

*   **Data Fabric (Entramado de Datos):** Arquitectura tecnológica de integración unificada y automatizada. Conecta fuentes de datos on-premise, cloud y edge utilizando **grafos de conocimiento (Knowledge Graphs)** y gestión activa de metadatos. Se apoya en inteligencia artificial para inferir relaciones y sugerir integraciones, operando como una capa de red técnica.
*   **Data Mesh (Malla de Datos):** Paradigma sociotécnico formulado por Zhamak Dehghani que rompe con la arquitectura de datos monolítica. Se fundamenta en cuatro pilares:
    1.  *Propiedad descentralizada orientada al dominio:* La responsabilidad funcional y técnica del dato recae en el área de negocio que lo produce, no en un equipo central de TI.
    2.  *El dato como producto (Data as a Product):* Los conjuntos de datos deben ser tratados con rigurosidad de producto (descubribles, direccionables, confiables, seguros e interoperables).
    3.  *Infraestructura de datos como plataforma de autoservicio:* Un equipo central provee la tecnología subyacente para facilitar a los dominios el almacenamiento y publicación de sus productos.
    4.  *Gobernanza computacional federada:* Políticas globales de cumplimiento y seguridad ejecutadas de forma automatizada y unificada, respetando la autonomía de los dominios.
*   **Gobernanza para la Inteligencia Artificial (AI Governance):** Condicionada por el reciente Reglamento de Inteligencia Artificial (Reglamento UE 2024/1689). Impone requisitos técnicos obligatorios para los sistemas de alto riesgo respecto a los datos de entrenamiento, validación y prueba, los cuales deben ser pertinentes, representativos, trazables y estar sujetos a controles de mitigación de sesgos.
*   **Augmented Analytics (Analítica Aumentada):** Uso de algoritmos de Machine Learning y Procesamiento de Lenguaje Natural (NLP) directamente embebidos en plataformas BI para automatizar el perfilado de datos, descubrir patrones anómalos y generar explicaciones narrativas de forma automática.
*   **Real-Time Stream Processing:** Evolución del análisis por lotes (batch) hacia el procesamiento continuo de eventos de baja latencia. Arquitecturas como **Kappa** (donde todo el procesamiento, histórico y en tiempo real, se maneja mediante un único motor de streaming sobre registros inmutables) consolidan tecnologías como Apache Kafka, Apache Flink y Spark Streaming.
*   **DataOps:** Conjunto de prácticas y cultura organizativa que traslada los principios de la metodología DevOps (integración y entrega continuas, automatización, colaboración entre equipos) al ciclo de vida de los pipelines de datos. Persigue acortar el tiempo de entrega de nuevos conjuntos de datos y análisis, automatizando las pruebas de calidad del dato, el control de versiones de los pipelines y la monitorización continua de su ejecución, de forma análoga a como MLOps aplica estos mismos principios al ciclo de vida de los modelos de aprendizaje automático.

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
*   Dixon, J., entrada de blog en la que acuña el término *"Data Lake"*, Pentaho, 2010.
*   Databricks, *"What Is a Lakehouse?"*, enero de 2020; documentación de los formatos de tabla abiertos Delta Lake, Apache Iceberg y Apache Hudi.
