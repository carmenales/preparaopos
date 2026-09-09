---
id: "cm-ad-innovacion-y-transformacion-digital-tema-013-tema-013-fundamentos-de-ia"
title: "Fundamentos de Inteligencia Artificial"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/innovacion-y-transformacion-digital"
profiles:
  - "p06-ingeniero-desarrollo"
official_profiles:
  - "P06 - Ingeniero de Desarrollo"
official_topic: "Tema 13. Fundamentos de Inteligencia Artificial"
source_ids: []
tags:
  - "ia"
  - "ia-agentica"
  - "ia-generativa"
  - "inteligencia-artificial"
  - "ml"
  - "machine-learning"
  - "deep-learning"
  - "modelo-supervisado"
  - "modelo-no-supervisado"
  - "modelo-de-lenguaje"
  - "automatizacion-inteligente"
  - "aplicaciones-ia"
  - "reglamento-ia"
  - "ai-act"
created_at: "2026-09-03"
last_reviewed: "2026-09-09"
ai_generated: true
ai_sources:
  - "perplexity"
  - "chatgpt"
  - "gemini"
needs_human_review: true
---

# Tema 13. Fundamentos de Inteligencia Artificial

## 1. Conceptos de IA, Machine Learning y Deep Learning.

**Inteligencia Artificial (IA)**
El Reglamento (UE) 2024/1689 del Parlamento Europeo y del Consejo, de 13 de junio de 2024, por el que se establecen normas armonizadas en materia de inteligencia artificial (Reglamento de Inteligencia Artificial), define normativamente en su artículo 3, apartado 1, un **sistema de IA** como un sistema basado en una máquina que está diseñado para funcionar con distintos niveles de autonomía y que puede mostrar capacidad de adaptación tras el despliegue, y que, para objetivos explícitos o implícitos, infiere de la información de entrada que recibe la manera de generar resultados de salida, como predicciones, contenidos, recomendaciones o decisiones, que pueden influir en entornos físicos o virtuales. La capacidad de inferencia trasciende el tratamiento básico de datos, permitiendo el aprendizaje, el razonamiento o la modelización.

El propio Reglamento es de aplicación general en todos los Estados miembros de la Unión Europea desde su publicación en el Diario Oficial de la Unión Europea el 12 de julio de 2024, con una entrada en vigor escalonada por bloques de disposiciones: las prohibiciones del artículo 5 resultan aplicables desde el 2 de febrero de 2025, las obligaciones relativas a los modelos de IA de uso general desde el 2 de agosto de 2025, y el grueso de las obligaciones sobre sistemas de alto riesgo del Anexo III desde el 2 de agosto de 2026, mientras que determinados sistemas de alto riesgo vinculados a productos regulados por legislación de armonización de la Unión (Anexo I) disponen de un plazo adicional hasta el 2 de agosto de 2027.

**Machine Learning (Aprendizaje Automático)**
El Machine Learning es la rama funcional de la IA que engloba las estrategias metodológicas que aprenden de los datos cómo alcanzar determinados objetivos, sin necesidad de ser programadas explícitamente mediante reglas de negocio estáticas. Permite a los sistemas deducir modelos o algoritmos a partir de la información de entrada o los datos.

**Deep Learning (Aprendizaje Profundo)**
Es una subdisciplina avanzada del Machine Learning basada en redes neuronales artificiales con múltiples capas ocultas (arquitecturas profundas). Estas redes están diseñadas para extraer progresivamente características de nivel superior a partir de los datos sin procesar, siendo el estándar tecnológico en tareas complejas como la visión artificial y el procesamiento del lenguaje natural.

## 2. Modelos supervisados y no supervisados.

El entrenamiento de los modelos algorítmicos se clasifica fundamentalmente en función de la estructura de los datos de entrada y la presencia o ausencia de variables objetivo (etiquetas).

**Modelos supervisados**
Utilizan conjuntos de datos de entrenamiento en los que la variable de salida u objetivo está explícitamente etiquetada o definida. El algoritmo aprende a establecer una función que mapea las características de entrada con la salida deseada, minimizando el error. Se dividen principalmente en:
*   **Clasificación:** Predicción de variables categóricas o clases discretas.
*   **Regresión:** Predicción de variables continuas o valores numéricos.

**Modelos no supervisados y otros enfoques**
En el aprendizaje no supervisado, el modelo infiere patrones, estructuras o agrupaciones inherentes a un conjunto de datos que carece de etiquetas previas. Las técnicas principales incluyen el agrupamiento (*clustering*), la reducción de dimensionalidad y la detección de anomalías.
Adicionalmente, el estado del arte contempla técnicas como el **aprendizaje autosupervisado** y el **aprendizaje por refuerzo**, métodos recurrentemente utilizados en el entrenamiento a gran escala de modelos fundacionales que procesan grandes volúmenes de datos.

## 3. IA generativa y modelos de lenguaje.

**IA Generativa**
La IA generativa comprende arquitecturas diseñadas para la generación flexible de contenidos, permitiendo producir elementos novedosos en formato de texto, audio, imágenes o vídeo, que pueden adaptarse fácilmente a una amplia gama de tareas diferenciadas. El desarrollo de estos modelos requiere acceder a grandes cantidades de datos y utilizar técnicas de prospección de textos y datos para la recuperación y el análisis de contenidos.

**Modelos de Lenguaje y Modelos de IA de Uso General**
Los grandes modelos de IA generativa (LLMs - *Large Language Models*) constituyen el ejemplo paradigmático de lo que el marco normativo define como **modelo de IA de uso general**. Un modelo de IA de uso general se caracteriza por:
*   Estar entrenado con un gran volumen de datos utilizando autosupervisión a gran escala.
*   Presentar un grado considerable de generalidad y ser capaz de realizar de manera competente una gran variedad de tareas distintas.
*   Ser capaz de integrarse en diversos sistemas o aplicaciones posteriores.

Estos modelos pueden plantear riesgos sistémicos derivados de sus capacidades de gran impacto, entendiéndose por estas las capacidades que igualan o superan las mostradas por los modelos más avanzados del mercado.

**Obligaciones de transparencia sobre interacción con sistemas de IA**
El artículo 50 del Reglamento (UE) 2024/1689 establece obligaciones específicas de transparencia para los proveedores y responsables del despliegue de determinados sistemas de IA, con independencia de si estos han sido calificados o no como de alto riesgo. En particular, los proveedores garantizarán que los sistemas de IA destinados a interactuar directamente con personas físicas se diseñen y desarrollen de forma que dichas personas estén informadas de que están interactuando con un sistema de IA, excepto cuando ello resulte evidente desde el punto de vista de una persona física razonablemente informada, atenta y perspicaz, teniendo en cuenta las circunstancias y el contexto de utilización. Asimismo, el artículo 50 impone obligaciones de etiquetado o marcado de los contenidos generados o manipulados por IA (por ejemplo, mediante marcas de agua técnicas), de forma que puedan detectarse como generados o manipulados artificialmente.

## 4. IA agentica y automatización inteligente.

**IA Agéntica (Agentes Autónomos)**
La Inteligencia Artificial agéntica representa la evolución desde los modelos reactivos o de consulta directa hacia sistemas autónomos o "agentes" capaces de planificar tareas, utilizar herramientas externas, razonar secuencialmente y tomar acciones para cumplir objetivos complejos sin supervisión continua. La gestión técnica del ciclo de vida de este paradigma, englobando su desarrollo, monitorización y gobernanza corporativa, se articula en torno a metodologías avanzadas de operaciones como **AgentOps**, que complementan a las tradicionales MLOps y LLMOps.

**Automatización Inteligente (Hiperautomatización)**
La hiperautomatización es un enfoque sistemático para la rápida identificación y automatización del máximo número posible de procesos de negocio y de TI. Involucra la orquestación estructurada de múltiples tecnologías, fundamentalmente la Inteligencia Artificial y la automatización robótica de procesos (RPA). Este enfoque modular permite brindar servicios públicos de manera eficiente y conectada, yendo más allá de la mera automatización de tareas aisladas.

## 5. Aplicaciones de la IA en organizaciones.

**Enfoque piramidal de riesgo del Reglamento (UE) 2024/1689**
El Reglamento de Inteligencia Artificial articula su régimen de obligaciones conforme a un enfoque basado en el riesgo, estructurado en cuatro niveles jerárquicos:

*   **Riesgo inaceptable:** prácticas de IA íntegramente prohibidas por el artículo 5 del Reglamento, por resultar especialmente perjudiciales y abusivas, contrarias a los valores de la Unión y vulneradoras de derechos fundamentales. Entre ellas se incluyen, literalmente: la introducción en el mercado, puesta en servicio o utilización de un sistema de IA que se sirva de técnicas subliminales que trasciendan la conciencia de una persona, o de técnicas deliberadamente manipuladoras o engañosas, con el objetivo o el efecto de alterar de manera sustancial el comportamiento de una persona o un colectivo, mermando su capacidad de tomar una decisión informada y provocando o siendo razonablemente probable que provoque perjuicios considerables; y la explotación de vulnerabilidades de una persona o colectivo derivadas de su edad, discapacidad o situación social o económica específica, con la finalidad o el efecto de alterar sustancialmente su comportamiento de un modo que provoque o sea razonablemente probable que provoque perjuicios considerables.
*   **Alto riesgo:** sistemas sujetos al conjunto más exigente de obligaciones (evaluación de conformidad, supervisión humana, gestión de riesgos, calidad de los datos, documentación técnica y registro), regulados en el Capítulo III del Reglamento.
*   **Riesgo limitado:** sistemas sujetos a obligaciones específicas de transparencia (artículo 50), como los chatbots o los sistemas generadores de contenido sintético (deepfakes).
*   **Riesgo mínimo o nulo:** el resto de sistemas de IA, no sujetos a obligaciones específicas más allá de códigos de conducta voluntarios.

**Reglas de clasificación de los sistemas de alto riesgo (artículo 6 y Anexo III)**
Según el artículo 6 del Reglamento, un sistema de IA se clasifica como de alto riesgo por una de estas dos vías: a) si el propio sistema de IA es en sí mismo un producto, o un componente de seguridad de un producto, cubierto por la legislación de armonización de la Unión enumerada en el Anexo I, y dicho producto debe someterse a una evaluación de conformidad por terceros con arreglo a esa legislación; o b) si el sistema de IA se encuadra en alguno de los ámbitos de uso enumerados en el Anexo III del Reglamento. En este segundo supuesto, el Anexo III recoge, entre otros, los siguientes ámbitos:

*   **Biometría** (en la medida en que su uso esté permitido por el Derecho de la Unión o nacional aplicable): sistemas de identificación biométrica remota, de categorización biométrica según atributos o características sensibles o protegidas, o de reconocimiento de emociones.
*   **Gestión y funcionamiento de infraestructuras críticas:** sistemas destinados a utilizarse como componentes de seguridad en la gestión y el funcionamiento de infraestructuras digitales críticas, del tráfico rodado o del suministro de agua, gas, calefacción o electricidad.
*   **Educación y formación profesional:** sistemas destinados a determinar el acceso o la admisión, o a asignar personas a instituciones educativas y de formación profesional en todos los niveles; a evaluar los resultados del aprendizaje; a evaluar el nivel de educación adecuado que una persona recibirá; o a supervisar y detectar comportamientos prohibidos durante las pruebas.
*   **Empleo, gestión de trabajadores y acceso al autoempleo:** sistemas destinados a utilizarse para la contratación o selección de personas físicas, en particular para publicar anuncios de empleo específicos, analizar y filtrar solicitudes de empleo y evaluar a los candidatos; y para adoptar decisiones que afecten a las condiciones de las relaciones laborales, la promoción o la extinción de las relaciones contractuales, para asignar tareas basándose en el comportamiento individual o los rasgos o características personales, o para supervisar y evaluar el rendimiento y la conducta de las personas en dichas relaciones.
*   **Acceso a servicios privados esenciales y a servicios y prestaciones públicos esenciales:** sistemas destinados a evaluar la elegibilidad de personas físicas para prestaciones y servicios de asistencia pública esenciales, así como para conceder, reducir, revocar o reclamar tales prestaciones y servicios; para evaluar la solvencia crediticia o establecer su solvencia; y para la evaluación y clasificación de las llamadas de emergencia o para su empleo con el fin de establecer la prioridad en el envío de los servicios de primera intervención, incluidos los cuerpos de policía y bomberos y la asistencia médica de urgencia, así como de sistemas de clasificación de pacientes de urgencia.
*   **Garantía del cumplimiento del Derecho:** en la medida en que su uso esté permitido, sistemas destinados a que las autoridades policiales los utilicen o en su nombre, entre otros, para evaluar el riesgo de que una persona física se convierta en víctima de infracciones penales, como polígrafos o herramientas similares, para evaluar la fiabilidad de las pruebas, o para evaluar el riesgo de que una persona física delinca o reincida.
*   **Migración, asilo y gestión del control fronterizo:** sistemas utilizados por las autoridades públicas competentes como polígrafos, para evaluar riesgos, tramitar solicitudes de asilo, visado o permiso de residencia, o con fines de detección, reconocimiento o identificación de personas físicas.
*   **Administración de justicia y procesos democráticos:** sistemas destinados a ser utilizados por una autoridad judicial o en su nombre para ayudar a dicha autoridad a investigar e interpretar los hechos y el Derecho y a aplicar la ley a unos hechos concretos, o para ser utilizados de forma similar en métodos alternativos de resolución de litigios; así como sistemas destinados a ser utilizados para influir en el resultado de una elección o referéndum o en el comportamiento electoral de las personas físicas en el ejercicio de su voto.

El propio artículo 6, apartado 3, establece excepciones a esta clasificación como alto riesgo, aun encuadrándose en los ámbitos del Anexo III, cuando el sistema de IA realice únicamente una tarea procedimental limitada, mejore el resultado de una actividad humana ya realizada, detecte patrones de toma de decisiones o desviaciones respecto de patrones anteriores sin pretender sustituir o influir en la evaluación humana previa sin revisión adecuada, o realice una tarea preparatoria de una evaluación pertinente. No obstante, estos sistemas se considerarán siempre de alto riesgo, sin excepción, cuando elaboren perfiles de personas físicas, entendiendo por tal el tratamiento automatizado de datos personales para evaluar diversos aspectos de la vida de una persona, como su rendimiento en el trabajo, su situación económica, salud, preferencias personales, intereses, fiabilidad, comportamiento, ubicación o desplazamientos.

En España, la autoridad nacional de supervisión y aplicación del Reglamento es la **Agencia Española de Supervisión de la Inteligencia Artificial (AESIA)**, adscrita al Ministerio para la Transformación Digital y de la Función Pública.

**Aplicaciones Operativas y de Transformación en la Administración Digital**
En el marco estratégico de la modernización de la Administración Pública, la IA actúa como palanca tecnológica para la transición hacia un modelo de gestión inteligente y proactiva:
*   **Servicios Cognitivos y Hub Analítico:** Despliegue de plataformas de análisis masivo de datos con retroalimentación en tiempo real. Estas arquitecturas están orientadas a identificar patrones y ejecutar modelos predictivos que permitan anticipar las necesidades de la ciudadanía y personalizar la prestación de los servicios públicos.
*   **Tratamiento de información no estructurada:** Automatización de procesos administrativos mediante algoritmos de inteligencia artificial, optimizando la búsqueda, clasificación y extracción de datos en repositorios de información no estructurada (documentos escaneados, imágenes y vídeos).
*   **Ciberseguridad y Centros de Operaciones (SOC):** Integración de IA en la cibervigilancia para la detección temprana de amenazas persistentes avanzadas (APT). El uso de IA permite el análisis dinámico de grandes volúmenes de eventos de seguridad y la ejecución de respuestas automatizadas de prevención y contención frente a incidentes.

## Referencias normativas

*   Reglamento (UE) 2024/1689 del Parlamento Europeo y del Consejo, de 13 de junio de 2024, por el que se establecen normas armonizadas en materia de inteligencia artificial (Reglamento de Inteligencia Artificial), publicado en el Diario Oficial de la Unión Europea el 12 de julio de 2024 (artículos 3, 5, 6, 50 y Anexo III).
