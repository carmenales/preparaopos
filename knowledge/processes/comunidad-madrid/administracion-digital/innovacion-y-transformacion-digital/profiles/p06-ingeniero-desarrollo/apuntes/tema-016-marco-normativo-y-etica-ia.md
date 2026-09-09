---
id: "cm-ad-innovacion-y-transformacion-digital-tema-016-marco-normativo-y-etica-ia"
title: "Marco normativo y ética de la Inteligencia Artificial"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/innovacion-y-transformacion-digital"
profiles:
  - "p06-ingeniero-desarrollo"
official_profiles:
  - "P06 - Ingeniero de Desarrollo"
official_topic: "Tema 16. Marco normativo y ética de la Inteligencia Artificial"
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
last_reviewed: "2026-09-09"
ai_generated: true
ai_sources:
  - "perplexity"
  - "chatgpt"
  - "gemini"
needs_human_review: true
---

# Tema 16. Marco normativo y ética de la Inteligencia Artificial

## 1. Reglamento de IA (AI Act – UE 2024/1689).

**Objeto y finalidad**
El Reglamento (UE) 2024/1689 establece un marco jurídico uniforme para el desarrollo, la introducción en el mercado, la puesta en servicio y la utilización de sistemas de inteligencia artificial (IA) en la Unión Europea[cite: 17]. Su objetivo es mejorar el funcionamiento del mercado interior y promover la adopción de una IA centrada en el ser humano y fiable, garantizando un elevado nivel de protección de la salud, la seguridad y los derechos fundamentales, incluidos la democracia, el Estado de Derecho y la protección del medio ambiente[cite: 17]. 

**Ámbito de aplicación**
El Reglamento se aplica de manera extraterritorial y abarca a toda la cadena de valor[cite: 17]. Están sujetos a sus disposiciones:
*   Proveedores que introduzcan en el mercado o pongan en servicio sistemas o modelos de IA de uso general en la Unión, independientemente de si están establecidos en un Estado miembro o en un tercer país[cite: 17].
*   Responsables del despliegue de sistemas de IA ubicados o establecidos en la Unión[cite: 17].
*   Proveedores y responsables del despliegue en terceros países, si los resultados de salida (output) generados por el sistema se utilizan en la Unión[cite: 17].
*   Importadores, distribuidores y representantes autorizados[cite: 17].
*   Fabricantes de productos que introduzcan sistemas de IA junto con su producto y bajo su propia marca[cite: 17].

**Exclusiones**
Quedan expresamente excluidos del ámbito de aplicación:
*   Los sistemas de IA desarrollados o utilizados exclusivamente con fines militares, de defensa o de seguridad nacional[cite: 17].
*   Los sistemas y modelos de IA desarrollados y puestos en servicio con la investigación y el desarrollo científicos como única finalidad[cite: 17].
*   Las actividades de investigación, prueba o desarrollo previas a la introducción en el mercado (con excepción de las pruebas en condiciones reales)[cite: 17].
*   Los sistemas de IA divulgados bajo licencias libres y de código abierto, salvo que sean clasificados como de alto riesgo o incurran en prácticas prohibidas[cite: 17].

## 2. Clasificación de riesgos en IA.

El Reglamento adopta un enfoque basado en los riesgos, adaptando la carga normativa a la intensidad de los riesgos que generan los sistemas[cite: 17].

**A) Riesgo Inaceptable (Prácticas de IA prohibidas - Art. 5)**
Se prohíbe la comercialización, puesta en servicio o uso de sistemas de IA que incurran en las siguientes prácticas[cite: 17]:
*   Uso de técnicas subliminales, manipuladoras o engañosas que alteren sustancialmente el comportamiento humano provocando perjuicios considerables[cite: 17].
*   Explotación de vulnerabilidades derivadas de la edad, discapacidad o situación socioeconómica[cite: 17].
*   Sistemas de "puntuación ciudadana" (social scoring) que evalúen o clasifiquen a personas dando lugar a un trato perjudicial injustificado o desproporcionado[cite: 17].
*   Evaluaciones de riesgo para predecir la comisión de delitos basándose únicamente en la elaboración de perfiles o rasgos de la personalidad[cite: 17].
*   Creación o ampliación de bases de datos de reconocimiento facial mediante extracción no selectiva (scraping) de imágenes de internet o circuitos cerrados de televisión (CCTV)[cite: 17].
*   Sistemas para inferir emociones en lugares de trabajo o centros educativos (salvo por motivos médicos o de seguridad)[cite: 17].
*   Categorización biométrica para deducir raza, opiniones políticas, afiliación sindical, religión o la orientación sexual[cite: 17].
*   Identificación biométrica remota "en tiempo real" en espacios de acceso público para fines de cumplimiento de la ley, salvo excepciones estrictamente tasadas (como la búsqueda de víctimas de secuestro o prevención de atentados terroristas), sujetas a autorización judicial o administrativa vinculante[cite: 17].

**B) Alto Riesgo (Sistemas de IA de alto riesgo - Art. 6)**
Un sistema de IA se clasifica como de alto riesgo si cumple alguna de estas condiciones[cite: 17]:
1.  Está destinado a utilizarse como componente de seguridad de un producto, o es en sí mismo un producto, regulado por la legislación de armonización de la Unión (ej. máquinas, productos sanitarios, juguetes, aviación) y requiere una evaluación de conformidad de terceros[cite: 17].
2.  Pertenece a los casos de uso enumerados en el Anexo III (ej. biometría, gestión de infraestructuras críticas, educación, empleo y gestión de trabajadores, acceso a servicios esenciales públicos y privados, cumplimiento de la ley, migración y administración de justicia)[cite: 17].
    *   *Excepción:* No se considerará de alto riesgo si el sistema realiza tareas procedimentales limitadas, mejora resultados de actividades humanas previas o detecta patrones sin sustituir la valoración humana, de modo que no influya sustancialmente en el resultado de la toma de decisiones[cite: 17]. No obstante, siempre será de alto riesgo si efectúa elaboración de perfiles de personas físicas[cite: 17].

**C) Riesgo Sistémico (Modelos de IA de uso general)**
Los modelos de IA de uso general (como los grandes modelos de lenguaje o LLM) pueden presentar "riesgos sistémicos" si poseen capacidades de gran impacto[cite: 17]. Se presume este riesgo cuando la cantidad acumulada de cálculo utilizado para el entrenamiento del modelo supera un umbral específico de operaciones de coma flotante (FLOPs)[cite: 17]. Estos modelos requieren evaluaciones rigurosas, simulación de adversarios (red-teaming) y políticas estrictas de ciberseguridad y mitigación de riesgos[cite: 17].

## 3. IA responsable: equidad, transparencia y explicabilidad.

Para mitigar los riesgos y garantizar la fiabilidad, los sistemas de IA de alto riesgo deben cumplir una serie de requisitos técnicos y organizativos esenciales[cite: 17].

**Transparencia y trazabilidad (Arts. 11 a 13)**
*   Los sistemas deben diseñarse de modo que su funcionamiento alcance un nivel de transparencia suficiente para que los responsables del despliegue interpreten y usen correctamente sus resultados de salida[cite: 17].
*   Deben estar provistos de instrucciones de uso claras, que detallen las capacidades, limitaciones, niveles de precisión, solidez técnica y medidas de mantenimiento[cite: 17].
*   Deben permitir el registro automático de acontecimientos (archivos de registro o logs) a lo largo de todo su ciclo de vida para garantizar la trazabilidad[cite: 17].
*   *Obligación general de transparencia:* Los sistemas diseñados para interactuar con personas físicas deben notificar al usuario que está interactuando con una IA[cite: 17]. Asimismo, el contenido generado o manipulado artificialmente (ultrasuplantaciones o deepfakes) debe marcarse en un formato legible por máquina indicando su origen artificial[cite: 17].

**Equidad y Gobernanza de Datos (Art. 10)**
*   Los conjuntos de datos de entrenamiento, validación y prueba deben someterse a prácticas de gobernanza adecuadas, examinando el origen de los datos, las operaciones de etiquetado y la formulación de supuestos[cite: 17].
*   Dichos conjuntos de datos deben ser pertinentes, representativos y, en la mayor medida posible, carecer de errores y estar completos[cite: 17].
*   Es obligatorio aplicar medidas para detectar, prevenir y mitigar posibles sesgos que puedan afectar negativamente a los derechos fundamentales o dar lugar a discriminación[cite: 17]. 
*   De forma excepcional, se permite el tratamiento de categorías especiales de datos personales si es estrictamente necesario para garantizar la detección y corrección de sesgos, aplicando medidas de seudonimización y seguridad punteras[cite: 17].

**Explicabilidad y Supervisión Humana (Art. 14)**
*   Los sistemas de IA de alto riesgo se diseñarán de tal forma que puedan ser vigilados de manera efectiva por personas físicas (incorporando herramientas de interfaz humano-máquina adecuadas)[cite: 17].
*   El objetivo de la supervisión humana es prevenir o minimizar los riesgos para la salud, la seguridad o los derechos fundamentales[cite: 17].
*   El responsable humano debe poder entender las capacidades del sistema, interpretar correctamente los resultados, ser consciente del riesgo de sesgo de automatización (exceso de confianza en la máquina) y tener la capacidad técnica para intervenir, descartar los resultados o detener el sistema de forma segura[cite: 17].
*   Para los sistemas de identificación biométrica (salvo excepciones en seguridad/cumplimiento de la ley), se exige que al menos dos personas físicas verifiquen y confirmen por separado los resultados antes de tomar decisiones[cite: 17].

## 4. Evaluación de impacto algorítmico.

La ejecución responsable de sistemas de IA en entornos reales exige identificar y atenuar preventivamente las externalidades negativas sobre los ciudadanos[cite: 17].

**Evaluación de impacto relativa a los derechos fundamentales (Art. 27)**
Antes de la puesta en funcionamiento de un sistema de IA de alto riesgo, determinados responsables del despliegue están obligados a llevar a cabo una evaluación de impacto relativa a los derechos fundamentales[cite: 17].
Están sujetos a esta obligación[cite: 17]:
*   Los organismos de Derecho público.
*   Las entidades privadas que presten servicios públicos.
*   Los responsables del despliegue de sistemas de IA de alto riesgo en sectores específicos, como las entidades bancarias o de seguros (evaluación de la calificación crediticia o evaluación de riesgos para seguros de vida y salud).

**Contenido de la evaluación**
La evaluación de impacto algorítmico y de derechos debe contemplar como mínimo[cite: 17]:
1.  Los procesos pertinentes en los que se utilizará el sistema, con arreglo a su finalidad prevista[cite: 17].
2.  El período de tiempo y la frecuencia con que se pretende utilizar[cite: 17].
3.  Las categorías concretas de personas físicas y colectivos que probablemente se vean afectados en ese contexto de uso específico[cite: 17].
4.  La determinación de los riesgos de perjuicio específicos que puedan afectar a los derechos fundamentales de dichas personas[cite: 17].
5.  Las medidas que han de adoptarse en caso de que se materialicen los riesgos, tales como sistemas de gobernanza, supervisión humana, y procedimientos de tramitación de reclamaciones y recursos[cite: 17].

El responsable del despliegue debe notificar los resultados de esta evaluación a la autoridad de vigilancia del mercado pertinente[cite: 17]. Si el sistema procesa datos personales, esta evaluación complementará a la Evaluación de Impacto en la Protección de Datos (EIPD) exigida por el RGPD.

## 5. Norma UNE-ISO/IEC 42001 (gestión de sistemas de IA).

Para dar cumplimiento a los estrictos requerimientos de gestión de calidad, análisis de riesgos y gobernanza exigidos por la legislación, las organizaciones se apoyan en los marcos de normalización técnica[cite: 17]. La normalización desempeña un papel fundamental para proporcionar soluciones técnicas a los proveedores y promover la competitividad[cite: 17].

El estándar internacional de referencia para las certificaciones oficiales en este ámbito es la norma **ISO/IEC 42001**, la cual especifica los requisitos para establecer, implementar, mantener y mejorar de forma continua un Sistema de Gestión de Inteligencia Artificial[cite: 1].

La adopción de este tipo de certificaciones basadas en estándares ISO/IEC como la ISO/IEC 42001 constituye un elemento objetivo para la demostración del cumplimiento normativo en relación con la gobernanza de la inteligencia artificial, la gestión de riesgos tecnológicos y la estructuración ética y auditable del ciclo de vida de los sistemas algorítmicos[cite: 1].
