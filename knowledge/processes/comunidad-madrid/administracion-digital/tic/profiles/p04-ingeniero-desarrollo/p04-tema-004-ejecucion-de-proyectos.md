---
id: "cm-ad-tic-p04-tema-004-ejecucion-proyectos"
title: "Ejecución de proyectos"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/tic"
profiles:
  - "p04-ingeniero-desarrollo"
official_profile: "P04 - Ingeniero de Desarrollo"
official_topic: "Tema 4. Ejecución de proyectos"
source_ids:
tags:
  - "ejecucion-proyectos"
  - "roles"
  - "organizacion"
  - "metrica-v3"
  - "scrum"
created_at: "2026-08-08"
last_reviewed: null
ai_generated: true
ai_sources:
  - "gemini"
needs_human_review: true
---

# Tema 4. Ejecución de proyectos

## 1. Formas de Organización de los Proyectos

Como ingeniero de desarrollo, saber cómo está estructurado el poder en tu proyecto te ahorra muchos quebraderos de cabeza. En el test, suelen preguntar por el tipo de estructura organizativa. Hay tres patrones clásicos:

**Patrón Lógico - Tipos de Organización:**
1.  **Organización Funcional (Clásica):** Agrupación por especialidad (ej. todos los programadores en el "Departamento de Desarrollo", los de redes en "Sistemas"). El Jefe de Proyecto **apenas tiene autoridad**; manda el jefe del departamento funcional.
2.  **Organización Orientada a Proyectos:** Todo el equipo trabaja a tiempo completo en el proyecto y responden *exclusivamente* al Jefe de Proyecto. Éste tiene **autoridad total**.
3.  **Organización Matricial (La más común):** Mezcla las dos anteriores. El técnico de bases de datos tiene un jefe "funcional" (el de bases de datos) pero está asignado a un proyecto donde responde también a un Jefe de Proyecto (estructura "matricial"). Puede ser *débil* (el Jefe de Proyecto manda poco) o *fuerte* (el Jefe de Proyecto manda más).

---

## 2. Roles y Responsabilidades Clave

Los tribunales adoran preguntar por "quién hace qué". En el documento de Métrica v3 que usamos como referencia, hay perfiles muy bien delimitados [cite: 6]. 

**Patrón Lógico - Los 3 roles principales de Métrica v3 [cite: 6]:**
*   **Comité de Dirección:** Son los "jefazos". Ellos promueven los recursos iniciales y son los únicos que **aprueban los procesos formalmente** (ej. dan luz verde a iniciar el proyecto en la fase PSI y aprueban el paso a producción) [cite: 6].
*   **Comité de Seguimiento:** Su misión es el seguimiento "político" y la resolución de bloqueos importantes. Si hay un **cambio grave en los requisitos**, el Jefe de Proyecto lo propone, pero quien lo **aprueba** es el Comité de Seguimiento [cite: 6].
*   **Jefe de Proyecto:** El gestor real. Estima el esfuerzo, elabora la planificación (Gantt, PERT), asigna tareas, registra y analiza el impacto de las **incidencias**, y hace informes de seguimiento [cite: 6]. En Métrica v3 es quien "archiva la documentación de gestión" cuando termina el proyecto [cite: 6].

*(Nota Ágil - Scrum): Recuerda que en metodologías ágiles estos roles cambian [cite: 6]. El Scrum Master actúa como facilitador eliminando impedimentos técnicos del día a día, y el Product Owner es quien prioriza los requisitos de negocio [cite: 6].*

---

## 3. Gestión por Excepción

"Gestión por excepción" es una palabra *chivata* clarísima en el mundo de los proyectos y está íntimamente ligada a metodologías como **PRINCE2** [cite: 6].

**Patrón Lógico - ¿Qué significa "Por Excepción"?:**
*   **Regla general:** El Jefe de Proyecto tiene delegada cierta autoridad y unas tolerancias (ej. puede pasarse del presupuesto un 5% o retrasarse 2 días sin tener que pedir permiso arriba). Mientras el proyecto se mantenga dentro de esas tolerancias, el trabajo sigue normal.
*   **La Excepción:** Si surge una incidencia que va a superar esas tolerancias (ej. un retraso previsto de 10 días), se considera una "excepción". El Jefe de Proyecto debe detenerse, escalar el problema al Comité y proponer una solución.
*   **En el test:** Si el enunciado habla de "fijar tolerancias" y "solo informar o pedir permiso a la dirección cuando se van a superar esos límites", la respuesta correcta siempre se asocia a la **Gestión por excepción** y a metodologías estructuradas (PRINCE2) [cite: 6].

---

## 4. Adaptación al Entorno (Enfoque al producto vs. Enfoque al proyecto)

Es fundamental distinguir qué estamos construyendo (el producto) y cómo lo estamos construyendo (el proyecto). 

**Patrón Lógico de Enfoques:**
*   **Enfoque en el Producto:** Se centra en la calidad y especificaciones de lo que vas a entregar. Por ejemplo, en Métrica v3, el aseguramiento de la calidad verifica los *productos intermedios* que van saliendo para ver si cumplen la norma (ej. revisar un esquema de base de datos) [cite: 6]. 
*   **Enfoque en el Proyecto (Proceso):** Se centra en la maquinaria organizativa: cumplir plazos, medir el esfuerzo gastado, gestionar los riesgos y controlar el presupuesto.

**Adaptación al entorno (Sastrería / Tailoring):**
Ni Métrica v3 ni PMBOK son camisas de fuerza. La adaptación significa que, dependiendo de la magnitud del proyecto, el Jefe de Proyecto seleccionará el ciclo de vida y decidirá qué actividades o tareas son obligatorias y cuáles se pueden omitir o simplificar [cite: 6]. Métrica v3 dice explícitamente que sus perfiles deben "adaptarse y dimensionarse" según las características particulares de cada proyecto [cite: 6].

---

## 5. Ejemplo Real (Sin analogías)

Estás trabajando en un proyecto para lanzar una nueva App móvil del ayuntamiento para el pago de impuestos.

*   **Organización:** Trabajas en una "Organización Matricial". Tu jefe de departamento de desarrollo te evalúa anualmente, pero estás asignado al "Proyecto App Ayuntamiento" y recibes tareas del Jefe de Proyecto.
*   **El Producto vs. El Proyecto:** El código en Java que haces, la interfaz gráfica y los manuales de usuario son el **Producto**. El cronograma de entregas, la gestión de la sala de reuniones para las presentaciones y la solicitud de licencias de software para tu equipo, son parte del **Proyecto**.
*   **Gestión por Excepción:** El Jefe de Proyecto tiene margen para absorber retrasos menores a una semana. Un día te das cuenta de que integrar la pasarela de pagos del banco va a retrasar todo 3 semanas. El Jefe de Proyecto "levanta la mano" por **excepción** y escala el problema al Comité de Seguimiento [cite: 6] para ver si se retrasa la salida a producción o si se contrata temporalmente a un especialista. 

---

## 6. Patrones de Examen y "Palabras Chivatas"

| Concepto | Palabra Chivata en el Test |
| :--- | :--- |
| **Organización Matricial** | "Dos jefes", "Gerente funcional + Gerente de proyecto", "Combinación". |
| **Comité de Dirección (Métrica v3)** | "Autoridad final", "Aprueba proceso de desarrollo", "Paso a producción" [cite: 6]. |
| **Comité de Seguimiento (Métrica v3)** | "Resuelve contingencias", "Aprueba cambios de requisitos propuestos por el Jefe de Proyecto" [cite: 6]. |
| **Gestión por Excepción (PRINCE2)** | "Tolerancias", "Límites fijados", "Solo reportar si se superan", "Delegación de autoridad" [cite: 6]. |
| **Adaptación / Tailoring** | "Ajustar la metodología", "Dimensionar los perfiles según magnitud", "No todas las tareas son obligatorias" [cite: 6]. |

### 6.1. Simulacro de Test: Desmontando trampas

**Pregunta:**
*Durante el desarrollo de un nuevo sistema de información en un ministerio siguiendo la metodología Métrica v3, surge un cambio importante en la legislación que obliga a modificar una funcionalidad troncal del sistema. Una vez analizado el impacto y propuestos los cambios, ¿qué órgano o rol tiene la responsabilidad de aprobar esta petición de cambio de requisitos?*
a) El Comité de Dirección, ya que es el máximo órgano.
b) El Comité de Seguimiento.
c) El Jefe de Proyecto, como responsable técnico.
d) El Analista principal del proyecto.

**Razonamiento Estructurado:**
1.  **Busca la palabra chivata:** El enunciado pregunta expresamente "quién tiene la responsabilidad de aprobar una petición de cambio de requisitos" en Métrica v3. 
2.  **Aplica tu patrón lógico de roles:**
    *   (C) El Jefe de Proyecto es el que gestiona el día a día. Si hay un cambio, él propone la solución, calcula el esfuerzo y se lo *presenta* a un comité, pero no tiene potestad para autorizar cambios graves que afectan a presupuesto o alcance [cite: 6]. Falsa.
    *   (D) El Analista principal se encarga del trabajo técnico (diseñar el nuevo modelo) [cite: 6], no de la gestión presupuestaria o aprobaciones de alcance. Falsa.
    *   (A) El Comité de Dirección se encarga de los grandes hitos y aprobaciones *a nivel de proceso* general (como iniciar el proyecto en PSI o dar el visto bueno final al paso a producción en IAS) [cite: 6]. 
    *   (B) **El Comité de Seguimiento**. Nuestro patrón nos indica que, según Métrica v3, si hay un cambio de requisitos, se somete a la aprobación del Comité de Seguimiento, previo análisis del impacto en la planificación por parte del Jefe de Proyecto [cite: 6]. 
3.  **Respuesta correcta:** B.
