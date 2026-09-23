---
title: OWASP Mobile Top 10 (2024)
---

# 📱 OWASP Mobile Top 10 

El **OWASP Mobile Top 10** es un documento de concienciación homólogo al Top 10 de aplicaciones web, pero centrado específicamente en los riesgos de seguridad más críticos que afectan a los ecosistemas móviles (Android e iOS).

## Objetivo

Proporcionar a los desarrolladores y equipos de seguridad una guía fundamental sobre cómo construir, probar y mantener aplicaciones móviles seguras, destacando las vulnerabilidades inherentes a la arquitectura de los dispositivos móviles (como el almacenamiento local, la comunicación inalámbrica y la ingeniería inversa de los binarios).


## Las 10 Vulnerabilidades Críticas en Movilidad

### M1: Uso inadecuado de credenciales (Improper Credential Usage)

Consiste en la gestión, almacenamiento y uso inseguro de credenciales por parte de la propia aplicación móvil.

#### Riesgos
* Presencia de **contraseñas hardcodeadas** (codificadas en texto plano dentro del código fuente de la app).
* **Claves API expuestas** directamente en el código.
* Almacenar **tokens o sesiones sin cifrar** en el dispositivo.

#### Mitigaciones
* **Evitar incrustar credenciales** fijas en el código de la app.
* Utilizar **sistemas seguros de almacenamiento** respaldados por el hardware del dispositivo (como el *Keychain* en iOS o *Keystore* en Android).
* Implementar mecanismos para **rotar periódicamente** las claves de las APIs.

### M2: Seguridad inadecuada en la cadena de suministro (Inadequate Supply Chain Security)

Se refiere a las vulnerabilidades introducidas a través de componentes externos utilizados en la construcción de la aplicación.

#### Riesgos
* Utilización de **bibliotecas de terceros o componentes de código abierto** vulnerables.
* Integración de **SDKs (Software Development Kits)** publicitarios o analíticos que tienen fallos de seguridad o exponen datos.

> *Nota: Si un componente de terceros falla, la app móvil hereda ese riesgo.*

#### Mitigaciones
* Mantener un inventario detallado de componentes de software **(SBOM - Software Bill of Materials)**.
* Analizar periódicamente las dependencias en busca de **vulnerabilidades conocidas (CVEs)**.
* Utilizar solo **SDKs de confianza** y firmar criptográficamente las versiones.

### M3: Autenticación / Autorización insegura (Insecure Authentication/Authorization)

Agrupa los fallos en la forma en que la app verifica la identidad del usuario o comprueba sus permisos antes de otorgar acceso a los recursos.

#### Riesgos
* Capacidad de **evadir la pantalla de inicio de sesión** forzando vistas internas.
* Generación de **tokens predecibles** o débiles.
* **No invalidar las sesiones** de manera segura en el servidor tras cerrar sesión en la app.

#### Mitigaciones
* **Delegar siempre las decisiones** de autenticación y autorización al backend (servidor).
* **No confiar en los controles de sesión** realizados únicamente en el lado del cliente (el dispositivo móvil).
* Implementar **Autenticación Multifactor (MFA)** y asegurar la expiración estricta de los tokens.

### M4: Validación insuficiente de entrada/salida (Insufficient Input/Output Validation)

Ocurre cuando la aplicación no valida o sanea adecuadamente los datos que recibe del usuario, de sensores, o de otras fuentes externas (como códigos QR o NFC).

#### Riesgos
* Sufrir **inyecciones de código local** (como inyección SQL en bases de datos SQLite locales).
* Ataques de **Cross-Site Scripting (XSS)** si la app renderiza datos en pantallas web integradas (*WebViews*).
* **Corrupción de datos** o bloqueos por entradas inesperadas.

#### Mitigaciones
* Validar fuertemente todas las entradas utilizando **listas blancas** de caracteres permitidos.
* Utilizar **consultas parametrizadas** en el acceso a las bases de datos locales (SQLite).
* **Desinfectar cualquier salida de datos** antes de renderizarla en componentes WebView.

### M5: Comunicación insegura (Insecure Communication)

Involucra la transmisión de datos confidenciales sin el nivel de protección adecuado a través de la red celular o WiFi.

#### Riesgos
* Usar tráfico en claro (**HTTP en lugar de HTTPS**).
* **No validar correctamente el certificado** del servidor al que se conecta la app.
* Sufrir ataques de intercepción o de **"Man in the Middle" (MitM)**.

#### Mitigaciones
* Forzar siempre **conexiones seguras** con protocolos TLS/SSL actualizados.
* Implementar **"Certificate Pinning" (Anclaje de certificados)** para aplicaciones altamente sensibles (banca, salud, AAPP).
* Evitar el envío de información crítica por **canales no seguros** (como mensajes SMS o notificaciones Push sin cifrar).

### M6: Controles de privacidad inadecuados (Inadequate Privacy Controls)

Trata sobre la fuga o exposición accidental de información confidencial del usuario derivada del propio funcionamiento del sistema operativo móvil.

#### Riesgos
* Exposición de **Información de Identificación Personal (PII)** de manera no intencionada.
* Fuga de datos a través de **logs de la aplicación** o volcados de memoria (crash dumps).
* Exposición visual por la **captura de pantalla de fondo** que hace el SO al minimizar la app, o al guardar datos en el **portapapeles**.

#### Mitigaciones
* **Ocultar o enmascarar datos sensibles** (poner pantalla en negro/borrosa) cuando la aplicación pasa a segundo plano.
* **Deshabilitar la copia al portapapeles** para campos de información crítica (ej. contraseñas, números de cuenta).
* Asegurarse de **no registrar en los logs** de depuración ningún dato personal o sensible.

### M7: Protección insuficiente de binarios (Insufficient Binary Protection)

Es la falta de medidas para evitar que el instalador de la aplicación (`.apk` o `.ipa`) sea analizado, destripado o modificado maliciosamente.

#### Riesgos
* Que la aplicación sea sometida a **ingeniería inversa (decompilada)** fácilmente.
* Que se modifique la app para **insertar código malicioso** (repackaging) creando clones falsos.
* Facilitar la piratería o el bypass de licencias y comprobaciones de seguridad locales.

#### Mitigaciones
* Aplicar técnicas de **ofuscación de código** para dificultar su lectura.
* Utilizar detección de manipulación (**tamper detection**).
* Detectar si el dispositivo tiene **jailbreak (iOS) o root (Android)** y asegurar que la app se cierre o alerte al usuario si el entorno base está comprometido.

### M8: Configuración de seguridad incorrecta (Security Misconfiguration)

Engloba los descuidos en la parametrización de la infraestructura de la aplicación móvil o la falta de ajuste en los manifiestos del proyecto.

#### Riesgos
* Solicitar **permisos excesivos** o innecesarios al sistema operativo.
* Dejar habilitadas **funcionalidades de depuración (debug mode)** en la versión final de producción.
* Exportar componentes o *Intents* (en Android) de forma insegura, permitiendo que otras apps interactúen con ellos.

#### Mitigaciones
* Implementar procesos de **endurecimiento (*hardening*) automatizados**.
* Solicitar **únicamente los permisos estrictamente necesarios** (principio de mínimo privilegio).
* Verificar rigurosamente que todas las **banderas de depuración estén apagadas** antes del lanzamiento a las tiendas (*App Store / Google Play*).

### M9: Almacenamiento de datos inseguro (Insecure Data Storage)

Implica guardar información sensible del usuario en áreas del sistema de archivos local sin la protección criptográfica adecuada.

#### Riesgos
* Guardar credenciales, PII, correos o fotos en **texto plano**.
* Uso de áreas no protegidas como **tarjetas SD o almacenamiento público**, accesibles por cualquier otra app.
* Exposición de datos en caso de pérdida, robo o incautación del dispositivo físico.

#### Mitigaciones
* **Cifrar todos los datos locales en reposo**.
* **Minimizar la cantidad de datos sensibles** que realmente se necesitan guardar en el almacenamiento físico del teléfono.
* Utilizar las librerías y **contenedores de almacenamiento seguro** proporcionados por Android (EncryptedSharedPreferences) e iOS.

### M10: Criptografía insuficiente (Insufficient Cryptography)

Deriva del uso de procesos de cifrado defectuosos o algoritmos débiles para intentar proteger los activos dentro de la app móvil.

#### Riesgos
* Uso de **algoritmos criptográficos débiles u obsoletos** (como MD5, SHA1 o DES).
* Implementar algoritmos fuertes de forma incorrecta (como usar **claves hardcodeadas** o estáticas).
* Generar **semillas de entropía predecibles** (usar `Math.random()` en lugar de `SecureRandom()`).

#### Mitigaciones
* Utilizar **estándares criptográficos modernos** y robustos (como AES de 256 bits y RSA de 2048+ bits).
* Confiar en las **bibliotecas criptográficas nativas** del sistema operativo en lugar de "inventar" algoritmos propios (No "roll your own crypto").
* Gestionar la generación y uso de claves mediante el **hardware de seguridad** (Secure Enclave / Trusted Execution Environment) del dispositivo.



## Tabla Resumen

| ID | Riesgo (Categoría) | Palabra Clave / Concepto | Defensa / Mitigación Principal |
|:---|:---|:---|:---|
| **M1** | Uso Inadecuado de Credenciales | Claves hardcodeadas, tokens en texto plano. | Usar Keystore (Android) / Keychain (iOS). |
| **M2** | Seguridad Cadena de Suministro | SDKs y librerías vulnerables. | SBOM, escanear dependencias (CVEs). |
| **M3** | Autenticación Insegura | Controles de sesión en el cliente, bypass de login. | Delegar autorización al servidor (Backend). |
| **M4** | Validación Insuficiente | SQLi en SQLite, XSS en WebViews. | Listas blancas, parametrizar consultas locales. |
| **M5** | Comunicación Insegura | Falta de HTTPS, ataques MitM, Wi-Fi abierta. | TLS/SSL, Certificate Pinning. |
| **M6** | Controles de Privacidad Inadecuados | PII en logs, capturas de pantalla de fondo, portapapeles. | Ocultar vista en 2º plano, no loguear datos sensibles. |
| **M7** | Protección de Binarios Insuficiente | Ingeniería inversa, decompilación, repackaging. | Ofuscación, detección de Tampering / Root / Jailbreak. |
| **M8** | Configuración de Seguridad Incorrecta | Modo Debug activado, permisos excesivos (Intents). | Apagar flags de depuración, principio de mínimo privilegio. |
| **M9** | Almacenamiento Inseguro | Guardar PII en SD o almacenamiento público. | Cifrar en reposo, usar contenedores seguros nativos. |
| **M10** | Criptografía Insuficiente | MD5/SHA1, random() predecible, claves estáticas. | Usar AES-256, bibliotecas nativas del SO, SecureRandom. |


## Bibliografía
[OWASP Mobile TOP 10 - 2024](https://owasp.org/www-project-mobile-top-10/)