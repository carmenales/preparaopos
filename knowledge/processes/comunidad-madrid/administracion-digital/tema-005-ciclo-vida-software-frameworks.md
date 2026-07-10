---
id: "tema-005-ciclo-vida-software-frameworks"
title: "Ciclo de vida del software y frameworks"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital"
official_topic: "Tema 5. Ciclo de vida del software y frameworks"
source_ids: []
tags:
  - ciclo-de-vida-software
  - sdlc
  - agile
  - scrum
  - pruebas-software
  - istqb
  - ci-cd
  - java
  - spring
  - microservicios
created_at: "2026-07-10"
last_reviewed: null
ai_generated: true
ai_sources:
  - "perplexity"
  - "chatgpt"
  - "gemini"
needs_human_review: true
---

# Ciclo de vida del software y frameworks

## Encaje en la convocatoria

Este tema corresponde al **Tema 5 del Anexo 3** de la Resolución 352/2026 (BOCM 11/06/2026), específico para el perfil **P01 (IA aplicada al ciclo de vida del software)** de la Agencia para la Administración Digital de la Comunidad de Madrid. El perfil P02 tiene un Tema 5 diferente.

El epígrafe exige conocimientos técnicos profundos sobre cinco bloques: **fases del ciclo de vida del software**, **modelo tradicional y modelo agile**, **pruebas del software**, **integración y despliegue continuo (CI/CD)** y **frameworks del stack de Java (3 capas y microservicios)**. 

Para un examen tipo test con penalización, el objetivo es diferenciar terminología técnica oficial y estándares de la industria (ISO/IEC/IEEE 12207, ISO/IEC 14764, Glosario ISTQB, Scrum Guide 2020) frente a conceptos coloquiales. Son fuente de distractores clásicos las diferencias entre **Delivery vs. Deployment**, **Verificación vs. Validación**, **JPA vs. Hibernate**, los **roles de Scrum** (actualizados a la guía 2020) y los **tipos de mantenimiento** según la ISO 14764.

## Ideas clave

- **Ciclo de Vida (SDLC):** Abarca desde la concepción hasta la retirada del producto. La norma de referencia para los procesos del ciclo de vida es la **ISO/IEC/IEEE 12207**.
- **Mantenimiento (ISO/IEC 14764):** Se divide normativamente en cuatro tipos: Correctivo, Adaptativo, Perfectivo y Preventivo.
- **Modelos de Ciclo de Vida:** **Cascada** es secuencial; **Espiral** (Boehm) se centra cíclicamente en el análisis de riesgos; **Agile** es iterativo e incremental.
- **Agile vs. Scrum:** *Agile* es un marco filosófico (4 valores, 12 principios del Manifiesto de 2001). *Scrum* es un framework empírico concreto.
- **Pruebas (Verificación vs. Validación):** Verificación responde a "¿Estamos construyendo el producto correctamente?" (cumple especificaciones técnicas). Validación responde a "¿Estamos construyendo el producto correcto?" (resuelve la necesidad de negocio del usuario).
- **CI/CD:** En la *Entrega Continua (Continuous Delivery)* el software está listo para producción pero requiere aprobación manual. En el *Despliegue Continuo (Continuous Deployment)*, la promoción a producción es 100% automática tras superar los tests.
- **Stack Java (3 Capas):** Se organiza lógicamente en Presentación, Negocio y Datos. **Spring MVC** utiliza el patrón *Front Controller* a través de su `DispatcherServlet`. **JPA** es la especificación; **Hibernate** es la implementación.
- **Microservicios Cloud-Native:** Mientras Spring Boot lidera la creación de *Fat-JARs*, nuevos frameworks como **Quarkus** y **Micronaut** compiten mediante compilación *Ahead-Of-Time (AOT)* y **GraalVM** para reducir drásticamente el consumo de memoria y tiempo de arranque en contenedores.

## Desarrollo

### 1. Fases del ciclo de vida del software

El **SDLC (Software Development Life Cycle)** es el marco que define las tareas en cada fase de construcción y mantenimiento de un producto de software. La referencia internacional estándar es la **ISO/IEC/IEEE 12207** (y sus revisiones), que divide el ciclo en procesos primarios, de apoyo y organizacionales.

Fases técnicas y secuenciales clásicas (a nivel de proyecto):

1. **Ingeniería de Requisitos:** Elicitación, análisis, especificación y validación. Produce el Documento de Especificación de Requisitos (SRS, clásicamente regido por IEEE 830, sustituido por ISO/IEC/IEEE 29148).
2. **Análisis y Diseño:**
   * **Diseño Arquitectónico (Alto Nivel):** Definición de componentes, interfaces, persistencia y despliegue lógico.
   * **Diseño Detallado (Bajo Nivel):** Algoritmos, diagramas de clases, estructuras de datos.
3. **Construcción (Implementación):** Codificación y configuración del software siguiendo estándares y prácticas seguras.
4. **Verificación y Pruebas:** Comprobación sistemática de la calidad (QA) frente a los requisitos funcionales y no funcionales.
5. **Aceptación y Puesta en Servicio (Despliegue):** Transición del entorno de desarrollo/preproducción a producción y validación por el usuario.
6. **Operación y Mantenimiento:** Garantizar el funcionamiento continuo y evolución.
7. **Retirada (Disposal):** Fin de vida útil, migración de datos y eliminación segura del sistema.

#### 1.1. Tipos de Mantenimiento (ISO/IEC 14764)
Clasificación normativa, recurrente en exámenes:
* **Correctivo:** Corrección de fallos y defectos descubiertos en el software en producción.
* **Adaptativo:** Modificación de un producto para mantener su uso ante un cambio en su entorno operativo (ej. nueva versión del S.O. o cambio de gestor de base de datos).
* **Perfectivo:** Mejora del rendimiento, mantenibilidad o adición de nuevas funcionalidades (evolución a petición del usuario).
* **Preventivo:** Modificación proactiva para detectar y corregir fallos latentes antes de que se conviertan en fallos operativos reales.

#### 1.2. Requisitos de Ciclo de Vida Seguro (ENS - RD 311/2022)
El **Esquema Nacional de Seguridad** obliga (medida *mp.sw.1*) a que el ciclo de vida del software en el sector público integre seguridad desde el diseño, mínimo privilegio, separación estricta entre entornos de desarrollo y producción, y la no utilización de datos reales en pruebas sin anonimización.

### 2. Modelo tradicional y modelo agile

#### 2.1. Modelos Tradicionales (Predictivos)
* **Cascada (*Waterfall*):** Modelo secuencial estricto. Cada fase debe completarse y documentarse formalmente antes de comenzar la siguiente. Alta rigidez ante cambios de requisitos tardíos.
* **Modelo en V:** Variante de la cascada que asocia explícitamente cada fase de desarrollo con su correspondiente nivel de pruebas (Ej. Requisitos de usuario $\leftrightarrow$ Pruebas de aceptación; Diseño arquitectónico $\leftrightarrow$ Pruebas de integración). Su objetivo es planificar las pruebas desde el inicio.
* **Espiral (Boehm):** Modelo evolutivo en ciclos. **Diferenciador clave para test:** Es el único modelo clásico centrado explícitamente en el **análisis iterativo de riesgos** en cada vuelta de la espiral.

#### 2.2. Modelo Agile (Adaptativo)
Basado en el **Manifiesto Ágil (2001)**. Se rige por 4 valores fundamentales (trampa típica de examen: Agile prefiere el primer elemento, pero no elimina el segundo):
1. **Individuos e interacciones** sobre procesos y herramientas.
2. **Software funcionando** sobre documentación exhaustiva.
3. **Colaboración con el cliente** sobre negociación contractual.
4. **Respuesta ante el cambio** sobre seguir un plan.

#### 2.3. Scrum (Guía 2020)
Es un *framework* empírico (basado en transparencia, inspección y adaptación) para abordar problemas complejos.
* **El Scrum Team (Roles):** No hay jerarquías.
  * **Product Owner:** Único responsable de maximizar el valor del producto y de gestionar/priorizar el *Product Backlog*.
  * **Scrum Master:** Líder servicial. Asegura la comprensión de Scrum y elimina impedimentos organizacionales.
  * **Developers:** Personas comprometidas con la creación del Incremento. *(Nota de test: El concepto "Development Team" desapareció en la guía de 2020).*
* **Artefactos y Compromisos:**
  * **Product Backlog** (Compromiso: *Product Goal*).
  * **Sprint Backlog** (Compromiso: *Sprint Goal*).
  * **Incremento** (Compromiso: *Definition of Done*).
* **Eventos:** *Sprint* (contenedor de máximo 1 mes), *Sprint Planning*, *Daily Scrum* (15 minutos, para inspeccionar el progreso hacia el Sprint Goal, exclusivo para Developers), *Sprint Review* (inspección del incremento con stakeholders) y *Sprint Retrospective* (inspección del equipo y sus procesos).

#### 2.4. Kanban
Marco basado en la gestión visual del flujo de valor continuo. A diferencia de Scrum, no prescribe Sprints de duración fija ni roles específicos, pero exige **limitar el trabajo en progreso (WIP - *Work In Progress*)** para evitar cuellos de botella.

### 3. Pruebas del software

Las definiciones técnicas estándar emanan del glosario **ISTQB** (*International Software Testing Qualifications Board*).
* **Error:** Acción humana equivocada (ej. el analista malinterpreta una norma).
* **Defecto / Bug:** Imperfección en el código fruto de un error humano.
* **Fallo:** Manifestación física u observable del defecto durante la ejecución del software.

#### 3.1. Niveles de Prueba
1. **Unitarias / De componente:** Verifican unidades pequeñas de código (métodos/clases) de forma aislada. Típicamente automatizadas por los desarrolladores (ej. JUnit).
2. **Pruebas de Integración:** Comprueban la interfaz y comunicación entre componentes internos (ej. Servicio y Repositorio) o con sistemas externos.
3. **Pruebas de Sistema:** Validan el comportamiento end-to-end del sistema completo integrado, evaluando requisitos funcionales y no funcionales (rendimiento, seguridad, etc.).
4. **Pruebas de Aceptación (UAT):** Verifican que el sistema cumple con las necesidades del cliente/negocio. Suelen ejecutarse por el usuario final antes de dar por buena la entrega.

#### 3.2. Técnicas de Diseño de Pruebas
* **Caja Blanca (Estructurales):** Se diseñan conociendo el código fuente y la arquitectura interna. Miden la **cobertura** (cobertura de sentencias, cobertura de ramas/decisiones, complejidad ciclomática de McCabe).
* **Caja Negra (Basadas en especificación):** Diseñadas sin ver el código, centradas puramente en las entradas y las salidas esperadas. *Técnicas típicas:* Partición de equivalencia, análisis de valores límite y tablas de decisión.

#### 3.3. Pruebas Dinámicas vs. Estáticas
* **Estáticas:** Se realizan **sin ejecutar** el código (ej. revisiones por pares, análisis estático de código, herramientas tipo SonarQube o SAST).
* **Dinámicas:** Requieren la ejecución física del software.

### 4. Integración y despliegue continuo (CI/CD)

Conjunto de prácticas fundamentales en el paradigma **DevOps/DevSecOps** orientadas a la industrialización del ciclo de vida del software.

* **Integración Continua (CI - *Continuous Integration*):** Los desarrolladores suben código frecuentemente a un repositorio central (ej. Git). Cada *commit* dispara una canalización (*pipeline*) automática que compila el código, pasa herramientas de análisis estático (linting, SAST) y ejecuta pruebas unitarias. **Objetivo:** Detectar defectos de integración de inmediato.
* **Entrega Continua (CD - *Continuous Delivery*):** Extiende la CI automatizando la promoción del artefacto compilado a entornos de preproducción. Garantiza que el código está empaquetado y "listo para desplegar". **Diferencia clave:** Requiere una **aprobación humana (clic manual)** para el paso final a producción.
* **Despliegue Continuo (CD - *Continuous Deployment*):** Automatización del 100% del pipeline. Si los tests automáticos son exitosos, el cambio pasa a producción **sin ninguna intervención humana**.

#### 4.1. Estrategias de Despliegue en Producción
* **Blue/Green Deployment:** Se mantienen dos entornos idénticos. El tráfico se redirige instantáneamente del Blue (producción actual) al Green (nueva versión) a nivel de enrutador/balanceador. Facilita un *rollback* inmediato.
* **Canary Release:** El nuevo código se despliega a un porcentaje pequeño de usuarios (ej. 5%) para monitorear errores. Si es estable, se amplía progresivamente al 100%. Orientado a la mitigación gradual de riesgos.

### 5. Frameworks de Java (3 capas y microservicios)

En la Administración Pública, Java empresarial (**Jakarta EE** y ecosistema **Spring**) constituye la pila tecnológica predominante.

#### 5.1. Arquitectura de 3 Capas
Patrón lógico para segregar responsabilidades y reducir el acoplamiento.
1. **Capa de Presentación:** Gestión de interfaces, controladores REST y validación de sintaxis de entrada. **Patrón MVC:** Separa el Modelo (datos), la Vista (representación) y el Controlador. En Spring MVC, el componente núcleo es el **`DispatcherServlet`** que actúa como *Front Controller* para enrutar todas las peticiones HTTP.
2. **Capa de Negocio (Business/Service):** Aloja las reglas de dominio, los casos de uso y la gestión de transacciones. No debe depender de la tecnología web ni de la base de datos subyacente.
3. **Capa de Persistencia / Acceso a Datos:** Realiza operaciones de entrada/salida sobre el almacenamiento. 
   * **JPA (Jakarta Persistence API):** Es la **especificación** estándar de Java para mapeo objeto-relacional (ORM). 
   * **Hibernate:** Es la **implementación** técnica más extendida de la especificación JPA.
   * **Spring Data JPA:** Es una abstracción de alto nivel de Spring que simplifica la creación de repositorios de datos evitando código repetitivo (*boilerplate*).

#### 5.2. Ecosistema Spring y Microservicios
Un microservicio es una unidad de software autónoma, centrada en un dominio de negocio específico, desplegable independientemente y que se comunica a través de contratos ligeros (HTTP/REST, gRPC, Eventos).

* **Spring Framework:** Núcleo tecnológico basado en dos principios fundamentales:
  * **Inversión de Control (IoC):** El framework dirige el flujo y gestiona el ciclo de vida de los objetos (Beans) mediante un contenedor (`ApplicationContext`).
  * **Inyección de Dependencias (DI):** El contenedor proporciona a un objeto sus dependencias sin que el objeto tenga que instanciarlas directamente, reduciendo el acoplamiento.
* **Spring Boot:** Subproyecto que aplica la *convención sobre configuración*. Permite crear aplicaciones autónomas empaquetando el servidor web (Tomcat, Jetty o Undertow) directamente en el compilado, generando un ejecutable único (**Fat-JAR**).
* **Spring Cloud:** Conjunto de librerías para gobernar sistemas distribuidos. Provee patrones como *API Gateway*, *Service Discovery* (Eureka) y resiliencia ante fallos (*Circuit Breaker* mediante Resilience4j).
* **Jakarta EE y MicroProfile:** Alternativa estándar promovida por Eclipse Foundation. Define especificaciones corporativas (Jakarta REST, CDI, Security). Eclipse MicroProfile optimiza Jakarta EE para arquitecturas de microservicios (Fault Tolerance, Metrics, JWT).

#### 5.3. Evolución Cloud-Native (AOT Compilation)
El ecosistema Spring tradicional usa intensivamente la reflexión (*reflection*) y el escaneo de *classpath* en tiempo de ejecución, lo que implica arranques lentos (*cold starts*) y alto consumo de memoria RAM, problemático en arquitecturas contenerizadas/Serverless.
Para solucionar esto, frameworks modernos como **Quarkus** y **Micronaut** (y más recientemente Spring Boot 3) realizan la inyección de dependencias y configuración en **tiempo de compilación (AOT - Ahead-Of-Time)** y utilizan **GraalVM** para compilar código Java en binarios nativos ligeros y extremadamente rápidos.

## Conceptos que suelen preguntarse

| Concepto a evaluar | Realidad técnica y normativa | Distractor típico en examen |
| :--- | :--- | :--- |
| **Delivery vs. Deployment (CD)** | Delivery = Paso a producción manual. Deployment = Paso automático. | "Despliegue Continuo siempre requiere confirmación por el Product Owner". |
| **Verificación vs. Validación** | Verificación = Cumplir requisitos técnicos (construir bien). Validación = Satisfacer necesidad del usuario (construir lo correcto). | "Son sinónimos definidos por el estándar ISTQB". |
| **Scrum Roles** | Product Owner (Maximiza valor/Backlog), Scrum Master, Developers. | "El Project Manager asigna las tareas diarias a los programadores". |
| **JPA vs. Hibernate** | JPA = Especificación oficial (API). Hibernate = Implementación de la API. | "Hibernate es una especificación y JPA es su implementación". |
| **Spring Framework MVC** | Basa su enrutamiento en el patrón *Front Controller* (`DispatcherServlet`). | "Spring MVC mezcla la lógica de negocio directamente en las vistas". |
| **Mantenimiento Adaptativo** | Se hace para que el software siga funcionando tras un cambio en su entorno (ej. S.O.). | "Consiste en arreglar un error descubierto en producción (eso es Correctivo)". |
| **Caja Blanca** | Mide cobertura lógica interna (caminos, sentencias, McCabe). | "Se centra en probar casos de uso desde la interfaz gráfica del usuario". |

## Posibles preguntas tipo test

**Pregunta 1.** Según la norma ISO/IEC 14764 sobre mantenimiento de software, la modificación de un producto software después de su entrega para mantener su operatividad funcional cuando se actualiza el sistema operativo subyacente del servidor se denomina:
A. Mantenimiento correctivo.
B. Mantenimiento preventivo.
C. Mantenimiento adaptativo.
D. Mantenimiento perfectivo.
**Respuesta correcta: C.** (La adaptación a cambios del entorno operativo, sin cambiar la funcionalidad base, es mantenimiento adaptativo).

**Pregunta 2.** En el contexto de los procesos de Integración y Despliegue Continuo (CI/CD), ¿cuál es la diferencia técnica fundamental entre *Continuous Delivery* (Entrega Continua) y *Continuous Deployment* (Despliegue Continuo)?
A. La Entrega Continua despliega automáticamente en producción, mientras que el Despliegue Continuo no.
B. En el Despliegue Continuo (Deployment) toda la promoción a producción es automática si se superan los tests, mientras que la Entrega Continua (Delivery) requiere una aprobación manual explícita para el paso final a producción.
C. La Entrega Continua utiliza pipelines de código, mientras que el Despliegue Continuo requiere despliegue mediante USB físico.
D. No existe diferencia, ambos términos son sinónimos absolutos definidos por la ISO/IEC 12207.
**Respuesta correcta: B.**

**Pregunta 3.** Según la Guía Scrum 2020, ¿quién es el único rol responsable y con autoridad para gestionar y priorizar los elementos del Product Backlog con el objetivo de maximizar el valor del producto?
A. El Scrum Master.
B. El Equipo de Desarrolladores (Developers) por consenso.
C. El Product Owner.
D. El Jefe de Proyecto (Project Manager).
**Respuesta correcta: C.** (El Product Owner gestiona en exclusiva el Product Backlog).

**Pregunta 4.** En el ámbito del diseño de pruebas de software, aquellas técnicas que derivan sus casos de prueba analizando el código fuente, la estructura interna y buscando métricas como la cobertura de sentencias o caminos, se denominan:
A. Técnicas de Caja Negra.
B. Pruebas Exploratorias empíricas.
C. Técnicas de Partición de Clases de Equivalencia.
D. Técnicas de Caja Blanca o estructurales.
**Respuesta correcta: D.** (Las técnicas de Caja Blanca requieren conocimiento y acceso a la estructura interna del código).

**Pregunta 5.** El patrón de diseño arquitectónico sobre el cual pivota el framework Spring Web MVC para canalizar todas las peticiones HTTP entrantes hacia el componente adecuado mediante el objeto `DispatcherServlet` se denomina:
A. Data Access Object (DAO).
B. Object-Relational Mapping (ORM).
C. Front Controller (Controlador Frontal).
D. Circuit Breaker.
**Respuesta correcta: C.** (El Front Controller centraliza el manejo de todas las peticiones de entrada; en Spring esto lo hace el DispatcherServlet).

**Pregunta 6.** En el ecosistema Java empresarial, ¿cuál es la relación técnica correcta entre las tecnologías de acceso a base de datos JPA e Hibernate?
A. JPA es una implementación concreta y propietaria, mientras que Hibernate es el estándar oficial del W3C.
B. JPA (Jakarta Persistence API) es la especificación estándar para mapeo objeto-relacional (ORM), e Hibernate es la implementación técnica más extendida de dicha especificación.
C. Son tecnologías opuestas e incompatibles diseñadas para arquitecturas distintas.
D. JPA se encarga exclusivamente de las bases de datos NoSQL e Hibernate de las bases de datos relacionales SQL.
**Respuesta correcta: B.**

**Pregunta 7.** Frente a las limitaciones de consumo de memoria y tiempos de arranque del ecosistema Spring tradicional en arquitecturas Cloud-Native (Serverless/Contenedores), la principal innovación tecnológica que introducen frameworks modernos como Quarkus o Micronaut es:
A. El uso exclusivo de XML para toda su configuración de Beans.
B. El procesamiento de la inyección de dependencias en tiempo de compilación (AOT) y la compilación a binarios nativos ligeros mediante GraalVM.
C. La ejecución obligatoria en servidores pesados como WebSphere o WebLogic.
D. La eliminación total de la necesidad de acceder a bases de datos.
**Respuesta correcta: B.** (El procesamiento Ahead-Of-Time reduce el uso de *reflection* en tiempo de ejecución, habilitando arranques casi instantáneos).

## Normativa o fuentes relacionadas

* **ISO/IEC/IEEE 12207:2017/2026:** *Systems and software engineering — Software life cycle processes.* Norma internacional matriz para el ciclo de vida del software.
* **ISO/IEC 14764:2006:** *Software Engineering — Software Life Cycle Processes — Maintenance.* Define los 4 tipos de mantenimiento de software.
* **Guía Scrum 2020** (Ken Schwaber y Jeff Sutherland). Documento oficial y definitivo de las reglas de Scrum.
* **ISTQB Foundation Level Syllabus (v4.0):** Estándar de la industria en terminología, procesos y niveles de pruebas de software.
* **Manifiesto por el Desarrollo Ágil de Software (2001):** Sus 4 valores y 12 principios rectores.
* **Real Decreto 311/2022 (Esquema Nacional de Seguridad):** Obligaciones de desarrollo de aplicaciones seguro (medida *mp.sw.1*), separación de entornos y uso de datos de prueba en la Administración.
* **Jakarta EE Specifications:** Definiciones formales empresariales (Servlet, JPA/Jakarta Persistence, CDI).

## Dudas o puntos pendientes

* **Mantenimiento Perfectivo vs. Preventivo:** En cierta bibliografía antigua, la refactorización (mejora de código sin añadir funcionalidad) se clasificaba como perfectiva. Normativamente (ISO 14764), si el objetivo es prevenir problemas futuros detectando fallos latentes, es preventivo; el perfectivo se ciñe a nuevas funcionalidades o mejora explícita de rendimiento solicitada. En exámenes tipo test de la Comunidad de Madrid suele predominar el enfoque estricto ISO.
* **Alcance de la versión de ISO 12207:** La ISO/IEC/IEEE 12207 fue revisada en 2017 y tiene proyecciones recientes, pero la estructura de procesos primarios, de apoyo y organizacionales varía ligeramente según la edición específica consultada. A efectos de oposiciones TIC, los tribunales suelen quedarse en la clasificación clásica (Adquisición, Suministro, Desarrollo, Operación y Mantenimiento como procesos primarios).