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
  - "nist-800-145"
  - "arquitectura-medallion"
created_at: "2026-09-03"
last_reviewed: "2026-09-12"
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

Dentro del Data Warehouse conviene distinguir dos niveles de granularidad complementarios: el **Data Warehouse corporativo (EDW - Enterprise Data Warehouse)**, que integra la visión consolidada de toda la organización, y los **Data Marts**, subconjuntos departamentales o funcionales del EDW (por ejemplo, un Data Mart de Recursos Humanos o de Contratación), orientados a necesidades analíticas específicas de un área de negocio y con un tiempo de implementación menor que el del almacén corporativo completo.

**Data Lake (Lago de Datos)**
*   **Definición:** Repositorio escalable que permite almacenar grandes volúmenes de datos en su formato original o crudo (raw), abarcando datos estructurados, semiestructurados (JSON, XML, logs) y no estructurados (texto libre, imágenes, vídeo).
*   **Paradigma:** Utiliza un enfoque *Schema-on-read* (esquema a la lectura). La estructura y la semántica se aplican en el momento de la consulta, aportando gran agilidad en la fase de ingesta.
*   **Características:** Implementado habitualmente sobre sistemas de archivos distribuidos o almacenamiento de objetos. Es el entorno ideal para analítica avanzada, *Data Science* y entrenamiento de modelos de *Machine Learning*.
*   **Riesgos:** La falta de gobernanza, catalogación y gestión de metadatos puede transformar un Data Lake en un *Data Swamp* (pantano de datos), inutilizando la información almacenada por la imposibilidad de localizarla o comprenderla.

**Data Lakehouse**
*   **Definición:** Arquitectura de datos híbrida que unifica la flexibilidad, la escalabilidad horizontal y el bajo coste de almacenamiento de un *Data Lake* con las capacidades de gestión, rendimiento y transaccionalidad de un *Data Warehouse*.
*   **Características:** Implementa una capa de abstracción de metadatos y gestión de transacciones (basada en formatos de tabla abiertos como Apache Iceberg, Delta Lake o Apache Hudi) directamente sobre el almacenamiento de objetos.
*   **Ventajas:** Proporciona transaccionalidad ACID, soporte nativo para la evolución de esquemas (*schema evolution*), unificación de cargas de trabajo *batch* y *streaming*, y consolidación de los entornos de Inteligencia de Negocio e Inteligencia Artificial en un único repositorio, eliminando silos de datos.

**Arquitectura Medallion (organización interna del Lakehouse)**
Un patrón de diseño ampliamente adoptado para organizar de forma lógica los datos dentro de un Data Lakehouse es la **arquitectura Medallion**, que estructura el flujo de datos en tres capas de calidad creciente:

*   **Capa Bronze (bronce):** zona de aterrizaje inicial (*landing zone*) donde los datos se almacenan exactamente como llegan de las fuentes de origen, sin transformaciones, limpieza ni validaciones, actuando como fuente de verdad inmutable que permite reprocesar la información en caso de error posterior.
*   **Capa Silver (plata):** capa donde ocurre la transformación sustancial: los datos de distintas fuentes se limpian, validan, deduplican y conforman en una vista de negocio unificada, habilitando el análisis de autoservicio y el entrenamiento preliminar de modelos.
*   **Capa Gold (oro):** capa de datos agregados y modelados para casos de uso concretos de negocio (paneles de control, informes, modelos de Machine Learning en producción), optimizada para consultas rápidas y consumo directo por parte de usuarios finales.

Este patrón por capas mejora de forma incremental y progresiva la calidad de los datos a medida que fluyen de Bronze a Silver y de Silver a Gold, y resulta especialmente relevante en preguntas de examen que pidan distinguir el propósito de cada capa dentro de un Lakehouse.

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

**Tabla comparativa ETL vs. ELT**

| Aspecto | ETL | ELT |
| :--- | :--- | :--- |
| Orden de las fases | Extraer → Transformar → Cargar | Extraer → Cargar → Transformar |
| Lugar de la transformación | Servidor/motor intermedio dedicado | Dentro del propio sistema de destino |
| Momento en que el dato transformado está disponible | Después de la transformación completa | El dato crudo está disponible desde la carga; la vista transformada se genera después |
| Infraestructura típica | Data Warehouse tradicional, herramientas ETL dedicadas | Cloud Data Warehouse / Data Lakehouse con motores MPP |
| Flexibilidad ante cambios de esquema | Baja (el esquema de destino se define antes de cargar) | Alta (se conserva el dato crudo, permitiendo reprocesar) |

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

**Arquitecturas de referencia para combinar batch y streaming: Lambda y Kappa**

Cuando una organización necesita ofrecer tanto una vista histórica completa y precisa (propia del batch) como una vista de baja latencia en tiempo real (propia del streaming), suelen adoptarse dos patrones arquitectónicos de referencia:

*   **Arquitectura Lambda:** combina tres capas diferenciadas. La **capa batch** almacena los datos históricos inmutables y calcula periódicamente vistas completas y precisas (habitualmente con motores como Hadoop o Spark). La **capa de velocidad (speed layer)** procesa los datos entrantes en tiempo real para ofrecer resultados de baja latencia, aunque con menor garantía de exactitud que la capa batch. La **capa de servicio (serving layer)** combina y expone los resultados de ambas capas a las aplicaciones consumidoras. Su principal inconveniente es la complejidad de mantener y sincronizar dos rutas de procesamiento (lógica batch y lógica streaming) que deben producir resultados coherentes entre sí.
*   **Arquitectura Kappa:** simplifica la Lambda eliminando la capa batch independiente. Todos los datos, tanto históricos como en tiempo real, se tratan como un único flujo continuo de eventos (*event log*, típicamente implementado sobre Apache Kafka), que se procesa mediante un único motor de streaming (como Kafka Streams o Apache Flink). El procesamiento batch se entiende, en este modelo, como un caso particular de streaming sobre un flujo de eventos acotado en el tiempo, evitando así la duplicidad de lógica de negocio entre dos rutas de procesamiento distintas.

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

**Definición normativa de referencia: NIST SP 800-145**
La definición técnica de referencia más citada internacionalmente sobre computación en la nube es la publicación **NIST SP 800-145, "The NIST Definition of Cloud Computing"**, del National Institute of Standards and Technology (NIST) de Estados Unidos. Define la computación en la nube como un modelo que permite el acceso ubicuo, cómodo y a demanda a través de la red a un conjunto compartido de recursos informáticos configurables (redes, servidores, almacenamiento, aplicaciones y servicios) que pueden aprovisionarse y liberarse rápidamente con un esfuerzo de gestión mínimo o una interacción mínima con el proveedor del servicio.

Este modelo se compone, según la propia publicación NIST, de **cinco características esenciales**, **tres modelos de servicio** y **cuatro modelos de despliegue**:

*Cinco características esenciales:*
1.  **Autoservicio a demanda (on-demand self-service):** el consumidor puede aprovisionar capacidad de cómputo de forma unilateral y automática, sin necesidad de interacción humana con cada proveedor de servicio.
2.  **Acceso a través de la red (broad network access):** las capacidades están disponibles a través de la red y se pueden acceder mediante mecanismos estándar desde diversos dispositivos cliente.
3.  **Agrupación de recursos (resource pooling):** los recursos informáticos del proveedor se agrupan para servir a múltiples consumidores mediante un modelo multiusuario (multi-tenant), con recursos físicos y virtuales asignados y reasignados dinámicamente según la demanda.
4.  **Elasticidad rápida (rapid elasticity):** las capacidades pueden aprovisionarse y liberarse de forma elástica, en algunos casos automáticamente, para escalar rápidamente en función de la demanda.
5.  **Servicio medido (measured service):** los sistemas en la nube controlan y optimizan automáticamente el uso de recursos mediante capacidades de medición a un nivel de abstracción apropiado al tipo de servicio (almacenamiento, procesamiento, ancho de banda, cuentas de usuario activas), permitiendo la monitorización, el control y la generación de informes, y proporcionando transparencia tanto para el proveedor como para el consumidor del servicio utilizado.

*Tres modelos de servicio:*
*   **Software as a Service (SaaS):** la capacidad proporcionada al consumidor es el uso de las aplicaciones del proveedor que se ejecutan sobre una infraestructura en la nube. El consumidor no gestiona ni controla la infraestructura subyacente (red, servidores, sistemas operativos, almacenamiento), ni siquiera las capacidades individuales de la aplicación, salvo posibles ajustes de configuración limitados y específicos del usuario.
*   **Platform as a Service (PaaS):** la capacidad proporcionada al consumidor es desplegar sobre la infraestructura en la nube aplicaciones creadas o adquiridas por el consumidor, desarrolladas utilizando lenguajes de programación, bibliotecas, servicios y herramientas admitidos por el proveedor.
*   **Infrastructure as a Service (IaaS):** la capacidad proporcionada al consumidor es aprovisionar procesamiento, almacenamiento, redes y otros recursos informáticos fundamentales, donde el consumidor puede desplegar y ejecutar software arbitrario, que puede incluir sistemas operativos y aplicaciones.

*Cuatro modelos de despliegue:* nube privada, nube comunitaria (compartida por varias organizaciones con intereses comunes), nube pública y nube híbrida (composición de dos o más de las anteriores, unidas por tecnología estandarizada o propietaria que permite la portabilidad de datos y aplicaciones).

## 5. Gobernanza de plataformas de datos

La gobernanza de datos define las políticas, procesos, estándares, roles y métricas que aseguran el uso efectivo y eficiente de la información para alcanzar los objetivos estratégicos. El marco de referencia ampliamente adoptado es DAMA-DMBOK (*Data Management Body of Knowledge*).

**Elementos críticos de la gobernanza de datos:**

1.  **Gestión de Datos Maestros (MDM) y Datos de Referencia:** Identificación, definición y gestión centralizada de los datos críticos de la organización (ciudadanos, empleados, entidades, activos) para proporcionar una visión única, coherente y precisa (*Golden Record*).
2.  **Calidad del Dato:** Monitorización proactiva y remediación para asegurar que los datos cumplen con dimensiones como exactitud, completitud, coherencia, integridad, actualidad y validez.
3.  **Gestión de Metadatos y Catálogo de Datos:** Creación de repositorios centralizados que indexan los activos de datos. Distingue entre metadatos técnicos (esquemas, tablas, tipos de datos), metadatos de negocio (glosario, definiciones, propietarios) y metadatos operativos (frecuencias de actualización, estadísticas de ejecución).
4.  **Trazabilidad y Linaje de Datos (*Data Lineage*):** Capacidad de rastrear el ciclo de vida del dato desde su origen, pasando por sus transformaciones, hasta su explotación final. Fundamental para la auditoría, análisis de impacto y depuración de incidencias.
5.  **Seguridad, Privacidad y Cumplimiento Normativo:**
    *   Definición de políticas de control de acceso basadas en roles (RBAC) o atributos (ABAC).
    *   Cumplimiento normativo estricto del marco jurídico aplicable: Esquema Nacional de Seguridad (ENS, Real Decreto 311/2022) para la categorización y protección técnica/organizativa, y el Reglamento General de Protección de Datos (RGPD) / LOPDGDD para la protección de la privacidad (minimizando datos y aplicando privacidad desde el diseño).
    *   Implementación de técnicas protectoras: cifrado (en tránsito y reposo), anonimización, seudonimización y enmascaramiento dinámico de datos.
6.  **Gobernanza para la Inteligencia Artificial:** Aseguramiento de la integridad y representatividad de los conjuntos de datos de entrenamiento, validación y prueba para mitigar sesgos algorítmicos. Cumplimiento de las obligaciones regulatorias emergentes (Reglamento (UE) 2024/1689 de Inteligencia Artificial) en cuanto a evaluación de impacto, trazabilidad y supervisión humana.

**Consideraciones específicas de gobernanza en plataformas cloud e híbridas**
Cuando la arquitectura de datos se despliega, total o parcialmente, sobre infraestructura cloud, la gobernanza debe incorporar de forma adicional:

*   **Soberanía y localización del dato:** control sobre la jurisdicción y ubicación física de los centros de datos donde reside la información, especialmente relevante cuando se trata de datos personales o de categorías especiales sujetos al RGPD, o de información clasificada según la Ley 9/1968 de Secretos Oficiales.
*   **Gestión de identidades y accesos entre entornos:** en arquitecturas híbridas (on-premise + nube), la gobernanza debe garantizar una gestión de identidades federada y coherente entre ambos entornos, evitando la proliferación de silos de control de acceso.
*   **Responsabilidad compartida (shared responsibility model):** en los modelos de servicio en la nube (IaaS, PaaS, SaaS) definidos por NIST SP 800-145, la responsabilidad sobre la seguridad y gobernanza del dato se distribuye entre el proveedor del servicio en la nube y la organización consumidora, correspondiendo a esta última, en todo caso, la responsabilidad final sobre el cumplimiento normativo de los datos que trata, con independencia del modelo de servicio elegido.

## Referencias técnicas y normativas

*   NIST Special Publication 800-145, *The NIST Definition of Cloud Computing*, National Institute of Standards and Technology (2011).
*   DAMA International, *DAMA-DMBOK: Data Management Body of Knowledge*, 2ª edición.
*   Real Decreto 311/2022, de 3 de mayo, por el que se regula el Esquema Nacional de Seguridad.
*   Reglamento (UE) 2016/679 (RGPD) y Ley Orgánica 3/2018 (LOPDGDD).
*   Reglamento (UE) 2024/1689, por el que se establecen normas armonizadas en materia de inteligencia artificial.
