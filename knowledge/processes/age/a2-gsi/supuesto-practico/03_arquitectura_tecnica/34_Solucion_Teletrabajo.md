# SOLUCIÓN TÉCNICA: TELETRABAJO Y SEGURIDAD CPD

Este archivo responde a las preguntas sobre implantación de teletrabajo (VPN vs VDI) y seguridad física/lógica del CPD.

---

## 1. ESTRATEGIA DE TELETRABAJO (SOLUCIÓN TÉCNICA)

Ante la pregunta "¿Qué usamos para teletrabajo?", la respuesta recomendada por eficiencia y seguridad es **VPN**.

### 1.1. Modelo de Conectividad: VPN (Red Privada Virtual)
* **Justificación:** Es la solución más coste-eficiente frente a los escritorios virtuales (VDI).
* **Implementación:** El firewall del CPD actuará como terminador de túneles **IPSec** o **TLS**.
* **Seguridad (ENS mp.com.2):** El canal está cifrado, garantizando la confidencialidad.

### 1.2. Tendencia: El "Puesto Único"
Se descarta el uso de ordenadores personales domésticos (BYOD inseguro) en favor del puesto único corporativo:

1.  **Hardware:** El empleado tiene un único portátil corporativo para oficina y casa.
2.  **Seguridad del Endpoint:** El disco duro está **cifrado** (BitLocker/FileVault) y cuenta con **EDR** (Antivirus avanzado) y **MDM** (Gestión remota) para borrado a distancia en caso de pérdida.
3.  **Datos:** No residen en local. Se trabaja contra la nube securizada (**Nube SARA** / OneDrive corporativo).

---

## 2. SEGURIDAD FÍSICA Y LÓGICA DEL CPD (ENS)

Esquema de seguridad para proteger la infraestructura.

### 2.1. Seguridad Física (El Búnker)
* **Control de Acceso:** Doble factor (Tarjeta + Pin/Biometría).
* **Protección del Hardware:** Racks enjaulados ("Cages") con llave.
* **Ambiental:** Sistemas anti-incendios (gas inerte), detección de agua, SAIs redundantes.

### 2.2. Seguridad Lógica (La Cebolla)
* **Defensa en Profundidad (Esquema de la Cebolla):** Diferentes capas de seguridad (Nivel 0, 1, 2). Si cae una barrera, hay otra.
* **Perímetro:**
    * **Firewalls:** Puntos únicos de acceso.
    * **IDS/IPS:** Detección y prevención de intrusiones.
    * **WAF (Web Application Firewall):** Para filtrar ataques a la capa web (SQL Injection, XSS).
* **Red:** Uso de **VLANs** para segregar tráfico (Gestión, Usuarios, Servidores).
* **Gestión:** Principio de **Mínimo Privilegio** y **Segregación de Funciones** (el que administra la BBDD no administra el S.O.).

---