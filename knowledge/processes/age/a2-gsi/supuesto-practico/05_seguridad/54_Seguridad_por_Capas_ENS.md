# 54. MEDIDAS DE SEGURIDAD ENS POR CAPAS (LÓGICO Y FÍSICO)

El Esquema Nacional de Seguridad (ENS) clasifica las medidas en familias que se pueden justificar fácilmente en capas. Esta estructura es la más útil para supuestos prácticos.

---

## 1. SEGURIDAD ORGANIZATIVA (ENS – Marco Organizativo)

**Objetivo:** Demostrar que el sistema se gobierna, documenta, revisa y supervisa.

### Medidas Típicas
* Política de seguridad aprobada y difundida.
* Roles y responsabilidades definidos (RSI, responsables de servicio, administradores).
* Procedimientos documentados.
* Ciclo de vida de mejora continua.
* Gestión de riesgos periódica.
* Clasificación de la información y activos.
* Formación y concienciación de usuarios.

> **Frase tipo para respuesta (con códigos):**
> "El sistema se encuadra en una política de seguridad aprobada formalmente **[org.pol]**, con roles y responsabilidades definidos **[org.org]** y procedimientos documentados, aplicando un ciclo de mejora continua y gestión de riesgos **[org.gesr]** en línea con los requisitos del ENS."

---

## 2. SEGURIDAD FÍSICA (ENS – Medidas de Protección – Entorno)

**Objetivo:** Proteger instalaciones, centros de proceso de datos, puestos, equipos y cableado.

### Medidas Típicas
* Control de acceso a salas técnicas (tarjeta, PIN, biometría).
* Registro de accesos.
* CCTV en perímetro.
* Armarios y racks cerrados.
* Señalización de zonas restringidas.
* Detección y extinción de incendios.
* SAI y grupo electrógeno.
* Control de temperatura y humedad.
* Protección de cableado físico.
* Centros redundantes.

> **Frase tipo para examen (con códigos):**
> "Se asegura la protección física de las instalaciones **[mp.if]** mediante control de accesos a la sala técnica y CCTV perimetral; y la protección del equipamiento **[mp.eq]** mediante racks cerrados, SAI, climatización supervisada y medidas de detección y extinción automática, garantizando disponibilidad e integridad."

---

## 3. SEGURIDAD LÓGICA (ENS – Control de Acceso y Protección)

**Objetivo:** Proteger sistemas, identidades, software, aplicaciones, autenticación y privilegios.

### Medidas Típicas
* Autenticación robusta (MFA en sistemas críticos).
* Gestión de identidades y accesos (IAM).
* Principio de mínimo privilegio.
* Segregación de funciones (admin / auditor).
* Roles y permisos revisados periódicamente.
* Cifrado de información en tránsito y reposo.
* Protección contra malware.
* Gestión de parches y actualizaciones.
* Endpoints con endurecimiento (hardening) y configuración segura.
* Contraseñas en política establecida conforme al ENS.

> **Frase tipo para examen (con códigos):**
> "El acceso lógico se controla mediante autenticación robusta **[op.acc.6]**, gestión centralizada de identidades y permisos basados en roles (principio de mínimo privilegio **[op.acc]**). Se aplica cifrado de la información en tránsito y en reposo **[mp.info.6]** y segregación de funciones."

---

## 4. OPERACIÓN Y EXPLOTACIÓN (ENS – Operación Segura)

**Objetivo:** Garantizar que la explotación del servicio es segura durante su vida útil.

### Medidas Típicas
* Gestión de parches periódica.
* Inventario de equipos y software.
* Hardening de sistemas operativos.
* Configuraciones basadas en estándares (CIS, CCN-STIC).
* Copias de seguridad verificadas y probadas.
* Procesos documentados: cambio, despliegue, mantenimiento.
* Antivirus/EDR instalado y centralizado.
* Plan de gestión de incidentes con escalado.

> **Frase tipo para examen (con códigos):**
> "La operación se gestiona mediante procedimientos formalizados de cambio **[op.exp.11]**, gestión de la configuración **[op.exp.2]**, parcheo y copias de seguridad verificadas **[mp.info.9]**, contando con monitorización activa y protección contra código dañino **[op.exp.5]**."

---

## 5. COMUNICACIONES Y REDES (ENS – Protección del Tráfico)

**Objetivo:** Proteger el tráfico de red entre elementos del sistema.

### Medidas Típicas
* Segmentación / VLAN.
* Zonas desmilitarizadas (DMZ).
* Cortafuegos perimetrales e internos.
* IDS/IPS y monitorización de tráfico.
* VPN corporativa con cifrado robusto.
* Control de acceso a red (NAC).
* Filtrado de puertos, protocolos y aplicaciones.
* Gestión de certificados digitales.
* DNS seguro.

> **Frase tipo para examen (con códigos):**
> "La red se asegura mediante segmentación en VLAN **[mp.com.4]**, arquitectura de defensa en profundidad con cortafuegos perimetrales e internos **[op.pl.2]**, cifrado en los canales de comunicación **[mp.com.2]** y monitorización del tráfico con IDS/IPS."

---

## 6. SEGURIDAD EN EL CICLO DE VIDA (ENS – Adquisición y Desarrollo)

**Objetivo:** Garantizar seguridad desde el diseño hasta el mantenimiento.

### Medidas Típicas
* Validación de seguridad en análisis y diseño.
* Integración de requisitos desde el pliego.
* Auditorías de código (cuando proceda).
* Pruebas de caja blanca o negra (según criticidad).
* Documentación actualizada del sistema.
* Gestión de proveedores y subcontratación.

> **Frase tipo para examen (con códigos):**
> "La seguridad se integra desde la fase de diseño **[mp.sw.1]**, exigiendo controles en los pliegos **[op.adq]**, pruebas de aceptación de seguridad **[mp.sw.2]** y documentación actualizada."

---

## 7. CONTINUIDAD, RECUPERACIÓN Y RESILIENCIA (ENS – Disponibilidad)

**Objetivo:** Garantizar continuidad del servicio ante fallos, ataques o desastres.

### Medidas Típicas
* Plan de continuidad y plan de recuperación (PCN / DRP).
* CPD secundario o réplica.
* Backups locales y remotos.
* Tiempos RTO y RPO definidos.
* Ensayos periódicos.
* Procedimiento manual o alternativo documentado.
* Gestión de crisis y comunicación.

> **Frase tipo para examen (con códigos):**
> "El servicio dispone de Plan de Continuidad **[op.cont]** probado periódicamente, con copias de seguridad remotas **[mp.info.9]**, punto de restauración (RPO) definido y procedimientos de actuación, garantizando la disponibilidad."

---

## 8. MONITORIZACIÓN, REGISTRO Y AUDITORÍA (ENS – Detección)

**Objetivo:** Detectar comportamientos anómalos y garantizar trazabilidad.

### Medidas Típicas
* SIEM centralizado.
* Recolección y correlación de eventos.
* Registros protegidos contra manipulación.
* Alarmas ante actividades sospechosas.
* Auditorías periódicas.
* Revisiones del cumplimiento ENS cada 2 años.

> **Frase tipo para examen (con códigos):**
> "Se habilita un sistema de monitorización **[op.mon]** y registro centralizado, con correlación de eventos y protección de logs, permitiendo el registro de actividad de los usuarios **[op.exp.8]**, detección temprana de incidentes y auditoría."

---

## 9. PLANTILLA PARA RESPONDER EN 10 LÍNEAS (EL RESUMEN)

Esta plantilla sirve para responder casi cualquier pregunta de "Justifique las medidas de seguridad":

> "Se aplican medidas de seguridad conforme al ENS, organizadas por capas:
> 
> 1. **Organizativa:** Política de seguridad formal **[org.pol]**, roles definidos y procedimientos documentados.
> 2. **Física:** Control de acceso **[mp.if]**, CCTV, racks cerrados, sistemas de detección y extinción y CPD con SAI.
> 3. **Lógica:** Autenticación robusta **[op.acc.6]**, permisos por rol y cifrado en tránsito y reposo.
> 4. **Operación:** Gestión de parches, copias verificadas **[mp.info.9]** y supervisión de explotación.
> 5. **Comunicaciones:** Segmentación **[mp.com.4]**, cortafuegos, VPN y monitorización de red.
> 6. **Ciclo de vida:** Seguridad integrada desde diseño **[mp.sw.1]** y control en adquisición.
> 7. **Continuidad:** Plan de recuperación probado **[op.cont]**, RTO/RPO definidos y backups remotos.
> 8. **Auditoría:** Registro centralizado, correlación de eventos y revisión periódica ENS."

---

## 10. EJEMPLO APLICADO A SUPUESTO REALISTA (RESUMIDO)

*"Las medidas de seguridad aplicadas al sistema se alinean con el ENS. A nivel organizativo, se dispone de política de seguridad y roles asignados. A nivel físico se asegura el CPD mediante control de accesos, vigilancia, racks especializados, SAI y detección y extinción automática. En seguridad lógica se integra autenticación fuerte **[op.acc.6]**, permisos basados en roles y cifrado de la información. En explotación se aplican procesos de parcheo y copias verificadas. Las comunicaciones se protegen mediante segmentación por VLAN, cortafuegos, VPN cifrada e IDS/IPS **[mp.com]**. Se integra seguridad desde el diseño y la continuidad se garantiza mediante plan de recuperación probado. Finalmente, un sistema de registro centralizado permite trazabilidad y auditoría conforme al ENS."*