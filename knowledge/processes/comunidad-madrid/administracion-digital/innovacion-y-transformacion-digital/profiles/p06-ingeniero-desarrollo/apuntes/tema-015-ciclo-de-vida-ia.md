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
  - "gestion-de-riesgos"
  - "gestion-de-la-calidad"
  - "evaluacion-de-la-conformidad"
  - "nist-ai-rmf"
  - "iso-42001"
created_at: "2026-09-03"
last_reviewed: "2026-09-12"
ai_generated: true
ai_sources:
  - "perplexity"
  - "chatgpt"
  - "gemini"
  - "claude"
needs_human_review: true
---

# Tema 15. Ciclo de vida de la IA

El ciclo de vida de la Inteligencia Artificial comprende todas las fases desde la conceptualización, diseño y preparación de datos hasta el desarrollo, despliegue, monitorización continua y eventual retirada del modelo. En el ámbito de la Unión Europea, este ciclo de vida está fuertemente regulado para los sistemas de alto riesgo mediante el Reglamento (UE) 2024/1689 (Reglamento de Inteligencia Artificial), exigiendo la integración de sistemas de gestión de riesgos iterativos y continuos, así como sistemas de gestión de la calidad debidamente documentados a lo largo de toda la vida útil del sistema.

## 1. Conceptos de MLOps, LLMOPs y AgentOps

La industrialización de la Inteligencia Artificial requiere la adopción de prácticas operativas estandarizadas, estructuradas y medibles que garanticen la escalabilidad, seguridad, observabilidad y fiabilidad de los modelos en producción.

*   **MLOps (Machine Learning Operations):** Es la extensión de la cultura y prácticas DevOps al ámbito específico del Machine Learning y la ciencia de datos. Su objetivo es unificar el desarrollo del sistema de aprendizaje automático (Dev) y su operación (Ops), garantizando la reproducibilidad y la gobernanza. Estandariza el ciclo de vida continuo mediante la automatización de la integración, prueba, despliegue (CI/CD) y entrenamiento continuo (CT - *Continuous Training*) de los modelos predictivos. 
    A nivel de arquitectura de referencia, marcos como el de Google Cloud distinguen tres niveles de madurez progresivos:
    *   *Nivel 0 (MLOps manual):* Proceso completamente manual, impulsado por científicos de datos en cuadernos interactivos (*notebooks*). No existen pipelines automatizados y el despliegue requiere intervención manual técnica.
    *   *Nivel 1 (Automatización del pipeline de ML):* Introducción del reentrenamiento continuo (CT). El pipeline de datos y modelos se ejecuta automáticamente ante nuevos datos o caídas de rendimiento (deriva), garantizando la entrega continua del servicio de predicción.
    *   *Nivel 2 (Automatización CI/CD/CT completa):* Nivel de máxima madurez organizativa. Se automatiza la construcción, prueba y despliegue del propio pipeline de ML. Permite a los equipos de ciencia de datos experimentar e implementar de forma fluida nuevas arquitecturas y lógicas en producción.

*   **LLMOps (Large Language Model Operations):** Subdisciplina de MLOps adaptada a las particularidades, escala y complejidad de los modelos fundacionales y grandes modelos de lenguaje (LLMs). Aborda retos técnicos específicos como el alto coste computacional de inferencia, la gestión de latencias, la orquestación de bases de datos vectoriales para almacenamiento de *embeddings*, la ingeniería de instrucciones (*Prompt Engineering*) y la monitorización de métricas específicas y cualitativas (como la toxicidad, la coherencia, la fidelidad o las alucinaciones).
    *   **RAG (Retrieval-Augmented Generation):** Técnica formulada originalmente en el artículo *"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"* (Lewis et al., Facebook AI Research, NeurIPS 2020). Combina un modelo generativo (paramétrico, basado en lo aprendido durante el entrenamiento) con un componente de recuperación no paramétrico que consulta una base de conocimiento externa y actualizada (habitualmente indexada en una base de datos vectorial mediante *embeddings*) antes de generar la respuesta. Esta combinación inyecta contexto en el *prompt*, permitiendo que el modelo genere respuestas más específicas, diversas y factualmente correctas. Resulta especialmente útil en la Administración Pública para reducir alucinaciones, citar fuentes documentales exactas y mantener el conocimiento del sistema actualizado sin necesidad de reentrenar el modelo base.
    *   **LoRA (Low-Rank Adaptation):** Técnica de ajuste fino eficiente en parámetros (PEFT - *Parameter-Efficient Fine-Tuning*) formulada en el artículo *"LoRA: Low-Rank Adaptation of Large Language Models"* (Hu et al., Microsoft, ICLR 2021/2022). Esta técnica congela los pesos originales del modelo preentrenado e introduce matrices de descomposición de rango reducido entrenables en cada capa de la arquitectura Transformer. Esto reduce drásticamente el número de parámetros entrenables (con reducciones de hasta 10.000 veces respecto al ajuste fino completo de modelos de cientos de miles de millones de parámetros) y minimiza el consumo de memoria VRAM de GPU necesario. Su principal ventaja arquitectónica es que no introduce latencia adicional en el momento de la inferencia, permitiendo el intercambio dinámico de adaptadores según el contexto de uso.

*   **AgentOps (Agent Operations):** Práctica emergente enfocada en la gestión del ciclo de vida de los agentes autónomos de IA. Un agente de IA trasciende la generación de texto para interactuar activamente con su entorno. AgentOps gestiona la orquestación multi-agente, la memoria a corto y largo plazo del agente (retención de estado y contexto), la ejecución segura de herramientas externas (Tool/Function Calling mediante APIs) y la alineación estricta del comportamiento del agente con los objetivos del sistema y las directrices éticas y normativas, incorporando mecanismos de intervención y bloqueo de acciones destructivas (*Guardrails*).

*   **Marcos internacionales de gobernanza y gestión de riesgos de la IA:** Junto a las prácticas de industrialización técnica (MLOps/LLMOps/AgentOps), existen marcos de referencia, de adopción voluntaria salvo que una norma los haga exigibles, que estructuran la gobernanza de la IA a nivel organizativo:
    *   *NIST AI Risk Management Framework (AI RMF 1.0):* Marco publicado por el *National Institute of Standards and Technology* (EE. UU.) en enero de 2023, de carácter voluntario y no certificable. Organiza la gestión del riesgo de la IA en torno a cuatro funciones nucleares que se aplican de forma iterativa a lo largo de todo el ciclo de vida del sistema:
        *   **Govern (Gobernar):** función transversal que atraviesa a las tres restantes; establece la cultura organizativa, las políticas, los procesos y las estructuras de rendición de cuentas para la gestión del riesgo de IA.
        *   **Map (Mapear):** comprende el contexto, las finalidades, las partes interesadas y los riesgos previsibles del sistema de IA concreto.
        *   **Measure (Medir):** analiza y evalúa, mediante métodos cuantitativos y cualitativos, las capacidades, limitaciones y factores de riesgo identificados en la fase anterior.
        *   **Manage (Gestionar):** asigna recursos para tratar los riesgos priorizados, documenta el riesgo residual aceptado y articula la respuesta ante incidentes.
    *   *ISO/IEC 42001:2023:* Primera norma internacional certificable que establece los requisitos para implantar un Sistema de Gestión de la Inteligencia Artificial (AIMS - *AI Management System*) en una organización, siguiendo la estructura de alto nivel común a otras normas ISO de sistemas de gestión (como ISO 9001 o ISO/IEC 27001). Su enfoque de gestión de riesgos guarda una fuerte equivalencia funcional con las obligaciones de gestión de riesgos y de calidad exigidas por el Reglamento (UE) 2024/1689, por lo que su certificación puede emplearse como evidencia de buenas prácticas de cumplimiento, sin que sustituya por sí sola a las obligaciones legales del Reglamento.

## 2. Pipeline de datos y modelos

El desarrollo y mantenimiento de un sistema de IA robusto requiere flujos de trabajo (*pipelines*) automatizados, modulares y reproducibles, integrados habitualmente en infraestructuras *Cloud* u *On-Premise* avanzadas.

*   **Pipeline de datos:** Abarca el flujo completo de la información: ingesta, validación, limpieza, transformación, enriquecimiento y almacenamiento de los datos. Incluye la orquestación de procesos ETL/ELT y la generación de características (*features*).
    *   *Feature Store (Almacén de características):* En arquitecturas maduras, las variables transformadas y estandarizadas se almacenan en un *Feature Store* centralizado, que sirve como única fuente de verdad tanto para el entrenamiento (*offline*) como para la inferencia (*online*), evitando inconsistencias computacionales (*training-serving skew*).
    *   *Gobernanza de Datos (Artículo 10 del Reglamento de IA):* Para los sistemas de IA de alto riesgo, los conjuntos de datos de entrenamiento, validación y prueba deben someterse a prácticas de gobernanza estrictas. Estos conjuntos deben ser pertinentes, suficientemente representativos y, en la mayor medida posible, carecer de errores y estar completos en vista de su finalidad prevista. Asimismo, deben examinarse de manera sistemática para detectar posibles sesgos que puedan dar lugar a discriminación prohibida por el Derecho de la Unión o a resultados perjudiciales para la salud y la seguridad.

*   **Pipeline de modelos:** Comprende la secuencia computacional que transforma los datos preparados en un artefacto predictivo. Incluye la selección de características, la selección del algoritmo, el ajuste de hiperparámetros (*Hyperparameter Tuning*), el entrenamiento del modelo y su evaluación automatizada. Herramientas de la industria como Kubeflow, MLflow o Apache Airflow se utilizan como estándar para orquestar estos flujos, que habitualmente se modelan y ejecutan como grafos acíclicos dirigidos (DAGs) para garantizar la correcta gestión de dependencias entre tareas.

## 3. Entrenamiento, validación y despliegue

Estas tres fases constituyen el núcleo técnico de la creación, certificación y puesta en producción del modelo de IA, debiendo quedar documentadas de forma exhaustiva para la trazabilidad y auditoría.

*   **Entrenamiento:** Proceso matemático e iterativo donde el algoritmo de aprendizaje optimiza y ajusta sus parámetros internos (pesos y sesgos) procesando los datos de entrenamiento para minimizar una función de pérdida o error (*Loss Function*). En los modelos de IA de uso general (GPAI), la cantidad acumulada de cálculo utilizado (medida en operaciones de coma flotante o *FLOPS*) constituye el principal indicador normativo de la capacidad del modelo y de la presunción de posibles riesgos sistémicos.

*   **Validación y pruebas:** Los sistemas de IA deben ser sometidos a pruebas rigurosas antes de su introducción en el mercado o puesta en servicio. Estas pruebas, realizadas sobre conjuntos de datos independientes (*Hold-out* o validación cruzada), comprobarán que los sistemas funcionan de manera coherente con su finalidad prevista y ayudarán a determinar las medidas de gestión de riesgos más adecuadas (precisión, solidez, ciberseguridad).
    *   *Pruebas en condiciones reales (Sandbox regulatorio y Art. 60):* El Reglamento de IA fomenta las pruebas fuera de entornos de laboratorio controlados para evaluar la conformidad. El artículo 60 regula estas pruebas en condiciones reales, exigiendo un plan de pruebas documentado, garantías específicas para la protección de sujetos vulnerables y, por norma general, la obtención del consentimiento informado de las personas físicas participantes.

*   **Precisión, solidez y ciberseguridad (Artículo 15 del Reglamento UE 2024/1689):** Los sistemas de IA de alto riesgo deben diseñarse y desarrollarse de modo que alcancen un nivel adecuado de precisión, solidez y ciberseguridad, y que funcionen de manera uniforme en esos aspectos durante todo su ciclo de vida. Las instrucciones de uso deben indicar los niveles de precisión alcanzados y los parámetros pertinentes para medirla. En cuanto a la solidez, los sistemas deben ser lo más resistentes posible frente a errores, fallos o incoherencias propios o del entorno, pudiendo alcanzarse mediante soluciones de redundancia técnica (copias de seguridad, planes de prevención contra fallos). Para los sistemas que continúan aprendiendo tras su puesta en servicio (*online learning*), deben adoptarse medidas técnicas específicas para eliminar o reducir al máximo el riesgo de que resultados de salida sesgados retroalimenten la información de entrada de operaciones futuras (bucles de retroalimentación). En materia de ciberseguridad, los sistemas deben contar con protección técnica frente a intentos de terceros no autorizados de alterar su uso, sus resultados o su rendimiento explotando sus vulnerabilidades, incluyendo específicamente medidas frente al envenenamiento de datos o de modelos (*data poisoning*, *model poisoning*), los ataques adversarios (*adversarial examples*) y los fallos de confidencialidad del modelo.

*   **Despliegue e integración:** Puesta en servicio del modelo en el entorno de producción, habitualmente encapsulado en contenedores (ej. Docker, Kubernetes) y expuesto mediante APIs (endpoints REST/gRPC). En el caso de sistemas de alto riesgo, el despliegue debe ir precedido, con carácter obligatorio, de un procedimiento de evaluación de la conformidad (Artículo 43 del Reglamento UE 2024/1689) y de la elaboración de una declaración UE de conformidad (marcado CE). El artículo 43 establece dos vías de evaluación de la conformidad para los sistemas enumerados en el anexo III:
    *   *Procedimiento basado en el control interno (Anexo VI):* Vía por defecto y mayoritaria, en la que el propio proveedor evalúa, bajo su responsabilidad, el cumplimiento del sistema de gestión de la calidad y de la documentación técnica, sin intervención de un tercero externo.
    *   *Procedimiento basado en la evaluación del sistema de gestión de la calidad y de la documentación técnica por un organismo notificado (Anexo VII):* Vía obligatoria cuando el sistema de IA de alto riesgo se destine a la identificación biométrica remota, o cuando no exista una norma armonizada que cubra todos los requisitos pertinentes ni se haya adoptado una especificación común.
    Toda modificación sustancial de un sistema de IA de alto riesgo tras la obtención de la declaración UE de conformidad o del certificado exige someterlo a una nueva evaluación de la conformidad.

    Existen diversas estrategias de despliegue seguro para mitigar riesgos operativos:

    *   **Despliegue Canary:** La nueva versión del modelo se libera inicialmente a un pequeño porcentaje del tráfico real de usuarios (ej. 5%). Se monitoriza su comportamiento y rendimiento antes de extender el enrutamiento gradualmente al 100% de los usuarios. Permite detectar problemas en producción con un impacto limitado.
    *   **Despliegue Blue-Green:** Se mantienen dos entornos de producción idénticos y completamente aprovisionados. El entorno "Azul" ejecuta la versión actual en producción, mientras que el entorno "Verde" ejecuta la nueva versión. Tras superar las pruebas, el tráfico se conmuta íntegra e instantáneamente del azul al verde a nivel de balanceador de carga. Permite una reversión (*rollback*) inmediata y sin tiempo de inactividad si se detecta un fallo, ya que el entorno anterior permanece intacto.
    *   **Despliegue Shadow (sombra):** La nueva versión del modelo se despliega en producción y recibe una copia asíncrona del tráfico real, generando predicciones en paralelo al modelo productivo principal. Sin embargo, sus resultados se registran únicamente para su análisis técnico y no se devuelven ni se muestran a los usuarios finales. Se emplea exclusivamente para comparar el rendimiento del nuevo modelo contra el vigente sin asumir ningún riesgo operativo para el usuario.

## 4. Monitorización, observabilidad y mantenimiento de modelos

A diferencia del software tradicional, el rendimiento de un modelo de IA tiende a degradarse orgánicamente con el tiempo debido a cambios dinámicos en el entorno de los datos y en el comportamiento del mundo real.

*   **Sistema de gestión de riesgos (Artículo 9 del Reglamento UE 2024/1689):** Para los sistemas de IA de alto riesgo se debe establecer, implantar, documentar y mantener un sistema de gestión de riesgos, entendido como un proceso iterativo continuo, planificado y ejecutado a lo largo de todo el ciclo de vida del sistema, que exige revisiones y actualizaciones sistemáticas y periódicas. Comprende, entre otras, las siguientes etapas:
    1.  La determinación y el análisis de los riesgos conocidos y previsibles que el sistema pueda plantear para la salud, la seguridad o los derechos fundamentales cuando se utilice conforme a su finalidad prevista.
    2.  La estimación y evaluación de los riesgos que puedan surgir tanto por el uso conforme a la finalidad prevista como por un uso indebido razonablemente previsible.
    3.  La evaluación de otros riesgos que puedan surgir a partir del análisis de los datos recogidos mediante el sistema de vigilancia poscomercialización (artículo 72).
    4.  La adopción de medidas adecuadas y específicas de gestión de riesgos, diseñadas para eliminar o reducir los riesgos detectados mediante el diseño y desarrollo del sistema, mitigarlos cuando no puedan eliminarse, e informar de ellos a los responsables del despliegue cuando corresponda.
    Las pruebas del sistema de IA de alto riesgo se realizan, según proceda, en cualquier momento del proceso de desarrollo y, en todo caso, antes de la introducción en el mercado o puesta en servicio, con parámetros y umbrales de probabilidad previamente definidos y adecuados a la finalidad prevista. El sistema de gestión de riesgos debe prestar especial atención a si el sistema puede afectar negativamente a menores de dieciocho años o a otros colectivos vulnerables.

*   **Monitorización técnica y observabilidad:** Consiste en la supervisión continua a dos niveles: el rendimiento computacional o de infraestructura (latencia de inferencia, uso de memoria, consumo de CPU/GPU, tasa de errores HTTP) y el rendimiento estadístico o predictivo del modelo. Desde la perspectiva de los datos, se vigilan estrechamente dos fenómenos de degradación:
    *   **Data Drift (Deriva de datos o *Covariate Shift*):** Alteración en las propiedades estadísticas y distribuciones subyacentes de las variables independientes (datos de entrada) a lo largo del tiempo frente a los datos con los que el modelo fue entrenado originalmente.
    *   **Concept Drift (Deriva del concepto):** Cambio en la relación estadística subyacente entre las variables de entrada y la variable objetivo a predecir. Provoca una caída directa en la exactitud y precisión, constituyendo la degradación funcional del modelo (*Model Decay*).

*   **Vigilancia poscomercialización (Artículo 72 del Reglamento UE 2024/1689):** Los proveedores de sistemas de IA de alto riesgo están legalmente obligados a establecer y operar un sistema de vigilancia poscomercialización proporcionado a la naturaleza de la tecnología y los riesgos del sistema. Este sistema debe recopilar, documentar y analizar de manera activa y sistemática los datos pertinentes proporcionados por los responsables del despliegue u obtenidos a través de otras fuentes sobre el funcionamiento del sistema durante toda su vida útil. Debe basarse en un **plan de vigilancia poscomercialización** formalmente documentado, integrado en la documentación técnica del sistema, permitiendo evaluar el cumplimiento continuo de los requisitos del Reglamento.

*   **Comunicación de incidentes graves (Artículo 73 del Reglamento UE 2024/1689):** Los proveedores de sistemas de IA de alto riesgo están obligados a comunicar a las autoridades de vigilancia del mercado pertinentes todo incidente grave inmediatamente después de haber establecido un vínculo causal entre el sistema de IA y el incidente grave (o la probabilidad razonable de dicho vínculo). La notificación debe realizarse, en cualquier caso, en un plazo máximo de 15 días a partir de que el proveedor tenga conocimiento del incidente grave.

*   **Archivos de registro (Logs) (Artículo 12 del Reglamento UE 2024/1689):** Los sistemas de IA de alto riesgo deben permitir técnicamente el registro automático de acontecimientos a lo largo de todo su ciclo de vida. Estos registros facilitan la trazabilidad, la vigilancia poscomercialización, el seguimiento del funcionamiento y la detección de situaciones que puedan presentar riesgos o dar lugar a una modificación sustancial.

*   **Mantenimiento:** Incluye la ejecución de los pipelines de reentrenamiento de modelos (*Continuous Training*) para corregir la deriva, el parcheo de vulnerabilidades de seguridad de las dependencias subyacentes y la gestión de incidentes técnicos.

## 5. Versionado, reproducibilidad y mejora continua

La gobernanza técnica y la trazabilidad exhaustiva son requisitos operativos y regulatorios indispensables a lo largo de todo el ciclo de vida de la IA.

*   **Versionado y Trazabilidad:** Dado el carácter iterativo y experimental del Machine Learning, se debe mantener un registro exacto e inmutable de la tríada que conforma el sistema:
    1.  *Versiones del código fuente e hiperparámetros* (ej. sistemas Git).
    2.  *Versiones de los conjuntos de datos* de entrenamiento y evaluación (ej. herramientas como DVC - Data Version Control).
    3.  *Versiones de los pesos, artefactos y metadatos del modelo* (ej. repositorios como MLflow Model Registry o Weights & Biases).

*   **Sistema de gestión de la calidad (Artículo 17 del Reglamento UE 2024/1689):** Los proveedores de sistemas de IA de alto riesgo deben establecer un sistema de gestión de la calidad que garantice el cumplimiento del Reglamento, consignado de manera sistemática y ordenada en documentación que recoja las políticas, los procedimientos y las instrucciones correspondientes. Debe incluir, al menos:
    *   Una estrategia para el cumplimiento de la normativa, incluidos los procedimientos de evaluación de la conformidad y de gestión de las modificaciones del sistema.
    *   Las técnicas, procedimientos y actuaciones sistemáticas empleadas en el diseño, el control y la verificación del diseño del sistema.
    *   Las técnicas, procedimientos y actuaciones sistemáticas empleadas en el desarrollo del sistema y en el control y aseguramiento de su calidad.
    *   Los procedimientos de examen, prueba y validación que se llevarán a cabo antes, durante y después del desarrollo, así como su frecuencia.
    *   Las especificaciones técnicas aplicadas, incluidas las normas armonizadas correspondientes.
    *   Los sistemas y procedimientos de gestión de datos empleados (adquisición, recogida, análisis, etiquetado, almacenamiento, filtrado, minería, agregación, conservación).
    *   El sistema de gestión de riesgos a que se refiere el artículo 9.
    *   El establecimiento, la aplicación y el mantenimiento de un sistema de vigilancia poscomercialización conforme al artículo 72.
    *   Los procedimientos relativos a la notificación de incidentes graves conforme al artículo 73.
    *   La gestión de la comunicación con las autoridades competentes, los organismos notificados, otros operadores, clientes u otras partes interesadas.
    *   Los sistemas y procedimientos de conservación de registros de toda la documentación e información pertinente.
    *   La gestión de recursos, incluidas las medidas relativas a la seguridad del suministro.
    *   Un marco de rendición de cuentas que defina las responsabilidades de la dirección y del resto del personal respecto a los aspectos anteriores.
    La aplicación de este sistema debe ser proporcional al tamaño de la organización del proveedor, sin que ello rebaje el grado de rigor ni el nivel de protección exigido para garantizar el cumplimiento del Reglamento.

*   **Conservación de la documentación (Artículo 18 del Reglamento UE 2024/1689):** El Reglamento establece la obligación de mantener a disposición de las autoridades nacionales competentes documentación crítica durante un período de **diez años** a contar desde la introducción en el mercado o la puesta en servicio del sistema de IA de alto riesgo. Esta documentación incluye:
    a) La documentación técnica completa del sistema.
    b) La documentación relativa al sistema de gestión de la calidad.
    c) La documentación relativa a los cambios aprobados por los organismos notificados, si procede.
    d) Las decisiones y otros documentos expedidos por los organismos notificados.
    e) La declaración UE de conformidad.

El apartado 2 del artículo 18 añade que cada Estado miembro determinará las condiciones en las que esta documentación permanecerá a disposición de las autoridades nacionales competentes durante ese periodo de diez años en los casos en que el proveedor o su representante autorizado quiebre o cese en su actividad antes de que finalice dicho plazo.

*   **Reproducibilidad:** Es la capacidad técnica de recrear y entrenar un modelo exacto utilizando las mismas versiones de datos, código y entorno de ejecución original. Es un principio de ingeniería crucial para las auditorías algorítmicas, la resolución de incidentes (troubleshooting) y para demostrar la conformidad y solidez del sistema ante las autoridades de vigilancia del mercado.

*   **Mejora continua y modificaciones sustanciales:** Los sistemas de IA pueden presentar capacidad de adaptación tras el despliegue (sistemas de aprendizaje continuo u *online learning*). Desde la perspectiva jurídica (Reglamento de IA), los cambios en el algoritmo y en el funcionamiento de los sistemas que siguen aprendiendo después de su puesta en servicio **no** constituyen una *modificación sustancial* (que obligaría a un nuevo procedimiento de evaluación de la conformidad) siempre y cuando dichos cambios y su lógica de adaptación hayan sido predeterminados de forma estricta por el proveedor y evaluados en la evaluación de la conformidad inicial. No obstante, deben aplicarse medidas técnicas de contención sólidas para evitar que los resultados de salida sesgados influyan negativamente en las informaciones de entrada de futuras operaciones, mitigando los bucles de retroalimentación perjudiciales.

## Referencias técnicas y normativas

*   Reglamento (UE) 2024/1689, por el que se establecen normas armonizadas en materia de inteligencia artificial (artículos 9, 10, 11, 12, 15, 17, 18, 43, 47, 60, 72 y 73).
*   Lewis, P. et al., *"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"*, Facebook AI Research, NeurIPS 2020 (arXiv:2005.11401).
*   Hu, E. J. et al., *"LoRA: Low-Rank Adaptation of Large Language Models"*, Microsoft, ICLR 2022 (arXiv:2106.09685).
*   Google Cloud, *"MLOps: Continuous delivery and automation pipelines in machine learning"*, Cloud Architecture Center.
*   NIST, *"Artificial Intelligence Risk Management Framework (AI RMF 1.0)"*, enero de 2023.
*   ISO/IEC 42001:2023, *"Information technology — Artificial intelligence — Management system"*.
