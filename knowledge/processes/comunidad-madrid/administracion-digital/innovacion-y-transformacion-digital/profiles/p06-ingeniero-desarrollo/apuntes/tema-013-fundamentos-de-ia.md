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
  - "historia-de-la-ia"
  - "retropropagacion"
  - "gan"
  - "vae"
  - "modelos-de-difusion"
  - "model-context-protocol"
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

# Tema 13. Fundamentos de Inteligencia Artificial

## 1. Conceptos de IA, Machine Learning y Deep Learning.

**Antecedentes históricos y tipología de la IA**
El nacimiento formal de la Inteligencia Artificial como campo de estudio se sitúa en la **Conferencia de Dartmouth**, celebrada durante el verano de 1956 en Dartmouth College (Hanover, New Hampshire), organizada por John McCarthy junto con Marvin Minsky, Nathaniel Rochester y Claude Shannon. Fue el propio McCarthy quien acuñó el término *"Artificial Intelligence"* en la propuesta de financiación presentada a la Fundación Rockefeller, eligiendo deliberadamente un nombre neutro que evitase la vinculación exclusiva con la cibernética o la teoría de autómatas. Entre los participantes en el encuentro se encontraban también Allen Newell y Herbert Simon, quienes presentaron el *Logic Theorist*, considerado el primer programa de IA capaz de demostrar teoremas matemáticos mediante razonamiento heurístico. Unos años antes, en 1950, Alan Turing había planteado en su artículo *"Computing Machinery and Intelligence"* el conocido como **Test de Turing**, un criterio conductual para valorar si una máquina exhibe un comportamiento indistinguible del de un ser humano en una conversación.

Doctrinalmente se distingue entre tres niveles o tipos de IA según su alcance y capacidad:
*   **IA débil o estrecha (*Narrow AI*):** sistemas diseñados y entrenados para realizar una tarea concreta y acotada (traducción automática, reconocimiento de imágenes, recomendación de contenidos). Es el único tipo de IA existente en la actualidad de forma operativa.
*   **IA fuerte o general (*Artificial General Intelligence*, AGI):** hipotética inteligencia artificial capaz de igualar la capacidad cognitiva humana en cualquier tarea intelectual, con capacidad de transferir el aprendizaje entre dominios dispares.
*   **Superinteligencia artificial (*Artificial Superintelligence*, ASI):** hipotético estadio posterior en el que la capacidad de la máquina superaría a la inteligencia humana en la práctica totalidad de los dominios.

**Inteligencia Artificial (IA)**
El Reglamento (UE) 2024/1689 del Parlamento Europeo y del Consejo, de 13 de junio de 2024, por el que se establecen normas armonizadas en materia de inteligencia artificial (Reglamento de Inteligencia Artificial), define normativamente en su artículo 3, apartado 1, un **sistema de IA** como un sistema basado en una máquina que está diseñado para funcionar con distintos niveles de autonomía y que puede mostrar capacidad de adaptación tras el despliegue, y que, para objetivos explícitos o implícitos, infiere de la información de entrada que recibe la manera de generar resultados de salida, como predicciones, contenidos, recomendaciones o decisiones, que pueden influir en entornos físicos o virtuales. La capacidad de inferencia trasciende el tratamiento básico de datos, permitiendo el aprendizaje, el razonamiento o la modelización.

El propio Reglamento es de aplicación general en todos los Estados miembros de la Unión Europea desde su publicación en el Diario Oficial de la Unión Europea el 12 de julio de 2024, con una entrada en vigor escalonada por bloques de disposiciones: las prohibiciones del artículo 5 resultan aplicables desde el 2 de febrero de 2025, las obligaciones relativas a los modelos de IA de uso general desde el 2 de agosto de 2025, y el grueso de las obligaciones sobre sistemas de alto riesgo del Anexo III desde el 2 de agosto de 2026, mientras que determinados sistemas de alto riesgo vinculados a productos regulados por legislación de armonización de la Unión (Anexo I) disponen de un plazo adicional hasta el 2 de agosto de 2027.

**Machine Learning (Aprendizaje Automático)**
El Machine Learning es la rama funcional de la IA que engloba las estrategias metodológicas que aprenden de los datos cómo alcanzar determinados objetivos, sin necesidad de ser programadas explícitamente mediante reglas de negocio estáticas. Permite a los sistemas deducir modelos o algoritmos a partir de la información de entrada o los datos. Se fundamenta en la extracción de características (*feature extraction*) para la identificación de patrones.

**Deep Learning (Aprendizaje Profundo)**
Es una subdisciplina avanzada del Machine Learning basada en redes neuronales artificiales con múltiples capas ocultas (arquitecturas profundas). Estas redes están diseñadas para extraer progresivamente características de nivel superior a partir de los datos sin procesar, automatizando la extracción de características, siendo el estándar tecnológico en tareas complejas como la visión artificial y el procesamiento del lenguaje natural.

*   **Redes Neuronales Artificiales (RNA):** Estructuras computacionales inspiradas en el cerebro humano. Se componen de una capa de entrada (*input layer*), una o múltiples capas ocultas (*hidden layers*) y una capa de salida (*output layer*). Cada conexión entre neuronas posee un "peso" (*weight*) y un "sesgo" (*bias*) que se ajustan durante el entrenamiento.
*   **Funciones de activación:** Elementos matemáticos que introducen no linealidad en la red, permitiendo resolver problemas complejos. Las más utilizadas son ReLU (*Rectified Linear Unit*), Sigmoide y Tanh.
*   **Topologías comunes:**
    *   *Redes Neuronales Convolucionales (CNN):* Especializadas en el procesamiento de datos con topología de cuadrícula, como imágenes y video (visión artificial).
    *   *Redes Neuronales Recurrentes (RNN):* Diseñadas para el procesamiento de datos secuenciales o series temporales, como texto o audio. LSTM (*Long Short-Term Memory*) es una de sus variantes más estables.
*   **Mecanismo de entrenamiento: descenso de gradiente y retropropagación:** El ajuste de los pesos y sesgos de una red neuronal durante el entrenamiento se realiza mediante el algoritmo de **descenso de gradiente** (*Gradient Descent*), un método de optimización iterativo que actualiza los parámetros del modelo en la dirección que reduce el valor de la función de pérdida (*loss function*), que cuantifica el error entre la predicción del modelo y el valor real esperado. El cálculo del gradiente de dicha función respecto de cada peso de la red se obtiene mediante el algoritmo de **retropropagación** (*Backpropagation*), que propaga el error desde la capa de salida hacia las capas anteriores aplicando la regla de la cadena del cálculo diferencial. La magnitud del ajuste en cada iteración viene determinada por la **tasa de aprendizaje** (*learning rate*), un hiperparámetro cuya elección condiciona la velocidad y la estabilidad de la convergencia del entrenamiento.

## 2. Modelos supervisados y no supervisados.

El entrenamiento de los modelos algorítmicos se clasifica fundamentalmente en función de la estructura de los datos de entrada y la presencia o ausencia de variables objetivo (etiquetas).

**Modelos supervisados**
Utilizan conjuntos de datos de entrenamiento en los que la variable de salida u objetivo está explícitamente etiquetada o definida. El algoritmo aprende a establecer una función que mapea las características de entrada con la salida deseada, minimizando el error. Se dividen principalmente en:
*   **Clasificación:** Predicción de variables categóricas o clases discretas (ej. detección de fraude: sí/no; clasificación de correos: spam/no spam). Algoritmos de referencia: Regresión Logística, Máquinas de Vectores de Soporte (SVM), Árboles de Decisión, Random Forest, Naïve Bayes.
*   **Regresión:** Predicción de variables continuas o valores numéricos (ej. previsión de recaudación fiscal, estimación de demanda). Algoritmos de referencia: Regresión Lineal, Regresión Polinómica.

**Modelos no supervisados y otros enfoques**
En el aprendizaje no supervisado, el modelo infiere patrones, estructuras o agrupaciones inherentes a un conjunto de datos que carece de etiquetas previas. Las técnicas principales incluyen:
*   **Agrupamiento (*clustering*):** Agrupación de datos en clústeres en función de su similitud intrínseca (ej. segmentación de ciudadanos para servicios proactivos). Algoritmos de referencia: K-Means, DBSCAN, Clustering Jerárquico.
*   **Reducción de dimensionalidad:** Simplificación de los datos minimizando la pérdida de información, útil para la compresión o visualización. Algoritmo de referencia: Análisis de Componentes Principales (PCA).
*   **Reglas de asociación:** Descubrimiento de relaciones interesantes entre variables en grandes bases de datos (ej. algoritmo Apriori).

Adicionalmente, el estado del arte contempla técnicas como:
*   **Aprendizaje autosupervisado:** El modelo genera sus propias etiquetas a partir de la estructura de los datos de entrada (técnica clave en el entrenamiento de grandes modelos de lenguaje).
*   **Aprendizaje por refuerzo (Reinforcement Learning):** El modelo (agente) aprende a tomar secuencias de decisiones interactuando con un entorno, maximizando una señal de recompensa acumulada (ej. procesos de decisión de Markov, Q-Learning).

**Métricas de Evaluación y Problemas de Entrenamiento**
La evaluación del rendimiento de los modelos es crítica para garantizar su fiabilidad. En modelos de clasificación, se utiliza la **Matriz de Confusión**, que cruza las predicciones del modelo con los valores reales (Verdaderos Positivos, Verdaderos Negativos, Falsos Positivos, Falsos Negativos). De ella se derivan métricas como:
*   *Exactitud (Accuracy):* Proporción de predicciones correctas totales.
*   *Precisión (Precision):* Proporción de verdaderos positivos sobre el total de positivos predichos.
*   *Exhaustividad (Recall / Sensibilidad):* Proporción de verdaderos positivos sobre el total de positivos reales.
*   *F1-Score:* Media armónica entre Precisión y Exhaustividad.

Durante el entrenamiento, deben evitarse dos problemas fundamentales:
*   **Sobreajuste (Overfitting):** El modelo memoriza los datos de entrenamiento, perdiendo capacidad de generalización ante datos nuevos. Se mitiga mediante técnicas de regularización, *dropout* (en redes neuronales) o validación cruzada (*cross-validation*).
*   **Subajuste (Underfitting):** El modelo es demasiado simple para capturar los patrones subyacentes en los datos de entrenamiento.

## 3. IA generativa y modelos de lenguaje.

**IA Generativa**
La IA generativa comprende arquitecturas diseñadas para la generación flexible de contenidos, permitiendo producir elementos novedosos en formato de texto, audio, imágenes o vídeo, que pueden adaptarse fácilmente a una amplia gama de tareas diferenciadas. El desarrollo de estos modelos requiere acceder a grandes cantidades de datos y utilizar técnicas de prospección de textos y datos para la recuperación y el análisis de contenidos. La arquitectura tecnológica que ha revolucionado este campo es el **Transformer**, formulada en el artículo *"Attention Is All You Need"* (Vaswani et al., Google, 2017), basado en mecanismos de atención (*Self-Attention*), que permite procesar secuencias de datos en paralelo, capturando el contexto a largo plazo con alta eficiencia.

**Otras arquitecturas de modelos generativos**
Junto a los modelos basados en Transformer (propios de los grandes modelos de lenguaje), la generación de contenido sintético, en particular de imágenes, se apoya históricamente en otras familias de arquitecturas de aprendizaje profundo:
*   **Autocodificadores variacionales (VAE - *Variational Autoencoders*):** Arquitectura compuesta por un codificador, que comprime los datos de entrada en una representación latente de menor dimensión siguiendo una distribución de probabilidad, y un decodificador, que reconstruye los datos originales a partir de dicha representación latente. Permiten generar nuevas muestras variando el espacio latente, si bien tienden a producir resultados de menor nitidez que otras arquitecturas.
*   **Redes generativas antagónicas (GAN - *Generative Adversarial Networks*):** Arquitectura propuesta por Ian Goodfellow y otros en 2014, compuesta por dos redes neuronales entrenadas de forma simultánea y competitiva: un **generador**, que crea muestras sintéticas a partir de ruido aleatorio, y un **discriminador**, que trata de distinguir las muestras generadas artificialmente de las muestras reales del conjunto de entrenamiento. Ambas redes se entrenan conjuntamente como un juego de suma cero, de modo que el generador mejora progresivamente su capacidad de producir muestras indistinguibles de las reales.
*   **Modelos de difusión (*Diffusion Models*):** Arquitectura generativa que aprende a revertir progresivamente un proceso de adición controlada de ruido gaussiano a una imagen, de modo que, partiendo de ruido puro, el modelo aprende a "limpiar" la imagen paso a paso hasta reconstruir una muestra coherente. Constituyen en la actualidad el estado del arte en la generación de imágenes de alta fidelidad, siendo la arquitectura subyacente de herramientas como Stable Diffusion o DALL·E.

**Modelos de Lenguaje y Modelos de IA de Uso General**
Los grandes modelos de IA generativa (LLMs - *Large Language Models*) constituyen el ejemplo paradigmático de lo que el marco normativo define como **modelo de IA de uso general**. Un modelo de IA de uso general se caracteriza por:
*   Estar entrenado con un gran volumen de datos utilizando autosupervisión a gran escala.
*   Presentar un grado considerable de generalidad y ser capaz de realizar de manera competente una gran variedad de tareas distintas.
*   Ser capaz de integrarse en diversos sistemas o aplicaciones posteriores.

Estos modelos pueden plantear riesgos sistémicos derivados de sus capacidades de gran impacto, entendiéndose por estas las capacidades que igualan o superan las mostradas por los modelos más avanzados del mercado. La clasificación de riesgo sistémico atiende a métricas como la cantidad acumulada de cálculo utilizado para su entrenamiento (medida en operaciones de coma flotante o *FLOPS*).

**Técnicas de Adaptación de Modelos de Lenguaje**
Para aplicar un LLM generalista a un dominio específico (como el entorno normativo de una Administración Pública), existen dos enfoques principales:
*   **RAG (Retrieval-Augmented Generation / Generación Aumentada por Recuperación):** Combina el modelo de lenguaje con un sistema de recuperación de información externa. Antes de generar la respuesta, el sistema busca documentos relevantes en una base de conocimiento (generalmente vectorizada) y los inyecta en el *prompt*. Esto reduce drásticamente las "alucinaciones" y permite citar fuentes verificables sin necesidad de reentrenar el modelo.
*   **Fine-Tuning (Ajuste Fino):** Proceso de reentrenamiento de un modelo preentrenado utilizando un conjunto de datos específico del dominio para modificar sus pesos internos. Técnicas recientes como PEFT (*Parameter-Efficient Fine-Tuning*) o LoRA (*Low-Rank Adaptation*) permiten realizar este ajuste con un coste computacional significativamente reducido.

**Obligaciones de transparencia sobre interacción con sistemas de IA**
El artículo 50 del Reglamento (UE) 2024/1689 establece obligaciones específicas de transparencia para los proveedores y responsables del despliegue de determinados sistemas de IA, con independencia de si estos han sido calificados o no como de alto riesgo. En particular, los proveedores garantizarán que los sistemas de IA destinados a interactuar directamente con personas físicas se diseñen y desarrollen de forma que dichas personas estén informadas de que están interactuando con un sistema de IA, excepto cuando ello resulte evidente desde el punto de vista de una persona física razonablemente informada, atenta y perspicaz, teniendo en cuenta las circunstancias y el contexto de utilización. Asimismo, el artículo 50 impone obligaciones de etiquetado o marcado de los contenidos generados o manipulados por IA (por ejemplo, mediante marcas de agua técnicas), de forma que puedan detectarse como generados o manipulados artificialmente (*Deepfakes*).

## 4. IA agentica y automatización inteligente.

**IA Agéntica (Agentes Autónomos)**
La Inteligencia Artificial agéntica representa la evolución desde los modelos reactivos o de consulta directa hacia sistemas autónomos o "agentes" capaces de planificar tareas, utilizar herramientas externas, razonar secuencialmente y tomar acciones para cumplir objetivos complejos sin supervisión continua.

Un agente autónomo se compone arquitectónicamente de:
*   **Cerebro (Brain):** El LLM que actúa como motor de razonamiento, toma de decisiones y procesamiento de lenguaje natural.
*   **Memoria (Memory):** Capacidad de retener contexto. Se divide en memoria a corto plazo (historial de la conversación actual) y memoria a largo plazo (almacenamiento vectorial de interacciones pasadas para recuperación de contexto histórico).
*   **Planificación (Planning):** Habilidad para descomponer un objetivo complejo en sub-tareas manejables (técnicas como *Chain of Thought* o *Tree of Thoughts*) y capacidad de autorreflexión para corregir errores durante la ejecución. Una técnica de planificación especialmente extendida es el patrón **ReAct** (*Reasoning + Acting*), formulado en el artículo *"ReAct: Synergizing Reasoning and Acting in Language Models"* (Yao et al., 2022), que intercala explícitamente pasos de razonamiento en lenguaje natural con la ejecución de acciones concretas sobre el entorno, de modo que el resultado de cada acción retroalimenta el razonamiento del paso siguiente.
*   **Herramientas/Actuadores (Tools/Action):** Interfaces que permiten al agente interactuar con el entorno exterior, tales como ejecutar código, consultar APIs, buscar en internet o ejecutar consultas SQL en bases de datos. Para estandarizar esta conexión entre el agente y las herramientas o fuentes de datos externas se ha extendido el uso del **Protocolo de Contexto de Modelo (MCP - *Model Context Protocol*)**, un estándar abierto presentado por Anthropic en noviembre de 2024, que define una arquitectura cliente-servidor (host, cliente y servidor MCP) para que un mismo sistema de IA pueda conectarse, mediante una interfaz uniforme, a múltiples herramientas, API o bases de datos externas sin necesidad de desarrollar una integración específica para cada combinación de modelo y servicio.

La gestión técnica del ciclo de vida de este paradigma, englobando su desarrollo, monitorización y gobernanza corporativa, se articula en torno a metodologías avanzadas de operaciones como **AgentOps**, que complementan a las tradicionales MLOps y LLMOps.

**Automatización Inteligente (Hiperautomatización)**
La hiperautomatización es un enfoque sistemático para la rápida identificación y automatización del máximo número posible de procesos de negocio y de TI. Involucra la orquestación estructurada de múltiples tecnologías convergentes:
*   **RPA (Robotic Process Automation):** Automatización basada en reglas para tareas repetitivas y estructuradas a nivel de interfaz de usuario (UI).
*   **BPM (Business Process Management):** Gestión y orquestación integral del flujo de trabajo organizativo.
*   **IA / Automatización Cognitiva:** Integración de OCR inteligente, procesamiento de lenguaje natural y machine learning para abordar procesos no estructurados, excepciones complejas y toma de decisiones probabilísticas.

Este enfoque modular permite brindar servicios públicos de manera eficiente y conectada, yendo más allá de la mera automatización de tareas aisladas y facilitando la transición hacia arquitecturas orientadas a eventos e impulsadas por datos.

## 5. Aplicaciones de la IA en organizaciones.

**Enfoque piramidal de riesgo del Reglamento (UE) 2024/1689**
El Reglamento de Inteligencia Artificial articula su régimen de obligaciones conforme a un enfoque basado en el riesgo, estructurado en cuatro niveles jerárquicos:

*   **Riesgo inaceptable:** Prácticas de IA íntegramente prohibidas por el artículo 5 del Reglamento, por resultar especialmente perjudiciales y abusivas, contrarias a los valores de la Unión y vulneradoras de derechos fundamentales. Entre ellas se incluyen:
    *   Técnicas subliminales manipuladoras que alteren sustancialmente el comportamiento humano causando perjuicios.
    *   Explotación de vulnerabilidades de personas por edad, discapacidad o situación social/económica.
    *   Sistemas de categorización biométrica que deduzcan origen racial, opiniones políticas, afiliación sindical, convicciones religiosas o filosóficas, u orientación sexual.
    *   Sistemas de "puntuación social" (*social scoring*) realizados por autoridades públicas o privadas que den lugar a un trato perjudicial injustificado.
    *   Uso de sistemas de identificación biométrica remota en tiempo real en espacios de acceso público con fines de garantía del cumplimiento del Derecho (con excepciones muy estrictas y tasadas, como la búsqueda de personas desaparecidas o la prevención de amenazas terroristas inminentes, previa autorización judicial).
*   **Alto riesgo:** Sistemas sujetos al conjunto más exigente de obligaciones, regulados en el Capítulo III. Exigen la implementación de un sistema de gestión de riesgos, gobernanza de datos, documentación técnica exhaustiva, registro automático de actividad (*logs*), transparencia, supervisión humana (interfaz humano-máquina), precisión, solidez y ciberseguridad. Requieren un procedimiento de **evaluación de la conformidad** y la colocación del **marcado CE** previo a su introducción en el mercado.
*   **Riesgo limitado:** Sistemas sujetos a obligaciones específicas de transparencia (artículo 50), como los chatbots o los sistemas generadores de contenido sintético (*deepfakes*).
*   **Riesgo mínimo o nulo:** El resto de sistemas de IA (ej. filtros de spam, videojuegos), no sujetos a obligaciones específicas más allá de la recomendación de adherirse a códigos de conducta voluntarios.

**Reglas de clasificación de los sistemas de alto riesgo (artículo 6 y Anexo III)**
Según el artículo 6 del Reglamento, un sistema de IA se clasifica como de alto riesgo por una de estas dos vías:
a) Si el sistema de IA es en sí mismo un producto, o un componente de seguridad de un producto, cubierto por la legislación de armonización de la Unión enumerada en el Anexo I, y debe someterse a una evaluación de conformidad por terceros.
b) Si el sistema de IA se encuadra en alguno de los ámbitos de uso enumerados en el Anexo III del Reglamento:
*   **Biometría:** Sistemas de identificación biométrica remota y reconocimiento de emociones.
*   **Gestión y funcionamiento de infraestructuras críticas:** Componentes de seguridad en el tráfico rodado, suministro de agua, gas, calefacción o electricidad.
*   **Educación y formación profesional:** Sistemas destinados a determinar el acceso, admisión o evaluación de estudiantes.
*   **Empleo, gestión de trabajadores y acceso al autoempleo:** Sistemas para la contratación, filtrado de solicitudes, decisiones sobre promoción, extinción contractual o evaluación del rendimiento.
*   **Acceso a servicios privados esenciales y a servicios y prestaciones públicos esenciales:** Sistemas para evaluar la elegibilidad para prestaciones de asistencia pública, calificación crediticia o clasificación de llamadas de emergencia/triaje de pacientes.
*   **Garantía del cumplimiento del Derecho:** Sistemas para evaluación de fiabilidad de pruebas, riesgo de reincidencia o polígrafos.
*   **Migración, asilo y gestión del control fronterizo:** Sistemas para evaluación de riesgos en solicitudes de visado o asilo.
*   **Administración de justicia y procesos democráticos:** Sistemas para ayudar a investigar e interpretar hechos y aplicar la ley, o sistemas para influir en resultados electorales.

Existen excepciones (artículo 6.3) si el sistema de IA realiza únicamente una tarea procedimental limitada o preparatoria, mejora el resultado de una actividad humana ya realizada o detecta desviaciones sin influir en la evaluación humana. No obstante, **siempre** será de alto riesgo si elabora perfiles de personas físicas.

**Gobernanza y Espacios Controlados de Pruebas (Sandboxes)**
Para fomentar el cumplimiento y la innovación segura, el Reglamento prevé la creación de un marco de gobernanza a nivel europeo y nacional:
*   **Oficina Europea de Inteligencia Artificial (AI Office):** Establecida en el seno de la Comisión Europea. Sus funciones incluyen la supervisión de los modelos de IA de uso general (GPAI), la promoción de códigos de buenas prácticas y la contribución a la aplicación uniforme del Reglamento.
*   **Agencia Española de Supervisión de la Inteligencia Artificial (AESIA):** Adscrita al Ministerio para la Transformación Digital y de la Función Pública. Es la autoridad nacional competente en España encargada de la supervisión, concienciación y ejecución del Reglamento de IA.
*   **Espacios Controlados de Pruebas (AI Regulatory Sandboxes):** El Capítulo V del Reglamento obliga a los Estados miembros a establecer al menos un espacio controlado de pruebas para la IA a nivel nacional. Estos *sandboxes* proporcionan un entorno controlado para el desarrollo, entrenamiento, validación y prueba de sistemas de IA innovadores bajo supervisión regulatoria directa, antes de su introducción en el mercado. Su objetivo es facilitar la innovación, reducir los obstáculos de acceso al mercado para las PYMES y asegurar la conformidad normativa temprana (*compliance by design*).

**Aplicaciones Operativas y de Transformación en la Administración Digital**
En el marco estratégico de la modernización de la Administración Pública, la IA actúa como palanca tecnológica para la transición hacia un modelo de gestión inteligente y proactiva:
*   **Servicios Cognitivos y Hub Analítico:** Despliegue de plataformas de análisis masivo de datos con retroalimentación en tiempo real. Estas arquitecturas están orientadas a identificar patrones y ejecutar modelos predictivos que permitan anticipar las necesidades de la ciudadanía y personalizar la prestación de los servicios públicos.
*   **Tratamiento de información no estructurada:** Automatización de procesos administrativos mediante algoritmos de inteligencia artificial, optimizando la búsqueda, clasificación y extracción de datos en repositorios de información no estructurada (documentos escaneados, imágenes y vídeos).
*   **Ciberseguridad y Centros de Operaciones (SOC):** Integración de IA en la cibervigilancia para la detección temprana de amenazas persistentes avanzadas (APT). El uso de IA permite el análisis dinámico de grandes volúmenes de eventos de seguridad y la ejecución de respuestas automatizadas de prevención y contención frente a incidentes.

## Referencias normativas y técnicas

*   Reglamento (UE) 2024/1689 del Parlamento Europeo y del Consejo, de 13 de junio de 2024, por el que se establecen normas armonizadas en materia de inteligencia artificial (Reglamento de Inteligencia Artificial), publicado en el Diario Oficial de la Unión Europea el 12 de julio de 2024 (artículos 3, 5, 6, 50 y Anexo III).
*   Turing, A. M., *"Computing Machinery and Intelligence"*, Mind, 1950.
*   McCarthy, J., Minsky, M., Rochester, N. y Shannon, C., propuesta de la Conferencia de Dartmouth (Dartmouth Summer Research Project on Artificial Intelligence), 1956.
*   Vaswani, A. et al., *"Attention Is All You Need"*, Google, NeurIPS 2017 (arXiv:1706.03762).
*   Goodfellow, I. et al., *"Generative Adversarial Networks"*, 2014 (arXiv:1406.2661).
*   Yao, S. et al., *"ReAct: Synergizing Reasoning and Acting in Language Models"*, 2022 (arXiv:2210.03629).
*   Anthropic, *"Introducing the Model Context Protocol"*, noviembre de 2024.
