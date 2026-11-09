# Servicios comunes AGE

Los servicios comunes permiten que las aplicaciones de las Administraciones:

* No reinventen la rueda.
* Sean interoperables.
* Reduzcan costes.
* Cumplan con ENI, ENS y normativa europea.

En un examen suma puntos leer el supuesto y citar:

1. El servicio adecuado.
2. Por qué se usa.
3. Cómo mejora la seguridad o la interoperabilidad.

## 2.1 Cl@ve – Identidad del ciudadano

### Qué es
Plataforma estatal de autenticación e identificación electrónica para acceso a servicios públicos.

### Modalidades

* **DNIe/Certificado digital**
* **Cl@ve PIN** (ocasional)
* **Cl@ve Permanente** (contraseña reforzada)
* **Cl@ve Firma** (firma en la nube)

### Cuándo citarlo
Siempre que haya acceso de ciudadanos a una sede electrónica, APP, portal o trámite.

### Frase tipo para supuesto
> “La autenticación de los ciudadanos se realizará mediante Cl@ve, garantizando identidad electrónica conforme a eIDAS y aprovechando servicios comunes interoperables de la AGE.”

---

## 2.2 @firma / FIRe – Plataforma de firma electrónica

### Qué es

* **@firma:** valida y genera firmas electrónicas.
* **FIRe:** permite firmar en servidor, incluso desde móvil.

### Qué aporta

* Ahorra tener que programar firma y validación.
* Asegura cumplimiento de:
    * NTI de Política de Firma.
    * ENS en seguridad.
    * eIDAS en Europa.

### Cuándo citarlo
Cuando documentos deban firmarse: solicitudes, resoluciones, notificaciones, informes.

### Frase tipo
> “El sistema delegará la firma electrónica en la plataforma @firma/FIRe, cumpliendo la NTI de Política de Firma y permitiendo validación y sello electrónico sin desarrollo propio.”

---

## 2.3 SIR – Sistema de Interconexión de Registros

### Qué es
La red que permite que los registros de las AAPP intercambien asientos electrónicamente.

### Objetivo
Que un documento registrado en un organismo llegue automáticamente al otro destino.

### Cuándo citarlo
Cuando el sistema tenga que enviar o recibir documentos desde otras administraciones.

### Frase tipo
> “El intercambio de asientos registrales se realizará mediante el Sistema de Interconexión de Registros (SIR), garantizando interoperabilidad técnica y organizativa conforme al ENI.”

---

## 2.4 GEISER – Cliente de Registro

### Qué es
Aplicación que utiliza SIR y permite:

* Registro de entrada/salida.
* Envío de asientos.
* Consulta de trámites enlazados.

### Uso típico en un examen
* Si el organismo no tiene registro propio.
* Si el sistema debe registrar documentación.

### Frase tipo
> “Para la gestión y remisión de asientos registrales se empleará GEISER, integrándose con SIR y evitando el desarrollo de clientes de registro propios.”

---

## 2.5 INSIDE – Gestión de Expediente Electrónico

### Qué es
Plataforma oficial para:

* Crear y custodiar expedientes electrónicos.
* Aplicar índice electrónico firmado.
* Mantener cumplimiento de NTIs.

### Cuándo citarlo
Si en el supuesto hay expedientes administrativos.

### Frase tipo
> “La gestión del expediente electrónico se realizará mediante INSIDE, asegurando índice electrónico firmado, metadatos normalizados y cumplimiento de las NTI de Documento y Expediente.”

---

## 2.6 Plataforma de Intermediación de Datos (PID)

### Qué es
Servicio para consultar datos de otras AAPP sin pedirlos al ciudadano.
Ejemplos: certificado de empadronamiento, datos de identidad, título de familia numerosa, situación laboral.

### Cuándo citarlo
Cuando el sistema requiera información que el ciudadano no debería aportar.

### Frase tipo
> “Los datos necesarios se consultarán a través de la Plataforma de Intermediación, evitando solicitar documentación redundante al ciudadano y cumpliendo el principio de simplificación de la Ley 39/2015.”

---

## 2.7 DIR3 – Directorio Común

### Qué es
Catálogo único con códigos de:

* Unidades organizativas.
* Oficinas.
* Organismos públicos.

### Cuándo citarlo
* Cuando necesites identificar qué organismo tramita expedientes o documentos.
* Cuando haya intercambio entre administraciones.

### Frase tipo
> “La identificación de organismos emisores y receptores seguirá el catálogo DIR3, conforme a la NTI de Directorios, garantizando interoperabilidad semántica.”

---

## 2.8 Notific@ / DEHú – Notificaciones electrónicas

### Qué es
Servicios para notificar electrónicamente resoluciones y comunicaciones.

* **Notific@:** Automatiza envío y gestión.
* **DEHú (Dirección Electrónica Habilitada Única):** Buzón único ciudadano.

### Cuándo citarlo
Si el trámite necesita notificaciones con validez legal.

### Frase tipo
> “Las notificaciones al interesado se canalizarán mediante Notific@/DEHú, asegurando trazabilidad, acceso seguro y validez jurídica conforme a Ley 39/2015.”

---

## 2.9 Portafirmas – Firma interna para empleados públicos

### Qué es
Solución para que empleados firmen internamente documentos administrativos sin desarrollo adicional.

### Frase tipo
> “Los documentos generados internamente se firmarán mediante Portafirmas, garantizando trazabilidad, sellado de tiempo y cumplimiento de ENS y NTI de Política de Firma.”

---

## 2.10 AutoFirma – Cliente de firma local

### Qué es
Aplicación para firmar documentos en el equipo del usuario.

### Cuándo citarlo
Si el canal requiere firma desde ordenador sin FIRe.

### Frase tipo
> “Se ofrecerá AutoFirma como cliente de firma local para quienes utilicen certificados en el equipo, manteniendo compatibilidad con @firma.”

---

## 2.11 Otros reutilizables útiles

* **Carpeta Ciudadana:** Permite recoger de forma agregada las actuaciones del ciudadano con la AGE.
* **ARCO / derechos RGPD:** Integra servicios para gestionar accesos, rectificación, supresión, oposición, etc.
* **ORVE (Registro Virtual):** Digitalización de documentación en ventanilla.

---

# Cómo integrar estos servicios en una respuesta del supuesto

Si el caso es: **“Aplicación para tramitar solicitudes electrónicas de becas”.**

**Respuesta modelo:**
> “La autenticación del ciudadano se realizará mediante **Cl@ve**, y la firma de documentos con **@firma/FIRe**.
>
> La documentación se registrará mediante **GEISER**, intercambiando asientos a través de **SIR**, y los expedientes se custodiarán en **INSIDE** con índice electrónico firmado cumpliendo las NTI aplicables.
>
> Cuando se requiera información adicional del interesado, los datos se consultarán mediante la **Plataforma de Intermediación**, evitando solicitar documentación innecesaria al ciudadano, en línea con la Ley 39/2015.”

---

# Tabla-resumen rápida

| Servicio | Para qué sirve | En qué caso citarlo |
| :--- | :--- | :--- |
| **Cl@ve** | Identificación/autenticación | Acceso ciudadano |
| **@firma / FIRe** | Firma electrónica | Firma de documentos |
| **GEISER / SIR** | Registro e intercambio | Entrada/salida de documentos |
| **INSIDE** | Gestión de expedientes | Tramitación administrativa |
| **PID** | Consulta de datos | No pedir papeles al ciudadano |
| **DIR3** | Identificación de unidades | Trámites con otros organismos |
| **Notific@ / DEHú** | Notificaciones electrónicas | Comunicación con validez legal |
| **Portafirmas** | Firma interna | Documentos de funcionarios |
| **AutoFirma** | Cliente local | Firmas con certificado en PC |