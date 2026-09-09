---
id: "cm-ad-innovacion-y-transformacion-digital-tema-008-gobierno-del-dato-y-marco-DAMA-DMBOK"
title: "Gobierno del dato y marco DAMA-DMBOK"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/innovacion-y-transformacion-digital"
profiles:
  - "p06-ingeniero-desarrollo"
official_profiles:
  - "P06 - Ingeniero de Desarrollo"
official_topic: "Tema 8. Gobierno del dato y marco DAMA-DMBOK"
source_ids: []
tags:
  - "gobierno-del-dato"
  - "DAMA"
  - "DMBOK"
  - "gestion-del-dato"
  - "ciclo-de-vida-del-dato"
created_at: "2026-09-03"
last_reviewed: "2026-09-09"
ai_generated: true
ai_sources:
  - "perplexity"
  - "chatgpt"
  - "gemini"
needs_human_review: true
---

# Tema 8. Gobierno del dato y marco DAMA-DMBOK

## 1. Concepto de gobierno del dato.

**Definición e implicaciones**
El Gobierno del Dato (Data Governance) se define como el ejercicio de autoridad, control y toma de decisiones compartida (planificación, monitorización y ejecución) sobre la gestión de los activos de datos de una organización. Su objetivo principal es asegurar que los datos sean fiables, seguros, accesibles, documentados y utilizables, alineando su gestión con los objetivos estratégicos de la entidad.

A diferencia de la *gestión del dato* (que tiene un carácter más técnico y operativo, orientado a la ejecución), el *gobierno del dato* ostenta un carácter estratégico y directivo. Proporciona el marco de políticas, procesos, estándares y métricas que dirigen y evalúan la gestión de la información.

**Marco normativo y estandarización**
El desarrollo del gobierno del dato en las Administraciones Públicas se apoya en un corpus normativo y técnico específico, destacando en el ámbito europeo y nacional:
*   **Reglamento (UE) 2022/868 (Data Governance Act):** Establece un marco para impulsar el intercambio de datos y aumentar la confianza en la intermediación de datos. Regula la reutilización de datos del sector público, los servicios de intermediación de datos y el altruismo de datos[cite: 1].
*   **Especificaciones UNE:** El ecosistema de estandarización español define directrices precisas a través de la familia de normas UNE[cite: 1]:
    *   *UNE 0077:* Gobierno del dato[cite: 1].
    *   *UNE 0078:* Gestión del dato[cite: 1].
    *   *UNE 0079:* Calidad del dato[cite: 1].
    *   *UNE 0085:* Implantación del gobierno del dato[cite: 1].

## 2. Marco DAMA-DMBOK: áreas de conocimiento.

El DAMA-DMBOK (Data Management Body of Knowledge), en su segunda edición (DMBOK2), es el marco de referencia internacional estándar desarrollado por DAMA (Data Management Association) para la gestión integral de datos. 

El modelo visual de DAMA se representa mediante la **Rueda de DAMA** (DAMA Wheel), que sitúa el Gobierno del Dato en el centro, interactuando de forma radial con otras 10 Áreas de Conocimiento (Knowledge Areas).

1.  **Gobierno de Datos (Data Governance):** Eje central. Define la dirección estratégica, la supervisión, las políticas, las métricas y la toma de decisiones sobre los activos de datos.
2.  **Arquitectura de Datos (Data Architecture):** Define la estructura global de los datos de la empresa, los modelos de datos a alto nivel y el diseño de la arquitectura tecnológica que soporta el flujo de información (Data Warehouse, Data Lake, Lakehouse)[cite: 1].
3.  **Modelado y Diseño de Datos (Data Modeling & Design):** Proceso de descubrimiento, análisis y especificación de requisitos de datos, representados en modelos conceptuales, lógicos y físicos.
4.  **Almacenamiento y Operaciones de Datos (Data Storage & Operations):** Diseño, implementación y soporte del almacenamiento de datos, maximizando su valor durante su ciclo de vida y garantizando el rendimiento y la recuperación.
5.  **Seguridad de los Datos (Data Security):** Garantizar la privacidad, la confidencialidad y el acceso adecuado a los datos en cumplimiento con el marco regulatorio (RGPD, ENS)[cite: 1].
6.  **Integración e Interoperabilidad de Datos (Data Integration & Interoperability):** Procesos de adquisición, extracción, transformación, movimiento, entrega, replicación (ETL/ELT) e intercambio de datos entre sistemas y unidades organizativas[cite: 1].
7.  **Gestión de Documentos y Contenidos (Document & Content Management):** Almacenamiento, protección, indexación y acceso a datos no estructurados y semiestructurados.
8.  **Datos Maestros y de Referencia (Reference & Master Data):** Gestión continua (MDM - Master Data Management) de los datos críticos de la organización (clientes, productos, ciudadanos) para asegurar que conforman una única fuente de la verdad ("Single Source of Truth")[cite: 1].
9.  **Data Warehousing e Inteligencia de Negocios (Data Warehousing & Business Intelligence):** Planificación, implementación y control de procesos que proporcionan datos para la toma de decisiones, análisis y reporting.
10. **Metadatos (Metadata):** Planificación, implementación y control de actividades para asegurar el acceso a metadatos integrados, precisos y de alta calidad. Incluye la creación de catálogos de datos y metadatos[cite: 1].
11. **Calidad de los Datos (Data Quality):** Planificación y ejecución de técnicas de medición, evaluación, mejora y certificación de la aptitud de los datos para su uso previsto.

## 3. Roles y responsabilidades en la gestión del dato.

La estructura organizativa del gobierno del dato exige la definición formal de roles con responsabilidades segregadas. Según las directrices de DMBOK y las mejores prácticas de la industria, destacan las siguientes figuras:

*   **Chief Data Officer (CDO):** Ejecutivo de más alto nivel responsable de definir y liderar la estrategia corporativa de datos. Preside el Consejo de Gobierno del Dato y garantiza la alineación con los objetivos de negocio.
*   **Comité/Consejo de Gobierno del Dato (Data Governance Council):** Órgano directivo y decisorio interdepartamental. Se encarga de priorizar iniciativas, aprobar políticas, asignar recursos y actuar como última instancia en la resolución de conflictos sobre datos.
*   **Propietario del Dato (Data Owner):** Figura de negocio (no técnica) responsable en última instancia de la calidad, definición, seguridad y autorización de acceso a un dominio de datos específico (ej. "Datos de Recursos Humanos").
*   **Gestor del Dato (Data Steward):** Enlace operativo entre negocio y tecnología. Se encarga de la gestión diaria del dato: vela por la calidad, define y valida metadatos, resuelve anomalías y vela por el cumplimiento de las políticas definidas por el Data Owner. Suele dividirse en roles especializados (Business Data Steward, Technical Data Steward).
*   **Custodio del Dato (Data Custodian):** Rol puramente tecnológico (habitualmente del área de Sistemas o Bases de Datos). Es responsable de la infraestructura técnica (almacenamiento, copias de seguridad, rendimiento, arquitectura). Implementa los controles de seguridad y acceso aprobados por el Data Owner.

## 4. Ciclo de vida del dato.

El ciclo de vida del dato (Data Lifecycle) aborda las diferentes etapas por las que transita la información desde su concepción hasta su eventual destrucción. A diferencia del ciclo de vida del desarrollo de sistemas (SDLC), el ciclo de vida del dato tiene una persistencia mayor e independiente de los sistemas que lo albergan. DAMA lo estructura en las siguientes fases fundamentales:

1.  **Planificación / Ideación (Plan):** Definición de la necesidad, los requerimientos analíticos o de IA, y el diseño de la arquitectura y el modelo de datos.
2.  **Creación / Captura (Create/Obtain):** Fase de entrada de la información. Incluye la captura directa mediante transacciones, ingesta mediante pipelines (ETL/ELT, streaming), adquisición de terceros o generación mediante sistemas de Inteligencia Artificial[cite: 1].
3.  **Almacenamiento y Mantenimiento (Store & Maintain):** Persistencia técnica de los datos en plataformas (Data Lake, Lakehouse, bases de datos)[cite: 1]. Involucra operaciones de enriquecimiento, depuración, cifrado y perfilado para asegurar la calidad.
4.  **Uso (Use):** Explotación de los datos. Incluye la integración de sistemas, la analítica avanzada, la apertura de datos (Open Data), el Business Intelligence y el entrenamiento e inferencia en modelos de IA (Machine Learning)[cite: 1].
5.  **Archivo (Archive):** Traslado de los datos que ya no son activamente necesarios para las operaciones transaccionales, pero que deben conservarse por imperativo legal, regulatorio (ej. ENS, Esquema Nacional de Interoperabilidad) o histórico, a un medio de almacenamiento secundario a largo plazo.
6.  **Destrucción / Eliminación (Destroy/Dispose):** Eliminación segura y definitiva de los datos una vez finalizado su plazo de conservación legal, técnica y operativa, garantizando el cumplimiento de la LOPDGDD y el RGPD[cite: 1].

En el ámbito analítico avanzado y de Inteligencia Artificial, la gestión del ciclo de vida del dato se integra ineludiblemente con la gestión del ciclo de vida de la IA (MLOps, LLMOps, AgentOps end-to-end), aplicando los estándares de experimentación, validación, despliegue, monitorización (drift) y mejora continua[cite: 1].

## 5. Buenas prácticas en gobierno del dato.

La implementación exitosa del gobierno del dato exige un enfoque paulatino e integral, que transcienda la dimensión tecnológica para abordar las dimensiones cultural y organizativa.

**Implantación de la Cultura del Dato**
La adopción de una cultura del dato y la ética en la IA resulta fundamental[cite: 1]. Como se establece en el Plan Estratégico de Madrid Digital 2022-2026, las organizaciones aprovechan al máximo el valor de sus datos cuando tienen una cultura del dato[cite: 3]. Para su correcta implantación, no basta con la tecnología; es ineludible llevar a cabo un cambio cultural que modifique la mentalidad, las actitudes y los hábitos, integrando los datos en la propia identidad de la organización[cite: 3]. El personal debe querer usar los datos y alentar a otros a hacer lo mismo[cite: 3]. 

**Directrices operativas y estratégicas**
*   **Gestión Integral (Disponibilidad, Integridad, Usabilidad y Seguridad):** Se requiere gestionar estos atributos a todos los niveles (operativo, táctico y estratégico) para maximizar el valor de la información y alinearlos con la estrategia corporativa[cite: 3].
*   **Cohesión y Visión Unificada:** Establecer una cultura de análisis de datos a nivel organizativo potencia la cohesión. Disponer de la información integrada ayuda a unificar visiones y tomar decisiones que beneficien al conjunto de la organización, evitando los silos de información[cite: 3].
*   **Medición y Monitorización (KPIs):** Definir y realizar un seguimiento de indicadores y cuadros de mando que permitan medir el impacto, la adopción, la calidad y el valor aportado por los proyectos de datos e IA[cite: 1].
*   **Fomento de la Interoperabilidad y la Reutilización:** Aplicar estándares, contratos de datos comunes e interfaces para favorecer la reutilización de datos, la portabilidad y la escalabilidad de las soluciones de analítica avanzada[cite: 1].
*   **Estrategia Iterativa:** Adoptar metodologías ágiles en la implantación del gobierno del dato, focalizando esfuerzos inicialmente en dominios de datos críticos (Master Data) mediante casos de uso priorizados por valor, riesgo y factibilidad[cite: 1].
