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
last_reviewed: "2026-08-08"
ai_generated: true
ai_sources:
  - "gemini"
  - "perplexity"
needs_human_review: true
---

# Tema 5. Estándares y Marcos de Referencia para la Gestión de Proyecto

## 1. PRINCE2 (PRojects IN Controlled Environments)

PRINCE2 no es un conjunto de buenas prácticas general, es una **metodología estructurada** y orientada a procesos. Como dice su nombre, busca entornos "controlados" para minimizar la incertidumbre [cite: 7].

**Patrón Lógico y Conceptos Clave de PRINCE2:**
*   **Business Case (Caso de Negocio):** Es el corazón de PRINCE2. Un proyecto solo se inicia y se mantiene vivo si el Business Case justifica que los beneficios superan a los costes y riesgos [cite: 7]. Se revisa continuamente [cite: 7].
*   **Gestión por Excepción:** Se definen unas "tolerancias" (márgenes de desviación permitidos en tiempo, coste, alcance, calidad, etc.). El Jefe de Proyecto trabaja de forma autónoma mientras no se superen. Si se prevé superar la tolerancia, se genera una "excepción" y se escala a la dirección para que decida [cite: 7].
*   **Enfoque en Productos:** PRINCE2 no se centra solo en las tareas a realizar, sino principalmente en la definición clara de los productos que se van a entregar.

PRINCE2 se estructura formalmente en **7 principios** (Justificación Comercial Continua, Aprender de la Experiencia, Roles y Responsabilidades Definidos, Gestión por Fases, Gestión por Excepción, Enfoque en los Productos y Adaptación al Entorno del Proyecto), **7 temas** (Business Case, Organización, Calidad, Planes, Riesgo, Cambio y Progreso) y **7 procesos** que marcan la secuencia temporal de gestión: Puesta en Marcha, Dirección de un Proyecto, Inicio de un Proyecto, Control de una Fase, Gestión de la Entrega de Productos, Gestión de los Límites de Fase y Cierre de un Proyecto. El órgano de gobierno del proyecto es el **Project Board**, compuesto por tres roles: **Executive** (máximo responsable, propietario del Business Case), **Senior User** (representa a los usuarios y sus beneficios esperados) y **Senior Supplier** (responde de la integridad técnica y calidad de los entregables).

## 2. PMBOK (Project Management Body of Knowledge)

A diferencia de PRINCE2, el PMBOK (del PMI) no es una metodología prescriptiva (no te dice paso a paso qué hacer), sino una **guía de buenas prácticas** y un estándar (ANSI) [cite: 7].

**Evolución en las Ediciones:**
*   **PMBOK 7ª Edición (2021):** Supuso un cambio de paradigma radical respecto a las anteriores. Pasó de estar basado en "Procesos" (las famosas 10 áreas de conocimiento) a estar basado en **12 Principios** y **8 Dominios de Desempeño** (Interesados, Equipo, Enfoque de Desarrollo y Ciclo de Vida, Planificación, Trabajo del Proyecto, Entrega, Medición e Incertidumbre). Se volvió mucho más adaptable, enfocándose en la entrega de valor y abrazando tanto enfoques predictivos (cascada) como adaptativos (ágiles). Incluye además, como publicación independiente dentro del mismo volumen, "The Standard for Project Management", que recoge estos principios con carácter normativo.
*   **PMBOK 8ª Edición:** Publicada oficialmente por el PMI en noviembre de 2025 (edición en PDF; la edición en papel llegó en enero de 2026), representa una síntesis entre la flexibilidad de la 7ª edición y la estructura práctica de las ediciones anteriores a esta. Sus novedades clave son:
    *   **6 Principios básicos** (frente a los 12 de la 7ª edición, ahora consolidados y simplificados): Adoptar una Visión Holística, Centrarse en el Valor, Integrar la Calidad, Liderar con Responsabilidad (*Accountability*), Integrar la Sostenibilidad y Construir Equipos Empoderados.
    *   **7 Dominios de Desempeño** (reducidos desde los 8 de la 7ª edición): Gobernanza, Alcance, Cronograma, Finanzas, Interesados, Recursos y Riesgo.
    *   **5 Áreas de Enfoque (*Focus Areas*)** que reintroducen la estructura práctica que se había perdido en la 7ª edición, con 40 procesos no prescriptivos organizados según los clásicos grupos de procesos: Inicio, Planificación, Ejecución, Monitoreo y Control, y Cierre. La diferencia frente al antiguo PMBOK 6 es que estos procesos son opciones adaptables, no pasos obligatorios.
    *   Incorpora de forma explícita contenido sobre **Inteligencia Artificial**, sostenibilidad, evolución del rol de las PMO (de "guardianas del cumplimiento" a "habilitadoras de valor") y modelos de contratación híbridos/ágiles.
    *   El nuevo examen PMP alineado con esta edición se lanza el 9 de julio de 2026, con un cambio muy significativo: el dominio "Entorno de Negocio" (*Business Environment*) pasa de pesar un 8% a un 26% del examen.

Para el examen de oposición conviene dominar bien ambas versiones recientes (7ª y 8ª), ya que el temario oficial las cita expresamente juntas; la clave para no confundirlas es recordar que la 8ª edición **no vuelve al PMBOK 6** sino que combina principios (ahora 6, no 12) con procesos adaptables agrupados en 5 Áreas de Enfoque (no en las 10 áreas de conocimiento clásicas).

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

Scrum se fundamenta formalmente en la **Scrum Guide** (Schwaber y Sutherland), sobre el **empirismo** y la teoría de control de procesos Lean, apoyándose en tres pilares (**Transparencia, Inspección y Adaptación**) y cinco valores (Compromiso, Foco, Apertura, Respeto y Coraje). Desde la actualización de 2020, ya no se habla de "3 roles" separados sino de un único **Scrum Team** (10 personas o menos) con tres tipos de responsabilidad: Product Owner, Scrum Master y **Developers** (término que sustituye a "Equipo de Desarrollo", ahora descrito como auto-gestionado en lugar de simplemente autoorganizado). Un artefacto adicional importante no mencionado en el original es el **Incremento**, el resultado tangible y utilizable que se produce en cada Sprint y que debe cumplir la **Definición de Terminado (Definition of Done)** acordada por el equipo.

### 3.2. Kanban
Método basado en el flujo continuo ("just in time") [cite: 7].

**Patrón de Reglas Kanban [cite: 7]:**
1.  **Visualizar el flujo:** Uso de un tablero dividido en columnas (ej. Cola, Análisis, Desarrollo, Pruebas) [cite: 7].
2.  **Limitar el WIP (Work in Progress):** Es la regla fundamental. Se limita el número máximo de tareas que pueden estar en cada columna para detectar cuellos de botella y asegurar el flujo [cite: 7].
3.  **Medir y optimizar (Throughput / Lead Time):** Se evalúa la cantidad de trabajo finalizado y el tiempo que tarda una tarea desde que entra hasta que sale del tablero [cite: 7].

Kanban proviene del sistema de producción de Toyota (Lean Manufacturing) y fue adaptado al desarrollo de software por David J. Anderson. A diferencia de Scrum, **no exige roles ni eventos fijos** ni trabaja en iteraciones de duración predeterminada, y puede aplicarse como capa de mejora continua sobre cualquier proceso existente. Sus **4 principios básicos** son: empezar con lo que se hace ahora, acordar cambios incrementales y evolutivos, respetar inicialmente los roles y responsabilidades actuales, y fomentar el liderazgo en todos los niveles. Conviene distinguir bien dos métricas que suelen confundirse en examen: el **Lead Time** (desde que la tarea se solicita hasta que se entrega) y el **Cycle Time** (desde que el equipo empieza a trabajar en ella hasta que se completa).

*(Nota: **Scrumban** es la hibridación de ambos: usa las iteraciones y reuniones de Scrum, pero gestiona el flujo de trabajo con un tablero y límites WIP típicos de Kanban)* [cite: 7].

## 4. ISO 21502

La norma **ISO 21502:2020** (Gestión de proyectos, programas y carteras - Orientación sobre la gestión de proyectos) vino a sustituir a la antigua ISO 21500.

**Conceptos Clave para el Test:**
*   **No es certificable:** Al igual que EFQM, es una guía de orientación, no se emiten certificados de cumplimiento ISO 21502 para organizaciones (a diferencia de la ISO 9001).
*   **Enfoque integral:** Ofrece directrices de alto nivel sobre conceptos y prácticas, centrándose no solo en la ejecución del proyecto, sino en el **entorno de la organización** y en cómo los proyectos contribuyen a la estrategia general, programas y carteras (portfolios).

El apartado 6 de la norma organiza las actividades de gestión del proyecto en una secuencia clara y muy preguntable: **Actividades previas al proyecto → Dirigir un proyecto → Iniciar un proyecto → Controlar un proyecto → Gestión de la entrega → Cerrar o terminar un proyecto → Actividades posteriores al proyecto**. La norma es deliberadamente agnóstica respecto al ciclo de vida: establece que el número y los nombres de las fases de un proyecto dependen del tipo de proyecto, de la gobernanza deseada y del riesgo previsto, y que las fases pueden reflejar un enfoque predictivo, iterativo, incremental, adaptativo o híbrido. Cada fase debe tener un inicio y un final definidos, ir precedida de un **punto de decisión** (llamado habitualmente "puerta" o *gate*) y estar asociada a hitos concretos (decisiones, entregables o resultados clave). Esta flexibilidad de ciclo de vida es lo que distingue a ISO 21502 de PRINCE2 (que sí define procesos y secuencia fijos) y la acerca más al espíritu de PMBOK 7/8.

---

## 5. Patrones de Examen y "Palabras Chivatas"

| Concepto | Palabra Chivata en el Test |
| :--- | :--- |
| **PRINCE2** | "Business Case continuo" [cite: 7], "Entornos controlados" [cite: 7], "Gestión por excepción", "Orientado a productos", "7 principios/temas/procesos". |
| **PMBOK 7ª ed.** | "12 principios", "8 dominios de desempeño", "The Standard for Project Management". |
| **PMBOK 8ª ed.** | "6 principios", "7 dominios de desempeño", "5 áreas de enfoque", "40 procesos no prescriptivos", "IA y sostenibilidad". |
| **Scrum - Product Owner** | "Voz del cliente", "Prioriza el Backlog", "Maximiza el valor de negocio" [cite: 7]. |
| **Scrum - Sprint** | "Iteración de 2-4 semanas", "Requisitos congelados" [cite: 7]. |
| **Kanban** | "Limitar el WIP (trabajo en curso)" [cite: 7], "Tablero visual", "Flujo continuo", "Lead Time vs. Cycle Time". |
| **ISO 21502** | "Guía", "No certificable", "Gestión de proyectos, programas y carteras", "Agnóstica del ciclo de vida", "Puntos de decisión/puertas". |

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

### 5.2. Simulacro de Test adicional

**Pregunta:**
*¿Cuál de las siguientes afirmaciones describe correctamente una diferencia entre el PMBOK 7ª edición y el PMBOK 8ª edición?*
a) La 8ª edición vuelve a las 10 áreas de conocimiento de la 6ª edición, eliminando los principios.
b) La 8ª edición reduce los 12 principios de la 7ª a 6 principios y reintroduce procesos adaptables organizados en 5 Áreas de Enfoque.
c) La 8ª edición elimina por completo los dominios de desempeño.
d) Ambas ediciones son idénticas en estructura y solo cambian de nombre.

**Razonamiento Estructurado:**
1.  (A) es falsa porque la 8ª edición no recupera las 10 áreas de conocimiento clásicas, sino que introduce 5 Áreas de Enfoque con procesos no prescriptivos. (C) es falsa porque mantiene dominios de desempeño, solo que reducidos de 8 a 7. (D) es obviamente falsa dado el cambio sustancial.
2.  La 8ª edición simplifica los 12 principios de la 7ª a 6, reduce los dominios de desempeño de 8 a 7, y añade 5 Áreas de Enfoque con 40 procesos adaptables que reintroducen estructura práctica.
3.  **Respuesta correcta:** B.

**Pregunta:**
*Según la norma ISO 21502:2020, ¿cuál de las siguientes afirmaciones es correcta respecto al ciclo de vida de un proyecto?*
a) La norma exige un número fijo de fases idéntico para todos los proyectos.
b) El número y los nombres de las fases dependen del tipo de proyecto, la gobernanza deseada y el riesgo previsto.
c) ISO 21502 solo admite el enfoque predictivo (cascada).
d) Las fases no pueden solaparse nunca entre sí.

**Razonamiento Estructurado:**
1.  (A) y (C) son falsas porque la norma es deliberadamente agnóstica respecto al enfoque y al número de fases. (D) es falsa porque la norma reconoce explícitamente que las fases pueden superponerse.
2.  La ISO 21502 indica que el número y los nombres de las fases dependen del tipo de proyecto, la gobernanza deseada y el riesgo previsto, admitiendo enfoques predictivos, iterativos, incrementales, adaptativos o híbridos.
3.  **Respuesta correcta:** B.
