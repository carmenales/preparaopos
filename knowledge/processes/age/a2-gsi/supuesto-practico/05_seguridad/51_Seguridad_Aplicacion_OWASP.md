# SEGURIDAD EN EL DESARROLLO (OWASP Y ANTI-HACKING)

Además de la seguridad perimetral (Firewalls), es obligatorio proteger el **código** de la aplicación. Nos basamos en el **OWASP Top 10** (Estándar de seguridad de aplicaciones web).

---

## 1. AMENAZA CRÍTICA: INYECCIÓN SQL (SQL Injection)

Es el ataque más común citado en exámenes. Ocurre cuando un atacante introduce código SQL malicioso en un formulario (ej. en el campo usuario pone `' OR 1=1 --`) para manipular la base de datos.

### Medidas de Protección (Solución Técnica)
Para evitar la inyección SQL, se implementarán estas 3 barreras:

1.  **Consultas Parametrizadas (Prepared Statements):**
    * *Explicación:* Nunca concatenar cadenas de texto para crear consultas. Usar las herramientas del lenguaje (Java/JDBC) que separan el código de los datos.
    * *Justificación:* "El uso de `PreparedStatement` en Java asegura que la base de datos trate la entrada del usuario como datos literales, nunca como comandos ejecutables."
2.  **Uso de ORM (Hibernate/JPA):**
    * Los frameworks de persistencia modernos generan el SQL automáticamente y sanitizan las entradas por defecto.
3.  **Validación de Entrada (Input Validation):**
    * Validar en el servidor que los datos tienen el formato esperado (ej. que un DNI tenga 8 números y una letra, no símbolos extraños).

---

## 2. OTRAS AMENAZAS WEB (OWASP)

### 2.1. Cross-Site Scripting (XSS)
* **Ataque:** Inyectar scripts (JavaScript) en la web para robar sesiones de otros usuarios.
* **Solución:** **Sanitización de Salida** (Escapar caracteres especiales HTML) y uso de cabeceras de seguridad (Content Security Policy).

### 2.2. Pérdida de Control de Acceso (Broken Access Control)
* **Ataque:** Un usuario accede a un expediente que no es suyo cambiando el ID en la URL (ej. `/expediente/105` -> `/expediente/106`).
* **Solución:** Verificar siempre en el servidor, mediante la sesión de **AutenticA** o **Cl@ve**, si el usuario tiene permisos sobre el objeto solicitado antes de mostrarlo.

---

## 3. PROTECCIÓN PERIMETRAL DE APLICACIÓN (WAF)

Además del código, se desplegará un **WAF (Web Application Firewall)** en la zona DMZ.
* **Función:** Analiza el tráfico HTTP/HTTPS y bloquea patrones de ataque conocidos (SQLi, XSS) antes de que lleguen al servidor web.

---