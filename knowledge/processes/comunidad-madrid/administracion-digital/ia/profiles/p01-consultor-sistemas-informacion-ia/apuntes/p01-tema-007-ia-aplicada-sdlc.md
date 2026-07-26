---
id: "cm-ad-ia-p01-tema-007-ia-aplicada-sdlc"
title: "IA aplicada al ciclo de vida de desarrollo del software"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/ia"
profiles:
  - "p01-consultor-sistemas-informacion-ia"
official_profile: "P01 - Consultor de Sistemas de Información - IA Aplicada al Ciclo de Vida del Software"
official_topic: "Tema 7. IA aplicada al ciclo de vida de desarrollo del software"
source_ids:
tags:
  - "inteligencia-artificial"
  - "ia-generativa"
  - "sdlc"
  - "devsecops"
  - "llm-coding"
  - "metricas-dora"
  - "nist-ssdf"
created_at: "2026-07-10"
last_reviewed: null
ai_generated: true
ai_sources:
  - "perplexity"
  - "chatgpt"
  - "gemini"
needs_human_review: true
---

# IA aplicada al ciclo de vida de desarrollo del software

## Encaje en la convocatoria

Este tema corresponde al **Tema 7 del Anexo 3** de la Resolución 352/2026 (BOCM 11/06/2026), exclusivo para el perfil **P01 – Consultor de Sistemas de Información especialista en IA aplicada al ciclo de vida del software** de la Agencia para la Administración Digital de la Comunidad de Madrid.  

El epígrafe oficial abarca: **implantación de la IA en el SDLC (estrategias, modelos de madurez y buenas prácticas)**, **modelos LLM específicos para código**, **casos de uso a lo largo del ciclo de vida** e **indicadores de medición del retorno (ROI)**, enlazando con preguntas sobre Shadow AI, DORA, SPACE, NIST SSDF, FIM y sesgo de automatización.

## Ideas clave

1. **La IA afecta a todo el SDLC:** Impacta requisitos, diseño, codificación, pruebas, seguridad, CI/CD y operación; por tanto, debe gobernarse de extremo a extremo, no solo en la generación inicial de código.  
2. **Shadow AI (IA en la sombra):** Uso no autorizado de LLMs públicos por los desarrolladores, enviando código corporativo o secretos, con riesgo de fuga de datos y reentrenamiento del modelo con información sensible.  
3. **Enterprise copilots y “Zero Data Retention”:** En sector público se exigen servicios corporativos con cláusulas de **no retención de datos**, de modo que prompts y código de contexto no alimentan el modelo base del proveedor.  
4. **Public Code Matching y propiedad intelectual:** Es vital bloquear sugerencias que coincidan con código público bajo licencias restrictivas (GPL, copyleft) para evitar obligación de liberar el código de la Administración.  
5. **Fill‑in‑the‑Middle (FIM):** Capacidad técnica diferencial de modelos de código, que predicen el bloque intermedio analizando simultáneamente el prefijo y el sufijo de código alrededor del cursor.  
6. **Métricas DORA y SPACE:** Medir líneas de código generadas es una métrica de vanidad; el ROI se evalúa con métricas DORA (Deployment Frequency, Lead Time, Change Failure Rate, Time to Restore) y SPACE (Satisfaction, Performance, Activity, Communication, Efficiency).  
7. **Sesgo de automatización:** Riesgo de aceptación ciega de sugerencias plausibles pero erróneas; aumenta la **Change Failure Rate** y compromete la calidad y seguridad del software.  
8. **NIST SP 800‑218A:** Extensión del **Secure Software Development Framework (SSDF)** con prácticas específicas para sistemas con IA generativa y modelos fundacionales.

## Desarrollo

### 1. Implantación de la IA en la práctica del SDLC

La adopción de IA en desarrollo es una transformación organizativa que requiere estrategia, arquitectura de plataforma (platform engineering), políticas de seguridad y gobierno de datos.

#### 1.1. Estrategias y buenas prácticas

- **ISO/IEC 5338:2023** describe procesos de ciclo de vida para sistemas de IA, alineando la implantación con estándares de ingeniería de sistemas.  
- **OWASP AISVS (AI Security Verification Standard, Appendix C)** define requisitos de seguridad para codificación asistida por IA, cubriendo diseño seguro, implementación, pruebas y monitorización en un SSDLC (Secure SDLC).  
- En la Administración, se exige **Human‑in‑the‑Loop (HITL)**: el modelo sugiere, pero el ingeniero revisa, decide y asume responsabilidad; el proveedor del modelo no responde de los defectos del código desplegado.

Esta filosofía se conecta con el ENS (RD 311/2022), que exige seguridad como proceso integral y diferenciación de responsabilidades en el ciclo de vida.

#### 1.2. Modelo de madurez de adopción de IA

Basado en modelos de la industria (IBM, etc.), se suelen distinguir cinco fases.

1. **Consumo ad‑hoc de modelos genéricos (Reactivo):**  
   Uso individual no regulado; máximo riesgo de Shadow AI y fuga de datos.
2. **Proyectos piloto (Conciencia básica):**  
   Herramientas aprobadas para casos aislados, documentación inicial y concienciación sobre calidad y seguridad.
3. **Estrategia centralizada / gobierno establecido:**  
   - Despliegue de asistentes corporativos (*enterprise copilots*) con protección de IP.  
   - Definición de políticas y catálogos de casos de uso permitidos.  
   - Formación estructurada y métricas base.
4. **Mejora de colaboración con medición cuantitativa:**  
   - Toma de decisiones basada en datos (dashboard DORA/SPACE).  
   - Uso sistemático de IA para abordar deuda técnica y tareas de bajo valor repetitivo.
5. **Innovación y gobierno avanzado (Optimizado):**  
   - Integración de agentes IA en CI/CD y testing (agentes revisores de código, generadores de pruebas).  
   - Operación bajo esquemas Human‑on‑the‑Loop (HOTL), con supervisión significativa y medición continua de riesgos.

### 2. Modelos LLM específicos para código

Los LLM generalistas (GPT‑4, Claude, etc.) son potentes en razonamiento, pero los modelos específicos de código se entrenan con grandes repositorios públicos (GitHub, GitLab), documentación técnica, issues y pull requests.

#### 2.1. Arquitectura Fill‑in‑the‑Middle (FIM)

FIM es clave en autocompletado de código en IDEs.

- En vez de solo predecir hacia adelante, se introduce un esquema de preentrenamiento con tokens especiales (`<PRE>`, `<MID>`, `<SUF>`).  
- El modelo analiza el **prefijo** (código antes del cursor) y el **sufijo** (código después del cursor) para inferir el bloque intermedio que falta.  
- Esto permite sugerencias que respetan el contexto global y evitan romper lógica antes y después del punto de edición.

#### 2.2. Tipos de modelos de código

- **Modelos de autocompletado de baja latencia:**  
  Optimizados para FIM en tiempo real, con tamaños moderados (1B‑7B parámetros) y latencias inferiores a ~200 ms.
- **Modelos conversacionales técnicos:**  
  Usados para refactorizaciones, explicación de código y revisiones; suelen integrar RAG interno leyendo el workspace del proyecto.
- **Modelos de embeddings de código:**  
  No generan código; convierten fragmentos en vectores para búsqueda semántica, deduplicación y análisis de repositorios corporativos.

Estos modelos requieren controles de propiedad intelectual (Public Code Matching) para evitar sugerencias de código sujeto a licencias restrictivas.

### 3. Casos de uso de IA a lo largo del SDLC

La IA se distribuye sobre todas las fases del ciclo de vida.

#### 3.1. Requisitos y análisis

- Generación asistida de **historias de usuario** en formato BDD (Gherkin: `Feature`, `Scenario`, `Given`, `When`, `Then`), que luego se usan en pruebas automatizadas.  
- Detección de ambigüedades, inconsistencias y requisitos incompletos en documentación.

#### 3.2. Diseño y arquitectura

- Generación de diagramas a partir de texto usando **diagram‑as‑code** (Mermaid, PlantUML).  
- Redacción de **Architecture Decision Records (ADR)** para documentar decisiones arquitecturales asistidas por IA.

#### 3.3. Codificación

- Generación de **boilerplate** (código repetitivo: controladores, DTOs, configuración).  
- Explicación de código complejos, especialmente en sistemas legacy sin documentación.  
- Traducción entre lenguajes (por ejemplo, modernización de COBOL/Java 8 a Java 21), teniendo siempre en cuenta las normas de seguridad y pruebas.

#### 3.4. Pruebas

- Sugerencia de casos de prueba unitarios, de integración y edge cases, incluyendo construcción de mocks y datos de prueba representativos.  
- Generación de código de test, que siempre se ejecuta en el motor de CI/CD; la IA **no ejecuta** las pruebas, solo las redacta.

#### 3.5. Seguridad: DevSecOps y SAST + IA

- Herramientas de análisis estático (SAST) detectan vulnerabilidades; la IA genera explicaciones más claras y propuestas de parches concretos.  
- El uso de IA debe alinearse con estándares como **OWASP ASVS** y **AISVS**, integrando revisión de seguridad en el flujo automatizado.

#### 3.6. CI/CD y operación

- Generación de pipelines (YAML para GitHub Actions, GitLab CI, Azure DevOps, etc.).  
- Explicación de builds fallidos y errores complejos.  
- Asistencia para análisis de logs y redacción de **post‑mortems** de incidentes (Root Cause Analysis).

### 4. Indicadores de medición del retorno (ROI)

Medir el éxito por volumen de código generado por IA es peligroso; puede incrementar deuda técnica y vulnerabilidades.

#### 4.1. Métricas de interacción y adopción

- **CAR (Code Acceptance Rate):** Porcentaje de sugerencias de código de IA que el desarrollador acepta y conserva.  
  - Valores típicos en equipos maduros se sitúan alrededor del 25‑40 %.  
  - Un CAR muy alto con alta Change Failure Rate puede indicar sesgo de automatización; uno muy bajo puede reflejar mala calidad de sugerencias o falta de confianza.

#### 4.2. Métricas DORA

El marco **DORA** (DevOps Research and Assessment) evalúa rendimiento de entrega, clave para ver el impacto real de IA.

1. **Deployment Frequency:**  
   ¿Permite la IA desplegar con más frecuencia sin comprometer estabilidad?
2. **Lead Time for Changes:**  
   ¿Reduce el tiempo desde commit hasta producción?.
3. **Change Failure Rate:**  
   Métrica crítica; si el sesgo de automatización lleva a aceptar código defectuoso, esta tasa se eleva.
4. **Time to Restore Service (MTTR):**  
   ¿Ayuda la IA a diagnosticar y resolver incidentes más rápido, reduciendo MTTR?.

Las preguntas de examen usan DORA como estándar recomendado para medir retorno del uso de IA en la entrega de software.

#### 4.3. Framework SPACE

El framework **SPACE** (GitHub/Microsoft) evalúa productividad más allá del código.

- **S – Satisfaction & Well‑being:**  
  Reducción de tareas repetitivas puede mejorar satisfacción y disminuir burnout.
- **P – Performance:**  
  Calidad y fiabilidad del software (menos fallos, mejores métricas de servicio).
- **A – Activity:**  
  Commits, PRs, despliegues; métricas crudas que no deben interpretarse en solitario.
- **C – Communication & Collaboration:**  
  IA puede ayudar en revisiones de código, redacción de PRs y documentación.
- **E – Efficiency & Flow:**  
  IA reduce **context switching** (ir al navegador a buscar información), permitiendo que el desarrollador mantenga flujo de trabajo continuo en el IDE.

En preguntas, SPACE se usa para justificar que asistentes IA mejoran **Efficiency & Flow** al reducir cambios de contexto.

#### 4.4. Cálculo general de ROI

De forma simplificada:

\[
\text{ROI} = \frac{\text{Ahorro en tiempo, defectos y retrabajo} - \text{Costes totales}}{\text{Costes totales}}
\]

Los **costes totales** incluyen licencias, tokens, infraestructura de soporte (RAG, gateways), formación, gestión del cambio, auditorías de seguridad y gobierno de datos.

La literatura comenta la posible **paradoja de Jevons**: hacer desarrollo más barato y rápido incrementa la demanda de software y funcionalidades, de modo que el gasto total puede mantenerse o aumentar, aunque el valor entregado crezca.

## Conceptos que suelen preguntarse

| Concepto                  | Realidad técnica / normativa                                                                                       | Distractor típico en examen                                                |
| :------------------------ | :------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------- |
| **Shadow AI**            | Uso de LLMs públicos no autorizados con datos corporativos; riesgo grave de fuga de PII y propiedad intelectual. | “Técnica de despliegue oscuro (shadow deployment).”              |
| **FIM (Fill‑in‑the‑Middle)** | Inferencia analizando prefijo y sufijo para insertar código en medio (autocompletado avanzado en IDEs).     | “Modelo que solo entiende código de arriba abajo.”              |
| **Métricas de productividad** | DORA (flujo de entrega) y SPACE (experiencia y fricción), no LOC generadas.                      | “Líneas de código generadas al día es la mejor métrica.”        |
| **NIST SP 800‑218A**     | Perfil del SSDF específico para GenAI y modelos fundacionales en desarrollo seguro.                       | “Ley europea que prohíbe IA en software crítico.”               |
| **Sesgo de automatización** | Aceptación ciega de sugerencias plausibles pero erróneas; aumenta Change Failure Rate.          | “Bug interno del modelo de ML.”                                 |
| **Public Code Matching** | Filtro que bloquea sugerencias idénticas a código público bajo licencias restrictivas (GPL/copyleft).    | “Buscador para descargar librerías open source.”                |
| **CAR (Code Acceptance Rate)** | Porcentaje de sugerencias de IA aceptadas y mantenidas por el desarrollador.                            | “Mide cuántos usuarios instalan la extensión en el IDE.”        |
| **DORA vs otras métricas** | DORA es estándar para medir rendimiento DevOps; se recomienda para medir impacto de IA en entrega.      | “ISO 25010 o OWASP son estándares de métricas de entrega.”      |
| **SPACE – Efficiency & Flow** | Dimensión que evalúa reducción de fricción y cambios de contexto, clave en uso de IA en IDEs.   | “La mejora de flujo se refleja solo en actividad (nº de commits).” |

## Posibles preguntas tipo test

**Pregunta 1.** Según DORA y SPACE, ¿cuál es el principal riesgo de usar como KPI principal “volumen total de líneas de código generadas por IA al día”?

A. Provoca latencia excesiva en la red del IDE.  
B. Es una métrica de vanidad que puede ocultar deuda técnica, vulnerabilidades y aumento de costes de mantenimiento.  
C. Las licencias corporativas cobran solo por línea de código.  
D. Reduce la temperatura algorítmica del modelo FIM.  

**Respuesta correcta: B.** (el volumen de código sin contexto puede degradar gravemente la calidad).

---

**Pregunta 2.** En LLMs de codificación, la capacidad FIM (*Fill‑in‑the‑Middle*) permite:

A. Reentrenar dinámicamente el modelo fundacional con los últimos commits en ejecución.  
B. Predecir y generar código faltante en la posición del cursor analizando simultáneamente código anterior y posterior.  
C. Traducir código fuente entre lenguajes antiguos y modernos.  
D. Ejecutar automáticamente pruebas de integración en sandbox.  

**Respuesta correcta: B.** (es la base del autocompletado avanzado en IDEs).

---

**Pregunta 3.** Tras implantar un asistente de IA, la métrica DORA **Change Failure Rate** aumenta significativamente. El diagnóstico arquitectónico más probable es:

A. El modelo genera código con sintaxis obsoleta que el compilador rechaza.  
B. El CAR ha caído por debajo del 10 %.  
C. Los desarrolladores sufren **sesgo de automatización**, aceptando sugerencias sintácticamente correctas pero lógicamente defectuosas sin revisar ni probar.  
D. SAST ha dejado de funcionar.  

**Respuesta correcta: C.**.

---

**Pregunta 4.** ¿Qué extensión del NIST SSDF se centra en prácticas para sistemas con IA generativa y modelos fundacionales?

A. ISO/IEC 25010.  
B. OWASP LLM01.  
C. NIST SP 800‑218A.  
D. DORA Metrics Framework.  

**Respuesta correcta: C.**.

---

**Pregunta 5.** Para evitar infracciones de propiedad intelectual (copyleft viral) al usar asistentes de codificación en la Administración, la buena práctica principal es:

A. Deshabilitar la inferencia probabilística (Temperatura = 0).  
B. Activar el filtro **Public Code Matching**, bloqueando sugerencias que coinciden con código público bajo licencias restrictivas.  
C. Subir todo código autogenerado a repositorios públicos.  
D. Desactivar integraciones IDE y usar solo interfaz web.  

**Respuesta correcta: B.**.

---

**Pregunta 6.** En el modelo de madurez de adopción de IA, la fase de “Estrategia centralizada / gobierno establecido” se caracteriza por:

A. Consumo caótico de modelos públicos (Shadow AI).  
B. Despliegue de herramientas corporativas estandarizadas, protección de datos, formación y establecimiento de métricas base.  
C. Sustitución total del 100 % de la plantilla por agentes IA.  
D. Prohibición absoluta de LLMs.  

**Respuesta correcta: B.**.

---

**Pregunta 7.** Según el framework SPACE, ¿qué dimensión justifica que asistentes de IA mejoren el rendimiento al reducir el cambio de contexto mental de ir al navegador a buscar respuestas?

A. S – Satisfaction & Well‑being.  
B. P – Performance.  
C. A – Activity.  
D. E – Efficiency & Flow.  

**Respuesta correcta: D.** (Efficiency & Flow se centra en mantener el flujo continuo en el IDE).

## Normativa o fuentes relacionadas

- **ISO/IEC 5338:2023 – AI system life cycle processes.** Referencia sobre procesos de ciclo de vida para sistemas de IA.  
- **NIST SP 800‑218 – Secure Software Development Framework (SSDF).** Marco de desarrollo seguro.  
- **NIST SP 800‑218A – Secure Software Development Practices for Generative AI and Dual‑Use Foundation Models.** Perfil específico para GenAI.  
- **OWASP AISVS – Appendix C: AI‑Assisted Secure Coding.** Estándar de verificación de seguridad para codificación asistida por IA.  
- **DORA Metrics (Accelerate).** Métricas de rendimiento de entrega (Lead Time, Deployment Frequency, Change Failure Rate, MTTR).  
- **SPACE Framework (Forsgren et al., GitHub/Microsoft).** Marco para medir productividad de desarrolladores.  
- **Real Decreto 311/2022 (ENS):** Medida `mp.sw.1` sobre desarrollo de aplicaciones y seguridad en el SDLC.  
- **Reglamento (UE) 2024/1689 – Ley de IA.** Referencias a clasificación de riesgo y gobernanza de sistemas de IA.

## Dudas o puntos pendientes

- **ROI económico y paradoja de Jevons:** No existe consenso sobre si el ahorro en tiempo se traduce en reducción de gasto; muchas organizaciones usan la productividad extra para entregar más valor, manteniendo o aumentando inversión.  
- **Modelo de madurez único:** No hay estándar ISO de madurez específico para IA en SDLC; se emplea un modelo de cinco fases basado en prácticas corporativas (IBM, etc.), por lo que el examen se centrará en la lógica progresiva más que en nombres rígidos.