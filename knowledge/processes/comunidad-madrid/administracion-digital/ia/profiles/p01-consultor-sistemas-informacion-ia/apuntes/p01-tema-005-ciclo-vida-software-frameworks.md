---
id: "cm-ad-ia-p01-tema-005-ciclo-vida-software-frameworks"
title: "Ciclo de vida del software y frameworks"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/ia"
profiles:
  - "p01-consultor-sistemas-informacion-ia"
official_profile: "P01 - Consultor de Sistemas de Información - IA Aplicada al Ciclo de Vida del Software"
official_topic: "Tema 5. Ciclo de vida del software y frameworks"
source_ids:
tags:
  - "ciclo-de-vida-software"
  - "sdlc"
  - "agile"
  - "scrum"
  - "pruebas-software"
  - "istqb"
  - "ci-cd"
  - "java"
  - "spring"
  - "microservicios"
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

Este tema corresponde al **Tema 5 del Anexo 3** de la Resolución 352/2026 (BOCM 11/06/2026), específico para el perfil **P01 – IA aplicada al ciclo de vida del software** de la Agencia para la Administración Digital de la Comunidad de Madrid. El perfil P02 tiene un Tema 5 diferente.

El epígrafe exige conocimientos técnicos profundos en cinco bloques: **fases del ciclo de vida del software**, **modelos tradicionales y agile**, **pruebas del software**, **integración y despliegue continuo (CI/CD)** y **frameworks del stack Java (arquitectura en capas y microservicios)**, conectando con preguntas de examen sobre Scrum, CI/CD, DevOps, Spring, JPA/Hibernate, BDD y métricas de pruebas.

## Ideas clave

- **Ciclo de Vida (SDLC):** Abarca desde la concepción hasta la retirada del producto; la norma matriz de procesos es **ISO/IEC/IEEE 12207**, que organiza procesos de ciclo de vida en primarios, de apoyo y organizacionales.
- **Mantenimiento (ISO/IEC 14764):** Se clasifica normativamente en cuatro tipos: **correctivo, adaptativo, perfectivo y preventivo**, y las preguntas de examen suelen centrar la atención en la distinción entre adaptativo y correctivo.
- **Modelos de ciclo de vida:** **Cascada** es secuencial y rígido; el **Modelo en V** vincula fases de desarrollo con niveles de prueba; la **Espiral de Boehm** enfatiza el **análisis iterativo de riesgos**; los modelos **ágiles** son iterativos e incrementales.
- **Agile vs Scrum:** Agile es el marco filosófico (Manifiesto ágil de 2001 con 4 valores y 12 principios); Scrum es un framework empírico concreto definido por la **Guía Scrum 2020**, con roles, artefactos y eventos bien delimitados.
- **Pruebas (Verificación vs Validación):** Verificación responde a “¿Estamos construyendo el producto correctamente?”; validación responde a “¿Estamos construyendo el producto correcto?”, siguiendo terminología **ISTQB**.
- **CI/CD:** La **Integración Continua (CI)** detecta pronto defectos de integración; en **Continuous Delivery** el paso a producción requiere aprobación humana; en **Continuous Deployment** la promoción a producción es 100 % automática tras superar los tests.
- **Stack Java (3 capas):** Separación en presentación, negocio y datos; **Spring MVC** utiliza el patrón **Front Controller** mediante el `DispatcherServlet`; **JPA** es la especificación estándar y **Hibernate** su implementación más extendida.
- **Microservicios cloud‑native:** Spring Boot facilita *fat‑JARs* autoejecutables; frameworks como **Quarkus** y **Micronaut**, combinados con **GraalVM**, usan compilación **Ahead‑Of‑Time (AOT)** y binarios nativos para reducir memoria y tiempos de arranque en contenedores.

## Desarrollo

### 1. Fases del ciclo de vida del software

El **Software Development Life Cycle (SDLC)** describe el conjunto de procesos para producir, mantener y retirar software, basándose en normas como **ISO/IEC/IEEE 12207**. A nivel proyecto, suele representarse en fases:

1. **Ingeniería de requisitos:**
   - Elicitación, análisis, especificación y validación de requisitos.
   - Produce un documento de requisitos (SRS), históricamente regido por IEEE 830 y hoy por ISO/IEC/IEEE 29148.
2. **Análisis y diseño:**
   - Diseño arquitectónico (alto nivel): componentes, interfaces, despliegue lógico.
   - Diseño detallado (bajo nivel): algoritmos, clases, estructuras de datos.
3. **Construcción (implementación):** Codificación y configuración del software siguiendo estándares de calidad y seguridad.
4. **Verificación y pruebas:** Asegurar que el producto cumple requisitos funcionales y no funcionales (rendimiento, seguridad, usabilidad).
5. **Aceptación y puesta en servicio:** Validación por el usuario y transición a producción.
6. **Operación y mantenimiento:** Explotación continua y evolución del sistema.
7. **Retirada (disposal):** Fin de vida útil, migración de datos, desmantelamiento y eliminación segura.

#### 1.1. Tipos de mantenimiento (ISO/IEC 14764)

Clasificación normativa recurrente en oposición:

- **Correctivo:** modificación para corregir errores detectados en el software en producción (fallos observados).
- **Adaptativo:** cambios para mantener la operatividad del software ante variaciones del entorno (nuevo sistema operativo, nueva BBDD) sin modificar la funcionalidad objetivo.
- **Perfectivo:** mejoras de rendimiento, mantenibilidad o ampliación funcional a petición del usuario.
- **Preventivo:** acciones proactivas para detectar y corregir defectos latentes antes de que se conviertan en fallos operativos.

El examen P01 destaca el mantenimiento **adaptativo** cuando el ejemplo se refiere explícitamente a cambios en el entorno (como actualización del sistema operativo o cambio de gestor de BBDD).

#### 1.2. Ciclo de vida seguro según ENS

El **Esquema Nacional de Seguridad (RD 311/2022)** establece que el ciclo de vida del software debe integrar seguridad desde el diseño, separación entre entornos, uso de datos de prueba y mínimo privilegio en la Administración. La medida **mp.sw.1** se refiere a requisitos de desarrollo de aplicaciones seguras, y el ENS subraya que la seguridad es un **proceso integral** que abarca elementos humanos, técnicos, organizativos y jurídicos.

### 2. Modelos de ciclo de vida: tradicionales y ágiles

#### 2.1. Modelos tradicionales (predictivos)

- **Cascada (Waterfall):** fases secuenciales, cada una debe completarse y documentarse antes de pasar a la siguiente; poca tolerancia a cambios tardíos.
- **Modelo en V:** relaciona cada fase de desarrollo con su nivel de prueba correspondiente (requisitos ↔ pruebas de aceptación; diseño ↔ pruebas de integración), para planificar las pruebas desde el inicio.
- **Espiral de Boehm:** modelo evolutivo que integra prototipado y análisis de riesgos en cada iteración; su rasgo distintivo en examen es el **foco explícito y continuo en la gestión de riesgos**.

#### 2.2. Modelo ágil

El **Manifiesto Ágil (2001)** define 4 valores:

1. Individuos e interacciones sobre procesos y herramientas.
2. Software funcionando sobre documentación exhaustiva.
3. Colaboración con el cliente sobre negociación contractual.
4. Respuesta ante el cambio sobre seguir un plan.

Los principios ágiles fomentan entregas frecuentes, adaptación continua y colaboración estrecha con el cliente; Agile es un paraguas que incluye frameworks como Scrum, Kanban, XP, etc.

#### 2.3. Scrum (Guía Scrum 2020)

Scrum es un framework empírico basado en transparencia, inspección y adaptación.

- **Roles del Scrum Team:**
  - **Product Owner:** responsable de maximizar el valor del producto y gestionar/priorizar el Product Backlog; es el único con autoridad sobre el Backlog.
  - **Scrum Master:** líder servicial que asegura que Scrum se entiende y aplica correctamente, eliminando impedimentos.
  - **Developers:** miembros comprometidos con crear el Incremento; el término “Development Team” desaparece en la Guía 2020.
- **Artefactos y compromisos:**
  - **Product Backlog** – compromiso: Product Goal.
  - **Sprint Backlog** – compromiso: Sprint Goal.
  - **Incremento** – compromiso: Definition of Done.
- **Eventos:**
  - **Sprint:** contenedor de máximo 1 mes.
  - **Sprint Planning, Daily Scrum (15 min, inspectar progreso hacia el Sprint Goal, solo Developers), Sprint Review, Sprint Retrospective.**

Los exámenes preguntan también por el **Burndown Chart**: una tendencia ascendente continuada indica incremento del trabajo pendiente, por reestimaciones o incorporación de nuevas tareas.

#### 2.4. Kanban

Kanban gestiona flujo continuo mediante un tablero visual (columnas como “Por hacer”, “En progreso”, “Hecho”), sin Sprints ni roles prescriptivos. Su práctica central es **limitar el trabajo en progreso (WIP)** para evitar cuellos de botella y favorecer un flujo estable.

### 3. Pruebas del software

La terminología estándar se basa en el glosario **ISTQB Foundation**.

- **Error:** acción humana equivocada (ej. analista interpreta mal una norma).
- **Defecto (bug):** imperfección en el artefacto de software debida a un error.
- **Fallo:** manifestación de un defecto durante la ejecución.

#### 3.1. Niveles de prueba

1. **Unitarias/de componente:** prueban unidades pequeñas de código (métodos, clases) de forma aislada; los desarrolladores las automatizan, típicamente con **JUnit**.
2. **Integración:** verifican interfaces y comunicación entre componentes internos (Servicio–Repositorio) o con sistemas externos.
3. **Sistema:** evalúan comportamiento end‑to‑end del sistema completo integrado, incluyendo requisitos funcionales y no funcionales (rendimiento, seguridad).
4. **Aceptación (UAT):** validan que el sistema satisface las necesidades del usuario/negocio; suelen ser ejecutadas por el cliente antes de la puesta en producción.

#### 3.2. Diseño de pruebas: caja negra y caja blanca

- **Caja negra (basadas en especificación):** diseñadas sin ver el código, centradas en entradas/salidas; técnicas típicas:
  - Partición de clases de equivalencia.
  - Análisis de valores límite.
  - Tablas de decisión.
- **Caja blanca (estructurales):** diseñadas analizando código y estructura interna; miden:
  - Cobertura de sentencias.
  - Cobertura de decisiones/ramas.
  - Complejidad ciclomática (McCabe).

#### 3.3. Pruebas estáticas vs dinámicas

- **Pruebas estáticas:** sin ejecutar el código (revisiones por pares, inspecciones, análisis estático con herramientas SAST/SonarQube).
- **Pruebas dinámicas:** requieren ejecutar el software para observar comportamientos.

#### 3.4. Cobertura, JaCoCo y mocking

En Java, herramientas como **JaCoCo** permiten medir:

- Cobertura de instrucciones.
- Cobertura de ramas.
- Complejidad ciclomática.

No miden cobertura de asserts correctos/erróneos como métrica específica, punto que aparece en preguntas.

Para pruebas unitarias aisladas, librerías como **Mockito** permiten simular el comportamiento de dependencias no implementadas (mocks), lo que es clave en preguntas de examen sobre testing en Java.

### 4. Integración y despliegue continuo (CI/CD) y prácticas DevOps

La cultura **DevOps/DevSecOps** busca integrar desarrollo, operaciones y seguridad, automatizando el ciclo de vida.

#### 4.1. CI, Continuous Delivery y Continuous Deployment

- **Integración Continua (CI):**
  - Los desarrolladores integran cambios frecuentemente en una rama principal.
  - Cada commit dispara un pipeline que compila, analiza estáticamente y ejecuta pruebas unitarias.
- **Continuous Delivery (Entrega continua):**
  - El artefacto está siempre listo para desplegar; se automatiza hasta preproducción.
  - El paso final a producción requiere **aprobación manual explícita**.
- **Continuous Deployment (Despliegue continuo):**
  - La promoción a producción está automatizada; si los tests pasan, se despliega sin intervención humana.

#### 4.2. Estrategias de despliegue

- **Blue/Green Deployment:** dos entornos idénticos; se redirige tráfico de Blue (versión actual) a Green (nueva versión) mediante el balanceador, facilitando rollback inmediato.
- **Canary Release:** despliegue progresivo de la nueva versión a un subconjunto de usuarios, aumentando porcentaje si el comportamiento es correcto.

#### 4.3. Imágenes Docker y reconstrucción de capas

En pipelines donde la imagen Docker es muy pesada, la estrategia adecuada es:

- Separar componentes estáticos y pesados en una **imagen base versionada**, publicar en el Container Registry y construir la imagen de aplicación sobre esa base, reconstruyendo solo las capas que cambian.

Esto mejora tiempos de build, mantiene trazabilidad (versión de imagen base) y facilita mantenibilidad.

#### 4.4. Trunk‑based development y métricas DORA

- **Trunk‑based development:** práctica donde los desarrolladores integran de forma frecuente cambios en una única rama principal (trunk), apoyándose en automatización de pruebas para evitar inestabilidad. Minimiza ramas largas y favorece entregas continuas.
- **Métricas DORA:** conjunto de indicadores de rendimiento DevOps (frecuencia de despliegue, tiempo de entrega de cambios, tasa de fallo en cambios, tiempo de recuperación), recomendadas para medir el retorno del uso de IA y automatización en el ciclo de vida.

### 5. Frameworks Java, arquitectura por capas y microservicios

Java empresarial (Jakarta EE, Spring) sigue siendo dominante en la Administración pública.

#### 5.1. Arquitectura de 3 capas

Patrón lógico para separar responsabilidades:

1. **Presentación:**
   - Interfaces de usuario (JSF, HTML/JS, REST controllers).
   - Validación sintáctica de entrada.
   - En Spring MVC, el `DispatcherServlet` actúa como **Front Controller**, centralizando y enrutando peticiones HTTP al controlador adecuado.
2. **Negocio (Service):**
   - Reglas de dominio, casos de uso, orquestación de transacciones.
   - No debe depender directamente de detalles de presentación o almacenamiento.
3. **Persistencia/acceso a datos:**
   - Repositorios y DAOs para operaciones sobre BBDD.
   - **JPA (Jakarta Persistence API):** especificación estándar de mapeo objeto‑relacional.
   - **Hibernate:** implementación concreta más extendida de JPA.
   - **Spring Data JPA:** abstracción que simplifica repositorios, reduciendo código repetitivo.

Examen P01 pregunta explícitamente por la relación correcta entre JPA e Hibernate: JPA es el estándar, Hibernate la implementación.

#### 5.2. Ecosistema Spring y inyección de dependencias

- **Spring Framework:**
  - **IoC (Inversión de control):** el contenedor (`ApplicationContext`) crea y gestiona beans.
  - **DI (Inyección de dependencias):** Spring inyecta dependencias en constructores, setters o atributos, reduciendo acoplamiento.
- Anotaciones clave:
  - `@Component`, `@Service`, `@Repository`: definen beans manejados por Spring.
  - `@Bean`: métodos en clases de configuración que registran beans en el contenedor.
  - `@Autowired`: indica dependencias que Spring debe resolver e inyectar.
- Configuración típica:
  - Clases de configuración con métodos `@Bean` para registrar objetos gestionados por Spring, según examenes.

#### 5.3. JSF y OmniFaces

En aplicaciones con **JSF**, librerías como **OmniFaces** facilitan gestión de mensajes, navegación y scopes. El siguiente código:

```java
Messages.addGlobalInfo("Operación correcta");
Messages.addGlobalError("Ha ocurrido un error");
Faces.redirect("home.xhtml");
Faces.getFlash().put("usuario", usuario);
```

corresponde a OmniFaces, según preguntas de examen.

#### 5.4. Microservicios y frameworks cloud‑native

Un **microservicio** es una unidad de software centrada en un dominio, desplegable independientemente y que se comunica mediante interfaces ligeras (HTTP/REST, gRPC, eventos).

- **Spring Boot:** empaqueta aplicaciones como *fat‑JARs* con servidor embebido (Tomcat/Jetty), facilitando despliegues en contenedores.
- **Spring Cloud:** ofrece componentes para API Gateway, Service Discovery (Eureka), configuración distribuida y tolerancia a fallos (por ejemplo, circuit breakers con Resilience4j).
- **Quarkus, Micronaut y Spring AOT/GraalVM:** frameworks que realizan procesamiento de DI y configuración en tiempo de compilación (AOT), junto con compilación a binarios nativos mediante GraalVM, reduciendo consumo de memoria y tiempos de arranque.

### 6. Otros conceptos técnicos conectados al temario y a preguntas

#### 6.1. Behavior Driven Development (BDD) y Gherkin

BDD describe el comportamiento esperado mediante lenguaje natural estructurado; **Gherkin** usa palabras reservadas:

- `Feature`, `Scenario`, `Given`, `When`, `Then`.

Estas palabras se usan en ficheros de especificación BDD, que luego herramientas como Cucumber ejecutan como pruebas automatizadas.

#### 6.2. WebSocket y APIs bidireccionales

Para comunicación **full‑duplex permanente** entre cliente y servidor (ej. chat en tiempo real) en una API, la tecnología adecuada es **WebSocket**, mientras que REST con polling, HTTP chunked o SSE son patrones de comunicación unidireccional o semiduplex.

### 7. Kubernetes y arquitectura de contenedores

Preguntas del bloque incluyen conceptos de Kubernetes:

- **Sidecar container:** contenedor auxiliar dentro de un Pod que ejecuta tareas complementarias (logging, proxy, sincronización), junto al contenedor principal.
- **RollingUpdate:** estrategia de actualización gradual de Pods en un Deployment, manteniendo disponibilidad del servicio (crea nuevas réplicas mientras elimina antiguas).
- **nodeSelector:** especifica en qué nodos se puede ejecutar un Pod mediante coincidencia simple clave‑valor en las labels del nodo.

### 8. Kafka y políticas de limpieza

En Kafka, `cleanup.policy=compact` indica que el log se compacta manteniendo únicamente el **último valor por clave (key)**, eliminando versiones antiguas de la misma clave.

### 9. API Manager y seguridad

Un **API Manager** suele:

- Validar firmas de tokens JWT.
- Insertar cabeceras adicionales.
- Realizar token exchange o emitir nuevos tokens.

No debería modificar directamente el contenido del JWT original añadiendo claims nuevos sin emitir un nuevo token; esa afirmación aparece como distractor en examen.

### 10. Arquitectura de datos y Data Fabric

**Data Fabric** se define como un enfoque de arquitectura de datos que proporciona una **capa unificada de acceso e integración de datos distribuidos**, basada en metadatos y automatización, permitiendo consumir datos sin necesidad de centralizarlos físicamente. Se diferencia de Data Warehouse (almacenamiento centralizado), Data Mart (subconjunto orientado a negocio) y Delta Lake (gestión ACID sobre data lakes).

## Conceptos que suelen preguntarse (trampas comunes)

| Concepto                       | Realidad técnica/normativa                                                    | Distractor típico en examen                                        |
| :----------------------------- | :---------------------------------------------------------------------------- | :------------------------------------------------------------------ |
| Mantenimiento adaptativo       | Cambios para mantener operatividad tras cambios de entorno (SO, BBDD). | “Corregir errores en producción” (eso es correctivo).    |
| Delivery vs Deployment         | Delivery: aprobación manual final; Deployment: 100 % automático tras tests. | “Son sinónimos; ambos despliegan automáticamente.”       |
| Verificación vs validación     | Verificación: producto bien construido; validación: producto correcto para el usuario. | “Son términos intercambiables según ISTQB.”              |
| Scrum – rol Product Owner      | Único responsable de Product Backlog y maximizar valor.  | “Scrum Master asigna tareas diarias a los programadores.” |
| Burndown Chart ascendente      | Indica incremento del trabajo pendiente (nuevas tareas/reestimaciones). | “El equipo está completando más trabajo del previsto.”   |
| Planning Poker discrepante     | Se discuten estimaciones extremas y se repite votación.           | “El Scrum Master decide la estimación final.”            |
| JPA vs Hibernate               | JPA = especificación; Hibernate = implementación.       | “Hibernate es la especificación y JPA su implementación.” |
| Spring `@Bean` vs `@Autowired` | `@Bean` registra objetos; `@Autowired` inyecta dependencias.      | “@Autowired crea manualmente el ApplicationContext.”     |
| JaCoCo métricas                | Instrucciones, ramas, complejidad ciclomática, líneas.           | “Cubre asserts correctos/erróneos como métrica propia.”  |
| Mockito vs JUnit               | Mockito simula dependencias; JUnit define casos de prueba.       | “JUnit sirve para simular clases no implementadas.”      |
| WebSocket vs SSE               | WebSocket = full‑duplex; SSE = flujo servidor→cliente.          | “REST con polling es full‑duplex permanente.”            |
| Sidecar container              | Contenedor auxiliar para logging, proxy, etc.                    | “Sustituye automáticamente al contenedor principal si falla.” |
| cleanup.policy=compact         | Mantiene último valor por key, eliminando versiones antiguas.    | “Borra mensajes por antigüedad (eso es delete).”         |
| Data Fabric                    | Capa unificada de acceso/integración sin centralizar físicamente. | “Es un Data Warehouse de nueva generación.”              |

## Posibles preguntas tipo test

**Pregunta 1.** Según ISO/IEC 14764, la modificación de un producto software para mantener su operatividad cuando se actualiza el sistema operativo del servidor se denomina:

A. Mantenimiento correctivo.  
B. Mantenimiento preventivo.  
C. Mantenimiento adaptativo.  
D. Mantenimiento perfectivo.  

**Respuesta correcta: C.**

---

**Pregunta 2.** ¿Cuál es la diferencia técnica fundamental entre *Continuous Delivery* y *Continuous Deployment*?

A. Delivery despliega automáticamente en producción; Deployment no.  
B. En Deployment la promoción a producción es automática si los tests pasan; en Delivery requiere aprobación manual final.  
C. Delivery usa pipelines; Deployment despliegues manuales.  
D. Son sinónimos según ISO/IEC 12207.  

**Respuesta correcta: B.**

---

**Pregunta 3.** ¿Quién es el único responsable de gestionar y priorizar el Product Backlog para maximizar el valor del producto en Scrum?

A. Scrum Master.  
B. Developers por consenso.  
C. Product Owner.  
D. Project Manager.  

**Respuesta correcta: C.**

---

**Pregunta 4.** En un Sprint, un Burndown Chart con tendencia ascendente durante varios días consecutivos indica principalmente:

A. Que el equipo completa más trabajo del previsto.  
B. Que aumenta el trabajo pendiente por reestimaciones o nuevas tareas.  
C. Que la velocidad ha aumentado.  
D. Que el Sprint ha terminado.  

**Respuesta correcta: B.**

---

**Pregunta 5.** En diseño de pruebas, las técnicas que derivan casos analizando código y estructura interna (cobertura de sentencias, caminos) se llaman:

A. Técnicas de caja negra.  
B. Pruebas exploratorias.  
C. Partición de clases de equivalencia.  
D. Técnicas de caja blanca o estructurales.  

**Respuesta correcta: D.**

---

**Pregunta 6.** ¿Qué patrón de diseño implementa el `DispatcherServlet` de Spring MVC?

A. DAO.  
B. ORM.  
C. Front Controller.  
D. Circuit Breaker.  

**Respuesta correcta: C.**

---

**Pregunta 7.** ¿Cuál es la relación correcta entre JPA e Hibernate?

A. JPA es una versión moderna de Hibernate.  
B. JPA es una especificación; Hibernate una implementación de esa especificación.  
C. Son capas de Spring que interactúan entre sí.  
D. JPA y Hibernate son lo mismo.  

**Respuesta correcta: B.**

---

**Pregunta 8.** Frente a arranques lentos y alto consumo de memoria en entornos container/Serverless, frameworks como Quarkus o Micronaut introducen principalmente:

A. Configuración exclusivamente en XML.  
B. Inyección de dependencias en tiempo de compilación (AOT) y binarios nativos via GraalVM.  
C. Requerimiento de servidores pesados como WebSphere.  
D. Eliminación total de acceso a BBDD.  

**Respuesta correcta: B.**

---

**Pregunta 9.** ¿Qué librería Java permite simular dependencias externas en pruebas unitarias para probar una clase aisladamente?

A. JUnit.  
B. Mockito.  
C. Moq.  
D. unittest.mock.  

**Respuesta correcta: B.**

---

**Pregunta 10.** En Kubernetes, ¿para qué se usa normalmente un contenedor sidecar?

A. Para sustituir al contenedor principal si falla.  
B. Para desplegar nuevos nodos del clúster.  
C. Para almacenamiento permanente sin volúmenes.  
D. Para ejecutar tareas auxiliares junto al contenedor principal (logging, proxy).  

**Respuesta correcta: D.**

---

**Pregunta 11.** En Kafka, ¿qué implica `cleanup.policy=compact`?

A. Borra mensajes mayores que `retention.bytes`.  
B. Comprime mensajes por antigüedad (`retention.ms`).  
C. Mantiene solo el último valor por key, eliminando versiones antiguas.  
D. Borra mensajes por antigüedad (`retention.ms`).  

**Respuesta correcta: C.**

---

**Pregunta 12.** ¿Qué mecanismo es más adecuado para comunicación bidireccional permanente full‑duplex entre cliente y servidor?

A. REST con polling.  
B. HTTP chunked.  
C. SSE.  
D. WebSocket.  

**Respuesta correcta: D.**

---

**Pregunta 13.** ¿En qué contexto se usan las palabras `Feature`, `Scenario`, `Given`, `When`, `Then`?

A. En pruebas de rendimiento con JMeter.  
B. En definición de pruebas de APIs con Postman.  
C. En casos de prueba usando el lenguaje Gherkin (BDD).  
D. En tests unitarios con JUnit.  

**Respuesta correcta: C.**

---

**Pregunta 14.** ¿Cuál es la estrategia adecuada para mejorar tiempos de construcción de una imagen Docker muy pesada manteniendo trazabilidad?

A. Construir siempre la imagen completa desde cero.  
B. Usar una imagen base etiquetada `latest` sin versionar.  
C. Separar la parte pesada en una imagen base **versionada**, publicar en el Registry y construir la aplicación sobre esa base.  
D. Construir la imagen directamente en nodos de Kubernetes.  

**Respuesta correcta: C.**

---

**Pregunta 15.** ¿Qué describe mejor el trunk‑based development?

A. Varias ramas de producción estables para diferentes versiones.  
B. Integrar cambios directamente en producción sin automatización.  
C. Integrar cambios frecuentemente en una única rama principal con pruebas automatizadas.  
D. Trabajar en ramas de larga duración que se integran al final.  

**Respuesta correcta: C.**

## Normativa o fuentes relacionadas

- **ISO/IEC/IEEE 12207:** *Systems and software engineering — Software life cycle processes.* Norma matriz para procesos de ciclo de vida.
- **ISO/IEC 14764:** *Software Engineering — Software Life Cycle Processes — Maintenance.* Clasificación de tipos de mantenimiento.
- **ISTQB Foundation Level Syllabus (v4.0):** Terminología y niveles de pruebas.
- **Manifiesto Ágil (2001):** Valores y principios ágiles.
- **Guía Scrum 2020:** Roles, artefactos y eventos de Scrum.
- **Real Decreto 311/2022 (ENS):** Principios básicos y requisitos mínimos de seguridad, incluyendo seguridad como proceso integral y desarrollo seguro.
- **Jakarta EE Specifications (Servlet, JPA/Persistence, CDI):** APIs estándar Java empresarial.

## Dudas o puntos pendientes

- **Interpretación de mantenimiento perfectivo vs preventivo:** Algunas fuentes consideran refactorización como perfectivo; ISO 14764 la clasifica como preventivo si se orienta a evitar fallos futuros. En oposiciones TIC suele predominar la interpretación estricta ISO.
- **Alcance de versiones de ISO 12207:** Las ediciones recientes refinan la clasificación de procesos; los tribunales suelen ceñirse a la estructura clásica de procesos primarios (Adquisición, Suministro, Desarrollo, Operación, Mantenimiento), de apoyo y organizacionales.