---
id: "cm-ad-tic-p01-tema-006-gestion-calidad"
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
  - "iso-9000"
  - "principios-calidad"
created_at: "2026-08-08"
last_reviewed: "2026-08-08"
ai_generated: true
ai_sources:
  - "gemini"
  - "perplexity"
needs_human_review: true
---

# Tema 6. Gestión de calidad en los sistemas y servicios TIC

## 1. Conceptos Clave de Calidad en TIC

La calidad en el desarrollo y servicio TIC no es que el software sea "bonito", sino que **cumpla exactamente con los requisitos** especificados y que sea **apto para el uso** del cliente.

**Patrón Lógico - Aseguramiento vs Control:** En los test siempre intentan confundir estos dos términos. Grábate esta diferencia:
*   **Aseguramiento de la Calidad (QA - Quality Assurance):** Orientado al **proceso**. Es *preventivo*. Define cómo se van a hacer las cosas para evitar errores. En Métrica v3 existe una interfaz específica para esto (Interfaz CAL), donde el Grupo de Aseguramiento de la Calidad elabora el plan y verifica que los productos intermedios cumplen las normas [cite: 4].
*   **Control de Calidad (QC - Quality Control):** Orientado al **producto**. Es *reactivo*. Son las pruebas reales que se hacen sobre el software ya construido para detectar fallos antes de entregarlo.

La familia de normas **ISO 9000** es el marco internacional de referencia sobre gestión de la calidad, y conviene diferenciar bien sus miembros porque es una trampa clásica de examen:
*   **ISO 9000:** Sistemas de gestión de la calidad — Fundamentos y vocabulario. Define los conceptos y los siete principios de gestión de la calidad.
*   **ISO 9001:** Sistemas de gestión de la calidad — Requisitos. Es la única de la familia que es **certificable**.
*   **ISO 9004:** Sistemas de gestión de la calidad — Directrices para la mejora continua del desempeño. Orientada a la gestión del éxito sostenido, no es certificable.
*   **ISO 19011:** Directrices para la auditoría de sistemas de gestión (calidad y medioambiente).

La norma ISO 9000:2015 establece **7 principios de gestión de la calidad** que son la base lógica de toda la ISO 9001 (hasta la versión 2008 eran 8; se redujeron a 7 tras fusionar "enfoque de sistema" dentro de "enfoque a procesos"):
1.  **Enfoque al cliente:** cumplir y superar sus expectativas.
2.  **Liderazgo:** la alta dirección crea las condiciones para que la calidad prospere.
3.  **Compromiso de las personas:** personal competente, facultado e implicado en todos los niveles.
4.  **Enfoque a procesos:** gestionar las actividades como procesos interrelacionados que funcionan como un sistema coherente.
5.  **Mejora:** búsqueda constante de un mejor desempeño.
6.  **Toma de decisiones basada en la evidencia:** decidir a partir del análisis de datos y hechos, no de la intuición.
7.  **Gestión de las relaciones:** administrar los vínculos con proveedores y aliados para lograr un desempeño sostenido.

---

## 2. El Modelo EFQM (Excelencia)

El modelo EFQM (European Foundation for Quality Management) no es una norma de obligado cumplimiento, sino un **marco de autoevaluación** para alcanzar la "Excelencia" organizativa.

**Patrón Lógico de EFQM - La regla Causa/Efecto:**
El modelo EFQM clásico (versión 2013, la más citada en manuales de oposición) se divide estrictamente en dos bloques que suman 9 criterios. Si te preguntan por un criterio, solo tienes que pensar: ¿es la herramienta (causa) o es lo que consigo (efecto)?
1.  **Agentes Facilitadores (Lo que la organización HACE):** Son 5 criterios. Liderazgo, Personas, Estrategia, Alianzas y Recursos, Procesos.
2.  **Resultados (Lo que la organización LOGRA):** Son 4 criterios. Resultados en los Clientes, Resultados en las Personas, Resultados en la Sociedad, Resultados Clave del negocio.

**La lógica RADAR (o REDER en español):** EFQM evalúa a las organizaciones usando esta matriz:
*   **R**esultados (Qué queremos lograr).
*   **E**nfoque (Approach - Cómo lo vamos a hacer).
*   **D**espliegue (Deploy - Ponerlo en práctica).
*   **E**valuación y **R**evisión (Assess & Refine - Medir y mejorar).

Desde enero de 2020 existe una **nueva versión del Modelo EFQM (EFQM Model 2020)** que sustituye a la de 2013 en las evaluaciones oficiales (desde el 1 de abril de 2021 solo se evalúa con esta versión), y que en el examen puede aparecer como actualización del modelo clásico. Sus cambios más relevantes:
*   Ya **no habla de "Excelencia"** sino de "organizaciones sobresalientes", y elimina la referencia expresa a 9 criterios agrupados en Agentes/Resultados.
*   Pasa a estructurarse en **7 criterios**, organizados según la lógica **Dirección → Ejecución → Resultados**: 1) Propósito, Visión y Estrategia; 2) Cultura de la Organización y Liderazgo; 3) Implicar a los Grupos de Interés; 4) Crear Valor Sostenible; 5) Impulsar el Rendimiento y la Transformación; 6) Percepción de los Grupos de Interés; 7) Rendimiento Estratégico y Operativo.
*   Ya no existe un criterio específico llamado "Personas": el factor humano queda transversal a lo largo de todo el modelo (especialmente en el criterio 2).
*   La matriz de puntuación pasa a llamarse simplemente REDER (ya no se publican las tablas de puntuación en el folleto público, sino en la plataforma digital de evaluación).
*   Los criterios de Resultados pasan de 500 a 400 puntos sobre 1000, dando mayor peso relativo a Dirección y Ejecución.

Para el examen, lo más seguro es dominar el **modelo clásico de 9 criterios y RADAR** (es el que suele aparecer en el temario oficial de oposiciones), pero conviene saber que existe esta actualización de 2020 por si se pregunta de forma explícita por la versión vigente.

---

## 3. ISO 9001 (Gestión de la Calidad)

A diferencia de EFQM, la norma ISO 9001 sí es **certificable**. Es el estándar internacional para los Sistemas de Gestión de Calidad (SGC).

**Patrón Lógico - El Ciclo de Deming (PDCA):**
Toda la ISO 9001 se basa en el ciclo de mejora continua o ciclo PDCA. En el test, asocia cada fase con su acción directa:
1.  **Plan (Planificar):** Establecer los objetivos y los procesos necesarios (ej. planificar cómo atender las incidencias de los usuarios).
2.  **Do (Hacer):** Implementar los procesos (ej. poner a los técnicos a atender llamadas según el plan).
3.  **Check (Verificar):** Medir y monitorizar los procesos contra los objetivos (ej. sacar un informe de cuánto tardamos en resolver las incidencias).
4.  **Act (Actuar):** Tomar acciones para mejorar el rendimiento continuamente (ej. si tardamos mucho, comprar una herramienta mejor o dar más formación).

La versión vigente de la norma es **ISO 9001:2015**, y su estructura de 10 capítulos sigue el llamado **"Anexo SL"**, la plantilla común de alto nivel que comparten todas las normas de sistemas de gestión ISO (también ISO 14001 de medio ambiente o ISO 27001 de seguridad), lo que facilita implantar sistemas integrados de gestión. Los capítulos con requisitos exigibles y su correspondencia con el ciclo PDCA son:
*   **4. Contexto de la organización** y **5. Liderazgo** → fase **Plan**, junto con el cap. 6.
*   **6. Planificación** → fase **Plan**: objetivos de calidad y gestión de riesgos.
*   **7. Apoyo** y **8. Operación** → fase **Do**: recursos, competencias, procesos operativos.
*   **9. Evaluación del desempeño** → fase **Check**: auditoría interna, revisión por la dirección, satisfacción del cliente.
*   **10. Mejora** → fase **Act**: no conformidades, acciones correctivas, mejora continua.

Un concepto que suele preguntarse junto al ciclo PDCA es el **enfoque basado en riesgos** (*risk-based thinking*), introducido de forma explícita en la versión 2015: la organización debe planificar acciones para abordar los riesgos y oportunidades que puedan afectar a la conformidad de sus productos/servicios, sustituyendo en parte al antiguo requisito de "acciones preventivas" de versiones anteriores (2008).

---

## 4. Ejemplo Real (Sin analogías)

Imagina el **Centro de Atención a Usuarios (CAU)** de tu ministerio:
*   **ISO 9001:** El CAU redacta un manual estricto sobre cómo se debe registrar un ticket, en qué tiempos debe resolverse y cómo se mide si se ha cumplido. Si viene un auditor externo y ve que todos los técnicos siguen el manual a rajatabla y que miden sus tiempos (Ciclo PDCA), el CAU **consigue el certificado ISO 9001**.
*   **EFQM:** El director del CAU quiere ir más allá de cumplir un manual; quiere la *excelencia*. Pasa cuestionarios anónimos a los técnicos para ver si están motivados (Agente: Personas), evalúa si los ministerios están contentos con el trato (Resultado en Clientes) e introduce mejoras basadas en la matriz RADAR. No recibe un "certificado" por cumplir mínimos, sino un **Sello de Excelencia (ej. +400 puntos EFQM)**.

---

## 5. Repaso

| Concepto | Palabra Chivata en el Test |
| :--- | :--- |
| **Aseguramiento de Calidad (QA)** | "Prevención", "Procesos", "Plan de calidad", "Métrica v3 interfaz CAL". |
| **Control de Calidad (QC)** | "Detección", "Producto", "Pruebas", "Inspección". |
| **ISO 9000** | "Fundamentos y vocabulario", "No certificable", "7 principios". |
| **ISO 9001** | "Certificable", "Sistema de Gestión de Calidad (SGC)", "Mejora continua", "Requisitos". |
| **ISO 9004** | "Mejora continua del desempeño", "Éxito sostenido", "No certificable". |
| **Ciclo PDCA (Deming)** | "Planificar, Hacer, Verificar, Actuar", "Mejora iterativa". |
| **Modelo EFQM (2013)** | "Autoevaluación", "Excelencia", "Agentes facilitadores y Resultados", "Matriz RADAR", "9 criterios". |
| **Modelo EFQM (2020)** | "Organización sobresaliente", "7 criterios", "Dirección-Ejecución-Resultados". |

### 5.1. Simulacro de Test

**Pregunta:**
*Dentro de los criterios del modelo de excelencia EFQM (versión clásica), ¿cuál de los siguientes elementos es considerado un "Agente Facilitador" y no un "Resultado"?*
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

**Pregunta:**
*¿Cuál de las siguientes normas de la familia ISO 9000 es la única que resulta certificable por una entidad externa?*
a) ISO 9000.
b) ISO 9001.
c) ISO 9004.
d) ISO 19011.

**Razonamiento Estructurado:**
1.  ISO 9000 recoge solo fundamentos y vocabulario; ISO 9004 son directrices para la mejora del desempeño; ISO 19011 son directrices de auditoría. Ninguna de las tres establece requisitos certificables.
2.  ISO 9001 es la norma de "Requisitos" del Sistema de Gestión de Calidad, y es la única que una organización puede certificar frente a un organismo acreditado.
3.  **Respuesta correcta:** B.

**Pregunta:**
*Según el Modelo EFQM 2020, ¿cuál de las siguientes afirmaciones es correcta respecto a la versión anterior (2013)?*
a) Mantiene los 9 criterios agrupados en Agentes Facilitadores y Resultados.
b) Introduce un criterio específico y aislado llamado "Personas".
c) Se estructura en 7 criterios bajo la lógica Dirección-Ejecución-Resultados.
d) Elimina por completo la matriz REDER de evaluación.

**Razonamiento Estructurado:**
1.  (A) es falsa porque el modelo 2020 abandona la estructura de 9 criterios en favor de 7. (B) es falsa porque las Personas dejan de tener un criterio propio y pasan a ser transversales. (D) es falsa porque REDER sigue siendo la lógica de evaluación, solo cambia cómo se publican las tablas de puntuación.
2.  (C) describe exactamente la nueva estructura: Dirección (criterios 1-2), Ejecución (criterios 3-5) y Resultados (criterios 6-7).
3.  **Respuesta correcta:** C.
