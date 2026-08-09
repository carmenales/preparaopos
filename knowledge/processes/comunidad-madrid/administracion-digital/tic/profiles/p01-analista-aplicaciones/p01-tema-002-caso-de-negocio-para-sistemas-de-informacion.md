---
id: "cm-ad-tic-p01-tema-002-caso-de-negocio"
title: "Caso de negocio para sistemas de información"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/tic"
profiles:
  - "p01-analista-aplicaciones"
official_profile: "P01 - Analista de Aplicaciones"
official_topic: "Tema 2. Caso de negocio para sistemas de información"
source_ids:
  - "A2_Bloque_IV.pdf"
tags:
  - "caso-de-negocio"
  - "business-case"
  - "prince2"
  - "gestion-proyectos"
  - "viabilidad"
  - "benefits-review-plan"
created_at: "2026-08-09"
last_reviewed: "2026-08-09"
ai_generated: true
ai_sources:
  - "gemini"
  - "perplexity"
needs_human_review: true
---

# Tema 2. Caso de negocio para sistemas de información

## 1. Casos de negocio en el ámbito de los sistemas de información (PRINCE2)

En el ámbito de la gestión de proyectos, especialmente bajo la metodología estructurada **PRINCE2**, el **Caso de Negocio (Business Case)** es el motor que impulsa el proyecto. No se trata de un documento estático que se escribe al principio y se olvida, sino de una herramienta dinámica de gestión.

La metodología PRINCE2 se fundamenta en 7 principios, siendo el primero y más importante la **Justificación Comercial Continua**. Esto significa que un proyecto para implementar o modificar un sistema de información solo debe iniciarse, y continuar, si existe una necesidad de negocio clara, unos beneficios cuantificables que superan a los costes, y unos riesgos aceptables.

Si en cualquier momento del ciclo de vida del desarrollo de software los costes se disparan o los beneficios esperados desaparecen (por ejemplo, por un cambio normativo o tecnológico), el Caso de Negocio deja de ser viable y el proyecto debe detenerse.

PRINCE2 formaliza la gestión del Caso de Negocio como el **tema "Business Case"**, uno de los 7 temas del método, y define su ciclo de vida mediante una **técnica de cuatro pasos** que conviene memorizar literalmente porque es muy examinable:
1.  **Desarrollar (*Develop*):** explorar opciones y reunir la información necesaria para la decisión de inversión.
2.  **Verificar (*Check*):** evaluar si el proyecto sigue mereciendo la pena, antes de cada autorización importante.
3.  **Mantener (*Maintain*):** mantener el Caso de Negocio actualizado con el progreso real y las previsiones vigentes, incluidos los beneficios previstos.
4.  **Confirmar (*Confirm*):** valorar si los beneficios previstos se han conseguido o se van a conseguir realmente; esta confirmación ocurre principalmente después del cierre del proyecto, aunque algunos beneficios pueden materializarse durante su ejecución.

El Caso de Negocio se desarrolla por primera vez en la fase de preproyecto (proceso *Starting Up a Project*) como un **Caso de Negocio Preliminar o Esbozado (*Outline Business Case*)**, y se completa y detalla durante la fase de inicio (proceso *Initiating a Project*) hasta convertirse en el **Caso de Negocio Detallado (*Detailed Business Case*)**, que se mantiene y actualiza durante toda la ejecución del proyecto.

## 2. Utilidad del caso de negocio

El Caso de Negocio tiene múltiples utilidades prácticas y de gobierno dentro de la Administración y la empresa privada:

*   **Toma de decisiones (Go / No-Go):** Es la base sobre la cual el Comité de Dirección (o Project Board en PRINCE2) decide si autoriza el inicio del proyecto, si aprueba el paso a la siguiente fase, o si cancela la iniciativa.
*   **Alineación Estratégica:** Garantiza que el sistema de información a desarrollar está alineado con los objetivos estratégicos de la organización (por ejemplo, el Plan de Digitalización de las AAPP).
*   **Gestión de Expectativas:** Define claramente qué valor se va a entregar, evitando que el proyecto se convierta en un fin técnico en sí mismo en lugar de una solución de negocio.
*   **Línea base para la evaluación final:** Al cerrar el proyecto, se utiliza para evaluar (Revisión de Beneficios) si el sistema de información entregado realmente ha generado el valor que prometió.

En el proceso **Dirigir un Proyecto (*Directing a Project*)**, el Comité de Proyecto debe confirmar expresamente, antes de autorizar el proyecto, que existe un Caso de Negocio adecuado y apropiado que demuestra un proyecto viable, y que están establecidos los mecanismos para medir y revisar los beneficios previstos. Esto convierte al Caso de Negocio en el documento habilitante de cada gran decisión de gobierno del proyecto (autorización de inicio, autorización del proyecto, autorización de cada fase y autorización del cierre).

## 3. Criterios

Para que un Caso de Negocio sea válido y autorizable, debe cumplir con una serie de criterios rigurosos:

*   **Deseable:** El balance entre los costes, los beneficios y los riesgos debe ser positivo.
*   **Viable:** La solución técnica debe ser posible de construir e integrar en la infraestructura existente.
*   **Alcanzable:** La organización debe tener la capacidad (recursos, tiempo, presupuesto) para entregar los productos que generarán los beneficios.

Desde el punto de vista financiero, los criterios se suelen apoyar en técnicas de evaluación de inversiones (Matemática Financiera):
*   **ROI (Retorno de la Inversión):** Porcentaje de beneficio obtenido frente a la inversión.
*   **VAN (Valor Actual Neto):** Valor presente de los flujos de caja futuros descontando la inflación/coste del dinero. Si VAN > 0, es rentable.
*   **TIR (Tasa Interna de Retorno):** Rentabilidad intrínseca del proyecto.
*   **Payback (Plazo de Recuperación):** Tiempo necesario para recuperar la inversión inicial.

Estos cuatro indicadores conforman lo que PRINCE2 denomina la sección de **Análisis de Inversión (*Investment Appraisal*)** del Caso de Negocio, que proporciona al Project Board la información necesaria para verificar que el Caso de Negocio justifica la autorización o continuación del proyecto. Un matiz importante para examen: el VAN y el TIR incorporan el valor temporal del dinero (descuentan flujos de caja futuros a valor presente mediante una tasa de descuento), mientras que el ROI simple y el Payback básico no lo hacen, por lo que ofrecen una visión menos precisa en proyectos de larga duración.

## 4. Contenido Típico

Según el estándar PRINCE2, un esquema de Caso de Negocio formal contiene los siguientes apartados:

| Sección | Descripción |
| :--- | :--- |
| **Resumen Ejecutivo** | Visión general de los puntos clave del documento (útil para la alta dirección). |
| **Razones (Motivos)** | El problema u oportunidad que justifica por qué se necesita el proyecto (ej. "La aplicación actual no cumple el ENS"). |
| **Opciones de Negocio** | Alternativas evaluadas. PRINCE2 exige al menos 3: *No hacer nada* (línea base), *Hacer lo mínimo*, y *Hacer algo* (la opción recomendada). |
| **Beneficios Esperados** | Mejoras cuantificables y medibles resultantes del proyecto (ej. "Ahorro de 50.000€ anuales en licencias"). Deben tener tolerancias. |
| **Disbeneficios** | Resultados medibles percibidos como negativos por uno o más interesados (ej. "El nuevo sistema requerirá que el personal trabaje fines de semana durante la migración"). |
| **Plazos (Timescale)** | Cuándo comenzará el proyecto, cuándo finalizará y cuándo se materializarán los beneficios. |
| **Costes** | Presupuesto necesario extraído del Plan del Proyecto, incluyendo costes de operación y mantenimiento a largo plazo. |
| **Análisis de Inversión** | Comparativa entre los costes de desarrollo/operación y el valor de los beneficios. |
| **Riesgos Principales** | Amenazas y oportunidades que podrían alterar la viabilidad del Caso de Negocio. |

Junto al propio documento del Caso de Negocio, PRINCE2 exige un producto de gestión complementario e inseparable: el **Plan de Revisión de Beneficios (*Benefits Review Plan*, BRP)**. Este plan define el alcance, el momento y la responsabilidad de las revisiones necesarias para comprobar si los beneficios previstos se están logrando (o se lograrán). Lo elabora por primera vez el Jefe de Proyecto durante la fase de inicio y lo aprueba el Project Board junto con el propio Caso de Negocio; se actualiza al final de cada fase incorporando los beneficios realmente conseguidos hasta ese momento, y contempla revisiones tanto durante el proyecto (cuando algún beneficio pueda materializarse antes del cierre) como, sobre todo, después de finalizado el proyecto (revisión postproyecto).

## 5. Responsabilidades

Los tribunales de oposición TIC suelen preguntar por la asignación de responsabilidades sobre el Caso de Negocio. Según PRINCE2, se distribuyen así:

*   **Ejecutivo (Executive):** Es el **dueño y responsable final** del Caso de Negocio. Su misión es asegurar que el proyecto aporta valor por el dinero invertido (*Value for Money*).
*   **Jefe de Proyecto (Project Manager):** Es quien **prepara, redacta y actualiza** el documento del Caso de Negocio en nombre del Ejecutivo, basándose en la información que recaba del resto del equipo.
*   **Usuario Principal (Senior User):** Es responsable de **especificar los beneficios esperados** en el Caso de Negocio y, posteriormente, demostrar que dichos beneficios se han hecho realidad tras la entrega del sistema.
*   **Proveedor Principal (Senior Supplier):** Es responsable de proporcionar las **estimaciones de coste y tiempo** (esfuerzo técnico) para alimentar el análisis de inversión del Caso de Negocio.

Existe un quinto rol, distinto de los tres del Project Board, que suele ser trampa habitual en examen por confundirse con el Ejecutivo: el **Project Assurance (Aseguramiento del Proyecto)**. Este rol, ejercido en nombre del Project Board (y con frecuencia delegado a cada uno de sus tres miembros en su ámbito respectivo: Business Assurance, User Assurance y Supplier Assurance), tiene entre sus funciones específicas sobre el Caso de Negocio:
*   Ayudar al Jefe de Proyecto en el desarrollo del Caso de Negocio y del Plan de Revisión de Beneficios.
*   **Verificar y monitorizar** el Caso de Negocio frente a eventos externos y frente al progreso real del proyecto (labor de control independiente, distinta de la autoría, que corresponde al Jefe de Proyecto).
*   Comprobar que el Caso de Negocio se sigue cumpliendo a lo largo de todo el proyecto y que el proyecto permanece alineado con la estrategia corporativa o de programa.

El matiz clave para no confundir roles: el **Ejecutivo es propietario y responsable último**, el **Jefe de Proyecto redacta y mantiene el documento por delegación**, y el **Project Assurance verifica de forma independiente** que ese documento sigue siendo válido, sin ser su autor ni su propietario.

## 6. Relación con el Plan del Proyecto

El Caso de Negocio y el Plan del Proyecto mantienen una relación de **dependencia bidireccional y evolución paralela** a lo largo de todo el ciclo de vida:

1.  **El Plan alimenta al Caso de Negocio:** Para poder justificar la viabilidad de un proyecto, necesitamos saber cuánto costará y cuánto tardará. Estos datos (Costes y Plazos) son el resultado directo de elaborar el Plan del Proyecto.
2.  **El Caso de Negocio justifica al Plan:** Por muy detallado e impecable que sea un Plan de Proyecto, no sirve de nada si no está justificado por un Caso de Negocio viable.
3.  **Actualización síncrona:** Si durante la ejecución se produce una incidencia técnica que retrasa el *Plan del Proyecto* 3 meses y encarece el desarrollo un 20%, el Jefe de Proyecto debe actualizar el *Caso de Negocio* con estos nuevos datos y elevarlo al Comité de Dirección para que decida si, con esos nuevos costes, los beneficios siguen mereciendo la pena.

Esta relación se concreta de forma muy precisa en el proceso de **Iniciar un Proyecto**: el Caso de Negocio Preliminar (elaborado en la fase de preproyecto con estimaciones muy generales) se actualiza a Caso de Negocio Detallado incorporando exactamente tres insumos procedentes de otros productos de gestión ya elaborados: los **costes y plazos calculados en el Plan de Proyecto**, los **riesgos principales identificados en el Registro de Riesgos** que afectan a la viabilidad y alcanzabilidad del proyecto, y los **beneficios y sus tolerancias**, alineados con el Plan de Revisión de Beneficios. Esta secuencia demuestra por qué, en PRINCE2, nunca se aprueba un Caso de Negocio Detallado sin haber elaborado primero un Plan de Proyecto: uno depende técnicamente del otro.

## 7. Resumen

| Concepto | Palabra Chivata en el Test |
| :--- | :--- |
| **Caso de Negocio** | "Justificación comercial", "Evaluar viabilidad", "Causa raíz del proyecto". |
| **Principio rector** | "Justificación comercial continua", "Revisión en los límites de fase". |
| **4 pasos de gestión del Business Case** | "Desarrollar, Verificar, Mantener, Confirmar". |
| **Outline vs. Detailed Business Case** | Outline = "preproyecto, estimaciones generales"; Detailed = "fase de inicio, datos del Plan de Proyecto". |
| **Plan de Revisión de Beneficios (BRP)** | "Define cuándo y cómo se medirán los beneficios", "Se actualiza al final de cada fase". |
| **Disbeneficios** | "Consecuencia negativa medible", "Efecto adverso inevitable". |
| **Ejecutivo (Executive)** | "Propietario del Business Case", "Asegura el Value for Money", "Responsable final". |
| **Jefe de Proyecto (PM)** | "Redacta", "Actualiza", "Mantiene". |
| **Usuario Principal** | "Identifica y especifica beneficios", "Rinde cuentas de los beneficios". |
| **Project Assurance** | "Verifica de forma independiente", "No es el autor ni el propietario", "Comprueba alineación estratégica". |
| **Opciones básicas** | "No hacer nada, Hacer lo mínimo, Hacer algo". |

### 7.1. Simulacro de Test: Desmontando trampas

**Pregunta:**
*Según PRINCE2, ¿cuál de los siguientes roles es responsable de verificar y monitorizar de forma independiente el Caso de Negocio frente a eventos externos y al progreso del proyecto, sin ser su propietario ni su autor?*
a) El Ejecutivo (Executive).
b) El Jefe de Proyecto (Project Manager).
c) El Project Assurance.
d) El Senior Supplier.

**Razonamiento Estructurado:**
1.  **Busca la palabra chivata:** "verificar y monitorizar de forma independiente... sin ser su propietario ni su autor".
2.  **Aplica el patrón de descarte:** El Ejecutivo (A) es el propietario y responsable final, no un verificador independiente. El Jefe de Proyecto (B) es el autor que redacta y actualiza el documento, no quien lo verifica de forma independiente. El Senior Supplier (D) aporta estimaciones de coste y tiempo, no verifica el Caso de Negocio en su conjunto.
3.  El **Project Assurance** es precisamente el rol que, actuando en nombre del Project Board, verifica y monitoriza el Caso de Negocio de forma independiente a lo largo de todo el proyecto.
4.  **Respuesta correcta:** C.

### 7.2. Simulacro de Test adicional

**Pregunta:**
*Según la técnica PRINCE2 de gestión del Caso de Negocio en cuatro pasos, ¿en qué paso se evalúa si los beneficios previstos se han conseguido realmente, comprobación que ocurre principalmente después del cierre del proyecto?*
a) Desarrollar (Develop).
b) Verificar (Check).
c) Mantener (Maintain).
d) Confirmar (Confirm).

**Razonamiento Estructurado:**
1.  "Desarrollar" (A) ocurre al principio, explorando opciones. "Verificar" (B) se hace antes de cada autorización importante, para decidir si el proyecto sigue mereciendo la pena. "Mantener" (C) consiste en actualizar el documento con el progreso real durante la ejecución.
2.  El enunciado describe exactamente la comprobación de si los beneficios se han materializado, lo cual ocurre sobre todo tras el cierre del proyecto: esa es la definición literal del paso "Confirmar".
3.  **Respuesta correcta:** D.

**Pregunta:**
*Durante el proceso de Iniciar un Proyecto en PRINCE2, el Jefe de Proyecto actualiza el Caso de Negocio Preliminar para convertirlo en el Caso de Negocio Detallado. ¿De qué producto de gestión obtiene los datos de costes y plazos necesarios para esta actualización?*
a) Del Registro de Riesgos.
b) Del Plan de Proyecto.
c) Del Informe de Excepción.
d) Del Registro de Interesados.

**Razonamiento Estructurado:**
1.  El Registro de Riesgos (A) aporta los riesgos principales, no los costes ni plazos. El Informe de Excepción (C) solo se genera si se prevé superar una tolerancia, no es un insumo estándar del Caso de Negocio Detallado. El Registro de Interesados (D) no aporta datos financieros ni de calendario.
2.  Los costes y plazos del Caso de Negocio Detallado provienen directamente del Plan de Proyecto, que ya ha sido elaborado con mayor precisión durante la fase de inicio.
3.  **Respuesta correcta:** B.
