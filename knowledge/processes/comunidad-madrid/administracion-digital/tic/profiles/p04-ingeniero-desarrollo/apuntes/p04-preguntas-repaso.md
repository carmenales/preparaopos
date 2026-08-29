---
id: "p04-preguntas-repaso"
title: "Preguntas test de repaso"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/tic"
profiles:
  - "p04-ingeniero-desarrollo"
official_profile: "P04 - Ingeniero de Desarrollo"
official_topic: "Preguntas tipo test de repaso"
source_ids:
tags:
created_at: "2026-08-29"
last_reviewed: "2026-08-29"
ai_generated: false
ai_sources:
  - "chatgpt"
  - "gemini"
  - "perplexity"
needs_human_review: false
---

# Preguntas tipo test de repaso

## Tema 2. Fundamentos y principios de la Gestión de Proyectos

**Pregunta 1:**
*Según la Guía PMBOK del PMI, ¿qué tipo de Oficina de Dirección de Proyectos (PMO) se caracteriza por tener un rol consultivo, suministrar plantillas, mejores prácticas y formación, ejerciendo un grado de control bajo sobre los proyectos?*
a) PMO Directiva.
b) PMO de Control.
c) PMO de Apoyo (*Supportive*).
d) PMO Estratégica / EPMO.

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**
> 
> 1.  **Palabra chivata:** "Rol consultivo", "suministra plantillas", "grado de control bajo".
> 
> 2.  **Descarte:** La PMO de Control (b) ejerce control moderado exigiendo marcos. La Directiva (a) ejerce control alto dirigiendo los proyectos.
> 
> 3.  El **Project Assurance** es precisamente el rol que, actuando en nombre del Project Board, verifica y monitoriza el Caso de Negocio de forma independiente a lo largo de todo el proyecto.
> 
> **Respuesta correcta:** C.

</details>

**Pregunta 2:**
*¿Cuál es la principal diferencia conceptual entre un proyecto y una operación en el ámbito de las tecnologías de la información?*
a) El proyecto busca mantener la continuidad del servicio, mientras que la operación genera un entregable único.
b) El proyecto se financia con OPEX recurrente, mientras que la operación se imputa como inversión de capital (CAPEX).
c) El proyecto es un esfuerzo temporal con inicio y fin orientados a un resultado único, mientras que la operación es un esfuerzo continuo y repetitivo.
d) El proyecto no asume riesgos ni incertidumbre, a diferencia de las operaciones de explotación.

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**
> 
> 1.  **Análisis:** (a) y (b) tienen los términos invertidos. (d) es falsa porque los proyectos concentran mayor incertidumbre.
> 
> 2.  (c) define de manera formal y literal la distinción según PMBOK e ISO 21502.
> 
> **Respuesta correcta:** **C**.

</details>

**Pregunta 3:**
*En el marco de la metodología Métrica v3, si durante la ejecución de las actividades de Seguimiento y Control (GPS) el equipo detecta una desviación en el alcance y formula una Petición de Cambio de Requisitos, ¿qué órgano tiene la potestad formal de autorizar o rechazar dicha modificación?*
a) El Jefe de Proyecto de forma unilateral.
b) El Comité de Seguimiento del proyecto.
c) El Grupo de Aseguramiento de la Calidad (CAL).
d) El Director de Sistemas de Información.

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**
> 
> **Análisis:** El Jefe de Proyecto analiza el impacto y propone la solución, pero en la interfaz GP de Métrica v3 la gobernanza y aprobación final recaen en el Comité de Seguimiento.
> 
> **Respuesta correcta:** **B**.
</details>

**Pregunta 4:**
*En la gestión del ciclo de vida bajo ITIL v4, ¿qué elemento es un requisito obligatorio que acompaña a una Solicitud de Cambio Normal (RFC) para garantizar la restauración del servicio si el despliegue falla?*
a) Acta de Constitución del Cambio.
b) Plan de Back-out (Reversión).
c) Diagrama de flujo acumulado.
d) Estimación por Puntos de Función.

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**
> 
> 1.  **Palabra chivata:** "Restauración del servicio si el despliegue falla".
> 
> 2.  El Plan de Back-out (marcha atrás) es la salvaguarda obligatoria exigida por el CAB para autorizar un cambio normal.
> 
> **Respuesta correcta:** **B**.

</details>

## Tema 3. Evaluación y selección de proyectos

**Pregunta 5:**
*Un comité de dirección evalúa dos proyectos tecnológicos mutuamente excluyentes para una infraestructura de almacenamiento. El Proyecto Alfa presenta un VAN de 320.000 € y una TIR del 14 %. El Proyecto Beta presenta un VAN de 210.000 € y una TIR del 22 %. Si el coste de capital de la organización es del 7 %, ¿cuál es la decisión financieramente correcta?*
a) Seleccionar el Proyecto Beta porque su rentabilidad porcentual (TIR) es netamente superior.
b) Seleccionar el Proyecto Alfa porque genera mayor valor absoluto (VAN), primando este criterio en proyectos mutuamente excluyentes.
c) Rechazar ambos proyectos porque la TIR supera excesivamente el coste de capital.
d) Seleccionar el Proyecto Beta únicamente si su periodo de recuperación simple es superior a 5 años.

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**
>
> 1.  **Identifica el conflicto:** En proyectos mutuamente excluyentes donde $VAN$ y $TIR$ discrepan, el criterio de decisión universal y jerárquicamente superior es el **Valor Actual Neto (VAN)**.
> 
> 2.  **Descarte:** La $TIR$ mide eficiencia relativa, pero el $VAN$ mide el incremento de riqueza o valor absoluto generado para la organización (Alfa aporta 320.000 € frente a los 210.000 € de Beta).
> 
> **Respuesta correcta: B.**

</details>

**Pregunta 6:**
*¿En qué categoría de métodos de selección de proyectos se engloban técnicas como la programación entera binaria (0-1), la programación lineal y la programación dinámica utilizadas para optimizar una cartera de proyectos sujeta a límites presupuestarios?*
a) Métodos de Medición de Beneficios.
b) Métodos de Optimización Restringida.
c) Modelos Cualitativos de Consenso.
d) Análisis de Reducción de Costes Operativos.

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**
> 
> 1.  **Palabra chivata:** "Programación entera, lineal, dinámica", "optimizar cartera sujeta a límites presupuestarios".
> 
> 2.  **Descarte:** Los métodos comparativos como scoring o Delphi pertenecen a Medición de Beneficios (a). Los modelos matemáticos basados en restricciones corresponden formalmente a la familia de **Optimización Restringida** (b).
> 
> **Respuesta correcta: B.**

</details>

**Pregunta 7:**
*Un organismo público ha invertido 180.000 € en el desarrollo de un módulo de software que ha quedado obsoleto antes de desplegarse debido a un cambio normativo. Para adaptarlo a la nueva ley se requieren 40.000 € adicionales, estimándose que el valor de los beneficios que aportará asciende a 70.000 €. ¿Cómo debe calificarse el gasto inicial de 180.000 € y cuál debe ser la decisión?*
a) Coste de Oportunidad; debe cancelarse el proyecto al superar el coste total acumulado a los beneficios.
b) Coste Hundido; el gasto previo debe ignorarse y el proyecto debe continuar porque el beneficio futuro (70.000 €) supera al coste pendiente (40.000 €).
c) Coste Amortizable; debe sumarse a la inversión restante obligando a rehacer el análisis de TIR.
d) Coste Marginal; debe descontarse íntegramente del Valor Monetario Esperado.

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**
> 
> 1.  **Identifica el concepto:** El dinero ya gastado e irrecuperable es un **Coste Hundido (*Sunk Cost*)**.
> 
> 2.  **Aplica la regla de oro:** Los costes hundidos son irrelevantes para decisiones futuras. Se evalúa exclusivamente lo que queda por gastar (40.000 €) frente a lo que se va a obtener (70.000 €). Como $70.000 > 40.000$, la continuación es favorable.
> 
> **Respuesta correcta: B.**

</details>

**Pregunta 8:**
*Al evaluar ofertas en una licitación de servicios cloud según el artículo 148 de la Ley 9/2017 de Contratos del Sector Público (LCSP), ¿qué enfoque de evaluación económica abarca no solo el precio de adquisición sino también los costes de utilización, mantenimiento y final de vida útil?*
a) Análisis Coste-Efectividad Simple.
b) Valor Monetario Esperado (VME).
c) Coste del Ciclo de Vida (LCC / TCO).
d) Retorno de la Inversión Contable (ROI).

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**
> 
> 1.  **Referencia legal:** El art. 148 LCSP define expresamente el cálculo del **Coste del Ciclo de Vida** (*Life Cycle Costing*).
> 
> 2.  **Definición:** Integra costes de adquisición, utilización (energía, recursos), mantenimiento y desmantelamiento/reciclaje.
> 
> **Respuesta correcta: C.**

</details>

**Pregunta 9:**
*Si un proyecto tecnológico tiene un 30 % de probabilidad de sufrir una sanción de seguridad de 100.000 € por fuga de datos y un 70 % de probabilidad de operar sin incidentes con un impacto de 0 €, ¿cuál es el Valor Monetario Esperado (VME) del riesgo considerado?*
a) -100.000 €
b) -30.000 €
c) 70.000 €
d) -70.000 €

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**
> 
> 1.  **Aplica la fórmula:** $VME = \sum (P_i \times I_i)$.
> 
> 2.  **Cálculo:** $VME = (0{,}30 \times (-100.000\text{ \euro})) + (0{,}70 \times 0\text{ \euro}) = -30.000\text{ \euro}$.
> 
> **Respuesta correcta: B.**
  
</details>

## Tema 4. Ejecución de proyectos

**Pregunta 10:**
*En una organización donde el Director de Proyecto actúa con dedicación a tiempo parcial, ejerciendo fundamentalmente un rol de coordinador de tareas o facilitador de comunicaciones y sin control sobre el presupuesto del proyecto, ¿qué estructura organizativa está implementada?*
a) Organización Matricial Fuerte.
b) Organización Orientada a Proyectos (Proyectizada).
c) Organización Matricial Débil.
d) Organización Matricial Equilibrada.

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**
> 
> 1.  **Palabras clave:** "Dedicación parcial", "rol de coordinador o facilitador", "sin control del presupuesto".
> 
> 2.  **Descarte:** En la Proyectizada (b) y Matricial Fuerte (a) el Director de Proyecto controla el presupuesto y tiene dedicación completa. En la Equilibrada (d) el poder es compartido. La figura del coordinador/expedidor con control del gerente funcional define a la **Matricial Débil**.
> 
> **Respuesta correcta: C.**

</details>

**Pregunta 11:**
*Según la metodología PRINCE2, ¿cuál de las siguientes opciones define con exactitud la responsabilidad del rol de Senior User dentro del Project Board?*
a) Garantizar la rentabilidad financiera y la justificación continua del Business Case.
b) Asegurar la integridad técnica y la calidad metodológica de los componentes desarrollados.
c) Especificar los requisitos funcionales, validar los criterios de aceptación y rendir cuentas de la obtención efectiva de los beneficios esperados.
d) Asignar y dirigir operativamente los paquetes de trabajo del equipo de programación.

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**
> 
> 1.  **Análisis:** (a) corresponde al *Executive*; (b) corresponde al *Senior Supplier*; (d) corresponde al *Team Manager*.
> 
> 2.  (c) define de manera literal las obligaciones del **Senior User** en el marco de gobierno de PRINCE2.
> 
> **Respuesta correcta: C.**

</details>

**Pregunta 12:**
*Durante la ejecución de un proyecto bajo PRINCE2, el Project Manager calcula que una desviación en las pruebas de integración retrasará la entrega del hito principal en 4 semanas, rebasando el límite de tolerancia de tiempo de 2 semanas fijado por el Project Board. ¿Cuál es la actuación metodológica obligatoria que debe seguir el Project Manager?*
a) Rediseñar el cronograma y aprobar unilateralmente la extensión del plazo al tratarse de un problema técnico.
b) Emitir de inmediato un Exception Report al Project Board informando del pronóstico y esperar directrices para la elaboración de un Exception Plan.
c) Cancelar inmediatamente el proyecto al haberse vulnerado una de las seis tolerancias directivas.
d) Transferir el impacto al registro de riesgos sin elevar la incidencia hasta la reunión de cierre de fase.

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**
> 
> 1.  **Principio aplicable:** Principio de **Gestión por Excepción**.
> 
> 2.  **Procedimiento:** Al prever la superación de una tolerancia, el Director de Proyecto no tiene autoridad para autoaprobar el retraso ni cancelar el proyecto; debe emitir formalmente un **Exception Report** al Project Board.
> 
> **Respuesta correcta: B.**

</details>

**Pregunta 13:**
*En el marco de la metodología Métrica v3, si un nuevo requerimiento legal exige una modificación sustancial del alcance durante las actividades de Seguimiento y Control (GPS), ¿a qué órgano corresponde la aprobación formal de dicha Petición de Cambio de Requisitos?*
a) Al Comité de Dirección.
b) Al Jefe de Proyecto.
c) Al Comité de Seguimiento.
d) Al Equipo de Aseguramiento de la Calidad (CAL).

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**
> 
> 1.  **Gobernanza Métrica v3:** El Jefe de Proyecto evalúa el impacto en tiempo/coste pero no decide. El Comité de Dirección aprueba procesos mayores de fase.
> 
> 2.  La aprobación formal de cambios en los requisitos del sistema es potestad reglada del **Comité de Seguimiento**.
> 
> **Respuesta correcta: C.**

</details>

**Pregunta 14:**
*Al aplicar el principio de Adaptación (Tailoring) en un proyecto público gestionado bajo PRINCE2 o PMBOK, ¿cuál de las siguientes actuaciones se considera contraria a las buenas prácticas metodológicas?*
a) Fusionar la documentación de inicio y planificación en un único artefacto formal para un proyecto pequeño.
b) Eliminar el principio de justificación comercial continua al considerar que el proyecto es de obligado cumplimiento normativo.
c) Ajustar la frecuencia de los informes de seguimiento pasando de entregas semanales a quincenales.
d) Delegar la función de Team Manager en el propio Project Manager en un equipo de desarrollo reducido.

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**
> 
> 1.  **Regla de oro:** El *tailoring* permite simplificar documentos, procesos, herramientas e integrar roles, pero **nunca permite eliminar principios universales**.
> 
> 2.  Omitir la Justificación Comercial Continua (b) viola las bases del método, siendo la respuesta contraria a la norma.
> 
> **Respuesta correcta: B.**

</details>

## Tema 5. Estándares y Marcos de Referencia para la Gestión de Proyecto

**Pregunta 15:**
*Un equipo de desarrollo ágil utiliza un tablero visual Kanban y establece una regla estricta que prohíbe tener más de 3 tareas simultáneas en la columna de "Pruebas de Integración". ¿Qué práctica fundamental de Kanban se está aplicando?*
a) Definición del Sprint Backlog.
b) Limitación del Trabajo en Curso (WIP - Work in Progress).
c) Control de la Velocidad mediante Burndown Chart.
d) Estimación por Planning Poker.

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**v
> 
> 1.  **Palabra chivata:** "Prohíbe tener más de X tareas simultáneas en una columna".
> 
> 2.  **Descarte:** Scrum limita por tiempo en Sprints (a); Kanban se basa en el flujo continuo y limita explícitamente el WIP por fase para evitar cuellos de botella.
> 
> **Respuesta correcta: B.**
  
</details>

**Pregunta 16:**
*¿Cuál de las siguientes afirmaciones describe con precisión la evolución estructural de la Guía PMBOK publicada por el PMI en su 8ª Edición (noviembre de 2025) frente a la 7ª Edición (2021)?*
a) La 8ª Edición restaura íntegramente las 10 Áreas de Conocimiento y 49 procesos rígidos de la 6ª Edición.
b) La 8ª Edición simplifica la estructura a 6 Principios Fundamentales, 7 Dominios de Desempeño y 5 Áreas de Enfoque con 40 procesos no prescriptivos, incorporando IA y sostenibilidad.
c) La 8ª Edición suprime todos los dominios de desempeño adoptando el modelo estricto de PRINCE2.
d) Ambas ediciones comparten idéntica cantidad de 12 principios y 8 dominios sin cambios.

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**
> 
> **Análisis:** La 8ª Edición no vuelve a la 6ª Edición (a), sino que evoluciona el modelo a 6 principios, 7 dominios y 5 áreas de enfoque (*Focus Areas*) con orientación de procesos no prescriptiva y foco en IA/ESG.
> 
> **Respuesta correcta: B.**

</details>

**Pregunta 17:**
*En el marco de la norma internacional ISO 21502:2020 sobre gestión de proyectos, ¿cuál de las siguientes afirmaciones es correcta respecto a su naturaleza y alcance?*
a) Es una norma certificable por entidades acreditadas externas mediante auditoría de conformidad formal.
b) Establece directrices de gestión de proyectos de alto nivel, no es certificable y resulta agnóstica respecto al ciclo de vida o enfoque de desarrollo adoptado.
c) Regula de forma exclusiva y exhaustiva la gestión de programas y portafolios estratégicos.
d) Impone obligatoriamente un ciclo de vida en cascada con 5 fases secuenciales estrictas.

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**
> 
> 1.  **Análisis:** ISO 21502 es una guía de directrices no certificable (a falsa); se centra en proyectos y no en programas/portafolios (c falsa); admite cualquier enfoque de ciclo de vida predictivo o adaptativo (d falsa).
> 
> 2.  (b) recoge con total rigor sus características fundamentales.
> 
> **Respuesta correcta: B.**

</details>

**Pregunta 18:**
*Según la Guía Scrum oficial (edición 2020), ¿cuál es el compromiso formal asociado al artefacto del Product Backlog?*
a) El Sprint Goal.
b) La Definition of Done (DoD).
c) El Product Goal (Objetivo del Producto).
d) La Matriz de Trazabilidad de Requisitos.

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**
> 
> **Correspondencias oficiales:**
> 
> *   Product Backlog $\rightarrow$ **Product Goal**.
> *   Sprint Backlog $\rightarrow$ **Sprint Goal**.
> *   Incremento $\rightarrow$ **Definition of Done**.
> 
> **Respuesta correcta: C.**

</details>

**Pregunta 19:**
*Para desplegar en el entorno de producción de una Consejería una actualización mayor del sistema de nóminas que requiere parada de servicio programada, ¿cómo debe tramitarse el cambio bajo el marco ITIL v4?*
a) Como un Cambio Estándar preautorizado.
b) Como un Cambio Normal, requiriendo solicitud RFC, evaluación de riesgos, Plan de Back-out y aprobación del CAB/CAC.
c) Como una Excepción no planificada de PRINCE2.
d) Mediante un Cambio de Emergencia sin documentación técnica previa.

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**
> 
> 1.  **Análisis:** Los cambios mayores no rutinarios con impacto en el servicio son **Cambios Normales**.
> 
> 2.  Requieren registro formal (RFC), análisis de impacto, ventana de parada, Plan de Back-out de reversión y autorización del CAB/CAC.
> 
> **Respuesta correcta: B.**

</details>

## Tema 6. Herramientas y Técnicas de Gestión

**Pregunta 20:**
*En el análisis del desempeño de un proyecto TIC mediante la técnica del Valor Ganado (EVM), se obtienen los siguientes datos a la fecha de control: Valor Planificado (PV) = 100.000 €, Valor Ganado (EV) = 80.000 € y Coste Real (AC) = 100.000 €. ¿Cuál es la situación exacta del proyecto respecto al cronograma y al presupuesto?*
a) Va adelantado en plazo ($SV > 0$) y en línea con el presupuesto planificado ($CV = 0$).
b) Va con retraso respecto al cronograma ($SV < 0$) y presenta un sobrecoste presupuestario ($CV < 0$).
c) Presenta un índice $CPI = 1{,}25$, generando un ahorro neto de costes.
d) Va en tiempo ($SPI = 1{,}0$) pero con una desviación negativa de costes.

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**
> 1.  **Cálculo de variaciones:**
> 
> *  $SV = EV - PV = 80.000\text{ \euro} - 100.000\text{ \euro} = -20.000\text{ \euro}$ ($SV < 0 \rightarrow$ Retraso en plazo).
> 
> *  $CV = EV - AC = 80.000\text{ \euro} - 100.000\text{ \euro} = -20.000\text{ \euro}$ ($CV < 0 \rightarrow$ Sobrecoste).
> 
> 2.  **Cálculo de índices:**
> 
> *  $SPI = \frac{EV}{PV} = \frac{80.000}{100.000} = 0{,}80$ ($SPI < 1 \rightarrow$ Ineficiencia temporal).
> 
> *  $CPI = \frac{EV}{AC} = \frac{80.000}{100.000} = 0{,}80$ ($CPI < 1 \rightarrow$ Ineficiencia de costes).
> 
> **Respuesta correcta: B.**

</details>

**Pregunta 21:**
*Al estimar la duración de una actividad crítica mediante la técnica PERT de tres puntos, el equipo determina una estimación optimista de 4 días, una más probable de 7 días y una pesimista de 16 días. ¿Cuál es la duración esperada y la varianza de dicha actividad?*
a) Duración esperada = 9 días; Varianza = 4 días².
b) Duración esperada = 8 días; Varianza = 4 días².
c) Duración esperada = 7 días; Varianza = 2 días².
d) Duración esperada = 8 días; Varianza = 2 días².

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**
> 
> 1.  **Fórmula de duración esperada:** $\mu_E = \frac{O + 4M + P}{6} = \frac{4 + (4 \times 7) + 16}{6} = \frac{4 + 28 + 16}{6} = \frac{48}{6} = 8\text{ días}$.
> 
> 2.  **Fórmula de varianza:** $\sigma^2 = \left( \frac{P - O}{6} \right)^2 = \left( \frac{16 - 4}{6} \right)^2 = \left( \frac{12}{6} \right)^2 = 2^2 = 4\text{ días}^2$.
> 
> **Respuesta correcta: B.**
  
</details>

**Pregunta 22:**
*En el marco de la metodología de desarrollo Métrica v3, si durante la ejecución de las actividades de Seguimiento y Control (GPS) un departamento usuario solicita una modificación técnica en la base de datos que altera los requisitos acordados, ¿qué procedimiento reglado debe seguirse?*
a) El Jefe de Proyecto aprueba directamente el cambio si el impacto es inferior a 10 días/persona.
b) El Jefe de Proyecto realiza el análisis de impacto técnico y económico y eleva la petición de cambio para su aprobación o rechazo al Comité de Seguimiento.
c) El cambio es aprobado unilateralmente por el equipo de Aseguramiento de la Calidad (CAL).
d) La solicitud se transfiere a la fase de Mantenimiento de Sistemas de Información (MSI) denegándose en la fase actual.

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**
> 
> 1.  **Gobernanza en Métrica v3:** El Jefe de Proyecto tiene la obligación de registrar y evaluar el impacto, pero carece de potestad para aprobar variaciones de alcance en la línea base.
> 
> 2.  La aprobación formal corresponde reglamentariamente al **Comité de Seguimiento**.
> 
> **Respuesta correcta: B.**

</details>

**Pregunta 23:**
*Según la norma ISO 21511 sobre Estructuras de Desglose del Trabajo (WBS/EDT), ¿cuál es la definición formal de la "Regla del 100%"?*
a) La WBS debe completarse en el 100% de los proyectos independientemente de su presupuesto.
b) La WBS debe contener el 100% del trabajo definido en el alcance del proyecto, incluyendo el trabajo de gestión, sin omitir ni añadir nada.
c) Cada paquete de trabajo debe representar exactamente el 100% de una tarea individual.
d) El cronograma debe ejecutarse al 100% sin permitir holguras en ninguna actividad.

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**
> 
> **Definición normativa:** La regla del 100% establece que la WBS captura la totalidad del trabajo acordado (alcance y dirección), garantizando que la suma de los niveles inferiores refleje íntegramente el nivel superior sin excederlo.
> 
> **Respuesta correcta: B.**

</details>

**Pregunta 24:**
*Bajo las mejores prácticas de ITIL v4, ¿cómo debe tramitarse el despliegue de un parche mayor de seguridad en el servidor de base de datos corporativo de una Consejería que requiere una ventana de parada de servicio planificada?*
a) Como un Cambio Estándar preautorizado.
b) Como un Cambio Normal, requiriendo registro RFC, análisis de riesgos, Plan de Back-out y aprobación del CAB/CAC.
c) Como un Cambio de Emergencia sin evaluación previa.
d) Mediante una solicitud directa al Centro de Atención a Usuarios (CAU).

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**
> 
> 1.  **Análisis:** Es un cambio no recurrente y con impacto potencial en la disponibilidad.
> 
> 2.  No es estándar (requiere evaluación) ni de emergencia inmediata (es planificado). Por tanto, es un **Cambio Normal** que exige solicitud RFC, plan de reversión (Back-out) y visto bueno del CAB/CAC.
> 
> **Respuesta correcta: B.**

</details>

## Tema 7. Tendencias en la Gestión de Proyectos

**Pregunta 25:**
*En un proyecto de administración digital gestionado con un enfoque híbrido, la dirección identifica a un alto cargo institucional con un elevado nivel de autoridad y poder de decisión sobre el presupuesto, pero con muy escaso interés en los detalles técnicos de los desarrollos diarios. Según la matriz de Poder/Interés de Mendelow, ¿cuál es la estrategia de comunicación adecuada?*
a) Gestionar estrechamente mediante reuniones diarias de seguimiento técnico.
b) Mantenerle satisfecho a través de resúmenes ejecutivos e informes de hitos periódicos.
c) Informarle exclusivamente si se produce una parada total del servicio en producción.
d) Monitorizarle con el mínimo esfuerzo sin remitirle comunicación formal.

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**
> 
> 1.  **Clasificación en la matriz:** El interesado posee **Alto Poder** y **Bajo Interés**.
> 
> 2.  **Descarte:**
> 
> *   *Gestionar estrechamente* (a) es para Alto Poder y Alto Interés.
> 
> *   *Monitorizar* (d) es para Bajo Poder y Bajo Interés.
> 
> *   *Mantener informado* es para Bajo Poder y Alto Interés.
> 
> 3.  La estrategia formal de Mendelow para este cuadrante es **Mantener Satisfecho** (b), facilitando información de alto nivel para asegurar su respaldo sin sobrecargarle con detalles operativos.
> 
> **Respuesta correcta: B.**

</details>

**Pregunta 26:**
*Según los estándares de gestión de interesados de la Guía PMBOK, ¿en qué proceso se elabora por primera vez el Registro de Interesados (*Stakeholder Register*), donde se documenta la clasificación inicial de los agentes como favorables, neutrales u opositores?*
a) Planificar el Involucramiento de los Interesados.
b) Identificar a los Interesados.
c) Gestionar el Involucramiento de los Interesados.
d) Monitorear el Involucramiento de los Interesados.

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**
> 
> 1.  **Artefacto evaluado:** El **Registro de Interesados**.
> 
> 2.  **Secuencia metodológica:** Se crea formalmente durante el primer proceso (**Identificar a los Interesados**). Los procesos posteriores (Planificar, Gestionar y Monitorear) utilizan, enriquecen y actualizan este registro, pero su generación original corresponde al proceso de identificación.
> 
> **Respuesta correcta: B.**

</details>

**Pregunta 27:**
*¿Cómo se denomina la filosofía de liderazgo adoptada en los marcos ágiles (Scrum) y reconocida en las 'Power Skills' del PMI, en la que el responsable del proyecto enfoca su labor en remover bloqueos técnicos, facilitar recursos y proteger al equipo de interferencias externas, en lugar de dirigir mediante jerarquía y órdenes directivas?*
a) Liderazgo Autocrático.
b) Liderazgo Transaccional.
c) Liderazgo Siervo (*Servant Leadership*).
d) Liderazgo Pasivo (*Laissez-Faire*).

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**
> 
> 1.  **Definición evaluada:** Líder enfocado en la facilitación, eliminación de impedimentos y servicio al equipo para potenciar su autogestión.
> 
> 2.  Corresponde literalmente al **Liderazgo Siervo (*Servant Leadership*)**, rol nuclear del *Scrum Master* e integrado en el PMBOK 7/8.
> 
> **Respuesta correcta: C.**

</details>

**Pregunta 28:**
*En un proyecto de desarrollo software para una Consejería, los análisis estáticos de código (SAST), la comprobación de dependencias (SCA) y las auditorías de conformidad con el Esquema Nacional de Seguridad (ENS) se integran y ejecutan de forma automatizada en el pipeline de despliegue continuo desde el inicio del proyecto. ¿Qué tendencia técnica define esta práctica?*
a) Bimodal IT.
b) Agile-fall.
c) DevSecOps (*Shift-Left Security*).
d) PRiSM Management.

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**
> 
> 1.  **Patrón identificado:** Integración de la seguridad de forma automatizada, continua y temprana (*Shift-Left*) dentro de las cadenas CI/CD de desarrollo y operaciones.
> 
> 2.  Define el paradigma **DevSecOps** (b/c/d descartadas).
> 
> **Respuesta correcta: C.**

</details>

**Pregunta 29:**
*De acuerdo con el Reglamento (UE) 2024/1689 (AI Act), ¿qué requisitos técnicos esenciales establece el artículo 15 para los proyectos que desarrollen o implanten sistemas de inteligencia artificial clasificados como de alto riesgo?*
a) Garantizar un VAN positivo y un periodo de recuperación inferior a 2 años.
b) Diseñar los sistemas de modo que alcancen niveles adecuados de precisión, robustez y ciberseguridad a lo largo de su ciclo de vida.
c) Exclusividad en el uso de modelos de lenguaje de código abierto no supervisados.
d) Delegación íntegra de la toma de decisiones sin supervisión humana obligatoria.

<details>
<summary>Mostrar respuesta</summary>

> **Razonamiento:**
> 
> 1.  **Referencia legal:** Artículo 15 del Reglamento de Inteligencia Artificial (AI Act).
> 
> 2.  **Exigencia normativa:** Exige explícitamente que los sistemas de IA de alto riesgo mantengan niveles adecuados de **precisión, robustez y ciberseguridad** durante todo su ciclo de vida, acompañados de supervisión humana (descartando la opción d).
> 
> **Respuesta correcta: B.**

</details>