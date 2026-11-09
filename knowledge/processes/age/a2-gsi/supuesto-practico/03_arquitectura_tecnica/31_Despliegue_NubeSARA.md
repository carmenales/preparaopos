# ARQUITECTURA FÍSICA Y DESPLIEGUE (NUBE SARA)

Este apartado cubre el **Diagrama de Despliegue**, donde definimos la infraestructura (Hardware/Nube), la redes y la seguridad perimetral. La clave aquí es la **Nube SARA** y el cumplimiento estricto del **ENS**.



[Image of 3 tier deployment diagram with DMZ and firewalls]


---

## 1. ELEMENTOS DEL DIAGRAMA (QUÉ DIBUJAR)

El diagrama debe representar una infraestructura segura con **defensa en profundidad**. Dibuja estos elementos:

1.  **Contenedor Principal:** Una caja grande llamada **"Nube SARA"** (o CPD del Organismo).
2.  **Zonas de Red (VLANs):**
    * **Zona DMZ (Desmilitarizada):** Accesible desde Internet. Aquí va el **Servidor Web** y el **Balanceador de Carga**.
    * **Zona de Aplicaciones (Interna):** Aquí va el **Servidor de Aplicaciones** (Business Logic).
    * **Zona de Datos (Crítica):** Aquí va el **Servidor de Base de Datos** y el almacenamiento (NAS/SAN).
3.  **Seguridad Perimetral:**
    * **Firewalls (Cortafuegos):** Separando Internet de la DMZ, y la DMZ de la red interna.
    * **Sondas CCN (SAT-INET):** Dibújala "escuchando" el tráfico en la entrada.
4.  **Conectividad Exterior:**
    * Una nube llamada **"Internet (Ciudadanos)"**.
    * Una nube llamada **"Red SARA (Funcionarios/Servicios Comunes)"**.

---

## 2. PLANTILLA DE JUSTIFICACIÓN TÉCNICA (TEXTO DE EXAMEN)

Este es el texto técnico (basado en los apuntes de referencia) que debes usar para defender tu diagrama ante el tribunal. Cita normativa específica (SUT, ENS, Guías CCN).

### 2.1. Introducción: Seguridad Integral
> *"El diseño de la arquitectura se basa en los principios del **Esquema Nacional de Seguridad (RD 311/2022)**, específicamente en la seguridad como proceso integral, la gestión basada en riesgos y la **defensa en profundidad**."*

### 2.2. Segmentación y Líneas de Defensa (ENS op.pl.2)
> *"Cumpliendo la medida **op.pl.2 (Arquitectura de Seguridad)**, se detalla un esquema de líneas de defensa para prevenir que una vulnerabilidad perfore todo el sistema.
> * **Segmentación:** Se segmenta la red en diferentes **VLANs** (medida **mp.com.4**) para acotar el acceso y evitar la propagación lateral de ataques.
> * **Perímetro:** Se utilizan Cortafuegos (Firewalls) para separar la zona pública (DMZ) de la zona de confianza (Aplicaciones y Datos)."*

### 2.3. Conectividad y SUT (Servicio Unificado de Telecomunicaciones)
> *"La conectividad se garantiza mediante el contrato centralizado de telecomunicaciones de la AGE:
> * **Red SARA (Lote 1 SUT):** Para el acceso de empleados públicos y la interconexión con otras AAPP y Servicios Comunes.
> * **Acceso a Internet (Lote 3 SUT):** Salida centralizada y segura para el acceso de ciudadanos a la Sede Electrónica."*

### 2.4. Accesos Remotos y VPN
> *"Para el teletrabajo o administración remota, se utilizarán **VPNs cifradas** cumpliendo la medida **mp.com.2** del ENS. Se configurarán según la **Guía CCN-STIC-836**, utilizando protocolo TLS 1.2 o superior para garantizar la confidencialidad."*

---

## 3. MONITORIZACIÓN DE SEGURIDAD (SAT)

Es vital mencionar las herramientas del **CCN-CERT** en el despliegue físico.

* **Sonda SAT-INET:** Se desplegará una sonda del Sistema de Alerta Temprana (SAT) en el punto de conexión a Internet para detectar amenazas en tiempo real.
* **Gestión de Incidentes:** La sonda reporta al CCN-CERT y al equipo de seguridad del organismo, facilitando la reacción ante ciberataques.

---

## 4. VENTAJAS DE LA NUBE SARA (Resumen)

Si te piden justificar por qué Nube SARA y no Amazon/Azure (Nube Pública):

1.  **Soberanía del Dato:** Los datos no salen de la infraestructura de la Administración (Cumplimiento RGPD/ENS simplificado).
2.  **Coste Eficiente:** Modelo de pago por uso interno (el dinero se queda en la AGE).
3.  **Interoperabilidad Nativa:** Conexión directa y de baja latencia con los Servicios Comunes (Cl@ve, Firma, Notifica) al estar en la misma red.