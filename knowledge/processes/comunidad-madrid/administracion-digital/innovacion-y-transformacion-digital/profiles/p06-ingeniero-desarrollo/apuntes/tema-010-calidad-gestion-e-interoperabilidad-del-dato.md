---
id: "cm-ad-innovacion-y-transformacion-digital-tema-010-calidad-gestion-e-interoperabilidad-del-dato"
title: "Calidad, gestión e interoperabilidad del dato"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/innovacion-y-transformacion-digital"
profiles:
  - "p06-ingeniero-desarrollo"
official_profiles:
  - "P06 - Ingeniero de Desarrollo"
official_topic: "Tema 10. Calidad, gestión e interoperabilidad del dato"
source_ids: []
tags:
  - "calidad-del-dato"
  - "gestion-de-metadatos"
  - "catalogo-de-datos"
  - "datos-maestros"
  - "mdm"
  - "interoperabilidad"
  - "integracion-de-datos"
created_at: "2026-09-03"
last_reviewed: "2026-09-09"
ai_generated: true
ai_sources:
  - "perplexity"
  - "chatgpt"
  - "gemini"
needs_human_review: true
---

# Tema 10. Calidad, gestión e interoperabilidad del dato

## 1. Dimensiones de calidad del dato.

En el marco de la Administración Pública, la calidad del dato constituye un pilar estructural indispensable dentro de la estrategia global de gobierno del dato. La consolidación de esta estrategia abarca la definición y ejecución de directrices orientadas a garantizar la calidad, la seguridad y la correcta gestión del ciclo de vida de la información. 

A nivel técnico y analítico, asegurar las dimensiones de calidad del dato es un requisito funcional crítico, especialmente en el contexto del entrenamiento, validación y despliegue de soluciones basadas en Inteligencia Artificial y *Machine Learning*. La precisión y fiabilidad técnica de los datos resultan fundamentales para el seguimiento de indicadores (KPIs), la trazabilidad, la prevención de sesgos algorítmicos y el soporte a la toma de decisiones basada en evidencias en los proyectos TIC del sector público.

## 2. Gestión de metadatos y catálogo de datos.

La implantación y el mantenimiento de catálogos de datos y metadatos deben ejecutarse en estricta alineación con los planes estratégicos de digitalización corporativos.

Desde una perspectiva técnico-jurídica, la normativa reguladora del funcionamiento del sector público por medios electrónicos define los **metadatos de gestión de documentos** como aquella información estructurada o semiestructurada que hace posible la creación, gestión y uso de documentos a lo largo del tiempo en el contexto de su creación. 

Las funciones esenciales de los metadatos en el entorno público incluyen:
*   Identificar, autenticar y contextualizar los documentos electrónicos.
*   Identificar a las personas, los procesos y los sistemas informáticos que los crean, gestionan, mantienen y utilizan.

El cumplimiento de los requisitos de metadatos se articula mediante el **Esquema Nacional de Interoperabilidad (ENI)**, concretamente a través de la Norma Técnica de Documento Electrónico, que establece los metadatos mínimos obligatorios, la asociación de los datos y metadatos de firma o de sellado de tiempo, y los formatos documentales admitidos. Adicionalmente, la Norma Técnica de Interoperabilidad de Política de gestión de documentos electrónicos proporciona las directrices para la administración de repositorios y su documentación asociada.

## 3. Datos maestros (MDM).

La gestión de **Datos Maestros (MDM - Master Data Management)** se enmarca dentro de las responsabilidades directas de las unidades de gobierno del dato y alineamiento estratégico. 

Su implantación tiene como finalidad establecer una única fuente de verdad para las entidades de datos más críticas y compartidas de la organización, facilitando la cohesión organizativa. La participación en el diseño, despliegue y mantenimiento de los repositorios de datos maestros debe realizarse garantizando su alineamiento transversal con el Plan Estratégico de la entidad. 

## 4. Interoperabilidad de datos y estándares.

**Concepto y alcance normativo**
La **interoperabilidad** se define normativamente como la capacidad de los sistemas de información, y por ende de los procedimientos a los que estos dan soporte, de compartir datos y posibilitar el intercambio de información entre ellos. Este principio general obliga al sector público a garantizar que las decisiones tecnológicas faciliten dicha interconexión.

El instrumento fundamental para su garantía es el **Esquema Nacional de Interoperabilidad (ENI)**, que comprende el conjunto de criterios y recomendaciones en materia de seguridad, conservación y normalización de la información, de los formatos y de las aplicaciones que deben adoptar las Administraciones Públicas.

**Normas Técnicas de Interoperabilidad (NTI)**
Para hacer efectiva la interoperabilidad, el marco jurídico establece el desarrollo de Normas Técnicas de obligado cumplimiento, entre las que destacan en el ámbito de los datos:
*   *Norma Técnica de Catálogo de estándares:* Establece el conjunto de estándares admitidos para garantizar la neutralidad y la interconexión.
*   *Norma Técnica de Relación de modelos de datos:* Define los modelos que tienen carácter de comunes en la Administración y aquellos sujetos a intercambio.
*   *Norma Técnica de Protocolos de intermediación de datos:* Regula las especificaciones que facilitan la integración y reutilización de servicios entre entidades.
*   *Norma Técnica de Reutilización de recursos de información:* Determina las normas comunes sobre localización, descripción e identificación unívoca de los recursos expuestos al público.

A nivel de arquitectura y desarrollo, la interoperabilidad técnica exige la definición y aplicación de interfaces estandarizadas, contratos de datos y el desarrollo de **APIs comunes** (apificación), contribuyendo activamente a la adopción de estándares que aseguren la portabilidad de los modelos y los *datasets* entre diferentes infraestructuras, sean *on-premise*, *cloud* o híbridas.

## 5. Integración de datos entre sistemas.

La integración de datos conforma la base de la arquitectura técnica para la explotación analítica y el desarrollo de servicios digitales. 

**Arquitectura de plataformas y pipelines**
En el ámbito de la ingeniería de desarrollo, la integración de datos requiere diseñar y mantener plataformas avanzadas, tales como entornos *Data Lake* o *Lakehouse*, y el despliegue de capacidades analíticas complejas que incluyen procesamiento por lotes y en tiempo real (*ETL/ELT*, *streaming*, *Business Intelligence*). Asimismo, la integración es imperativa en el ciclo de vida de las soluciones de Inteligencia Artificial para conformar los *pipelines* de datos, el entrenamiento e inferencia de los modelos y los servicios de integración mediante APIs.

**Plataformas de intermediación de datos**
Desde el punto de vista del funcionamiento del sector público, la integración y cesión de información interadministrativa se materializa a través de las **plataformas de intermediación de datos**. 
*   Estas plataformas deben garantizar la trazabilidad, dejando constancia de la fecha y hora de la transmisión, así como del procedimiento o trámite al que se refiere la consulta.
*   Resulta obligatorio que cualquier plataforma de intermediación existente en el sector público sea plenamente interoperable con la Plataforma de Intermediación de la Administración General del Estado, posibilitando el intercambio de documentos y datos conforme al principio de simplificación administrativa (Derecho a no aportar documentos que ya obren en poder de las Administraciones).
