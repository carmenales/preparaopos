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
created_at: "2026-09-03"
last_reviewed: null
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
El marco regulatorio de la Inteligencia Artificial (Reglamento UE 2024/1689) se aplica sin perjuicio del Derecho de la Unión o nacional en materia de protección de datos personales[cite: 18]. En la medida en que el diseño, desarrollo o uso de sistemas de IA impliquen el tratamiento de datos personales, resultan de plena y directa aplicación el Reglamento General de Protección de Datos (RGPD) y la Ley Orgánica 3/2018 (LOPDGDD)[cite: 18].

**Tratamiento de categorías especiales de datos en la IA**
Con carácter general, el tratamiento de categorías especiales de datos (origen racial, opiniones políticas, datos genéticos, biométricos o de salud) está sujeto a las estrictas prohibiciones y excepciones del artículo 9 del RGPD y el artículo 9 de la LOPDGDD[cite: 20]. 
No obstante, el Reglamento de IA introduce una habilitación excepcional: los proveedores de sistemas de IA de alto riesgo podrán tratar categorías especiales de datos personales exclusivamente en la medida en que sea estrictamente necesario para garantizar la detección y corrección de sesgos asociados a dichos sistemas[cite: 18]. Este tratamiento excepcional está condicionado al cumplimiento acumulativo de las siguientes garantías[cite: 18]:
*   Imposibilidad de realizar la detección y corrección de sesgos mediante el tratamiento de otros datos (como datos sintéticos o anonimizados)[cite: 18].
*   Aplicación de limitaciones técnicas relativas a la reutilización, implementando medidas punteras de seguridad y privacidad, incluida la seudonimización[cite: 18].
*   Controles de acceso estrictos, documentados y sujetos a obligaciones de confidencialidad[cite: 18].
*   Prohibición absoluta de transmisión o transferencia a terceros[cite: 18].
*   Eliminación inmediata de los datos una vez corregido el sesgo o alcanzado el límite del período de conservación[cite: 18].

**Decisiones individuales automatizadas**
La normativa de protección de datos garantiza el derecho de los interesados a no ser objeto de una decisión basada únicamente en el tratamiento automatizado, incluida la elaboración de perfiles, que produzca efectos jurídicos o les afecte significativamente de modo similar (Art. 22 RGPD)[cite: 20]. El Reglamento de IA complementa esta garantía estableciendo que las personas afectadas tienen derecho a obtener una explicación clara y significativa cuando la decisión de un responsable del despliegue se base principalmente en los resultados de salida de un sistema de IA de alto riesgo y produzca efectos jurídicos o perjudiciales en su salud, seguridad o derechos fundamentales[cite: 18].

## 2. Esquema Nacional de Seguridad (ENS).

**Integración del ENS en sistemas de IA**
El Real Decreto 311/2022, regulador del Esquema Nacional de Seguridad, impone la adopción de medidas técnicas, organizativas y operacionales proporcionadas al riesgo para la protección de la información tratada y los servicios prestados por el sector público[cite: 17]. 
Cuando un sistema de IA desarrollado, adquirido o explotado por la Administración Pública trate datos personales, la gestión de riesgos deberá coordinar las exigencias del ENS con las del RGPD[cite: 17]. En caso de discrepancia normativa entre las medidas derivadas del análisis de riesgos de protección de datos (Art. 24 y 35 del RGPD) y las exigidas por el ENS, prevalecerán siempre las más estrictas o agravadas[cite: 17].

**Requisitos de ciberseguridad en IA**
El ENS exige una estrategia de defensa en profundidad, vigilancia continua y reevaluación periódica[cite: 17]. Las soluciones de Inteligencia Artificial que se integren en las Administraciones Públicas, particularmente si se comercializan como servicios en la nube (SaaS, PaaS, IaaS), deberán cumplir con las medidas del ENS y utilizar componentes o servicios que posean las correspondientes declaraciones o certificaciones de conformidad[cite: 17]. 

## 3. Protección de datos por diseño y por defecto.

**Principios fundamentales**
El derecho a la intimidad y a la protección de datos personales debe garantizarse de forma proactiva a lo largo de todo el ciclo de vida del sistema de IA[cite: 18]. Los principios de minimización de datos y de protección de datos desde el diseño y por defecto (Privacy by Design and by Default), consagrados en el RGPD, son de obligado cumplimiento en el diseño de las arquitecturas de aprendizaje automático[cite: 18].

**Técnicas de implementación**
Para satisfacer estos principios en entornos de IA, las medidas adoptadas por los proveedores y responsables del despliegue deben contemplar[cite: 18]:
*   El uso exhaustivo de técnicas de anonimización y cifrado de los conjuntos de datos[cite: 18].
*   La implementación de arquitecturas que permitan llevar los algoritmos a los datos (como el aprendizaje federado o *Federated Learning*), posibilitando el entrenamiento de los sistemas de IA sin que resulte necesaria la transmisión centralizada, el intercambio entre partes o la copia de los datos en bruto[cite: 18].
*   El aseguramiento de la integridad y representatividad estadística del conjunto de datos de entrenamiento, validación y prueba, respetando siempre la finalidad original de la recopilación de datos personales[cite: 18].

## 4. Riesgos de seguridad en datos e IA.

Los sistemas de IA introducen vectores de ataque y vulnerabilidades que trascienden la ciberseguridad tradicional del software. Para garantizar un nivel de ciberseguridad adecuado a los riesgos, los proveedores de sistemas de IA de alto riesgo deben adoptar medidas y controles de seguridad específicos que protejan la infraestructura TIC subyacente y los propios activos del modelo[cite: 18].

Entre las vulnerabilidades y ciberataques específicos dirigidos contra los sistemas de IA destacan[cite: 18]:
*   **Envenenamiento de datos (Data Poisoning) y modelos:** Intentos de terceros no autorizados de manipular o alterar intencionadamente el conjunto de datos de entrenamiento o los componentes previamente entrenados, con el fin de modificar el comportamiento, las decisiones o los resultados de salida del sistema de IA[cite: 18].
*   **Ataques adversarios (Evasión de modelos):** Inyección de información de entrada maliciosa o imperceptiblemente alterada que está diseñada específicamente para hacer que el modelo de IA cometa un error de clasificación o predicción[cite: 18].
*   **Ataques a la confidencialidad (Inferencia de pertenencia):** Técnicas destinadas a deducir si un determinado dato personal o registro formó parte del conjunto de datos utilizado para entrenar el modelo de IA, comprometiendo el deber de confidencialidad y privacidad[cite: 18].
*   **Defectos en el modelo:** Fallos inherentes o debilidades estructurales en el algoritmo que pueden ser explotados mediante la elusión de las salvaguardias (jailbreaking)[cite: 18].

Los sistemas de IA de alto riesgo deben ser resilientes ante estas amenazas, debiendo el proveedor documentar las soluciones técnicas adoptadas para prevenir, detectar, combatir, resolver y controlar dichos ataques[cite: 18]. 

## 5. Buenas prácticas en seguridad, privacidad y cumplimiento.

El cumplimiento integral del marco de seguridad y privacidad en el despliegue de IA exige la adopción de medidas proactivas que integren las obligaciones legales con los estándares técnicos y la vigilancia continua.

**Sistemas de gestión de calidad y riesgos**
Los proveedores de sistemas de IA de alto riesgo están obligados a implantar un sistema de gestión de la calidad sólido que documente de manera sistemática las políticas, los procedimientos y las instrucciones aplicadas al diseño, desarrollo, control de datos y gestión de modificaciones del modelo[cite: 18]. Asimismo, el ciclo de vida del sistema requiere un sistema de vigilancia poscomercialización destinado a evaluar el funcionamiento continuo del sistema en entornos reales, documentando y reportando incidentes graves o defectos de funcionamiento a las autoridades competentes[cite: 18].

**Espacios controlados de pruebas para la IA (Regulatory Sandboxes)**
Con el fin de garantizar una innovación responsable que integre salvaguardias éticas y medidas de reducción de riesgos antes de su puesta en mercado, se promueve el establecimiento de espacios controlados de pruebas (sandboxes regulatorios)[cite: 18]. Estos entornos proporcionan un marco seguro bajo la supervisión de las autoridades competentes, permitiendo a los proveedores desarrollar, entrenar, validar y probar sistemas de IA innovadores en condiciones reales controladas, garantizando el respeto a la legalidad y la protección de datos[cite: 18].

**Códigos de conducta voluntarios y estandarización**
Se fomenta que los proveedores de sistemas de IA no clasificados como de alto riesgo se adhieran de forma voluntaria a códigos de conducta y buenas prácticas[cite: 18]. Estos códigos impulsan la aplicación proactiva de requisitos de transparencia, supervisión humana, solidez y sostenibilidad ambiental aplicables a la IA de alto riesgo, adaptados proporcionalmente al riesgo del sistema[cite: 18]. 
La demostración de la conformidad con los requisitos de seguridad y privacidad se facilita de manera significativa mediante la adhesión y certificación frente a normas armonizadas o especificaciones comunes reconocidas a nivel europeo o internacional[cite: 18].