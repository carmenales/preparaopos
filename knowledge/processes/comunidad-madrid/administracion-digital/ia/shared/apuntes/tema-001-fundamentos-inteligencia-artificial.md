---
id: "cm-ad-ia-tema-001-fundamentos-inteligencia-artificial"
title: "Fundamentos de Inteligencia Artificial"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/ia"
profiles:
  - "p01-consultor-sistemas-informacion-ia"
  - "p02-consultor-sistemas-informacion-gobierno-ia"
official_profiles:
  - "P01 - Consultor de Sistemas de Información - IA Aplicada al Ciclo de Vida del Software"
  - "P02 - Consultor de Sistemas de Información - Gobierno de IA"
official_topic: "Tema 1. Fundamentos de Inteligencia Artificial"
source_ids:
tags:
  - "inteligencia-artificial"
  - "machine-learning"
  - "deep-learning"
  - "pln"
  - "mlops"
  - "gobierno-ia"
  - "ai-act"
  - "iso-iec-22989"
created_at: "2026-07-17"
last_reviewed: null
ai_generated: true
ai_sources:
  - "chatgpt"
  - "perplexity"
  - "gemini"
needs_human_review: true
---

# Fundamentos de Inteligencia Artificial

## Encaje en la convocatoria

Este tema corresponde al **Tema 1 del Anexo 3** de la Resolución 352/2026 (BOCM 11/06/2026), dentro de las áreas de conocimiento objeto de la Fase 1 de oposición, común a los perfiles **P01: Consultor de Sistemas de Información - IA Aplicada al Ciclo de Vida del Software** y **P02: Consultor de Sistemas de Información - Especialista en Gobierno de IA** de la Agencia para la Administración Digital de la Comunidad de Madrid.

El contenido base (conceptos de IA, ML, DL, PLN y MLOps) es común a ambos perfiles, pero el enfoque de estudio difiere. Para el perfil **P01**, el examinador puede evaluar aspectos más técnicos de implementación y ciclo de vida del software. Para el perfil **P02**, el enfoque se traslada a **cómo auditar el sistema, gobernar sus datos, trazar su linaje, controlar sus sesgos y encuadrarlo en el marco regulatorio**.

En ambos casos, la prueba exige diferenciar con precisión la terminología normativa (Reglamento (UE) 2024/1689 de la IA), los estándares técnicos internacionales (ISO/IEC 22989:2022) y los marcos de gestión de riesgos institucionales (NIST AI RMF 1.0). Es crítico dominar la diferencia entre la degradación de los datos (*Data Drift*) y la del concepto (*Concept Drift*), así como entender MLOps como el marco operativo y de control auditable necesario para cumplir con la legislación.

## Ideas clave

1. **Inteligencia Artificial (IA)** es el campo general orientado a construir sistemas capaces de percibir, razonar, aprender y actuar.
2. **Definición Normativa de IA (Reglamento UE 2024/1689, Art. 3.1):** Un sistema basado en una máquina, diseñado para funcionar con distintos niveles de autonomía, que puede mostrar capacidad de adaptación tras el despliegue y que **infiere** de la información de entrada la manera de generar resultados (predicciones, contenidos, recomendaciones o decisiones) que pueden influir en entornos físicos o virtuales.
3. **Jerarquía Técnica y Normativa (ISO/IEC 22989:2022):** Estándar internacional de terminología. Establece que la IA es el dominio principal, el **Machine Learning (ML)** es una de sus disciplinas, y el **Deep Learning (DL)** es una técnica dentro del ML basada en redes neuronales profundas.
4. **Machine Learning (ML)** es un subcampo de la IA donde el sistema aprende de los datos sin programación explícita de reglas. Se caracteriza por requerir la **extracción manual de características (Feature Engineering)** por parte de expertos.
5. **Deep Learning (DL)** es un subcampo del ML basado en redes neuronales de múltiples capas. Se diferencia en que realiza un **aprendizaje de representaciones (Feature Learning)** automático a partir de datos brutos. Para el Gobierno de IA, el DL presenta un reto crítico de **explicabilidad** ("caja negra").
6. **Sistema vs. Modelo:** El Reglamento (UE) 2024/1689 regula *sistemas de IA* (con autonomía, inferencia e impacto), no simples modelos matemáticos aislados. Si un sistema aplica reglas estáticas "if-then-else" sin capacidad de inferencia ni aprendizaje, puede quedar fuera del ámbito de aplicación del AI Act.
7. **Categorías de aprendizaje (ISO/IEC 22989):** La norma reconoce formalmente cuatro paradigmas: **supervisado** (con variable objetivo etiquetada), **no supervisado** (sin etiqueta, busca estructuras intrínsecas), **semi-supervisado** (combina datos etiquetados y sin etiquetar) y **por refuerzo** (aprende por ensayo/error maximizando una recompensa; no es un subtipo de los anteriores).
8. **Regresión Logística:** A pesar de su nombre, es un algoritmo fundamentalmente de **clasificación**, no de regresión continua. (Distractor clásico de examen).
9. **PLN (Procesamiento de Lenguaje Natural):** Reconocido como dominio propio de la IA (sección 9.2 de la ISO/IEC 22989). Integra dos grandes ramas funcionales: **NLU** (comprensión, extracción de significado) y **NLG** (generación de texto).
10. **Stemming vs. Lematización:** El *stemming* aplica reglas heurísticas de recorte rápido (a menudo generando falsas palabras), mientras que la *lematización* usa diccionarios y contexto morfológico para hallar el lema real.
11. **MLOps** extiende DevOps añadiendo la gestión de **datos y modelos** al código. Su rasgo más distintivo es el **CT (Continuous Training)** para combatir la degradación del modelo en producción. Para el perfil de Gobierno de IA, MLOps es el marco de infraestructura y procesos que hace posible la trazabilidad, la auditoría y el cumplimiento normativo.
12. **Degradación (Drift):** Se distingue entre *Data Drift* (cambia la distribución de las variables de entrada) y *Concept Drift* (cambia la relación entre la entrada y la predicción objetivo).

## Desarrollo

### 1. Conceptos de IA, Machine Learning y Deep Learning

#### 1.1. Inteligencia Artificial (IA)

Existen dos aproximaciones conceptuales clave para una oposición:

* **Definición normativa (Reglamento UE 2024/1689, Art. 3.1):** Un «sistema basado en una máquina que está diseñado para funcionar con distintos niveles de autonomía y que puede mostrar capacidad de adaptación tras el despliegue, y que, para objetivos explícitos o implícitos, **infiere** de la información de entrada que recibe la manera de generar resultados de salida, como predicciones, contenidos, recomendaciones o decisiones, que pueden influir en entornos físicos o virtuales».
* **Definición técnica (ISO/IEC 22989:2022):** Dominio técnico y científico dedicado a los sistemas técnicos que generan resultados como contenido, predicciones, recomendaciones o decisiones, para un conjunto de objetivos definidos por el ser humano. También se describe como la capacidad de un sistema de ingeniería para adquirir, procesar y aplicar conocimiento y habilidades.

*Punto fino de examen / auditoría (Resolución de aparente contradicción):* Un sistema informático basado en un árbol de reglas "if-else" deterministas rígidas (sin motor de inferencia ni aprendizaje) **no** encaja en la definición legal del Art. 3.1, ya que carece de la capacidad de *inferencia*, y puede quedar fuera del ámbito de aplicación del AI Act, considerándose software tradicional. Sin embargo, la IA tradicional sí incluye sistemas expertos y lógica (IA simbólica) siempre que posean un motor de inferencia.

**Diferenciación conceptual (NIST):**
* **IA estrecha (*Narrow AI*):** Diseñada para un dominio de tareas específico y limitado (ej. clasificar expedientes). Su conocimiento no es transferible. Es la IA regulada y auditada actualmente.
* **IA general (*General AI*):** Sistemas teóricos capaces de realizar cualquier tarea intelectual humana y transferir aprendizaje entre dominios.

#### 1.2. Machine Learning (ML)

Es el subcampo de la IA que construye modelos que aprenden patrones a partir de datos optimizando una función de pérdida, sin ser programados explícitamente con reglas deterministas para cada tarea.
* **Característica técnica diferencial:** Habitualmente requiere *Feature Engineering* (ingeniería de características). Los científicos de datos deben seleccionar, transformar e inyectar las variables relevantes antes de entrenar el algoritmo. Esto introduce un punto de control, pero también un riesgo crítico de **sesgo cognitivo humano** en la selección de atributos.
* **Ejemplos:** Árboles de decisión, Random Forest, Máquinas de Vectores de Soporte (SVM), k-NN, Regresión Logística.

#### 1.3. Deep Learning (DL)

Subconjunto de ML basado en Redes Neuronales Artificiales (ANN) con múltiples capas ocultas.
* **Característica técnica diferencial:** Realiza *Feature Learning* (aprendizaje de representaciones). El algoritmo descubre y extrae automáticamente las características relevantes (bordes en una imagen, sintaxis en un texto) sin intervención humana explícita. Esto genera alta precisión técnica, pero crea el problema de la **"Caja Negra" (opacidad)**, dificultando la auditabilidad y el cumplimiento del derecho a la explicabilidad de las decisiones automatizadas.
* **Ejemplos:** CNN (Redes Convolucionales para imágenes), RNN (Redes Recurrentes), Transformers (base de los LLMs modernos).

### 2. Modelos supervisados, no supervisados y otros paradigmas

La norma **ISO/IEC 22989:2022** reconoce formalmente cuatro paradigmas de aprendizaje, que presentan diferentes perfiles de riesgo y estrategias de gobierno.

| Categoría | Datos | Objetivo | Tareas típicas |
|---|---|---|---|
| **Supervisado** | Etiquetados (X, Y) | Aprender una función que mapee entradas a salidas. | Clasificación (clase discreta), Regresión (valor continuo). |
| **No supervisado** | Sin etiquetar (Solo X) | Descubrir patrones, agrupaciones o estructuras ocultas. | Clustering, Reducción de dimensionalidad, Detección de anomalías. |
| **Semi-supervisado** | Mezcla de etiquetados y sin etiquetar | Aprovechar pocos datos etiquetados junto a un gran volumen sin etiquetar. | Categoría formal reconocida por ISO/IEC 22989. |
| **Por refuerzo** | Interacción con entorno | Optimizar una política de acción para maximizar recompensa. | Robótica, Navegación, Juegos, RLHF en LLMs. |

#### 2.1. Aprendizaje supervisado: tareas y algoritmos clave

* **Clasificación:** Predice una categoría discreta (ej. spam/no spam, Fraude/No Fraude). *Algoritmo estrella engañoso:* La **Regresión Logística**. Otros algoritmos comunes: Árboles de Decisión, SVM.
* **Regresión:** Predice un valor continuo (ej. temperatura, presupuesto, coste estimado en euros). *Algoritmo típico:* Regresión Lineal, Regresión Polinómica.
* **Riesgo de Gobierno (Art. 10 AI Act):** La calidad del modelo depende enteramente de la calidad de las etiquetas humanas. Los datasets deben ser "pertinentes, representativos y carecer de errores", lo que exige una estricta gobernanza de datos para evitar sesgos heredados.

#### 2.2. Aprendizaje no supervisado: tareas y algoritmos clave

* **Clustering (Agrupamiento):** Agrupa observaciones por similitud sin conocer las categorías a priori (ej. segmentación de perfiles de usuarios). *Algoritmos:* K-Means, DBSCAN, Clustering Jerárquico.
* **Reducción de dimensionalidad:** Reduce el número de variables de entrada perdiendo la menor información posible (ej. comprime variables preservando la varianza). *Algoritmos:* PCA (Análisis de Componentes Principales), t-SNE, UMAP.
* **Detección de anomalías:** Identifica comportamientos desviados; puede ser no supervisada si no hay histórico etiquetado de anomalías.
* **Riesgo de Gobierno:** Al no existir una "verdad base" (*ground truth*) etiquetada, la validación de la equidad y la corrección del resultado es altamente compleja de auditar.

#### 2.3. Otros paradigmas

* **Aprendizaje semisupervisado:** Mezcla una pequeña cantidad de datos etiquetados con una gran masa de datos sin etiquetar. Es una categoría formal reconocida por la ISO/IEC 22989, no una "mezcla informal".
* **Aprendizaje autosupervisado:** Los propios datos generan la señal de entrenamiento (ej. ocultar una palabra de una frase y hacer que el modelo intente adivinarla). Es la base del preentrenamiento de los LLMs.
* **Aprendizaje por refuerzo:** Un agente aprende a tomar decisiones interactuando con un entorno, maximizando una función de recompensa mediante ensayo y error, sin depender de un dataset estático pre-etiquetado.

### 3. Procesamiento de Lenguaje Natural (PLN/NLP)

El PLN (o NLP) es un dominio de la IA (reconocido en la sección 9.2 de la ISO/IEC 22989) dedicado a que los sistemas informáticos analicen, comprendan y generen lenguaje humano. No se limita a los grandes modelos de lenguaje (LLMs); incluye múltiples subtareas clásicas. Sus dos pilares son:

1. **NLU (Natural Language Understanding):** Comprensión del lenguaje. Implica extraer significado, sintaxis, intenciones, sentimiento y entidades (NER - *Named Entity Recognition*).
2. **NLG (Natural Language Generation):** Capacidad de redactar texto coherente a partir de datos o instrucciones. (Nota: los LLMs actuales realizan ambas funciones integradas).

#### 3.1. Técnicas de Preprocesamiento

La forma en que se limpia el texto afecta a los sesgos y a la precisión del modelo:

* **Tokenización:** División del texto en unidades operables computacionalmente. Un token no es siempre una palabra; en modelos modernos suele ser una *subpalabra* o un carácter (ej. "administración" → ["admin", "istración"]).
* **Stemming (Truncamiento):** Algoritmo de reglas heurísticas (fuerza bruta) que "corta" prefijos o sufijos para dejar una raíz estática (ej. "estudios" → "estudi"). Es rápido, no usa diccionario y puede generar no-palabras.
* **Lematización:** Análisis morfosintáctico apoyado en un corpus lingüístico o diccionario que transforma la palabra a su lema real de diccionario (ej. "fui" → "ir"). Es costoso pero preciso.

#### 3.2. Representación y Arquitecturas

* **One-hot encoding:** Vector inmenso lleno de ceros y un solo 1. No captura semántica.
* **TF-IDF:** Pondera la frecuencia de un término en un documento frente a su rareza en el corpus total.
* **Embeddings:** Representación vectorial densa (ej. array de 768 números) en un espacio continuo, donde palabras con semántica similar están físicamente cerca. *Riesgo de Gobierno:* Los embeddings entrenados en corpus históricos de internet capturan y codifican matemáticamente sesgos sociales discriminatorios, requiriendo auditoría específica.
* **Transformers:** Arquitectura basada en **Autoatención (Self-Attention)**. Procesa el texto en paralelo evaluando la importancia de todas las palabras de una frase respecto a las demás simultáneamente. Es la base técnica de la IA Generativa textual.

### 4. Conceptos de MLOps y Operación

**MLOps** es la extensión de las prácticas DevOps aplicadas a los sistemas de aprendizaje automático. Desde una perspectiva de ciclo de vida del software, es la disciplina que gestiona el código, los datos y el modelo; desde una perspectiva de Gobierno de IA, es el **marco de infraestructura y procesos que hace posible la trazabilidad, la auditoría y el cumplimiento normativo** de un sistema en producción.

#### 4.1. Artefactos gestionados (diferencia con DevOps)

Mientras que DevOps se centra en versionar y desplegar código, MLOps requiere el gobierno versionado de un triplete interdependiente:
1. **Código** (algoritmos y pipelines).
2. **Modelos** (ficheros de pesos, versionados en un *Model Registry*).
3. **Datos** (datasets de entrenamiento/validación y características, en un *Feature Store*). Esto garantiza el linaje del dato (*Data Provenance*), esencial para auditorías del AI Act.

#### 4.2. CI, CD y CT

* **CI (Continuous Integration):** En ML, no solo valida código con tests unitarios, sino que valida esquemas de datos, calidad estadística y evalúa métricas del modelo candidato (Data testing).
* **CD (Continuous Delivery/Deployment):** Automatiza el despliegue de *pipelines* de predicción, endpoints o servicios de inferencia (API) de forma segura, no solo binarios de software.
* **CT (Continuous Training):** Pilar diferencial y exclusivo de MLOps. Es la automatización del reentrenamiento de un modelo en producción tras detectar que su rendimiento ha caído (por *drift*) o al recibir nuevos lotes de datos estructurados.

#### 4.3. Monitorización y Degradación (Drift)

Los modelos ML se degradan de forma silente aunque el código no falle (errores 200 OK con predicciones inútiles), porque el mundo real cambia, perdiendo precisión y equidad. Monitorizar este fenómeno es crítico para el gobierno del sistema:

* **Data Drift (Deriva de datos o Covariate Shift):** Cambia la distribución estadística de las variables de entrada (X) respecto al dataset original, pero la regla de negocio no varía. (Ej: Cambia el perfil sociodemográfico de los ciudadanos que piden una ayuda).
* **Concept Drift (Deriva de concepto):** Cambia la relación subyacente entre la entrada (X) y la variable objetivo (Y). (Ej: Cambia la normativa legal, por lo que solicitudes que antes eran "Aprobadas" con los mismos datos de entrada, ahora deben ser "Denegadas").
* **Training-serving skew:** Fuga o discrepancia técnica donde una variable se calcula de manera distinta durante el entrenamiento (ej. un histórico de base de datos) y durante el servicio en vivo (ej. un valor extraído de una sesión web).

#### 4.4. Riesgos, Auditoría y Obligaciones Legales

* **Fuga de datos (Data Leakage):** Variables futuras, que no existirán en producción en el momento de inferir, se colaron accidentalmente en la fase de entrenamiento inflando la métrica de éxito (*Accuracy*).
* **Registro de eventos (Logging):** Según el **Art. 12 del Reglamento (UE) 2024/1689**, los sistemas de IA de alto riesgo deben disponer obligatoriamente de un registro automático de eventos ("logs") para garantizar la trazabilidad de su funcionamiento a lo largo de todo el ciclo de vida. MLOps provee los mecanismos técnicos para cumplir esta exigencia legal.
* **Alcance de los algoritmos clásicos en la Ley de IA:** Aunque técnicamente un algoritmo de regresión logística o un árbol de decisión simple pertenecen al Machine Learning clásico, estos sistemas simples también quedan subsumidos bajo la definición legal de "Sistema de IA" del AI Act si cumplen el criterio de inferencia. El reglamento europeo adopta una visión tecnológicamente neutra.

## Conceptos que suelen preguntarse (Trampas comunes)

| Concepto | Realidad técnica / jurídica | Distractor típico en examen |
|---|---|---|
| **Regresión Logística** | Es un algoritmo supervisado de **clasificación**. | "Es un algoritmo de regresión continua por llamarse regresión". |
| **IA vs. Machine Learning** | Relación jerárquica: ML es un subconjunto de IA. | "Son términos sinónimos e intercambiables según ISO". |
| **ML vs. DL** | ML = Feature engineering (manual); DL = Feature learning (automático, "caja negra"). | "Todo el ML moderno es DL" / "El DL es más transparente y fácil de auditar que el ML clásico". |
| **Aprendizaje por refuerzo** | Categoría independiente basada en recompensas. | "Es un subtipo de aprendizaje no supervisado". |
| **Supervisado vs. No supervisado** | Supervisado tiene etiquetas ($Y$); no supervisado busca patrones sin etiquetas. | "El no supervisado requiere validación constante de un operario humano". |
| **Token vs. Palabra** | Un token puede ser subpalabra o carácter. | "Un token siempre equivale exactamente a una palabra". |
| **Stemming vs. Lematización** | Stemming = recortes heurísticos; Lematización = diccionario/lema real. | "Ambos procesos garantizan que la palabra resultante exista en el idioma". |
| **Drift** | Data Drift = Cambia la X; Concept Drift = Cambia la relación X→Y. | "El Data Drift es un bug de compilación de código / se soluciona reiniciando el servidor". |
| **CT (Continuous Training)** | Fase exclusiva de MLOps para reentrenar modelos ante el *drift*. | "CT significa Continuous Testing y ya existía en DevOps tradicional". |
| **Accuracy vs. Recall/Precision** | Accuracy es engañosa en clases desbalanceadas (ej. fraude). | "Accuracy siempre es la mejor métrica técnica". |

## Posibles preguntas tipo test

**Pregunta 1.** Según el Art. 3.1 del Reglamento (UE) 2024/1689, ¿cuál de los siguientes elementos es un requisito clave para que un software sea considerado "sistema de IA"?

A. Estar basado exclusivamente en redes neuronales.

B. Funcionar siempre con total autonomía y sin supervisión.

C. Inferir la manera de generar resultados (predicciones, recomendaciones, etc.) a partir de información de entrada.

D. Ser un programa informático que opera bajo reglas estáticas "if-then" sin motor de inferencia.

**Respuesta correcta: C.** (La norma exige capacidad de inferencia; descarta software determinista clásico sin ella).

**Pregunta 2.** En un proyecto de la Administración se dispone de un histórico de miles de reclamaciones etiquetadas previamente por funcionarios en las categorías: "Tributos", "Medio Ambiente", "Sanidad". Se requiere automatizar el triaje. ¿Qué enfoque técnico es el adecuado?

A. Clustering jerárquico.

B. Clasificación mediante aprendizaje supervisado.

C. Regresión mediante aprendizaje no supervisado.

D. Reducción de dimensionalidad algorítmica.

**Respuesta correcta: B.** (Existen etiquetas objetivo, se busca predecir clases discretas).

**Pregunta 3.** Si utilizamos un algoritmo de Regresión Logística, estamos aplicando un modelo de:

A. Aprendizaje no supervisado para agrupamiento.

B. Aprendizaje supervisado para predicción continua.

C. Aprendizaje supervisado para clasificación.

D. Aprendizaje por refuerzo iterativo.

**Respuesta correcta: C.** (Es un distractor clásico. Su salida pasa por una función sigmoide para predecir probabilidades entre clases).

**Pregunta 4.** En el preprocesamiento de PLN, ¿cuál es la principal diferencia entre el *Stemming* y la Lematización?

A. El Stemming utiliza un análisis morfológico detallado, la Lematización aplica recortes heurísticos.

B. La Lematización busca reducir la palabra a un lema válido existente en el idioma, el Stemming aplica reglas de recorte rápido.

C. Ambos conceptos son sinónimos absolutos y obligatorios en el uso de Transformers.

D. El Stemming solo se aplica a IA Generativa y la Lematización a ML clásico.

**Respuesta correcta: B.**

**Pregunta 5.** En el ámbito de MLOps, ¿cómo se denomina el fenómeno por el cual la relación estadística subyacente entre las variables de entrada y la variable objetivo cambia con el tiempo, invalidando la eficacia del modelo?

A. Data Drift (Deriva de datos o Covariate Shift).

B. Continuous Training (CT).

C. Concept Drift (Deriva de concepto).

D. Training-Serving Skew.

**Respuesta correcta: C.** (El cambio en la relación o definición de lo que se predice es deriva de concepto).

**Pregunta 6.** Un algoritmo capaz de extraer automáticamente representaciones o características complejas (Feature Learning) a partir de datos brutos como píxeles de una imagen, sin que un ingeniero defina manualmente qué variables importar, es característico de:

A. Machine Learning tradicional.

B. Aprendizaje por refuerzo estocástico.

C. Deep Learning.

D. Árboles de decisión clásicos.

**Respuesta correcta: C.** (La extracción jerárquica automática de características diferencia al DL del ML clásico).

**Pregunta 7.** El Art. 12 del Reglamento (UE) 2024/1689 exige de forma específica garantizar la trazabilidad durante el funcionamiento mediante la generación automática de un registro de eventos ("logs"). Esta obligación recae explícitamente sobre:

A. Sistemas de IA de alto riesgo.

B. Únicamente sobre Modelos Generativos (LLMs).

C. Cualquier tipo de software de las Administraciones Públicas.

D. Solo sistemas basados en Clustering no supervisado.

**Respuesta correcta: A.**

**Pregunta 8.** ¿Qué diferencia importante introduce el ciclo MLOps respecto al ciclo de vida del software tradicional (DevOps)?

A. No necesita validación técnica, basta con el test de la API.

B. Añade a la gestión de versiones de código la gestión de datos, características (features) y el artefacto del modelo.

C. DevOps realiza Continuous Training (CT) y MLOps Continuous Integration (CI).

D. El rendimiento en MLOps solo depende de bugs en el código, ignorando el entorno.

**Respuesta correcta: B.**

**Pregunta 9.** Desde la perspectiva del gobierno de un sistema de IA en producción, ¿qué fenómeno se está produciendo si las distribuciones estadísticas de las variables de entrada que envían los ciudadanos cambian con el tiempo respecto al conjunto de entrenamiento original, pero la regla de negocio que define la salida correcta no ha variado?

A. Deriva de concepto (*Concept Drift*).

B. Deriva de datos (*Data Drift*).

C. Fuga de datos (*Data Leakage*).

D. Sobreajuste algorítmico (*Overfitting*).

**Respuesta correcta: B.** (Si solo cambian las características de la entrada X, se trata de deriva de datos. Si cambiase la regla que asocia X con Y, sería deriva de concepto).

## Normativa o fuentes relacionadas

* **Fuente de Convocatoria:** BOCM, 11 de junio de 2026, Resolución 352/2026.
* **Fuentes Normativas:**
  * **Reglamento (UE) 2024/1689** del Parlamento Europeo y del Consejo (Ley de Inteligencia Artificial). Fuente esencial para las definiciones jurídicas de IA (Art. 3), los requisitos de gobierno de datos de entrenamiento (Art. 10) y las obligaciones de registro (Art. 12).
  * Reglamento (UE) 2016/679 (RGPD) y RD 311/2022 (Esquema Nacional de Seguridad).
* **Estándares Oficiales:**
  * **ISO/IEC 22989:2022 (UNE-EN ISO/IEC 22989:2023)**: *Information technology — Artificial intelligence concepts and terminology*. Norma de referencia para el vocabulario técnico (IA, ML, DL, paradigmas de aprendizaje, PLN).
* **Documentación Institucional:**
  * **NIST AI RMF 1.0**, **ISO/IEC 23894:2023** y **NIST AI 100-2e2025** (Terminología, taxonomía y marcos de gestión de riesgos para operaciones y ataques en ML).
  * **ENISA**, Securing Machine Learning Algorithms.

## Dudas o puntos pendientes

* **IA General (GPAI) frente a IA Específica:** El AI Act introduce conceptos de "Modelos de propósito general", los cuales encajan más de lleno en el Tema 2 (LLMs e IA Generativa). Queda pendiente asegurar que las preguntas sobre GPAI se agrupan en su bloque correspondiente y no en este tema fundacional.
* **Despliegues y Orquestación:** Existen aspectos técnicos de MLOps (Kubernetes, Model Registries, Feature Stores) documentados exhaustivamente por proveedores de la industria (AWS, Google Cloud, Azure). Sin embargo, carecen de norma UNE/ISO explícita que las regule al nivel técnico más bajo. Nos hemos ceñido a los conceptos consolidados independientes del proveedor.
* **Taxonomía exacta de MLOps:** Aunque los pilares CI/CD/CT provienen de la documentación técnica consolidada de la industria (ej. Google Cloud Architecture Center), es la conceptualización más extendida a falta de un estándar normativo ISO específico y exclusivo que certifique los niveles de madurez de MLOps.
* **Procesos de Ciberseguridad de la Comunidad de Madrid:** Queda confirmar si en convocatorias paralelas de la Agencia de Ciberseguridad el temario incluye una ampliación específica de modelos adversarios en ML.
