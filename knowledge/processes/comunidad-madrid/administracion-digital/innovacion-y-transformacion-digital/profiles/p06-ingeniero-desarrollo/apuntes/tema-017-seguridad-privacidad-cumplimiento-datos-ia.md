---
id: "cm-ad-innovacion-y-transformacion-digital-tema-017-seguridad-privacidad-cumplimiento-datos-ia.md"
title: "Seguridad, privacidad y cumplimiento en datos e IA"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/innovacion-y-transformacion-digital"
profiles:
  - "p06-ingeniero-desarrollo"
official_profiles:
  - "P06 - Ingeniero de Desarrollo"
official_topic: "Tema 17. Seguridad, privacidad y cumplimiento en datos e IA"
source_ids: []
tags:
  - "reglamento-ia"
  - "ai-act"
  - "ue-2024-2689"
  - "riesgos-ia"
  - "ia-responsable"
  - "evaluacion-impacto"
  - "evaluacion-impacto-algoritmico"
  - "une-iso-iec-42001"
  - "gestion-sistemas-ia"
  - "sandbox-regulatorio"
  - "articulo-22-rgpd"
created_at: "2026-09-03"
last_reviewed: "2026-09-09"
ai_generated: true
ai_sources:
  - "perplexity"
  - "chatgpt"
  - "gemini"
needs_human_review: true
---

# Tema 17. Seguridad, privacidad y cumplimiento en datos e IA

## 1. RGPD y LOPDGDD aplicados a datos e IA.

**Compatibilidad normativa**
El marco regulatorio de la Inteligencia Artificial (Reglamento UE 2024/1689) se aplica sin perjuicio del Derecho de la Unión o nacional en materia de protección de datos personales. En la medida en que el diseño, desarrollo o uso de sistemas de IA impliquen el tratamiento de datos personales, resultan de plena y directa aplicación el Reglamento General de Protección de Datos (RGPD) y la Ley Orgánica 3/2018 (LOPDGDD).

**Tratamiento de categorías especiales de datos en la IA**
Con carácter general, el tratamiento de categorías especiales de datos (origen racial, opiniones políticas, datos genéticos, biométricos o de salud) está sujeto a las estrictas prohibiciones y excepciones del artículo 9 del RGPD y el artículo 9 de la LOPDGDD.
No obstante, el Reglamento de IA introduce una habilitación excepcional: los proveedores de sistemas de IA de alto riesgo podrán tratar categorías especiales de datos personales exclusivamente en la medida en que sea estrictamente necesario para garantizar la detección y corrección de sesgos asociados a dichos sistemas. Este tratamiento excepcional está condicionado al cumplimiento acumulativo de las siguientes garantías:
*   Imposibilidad de realizar la detección y corrección de sesgos mediante el tratamiento de otros datos (como datos sintéticos o anonimizados).
*   Aplicación de limitaciones técnicas relativas a la reutilización, implementando medidas punteras de seguridad y privacidad, incluida la seudonimización.
*   Controles de acceso estrictos, documentados y sujetos a obligaciones de confidencialidad.
*   Prohibición absoluta de transmisión o transferencia a terceros.
*   Eliminación inmediata de los datos una vez corregido el sesgo o alcanzado el límite del período de conservación.

**Decisiones individuales automatizadas**
El **artículo 22, apartado 1, del RGPD** establece literalmente que todo interesado tendrá derecho a no ser objeto de una decisión basada únicamente en el tratamiento automatizado, incluida la elaboración de perfiles, que produzca efectos jurídicos en él o le afecte significativamente de modo similar. Este derecho admite excepciones tasadas cuando la decisión sea necesaria para la celebración o ejecución de un contrato, esté autorizada por el Derecho de la Unión o de los Estados miembros, o se base en el consentimiento explícito del interesado, debiendo en estos casos adoptarse medidas adecuadas para salvaguardar los derechos, libertades e intereses legítimos del interesado, incluido como mínimo el derecho a obtener intervención humana, a expresar su punto de vista y a impugnar la decisión.

El Tribunal de Justicia de la Unión Europea ha interpretado este precepto de forma amplia: en su sentencia de 7 de diciembre de 2023 (asunto SCHUFA Holding y otros, C-634/21), declaró que la generación automatizada de un valor de probabilidad sobre la solvencia futura de una persona constituye una "decisión individual automatizada" en el sentido del artículo 22.1 del RGPD cuando de ese valor dependa de manera determinante que un tercero establezca, ejecute o ponga fin a una relación contractual con dicha persona.

El Reglamento de IA complementa esta garantía estableciendo que las personas afectadas tienen derecho a obtener una explicación clara y significativa cuando la decisión de un responsable del despliegue se base principalmente en los resultados de salida de un sistema de IA de alto riesgo y produzca efectos jurídicos o perjudiciales en su salud, seguridad o derechos fundamentales.


### 1.1. Principios del RGPD aplicables a sistemas de IA

Cuando un sistema de IA trate datos personales, el tratamiento debe respetar los principios del artículo 5 del RGPD:

* licitud, lealtad y transparencia;
* limitación de la finalidad;
* minimización de datos;
* exactitud;
* limitación del plazo de conservación;
* integridad y confidencialidad;
* responsabilidad proactiva.

En sistemas de aprendizaje automático estos principios deben analizarse en las distintas etapas del ciclo de vida del dato: obtención, preparación, entrenamiento, validación, prueba, explotación, monitorización, conservación y supresión.

La existencia de una base jurídica para utilizar determinados datos no permite reutilizarlos automáticamente para cualquier finalidad posterior. Deben analizarse la finalidad y compatibilidad del tratamiento y la base jurídica aplicable.

### 1.2. Base jurídica y categorías especiales de datos

Antes de incorporar datos personales a un sistema de IA debe identificarse la base jurídica del tratamiento conforme al artículo 6 del RGPD. Cuando se traten categorías especiales de datos, debe concurrir además alguna de las condiciones previstas en el artículo 9.

En el análisis de un sistema de IA deben distinguirse los datos personales utilizados como datos de entrenamiento, los introducidos durante la utilización del sistema, los generados como salida y los datos derivados o inferidos. Estos últimos pueden seguir siendo datos personales cuando permitan identificar o hacer identificable a una persona física.

### 1.3. Responsable, encargado y corresponsables

El proyecto debe determinar quién actúa como **responsable del tratamiento**, quién como **encargado** y, en su caso, si existe **corresponsabilidad**.

El responsable determina los fines y medios del tratamiento. El encargado trata datos personales por cuenta del responsable y debe actuar conforme a las instrucciones documentadas y a las obligaciones del artículo 28 del RGPD.

Cuando dos o más responsables determinen conjuntamente los fines y medios del tratamiento, debe analizarse la aplicación del artículo 26 del RGPD.

### 1.4. Transparencia e información

El responsable debe facilitar a los interesados la información exigida por los artículos 13 y 14 del RGPD, según los datos hayan sido obtenidos directamente del interesado o de otras fuentes.

En sistemas de IA debe analizarse además cómo informar sobre las finalidades, categorías de datos, existencia de decisiones automatizadas y elaboración de perfiles cuando proceda y derechos de los interesados.

### 1.5. Decisiones automatizadas y elaboración de perfiles

El artículo 22 del RGPD regula las decisiones individuales basadas únicamente en tratamientos automatizados, incluida la elaboración de perfiles, cuando produzcan efectos jurídicos en el interesado o le afecten significativamente de modo similar.

Las excepciones previstas en el artículo 22.2 están sujetas a las garantías correspondientes. Entre ellas se encuentra, cuando proceda, el derecho a obtener intervención humana, expresar el punto de vista e impugnar la decisión.

Debe distinguirse entre utilizar IA como apoyo a una decisión adoptada por una persona y adoptar una decisión exclusivamente automatizada.

### 1.6. Evaluación de impacto relativa a la protección de datos

La **EIPD/DPIA** corresponde al responsable del tratamiento y debe realizarse antes del tratamiento cuando sea probable que este entrañe un alto riesgo para los derechos y libertades de las personas físicas.

La evaluación debe contener, como mínimo:

* descripción sistemática de las operaciones de tratamiento y de sus fines;
* evaluación de la necesidad y proporcionalidad;
* evaluación de los riesgos para los derechos y libertades;
* medidas previstas para afrontar los riesgos y demostrar el cumplimiento del RGPD.

La EIPD debe revisarse cuando se produzca un cambio relevante que pueda afectar al nivel de riesgo del tratamiento.

## 2. Esquema Nacional de Seguridad (ENS).

**Integración del ENS en sistemas de IA**
El Real Decreto 311/2022, regulador del Esquema Nacional de Seguridad, impone la adopción de medidas técnicas, organizativas y operacionales proporcionadas al riesgo para la protección de la información tratada y los servicios prestados por el sector público.
Cuando un sistema de IA desarrollado, adquirido o explotado por la Administración Pública trate datos personales, la gestión de riesgos deberá coordinar las exigencias del ENS con las del RGPD. En caso de discrepancia normativa entre las medidas derivadas del análisis de riesgos de protección de datos (Art. 24 y 35 del RGPD) y las exigidas por el ENS, prevalecerán siempre las más estrictas o agravadas.

**Requisitos de ciberseguridad en IA**
El ENS exige una estrategia de defensa en profundidad, vigilancia continua y reevaluación periódica. Las soluciones de Inteligencia Artificial que se integren en las Administraciones Públicas, particularmente si se comercializan como servicios en la nube (SaaS, PaaS, IaaS), deberán cumplir con las medidas del ENS y utilizar componentes o servicios que posean las correspondientes declaraciones o certificaciones de conformidad.


### 2.1. Integración del ENS en el ciclo de vida

El artículo 36 del Real Decreto 311/2022 establece que la seguridad se considerará un requisito integral del ciclo de vida de los servicios y sistemas, desde su especificación hasta su retirada o sustitución.

En sistemas de IA esto implica incorporar la seguridad en el análisis, diseño, adquisición o desarrollo, integración, pruebas, puesta en servicio, operación, mantenimiento, gestión de cambios y retirada.

La categorización del sistema y el análisis de riesgos deben utilizarse para determinar las medidas de seguridad aplicables.

### 2.2. Principios y medidas del ENS

El ENS se basa, entre otros, en los principios de seguridad integral, gestión de riesgos, prevención, reacción y recuperación, líneas de defensa, vigilancia continua y reevaluación periódica y diferenciación de responsabilidades.

Las medidas de seguridad se estructuran en:

* **marco organizativo**;
* **marco operacional**;
* **medidas de protección**.

Su aplicación se adecua a la categoría de seguridad del sistema y al análisis de riesgos.

### 2.3. Categorías y dimensiones de seguridad

El ENS establece las categorías **BÁSICA, MEDIA y ALTA**.

La valoración considera las dimensiones:

* **Confidencialidad (C)**.
* **Integridad (I)**.
* **Trazabilidad (T)**.
* **Autenticidad (A)**.
* **Disponibilidad (D)**.

La categoría determina el conjunto de medidas exigibles. Los sistemas que tratan datos personales deben coordinar las medidas de seguridad del ENS con las obligaciones derivadas de la normativa de protección de datos.

### 2.4. Riesgos específicos de sistemas de IA

Además de las amenazas tradicionales de software e infraestructura, los sistemas de IA pueden presentar riesgos asociados a:

* manipulación de datos de entrenamiento;
* manipulación de datos de entrada;
* alteración o extracción de modelos;
* ataques adversarios;
* extracción de información del modelo;
* inferencia sobre datos utilizados en entrenamiento;
* revelación accidental de información;
* abuso de interfaces de modelos generativos;
* dependencias y componentes de terceros.

La evaluación de riesgos debe considerar el modelo, los datos, las interfaces, la infraestructura, los agentes humanos y las dependencias externas.

### 2.5. Seguridad de la cadena de suministro de IA

Cuando un sistema integra modelos, bibliotecas, conjuntos de datos, APIs o servicios de terceros, deben identificarse las dependencias y sus riesgos.

La gestión de la cadena de suministro debe considerar procedencia, integridad, versiones, vulnerabilidades conocidas, actualizaciones, controles de acceso, condiciones contractuales y capacidad de respuesta ante incidentes.

### 2.6. Protección de datos desde el diseño

El artículo 25 del RGPD obliga al responsable a aplicar, desde el momento de determinar los medios del tratamiento y durante el propio tratamiento, medidas técnicas y organizativas apropiadas para aplicar eficazmente los principios de protección de datos.

La protección de datos desde el diseño debe considerar la naturaleza, alcance, contexto y fines del tratamiento, los riesgos para los derechos y libertades, el estado de la técnica y los costes de aplicación.

### 2.7. Protección de datos por defecto

La protección de datos por defecto exige que, de manera predeterminada, solo sean objeto de tratamiento los datos personales necesarios para cada finalidad específica.

La obligación afecta, entre otros aspectos, a la cantidad de datos recogidos, la extensión del tratamiento, el plazo de conservación y la accesibilidad.

## 3. Protección de datos por diseño y por defecto.

**Principios fundamentales**
El derecho a la intimidad y a la protección de datos personales debe garantizarse de forma proactiva a lo largo de todo el ciclo de vida del sistema de IA. Los principios de minimización de datos y de protección de datos desde el diseño y por defecto (Privacy by Design and by Default), consagrados en el RGPD, son de obligado cumplimiento en el diseño de las arquitecturas de aprendizaje automático.

**Técnicas de implementación**
Para satisfacer estos principios en entornos de IA, las medidas adoptadas por los proveedores y responsables del despliegue deben contemplar:
*   El uso exhaustivo de técnicas de anonimización y cifrado de los conjuntos de datos.
*   La implementación de arquitecturas que permitan llevar los algoritmos a los datos (como el aprendizaje federado o *Federated Learning*), posibilitando el entrenamiento de los sistemas de IA sin que resulte necesaria la transmisión centralizada, el intercambio entre partes o la copia de los datos en bruto.
*   El aseguramiento de la integridad y representatividad estadística del conjunto de datos de entrenamiento, validación y prueba, respetando siempre la finalidad original de la recopilación de datos personales.


### 3.1. Minimización, seudonimización y anonimización

La **minimización** exige limitar los datos a los adecuados, pertinentes y necesarios para las finalidades del tratamiento.

La **seudonimización** reduce la vinculación directa con la identidad mediante información adicional separada. Los datos seudonimizados continúan siendo datos personales cuando puedan atribuirse a una persona utilizando esa información adicional.

La **anonimización** requiere que la persona no pueda ser identificada por medios razonablemente utilizables. Los datos efectivamente anonimizados quedan fuera del ámbito del RGPD.

En IA estas técnicas deben evaluarse en función del riesgo real de reidentificación.

### 3.2. Técnicas de preservación de la privacidad en IA

Dependiendo del tratamiento pueden utilizarse:

* anonimización;
* seudonimización;
* cifrado;
* control granular de acceso;
* segregación de datos;
* minimización;
* aprendizaje federado;
* privacidad diferencial;
* procesamiento local o descentralizado.

La selección debe estar justificada por el riesgo, la finalidad y la naturaleza del tratamiento.

### 3.3. Requisitos del artículo 15 del Reglamento de IA

El artículo 15 del Reglamento (UE) 2024/1689 exige que los sistemas de IA de alto riesgo alcancen niveles adecuados de **precisión, solidez y ciberseguridad** y mantengan estas características durante todo su ciclo de vida.

Los sistemas deben ser resistentes a errores, fallos, incoherencias y determinados intentos de terceros no autorizados de alterar su uso, resultados o funcionamiento.

El artículo contempla expresamente amenazas como el **envenenamiento de datos o modelos**, determinados **ataques adversarios o de evasión** y ataques dirigidos a comprometer la confidencialidad.

### 3.4. Evaluación de seguridad y pruebas

El proyecto debe establecer procedimientos para evaluar la robustez y seguridad del sistema antes de su despliegue y durante su funcionamiento.

Pueden formar parte del proceso, según el sistema:

* análisis de vulnerabilidades;
* pruebas de seguridad;
* pruebas adversariales;
* validación de entradas;
* revisión de controles de acceso;
* pruebas de recuperación;
* monitorización de comportamiento;
* evaluación de dependencias.

La intensidad de las pruebas debe adecuarse al riesgo y al uso previsto.

## 4. Riesgos de seguridad en datos e IA.

Los sistemas de IA introducen vectores de ataque y vulnerabilidades que trascienden la ciberseguridad tradicional del software. La base jurídica específica de esta obligación es el **artículo 15 del Reglamento (UE) 2024/1689 ("Precisión, solidez y ciberseguridad")**, que exige que los sistemas de IA de alto riesgo se diseñen y desarrollen de modo que alcancen un nivel adecuado de precisión, solidez y ciberseguridad y funcionen de manera uniforme en esos sentidos durante todo su ciclo de vida. El apartado 3 de este artículo exige, además, que en las instrucciones de uso que acompañen a los sistemas de IA de alto riesgo se indiquen los niveles de precisión de dichos sistemas y los parámetros pertinentes para medirla, mientras que el apartado 4 exige que estos sistemas sean lo más resistentes posible en lo que respecta a los errores, fallos o incoherencias que puedan surgir en los propios sistemas o en el entorno en el que funcionan, en particular a causa de su interacción con personas físicas u otros sistemas.

El apartado 5 del artículo 15 exige literalmente que los sistemas de IA de alto riesgo sean resistentes a los intentos de terceros no autorizados de alterar su uso, sus resultados de salida o su funcionamiento aprovechando las vulnerabilidades del sistema, precisando que las soluciones técnicas destinadas a subsanar vulnerabilidades específicas de la IA deberán incluir, según corresponda, medidas para prevenir, detectar, combatir, resolver y controlar los siguientes ataques, enumerados de forma literal en el propio precepto:

*   **Envenenamiento de datos (Data Poisoning) y modelos:** Intentos de terceros no autorizados de manipular o alterar intencionadamente el conjunto de datos de entrenamiento o los componentes previamente entrenados, con el fin de modificar el comportamiento, las decisiones o los resultados de salida del sistema de IA.
*   **Ataques adversarios (Evasión de modelos):** Inyección de información de entrada maliciosa o imperceptiblemente alterada que está diseñada específicamente para hacer que el modelo de IA cometa un error de clasificación o predicción.
*   **Ataques a la confidencialidad (Inferencia de pertenencia):** Técnicas destinadas a deducir si un determinado dato personal o registro formó parte del conjunto de datos utilizado para entrenar el modelo de IA, comprometiendo el deber de confidencialidad y privacidad.
*   **Defectos en el modelo:** Fallos inherentes o debilidades estructurales en el algoritmo que pueden ser explotados mediante la elusión de las salvaguardias (jailbreaking).

Los sistemas de IA de alto riesgo deben ser resilientes ante estas amenazas, debiendo el proveedor documentar las soluciones técnicas adoptadas para prevenir, detectar, combatir, resolver y controlar dichos ataques. El propio artículo 13 del Reglamento exige que estas características, capacidades y limitaciones (incluido el nivel de precisión, solidez y ciberseguridad del artículo 15) se recojan expresamente en la información que el proveedor debe comunicar al responsable del despliegue antes o en el momento de la puesta en servicio del sistema.


### 4.1. Prácticas de IA prohibidas y enfoque basado en riesgo

El Reglamento (UE) 2024/1689 adopta un enfoque basado en el riesgo.

El **artículo 5** establece determinadas prácticas de IA prohibidas.

Los sistemas clasificados como **de alto riesgo** están sujetos a requisitos específicos sobre gestión de riesgos, datos, documentación, transparencia, supervisión humana, precisión, solidez y ciberseguridad.

La clasificación debe realizarse atendiendo a la finalidad prevista y a los supuestos definidos por el Reglamento y sus anexos.

### 4.2. Obligaciones de los proveedores de sistemas de IA de alto riesgo

El artículo 16 establece, entre otras, las siguientes obligaciones para los proveedores:

* garantizar la conformidad del sistema con los requisitos aplicables;
* disponer de un sistema de gestión de la calidad;
* conservar la documentación técnica;
* conservar determinados registros generados automáticamente;
* realizar la evaluación de conformidad que corresponda;
* elaborar la declaración UE de conformidad;
* cumplir las obligaciones de registro;
* adoptar las medidas correctoras necesarias cuando corresponda.

### 4.3. Obligaciones de los responsables del despliegue

El artículo 26 establece obligaciones específicas para los responsables del despliegue de sistemas de IA de alto riesgo.

Deben, entre otros aspectos:

* utilizar el sistema conforme a las instrucciones de uso;
* asignar supervisión humana a personas con competencia, formación y autoridad necesarias;
* asegurar la pertinencia y representatividad de los datos de entrada cuando ejerzan control sobre ellos;
* monitorizar el funcionamiento;
* conservar los registros generados bajo su control durante el periodo establecido;
* informar de determinados riesgos o incidentes y suspender el uso cuando resulte necesario.

### 4.4. Supervisión humana

La supervisión humana debe diseñarse de acuerdo con el propósito y el riesgo del sistema.

La persona responsable de la supervisión debe poder comprender las capacidades y limitaciones relevantes, interpretar las salidas, evitar una dependencia excesiva de ellas y, cuando proceda, decidir no utilizar la salida, anularla o detener el sistema.

### 4.5. Monitorización y vigilancia poscomercialización

Los proveedores de sistemas de IA de alto riesgo deben establecer mecanismos de **vigilancia poscomercialización** para recopilar y analizar información sobre el funcionamiento del sistema durante su vida útil y evaluar su conformidad continuada.

La gestión del ciclo de vida debe contemplar incidentes, cambios de versión, modificaciones del modelo, cambios en los datos y evolución del contexto de uso.

### 4.6. Gestión de calidad y documentación

El Reglamento de IA exige para los sistemas de alto riesgo un **sistema de gestión de la calidad** y documentación técnica suficiente para demostrar la conformidad.

La documentación debe permitir comprender el sistema y las medidas adoptadas para cumplir los requisitos aplicables. La trazabilidad debe abarcar, según corresponda, datos, diseño, desarrollo, pruebas, validación, evaluación de riesgos y modificaciones.

### 4.7. Obligaciones de transparencia

El artículo 50 establece obligaciones de transparencia para determinados sistemas de IA.

Los sistemas destinados a interactuar directamente con personas deben informar de la interacción con un sistema de IA, salvo que dicha circunstancia resulte evidente en el contexto de uso.

Para determinados contenidos sintéticos, el Reglamento establece obligaciones de marcado o etiquetado que permitan identificar su carácter generado o manipulado artificialmente.

## 5. Buenas prácticas en seguridad, privacidad y cumplimiento.

El cumplimiento integral del marco de seguridad y privacidad en el despliegue de IA exige la adopción de medidas proactivas que integren las obligaciones legales con los estándares técnicos y la vigilancia continua.

**Sistemas de gestión de calidad y riesgos**
Los proveedores de sistemas de IA de alto riesgo están obligados a implantar un sistema de gestión de la calidad sólido que documente de manera sistemática las políticas, los procedimientos y las instrucciones aplicadas al diseño, desarrollo, control de datos y gestión de modificaciones del modelo. Asimismo, el ciclo de vida del sistema requiere un sistema de vigilancia poscomercialización destinado a evaluar el funcionamiento continuo del sistema en entornos reales, documentando y reportando incidentes graves o defectos de funcionamiento a las autoridades competentes.

**Espacios controlados de pruebas para la IA (Regulatory Sandboxes)**
Con el fin de garantizar una innovación responsable que integre salvaguardias éticas y medidas de reducción de riesgos antes de su puesta en mercado, el **artículo 57 del Reglamento (UE) 2024/1689** obliga a los Estados miembros a velar por que sus autoridades competentes establezcan al menos un **espacio controlado de pruebas para la IA a escala nacional**, que deberá estar operativo a más tardar el **2 de agosto de 2026**. El artículo 3, apartado 55, del propio Reglamento define este concepto como un marco controlado establecido por una autoridad competente que ofrece a los proveedores y proveedores potenciales de sistemas de IA la posibilidad de desarrollar, entrenar, validar y probar, en condiciones reales cuando proceda, un sistema de IA innovador, con arreglo a un plan del espacio controlado de pruebas y durante un tiempo limitado, bajo supervisión regulatoria.

Estos entornos proporcionan un marco seguro bajo la supervisión de las autoridades competentes, permitiendo a los proveedores desarrollar, entrenar, validar y probar sistemas de IA innovadores en condiciones reales controladas, garantizando el respeto a la legalidad y la protección de datos. El artículo 59 del Reglamento habilita, con carácter excepcional y sujeto a garantías estrictas, el tratamiento en el espacio controlado de pruebas de datos personales recabados lícitamente con otros fines, exclusivamente con el objetivo de desarrollar, entrenar y probar determinados sistemas de IA dentro de dicho espacio controlado. El propio Reglamento contempla, además, la posibilidad de crear espacios controlados de pruebas conjuntos entre varios Estados miembros.

**Códigos de conducta voluntarios y estandarización**
Se fomenta que los proveedores de sistemas de IA no clasificados como de alto riesgo se adhieran de forma voluntaria a códigos de conducta y buenas prácticas. Estos códigos impulsan la aplicación proactiva de requisitos de transparencia, supervisión humana, solidez y sostenibilidad ambiental aplicables a la IA de alto riesgo, adaptados proporcionalmente al riesgo del sistema.
La demostración de la conformidad con los requisitos de seguridad y privacidad se facilita de manera significativa mediante la adhesión y certificación frente a normas armonizadas o especificaciones comunes reconocidas a nivel europeo o internacional.


### 5.1. Evaluación de impacto sobre los derechos fundamentales

El artículo 27 del Reglamento de IA establece, para determinados responsables del despliegue, incluidas determinadas entidades u organismos de Derecho público, la obligación de realizar una **evaluación de impacto sobre los derechos fundamentales** antes de poner en servicio determinados sistemas de IA de alto riesgo.

Esta evaluación complementa, cuando proceda, la EIPD del RGPD. Tienen objetos diferentes:

* la **EIPD** evalúa los riesgos del tratamiento de datos personales para los derechos y libertades;
* la **evaluación de impacto sobre los derechos fundamentales** analiza los efectos del sistema de IA sobre los derechos fundamentales en los supuestos establecidos por el Reglamento de IA.

### 5.2. Alfabetización en materia de IA

El artículo 4 del Reglamento de IA exige a proveedores y responsables del despliegue adoptar medidas para garantizar un nivel suficiente de **alfabetización en materia de IA** de su personal y de las personas encargadas del funcionamiento y utilización de sistemas de IA, teniendo en cuenta conocimientos técnicos, experiencia, educación, formación y contexto de uso.

### 5.3. Espacios controlados de pruebas para la IA

Los **espacios controlados de pruebas para la IA (regulatory sandboxes)** son entornos controlados establecidos por autoridades competentes para desarrollar, entrenar, validar y probar sistemas de IA innovadores bajo supervisión regulatoria y durante un tiempo limitado.

El Reglamento regula estos espacios en los artículos 57 y siguientes y contempla condiciones específicas para determinadas operaciones de tratamiento de datos personales dentro de ellos.

### 5.4. Normas y marcos técnicos de gestión de IA

Entre las referencias técnicas reconocidas se encuentran:

* **ISO/IEC 42001:2023**, que establece requisitos para un sistema de gestión de inteligencia artificial.
* **ISO/IEC 23894:2023**, que proporciona orientación sobre gestión de riesgos de inteligencia artificial.
* **NIST AI Risk Management Framework (AI RMF 1.0)**, marco voluntario para la gestión de riesgos asociados a sistemas de IA.
* **NIST AI 600-1**, perfil del AI RMF para inteligencia artificial generativa.

Estos marcos constituyen referencias técnicas y no sustituyen las obligaciones jurídicas del RGPD, del Reglamento de IA o del ENS.

### 5.5. Entrada en aplicación del Reglamento de IA

El Reglamento (UE) 2024/1689 establece una aplicación escalonada:

* **2 de febrero de 2025:** aplicación de los capítulos I y II, con las excepciones previstas en el artículo 113.
* **2 de agosto de 2025:** aplicación de las disposiciones indicadas en el artículo 113.
* **2 de agosto de 2026:** aplicación general del Reglamento, con las excepciones previstas.
* **2 de diciembre de 2027:** aplicación de determinadas obligaciones a determinados sistemas de alto riesgo del artículo 6.2.
* **2 de agosto de 2028:** aplicación de determinadas obligaciones a determinados sistemas de alto riesgo del artículo 6.1.

Los artículos 102 a 110 son aplicables desde el **27 de julio de 2026**, conforme a la versión consolidada vigente.

### 5.6. Integración de seguridad, privacidad y cumplimiento

En un sistema de IA, la gobernanza debe integrar:

**Gobernanza → datos → desarrollo → validación → despliegue → supervisión → cambios → incidentes → retirada.**

En cada etapa deben identificarse los requisitos legales, de seguridad, privacidad, calidad, trazabilidad y gestión de riesgos que resulten aplicables.

## 6. Referencias normativas y técnicas

*   Reglamento (UE) 2024/1689 del Parlamento Europeo y del Consejo, de 13 de junio de 2024 (artículos 3.55, 9, 10, 13, 14, 15, 22, 57 y 59).
*   Reglamento (UE) 2016/679 del Parlamento Europeo y del Consejo, de 27 de abril de 2016 (RGPD), artículos 9, 22, 24 y 35.
*   Ley Orgánica 3/2018, de 5 de diciembre, de Protección de Datos Personales y garantía de los derechos digitales (LOPDGDD), artículo 9.
*   Real Decreto 311/2022, de 3 de mayo, por el que se regula el Esquema Nacional de Seguridad.
*   Sentencia del Tribunal de Justicia de la Unión Europea de 7 de diciembre de 2023, asunto C-634/21 (SCHUFA Holding y otros), relativa a la interpretación del artículo 22.1 del RGPD.

## 6. Referencias normativas y técnicas

* Reglamento (UE) 2016/679 (RGPD).
* Ley Orgánica 3/2018, de 5 de diciembre, de Protección de Datos Personales y garantía de los derechos digitales.
* Real Decreto 311/2022, de 3 de mayo, por el que se regula el Esquema Nacional de Seguridad.
* Reglamento (UE) 2024/1689, por el que se establecen normas armonizadas en materia de inteligencia artificial (Reglamento de Inteligencia Artificial).
* ISO/IEC 42001:2023, Information technology — Artificial intelligence — Management system.
* ISO/IEC 23894:2023, Information technology — Artificial intelligence — Guidance on risk management.
* NIST AI Risk Management Framework (AI RMF 1.0).
* NIST AI 600-1, Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile.
