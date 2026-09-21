# TECNOLOGÍAS DE ARQUITECTURA Y COMUNICACIONES

Este archivo justifica las elecciones técnicas en la **Capa Lógica** y la **Capa de Integración**, demostrando conocimiento en protocolos de interoperabilidad (ENI) y acceso a datos.

---

## 1. PROTOCOLOS DE COMUNICACIÓN (SOAP vs REST)

La elección del protocolo es fundamental para la **interoperabilidad** y el **rendimiento**.

| Característica | SOAP (Protocolo) | REST (Estilo Arquitectónico) | Criterio AGE |
| :--- | :--- | :--- | :--- |
| **Definición** | Protocolo estricto basado en XML. | Estilo basado en HTTP. | **Uso Mayoritario** |
| **Diseño** | Basado en **Operaciones**. | Basado en **Recursos** (URL). | **REST (Moderno)** |
| **Estado** | Con estado (difícil de escalar). | **Sin estado** (fácil de escalar). | **REST (Escalabilidad)** |
| **Seguridad** | WS-Security (sobrecarga). | HTTPS (TLS) nativo. | **REST (Rendimiento)** |

> **Criterio de Elección:** Se optará por servicios **RESTful** para integraciones nuevas y apps móviles por su eficiencia. **SOAP** se reservará para sistemas legacy (ej. versiones antiguas de @firma).

---

## 2. FORMATOS DE INTERCAMBIO (JSON vs XML)

Si se pide definir el formato de los datos, justifica la elección con esta tabla:

| Formato | Descripción | Ventajas (Justificación) | Desventajas |
| :--- | :--- | :--- | :--- |
| **JSON** | Formato ligero clave-valor. Estándar de **REST**. | **Eficiencia:** Menor tamaño, ideal para móviles y alto tráfico. **Simplicidad:** Fácil de procesar por navegadores (JS). | Validación de esquema menos estricta que XML. |
| **XML** | Formato jerárquico de etiquetas. Estándar de **SOAP**. | **Robustez:** Validación estricta (XML Schema) y soporte de firma digital avanzada (XAdES). | **Sobrecarga:** Mayor tamaño y consumo de CPU al procesar. |

---

## 3. MODELO OBJETO RELACIONAL (ORM)

### 3.1. Definición y Justificación
El **ORM** es la capa intermedia entre la Base de Datos Relacional y la Lógica de Negocio (Objetos).

* **Ventaja Crítica (Portabilidad):** Permite cambiar el motor de base de datos (ej. de Oracle a PostgreSQL) sin modificar el código.
* **Seguridad:** Evita la inyección SQL al utilizar consultas parametrizadas automáticamente.

### 3.2. Implementación AGE
* **Tecnología:** **JPA (Java Persistence API)** con implementación en **Hibernate**.

---

## 4. ELECCIÓN DE LA PILA TECNOLÓGICA (OPEN SOURCE)

En la AGE se prioriza el **Código Abierto** y la **Reutilización** para evitar el *vendor lock-in*.

### 4.1. Lenguaje y Framework
* **Opción Preferente:** **JAVA / Jakarta EE**. Es el estándar de facto por robustez, madurez y comunidad.
* **Alternativa:** **Python** solo si el proyecto es de Ciencia de Datos/IA.

### 4.2. Sistema Operativo del Servidor

| S.O. | Justificación de Elección |
| :--- | :--- |
| **Linux (Recomendado)** | **Coste Cero** (sin licencias), **Seguridad** (menos malware, gestión por terminal), **Eficiencia** (menor consumo de recursos). Ideal para servidores web (Apache/Nginx). |
| **Windows Server** | Solo si existe una fuerte dependencia de tecnologías propietarias (.NET / SharePoint). |

---