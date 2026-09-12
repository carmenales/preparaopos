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
  - "proyectos-ia"
  - "metodologias-agiles"
  - "gestion-ciclo-de-vida-de-modelos"
created_at: "2026-09-03"
last_reviewed: null
ai_generated: true
ai_sources:
  - "perplexity"
  - "chatgpt"
  - "gemini"
needs_human_review: true
---

# Tema 14. Metodología de proyectos de datos: CRISP-DM

CRISP-DM (*Cross-Industry Standard Process for Data Mining*) es el marco de trabajo y la metodología estándar de facto más utilizada a nivel mundial para el desarrollo de proyectos de minería de datos, análisis predictivo e Inteligencia Artificial. Su principal característica es que es un modelo iterativo, cíclico y flexible, independiente de la tecnología o herramienta subyacente.

## 1. Fases de CRISP-DM

El ciclo de vida de un proyecto según CRISP-DM se estructura en seis fases secuenciales, aunque iterativas (es común retroceder a fases anteriores según los hallazgos).

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

## 2. Aplicación práctica en proyectos de IA

La metodología CRISP-DM, aunque diseñada originalmente para minería de datos tradicional, se ha adaptado al ciclo de vida del *Machine Learning* y la Inteligencia Artificial moderna. 
La aplicación práctica en proyectos de IA requiere ciertas consideraciones adicionales:
*   **Datos no estructurados:** A las fases 2 y 3 se añaden técnicas de procesamiento de lenguaje natural (NLP) o visión artificial (Computer Vision).
*   **Ética y explicabilidad:** En la fase de Evaluación, además del rendimiento, se exige analizar la caja negra del modelo (XAI - *Explainable AI*), comprobar la equidad (ausencia de sesgos discriminatorios) y cumplir el marco regulatorio (AI Act).
*   **Complejidad de algoritmos:** En la fase de Modelado, el uso de *Deep Learning* requiere capacidades de computación intensiva (GPUs) y mayor tiempo de entrenamiento, lo que altera los recursos del proyecto.

## 3. Relación con metodologías ágiles

CRISP-DM se integra de manera natural con metodologías ágiles (Scrum, Kanban) mediante la adaptación de los ciclos de vida del dato a los ciclos de desarrollo iterativo.
*   **Iteración rápida:** Un proyecto de IA ágil con CRISP-DM busca completar las seis fases en un producto mínimo viable (MVP) rápidamente, utilizando algoritmos simples de *baseline*. Las iteraciones posteriores refinan los datos y complejizan los modelos.
*   **Sprints de experimentación:** El desarrollo se divide en *sprints*. La fase de preparación de datos y modelado encaja en *Timeboxes* de experimentación donde el equipo de *Data Science* valida hipótesis.
*   **Equipos multidisciplinares:** La metodología ágil requiere un Product Owner (alineado con la Fase 1: Comprensión del negocio) trabajando junto a Data Engineers (Fase 2 y 3) y Data Scientists (Fase 4 y 5).

## 4. Gestión del ciclo de vida de modelos

En los entornos actuales, la fase 6 (Despliegue) de CRISP-DM evoluciona hacia la disciplina de **MLOps** (*Machine Learning Operations*), cuyo objetivo es unificar el desarrollo de sistemas de aprendizaje automático (ML) y su operación (Ops), garantizando la fiabilidad en la producción.

Elementos de la gestión del ciclo de vida de modelos:
*   **Despliegue continuo (CI/CD/CT):** Integración continua del código, entrega continua del modelo y entrenamiento continuo (CT - *Continuous Training*), donde el modelo se reentrena automáticamente al detectar nuevos patrones de datos.
*   **Monitorización del modelo en producción:** 
    *   **Data Drift (Deriva de datos):** Alteración en las propiedades estadísticas de la variable independiente (datos de entrada) a lo largo del tiempo.
    *   **Concept Drift (Deriva del concepto):** Cambio en la relación estadística entre las variables de entrada y la variable objetivo, que provoca la degradación del rendimiento del modelo (*Model Decay*).
*   **Registro y Versionado de modelos (Model Registry):** Uso de repositorios centrales (como MLflow o DVC) para almacenar modelos, parámetros, métricas y artefactos con control de versiones.
*   **Gobernanza de modelos:** Auditoría, control de acceso, validación de sesgos y trazabilidad para el cumplimiento normativo.