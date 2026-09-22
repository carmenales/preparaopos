# IDENTIFICACIÓN DE ACTORES Y SISTEMAS (ANÁLISIS Y MÉTODO)

Este documento combina la identificación de elementos del sistema con la metodología para extraerlos del enunciado.

---

## 1. GUÍA METODOLÓGICA DE LECTURA

Para no perder detalles en el examen, sigue este proceso mental:

1.  **Primera Lectura:** Comprensión general del problema.
2.  **Segunda Lectura (Extracción):** Apunta en sucio cada persona o sistema mencionado.
3.  **Tercera Lectura (Deducción):** Añade lo que falta por ley (ej. si hay firma, falta @firma; si hay tasas, falta Pasarela de Pagos).

---

## 2. IDENTIFICACIÓN DE ACTORES Y SISTEMAS (NO EXPLÍCITOS)

El objetivo es traducir los requisitos del negocio a la tecnología de la AGE, identificando los actores que intervienen obligatoriamente.

### 2.1. Preguntas Clave para Deducir Interfaces
| Pregunta Clave | Implicación Legal / Técnica | Solución AGE a Citar |
| :--- | :--- | :--- |
| **¿Cómo accede el usuario?** | Identificación de Ciudadano/Funcionario. | **Cl@ve** / **AutenticA** |
| **¿El trámite requiere voluntad?** | Firma electrónica (L39/2015). | **FIRe / @firma** y **Portafirmas** |
| **¿Hay documentos en el expediente?** | Gestión documental y almacenamiento ENI. | **INSIDE** (documentos) y **ARCHIVE** (archivo definitivo) |
| **¿Hay entrada/salida de documentos?** | Registro único oficial. | **GEISER/REGECO** y **SIR** (si es presencial) |
| **¿Se evitan documentos al ciudadano?** | Derecho a no aportar (L39/2015). | **Plataforma de Intermediación (PID)** |
| **¿Se notifica formalmente?** | Notificación obligatoria a DEHú. | **NOTIFIC@** (Servicio de Notificaciones Electrónicas) |
| **¿El funcionario actúa en nombre de otro?** | Comprobación de apoderamientos. | **Representa (REA)** y **HABILITA** |
| **¿Hay cobro de tasas?** | Pasarela de pagos del Estado. | **Pasarela de Pagos (PAGe)** |

### 2.2. Clasificación de Actores (Personas)
* **Externos:** Ciudadano, Empresa, Representante Legal (Sede Electrónica).
* **Internos:** Tramitador, Revisor, Firmante (Intranet/Red SARA).
* **Administración:** Administrador de Sistemas (Consola VPN).

### 2.3. Deducción de Sistemas Comunes (Interfaces)
Aunque no se nombren en el supuesto, se deduce su intervención:

* **Identidad:** Cl@ve, Autentic@.
* **Gestión Documental:** INSIDE, ARCHIVE.
* **Registro y Comunicación:** REGAGE, GEISER, NOTIFIC@ (DEHú), SIM.
* **Servicios Específicos:** PLATA, EGEO/GIS, PORTAFIRMAS.

---

## 3. MATRIZ DE CONTEXTO Y FLUJO (DIAGRAMA DE CONTEXTO)

Una vez identificados, deben organizarse para el Diagrama de Contexto (DFD Nivel 0).

### A. Tipos de Interfaces (Sistemas)
| Clasificación | Ejemplos |
| :--- | :--- |
| **Sistemas Internos** | Registro Propio, Data Warehouse, Plataforma de Firma Local, Legacy Systems, ERP/CRM. |
| **Sistemas Externos Comunes** | Cl@ve, @firma, INSIDE, NOTIFIC@, PID, Pasarela de Pagos. |
| **Sistemas Externos Otros** | BOE/BOPI, AEAT, Seguridad Social, Organismos Internacionales. |

### B. Flujo de Información (Entradas y Salidas)
| Tipo de Información | Ejemplos Típicos | Vinculación ENI |
| :--- | :--- | :--- |
| **Entrada (Input)** | Solicitud, Formularios de pago, Subsanaciones. | Documento Electrónico. |
| **Salida (Output)** | Recibo, Justificante, Resolución, Requerimiento. | Documento Electrónico (con CSV). |
| **Consulta (PID)** | Datos de Renta, Empadronamiento. | Protocolos de Intermediación. |

---

## 4. PREGUNTAS DE CONTROL Y COHERENCIA (CHECKLIST)

Para cada actor principal, plantéate:

1.  **¿Cómo accede?** (Sede vs Red SARA).
2.  **¿Cómo se autentica?** (Cl@ve vs Certificado).
3.  **¿Tiene que firmar?** (Integración AutoFirma/FIRe).
4.  **¿Hay pagos?** (Pasarela).

> **Regla de Oro de Coherencia:** Si identificas un actor aquí, debe aparecer con el mismo nombre en el Diagrama de Contexto, Casos de Uso y Secuencia.