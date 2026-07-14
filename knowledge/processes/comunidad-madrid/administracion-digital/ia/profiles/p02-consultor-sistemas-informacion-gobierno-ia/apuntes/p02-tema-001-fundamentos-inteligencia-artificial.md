---
id: "cm-ad-ia-p02-tema-001-fundamentos-inteligencia-artificial"
title: "Fundamentos de Inteligencia Artificial"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/ia"
profiles:
  - "p02-consultor-sistemas-informacion-ia"
official_profile: "P02 - Consultor de Sistemas de Información - Especialista en Gobierno de IA"
official_topic: "Tema 1. Fundamentos de Inteligencia Artificial"
source_ids: []
tags:
  - "inteligencia-artificial"
  - "machine-learning"
  - "deep-learning"
  - "pln"
  - "mlops"
  - "gobierno-ia"
  - "ai-act"
  - "iso-iec-22989"
created_at: "2026-07-14"
last_reviewed: null
ai_generated: true
ai_sources:
  - "chatgpt"
  - "perplexity"
  - "gemini"
  - "base-apunte"
  - "eur-lex"
needs_human_review: true
---

# Fundamentos de Inteligencia Artificial

## Encaje en la convocatoria

Este tema corresponde al **Tema 1 del Anexo 3** de la Resolución 352/2026 (BOCM 11/06/2026)[cite: 1], dentro de las áreas de conocimiento objeto de la Fase 1 de oposición para el perfil **P02: Consultor de Sistemas de Información - Especialista en Gobierno de IA** de la Agencia para la Administración Digital de la Comunidad de Madrid[cite: 1].

Aunque el contenido base (conceptos de IA, ML, DL, PLN y MLOps) coincide con el perfil P01, el enfoque de estudio para el perfil P02 debe ser radicalmente distinto. En un examen tipo test para este perfil, el examinador no evaluará cómo codificar un algoritmo, sino **cómo auditarlo, gobernar sus datos, trazar su linaje, controlar sus sesgos y encuadrarlo en el marco regulatorio**. 

La prueba exige diferenciar con precisión la terminología normativa (Reglamento (UE) 2024/1689 de la IA), los estándares técnicos internacionales (ISO/IEC 22989:2022) y los marcos de gestión de riesgos institucionales (NIST AI RMF 1.0). Es crítico dominar la diferencia entre la degradación de los datos (*Data Drift*) y la del concepto (*Concept Drift*), así como entender MLOps no como una herramienta de desarrollo, sino como el **marco de control auditable** necesario para cumplir con la legislación.

## Ideas clave

1.  **Definición Normativa de IA:** El Reglamento (UE) 2024/1689 (AI Act) define un sistema de IA huyendo del término "software". Lo categoriza como un "sistema basado en una máquina" que infiere resultados a partir de entradas, con distintos niveles de autonomía[cite: 2].
2.  **Jerarquía Técnica y Normativa:** La **ISO/IEC 22989:2022** es el estándar internacional de terminología. Establece que la IA es el dominio principal, el *Machine Learning* (ML) es una de sus disciplinas, y el *Deep Learning* (DL) es una técnica dentro del ML basada en redes neuronales profundas[cite: 2].
3.  **ML vs. DL (El Problema de la Caja Negra):** En ML clásico, las características se extraen manualmente (*Feature Engineering*). En DL, se extraen automáticamente (*Feature Learning*). Para el Gobierno de IA, el DL presenta un reto crítico de **explicabilidad** y opacidad.
4.  **Paradigmas de Aprendizaje (ISO/IEC 22989):** La norma reconoce formalmente cuatro enfoques: Supervisado, No Supervisado, Semi-supervisado y Por Refuerzo[cite: 2].
5.  **Regresión Logística:** Trampa clásica de examen. A pesar de llevar la palabra "regresión", es un algoritmo de **clasificación** supervisada.
6.  **Procesamiento de Lenguaje Natural (PLN/NLP):** Reconocido como un dominio de IA propio en la ISO/IEC 22989[cite: 2]. No se limita a la generación (NLG); requiere comprensión (NLU). En preprocesamiento, distinguir *Stemming* (fuerza bruta/heurística) de *Lematización* (uso de diccionarios/léxico).
7.  **MLOps como mecanismo de Gobierno:** MLOps extiende DevOps añadiendo el control de versiones de **Datos y Modelos**. Su fase exclusiva, el **Entrenamiento Continuo (CT)**, es la respuesta operativa para mitigar la degradación del modelo (*Drift*) y asegurar la robustez exigida por la legislación.

## Desarrollo

### 1. Conceptos de IA, Machine Learning y Deep Learning

#### 1.1. Inteligencia Artificial (IA)

Desde la perspectiva del Gobierno de IA, coexisten dos definiciones fundamentales:

*   **Definición Normativa Europea (Reglamento UE 2024/1689, Art. 3.1):** Un «sistema basado en una máquina que está diseñado para funcionar con distintos niveles de autonomía y que puede mostrar capacidad de adaptación tras el despliegue, y que, para objetivos explícitos o implícitos, **infiere** de la información de entrada que recibe la manera de generar resultados de salida, como predicciones, contenidos, recomendaciones o decisiones, que pueden influir en entornos físicos o virtuales»[cite: 2].
    *   *Punto de auditoría:* Si un sistema aplica reglas estáticas programadas (*if-then-else*) sin capacidad de inferencia o aprendizaje, puede quedar fuera del ámbito de aplicación del AI Act como sistema de IA, considerándose software tradicional.
*   **Definición Técnica Internacional (ISO/IEC 22989:2022):** Dominio técnico y científico dedicado a los sistemas técnicos que generan resultados como contenido, predicciones, recomendaciones o decisiones, para un conjunto de objetivos definidos por el ser humano[cite: 2].

**Diferenciación conceptual (NIST):**
*   **IA estrecha (*Narrow AI*):** Diseñada para un dominio de tareas específico y limitado (ej. clasificar expedientes). Su conocimiento no es transferible. Es la IA regulada y auditada actualmente.
*   **IA general (*General AI*):** Sistemas teóricos capaces de realizar cualquier tarea intelectual humana y transferir aprendizaje entre dominios.

#### 1.2. Machine Learning (ML - Aprendizaje Automático)

*   **Concepto:** Subcampo de la IA en el que los sistemas construyen modelos matemáticos a partir de datos de entrenamiento (optimización de una función de pérdida), sin ser programados explícitamente con reglas deterministas para cada tarea[cite: 2].
*   **Implicación para Gobierno:** El ML tradicional requiere **Ingeniería de Características (*Feature Engineering*)**. Expertos humanos seleccionan qué variables ($X$) alimentan al modelo. Esto introduce un punto de control, pero también un riesgo crítico de **sesgo cognitivo humano** en la selección de atributos.

#### 1.3. Deep Learning (DL - Aprendizaje Profundo)

*   **Concepto:** Subconjunto del ML que utiliza Redes Neuronales Artificiales (ANN) con múltiples capas ocultas (*hidden layers*)[cite: 2].
*   **Implicación para Gobierno:** A diferencia del ML clásico, el DL realiza un **Aprendizaje de Representaciones (*Feature Learning*)**. El propio algoritmo extrae automáticamente las características relevantes de los datos brutos. Esto genera una alta precisión técnica, pero crea el problema de la **"Caja Negra" (opacidad)**, dificultando la auditabilidad y el cumplimiento del derecho a la explicabilidad de las decisiones automatizadas.

### 2. Modelos supervisados y no supervisados

La norma **ISO/IEC 22989:2022** reconoce formalmente cuatro paradigmas de aprendizaje, que presentan diferentes perfiles de riesgo y estrategias de gobierno[cite: 2].

#### 2.1. Aprendizaje Supervisado

*   **Mecánica:** El modelo se entrena utilizando un conjunto de datos **etiquetados** históricamente (se proporciona la entrada $X$ y la respuesta/variable objetivo correcta $Y$).
*   **Riesgo de Gobierno (Art. 10 AI Act):** La calidad del modelo depende enteramente de la calidad de las etiquetas humanas. Los datasets deben ser "pertinentes, representativos y carecer de errores", lo que exige una estricta gobernanza de datos para evitar sesgos heredados.
*   **Tareas típicas:**
    *   **Clasificación:** Predice una variable categórica discreta (ej. Fraude / No Fraude). *Algoritmos comunes:* Árboles de Decisión, *Support Vector Machines* (SVM), y **Regresión Logística**.
    *   **Regresión:** Predice una variable numérica continua (ej. Coste estimado en euros). *Algoritmos comunes:* Regresión Lineal.

#### 2.2. Aprendizaje No Supervisado

*   **Mecánica:** Se entrena con datos **sin etiquetar**. El objetivo no es predecir una salida predefinida, sino descubrir estructuras ocultas, topologías o patrones intrínsecos en los datos[cite: 2].
*   **Riesgo de Gobierno:** Al no existir una "verdad base" (*ground truth*) etiquetada, la validación de la equidad y la corrección del resultado es altamente compleja de auditar.
*   **Tareas típicas:**
    *   **Clustering (Agrupamiento):** Agrupa observaciones por similitud (ej. Segmentación de perfiles de usuarios). *Algoritmos:* K-Means, DBSCAN.
    *   **Reducción de Dimensionalidad:** Comprime variables preservando la varianza (ej. PCA).
    *   **Detección de anomalías:** Identificar comportamientos desviados (puede ser no supervisado si no hay histórico etiquetado de anomalías).

#### 2.3. Otros Paradigmas Reconocidos (ISO/IEC 22989)

*   **Aprendizaje Semi-supervisado:** Combina un pequeño volumen de datos etiquetados con un gran volumen de datos no etiquetados. Es una categoría formal, no una "mezcla informal"[cite: 2].
*   **Aprendizaje por Refuerzo:** Un agente aprende a tomar decisiones interactuando con un entorno, maximizando una función de recompensa mediante ensayo y error, sin depender de un dataset estático pre-etiquetado[cite: 2].

### 3. Procesamiento de Lenguaje Natural (PLN / NLP)

El PLN (o NLP) es un dominio de la IA (reconocido en la sección 9.2 de la ISO/IEC 22989) dedicado a que los sistemas informáticos analicen, comprendan y generen lenguaje humano[cite: 2]. No se limita a los grandes modelos de lenguaje (LLMs); incluye múltiples subtareas clásicas.

#### 3.1. Subáreas funcionales

*   **NLU (*Natural Language Understanding*):** Comprensión del lenguaje. Implica extraer significado, intenciones, sentimiento y entidades (NER - *Named Entity Recognition*).
*   **NLG (*Natural Language Generation*):** Generación de lenguaje. Implica redactar texto coherente a partir de datos o instrucciones. (Los LLMs modernos realizan ambas funciones integradas).

#### 3.2. Preprocesamiento (Conceptos de auditoría técnica)

La forma en que se limpia el texto afecta a los sesgos y a la precisión del modelo:
*   **Tokenización:** División del texto en unidades operables computacionalmente (palabras, subpalabras, caracteres). Un *token* no es sinónimo absoluto de "palabra".
*   **Stemming (Truncamiento):** Algoritmo heurístico (fuerza bruta) que recorta prefijos o sufijos para obtener una raíz estática (ej. "resoluciones" $\rightarrow$ "resoluc"). Es rápido pero genera palabras inexistentes.
*   **Lematización:** Análisis morfológico apoyado en diccionarios lingüísticos que transforma la palabra a su lema canónico o de diccionario (ej. "fueron" $\rightarrow$ "ir"). Es más preciso y costoso computacionalmente.

#### 3.3. Representación Vectorial

Para que un modelo matemático procese texto, este debe ser convertido a números.
*   **One-hot encoding:** Vectores dispersos llenos de ceros con un solo '1'. No capturan significado.
*   **Embeddings:** Representaciones vectoriales densas en un espacio multidimensional continuo. Las palabras con significado o contexto similar están geométricamente cerca. *Riesgo de Gobierno:* Los embeddings entrenados en corpus históricos de internet capturan y codifican matemáticamente sesgos sociales discriminatorios, requiriendo auditoría específica.

### 4. Conceptos de MLOps (Perspectiva de Gobierno)

**MLOps (*Machine Learning Operations*)** es la extensión de las prácticas DevOps aplicadas a los sistemas de aprendizaje automático. Para un perfil de Gobierno de IA (P02), MLOps es el **marco de infraestructura y procesos que hace posible la trazabilidad, la auditoría y el cumplimiento normativo** de un sistema en producción.

#### 4.1. Artefactos Gestionados (Diferencia con DevOps)

Mientras que DevOps se centra en versionar y desplegar código, MLOps requiere el gobierno versionado de un triplete interdependiente:
1.  **Código** (algoritmos y pipelines).
2.  **Modelos** (ficheros de pesos, versionados en un *Model Registry*).
3.  **Datos** (datasets de entrenamiento/validación y características en un *Feature Store*). Esto garantiza el linaje del dato (*Data Provenance*), esencial para auditorías del AI Act.

#### 4.2. Fases Integradas en MLOps (CI/CD/CT)

Según los niveles de madurez consolidados en la industria (ej. Google Cloud)[cite: 2]:
*   **CI (Integración Continua):** No solo ejecuta tests de código, sino que incluye pruebas de calidad de datos, validación de esquemas y evaluación de métricas del modelo candidato.
*   **CD (Despliegue Continuo):** Automatiza el despliegue del servicio de inferencia o del pipeline de predicción de forma segura.
*   **CT (Entrenamiento Continuo - *Continuous Training*):** Es el **pilar diferencial** de MLOps. Es la automatización del reentrenamiento del modelo en producción cuando se detecta degradación o llegan nuevos datos[cite: 2].

#### 4.3. Degradación del Modelo (*Drift*) y Monitorización

A diferencia del software tradicional (que solo falla por *bugs* en el código), un modelo de ML puede degradarse silenciosamente en producción porque el mundo real cambia, perdiendo precisión y equidad. Monitorizar este fenómeno es crítico para el gobierno.

*   **Data Drift (Deriva de datos o *Covariate Shift*):** Ocurre cuando cambia la distribución estadística de las variables de entrada ($X$) respecto a los datos con los que se entrenó el modelo. El contexto cambia, pero la regla de negocio no. *Ejemplo: Un modelo entrenado con perfiles jóvenes empieza a recibir solicitudes de un grupo demográfico envejecido.*
*   **Concept Drift (Deriva de concepto):** Ocurre cuando cambia la relación estadística subyacente entre las entradas ($X$) y la variable objetivo a predecir ($Y$). La "verdad" o regla de negocio ha cambiado. *Ejemplo: Cambia la legislación y lo que antes era un expediente "Aprobado", ahora debe predecirse como "Denegado" con los mismos datos de entrada.*

## Conceptos que suelen preguntarse

| Concepto | Realidad Técnica / Normativa | Distractor típico en examen |
| :--- | :--- | :--- |
| **Regresión Logística** | Es un algoritmo supervisado de **Clasificación**. | "Es un algoritmo para predecir valores numéricos continuos". |
| **IA vs. Machine Learning** | Relación jerárquica: ML es un subconjunto de IA. | "Son términos sinónimos e intercambiables según ISO". |
| **ML vs. Deep Learning** | ML requiere *Feature Engineering* (manual). DL realiza *Feature Learning* (automático, en "caja negra"). | "El DL es más transparente y fácil de auditar que el ML clásico". |
| **Supervisado vs. No Supervisado** | Supervisado: Tiene etiquetas/variable objetivo ($Y$). No supervisado: Busca patrones sin etiquetas predefinidas. | "El no supervisado requiere validación constante de un operario humano". |
| **Stemming vs. Lematización** | Stemming = recorte por reglas heurísticas. Lematización = análisis morfológico usando diccionario. | "Ambos procesos garantizan que la palabra resultante exista en el idioma". |
| **Data Drift vs. Concept Drift** | Data Drift = Cambia la entrada ($X$). Concept Drift = Cambia la relación subyacente ($X \rightarrow Y$). | "El Data Drift se soluciona reiniciando el servidor de la base de datos". |
| **CT (Continuous Training)** | Fase exclusiva de MLOps para reentrenar modelos ante el *drift*. | "CT significa Continuous Testing y ya existía en DevOps tradicional". |

## Posibles preguntas tipo test

**Pregunta 1.** Desde la perspectiva del gobierno de un sistema de IA en producción, ¿qué fenómeno se está produciendo si las distribuciones estadísticas de las variables de entrada que envían los ciudadanos cambian con el tiempo respecto al conjunto de entrenamiento original, pero la regla de negocio que define la salida correcta no ha variado?
A. Deriva de concepto (*Concept Drift*).
B. Deriva de datos (*Data Drift*).
C. Fuga de datos (*Data Leakage*).
D. Sobreajuste algorítmico (*Overfitting*).
**Respuesta correcta: B.** (Si solo cambian las características de la entrada $X$, se trata de deriva de datos. Si cambiase la regla que asocia $X$ con $Y$, sería deriva de concepto).

**Pregunta 2.** De acuerdo con el Reglamento (UE) 2024/1689 (Ley de IA), ¿cuál de los siguientes elementos es un requisito definitorio fundamental para considerar a un software como un "sistema de inteligencia artificial" sujeto a dicha regulación?
A. Estar programado exclusivamente mediante redes neuronales profundas.
B. Funcionar bajo un paradigma de total ausencia de supervisión humana (*Human-out-of-the-loop*).
C. La capacidad de inferir, a partir de información de entrada, la manera de generar resultados como predicciones o decisiones.
D. Su ejecución obligatoria en infraestructuras de computación en la nube (Cloud).
**Respuesta correcta: C.** (La inferencia es el elemento central de la definición legal en el Art. 3.1, abarcando tanto el ML como enfoques basados en lógica/conocimiento)[cite: 2].

**Pregunta 3.** Si la Agencia para la Administración Digital entrena un modelo utilizando un conjunto de datos históricos que contiene miles de resoluciones previamente clasificadas por funcionarios como "Favorables" o "Desfavorables", con el objetivo de automatizar esta tarea, ¿qué paradigma de aprendizaje está aplicando según la clasificación de la ISO/IEC 22989?
A. Aprendizaje por refuerzo.
B. Aprendizaje no supervisado de agrupamiento (*Clustering*).
C. Aprendizaje semi-supervisado.
D. Aprendizaje supervisado de clasificación.
**Respuesta correcta: D.** (Existe un conjunto de datos con una variable objetivo etiquetada previamente y se busca predecir una categoría discreta).

**Pregunta 4.** En el contexto de MLOps como marco de gobierno para el ciclo de vida de la IA, ¿qué práctica técnica diferencial se añade respecto al paradigma DevOps tradicional del software para hacer frente a la degradación probabilística de los modelos?
A. La Integración Continua (CI) de pruebas unitarias de código.
B. El Despliegue Continuo (CD) mediante contenedores.
C. El Entrenamiento Continuo (CT - Continuous Training) automatizado.
D. El uso de repositorios de control de versiones Git.
**Respuesta correcta: C.** (El reentrenamiento continuo es la respuesta operativa de MLOps al problema del *Drift* de los modelos)[cite: 2].

**Pregunta 5.** En el preprocesamiento de textos dentro del Procesamiento de Lenguaje Natural (PLN), ¿cuál es la principal diferencia funcional entre las técnicas de *Stemming* y Lematización de cara a la calidad del dato?
A. No existe diferencia funcional, son sinónimos definidos por el estándar ISO.
B. El *Stemming* aplica recortes heurísticos rápidos que pueden generar pseudopalabras, mientras que la Lematización emplea diccionarios morfológicos para extraer lemas válidos.
C. La Lematización es un proceso estadístico de *Machine Learning*, mientras que el *Stemming* solo se usa en redes neuronales.
D. El *Stemming* requiere altos recursos computacionales, siendo la Lematización la técnica más ligera y rápida.
**Respuesta correcta: B.**

## Normativa o fuentes relacionadas

*   **Reglamento (UE) 2024/1689** del Parlamento Europeo y del Consejo (Ley de IA). *Fuente fundamental para las definiciones legales (Art. 3) y los requisitos de gobierno de datos de entrenamiento.*
*   **ISO/IEC 22989:2022** (*Information technology — Artificial intelligence concepts and terminology*). Estándar internacional ratificado para la taxonomía técnica (IA, ML, paradigmas de aprendizaje, PLN)[cite: 2].
*   **NIST AI RMF 1.0 / ISO/IEC 23894:2023**. Marcos de gestión de riesgos de Inteligencia Artificial que contextualizan el uso de MLOps como mecanismo de control, medición y gobernanza.

## Dudas o puntos pendientes

*   **Alcance de los algoritmos clásicos en la Ley de IA:** Aunque técnicamente un algoritmo de regresión logística o un árbol de decisión simple pertenecen al Machine Learning clásico, a efectos de examen del perfil de Gobierno (P02), el opositor debe recordar que **estos sistemas simples también quedan subsumidos bajo la definición legal de "Sistema de IA" del AI Act** si cumplen el criterio de inferencia. El reglamento europeo adopta una visión tecnológicamente neutra.
*   **Taxonomía exacta de MLOps:** Aunque los pilares CI/CD/CT provienen de la documentación técnica consolidada de la industria (ej. *Google Cloud Architecture Center*)[cite: 2], es la conceptualización más extendida a falta de un estándar normativo ISO específico y exclusivo que certifique los niveles de madurez de MLOps.