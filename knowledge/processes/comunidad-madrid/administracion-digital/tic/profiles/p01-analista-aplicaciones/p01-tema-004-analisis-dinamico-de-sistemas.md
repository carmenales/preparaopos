---
id: "cm-ad-tic-p01-tema-004-analisis-dinamico"
title: "Análisis dinámico de sistemas"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/tic"
profiles:
  - "p01-analista-aplicaciones"
official_profile: "P01 - Analista de Aplicaciones"
official_topic: "Tema 4. Análisis dinámico de sistemas"
source_ids:
  - "A2_Bloque_IV.pdf"
tags:
  - "analisis-dinamico"
  - "bpmn"
  - "modelado-procesos"
  - "omg"
  - "uml"
  - "bpm"
  - "dmn"
created_at: "2026-08-09"
last_reviewed: "2026-08-09"
ai_generated: true
ai_sources:
  - "gemini"
  - "perplexity"
needs_human_review: true
---

# Tema 4. Análisis dinámico de sistemas

Este tema aborda cómo modelar el comportamiento temporal y procedimental de un sistema o negocio. A diferencia del análisis estático (que define "qué elementos hay", como un Diagrama de Clases o un Modelo Entidad-Relación), el análisis dinámico define **"qué ocurre, en qué orden y bajo qué condiciones"**.

## 1. Modelado de Procesos

El modelado de procesos es la representación gráfica y estructurada de los procesos de negocio de una organización. Es el paso fundamental para la digitalización, ya que no se puede automatizar un proceso que no se comprende.

*   **AS-IS (Situación actual):** Modelado de cómo funciona el proceso hoy en día, con sus ineficiencias, cuellos de botella y tareas manuales.
*   **TO-BE (Situación futura):** Modelado de cómo debería funcionar el proceso tras la mejora o implantación del nuevo sistema de información.
*   **BPR (Business Process Reengineering):** Reingeniería de procesos. Implica rediseñar un proceso desde cero para lograr mejoras drásticas, a diferencia del BPM (Business Process Management), que busca la mejora continua y progresiva.

### 1.1. BPM (Business Process Management) y su ciclo de vida

El **BPM** no es solo una notación gráfica, sino una disciplina de gestión completa que abarca descubrir, modelar, ejecutar, monitorizar y optimizar los procesos de negocio de forma continua. Su ciclo de vida se estructura habitualmente en **5 fases**, muy preguntables porque distintos autores/herramientas usan nombres ligeramente distintos que conviene saber equiparar:

1.  **Diseño / Descubrimiento (*Design/Discover*):** se analiza el proceso AS-IS existente, identificando actividades, responsables (propietarios de tarea) y puntos de mejora.
2.  **Modelado (*Model*):** se construye la representación visual del proceso TO-BE, habitualmente en notación **BPMN**, incluyendo tareas, decisiones, eventos y flujos de datos.
3.  **Ejecución (*Execute*):** el proceso modelado se implementa, bien mediante un motor BPM (BPMS) que interpreta directamente el diagrama, bien integrándolo en las aplicaciones existentes; se suele validar primero con una prueba piloto.
4.  **Monitorización (*Monitor*):** se hace seguimiento en tiempo real del proceso en ejecución, midiendo indicadores clave de rendimiento (KPI) como tiempos de ciclo, cuellos de botella y tasas de excepción.
5.  **Optimización (*Optimize*):** con los datos reales obtenidos, se ajusta y mejora el proceso (eliminando pasos sin valor, automatizando decisiones repetitivas), cerrando el ciclo y volviendo a la fase de diseño de forma iterativa (enfoque tipo PDCA/Kaizen aplicado a procesos).

Esta naturaleza cíclica y de mejora continua es precisamente lo que distingue al **BPM** del **BPR**: el BPR rompe con el proceso existente y lo rediseña desde cero buscando un salto drástico de rendimiento, mientras que el BPM gestiona el proceso de forma evolutiva a lo largo de su ciclo de vida completo.

## 2. Modelado Dinámico de Sistemas (UML)

En el ámbito de la Ingeniería de Software, el Lenguaje Unificado de Modelado (UML) proporciona varios diagramas de comportamiento (dinámicos) para representar cómo cambia el sistema a lo largo del tiempo:

*   **Diagrama de Actividades:** Muestra el flujo de control o flujo de datos paso a paso. Es el equivalente UML a un diagrama de flujo tradicional y precursor de lo que hoy es BPMN para negocio.
*   **Diagrama de Estados (Máquina de Estados):** Muestra los diferentes estados por los que pasa un objeto durante su ciclo de vida y los eventos que provocan las transiciones de un estado a otro.
*   **Diagrama de Secuencia:** Muestra cómo los objetos interactúan entre sí y el orden temporal en que se intercambian los mensajes. Es fundamental para diseñar el comportamiento de los Casos de Uso.
*   **Diagrama de Tiempos:** Se centra específicamente en las restricciones de tiempo y la duración de los eventos (muy usado en sistemas empotrados o de tiempo real).

Un quinto diagrama de comportamiento que suele omitirse pero que UML define formalmente es el **Diagrama de Comunicación (*Communication Diagram*)**, variante del diagrama de secuencia que pone el énfasis en las relaciones estructurales entre los objetos que intercambian mensajes, en lugar de en el orden temporal estricto. Conviene también distinguir con precisión el **Diagrama de Actividades** del **Diagrama de Estados**: el primero modela el flujo de un *proceso o algoritmo* (qué pasos se ejecutan y en qué orden), mientras que el segundo modela el *ciclo de vida de un objeto concreto* (en qué estado se encuentra y qué eventos provocan su cambio de estado); es una trampa de examen habitual confundir ambos por su similitud visual.

## 3. BPMN (Business Process Model and Notation)

BPMN es el estándar internacional *de facto* para el modelado de procesos de negocio. Está mantenido por el **OMG (Object Management Group)** y su versión actual estandarizada por ISO es **BPMN 2.0.2 (ISO/IEC 19510)**.

Su objetivo principal es proveer una notación gráfica fácilmente comprensible por todos los usuarios del negocio (desde los analistas que crean los borradores, hasta los desarrolladores técnicos que implementan la tecnología, y los gerentes que monitorean los resultados), sirviendo como lenguaje común para cerrar la brecha entre el diseño del negocio y su implementación.

### 3.1. Tipos de Modelos en BPMN 2.0

Una pregunta clásica de examen es distinguir los tres tipos de diagramas que soporta BPMN 2.0:

1.  **Procesos de Orquestación (Orchestration):** Representan un proceso privado interno de una organización o departamento (todo ocurre dentro de un único Pool).
2.  **Procesos de Colaboración (Collaboration):** Muestran las interacciones entre dos o más entidades de negocio independientes (dos o más Pools). Se representan mediante flujos de mensajes entre los participantes.
3.  **Coreografía (Choreography):** Formaliza la forma en que los participantes coordinan sus interacciones. El enfoque no está en el trabajo interno de un participante, sino en el **intercambio de mensajes** entre ellos, sin que exista un controlador central.

### 3.2. DMN (Decision Model and Notation): la notación complementaria

**DMN** es otro estándar del OMG, hermano de BPMN, diseñado específicamente para modelar **decisiones de negocio** de forma independiente del proceso que las contiene. Es habitual encontrarlo mencionado junto a BPMN porque ambas notaciones se complementan: BPMN modela el "cómo fluye el trabajo" y DMN modela el "cómo se toma una decisión concreta dentro de ese flujo" (típicamente mediante **Tablas de Decisión**, que listan de forma tabular las combinaciones de condiciones de entrada y su resultado). En BPMN, una actividad de tipo **Tarea de Regla de Negocio (*Business Rule Task*)** es la que delega su lógica en un modelo DMN externo, evitando "ensuciar" el diagrama de proceso con reglas complejas de decisión.

## 4. Elementos Clave de BPMN 2.0

Los tribunales TIC suelen poner preguntas descriptivas de las figuras ("¿Qué representa un rombo con un signo + en su interior?"). BPMN se divide en cuatro categorías fundamentales:

### A) Objetos de Flujo (Flow Objects)
Son los elementos que definen el comportamiento del proceso.

*   **Eventos (Círculos):** Algo que ocurre durante el proceso.
    *   *Inicio (Start):* Línea fina y simple.
    *   *Intermedio (Intermediate):* Línea doble. Pueden "capturar" (Catch) un evento o "lanzar" (Throw) un evento.
    *   *Fin (End):* Línea gruesa simple. Resultan siempre en el lanzamiento de una señal o la conclusión del proceso.
*   **Actividades (Rectángulos con esquinas redondeadas):** El trabajo que se realiza dentro del proceso.
    *   *Tarea (Task):* Unidad atómica de trabajo.
    *   *Subproceso (Sub-process):* Actividad compuesta que puede desglosarse en niveles más bajos de detalle (se marca con un pequeño "+" en el centro inferior).
*   **Pasarelas o Gateways (Rombos):** Controlan la divergencia y convergencia del flujo de secuencia.
    *   **Exclusiva (XOR):** Rombo vacío o con una "X". Solo se puede seguir **UN** camino válido.
    *   **Paralela (AND):** Rombo con un "+". El flujo se divide en todos los caminos simultáneamente, o espera a que todos converjan para continuar.
    *   **Inclusiva (OR):** Rombo con un círculo "O". Se pueden seguir **UNO O MÁS** caminos dependiendo de la condición.
    *   **Basada en Eventos:** Rombo con un símbolo de evento intermedio. El flujo sigue el camino del primer evento que ocurra (ej. "Recibir correo" vs "Pasan 5 días de espera").

**Ampliación de los tipos de Eventos por su disparador (icono interior):** además de la clasificación por posición (inicio/intermedio/fin), cada evento se clasifica por el tipo de disparador que representa, un contenido muy preguntado de forma gráfica en examen:
*   **Evento de Mensaje (icono de sobre):** se dispara al enviar o recibir un mensaje de otro participante; es el tipo de evento que conecta directamente con los Flujos de Mensaje entre Pools.
*   **Evento de Temporizador (icono de reloj):** se dispara al cumplirse una fecha, una duración o un ciclo recurrente (ej. "esperar 5 días"). Es la base de los escalados automáticos por vencimiento de plazo (SLA).
*   **Evento de Error (icono de rayo):** representa un fallo grave; solo puede "capturarse" en el borde de una actividad o en el inicio de un subproceso de evento, y solo puede "lanzarse" en un evento de fin.
*   **Evento de Señal (icono de triángulo):** representa una difusión (*broadcast*) sin destinatario concreto; a diferencia del mensaje (dirigido a un participante específico), cualquier proceso que esté "escuchando" esa señal puede reaccionar a ella.
*   **Evento Condicional:** se dispara cuando se cumple una condición lógica de negocio evaluada sobre los datos del proceso.

Un matiz muy examinable sobre los **Eventos de Borde (*Boundary Events*)**: se adjuntan al borde de una actividad y pueden ser **interruptivos** (círculo de borde sólido: si se dispara, cancela la actividad y desvía el flujo) o **no interruptivos** (círculo de borde discontinuo: se dispara en paralelo sin cancelar la actividad en curso, por ejemplo para enviar una notificación de recordatorio sin detener la tarea).

### B) Objetos de Conexión (Connecting Objects)
Conectan los objetos de flujo entre sí o con otra información. **(¡ALERTA TRAMPA DE EXAMEN!)**

*   **Flujo de Secuencia (Sequence Flow):** Línea continua con flecha cerrada. Muestra el orden en que se ejecutan las actividades. **Regla de Oro:** Un flujo de secuencia NUNCA puede cruzar los límites de un Pool.
*   **Flujo de Mensaje (Message Flow):** Línea discontinua con flecha abierta en la punta y un pequeño círculo en el inicio. Representa mensajes entre participantes. **Regla de Oro:** Un flujo de mensaje SÓLO puede existir entre Pools distintos; NUNCA dentro del mismo Pool.
*   **Asociación (Association):** Línea de puntos que asocia información (artefactos, anotaciones) con los objetos de flujo.

### C) Carriles (Swimlanes)
Organizan las responsabilidades de las actividades.

*   **Pool (Piscina):** Representa a un Participante (una organización, un cliente, una entidad). Sirve como contenedor del proceso.
*   **Lane (Calle):** Es una sub-partición dentro de un Pool. Suele representar un rol (ej. Analista), un departamento o un sistema informático específico dentro de la organización.

### D) Artefactos (Artifacts)
Proveen información adicional sobre el proceso sin afectar directamente el flujo.

*   **Objeto de Datos (Data Object):** Muestra qué datos se requieren o se producen en una actividad (ícono de un folio doblado en la esquina).
*   **Grupo (Group):** Caja con borde punteado que agrupa visualmente varios elementos para su comprensión, sin afectar al flujo.
*   **Anotación (Text Annotation):** Texto libre conectado con una Asociación para explicar un elemento complejo.

## 5. Patrones de Examen y "Palabras Chivata"

| Concepto | Palabra Chivata o Regla para el Test |
| :--- | :--- |
| **OMG (Object Management Group)** | "Organización responsable del estándar BPMN, DMN y UML". |
| **Flujo de Secuencia** | "Línea continua", "**NUNCA** cruza límites de un Pool". |
| **Flujo de Mensajes** | "Línea discontinua", "**SIEMPRE** cruza límites de un Pool (entre participantes)". |
| **Gateway Exclusivo (XOR)** | "Rombo vacío o con X", "Caminos mutuamente excluyentes", "Solo un camino válido". |
| **Gateway Inclusivo (OR)** | "Rombo con un círculo interno O", "Uno o varios caminos válidos simultáneos". |
| **Pool vs Lane** | Pool = Participante / Organización entera; Lane = Departamento / Rol específico interno. |
| **Coreografía (Choreography)** | "Sin controlador central", "Enfocado en el intercambio de mensajes entre participantes". |
| **AS-IS / TO-BE** | "AS-IS = Situación actual (cómo es)", "TO-BE = Situación futura tras reingeniería". |
| **Evento de Temporizador** | "Icono de reloj", "Espera/plazo/SLA", "Solo captura (catching)". |
| **Evento de Señal** | "Icono de triángulo", "Difusión sin destinatario concreto", "Cualquiera puede escuchar". |
| **Evento de Error** | "Icono de rayo", "Captura solo en borde de actividad", "Lanza solo en evento de fin". |
| **Evento de borde interruptivo vs. no interruptivo** | Borde sólido = cancela la actividad; borde discontinuo = no la cancela. |
| **DMN** | "Tablas de decisión", "Complementa a BPMN", "Business Rule Task". |
| **Ciclo de vida BPM** | "Diseñar-Modelar-Ejecutar-Monitorizar-Optimizar", "Mejora continua e iterativa". |

### 5.1. Simulacro de Test: Desmontando trampas

**Pregunta 1:**
*En un diagrama de colaboración BPMN 2.0 que representa la interacción entre un "Ciudadano" y el "Ministerio de Hacienda", necesitas conectar la actividad "Enviar Solicitud" (situada en el pool del Ciudadano) con el evento "Recepción de Solicitud" (situado en el pool del Ministerio). ¿Qué tipo de conector debes utilizar obligatoriamente?*
a) Flujo de Secuencia (Sequence Flow).
b) Flujo de Mensaje (Message Flow).
c) Asociación Bidireccional.
d) Gateway de Comunicación.

**Razonamiento Estructurado:**
1.  **Aplica la regla de oro de los Pools:** El enunciado habla de conectar elementos situados en **dos Pools distintos** ("Ciudadano" y "Ministerio").
2.  **Desmontando:**
    *   (A) Es la trampa clásica. El Flujo de Secuencia indica el orden de ejecución, pero en BPMN *jamás* puede cruzar de un Pool a otro, porque cada Pool tiene su propio control de proceso interno.
    *   (C) y (D) No son conectores de flujo válidos para esta acción.
    *   (B) El Flujo de Mensaje se utiliza exclusivamente para mostrar la comunicación e interacción entre participantes diferentes (Pools distintos).
3.  **Respuesta correcta: B.**

**Pregunta 2:**
*Durante el modelado de un proceso de aprobación de expedientes en BPMN, el flujo llega a un punto donde, dependiendo de ciertas reglas de negocio, el expediente puede enviarse a "Revisión Económica", a "Revisión Jurídica", o a **ambas simultáneamente**. ¿Qué tipo de Gateway o Pasarela se debe utilizar para modelar correctamente este comportamiento divergente?*
a) Pasarela Exclusiva (XOR).
b) Pasarela Paralela (AND).
c) Pasarela Inclusiva (OR).
d) Pasarela Basada en Eventos.

**Razonamiento Estructurado:**
1.  **Busca el patrón:** Se pueden seguir "una, la otra, o ambas". Hay que elegir caminos basados en condiciones, pudiendo ser válidos más de uno a la vez.
2.  **Desmontando:**
    *   (A) La Exclusiva (XOR) forzaría a que solo se pueda elegir uno de los caminos, excluyendo al resto de forma absoluta. Falsa.
    *   (B) La Paralela (AND) forzaría a que el flujo *siempre* tome obligatoriamente todos los caminos (tanto Económica como Jurídica), sin importar la condición. Falsa.
    *   (D) La basada en eventos se bifurca según qué evento externo ocurra primero, no por evaluación de datos. Falsa.
    *   (C) La Pasarela Inclusiva (OR) evalúa todas las condiciones y activa todos los caminos de salida que resulten ciertos (puede ser uno, varios, o todos).
3.  **Respuesta correcta: C.**

**Pregunta 3:**
*¿Cuál de las siguientes afirmaciones respecto a la diferencia entre BPM (Business Process Management) y BPR (Business Process Reengineering) es cierta en el ámbito del modelado y mejora de procesos?*
a) El BPR se enfoca en la mejora continua, progresiva e incremental, mientras que el BPM requiere rediseñar todo desde cero.
b) El BPR busca cambios radicales y rupturistas rediseñando el proceso desde su raíz, mientras que el BPM se basa en la gestión y mejora continua del proceso existente.
c) Ambos términos son sinónimos absolutos definidos por el estándar OMG.
d) El BPM es la notación gráfica y el BPR es el motor de ejecución tecnológica del software.

**Razonamiento Estructurado:**
1.  **Identifica los conceptos clave:**
    *   *BPR (Reengineering):* Reingeniería, romper con lo establecido y empezar de nuevo para un salto drástico en métricas.
    *   *BPM (Management):* Ciclo de vida completo, medir y mejorar continuamente (enfoque iterativo tipo Kaizen/PDCA).
2.  **Desmontando las opciones:** La opción A tiene las definiciones invertidas. La opción C es falsa. La opción D confunde BPM con BPMN (que sí es la notación) y BPMS (el motor). La opción B describe de forma precisa y exacta ambos conceptos.
3.  **Respuesta correcta: B.**

### 5.2. Simulacro de Test adicional

**Pregunta 4:**
*Un proceso BPMN necesita que, si una actividad de "Revisión de Documentación" tarda más de 48 horas sin completarse, se cancele automáticamente y el flujo se desvíe hacia una tarea de "Escalado a Supervisor". ¿Qué elemento BPMN modela correctamente este comportamiento?*
a) Un Evento de Temporizador de Inicio.
b) Un Evento de Borde de Temporizador interruptivo, adjunto a la actividad.
c) Un Evento de Borde de Temporizador no interruptivo, adjunto a la actividad.
d) Una Pasarela Basada en Eventos.

**Razonamiento Estructurado:**
1.  El Evento de Temporizador de Inicio (A) solo sirve para arrancar procesos en una fecha/ciclo, no para vigilar una actividad en curso. La Pasarela Basada en Eventos (D) se usa para bifurcar el flujo según qué evento ocurra primero, no para cancelar una actividad concreta.
2.  La clave del enunciado es que la actividad debe **cancelarse** ("se cancele automáticamente") si se supera el plazo: eso exige un evento de borde **interruptivo** (borde sólido), no uno no interruptivo (C), que dejaría continuar la actividad en paralelo.
3.  **Respuesta correcta: B.**

**Pregunta 5:**
*¿Qué notación del OMG se utiliza específicamente para modelar tablas de decisión y lógica de reglas de negocio de forma independiente y complementaria a un diagrama de proceso BPMN?*
a) UML.
b) DMN (Decision Model and Notation).
c) BPEL.
d) ArchiMate.

**Razonamiento Estructurado:**
1.  UML (A) modela software orientado a objetos, no reglas de decisión de negocio en tablas. BPEL (C) es un lenguaje de ejecución de procesos, no de modelado de decisiones. ArchiMate (D) es una notación de arquitectura empresarial, no de reglas de decisión.
2.  DMN es el estándar del OMG diseñado específicamente para modelar decisiones mediante tablas de decisión, complementando a BPMN mediante la Tarea de Regla de Negocio.
3.  **Respuesta correcta: B.**
