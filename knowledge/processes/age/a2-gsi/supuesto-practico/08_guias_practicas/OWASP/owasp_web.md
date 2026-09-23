---
title: OWASP Top 10 Aplicaciones Web
---

# 🛡️ OWASP Top 10

El **OWASP (Open Worldwide Application Security Project)** es una fundación global sin ánimo de lucro dedicada a mejorar la seguridad del software. Su proyecto más célebre es el **OWASP Top 10**, un documento de concienciación que sirve como estándar de facto en la industria de la ciberseguridad.

## Objetivo

Representa un consenso amplio de expertos sobre cuáles son los **10 riesgos de seguridad más críticos** para las aplicaciones web. Su objetivo principal es educar a desarrolladores, arquitectos y organizaciones, ayudándoles a priorizar sus esfuerzos defensivos y establecer una cultura de "seguridad desde el diseño" (*Security by Design*).


## Las 10 Vulnerabilidades Críticas

### A01:2025 - Pérdida de Control de Acceso (Broken Access Control)

Ocurre cuando la aplicación no verifica correctamente los permisos de un usuario, permitiendo que atacantes accedan a datos o funcionalidades fuera de su alcance.

#### Riesgos
* **Escalada de privilegios** (acceder a funciones de administrador siendo usuario raso).
* Manipulación de URLs para acceder a cuentas ajenas (**IDOR** - Insecure Direct Object Reference).
* Falsificación de solicitudes del lado del servidor (**SSRF** - Server-Side Request Forgery).

#### Mitigaciones
* Aplicar el **principio de mínimo privilegio** (denegar el acceso por defecto).
* Realizar las **verificaciones** de autorización únicamente en el **lado del servidor**. 
* Utilizar **identificadores impredecibles** (como UUID, en lugar de ID secuenciales).
* **Registrar (log)** todos los intentos de acceso no autorizado.

### A02:2025 - Configuración de Seguridad Incorrecta (Security Misconfiguration)

Se produce cuando la infraestructura, los frameworks o la propia aplicación no tienen definidos ajustes de seguridad adecuados o se mantienen valores de fábrica.

#### Riesgos
* Dejar **configuraciones inseguras por defecto** (como cuentas `admin/admin`).
* Mantener **servicios o puertos** innecesarios **habilitados** en el servidor.
* Carecer de **cabeceras de seguridad HTTP** (ej. Security Headers).
* Exponer **mensajes de error técnicos** (trazas de pila/stack traces) que revelan detalles internos del sistema.

#### Mitigaciones
* **Eliminar cuentas y características de muestra** antes de pasar a producción.
* Automatizar procesos de **endurecimiento (*hardening*)** del servidor.
* Configurar **páginas de error genéricas** para los usuarios.
* Forzar **políticas de seguridad en el cliente** implementando cabeceras como CSP y HSTS.

### A03:2025 - Fallas en la Cadena de Suministro de Software (Software Supply Chain Failures)

Surge al integrar componentes, bibliotecas o herramientas en el ciclo de desarrollo sin garantizar o verificar previamente su integridad y seguridad.

#### Riesgos
* Depender de **ecosistemas externos no controlados**.
* Usar **bibliotecas de terceros desactualizadas** o directamente maliciosas.
* Vulnerabilidades en los propios **sistemas de construcción e integración continua** (CI/CD).

#### Mitigaciones
* Adoptar una **Lista de Materiales de Software (SBOM)** para auditar y conocer todos los componentes.
* Usar herramientas de **escaneo automático de dependencias** (SCA).
* **Automatizar las actualizaciones** de librerías parcheadas.
* Asegurar los flujos CI/CD implementando **repositorios de paquetes internos y privados**.

### A04:2025 - Fallas Criptográficas (Cryptographic Failures)

Consiste en la desprotección de información sensible debido a la ausencia de cifrado o al uso de mecanismos de protección débiles.

#### Riesgos
* La **falta de cifrado** absoluto para proteger datos sensibles (contraseñas, datos financieros/médicos).
* Uso de **algoritmos obsoletos o rotos** (como MD5 o SHA1).
* Exposición de los datos tanto en **reposo** (base de datos) como en **transmisión** (red).

#### Mitigaciones
* Forzar siempre conexiones cifradas mediante **HTTPS/HSTS**.
* Utilizar **algoritmos de hash robustos con sal (salt)** (como bcrypt o Argon2) para contraseñas.
* **No almacenar claves criptográficas** directamente en el código fuente.
* Preferir **hardware especializado** (HSM) o **gestores de secretos** (Vaults).

### A05:2025 - Inyección (Injection)
Ocurre cuando un atacante logra engañar a un intérprete proporcionando datos o código malicioso que el sistema procesa como si fueran comandos legítimos.

#### Riesgos
* Enviar **datos proporcionados por el usuario a un intérprete** (como SQL, NoSQL, LDAP o OS) sin validarlos ni sanearlos.
* Ejecución de **comandos hostiles** en el servidor de base de datos o sistema operativo.
* Inyección de scripts en el navegador del cliente (**XSS** - Cross-site Scripting, integrado ahora en esta categoría).

#### Mitigaciones
* Usar siempre **consultas parametrizadas (*prepared statements*)** o herramientas **ORM**.
* Si no es posible parametrizar, se deben **validar, sanear y escapar estrictamente** todas las entradas del usuario (*Input validation*).

### A06:2025 - Diseño Inseguro (Insecure Design)

Se refiere a los riesgos derivados de fallos estructurales y conceptuales en la fase de arquitectura, donde no se han previsto o modelado las amenazas.

#### Riesgos
* **Decisiones arquitectónicas deficientes** tomadas antes incluso de escribir el código.
* Falta de **límites de velocidad (*rate limiting*)** (facilita la fuerza bruta y la saturación).
* **Fallos en la lógica de negocio** que un atacante puede explotar porque nunca se conceptualizó una defensa.

#### Mitigaciones
* Integrar el **"modelado de amenazas"** en las fases tempranas del ciclo de vida de desarrollo.
* Utilizar componentes que sean **seguros por defecto** (patrones de "camino pavimentado").
* Identificar proactivamente los **estados de falla esperados** para hacer el sistema resiliente.

### A07:2025 - Fallas de Autenticación (Authentication Failures)

Abarca las debilidades en los mecanismos que comprueban la identidad de un usuario, permitiendo que atacantes comprometan cuentas legítimas.

#### Riesgos
* Debilidades en los flujos de **inicio de sesión y manejo de sesiones**.
* Robo de cuentas mediante ataques de **fuerza bruta**.
* Uso de **contraseñas filtradas** (*credential stuffing*).
* **Robo o fijación de identificadores de sesión** (*session hijacking*).

#### Mitigaciones
* Obligar al uso de **Autenticación Multifactor (MFA)**.
* Implementar **bloqueos temporales de cuenta** tras varios intentos fallidos.
* Generar identificadores de sesión con **alta entropía** exclusivamente desde el servidor.
* Asegurar que las **sesiones expiren** tras un periodo de inactividad absoluto.

### A08:2025 - Fallas de Integridad del Software y de los Datos (Software or Data Integrity Failures)

Se produce cuando la aplicación o infraestructura asume como confiables componentes, datos o actualizaciones de software sin validar su origen.

#### Riesgos
* Falta de verificación al **recibir datos o actualizaciones** de software.
* Posibilitar la instalación o **inyección de software alterado** por un atacante.
* Ataques de **deserialización insegura** (donde objetos manipulados ejecutan código remoto RCE en el servidor al ser reconstruidos).

#### Mitigaciones
* Requerir **firmas digitales** (checksums) para verificar el origen y legitimidad del software/parches.
* **Nunca deserializar datos** que provengan de fuentes no confiables sin cifrado previo.
* Establecer **límites claros de confianza** entre los componentes de la aplicación.

### A09:2025 - Fallas en el Registro y Alerta de Seguridad (Security Logging and Alerting Failures)

Aparece cuando el sistema carece de mecanismos proactivos para registrar eventos y trazar la actividad sospechosa, dejando a los administradores "ciegos". 

#### Riesgos
* No guardar un **historial adecuado (logs)** de actividades críticas.
* **Falta de generación de alertas** proactivas ante un incidente.
* Permitir a los atacantes operar en el sistema **sin ser detectados** durante largos periodos (persistencia).

#### Mitigaciones
* **Registrar exhaustivamente** todos los fallos de acceso y autenticación (pero *sin* exponer datos sensibles en el log).
* **Centralizar los registros** en soluciones de monitoreo y correlación (como un SIEM).
* Configurar **alertas automáticas** ante umbrales o comportamientos anómalos.

### A10:2025 - Manejo Incorrecto de Condiciones Excepcionales (Mishandling of Exceptional Conditions)

Esta nueva categoría engloba la incapacidad del software para reaccionar de forma predecible y segura ante fallos sistémicos o entradas anómalas.

#### Riesgos
* Provocar **Denegaciones de Servicio (DoS)** por agotar la memoria al no liberar recursos de forma adecuada.
* Generar **transacciones corruptas** o datos huérfanos por caídas de red.
* **Exposición de información confidencial** a través de errores no capturados (unhandled exceptions).

#### Mitigaciones
* Implementar un **manejo de excepciones global y centralizado** (bloques try-catch estructurados).
* Adoptar el **principio de "fallar cerrado"** (si ocurre un error inusual, se deniega la acción y se cierra el acceso por seguridad).
* Asegurar que las transacciones complejas **se reviertan automáticamente** (*rollback*) en caso de interrupción.


## Tabla Resumen

| ID | Riesgo (Categoría) | Palabra Clave / Concepto | Defensa / Mitigación Principal |
|:---|:---|:---|:---|
| **A01** | Pérdida de Control de Acceso | Escalada de privilegios, IDOR, SSRF. | Principio de mínimo privilegio (Default Deny). |
| **A02** | Configuración Incorrecta | Cuentas por defecto, trazas de error expuestas. | Hardening, eliminar recursos innecesarios. |
| **A03** | Fallas Cadena Suministro | Librerías de terceros vulnerables, CI/CD débil. | SBOM (Lista de Materiales de Software), escaneo de dependencias. |
| **A04** | Fallas Criptográficas | MD5/SHA1, falta de HTTPS, contraseñas en plano. | Algoritmos robustos, proteger datos en tránsito y reposo. |
| **A05** | Inyección | SQLi, NoSQLi, XSS, falta de validación. | Consultas parametrizadas (Prepared Statements) / ORM. |
| **A06** | Diseño Inseguro | Fallos arquitectónicos, falta de límites (Rate limit). | Modelado de amenazas desde la fase inicial. |
| **A07** | Fallas de Autenticación | Robo de sesiones, fuerza bruta, passwords débiles. | Autenticación Multifactor (MFA), bloqueo de cuentas. |
| **A08** | Fallas de Integridad | Deserialización insegura, actualizaciones sin firmar. | Firmas digitales, validación estricta de fuentes. |
| **A09** | Fallas de Registro/Alerta | Falta de logs, atacantes indetectados. | Logs centralizados (SIEM), alertas proactivas. |
| **A10** | Manejo de Excepciones | Caídas por falta de memoria, exposición en errores. | Manejo global de excepciones, principio de "fallar cerrado". |

## Bibliografía
[OWASP TOP 10 - 2025](https://owasp.org/Top10/2025/)