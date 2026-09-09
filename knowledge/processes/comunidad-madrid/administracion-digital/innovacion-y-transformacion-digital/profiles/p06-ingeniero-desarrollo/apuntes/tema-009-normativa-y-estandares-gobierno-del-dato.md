---
id: "cm-ad-innovacion-y-transformacion-digital-tema-009-normativa-y-estandaresgobierno-del-dato.md"
title: "Normativa y estándares de gobierno del dato"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/innovacion-y-transformacion-digital"
profiles:
  - "p06-ingeniero-desarrollo"
official_profiles:
  - "P06 - Ingeniero de Desarrollo"
official_topic: "Tema 9. Normativa y estándares de gobierno del dato"
source_ids: []
tags:
  - "gobierno-del-dato"
  - "gestión-del-dato"
  - "calidad-del-dato"
  - "implantación-del-gobierno-del dato"
  - "rdl-24-2021"
  - "ley-37-2007"
  - "reutilizacion"
  - "información-del-sector-publico"
  - "datos-abiertos"
  - "interoperabilidad"
  - "une-0077"
  - "une-0078"
  - "une-0079"
  - "une-0085"
  - "dcat-ap"
  - "eni"
created_at: "2026-09-03"
last_reviewed: "2026-09-09"
ai_generated: true
ai_sources:
  - "perplexity"
  - "chatgpt"
  - "gemini"
needs_human_review: true
---

# Tema 9. Normativa y estándares de gobierno del dato

## 1. Data Governance Act (Reglamento UE 2022/868).

**Naturaleza y Objeto**
El Reglamento (UE) 2022/868, conocido como la Ley de Gobernanza de Datos (Data Governance Act - DGA), establece un marco normativo armonizado a nivel europeo destinado a fomentar la disponibilidad de los datos y a crear un entorno de confianza que facilite su intercambio sectorial e intersectorial. Es aplicable en todos los Estados miembros desde el 24 de septiembre de 2023.

**Ejes principales de regulación**
*   **Reutilización de categorías protegidas de datos del sector público:** Establece un marco para la reutilización de datos en poder de organismos del sector público que están sujetos a derechos de terceros (protegidos por confidencialidad comercial, secreto estadístico, derechos de propiedad intelectual o protección de datos personales). Esta regulación no otorga un derecho de acceso absoluto, sino que articula los mecanismos técnicos y jurídicos seguros para su uso (por ejemplo, entornos de tratamiento seguro o técnicas de anonimización y seudonimización).
*   **Servicios de intermediación de datos:** Regula la figura de los proveedores de servicios de intermediación de datos (incluidas las cooperativas de datos). Impone un régimen de notificación a la autoridad competente y un estricto deber de neutralidad estructural: los proveedores no pueden utilizar los datos compartidos para otros fines distintos a la propia intermediación, debiendo existir separación estructural entre el servicio de intermediación y cualquier otro servicio prestado.
*   **Altruismo de datos:** Fomenta la cesión voluntaria de datos por parte de personas físicas (consentimiento) o jurídicas (permiso) para fines de interés general (investigación científica, mejora de servicios públicos, salud, lucha contra el cambio climático, etc.). Crea la figura de "organización reconocida de altruismo de datos", que exige su inscripción en un registro público transparente y el cumplimiento de estrictos requisitos de transparencia y salvaguarda de derechos.
*   **Comité Europeo de Innovación de Datos (EDIB):** Crea un grupo formal de expertos que asiste y asesora a la Comisión Europea en el desarrollo de directrices coherentes para el intercambio de datos, la interoperabilidad intersectorial y la adopción de normas relativas a los servicios de intermediación y el altruismo de datos.

## 2. Reutilización de la información del sector público.

**Marco jurídico: Ley 37/2007 y su modificación por el RDL 24/2021**

La regulación básica del régimen jurídico aplicable a la reutilización de los documentos elaborados o custodiados por los sujetos del sector público en España se encuentra en la **Ley 37/2007, de 16 de noviembre, sobre reutilización de la información del sector público**, que traspuso originalmente al ordenamiento español la primera Directiva europea sobre esta materia.

El **Real Decreto-ley 24/2021, de 2 de noviembre**, es una norma de transposición múltiple que incorpora al Derecho español varias Directivas de la Unión Europea en distintas materias (bonos garantizados, distribución transfronteriza de organismos de inversión colectiva, derechos de autor, protección de personas consumidoras, entre otras). En lo que respecta a datos abiertos y reutilización de la información del sector público, su **artículo 64 modifica expresamente la Ley 37/2007**, incorporando a dicha ley la transposición de la **Directiva (UE) 2019/1024 del Parlamento Europeo y del Consejo, de 20 de junio de 2019, relativa a los datos abiertos y la reutilización de la información del sector público** (conocida como "Directiva de Datos Abiertos" o "Directiva Open Data", que deroga la anterior Directiva 2003/98/CE). El Real Decreto-ley 24/2021 fue publicado en el BOE núm. 263, de 3 de noviembre de 2021, entró en vigor el 4 de noviembre de 2021, y fue convalidado por el Pleno del Congreso de los Diputados el 2 de diciembre de 2021.

Por tanto, la norma jurídica sustantiva que rige actualmente la reutilización de la información del sector público en España es la **Ley 37/2007**, en su redacción vigente tras la modificación operada por el artículo 64 del Real Decreto-ley 24/2021, y no este último de forma autónoma.

**Disposiciones clave**
*   **Diseño por defecto y desde el diseño (Open by default):** Consagra la obligación de las Administraciones Públicas y entes del sector público de garantizar que los documentos y datos estén disponibles desde su origen en formatos abiertos, legibles por máquina, accesibles, localizables y reutilizables, acompañados de sus respectivos metadatos.
*   **Conjuntos de datos de alto valor (High Value Datasets):** Introduce esta categoría jurídica referida a conjuntos de datos cuya reutilización se asocia a beneficios sistémicos para la sociedad, el medio ambiente y la economía. Se estructuran en seis categorías temáticas:
    1. Geoespaciales.
    2. Observación de la Tierra y medio ambiente.
    3. Meteorológicos.
    4. Estadística.
    5. Sociedades y propiedad de sociedades.
    6. Movilidad.
    Estos datos deben estar disponibles de forma gratuita, en formatos legibles por máquina, a través de interfaces de programación de aplicaciones (APIs) estandarizadas y, cuando proceda, mediante descarga masiva.
*   **Datos dinámicos:** Los datos sujetos a actualizaciones frecuentes o en tiempo real (datos dinámicos) deberán ponerse a disposición para su reutilización inmediatamente después de su recopilación mediante APIs adecuadas y, si procede, como descarga masiva.
*   **Datos de investigación:** Extiende el ámbito de aplicación a los datos de investigación financiados con fondos públicos. Rige el principio "tan abierto como sea posible, tan cerrado como sea necesario", salvaguardando la privacidad, los secretos comerciales, la seguridad nacional y la propiedad intelectual.
*   **Régimen de tarifas:** Como norma general, la reutilización será gratuita. Excepcionalmente, se permite la recuperación de costes marginales directamente derivados de la reproducción, puesta a disposición y difusión. Solo en supuestos muy tasados (organismos que deban generar ingresos para cubrir una parte sustancial de sus costes) se permite el cobro de tarifas superiores, que deberán calcularse con arreglo a criterios objetivos, transparentes y verificables.

## 3. Normas UNE:

El marco de estandarización español, impulsado institucionalmente a través de la Oficina del Dato (dependiente de la Secretaría de Estado de Digitalización e Inteligencia Artificial), ha publicado la familia de Especificaciones UNE 0077, 0078, 0079 y 0085. Estas especificaciones asientan las bases técnicas, semánticas y organizativas del gobierno, la gestión y la calidad del dato en las organizaciones.

### 3.1. UNE 0077: gobierno del dato
*   **Objeto:** Establece un modelo de referencia para el Gobierno del Dato en las organizaciones, proporcionando las directrices operativas y directivas necesarias para transformar el dato en un activo estratégico, maximizando su valor y mitigando sus riesgos.
*   **Alcance organizativo:** Define los principios fundamentales y la estructura organizativa requerida, formalizando los roles y responsabilidades críticos:
    *   *Sponsor:* Patrocinador ejecutivo de la iniciativa.
    *   *Chief Data Officer (CDO):* Máximo responsable directivo de la estrategia y gobierno de los datos.
    *   *Propietario del Dato (Data Owner):* Responsable de negocio sobre la definición, calidad y reglas de acceso a un dominio de datos específico.
    *   *Gestor del Dato (Data Steward):* Enlace operativo encargado de la ejecución de las políticas, gestión de metadatos y resolución de incidencias de calidad.
*   **Funciones:** Garantiza que los datos satisfagan los requisitos de negocio, promoviendo el cumplimiento regulatorio, la seguridad y la privacidad desde el diseño.

### 3.2. UNE 0078: gestión del dato
*   **Objeto:** Describe los procesos operativos y tácticos necesarios para la correcta ejecución técnica y funcional de la gestión de datos, subordinada a las directrices establecidas por el gobierno del dato.
*   **Alcance:** Establece el marco procedimental para gestionar el ciclo de vida completo del dato (creación/adquisición, almacenamiento, uso/mantenimiento, archivo y destrucción). Regula áreas de conocimiento técnicas fundamentales:
    *   Arquitectura y modelado de datos.
    *   Integración e interoperabilidad.
    *   Gestión de datos maestros y de referencia (MDM).
    *   Gestión técnica de metadatos.
    *   Seguridad operativa y almacenamiento.

### 3.3. UNE 0079: calidad del dato
*   **Objeto:** Proporciona un marco metodológico estructurado para planificar, evaluar, medir y mejorar la calidad de los datos de manera sistemática y continua en la organización.
*   **Alcance:** Define un catálogo estandarizado de dimensiones de calidad, entre las que destacan:
    *   *Exactitud (Accuracy):* Grado en el que el dato representa fielmente la realidad.
    *   *Completitud (Completeness):* Ausencia de valores nulos o atributos faltantes requeridos.
    *   *Consistencia (Consistency):* Coherencia del dato a través de distintos sistemas o conjuntos.
    *   *Integridad (Integrity):* Validez de las relaciones estructurales de los datos.
    *   *Actualidad (Timeliness):* Disponibilidad del dato en el momento requerido por el proceso de negocio.
    *   *Trazabilidad (Traceability):* Capacidad de identificar el linaje del dato (origen y transformaciones).
    Establece las pautas para el perfilado de datos (data profiling), la definición de reglas de validación y la monitorización mediante indicadores clave de calidad (KQI).

### 3.4. UNE 0085: implantación del gobierno del dato
*   **Objeto:** Establece una guía metodológica y de buenas prácticas organizativas orientada a la adopción, despliegue y evaluación continua del gobierno del dato.
*   **Alcance:** Proporciona una hoja de ruta para la implantación progresiva de las capacidades descritas en las normas UNE 0077, 0078 y 0079. Facilita metodologías estructuradas para:
    *   Evaluar el nivel de madurez inicial de la organización en la gestión de la información.
    *   Definir un modelo iterativo de adopción (roadmap).
    *   Articular la gestión del cambio cultural necesario para la transición hacia una organización orientada al dato (data-driven).

## 4. Datos abiertos e interoperabilidad.

**Fundamentos de la apertura de datos (Open Data)**
La apertura de datos del sector público requiere la puesta a disposición de la información bajo condiciones técnicas y jurídicas que no impongan restricciones indebidas a su reutilización. Este paradigma se sustenta en la interoperabilidad en sus dimensiones organizativa, semántica, técnica y legal, garantizando la independencia tecnológica.

**Esquema Nacional de Interoperabilidad (ENI) y NTI de Reutilización**
El **Esquema Nacional de Interoperabilidad (ENI)** se regula mediante el **Real Decreto 4/2010, de 8 de enero**, que establece las condiciones necesarias de interoperabilidad para el adecuado ejercicio de los derechos y el cumplimiento de los deberes de acceso electrónico a los servicios públicos, en el ámbito de la Administración Electrónica. El propio Real Decreto 4/2010 prevé el desarrollo de un conjunto de Normas Técnicas de Interoperabilidad (NTI), definiendo entre ellas la **Norma Técnica de Interoperabilidad de Reutilización de recursos de información**, que trata sobre las normas comunes relativas a la localización, descripción e identificación unívoca de los recursos de información puestos a disposición del público por medios electrónicos para su reutilización.

Esta NTI de Reutilización se aprobó específicamente mediante la **Resolución de 19 de febrero de 2013, de la Secretaría de Estado de Administraciones Públicas**. Su objeto es establecer el conjunto de pautas básicas para la reutilización de documentos y recursos de información elaborados o custodiados por el sector público a los que se refiere el artículo 3 de la Ley 37/2007, de 16 de noviembre, estableciendo condiciones comunes sobre selección, identificación, descripción, formato, condiciones de uso y puesta a disposición de dichos recursos, relativos a numerosos ámbitos de interés como la información social, económica, jurídica, turística, sobre empresas o educación.

**Principios técnicos de publicación e interoperabilidad**
*   **Formatos abiertos y estándares:** La información debe exponerse en formatos no propietarios, independientes de plataforma y estructurados (tales como CSV, JSON, XML, RDF), proscribiendo el uso exclusivo de formatos de representación visual cerrados (como PDF no estructurados o imágenes).
*   **Gestión de metadatos y vocabularios comunes:** La interoperabilidad semántica exige describir el contexto, calidad, estructura y características técnicas de los datos mediante esquemas de metadatos estandarizados. A nivel europeo, el estándar de referencia es el perfil de aplicación **DCAT-AP** (Data Catalog Vocabulary — Application Profile), un perfil de aplicación basado en el vocabulario DCAT del W3C, diseñado para mejorar la interoperabilidad de los catálogos de datos abiertos del sector público en Europa, proporcionando un modelo común de metadatos que facilita el intercambio, agregación y federación de catálogos de diferentes países y organizaciones. A nivel nacional, se está desarrollando el perfil de aplicación **DCAT-AP-ES**, que adapta las directrices del esquema europeo DCAT-AP a las particularidades del contexto español, y que se plantea como ampliación y evolución de la actual NTI de Reutilización de recursos de información (NTI-RISP), enmarcada en el propio Esquema Nacional de Interoperabilidad. El uso de DCAT-AP y DCAT-AP-ES permite el descubrimiento semántico, la federación de catálogos y la recolección automática (harvesting) por parte del portal nacional de datos abiertos (*datos.gob.es*) y el portal europeo (*data.europa.eu*).
*   **Identificadores Uniformes de Recursos (URI):** El diseño del esquema de direccionamiento de los recursos de información debe basarse en identificadores únicos y persistentes en el tiempo (URIs permanentes). Esto resulta crítico para garantizar la correcta hipervinculación semántica y la conformación de la web de datos enlazados (Linked Open Data).
*   **Licenciamiento y acceso legal:** La interoperabilidad legal exige la vinculación explícita de los conjuntos de datos a condiciones de uso estandarizadas y abiertas, preferentemente mediante licencias tipo *Creative Commons* (como CC-BY para requerir atribución, o CC0 para dominio público). Quedan proscritas las cláusulas de exclusividad o las limitaciones discriminatorias, con las únicas excepciones tasadas por la legislación en materia de protección de datos de carácter personal, seguridad nacional, o propiedad industrial e intelectual de terceros.

## Referencias normativas y técnicas

*   Reglamento (UE) 2022/868 del Parlamento Europeo y del Consejo, de 30 de mayo de 2022, relativo a la gobernanza europea de datos (Data Governance Act), de aplicación desde el 24 de septiembre de 2023.
*   Ley 37/2007, de 16 de noviembre, sobre reutilización de la información del sector público.
*   Real Decreto-ley 24/2021, de 2 de noviembre (BOE núm. 263, de 3 de noviembre de 2021), artículo 64, que modifica la Ley 37/2007 para transponer la Directiva (UE) 2019/1024, de 20 de junio de 2019, relativa a los datos abiertos y la reutilización de la información del sector público.
*   Real Decreto 4/2010, de 8 de enero, por el que se regula el Esquema Nacional de Interoperabilidad (ENI) en el ámbito de la Administración Electrónica.
*   Resolución de 19 de febrero de 2013, de la Secretaría de Estado de Administraciones Públicas, por la que se aprueba la Norma Técnica de Interoperabilidad de Reutilización de recursos de información (NTI-RISP).
*   Especificación UNE 0077:2023, Gobierno del dato.
*   Especificación UNE 0078:2023, Gestión del dato.
*   Especificación UNE 0079:2023, Gestión de la calidad del dato.
*   Especificación UNE 0085, Implantación del gobierno del dato.
*   DCAT-AP (Data Catalog Vocabulary — Application Profile), perfil de aplicación europeo basado en el vocabulario DCAT del W3C.
*   DCAT-AP-ES, perfil de aplicación nacional derivado de DCAT-AP, en desarrollo como ampliación de la NTI-RISP.
