---
id: "cm-ad-innovacion-y-transformacion-digital-tema-015-ciclo-de-vida-ia"
title: "Ciclo de vida de la IA"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/innovacion-y-transformacion-digital"
profiles:
  - "p06-ingeniero-desarrollo"
official_profiles:
  - "P06 - Ingeniero de Desarrollo"
official_topic: "Tema 15. Ciclo de vida de la IA"
source_ids: []
tags:
  - "ciclo-de-vida-ia"
  - "mlops"
  - "llmops"
  - "agentops"
  - "pipeline"
  - "entrenamiento"
  - "validacion"
  - "despliegue"
  - "modelos"
  - "versionado"
  - "reproducibilidad"
  - "mejora-continua"
created_at: "2026-09-03"
last_reviewed: "2026-09-12"
ai_generated: true
ai_sources:
  - "perplexity"
  - "chatgpt"
  - "gemini"
needs_human_review: true
---

# Tema 15. Ciclo de vida de la IA

El ciclo de vida de la Inteligencia Artificial comprende todas las fases desde la conceptualización y preparación de datos hasta el despliegue, monitorización y retirada del modelo. En el ámbito de la Unión Europea, este ciclo de vida está fuertemente regulado para los sistemas de alto riesgo, exigiendo sistemas de gestión de riesgos iterativos y continuos, así como sistemas de gestión de la calidad debidamente documentados[cite: 11].

## 1. Conceptos de MLOps, LLMOPs y AgentOps

La industrialización de la Inteligencia Artificial requiere la adopción de prácticas operativas estandarizadas que garanticen la escalabilidad, seguridad y fiabilidad de los modelos en producción.

*   **MLOps (Machine Learning Operations):** Es la extensión de la cultura DevOps al ámbito del Machine Learning. Su objetivo es unificar el desarrollo del sistema de aprendizaje automático (Dev) y su operación (Ops). Estandariza el ciclo de vida continuo mediante la automatización de la integración, prueba, despliegue (CI/CD) y entrenamiento continuo (CT) de los modelos predictivos.
*   **LLMOps (Large Language Model Operations):** Subdisciplina de MLOps adaptada a las particularidades de los modelos fundacionales y grandes modelos de lenguaje (LLMs)[cite: 11]. Aborda retos específicos como el alto coste computacional, la orquestación de bases de datos vectoriales, el ajuste fino eficiente (PEFT, LoRA), la ingeniería de instrucciones (*Prompt Engineering*), arquitecturas RAG (*Retrieval-Augmented Generation*) y la monitorización de métricas específicas como la toxicidad o las alucinaciones.
*   **AgentOps (Agent Operations):** Práctica emergente enfocada en el ciclo de vida de los agentes autónomos de IA. Gestiona la orquestación multi-agente, la memoria a corto y largo plazo del agente, la ejecución segura de herramientas externas (APIs) y la alineación del comportamiento del agente con los objetivos del sistema y las directrices éticas.

## 2. Pipeline de datos y modelos

El desarrollo de un sistema de IA requiere flujos de trabajo (*pipelines*) automatizados y reproducibles.

*   **Pipeline de datos:** Abarca la ingesta, limpieza, transformación y almacenamiento de los datos. Para los sistemas de IA de alto riesgo, los conjuntos de datos de entrenamiento, validación y prueba deben someterse a prácticas de gobernanza adecuadas[cite: 11]. Estos conjuntos deben ser pertinentes, suficientemente representativos y, en la mayor medida posible, carecer de errores y estar completos en vista de su finalidad prevista[cite: 11]. Asimismo, deben examinarse para detectar posibles sesgos que puedan dar lugar a discriminación prohibida por el Derecho de la Unión[cite: 11].
*   **Pipeline de modelos:** Comprende la ingeniería de características (*Feature Engineering*), la selección del algoritmo, el ajuste de hiperparámetros y el entrenamiento del modelo. Herramientas como Kubeflow, MLflow o Apache Airflow son estándares de la industria para orquestar estos flujos dirigidos por grafos acíclicos dirigidos (DAGs).

## 3. Entrenamiento, validación y despliegue

Estas tres fases constituyen el núcleo técnico de la creación y puesta en producción del modelo de IA.

*   **Entrenamiento:** Proceso iterativo donde el algoritmo ajusta sus parámetros internos procesando los datos de entrenamiento[cite: 11]. En los modelos de IA de uso general, la cantidad acumulada de cálculo utilizado (operaciones de coma flotante) es un indicador de la capacidad del modelo y de sus posibles riesgos sistémicos[cite: 11].
*   **Validación y pruebas:** Los sistemas de IA deben ser sometidos a pruebas antes de su introducción en el mercado o puesta en servicio[cite: 11]. Estas pruebas comprobarán que los sistemas funcionan de manera coherente con su finalidad prevista y ayudarán a determinar las medidas de gestión de riesgos más adecuadas[cite: 11]. Pueden incluir pruebas en condiciones reales (*sandbox* regulatorio)[cite: 11].
*   **Despliegue:** Puesta en servicio del modelo en el entorno de producción. En el caso de sistemas de alto riesgo, el despliegue debe ir precedido de un procedimiento de evaluación de la conformidad y de la elaboración de una declaración UE de conformidad[cite: 11]. Existen diversas estrategias de despliegue seguro, como el despliegue *Canary* (liberación a un pequeño subconjunto de usuarios), *Blue-Green* (entornos paralelos) o *Shadow* (ejecución en segundo plano sin impacto real).

## 4. Monitorización, observabilidad y mantenimiento de modelos

El rendimiento de un modelo de IA tiende a degradarse con el tiempo debido a cambios en el entorno de los datos.

*   **Monitorización técnica y observabilidad:** Consiste en la supervisión continua del rendimiento computacional (latencia, uso de CPU/GPU) y del rendimiento estadístico del modelo. Se vigilan fenómenos como la deriva de datos (*Data Drift*) y la deriva de conceptos (*Concept Drift*), que provocan la degradación del modelo (*Model Decay*).
*   **Vigilancia poscomercialización:** Los proveedores de sistemas de IA de alto riesgo están obligados a establecer y mantener un sistema de vigilancia poscomercialización[cite: 11]. Este sistema está destinado a recoger y examinar de forma activa y sistemática la experiencia obtenida con el uso de los sistemas de IA para aplicar medidas correctoras o preventivas[cite: 11].
*   **Archivos de registro (Logs):** Los sistemas de IA de alto riesgo deben permitir técnicamente el registro automático de acontecimientos a lo largo de todo su ciclo de vida[cite: 11]. Estos registros facilitan la vigilancia poscomercialización y la detección de situaciones que puedan presentar riesgos[cite: 11].
*   **Mantenimiento:** Incluye el reentrenamiento de modelos y la gestión de incidentes. Los proveedores deben comunicar a las autoridades pertinentes cualquier incidente grave asociado al uso de sus sistemas de IA[cite: 11].

## 5. Versionado, reproducibilidad y mejora continua

La trazabilidad es un requisito técnico y regulatorio indispensable a lo largo del ciclo de vida de la IA.

*   **Versionado y Trazabilidad:** Consiste en mantener un registro exacto de las versiones de los datos (ej. DVC), del código fuente (ej. Git) y de los pesos y parámetros del modelo (ej. MLflow Model Registry). Para los sistemas de IA de alto riesgo, los proveedores deben conservar la documentación técnica y los archivos de registro durante un período de diez años a contar desde la introducción en el mercado o la puesta en servicio[cite: 11].
*   **Reproducibilidad:** Es la capacidad de recrear un modelo exacto utilizando las mismas versiones de datos, código y entorno de ejecución. Es crucial para las auditorías algorítmicas y para demostrar la conformidad con los requisitos legales en inspecciones de las autoridades de vigilancia del mercado[cite: 11].
*   **Mejora continua:** Los sistemas de IA pueden tener capacidad de adaptación tras el despliegue mediante el autoaprendizaje[cite: 11]. Los cambios en el algoritmo y en el funcionamiento de los sistemas de IA que siguen aprendiendo después de su puesta en servicio no constituyen una modificación sustancial si dichos cambios fueron predeterminados por el proveedor y evaluados en la evaluación de la conformidad inicial[cite: 11]. No obstante, deben aplicarse medidas para evitar que los resultados de salida sesgados influyan negativamente en las informaciones de entrada de futuras operaciones (bucles de retroalimentación)[cite: 11].
