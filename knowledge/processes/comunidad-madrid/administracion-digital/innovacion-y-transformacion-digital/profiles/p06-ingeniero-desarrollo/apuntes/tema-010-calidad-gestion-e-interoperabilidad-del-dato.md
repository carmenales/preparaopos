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
  - "iso-25012"
  - "dcat-ap"
  - "gobernanza-europea-del-dato"
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

# Tema 10. Calidad, gestión e interoperabilidad del dato

## 1. Dimensiones de calidad del dato.

En el marco de la Administración Pública, la calidad del dato constituye un pilar estructural indispensable dentro de la estrategia global de gobierno del dato. La consolidación de esta estrategia abarca la definición y ejecución de directrices orientadas a garantizar la calidad, la seguridad y la correcta gestión del ciclo de vida de la información.

A nivel técnico y analítico, asegurar las dimensiones de calidad del dato es un requisito funcional crítico, especialmente en el contexto del entrenamiento, validación y despliegue de soluciones basadas en Inteligencia Artificial y *Machine Learning*. La precisión y fiabilidad técnica de los datos resultan fundamentales para el seguimiento de indicadores (KPIs), la trazabilidad, la prevención de sesgos algorítmicos y el soporte a la toma de decisiones basada en evidencias en los proyectos TIC del sector público.

### 1.1. El modelo normalizado de calidad del dato: ISO/IEC 25012 y UNE 0081:2023

La norma **ISO/IEC 25012**, integrada en la familia **SQuaRE** (*System and Data Quality Requirements and Evaluation*, ISO/IEC 25000), define el modelo de referencia de calidad del producto de datos. Este modelo se estructura en quince características, agrupadas en dos categorías:

*   **Calidad de datos inherente** (propia del dato en sí mismo, con independencia del sistema que lo trate): exactitud, completitud, consistencia, credibilidad y actualidad.
*   **Calidad de datos inherente y dependiente del sistema** (condicionada, además, por el sistema informático que la sustenta): accesibilidad, conformidad, confidencialidad, eficiencia, precisión, trazabilidad, comprensibilidad, disponibilidad, portabilidad y recuperabilidad.

Las cinco características inherentes, núcleo habitual de cualquier evaluación de calidad de datos, se definen como sigue:

*   **Exactitud:** grado en el que los datos representan correctamente el valor verdadero del atributo deseado en un contexto de uso específico. Se distingue entre exactitud sintáctica (cercanía a un conjunto de valores sintácticamente correctos en un dominio) y exactitud semántica (cercanía a los valores semánticamente correctos).
*   **Completitud:** grado en el que los datos asociados a una entidad presentan valores para todos los atributos necesarios para su representación.
*   **Consistencia:** grado en el que los datos están libres de contradicción y son coherentes con el resto de datos de su contexto de uso.
*   **Credibilidad:** grado en el que los datos tienen atributos que se consideran ciertos y creíbles por los usuarios, incorporando el concepto de autenticidad.
*   **Actualidad:** grado en el que los datos tienen atributos con valores vigentes para su contexto de uso.

La métrica asociada a cada una de estas características se desarrolla en la norma complementaria **ISO/IEC 25024**. En España, la especificación **UNE 0081:2023** («Calidad de datos. Modelo de referencia»), elaborada a partir de las normas ISO/IEC 25012 e ISO/IEC 25024, ha sido adoptada como modelo de evaluación de la calidad de los conjuntos de datos abiertos publicados por las Administraciones Públicas, tomando como conjunto mínimo de referencia las cinco características de calidad inherente (exactitud, completitud, consistencia, credibilidad y actualidad).

### 1.2. Calidad del dato en la Inteligencia Artificial: Reglamento (UE) 2024/1689

En el ámbito de la Inteligencia Artificial, el Reglamento (UE) 2024/1689 (Reglamento de IA) impone en su artículo 10 requisitos estrictos de gobernanza y calidad del dato para los sistemas de IA de alto riesgo que empleen técnicas de entrenamiento con datos.

Conforme al artículo 10.2, los conjuntos de datos de entrenamiento, validación y prueba deben someterse a prácticas de gobernanza y gestión de datos adecuadas a la finalidad prevista del sistema, centradas particularmente en:

*   Las decisiones pertinentes relativas al diseño.
*   Los procesos de recogida de datos y el origen de estos y, en el caso de datos personales, la finalidad original de su recogida.
*   Las operaciones pertinentes de preparación de datos, tales como anotación, etiquetado, depuración, actualización, enriquecimiento y agregación.
*   La formulación de supuestos, en particular con respecto a la información que se pretende que los datos midan y representen.
*   Una evaluación de la disponibilidad, cantidad e idoneidad de los conjuntos de datos necesarios.
*   El examen orientado a detectar posibles sesgos que puedan afectar a la salud y la seguridad de las personas físicas, tener repercusiones negativas en los derechos fundamentales o dar lugar a discriminación prohibida por el Derecho de la Unión.
*   La identificación de posibles lagunas o deficiencias de datos y la forma de subsanarlas.

El artículo 10.3 exige, en consonancia con lo anterior, que los conjuntos de datos de entrenamiento, validación y prueba sean pertinentes, suficientemente representativos y, en la mayor medida posible, carezcan de errores y estén completos en vista de su finalidad prevista, debiendo tener además las propiedades estadísticas adecuadas respecto a las personas o colectivos sobre los que esté previsto utilizar el sistema.

Como excepción particular, el artículo 10.5 permite, cuando resulte estrictamente necesario para garantizar la detección y corrección de sesgos, el tratamiento de categorías especiales de datos personales, sujeto a garantías apropiadas para los derechos y libertades de las personas físicas (imposibilidad de transmitir dichos datos a terceros, medidas de seguridad adecuadas, supresión de los datos personales una vez corregido el sesgo o finalizado el período de conservación, y limitación del acceso a personal autorizado con obligaciones de confidencialidad).

### 1.3. Exactitud del dato en protección de datos personales: LOPDGDD

Desde la perspectiva de la protección de datos personales, la Ley Orgánica 3/2018, de 5 de diciembre (LOPDGDD), consagra en su artículo 4 el principio de exactitud, estableciendo, en línea con el artículo 5.1.d) del Reglamento (UE) 2016/679, que los datos serán exactos y, si fuere necesario, actualizados. No será imputable al responsable del tratamiento la inexactitud cuando los datos hubiesen sido obtenidos directamente del afectado, de un mediador o intermediario, de otro responsable en virtud del derecho a la portabilidad, o de un registro público, siempre que el responsable haya adoptado todas las medidas razonables para que se supriman o rectifiquen sin dilación. El mediador o intermediario asumirá, en su caso, las responsabilidades derivadas de la comunicación de datos que no se correspondan con los facilitados por el afectado.

### 1.4. Dimensiones de seguridad de la información: Esquema Nacional de Seguridad (ENS)

El Esquema Nacional de Seguridad (Real Decreto 311/2022) exige garantizar de forma integral la protección de la información tratada, estando constituido por los principios básicos y requisitos mínimos necesarios para asegurar el acceso, la confidencialidad, la integridad, la trazabilidad, la autenticidad, la disponibilidad y la conservación de los datos, la información y los servicios utilizados por medios electrónicos.

El anexo I del Real Decreto 311/2022 identifica, a efectos de la categorización de los sistemas de información, cinco dimensiones de la seguridad, cuyas iniciales conforman el acrónimo **CITAD**: Confidencialidad [C], Integridad [I], Trazabilidad [T], Autenticidad [A] y Disponibilidad [D]. El anexo IV (glosario) las define como sigue:

*   **Confidencialidad:** propiedad o característica consistente en que la información ni se pone a disposición, ni se revela a individuos, entidades o procesos no autorizados.
*   **Integridad:** propiedad o característica consistente en que el activo de información no ha sido alterado de manera no autorizada.
*   **Trazabilidad:** propiedad o característica consistente en que las actuaciones de una entidad pueden ser trazadas de forma indiscutible hasta dicha entidad.
*   **Autenticidad:** propiedad o característica consistente en que una entidad es quien dice ser o bien que garantiza la fuente de la que proceden los datos.
*   **Disponibilidad:** propiedad o característica de los activos consistente en que las entidades o procesos autorizados tienen acceso a los mismos cuando lo requieren.

La valoración del impacto que tendría sobre cada una de estas cinco dimensiones un incidente de seguridad determina, conforme al procedimiento del anexo I, la categoría de seguridad del sistema de información (Básica, Media o Alta), categoría que a su vez condiciona la selección proporcional de las medidas de seguridad recogidas en el anexo II.

## 2. Gestión de metadatos y catálogo de datos.

La implantación y el mantenimiento de catálogos de datos y metadatos deben ejecutarse en estricta alineación con los planes estratégicos de digitalización corporativos.

Desde una perspectiva técnico-jurídica, la normativa reguladora del funcionamiento del sector público por medios electrónicos define los **metadatos de gestión de documentos** como aquella información estructurada o semiestructurada que hace posible la creación, gestión y uso de documentos a lo largo del tiempo en el contexto de su creación.

Las funciones esenciales de los metadatos en el entorno público incluyen:
*   Identificar, autenticar y contextualizar los documentos electrónicos.
*   Identificar a las personas, los procesos y los sistemas informáticos que los crean, gestionan, mantienen y utilizan.

El cumplimiento de los requisitos de metadatos se articula mediante el **Esquema Nacional de Interoperabilidad (ENI)**, regulado por el **Real Decreto 4/2010, de 8 de enero**, concretamente a través de la **Norma Técnica de Interoperabilidad de Documento Electrónico**. Esta norma tiene por objeto establecer los componentes del documento electrónico (contenido, firma electrónica y metadatos), así como la estructura y formato para su intercambio, estableciendo los **metadatos mínimos obligatorios** que deben estar presentes en cualquier proceso de intercambio de documentos electrónicos entre órganos de la Administración.

De forma análoga, la **Norma Técnica de Interoperabilidad de Expediente Electrónico**, establece la estructura y el formato del expediente electrónico (documentos electrónicos, índice electrónico, firma electrónica y metadatos mínimos obligatorios), así como las especificaciones para los servicios de remisión y puesta a disposición.

Adicionalmente, la **Norma Técnica de Interoperabilidad de Política de gestión de documentos electrónicos**, tiene por objeto establecer las directrices para la administración de repositorios electrónicos y su documentación asociada, exigiendo expresamente que las organizaciones garanticen la disponibilidad e integridad de los metadatos de sus documentos electrónicos, manteniendo de manera permanente las relaciones entre cada documento y sus metadatos.

El Real Decreto 203/2021, de 30 de marzo, consolida esta perspectiva exigiendo en su artículo 54 la conservación de los documentos electrónicos con sus metadatos de forma que se permita su acceso y reconstrucción. Asimismo, el artículo 55 define el archivo electrónico único como el conjunto de sistemas que sustenta la gestión, custodia y recuperación de documentos electrónicos, garantizando su autenticidad, integridad, confidencialidad y cadena de custodia en las condiciones exigidas por el Esquema Nacional de Interoperabilidad y el Esquema Nacional de Seguridad.

### 2.1. El modelo semántico de catálogos de datos: DCAT y DCAT-AP-ES

La interoperabilidad semántica de los catálogos de datos del sector público se articula mediante el vocabulario **DCAT** (*Data Catalog Vocabulary*), publicado por el W3C como recomendación en 2014, vocabulario RDF orientado a describir catálogos y conjuntos de datos de forma que resulten legibles e intercambiables entre sistemas.

A partir de dicho vocabulario, la Comisión Europea desarrolló el **perfil de aplicación DCAT-AP** (*DCAT Application Profile*), especificación destinada a describir mediante metadatos los catálogos y conjuntos de datos de los portales de datos del sector público europeo, con el fin de que esas descripciones puedan compartirse entre distintos catálogos nacionales o agregarse en un único punto de acceso común, asegurando la interoperabilidad semántica entre los portales de datos abiertos europeos.

En España, la **Norma Técnica de Interoperabilidad de Reutilización de recursos de información** (Resolución de 19 de febrero de 2013, de la Secretaría de Estado de Administraciones Públicas) exige que los catálogos, los metadatos y los servicios asociados a los documentos y recursos de información reutilizables utilicen estándares abiertos, debiendo ofrecerse el propio catálogo como un conjunto de datos reutilizable mediante información procesable automáticamente que emplee el vocabulario internacionalmente reconocido DCAT, garantizando así la reutilización de los propios metadatos del catálogo y la interoperabilidad con otros catálogos.

Este marco se ha actualizado mediante **DCAT-AP-ES**, adaptación nacional del perfil europeo DCAT-AP que constituye el modelo de referencia para la descripción de catálogos, conjuntos de datos y servicios de datos en el ámbito de la denominada NTI-RISP (Norma Técnica de Interoperabilidad de Recursos de Información del Sector Público). DCAT-AP-ES incorpora, entre otras novedades, metadatos para la descripción de los conjuntos de datos de alto valor (*High Value Datasets*), la posibilidad de enlazar catálogos entre sí, el registro de la autoría del catálogo, la documentación de la procedencia y las relaciones entre recursos, y la gestión de versiones, con el objetivo de mejorar la localización, la búsqueda y la reutilización de los recursos publicados y de reducir las incidencias en los procesos de federación entre catálogos.

El **Catálogo de datos de datos.gob.es** actúa como catálogo agregador o federador de ámbito estatal, recolectando de forma automatizada, mediante ficheros en formato semántico DCAT/RDF, los metadatos de los conjuntos de datos publicados por los catálogos de las distintas Administraciones Públicas.

## 3. Datos maestros (MDM).

La gestión de **Datos Maestros (MDM - Master Data Management)** se enmarca dentro de las responsabilidades directas de las unidades de gobierno del dato y alineamiento estratégico.

Su implantación tiene como finalidad establecer una única fuente de verdad para las entidades de datos más críticas y compartidas de la organización, facilitando la cohesión organizativa. La participación en el diseño, despliegue y mantenimiento de los repositorios de datos maestros debe realizarse garantizando su alineamiento transversal con el Plan Estratégico de la entidad.

En la Administración Pública española, los principios de MDM se materializan en instrumentos horizontales de interoperabilidad, regulados de forma actualizada por el Real Decreto 203/2021 en su modificación del artículo 9 del Esquema Nacional de Interoperabilidad (ENI). Así, el Sistema de Información Administrativa (SIA) actúa como repositorio maestro de procedimientos y servicios, mientras que el Directorio Común de Unidades Orgánicas y Oficinas (DIR3) provee una codificación unívoca y centralizada de la estructura organizativa de las Administraciones Públicas.

En términos precisos, el artículo 9.1 del Real Decreto 4/2010, en su redacción dada por el Real Decreto 203/2021, define el **Sistema de Información Administrativa (SIA)** como el inventario de procedimientos administrativos, servicios prestados y otras actuaciones administrativas que generen documentación pública, conteniendo información de los mismos clasificada por funciones, con indicación de su nivel de informatización, así como información acerca de sus interfaces al objeto de favorecer la interacción o, en su caso, la integración de los procesos. El SIA es gestionado por el Ministerio con competencias en materia de Función Pública, en colaboración con el Ministerio competente en Transformación Digital.

Por su parte, el **Directorio Común de Unidades Orgánicas y Oficinas (DIR3)** constituye el inventario unificado y común a toda la Administración de las unidades orgánicas y sus oficinas asociadas, gestionado por el Ministerio con competencias en Transformación Digital en colaboración con el de Función Pública. DIR3 facilita el mantenimiento distribuido y corresponsable de dicha información y proporciona la codificación unívoca de los órganos administrativos y oficinas de registro y atención al ciudadano, codificación que se difunde entre las Administraciones Públicas.

## 4. Interoperabilidad de datos y estándares.

**Concepto y alcance normativo**
La **interoperabilidad** se define normativamente como la capacidad de los sistemas de información, y por ende de los procedimientos a los que estos dan soporte, de compartir datos y posibilitar el intercambio de información entre ellos. Este principio general obliga al sector público a garantizar que las decisiones tecnológicas faciliten dicha interconexión.

El instrumento fundamental para su garantía es el **Esquema Nacional de Interoperabilidad (ENI)**, regulado por el **Real Decreto 4/2010, de 8 de enero**, que comprende el conjunto de criterios y recomendaciones en materia de seguridad, conservación y normalización de la información, de los formatos y de las aplicaciones que deben adoptar las Administraciones Públicas para garantizar el adecuado ejercicio de los derechos y el cumplimiento de los deberes derivados del acceso electrónico a los servicios públicos.

**Normas Técnicas de Interoperabilidad (NTI)**
La disposición adicional primera del Real Decreto 4/2010 establece el desarrollo de una extensa serie de Normas Técnicas de Interoperabilidad, de obligado cumplimiento para las Administraciones Públicas. En su redacción original, dicha disposición adicional primera contemplaba las siguientes:

*   **Catálogo de estándares:** establece un conjunto mínimo de estándares que satisfacen lo previsto en el artículo 11 del Real Decreto 4/2010 y que dan soporte al resto de Normas Técnicas de Interoperabilidad, estableciendo las condiciones necesarias para su revisión y actualización.
*   **Documento electrónico:** trata los metadatos mínimos obligatorios, firmas y formatos.
*   **Digitalización de documentos:** regula los requisitos técnicos para la digitalización de documentos en soporte papel.
*   **Expediente electrónico:** trata su estructura, formato y especificaciones de puesta a disposición.
*   **Política de firma electrónica y de certificados de la Administración:** establece el marco general para la interoperabilidad y reconocimiento mutuo de las firmas electrónicas.
*   **Protocolos de intermediación de datos:** regula las especificaciones que facilitan la integración y reutilización de servicios entre entidades.
*   **Relación de modelos de datos** que tengan el carácter de comunes en la Administración y de aquellos que se refieran a materias sujetas a intercambio de información con los ciudadanos y otras administraciones.
*   **Política de gestión de documentos electrónicos:** establece las directrices para la administración de los repositorios electrónicos y su documentación asociada a lo largo de todo el ciclo de vida de los documentos.
*   **Requisitos de conexión a la red de comunicaciones de las Administraciones Públicas españolas** (red SARA).
*   **Procedimientos de copiado auténtico y conversión entre documentos electrónicos**, así como desde papel u otro medio físico a formato electrónico.
*   **Modelo de Datos para el Intercambio de asientos** entre las Entidades Registrales.
*   **Reutilización de recursos de información:** determina las normas comunes sobre localización, descripción e identificación unívoca de los recursos expuestos al público, así como los estándares de metadatos aplicables (véase el apartado 2.1 anterior).

Tras la modificación de la disposición adicional primera del Real Decreto 4/2010 por la disposición final segunda del Real Decreto 203/2021, dicho catálogo de Normas Técnicas de Interoperabilidad se amplió incorporando, entre otras, las relativas al ámbito estructural y del ciclo de vida de los datos:

*   **Norma Técnica de Interoperabilidad de inventario y codificación de objetos administrativos:** trata las reglas relativas a la codificación de objetos administrativos, incluyendo unidades orgánicas, procedimientos y servicios.
*   **Norma Técnica de Interoperabilidad de Transferencia e Ingreso de documentos y expedientes electrónicos:** regula la transferencia entre sistemas de gestión y sistemas de archivo.
*   **Norma Técnica de Interoperabilidad de Valoración y Eliminación de documentos y expedientes electrónicos:** aborda los plazos de conservación, transferencia y eliminación.
*   **Norma Técnica de Interoperabilidad de tratamiento y preservación de bases de datos:** trata las condiciones y requisitos para conservar las bases de datos garantizando su autenticidad, integridad, confidencialidad, disponibilidad y trazabilidad.

Asimismo, el artículo 16 del ENI, modificado por el Real Decreto 203/2021, establece que las condiciones de licenciamiento de los objetos de información y aplicaciones de las Administraciones se realizarán por defecto sin contraprestación, procurando la aplicación de licencias de fuentes abiertas (como la Licencia Pública de la Unión Europea) que aseguren la posibilidad de ejecución, conocimiento del código, modificación y redistribución. El artículo 17 formaliza el uso del Directorio general de aplicaciones (Centro de Transferencia de Tecnología) como punto neutro para la reutilización.

A nivel de arquitectura y desarrollo, la interoperabilidad técnica exige la definición y aplicación de interfaces estandarizadas, contratos de datos y el desarrollo de **APIs comunes** (apificación), contribuyendo activamente a la adopción de estándares que aseguren la portabilidad de los modelos y los *datasets* entre diferentes infraestructuras, sean *on-premise*, *cloud* o híbridas.

### 4.1. Marco europeo de interoperabilidad y gobernanza del dato

El desarrollo normativo de la interoperabilidad y la gestión del dato en el sector público se ha visto reforzado en los últimos años por un conjunto de reglamentos europeos de aplicación directa, complementarios al ENI y de especial relevancia en el ámbito de la ingeniería de desarrollo y la transformación digital de las Administraciones Públicas.

**Reglamento sobre la Europa Interoperable — Reglamento (UE) 2024/903**

El Reglamento (UE) 2024/903 del Parlamento Europeo y del Consejo, de 13 de marzo de 2024, establece medidas para garantizar un alto nivel de interoperabilidad del sector público en toda la Unión. Su objeto es fomentar la interoperabilidad transfronteriza de los servicios públicos digitales transeuropeos, contribuyendo a la interoperabilidad de las redes y sistemas de información subyacentes mediante el establecimiento de normas comunes y un marco de gobernanza.

El Reglamento define la **interoperabilidad transfronteriza** como la capacidad de las entidades de la Unión y de los organismos del sector público de los Estados miembros para interactuar entre sí a través de las fronteras mediante el intercambio de datos, información y conocimientos a través de procesos digitales acordes con los requisitos jurídicos, organizativos, semánticos y técnicos relacionados con dicha interacción.

Entre sus principales previsiones destacan:

*   La obligación de que las entidades de la Unión y los organismos del sector público lleven a cabo **evaluaciones de interoperabilidad** antes de implantar sistemas digitales nuevos o modificados que presten o gestionen servicios públicos digitales transeuropeos, valorando los efectos de dichos sistemas en la interoperabilidad transfronteriza, identificando a las partes interesadas afectadas y proponiendo soluciones a los obstáculos detectados.
*   La creación del **portal de la Europa Interoperable**, como punto único de acceso a la información sobre interoperabilidad transfronteriza, a las soluciones de interoperabilidad y al Marco Europeo de Interoperabilidad, garantizando que dichas soluciones sean accesibles, legibles por máquina y reutilizables.
*   La obligación de puesta en común y reutilización de las soluciones de interoperabilidad (buenas prácticas, especificaciones y código del programa, junto con su documentación) entre entidades de la Unión y organismos del sector público, debiendo priorizarse las soluciones sin condiciones de licencia restrictivas cuando existan alternativas equivalentes.
*   La constitución de un **Comité**, integrado por un representante de cada Estado miembro y uno de la Comisión, encargado de desarrollar y actualizar el **Marco Europeo de Interoperabilidad** y de adoptar el **Programa de la Europa Interoperable** para coordinar las prioridades de desarrollo de la interoperabilidad transfronteriza.
*   El objetivo declarado de lograr unos servicios públicos plenamente interoperables en la Unión de aquí a 2030, fomentando el desarrollo de soluciones de interoperabilidad de código abierto y la cooperación con los agentes del ecosistema GovTech.

**Reglamento de Gobernanza de Datos — Reglamento (UE) 2022/868**

El Reglamento (UE) 2022/868 del Parlamento Europeo y del Consejo, de 30 de mayo de 2022, relativo a la gobernanza europea de datos (Reglamento de Gobernanza de Datos), tiene por objeto aumentar la disponibilidad de los datos para su reutilización y facilitar el intercambio de datos entre ámbitos como la salud, el medio ambiente, la energía, la agricultura, la movilidad, las finanzas, la fabricación, la administración pública y las competencias.

El Reglamento establece, entre otros elementos:

*   Un régimen horizontal de condiciones para la **reutilización de determinadas categorías de datos protegidos** en poder de organismos del sector público (datos sujetos a confidencialidad comercial o estadística, datos personales o datos protegidos por derechos de propiedad intelectual de terceros), categorías que quedan fuera del ámbito de la Directiva (UE) 2019/1024 de datos abiertos. Los organismos del sector público competentes deberán publicar las condiciones de reutilización y el procedimiento para solicitarla, condiciones que no podrán ser discriminatorias y deberán ser transparentes, proporcionadas y estar objetivamente justificadas.
*   Un marco de notificación y supervisión para la prestación de **servicios de intermediación de datos**.
*   Un régimen para la **cesión altruista de datos**, con inscripción voluntaria de las entidades que recojan y traten datos cedidos con dicha finalidad.
*   La obligación de garantizar un **punto de información único** a través del cual sea posible localizar toda la información pertinente sobre las condiciones de reutilización y los costes asociados.
*   La creación del **Comité Europeo de Innovación de Datos**, encargado de asesorar y ayudar a la Comisión a mejorar la interoperabilidad de los servicios de intermediación de datos y a facilitar el desarrollo de los espacios europeos de datos.

Este Reglamento modificó, a su vez, el Reglamento (UE) 2018/1724, por el que se establece una **pasarela digital única**, instrumento con el que la Plataforma de Intermediación de Datos (PID) de la Administración General del Estado actúa como punto de conexión a nivel europeo, tal y como se detalla en el epígrafe siguiente.

## 5. Integración de datos entre sistemas.

La integración de datos conforma la base de la arquitectura técnica para la explotación analítica y el desarrollo de servicios digitales.

**Arquitectura de plataformas y pipelines**
En el ámbito de la ingeniería de desarrollo, la integración de datos requiere diseñar y mantener plataformas avanzadas, tales como entornos *Data Lake* o *Lakehouse*, y el despliegue de capacidades analíticas complejas que incluyen procesamiento por lotes y en tiempo real (*ETL/ELT*, *streaming*, *Business Intelligence*). Asimismo, la integración es imperativa en el ciclo de vida de las soluciones de Inteligencia Artificial para conformar los *pipelines* de datos, el entrenamiento e inferencia de los modelos y los servicios de integración mediante APIs.

**Plataformas de intermediación de datos y transmisión telemática**
Desde el punto de vista del funcionamiento del sector público, la integración y cesión de información interadministrativa se materializa a través de las **plataformas de intermediación de datos**.
*   El artículo 62 del Real Decreto 203/2021 exige que estas plataformas dejen constancia de la fecha y hora en que se produjo la transmisión, así como del procedimiento administrativo, trámite o actuación al que se refiere la consulta.
*   Resulta obligatorio que cualquier plataforma de intermediación existente en el sector público sea plenamente interoperable con la Plataforma de Intermediación de la Administración General del Estado (PID). La PID actuará además como punto de conexión con el sistema técnico regulado por el Reglamento (UE) 2018/1724 para la pasarela digital única a nivel europeo.
*   Las transmisiones de datos realizadas a través de redes corporativas mediante consulta a las plataformas de intermediación u otros sistemas habilitados tienen la consideración de certificados administrativos necesarios para el procedimiento o actuación administrativa (Art. 61 del Real Decreto 203/2021).
*   Esta cesión de datos dentro de una actuación administrativa puede llevarse a cabo de manera automatizada, entendida como una consulta íntegramente telemática sin intervención directa de un empleado público.

Este principio de simplificación administrativa y transmisión telemática de datos se fundamenta jurídicamente en el **artículo 28 de la Ley 39/2015, de 1 de octubre, del Procedimiento Administrativo Común de las Administraciones Públicas**, que regula el denominado **derecho a no aportar documentos que ya obren en poder de las Administraciones Públicas**. Dicho precepto se estructura en tres apartados:

*   El **apartado 1** dispone que los interesados deberán aportar al procedimiento administrativo los datos y documentos exigidos por las Administraciones Públicas de acuerdo con lo dispuesto en la normativa aplicable, pudiendo aportar además cualquier otro documento que estimen conveniente.
*   El **apartado 2** establece que los interesados tienen derecho a no aportar documentos que ya se encuentren en poder de la Administración actuante o que hayan sido elaborados por cualquier otra Administración, pudiendo la Administración actuante consultar o recabar dichos documentos salvo que el interesado se opusiera a ello. El propio artículo 28.2 precisa que no cabrá tal oposición cuando la aportación del documento se exija en el marco del ejercicio de potestades sancionadoras o de inspección.
*   El **apartado 3** dispone que las Administraciones Públicas no exigirán a los interesados la presentación de documentos originales, salvo que, con carácter excepcional, la normativa reguladora aplicable establezca lo contrario.

## Referencias normativas y técnicas

*   Reglamento (UE) 2024/1689 del Parlamento Europeo y del Consejo, de 13 de junio de 2024, por el que se establecen normas armonizadas en materia de inteligencia artificial (Reglamento de Inteligencia Artificial).
*   Reglamento (UE) 2024/903 del Parlamento Europeo y del Consejo, de 13 de marzo de 2024, por el que se establecen medidas a fin de garantizar un alto nivel de interoperabilidad del sector público en toda la Unión (Reglamento sobre la Europa Interoperable).
*   Reglamento (UE) 2022/868 del Parlamento Europeo y del Consejo, de 30 de mayo de 2022, relativo a la gobernanza europea de datos y por el que se modifica el Reglamento (UE) 2018/1724 (Reglamento de Gobernanza de Datos).
*   Reglamento (UE) 2018/1724 del Parlamento Europeo y del Consejo, de 2 de octubre de 2018, relativo a la creación de una pasarela digital única de acceso a información, procedimientos y servicios de asistencia y resolución de problemas.
*   Ley Orgánica 3/2018, de 5 de diciembre, de Protección de Datos Personales y garantía de los derechos digitales.
*   Real Decreto 311/2022, de 3 de mayo, por el que se regula el Esquema Nacional de Seguridad.
*   Real Decreto 203/2021, de 30 de marzo, por el que se aprueba el Reglamento de actuación y funcionamiento del sector público por medios electrónicos.
*   Real Decreto 4/2010, de 8 de enero, por el que se regula el Esquema Nacional de Interoperabilidad (ENI) en el ámbito de la Administración Electrónica.
*   Resolución de 19 de julio de 2011, de la Secretaría de Estado para la Función Pública, por la que se aprueba la Norma Técnica de Interoperabilidad de Documento Electrónico.
*   Resolución de 19 de julio de 2011, de la Secretaría de Estado para la Función Pública, por la que se aprueba la Norma Técnica de Interoperabilidad de Expediente Electrónico.
*   Resolución de 28 de junio de 2012, de la Secretaría de Estado de Administraciones Públicas, por la que se aprueba la Norma Técnica de Interoperabilidad de Política de gestión de documentos electrónicos.
*   Resolución de 3 de octubre de 2012, de la Secretaría de Estado de Administraciones Públicas, por la que se aprueba la Norma Técnica de Interoperabilidad de Catálogo de estándares.
*   Resolución de 19 de febrero de 2013, de la Secretaría de Estado de Administraciones Públicas, por la que se aprueba la Norma Técnica de Interoperabilidad de Reutilización de recursos de información.
*   Ley 39/2015, de 1 de octubre, del Procedimiento Administrativo Común de las Administraciones Públicas.
*   Norma ISO/IEC 25012, Ingeniería de software y de sistemas — Requisitos y evaluación de calidad de sistemas y software (SQuaRE) — Modelo de calidad de datos.
*   Norma ISO/IEC 25024, Ingeniería de software y de sistemas — Requisitos y evaluación de calidad de sistemas y software (SQuaRE) — Medición de la calidad de datos.
*   Especificación UNE 0081:2023, Calidad de datos. Modelo de referencia.
