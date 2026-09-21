# 30. ARQUITECTURA DE COMPONENTES (ARTEFACTOS SOFTWARE)

El Diagrama de Componentes muestra cómo se agrupan las clases en módulos físicos (ficheros compilados, librerías, ejecutables). En el contexto de la AGE y Java (Jakarta EE), hablamos de ficheros **.WAR**, **.JAR** y **Librerías**.



---

## 1. ELEMENTOS DEL DIAGRAMA (QUÉ DIBUJAR)

Para un supuesto estándar (aplicación web de tramitación), tu diagrama debe identificar estos componentes clave:

### 1.1. Componente de Presentación (`Web.war`)
* **Descripción:** Fichero empaquetado desplegable en el servidor web/aplicaciones.
* **Contenido:** Ficheros HTML, CSS, JavaScript (Angular/React) y Controladores (Servlets/REST).
* **Dependencias:** Requiere la interfaz de la Lógica de Negocio.

### 1.2. Componente de Negocio (`Core.jar` o EJB)
* **Descripción:** Librería o módulo que contiene las reglas del negocio.
* **Contenido:** Clases de servicio, gestión del expediente, validaciones.
* **Interfaces:**
    * Ofrece: `Interfaz_Tramitacion` (usada por la web).
    * Requiere: `Interfaz_Persistencia` y `Interfaz_ServiciosExternos`.

### 1.3. Componentes de Integración (Los "Connectors")
Es vital dibujar componentes separados para los servicios comunes para demostrar desacoplamiento.

* **`Cliente_Inside.jar`:** Encapsula la complejidad de llamar a los Web Services de INSIDE.
* **`Cliente_Clave.jar`:** Gestiona las redirecciones SAML con Cl@ve.
* **`Cliente_Firma.jar`:** Gestiona la comunicación con FIRe/@firma.

### 1.4. Componente de Datos
* **`Persistencia.jar`:** Implementación de DAO/Repository (Hibernate).
* **`Driver_JDBC.jar`:** El driver específico de la base de datos (Oracle/PostgreSQL).

---

## 2. NOTACIÓN UML CLAVE

* **Componente:** Una caja con un icono de componente en la esquina superior derecha.
* **Interfaz (Lollipop):**
    * **Círculo completo (Bola):** Interfaz Proporcionada (lo que el componente "ofrece" al mundo).
    * **Medio círculo (Copa):** Interfaz Requerida (lo que el componente "necesita" para funcionar).
* **Dependencia:** Línea discontinua con flecha.

---

## 3. PLANTILLA DE JUSTIFICACIÓN TÉCNICA

> **Defensa del Diseño Modular:**
> "El sistema se ha estructurado en componentes desacoplados para facilitar el mantenimiento correctivo y evolutivo.
>
> 1.  **Desacoplamiento:** La separación de la lógica de integración en componentes independientes (`Cliente_Inside.jar`, etc.) permite actualizar las versiones de los Servicios Comunes de la AGE sin afectar al núcleo del negocio.
> 2.  **Intercambiabilidad:** El uso de interfaces para la persistencia permite cambiar el motor de base de datos (ej. de Oracle a PostgreSQL) sustituyendo únicamente el componente de acceso a datos y el driver JDBC, sin reescribir la lógica de negocio.
> 3.  **Seguridad:** Las librerías de terceros se gestionarán mediante un repositorio de artefactos seguro (ej. Nexus) para controlar vulnerabilidades y asegurar la cadena de suministro de software."

---