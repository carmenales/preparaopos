---
id: "cm-ad-tic-p04-tema-005-estandares-marcos"
title: "Estándares y Marcos de Referencia para la Gestión de Proyecto"
type: "apunte"
status: "revisado"
processes:
  - "comunidad-madrid/administracion-digital/tic"
profiles:
  - "p04-ingeniero-desarrollo"
official_profile: "P04 - Ingeniero de Desarrollo"
official_topic: "Tema 5. Estándares y Marcos de Referencia para la Gestión de Proyecto"
source_ids:
  - "A2_Bloque_III.pdf"
  - "A2_Bloque_IV.pdf"
tags:
  - "gestion-proyectos"
  - "pmbok"
  - "prince2"
  - "scrum"
  - "kanban"
  - "iso-21502"
  - "itil"
created_at: "2026-08-08"
last_reviewed: "2026-08-29"
ai_generated: true
ai_sources:
  - "chatgpt"
  - "gemini"
  - "perplexity"
needs_human_review: false
---

# Tema 5. Estándares y Marcos de Referencia para la Gestión de Proyecto

## 1. PRINCE2 (PRojects IN Controlled Environments)

**PRINCE2** (mantenido por *PeopleCert*) es una **metodología estructurada y orientada a procesos** para la gestión eficaz de proyectos. A diferencia de una guía de buenas prácticas, establece un método prescriptivo de **gobernanza y control** diseñado para **minimizar la incertidumbre**.

```mermaid
graph TD
    classDef princ fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#000
    classDef prac fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000
    classDef proc fill:#f1f8e9,stroke:#33691e,stroke-width:2px,color:#000

    subgraph PRINCE2_7 ["PRINCE2 7"]
        direction TB
        P["<b>7 PRINCIPIOS</b><br>(Obligatorios y Universales)"]:::princ
        PR["<b>7 PRÁCTICAS</b><br>(Aspectos Transversales Continuos)"]:::prac
        PC["<b>7 PROCESOS</b><br>(Ciclo de Vida Cronológico)"]:::proc
        
        P --> PR --> PC
    end
```

### 1.1. Pilares Conceptuales de PRINCE2
*   **Justificación Comercial Continua** (*Business Case*): 
    *   Es el motor del proyecto. 
    *   La iniciativa solo debe iniciarse y continuar si se demuestra en todo momento que los beneficios superan a los costes y riesgos. 
    *   Si deja de ser viable en algún límite de fase, debe cerrarse de forma controlada.
*   **Gestión por Excepción** (*Management by Exception*): 
    *   Se delega autoridad mediante **6 tolerancias** (Tiempo, Coste, Calidad, Alcance, Beneficio y Riesgo). 
    *   Si se prevé superar un límite, se escala al *Project Board* mediante un *Exception Report* y un *Exception Plan*.
*   **Enfoque en los Productos** (*Focus on Products*): 
    *   La planificación parte de la definición formal de los entregables y sus criterios de calidad (*Product Descriptions* / PBS) antes de secuenciar las actividades.
*   **Aprender de la Experiencia:** 
    *   Se recopilan y aplican lecciones aprendidas de proyectos previos y a lo largo de la ejecución.
*   **Roles y Responsabilidades Definidos:** 
    *   Estructura organizativa con representación explícita del negocio, usuarios y proveedores.
*   **Gestión por Fases:** 
    *   División del proyecto en etapas manejables de planificación, supervisión y control.
*   **Adaptación al Entorno** (*Tailoring*): 
    *   Ajuste del método a la escala, complejidad, criticidad y riesgo, sin omitir ningún principio universal.

### 1.2. Gobernanza: El Project Board
El máximo órgano de gobierno gerencial está integrado por tres roles obligatorios:
*   **Executive (Ejecutivo):** Responsable individual último; propietario del *Business Case* y garante de la relación calidad-precio (*Value for Money*).
*   **Senior User (Usuario Principal):** Representa a quienes usarán la solución; especifica necesidades y rinde cuentas de la consecución de beneficios.
*   **Senior Supplier (Proveedor Principal):** Representa a los desarrolladores y técnicos; responde de la integridad técnica y calidad de los entregables.

### 1.3. PRINCE2 7: Las 7 Prácticas y los 7 Procesos
En **PRINCE2 7**, los antiguos "Temas" de la edición 6 pasan a denominarse formalmente **Prácticas**:

| 7 Prácticas (*Practices*) | 7 Procesos (*Processes*) |
| :--- | :--- |
| 1. **Business Case** (Caso de Negocio)<br>2. **Organizing** (Organización)<br>3. **Plans** (Planes)<br>4. **Quality** (Calidad)<br>5. **Risk** (Riesgo)<br>6. **Issues** (Cuestiones, sustituye a Cambio)<br>7. **Progress** (Progreso) | 1. **SU** - *Starting Up a Project* (Puesta en Marcha)<br>2. **DP** - *Directing a Project* (Dirección de un Proyecto)<br>3. **IP** - *Initiating a Project* (Inicio de un Proyecto)<br>4. **CS** - *Controlling a Stage* (Control de una Fase)<br>5. **MP** - *Managing Product Delivery* (Entrega de Productos)<br>6. **SB** - *Managing a Stage Boundary* (Límites de Fase)<br>7. **CP** - *Closing a Project* (Cierre del Proyecto) |

> **Novedades de PRINCE2 7**: Incorpora la gestión de personas como elemento transversal, sostenibilidad (*Green IT*), gobernanza de datos y modelos de entrega híbridos y adaptativos.


## 2. PMBOK (Project Management Body of Knowledge)

El **PMBOK** (publicado por el *PMI*) es un estándar *ANSI* y una **guía de fundamentos y buenas prácticas**, de carácter no prescriptivo.

```mermaid
graph LR
    classDef v6 fill:#f5f5f5,stroke:#757575,stroke-width:1px,color:#000
    classDef v7 fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#000
    classDef v8 fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000

    A["<b>PMBOK 6ª Ed. (2017)</b><br>• Enfoque en Procesos<br>• 5 Grupos de Procesos<br>• 10 Áreas de Conocimiento<br>• 49 Procesos rígidos"]:::v6
    
    B["<b>PMBOK 7ª Ed. (2021)</b><br>• Enfoque en Entrega de Valor<br>• 12 Principios Rectores<br>• 8 Dominios de Desempeño<br>• Estándar basado en principios"]:::v7
    
    C["<b>PMBOK 8ª Ed. (Nov. 2025)</b><br>• Enfoque Holístico y Accionable<br>• 6 Principios Fundamentales<br>• 7 Dominios de Desempeño<br>• 5 Áreas de Enfoque (40 procesos)<br>• IA, Sostenibilidad y PMO"]:::v8

    A --> B --> C
```

### 2.1. PMBOK 7ª Edición (2021)
Estableció la transición desde la estructura basada en procesos hacia un modelo orientado a la entrega de valor:
*   **12 Principios Rectores:** *Stewardship* (administración diligente), equipo colaborativo, interesados, enfoque en valor, pensamiento sistémico, liderazgo, *tailoring*, calidad, complejidad, riesgos, adaptabilidad/resiliencia y gestión del cambio.
*   **8 Dominios de Desempeño:** *Interesados, Equipo, Enfoque de Desarrollo y Ciclo de Vida, Planificación, Trabajo del Proyecto, Entrega, Medición* e *Incertidumbre*.

### 2.2. PMBOK 8ª Edición (Noviembre 2025)
Consolida y hace más práctica la guía, manteniendo los principios y dominios pero reintroduciendo orientación por procesos de forma no prescriptiva:

*   **6 Principios Fundamentales:**
    1. Adoptar una visión holística.
    2. Centrarse en el valor.
    3. Integrar la calidad.
    4. Liderar con responsabilidad (*Accountability*).
    5. Integrar la sostenibilidad.
    6. Construir equipos empoderados.
*   **7 Dominios de Desempeño:** *Gobernanza, Alcance, Cronograma, Finanzas, Interesados, Recursos* y *Riesgo*.
*   **5 Áreas de Enfoque** (*Focus Areas*): Recupera la orientación estructurada de 40 procesos distribuidos en *Inicio, Planificación, Ejecución, Monitoreo y Control*, y *Cierre*.
*   **Novedades Tecnológicas y de Gestión:** Incorporación formal del impacto de la **Inteligencia Artificial**, oficinas de dirección de proyectos (**PMO**), adquisiciones avanzadas y sostenibilidad ambiental/social.

### 2.3. Comparativa Estructural PMBOK 7ª vs. PMBOK 8ª

| Aspecto | PMBOK 7ª Edición (2021) | PMBOK 8ª Edición (Noviembre 2025) |
| :--- | :--- | :--- |
| **Principios** | **12 Principios** | **6 Principios Fundamentales** |
| **Dominios de Desempeño** | **8 Dominios** | **7 Dominios** |
| **Orientación de Procesos** | Eliminó los procesos rígidos en el estándar principal | **5 Áreas de Enfoque** con 40 procesos no prescriptivos |
| **Enfoque de Valor** | Entrega de valor en cualquier ciclo de vida | Entrega de valor integrada con gobernanza financiera y sostenibilidad |
| **Nuevas Dimensiones** | Modelos predictivos, ágiles e híbridos | **Inteligencia Artificial**, PMO, ESG y gobernanza de adquisiciones |

---

## 3. Metodologías Ágiles: Scrum y Kanban

Orientadas a proyectos en entornos complejos con alta volatilidad de requisitos, donde la entrega temprana de valor y la inspección continua priman sobre la planificación exhaustiva.

### 3.1. Scrum (Scrum Guide 2020)
Marco de trabajo (*framework*) iterativo e incremental basado en el **empirismo** (conocimiento derivado de la experiencia) y el control de procesos **Lean**.

```mermaid
graph TD
    classDef event fill:#e3f2fd,stroke:#1565c0,stroke-width:2px,color:#000
    classDef art fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000
    classDef commit fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px,color:#000

    PB["<b>Product Backlog</b><br>Lista priorizada de requisitos"]:::art -->|Commitment| PG["<b>Product Goal</b><br>Objetivo a largo plazo"]:::commit
    
    PB --> SP["Sprint Planning<br>(⏱️ Máx. 8h/mes)"]:::event
    
    SP --> SB["<b>Sprint Backlog</b><br>Plan + Ítems seleccionados"]:::art
    SB -->|Commitment| SG["<b>Sprint Goal</b><br>Objetivo de la iteración"]:::commit
    
    SB --> SPRINT["<b>SPRINT (1 a 4 semanas)</b><br>Contenedor de eventos"]:::event
    
    SPRINT --> DS["Daily Scrum<br>(⏱️ 15 min - Developers)"]:::event
    SPRINT --> INC["<b>Incremento</b><br>Software utilizable"]:::art
    
    INC -->|Commitment| DOD["<b>Definition of Done (DoD)</b><br>Criterio formal de calidad"]:::commit
    
    INC --> SR["Sprint Review<br>(⏱️ Máx. 4h/mes - Stakeholders)"]:::event
    SR --> SRet["Sprint Retrospective<br>(⏱️ Máx. 3h/mes - Scrum Team)"]:::event
```

*   **Los 3 Pilares Empíricos:** *Transparencia, Inspección y Adaptación*.
*   **Los 5 Valores:** *Compromiso, Foco, Apertura, Respeto y Coraje*.
*   **Estructura del Scrum Team (10 o menos personas, autogestionado):**
    *   **Product Owner:** Maximiza el valor del producto; gestiona y prioriza en exclusiva el *Product Backlog*.
    *   **Scrum Master:** Responsable de la efectividad del equipo y de liderar la adopción de Scrum; actúa como líder servicial eliminando impedimentos.
    *   **Developers:** Profesionales comprometidos a construir cualquier aspecto de un Incremento utilizable en cada Sprint.
*   **Los 3 Artefactos y sus 3 Compromisos** (*Commitments*):
    1.  **Product Backlog** $\rightarrow$ Su compromiso es el **Product Goal** (meta del producto a largo plazo).
    2.  **Sprint Backlog** $\rightarrow$ Su compromiso es el **Sprint Goal** (meta concreta de la iteración).
    3.  **Increment (Incremento)** $\rightarrow$ Su compromiso es la **Definition of Done (DoD)** (definición formal de terminado y estándar de calidad).

### 3.2. Kanban
Método de gestión visual del flujo de trabajo continuo ("just-in-time") derivado de Lean Manufacturing. No prescribe Sprints con duración fija ni roles predeterminados.

*   **Prácticas Fundamentales:**
    1.  *Visualizar el flujo:* Tablero segmentado por estados (Backlog, Análisis, Desarrollo, Test, Done).
    2.  *Limitar el Trabajo en Curso (WIP - Work In Progress):* **Regla cardinal**. Fija el límite máximo de tarjetas por columna para evitar la sobrecarga y aflorar cuellos de botella.
    3.  *Gestionar y medir el flujo:* Optimización continua mediante políticas explícitas.
*   **Métricas Clave de Flujo:**
    *   **Lead Time:** Tiempo transcurrido desde que la tarea es solicitada por el usuario hasta su entrega final.
    *   **Cycle Time:** Tiempo transcurrido desde que el equipo inicia el desarrollo activo de la tarea hasta su compleción.
    *   **Ley de Little:** $\text{WIP} = \text{Throughput} \times \text{Lead Time}$.
*   **Scrumban:** Enfoque híbrido que aplica tableros y límites WIP de Kanban dentro de los Sprints y eventos de Scrum.

## 4. ISO 21502:2020 y la Familia Normativa ISO 21500

La norma **ISO 21502:2020** (*Project, programme and portfolio management — Guidance on project management*) proporciona directrices para la gestión de proyectos en cualquier organización. Sustituye a la anterior **ISO 21500:2012**.

```mermaid
graph TD
    classDef fam fill:#e8eaf6,stroke:#283593,stroke-width:2px,color:#000
    classDef std fill:#e3f2fd,stroke:#1565c0,stroke-width:1px,color:#000
    classDef focal fill:#fff3e0,stroke:#e65100,stroke-width:2px,color:#000

    FAM["<b>FAMILIA NORMATIVA ISO 21500</b><br>(Gobernanza de Proyectos, Programas y Portafolios)"]:::fam
    
    FAM --> ISO21500["<b>ISO 21500:2021</b><br>Contexto y Conceptos Globales"]:::std
    FAM --> ISO21502["<b>ISO 21502:2020</b><br>Guía de GESTIÓN DE PROYECTOS"]:::focal
    FAM --> ISO21503["<b>ISO 21503:2022</b><br>Guía de Gestión de Programas"]:::std
    FAM --> ISO21504["<b>ISO 21504:2022</b><br>Guía de Gestión de Portafolios"]:::std
    FAM --> ISO21505["<b>ISO 21505:2017</b><br>Guía sobre Gobernanza"]:::std
    FAM --> ISO21506["<b>ISO 21506:2024</b><br>Vocabulario y Términos"]:::std
```

### 4.1. Características Esenciales de ISO 21502:2020
*   **Carácter No Certificable:** Al igual que el modelo **EFQM**, es una guía de directrices de alto nivel y buenas prácticas; las organizaciones no se certifican bajo **ISO 21502** (a diferencia de **ISO 9001** o **ISO 27001**).
*   **Agnóstica del Ciclo de Vida:** Admite modelos predictivos, incrementales, iterativos, adaptativos (ágiles) e híbridos.
*   **Enfoque de Proceso Integrado:** Estructura la gestión en prácticas previas, dirección, inicio, control, entrega, cierre y actividades posteriores, vinculadas a puntos de decisión (*gates* o compuertas de fase).
*   **Delimitación Temática:** Aunque el título del comité paraguas incluye programas y portafolios, **ISO 21502 se ocupa exclusivamente de proyectos**.


## 5. Relación con la Transición a Operaciones (ITIL v4)

La finalización de un proyecto TIC implica transferir los entregables a los equipos de explotación y soporte continuo. La práctica de **Habilitación del Cambio** (*Change Enablement*) de **ITIL v4** gobierna esta transición técnica para minimizar el impacto en la disponibilidad del servicio:

*   **Cambio Estándar:** Modificación recurrente, documentada, de bajo riesgo y preautorizada (*ej. reemplazo rutinario de hardware, parches estándar en preproducción*).
*   **Cambio Normal:** Modificación no recurrente que requiere solicitud formal (**RFC** - *Request for Change*), análisis de riesgos e impacto, ventana de mantenimiento, **Plan de Back-out obligatorio** (plan de reversión en caso de fallo) y aprobación por el **CAB / CAC** (*Change Advisory Board*).
*   **Cambio de Emergencia:** Resolución rápida ante incidentes críticos que amenazan la continuidad o seguridad; evaluado con urgencia por el **ECAB / CAC de Emergencia**.


## 6. Resumen

| Estándar / Marco | Enfoque Principal | Conceptos Clave / Palabras Chivata en Test |
| :--- | :--- | :--- |
| **PRINCE2 7** | Metodología estructurada de procesos | "Justificación comercial continua", "6 Tolerancias", "7 Prácticas, 7 Principios, 7 Procesos", "Project Board". |
| **PMBOK 7ª Ed.** | Guía de estándares de valor | "12 Principios", "8 Dominios de Desempeño", "The Standard for Project Management". |
| **PMBOK 8ª Ed. (2025)** | Guía estructurada holística | "6 Principios", "7 Dominios", "5 Áreas de Enfoque (40 procesos)", "IA y Sostenibilidad". |
| **Scrum** | Framework ágil empírico | "Transparencia-Inspección-Adaptación", "PO, SM, Developers", "Sprint (1-4 sem)", "3 Compromisos (Product Goal, Sprint Goal, DoD)". |
| **Kanban** | Método de flujo continuo | "Limitar el WIP (Trabajo en curso)", "Visualizar el flujo", "Lead Time vs. Cycle Time", "Ley de Little". |
| **ISO 21502:2020** | Guía de directrices de proyecto | "No certificable", "Agnóstica del ciclo de vida", "Solo proyectos dentro de la serie ISO 21500", "Puntos de decisión (Gates)". |
| **ITIL v4** | Gestión de servicios y cambios | "Change Enablement", "Cambio Normal (RFC, Back-out, CAB/CAC)", "Cambio Estándar preautorizado". |

## 7. Referencias Normativas y Técnicas

* **Project Management Institute (PMI)**, *A Guide to the Project Management Body of Knowledge (PMBOK® Guide)* — 7ª Edición (2021) y 8ª Edición (Noviembre 2025).
* **PeopleCert**, *PRINCE2® 7 Management Framework* (2023/2024).
* **Ken Schwaber y Jeff Sutherland**, *The Scrum Guide: The Definitive Guide to Scrum* (Noviembre 2020).
* **David J. Anderson**, *Kanban: Successful Evolutionary Change for Your Technology Business*.
* **ISO 21500:2021**, *Project, programme and portfolio management — Context and concepts*.
* **ISO 21502:2020**, *Project, programme and portfolio management — Guidance on project management*.
* **AXELOS**, *ITIL® 4: Create, Deliver and Support / Service Management Framework*.
