# GUÍA METODOLÓGICA: DISEÑO DE SUBSISTEMAS Y ACTORES

Esta guía establece el método para descomponer un sistema complejo en subsistemas manejables, garantizando la modularidad, la seguridad y la reutilización (CTT).

---

## 1. PASO 1: IDENTIFICACIÓN PRECISA DE ACTORES

Antes de definir los módulos, debemos saber quién los usa. No te limites a "Usuario". Sé específica:

### 1.1. Tipología de Actores Humanos
* **Ciudadano/Interesado:** Accede a la Sede. Requiere usabilidad y accesibilidad máximas.
* **Representante:** Actúa por otro. Requiere validación de poderes (**Representa**).
* **Funcionario Tramitador:** Valida y gestiona. Accede desde la Intranet.
* **Funcionario Habilitado:** Actúa en nombre del ciudadano presencialmente (Oficinas OAMR).
* **Administrador del Sistema:** Gestión técnica y auditoría.

### 1.2. Actores "Sistema" (Interfaces)
Trata a los sistemas externos como actores que "piden" o "envían" cosas.

* **Servicios Comunes:** Cl@ve, Notifica, PID.
* **Sistemas del Organismo:** Registro contable (SIC), RRHH (NEDAES).

---

## 2. PASO 2: DEFINICIÓN DE SUBSISTEMAS (ESTRATEGIA DE DIVIDE Y VENCERÁS)

En lugar de una aplicación monolítica gigante, propón una arquitectura dividida en **Subsistemas Funcionales**. Esto demuestra visión de arquitectura.

### 2.1. Subsistemas Estándar en la AGE
Casi cualquier supuesto se puede resolver con esta combinación:

1.  **Subsistema de Sede Electrónica (Front-Office):**
    * *Función:* Catálogo de trámites, inicio de solicitud, "Mi Carpeta".
    * *Requisito:* Alta disponibilidad (24x7) y Seguridad Perimetral (DMZ).
2.  **Subsistema de Tramitación (Back-Office):**
    * *Función:* Bandejas de entrada de expedientes, validación, generación de documentos, firma de resoluciones.
    * *Acceso:* Solo red interna (SARA).
3.  **Subsistema de Integración (Interoperabilidad):**
    * *Función:* Concentrador de llamadas a servicios externos (Bus de Servicios / ESB).
4.  **Subsistema de Archivo y Gestión Documental:**
    * *Función:* Almacenamiento de documentos y expedientes ENI.
5.  **Subsistema de Administración y Auditoría:**
    * *Función:* Configuración de tablas maestras, gestión de usuarios, consulta de trazas (logs).

### 2.2. Criterio de Reutilización (Art. 157 Ley 40/2015)
Antes de diseñar un subsistema desde cero, justifica que has consultado el **CTT (Centro de Transferencia de Tecnología)**.

* *Ejemplo:* "Para el subsistema de tramitación, se evaluará la reutilización de la solución **ACCEDA** (del SGAD) antes de iniciar un desarrollo a medida."

---

## 3. PASO 3: DEFINICIÓN DE INTERFACES (CONEXIONES)

Define cómo se hablan los subsistemas entre sí y con el mundo.

### 3.1. Interfaces de Usuario (Personas)
* Deben cumplir el **RD 1112/2018** (Accesibilidad Web/Móvil).
* Deben diseñarse bajo principios de **Usabilidad** (Diseño Centrado en el Usuario).

### 3.2. Interfaces de Sistema (Máquinas)
* **Internas:** Comunicación entre el Front-Office y el Back-Office (vía API REST / JSON).
* **Externas:** Comunicación con la AGE.
    * *Protocolo:* Preferencia por **Web Services (SOAP/XML)** para sistemas legacy (ej. @firma) o **REST/JSON** para modernos (ej. Cl@ve API).
    * *Normativa:* Cumplimiento de la **NTI de Protocolos de Intermediación de Datos**.

---

## 4. PASO 4: ESTRATEGIA DE AUTENTICACIÓN POR SUBSISTEMA

Asigna el método de seguridad correcto a cada pieza del puzle:

| Subsistema | Actor Principal | Método de Autenticación Recomendado |
| :--- | :--- | :--- |
| **Sede Electrónica** | Ciudadano | **Cl@ve** (Certificado, PIN, Permanente, Móvil). Nivel de seguridad según el trámite (Sustancial/Alto). |
| **Back-Office** | Funcionario | **AutenticA** (Repositorio horizontal de empleados públicos) o Certificado de Empleado Público (Pseudónimo/Cargo). |
| **Administración** | Admin TIC | **Doble Factor (2FA)** + VPN. (Requisito ENS para administradores). |
| **API / Servicios** | Sistemas Externos | **Certificado de Sello Electrónico** (para actuación automatizada y autenticación servidor-servidor). |

---