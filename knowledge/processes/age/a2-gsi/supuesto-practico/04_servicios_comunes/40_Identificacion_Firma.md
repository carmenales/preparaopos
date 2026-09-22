# SERVICIOS DE IDENTIFICACIÓN Y FIRMA

Este documento detalla las soluciones horizontales de la AGE para identificar usuarios y firmar documentos, cumpliendo con la **Ley 39/2015** (Art. 9 y 10) y el Reglamento **eIDAS**.

---

## 1. DIFERENCIA LEGAL: IDENTIFICACIÓN VS FIRMA

Es crucial distinguir estos dos conceptos en el examen:

| Concepto | Definición | Herramienta AGE |
| :--- | :--- | :--- |
| **Identificación** | Demostrar **quién eres**. Se exige para acceder a la Sede o consultar datos. | **Cl@ve** / **AutenticA** |
| **Firma Electrónica** | Demostrar la **voluntad** (consentimiento). Se exige para: Solicitudes, Recursos, Desistimientos y Renuncias. | **@firma** / **FIRe** |

---

## 2. CL@VE (IDENTIDAD DEL CIUDADANO)

**Definición:** Plataforma común de identificación, autenticación y firma electrónica para los ciudadanos. Actúa como un **Identity Provider (IdP)** centralizado.

### 2.1. Métodos de Identificación
El sistema que diseñes debe permitir los 4 métodos de Cl@ve:

1.  **Cl@ve PIN:** Código temporal (validez 24h). Orientado a uso esporádico.
2.  **Cl@ve Permanente:** Usuario y contraseña + OTP (SMS). Orientado a uso habitual. Nivel de seguridad avanzado.
3.  **Certificado Electrónico / DNIe:** Nivel de seguridad alto.
4.  **Cl@ve Móvil:** Autenticación mediante App.

### 2.2. Protocolo Técnico (Dato de Examen)
* **SAML 2.0:** Cl@ve utiliza el estándar **SAML 2.0** (Security Assertion Markup Language) para el intercambio de credenciales.
* **Nodo eIDAS:** Cl@ve actúa como pasarela para permitir la identificación de ciudadanos europeos (Reglamento eIDAS).

---

## 3. AUTENTICA (IDENTIDAD DEL EMPLEADO PÚBLICO)

**Definición:** Repositorio horizontal de usuarios y atributos para el personal de la AGE. Funciona como un **Single Sign-On (SSO)**.

### 3.1. Funcionalidad Clave: Gestión de Roles
A diferencia de Cl@ve, AutenticA no solo dice "quién eres", sino **"qué eres"**:

* Provee atributos: Cargo, Unidad de destino, Nivel.
* Permite la **Autorización**: Tu aplicación puede preguntar a AutenticA si el usuario "Javier" tiene permiso para acceder al "Backoffice de Becas".

---

## 4. PLATAFORMA @FIRMA Y SUITE FIRe

Aquí suele haber confusión. Vamos a separarlos:

### 4.1. @firma (El Motor / Backend)
Es la Plataforma de validación y firma multi-PKI del Ministerio.

* **Función:** Valida certificados, verifica firmas y realiza firmas de servidor (Sellos).
* **Servicios:** No interactúa directamente con el usuario final, sino con las aplicaciones.

### 4.2. FIRe (El Integrador / Frontend)
**Firma en la Nube y Componente Integrable.** Es la evolución del "MiniApplet".

* **Función:** Es el componente que **integras en tu aplicación web** para que el usuario pueda firmar.
* **Ventaja:** Permite firmar en escritorio (usando **AutoFirma**) o en la nube (Certificados centralizados), haciendo la firma compatible con dispositivos móviles.

### 4.3. AutoFirma (Cliente de Escritorio)
Aplicación que el ciudadano instala en su PC. Es invocada por el navegador (por FIRe) para realizar la firma localmente cuando el certificado está en el ordenador o tarjeta criptográfica.

---

## 5. OTROS SERVICIOS RELACIONADOS

### 5.1. VALIDe (Validación)
Servicio web para:

* Validar si un certificado está revocado (consulta listas CRL/OCSP).
* Validar si un archivo firmado (XML, PDF) es correcto y no ha sido manipulado.

### 5.2. REPRESENTA (Apoderamientos)
Registro Electrónico de Apoderamientos (REA).

* **Uso:** Permite que un "Representante" (Gestor) actúe en nombre de un "Poderdante" (Ciudadano/Empresa).
* **Integración:** Tu sistema debe consultar a Representa antes de dejar entrar a alguien que dice actuar en nombre de otro.

---

## 6. RESUMEN TÉCNICO PARA DIAGRAMAS

Si tienes que dibujar un diagrama de componentes o despliegue:

1.  **Tu Aplicación Web** habla con **FIRe** (Front) para pedir la firma.
2.  **FIRe** habla con **AutoFirma** (PC Usuario) o con la Nube.
3.  **Tu Servidor** habla con **@firma** (Back) para validar esa firma.
4.  **Tu Servidor** habla con **Cl@ve** (vía SAML) para dejar entrar al usuario.



---