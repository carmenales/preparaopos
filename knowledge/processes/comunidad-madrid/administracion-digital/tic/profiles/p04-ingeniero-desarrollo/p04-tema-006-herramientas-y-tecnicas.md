---
id: "cm-ad-tic-p04-tema-006-herramientas-tecnicas"
title: "Herramientas y Técnicas de Gestión"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/tic"
profiles:
  - "p04-ingeniero-desarrollo"
official_profile: "P04 - Ingeniero de Desarrollo"
official_topic: "Tema 6. Herramientas y Técnicas"
source_ids:
  - "A2_Bloque_III.pdf"
tags:
  - "wbs"
  - "pert"
  - "gantt"
  - "riesgos"
  - "evm"
  - "metrica-v3"
created_at: "2026-08-08"
last_reviewed: null
ai_generated: true
ai_sources:
  - "A2_Bloque_III.pdf"
needs_human_review: true
---

# Tema 6. Herramientas y Técnicas

Este tema es el núcleo operativo de Métrica v3 (Interfaz de Gestión de Proyectos - GP). Como ingeniero, esto es "código de gestión": reglas claras para construir la estructura del proyecto.

## 1. Planificación: WBS, Cronogramas y Estimación

La planificación transforma la idea en tareas ejecutables.

*   **WBS (Work Breakdown Structure):** Es el **árbol jerárquico** que descompone el proyecto en entregables manejables (fases -> actividades -> tareas). Es la base para cualquier estimación.
*   **Estimación:**
    *   **Puntos Función (Albrecht / Mark II):** Técnica empírica e independiente del lenguaje. Mide la complejidad de la funcionalidad.
    *   **Staffing Size:** Específico para **Orientación a Objetos**. Se basa en estimar el número de clases clave y secundarias para determinar el esfuerzo en días/persona.
*   **Cronogramas:**
    *   **PERT:** Grafo de redes (nodos/flechas). Permite calcular la **Ruta Crítica** (la secuencia de tareas sin holgura).
    *   **Gantt:** El diagrama de barras clásico para visualizar plazos y superposición de tareas en el tiempo.

## 2. Gestión de Riesgos y Cambios

En Métrica v3, la gestión de incidencias y cambios se hace en la fase **GPS (Seguimiento y Control)**.

*   **Riesgos:** Deben identificarse, analizarse y cuantificarse (probabilidad e impacto).
*   **Control de Cambios:** Cuando un usuario pide cambiar un requisito, el Jefe de Proyecto realiza un **Análisis de Impacto** (¿cuánto tiempo/dinero extra supone?). El cambio se registra formalmente, pero **solo lo aprueba el Comité de Seguimiento**.

## 3. Métricas: Valor Ganado (EVM)

Es la técnica estrella para saber si el proyecto va bien sin esperar al final. Se basa en tres valores clave:
*   **PV (Valor Planificado):** Lo que *debíamos* haber hecho a día de hoy (según presupuesto).
*   **EV (Valor Ganado):** El valor real del trabajo *finalizado* a día de hoy.
*   **AC (Coste Real):** Lo que hemos gastado *realmente* hasta hoy.

**Patrones para el test:**
*   Si **EV > PV**, vas por delante del cronograma (SPI > 1).
*   Si **EV > AC**, estás ahorrando dinero (CPI > 1).

## 4. Patrones de Examen y "Palabras Chivatas"

| Concepto | Palabra Chivata |
| :--- | :--- |
| **WBS** | "Descomposición jerárquica", "Árbol", "Entregables". |
| **PERT** | "Probabilístico", "Ruta crítica", "Holgura", "Grafo". |
| **Gantt** | "Diagrama de barras", "Visualización temporal". |
| **EVM (Valor Ganado)** | "Línea base", "Desviación de coste/plazo", "CPI", "SPI". |
| **Comité de Seguimiento** | "Aprueba los cambios de requisitos" (el Jefe de Proyecto solo analiza). |

### 4.1. Simulacro de Test: Desmontando trampas

**Pregunta:**
*En el contexto de la Gestión del Valor Ganado (EVM), si el índice de rendimiento de costes (CPI) es 0,8, ¿qué significa?*
a) El proyecto está costando un 20% menos de lo planificado.
b) El proyecto está costando un 80% más de lo planificado.
c) Por cada euro invertido, solo estamos obteniendo 0,80 euros de valor.
d) El proyecto va un 20% retrasado.

**Razonamiento Estructurado:**
1.  **Busca el patrón:** CPI = EV / AC. Si CPI < 1, significa que gastamos más de lo que ganamos (ineficiencia).
2.  **Desmontando:**
    *   (A) Imposible, el CPI sería > 1.
    *   (B) Si el CPI fuera 0,8, es una ineficiencia, pero no implica un 80% extra de coste, sino una relación 1:0,8.
    *   (D) El SPI mide el tiempo, el CPI mide el coste. Falsa.
3.  **Respuesta correcta: C.** La definición técnica de CPI es la eficiencia de costes. Un valor de 0,8 indica que por cada unidad monetaria real (AC) aplicada, solo se genera 0,8 unidades de valor ganado (EV).