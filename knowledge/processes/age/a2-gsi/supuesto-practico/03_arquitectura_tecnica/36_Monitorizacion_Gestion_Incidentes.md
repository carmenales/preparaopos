# MONITORIZACIÓN, EVENTOS Y GESTIÓN DE INCIDENTES

La vigilancia del sistema es una obligación del ENS (medida **op.mon**). Debemos distinguir entre monitorización de sistemas (rendimiento) y monitorización de seguridad (eventos/ataques).

---

## 1. NIVELES DE MONITORIZACIÓN

El sistema contará con una arquitectura de monitorización a tres niveles:

### 1.1. Monitorización de Infraestructura y Red (NOC)
* **Objetivo:** Saber si los servidores están "vivos" (Up/Down), consumo de CPU, Disco y Ancho de Banda.
* **Protocolo:** SNMP / Agentes.
* **Herramientas (Open Source):** **Nagios**, **Zabbix**, Prometheus.

### 1.2. Monitorización de Aplicación (APM)
* **Objetivo:** Saber si la aplicación responde rápido, si hay errores Java, o cuellos de botella en la Base de Datos.
* **Herramientas:** Dynatrace, AppDynamics, o stacks ELK (Elasticsearch, Logstash, Kibana).

### 1.3. Monitorización de Seguridad (SOC) - **CRÍTICO ENS**
* **Objetivo:** Detectar intrusiones, accesos indebidos o anomalías.
* **Herramienta Clave:** **SIEM** (Gestor de Información y Eventos de Seguridad).
    * Recolecta logs de Firewalls, Servidores y Aplicaciones.
    * Correlaciona eventos (ej. "5 intentos fallidos de login + acceso desde IP extranjera = Alerta").
* **Sondas:** Despliegue de **SAT-INET** (Sonda del CCN).

---

## 2. GESTIÓN DE LOGS (REGISTRO DE ACTIVIDAD)

Cumplimiento de la medida **[op.exp.8] Registro de la actividad de los usuarios**:

* **Qué registrar:** Identidad del usuario, Fecha/Hora, Recurso accedido, Acción realizada, Resultado (Éxito/Fallo).
* **Protección:** Los logs deben firmarse o almacenarse en un servidor syslog remoto para evitar su manipulación por un atacante (integridad).

---

## 3. GESTIÓN DE INCIDENTES DE SEGURIDAD

Si la monitorización detecta una alerta, se activa el Procedimiento de Gestión de Incidentes (Guía **CCN-STIC-817**).

### 3.1. Herramienta LUCIA (CCN-CERT)
En la AGE, se recomienda el uso de **LUCIA** (Listado Unificado de Coordinación de Incidentes y Amenazas) para:

* Gestionar el ciclo de vida del incidente.
* **Notificar** incidentes al CCN-CERT (obligatorio para Categoría Media/Alta según ENS).

### 3.2. Ciclo de Vida del Incidente
1.  **Detección:** Alerta del SIEM o reporte de usuario (CAU).
2.  **Triaje/Clasificación:** Determinar impacto y prioridad.
3.  **Contención:** Aislar el equipo infectado o bloquear la IP atacante en el Firewall.
4.  **Erradicación:** Eliminar la amenaza (limpiar malware, parchear vulnerabilidad).
5.  **Recuperación:** Restaurar servicio desde **Backup** (Archive).
6.  **Lecciones Aprendidas:** Actualizar la base de conocimiento.

---