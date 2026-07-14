---
id: "cm-ad-ia-p01-tema-002-ia-generativa"
title: "IA Generativa"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/ia"
profiles:
  - "p01-consultor-sistemas-informacion-ia"
official_profile: "P01 - Consultor de Sistemas de Información - IA Aplicada al Ciclo de Vida del Software"
official_topic: "Tema 2. IA Generativa"
source_ids:
tags:
  - "inteligencia-artificial"
  - "ia-generativa"
  - "llm"
  - "tokenizacion"
  - "embeddings"
  - "transformer"
  - "rag"
  - "llmops"
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

# IA Generativa

## Encaje en la convocatoria

Este tema corresponde al **Tema 2. IA Generativa** del Anexo 3 de la Resolución 352/2026 (BOCM 11/06/2026), dentro de las áreas de conocimiento objeto de la Fase 1 de oposición para los perfiles TIC (A2/Grupo IV) de la Agencia para la Administración Digital de la Comunidad de Madrid. El tema aparece tanto para el perfil **P01 (IA aplicada al ciclo de vida del software)** como para el perfil **P02 (Gobierno de IA)**.

El epígrafe oficial incluye cinco bloques: **LLMs: tokenización, embeddings y predicción**, **arquitectura transformer**, **Generación Aumentada por Recuperación (RAG)**, **usos y limitaciones** y **conceptos de LLMOps**. Se apoya directamente en el Tema 1 (Fundamentos) y conecta con el Tema 3 (IA Agéntica).

La prueba es tipo test con penalización, por lo que el enfoque debe ser estrictamente técnico y normativo, evitando divulgación genérica. Es crucial dominar con precisión las diferencias entre **modelo fundacional**, **modelo de IA de uso general (GPAI)**, **RAG vs. Fine-tuning**, **arquitecturas secuenciales vs. atención paralela**, y las métricas propias de **LLMOps**.

## Ideas clave

1. **IA generativa:** Capacidad de un sistema para producir contenido nuevo (texto, código, imagen, etc.) a partir de patrones aprendidos en un proceso de entrenamiento masivo.
2. **Tokens y Embeddings:** Los LLM no procesan "palabras". Procesan **tokens** (subunidades de texto) que se representan matemáticamente en un espacio multidimensional continuo llamado **embedding**, capturando su semántica.
3. **Predicción Autorregresiva:** El mecanismo central de generación de texto es la predicción probabilística del siguiente token: $P(token_t | token_1, \dots, token_{t-1})$.
4. **Arquitectura Transformer (2017):** Revolucionó la IA al eliminar el procesamiento secuencial de las redes RNN/LSTM. Su mecanismo de **Autoatención (Self-Attention)** permite procesar secuencias en paralelo, capturando dependencias a largo plazo.
5. **RAG (Generación Aumentada por Recuperación):** Patrón que inyecta conocimiento externo y veraz en el contexto (prompt) en tiempo de inferencia, mitigando alucinaciones **sin necesidad de reentrenar** el modelo.
6. **RAG vs. Fine-Tuning:** RAG modifica el *contexto* temporalmente. El *Fine-Tuning* (ajuste fino) modifica los *pesos* neuronales del modelo de forma permanente.
7. **LLMOps y PEFT/LoRA:** A diferencia de MLOps (donde se suele entrenar desde cero), LLMOps gestiona modelos preentrenados masivos. Para adaptarlos con bajo coste computacional se usan técnicas como **LoRA (Low-Rank Adaptation)**.
8. **Marco Normativo (AI Act):** El Reglamento (UE) 2024/1689 distingue estrictamente entre "modelo de IA de uso general" (el componente subyacente entrenado masivamente) y el "sistema de IA de uso general" (el producto final integrado que se despliega).

## Desarrollo

### 1. LLMs: tokenización, embeddings y predicción

#### 1.1. LLM y Modelo Fundacional

Un **LLM (Large Language Model)** es un modelo de lenguaje de gran escala entrenado mediante aprendizaje autosupervisado sobre grandes corpus textuales. Se engloba dentro de los **modelos fundacionales**: arquitecturas entrenadas a tal escala que resultan adaptables a una amplísima variedad de tareas posteriores.

#### 1.2. Tokenización

La **tokenización** es el proceso de dividir una secuencia de texto en unidades mínimas operables (tokens) y convertirlas a identificadores numéricos discretos.
* **Algoritmos técnicos estándar:** *Byte Pair Encoding (BPE)*, *WordPiece*, *SentencePiece*.
* **Características operativas:** Un token no equivale a una palabra. En español o en terminología técnica compleja, una sola palabra puede dividirse en 2 o 3 tokens subléxicos.
* **Context Window (Ventana de contexto):** El límite estricto de memoria a corto plazo del modelo, medido en tokens. Incluye el *prompt* del sistema, el historial, el contexto RAG y la respuesta generada.

#### 1.3. Embeddings

Un **embedding** es una representación matemática vectorial densa de los tokens en un espacio multidimensional continuo.
* **Función:** Capturan la semántica contextual. Vectores próximos en este espacio representan conceptos semánticamente similares.
* **Métrica de evaluación:** La similitud semántica en recuperación (RAG) se mide típicamente mediante la **Similitud del Coseno** o el Producto Escalar (Dot Product).

#### 1.4. Predicción del siguiente token y Decodificación

En la inferencia de un LLM autorregresivo, la tarea es predecir el siguiente token. La salida bruta del modelo son *logits*, que se transforman en una distribución de probabilidad mediante la función $Softmax$.

La selección final del token se controla mediante parámetros de decodificación:
* **Temperatura:** Ajusta la aleatoriedad.
  * **Temperatura = 0:** Decodificación determinista o *Greedy* (codiciosa). Elige siempre el token más probable. Ideal para código, SQL o consultas normativas.
  * **Temperatura > 0:** Aplana la curva de probabilidad, permitiendo selecciones subóptimas pero generando textos más "creativos" y variados.
* **Top-k y Top-p (Nucleus Sampling):** Restringen el abanico de tokens candidatos antes del muestreo, limitando a los $k$ más probables o a aquellos cuya probabilidad acumulada alcanza $p$.

### 2. Arquitectura Transformer

Introducida en el documento técnico *"Attention Is All You Need"* (Vaswani et al., 2017), sustituyó a las arquitecturas recurrentes (RNN) y convolucionales en el procesamiento de secuencias.

#### 2.1. Ventaja estructural: Paralelización

Las RNN/LSTM procesaban el texto secuencialmente (palabra por palabra), impidiendo la paralelización masiva y perdiendo el contexto a largo plazo. Los Transformers procesan todos los tokens **en paralelo**.

#### 2.2. Componentes Clave

* **Self-attention (Autoatención):** Mecanismo matemático que permite al modelo, al evaluar un token, ponderar la relevancia de *todos los demás tokens de la secuencia simultáneamente*. Conceptualmente se basa en vectores *Query (Q)*, *Key (K)* y *Value (V)*:
  $$Attention(Q, K, V) = softmax\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$
* **Multi-head attention:** Ejecuta varios mecanismos de atención en paralelo, permitiendo al modelo capturar simultáneamente distintas relaciones sintácticas y semánticas.
* **Codificación posicional (Positional Encoding):** Al procesarse en paralelo, la arquitectura carece de noción de orden. Se inyecta información matemática (fórmulas senoidales) en los embeddings de entrada para indicar la posición secuencial de cada token.

#### 2.3. Tipos de Arquitectura

* **Encoder-only (ej. BERT):** Atención bidireccional. Excelente para clasificación de texto, análisis de sentimiento y generación de embeddings para búsqueda.
* **Decoder-only (ej. GPT, LLaMA):** Atención unidireccional (causal). Excelente para la generación autorregresiva de texto.
* **Encoder-Decoder (ej. T5):** Tradicionalmente usado para traducción o resúmenes.

### 3. Generación Aumentada por Recuperación (RAG)

El **RAG (Retrieval-Augmented Generation)** es una arquitectura que combina las capacidades de generación de un LLM con un sistema de recuperación de información independiente y externo (NIST AI 100-2e2025).

#### 3.1. Objetivo principal

Inyectar contexto fáctico, actualizado o privado al LLM en tiempo de inferencia para mitigar alucinaciones y proveer trazabilidad de fuentes, **sin modificar los pesos ni reentrenar el modelo**.

#### 3.2. Fases técnicas de RAG

1. **Ingesta e Indexación:** Los documentos se dividen en fragmentos lógicos (*Chunking*), se vectorizan mediante un modelo de embeddings y se almacenan en una base de datos vectorial (Vector Store).
2. **Recuperación (*Retrieval*):** La consulta del usuario se vectoriza. Se realiza una búsqueda (Vectorial, Léxica basada en palabras clave como BM25, o Híbrida) para encontrar los *chunks* más relevantes. Suele aplicarse un *Reranker* para mejorar el orden de relevancia.
3. **Generación:** El sistema construye un *prompt* que incluye la instrucción del sistema, la consulta del usuario y los *chunks* recuperados, indicando al LLM que base su respuesta exclusivamente en dicho contexto.

#### 3.3. RAG vs. Fine-Tuning

| Característica | RAG (Retrieval-Augmented Generation) | Fine-Tuning (Ajuste Fino) |
| :--- | :--- | :--- |
| **Objetivo** | Añadir conocimiento externo / fáctico | Modificar comportamiento o formato/estilo |
| **Conocimiento** | Dinámico (cambia la base de datos) | Estático (incorporado a los pesos) |
| **Privacidad/ACL** | Permite filtrar contexto según permisos de usuario | Difícil aislar el conocimiento una vez aprendido |
| **Alucinaciones** | Las reduce significativamente (mediante *Grounding*) | No garantiza exactitud fáctica |
| **Coste** | Bajo (requiere almacenamiento vectorial) | Alto (requiere entrenamiento GPU) |

### 4. Usos y Limitaciones

#### 4.1. Limitaciones Técnicas y Operativas

* **Alucinaciones (Confabulaciones):** Respuestas sintácticamente perfectas pero factualmente incorrectas o inventadas. Producto de la naturaleza estadística y probabilística del modelo.
* **Olvido Catastrófico (*Catastrophic Forgetting*):** Riesgo al realizar *Fine-Tuning* continuo; el modelo puede sobreescribir y perder los conocimientos latentes adquiridos en su preentrenamiento masivo original.
* **Límites de la Ventana de Contexto:** Si la información inyectada mediante RAG o el historial exceden el límite de tokens, el sistema truncará información crítica.
* **Naturaleza "Caja Negra":** Alta opacidad técnica; dificultad de explicabilidad matemática directa sobre por qué se generó un output específico (riesgo tipificado en NIST AI RMF).

#### 4.2. Marco Normativo (Reglamento UE 2024/1689 - AI Act)

La Ley de Inteligencia Artificial establece distinciones jurídicas críticas que son materia de examen:
* **Modelo de IA de uso general (Art. 3.63):** Modelo entrenado con gran volumen de datos, que muestra generalidad significativa, capaz de ejecutar una amplia gama de tareas y de integrarse en sistemas posteriores. **Distractor jurídico:** Modelos usados exclusivamente para investigación o prototipado antes de su comercialización quedan excluidos de esta definición.
* **Sistema de IA de uso general (Art. 3.66):** El sistema final desplegable, basado en un modelo de uso general, con capacidad de servir a diversos fines directamente o integrado.

### 5. Conceptos de LLMOps

**LLMOps (Large Language Model Operations)** adapta las prácticas de MLOps al ciclo de vida de los LLMs. A diferencia del MLOps clásico (centrado en el ciclo completo de entrenamiento y métricas cuantitativas como *Accuracy*), LLMOps asume habitualmente el consumo de un modelo preentrenado masivo y se centra en su orquestación y evaluación cualitativa.

#### 5.1. Adaptación y Entrenamiento Eficiente

Si el *Prompt Engineering* o RAG son insuficientes, se recurre a modificar los pesos. Dado el tamaño masivo de los modelos, se utiliza:
* **PEFT (Parameter-Efficient Fine-Tuning):** Familia de técnicas para ajustar LLMs en hardware modesto.
* **LoRA (Low-Rank Adaptation):** Técnica estrella dentro de PEFT. Congela los pesos originales del modelo preentrenado e inyecta pequeñas matrices entrenables de rango inferior en las capas de atención. Reduce drásticamente el coste computacional.

#### 5.2. Alineamiento (Alignment)

* **RLHF (Reinforcement Learning from Human Feedback):** Técnica crucial que emplea evaluadores humanos para entrenar un "Modelo de Recompensa", el cual optimiza al LLM (usando algoritmos como PPO) para que sus salidas sean útiles, honestas e inofensivas.

#### 5.3. Evaluación en LLMOps

La evaluación cualitativa es compleja y requiere métricas específicas:
* **Métricas clásicas NLP:** **Perplejidad** (mide la incertidumbre del modelo al predecir), **BLEU** (coincidencia de n-gramas, clásico en traducción), **ROUGE** (clásico para evaluación de resúmenes).
* **Evaluación RAG (Ej. framework RAGAS):** Mide la relevancia de la recuperación, la fidelidad de la respuesta al contexto (*Groundedness*) y la respuesta frente al sesgo.

#### 5.4. Gestión de Riesgos y Seguridad Operacional

* **Prompt Injection y Jailbreaking:** Riesgo de que la entrada del usuario (o de un documento en RAG) contenga instrucciones maliciosas que desvíen al modelo de sus directrices del sistema.
* **Trazabilidad:** Control estricto (versionado) de modelos, *prompts* del sistema, configuraciones de recuperación y umbrales de temperatura.

## Conceptos que suelen preguntarse

| Concepto | Qué es realmente | Distractor típico en examen |
| :--- | :--- | :--- |
| **Token vs. Palabra** | El token es la subunidad del tokenizador. | "Un token siempre equivale a una palabra". |
| **Transformer vs. RNN** | Transformer procesa en paralelo usando *Self-Attention*. | "Transformer procesa textos palabra por palabra secuencialmente". |
| **RAG** | Inyecta información en el *prompt* en tiempo de inferencia. | "RAG reentrena los parámetros del modelo con datos corporativos". |
| **Temperatura = 0** | Decodificación *Greedy* (determinista). | "Garantiza al 100% que la respuesta será cierta/verdadera". |
| **Fine-Tuning vs. LoRA** | LoRA es una técnica eficiente de Fine-Tuning (PEFT) que inyecta matrices menores y congela el resto. | "LoRA entrena todos los parámetros del modelo base desde cero". |
| **Modelo vs. Sistema GPAI** | Modelo es el componente matemático (Art. 3.63 AI Act); Sistema es el software final integrado (Art. 3.66). | "Cualquier LLM es jurídicamente un Sistema de Alto Riesgo automáticamente". |

## Posibles preguntas tipo test

**Pregunta 1.** En la arquitectura de un modelo basado en Transformers, ¿qué mecanismo permite evaluar la importancia de cada token de una frase con respecto a todos los demás de forma simultánea y paralela?

A. El truncamiento heurístico de raíces (Stemming).

B. El mecanismo de Autoatención (Self-Attention).

C. Las Redes Neuronales Recurrentes (RNN).

D. El ajuste del parámetro de Perplejidad.

**Respuesta correcta: B.** (La Autoatención pondera relaciones en toda la secuencia a la vez, resolviendo el cuello de botella secuencial de las RNN).

**Pregunta 2.** Según el Art. 3 del Reglamento (UE) 2024/1689, un modelo de lenguaje masivo usado exclusivamente para investigación y creación de prototipos antes de su comercialización:

A. Se considera modelo de IA de uso general con riesgo sistémico.

B. Queda excluido de la definición legal de modelo de IA de uso general.

C. Se considera automáticamente un sistema de IA de alto riesgo.

D. Requiere marcado CE obligatorio inmediato.

**Respuesta correcta: B.**

**Pregunta 3.** La Agencia para la Administración Digital desea integrar un LLM corporativo que consulte en tiempo real normativas publicadas en el BOCM diario para responder a ciudadanos, controlando los permisos de acceso y sin coste de reentrenamiento. La técnica de arquitectura recomendada es:

A. Continuous Pre-training diario desde cero.

B. Fine-Tuning profundo con todos los PDFs.

C. Generación Aumentada por Recuperación (RAG).

D. Ajuste fino eficiente mediante LoRA (Low-Rank Adaptation).

**Respuesta correcta: C.** (RAG consulta la información dinámica en tiempo de inferencia y permite aplicar control de acceso en la fase de búsqueda, sin reentrenar ni ajustar pesos neuronales).

**Pregunta 4.** Si al invocar la API de inferencia de un LLM establecemos el parámetro "Temperatura" en un valor de 0 (cero), el comportamiento esperado del sistema será:

A. Generar textos aleatorios con alta variabilidad léxica.

B. Volverse altamente determinista (Greedy decoding), eligiendo siempre el token con mayor probabilidad.

C. Devolver un error de saturación de GPU (Out of Memory).

D. Reducir la ventana de contexto al mínimo permitido.

**Respuesta correcta: B.**

**Pregunta 5.** ¿Cuál es la diferencia principal entre las técnicas de Fine-Tuning y el uso de RAG en aplicaciones con LLMs?

A. RAG modifica los pesos neuronales del modelo; el Fine-Tuning no.

B. RAG inyecta conocimiento temporal en el contexto durante la inferencia; Fine-Tuning ajusta permanentemente los pesos matemáticos del modelo.

C. RAG solo se utiliza en modelos Encoder-only; Fine-Tuning en Decoder-only.

D. No existe diferencia, son términos sinónimos definidos por el estándar NIST.

**Respuesta correcta: B.**

**Pregunta 6.** Dentro del ciclo de vida LLMOps, si requerimos ajustar el estilo o la estructura de respuesta de un LLM muy pesado pero carecemos de grandes recursos computacionales, la técnica más adecuada para "congelar" el modelo base e inyectar pequeñas matrices entrenables es:

A. RAG Vectorial.

B. RLHF estocástico.

C. LoRA (Low-Rank Adaptation).

D. Tokenización BPE.

**Respuesta correcta: C.** (LoRA es la técnica estándar de Parameter-Efficient Fine-Tuning (PEFT) para estos escenarios).

**Pregunta 7.** ¿Qué afirmación sobre el límite de la "Ventana de Contexto" (Context Window) de un LLM es correcta?

A. Se mide en Megabytes exactos de texto procesado.

B. Equivale a una base de datos relacional ilimitada para el modelo.

C. Determina la cantidad finita máxima de tokens (entrada + salida) que el modelo puede procesar en una inferencia.

D. Aumentar la ventana de contexto elimina automáticamente las alucinaciones del modelo.

**Respuesta correcta: C.**

**Pregunta 8.** En el marco de LLMOps y evaluación de respuestas de lenguaje natural, ¿qué métrica suele utilizarse tradicionalmente para medir el grado de incertidumbre o duda de un modelo al predecir la siguiente palabra en una secuencia?

A. Similitud del Coseno (Cosine Similarity).

B. Perplejidad (Perplexity).

C. Exactitud (Accuracy).

D. Distancia Euclidiana.

**Respuesta correcta: B.**

## Normativa o fuentes relacionadas

* **Reglamento (UE) 2024/1689 del Parlamento Europeo y del Consejo (Ley de Inteligencia Artificial):** Especialmente su Título VIII y el Artículo 3 (definiciones 63, 64 y 66 relativas a modelos y sistemas de IA de uso general - GPAI).
* **NIST AI 100-2e2025:** Glosario NIST CSRC, que asienta la definición técnica de *Retrieval-Augmented Generation (RAG)*.
* **NIST AI 600-1:** *Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile* (identificación de riesgos característicos como confabulaciones, propiedad intelectual, seguridad).
* **ISO/IEC TR 24372:2021:** *Information technology — Artificial intelligence (AI) — Overview of computational approaches for AI systems.* (Refiere a las arquitecturas base de ML).
* **Vaswani, A. et al. (2017):** *"Attention Is All You Need"*, NeurIPS. (Publicación científica fundacional de la arquitectura Transformer).

## Dudas o puntos pendientes

* **Grounding vs. RAG:** En algunos exámenes o documentación técnica comercial, se emplea el término *Grounding* (enraizamiento fáctico) como sinónimo de RAG. Rigurosamente, el *Grounding* es un objetivo o concepto metodológico (vincular la generación a datos fehacientes), mientras que RAG es el patrón de arquitectura técnica para lograrlo.
* **Falta de norma técnica pura para LLMOps:** La disciplina de LLMOps, al ser emergente, carece de un estándar oficial único (tipo ISO/IEC o UNE específico hasta la fecha de la convocatoria) que establezca taxativamente sus límites frente a MLOps clásico, por lo que su definición se deriva de las guías de los principales proveedores *Cloud* y prácticas de la industria.
