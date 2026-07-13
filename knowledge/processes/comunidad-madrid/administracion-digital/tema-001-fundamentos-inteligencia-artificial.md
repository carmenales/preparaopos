---
id: "tema-001-fundamentos-inteligencia-artificial"
title: "Fundamentos de Inteligencia Artificial"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital"
official_topic: "Tema 1. Fundamentos de Inteligencia Artificial"
source_ids: []
tags:
  - inteligencia-artificial
  - machine-learning
  - deep-learning
  - pln
  - mlops
created_at: "2026-07-09"
last_reviewed: null
ai_generated: true
ai_sources:
  - "chatgpt"
  - "perplexity"
  - "gemini"
  - "base-apunte"
needs_human_review: true
---

# Fundamentos de Inteligencia Artificial

## Ideas clave

1. **Inteligencia Artificial (IA)** es el campo general orientado a construir sistemas capaces de percibir, razonar, aprender y actuar.
2. **Machine Learning (ML)** es un subcampo de la IA donde el sistema aprende de los datos sin programación explícita de reglas. Se caracteriza por requerir la **extracción manual de características (Feature Engineering)** por parte de expertos.
3. **Deep Learning (DL)** es un subcampo del ML basado en redes neuronales de múltiples capas. Se diferencia en que realiza un **aprendizaje de representaciones (Feature Learning)** automático a partir de datos brutos.
4. **Sistema vs. Modelo:** El Reglamento (UE) 2024/1689 regula *sistemas de IA* (con autonomía, inferencia e impacto), no simples modelos matemáticos aislados.
5. **Categorías de aprendizaje:** Se dividen principalmente en **supervisado** (con variable objetivo etiquetada), **no supervisado** (sin etiqueta, busca estructuras intrínsecas) y **por refuerzo** (aprende por ensayo/error maximizando una recompensa; no es un subtipo de los anteriores).
6. **Regresión Logística:** A pesar de su nombre, es un algoritmo fundamentalmente de **clasificación**, no de regresión continua. (Distractor clásico de examen).
7. **PLN (Procesamiento de Lenguaje Natural):** Integra dos grandes ramas funcionales: **NLU** (comprensión, extracción de significado) y **NLG** (generación de texto).
8. **Stemming vs. Lematización:** El *stemming* aplica reglas heurísticas de recorte rápido (a menudo generando falsas palabras), mientras que la *lematización* usa diccionarios y contexto morfológico para hallar el lema real.
9. **MLOps** extiende DevOps añadiendo la gestión de **datos y modelos** al código. Su rasgo más distintivo es el **CT (Continuous Training)** para combatir la degradación del modelo en producción.
10. **Degradación (Drift):** Se distingue entre *Data Drift* (cambia la distribución de las variables de entrada) y *Concept Drift* (cambia la relación entre la entrada y la predicción objetivo).

## Desarrollo

### 1. Conceptos de IA, Machine Learning y Deep Learning

#### 1.1. Inteligencia Artificial (IA)

Existen dos aproximaciones conceptuales clave para una oposición:

* **Definición normativa (Reglamento UE 2024/1689, Art. 3.1):** Un «sistema basado en una máquina que está diseñado para funcionar con distintos niveles de autonomía y que puede mostrar capacidad de adaptación tras el despliegue, y que, para objetivos explícitos o implícitos, **infiere** de la información de entrada que recibe la manera de generar resultados de salida, como predicciones, contenidos, recomendaciones o decisiones, que pueden influir en entornos físicos o virtuales».
* **Definición técnica (ISO/IEC 22989:2022):** Capacidad de un sistema de ingeniería para adquirir, procesar y aplicar conocimiento y habilidades.

*Punto fino de examen (Resolución de aparente contradicción):* Un sistema informático basado en un árbol de reglas "if-else" deterministas rígidas (sin motor de inferencia ni aprendizaje) **no** encaja en la definición legal del Art. 3.1, ya que carece de la capacidad de *inferencia*. Sin embargo, la IA tradicional sí incluye sistemas expertos y lógica (IA simbólica) siempre que posean un motor de inferencia.

#### 1.2. Machine Learning (ML)

Es el subcampo de la IA que construye modelos que aprenden patrones a partir de datos optimizando una función de pérdida.
* **Característica técnica diferencial:** Habitualmente requiere *Feature Engineering* (ingeniería de características). Los científicos de datos deben seleccionar, transformar e inyectar las variables relevantes antes de entrenar el algoritmo.
* **Ejemplos:** Árboles de decisión, Random Forest, Máquinas de Vectores de Soporte (SVM), k-NN, Regresión Logística.

#### 1.3. Deep Learning (DL)

Subconjunto de ML basado en Redes Neuronales Artificiales (ANN) con múltiples capas ocultas.
* **Característica técnica diferencial:** Realiza *Feature Learning* (aprendizaje de representaciones). El algoritmo descubre y extrae automáticamente las características relevantes (bordes en una imagen, sintaxis en un texto) sin intervención humana explícita.
* **Ejemplos:** CNN (Redes Convolucionales para imágenes), RNN (Redes Recurrentes), Transformers (base de los LLMs modernos).

### 2. Modelos supervisados, no supervisados y otros paradigmas

| Categoría | Datos | Objetivo | Tareas típicas |
|---|---|---|---|
| **Supervisado** | Etiquetados ($X, Y$) | Aprender una función que mapee entradas a salidas. | Clasificación (clase discreta), Regresión (valor continuo). |
| **No supervisado** | Sin etiquetar (Solo $X$) | Descubrir patrones, agrupaciones o estructuras ocultas. | Clustering, Reducción de dimensionalidad, Reglas de asociación. |
| **Por refuerzo** | Interacción con entorno | Optimizar una política de acción para maximizar recompensa. | Robótica, Navegación, Juegos, RLHF en LLMs. |

#### 2.1. Tareas y algoritmos clave

* **Clasificación (Supervisado):** Predice una categoría discreta (ej. spam/no spam). *Algoritmo estrella engañoso:* La **Regresión Logística**.
* **Regresión (Supervisado):** Predice un valor continuo (ej. temperatura, presupuesto). *Algoritmo típico:* Regresión Lineal, Regresión Polinómica.
* **Clustering (No supervisado):** Agrupa observaciones por similitud sin conocer las categorías a priori. *Algoritmos:* K-Means, DBSCAN, Clustering Jerárquico.
* **Reducción de dimensionalidad (No supervisado):** Reduce el número de variables de entrada perdiendo la menor información posible. *Algoritmos:* PCA (Análisis de Componentes Principales), t-SNE, UMAP.

#### 2.2. Conceptos complementarios
* **Aprendizaje semisupervisado:** Mezcla una pequeña cantidad de datos etiquetados con una gran masa de datos sin etiquetar.
* **Aprendizaje autosupervisado:** Los propios datos generan la señal de entrenamiento (ej. ocultar una palabra de una frase y hacer que el modelo intente adivinarla). Es la base del preentrenamiento de los LLMs.

### 3. Procesamiento de Lenguaje Natural (PLN/NLP)

El PLN abarca la interacción entre computadoras y el lenguaje humano. Sus dos pilares son:
1. **NLU (Natural Language Understanding):** Comprender la semántica, sintaxis, intenciones y extraer entidades.
2. **NLG (Natural Language Generation):** Capacidad de redactar texto coherente. (Nota: los LLMs actuales realizan ambas).

#### 3.1. Técnicas de Preprocesamiento

* **Tokenización:** División del texto en unidades. Un token no es siempre una palabra; en modelos modernos suele ser una *subpalabra* o un carácter (ej. "administración" $\rightarrow$ ["admin", "istración"]).
* **Stemming (Truncamiento):** Algoritmo de reglas heurísticas que "corta" sufijos para dejar una raíz estática (ej. "estudios" $\rightarrow$ "estudi"). Es rápido, no usa diccionario y puede generar no-palabras.
* **Lematización:** Análisis morfosintáctico apoyado en un corpus lingüístico que transforma la palabra a su lema real de diccionario (ej. "fui" $\rightarrow$ "ir"). Es costoso pero preciso.

#### 3.2. Representación y Arquitecturas

* **One-hot encoding:** Vector inmenso lleno de ceros y un solo 1. No captura semántica.
* **TF-IDF:** Pondera la frecuencia de un término en un documento frente a su rareza en el corpus total.
* **Embeddings:** Representación vectorial densa (ej. array de 768 números) en un espacio continuo, donde palabras con semántica similar están físicamente cerca.
* **Transformers:** Arquitectura basada en **Autoatención (Self-Attention)**. Procesa el texto en paralelo evaluando la importancia de todas las palabras de una frase respecto a las demás simultáneamente. Es la base técnica de la IA Generativa textual.

### 4. Conceptos de MLOps y Operación

**MLOps** es la extensión de DevOps al ciclo de vida del ML. A diferencia del software tradicional (donde se versiona código), en MLOps se deben versionar tres artefactos interdependientes: **Código, Datos y Modelo**.

#### 4.1. CI, CD y CT

* **CI (Continuous Integration):** En ML, no solo valida código con tests unitarios, sino que valida esquemas de datos, calidad estadística y comprueba distribuciones (Data testing).
* **CD (Continuous Delivery/Deployment):** Despliega *pipelines* de predicción, endpoints o servicios de inferencia (API), no solo binarios de software.
* **CT (Continuous Training):** Exclusivo de MLOps. Es la automatización del reentrenamiento de un modelo en producción tras detectar que su rendimiento ha caído o al recibir nuevos lotes de datos estructurados.

#### 4.2. Monitorización y Degradación (Drift)

Los modelos ML se degradan de forma silente aunque el código no falle (errores 200 OK con predicciones inútiles):

* **Data Drift (Deriva de datos o Covariate Shift):** Cambia la distribución estadística de las variables de entrada ($X$) respecto al dataset original. (Ej: Cambia el perfil sociodemográfico de los ciudadanos que piden una ayuda).
* **Concept Drift (Deriva de concepto):** Cambia la relación subyacente entre la entrada ($X$) y la variable objetivo ($Y$). (Ej: Cambia la normativa legal, por lo que solicitudes que antes eran "Aprobadas" con los mismos datos de entrada, ahora deben ser "Denegadas").
* **Training-serving skew:** Fuga o discrepancia técnica donde una variable se calcula de manera distinta durante el entrenamiento (ej. un histórico de base de datos) y durante el servicio en vivo (ej. un valor extraído de una sesión web).

#### 4.3. Riesgos, Auditoría y Obligaciones Legales

* **Fuga de datos (Data Leakage):** Variables futuras, que no existirán en producción en el momento de inferir, se colaron accidentalmente en la fase de entrenamiento inflando la métrica de éxito (*Accuracy*).
* **Registro de eventos (Logging):** Según el **Art. 12 del Reglamento (UE) 2024/1689**, los sistemas de IA de alto riesgo deben disponer obligatoriamente de un registro automático de eventos ("logs") para garantizar la trazabilidad de su funcionamiento a lo largo de todo el ciclo de vida. MLOps provee los mecanismos técnicos para cumplir esta exigencia legal.

## Conceptos que suelen preguntarse (Trampas comunes)

| Concepto | Realidad técnica / jurídica | Distractor típico en examen |
|---|---|---|
| **Regresión Logística** | Es un algoritmo supervisado de **clasificación**. | "Es un algoritmo de regresión continua por llamarse regresión". |
| **Aprendizaje por refuerzo** | Categoría independiente basada en recompensas. | "Es un subtipo de aprendizaje no supervisado". |
| **Token vs. Palabra** | Un token puede ser subpalabra o carácter. | "Un token siempre equivale exactamente a una palabra". |
| **Stemming vs. Lematización** | Stemming = recortes heurísticos; Lematización = diccionario/lema real. | "Ambos son procesos exactos idénticos definidos por la ISO". |
| **ML vs. DL** | ML = Feature engineering; DL = Feature learning (automático). | "Todo el ML moderno es DL". |
| **Drift** | Data Drift = Cambia la $X$; Concept Drift = Cambia la relación $X \rightarrow Y$. | "Data drift es un bug de compilación de código". |
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

## Normativa o fuentes relacionadas

* **Fuentes de Convocatoria:** BOCM, 11 de junio de 2026, Resolución 352/2026.
* **Fuentes Normativas:** 
  * **Reglamento (UE) 2024/1689 del Parlamento Europeo y del Consejo (Ley de Inteligencia Artificial)**. Fuente esencial para las definiciones jurídicas de IA (Art. 3) y obligaciones de registro (Art. 12).
  * Reglamento (UE) 2016/679 (RGPD) y RD 311/2022 (Esquema Nacional de Seguridad).
* **Estándares Oficiales:**
  * **ISO/IEC 22989:2022 (UNE-EN ISO/IEC 22989:2023)**: *Information technology — Artificial intelligence concepts and terminology*. Norma de referencia para el vocabulario técnico puramente tecnológico (ML, DL, supervisado).
* **Documentación Institucional:**
  * **NIST AI RMF 1.0** y **NIST AI 100-2e2025** (Terminología y taxonomía técnica para operaciones, riesgos y ataques en ML).
  * **ENISA**, Securing Machine Learning Algorithms.

## Dudas o puntos pendientes

* **IA General (GPAI) frente a IA Específica:** El AI Act introduce conceptos de "Modelos de propósito general", los cuales encajan más de lleno en el Tema 2 (LLMs e IA Generativa). Queda pendiente asegurar que las preguntas sobre GPAI se agrupan en su bloque correspondiente y no en este tema fundacional.
* **Despliegues y Orquestación:** Existen aspectos técnicos de MLOps (Kubernetes, Model Registries, Feature Stores) documentados exhaustivamente por proveedores de la industria (AWS, Google Cloud, Azure). Sin embargo, carecen de norma UNE/ISO explícita que las regule al nivel técnico más bajo. Nos hemos ceñido a los conceptos consolidados independientes del proveedor.
* **Procesos de Ciberseguridad de la Comunidad de Madrid:** Queda confirmar si en convocatorias paralelas de la Agencia de Ciberseguridad el temario incluye una ampliación específica de modelos adversarios en ML.
