# REQUISITOS Y CASOS DE USO

Una vez identificados los actores y la normativa, se procede a detallar el comportamiento del sistema. Este apartado cubre la **Ingeniería de Requisitos** y el modelado funcional.

---

## 1. CATÁLOGO DE REQUISITOS

Es fundamental distinguir entre lo que el sistema *debe hacer* y las *restricciones* que debe cumplir.

### 1.1. Requisitos Funcionales (RF)
Describen las funciones específicas del sistema. En un supuesto de la AGE, suelen seguir el ciclo de vida de un expediente administrativo.

| ID | Requisito Funcional | Actor Principal | Servicio Común Implicado |
| :--- | :--- | :--- | :--- |
| **RF-01** | **Autenticación:** El sistema debe permitir el acceso seguro de ciudadanos y empleados. | Todos | **Cl@ve** / **Autentica** |
| **RF-02** | **Registro de Solicitud:** Permitir la entrada de solicitudes telemáticas generando asiento registral. | Ciudadano | **GEISER / REGECO** |
| **RF-03** | **Consulta de Datos:** Verificar datos del interesado sin pedir documentación (Interoperabilidad). | Sistema | **PID** (SVD) |
| **RF-04** | **Firma Electrónica:** Permitir la firma de solicitudes y actos administrativos. | Ciudadano / Funcionario | **FIRe** / **@firma** |
| **RF-05** | **Notificación:** Puesta a disposición de notificaciones fehacientes. | Sistema | **Notifica** (DEHú) |
| **RF-06** | **Gestión de Expediente:** Generación del índice electrónico y foliado. | Sistema | **INSIDE** (ENI) |

### 1.2. Requisitos No Funcionales (RNF) - ¡Puntos Clave!
Aquí es donde demuestras conocimiento normativo. Estos requisitos condicionan la arquitectura.

| ID | Requisito No Funcional | Normativa / Justificación |
| :--- | :--- | :--- |
| **RNF-01** | **Accesibilidad:** El portal debe cumplir nivel AA. | **RD 1112/2018** y Norma UNE 301549 (WCAG 2.1). |
| **RNF-02** | **Seguridad:** El sistema debe cumplir las medidas del Anexo II según su categoría. | **ENS** (RD 311/2022). |
| **RNF-03** | **Interoperabilidad:** Uso de estándares de intercambio (XML, JSON) y firma (XAdES, PAdES). | **ENI** y NTI de Catálogo de Estándares. |
| **RNF-04** | **Auditoría y Trazabilidad:** Registrar quién accede y qué hace. | **ENS** (Marco Operacional) y **RGPD**. |
| **RNF-05** | **Disponibilidad:** El sistema debe estar operativo 24x7 (Sede Electrónica). | **Ley 39/2015**. |

---

## 2. DIAGRAMA DE CASOS DE USO (UML)



[Image of UML use case diagram example]


El Diagrama de Casos de Uso muestra la relación entre los **Actores** (identificados en el paso anterior) y las **Funcionalidades** (RF).

### 2.1. Plantilla de Descripción del Diagrama
Al presentar el diagrama en el examen, utiliza este texto para justificarlo:

> *"El Diagrama de Casos de Uso representa el comportamiento del sistema desde el punto de vista del usuario. Se han identificado dos grandes paquetes de funcionalidad según el perfil de acceso:"*

#### A. Paquete Ciudadano (Sede Electrónica)
* **Actores:** Ciudadano, Representante (vía **Representa**).
* **Casos de Uso Principales:**
    * `Iniciar Trámite` (Incluye `Autenticarse con Cl@ve`).
    * `Firmar Solicitud` (Usa `FIRe`).
    * `Consultar Estado` (Acceso a Carpeta Ciudadana).
    * `Recibir Notificación` (Acceso a DEHú).

#### B. Paquete Tramitador (Red SARA / Intranet)
* **Actores:** Funcionario Tramitador, Jefe de Servicio, Administrador.
* **Casos de Uso Principales:**
    * `Validar Solicitud` (Usa `Autentica` para SSO).
    * `Generar Resolución` (Usa `INSIDE` para conformar expediente).
    * `Firmar Resolución` (Usa `Portafirmas`).
    * `Enviar a Archivo` (Usa `Archive`).

---

## 3. RELACIONES UML CLAVE

Recuerda usar estas relaciones para dar riqueza técnica al diagrama:

* **<< include >> (Inclusión):** Cuando un caso de uso *siempre* necesita a otro.
    * *Ejemplo:* `Realizar Trámite` **<< include >>** `Autenticarse`.
* **<< extend >> (Extensión):** Cuando un caso de uso es opcional o ocurre bajo ciertas condiciones.
    * *Ejemplo:* `Pagar Tasa` **<< extend >>** `Realizar Trámite` (Solo si el trámite no es gratuito).
* **Generalización (Herencia):**
    * *Ejemplo:* El actor `Administrador` hereda de `Funcionario` (puede hacer todo lo que hace el funcionario más sus tareas propias).

---