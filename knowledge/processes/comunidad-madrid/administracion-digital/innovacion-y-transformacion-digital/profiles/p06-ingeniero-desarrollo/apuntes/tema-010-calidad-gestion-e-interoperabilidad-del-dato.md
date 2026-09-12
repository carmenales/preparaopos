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
  - "eni"
  - "nti"
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

En el ámbito de la Inteligencia Artificial, el Reglamento (UE) 2024/1689 (Reglamento de IA) impone en su artículo 10 requisitos estrictos de calidad para los sistemas de IA de alto riesgo[cite: 9]. Los conjuntos de datos de entrenamiento, validación y prueba deben someterse a prácticas de gobernanza adecuadas, debiendo ser pertinentes, suficientemente representativos y, en la mayor medida posible, carecer de errores y estar completos en vista de su finalidad prevista[cite: 9].

Desde la perspectiva de la protección de datos personales, la Ley Orgánica 3/2018, de 5 de diciembre (LOPDGDD), consagra en su artículo 4 el principio de exactitud, estableciendo que los datos serán exactos y actualizados[cite: 11]. No será imputable al responsable del tratamiento la inexactitud cuando los datos hubiesen sido obtenidos directamente del afectado, de un mediador o intermediario, de otro responsable en virtud del derecho a la portabilidad, o de un registro público[cite: 11].

Adicionalmente, el Esquema Nacional de Seguridad (Real Decreto 311/2022) exige garantizar de forma integral la protección de la información tratada[cite: 8]. En este marco, define la integridad como la propiedad o característica consistente en que el activo de información no ha sido alterado de manera no autorizada, y la trazabilidad como la propiedad consistente en que las actuaciones de una entidad pueden ser trazadas de forma indiscutible hasta dicha entidad[cite: 8].

## 2. Gestión de metadatos y catálogo de datos.

La implantación y el mantenimiento de catálogos de datos y metadatos deben ejecutarse en estricta alineación con los planes estratégicos de digitalización corporativos.

Desde una perspectiva técnico-jurídica, la normativa reguladora del funcionamiento del sector público por medios electrónicos define los **metadatos de gestión de documentos** como aquella información estructurada o semiestructurada que hace posible la creación, gestión y uso de documentos a lo largo del tiempo en el contexto de su creación[cite: 10].

Las funciones esenciales de los metadatos en el entorno público incluyen:
*   Identificar, autenticar y contextualizar los documentos electrónicos.
*   Identificar a las personas, los procesos y los sistemas informáticos que los crean, gestionan, mantienen y utilizan[cite: 10].

El cumplimiento de los requisitos de metadatos se articula mediante el **Esquema Nacional de Interoperabilidad (ENI)**, regulado por el **Real Decreto 4/2010, de 8 de enero**, concretamente a través de la **Norma Técnica de Interoperabilidad de Documento Electrónico**. Esta norma tiene por objeto establecer los componentes del documento electrónico (contenido, firma electrónica y metadatos), así como la estructura y formato para su intercambio, estableciendo los **metadatos mínimos obligatorios** que deben estar presentes en cualquier proceso de intercambio de documentos electrónicos entre órganos de la Administración. 

De forma análoga, la **Norma Técnica de Interoperabilidad de Expediente Electrónico**, establece la estructura y el formato del expediente electrónico (documentos electrónicos, índice electrónico, firma electrónica y metadatos mínimos obligatorios), así como las especificaciones para los servicios de remisión y puesta a disposición.

Adicionalmente, la **Norma Técnica de Interoperabilidad de Política de gestión de documentos electrónicos**, tiene por objeto establecer las directrices para la administración de repositorios electrónicos y su documentación asociada, exigiendo expresamente que las organizaciones garanticen la disponibilidad e integridad de los metadatos de sus documentos electrónicos, manteniendo de manera permanente las relaciones entre cada documento y sus metadatos.

El Real Decreto 203/2021, de 30 de marzo, consolida esta perspectiva exigiendo en su artículo 54 la conservación de los documentos electrónicos con sus metadatos de forma que se permita su acceso y reconstrucción[cite: 10]. Asimismo, el artículo 55 define el archivo electrónico único como el conjunto de sistemas que sustenta la gestión, custodia y recuperación de documentos electrónicos, garantizando su autenticidad, integridad, confidencialidad y cadena de custodia en las condiciones exigidas por el Esquema Nacional de Interoperabilidad y el Esquema Nacional de Seguridad[cite: 10].

## 3. Datos maestros (MDM).

La gestión de **Datos Maestros (MDM - Master Data Management)** se enmarca dentro de las responsabilidades directas de las unidades de gobierno del dato y alineamiento estratégico.

Su implantación tiene como finalidad establecer una única fuente de verdad para las entidades de datos más críticas y compartidas de la organización, facilitando la cohesión organizativa. La participación en el diseño, despliegue y mantenimiento de los repositorios de datos maestros debe realizarse garantizando su alineamiento transversal con el Plan Estratégico de la entidad.

En la Administración Pública española, los principios de MDM se materializan en instrumentos horizontales de interoperabilidad, regulados de forma actualizada por el Real Decreto 203/2021 en su modificación del artículo 9 del Esquema Nacional de Interoperabilidad (ENI)[cite: 10]. Así, el Sistema de Información Administrativa (SIA) actúa como repositorio maestro de procedimientos y servicios, mientras que el Directorio Común de Unidades Orgánicas y Oficinas (DIR3) provee una codificación unívoca y centralizada de la estructura organizativa de las Administraciones Públicas[cite: 10].

## 4. Interoperabilidad de datos y estándares.

**Concepto y alcance normativo**
La **interoperabilidad** se define normativamente como la capacidad de los sistemas de información, y por ende de los procedimientos a los que estos dan soporte, de compartir datos y posibilitar el intercambio de información entre ellos[cite: 10]. Este principio general obliga al sector público a garantizar que las decisiones tecnológicas faciliten dicha interconexión[cite: 10].

El instrumento fundamental para su garantía es el **Esquema Nacional de Interoperabilidad (ENI)**, regulado por el **Real Decreto 4/2010, de 8 de enero**, que comprende el conjunto de criterios y recomendaciones en materia de seguridad, conservación y normalización de la información, de los formatos y de las aplicaciones que deben adoptar las Administraciones Públicas para garantizar el adecuado ejercicio de los derechos y el cumplimiento de los deberes derivados del acceso electrónico a los servicios públicos.

**Normas Técnicas de Interoperabilidad (NTI)**
La disposición adicional primera del Real Decreto 4/2010 (actualizada por la disposición final segunda del Real Decreto 203/2021) establece el desarrollo de una extensa serie de Normas Técnicas de Interoperabilidad[cite: 10]. Entre ellas destacan, en el ámbito estructural y del ciclo de vida de los datos:

*   **Norma Técnica de Catálogo de estándares:** establece un conjunto de estándares estructurados.
*   **Norma Técnica de Documento electrónico:** trata los metadatos mínimos obligatorios, firmas y formatos.
*   **Norma Técnica de Expediente electrónico:** trata su estructura, formato y especificaciones de puesta a disposición.
*   **Norma Técnica de Protocolos de intermediación de datos:** regula las especificaciones que facilitan la integración y reutilización de servicios entre entidades.
*   **Norma Técnica de Reutilización de recursos de información:** determina las normas comunes sobre localización, descripción e identificación unívoca de los recursos expuestos al público.
*   **Norma Técnica de Interoperabilidad de inventario y codificación de objetos administrativos:** trata las reglas relativas a la codificación de objetos administrativos, incluyendo unidades orgánicas, procedimientos y servicios[cite: 10].
*   **Norma Técnica de Interoperabilidad de Transferencia e Ingreso de documentos y expedientes electrónicos:** regula la transferencia entre sistemas de gestión y sistemas de archivo[cite: 10].
*   **Norma Técnica de Interoperabilidad de Valoración y Eliminación de documentos y expedientes electrónicos:** aborda los plazos de conservación, transferencia y eliminación[cite: 10].
*   **Norma Técnica de Interoperabilidad de tratamiento y preservación de bases de datos:** trata las condiciones y requisitos para conservar las bases de datos garantizando su autenticidad, integridad, confidencialidad, disponibilidad y trazabilidad[cite: 10].

Asimismo, el artículo 16 del ENI, modificado por el Real Decreto 203/2021, establece que las condiciones de licenciamiento de los objetos de información y aplicaciones de las Administraciones se realizarán por defecto sin contraprestación, procurando la aplicación de licencias de fuentes abiertas (como la Licencia Pública de la Unión Europea) que aseguren la posibilidad de ejecución, conocimiento del código, modificación y redistribución[cite: 10]. El artículo 17 formaliza el uso del Directorio general de aplicaciones (Centro de Transferencia de Tecnología) como punto neutro para la reutilización[cite: 10].

A nivel de arquitectura y desarrollo, la interoperabilidad técnica exige la definición y aplicación de interfaces estandarizadas, contratos de datos y el desarrollo de **APIs comunes** (apificación), contribuyendo activamente a la adopción de estándares que aseguren la portabilidad de los modelos y los *datasets* entre diferentes infraestructuras, sean *on-premise*, *cloud* o híbridas.

## 5. Integración de datos entre sistemas.

La integración de datos conforma la base de la arquitectura técnica para la explotación analítica y el desarrollo de servicios digitales.

**Arquitectura de plataformas y pipelines**
En el ámbito de la ingeniería de desarrollo, la integración de datos requiere diseñar y mantener plataformas avanzadas, tales como entornos *Data Lake* o *Lakehouse*, y el despliegue de capacidades analíticas complejas que incluyen procesamiento por lotes y en tiempo real (*ETL/ELT*, *streaming*, *Business Intelligence*). Asimismo, la integración es imperativa en el ciclo de vida de las soluciones de Inteligencia Artificial para conformar los *pipelines* de datos, el entrenamiento e inferencia de los modelos y los servicios de integración mediante APIs.

**Plataformas de intermediación de datos y transmisión telemática**
Desde el punto de vista del funcionamiento del sector público, la integración y cesión de información interadministrativa se materializa a través de las **plataformas de intermediación de datos**.
*   El artículo 62 del Real Decreto 203/2021 exige que estas plataformas dejen constancia de la fecha y hora en que se produjo la transmisión, así como del procedimiento administrativo, trámite o actuación al que se refiere la consulta[cite: 10].
*   Resulta obligatorio que cualquier plataforma de intermediación existente en el sector público sea plenamente interoperable con la Plataforma de Intermediación de la Administración General del Estado (PID)[cite: 10]. La PID actuará además como punto de conexión con el sistema técnico regulado por el Reglamento (UE) 2018/1724 para la pasarela digital única a nivel europeo[cite: 10].
*   Las transmisiones de datos realizadas a través de redes corporativas mediante consulta a las plataformas de intermediación u otros sistemas habilitados tienen la consideración de certificados administrativos necesarios para el procedimiento o actuación administrativa (Art. 61 del Real Decreto 203/2021)[cite: 10].
*   Esta cesión de datos dentro de una actuación administrativa puede llevarse a cabo de manera automatizada, entendida como una consulta íntegramente telemática sin intervención directa de un empleado público[cite: 10].

Este principio de simplificación administrativa y transmisión telemática de datos se fundamenta jurídicamente en el **artículo 28 de la Ley 39/2015, de 1 de octubre, del Procedimiento Administrativo Común de las Administraciones Públicas**, que regula el denominado **derecho a no aportar documentos que ya obren en poder de las Administraciones Públicas**. Concretamente, su apartado 2 establece que los interesados tienen derecho a no aportar documentos que ya se encuentren en poder de la Administración actuante o que hayan sido elaborados por cualquier otra Administración, pudiendo la Administración actuante consultar o recabar dichos documentos salvo que el interesado se opusiera a ello. El propio artículo 28.2 precisa que no cabrá tal oposición cuando la aportación del documento se exija en el marco del ejercicio de potestades sancionadoras o de inspección.

## Referencias normativas y técnicas

*   Reglamento (UE) 2024/1689 del Parlamento Europeo y del Consejo, de 13 de junio de 2024, por el que se establecen normas armonizadas en materia de inteligencia artificial (Reglamento de Inteligencia Artificial).
*   Ley Orgánica 3/2018, de 5 de diciembre, de Protección de Datos Personales y garantía de los derechos digitales.
*   Real Decreto 311/2022, de 3 de mayo, por el que se regula el Esquema Nacional de Seguridad.
*   Real Decreto 203/2021, de 30 de marzo, por el que se aprueba el Reglamento de actuación y funcionamiento del sector público por medios electrónicos.
*   Real Decreto 4/2010, de 8 de enero, por el que se regula el Esquema Nacional de Interoperabilidad (ENI) en el ámbito de la Administración Electrónica.
*   Resolución de 19 de julio de 2011, de la Secretaría de Estado para la Función Pública, por la que se aprueba la Norma Técnica de Interoperabilidad de Documento Electrónico.
*   Resolución de 19 de julio de 2011, de la Secretaría de Estado para la Función Pública, por la que se aprueba la Norma Técnica de Interoperabilidad de Expediente Electrónico.
*   Resolución de 28 de junio de 2012, de la Secretaría de Estado de Administraciones Públicas, por la que se aprueba la Norma Técnica de Interoperabilidad de Política de gestión de documentos electrónicos.
*   Resolución de 19 de febrero de 2013, de la Secretaría de Estado de Administraciones Públicas, por la que se aprueba la Norma Técnica de Interoperabilidad de Reutilización de recursos de información.
*   Ley 39/2015, de 1 de octubre, del Procedimiento Administrativo Común de las Administraciones Públicas.