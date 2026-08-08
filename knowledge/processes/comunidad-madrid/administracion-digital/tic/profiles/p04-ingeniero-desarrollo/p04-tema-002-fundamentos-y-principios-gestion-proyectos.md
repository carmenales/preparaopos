---
id: "cm-ad-tic-p04-tema-002-fundamentos-gestion-proyectos"
title: "Fundamentos y principios de la Gestión de Proyectos"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/tic"
profiles:
  - "p04-ingeniero-desarrollo"
official_profile: "P04 - Ingeniero de Desarrollo"
official_topic: "Tema 2. Fundamentos y principios de la Gestión de Proyectos"
source_ids:
tags:
  - "gestion-proyectos"
  - "pmbok"
  - "prince2"
  - "pmo"
  - "metrica-v3"
created_at: "2026-08-08"
last_reviewed: null
ai_generated: true
ai_sources:
  - "gemini"
needs_human_review: true
---

# Tema 2. Fundamentos y principios de la Gestión de Proyectos

## 1. Conceptos Básicos: Proyecto vs. Operación

Como ingeniero de desarrollo, estás acostumbrado a picar código y apagar fuegos. Para el examen, el tribunal quiere que sepas distinguir exactamente cuándo estás haciendo un "Proyecto" y cuándo estás haciendo una "Operación". Es pura lógica booleana:

**Patrón Lógico - La diferencia fundamental:**
*   **Proyecto:** Tiene un **inicio y un fin definido** (es temporal) y crea un producto, servicio o resultado **único**.
*   **Operación:** Es trabajo **continuo y repetitivo**. No tiene una fecha de fin predefinida; sirve para mantener el negocio funcionando.

**Concepto de PMO (Project Management Office):**
La Oficina de Dirección de Proyectos es el departamento que estandariza los procesos de gobierno relacionados con los proyectos. Su función es centralizar recursos, metodologías, herramientas y técnicas para que todos los jefes de proyecto trabajen igual.

---

## 2. Estándares y Marcos de Referencia

En las preguntas tipo test te van a pedir que identifiques a qué metodología o estándar pertenece cada concepto. Vamos a ir a las palabras clave directas [cite: 5]:

*   **PMBOK (Project Management Institute - PMI):** No es una metodología paso a paso, sino un estándar ANSI y una guía de **buenas prácticas** [cite: 5]. Se basa en áreas de conocimiento (alcance, tiempo, costes, etc.). *Nota: Su versión ágil se llama PMI-ACP [cite: 5].*
*   **PRINCE2:** Es una **metodología** estructurada. Su palabra chivata es que busca convertir proyectos en **"entornos controlados"** [cite: 5]. Se justifica obligatoriamente por un **"Business Case" (Estudio de Viabilidad)** que debe revisarse continuamente para asegurar que el proyecto sigue dando beneficios [cite: 5].

---

## 3. Ciclo de Vida del Proyecto (Enfoque Métrica v3)

Aunque el PMBOK tiene sus propias fases, en las oposiciones TIC del Estado y de la Comunidad de Madrid, el ciclo de vida de la gestión del proyecto se suele preguntar basándose en la interfaz de **Gestión de Proyectos (GP) de Métrica v3** [cite: 5]. 

**Patrón Lógico - Las 3 Fases de Métrica v3 [cite: 5]:**
1.  **GPI (Actividades de Inicio del Proyecto):** Se hace justo al terminar el Estudio de Viabilidad. Aquí se realizan dos cosas clave: la **estimación de esfuerzo** y la **planificación detallada** (hitos, calendario, recursos) [cite: 5].
2.  **GPS (Actividades de Seguimiento y Control):** Es la fase más larga. Va desde la asignación de tareas hasta su aceptación interna [cite: 5]. Aquí se hace la **Gestión de Incidencias** (retrasos, fallos de infraestructura) y el control de **Peticiones de Cambio de Requisitos** [cite: 5].
3.  **GPF (Actividades de Finalización del Proyecto):** Se hace el **cierre del proyecto**, resumiendo datos (funcionalidad, tecnología, recursos) para que sirvan de histórico, y se archiva la documentación [cite: 5].

**El Rol del Jefe de Proyecto [cite: 5]:**
Es la figura principal. Selecciona el ciclo de vida, estima el esfuerzo, planifica, hace el seguimiento, resuelve incidencias y archiva la documentación [cite: 5]. Si hay un cambio en los requisitos, él analiza el impacto, pero quien aprueba ese cambio es el **Comité de Seguimiento** [cite: 5].

---

## 4. Ejemplo Real (Sin analogías)

Imagina que en tu departamento TIC se aprueba la creación de un nuevo "Portal del Empleado Público" para gestionar nóminas y vacaciones.

*   **El Proyecto:** Todo el trabajo desde que se aprueba la idea hasta que el portal se instala en los servidores de producción y los usuarios empiezan a usarlo. Tiene una fecha de entrega (ej. 1 de diciembre).
*   **La Operación:** A partir del 2 de diciembre, el trabajo diario de los técnicos resolviendo tickets de funcionarios que no recuerdan su contraseña o reiniciando el servidor si se queda sin memoria. 
*   **La PMO:** Es el departamento que te obliga a usar una plantilla específica de Excel para reportar los costes de este desarrollo, porque es la misma que usan para el resto de proyectos del ministerio.
*   **Fase GPS (Seguimiento Métrica v3):** Durante el desarrollo, a un programador se le estropea el ordenador y pierde dos días de trabajo. El Jefe de Proyecto registra esto como una **incidencia**, analiza el impacto y actualiza la planificación [cite: 5].

---

## 5. Patrones de Examen y "Palabras Chivatas"

| Concepto | Palabra Chivata en el Test |
| :--- | :--- |
| **Proyecto** | "Temporal", "Inicio y fin", "Producto o servicio único". |
| **Operación** | "Continuo", "Repetitivo", "Mantenimiento del negocio". |
| **PMBOK (PMI)** | "Estándar ANSI", "Buenas prácticas", "Áreas de conocimiento" [cite: 5]. |
| **PRINCE2** | "Entornos controlados", "Business Case", "Justificación de beneficios" [cite: 5]. |
| **PMO (Oficina de Proyectos)** | "Estandarizar procesos", "Compartir recursos y metodologías". |
| **GPS (Seguimiento - Métrica v3)** | "Gestión de incidencias", "Cambio de requisitos", "Actualizar planificación" [cite: 5]. |

### 5.1. Simulacro de Test: Desmontando trampas

**Pregunta:**
*Según la metodología PRINCE2, ¿cuál es el elemento fundamental que justifica la existencia del proyecto en todo momento y que debe ser revisado continuamente para asegurar la consecución de los beneficios esperados?*
a) La Oficina de Dirección de Proyectos (PMO).
b) El acta de constitución del proyecto.
c) El Business Case (o estudio de viabilidad).
d) El registro de incidencias y cambios de Métrica v3.

**Razonamiento Estructurado:**
1.  **Busca la palabra chivata:** El enunciado pregunta por "PRINCE2" y la "justificación del proyecto" mediante la "consecución de los beneficios esperados".
2.  **Aplica tu patrón lógico de descarte:**
    *   (A) La PMO es una oficina estructural de la organización, no un documento o elemento que justifique un proyecto concreto. Falsa.
    *   (B) El acta de constitución es un concepto puramente del PMBOK para iniciar un proyecto, pero el enunciado habla específicamente de PRINCE2 y de beneficios continuos. Falsa.
    *   (D) El registro de incidencias es de la fase de seguimiento (GPS) de Métrica v3 [cite: 5], no tiene nada que ver con la justificación financiera inicial en PRINCE2. Falsa.
    *   (C) **Business Case**: Nuestro patrón nos dice que PRINCE2 se basa explícitamente en el *Business Case* para mantener el entorno controlado y justificar los beneficios en todo momento [cite: 5]. 
3.  **Respuesta correcta:** C.
