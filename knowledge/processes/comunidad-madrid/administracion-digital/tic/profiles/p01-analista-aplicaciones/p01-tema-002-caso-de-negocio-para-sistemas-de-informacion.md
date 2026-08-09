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

## 2. Utilidad del caso de negocio

El Caso de Negocio tiene múltiples utilidades prácticas y de gobierno dentro de la Administración y la empresa privada:

*   **Toma de decisiones (Go / No-Go):** Es la base sobre la cual el Comité de Dirección (o Project Board en PRINCE2) decide si autoriza el inicio del proyecto, si aprueba el paso a la siguiente fase, o si cancela la iniciativa.
*   **Alineación Estratégica:** Garantiza que el sistema de información a desarrollar está alineado con los objetivos estratégicos de la organización (por ejemplo, el Plan de Digitalización de las AAPP).
*   **Gestión de Expectativas:** Define claramente qué valor se va a entregar, evitando que el proyecto se convierta en un fin técnico en sí mismo en lugar de una solución de negocio.
*   **Línea base para la evaluación final:** Al cerrar el proyecto, se utiliza para evaluar (Revisión de Beneficios) si el sistema de información entregado realmente ha generado el valor que prometió.

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

## 5. Responsabilidades

Los tribunales de oposición TIC suelen preguntar por la asignación de responsabilidades sobre el Caso de Negocio. Según PRINCE2, se distribuyen así:

*   **Ejecutivo (Executive):** Es el **dueño y responsable final** del Caso de Negocio. Su misión es asegurar que el proyecto aporta valor por el dinero invertido (*Value for Money*).
*   **Jefe de Proyecto (Project Manager):** Es quien **prepara, redacta y actualiza** el documento del Caso de Negocio en nombre del Ejecutivo, basándose en la información que recaba del resto del equipo.
*   **Usuario Principal (Senior User):** Es responsable de **especificar los beneficios esperados** en el Caso de Negocio y, posteriormente, demostrar que dichos beneficios se han hecho realidad tras la entrega del sistema.
*   **Proveedor Principal (Senior Supplier):** Es responsable de proporcionar las **estimaciones de coste y tiempo** (esfuerzo técnico) para alimentar el análisis de inversión del Caso de Negocio.

## 6. Relación con el Plan del Proyecto

El Caso de Negocio y el Plan del Proyecto mantienen una relación de **dependencia bidireccional y evolución paralela** a lo largo de todo el ciclo de vida:

1.  **El Plan alimenta al Caso de Negocio:** Para poder justificar la viabilidad de un proyecto, necesitamos saber cuánto costará y cuánto tardará. Estos datos (Costes y Plazos) son el resultado directo de elaborar el Plan del Proyecto.
2.  **El Caso de Negocio justifica al Plan:** Por muy detallado e impecable que sea un Plan de Proyecto, no sirve de nada si no está justificado por un Caso de Negocio viable.
3.  **Actualización síncrona:** Si durante la ejecución se produce una incidencia técnica que retrasa el *Plan del Proyecto* 3 meses y encarece el desarrollo un 20%, el Jefe de Proyecto debe actualizar el *Caso de Negocio* con estos nuevos datos y elevarlo al Comité de Dirección para que decida si, con esos nuevos costes, los beneficios siguen mereciendo la pena.

## 7. Resumen

| Concepto | Palabra Chivata en el Test |
| :--- | :--- |
| **Caso de Negocio** | "Justificación comercial", "Evaluar viabilidad", "Causa raíz del proyecto". |
| **Principio rector** | "Justificación comercial continua", "Revisión en los límites de fase". |
| **Disbeneficios** | "Consecuencia negativa medible", "Efecto adverso inevitable". |
| **Ejecutivo (Executive)** | "Propietario del Business Case", "Asegura el Value for Money", "Responsable final". |
| **Jefe de Proyecto (PM)** | "Redacta", "Actualiza", "Mantiene". |
| **Usuario Principal** | "Identifica y especifica beneficios", "Rinde cuentas de los beneficios". |
| **Opciones básicas** | "No hacer nada, Hacer lo mínimo, Hacer algo". |