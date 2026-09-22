# SUPUESTO PRÁCTICO RESUELTO: GESTIÓN DE SUBVENCIONES

**Enunciado Tipo:** "El Ministerio X necesita un sistema para la tramitación telemática de solicitudes de ayuda al alquiler. Se requiere gestión completa desde la solicitud hasta la notificación, asegurando la interoperabilidad."

---

## 1. INTRODUCCIÓN Y ESTRATEGIA

> *La Administración Pública, en su compromiso de servir con objetividad los intereses generales (Art. 103 CE), ha diseñado el sistema 'SIGES-AYUDAS' con el objetivo de **reutilizar los servicios comunes del Estado** (Art. 157 Ley 40/2015), en un marco de eficiencia y contención del gasto.*
>
> *El proyecto se alinea con el **Plan de Digitalización de las AAPP 2021-2025**, garantizando el cumplimiento de la **Ley 39/2015** (derechos de los ciudadanos) y la **Ley 40/2015** (régimen jurídico). El diseño observará estrictamente el **Esquema Nacional de Seguridad (ENS)** y el **Esquema Nacional de Interoperabilidad (ENI)**.*

---

## 2. ANÁLISIS FUNCIONAL (ACTORES E INTERFACES)

### 2.1. Identificación de Actores
* **Ciudadano (Solicitante):** Accede a la Sede Electrónica.
* **Representante:** Actúa en nombre del solicitante (Requiere validación en **Representa**).
* **Funcionario Tramitador:** Accede desde la Intranet (Red SARA) para validar y resolver.
* **Sistemas Externos (Interfaces):** Cl@ve, @firma, AEAT/Catastro (vía PID), Notifica, GEISER.

### 2.2. Solución Funcional (Tabla de Requisitos y Servicios)
Para cada fase del trámite administrativo, se propone la solución horizontal de la AGE:

| Fase del Trámite | Requisito Funcional | Solución Técnica (Servicio Común) |
| :--- | :--- | :--- |
| **1. Acceso** | Identificación segura del solicitante. | **Cl@ve** (Nivel Sustancial/Alto) y **Representa** (si actúa por otro). |
| **2. Solicitud** | Formulario web y aportar datos. | **PID** (Consulta de Renta en AEAT y Propiedad en Catastro - Derecho a no aportar). |
| **3. Firma** | Firma electrónica de la solicitud. | **FIRe** (integrado con AutoFirma o Firma en Nube). |
| **4. Registro** | Asiento registral de entrada y recibo. | **GEISER / REGECO**. |
| **5. Tramitación** | Conformación del expediente y validación. | **INSIDE** (Expediente ENI) y **Portafirmas** (para la resolución del funcionario). |
| **6. Notificación** | Comunicar la concesión/denegación. | **Notifica** (Puesta a disposición en la DEHú). |



---

## 3. MODELO DE DATOS (CUMPLIMIENTO ENI/RGPD)

Se propone un modelo relacional normalizado (3FN) que cumple con las Normas Técnicas de Interoperabilidad (NTI).

### 3.1. Entidades Clave y Atributos NTI
* **Clase `Expediente`:**
    * `codigo_SIA`: Identificador del procedimiento (Interoperabilidad semántica).
    * `Indice_Electronico`: Relación de composición. XML firmado que garantiza la integridad del expediente (Obligación ENI).
* **Clase `Documento`:**
    * `Metadatos_ENI`: Atributos obligatorios (Órgano, Fecha Captura, Tipo Documental, Estado Elaboración).
    * `CSV`: Código Seguro de Verificación para cotejo.
* **Clase `Interesado`:**
    * `Datos_Personales`: Diseñado bajo el principio de **Minimización** (RGPD). Los datos económicos sensibles se almacenarán cifrados.



---

## 4. ARQUITECTURA TÉCNICA (4 CAPAS)

Se propone una arquitectura multicapa modular para garantizar el desacoplamiento y la mantenibilidad.

### 4.1. Diagrama de Paquetes (Lógica)
1.  **Capa de Presentación:** Portal Web Responsive (HTML5/Angular) cumpliendo **Accesibilidad AA** (RD 1112/2018) y Usabilidad.
2.  **Capa de Negocio:** Implementada en **Java (Jakarta EE)**. Contiene la lógica de baremación de la ayuda.
3.  **Capa de Integración (Servicios):** Módulo específico que aísla la lógica de negocio de los conectores externos:
    * `Conector_Inside`: Gestión documental.
    * `Conector_Clave`: Gestión de identidad.
    * `Conector_Intermediacion`: Cliente SVD (PID).
4.  **Capa de Datos:** Persistencia abstraída mediante ORM (**Hibernate**) sobre base de datos relacional.



[Image of 4-tier architecture diagram]


### 4.2. Diagrama de Despliegue (Física)
* **Infraestructura:** Despliegue en **Nube SARA** (Soberanía del dato y eficiencia).
* **Seguridad (Defensa en Profundidad):**
    * Segmentación de red en **VLANs** (DMZ, Aplicaciones, Datos).
    * Despliegue de **Cortafuegos** perimetrales e internos.
    * Monitorización mediante sonda **SAT-INET** (CCN-CERT).

---

## 5. SEGURIDAD (CATEGORIZACIÓN ENS)

El sistema maneja datos personales y económicos, lo que exige un análisis riguroso.

### 5.1. Valoración de Dimensiones
* **Disponibilidad (D): MEDIO.** La caída del servicio impediría solicitar la ayuda en plazo, causando un perjuicio grave a los derechos de los ciudadanos.
* **Confidencialidad (C): MEDIO.** Se tratan datos personales y económicos (Renta).
* **Integridad (I): MEDIO.** La alteración no autorizada de los datos podría derivar en la concesión de ayudas indebidas (fraude).
* **Trazabilidad (T) y Autenticidad (A): MEDIO.**

### 5.2. Categoría del Sistema
Al ser las dimensiones predominantes de nivel MEDIO, el sistema se clasifica como **CATEGORÍA MEDIA**.

### 5.3. Medidas de Seguridad (Anexo II)
Se aplicarán, entre otras:

* **[op.acc]** Identificación robusta (Cl@ve).
* **[mp.com.2]** Protección de comunicaciones (Cifrado TLS 1.2+).
* **[op.bcp]** Plan de Continuidad de Negocio y copias de seguridad en **Archive**.

---