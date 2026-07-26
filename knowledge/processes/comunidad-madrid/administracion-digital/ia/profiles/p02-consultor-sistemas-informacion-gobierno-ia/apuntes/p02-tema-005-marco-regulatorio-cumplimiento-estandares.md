---
id: "cm-ad-ia-p02-tema-005-marco-regulatorio-cumplimiento-estandares"
title: "Marco Regulatorio, Cumplimiento y Estándares"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/ia"
profiles:
  - "p02-consultor-sistemas-informacion-ia"
official_profile: "P02 - Consultor de Sistemas de Información - Especialista en Gobierno de IA"
official_topic: "Tema 5. Marco Regulatorio, Cumplimiento y Estándares"
source_ids: []
tags:
  - "cumplimiento"
  - "ai-act"
  - "rgpd"
  - "lopdgdd"
  - "propiedad-intelectual"
  - "iso-iec-42001"
  - "sgia"
  - "proveedores-ia"
  - "responsables-despliegue"
created_at: "2026-07-14"
last_reviewed: null
ai_generated: true
ai_sources:
  - "perplexity"
  - "chatgpt"
  - "gemini"
  - "base-apunte"
  - "eur-lex"
needs_human_review: true
---

# Marco Regulatorio, Cumplimiento y Estándares

## Encaje en la convocatoria

Este tema es el **núcleo jurídico‑técnico** del perfil **P02: Consultor de Sistemas de Información especialista en Gobierno de IA** (Tema 5 del Anexo 3 de la Resolución 352/2026).  

El tribunal exige dominio del **Reglamento (UE) 2024/1689 (Ley de IA / AI Act)**, sus niveles de riesgo, la distinción de roles (Proveedor vs Responsable del despliegue), su interacción con **RGPD/LOPDGDD**, y el papel de estándares certificables como **ISO/IEC 42001** (SGIA).

## Ideas clave

1. **AI Act – enfoque basado en riesgo:** Clasifica sistemas en cuatro niveles: riesgo inaceptable (prohibido, art. 5), alto riesgo (altamente regulado, art. 6 y anexos I/III), riesgo limitado de transparencia (art. 50) y riesgo mínimo.  
2. **Roles críticos:**  
   - **Proveedor (*provider*):** quien desarrolla y comercializa el sistema bajo su nombre, responsable de evaluación de conformidad y marcado CE.  
   - **Responsable del despliegue (*deployer*):** quien utiliza el sistema bajo su autoridad (Administración, empresa), tradicionalmente mal llamado “usuario”.  
3. **Cambio sustancial de finalidad:** Si el desplegador modifica sustancialmente un sistema, de forma que se convierte en alto riesgo, **asume obligaciones de proveedor** (incluyendo marcado CE).  
4. **Excepción de datos sensibles (art. 10.5 AI Act):** Se permite tratar categorías especiales del art. 9 RGPD de forma excepcional y temporal, sólo para detectar y corregir sesgos en sistemas de alto riesgo. 
5. **FRIA vs DPIA/EIPD:** La FRIA (art. 27 AI Act) evalúa impacto sobre derechos fundamentales; la DPIA (art. 35 RGPD) evalúa riesgos de protección de datos; son **complementarias**, no se sustituyen. 
6. **ISO/IEC 42001 (SGIA):** Norma certificable para sistemas de gestión de IA, basada en ciclo PHVA e integrada con ISO 27001; certifica la gobernanza organizativa, no un algoritmo concreto.  
7. **Modelos GPAI y propiedad intelectual:** El AI Act obliga a proveedores de modelos de uso general (GPAI) a respetar derechos de autor (TDM, opt‑out) y publicar un resumen suficientemente detallado del contenido usado para entrenamiento.

---

## 1. Reglamento Europeo de Inteligencia Artificial (AI Act – UE 2024/1689)

El AI Act se publica en el DOUE el 12 de julio de 2024 y es de aplicación directa en todos los Estados miembros como **reglamento de mercado interior, seguridad y derechos fundamentales**.

### 1.1. Fechas clave de aplicación escalonada

En examen te pueden pedir plazos y qué entra en cada fase.

- **Entrada en vigor:** agosto 2024.  
- **+ 6 meses (~febrero 2025):** aplicación de las **prácticas prohibidas** (riesgo inaceptable, art. 5).  
- **+ 12 meses (~agosto 2025):** obligaciones para **Modelos de IA de uso general (GPAI)** y régimen sancionador.  
- **+ 24 meses (~agosto 2026):** aplicación general a sistemas de alto riesgo del **Anexo III**.  
- **+ 36 meses (~agosto 2027):** sistemas de alto riesgo del **Anexo I** (componentes de seguridad de productos regulados).  

Las directrices citan además **02 de diciembre de 2027** como fecha límite para cumplimiento de obligaciones de alto riesgo según Anexo III, que aparece en preguntas de test.

### 1.2. Clasificación por niveles de riesgo

#### Riesgo inaceptable – prácticas prohibidas (art. 5)

Prohibidas salvo excepciones tasadas en biometría remota:

- Técnicas manipuladoras subliminales que causen daño.  
- Explotación de vulnerabilidades específicas de grupos (niños, personas con discapacidad).  
- **Social scoring** por autoridades públicas (puntuaciones generalizadas de comportamiento). 
- Sistemas de IA que infieran probabilidad de comisión de delitos basados únicamente en perfiles de personalidad.  
- **Identificación biométrica remota en tiempo real en espacios públicos con fines policiales**, calificada como riesgo inaceptable salvo un conjunto muy cerrado de excepciones judiciales, estrictamente necesarias y autorizadas.

#### Alto riesgo (art. 6, anexos I y III)

Incluye:

- **Anexo I:** componentes de seguridad de productos sometidos a legislación armonizada (aviación, productos sanitarios, juguetes, etc.).  
- **Anexo III:** casos de uso sensibles: biometría, infraestructuras críticas, educación, empleo, acceso a servicios esenciales, aplicación de la ley, control de migración y justicia.

**Excepción (art. 6.3):** un sistema del Anexo III no será de alto riesgo si sólo realiza tareas procedimentales limitadas o preparatorias, sin plantear riesgo de perjuicio significativo; sin embargo, la **elaboración de perfiles (profiling)** se considera siempre de alto riesgo.

#### Riesgo limitado / transparencia (art. 50)

Obligaciones específicas de transparencia:

- Informar claramente cuando se interactúa con un sistema de IA (chatbots).  
- Etiquetar contenido sintético (*deepfakes*) mediante marcas visibles y legibles por máquina.

#### Riesgo mínimo

Sistemas de riesgo mínimo (por ejemplo, IA en videojuegos) quedan sometidos a buenas prácticas voluntarias, códigos de conducta y estándares, no a obligaciones estrictas del reglamento.

---

## 2. Roles y obligaciones en la cadena de valor

### 2.1. Proveedor (provider) – art. 16

El **Proveedor** es la entidad que desarrolla o hace desarrollar un sistema de IA y lo pone en el mercado bajo su nombre o marca.

Obligaciones principales para sistemas de alto riesgo:

- Establecer un **Sistema de Gestión de Calidad** (art. 17 AI Act).  
- Elaborar la **Documentación técnica** que describa diseño, finalidad, datos, métricas y pruebas (art. 11).  
- Someter el sistema a una **Evaluación de conformidad** (art. 43), que puede incluir inspección de organismo notificado.  
- Emitir la **Declaración UE de conformidad** (art. 47) y colocar el **marcado CE** (art. 48).  
- Registrar el sistema en la base de datos europea de sistemas de IA de alto riesgo (art. 49).  
- Establecer y mantener un sistema de **seguimiento poscomercialización** (art. 72): vigilancia continua y respuesta a incidentes. 
- Conservar los **logs** generados automáticamente durante un tiempo suficiente cuando estén bajo su control.

### 2.2. Responsable del despliegue (deployer) – art. 26

El **Responsable del despliegue** (deployer) es la entidad que utiliza el sistema bajo su autoridad (por ejemplo, una consejería de la Comunidad de Madrid).

Obligaciones clave:

- Usar el sistema **conforme a las instrucciones del proveedor**, sin desviaciones no autorizadas.  
- Asegurar que existe **supervisión humana** por personas competentes y debidamente formadas, especialmente en sistemas de alto riesgo. 
- Conservar los **logs** bajo su control por **un periodo mínimo de 6 meses** (art. 26.6).  
- Realizar una **FRIA** (Evaluación de Impacto sobre Derechos Fundamentales, art. 27) antes del despliegue en organismos de Derecho público.

### 2.3. Cambio sustancial y asunción del rol de proveedor

El art. 25 regula la responsabilidad compartida en la cadena de valor.

Si el responsable del despliegue:

- Modifica un sistema de forma sustancial (por ejemplo, cambia la finalidad o altera parámetros de manera relevante), y  
- como resultado lo convierte en un sistema de alto riesgo,

entonces se le considera **Proveedor** a efectos legales y asume todas sus obligaciones (evaluación de conformidad, marcado CE, documentación técnica, etc.).

Esta situación aparece explícitamente en preguntas de examen: la respuesta correcta es que el desplegador pasa a ser proveedor cuando realiza un cambio sustancial de finalidad que lo convierte en alto riesgo.

---

## 3. Tratamiento de datos personales y propiedad intelectual

### 3.1. Intersección entre AI Act, RGPD y LOPDGDD

El AI Act y el RGPD se aplican **acumulativamente**:

- El AI Act **no** proporciona una base jurídica independiente para tratar datos personales; la legitimidad debe derivar de art. 6 RGPD (consentimiento, obligación legal, interés público, etc.). 
- El RGPD sigue regulando principios como licitud, lealtad, transparencia, minimización y responsabilidad proactiva.

**Privacidad por diseño y por defecto (art. 25 RGPD):**  
Exige que el responsable del tratamiento integre medidas técnicas y organizativas apropiadas desde el diseño de la arquitectura, y que por defecto se limite el tratamiento a datos estrictamente necesarios.

**DPIA/EIPD vs FRIA:**  
- La **DPIA** (art. 35 RGPD) evalúa alto riesgo para privacidad y libertades derivadas del tratamiento de datos personales. 
- La **FRIA** (art. 27 AI Act) evalúa impacto sobre el conjunto de derechos fundamentales (no discriminación, tutela judicial, dignidad, etc.). 
- El art. 27.4 AI Act establece que, cuando coinciden, la FRIA **complementará** a la DPIA; ninguna sustituye a la otra.

### 3.2. Excepción de datos sensibles (art. 10.5 AI Act)

Normalmente, el art. 9 RGPD prohíbe tratar categorías especiales de datos personales (origen racial, convicciones religiosas, salud, etc.), salvo supuestos específicos.

El AI Act introduce una **excepción muy tasada**:

- Para sistemas de alto riesgo, se permite tratar temporalmente estas categorías especiales con el **único propósito de detectar, prevenir o corregir sesgos**. 
- Deben aplicarse salvaguardas técnicas (seudonimización, cifrado, acceso restringido) y eliminar los datos una vez alcanzada la finalidad de corrección. 

En examen se presenta esta excepción como contraintuitiva frente a la prohibición general del RGPD.

### 3.3. Propiedad intelectual y modelos GPAI (art. 53 AI Act)

La regulación de derechos de autor en IA se apoya en la **Directiva (UE) 2019/790** sobre derechos de autor en el mercado único digital.

Obligaciones para proveedores de **Modelos de IA de Uso General (GPAI)**:

1. Establecer políticas internas para respetar derechos de autor.  
2. Respetar la **reserva de derechos (opt‑out)** frente a la minería de textos y datos (TDM), cuando titulares la ejerzan.  
3. Elaborar y publicar un **resumen suficientemente detallado** del contenido utilizado para entrenamiento del modelo GPAI.

Este resumen no exige listar cada fichero individual, pero sí describir tipos de fuentes, categorías, criterios de selección y presencia de obras protegidas.

En preguntas se resalta que esta obligación recae en proveedores de GPAI, no en cada organización usuaria.

---

## 4. Sistemas de Gestión de IA (SGIA) e ISO/IEC 42001

Un **Sistema de Gestión de IA (SGIA)** es el marco organizativo para dirigir y controlar el desarrollo, uso y operación de sistemas de IA, definiendo políticas, roles, riesgos, controles y métricas.

### 4.1. Naturaleza de ISO/IEC 42001:2023

- Es la primera norma internacional **certificable** para SGIA.  
- Es una **Norma de Sistema de Gestión (NSG)** basada en la estructura de alto nivel (HLS), compatible con ISO 27001 (seguridad) y ISO 9001 (calidad).  
- Se basa en el ciclo **PHVA (Planificar–Hacer–Verificar–Actuar)** de mejora continua.  
- No certifica que un algoritmo concreto sea “ético” o “sin sesgos”, sino que la organización dispone de procesos, controles y auditorías para gobernar responsablemente sus sistemas de IA.

Una diferencia importante frente a ISO 27001 es que ISO/IEC 42001 exige evaluar impactos **hacia individuos y sociedad**, no sólo riesgos hacia la organización, alineándose con la lógica de la FRIA.

### 4.2. Política de IA y evaluación de riesgos

Relación clave que aparece en preguntas de examen:

- La **política de IA** define objetivos, principios, criterios y **tolerancia al riesgo (risk appetite)** de la organización.  
- El proceso de **evaluación de riesgos** utiliza estos criterios como referencia para valorar si los riesgos identificados son aceptables o requieren mitigación.

Procedimiento correcto cuando un riesgo calculado supera el apetito de riesgo:

1. Implementar medidas de control para reducir su probabilidad o impacto.  
2. Recalcular el riesgo; cuando el nuevo valor esté por debajo del apetito, la organización puede decidir aceptar el riesgo residual, dejándolo documentado.

No es buena práctica “subir el apetito” sin controles, ni limitarse a transferir el riesgo mediante seguros.

### 4.3. Ciclo de vida, reutilización y mejora continua

El SGIA contempla riesgos asociados a todas las fases del ciclo de vida del sistema de IA.

- **Reutilización (Reuse):** riesgo cuando se usa el sistema en un contexto distinto al originalmente diseñado, con requisitos diferentes (por ejemplo, más precisión o otras garantías), lo que puede generar decisiones inadecuadas.  
- **Mejora continua:** la norma exige que resultados y riesgos emergentes alimenten las fases de diseño y desarrollo, actualizando controles y políticas.

---

## 5. Transparencia, golden data set y documentación (AESIA, ISO/IEC 42001)

La **Guía de Transparencia de AESIA** y el Anexo A de ISO/IEC 42001 enfatizan que la organización debe proporcionar **información apropiada** sobre el sistema de IA a las partes interesadas.

### 5.1. Principio de transparencia (AESIA)

AESIA define transparencia como:

> “La cualidad de ser interpretable y comprensible por quienes crean y utilizan el sistema a lo largo de su ciclo de vida, estrechamente ligada a las técnicas de explicabilidad e interpretabilidad”.

No implica publicar necesariamente código fuente ni todos los datos de entrenamiento, sino:

- Informar sobre capacidades, limitaciones y modos de fallo.  
- Proporcionar métricas de rendimiento (precisión, tasas de error, incertidumbre).  
- Documentar supuestos, restricciones y contextos de uso adecuado.

### 5.2. Golden data set

Las guías mencionan el **“golden data set”** como:

- Un conjunto de datos de **alta calidad, representativo y controlado** que sirve de referencia para **evaluar y validar el funcionamiento del sistema**.  
- Se usa en pruebas de regresión, comparaciones entre versiones y análisis de explicabilidad.

En examen se pregunta que no es un almacén de contraseñas ni de incidentes, sino precisamente ese conjunto de referencia de evaluación.

---

## 6. AEPD, EIPD y políticas de uso de IA generativa

Las guías de la **AEPD** sobre IA generativa y tratamiento de datos establecen:

- Es imperativo realizar o revisar una **EIPD** cuando el caso de uso entrañe **alto riesgo para los derechos y libertades** de las personas (por ejemplo, decisiones automatizadas significativas o análisis masivo de textos con datos personales).  
- La organización debe establecer políticas y herramientas para **impedir la inclusión accidental de datos personales en prompts**, por ejemplo mediante DLP, validaciones de entrada, formación y prohibiciones expresas.

En test se remarca que no basta con requerir uso de VPN; deben existir mecanismos efectivos que impidan pegado accidental de datos sensibles en prompts.

---

## 7. Comisión Europea, Oficina de IA y modelos de uso general

El AI Act crea la **Oficina de IA** dentro de la Comisión Europea con competencia exclusiva para supervisar proveedores de **modelos de uso general (GPAI)**.

Funciones clave:

- Supervisar el cumplimiento de obligaciones de transparencia, documentación y gestión de riesgos sistémicos por parte de proveedores de GPAI.  
- Coordinar autoridades nacionales competentes y publicar directrices y plantillas (por ejemplo, cuestionario tipo FRIA).

En preguntas se aclara que no son las autoridades de protección de datos ni oficinas nacionales quienes tienen esta competencia exclusiva, sino la Comisión a través de la Oficina de IA.

---

## Conceptos que suelen preguntarse

| Concepto / Distractor              | Realidad jurídico‑técnica                                                                                                  |
| :--------------------------------- | :------------------------------------------------------------------------------------------------------------------------- |
| **Usuario vs responsable despliegue** | El término “usuario” se sustituye por **Responsable del despliegue (deployer)** para la entidad que usa la IA bajo su autoridad. |
| **Cambio de finalidad sustancial** | Si el desplegador modifica sustancialmente el sistema y lo convierte en alto riesgo, asume el rol y obligaciones de **Proveedor**. |
| **FRIA vs DPIA/EIPD**              | FRIA (AI Act) evalúa derechos fundamentales; DPIA (RGPD) evalúa protección de datos; se aplican de forma **complementaria**.|
| **Datos sensibles art. 10.5**      | Tratamiento permitido de forma excepcional, temporal y con salvaguardas, sólo para detectar/corregir sesgos en alto riesgo.|
| **Marcado CE**                     | Obligación del **Proveedor** tras evaluación de conformidad; no corresponde al responsable del despliegue.      |
| **Retención de logs (deployer)**   | Periodo mínimo de **6 meses** bajo control del responsable del despliegue (art. 26.6 AI Act).        |
| **ISO/IEC 42001**                  | Norma certificable que acredita la gobernanza del SGIA de la organización, no la calidad de un modelo concreto. |
| **Golden data set**               | Conjunto de datos de alta calidad usado para validar y explicar el comportamiento del sistema, no almacén de incidentes. |
| **Oficina de IA**                 | Órgano de la Comisión con competencia exclusiva para supervisar proveedores de modelos de IA de uso general.   |

---

## Posibles preguntas tipo test

**Pregunta 1.** Según el Reglamento (UE) 2024/1689, ¿cuándo asume un responsable del despliegue las obligaciones equivalentes a las de un proveedor?

A. Cuando ejecuta el sistema en servidores on‑premises en lugar de la nube.  
B. Cuando modifica la finalidad prevista de un sistema, de forma que se convierta en un sistema de IA de alto riesgo.  
C. Cuando designa al personal de supervisión humana.  
D. Cuando el sistema procesa categorías especiales de datos personales.  

**Respuesta correcta: B.**.

---

**Pregunta 2.** ¿Cuál es el plazo mínimo durante el cual el responsable del despliegue debe conservar los archivos de registro generados automáticamente, siempre que estén bajo su control?

A. 30 días.  
B. 6 meses.  
C. 1 año.  
D. 10 años.  

**Respuesta correcta: B.** (art. 26.6 AI Act).

---

**Pregunta 3.** Si un sistema requiere tanto FRIA (art. 27 AI Act) como EIPD (art. 35 RGPD), ¿qué establece la normativa?

A. La FRIA sustituye la EIPD.  
B. La EIPD sustituye la FRIA.  
C. La FRIA complementará a la EIPD.  
D. Debe elegirse sólo una de ellas.  

**Respuesta correcta: C.** (art. 27.4 AI Act).

---

**Pregunta 4.** ¿Cuál es la naturaleza de la norma ISO/IEC 42001?

A. Guía no vinculante y no certificable.  
B. Norma de sistema de gestión certificable para establecer, implementar, mantener y mejorar un SGIA.  
C. Norma incompatible con ISO 27001.  
D. Norma que sustituye legalmente el marcado CE.  

**Respuesta correcta: B.**.

---

**Pregunta 5.** El uso de sistemas de identificación biométrica remota “en tiempo real” en espacios públicos con fines policiales se considera:

A. Riesgo de transparencia, sólo con señalización visible.  
B. Alto riesgo, permitido con marcado CE.  
C. Riesgo inaceptable sin excepciones.  
D. Riesgo inaceptable (práctica prohibida), salvo excepciones tasadas, estrictamente necesarias y sujetas a autorización judicial.  

**Respuesta correcta: D.**.

---

**Pregunta 6.** ¿Cuál de las siguientes obligaciones recae específicamente sobre proveedores de modelos de IA de uso general (GPAI)?

A. Supervisión humana directa en cada inferencia del usuario final.  
B. Elaborar y publicar un resumen suficientemente detallado del contenido usado para entrenamiento.  
C. Anonimizar obligatoriamente todos los datos de entrada en tiempo real.  
D. Realizar una FRIA antes de cada comercialización.  

**Respuesta correcta: B.**.

---

**Pregunta 7.** ¿Qué órgano tiene competencia exclusiva para supervisar proveedores de modelos de IA de uso general?

A. Banco Central Europeo.  
B. Oficinas de IA de cada Estado miembro.  
C. Comisión Europea, a través de la Oficina de IA.  
D. Autoridades nacionales de protección de datos.  

**Respuesta correcta: C.**.

---

## Normativa o fuentes relacionadas

- **Reglamento (UE) 2024/1689 (Ley de IA):** arts. 5 (prácticas prohibidas), 6 (alto riesgo), 10.5 (datos sensibles para sesgos), 16 (proveedores), 25–27 (responsabilidades y FRIA), 26.6 (logs), 50 (transparencia), 53 (GPAI), 72 (poscomercialización). 
- **Reglamento (UE) 2016/679 (RGPD):** arts. 22 (decisiones automatizadas), 25 (privacidad por diseño y por defecto), 35 (EIPD/DPIA). 
- **Ley Orgánica 3/2018 (LOPDGDD).** Aplicación nacional complementaria al RGPD.  
- **ISO/IEC 42001:2023 – Information technology — Artificial intelligence — Management system.** Estándar certificable para SGIA.  
- **Guías AEPD y AESIA** sobre IA generativa, transparencia, explicabilidad y EIPD.

## Dudas o puntos pendientes

- **Plantilla FRIA oficial:** La Oficina de IA debe publicar un cuestionario estándar para FRIA; a efectos de oposición, lo importante es el contenido mínimo descrito en el art. 27.1 AI Act. 
- **Jurisprudencia sobre titularidad de obras generadas por IA:** La LPI española exige autoría humana; aún se esperan pronunciamientos que aclaren derechos sobre prompts complejos y outputs generados, en relación con excepciones TDM.