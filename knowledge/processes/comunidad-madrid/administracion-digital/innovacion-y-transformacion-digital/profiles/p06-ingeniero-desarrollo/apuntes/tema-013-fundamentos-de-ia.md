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
El Reglamento (UE) 2024/1689 define normativamente un sistema de IA como un sistema basado en una máquina que está diseñado para funcionar con distintos niveles de autonomía y que puede mostrar capacidad de adaptación tras el despliegue, y que, para objetivos explícitos o implícitos, infiere de la información de entrada que recibe la manera de generar resultados de salida, como predicciones, contenidos, recomendaciones o decisiones, que pueden influir en entornos físicos o virtuales. La capacidad de inferencia trasciende el tratamiento básico de datos, permitiendo el aprendizaje, el razonamiento o la modelización.

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

## 4. IA agentica y automatización inteligente.

**IA Agéntica (Agentes Autónomos)**
La Inteligencia Artificial agéntica representa la evolución desde los modelos reactivos o de consulta directa hacia sistemas autónomos o "agentes" capaces de planificar tareas, utilizar herramientas externas, razonar secuencialmente y tomar acciones para cumplir objetivos complejos sin supervisión continua. La gestión técnica del ciclo de vida de este paradigma, englobando su desarrollo, monitorización y gobernanza corporativa, se articula en torno a metodologías avanzadas de operaciones como **AgentOps**, que complementan a las tradicionales MLOps y LLMOps.

**Automatización Inteligente (Hiperautomatización)**
La hiperautomatización es un enfoque sistemático para la rápida identificación y automatización del máximo número posible de procesos de negocio y de TI. Involucra la orquestación estructurada de múltiples tecnologías, fundamentalmente la Inteligencia Artificial y la automatización robótica de procesos (RPA). Este enfoque modular permite brindar servicios públicos de manera eficiente y conectada, yendo más allá de la mera automatización de tareas aisladas.

## 5. Aplicaciones de la IA en organizaciones.

**Aplicaciones de Alto Riesgo en el Sector Público y Privado (Reglamento UE 2024/1689)**
El despliegue de sistemas de Inteligencia Artificial en las organizaciones se clasifica normativamente en función de su criticidad. Las aplicaciones categorizadas como de alto riesgo, que exigen un estricto cumplimiento normativo, evaluación de conformidad y supervisión humana, incluyen:
*   **Gestión de infraestructuras críticas:** Sistemas destinados a utilizarse como componentes de seguridad en la gestión de infraestructuras digitales, tráfico rodado y suministro de agua, gas, calefacción y electricidad, cuyo fallo suponga un riesgo para la vida, la salud o la actividad económica.
*   **Empleo y gestión de trabajadores:** Sistemas utilizados para la contratación y selección de personal, la toma de decisiones sobre la promoción o rescisión de contratos, la asignación de tareas basada en el comportamiento y la supervisión del rendimiento de los empleados.
*   **Educación y formación profesional:** Sistemas orientados a determinar el acceso a instituciones educativas, evaluar los resultados del aprendizaje o supervisar comportamientos durante la realización de pruebas.
*   **Acceso a servicios esenciales:** Sistemas que evalúan la concesión, reducción o revocación de prestaciones de asistencia pública (servicios sociales, sanitarios, vivienda), así como los utilizados para la evaluación de la solvencia crediticia y el triaje y priorización en servicios de asistencia médica de emergencia.
*   **Garantía del cumplimiento del Derecho y Administración de Justicia:** Herramientas de evaluación de fiabilidad de pruebas, análisis de riesgos (siempre que no se basen en el perfilado exclusivo de personalidad) y sistemas de apoyo a la investigación e interpretación de hechos y leyes por parte de autoridades judiciales.

**Aplicaciones Operativas y de Transformación en la Administración Digital**
En el marco estratégico de la modernización de la Administración Pública, la IA actúa como palanca tecnológica para la transición hacia un modelo de gestión inteligente y proactiva:
*   **Servicios Cognitivos y Hub Analítico:** Despliegue de plataformas de análisis masivo de datos con retroalimentación en tiempo real. Estas arquitecturas están orientadas a identificar patrones y ejecutar modelos predictivos que permitan anticipar las necesidades de la ciudadanía y personalizar la prestación de los servicios públicos.
*   **Tratamiento de información no estructurada:** Automatización de procesos administrativos mediante algoritmos de inteligencia artificial, optimizando la búsqueda, clasificación y extracción de datos en repositorios de información no estructurada (documentos escaneados, imágenes y vídeos).
*   **Ciberseguridad y Centros de Operaciones (SOC):** Integración de IA en la cibervigilancia para la detección temprana de amenazas persistentes avanzadas (APT). El uso de IA permite el análisis dinámico de grandes volúmenes de eventos de seguridad y la ejecución de respuestas automatizadas de prevención y contención frente a incidentes.