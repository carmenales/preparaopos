---
id: "cm-ad-ia-p01-tema-006-gestion-calidad"
title: "Gestión de calidad en los sistemas y servicios TIC"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/tic"
profiles:
  - "p01-analista-aplicaciones"
official_profile: "P01 - Analista de Aplicaciones"
official_topic: "Tema 6. Gestión de calidad en los sistemas y servicios TIC"
source_ids:
tags:
  - "calidad"
  - "efqm"
  - "iso-9001"
  - "pdca"
created_at: "2026-08-08"
last_reviewed: null
ai_generated: true
ai_sources:
  - "gemini"
needs_human_review: true
---

# Tema 6. Gestión de calidad en los sistemas y servicios TIC

## 1. Conceptos Clave de Calidad en TIC

La calidad en el desarrollo y servicio TIC no es que el software sea "bonito", sino que **cumpla exactamente con los requisitos** especificados y que sea **apto para el uso** del cliente. 

**Patrón Lógico - Aseguramiento vs Control:** En los test siempre intentan confundir estos dos términos. Grábate esta diferencia:
*   **Aseguramiento de la Calidad (QA - Quality Assurance):** Orientado al **proceso**. Es *preventivo*. Define cómo se van a hacer las cosas para evitar errores. En Métrica v3 existe una interfaz específica para esto (Interfaz CAL), donde el Grupo de Aseguramiento de la Calidad elabora el plan y verifica que los productos intermedios cumplen las normas [cite: 4].
*   **Control de Calidad (QC - Quality Control):** Orientado al **producto**. Es *reactivo*. Son las pruebas reales que se hacen sobre el software ya construido para detectar fallos antes de entregarlo.

---

## 2. El Modelo EFQM (Excelencia)

El modelo EFQM (European Foundation for Quality Management) no es una norma de obligado cumplimiento, sino un **marco de autoevaluación** para alcanzar la "Excelencia" organizativa.

**Patrón Lógico de EFQM - La regla Causa/Efecto:**
El modelo EFQM clásico se divide estrictamente en dos bloques que suman 9 criterios. Si te preguntan por un criterio, solo tienes que pensar: ¿es la herramienta (causa) o es lo que consigo (efecto)?
1.  **Agentes Facilitadores (Lo que la organización HACE):** Son 5 criterios. Liderazgo, Personas, Estrategia, Alianzas y Recursos, Procesos.
2.  **Resultados (Lo que la organización LOGRA):** Son 4 criterios. Resultados en los Clientes, Resultados en las Personas, Resultados en la Sociedad, Resultados Clave del negocio.

**La lógica RADAR:** EFQM evalúa a las organizaciones usando la matriz RADAR:
*   **R**esultados (Qué queremos lograr).
*   **E**nfoque (Approach - Cómo lo vamos a hacer).
*   **D**espliegue (Deploy - Ponerlo en práctica).
*   **E**valuación y **R**evisión (Assess & Refine - Medir y mejorar).

---

## 3. ISO 9001 (Gestión de la Calidad)

A diferencia de EFQM, la norma ISO 9001 sí es **certificable**. Es el estándar internacional para los Sistemas de Gestión de Calidad (SGC).

**Patrón Lógico - El Ciclo de Deming (PDCA):**
Toda la ISO 9001 se basa en el ciclo de mejora continua o ciclo PDCA. En el test, asocia cada fase con su acción directa:
1.  **Plan (Planificar):** Establecer los objetivos y los procesos necesarios (ej. planificar cómo atender las incidencias de los usuarios).
2.  **Do (Hacer):** Implementar los procesos (ej. poner a los técnicos a atender llamadas según el plan).
3.  **Check (Verificar):** Medir y monitorizar los procesos contra los objetivos (ej. sacar un informe de cuánto tardamos en resolver las incidencias).
4.  **Act (Actuar):** Tomar acciones para mejorar el rendimiento continuamente (ej. si tardamos mucho, comprar una herramienta mejor o dar más formación).

---

## 4. Ejemplo Real (Sin analogías)

Imagina el **Centro de Atención a Usuarios (CAU)** de tu ministerio:
*   **ISO 9001:** El CAU redacta un manual estricto sobre cómo se debe registrar un ticket, en qué tiempos debe resolverse y cómo se mide si se ha cumplido. Si viene un auditor externo y ve que todos los técnicos siguen el manual a rajatabla y que miden sus tiempos (Ciclo PDCA), el CAU **consigue el certificado ISO 9001**.
*   **EFQM:** El director del CAU quiere ir más allá de cumplir un manual; quiere la *excelencia*. Pasa cuestionarios anónimos a los técnicos para ver si están motivados (Agente: Personas), evalúa si los ministerios están contentos con el trato (Resultado en Clientes) e introduce mejoras basadas en la matriz RADAR. No recibe un "certificado" por cumplir mínimos, sino un **Sello de Excelencia (ej. +400 puntos EFQM)**.

---

## 5. Patrones de Examen y "Palabras Chivatas"

| Concepto | Palabra Chivata en el Test |
| :--- | :--- |
| **Aseguramiento de Calidad (QA)** | "Prevención", "Procesos", "Plan de calidad", "Métrica v3 interfaz CAL". |
| **Control de Calidad (QC)** | "Detección", "Producto", "Pruebas", "Inspección". |
| **Modelo EFQM** | "Autoevaluación", "Excelencia", "Agentes facilitadores y Resultados", "Matriz RADAR". |
| **ISO 9001** | "Certificable", "Sistema de Gestión de Calidad (SGC)", "Mejora continua". |
| **Ciclo PDCA (Deming)** | "Planificar, Hacer, Verificar, Actuar", "Mejora iterativa". |

### 5.1. Simulacro de Test: Desmontando trampas

**Pregunta:**
*Dentro de los criterios del modelo de excelencia EFQM, ¿cuál de los siguientes elementos es considerado un "Agente Facilitador" y no un "Resultado"?*
a) Resultados en la sociedad.
b) El Liderazgo.
c) Satisfacción del cliente.
d) Resultados clave del negocio.

**Razonamiento Estructurado:**
1.  **Busca el patrón:** Te piden distinguir entre la "Causa" (lo que hacemos = Agente facilitador) y el "Efecto" (lo que conseguimos = Resultado).
2.  **Aplica tu patrón lógico de descarte:**
    *   (A) "Resultados en la sociedad": Contiene la palabra "resultado". Es el efecto que nuestra organización tiene en el entorno. Falsa.
    *   (C) "Satisfacción del cliente": Es la consecuencia (efecto) de dar un buen servicio. Es un resultado. Falsa.
    *   (D) "Resultados clave": Contiene la palabra "resultado". Falsa.
    *   (B) "El Liderazgo": ¿Es algo que *hacemos* internamente para mover la organización? Sí. Es la forma en que los directivos guían al equipo. Es una causa (Agente Facilitador). 
3.  **Respuesta correcta:** B.
