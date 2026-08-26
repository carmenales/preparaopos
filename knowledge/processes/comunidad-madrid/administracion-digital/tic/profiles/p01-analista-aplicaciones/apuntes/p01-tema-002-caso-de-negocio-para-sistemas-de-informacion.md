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
  - "five-case-model"
created_at: "2026-08-09"
last_reviewed: "2026-08-10"
ai_generated: true
ai_sources:
  - "chatgpt"
  - "gemini"
  - "perplexity"
needs_human_review: false
---

# Tema 2. Caso de negocio para sistemas de información

## 1. PRINCE2

PRINCE2 (*Projects IN Controlled Environments*) es una **metodología estructurada para la gestión de proyectos centrada en la organización, el control y la calidad** del proceso. Es decir, es un método estructurado para la gestión de proyectos de **enfoque predictivo**.

Se trata de un estándar reconocido internacionalmente que proporciona un marco claro para gestionar proyectos de cualquier tamaño o sector, dividiéndolos en fases manejables y bien definidas.

Está desarrollado y mantenido actualmente por PeopleCert (anteriormente por AXELOS y, en sus orígenes, por la OGC - *Office of Government Commerce* del gobierno británico). Es el estándar de facto en gestión de proyectos en el Reino Unido y países de influencia anglosajona, conviviendo en las Administraciones Públicas con marcos como el PMBOK o normativas como la ISO 21502:2020.

PRINCE2 proporciona principios, procesos y temáticas (denominadas prácticas en su versión 7) que guían la planificación, ejecución y control de proyectos. Se caracteriza por su énfasis en la justificación continua del negocio, la gestión por excepción y una estructura clara de roles y responsabilidades.

Tiene su origen en el modelo PROMPT, desarrollado en 1975 por la CCTA (*Central Computer and Telecommunications Agency*). La evolución de ese modelo tomó en 1989 el nombre de PRINCE y en 1996 se actualizó a PRINCE2. La CCTA se integró posteriormente en la OGC, que en 2013 cedió el desarrollo de PRINCE2 a AXELOS, hasta su actual gestión por PeopleCert.

### 1.1. Metodología PRINCE2 (Versión 7)

En el ámbito de la gestión de proyectos, PRINCE2 se posiciona como una de las metodologías más completas y estructuradas. Se basa en una matriz de **siete principios, siete prácticas (antiguos temas) y siete procesos** que guían el desarrollo del proyecto de principio a fin.

#### 1.1.1. Los 7 Principios
Son las obligaciones universales que todo proyecto debe cumplir inexcusablemente para considerarse gestionado bajo PRINCE2:

1. **Justificación comercial continua:** el proyecto debe aportar valor, tener una necesidad documentada y seguir siendo viable en todo momento.
2. **Aprender de la experiencia:** se identifican, registran y aplican lecciones de proyectos anteriores y del propio proyecto en curso.
3. **Roles y responsabilidades definidos:** estructura organizativa explícita que representa los intereses del negocio, del usuario y del proveedor.
4. **Gestión por fases:** el proyecto se planifica, supervisa y controla etapa por etapa.
5. **Gestión por excepción:** delegación de autoridad estableciendo límites (tolerancias) de tiempo, coste, calidad, alcance, beneficios y riesgo, para escalar decisiones solo cuando sea necesario.
6. **Enfoque en los productos:** se priorizan los entregables (outputs) y sus requisitos de calidad claros.
7. **Adaptación al entorno del proyecto** (*Tailoring*): la metodología se ajusta según la complejidad, escala, riesgo o entorno normativo del proyecto.

#### 1.1.2. Las 7 Prácticas (Antiguos "Temas" en v6)
Son los aspectos de gestión transversales que deben supervisarse continuamente:

1. **Business case (Caso de negocio):** analiza si el proyecto sigue siendo rentable y necesario.
2. **Organización:** define la estructura, las responsabilidades y la toma de decisiones.
3. **Calidad:** asegura que los resultados son aptos para el propósito y cumplen los requisitos.
4. **Planes:** organiza el "cómo", "cuándo", "cuánto" (tiempos, recursos, costes y entregables).
5. **Riesgo:** gestiona la incertidumbre (identifica amenazas y oportunidades).
6. **Cuestiones** (*Issues*, sustituye a "Cambio" de v6): gestiona modificaciones en el alcance, eventos no planificados o problemas que requieran intervención.
7. **Progreso:** controla el avance real frente a las líneas base aprobadas.

#### 1.1.3. Los 7 Procesos
Describen la progresión cronológica y el ciclo de vida del proyecto (es crucial dominar sus siglas oficiales en inglés):

1. **Puesta en marcha del proyecto** (SU - *Starting up a Project*): filtro previo para evaluar si merece la pena iniciarlo, evitando invertir en ideas inviables.
2. **Dirección del proyecto** (DP - *Directing a Project*): proceso continuo donde la Junta de Proyecto (*Project Board*) ejerce el gobierno y la toma de decisiones clave.
3. **Inicio del proyecto** (IP - *Initiating a Project*): establecimiento de las bases sólidas y planificación detallada.
4. **Control de una fase** (CS - *Controlling a Stage*): seguimiento operativo del trabajo diario por parte del Jefe de Proyecto.
5. **Gestión de entrega de productos** (MP - *Managing Product Delivery*): vínculo entre el Jefe de Proyecto y los Jefes de Equipo; es la ejecución técnica y coordinación de entregables.
6. **Gestión de los límites de fase** (SB - *Managing a Stage Boundary*): evaluación del final de una fase y planificación de la siguiente (incluye actualizar el Business Case).
7. **Cierre del proyecto** (CP - *Closing a Project*): desmantelamiento controlado, validación final, entrega y extracción de lecciones aprendidas.

### 1.2. Casos de negocio en el ámbito de los sistemas de información (PRINCE2)

En el ámbito de la gestión de proyectos, el **Caso de Negocio (Business Case)** es el motor que impulsa el proyecto. No se trata de un documento estático que se escribe al principio y se olvida, sino de una herramienta dinámica de gestión.

La metodología PRINCE2 se fundamenta en el principio de **Justificación Comercial Continua**. Esto significa que un proyecto para implementar o modificar un sistema de información solo debe iniciarse, y continuar, si existe una necesidad de negocio clara, unos beneficios cuantificables que superan a los costes, y unos riesgos aceptables. Este principio exige que la justificación se mantenga durante todo el proyecto y que las decisiones de continuación se apoyen en información actualizada. 

Si la justificación deja de ser válida —por ejemplo, porque cambia la normativa aplicable, las prioridades estratégicas, la tecnología disponible, los costes se disparan o los beneficios desaparecen— la organización debe disponer de información suficiente para decidir si modifica el proyecto o lo detiene inmediatamente.

PRINCE2 define la gestión del **Business Case** mediante una **técnica de cuatro pasos**:

1.  **Desarrollar** (*Develop*): explorar opciones y reunir la información necesaria para la decisión de inversión. Se desarrolla por primera vez en la fase de preproyecto (proceso *SU*) como un **Caso de Negocio Preliminar** (*Outline Business Case*), y se completa durante la fase de inicio (proceso *IP*) hasta convertirse en el **Caso de Negocio Detallado** (*Detailed Business Case*).
2.  **Verificar** (*Check*): evaluar si el proyecto sigue mereciendo la pena antes de cada autorización importante (generalmente en los límites de fase, proceso *SB*).
3.  **Mantener** (*Maintain*): el Jefe de Proyecto actualiza el Caso de Negocio con el progreso real, costes incurridos y previsiones vigentes.
4.  **Confirmar** (*Confirm*): valorar si los beneficios previstos se han conseguido. Comienza durante el proyecto y ocurre principalmente después del cierre del proyecto (*Post-project Benefits Review*).

**PRINCE2 7** incorpora además dos focos que resultan especialmente relevantes para el análisis de sistemas de información en las Administraciones Públicas: 
*   La **sostenibilidad** como aspecto del desempeño del proyecto (consumo energético de infraestructuras, *Green IT*, gestión de residuos electrónicos).
*   Un enfoque explícito sobre **gestión digital y de datos** (calidad, gobernanza de los datos, soberanía, interoperabilidad y seguridad de la información). Ambos elementos condicionan la viabilidad y deben incluir el coste de cumplimiento de normativas de obligado cumplimiento como el **Esquema Nacional de Seguridad (ENS - RD 311/2022)** y el **RGPD (UE 2016/679)** (Auditorías, arquitectura de alta disponibilidad, EIPD, cifrado).

## 2. Utilidad del Business Case

El **Business Case** tiene múltiples utilidades prácticas y de gobierno dentro de la Administración y la empresa privada:

*   **Toma de decisiones (Go / No-Go):** Es la base sobre la cual el Comité de Dirección (o *Project Board* en PRINCE2) decide si autoriza el inicio del proyecto, si aprueba el paso a la siguiente fase, o si cancela la iniciativa.
*   **Alineación Estratégica:** Garantiza que el sistema de información está alineado con los objetivos estratégicos (*por ejemplo, el Plan de Digitalización de las AAPP o la Estrategia Nacional de Inteligencia Artificial*).
*   **Gestión de Expectativas:** Define claramente qué valor se va a entregar, evitando que el proyecto se convierta en un fin técnico en sí mismo.
*   **Línea base para la evaluación final:** Al cerrar el proyecto, se utiliza para evaluar si el sistema entregado realmente ha generado el valor prometido.

En el proceso **Dirigir un Proyecto (DP)**, el *Project Board* debe confirmar expresamente que existe un Business Case adecuado y que están establecidos los mecanismos para medir los beneficios. Esto convierte al Business Case en el **documento habilitante** de cada gran decisión de gobierno del proyecto.

## 3. Criterios

Para que un **Caso de Negocio** sea **válido** y **autorizable**, debe demostrar que la iniciativa es:

*   **Deseable:** El balance económico y estratégico (beneficios frente a costes y riesgos) es positivo.
*   **Viable:** La solución técnica es factible de construir e integrar en la infraestructura tecnológica existente.
*   **Alcanzable:** La organización tiene la capacidad (recursos, presupuesto, competencias y mercado de proveedores) para entregar los productos que generarán los beneficios.

### 3.1. Perspectiva Financiera (Matemática de la Inversión)

Desde el punto de vista financiero, los criterios se apoyan en técnicas de evaluación de inversiones que conforman la sección de **Análisis de Inversión** (*Investment Appraisal*):

*   **ROI (Retorno de la Inversión):** Mide el porcentaje de rentabilidad respecto al capital invertido. *(Fórmula: [Beneficios Netos / Costes de Inversión] x 100)*.
*   **Payback (Plazo de Recuperación):** Tiempo exacto necesario para que los ahorros o flujos de caja positivos acumulados igualen a la inversión inicial.
*   **VAN (Valor Actual Neto o NPV):** Consiste en traer todos los flujos de caja futuros (ingresos y gastos) al momento presente, descontándolos mediante una tasa (coste de capital o inflación). Si **VAN > 0**, el proyecto es financieramente **rentable**.
*   **TIR (Tasa Interna de Retorno o IRR):** Es la tasa de descuento exacta que hace que el VAN de un proyecto sea igual a cero. Mide la rentabilidad intrínseca.

> **Nota técnica:** El **VAN** y el **TIR** incorporan el **valor temporal del dinero** (descuentan flujos de caja futuros). Mientras que el **ROI** simple y el **Payback** básico no lo hacen, ofreciendo una visión menos precisa en proyectos plurianuales.

### 3.2. Evaluación en el Sector Público (El "Five Case Model")

En el sector público, la evaluación no puede reducirse a la rentabilidad financiera privada. Debe considerarse el **valor público** (reducción de cargas administrativas, mejora de la transparencia, interoperabilidad, cumplimiento normativo). 

En el ámbito anglosajón, esto se articula mediante el **Five Case Model** de **HM Treasury** (recogido en el *Green Book*), un marco compuesto por cinco dimensiones que se adaptan perfectamente a la evaluación de inversiones en las AAPP españolas:

1.  **Strategic Case (Caso Estratégico):** justificación y objetivos de la intervención y su encaje con la estrategia normativa de la organización.
2.  **Economic Case (Caso Económico):** análisis de una relación de alternativas (longlist/shortlist) para determinar la opción que ofrece mejor relación calidad-precio (*Value for Money*) para la sociedad.
3.  **Commercial Case (Caso Comercial):** viabilidad comercial, estrategia de contratación y viabilidad de licitación (en España, enmarcado en la **Ley 9/2017, de Contratos del Sector Público - LCSP**).
4.  **Financial Case (Caso Financiero):** asequibilidad de la propuesta y existencia de crédito en la partida presupuestaria del organismo público.
5.  **Management Case (Caso de Gestión):** capacidad metodológica (ej. PRINCE2), recursos y mecanismos para ejecutar y evaluar la propuesta.

> El **Five Case Model** avanza por etapas de maduración equivalentes a PRINCE2: **Strategic Outline Case (SOC)**, **Outline Business Case (OBC)** y **Full Business Case (FBC)** (equivalente al Business Case Detallado).

## 4. Contenido Típico

Según el estándar **PRINCE2**, un esquema de **Business Case** formal contiene los siguientes apartados:

| Sección | Descripción Técnica |
| :--- | :--- |
| **Resumen Ejecutivo** | Visión general para la alta dirección (decisión solicitada, coste total, TIR/VAN y riesgos críticos). |
| **Razones (Motivos)** | El problema u oportunidad (ej. normativo, operativo) que justifica **por qué se necesita el proyecto**. |
| **Opciones de Negocio** | Alternativas evaluadas. PRINCE2 exige al menos 3:<br>-*No hacer nada* (línea base).<br>-*Hacer lo mínimo* (cumplimiento normativo estricto).<br>-*Hacer algo* (opción recomendada). |
| **Beneficios Esperados** | Mejoras cuantificables y medibles resultantes del proyecto con sus **tolerancias** definidas. |
| **Disbeneficios** | **Resultados medibles percibidos como negativos** por uno o más interesados (ej. curva de aprendizaje o carga de trabajo extra durante una migración). |
| **Plazos (Timescale)** | Cronograma macro: cuándo comenzará, finalizará y cuándo se materializarán los beneficios. |
| **Costes** | Presupuesto extraído del Plan del Proyecto. Debe incluir el **TCO (Total Cost of Ownership)**: licitación, desarrollo, licencias, operación, mantenimiento y retiro. |
| **Análisis de Inversión** | Comparativa detallada entre costes (TCO) y beneficios a lo largo del tiempo (VAN, TIR, Payback). |
| **Riesgos Principales** | Amenazas y oportunidades que podrían alterar la viabilidad del documento. |

Para interpretar correctamente las secciones de **Beneficios** y **Disbeneficios**, es crítico distinguir en un sistema de información la siguiente cadena de valor: 
- El **producto (output):** elemento tangible o intangible que el proyecto entrega (ej. Plataforma de tramitación electrónica desplegada).
- El **resultado (outcome):** el cambio que se produce al utilizar el producto (ej. Los procedimientos pasan a tramitarse 100% online).
- El **beneficio (benefit):** la mejora medible que se obtiene (ej. Reducción del tiempo medio de resolución en un 30%).
- El **disbeneficio:** consecuencia medible, cierta y negativa del cambio (no confundir con **riesgo**, que es un acontecimiento incierto).

Junto al Business Case, PRINCE2 exige el **Plan de Revisión de Beneficios** (*Benefits Review Plan* en v6, actualizado a *Benefits Management Approach* en v7). Este plan define qué KPIs se medirán, la línea base (situación de partida), la meta, el responsable y el momento de las revisiones (durante y, sobre todo, tras el cierre del proyecto).

## 5. Responsabilidades

La gobernanza del Business Case exige una estricta segregación de roles:

*   **Ejecutivo** (*Executive*): Es el **dueño y responsable final** del Business Case. Pertenece al *Project Board* y su misión es asegurar que el proyecto aporta valor por el dinero invertido (*Value for Money*).
*   **Usuario Principal** (*Senior User*): Representa a quienes usarán la solución. Es responsable de **especificar los beneficios esperados** y, posteriormente, **rendir cuentas** para demostrar que dichos beneficios se han hecho realidad tras la entrega.
*   **Proveedor Principal** (*Senior Supplier*): Representa a quienes construyen el sistema. Responsable de proporcionar las **estimaciones fidedignas de coste, tiempo técnico y riesgos de arquitectura** para alimentar el análisis de inversión.
*   **Jefe de Proyecto** (*Project Manager*): Carece de autoridad ejecutiva. Es quien **prepara, redacta, mantiene y actualiza** el documento delegadamente, recopilando la información del equipo.
*   **Aseguramiento del Proyecto** (*Project Assurance*): Rol delegado por el *Project Board*. Tiene la función de **verificar, auditar y monitorizar de forma independiente** que el Caso de Negocio sigue siendo válido frente a eventos externos y al progreso real, comprobando la alineación estratégica. No son los autores del documento.

> **Matiz clave para exámenes:** El Ejecutivo es propietario; el Jefe de Proyecto redacta; el Project Assurance audita de forma independiente.

## 6. Relación con el Plan del Proyecto

El Caso de Negocio y el Plan del Proyecto mantienen una relación de **dependencia bidireccional y evolución paralela** (*el Caso justifica el Plan; el Plan cuantifica el Caso*).

En el proceso de **Iniciar un Proyecto (IP)**, el Caso de Negocio Preliminar se actualiza a **Caso de Negocio Detallado** incorporando tres insumos procedentes de los productos de gestión: 
1. Los **costes y plazos** calculados en el Plan de Proyecto.
2. Los **riesgos principales** identificados en el Registro de Riesgos.
3. Los **beneficios y tolerancias** alineados con el Plan de Revisión de Beneficios. 

Durante la ejecución (*Controlar una fase*), si el Jefe de Proyecto prevé superar las tolerancias (ej. un sobrecoste del 20%), emitirá un *Informe de Excepción*. El *Project Board* deberá actualizar el Caso de Negocio con estos nuevos datos para decidir si, financieramente, el proyecto debe continuar o clausurarse.

## 7. Terminología PRINCE2 6 frente a PRINCE2 7

Dado que la bibliografía y tribunales pueden mezclar terminología, la correspondencia exacta es:

| PRINCE2 6 | PRINCE2 7 (Actual) |
| :--- | :--- |
| Temas (*Themes*) | Prácticas (*Practices*) |
| Tema Business Case | Práctica Business Case |
| Tema Cambio (*Change*) | Práctica Cuestiones (*Issues*) |
| Enfoque documental estricto | Mayor flexibilidad y adaptación (*Tailoring*) |
| Sin foco explícito en sostenibilidad | Sostenibilidad como pilar de desempeño |
| Sin foco explícito en datos | Enfoque explícito en gestión digital y de datos |

## 8. PRINCE2 vs otras metodologías

| Metodología | Enfoque principal | Nivel de flexibilidad | Uso habitual en AAPP |
| :--- | :--- | :--- | :--- |
| **PRINCE2** | Procesos estructurados, gobierno corporativo y control de viabilidad | Medio (requiere *tailoring*) | Proyectos tractores, grandes licitaciones y despliegues estructurales |
| **Agile (Scrum / Kanban)** | Iteraciones rápidas, entrega de valor continuo y adaptación | Alto | Desarrollo de software a medida, entornos de alta incertidumbre |
| **PMBOK / ISO 21502** | Guía de fundamentos y buenas prácticas técnicas | Variable | Base de conocimiento de referencia técnica y organizativa |

## 9. Resumen

| Concepto | Palabra Chivata en el Test |
| :--- | :--- |
| **Caso de Negocio** | "Justificación comercial", "Evaluar viabilidad", "Causa raíz del proyecto". |
| **Principio rector** | "Justificación comercial continua", "Revisión en los límites de fase". |
| **Práctica (PRINCE2 7) / Tema (PRINCE2 6)** | Business Case es una práctica en PRINCE2 7 y era un tema en PRINCE2 6. |
| **4 pasos de gestión del Business Case** | "Desarrollar, Verificar, Mantener, Confirmar". |
| **Outline vs. Detailed Business Case** | Outline = "preproyecto, estimaciones generales"; Detailed = "fase de inicio, datos del Plan de Proyecto". |
| **Plan de Revisión de Beneficios (BRP)** | "Define cuándo y cómo se medirán los beneficios", "Se actualiza al final de cada fase". |
| **Producto / Resultado / Beneficio** | Producto = "lo que se entrega"; Resultado = "el cambio"; Beneficio = "la mejora medible". |
| **Disbeneficios** | "Consecuencia negativa medible y esperada", distinta de un riesgo (incierto). |
| **Ejecutivo (Executive)** | "Propietario del Business Case", "Asegura el Value for Money", "Responsable final". |
| **Jefe de Proyecto (PM)** | "Redacta", "Actualiza", "Mantiene". |
| **Usuario Principal** | "Identifica y especifica beneficios", "Rinde cuentas de los beneficios". |
| **Project Assurance** | "Verifica de forma independiente", "No es el autor ni el propietario", "Comprueba alineación estratégica". |
| **Opciones básicas** | "No hacer nada, Hacer lo mínimo, Hacer algo". |
| **Five Case Model (HM Treasury)** | "Strategic, Economic, Commercial, Financial, Management Case", marco del sector público británico. |

## 10 Simulacro de Test

**Pregunta 1:**
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

**Pregunta 2:**
*Según la técnica PRINCE2 de gestión del Caso de Negocio en cuatro pasos, ¿en qué paso se evalúa si los beneficios previstos se han conseguido realmente, comprobación que ocurre principalmente después del cierre del proyecto?*
a) Desarrollar (Develop).
b) Verificar (Check).
c) Mantener (Maintain).
d) Confirmar (Confirm).

**Razonamiento Estructurado:**
1.  "Desarrollar" (A) ocurre al principio, explorando opciones. "Verificar" (B) se hace antes de cada autorización importante, para decidir si el proyecto sigue mereciendo la pena. "Mantener" (C) consiste en actualizar el documento con el progreso real durante la ejecución.
2.  El enunciado describe exactamente la comprobación de si los beneficios se han materializado, lo cual ocurre sobre todo tras el cierre del proyecto: esa es la definición literal del paso "Confirmar".
3.  **Respuesta correcta:** D.

**Pregunta 3:**
*Durante el proceso de Iniciar un Proyecto en PRINCE2, el Jefe de Proyecto actualiza el Caso de Negocio Preliminar para convertirlo en el Caso de Negocio Detallado. ¿De qué producto de gestión obtiene los datos de costes y plazos necesarios para esta actualización?*
a) Del Registro de Riesgos.
b) Del Plan de Proyecto.
c) Del Informe de Excepción.
d) Del Registro de Interesados.

**Razonamiento Estructurado:**
1.  El Registro de Riesgos (A) aporta los riesgos principales, no los costes ni plazos. El Informe de Excepción (C) solo se genera si se prevé superar una tolerancia, no es un insumo estándar del Caso de Negocio Detallado. El Registro de Interesados (D) no aporta datos financieros ni de calendario.
2.  Los costes y plazos del Caso de Negocio Detallado provienen directamente del Plan de Proyecto, que ya ha sido elaborado con mayor precisión durante la fase de inicio.
3.  **Respuesta correcta:** B.

**Pregunta 4:**
*Según la terminología vigente de PRINCE2 Project Management (Version 7), ¿cómo se denomina el elemento que en la edición anterior del método se conocía como "tema" y que incluye al Business Case?*
a) Proceso.
b) Principio.
c) Práctica (Practice).
d) Componente de gobierno.

**Razonamiento Estructurado:**
1.  Los 7 procesos (A) y los 7 principios (B) son categorías distintas que no cambiaron de nombre entre ediciones. "Componente de gobierno" (D) no es terminología oficial de PRINCE2.
2.  Lo que en PRINCE2 6 se llamaba "tema" (*Theme*) pasa a llamarse "práctica" (*Practice*) en PRINCE2 7, incluyendo la práctica Business Case.
3.  **Respuesta correcta:** C.

**Pregunta 5:**
*Un organismo público británico está desarrollando un caso de negocio siguiendo el Five Case Model de HM Treasury. En la dimensión que analiza el listado de alternativas posibles y determina la opción que ofrece la mejor relación calidad-precio, ¿qué "caso" está desarrollando?*
a) Strategic Case.
b) Economic Case.
c) Commercial Case.
d) Financial Case.

**Razonamiento Estructurado:**
1.  El Strategic Case (A) justifica la necesidad y el encaje estratégico, no compara alternativas. El Commercial Case (C) se centra en cómo obtener los bienes o servicios (contratación). El Financial Case (D) analiza la asequibilidad para el organismo.
2.  El análisis de la relación de alternativas (longlist/shortlist) para identificar la opción de mejor relación calidad-precio es, por definición, el Economic Case.
3.  **Respuesta correcta:** B.

## 11. Fuentes utilizadas para la ampliación

**PRINCE2 / PeopleCert:**
- PeopleCert, *PRINCE2 Project Management Foundation (Version 7)*: información oficial sobre principios, prácticas y materiales oficiales.
- PeopleCert, *PRINCE2 Project Management Practitioner (Version 7)*: información oficial sobre la aplicación y adaptación de PRINCE2 7.
- PeopleCert, *PRINCE2 7. Best practice made better*: cambios introducidos en PRINCE2 7, incluyendo personas, flexibilidad, sostenibilidad y gestión digital y de datos.
- PeopleCert, *PRINCE2 7 – A Process of Evolution*: evolución de la séptima edición y mantenimiento de los siete procesos.
- PeopleCert, *Partners Support / FAQ*: información oficial sobre la transición y retirada de PRINCE2 6 y la disponibilidad de PRINCE2 7.

**Administración pública / evaluación de business cases:**
- HM Treasury, *The Green Book 2026*: marco oficial para la evaluación de costes, beneficios y riesgos de propuestas públicas y Five Case Model.
- HM Treasury, *Guidance on developing business cases for projects and programmes* (actualizada en junio de 2026): desarrollo de business cases mediante el Five Case Model.
- HM Treasury, *Green Book supplementary guidance: discounting*: tratamiento del valor temporal y descuento de costes y beneficios futuros.
- GOV.UK, *Project and programme management*: orientación oficial sobre evaluación de propuestas, Green Book y gestión de proyectos.
