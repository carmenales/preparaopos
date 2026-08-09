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

## 2. Modelado Dinámico de Sistemas (UML)

En el ámbito de la Ingeniería de Software, el Lenguaje Unificado de Modelado (UML) proporciona varios diagramas de comportamiento (dinámicos) para representar cómo cambia el sistema a lo largo del tiempo:

*   **Diagrama de Actividades:** Muestra el flujo de control o flujo de datos paso a paso. Es el equivalente UML a un diagrama de flujo tradicional y precursor de lo que hoy es BPMN para negocio.
*   **Diagrama de Estados (Máquina de Estados):** Muestra los diferentes estados por los que pasa un objeto durante su ciclo de vida y los eventos que provocan las transiciones de un estado a otro.
*   **Diagrama de Secuencia:** Muestra cómo los objetos interactúan entre sí y el orden temporal en que se intercambian los mensajes. Es fundamental para diseñar el comportamiento de los Casos de Uso.
*   **Diagrama de Tiempos:** Se centra específicamente en las restricciones de tiempo y la duración de los eventos (muy usado en sistemas empotrados o de tiempo real).

## 3. BPMN (Business Process Model and Notation)

BPMN es el estándar internacional *de facto* para el modelado de procesos de negocio. Está mantenido por el **OMG (Object Management Group)** y su versión actual estandarizada por ISO es **BPMN 2.0.2 (ISO/IEC 19510)**.

Su objetivo principal es proveer una notación gráfica fácilmente comprensible por todos los usuarios del negocio (desde los analistas que crean los borradores, hasta los desarrolladores técnicos que implementan la tecnología, y los gerentes que monitorean los resultados), sirviendo como lenguaje común para cerrar la brecha entre el diseño del negocio y su implementación.

### 3.1. Tipos de Modelos en BPMN 2.0

Una pregunta clásica de examen es distinguir los tres tipos de diagramas que soporta BPMN 2.0:

1.  **Procesos de Orquestación (Orchestration):** Representan un proceso privado interno de una organización o departamento (todo ocurre dentro de un único Pool).
2.  **Procesos de Colaboración (Collaboration):** Muestran las interacciones entre dos o más entidades de negocio independientes (dos o más Pools). Se representan mediante flujos de mensajes entre los participantes.
3.  **Coreografía (Choreography):** Formaliza la forma en que los participantes coordinan sus interacciones. El enfoque no está en el trabajo interno de un participante, sino en el **intercambio de mensajes** entre ellos, sin que exista un controlador central.



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
| **OMG (Object Management Group)** | "Organización responsable del estándar BPMN y UML". |
| **Flujo de Secuencia** | "Línea continua", "**NUNCA** cruza límites de un Pool". |
| **Flujo de Mensajes** | "Línea discontinua", "**SIEMPRE** cruza límites de un Pool (entre participantes)". |
| **Gateway Exclusivo (XOR)** | "Rombo vacío o con X", "Caminos mutuamente excluyentes", "Solo un camino válido". |
| **Gateway Inclusivo (OR)** | "Rombo con un círculo interno O", "Uno o varios caminos válidos simultáneos". |
| **Pool vs Lane** | Pool = Participante / Organización entera; Lane = Departamento / Rol específico interno. |
| **Coreografía (Choreography)** | "Sin controlador central", "Enfocado en el intercambio de mensajes entre participantes". |
| **AS-IS / TO-BE** | "AS-IS = Situación actual (cómo es)", "TO-BE = Situación futura tras reingeniería". |

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