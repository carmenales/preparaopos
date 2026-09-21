# ARQUITECTURA LÓGICA (PAQUETES Y CAPAS)

El Diagrama de Paquetes organiza el sistema en subsistemas lógicos. Para la AGE, el estándar de facto es una **Arquitectura Multicapa (n-tier)**, generalmente de 3 capas, que garantiza el desacoplamiento y la escalabilidad.



---

## 1. ESTRUCTURA DE CAPAS (EL ESQUELETO)

Al diseñar el diagrama, debes representar estas tres grandes "cajas" o paquetes principales y sus dependencias.

### 1.1. Capa de Presentación (Interfaz)
Es el medio de acceso para ciudadanos y funcionarios.

* **Módulos:**
    * **Portal Web Ciudadano (Sede):** Acceso a trámites.
    * **Backoffice Funcionario:** Gestión de expedientes.
    * **App Móvil (Opcional):** Si el supuesto lo pide (ej. "Ruraliza").
* **Tecnología:** HTML5, CSS3, Frameworks JS (Angular/React). Si hay App, se recomienda **Híbrida** (Apache Cordova) para aprovechar el desarrollo web.
* **Normativa:** Debe cumplir **Accesibilidad** (RD 1112/2018, WCAG 2.1 Nivel AA).

### 1.2. Capa de Lógica de Negocio (El Cerebro)
Aquí reside la inteligencia del sistema y los servicios.

* **Tecnología:** **Java (Jakarta EE)**.
    * *Justificación:* Es un estándar abierto, robusto y el más extendido en la AGE (lo que facilita el mantenimiento).
* **Paquete de Integración (Vital):** Dentro de esta capa, debe haber un paquete específico para conectarse con los **Servicios Comunes** (Cl@ve, INSIDE, PID). Esto aísla la lógica del trámite de la complejidad de las llamadas externas.

### 1.3. Capa de Acceso a Datos (Persistencia)
Encargada de guardar y recuperar la información.

* **Tecnología:** SGBD Relacional (MySQL/Oracle/PostgreSQL).
* **ORM (Object-Relational Mapping):** Se debe citar el uso de **JPA / Hibernate**.
    * *Justificación:* Desacopla el código de la base de datos específica, permitiendo cambiar de gestor de BBDD sin reescribir la aplicación.

---

## 2. PLANTILLA DE JUSTIFICACIÓN TÉCNICA (TEXTO DE EXAMEN)

Este texto (adaptado de fuentes de preparación avanzadas) justifica la elección tecnológica ante el tribunal:

> **Defensa de la Arquitectura en 3 Capas:**
> "Se propone una arquitectura en 3 capas para garantizar la **reutilización** de componentes y facilitar el **mantenimiento** evolutivo (Principios SOLID).
>
> 1. **Capa de Presentación:** Se prestará especial atención a los principios de accesibilidad (Art. 2 RD 203/2021), cumpliendo el **RD 1112/2018** y la norma **UNE 301 549:2022** (Niveles A y AA de WCAG 2.1). Se implementará como una aplicación web responsive (HTML5+CSS+JS) o híbrida (Apache Cordova) para adaptarse a cualquier dispositivo.
>
> 2. **Capa Lógica:** Se implementará en **Java mediante Jakarta EE**. Esta elección se debe a que es un lenguaje basado en estándares abiertos, lo cual facilita la integración y evita el 'vendor lock-in'. Incluirá módulos para la gestión del expediente y la integración con servicios horizontales (Interoperabilidad).
>
> 3. **Capa de Acceso a Datos:** Se utilizará el patrón DAO y un framework de persistencia estándar como **JPA (implementación Hibernate)** para asegurar la independencia del motor de base de datos y la integridad de la información."

---

## 3. DETALLE DE LOS PAQUETES DE INTEGRACIÓN (ENI)

En tu diagrama, dibuja un paquete llamado **"Integración"** o **"Servicios Externos"** dentro de la Capa Lógica y detalla sus componentes:

| Componente | Función en el diagrama |
| :--- | :--- |
| `Conector_Identidad` | Gestiona las llamadas SAML a **Cl@ve**. |
| `Conector_Documental` | Gestiona las llamadas SOAP/REST a **INSIDE**. |
| `Conector_Notificaciones` | Gestiona los envíos a **Notifica**. |
| `Conector_Firma` | Gestiona las peticiones a **FIRe / @firma**. |

---