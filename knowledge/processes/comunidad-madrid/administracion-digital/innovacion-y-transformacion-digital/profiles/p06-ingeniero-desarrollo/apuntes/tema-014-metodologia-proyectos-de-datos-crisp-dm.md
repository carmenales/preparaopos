---
id: "cm-ad-innovacion-y-transformacion-digital-tema-014-metodologia-proyectos-de-datos-crisp-dm"
title: "Metodología de proyectos de datos: CRISP-DM"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/innovacion-y-transformacion-digital"
profiles:
  - "p06-ingeniero-desarrollo"
official_profiles:
  - "P06 - Ingeniero de Desarrollo"
official_topic: "Tema 14. Metodología de proyectos de datos: CRISP-DM"
source_ids: []
tags:
  - "crisp-dm"
  - "crisp-ml-q"
  - "kdd"
  - "semma"
  - "tdsp"
  - "asum-dm"
  - "proyectos-ia"
  - "metodologias-agiles"
  - "gestion-ciclo-de-vida-de-modelos"
  - "mlops"
  - "data-drift"
  - "concept-drift"
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

# Tema 14. Metodología de proyectos de datos: CRISP-DM

CRISP-DM (*Cross-Industry Standard Process for Data Mining*) es el marco de trabajo y la metodología estándar de facto más utilizada a nivel mundial para el desarrollo de proyectos de minería de datos, análisis predictivo e Inteligencia Artificial. Su principal característica es que es un modelo iterativo, cíclico y flexible, independiente de la tecnología o herramienta subyacente.

**Origen de la metodología**
CRISP-DM fue desarrollada entre 1996 y 2000 por un consorcio de empresas europeas conformado por **NCR, SPSS (posteriormente adquirida por IBM) y DaimlerChrysler**, con el respaldo de la Comisión Europea a través del programa ESPRIT. El documento fundacional de referencia, *"CRISP-DM 1.0: Step-by-Step Data Mining Guide"* (Chapman, Clinton, Kerber, Khabaza, Reinartz y Wirth, publicado por SPSS Inc. en el año 2000), constituye desde entonces el manual metodológico oficial de referencia, sin que haya existido hasta la fecha una versión 2.0 formalmente publicada por el consorcio original, aunque numerosas organizaciones han desarrollado adaptaciones propias (como CRISP-ML(Q), orientada específicamente a proyectos de Machine Learning con enfoque en calidad).

## 1. Fases de CRISP-DM

El ciclo de vida de un proyecto según CRISP-DM se estructura en seis fases secuenciales, aunque iterativas (es común retroceder a fases anteriores según los hallazgos). El propio manual metodológico original precisa que la secuencia de las fases **no es rígida**: el movimiento hacia adelante y hacia atrás entre fases distintas es siempre necesario, y el resultado de cada fase determina qué fase (o qué tarea concreta dentro de una fase) debe realizarse a continuación. El diagrama de referencia del ciclo de vida representa estas dependencias mediante flechas que indican las relaciones más importantes y frecuentes entre fases, sin que ello agote todas las relaciones posibles, que dependen en última instancia de los objetivos, el contexto y el interés del usuario sobre los datos.

### 1.1. Comprensión del negocio (*Business Understanding*)
Esta fase inicial se centra en comprender los objetivos y requisitos del proyecto desde una perspectiva puramente de negocio (o de servicio público), para luego convertir este conocimiento en la definición de un problema de análisis de datos.
*   **Determinación de objetivos de negocio:** Identificar los criterios de éxito y el valor aportado.
*   **Evaluación de la situación actual:** Análisis de recursos, requisitos, supuestos, restricciones y riesgos.
*   **Determinación de objetivos de minería de datos:** Traducción de los objetivos de negocio a objetivos técnicos.
*   **Plan de proyecto:** Definición de los pasos a seguir, tecnologías iniciales y asignación de tiempos.

### 1.2. Comprensión de los datos (*Data Understanding*)
Comienza con la recolección de los datos iniciales y continúa con actividades orientadas a familiarizarse con ellos, identificar problemas de calidad del dato y descubrir primeros patrones (Análisis Exploratorio de Datos - EDA).
*   **Recopilación de datos iniciales:** Identificación y extracción desde las fuentes de origen.
*   **Descripción de los datos:** Examen del volumen, formato y estructura de los datos adquiridos.
*   **Exploración de datos:** Aplicación de estadísticas básicas, consultas y visualizaciones (distribuciones, correlaciones).
*   **Verificación de la calidad de los datos:** Identificación de valores nulos, atípicos (*outliers*) o inconsistentes.

### 1.3. Preparación de datos (*Data Preparation*)
Fase que consume habitualmente entre el 70% y el 80% del tiempo del proyecto. Consiste en todas las tareas necesarias para construir el conjunto de datos final (el *dataset* que alimentará el modelo) a partir de los datos en bruto.
*   **Selección de datos:** Decidir qué subconjuntos de datos, tablas y atributos son relevantes.
*   **Limpieza de datos:** Imputación de valores faltantes, corrección de errores y tratamiento de *outliers*.
*   **Construcción de datos:** Creación de atributos derivados, transformación de variables y *Feature Engineering* (Ingeniería de características).
*   **Integración de datos:** Fusión y cruce de datos procedentes de múltiples bases de datos o archivos.
*   **Formateo de datos:** Cambios sintácticos, como reestructuración de formatos de fecha o normalización de textos.

### 1.4. Modelado (*Modeling*)
En esta fase se seleccionan y aplican diversas técnicas de modelado, y se calibran sus parámetros hasta alcanzar valores óptimos. Suelen existir varias técnicas para el mismo problema de minería de datos, lo que requiere volver a la fase de preparación de datos si la técnica elegida tiene requerimientos específicos.
*   **Selección de la técnica de modelado:** Decisión sobre el algoritmo a emplear (ej. Regresión Logística, Random Forest, Redes Neuronales).
*   **Generación del diseño de prueba:** División del conjunto de datos en subconjuntos de entrenamiento (*Train*), validación (*Validation*) y prueba (*Test*) para asegurar la robustez del modelo.
*   **Construcción del modelo:** Entrenamiento de los algoritmos con los datos preparados.
*   **Evaluación del modelo:** Evaluación técnica y ajuste de hiperparámetros (Accuracy, Precision, Recall, F1-Score, Curva ROC).

### 1.5. Evaluación (*Evaluation*)
En esta etapa se dispone de uno o varios modelos que parecen tener alta calidad desde el punto de vista técnico. Antes del despliegue definitivo, se debe asegurar que el modelo logra los objetivos de negocio definidos en la Fase 1.
*   **Evaluación de los resultados:** Contraste del rendimiento técnico con el criterio de éxito de negocio.
*   **Revisión del proceso:** Auditoría de los pasos ejecutados para asegurar que no se ha omitido ningún factor crítico o de cumplimiento (ej. sesgos cognitivos o infracción de protección de datos).
*   **Determinación de los próximos pasos:** Decisión GO/NO-GO sobre el paso a producción o la necesidad de iniciar una nueva iteración.

### 1.6. Despliegue (*Deployment*)
La creación del modelo generalmente no es el final del proyecto. El conocimiento adquirido o el modelo analítico deben integrarse en los procesos de la organización o de toma de decisiones.
*   **Plan de despliegue:** Integración del modelo en la arquitectura de sistemas corporativa (vía API, procesamiento batch, etc.).
*   **Plan de monitorización y mantenimiento:** Definición de la estrategia para vigilar el comportamiento del modelo a lo largo del tiempo.
*   **Producción del informe final:** Documentación de todo el proyecto y presentación de resultados a los *stakeholders*.
*   **Revisión final del proyecto:** Evaluación de las lecciones aprendidas.

**Estructura jerárquica de la metodología (los cuatro niveles de abstracción)**
El manual metodológico original de CRISP-DM precisa que el modelo de proceso se describe en una **jerarquía de cuatro niveles**, y no únicamente como una lista de seis fases, distinción que conviene conocer con precisión:
1.  **Fases (Phases):** el nivel más general, las seis fases ya descritas (Comprensión del negocio, Comprensión de los datos, Preparación de datos, Modelado, Evaluación y Despliegue).
2.  **Tareas genéricas (Generic Tasks):** dentro de cada fase, un conjunto de tareas genéricas suficientemente completo para cubrir todas las situaciones posibles de un proyecto de minería de datos (por ejemplo, dentro de la fase de Comprensión del Negocio: Determinar Objetivos de Negocio, Evaluar la Situación, Determinar los Objetivos de Minería de Datos y Producir el Plan de Proyecto).
3.  **Tareas especializadas (Specialized Tasks):** el nivel donde se describe cómo se llevan a cabo las acciones de las tareas genéricas en situaciones específicas (por ejemplo, si el problema es de limpieza de datos, si los datos son categóricos o continuos, o si el problema consiste en segmentación frente a clasificación).
4.  **Instancias de proceso (Process Instances):** el registro concreto de las acciones, decisiones y resultados de un proyecto real de minería de datos concreto, organizado según las fases, tareas y salidas definidas en los niveles anteriores.

**CRISP-ML(Q): la extensión de CRISP-DM para proyectos de Machine Learning**
CRISP-ML(Q) (*Cross-Industry Standard Process for the development of Machine Learning applications with Quality assurance methodology*) es un modelo de proceso propuesto por Studer et al. en el artículo *"Towards CRISP-ML(Q): A Machine Learning Process Model with Quality Assurance Methodology"* (2021), concebido explícitamente para mantener la compatibilidad conceptual con CRISP-DM subsanando dos carencias que sus autores identifican en el modelo original:
1.  CRISP-DM se centra en la minería de datos y no cubre el escenario de un modelo de Machine Learning que infiere decisiones en tiempo real de forma sostenida en el tiempo: el modelo debe adaptarse a un entorno cambiante o su rendimiento se degradará, por lo que resulta imprescindible una monitorización y un mantenimiento permanentes tras el despliegue.
2.  CRISP-DM carece de una metodología de aseguramiento de la calidad explícita para las aplicaciones de Machine Learning desplegadas como parte de un producto o servicio.

CRISP-ML(Q) se estructura en seis fases:
1.  **Business and Data Understanding** (Comprensión del negocio y de los datos): se ejecutan de forma conjunta, puesto que la disponibilidad real de los datos condiciona con frecuencia la viabilidad del proyecto.
2.  **Data Engineering** (Ingeniería/Preparación de datos).
3.  **Machine Learning Model Engineering** (Ingeniería del modelo de Machine Learning).
4.  **Machine Learning Model Evaluation** (Evaluación del modelo).
5.  **Deployment** (Despliegue).
6.  **Monitoring and Maintenance** (Monitorización y mantenimiento): fase añadida ex profeso respecto de CRISP-DM, dado el riesgo de degradación del modelo en un entorno cambiante; incluye el seguimiento continuo del rendimiento en producción para detectar dicha degradación, la actualización o el reentrenamiento del modelo cuando resulte necesario y el mantenimiento de su infraestructura y dependencias.

La aportación diferencial de CRISP-ML(Q) es que, para cada tarea de cada una de las seis fases, exige de forma sistemática: la definición de requisitos y restricciones (rendimiento, calidad del dato, robustez del modelo, etc.), la concreción de las tareas específicas correspondientes, la identificación de los riesgos que puedan perjudicar el éxito o la eficiencia de la aplicación (sesgo, sobreajuste, falta de reproducibilidad, entre otros) y la aplicación de métodos de aseguramiento de la calidad orientados a mitigar dichos riesgos.

## 2. Aplicación práctica en proyectos de IA

La metodología CRISP-DM, aunque diseñada originalmente para minería de datos tradicional, se ha adaptado al ciclo de vida del *Machine Learning* y la Inteligencia Artificial moderna.
La aplicación práctica en proyectos de IA requiere ciertas consideraciones adicionales:
*   **Datos no estructurados:** A las fases 2 y 3 se añaden técnicas de procesamiento de lenguaje natural (NLP) o visión artificial (Computer Vision).
*   **Ética y explicabilidad:** En la fase de Evaluación, además del rendimiento, se exige analizar la caja negra del modelo (XAI - *Explainable AI*), comprobar la equidad (ausencia de sesgos discriminatorios) y cumplir el marco regulatorio (Reglamento (UE) 2024/1689, de Inteligencia Artificial).
*   **Complejidad de algoritmos:** En la fase de Modelado, el uso de *Deep Learning* requiere capacidades de computación intensiva (GPUs) y mayor tiempo de entrenamiento, lo que altera los recursos del proyecto.

En el ámbito de la Administración Pública, la aplicación de CRISP-DM a proyectos de analítica institucional adapta habitualmente la denominación de la primera fase, sustituyendo "Comprensión del negocio" por **"Comprensión Institucional"**, entendida como la fase que parte de una necesidad o pregunta estratégica, operativa o de gestión que emerge del seguimiento y la planificación institucional del organismo correspondiente, manteniendo intacta la lógica y el resto de fases del modelo original.

## 3. Relación con metodologías ágiles

CRISP-DM se integra de manera natural con metodologías ágiles (Scrum, Kanban) mediante la adaptación de los ciclos de vida del dato a los ciclos de desarrollo iterativo.
*   **Iteración rápida:** Un proyecto de IA ágil con CRISP-DM busca completar las seis fases en un producto mínimo viable (MVP) rápidamente, utilizando algoritmos simples de *baseline*. Las iteraciones posteriores refinan los datos y complejizan los modelos.
*   **Sprints de experimentación:** El desarrollo se divide en *sprints*. La fase de preparación de datos y modelado encaja en *Timeboxes* de experimentación donde el equipo de *Data Science* valida hipótesis.
*   **Equipos multidisciplinares:** La metodología ágil requiere un Product Owner (alineado con la Fase 1: Comprensión del negocio) trabajando junto a Data Engineers (Fase 2 y 3) y Data Scientists (Fase 4 y 5).

Conviene precisar la relación conceptual entre ambos marcos: CRISP-DM es un modelo de **proceso o ciclo de vida del proyecto de datos** (qué hacer y en qué orden lógico), mientras que Scrum o Kanban son **marcos de gestión del trabajo** (cómo organizar equipos, tiempos y entregas). No son alternativas mutuamente excluyentes sino complementarias: es habitual mapear cada Sprint de Scrum a una o varias tareas concretas de una fase de CRISP-DM, de forma que el Product Backlog recoja hipótesis de análisis de datos priorizadas por valor de negocio, y cada Sprint Review muestre los resultados de la iteración de comprensión, preparación o modelado alcanzada hasta ese momento.

## 4. Gestión del ciclo de vida de modelos

En los entornos actuales, la fase 6 (Despliegue) de CRISP-DM evoluciona hacia la disciplina de **MLOps** (*Machine Learning Operations*), cuyo objetivo es unificar el desarrollo de sistemas de aprendizaje automático (ML) y su operación (Ops), garantizando la fiabilidad en la producción.

**Niveles de madurez MLOps**
Un marco de referencia ampliamente citado para caracterizar la madurez de la implantación de MLOps en una organización es el propuesto por **Google Cloud** en su guía de arquitectura *"MLOps: Continuous delivery and automation pipelines in machine learning"*, que distingue tres niveles progresivos de automatización:

*   **Nivel 0 (MLOps manual):** es el nivel más común y básico. El proceso completo, desde la preparación de datos hasta el despliegue, es manual y está impulsado por científicos de datos que trabajan en cuadernos interactivos (notebooks); no existe integración continua (CI) ni entrega continua (CD) real, y el traspaso del modelo entrenado al equipo de operaciones se realiza como un artefacto aislado, sin un pipeline reproducible.
*   **Nivel 1 (Automatización del pipeline de ML / Entrenamiento Continuo):** el objetivo de este nivel es realizar el reentrenamiento continuo del modelo (**CT - Continuous Training**) automatizando el propio pipeline de Machine Learning, lo que permite lograr la entrega continua del servicio de predicción del modelo. Se despliega y ejecuta de forma recurrente un pipeline completo (no ya un modelo aislado), y el reentrenamiento se dispara automáticamente ante la llegada de nuevos datos o la detección de una caída de rendimiento.
*   **Nivel 2 (Automatización CI/CD completa):** el nivel de mayor madurez, en el que se automatizan tanto el pipeline de ML como el propio pipeline de integración y entrega continua (CI/CD) que construye, prueba y despliega dicho pipeline, permitiendo a los equipos de ciencia de datos experimentar rápidamente con nueva lógica de modelado, extracción de características o hiperparámetros, e implementar estos experimentos en producción de forma prácticamente automática.

Elementos de la gestión del ciclo de vida de modelos:
*   **Despliegue continuo (CI/CD/CT):** Integración continua del código, entrega continua del modelo y entrenamiento continuo (CT - *Continuous Training*), donde el modelo se reentrena automáticamente al detectar nuevos patrones de datos.
*   **Monitorización del modelo en producción:**
    *   **Data Drift (Deriva de datos):** Alteración en las propiedades estadísticas de la variable independiente (datos de entrada) a lo largo del tiempo.
    *   **Concept Drift (Deriva del concepto):** Cambio en la relación estadística entre las variables de entrada y la variable objetivo, que provoca la degradación del rendimiento del modelo (*Model Decay*).
*   **Registro y Versionado de modelos (Model Registry):** Uso de repositorios centrales (como MLflow o DVC) para almacenar modelos, parámetros, métricas y artefactos con control de versiones.
*   **Gobernanza de modelos:** Auditoría, control de acceso, validación de sesgos y trazabilidad para el cumplimiento normativo.

## 5. Metodologías afines y comparativa

CRISP-DM no es la única metodología de referencia para estructurar proyectos de datos. Conviene conocer con precisión sus antecedentes, sus alternativas de la industria y sus evoluciones directas, ya que son objeto habitual de comparación.

*   **KDD (*Knowledge Discovery in Databases*):** Es el marco conceptual precedente y más amplio, formulado por Fayyad, Piatetsky-Shapiro y Smith en 1996, que define el descubrimiento de conocimiento como "el proceso no trivial de identificar patrones válidos, novedosos, potencialmente útiles y, en última instancia, comprensibles a partir de los datos". El proceso KDD se estructura clásicamente en cinco etapas: **Selección** (determinación de las fuentes y los datos relevantes), **Preprocesamiento/limpieza** (tratamiento de datos faltantes, ruido e inconsistencias), **Transformación** (reducción y proyección de los datos mediante variables adecuadas), **Minería de datos** (aplicación del algoritmo de extracción de patrones propiamente dicho) y **Evaluación/interpretación** (identificación de los patrones realmente interesantes y representación del conocimiento obtenido). La distinción conceptual clave es que, en la terminología KDD, la "minería de datos" es una única etapa del proceso completo de descubrimiento de conocimiento, mientras que en CRISP-DM esa etapa equivale aproximadamente a la fase de Modelado; KDD, además, ofrece una guía más general del trabajo a realizar en cada fase, frente al mayor grado de detalle operativo de CRISP-DM.

*   **SEMMA (*Sample, Explore, Modify, Model, Assess*):** Metodología desarrollada por el SAS Institute, estrechamente ligada a su herramienta SAS Enterprise Miner, que el propio fabricante describe como una organización lógica del conjunto de funcionalidades de dicho producto más que como una metodología de minería de datos independiente de la tecnología. Se estructura en cinco fases: **Sample** (extracción de una muestra representativa, suficientemente grande para contener información significativa pero manejable), **Explore** (búsqueda visual y estadística de relaciones y anomalías no anticipadas), **Modify** (selección, creación y transformación de variables de cara al modelado), **Model** (aplicación de las técnicas de minería de datos para obtener el modelo predictivo) y **Assess** (evaluación de la fiabilidad y utilidad de los resultados obtenidos). A diferencia de CRISP-DM, SEMMA no contempla de forma explícita ni una fase inicial de comprensión del negocio ni una fase final de despliegue, al estar centrada en el ciclo puramente analítico y técnico.

*   **TDSP (*Team Data Science Process*):** Metodología ágil e iterativa publicada por Microsoft, orientada a maximizar la colaboración y el aprendizaje en equipo en proyectos de analítica predictiva e IA. Estructura el ciclo de vida en cinco etapas: **Business Understanding**, **Data Acquisition and Understanding** (que combina de facto la comprensión y la limpieza de datos de CRISP-DM), **Modeling** (que combina el modelado y la evaluación de CRISP-DM), **Deployment** y una quinta etapa adicional, **Customer Acceptance** (validación explícita por parte del cliente de que la solución satisface las necesidades de negocio), que CRISP-DM no contempla de forma expresa. La aportación diferencial de TDSP frente a CRISP-DM es que define de forma explícita los roles del equipo de proyecto (arquitecto de soluciones, jefe de proyecto, ingeniero de datos, científico de datos, desarrollador de aplicaciones y responsable de proyecto) y una estructura estandarizada de carpetas, plantillas y artefactos de documentación para cada etapa, careciendo CRISP-DM de esta dimensión de organización de equipos.

*   **ASUM-DM (*Analytics Solutions Unified Method for Data Mining/Predictive Analytics*):** Metodología publicada por IBM en 2015 como evolución práctica de CRISP-DM, manteniendo su compatibilidad conceptual. Se estructura en cinco fases (Analyze, Design, Configure and Build, Deploy, y Operate and Optimize), gobernadas por un flujo de trabajo continuo de gestión de proyecto que discurre en paralelo a todas ellas. Su aportación diferencial respecto de CRISP-DM es la incorporación explícita de tareas y actividades de infraestructura, operación, gestión de proyecto y despliegue, junto con plantillas y guías prácticas asociadas a cada tarea, careciendo CRISP-DM original de esta dimensión operativa.

**Cuadro comparativo de metodologías**

| Metodología | Origen | Nº de fases | Fases principales | Rasgo distintivo |
| --- | --- | --- | --- | --- |
| **KDD** | Fayyad, Piatetsky-Shapiro y Smith (1996) | 5 | Selección · Preprocesamiento · Transformación · Minería de datos · Evaluación/interpretación | Marco conceptual más amplio; la "minería de datos" es solo una de sus etapas |
| **SEMMA** | SAS Institute | 5 | Sample · Explore · Modify · Model · Assess | Ligada a una herramienta (SAS Enterprise Miner); sin fases de negocio ni de despliegue |
| **CRISP-DM** | Consorcio NCR, SPSS/IBM y DaimlerChrysler (1996-2000) | 6 | Comprensión del negocio · Comprensión de los datos · Preparación de datos · Modelado · Evaluación · Despliegue | Estándar de facto, independiente de la tecnología, con jerarquía de 4 niveles |
| **ASUM-DM** | IBM (2015) | 5 | Analyze · Design · Configure and Build · Deploy · Operate and Optimize | Extiende CRISP-DM con tareas de infraestructura, operación y gestión de proyecto |
| **TDSP** | Microsoft | 5 | Business Understanding · Data Acquisition and Understanding · Modeling · Deployment · Customer Acceptance | Define roles de equipo y estructura estandarizada de artefactos; añade aceptación del cliente |
| **CRISP-ML(Q)** | Studer et al. (2021) | 6 | Business and Data Understanding · Data Engineering · ML Model Engineering · ML Model Evaluation · Deployment · Monitoring and Maintenance | Añade una fase de monitorización/mantenimiento y una metodología explícita de aseguramiento de la calidad en cada tarea |

## Referencias técnicas

*   Chapman, P., Clinton, J., Kerber, R., Khabaza, T., Reinartz, T., Shearer, C. y Wirth, R., *"CRISP-DM 1.0: Step-by-Step Data Mining Guide"*, SPSS Inc., 2000.
*   IBM, *Guía de CRISP-DM de IBM SPSS Modeler* (documentación oficial del modelo de referencia CRISP-DM).
*   IBM, *"Analytics Solutions Unified Method for Data Mining/Predictive Analytics (ASUM-DM)"*, 2015.
*   Fayyad, U., Piatetsky-Shapiro, G. y Smith, P., *"From Data Mining to Knowledge Discovery in Databases"*, AI Magazine, 1996.
*   Microsoft, *"What is the Team Data Science Process (TDSP)?"*, Azure Architecture Center.
*   Studer, S. et al., *"Towards CRISP-ML(Q): A Machine Learning Process Model with Quality Assurance Methodology"*, Machine Learning and Knowledge Extraction, 2021 (arXiv:2003.05155).
*   Google Cloud, *"MLOps: Continuous delivery and automation pipelines in machine learning"*, Cloud Architecture Center.
*   Reglamento (UE) 2024/1689, por el que se establecen normas armonizadas en materia de inteligencia artificial.
