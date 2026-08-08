---
id: "cm-ad-ia-p01-tema-003-analisis-funcional-diseño"
title: "Análisis funcional/diseño"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/tic"
profiles:
  - "p01-analista-aplicaciones"
official_profile: "P01 - Analista de Aplicaciones"
official_topic: "Tema 3. Análisis funcional/diseño"
source_ids:
tags:
  - "analisis-funcional"
  - "casos-de-uso"
  - "historias-de-usuario"
  - "scrum"
  - "kanban"
  - "dsdm"
created_at: "2026-08-08"
last_reviewed: null
ai_generated: true
ai_sources:
  - "gemini"
needs_human_review: true
---

# Tema 3. Análisis funcional/diseño

## 1. Análisis Funcional y de Requisitos

El análisis funcional es la fase donde definimos **qué** debe hacer el sistema, sin entrar todavía en **cómo** lo va a hacer técnicamente a nivel de código. La base de esto es la Ingeniería de Requerimientos [cite: 2].

### 1.1. Ingeniería de Requerimientos
Su tarea principal es generar especificaciones correctas, claras y sin ambigüedades sobre el comportamiento del sistema [cite: 2].

**Técnicas principales de obtención de requisitos [cite: 2]:**
*   **Entrevistas:** Encuentros "cara a cara" con los usuarios. Requieren preparación previa, envío de un guion y elaboración de un acta final [cite: 2].
*   **Reuniones JAD (Joint Application Design):** Sesiones de trabajo largas y preparadas para conseguir consenso rápido. Reúnen a usuarios, desarrolladores y un moderador. El objetivo es reducir el tiempo de desarrollo manteniendo la calidad [cite: 2].
*   **Reuniones JRP (Joint Requirement Planning):** Similares a las JAD, pero enfocadas a la Alta Dirección para tomar decisiones estratégicas [cite: 2].

### 1.2. Casos de Uso e Historias de Usuario

Son las dos herramientas principales para documentar requisitos, dependiendo de si usamos metodologías tradicionales o ágiles.

*   **Historias de Usuario (Metodologías Ágiles - XP/Scrum):**
    *   Son tarjetas de papel donde el cliente describe brevemente una característica que el sistema debe tener [cite: 2].
    *   Se descomponen luego en tareas de programación [cite: 2].
    *   **Estructura patrón:** "Como [Rol], quiero [Funcionalidad], para [Beneficio/Objetivo]". Ejemplo real: "Como ciudadano, quiero un botón de descarga en PDF para guardar mi certificado de empadronamiento".

*   **Casos de Uso (Metodologías Tradicionales/UML - Métrica v3):**
    *   Definen la interacción exacta entre un "Actor" (un usuario u otro sistema) y el sistema.
    *   Especifican el comportamiento del sistema [cite: 2]. 
    *   Tienen un flujo principal (lo que pasa si todo va bien) y flujos alternativos (excepciones).

---

## 2. Metodologías Ágiles de Desarrollo

Las metodologías ágiles valoran la adaptación al cambio, las entregas tempranas y la interacción de los individuos por encima de los procesos rígidos y la documentación exhaustiva [cite: 2].

### 2.1. Scrum
Es un marco de trabajo iterativo e incremental para proyectos en entornos complejos [cite: 2].

**Patrón Lógico - Los 3 Roles [cite: 2]:**
1.  **Product Owner (El cliente):** Escribe las historias de usuario y prioriza el trabajo (Product Backlog) basándose en el valor de negocio.
2.  **Scrum Master (El facilitador):** Mantiene el proceso, elimina obstáculos (impedimentos) y protege al equipo de interrupciones externas. No es un jefe, es un facilitador.
3.  **Team (El equipo de desarrollo):** Equipo autoorganizado (de 4 a 9 personas) que construye el software.

**Patrón Lógico - Los Artefactos y Eventos [cite: 2]:**
*   **Sprint:** Iteración de 1 a 4 semanas. Durante el Sprint, los requisitos están congelados [cite: 2].
*   **Product Backlog:** Lista completa y priorizada de todo lo que el sistema necesita [cite: 2].
*   **Sprint Backlog:** Subconjunto del Product Backlog que el equipo se compromete a hacer en el Sprint actual [cite: 2].
*   **Daily Scrum:** Reunión diaria de 15 minutos, de pie, para sincronizar el trabajo [cite: 2].
*   **Sprint Review:** Reunión al final del Sprint para mostrar el software funcionando a los interesados (Stakeholders) [cite: 2].
*   **Sprint Retrospective:** Reunión interna del equipo para analizar qué ha ido bien y qué mejorar en sus procesos [cite: 2].

### 2.2. Kanban
Método para gestionar el flujo de trabajo con énfasis en la entrega "justo a tiempo" [cite: 2].

**Patrón Lógico y Reglas Clave [cite: 2]:**
1.  **Mostrar el proceso:** Uso de un tablero visual con columnas (Ej: Cola, Análisis, Desarrollo, Pruebas) [cite: 2].
2.  **Limitar el Trabajo en Curso (WIP - Work In Progress):** Regla fundamental. Se fija un límite máximo de tareas por columna para evitar cuellos de botella [cite: 2].
3.  **Optimizar el flujo (Cycle Time / Lead Time):** Se mide el tiempo desde que una tarea entra al tablero hasta que sale [cite: 2].

### 2.3. DSDM (Dynamic Systems Development Method)
Enfoque iterativo e incremental basado en el desarrollo rápido de aplicaciones (RAD) [cite: 2]. 

**Patrón Lógico de DSDM [cite: 2]:**
*   **Fijo:** El tiempo (plazos) y el presupuesto están fijados estrictamente desde el principio [cite: 2].
*   **Variable:** Los requisitos son variables y se negocian para asegurar que se cumple el plazo [cite: 2].

---

## 3. Pruebas Funcionales y Metodologías Dirigidas por Pruebas

### 3.1. TDD (Test Driven Development - Desarrollo Guiado por Pruebas)
Metodología donde **primero se escribe la prueba** antes de escribir el código fuente [cite: 2].
*   **Ciclo patrón [cite: 2]:** 
    1. Escribir una prueba que falla (porque el código no existe).
    2. Escribir el código más simple posible (KISS) para que la prueba pase.
    3. Refactorizar (limpiar y optimizar el código eliminando duplicidades).

### 3.2. BDD (Behavior Driven Development - Desarrollo Orientado al Comportamiento)
Evolución del TDD que fomenta la colaboración entre desarrolladores, probadores y clientes [cite: 2]. Se usan lenguajes naturales estructurados (como Gherkin: `Dado que... Cuando... Entonces...`) para definir el comportamiento del sistema de forma que el cliente lo entienda fácilmente [cite: 2].

---

## 4. Enfoque CMMI (Capability Maturity Model Integration)

CMMI es un modelo para evaluar la madurez de los procesos de desarrollo de software de una organización. Identifica 5 niveles de madurez:
1.  **Inicial:** Procesos impredecibles, reactivos y caóticos. Depende del heroísmo individual.
2.  **Gestionado (Managed):** Proyectos planificados, medidos y controlados a nivel básico.
3.  **Definido:** Procesos estandarizados y documentados a nivel de toda la organización.
4.  **Gestionado Cuantitativamente:** Se usan métricas estadísticas para controlar el rendimiento.
5.  **En Optimización:** Mejora continua de los procesos.

---

## 5. Patrones de Examen y "Palabras Chivatas"

| Concepto | Palabra Chivata en el Test |
| :--- | :--- |
| **Scrum** | "Marco de trabajo", "Iterativo e incremental", "Autoorganizado", "Sprints". |
| **Product Owner** | "Voz del cliente", "Prioriza el Backlog", "Maximiza el valor". |
| **Scrum Master** | "Elimina impedimentos/obstáculos", "Facilitador". |
| **Kanban** | "Límites WIP", "Tablero visual", "Flujo continuo", "Just in time". |
| **DSDM** | "Presupuestos y plazos estrictos/fijos", "Extensión de RAD". |
| **JAD (Joint Application Design)** | "Reuniones largas estructuradas", "Usuarios y desarrolladores", "Prototipos". |
| **TDD** | "Prueba antes que el código", "Refactorización". |

### 5.1. Simulacro de Test: Desmontando trampas

**Pregunta:**
*En el marco de trabajo Scrum, ¿quién es el único responsable de decidir qué elementos del Product Backlog tienen mayor prioridad para el negocio y, por tanto, deben desarrollarse primero?*
a) El Scrum Master, ya que gestiona el proceso.
b) El Director del Proyecto.
c) El Product Owner.
d) El Equipo de Desarrollo de forma consensuada.

**Razonamiento Estructurado:**
1.  **Busca la palabra chivata:** El enunciado pregunta por el "único responsable de decidir qué elementos tienen mayor prioridad para el negocio" en Scrum.
2.  **Aplica el patrón:** 
    *   El equipo de desarrollo (D) construye. 
    *   El Scrum Master (A) facilita y quita estorbos, no decide prioridades de negocio [cite: 2].
    *   El Director de Proyecto (B) es un rol de metodologías clásicas (como Métrica v3), pero en Scrum puro **no existe** la figura del Director de Proyecto como tal que dicte prioridades de negocio.
    *   El **Product Owner** (C) es literalmente "la voz del cliente" y el dueño del producto. Su única función clave es ordenar el Backlog [cite: 2].
3.  **Respuesta correcta:** C.
