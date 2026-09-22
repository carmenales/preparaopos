# 42. PILAS TECNOLÓGICAS, SERVIDORES Y SUT

Este archivo integra la justificación técnica de la plataforma (Ecosistema, S.O., Servidor de Aplicaciones) dentro de los principios de **Código Abierto** y **Eficiencia** de la AGE.

---

## 1. ELECCIÓN ESTRATÉGICA DEL ECOSISTEMA

La AGE tiende a favorecer soluciones de **Código Abierto** para evitar el **'vendor lock-in'** (dependencia de un único proveedor como Microsoft) y optimizar los costes de licencia.

### 1.1. Ecosistema Java / Jakarta EE (Opción Preferente)
* **Lenguaje:** Java / Kotlin.
* **Justificación:** Robustez, madurez, alto rendimiento y su naturaleza de **código abierto** lo convierten en el estándar en la mayoría de los organismos.
* **Componentes Clave a Citar:**
    * **Frameworks:** Spring Framework o Jakarta EE.
    * **ORM:** Hibernate / JPA (Persistencia de Datos).
    * **Servidores de Aplicaciones:** **WildFly (JBoss)**, Payara o Apache TomEE.

### 1.2. Alternativas (A citar si el supuesto lo justifica)
* **Python:** Para proyectos de **Ciencia de Datos, Machine Learning** y análisis de datos (librerías Pandas, NumPy).
* **.NET Core (C#):** Solo si el organismo tiene un fuerte **LEGACY** (sistemas heredados) en productos de Microsoft.

---

## 2. SERVIDORES Y SISTEMAS OPERATIVOS (ELECCIÓN DEL S.O.)

La elección del S.O. y Servidor debe basarse en el **ahorro de costes** y la **seguridad**.

### 2.1. Comparativa de Sistemas Operativos (S.O.)

| Característica | Linux (Código Abierto) | Windows Server (Privativo) | Criterio AGE |
| :--- | :--- | :--- | :--- |
| **Coste** | Uso gratuito, sin costes de licencia. | Elevados costes de licencia por usuario. | **Linux (Eficiencia)** |
| **Seguridad** | Menos vulnerable a malware. Acceso solo por línea de comandos (terminal). | Potencialmente más vulnerable; la interfaz gráfica es un punto de ataque. | **Linux (Seguridad)** |
| **Recursos** | Bajos requisitos de hardware. | Requiere más recursos (por las interfaces gráficas). | **Linux (Eficiencia)** |

* **Conclusión AGE:** Se recomienda **Linux** (con servidores **Apache** o **Nginx**) como S.O. para servidores Web y de Aplicaciones por su robustez, seguridad y coste nulo de licencia.

### 2.2. Servidores de Aplicaciones (Contenedores)
El contenedor de Servlets es donde se despliega tu fichero `.WAR`.
* **Contenedor Web:** **Apache Tomcat**.
* **Servidores EE (Empresariales):** **WildFly (JBoss)** o **Payara**.

---

## 3. SERVICIO UNIFICADO DE TELECOMUNICACIONES (SUT)

El SUT es el contrato centralizado de la AGE para las comunicaciones. Citar estos lotes en el **Diagrama de Despliegue** demuestra conocimiento de infraestructura institucional.

| Lote SUT | Servicio (Lógica) | Justificación en el Supuesto |
| :--- | :--- | :--- |
| **Lote 1** | **Red SARA** | Conexión segura de la Intranet y del CPD con los **Servicios Comunes** y otras AA.PP. |
| **Lote 3** | **Acceso a Internet** | **Salida centralizada** y segura a Internet para el acceso de ciudadanos a la Sede Electrónica. |
| **Lote (VPN)** | **Accesos Remotos** | Conexión segura para **Administradores** y **Teletrabajadores** (Guía CCN-STIC-836). |

---

## 4. RELACIÓN CON OTROS ARCHIVOS

* Este contenido se aplica directamente en la justificación del archivo [Arquitectura Física y Despliegue](../3_Arquitectura_Tecnica/31_Despliegue_NubeSARA.md) y [Arquitectura de Paquetes](../2_Arquitectura_Logica/21_Arquitectura_Paquetes.md).

---