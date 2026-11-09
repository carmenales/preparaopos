# CATÁLOGO DE MÓDULOS SOFTWARE Y WORKFLOW

Para diseñar la solución, no reinventamos la rueda. Utilizamos módulos de mercado (Open Source o Propietarios) y soluciones del CTT.

---

## 1. EL MOTOR DE WORKFLOW (BPM)

Es el corazón de la tramitación administrativa. Automatiza el flujo del expediente.

### 1.1. ¿Qué es y para qué sirve?
Componente que orquesta las tareas, usuarios y documentos.

* **Automatización:** Asigna tareas automáticamente (ej. "Revisar Solicitud" al tramitador).
* **Reglas de Negocio:** Decide el camino (ej. Si `importe > 1000`, requiere firma del Jefe).
* **Trazabilidad:** Registra quién hizo qué y cuándo (Auditoría).

### 1.2. Ejemplo de Uso en Supuesto
> *"Para la gestión del expediente, se integrará un Motor de Workflow (BPM) que orquestará las fases del procedimiento: desde la entrada en Registro, pasando por la validación automática de reglas, hasta la generación de la Resolución y su envío a Portafirmas."*

---

## 2. MÓDULOS HABITUALES (CAJA DE HERRAMIENTAS)

Al definir la arquitectura lógica, puedes citar estos productos concretos para dar realismo.

| Categoría | Función | Soluciones Open Source | Soluciones Propietarias |
| :--- | :--- | :--- | :--- |
| **Gestor de Portales (CMS)** | Crear la Sede Electrónica. | **Liferay**, Drupal, WordPress. | Oracle WebCenter, SharePoint. |
| **Gestor Documental (ECM)** | Almacenar documentos (si no usas solo INSIDE). | **Alfresco**, OpenKM. | Documentum, SharePoint. |
| **Workflow (BPM)** | Tramitación de expedientes. | **Bonita BPM**, Camunda. | Bizagi, Appian. |
| **Business Intelligence (BI)** | Cuadros de Mando y Estadísticas. | **Pentaho**, Grafana (Monitorización). | Power BI, Tableau, QlikView. |
| **Bus de Servicios (ESB)** | Integración entre aplicaciones. | **WSO2**, Red Hat Fuse. | Oracle Service Bus, MuleSoft. |

> **Nota CTT:** Siempre se debe mencionar que se consultará el **CTT** (Centro de Transferencia de Tecnología) antes de adquirir licencias, priorizando soluciones reutilizables de la AGE (como **ACCEDA** para tramitación).

---