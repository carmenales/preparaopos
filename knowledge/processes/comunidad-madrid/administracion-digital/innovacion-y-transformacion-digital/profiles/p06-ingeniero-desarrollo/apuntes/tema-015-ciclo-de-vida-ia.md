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
  - "rag"
  - "lora"
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

El ciclo de vida de la Inteligencia Artificial comprende todas las fases desde la conceptualización y preparación de datos hasta el despliegue, monitorización y retirada del modelo. En el ámbito de la Unión Europea, este ciclo de vida está fuertemente regulado para los sistemas de alto riesgo, exigiendo sistemas de gestión de riesgos iterativos y continuos, así como sistemas de gestión de la calidad debidamente documentados.

## 1. Conceptos de MLOps, LLMOPs y AgentOps

La industrialización de la Inteligencia Artificial requiere la adopción de prácticas operativas estandarizadas que garanticen la escalabilidad, seguridad y fiabilidad de los modelos en producción.

*   **MLOps (Machine Learning Operations):** Es la extensión de la cultura DevOps al ámbito del Machine Learning. Su objetivo es unificar el desarrollo del sistema de aprendizaje automático (Dev) y su operación (Ops). Estandariza el ciclo de vida continuo mediante la automatización de la integración, prueba, despliegue (CI/CD) y entrenamiento continuo (CT) de los modelos predictivos. Google Cloud, en su guía de referencia sobre MLOps, distingue tres niveles de madurez progresivos: el Nivel 0 (proceso manual, sin pipelines automatizados), el Nivel 1 (automatización del pipeline de ML con reentrenamiento continuo o CT) y el Nivel 2 (automatización completa del propio pipeline de integración y entrega continua, CI/CD, que construye y despliega el pipeline de ML).

*   **LLMOps (Large Language Model Operations):** Subdisciplina de MLOps adaptada a las particularidades de los modelos fundacionales y grandes modelos de lenguaje (LLMs). Aborda retos específicos como el alto coste computacional, la orquestación de bases de datos vectoriales, el ajuste fino eficiente (PEFT, LoRA), la ingeniería de instrucciones (*Prompt Engineering*), arquitecturas RAG (*Retrieval-Augmented Generation*) y la monitorización de métricas específicas como la toxicidad o las alucinaciones.

    *   **RAG (Retrieval-Augmented Generation):** técnica formulada originalmente en el artículo *"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"* (Lewis et al., Facebook AI Research, presentado en NeurIPS 2020), que combina un modelo generativo (paramétrico, basado en lo aprendido durante el entrenamiento) con un componente de recuperación no paramétrico que consulta una base de conocimiento externa (habitualmente indexada en una base de datos vectorial) antes de generar la respuesta. Esta combinación permite que el modelo genere respuestas más específicas, diversas y factualmente correctas que un modelo generativo puro, y resulta especialmente útil para reducir alucinaciones y mantener el conocimiento del sistema actualizado sin necesidad de reentrenar el modelo base.
    *   **LoRA (Low-Rank Adaptation):** técnica de ajuste fino eficiente en parámetros (PEFT) formulada en el artículo *"LoRA: Low-Rank Adaptation of Large Language Models"* (Hu et al., Microsoft, ICLR 2021/2022), que congela los pesos del modelo preentrenado e introduce matrices de descomposición de rango reducido entrenables en cada capa de la arquitectura Transformer. Esto reduce drásticamente el número de parámetros entrenables (los propios autores documentan reducciones de hasta 10.000 veces respecto al ajuste fino completo de un modelo de 175.000 millones de parámetros) y el consumo de memoria de GPU necesario, sin introducir latencia adicional en el momento de la inferencia.

*   **AgentOps (Agent Operations):** Práctica emergente enfocada en el ciclo de vida de los agentes autónomos de IA. Gestiona la orquestación multi-agente, la memoria a corto y largo plazo del agente, la ejecución segura de herramientas externas (APIs) y la alineación del comportamiento del agente con los objetivos del sistema y las directrices éticas.

## 2. Pipeline de datos y modelos

El desarrollo de un sistema de IA requiere flujos de trabajo (*pipelines*) automatizados y reproducibles.

*   **Pipeline de datos:** Abarca la ingesta, limpieza, transformación y almacenamiento de los datos. Para los sistemas de IA de alto riesgo, los conjuntos de datos de entrenamiento, validación y prueba deben someterse a prácticas de gobernanza adecuadas. Estos conjuntos deben ser pertinentes, suficientemente representativos y, en la mayor medida posible, carecer de errores y estar completos en vista de su finalidad prevista. Asimismo, deben examinarse para detectar posibles sesgos que puedan dar lugar a discriminación prohibida por el Derecho de la Unión.
*   **Pipeline de modelos:** Comprende la ingeniería de características (*Feature Engineering*), la selección del algoritmo, el ajuste de hiperparámetros y el entrenamiento del modelo. Herramientas como Kubeflow, MLflow o Apache Airflow son estándares de la industria para orquestar estos flujos dirigidos por grafos acíclicos dirigidos (DAGs).

## 3. Entrenamiento, validación y despliegue

Estas tres fases constituyen el núcleo técnico de la creación y puesta en producción del modelo de IA.

*   **Entrenamiento:** Proceso iterativo donde el algoritmo ajusta sus parámetros internos procesando los datos de entrenamiento. En los modelos de IA de uso general, la cantidad acumulada de cálculo utilizado (operaciones de coma flotante) es un indicador de la capacidad del modelo y de sus posibles riesgos sistémicos.
*   **Validación y pruebas:** Los sistemas de IA deben ser sometidos a pruebas antes de su introducción en el mercado o puesta en servicio. Estas pruebas comprobarán que los sistemas funcionan de manera coherente con su finalidad prevista y ayudarán a determinar las medidas de gestión de riesgos más adecuadas. Pueden incluir pruebas en condiciones reales (*sandbox* regulatorio).
*   **Despliegue:** Puesta en servicio del modelo en el entorno de producción. En el caso de sistemas de alto riesgo, el despliegue debe ir precedido de un procedimiento de evaluación de la conformidad y de la elaboración de una declaración UE de conformidad. Existen diversas estrategias de despliegue seguro, como el despliegue *Canary* (liberación a un pequeño subconjunto de usuarios), *Blue-Green* (entornos paralelos) o *Shadow* (ejecución en segundo plano sin impacto real).

**Precisión sobre estrategias de despliegue seguro**
Conviene distinguir con exactitud el propósito de cada estrategia, ya que suelen confundirse entre sí en examen:
*   **Despliegue Canary:** la nueva versión del modelo se libera inicialmente a un pequeño porcentaje del tráfico real de usuarios, monitorizando su comportamiento antes de extenderla gradualmente al resto, lo que permite detectar problemas con un impacto limitado.
*   **Despliegue Blue-Green:** se mantienen dos entornos de producción idénticos y completos (el "azul", en producción activa, y el "verde", con la nueva versión), y el tráfico se conmuta de golpe de uno al otro, permitiendo una reversión (*rollback*) inmediata si algo falla, ya que el entorno anterior permanece disponible.
*   **Despliegue Shadow (sombra):** la nueva versión del modelo recibe una copia del tráfico real y genera predicciones en paralelo al modelo en producción, pero sus resultados no se muestran a los usuarios finales; se emplea exclusivamente para comparar el rendimiento del nuevo modelo contra el vigente sin ningún riesgo para el usuario.

## 4. Monitorización, observabilidad y mantenimiento de modelos

El rendimiento de un modelo de IA tiende a degradarse con el tiempo debido a cambios en el entorno de los datos.

*   **Monitorización técnica y observabilidad:** Consiste en la supervisión continua del rendimiento computacional (latencia, uso de CPU/GPU) y del rendimiento estadístico del modelo. Se vigilan fenómenos como la deriva de datos (*Data Drift*) y la deriva de conceptos (*Concept Drift*), que provocan la degradación del modelo (*Model Decay*).

*   **Vigilancia poscomercialización (artículo 72 del Reglamento (UE) 2024/1689):** Los proveedores de sistemas de IA de alto riesgo están obligados a establecer y operar un sistema de vigilancia poscomercialización proporcionado a la naturaleza de las tecnologías de IA y de los riesgos del sistema. El artículo 72, apartados 1 y 2, exige que este sistema recopile, documente y analice de manera activa y sistemática los datos pertinentes proporcionados por los responsables del despliegue u obtenidos a través de otras fuentes sobre el funcionamiento de los sistemas de IA de alto riesgo durante toda su vida útil, permitiendo evaluar el cumplimiento continuo de los requisitos del propio Reglamento. El apartado 3 exige que dicho sistema se base en un **plan de vigilancia poscomercialización** documentado, que forma parte de la documentación técnica exigida por el Anexo IV, en virtud del artículo 11 (concretamente, en su punto 9).

*   **Archivos de registro (Logs):** Los sistemas de IA de alto riesgo deben permitir técnicamente el registro automático de acontecimientos a lo largo de todo su ciclo de vida. Estos registros facilitan la vigilancia poscomercialización y la detección de situaciones que puedan presentar riesgos.

*   **Mantenimiento:** Incluye el reentrenamiento de modelos y la gestión de incidentes. Los proveedores deben comunicar a las autoridades pertinentes cualquier incidente grave asociado al uso de sus sistemas de IA.

## 5. Versionado, reproducibilidad y mejora continua

La trazabilidad es un requisito técnico y regulatorio indispensable a lo largo del ciclo de vida de la IA.

*   **Versionado y Trazabilidad:** Consiste en mantener un registro exacto de las versiones de los datos (ej. DVC), del código fuente (ej. Git) y de los pesos y parámetros del modelo (ej. MLflow Model Registry).

**Conservación de la documentación (artículo 18 del Reglamento (UE) 2024/1689)**
Este artículo precisa con exactitud, en su apartado 1, que durante un período de **diez años** a contar desde la introducción en el mercado o la puesta en servicio del sistema de IA de alto riesgo, el proveedor mantendrá a disposición de las autoridades nacionales competentes los siguientes cinco documentos, de forma literal:
*   a) la documentación técnica a que se refiere el artículo 11 (que incluye, entre otros elementos, el propio plan de vigilancia poscomercialización);
*   b) la documentación relativa al sistema de gestión de la calidad a que se refiere el artículo 17;
*   c) la documentación relativa a los cambios aprobados por los organismos notificados, si procede;
*   d) las decisiones y otros documentos expedidos por los organismos notificados, si procede;
*   e) la declaración UE de conformidad contemplada en el artículo 47.

El apartado 2 del artículo 18 añade que cada Estado miembro determinará las condiciones en las que esta documentación permanecerá a disposición de las autoridades nacionales competentes durante ese periodo de diez años en los casos en que el proveedor o su representante autorizado quiebre o cese en su actividad antes de que finalice dicho plazo.

*   **Reproducibilidad:** Es la capacidad de recrear un modelo exacto utilizando las mismas versiones de datos, código y entorno de ejecución. Es crucial para las auditorías algorítmicas y para demostrar la conformidad con los requisitos legales en inspecciones de las autoridades de vigilancia del mercado.

*   **Mejora continua:** Los sistemas de IA pueden tener capacidad de adaptación tras el despliegue mediante el autoaprendizaje. Los cambios en el algoritmo y en el funcionamiento de los sistemas de IA que siguen aprendiendo después de su puesta en servicio no constituyen una modificación sustancial si dichos cambios fueron predeterminados por el proveedor y evaluados en la evaluación de la conformidad inicial. No obstante, deben aplicarse medidas para evitar que los resultados de salida sesgados influyan negativamente en las informaciones de entrada de futuras operaciones (bucles de retroalimentación).

## Referencias técnicas y normativas

*   Reglamento (UE) 2024/1689, por el que se establecen normas armonizadas en materia de inteligencia artificial (artículos 11, 17, 18, 47 y 72).
*   Lewis, P. et al., *"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"*, Facebook AI Research, NeurIPS 2020 (arXiv:2005.11401).
*   Hu, E. J. et al., *"LoRA: Low-Rank Adaptation of Large Language Models"*, Microsoft, ICLR 2022 (arXiv:2106.09685).
*   Google Cloud, *"MLOps: Continuous delivery and automation pipelines in machine learning"*, Cloud Architecture Center.
