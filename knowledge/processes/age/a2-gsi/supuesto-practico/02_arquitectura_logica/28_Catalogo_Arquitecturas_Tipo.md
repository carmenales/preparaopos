# ARQUITECTURAS TÍPICAS EN UN SUPUESTO DEL A2

## 1. Arquitectura 3 capas (presentación + negocio + datos)

**Cuándo usarla**

* Sistema web clásico
* Tramitación interna
* Aplicaciones corporativas
* Exámenes donde quieren arquitectura “segura y ordenada”

**Frases para usar en examen (copy-paste)**

### Justificación general
> Se implementa una arquitectura de tres capas (presentación, lógica de negocio y datos) porque permite separar responsabilidades, mejorar mantenibilidad y facilitar la escalabilidad, modelo común en los sistemas corporativos de la AGE.

### Seguridad acorde al ENS
> Este enfoque permite aplicar medidas de seguridad por capas según el ENS, como segmentación en red, controles de acceso diferenciados y registro de auditoría en cada nivel.

### Integración con servicios comunes
> La capa de negocio facilita exponer servicios REST para integrarse con servicios comunes como Cl@ve, Notifica o INSIDE cumpliendo los requisitos del ENI.

---

## 2. Arquitectura Web + API REST

**Cuándo usarla**

* Cuando el cliente (front) es distinto del servidor
* Cuando puede haber app móvil en el futuro
* Cuando va a haber integración con otros organismos

**Frases rápidas de examen**

### Justificación de REST
> Se expone la funcionalidad mediante una API REST porque facilita la interoperabilidad, desacopla presentación y negocio, y permite integrar fácilmente servicios comunes cumpliendo el ENI.

### Ventaja para nuevas plataformas
> Esta arquitectura permite que en el futuro pueda desarrollarse una aplicación móvil reutilizando la API sin alterar la lógica de negocio.

### Seguridad ENS
> Las comunicaciones se protegen mediante TLS, control de acceso basado en tokens y registro de uso para auditoría, de acuerdo con el ENS.

---

## 3. Arquitectura Microservicios

**Cuándo usarla**

* Grandes sistemas
* Escalabilidad alta
* Mantenimiento y despliegues independientes
* Integraciones complejas

**Frases para el examen**

### Justificación
> Se emplea una arquitectura de microservicios para que cada módulo del sistema pueda evolucionar, escalarse y desplegarse de forma independiente, reduciendo el riesgo y mejorando el tiempo de entrega de nuevas funcionalidades.

### Ventaja técnica
> Cada servicio podrá tener su propio ciclo de despliegue, facilitando metodologías ágiles y reduciendo el impacto de cambios en producción.

### Seguridad ENS
> La segmentación entre microservicios permite aplicar el principio de mínimo privilegio y controlar el tráfico mediante firewalls y balanceadores, alineado con el ENS.

---

## 4. Arquitectura N-capas corporativa en la AGE

**Cuándo usarla**

* Cuando quieras sonar “más AGE”
* Casos con:
    * ESB (Enterprise Service Bus)
    * Sistemas transversales
    * Integración entre Ministerios

**Frases tipo**

### Justificación
> Se adopta una arquitectura N-capas con bus corporativo (ESB) que permite desacoplar emisores y consumidores y facilitar el intercambio de información entre organismos, cumpliendo con el ENI y las NTI.

### Beneficio administrativo
> Este modelo evita integraciones punto a punto, reduciendo costes de mantenimiento y facilitando escalabilidad funcional.

---

## 5. Arquitectura Contenerizada (Docker / Kubernetes)

**Cuándo usarla**

* Si se habla de despliegue moderno
* Si se exige alta disponibilidad
* Si se quiere CI/CD o despliegues rápidos

**Frases rápidas**

### Justificación
> Se emplean contenedores porque permiten aislar la ejecución de los servicios, un despliegue reproducible y una escalabilidad horizontal rápida.

### Alta disponibilidad
> El orquestador (p. ej. Kubernetes) permite ejecutar múltiples réplicas y redistribuir carga automáticamente, manteniendo el servicio disponible con fallos de nodo.

### ENS
> Los contenedores permiten aplicar controles específicos de seguridad a nivel de imagen, nodo y red, alineados con las medidas del ENS.

---

## 6. Arquitectura para una Aplicación Móvil pública

**Estructura típica que puedes soltar:**

* App móvil (Android / iOS)
* Que se conecta a API REST segura
* Que integra:
    * Cl@ve
    * Notificaciones (Notifica)
    * INSIDE o repositorio documental
    * Carpeta Ciudadana

**Frases para examen**

### Modelo típico
> La aplicación móvil actúa como cliente y consume los servicios de la API REST corporativa, lo que permite reutilizar la lógica existente y mantener un único punto de acceso seguro.

### Justificación de seguridad
> La comunicación se realiza exclusivamente sobre TLS, con autenticación basada en Cl@ve y trazabilidad registrada en la plataforma de auditoría conforme al ENS.

---

## 7. Arquitectura de tramitación con registro y expediente

Muy típica de examen.

**Frase corta estándar**
> El sistema implementa el ciclo completo de tramitación administrativa: identificación mediante Cl@ve, registro en la sede electrónica, generación y custodia de expedientes en INSIDE y notificación mediante Notifica.

**Con solo esa frase:**

* Has metido interoperabilidad
* Has metido 3 plataformas comunes
* Suena 100% AGE

---

## 8. Cómo introducir la arquitectura en una respuesta de manera limpia

**Plantilla “universal” para empezar respuesta:**
> La arquitectura propuesta se diseña para cumplir los requisitos funcionales del enunciado garantizando interoperabilidad, seguridad y escalabilidad, en línea con el ENI, ENS y la Ley 40/2015.

**Y luego añades:**
> Para ello se adopta una arquitectura de [TIPO] compuesta por:
> 
> 1. Capa de presentación (web / móvil)
> 2. Servicios de negocio expuestos mediante REST
> 3. Base de datos corporativa
> 4. Integración con servicios comunes de la AGE

**Acabas con:**
> Este modelo facilita mantenimiento, permite ampliar funcionalidades en el futuro y asegura protección de datos según el ENS y el RGPD.

*(Esa estructura te sirve en el 80% de preguntas).*

---

# JUSTIFICACIÓN DE ARQUITECTURA (PLANTILLA GENERAL)

En el examen te suelen pedir: "Diseñe la arquitectura...", "Explique la arquitectura física...", "Justifique la tecnología...". Para contestar de forma sólida, rápida y correcta necesitas tener una plantilla mental muy clara.

---

## 10. PLANTILLA GENERAL: ESTRUCTURA DE UNA RESPUESTA

Una respuesta completa y sólida debe seguir siempre este orden:

1.  **Objetivo del sistema.**
2.  **Arquitectura seleccionada.**
3.  **Criterios de elección.**
4.  **Componentes y capas.**
5.  **Seguridad aplicada (ENS).**
6.  **Disponibilidad y continuidad.**
7.  **Justificación tecnológica.**
8.  **Cumplimiento legal (ENS, ENI, RGPD/LOPDGDD).**

Con ese guión puedes responder prácticamente cualquier pregunta relacionada con diseño de sistemas.

---

## 11. ARQUITECTURA N-CAPAS (CASO MÁS FRECUENTE)

### Plantilla rápida de respuesta
> "Se adopta una arquitectura de n-capas que separa presentación, lógica de negocio y acceso a datos, proporcionando modularidad, facilidad de mantenimiento, escalabilidad horizontal y sustitución de componentes con impacto mínimo."

### Capas
* **Capa de presentación (frontend):** Web Angular/React o App móvil consumiendo APIs.
* **Capa de negocio:** Servicios REST implementados en Java/Spring, .NET, Python, etc.
* **Capa de acceso a datos:** ORM, DAO o repositorios, aislando la persistencia.
* **Capa de base de datos:** PostgreSQL, Oracle, SQL Server, etc.

### Ventajas que puedes soltar de memoria
* Reduce acoplamiento.
* Favorece escalabilidad.
* Facilita pruebas unitarias y funcionales.
* Permite evolución tecnológica independiente por capa.
* Encaja naturalmente con despliegues en CPD o cloud híbrido.

### Mini-frase para el examen
> "Se adopta arquitectura n-capas, muy adecuada para sistemas corporativos de la AGE, aportando modularidad, separación de responsabilidades, facilidad de mantenimiento y escalabilidad horizontal."

---

## 12. ARQUITECTURA DE MICROSERVICIOS

### Cuándo usarla en un examen
* Sistema grande.
* Alta escalabilidad.
* Muchos equipos de desarrollo.
* Integraciones entre organismos.
* Evolución rápida.

### Frase formal para el examen
> "Se diseña el sistema sobre arquitectura de microservicios, donde cada servicio implementa una funcionalidad de negocio concreta, es autónomo, escalable independientemente y se comunica mediante API REST segura."

### Ventajas que puntúan
* Escalabilidad independiente por servicio.
* Despliegue individual sin interrumpir el resto.
* Facilita integración con terceros (AGE, CC.AA., UE).
* Encaja con contenedores en Kubernetes, OpenShift, etc.

### Riesgos que puedes mencionar para demostrar madurez técnica
* Mayor complejidad de observabilidad.
* Necesidad de API Gateway y trazabilidad.
* Gestión distribuida de logs (SIEM).
* Seguridad por diseño (Zero Trust).

---

## 13. ARQUITECTURA PARA APLICACIÓN MÓVIL EN LA AGE

### Respuesta tipo
> "Se adopta una arquitectura cliente-servidor donde la aplicación móvil actúa como cliente ligero consumiendo APIs REST alojadas en el CPD/Cloud corporativo. Las APIs implementan lógica de negocio, autenticación mediante Cl@ve o certificado, y acceso seguro a datos cifrados en reposo y tránsito."

### Qué debe aparecer siempre
* Cliente (Android/iOS).
* Servidor con APIs REST.
* Autenticación de ciudadanos vía Cl@ve.
* Seguridad por TLS 1.2+.
* Registro y auditoría.
* Integración con plataformas comunes.

### Servicios comunes que conviene citar
* Cl@ve / Autentica.
* @firma / FIRe.
* INSIDE.
* GEISER.
* SIR.
* PortaSIG.
* Carpeta Ciudadana.

---

## 14. DIAGRAMA DE DESPLIEGUE – GUION PARA HACERLO SIEMPRE BIEN

En una pregunta de arquitectura, si te piden: **“Realice un diagrama de despliegue”**, debes representar al menos:
* CPD (o nube pública/privada).
* Servidor web.
* Servidor de aplicaciones.
* Servidor de base de datos.
* Cliente (navegador o app móvil).
* Fronteras de seguridad (firewall, DMZ, VLAN).
* SIEM o sistema de monitorización si procede.

### Frase formal de acompañamiento
> "El despliegue se organiza en tres zonas: red externa (usuario), DMZ con servidores web/APIs protegidos mediante firewall, y red interna donde residen servidores de negocio y bases de datos. Se aplican controles del ENS en cada nivel."

---

## 15. COMPARATIVA PARA DECIDIR RÁPIDAMENTE EN EXAMEN

| Situación en el enunciado | Mejor arquitectura |
| :--- | :--- |
| **Sistema pequeño, estable, poco tráfico** | N-capas clásica. |
| **Sistema corporativo general de la AGE** | N-capas + servicios comunes. |
| **Crecimiento continuo, integración con terceros, varias unidades desarrollando** | Microservicios. |
| **Aplicación móvil** | Cliente móvil + APIs REST + servicios comunes. |
| **Servicios críticos con alta disponibilidad** | Microservicios con balanceo + cluster. |

---

## 16. JUSTIFICACIÓN DE TECNOLOGÍAS – PLANTILLA PARA EXAMEN

### Base de datos
> "Se selecciona **PostgreSQL** por ser software ampliamente utilizado en la AGE, compatible con el ENS, escalable, robusto y con soporte en CPD y cloud híbrido."

### Backend
> "Se utiliza **Java con Spring Boot** por su madurez, amplia comunidad, facilidad para implementar APIs REST y disponibilidad de perfiles profesionales en la Administración Pública."

### Frontend
> "**Angular/React** para desarrollar cliente desacoplado, interoperable, modular y mantenible."

### Contenedores
> "Se emplean contenedores **Docker** orquestados con **Kubernetes/OpenShift**, permitiendo despliegues reproducibles, escalado automático e integración con CI/CD."

---

## 17. CUMPLIMIENTO NORMATIVO – FRASES TIPO

### ENS
> "La arquitectura incorpora medidas de protección física, lógica y de comunicaciones conforme al Esquema Nacional de Seguridad, incluyendo segmentación de redes, autenticación robusta, cifrado y monitorización centralizada."

### ENI
> "El sistema garantiza interoperabilidad mediante el uso de estándares abiertos y servicios comunes como Cl@ve y @firma, en cumplimiento del ENI."

### RGPD/LOPDGDD
> "El sistema aplica privacidad desde el diseño, minimización de datos, cifrado, registro de eventos y control de accesos conforme al RGPD y la LOPDGDD."

---

## 18. RESPUESTA COMPLETA EN 12-14 LÍNEAS PARA EXAMEN

> "El sistema adopta una arquitectura n-capas donde la capa de presentación interactúa con APIs REST alojadas en una capa de servicios. Estas APIs implementan lógica de negocio, acceso a datos y control de seguridad. La base de datos corporativa almacena la información cifrada y accesible únicamente desde la red interna.
>
> La arquitectura se despliega en tres zonas: red externa de usuario, DMZ con balanceador y servidores de aplicaciones protegidos mediante cortafuegos, y red interna donde residen los servicios y la base de datos. Se aplican medidas del ENS como autenticación robusta, principio de mínimo privilegio, segmentación de red, cifrado TLS, copias de seguridad, monitorización centralizada y auditoría.
>
> La solución garantiza interoperabilidad con ENI mediante uso de estándares abiertos y servicios comunes (Cl@ve, @firma). Se cumple RGPD/LOPDGDD mediante privacidad desde el diseño, control de accesos y trazabilidad."