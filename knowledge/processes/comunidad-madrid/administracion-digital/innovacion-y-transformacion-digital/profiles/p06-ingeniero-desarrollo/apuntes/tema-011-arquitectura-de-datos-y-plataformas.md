---
id: "cm-ad-innovacion-y-transformacion-digital-tema-011-arquitectura-de-datos-y-plataformas"
title: "Arquitectura de datos y plataformas"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/innovacion-y-transformacion-digital"
profiles:
  - "p06-ingeniero-desarrollo"
official_profiles:
  - "P06 - Ingeniero de Desarrollo"
official_topic: "Tema 11. Arquitectura de datos y plataformas"
source_ids: []
tags:
  - "arquitectura-del-dato"
  - "data-warehouse"
  - "data-lake"
  - "data-lakehouse"
  - "olap"
  - "etl"
  - "procesos-etl"
  - "procesamiento-batch"
  - "procesamiento-streaming"
  - "cloud"
  - "plataforma-cloud"
  - "plataforma-on-premise"
  - "on-premise"
created_at: "2026-09-03"
last_reviewed: null
ai_generated: true
ai_sources:
  - "perplexity"
  - "chatgpt"
  - "gemini"
needs_human_review: true
---

# Tema 11. Arquitectura de datos y plataformas

## 1. Arquitecturas de datos: Data Warehouse, Data Lake y Lakehouse

La arquitectura de datos establece los principios, modelos y tecnologías que rigen la ingesta, almacenamiento, procesamiento y explotación de los datos en una organización. En la evolución de los repositorios analíticos destacan tres paradigmas fundamentales:

**Data Warehouse (Almacén de Datos)**
*   **Definición:** Repositorio centralizado de datos estructurados, consolidados e integrados desde múltiples fuentes, optimizado para la consulta rápida y el análisis multidimensional (OLAP - *Online Analytical Processing*). Es la base tradicional de la Inteligencia de Negocio (BI).
*   **Paradigma:** Utiliza un enfoque *Schema-on-write* (esquema a la escritura). Los datos deben ser modelados, transformados y adaptados a un esquema predefinido (como estrella o copo de nieve) antes de ser cargados.
*   **Características:** Garantiza el cumplimiento de las propiedades ACID (Atomicidad, Consistencia, Aislamiento, Durabilidad). Su principal limitación radica en el alto coste de escalabilidad para volúmenes masivos y en su incapacidad nativa para gestionar datos no estructurados o semiestructurados.

**Data Lake (Lago de Datos)**
*   **Definición:** Repositorio escalable que permite almacenar grandes volúmenes de datos en su formato original o crudo (raw), abarcando datos estructurados, semiestructurados (JSON, XML, logs) y no estructurados (texto libre, imágenes, vídeo).
*   **Paradigma:** Utiliza un enfoque *Schema-on-read* (esquema a la lectura). La estructura y la semántica se aplican en el momento de la consulta, aportando gran agilidad en la fase de ingesta.
*   **Características:** Implementado habitualmente sobre sistemas de archivos distribuidos o almacenamiento de objetos. Es el entorno ideal para analítica avanzada, *Data Science* y entrenamiento de modelos de *Machine Learning*.
*   **Riesgos:** La falta de gobernanza, catalogación y gestión de metadatos puede transformar un Data Lake en un *Data Swamp* (pantano de datos), inutilizando la información almacenada por la imposibilidad de localizarla o comprenderla.

**Data Lakehouse**
*   **Definición:** Arquitectura de datos híbrida que unifica la flexibilidad, la escalabilidad horizontal y el bajo coste de almacenamiento de un *Data Lake* con las capacidades de gestión, rendimiento y transaccionalidad de un *Data Warehouse*.
*   **Características:** Implementa una capa de abstracción de metadatos y gestión de transacciones (basada en formatos de tabla abiertos como Apache Iceberg, Delta Lake o Apache Hudi) directamente sobre el almacenamiento de objetos.
*   **Ventajas:** Proporciona transaccionalidad ACID, soporte nativo para la evolución de esquemas (*schema evolution*), unificación de cargas de trabajo *batch* y *streaming*, y consolidación de los entornos de Inteligencia de Negocio e Inteligencia Artificial en un único repositorio, eliminando silos de datos.

## 2. Procesos ETL y ELT

Los procesos de integración son los responsables del movimiento, limpieza y adecuación de los datos desde los sistemas transaccionales u operacionales (orígenes) hacia los sistemas analíticos (destinos).

**ETL (Extract, Transform, Load)**
*   **Extracción (Extract):** Lectura y captura de los datos desde las fuentes de origen (BBDD relacionales, APIs, archivos planos, etc.).
*   **Transformación (Transform):** Procesamiento de los datos en un servidor intermedio dedicado (motor ETL). Incluye tareas de limpieza, normalización, enriquecimiento, agregación, cruce de tablas y enmascaramiento de datos.
*   **Carga (Load):** Escritura de los datos ya procesados y modelados en el repositorio de destino.
*   **Contexto de uso:** Es el enfoque tradicional. Resulta necesario cuando el sistema de destino no posee capacidad de cómputo eficiente para transformaciones complejas o cuando normativas de privacidad exigen que los datos sensibles sean anonimizados antes de alcanzar el repositorio final.

**ELT (Extract, Load, Transform)**
*   **Extracción y Carga (Extract & Load):** Los datos se extraen de las fuentes y se cargan directamente en el sistema de destino (generalmente en una capa *raw* o *landing zone*) sin sufrir alteraciones estructurales.
*   **Transformación (Transform):** Las reglas de negocio y transformaciones se aplican *dentro* del sistema de destino mediante sentencias nativas.
*   **Contexto de uso:** Es el estándar en arquitecturas Big Data y Cloud Data Warehouses modernos. Aprovecha la capacidad de procesamiento masivo paralelo (MPP) de las plataformas actuales, optimizando el tiempo de ingesta y reduciendo la complejidad de la infraestructura intermedia.

## 3. Procesamiento batch y streaming

El procesamiento de los datos se diseña atendiendo a la latencia requerida por el negocio y al volumen de la información.

**Procesamiento Batch (Por lotes)**
*   **Definición:** Los datos se recopilan durante un período de tiempo y se procesan en bloques o lotes de forma programada (ej. procesos nocturnos).
*   **Características:** Presenta una alta latencia desde que el dato se genera hasta que está disponible para análisis (horas o días). Es óptimo para el manejo de grandes volúmenes históricos, cálculos agregados complejos y generación de modelos predictivos base.
*   **Tecnologías habituales:** Apache Hadoop (MapReduce), Apache Spark (Core/SQL), herramientas de orquestación (Apache Airflow).

**Procesamiento Streaming (Flujo continuo)**
*   **Definición:** Los datos se ingieren, procesan y analizan de forma continua e ininterrumpida a medida que se generan, registro a registro o en micro-lotes (*micro-batching*).
*   **Características:** Permite latencias muy bajas (milisegundos a segundos). Es fundamental en arquitecturas orientadas a eventos (*Event-Driven Architectures*).
*   **Casos de uso:** Sistemas de recomendación en tiempo real, detección de fraude, monitorización de logs de ciberseguridad y procesamiento de telemetría en Internet de las Cosas (IoT).
*   **Tecnologías habituales:** Apache Kafka, Apache Flink, Apache Spark Streaming, Apache Storm.

## 4. Plataformas cloud y on-premise

El modelo de infraestructura sobre el que se despliega la arquitectura de datos determina su escalabilidad, mantenimiento y modelo financiero.

**Plataformas On-Premise (Instalaciones Locales)**
*   **Concepto:** La infraestructura física (servidores, red, almacenamiento) y el software residen en las instalaciones de la propia organización.
*   **Modelo Financiero:** Basado en CAPEX (*Capital Expenditure*). Requiere fuertes inversiones de capital inicial en hardware y licencias.
*   **Características:** Control total y directo sobre la soberanía física del dato. La escalabilidad es rígida y está limitada por la capacidad de hardware adquirida (*capacity planning*), requiriendo tiempos prolongados para su ampliación. La organización asume la gestión integral del CPD (climatización, energía, seguridad física y mantenimiento).

**Plataformas Cloud (En la Nube)**
*   **Concepto:** Los recursos de computación y almacenamiento son provistos por un tercero (Hiperescalares como AWS, Google Cloud o Microsoft Azure) y se acceden a través de redes de telecomunicaciones.
*   **Modelo Financiero:** Basado en OPEX (*Operational Expenditure*). Sistema de pago por uso, transformando costes fijos en variables.
*   **Características:** Elasticidad extrema que permite el escalado horizontal y vertical bajo demanda de forma cuasi inmediata. Alta disponibilidad delegada y acceso a servicios administrados (*PaaS*, *SaaS*) que reducen la carga operativa de la administración de sistemas.
*   **Variantes:**
    *   *Nube Pública:* Infraestructura de recursos compartida.
    *   *Nube Privada:* Infraestructura dedicada exclusivamente a una sola organización, aportando mayor aislamiento.
    *   *Nube Híbrida:* Integración de infraestructura on-premise con nube pública, permitiendo la orquestación entre ambas. Facilita la portabilidad de datos y la gestión de picos de carga (*cloud bursting*).

## 5. Gobernanza de plataformas de datos

La gobernanza de datos define las políticas, procesos, estándares, roles y métricas que aseguran el uso efectivo y eficiente de la información para alcanzar los objetivos estratégicos. El marco de referencia ampliamente adoptado es DAMA-DMBOK (*Data Management Body of Knowledge*).

**Elementos críticos de la gobernanza de datos:**

1.  **Gestión de Datos Maestros (MDM) y Datos de Referencia:** Identificación, definición y gestión centralizada de los datos críticos de la organización (ciudadanos, empleados, entidades, activos) para proporcionar una visión única, coherente y precisa (*Golden Record*).
2.  **Calidad del Dato:** Monitorización proactiva y remediación para asegurar que los datos cumplen con dimensiones como exactitud, completitud, coherencia, integridad, actualidad y validez.
3.  **Gestión de Metadatos y Catálogo de Datos:** Creación de repositorios centralizados que indexan los activos de datos. Distingue entre metadatos técnicos (esquemas, tablas, tipos de datos), metadatos de negocio (glosario, definiciones, propietarios) y metadatos operativos (frecuencias de actualización, estadísticas de ejecución).
4.  **Trazabilidad y Linaje de Datos (*Data Lineage*):** Capacidad de rastrear el ciclo de vida del dato desde su origen, pasando por sus transformaciones, hasta su explotación final. Fundamental para la auditoría, análisis de impacto y depuración de incidencias.
5.  **Seguridad, Privacidad y Cumplimiento Normativo:**
    *   Definición de políticas de control de acceso basadas en roles (RBAC) o atributos (ABAC).
    *   Cumplimiento normativo estricto del marco jurídico aplicable: Esquema Nacional de Seguridad (ENS) para la categorización y protección técnica/organizativa, y el Reglamento General de Protección de Datos (RGPD) / LOPDGDD para la protección de la privacidad (minimizando datos y aplicando privacidad desde el diseño).
    *   Implementación de técnicas protectoras: cifrado (en tránsito y reposo), anonimización, seudonimización y enmascaramiento dinámico de datos.
6.  **Gobernanza para la Inteligencia Artificial:** Aseguramiento de la integridad y representatividad de los conjuntos de datos de entrenamiento, validación y prueba para mitigar sesgos algorítmicos. Cumplimiento de las obligaciones regulatorias emergentes (p. ej., Reglamento Europeo de Inteligencia Artificial) en cuanto a evaluación de impacto, trazabilidad y supervisión humana.