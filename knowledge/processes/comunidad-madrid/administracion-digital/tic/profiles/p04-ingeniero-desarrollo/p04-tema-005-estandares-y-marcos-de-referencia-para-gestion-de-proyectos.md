---
id: "cm-ad-tic-p04-tema-005-estandares-marcos"
title: "Estándares y Marcos de Referencia para la Gestión de Proyecto"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/tic"
profiles:
  - "p04-ingeniero-desarrollo"
official_profile: "P04 - Ingeniero de Desarrollo"
official_topic: "Tema 5. Estándares y Marcos de Referencia para la Gestión de Proyecto"
source_ids:
tags:
  - "gestion-proyectos"
  - "pmbok"
  - "prince2"
  - "scrum"
  - "kanban"
  - "iso-21502"
created_at: "2026-08-08"
last_reviewed: null
ai_generated: true
ai_sources:
  - "gemini"
needs_human_review: true
---

# Tema 5. Estándares y Marcos de Referencia para la Gestión de Proyecto

## 1. PRINCE2 (PRojects IN Controlled Environments)

PRINCE2 no es un conjunto de buenas prácticas general, es una **metodología estructurada** y orientada a procesos. Como dice su nombre, busca entornos "controlados" para minimizar la incertidumbre [cite: 7].

**Patrón Lógico y Conceptos Clave de PRINCE2:**
*   **Business Case (Caso de Negocio):** Es el corazón de PRINCE2. Un proyecto solo se inicia y se mantiene vivo si el Business Case justifica que los beneficios superan a los costes y riesgos [cite: 7]. Se revisa continuamente [cite: 7].
*   **Gestión por Excepción:** Se definen unas "tolerancias" (márgenes de desviación permitidos en tiempo, coste, alcance, calidad, etc.). El Jefe de Proyecto trabaja de forma autónoma mientras no se superen. Si se prevé superar la tolerancia, se genera una "excepción" y se escala a la dirección para que decida [cite: 7].
*   **Enfoque en Productos:** PRINCE2 no se centra solo en las tareas a realizar, sino principalmente en la definición clara de los productos que se van a entregar.

---

## 2. PMBOK (Project Management Body of Knowledge)

A diferencia de PRINCE2, el PMBOK (del PMI) no es una metodología prescriptiva (no te dice paso a paso qué hacer), sino una **guía de buenas prácticas** y un estándar (ANSI) [cite: 7].

**Evolución en las Ediciones:**
*   **PMBOK 7ª Edición:** Supuso un cambio de paradigma radical respecto a las anteriores. Pasó de estar basado en "Procesos" (las famosas 10 áreas de conocimiento) a estar basado en **"Principios" y "Dominios de Desempeño"**. Se volvió mucho más adaptable, enfocándose en la entrega de valor y abrazando tanto enfoques predictivos (cascada) como adaptativos (ágiles).
*   **PMBOK 8ª Edición:** (La tendencia actual del PMI consolida el enfoque de la 7ª). Sigue profundizando en la orientación al valor, la adaptación ("tailoring"), la hibridación de metodologías y el impacto de la Inteligencia Artificial y la automatización en la gestión de proyectos.

---

## 3. Metodologías Ágiles: Scrum y Kanban

En entornos donde la incertidumbre es alta y los requisitos cambian rápidamente, se aplican los marcos ágiles.

### 3.1. Scrum
Es un marco de trabajo (framework) iterativo e incremental [cite: 7]. 

**Patrón de Roles en Scrum [cite: 7]:**
1.  **Product Owner:** Es el cliente. Prioriza los requisitos (escribe las historias de usuario) en el *Product Backlog* maximizando el valor de negocio [cite: 7].
2.  **Scrum Master:** El facilitador. Elimina los obstáculos (impedimentos) y asegura que se siga el proceso Scrum [cite: 7].
3.  **Equipo de Desarrollo (Team):** Equipo autoorganizado que construye el incremento de producto [cite: 7].

**Patrón de Eventos y Artefactos [cite: 7]:**
*   **Sprint:** Iteración corta (2 a 4 semanas) con los requisitos "congelados" [cite: 7].
*   **Reuniones Clave:** *Sprint Planning* (qué vamos a hacer), *Daily Scrum* (sincronización diaria de 15 min), *Sprint Review* (demostración del producto al cliente) y *Sprint Retrospective* (mejora continua del equipo) [cite: 7].
*   **Gráfico Burn Down:** Mide el trabajo pendiente por realizar en el sprint a lo largo del tiempo [cite: 7].

### 3.2. Kanban
Método basado en el flujo continuo ("just in time") [cite: 7].

**Patrón de Reglas Kanban [cite: 7]:**
1.  **Visualizar el flujo:** Uso de un tablero dividido en columnas (ej. Cola, Análisis, Desarrollo, Pruebas) [cite: 7].
2.  **Limitar el WIP (Work in Progress):** Es la regla fundamental. Se limita el número máximo de tareas que pueden estar en cada columna para detectar cuellos de botella y asegurar el flujo [cite: 7].
3.  **Medir y optimizar (Throughput / Lead Time):** Se evalúa la cantidad de trabajo finalizado y el tiempo que tarda una tarea desde que entra hasta que sale del tablero [cite: 7].

*(Nota: **Scrumban** es la hibridación de ambos: usa las iteraciones y reuniones de Scrum, pero gestiona el flujo de trabajo con un tablero y límites WIP típicos de Kanban)* [cite: 7].

---

## 4. ISO 21502

La norma **ISO 21502:2020** (Gestión de proyectos, programas y carteras - Orientación sobre la gestión de proyectos) vino a sustituir a la antigua ISO 21500.

**Conceptos Clave para el Test:**
*   **No es certificable:** Al igual que EFQM, es una guía de orientación, no se emiten certificados de cumplimiento ISO 21502 para organizaciones (a diferencia de la ISO 9001).
*   **Enfoque integral:** Ofrece directrices de alto nivel sobre conceptos y prácticas, centrándose no solo en la ejecución del proyecto, sino en el **entorno de la organización** y en cómo los proyectos contribuyen a la estrategia general, programas y carteras (portfolios).

---

## 5. Patrones de Examen y "Palabras Chivatas"

| Concepto | Palabra Chivata en el Test |
| :--- | :--- |
| **PRINCE2** | "Business Case continuo" [cite: 7], "Entornos controlados" [cite: 7], "Gestión por excepción", "Orientado a productos". |
| **PMBOK** | "Guía de buenas prácticas", "PMI", "Basado en principios y dominios de desempeño" (si es a partir de la 7ª edición). |
| **Scrum - Product Owner** | "Voz del cliente", "Prioriza el Backlog", "Maximiza el valor de negocio" [cite: 7]. |
| **Scrum - Sprint** | "Iteración de 2-4 semanas", "Requisitos congelados" [cite: 7]. |
| **Kanban** | "Limitar el WIP (trabajo en curso)" [cite: 7], "Tablero visual", "Flujo continuo". |
| **ISO 21502** | "Guía", "No certificable", "Gestión de proyectos, programas y carteras". |

### 5.1. Simulacro de Test: Desmontando trampas

**Pregunta:**
*Un equipo de desarrollo de software está implementando una metodología ágil. Han decidido utilizar un tablero visual para representar las distintas fases de su proceso y han establecido reglas estrictas que prohíben que haya más de tres tareas simultáneas en la columna de "Pruebas". ¿Qué metodología o práctica están aplicando principalmente?*
a) Scrum, aplicando el artefacto Sprint Backlog.
b) Programación Extrema (XP), mediante la propiedad colectiva del código.
c) PRINCE2, utilizando la gestión por excepción.
d) Kanban, aplicando límites WIP (Work In Progress).

**Razonamiento Estructurado:**
1.  **Busca el patrón:** El enunciado habla de un "tablero visual" y de "prohibir que haya más de tres tareas simultáneas en una columna". La palabra chivata es "límite de tareas simultáneas".
2.  **Aplica tu patrón lógico de descarte:**
    *   (C) PRINCE2 es un marco tradicional estructurado (cascada), no es ágil ni usa tableros de flujo [cite: 7]. Falsa.
    *   (B) XP se centra en las prácticas de programación (programación por parejas, pruebas unitarias TDD), no en limitar el flujo de tareas en un tablero [cite: 7]. Falsa.
    *   (A) Scrum usa un tablero a veces, pero su elemento restrictivo no es limitar las tareas por columna, sino limitar las tareas por *tiempo* (el Sprint, donde los requisitos se congelan) [cite: 7].
    *   (D) **Kanban**. Limitar el "Trabajo en Curso" (WIP) por cada fase/columna es la característica definitoria y exclusiva de Kanban [cite: 7].
3.  **Respuesta correcta:** D.
