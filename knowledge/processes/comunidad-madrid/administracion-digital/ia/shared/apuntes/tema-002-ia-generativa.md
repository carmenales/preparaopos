---
id: "cm-ad-ia-tema-002-ia-generativa"
title: "IA Generativa"
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
  - "gobierno-ia"
  - "riesgos-ia"
created_at: "2026-07-17"
last_reviewed: null
ai_generated: true
ai_sources:
  - "chatgpt"
  - "perplexity"
  - "gemini"
needs_human_review: true
---

# IA Generativa

## Encaje en la convocatoria

Este tema corresponde al **Tema 2 del Anexo 3** de la Resolución 352/2026 (BOCM 11/06/2026), dentro de las áreas de conocimiento objeto de la Fase 1 de oposición, común a los perfiles **P01: Consultor de Sistemas de Información - IA Aplicada al Ciclo de Vida del Software** y **P02: Consultor de Sistemas de Información - Especialista en Gobierno de IA** de la Agencia para la Administración Digital de la Comunidad de Madrid.[file:151]

El epígrafe oficial incluye cinco bloques: **LLMs: tokenización, embeddings y predicción**, **arquitectura transformer**, **Generación Aumentada por Recuperación (RAG)**, **usos y limitaciones** y **conceptos de LLMOps**.[file:151] Se apoya directamente en el Tema 1 (Fundamentos) y conecta con el Tema 3 (IA Agéntica). El contenido base es común a ambos perfiles, pero el enfoque de estudio difiere: para **P01** el énfasis recae en la mecánica técnica y la implementación (algoritmos de tokenización, decodificación, PEFT/LoRA), mientras que para **P02** el estudio se traslada a las **implicaciones de gobernanza, riesgo, cumplimiento y auditoría** de estos sistemas en la Administración Pública.[file:151]

## Ideas clave

1. **IA Generativa vs. Discriminativa:** La IA generativa produce contenido nuevo (texto, código, imagen) basándose en distribuciones de probabilidad aprendidas en un entrenamiento masivo; la IA discriminativa se centra en tareas de clasificación o predicción (ej. fraude/no fraude). Ambas presentan riesgos distintos de auditoría y se tratan de forma diferenciada en marcos como NIST AI RMF.[file:151]
2. **Tokens y Embeddings:** Los LLM no procesan “palabras”, sino **tokens** (subunidades de texto) que se representan matemáticamente en un espacio multidimensional continuo mediante **embeddings**, capturando su semántica; los tokens consumidos determinan el coste computacional (*FinOps*) y el límite de la ventana de contexto, mientras que los embeddings heredan los sesgos del corpus de entrenamiento.[file:151]
3. **Predicción Autorregresiva:** El mecanismo central de generación de texto es la predicción probabilística del siguiente token, calculada mediante la función *softmax* sobre los *logits* de salida y condicionada por el contexto previo; la calidad de esta predicción se evalúa con métricas como la perplejidad.[file:151]
4. **Arquitectura Transformer (2017):** Sustituyó a las redes recurrentes (RNN/LSTM), eliminando el procesamiento estrictamente secuencial; su núcleo es el mecanismo de **Autoatención (Self‑Attention)** con vectores Q, K y V y codificación posicional, que permite paralelización masiva y modelado de dependencias a largo alcance.[file:151]
5. **RAG (Generación Aumentada por Recuperación):** Patrón arquitectónico clave para el sector público que inyecta conocimiento externo y veraz en el contexto (prompt) en tiempo de inferencia, mitigando alucinaciones y garantizando trazabilidad documental (*groundedness*), sin modificar los pesos del modelo; integra búsqueda léxica y vectorial.[file:151]
6. **RAG vs. Fine‑Tuning:** RAG modifica el *contexto* temporalmente y aporta trazabilidad y control de acceso (ACL) sin reentrenar el modelo, mientras que el *Fine‑Tuning* modifica los *pesos* neuronales de forma permanente, dificultando la auditoría de qué datos se han memorizado y el ejercicio del derecho de supresión en RGPD.[file:151]
7. **LLMOps, PEFT/LoRA y QLoRA:** LLMOps es el subconjunto de MLOps que gestiona modelos fundacionales preentrenados masivos, desplazando el foco desde el entrenamiento clásico hacia la gestión de *prompts* (tratados como código), guardrails, evaluación factual (RAGAS, groundedness) y control de costes por tokens; PEFT incluye técnicas como **LoRA** y **QLoRA** que permiten adaptar modelos con bajo coste computacional.[file:151][web:175]
8. **Marco Normativo (AI Act, AESIA, OWASP):** El Reglamento (UE) 2024/1689 distingue entre “modelo de IA de uso general” (Art. 3.63) y “sistema de IA de uso general” (Art. 3.66), fija obligaciones de transparencia (Art. 50) y requisitos adicionales para modelos GPAI de riesgo sistémico, mientras que AESIA y AEPD definen principios de transparencia y explicabilidad y OWASP establece catálogos de riesgos para LLM y aplicaciones agénticas.[file:151][web:166]

## Desarrollo

### 1. LLMs: tokenización, embeddings y predicción

Un **LLM (Large Language Model)** es un modelo estadístico de gran escala entrenado mediante aprendizaje autosupervisado sobre grandes corpus textuales, diseñado para modelar secuencias de lenguaje; se considera **modelo fundacional** cuando ha sido entrenado a tal escala que resulta adaptable a una amplia variedad de tareas posteriores.[file:151]

#### 1.1. Tokenización y Token ID

La **tokenización** es el proceso de dividir una secuencia de texto en unidades mínimas operables (tokens: subpalabras, caracteres o bytes) y convertirlas en identificadores numéricos discretos (Token ID).[file:151]

- Algoritmos estándar: *Byte Pair Encoding (BPE)*, *WordPiece*, *SentencePiece*.[file:151]
- Un token no equivale necesariamente a una palabra; en español o en terminología técnica compleja una sola palabra puede dividirse en varios tokens subléxicos.[file:151]
- **Ventana de contexto (Context Window):** límite estricto de la memoria a corto plazo del modelo, medido en tokens, que incluye el prompt del sistema, el historial de conversación, el contexto RAG y la respuesta generada.[file:151]

La cantidad de tokens consumidos determina el coste computacional y condiciona cuánta información normativa o de expediente puede considerarse simultáneamente en una interacción.[file:151]

#### 1.2. Embeddings (Vectores densos)

Un **embedding** es una representación matemática vectorial densa de los tokens en un espacio multidimensional continuo, donde la proximidad geométrica captura la similitud semántica.[file:151]

- Función: capturar semántica contextual; vectores próximos representan conceptos semánticamente similares.
- Métricas típicas: similitud del coseno, producto escalar y distancia euclidiana, utilizadas en búsqueda semántica y recuperación RAG.[file:151]

Los embeddings heredan los sesgos del corpus de entrenamiento histórico, de modo que si el espacio vectorial codifica sesgos discriminatorios el sistema puede emitir respuestas sesgadas, vulnerando principios de equidad y no discriminación exigibles en la Administración.[file:151]

#### 1.3. Predicción del siguiente token y decodificación

En la **generación autorregresiva** el modelo calcula una distribución de probabilidad sobre el siguiente token condicionada por el contexto previo, normalmente aplicando la función *softmax* sobre los *logits* de salida.[file:151]

La selección final del token se controla mediante parámetros de decodificación:

- **Temperatura:** ajusta la aleatoriedad del muestreo.
  - Temperatura = 0: decodificación *Greedy* (determinista), el modelo elige siempre el token con mayor probabilidad, útil para tareas donde se requiere consistencia (código, SQL, respuestas normativas).[file:151]
  - Temperatura > 0: aplana la distribución de probabilidad permitiendo seleccionar tokens menos probables y generando textos más variados y creativos.[file:151]
- **Top‑k y Top‑P (nucleus sampling):** restringen el conjunto de tokens candidatos antes del muestreo.
  - Top‑k: se consideran únicamente los k tokens más probables.
  - Top‑P: se seleccionan los tokens cuya probabilidad acumulada alcanza el umbral P, formando un “núcleo” de probabilidad.[file:151]

Valores de Top‑P muy bajos restringen mucho el conjunto de tokens candidatos favoreciendo respuestas conservadoras, mientras que Top‑P=1 implica que no se recorta la distribución y que todos los tokens candidatos permanecen disponibles para la selección.[file:151]

### 2. Arquitectura Transformer

La arquitectura **Transformer**, introducida en *Attention Is All You Need* (Vaswani et al., 2017), sustituyó a las redes RNN/LSTM eliminando el procesamiento estrictamente secuencial y permitiendo procesar todos los tokens de la secuencia en paralelo gracias a la autoatención.[file:151]

#### 2.1. Ventaja estructural: paralelización

Las RNN/LSTM procesaban secuencias token a token, lo que impedía la paralelización masiva y dificultaba la captura de dependencias a largo plazo; los Transformers procesan todos los tokens simultáneamente, calculando relaciones entre pares de posiciones mediante atención y escalando mejor en grandes volúmenes de datos.[file:151]

#### 2.2. Autoatención (Self‑Attention): Q, K, V

Cada posición de la secuencia genera tres vectores: Query (Q), Key (K) y Value (V), y la atención se calcula mediante:

\[
Attention(Q, K, V) = softmax\left(\frac{QK^T}{\sqrt{d_k}}\right)V
\]

Los vectores Q y K se combinan para calcular los pesos de atención (relevancia relativa entre posiciones) y esos pesos se aplican sobre V para obtener una salida contextualizada donde cada token “ve” al resto con distinta importancia.[file:151]

El **multi‑head attention** ejecuta varias autoatenciones en paralelo, permitiendo al modelo capturar simultáneamente distintas relaciones sintácticas, semánticas y de dependencia a largo alcance.[file:151]

#### 2.3. Codificación posicional

Como la arquitectura procesa tokens en paralelo, necesita incorporar información de orden; para ello se añaden **positional encodings** a los embeddings originales (vectores senoidales o aprendidos) que indican la posición de cada token en la secuencia.[file:151]

#### 2.4. Tipos de arquitectura y opacidad

- **Encoder‑only (ej. BERT):** atención bidireccional sobre la secuencia completa, adecuado para tareas de comprensión, clasificación de texto, extracción de entidades y generación de embeddings semánticos.[file:151]
- **Decoder‑only (ej. GPT, LLaMA):** atención causal (unidireccional), donde cada posición sólo puede “ver” el pasado; adecuado para generación autoregresiva de texto.[file:151]
- **Encoder‑decoder (ej. T5):** combina un encoder que codifica la secuencia de entrada y un decoder que genera la salida, concebida originalmente para **traducción automática** y utilizada también para tareas de resumen.[file:151]

La enorme cantidad de parámetros y la complejidad de las interacciones de atención hacen que los Transformers se comporten como una **caja negra**, dificultando la explicabilidad causal de salidas concretas, lo que plantea retos para la transparencia y el derecho a explicación en decisiones automatizadas.[file:151]

### 3. Generación Aumentada por Recuperación (RAG)

El patrón **RAG (Retrieval‑Augmented Generation)** combina un LLM generativo con un recuperador externo de información (búsqueda léxica y vectorial) y una base de datos vectorial, de forma que la generación se “enraíza” en documentos concretos.[file:151]

#### 3.1. Objetivo principal

El objetivo es inyectar contexto fáctico, actualizado o privado en el prompt en tiempo de inferencia, mitigando alucinaciones y proporcionando trazabilidad de fuentes sin modificar los pesos del modelo, lo que facilita el cumplimiento normativo y la protección de datos.[file:151]

#### 3.2. Fases técnicas y de gobierno

1. **Ingesta y chunking:** los documentos (normativa, procedimientos, informes) se dividen en fragmentos lógicos (*chunks*) y se vectorizan mediante un modelo de embeddings, almacenándose en una base vectorial.[file:151]
2. **Recuperación híbrida:** la consulta del usuario se vectoriza y se ejecuta una búsqueda vectorial y/o léxica (ej. BM25), pudiendo combinar ambas en búsqueda híbrida para captar tanto intención semántica como coincidencias exactas de códigos o referencias.[file:151]
3. **Prompt assembly y generación:** se construye un prompt que incluye instrucciones del sistema, la pregunta del usuario y los chunks recuperados, ordenando explícitamente al modelo basar su respuesta en ese contexto.[file:151]

La fase de recuperación puede filtrarse por ACL de usuario o rol, de forma que el modelo sólo tenga acceso a documentos que el ciudadano o el empleado esté autorizado a consultar.[file:151]

#### 3.3. RAG vs Fine‑Tuning

| Característica      | RAG (Retrieval‑Augmented Generation)                          | Fine‑Tuning (Ajuste fino)                         |
| :------------------ | :------------------------------------------------------------ | :------------------------------------------------ |
| Objetivo            | Añadir conocimiento externo fáctico en tiempo de inferencia   | Modificar comportamiento, tono o estilo del modelo|
| Conocimiento        | Dinámico (base de conocimiento editable)                      | Estático (incrustado en pesos)                    |
| Privacidad / ACL    | Filtrado de contexto según permisos de usuario                | Difícil borrar conocimiento específico (RGPD)     |
| Alucinaciones       | Mitigadas mediante grounding, sin eliminación total           | No garantiza exactitud fáctica                    |
| Coste               | Moderado (infraestructura de búsqueda y vector store)         | Elevado (entrenamiento con GPU)                   |
| Auditoría           | Trazable a documentos concretos                               | Caja negra sobre qué datos se memorizaron        |

#### 3.4. Métricas de ranking: DCG, IDCG y NDCG

Para evaluar la calidad del ranking del recuperador se usan métricas basadas en relevancia y posición:

- **DCG@K (Discounted Cumulative Gain):** suma las relevancias de los documentos recuperados hasta la posición K, aplicando un descuento por posición de forma que los relevantes en primeras posiciones aportan más ganancia.[web:169]
- **IDCG@K (Ideal DCG):** DCG@K que se obtendría si el ranking fuera perfecto (todos los documentos relevantes en las posiciones óptimas); sirve de referencia para normalizar.[web:169]
- **NDCG@K:** cociente DCG@K / IDCG@K, produce un valor entre 0 y 1 que indica lo cerca que está el ranking real del ideal.[web:169]

#### 3.5. Métricas en frameworks RAG (ej. RAGAS)

Frameworks como RAGAS evalúan tanto la recuperación como la generación:

- **Answer Accuracy / Correctness:** grado en que la respuesta del LLM es factual y correcta respecto al conocimiento del dominio.[file:151]
- **Faithfulness / Groundedness:** medida de hasta qué punto la respuesta se apoya exclusivamente en la información contenida en los chunks recuperados, sin inventar datos externos.[file:151]
- **Context Recall:** proporción de fragmentos relevantes presentes en los K primeros resultados de recuperación.
- **Answer Relevance:** alineación de la respuesta con la intención de la pregunta y el contexto proporcionado.

Estas métricas permiten auditar que el sistema no se aparte de las fuentes oficiales ni introduzca sesgos no deseados.[file:151]

### 4. Usos y limitaciones

#### 4.1. Limitaciones técnicas y de gobierno

- **Alucinaciones:** generación de información plausible pero falsa o no respaldada por evidencias, derivada de la naturaleza estadística del modelo.[file:151]
- **Conocimiento estático:** sin RAG, el modelo puro está congelado en la fecha de entrenamiento y no conoce cambios normativos posteriores.[file:151]
- **Olvido catastrófico:** fine‑tuning continuado puede degradar conocimientos previos del modelo base.[file:151]
- **Límites de contexto:** si el prompt y el contexto RAG exceden la ventana de tokens, se truncará información potencialmente crítica.[file:151]
- **Caja negra:** dificultad de explicar por qué se generó una salida concreta, problema señalado en NIST AI RMF.[file:151]
- **Prompt injection directa:** el usuario introduce instrucciones maliciosas en el chat que intentan sobreescribir el system prompt.[file:151]
- **Prompt injection indirecta:** el modelo consume documentos externos (PDF, páginas web, registros) que contienen instrucciones ocultas que buscan subvertir el system prompt, especialmente crítico en arquitecturas RAG.[file:151][web:166]

#### 4.2. AI Act: modelo y sistema GPAI, transparencia

El Reglamento (UE) 2024/1689 establece:

- **Modelo de IA de uso general (Art. 3.63):** modelo entrenado con gran volumen de datos mostrando generalidad significativa y capaz de servir múltiples tareas; los modelos utilizados exclusivamente para investigación o prototipado antes de su comercialización quedan fuera de esta definición.[file:151]
- **Sistema de IA de uso general (Art. 3.66):** sistema final basado en un modelo de uso general, desplegado para diversos fines directamente o integrado en productos o servicios.[file:151]
- **Transparencia (Art. 50):** obligación de informar a las personas de que interactúan con un sistema de IA (por ejemplo, chatbots), salvo que resulte evidente dadas las circunstancias y el contexto.[file:151]
- **Riesgo sistémico:** determinados modelos GPAI que superan un umbral de capacidad de cómputo (FLOPs) deben someterse a red teaming y documentación reforzada.[file:151]

#### 4.3. OWASP Top 10 para Aplicaciones LLM

El **OWASP Top 10 for Large Language Model Applications 2025** identifica los diez riesgos de seguridad más críticos en aplicaciones que usan LLMs.[web:166][web:169]

- **LLM01: Prompt Injection**  
  Manipulación del modelo mediante prompts construidos para forzarle a ignorar instrucciones, acceder a datos, ejecutar acciones o revelar información no prevista.[web:169]
- **LLM02: Sensitive Information Disclosure**  
  Exposición de información sensible a través de prompts, respuestas o datos de entrenamiento, incluyendo PII, secretos corporativos o credenciales.[web:169]
- **LLM03: Training Data Poisoning**  
  Envenenamiento de datos de entrenamiento que introduce sesgos, comportamientos maliciosos o degradación de rendimiento.[web:169]
- **LLM04: Model Denial of Service**  
  Sobrecarga del modelo mediante consultas costosas o abusivas que consumen recursos y provocan indisponibilidad o costes incontrolados.[web:169]
- **LLM05: Supply Chain Vulnerabilities**  
  Riesgos derivados de componentes externos (modelos de terceros, bibliotecas, servicios) comprometidos que afectan a la seguridad de la aplicación.[web:169]
- **LLM06: Excessive Agency**  
  Concesión de demasiada autonomía al modelo o agente para actuar sobre sistemas externos (APIs, bases de datos, infraestructuras) sin guardrails suficientes.[web:169]
- **LLM07: System Prompt Leakage**  
  Divulgación accidental o maliciosa del prompt del sistema, lo que permite a atacantes comprender y explotar las instrucciones internas del modelo.[web:169]
- **LLM08: Vector and Embedding Weaknesses**  
  Debilidades en bases vectoriales y embeddings (ej. acceso no controlado, inferencia de datos sensibles a partir de vectores, ataques a indexadores).[web:169]
- **LLM09: Overreliance / Misinformation**  
  Dependencia excesiva de las respuestas del modelo sin verificación humana, pudiendo tomar decisiones en base a información incorrecta.[web:169]
- **LLM10: Unbounded Consumption**  
  Falta de límites sobre uso de recursos (tokens, contexto, llamadas a API) que puede derivar en gastos descontrolados o impacto operativo.[web:169]

Para la Administración Digital son especialmente relevantes LLM01, LLM02, LLM08, LLM09 y LLM10, que se relacionan con confidencialidad, integridad, disponibilidad y fiabilidad de información y servicios.[web:162]

### 5. Conceptos de LLMOps

**LLMOps (Large Language Model Operations)** adapta las prácticas de MLOps al ciclo de vida de los LLMs, asumiendo habitualmente el consumo de modelos fundacionales preentrenados y centrando la gobernanza en su uso, adaptación y operación.[file:151]

#### 5.1. Diferencias con MLOps clásico

En LLMOps se versionan:

- Código de orquestación y pipelines.
- Modelos fundacionales base y variantes ajustadas.
- Prompts del sistema y de usuario (tratados como artefactos de configuración).
- Modelos de embeddings y índices vectoriales.
- Reglas de guardrails, políticas de filtrado y parámetros de decodificación.[file:151]

Mientras que MLOps clásico se centra más en ciclos de entrenamiento y despliegue de modelos supervisados, LLMOps se centra en control de contexto, grounding, seguridad y costes por token.[file:151]

#### 5.2. Adaptación eficiente: PEFT, LoRA y QLoRA

Para adaptar LLMs sin reentrenar todos sus parámetros se usan técnicas de **Parameter‑Efficient Fine‑Tuning (PEFT)**:

- **LoRA (Low‑Rank Adaptation):** congela los pesos originales del modelo base e inyecta pequeñas matrices entrenables de rango inferior en capas de atención, reduciendo el coste de entrenamiento manteniendo el modelo base intacto.[file:151]
- **QLoRA (Quantized LoRA):** aplica LoRA sobre modelos previamente cuantizados (por ejemplo, a 4 bits), lo que reduce significativamente el consumo de memoria y permite ajustar LLMs grandes en hardware más limitado, con calidad similar a la de LoRA estándar.[web:175]

#### 5.3. Alineamiento: RLHF y RLAIF

Para alinear el comportamiento del modelo con criterios de utilidad y seguridad se usan técnicas de aprendizaje por refuerzo:

- **RLHF (Reinforcement Learning from Human Feedback):** emplea evaluadores humanos que puntúan salidas del modelo como preferibles o no; se entrena un modelo de recompensa y se ajusta el LLM, típicamente con algoritmos como PPO, para producir respuestas útiles, honestas e inofensivas.[file:151]
- **RLAIF (Reinforcement Learning from AI Feedback):** sustituye parcialmente el feedback humano por las valoraciones de otro modelo de lenguaje que puntúa las respuestas, reduciendo el coste de anotación pero trasladando posibles sesgos del modelo evaluador.[web:178]

La diferencia clave es la fuente de feedback: humano vs IA, aspecto que aparece explícitamente en preguntas de examen.[file:149]

#### 5.4. Evaluación en LLMOps

Además de métricas clásicas (Accuracy, F1‑Score), se utilizan:

- **Perplejidad:** mide la incertidumbre del modelo al predecir la siguiente palabra, siendo menor perplejidad indicativa de mejor modelo.[file:151]
- **BLEU y ROUGE:** métricas de coincidencia de n‑gramas usadas en traducción automática y resumen.[file:151]
- Métricas específicas de RAG (Answer Accuracy, Faithfulness, Context Recall) y frameworks como RAGAS para auditar grounding y sesgos.[file:151][web:169]

#### 5.5. Herramientas y controles operativos de seguridad

En LLMOps se integran controles de seguridad:

- **Guardrails:** filtros en entrada y salida para sanitizar texto, enmascarar PII y bloquear contenidos peligrosos.[file:151]
- **Red Teaming:** pruebas sistemáticas de ataque que simulan adversarios, exigidas para ciertos modelos GPAI de riesgo sistémico según el AI Act.[file:151]
- **Trazabilidad:** versionado de modelos, prompts del sistema, configuraciones de RAG y parámetros de inferencia.[file:151]
- **Observabilidad:** métricas de consumo de tokens, tiempos de respuesta, tasas de override humano y otras, conectadas con plataformas de logging y SIEM.[web:169]

#### 5.6. QLoRA frente a LoRA

LoRA permite adaptar el modelo con coste razonable congelando pesos base e inyectando parámetros de bajo rango, mientras que QLoRA permite aplicar LoRA sobre un modelo cuantizado reduciendo aún más consumo de memoria; QLoRA es especialmente útil cuando el hardware disponible es limitado y se quiere mantener calidad similar.[file:151][web:175]

#### 5.7. RLHF frente a RLAIF

RLHF utiliza retroalimentación humana para entrenar el modelo de recompensa, mientras que RLAIF utiliza otro modelo de IA como “juez” para puntuar las salidas, reduciendo costes pero aumentando la dependencia de la calidad y sesgos del modelo evaluador.[file:151][web:178]

### 6. Notas normativas: Golden dataset y transparencia AESIA

En documentos institucionales españoles y europeos se utilizan conceptos relevantes para la gobernanza de sistemas de IA:

- **Golden dataset:** conjunto de datos de referencia de alta calidad usado para evaluar, validar y auditar el comportamiento del sistema de IA de forma consistente; no es un repositorio de credenciales ni de secretos, sino un “patrón de oro” para comprobar corrección y equidad de salidas.[file:151]
- **Transparencia según AESIA/AEPD:** implica la capacidad de comprender el funcionamiento del sistema, su propósito, las fuentes de datos y las decisiones, mediante explicabilidad, interpretabilidad y documentación clara; no exige publicar todo el código fuente o pesos del modelo, pero sí informar a las personas cuando interactúan con IA y ofrecer explicaciones significativas.[file:151]

## Conceptos que suelen preguntarse (Trampas comunes)

| Concepto                    | Realidad técnica / jurídica                                                | Distractor típico en examen                                       |
| :-------------------------- | :------------------------------------------------------------------------- | :---------------------------------------------------------------- |
| Token vs palabra / embedding| El token define coste y límites; el embedding captura semántica y sesgos  | “Un token siempre equivale a una palabra”                         |
| Transformer vs RNN          | Transformer procesa en paralelo usando Self‑Attention                      | “Transformer procesa palabra por palabra de forma secuencial”     |
| RAG                         | Inyecta información en el prompt en tiempo de inferencia sin tocar pesos  | “RAG reentrena el modelo con PDFs corporativos”                   |
| RAG vs Fine‑Tuning          | RAG aporta trazabilidad y ACL sin reentrenar; FT incrusta conocimiento     | “El Fine‑Tuning es la opción más segura para datos confidenciales”|
| Alucinación vs error RAG    | Alucinación = invención del modelo; error RAG = recuperación de fuente errónea| “RAG elimina el 100% de las alucinaciones”                    |
| Temperatura = 0             | Decodificación Greedy determinista; no garantiza verdad absoluta           | “Con temperatura 0 la respuesta siempre es cierta”                |
| Fine‑Tuning vs LoRA         | LoRA es técnica PEFT que inyecta matrices pequeñas y congela el resto     | “LoRA entrena todos los parámetros del modelo base”               |
| Modelo vs sistema GPAI      | Modelo = componente técnico (Art. 3.63); sistema = aplicación integrada   | “Todo LLM es automáticamente sistema de alto riesgo”              |
| Prompt injection indirecta  | Ataque vía documentos consumidos (RAG, navegadores, etc.)                  | “Es un error de hardware de los clusters del proveedor”           |
| RLHF vs RLAIF               | RLHF usa feedback humano; RLAIF usa otro modelo de IA                     | “RLAIF es un simple ajuste de hiperparámetros sin feedback”       |

## Posibles preguntas tipo test

**Pregunta 1.** En la arquitectura de un modelo basado en Transformers, ¿qué mecanismo permite evaluar la importancia de cada token de una frase con respecto a todos los demás de forma simultánea y paralela?

A. El truncamiento heurístico de raíces (Stemming).  
B. El mecanismo de Autoatención (Self‑Attention).  
C. Las Redes Neuronales Recurrentes (RNN).  
D. El ajuste del parámetro de Perplejidad.

**Respuesta correcta: B.**

**Pregunta 2.** Según el Art. 3 del Reglamento (UE) 2024/1689, un modelo de lenguaje masivo usado exclusivamente para investigación y creación de prototipos antes de su comercialización:

A. Se considera modelo de IA de uso general con riesgo sistémico.  
B. Queda excluido de la definición legal de modelo de IA de uso general.  
C. Se considera automáticamente un sistema de IA de alto riesgo.  
D. Requiere marcado CE obligatorio inmediato.

**Respuesta correcta: B.**

**Pregunta 3.** La Agencia para la Administración Digital desea implementar un asistente conversacional que responda a ciudadanos basándose estrictamente en las normativas publicadas en boletines oficiales, controlando permisos de acceso y sin coste de reentrenamiento constante. La arquitectura recomendada, que mitiga el riesgo de alucinación y garantiza trazabilidad documental, es:

A. Continuous Pre‑training diario desde cero.  
B. Fine‑Tuning profundo con todos los PDFs.  
C. Generación Aumentada por Recuperación (RAG).  
D. Ajuste fino eficiente mediante LoRA.

**Respuesta correcta: C.**

**Pregunta 4.** Si al invocar la API de inferencia de un LLM se establece el parámetro “Temperatura” en 0 (cero), el comportamiento esperado del sistema será:

A. Generar textos aleatorios con alta variabilidad léxica.  
B. Volverse altamente determinista (Greedy decoding), eligiendo siempre el token con mayor probabilidad.  
C. Devolver un error de saturación de GPU.  
D. Reducir la ventana de contexto al mínimo permitido.

**Respuesta correcta: B.**

**Pregunta 5.** ¿Cuál es la diferencia principal entre las técnicas de Fine‑Tuning y el uso de RAG en aplicaciones con LLMs?

A. RAG modifica los pesos neuronales del modelo; el Fine‑Tuning no.  
B. RAG inyecta conocimiento temporal en el contexto durante la inferencia; Fine‑Tuning ajusta permanentemente los pesos del modelo.  
C. RAG sólo se utiliza en modelos encoder‑only; Fine‑Tuning en decoder‑only.  
D. No existe diferencia, son términos sinónimos.

**Respuesta correcta: B.**

**Pregunta 6.** Dentro del ciclo de vida LLMOps, si se requiere ajustar estilo o estructura de respuesta de un LLM muy pesado pero se dispone de hardware limitado, la técnica más adecuada para “congelar” el modelo base e inyectar pequeñas matrices entrenables es:

A. RAG vectorial.  
B. RLHF.  
C. LoRA (Low‑Rank Adaptation).  
D. Tokenización BPE.

**Respuesta correcta: C.**

**Pregunta 7.** ¿Qué afirmación sobre el límite de la “Ventana de Contexto” (Context Window) de un LLM es correcta?

A. Se mide en megabytes de texto.  
B. Equivale a una base de datos ilimitada para el modelo.  
C. Determina la cantidad máxima de tokens (entrada + salida) que el modelo puede procesar en una inferencia.  
D. Aumentar la ventana de contexto elimina automáticamente las alucinaciones del modelo.

**Respuesta correcta: C.**

**Pregunta 8.** En LLMOps, ¿qué métrica se utiliza tradicionalmente para medir el grado de incertidumbre de un modelo al predecir la siguiente palabra en una secuencia?

A. Similitud del coseno.  
B. Perplejidad.  
C. Exactitud (Accuracy).  
D. Distancia euclidiana.

**Respuesta correcta: B.**

**Pregunta 9.** Según el AI Act, ¿qué obligación de transparencia específica aplica a sistemas de IA generativa desplegados para atención ciudadana (ej. chatbots)?

A. Publicar código fuente y pesos del modelo en un repositorio de la UE.  
B. Informar a las personas físicas de que interactúan con un sistema de IA, salvo que resulte evidente dadas las circunstancias.  
C. Prohibir el uso de algoritmos decoder‑only.  
D. Revisar manualmente cada prompt ciudadano antes de su envío.

**Respuesta correcta: B.**

**Pregunta 10.** ¿Qué vector de riesgo de seguridad ocurre cuando un sistema de IA con RAG lee un PDF malicioso cargado por un usuario que contiene comandos ocultos diseñados para anular las instrucciones del sistema?

A. Extracción de características.  
B. Deriva de datos (Data Drift).  
C. Inyección indirecta de instrucciones (Indirect Prompt Injection).  
D. Alineamiento mediante RLHF.

**Respuesta correcta: C.**

## Normativa o fuentes relacionadas

- **Reglamento (UE) 2024/1689** (Ley de IA): definiciones de modelos y sistemas de IA de uso general, obligaciones de transparencia y requisitos para modelos GPAI de riesgo sistémico.[file:151]
- **NIST AI RMF y perfiles generativos (NIST AI 600‑1):** identificación de riesgos específicos de IA generativa (confabulaciones, propiedad intelectual, seguridad de información).[file:151]
- **NIST AI 100‑2e2025:** glosario técnico que recoge RAG como patrón arquitectónico.[file:151]
- **OWASP Top 10 for LLM Applications 2025:** marco de referencia de riesgos para aplicaciones LLM (LLM01–LLM10).[web:166][web:169]
- **ISO/IEC TR 24372:2021:** visión general de enfoques computacionales de sistemas de IA.[file:151]
- **AESIA / AEPD:** guías de transparencia, explicabilidad y evaluación de impacto en sistemas de IA en España.[file:151]