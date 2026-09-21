# UML en un supuesto práctico del Cuerpo TIC (Bloque III)

## 1. Qué diagramas son rentables para el examen

En orden de utilidad real:

1.  Diagrama de Casos de Uso
2.  Diagrama de Clases
3.  Diagrama de Secuencia
4.  Diagrama E/R (lógico o conceptual)
5.  Diagrama de Despliegue (Deployment)
6.  Diagrama de Paquetes

Con estos se cubre más del 95% de lo que puede caer.

## 2. Cómo elegir qué diagramas poner

| Situación del supuesto | Diagrama que deberías poner |
| :--- | :--- |
| Te piden funcionalidades del sistema | **Casos de uso** |
| Te piden estructura de datos o modelo | **Clases o E/R** |
| Te piden interacción entre sistemas | **Secuencia** |
| Te piden arquitectura técnica | **Despliegue** |
| Te piden organización en módulos | **Paquetes** |

**Tiempo medio de dibujar cada uno en el examen:**

* Casos de uso: 2–4 min
* Clases: 4–6 min
* Secuencia: 4–7 min
* Despliegue: 2–4 min
* Paquetes: 2–4 min
* E/R: 5–8 min

## 3. Argumentos “tipo” para justificar cada diagrama
Útiles para meter 1–2 frases y parecer que lo haces porque debes, no por gusto.

### 3.1. Casos de Uso
Se utiliza un diagrama de casos de uso para identificar las funcionalidades del sistema desde la perspectiva del usuario, permitiendo definir claramente los requisitos funcionales y los actores implicados.

### 3.2. Clases
Se emplea un diagrama de clases para modelar la estructura lógica del sistema, identificando entidades, atributos y relaciones que serán la base del diseño y posterior implementación.

### 3.3. Secuencia
Mediante un diagrama de secuencia se representa el flujo temporal de mensajes entre objetos, facilitando la definición de la lógica de interacción y la trazabilidad de escenarios clave.

### 3.4. E/R
Se desarrolla un modelo entidad–relación para identificar las entidades principales de datos, sus atributos y relaciones, asegurando un diseño normalizado y coherente con los requisitos funcionales.

### 3.5. Despliegue
Se realiza un diagrama de despliegue para definir la arquitectura física del sistema, servidores, capas y nodos, garantizando escalabilidad, separación de responsabilidades y seguridad.

### 3.6. Paquetes
Se define un diagrama de paquetes para agrupar funcionalmente los componentes del sistema, permitiendo modularidad, mantenibilidad y un diseño orientado a evolución.

## 4. Ejemplos completos como si fueran de examen

### 4.1 Ejemplo real: Aplicación móvil para la AEAT que permite consultar y presentar declaraciones

**Diagrama de Casos de Uso (texto)**

Actores:

* Contribuyente
* Sistema Cl@ve
* Plataforma AEAT

Casos de uso:

* Autenticarse con Cl@ve
* Consultar declaraciones anteriores
* Presentar una nueva declaración
* Descargar justificante

**Justificación para poner en el examen**
> Se incluye un diagrama de casos de uso para identificar de forma clara las funcionalidades ofrecidas al contribuyente y los actores externos que intervienen, facilitando la captura de requisitos funcionales del sistema.

### 4.2 Diagrama de Clases (texto)

* Contribuyente - NIF - Nombre - Email
* Declaracion - Año - Estado - FechaPresentacion
* Justificante - NumeroReferencia - FechaEmision

Relaciones:

* Contribuyente 1..* ---- 1..* Declaracion
* Declaracion 1 ---- 1 Justificante

**Frase tipo**
> Se desarrolla un diagrama de clases para modelar las entidades del sistema y sus relaciones, sirviendo de base para el diseño de la capa de datos y la implementación posterior.

### 4.3 Diagrama de Secuencia

* Contribuyente → App Móvil: Solicita inicio de sesión
* App Móvil → Cl@ve: Autenticación
* Cl@ve → App Móvil: Autenticación válida
* App Móvil → AEAT: Solicita declaración
* AEAT → App Móvil: Devuelve resultado

**Frase para el examen**
> Se emplea un diagrama de secuencia para describir el flujo temporal de mensajes entre el usuario, Cl@ve y los servicios internos de la AEAT, definiendo de forma clara el escenario de autenticación y consulta.

### 4.4 Diagrama de Despliegue (Deployment)

* Móvil del ciudadano - Aplicación Android/iOS
* DMZ - API Gateway
* Centro de datos AEAT - Servidor de negocio - Servidor de base de datos - Integración con Cl@ve

**Frase tipo**
> Se realiza un diagrama de despliegue para representar la arquitectura física del sistema, separando cliente, pasarela de servicios y servidores internos, cumpliendo los principios de seguridad establecidos en el ENS.

### 4.5 Diagrama de Paquetes

* UI
* Autenticacion
* Declaraciones
* Notificaciones
* ServiciosExternos

**Justificación**
> Se define un diagrama de paquetes para agrupar los módulos del sistema, mejorando la modularidad, mantenibilidad y capacidad de evolución futura.

## 5. Modelo E/R aplicado (AEAT)

ENTIDADES:

* Contribuyente (NIF, Nombre, Email)
* Declaracion (Id, Año, Estado, FechaPresentacion)
* Justificante (Id, NumReferencia, FechaEmision)

RELACIONES:

* Contribuyente 1:N Declaracion
* Declaracion 1:1 Justificante

**Frase tipo**
> Se desarrolla un modelo entidad–relación para definir la estructura de datos del sistema de forma normalizada y coherente con las funcionalidades definidas.

## 6. Cómo meter UML en una respuesta sin gastar tiempo
Puedes usar una frase resumen:

> Se incluyen los diagramas UML (casos de uso, clases, secuencia y despliegue) para representar funcionalmente el sistema, su estructura lógica, los flujos de interacción y la arquitectura física, asegurando trazabilidad completa desde los requisitos hasta el diseño.

---

## 2.1 Plantilla para justificar un diagrama UML de Casos de Uso
Se utiliza un diagrama de Casos de Uso para representar funcionalmente la interacción entre los usuarios y el sistema. Este modelo permite identificar claramente los requisitos funcionales del enunciado y visualizar las responsabilidades principales sin entrar aún en detalles de diseño interno.

En el caso descrito, se representan los actores [ACTORES] y los casos de uso necesarios para [OBJETIVO DEL SISTEMA]. Este diagrama facilita la trazabilidad del sistema desde los requisitos funcionales hasta el diseño y posterior implementación, alineándose con las buenas prácticas de modelado utilizadas en la AGE.

## 2.2 Plantilla para justificar un diagrama de Clases
Se utiliza un diagrama de clases para modelar la estructura de la información del sistema, mostrando las entidades principales, sus atributos y las relaciones entre ellas. Este diagrama permite representar el modelo de datos que dará soporte a los requisitos definidos y facilita posteriormente la generación del modelo relacional.

Las clases representadas corresponden a los elementos identificados a partir de los casos de uso, como [ELEMENTOS DEL DOMINIO], aplicando principios de cohesión y bajo acoplamiento. Esta representación es adecuada para el ciclo de vida iterativo-incremental empleado habitualmente en la AGE.

## 2.3 Plantilla para justificar un diagrama de Secuencia
Se emplea un diagrama de secuencia para modelar la interacción temporal entre los componentes del sistema durante la ejecución de un caso de uso concreto. Este diagrama muestra los mensajes intercambiados entre los objetos implicados, permitiendo detallar la lógica del flujo, validaciones y llamadas a servicios externos.

En este caso, el diagrama describe el flujo del caso de uso [NOMBRE], incluyendo los pasos de autenticación, validación y acceso a datos, garantizando trazabilidad y cumplimiento de seguridad según el ENS.

## 2.4 Plantilla para justificar un diagrama de Despliegue
Se utiliza un diagrama de despliegue para representar la distribución física del sistema en nodos e infraestructuras reales. Este modelo muestra servidores, balanceadores, bases de datos y otros componentes del entorno, así como las conexiones y protocolos.

Este diagrama es especialmente relevante porque permite evidenciar que el sistema se aloja en CPD o infraestructura certificada conforme al ENS, y que la red, los dispositivos y los canales de comunicación cumplen medidas de seguridad adecuadas (cifrado TLS, segmentación, registros, etc.).

## 2.5 Plantilla para justificar un diagrama de Paquetes
El diagrama de paquetes organiza el sistema en módulos lógicamente independientes, lo que facilita mantenibilidad, reutilización y control de dependencias. Esta estructura reduce el acoplamiento entre componentes, mejorando la extensibilidad del sistema y permitiendo ciclos de implantación iterativos e incrementalmente gestionables.

Además, esta organización modular se alinea con los principios de diseño orientado a componentes utilizados en Métrica v3 y en metodologías ágiles aplicadas en la AGE.

## 2.6 Plantilla para defender la elección de una API REST
Se propone implementar la comunicación entre el front-end y el back-end mediante una API REST porque facilita la separación cliente-servidor, la escalabilidad y la interoperabilidad. Este enfoque soporta el intercambio de datos con plataformas comunes de la AGE de forma estándar (JSON sobre HTTPs), cumpliendo el ENI y sus NTI.

REST permite desacoplar la capa de presentación, lo que facilita el desarrollo de nuevas versiones, apps móviles o integraciones futuras con otros organismos sin afectar al funcionamiento del back-end. Además, simplifica aplicar auditoría, control de acceso basado en tokens y cifrado TLS, alineado con el ENS.

## 2.7 Plantilla para defender que la solución sea Web y no móvil
Se opta inicialmente por una aplicación web responsive porque garantiza el acceso multiplataforma sin necesidad de instalación, reduciendo costes y tiempos de desarrollo. Esta decisión permite llegar rápidamente a toda la ciudadanía desde navegador estándar, alineándose con los principios de eficiencia y servicio público.

Además, este enfoque facilita el cumplimiento normativo (firma, trazabilidad, registro, auditoría, integración con servicios como Cl@ve y Notifica), lo que resulta más complejo si la prioridad inicial fuera una aplicación móvil nativa. En fases posteriores y si se justifica su necesidad, podría desarrollarse una app móvil reutilizando la API REST existente.

## 2.8 Plantilla para justificar Métrica v3
Se aplica Métrica v3 por ser la metodología oficial recomendada en la Administración Pública para la planificación, análisis, diseño y construcción de sistemas de información. Su estructura modular permite cubrir el ciclo de vida completo garantizando:

* análisis riguroso,
* trazabilidad,
* diseño estructurado,
* control de calidad.

Métrica v3 se adapta al desarrollo incremental y mejora la documentación del sistema, aspecto crítico en entornos de la AGE donde se exige trazabilidad, auditabilidad y continuidad del servicio.

## 2.9 Plantilla para justificar uso de Metodología Ágil
Se emplea metodología ágil (Scrum) porque permite entregar valor de forma iterativa e incremental, reduciendo riesgos y ajustando requisitos sobre la marcha. Es especialmente útil cuando el enunciado muestra cambios funcionales o necesidades de obtener feedback rápido.

Aunque la documentación es más ligera que en enfoques clásicos, se mantienen los artefactos necesarios para cumplir con trazabilidad, gestión y control requeridos en proyectos de la AGE.

## 2.10 Plantilla para justificar un modelo E/R
Se utiliza un modelo Entidad-Relación porque permite representar de forma clara las entidades de negocio, sus atributos y relaciones. Este modelo sirve de base para definir el modelo relacional posterior en la base de datos y asegurar integridad referencial, normalización y trazabilidad de la información, alineado con los requisitos del ENS y la gestión documental pública.