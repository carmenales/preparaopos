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
created_at: "2026-09-03"
last_reviewed: null
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
*   **Seguridad de los Datos:** Garantía de la privacidad, confidencialidad y acceso adecuado. En la Administración Pública Española, esto se rige de forma estricta por el Esquema Nacional de Seguridad (ENS) y el Reglamento General de Protección de Datos (RGPD) junto con la LOPDGDD.

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

### 4.2 Categorías de Herramientas BI
*   **Cuadros de mando (Dashboards):** Herramientas de visualización interactiva que consolidan KPIs y métricas críticas en una única pantalla (ej. Power BI, Tableau, Qlik Sense).
*   **Reporting Empresarial:** Generación de informes estáticos, altamente formateados y paginados (ej. SQL Server Reporting Services).
*   **Data Discovery y Self-Service BI:** Plataformas que permiten a los usuarios de negocio, sin profundos conocimientos técnicos, explorar datos, crear modelos y generar sus propias visualizaciones de forma autónoma.

## 5. Tendencias tecnológicas en gestión del dato

El ecosistema de gestión de datos está en constante evolución, impulsado por el volumen de información y la necesidad de agilidad en la Inteligencia Artificial.

*   **Data Fabric (Tejido de Datos):** Arquitectura de gestión de datos que integra y conecta datos a través de plataformas dispares (on-premise, cloud, edge) mediante un acceso continuo. Utiliza la automatización impulsada por IA para el descubrimiento y orquestación de datos y metadatos.
*   **Data Mesh (Malla de Datos):** Paradigma organizativo y arquitectónico descentralizado. Trata a los datos como un "producto", donde los equipos de dominio específicos son propietarios de sus datos y los exponen a través de interfaces estandarizadas, rompiendo el modelo monolítico del Data Lake central.
*   **Augmented Analytics (Analítica Aumentada):** Integración de Machine Learning y Procesamiento de Lenguaje Natural (NLP) en las plataformas de BI para automatizar la preparación de datos, el descubrimiento de patrones (insights) y la generación de narrativas, democratizando el análisis complejo.
*   **Gobernanza de Datos para IA (AI Governance):** Con la irrupción del Reglamento Europeo de IA (AI Act), se exige una trazabilidad exhaustiva, control de sesgos (*bias detection*) y calidad demostrable en los conjuntos de datos de entrenamiento, validación y prueba para sistemas de IA de alto riesgo.
*   **Real-time Stream Processing:** Transición de los procesos por lotes (batch) al análisis de datos en movimiento. Tecnologías como Apache Kafka, Apache Flink y Spark Streaming permiten ingerir y analizar eventos en tiempo real, habilitando respuestas instantáneas del sistema ante anomalías operativas o de seguridad.