---
id: "cm-ad-tic-p04-tema-003-evaluacion-seleccion"
title: "Evaluación y selección de proyectos"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/tic"
profiles:
  - "p04-ingeniero-desarrollo"
official_profile: "P04 - Ingeniero de Desarrollo"
official_topic: "Tema 3. Evaluación y selección de proyectos"
source_ids:
  - "A2_Bloque_IV.pdf"
tags:
  - "seleccion-proyectos"
  - "van"
  - "tir"
  - "payback"
  - "roi"
  - "pmo"
  - "portfolio"
created_at: "2026-08-09"
last_reviewed: "2026-08-09"
ai_generated: true
ai_sources:
  - "gemini"
  - "perplexity"
needs_human_review: true
---

# Tema 3. Evaluación y selección de proyectos

La selección de proyectos es un proceso estratégico. Las organizaciones (y especialmente la Administración Pública) tienen recursos limitados y no pueden ejecutar todas las ideas que surgen. Este tema aborda cómo la Alta Dirección o la PMO de Portfolio deciden qué proyectos se aprueban (Go) y cuáles se descartan (No-Go).

## 1. Criterios de Evaluación de un Proyecto

Para comparar manzanas con manzanas, los proyectos se evalúan bajo dos grandes prismas: el financiero (cuantitativo puro, basado en el dinero) y el no financiero (alineación estratégica y cumplimiento).

### 1.1. Criterios Financieros (Las fórmulas del test)

Estas métricas son matemáticas y buscan maximizar el retorno económico. En el examen, no te pedirán calcular raíces cuadradas complejas, pero **sí debes saber la teoría de cada fórmula y qué valor elegir al comparar dos proyectos**.

*   **Valor Actual Neto (VAN / NPV):** Es el valor presente de los flujos de caja futuros (ingresos menos gastos), descontando la tasa de interés o inflación.
    *   *Regla de oro:* Si $VAN > 0$, el proyecto es rentable. Si $VAN < 0$, perderás dinero.
    *   *Comparativa:* Entre dos proyectos, **elige siempre el que tenga el VAN más alto**.
*   **Tasa Interna de Retorno (TIR / IRR):** Es la tasa de interés que hace que el VAN sea exactamente cero. Mide la rentabilidad intrínseca del proyecto expresada en porcentaje.
    *   *Regla de oro:* Si la TIR es mayor que el coste de capital de la organización, el proyecto es viable.
    *   *Comparativa:* Entre dos proyectos, **elige el que tenga la TIR más alta**.
*   **Plazo de Recuperación (Payback Period):** Mide el tiempo exacto que se tarda en recuperar la inversión inicial. 
    *   *Regla de oro:* Mide riesgo y liquidez, no rentabilidad total (ignora lo que pasa después de recuperar la inversión).
    *   *Comparativa:* Entre dos proyectos, **elige el que tenga el Payback más corto**.
*   **Retorno de la Inversión (ROI):** Es un porcentaje que indica el beneficio obtenido en relación con la inversión. $ROI = (Beneficio Neto / Coste de Inversión) \times 100$.
*   **Coste de Oportunidad:** Es el valor del proyecto que *descartas* al elegir otro. Si el proyecto A tiene un VAN de 100.000€ y el B tiene un VAN de 80.000€, si eliges A, el coste de oportunidad es 80.000€.
*   **Costos Hundidos (Sunk Costs):** Son costes en los que ya se ha incurrido y no se pueden recuperar. *Regla de examen:* **Los costes hundidos NUNCA deben considerarse** al decidir si se continúa o se cancela un proyecto.

### 1.2. Criterios No Financieros

Especialmente críticos en la Administración Pública, donde el objetivo principal no siempre es ganar dinero, sino prestar un servicio al ciudadano.

*   **Alineación Estratégica:** Grado en el que el proyecto apoya los objetivos de la organización (ej. alineación con el Plan de Digitalización de las AAPP).
*   **Cumplimiento Normativo / Legal:** Proyectos obligatorios por ley (ej. adaptación urgente al Esquema Nacional de Seguridad o GDPR). Estos proyectos suelen tener prioridad absoluta independientemente de su VAN.
*   **Impacto Social y Sostenibilidad (ESG):** Beneficios intangibles como la mejora de la imagen pública, la reducción de la huella de carbono o la mejora de la accesibilidad ciudadana.
*   **Riesgo y Complejidad Técnica:** Nivel de incertidumbre tecnológica o resistencia al cambio organizacional.



## 2. Métodos de Selección de Proyectos

Una vez tenemos los criterios, necesitamos métodos estructurados para aplicar esos criterios y tomar la decisión.

### 2.1. Métodos Cuantitativos (Modelos Matemáticos)

Se basan en algoritmos y números.

*   **Modelos de Puntuación Ponderada (Scoring Models):** Se crea una matriz con varios criterios (VAN, riesgo, alineación). A cada criterio se le asigna un peso (ej. VAN 40%, Riesgo 20%, Estrategia 40%). Cada proyecto se puntúa y se elige el de mayor puntuación total ponderada.
*   **Modelos de Optimización Matemática:** Utilizados para carteras complejas. Se basan en programación lineal, programación no lineal, programación entera o algoritmos multiobjetivo para maximizar el valor de un portfolio de proyectos sujetos a restricciones estrictas (ej. "no superar un presupuesto total de 5M€ y utilizar un máximo de 50 programadores").

### 2.2. Métodos Cualitativos (Análisis Experto)

Se basan en el juicio humano y el consenso.

*   **Revisión por Pares (Peer Review) o Comités:** Un grupo de expertos o la PMO de Portfolio evalúa las propuestas y debate su viabilidad.
*   **Método Delphi:** Técnica estructurada para obtener el consenso de un panel de expertos de forma anónima. Se realizan varias rondas de cuestionarios para evitar que la opinión de un "experto dominante" sesgue al resto del grupo.
*   **Q-Sort:** Método de clasificación comparativa. Los expertos clasifican los proyectos propuestos en grupos según su prioridad (Alta, Media, Baja) distribuyéndolos de forma forzada bajo una curva normal.
*   **Asesinato de Proyectos (Murder Board):** Un comité agresivo ataca la propuesta de proyecto buscando todos sus fallos para asegurar que solo sobrevivan las propuestas verdaderamente robustas.



## 3. Factores Clave en la Toma de Decisiones

La decisión de seleccionar un proyecto no se basa en una única fórmula matemática. Los directivos y la PMO combinan los métodos anteriores sopesando varios factores clave:

1.  **Relación Riesgo vs. Recompensa:** Un proyecto con un VAN enorme puede ser rechazado si tiene un riesgo de fracaso tecnológico inasumible.
2.  **Capacidad Operativa y Disponibilidad de Recursos:** Un proyecto puede ser excelente sobre el papel, pero si la organización no tiene el personal cualificado (o no puede contratarlo a tiempo), se descartará o pospondrá.
3.  **Dependencias e Interrelaciones:** Un proyecto puede tener un VAN negativo, pero ser un prerrequisito técnico obligatorio (habilitador) para otro proyecto que tiene un VAN extremadamente positivo.
4.  **Restricciones Presupuestarias (Entorno Público):** En la AGE, los presupuestos son anualizados. Un proyecto debe encajar en las partidas presupuestarias aprobadas en los PGE (Presupuestos Generales del Estado) o contar con fondos específicos europeos (ej. PRTR).



## 4. Herramientas y Técnicas de Selección

Para ejecutar los métodos descritos, se emplean herramientas visuales y analíticas.

*   **El Caso de Negocio (Business Case):** Es el documento fundamental (central en PRINCE2) que consolida toda la información: los motivos, las opciones, los costes, los beneficios esperados, el análisis de inversión (VAN, TIR) y los riesgos. Es la herramienta de venta del proyecto ante el Comité.
*   **Árboles de Decisión y Valor Monetario Esperado (VME):** Herramienta gráfica que representa diferentes alternativas de decisión y sus posibles resultados futuros, asignando probabilidades. El VME se calcula multiplicando la probabilidad de un evento por su impacto económico.
    *   *Fórmula VME:* $Probabilidad (\%) \times Impacto Económico (\$)$. 
    *   *Suma de Nodos:* Un nodo de decisión se evalúa sumando el VME de todas sus ramas.
*   **Análisis DAFO / SWOT:** Técnica de análisis de la situación que evalúa las Debilidades, Amenazas, Fortalezas y Oportunidades del proyecto en relación con el entorno competitivo o institucional.
*   **Matrices de Decisión (Matriz Causa-Efecto):** Tablas que cruzan las alternativas de proyecto con los criterios de evaluación, muy utilizadas en los modelos de puntuación ponderada.



## 5. ResumenW

| Concepto | Regla para el Test / Palabra Chivata |
| :--- | :--- |
| **VAN (Valor Actual Neto)** | "Flujos de caja descontados". A mayor VAN, mejor. Si es $>0$, se acepta. |
| **TIR (Tasa Interna de Retorno)** | "Rentabilidad en %". Hace que el $VAN = 0$. A mayor TIR, mejor. |
| **Payback (Plazo de recuperación)** | "Tiempo en recuperar la inversión". Mide **liquidez y riesgo**, NO rentabilidad. Se elige el más corto. |
| **Coste de Oportunidad** | "El valor del proyecto que se rechaza". No se suma ni se resta, es simplemente el valor de la alternativa descartada. |
| **Costos Hundidos** | "Costos ya gastados irrecuperables". **NUNCA** se tienen en cuenta para decisiones futuras. |
| **Scoring Models** | "Puntuación ponderada", "Criterios con pesos". |
| **Programación Lineal/Matemática** | "Métodos de optimización", "Maximizar con recursos limitados". |
| **Método Delphi** | "Panel de expertos", "Anónimo", "Rondas sucesivas", "Consenso". |
| **VME (Valor Monetario Esperado)** | "Árboles de decisión", "Probabilidad por Impacto". |



## 6. Simulacro de Test

**Pregunta 1:**
*La PMO de un Ministerio está evaluando dos proyectos mutuamente excluyentes para modernizar el archivo digital. El Proyecto A tiene un VAN de 150.000€ y una duración de 3 años. El Proyecto B tiene un VAN de 85.000€ y una duración de 1 año. Si no existen otras restricciones, ¿qué decisión debe tomar el comité basándose estrictamente en los criterios financieros?*
a) Seleccionar el Proyecto B porque su plazo de recuperación es mucho menor.
b) Seleccionar el Proyecto A porque su VAN es mayor, independientemente de la duración.
c) Rechazar ambos porque no se detalla la TIR de ninguno.
d) Sumar ambos VAN y ejecutar ambos proyectos para maximizar beneficios.

**Razonamiento:**
*   La regla de oro de la selección financiera dictamina que, ante proyectos mutuamente excluyentes, el criterio rey absoluto de rentabilidad es el Valor Actual Neto (VAN). Siempre se escoge el proyecto con el VAN superior. 
*   El Proyecto A (150.000€) aporta más valor a la organización que el B (85.000€).
**Respuesta correcta: B.**

**Pregunta 2:**
*Durante una reunión de selección de cartera, la directiva no logra ponerse de acuerdo sobre qué proyectos tecnológicos priorizar debido a la fuerte influencia y presión del Director Financiero sobre el resto de vocales. Para evitar este sesgo, deciden utilizar una técnica donde expertos evalúan los proyectos de forma estructurada, iterativa y, sobre todo, anónima. ¿Qué técnica han decidido utilizar?*
a) Revisión por pares (Peer Review).
b) Q-Sort.
c) Método Delphi.
d) Modelos de puntuación ponderada.

**Razonamiento:**
*   Las palabras chivata del enunciado son "iterativa" y "anónima" para evitar el "sesgo de la influencia".
*   Esta es la definición de manual del Método Delphi.
**Respuesta correcta: C.**

**Pregunta 3:**
*Se está evaluando la viabilidad de continuar o cancelar un proyecto de desarrollo de software que lleva 6 meses de retraso. El departamento de contabilidad informa que ya se han gastado 250.000€ en licencias que no se pueden devolver. En la terminología de selección financiera de proyectos, ¿cómo se denomina este importe y cómo debe afectar a la decisión?*
a) Es el Coste de Oportunidad, y debe restarse de los beneficios futuros.
b) Es un Costo Hundido (Sunk Cost), y no debe tenerse en cuenta al decidir si se continúa o cancela el proyecto.
c) Es el Valor Monetario Esperado (VME), y obliga a la finalización obligatoria del proyecto.
d) Es un Costo Hundido (Sunk Cost), y debe sumarse al cálculo del nuevo VAN para justificar la inversión.

**Razonamiento:**
*   El dinero ya gastado que es irrecuperable es, por definición, un "Costo Hundido" (Sunk Cost).
*   La regla fundamental en la evaluación de proyectos es que los costos hundidos nunca se deben incluir en el análisis de decisiones futuras (no "llorar sobre la leche derramada"). La decisión de seguir o parar solo debe basarse en el coste necesario *desde hoy hasta el final* frente al beneficio esperado.
**Respuesta correcta: B.**