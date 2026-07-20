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

Este tema corresponde al **Tema 7 del Anexo 3** de la Resolución 352/2026 (BOCM 11/06/2026), exclusivo para el perfil **P01 (Consultor de Sistemas de Información especialista en IA aplicada al ciclo de vida del software)** de la Agencia para la Administración Digital de la Comunidad de Madrid. 

El epígrafe oficial abarca: **implantación de la IA en el SDLC (estrategias, modelos de madurez y buenas prácticas)**, **modelos LLM específicos**, **casos de uso** e **indicadores de medición del retorno (ROI)**. 

## Ideas clave

1. **Más allá del código:** La IA impacta en todo el SDLC (requisitos, arquitectura, pruebas, seguridad, CI/CD y despliegue), no solo en la codificación. Su flujo debe ser auditado de extremo a extremo, no solo en la generación inicial.
2. **Shadow AI (IA en la sombra):** Principal riesgo en etapas tempranas. Consiste en desarrolladores enviando código corporativo o secretos a LLMs públicos (Consumer/Free tier) que utilizan esos datos para reentrenarse (Data Leakage).
3. **Enterprise Copilots y Zero Data Retention:** La implantación en el sector público exige licencias corporativas con cláusulas de "Cero Retención de Datos", donde los *prompts* y el contexto del código no alimentan el modelo base del proveedor.
4. **Filtros de Propiedad Intelectual (Public Code Matching):** Mecanismo técnico y legal indispensable para bloquear sugerencias de la IA si coinciden exactamente con código público bajo licencias restrictivas (ej. GPL), evitando el "Copyleft viral" en el software de la Administración.
5. **Fill-in-the-Middle (FIM):** Capacidad técnica diferencial de los modelos específicos de código. A diferencia de un LLM estándar que predice de forma autorregresiva hacia adelante, FIM analiza el prefijo (código antes del cursor) y el sufijo (código después del cursor) para inferir el bloque intermedio exacto.
6. **Métricas DORA y SPACE:** "Líneas de código generadas" es una métrica engañosa (*vanity metric*). El ROI real se mide a través del flujo de entrega (DORA: *Deployment Frequency, Lead Time, Change Failure Rate, Time to Restore*) y el bienestar/fricción del equipo (SPACE).
7. **Sesgo de Automatización (*Automation Bias*):** Riesgo de que los desarrolladores confíen ciegamente en el código generado (que parece sintácticamente perfecto) e introduzcan vulnerabilidades semánticas o arquitectónicas en producción. Se refleja en un aumento de la métrica *Change Failure Rate*.
8. **NIST SP 800-218A:** Extensión del Secure Software Development Framework (SSDF) con prácticas específicas para el uso de modelos fundacionales e IA generativa en el SDLC.

## Desarrollo

### 1. Implantación de la IA en la práctica del SDLC

La adopción de la IA en el desarrollo no es "encender un software", sino una transformación del sistema de ingeniería que exige estrategia, arquitectura (Platform Engineering) y políticas de seguridad.

#### 1.1. Estrategias de Implantación y Buenas Prácticas
* **ISO/IEC 5338:2023:** Norma de referencia sobre los procesos del ciclo de vida de los sistemas de IA.
* **OWASP AISVS (AI Security Verification Standard - Appendix C):** Exige que la codificación asistida por IA cubra revisiones de seguridad en todas las fases del ciclo SSDLC (*Secure* SDLC), desde el modelado de amenazas hasta el escaneo de código generado.
* **Human-in-the-loop (HITL) Obligatorio:** En ingeniería de software pública, el modelo *sugiere*, el ingeniero *acepta y se responsabiliza*. El proveedor del modelo nunca asume la responsabilidad del código en producción.

#### 1.2. Modelo de Madurez de Adopción de IA (Basado en IBM / Marcos de la Industria)
La implantación se evalúa frecuentemente mediante modelos de 5 fases:
1. **Consumir modelos genéricos (Ad-hoc / Reactivo):** Uso individual no regulado. Alto riesgo de *Shadow AI*.
2. **Proyectos piloto (Conciencia básica):** Herramientas aprobadas para casos aislados. Documentación inicial y concienciación sobre calidad/seguridad.
3. **Estrategia centralizada:** Gobierno establecido. Despliegue de asistentes corporativos (*Enterprise Copilots*) con protección de IP. Entrenamiento formal.
4. **Mejora de colaboración (Medición cuantitativa):** Toma de decisiones basada en datos. Seguimiento activo de métricas de flujo (DORA). Abordaje de *tech debt* asistido.
5. **Innovación y gobierno avanzado (Optimizado):** Integración de agentes IA autónomos en CI/CD (Agentes revisores de código, testers automáticos) operando bajo esquemas *Human-on-the-loop*. Gestión robusta y continua de riesgos.

### 2. Modelos LLM específicos para código

Un LLM generalista (ej. GPT-4 general, Claude 3 general) destaca en razonamiento, pero los LLMs específicos para código (ej. StarCoder, Code Llama, variantes de OpenAI Codex) están entrenados masivamente con repositorios (GitHub, GitLab), documentación técnica, *issues* y *pull requests*.

#### 2.1. Arquitectura de Inferencia: Fill-in-the-Middle (FIM)
Es el corazón del autocompletado en los IDE. Un modelo estándar lee de izquierda a derecha. FIM altera el preentrenamiento añadiendo tokens especiales que separan el contexto en `<PRE>` (prefijo), `<SUF>` (sufijo) y `<MID>` (medio). El modelo analiza simultáneamente lo que hay arriba y abajo del cursor para proponer una inserción precisa y coherente.

#### 2.2. Tipología de Modelos de Código
* **Modelos de Autocompletado (Baja Latencia):** Optimizados para FIM en tiempo real. Son más pequeños (ej. 1B - 7B parámetros) para garantizar latencias < 200ms.
* **Modelos Conversacionales (Chat Técnico):** Usados para refactorización o explicación. Son más pesados y ejecutan RAG interno leyendo el *workspace* del proyecto.
* **Modelos de Embeddings de Código:** No generan código; convierten fragmentos (funciones, clases) en vectores densos para búsqueda semántica masiva en repositorios corporativos y detección de código duplicado.

### 3. Casos de uso a lo largo del SDLC

La IA asiste en todas las fases tradicionales:

* **Requisitos y Análisis:** Generación de Historias de Usuario estructuradas (formato *Given-When-Then* / Gherkin) para TDD/BDD. Detección de ambigüedades.
* **Diseño y Arquitectura:** Generación de diagramas a partir de texto (*Diagram-as-Code* mediante Mermaid/PlantUML). Propuestas de ADRs (*Architecture Decision Records*).
* **Codificación:** * Generación de *Boilerplate* (código estructural repetitivo).
  * Explicación de Código (*Code Explanation*), vital para modernizar sistemas legados sin documentación.
  * Traducción entre lenguajes (ej. COBOL/Java 8 a Java 21 moderno).
* **Pruebas (Testing):** Generación de *mocks*, pruebas unitarias y casos extremos (*Edge Cases*). **Atención:** La IA redacta el código del test, pero *no lo ejecuta*; la ejecución ocurre en el motor del CI/CD.
* **Seguridad (DevSecOps):** SAST + IA. Los analizadores estáticos tradicionales levantan alertas; la IA generativa contextualiza el hallazgo de la vulnerabilidad y propone el parche de código exacto (remediación automática).
* **CI/CD y Operación:** Generación de pipelines YAML, explicación de *builds* fallidos, y análisis rápido de *logs* para redactar *Post-Mortems* de incidentes (RCA).

### 4. Indicadores de medición del retorno (ROI)

El mayor error estratégico es medir el éxito por el "volumen de código generado". Un exceso de código generado por IA sin rigor aumenta la deuda técnica y los costes de mantenimiento a largo plazo. 

#### 4.1. Métricas de Interacción y Adopción (Operativas)
* **CAR (Code Acceptance Rate):** Porcentaje de sugerencias autogeneradas que el desarrollador acepta y mantiene sin borrar (suele oscilar entre el 25% y 40% en equipos consolidados).

#### 4.2. Métricas DORA (Métricas de Flujo y Entrega)
Estándar del sector para medir el rendimiento de DevOps, aplicable para ver si la IA realmente acelera el valor o genera cuellos de botella:
1. **Deployment Frequency (Frecuencia de Despliegue):** ¿Permite la IA integrar y desplegar más a menudo?
2. **Lead Time for Changes (Tiempo de Entrega de Cambios):** ¿Reduce la IA el tiempo desde el *commit* hasta la producción?
3. **Change Failure Rate (Tasa de Fallo en Cambios):** **Métrica Crítica.** Si la IA introduce código aparentemente correcto pero con errores lógicos (Sesgo de automatización), esta tasa aumentará. Debe mantenerse baja.
4. **Time to Restore Service (MTTR):** ¿Ayuda la IA a diagnosticar *logs* y resolver incidentes más rápido?

#### 4.3. Framework SPACE (Métricas de Experiencia)
Desarrollado por GitHub y Microsoft Research, mide dimensiones de productividad que van más allá del código crudo:
* **S (Satisfaction & Well-being):** La IA reduce el agotamiento al hacer las tareas repetitivas.
* **P (Performance):** Calidad y fiabilidad del software.
* **A (Activity):** Commits, Pull Requests, despliegues (métricas crudas).
* **C (Communication & Collaboration):** Ayuda en revisiones de código y *Pull Requests* asistidas.
* **E (Efficiency & Flow):** La IA permite al desarrollador mantenerse en estado de "flujo" en el IDE, reduciendo drásticamente la fricción y el cambio de contexto (*Context Switching*) de ir al navegador a buscar respuestas.

#### 4.4. Cálculo General del ROI
`ROI = (Ahorro Tiempo/Defectos/Retrabajo - Costes Totales) / Costes Totales`
*Costes totales* incluye: Licencias, tokens consumidos, infraestructura RAG corporativa, formación, revisiones de seguridad adicionales y gestión del cambio.

## Conceptos que suelen preguntarse

| Concepto | Realidad Técnica / Normativa | Distractor típico en examen |
| :--- | :--- | :--- |
| **Shadow AI** | Uso de IA pública no autorizada. Riesgo de fuga de PII y Propiedad Intelectual. | "Es una técnica de despliegue oscuro (Shadow Deployment)". |
| **FIM (Fill-in-the-Middle)** | Analiza contexto previo y posterior al cursor para insertar código en medio. | "Es un modelo que solo entiende el código de arriba a abajo". |
| **Métricas de Productividad** | DORA (Flujo) y SPACE (Experiencia y fricción). | "Líneas de código (LOC) generadas al día es la mejor métrica". |
| **NIST SP 800-218A** | Perfil del SSDF específico para integrar y desarrollar sistemas con IA Generativa. | "Es una ley europea que prohíbe el uso de IA en software crítico". |
| **Sesgo de Automatización** | Aceptación ciega de sugerencias plausibles pero erróneas. Sube el *Change Fail Rate*. | "Es un bug interno del modelo de Machine Learning". |
| **Public Code Matching** | Filtro corporativo para evitar copiar código bajo licencias restrictivas (GPL). | "Es un buscador para descargar librerías Open Source". |
| **CAR (Code Acceptance Rate)** | Porcentaje de sugerencias de código de la IA que el desarrollador acepta. | "Mide cuántos usuarios instalan la extensión en su IDE". |

## Posibles preguntas tipo test

**Pregunta 1.** Según los modelos de medición de productividad en ingeniería de software como DORA y SPACE, ¿cuál es el principal riesgo operativo de utilizar como KPI principal "el volumen total de líneas de código generadas por IA al día"?
A. Provoca latencia excesiva en la conexión de red del IDE.
B. Es una "métrica de vanidad" que puede enmascarar la introducción masiva de deuda técnica, vulnerabilidades y aumento de los costes de mantenimiento.
C. Las licencias corporativas cobran exclusivamente por línea de código, agotando el presupuesto de forma exponencial.
D. Afecta al modelo FIM (Fill-in-the-Middle) reduciendo su temperatura algorítmica.
**Respuesta correcta: B.** (El volumen de código aislado no aporta valor y puede degradar gravemente la calidad del sistema).

**Pregunta 2.** En la aplicación de Modelos de Lenguaje de Gran Escala (LLMs) especializados en asistencia a la programación, la capacidad técnica denominada FIM (*Fill-in-the-Middle*) permite:
A. Reentrenar dinámicamente el modelo fundacional con los últimos commits en tiempo de ejecución.
B. Predecir y generar el código faltante en la posición del cursor analizando simultáneamente el código que lo precede y el que lo sucede.
C. Traducir código fuente de un lenguaje antiguo a uno moderno utilizando integración continua.
D. Ejecutar automáticamente las pruebas de integración en entornos aislados de Sandbox.
**Respuesta correcta: B.** (La inferencia bidireccional prefijo-sufijo es la base del autocompletado en el IDE).

**Pregunta 3.** La Agencia para la Administración Digital implanta un asistente de IA para desarrolladores. Tras tres meses, los cuadros de mando indican que la métrica DORA denominada 'Tasa de Fallo en Cambios' (*Change Failure Rate*) ha aumentado significativamente. El diagnóstico arquitectónico más probable, relacionado con los riesgos humanos en IA, es:
A. Los desarrolladores están sufriendo el "Sesgo de automatización" (*Automation Bias*), aceptando sugerencias sintácticamente perfectas pero lógicamente defectuosas sin la debida revisión manual ni pruebas.
B. El modelo de IA está generando código con sintaxis obsoleta que el compilador rechaza automáticamente, bloqueando la *build*.
C. El *Code Acceptance Rate* (CAR) ha caído por debajo del 10%.
D. El análisis estático de seguridad (SAST) ha dejado de funcionar al no soportar IA generativa.
**Respuesta correcta: A.**

**Pregunta 4.** El marco de mejores prácticas NIST SP 800-218 (SSDF) cuenta con una extensión oficial específica destinada a gobernar el desarrollo de software y sistemas que integran modelos fundacionales y de IA Generativa. Esta extensión es la:
A. ISO/IEC 25010.
B. OWASP Top 10 LLM01.
C. NIST SP 800-218A.
D. DORA Metrics Framework.
**Respuesta correcta: C.** (El SP 800-218A es el *Community Profile* del SSDF centrado en GenAI).

**Pregunta 5.** Para evitar infracciones de propiedad intelectual (ej. la incorporación involuntaria de código sujeto a licencias restrictivas tipo GPL o "Copyleft" en software propietario de la Administración), la buena práctica principal al configurar un asistente de codificación empresarial es:
A. Activar el filtro de bloqueo de coincidencias de código público (*Public Code Matching*), que impide la sugerencia si el fragmento coincide exactamente con código existente en repositorios *open source*.
B. Deshabilitar la inferencia probabilística forzando Temperatura = 0.
C. Exigir que todo el código autogenerado se suba obligatoriamente a repositorios públicos.
D. Desactivar las integraciones del IDE y utilizar el asistente únicamente vía interfaz web.
**Respuesta correcta: A.** (La protección frente al copyleft viral es una exigencia legal básica en SDLC corporativo).

**Pregunta 6.** Según el modelo general de madurez de adopción de IA generativa (propuesto por IBM y aplicable al ciclo de vida de desarrollo), la fase de "Estrategia Centralizada" o "Gobierno establecido" se caracteriza por superar los pilotos aislados para implementar:
A. Consumo caótico de modelos genéricos públicos (*Shadow AI*) por parte de individuos.
B. El despliegue de herramientas estandarizadas corporativas, protección de datos, entrenamiento organizativo y establecimiento de métricas bases.
C. La sustitución total del 100% de la plantilla de desarrollo por agentes IA.
D. La prohibición absoluta de los LLMs.
**Respuesta correcta: B.** (Corresponde a la Fase 3, donde la organización controla y homogeneiza la adopción).

**Pregunta 7.** Según el *framework* de medición de productividad SPACE (utilizado para evaluar el impacto de la IA), ¿qué dimensión justifica que los asistentes de IA mejoren el rendimiento al reducir el "cambio de contexto mental" (*Context Switching*) de ir a buscar respuestas a un navegador web?
A. S (Satisfaction and well-being).
B. P (Performance).
C. A (Activity).
D. E (Efficiency and flow).
**Respuesta correcta: D.** (El "Flujo" o *Flow* mide la capacidad del programador de mantenerse centrado y eficiente en el IDE sin interrupciones).

## Normativa o fuentes relacionadas

* **ISO/IEC 5338:2023:** *Information technology — Artificial intelligence — AI system life cycle processes.*
* **NIST SP 800-218:** *Secure Software Development Framework (SSDF).*
* **NIST SP 800-218A:** *Secure Software Development Practices for Generative AI and Dual-Use Foundation Models.* (Ampliación esencial para este tema).
* **OWASP AISVS (AI Security Verification Standard):** *Appendix C: AI-Assisted Secure Coding*. Cubre todo el ciclo SSDLC, diseño, implementación, pruebas y monitorización para IA.
* **DORA (DevOps Research and Assessment) Metrics:** Marco de la industria (Google/Accelerate) estandarizado para evaluar la entrega de software (Lead Time, Deployment Frequency, Change Failure Rate, Time to Restore).
* **SPACE Framework:** *The SPACE of Developer Productivity* (Forsgren et al., GitHub/Microsoft Research). Define dimensiones cualitativas y cuantitativas.
* **Real Decreto 311/2022 (Esquema Nacional de Seguridad):** Especialmente la medida `mp.sw.1` (Desarrollo de aplicaciones), que exige separación de entornos y metodología de desarrollo seguro, aplicables a la generación por IA.
* **Reglamento (UE) 2024/1689 (Ley de IA):** Marco de riesgo. Un copiloto de código no es inherentemente un sistema de "Alto Riesgo" de forma automática, dependerá de su finalidad concreta en la Administración.

## Dudas o puntos pendientes

* **Cuantificación económica exacta del ROI (Paradoja de Jevons):** Existe un debate no resuelto en la industria sobre si la reducción de tiempos de desarrollo mediante IA (medido con DORA/SPACE) se traduce en reducción de presupuestos. A menudo ocurre la Paradoja de Jevons: al ser más barato y rápido generar código, la demanda de software y funcionalidades aumenta, por lo que el gasto global de la organización en desarrollo se mantiene igual o sube, invirtiéndose en "más valor entregado" en lugar de ahorro neto en nóminas.
* **Modelos de Madurez:** No existe un único modelo de madurez estandarizado a nivel ISO para la IA en el SDLC. En este apunte se ha integrado el modelo progresivo de 5 fases de IBM, que es el *framework* más estructurado disponible en la literatura técnica corporativa consolidada. En el examen, estas fases se evaluarán desde el sentido común progresivo: Ad-hoc $\rightarrow$ Piloto $\rightarrow$ Centralización/Gobierno $\rightarrow$ Medición Cuantitativa $\rightarrow$ Optimización/Agentes.
