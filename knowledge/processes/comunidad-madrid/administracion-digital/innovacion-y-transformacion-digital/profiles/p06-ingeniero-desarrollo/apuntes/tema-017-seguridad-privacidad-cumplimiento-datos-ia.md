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

## 2. Esquema Nacional de Seguridad (ENS).

**Integración del ENS en sistemas de IA**
El Real Decreto 311/2022, regulador del Esquema Nacional de Seguridad, impone la adopción de medidas técnicas, organizativas y operacionales proporcionadas al riesgo para la protección de la información tratada y los servicios prestados por el sector público.
Cuando un sistema de IA desarrollado, adquirido o explotado por la Administración Pública trate datos personales, la gestión de riesgos deberá coordinar las exigencias del ENS con las del RGPD. En caso de discrepancia normativa entre las medidas derivadas del análisis de riesgos de protección de datos (Art. 24 y 35 del RGPD) y las exigidas por el ENS, prevalecerán siempre las más estrictas o agravadas.

**Requisitos de ciberseguridad en IA**
El ENS exige una estrategia de defensa en profundidad, vigilancia continua y reevaluación periódica. Las soluciones de Inteligencia Artificial que se integren en las Administraciones Públicas, particularmente si se comercializan como servicios en la nube (SaaS, PaaS, IaaS), deberán cumplir con las medidas del ENS y utilizar componentes o servicios que posean las correspondientes declaraciones o certificaciones de conformidad.

## 3. Protección de datos por diseño y por defecto.

**Principios fundamentales**
El derecho a la intimidad y a la protección de datos personales debe garantizarse de forma proactiva a lo largo de todo el ciclo de vida del sistema de IA. Los principios de minimización de datos y de protección de datos desde el diseño y por defecto (Privacy by Design and by Default), consagrados en el RGPD, son de obligado cumplimiento en el diseño de las arquitecturas de aprendizaje automático.

**Técnicas de implementación**
Para satisfacer estos principios en entornos de IA, las medidas adoptadas por los proveedores y responsables del despliegue deben contemplar:
*   El uso exhaustivo de técnicas de anonimización y cifrado de los conjuntos de datos.
*   La implementación de arquitecturas que permitan llevar los algoritmos a los datos (como el aprendizaje federado o *Federated Learning*), posibilitando el entrenamiento de los sistemas de IA sin que resulte necesaria la transmisión centralizada, el intercambio entre partes o la copia de los datos en bruto.
*   El aseguramiento de la integridad y representatividad estadística del conjunto de datos de entrenamiento, validación y prueba, respetando siempre la finalidad original de la recopilación de datos personales.

## 4. Riesgos de seguridad en datos e IA.

Los sistemas de IA introducen vectores de ataque y vulnerabilidades que trascienden la ciberseguridad tradicional del software. La base jurídica específica de esta obligación es el **artículo 15 del Reglamento (UE) 2024/1689 ("Precisión, solidez y ciberseguridad")**, que exige que los sistemas de IA de alto riesgo se diseñen y desarrollen de modo que alcancen un nivel adecuado de precisión, solidez y ciberseguridad y funcionen de manera uniforme en esos sentidos durante todo su ciclo de vida. El apartado 3 de este artículo exige, además, que en las instrucciones de uso que acompañen a los sistemas de IA de alto riesgo se indiquen los niveles de precisión de dichos sistemas y los parámetros pertinentes para medirla, mientras que el apartado 4 exige que estos sistemas sean lo más resistentes posible en lo que respecta a los errores, fallos o incoherencias que puedan surgir en los propios sistemas o en el entorno en el que funcionan, en particular a causa de su interacción con personas físicas u otros sistemas.

El apartado 5 del artículo 15 exige literalmente que los sistemas de IA de alto riesgo sean resistentes a los intentos de terceros no autorizados de alterar su uso, sus resultados de salida o su funcionamiento aprovechando las vulnerabilidades del sistema, precisando que las soluciones técnicas destinadas a subsanar vulnerabilidades específicas de la IA deberán incluir, según corresponda, medidas para prevenir, detectar, combatir, resolver y controlar los siguientes ataques, enumerados de forma literal en el propio precepto:

*   **Envenenamiento de datos (Data Poisoning) y modelos:** Intentos de terceros no autorizados de manipular o alterar intencionadamente el conjunto de datos de entrenamiento o los componentes previamente entrenados, con el fin de modificar el comportamiento, las decisiones o los resultados de salida del sistema de IA.
*   **Ataques adversarios (Evasión de modelos):** Inyección de información de entrada maliciosa o imperceptiblemente alterada que está diseñada específicamente para hacer que el modelo de IA cometa un error de clasificación o predicción.
*   **Ataques a la confidencialidad (Inferencia de pertenencia):** Técnicas destinadas a deducir si un determinado dato personal o registro formó parte del conjunto de datos utilizado para entrenar el modelo de IA, comprometiendo el deber de confidencialidad y privacidad.
*   **Defectos en el modelo:** Fallos inherentes o debilidades estructurales en el algoritmo que pueden ser explotados mediante la elusión de las salvaguardias (jailbreaking).

Los sistemas de IA de alto riesgo deben ser resilientes ante estas amenazas, debiendo el proveedor documentar las soluciones técnicas adoptadas para prevenir, detectar, combatir, resolver y controlar dichos ataques. El propio artículo 13 del Reglamento exige que estas características, capacidades y limitaciones (incluido el nivel de precisión, solidez y ciberseguridad del artículo 15) se recojan expresamente en la información que el proveedor debe comunicar al responsable del despliegue antes o en el momento de la puesta en servicio del sistema.

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

## Referencias normativas

*   Reglamento (UE) 2024/1689 del Parlamento Europeo y del Consejo, de 13 de junio de 2024 (artículos 3.55, 9, 10, 13, 14, 15, 22, 57 y 59).
*   Reglamento (UE) 2016/679 del Parlamento Europeo y del Consejo, de 27 de abril de 2016 (RGPD), artículos 9, 22, 24 y 35.
*   Ley Orgánica 3/2018, de 5 de diciembre, de Protección de Datos Personales y garantía de los derechos digitales (LOPDGDD), artículo 9.
*   Real Decreto 311/2022, de 3 de mayo, por el que se regula el Esquema Nacional de Seguridad.
*   Sentencia del Tribunal de Justicia de la Unión Europea de 7 de diciembre de 2023, asunto C-634/21 (SCHUFA Holding y otros), relativa a la interpretación del artículo 22.1 del RGPD.
