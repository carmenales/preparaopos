# JUSTIFICACIÓN NORMATIVA DEL DISEÑO

El diseño de cualquier Sistema de Información en la Administración General del Estado (AGE) debe regirse por el principio de **legalidad y eficiencia** (Ley 40/2015), asegurando la **interoperabilidad** (ENI) y la **seguridad** (ENS).

---

## 1. LEYES FUNDAMENTALES (Leyes 39 y 40/2015)

Son el marco jurídico troncal que justifica la **obligación de tramitar electrónicamente**.

### 1.1. Ley 39/2015 (LPAC - Procedimiento hacia el Ciudadano)

**Cuándo citarla:** Siempre que intervenga un **ciudadano** o persona jurídica como interesado.

| Concepto | Justificación y Aplicación en el Sistema |
| :--- | :--- |
| **Relación Electrónica** | Justifica la necesidad de la **Sede Electrónica** como canal de acceso, garantizando el derecho a la asistencia y la **validez del documento electrónico**. |
| **Identificación (Art. 9)** | Obliga al uso de sistemas como **Cl@ve** o certificados electrónicos. |
| **Firma (Art. 10)** | Define los actos que requieren firma (**Formular solicitudes, interponer recursos**) y justifica el uso de **@firma/FIRe**. |
| **Registro Electrónico** | Toda presentación de documentos debe generar un asiento registral. Justifica el uso de **GEISER/REGECO**. |
| **Derecho a No Aportar** | El ciudadano no debe aportar documentos que ya obren en poder de la AAPP. Justifica la integración con la **PID/SCSP** (Plataforma de Intermediación de Datos). |
| **Notificación (Art. 41)** | Las notificaciones deben ser electrónicas. Justifica la integración con **Notifica**. |

### 1.2. Ley 40/2015 (LRJSP - Régimen Jurídico Interno)

**Cuándo citarla:** Siempre. Regula cómo se organiza la administración "por dentro" y establece los principios de actuación.

| Concepto | Justificación y Aplicación en el Sistema |
| :--- | :--- |
| **Reutilización (Art. 157)** | Obliga a las AAPP a reutilizar sistemas y aplicaciones existentes. Justifica el uso de **Servicios Comunes (INSIDE, Cl@ve)** antes que desarrollar algo nuevo. |
| **Interoperabilidad y Seguridad (Art. 156)** | Establece el cumplimiento obligatorio del **ENI** (para la NTI de Expediente) y el **ENS** (para la seguridad). |
| **Actuación Administrativa Automatizada (AAA)** | Permite que el sistema tome decisiones o emita actos sin intervención humana directa. Justifica el uso del **Sello Electrónico de Órgano** (Art. 42). |

---

## 2. REGLAMENTOS CLAVE DE GOBIERNO TIC

### 2.1. ENS (Esquema Nacional de Seguridad - RD 311/2022)

**Lógica Clave:** Todo sistema AGE debe **categorizarse** (Básico, Medio o Alto) y aplicar las medidas de seguridad del **Anexo II**.

* **Objetivo:** Establecer la política de seguridad y los requisitos mínimos para proteger la información (dimensiones de Confidencialidad, Integridad y Disponibilidad).
* **Aplicación:** Se citará en el Diagrama de Despliegue (seguridad física y lógica) y en la fase de Análisis de Riesgos.

### 2.2. ENI (Esquema Nacional de Interoperabilidad - RD 4/2010)

**Lógica Clave:** Garantizar que el sistema se comunica correctamente con otros y gestiona bien los documentos.

* **Objetivo:** Garantizar la interoperabilidad técnica y semántica entre AAPP.
* **Aplicación:**
    * Uso de **Estándares Abiertos** (Ej. XML, JSON) para el intercambio de datos.
    * Obligación de usar las **NTI de Documento y Expediente Electrónico** (Justifica el uso de INSIDE y la firma del Índice del Expediente).

### 2.3. RGPD y LOPDGDD (Protección de Datos)

**Cuándo citarlo:** Cuando definas los datos (Diagrama de Clases/E-R) o la seguridad.

* **Concepto Clave:** **"Privacidad desde el Diseño"** (*Privacy by Design*). El diseño (Diagrama de Clases) debe minimizar el tratamiento de datos y aplicar las medidas de seguridad del nivel correspondiente.
* **Aplicación:** Se requiere la **Evaluación de Impacto (EIPD)** si hay tratamiento de alto riesgo.


---

# ESQUEMA NACIONAL DE INTEROPERABILIDAD (ENI)

## Qué es
El ENI (RD 4/2010) establece los criterios y requisitos de interoperabilidad que deben cumplir las AAPP para:

* Intercambiar información,
* Garantizar formatos y procedimientos comunes,
* Asegurar que los sistemas se entienden entre sí,
* Facilitar que el ciudadano no tenga que aportar documentación varias veces.

Es obligatorio para todos los sistemas y servicios públicos.

## Principios del ENI (muy preguntables)

* **Interoperabilidad organizativa:** Las administraciones deben cooperar y adoptar procedimientos que permitan el intercambio de información.
* **Interoperabilidad semántica:** Asegura que los datos enviados y recibidos tengan el mismo significado, usando metadatos y modelos comunes.
* **Interoperabilidad técnica:** Se definen estándares, formatos y protocolos comunes para garantizar que los sistemas se entienden.
* **Reutilización:** Aprovechar soluciones existentes → el Portal de Administración Electrónica (PAe) y el CCSAE promueven su reutilización.
* **Seguridad y protección de datos:** Coordinado con el ENS, RGPD y LOPDGDD.
* **Accesibilidad y multicanalidad**
* **Neutralidad tecnológica**

## Qué exige el ENI en la práctica

### 1. Uso de formatos válidos y abiertos
Ejemplo:

* PDF/A
* ODT
* XML
* HTML
* JPG, PNG
* Firmas XAdES, CAdES y PAdES

En AGE, si puedes decir en el examen:
> “La documentación electrónica generada seguirá formatos válidos y estándares aprobados en el ENI para garantizar su interoperabilidad a largo plazo.”

Queda perfecto.

### 2. Uso de metadatos obligatorios
Todo documento administrativo debe incluir:

* Identificador,
* Fecha,
* Emisor,
* Tipo,
* Carácter original/copia,
* Huella digital si aplica.

Los NTI de Documento Electrónico y de Expediente Electrónico detallan esto.

### 3. Expediente electrónico
El expediente electrónico debe:

* Tener índice electrónico firmado,
* Ser transferible entero a otro organismo,
* Cumplir NTI de Expediente Electrónico.

**Servicio asociado típico:** Inside → creación y gestión de expedientes electrónicos.

### 4. Intercambio entre administraciones
El ENI habilita el intercambio mediante:

* **SIR** – Sistema de Interconexión de Registros, usando:

    * **Geiser** como plataforma de registro,
    * Protocolos comunes y seguros.

### 5. Reutilización de servicios comunes
Normalmente el exam corrector espera que cites:

* **Cl@ve** → autenticación.
* **@firma / FIRe** → firma.
* **Inside** → expedientes electrónicos.
* **Geiser** → registro.
* **SIR** → intercambio de asientos.
* **PSIS / Intermediación** → consulta de datos de otras administraciones (certificados, empadronamientos, etc.).

## Listado rápido de NTI que salen en examen
(Nunca vienen mal citarlos como autoridad)

* NTI de Documento Electrónico
* NTI de Expediente Electrónico
* NTI de Política de Firma
* NTI de Digitalización
* NTI de Procedimientos
* NTI de Requisitos de conexión a red
* NTI de Relación de modelos de datos

Si nombras 1–2 ya sumas puntos.

---

# Cómo meter ENI en una respuesta real

## Ejemplo general para casi cualquier supuesto
> El desarrollo y funcionamiento del sistema cumplirá el Esquema Nacional de Interoperabilidad (ENI) garantizando que el intercambio de información con otras Administraciones se realice con formatos abiertos y estándar y con metadatos definidos según los NTI aplicables.

## 1. Si te preguntan por documentación o expedientes
> Los documentos electrónicos incluirán los metadatos obligatorios establecidos en el ENI, siguiendo los NTI de Documento y Expediente Electrónico, y se estructurarán de forma que puedan ser transferidos a otros organismos manteniendo la integridad, la firma y el índice electrónico.

## 2. Si describen una aplicación que debe conectarse con otros sistemas
> El sistema se integrará con la red de intercambio SIR, gestionada mediante Geiser, garantizando la interoperabilidad organizativa, semántica y técnica exigida por el ENI.

## 3. Si te piden autenticación o acceso
> La autenticación se realizará mediante los servicios comunes de la AGE, como Cl@ve, cumpliendo las exigencias de interoperabilidad del ENI y aprovechando soluciones reutilizables promovidas por el PAe.

## 4. Si hay generación de documentos administrativos
> Toda la documentación archivada en el sistema se almacenará en formatos válidos (PDF/A, XML, etc.) definidos por el ENI, asegurando su conservación y accesibilidad a largo plazo.

## 5. Si piden que asegures coordinación entre organismos
> Se aplicarán los principios de interoperabilidad organizativa, semántica y técnica definidos en el ENI, permitiendo que los sistemas de distintas AAPP puedan intercambiar información de forma segura y transparente para el ciudadano.

## Frase “comodín” para usar sin pensar
> La solución se ajustará al Esquema Nacional de Interoperabilidad (RD 4/2010), aplicando los NTI correspondientes, garantizando el uso de formatos abiertos, metadatos normalizados y la interoperabilidad con otras AAPP a lo largo de todo el ciclo de vida del expediente electrónico.

---

# NTIs (Normas Técnicas de Interoperabilidad)

## ¿Qué son las NTIs y por qué importan en el examen?
Las NTIs son documentos técnicos que desarrollan y concretan los requisitos del ENI. Definen formatos, metadatos, políticas de firma, requisitos de conservación, intercambio de expedientes, etc.

En los supuestos del Bloque III suelen pedirte que justifiques formatos, metadatos, procedimientos de archivo o intercambio: citar la NTI correcta y aplicar su concepto suma muchos puntos.

## Lista prioritaria de NTIs (las que más suelen salir)

### NTI de Documento Electrónico

* **Qué hace:** Define qué es un documento electrónico, metadatos mínimos y formato.
* **Cuándo citarla:** Si el supuesto genera o almacena documentos administrativos (informes, resoluciones, certificados).
* **Frase tipo:**

> “Los documentos se generarán y custodiarán según la NTI de Documento Electrónico, incluyendo metadatos mínimos (identificador, emisor, fecha, tipo) y utilizando formatos normalizados (PDF/A, XML).”

### NTI de Expediente Electrónico

* **Qué hace:** Define estructura del expediente, índice electrónico, integridad y migración.
* **Cuándo citarla:** Si el sistema gestiona trámites/expedientes (subvenciones, recursos, solicitudes).
* **Frase tipo:**

> “El expediente electrónico se construirá conforme a la NTI de Expediente Electrónico, con índice firmado y estructura que permita la transferencia completa entre organismos.”

### NTI de Política de Firma

* **Qué hace:** Establece requisitos sobre firmas electrónicas, sellos, formatos (XAdES, PAdES, CAdES).
* **Cuándo citarla:** Si el supuesto requiere firma electrónica de documentos o transacciones.
* **Frase tipo:**

> “Las firmas digitales seguirán la NTI de Política de Firma, empleando formatos y niveles de firma compatibles con @firma/FIRe y eIDAS.”

### NTI de Digitalización

* **Qué hace:** Requisitos para digitalizar documentos papel con validez jurídica.
* **Cuándo citarla:** Si el flujo incluye incorporación de documentos en papel al sistema.
* **Frase tipo:**

> “La incorporación de documentos papel seguirá la NTI de Digitalización, garantizando cadena de custodia y metadatos de digitalización.”

### NTI de Conservación y Archivo

* **Qué hace:** Establece políticas de conservación, formatos preservables, y requisitos de migración.
* **Cuándo citarla:** Si se pide política de retención o almacenamiento a largo plazo.
* **Frase tipo:**

> “La custodia y preservación de los documentos se realizará según la NTI de Conservación, garantizando formatos preservables (p.ej. PDF/A) y procedimientos de migración periódica.”

### NTI de Requisitos de Conexión y Seguridad

* **Qué hace:** Requisitos técnicos para conexiones seguras entre sistemas, puntos de intercambio y redes.
* **Cuándo citarla:** Si el supuesto describe integración con otras AAPP o uso del SIR/Geiser.
* **Frase tipo:**

> “Las comunicaciones entre organismos se ajustarán a la NTI de Requisitos de Conexión, usando canales cifrados y protocolos interoperables.”

### NTI de Metadatos y Catálogo de Datos

* **Qué hace:** Define esquemas de metadatos y modelos de datos para interoperabilidad semántica.
* **Cuándo citarla:** Si hay intercambio de datos entre sistemas y necesitas justificar semántica uniformizada.
* **Frase tipo:**

> “Los datos intercambiados cumplirán el catálogo/NTI de Metadatos, garantizando semántica compartida entre los servicios interconectados.”

### NTI de Procedimientos y Tramitación

* **Qué hace:** Reglas para modelar procedimientos administrativos y sus fases.
* **Cuándo citarla:** Si el supuesto describe flujos de tramitación (estados, plazos, notificaciones).
* **Frase tipo:**

> “La lógica de negocio y estados de tramitación se modelarán conforme a la NTI de Procedimientos, permitiendo interoperabilidad de procesos.”

### NTI de Servicios Web e Interconexión

* **Qué hace:** Estándares para servicios (SOAP/REST), políticas de seguridad, headers, errores.
* **Cuándo citarla:** Si el sistema expone o consume APIs con otras AAPP.
* **Frase tipo:**

> “Las APIs se diseñarán según la NTI de Servicios Web, definiendo contratos, modelos de error y seguridad a nivel de API.”

### NTI de Identificadores y Directorios (DIR3)

* **Qué hace:** Modelos de codificación de unidades orgánicas y directorios.
* **Cuándo citarla:** Si integras con DIR3 o necesitas referenciar unidades administrativas.
* **Frase tipo:**

> “Las referencias a unidades organizativas utilizarán los códigos y modelos establecidos en la NTI de Directorios (DIR3) para asegurar interoperabilidad.”

## Cómo usar la lista de NTIs en un supuesto (guía práctica rápida)

1.  Lee el enunciado y detecta si aparece: expediente, documento, firma, intercambio, directorios, metadatos, digitalización.
2.  Relaciona cada mención con la NTI correspondiente (ej.: “expediente” → NTI Expediente Electrónico).
3.  Inserta una frase concreta citando la NTI y la medida práctica (formato, índice, firma, metadatos).
4.  Si toca justificar técnica, añade cómo lo implementarías (p. ej., “índice electrónico firmado + almacén en formato PDF/A + metadatos X,Y,Z”).

## Ejemplos concretos (frases completas reutilizables)

**Ejemplo A — sistema que genera resoluciones:**

> “Las resoluciones emitidas por el sistema se firmarán electrónicamente conforme a la NTI de Política de Firma, empleando PAdES/XAdES y garantizando su validez jurídica y su integridad en el expediente electrónico.”

**Ejemplo B — intercambio con otra administración:**

> “El intercambio de información con otras AAPP se realizará mediante servicios definidos en la NTI de Servicios Web e Interconexión, aplicando contratos WSDL/OpenAPI y transportes seguros conforme a la NTI de Requisitos de Conexión.”

**Ejemplo C — digitalización de documentos:**

> “La recepción de documentación en papel y su incorporación al expediente se hará según la NTI de Digitalización, garantizando la huella, metadatos y cadena de custodia exigidos para su validez administrativa.”

**Ejemplo D — preservación a largo plazo:**

> “La preservación de documentos se ejecutará conforme a la NTI de Conservación, almacenando preferentemente en PDF/A y aplicando procesos de migración y verificación periódica.”

## NTIs + ENS + RGPD: combinación práctica (frase tipo)

> “El diseño se ajustará a la vez al ENI (NTIs aplicables para formatos, metadatos y expediente electrónico), al ENS (medidas de seguridad: cifrado, trazabilidad, control de acceso) y al RGPD (minimización, derechos de los interesados y medidas organizativas), garantizando interoperabilidad, protección y cumplimiento normativo.”

Esa frase es muy potente si la pones en la introducción o en la sección de normativa de tu respuesta.

## Nota práctica sobre referencias en el examen

* No escribas URLs en la hoja de examen (no las piden). Citar "NTI de Documento Electrónico" o "NTI de Expediente Electrónico" es suficiente.
* Si te piden concreción, nombra un metadato obligatorio (identificador, fecha, emisor) o un formato (PDF/A).
* Si dudas entre NTIs, prioriza Documento, Expediente, Política de Firma, Digitalización y Servicios Web.

## Tabla-resumen (para memorizar rápido)

| Tema | NTI más relevante | Qué pide / formato típico |
| :--- | :--- | :--- |
| **Documentos administrativos** | Documento Electrónico | Metadatos mínimos, PDF/A, huella digital |
| **Expedientes** | Expediente Electrónico | Índice electrónico, transferencia, firma |
| **Firma** | Política de Firma | PAdES/XAdES/CAdES, políticas de firma |
| **Digitalización** | Digitalización | Cadena de custodia, metadatos de escaneo |
| **Conservación** | Conservación/Archivo | Formatos preservables, migración |
| **APIs / Intercambio** | Servicios Web e Interconexión | Contratos API, errores, seguridad |
| **Conexión** | Requisitos de Conexión | Canales cifrados, VPN, certificados |
| **Metadatos** | Metadatos y Catálogo de Datos | Esquemas, vocabularios controlados |
| **Directorios** | Identificadores / DIR3 | Códigos de unidades, interoperabilidad |

---

# RGPD + LOPDGDD: Apuntes y Guía de Redacción para Supuestos Prácticos

---

# PARTE I: Conceptos Clave y Aplicación (Bloque III)

## 1. Qué espera el tribunal
En un examen del segundo ejercicio, no basta con decir “cumpliremos RGPD”.

El corrector espera que:
* Identifiques si hay tratamiento de datos personales.
* Demuestres que conoces los principios y obligaciones aplicables.
* Los aterrices al caso real del supuesto.
* Tengas frases claras y correctas para justificar soluciones.

Si haces eso, sumas muchos puntos.

## 2. Cuándo meter RGPD en una pregunta
Inclúyelo siempre que:
* Se manejen datos de personas físicas (empleados, ciudadanos, empresas unipersonales).
* Se realicen cesiones entre organismos.
* Se pidan integraciones con otros sistemas.
* Se produzcan accesos desde terceros.
* Haya almacenamiento en cloud o fuera de España.
* El sistema gestione historiales, expedientes, trámites, registros, notificaciones, usuarios o autenticación.

**En otras palabras:** Si hay personas, hay RGPD.

## 3. Frase rápida para comenzar (comodín)
Puedes iniciar casi cualquier respuesta con:

> "El sistema realizará el tratamiento de datos personales cumpliendo el Reglamento General de Protección de Datos (RGPD) y la Ley Orgánica 3/2018 (LOPDGDD), aplicando las medidas técnicas y organizativas necesarias para garantizar la licitud, integridad, confidencialidad y disponibilidad de la información."

Con esta frase ya entras en el terreno correcto.

## 4. Principios del RGPD que más puntúan si los citamos
Citar dos o tres con sentido aplicado al caso genera buena impresión. Los principales:
* Licitud, lealtad y transparencia.
* Minimización de datos.
* Limitación de la finalidad.
* Exactitud.
* Limitación de conservación.
* Integridad y confidencialidad.
* Responsabilidad proactiva (accountability).

**Ejemplos aplicados:**
> "Se aplicará el principio de minimización, recogiendo únicamente los datos necesarios para la prestación del servicio descrito en el supuesto."

> "El tratamiento tendrá finalidades determinadas, explícitas y legítimas, informadas al ciudadano de forma transparente."

> "Se implantará una política de retención que garantice que los datos no se conservan más tiempo del necesario."

Con frases simples, sumas.

## 5. Obligaciones que sí esperan que cites
Las que más debes usar:

### 5.1 Registro de actividades del tratamiento (RAT)
> "Se documentará el tratamiento en el Registro de Actividades conforme exige el RGPD, describiendo finalidad, bases de legitimación, cesiones y medidas de seguridad aplicadas."

### 5.2 Identificación de roles
En una respuesta se identifican los roles obligatorios:
* **Responsable del tratamiento** (organismo titular del sistema).
* **Encargados del tratamiento** si hay proveedores externos.
* **Delegado de Protección de Datos (DPO).**

### 5.3 Evaluación de Impacto (EIPD – DPIA)
Muy valorado si el supuesto es sensible: Historias clínicas, Datos financieros, Datos especialmente protegidos, Evaluaciones masivas, Perfilado.

**Frase aplicable:**
> "Si el tratamiento presenta alto riesgo para los derechos y libertades de los ciudadanos, se realizará una Evaluación de Impacto en Protección de Datos (EIPD) conforme al RGPD."

### 5.4 Información y derechos del interesado
Siempre queda bien decir:
> "El sistema garantizará el ejercicio de los derechos de acceso, rectificación, supresión, oposición, limitación y portabilidad mediante procedimientos accesibles desde la sede electrónica."

## 6. Bases de legitimación que puedes meter
Las más habituales en AGE:
* **Misión en interés público o ejercicio de poderes públicos** (art. 6.1.e RGPD).
* **Cumplimiento de obligación legal** (6.1.c).
* **Consentimiento** (solo en casos donde no aplique lo anterior).

**Frase simple:**
> "El tratamiento se fundamenta en el artículo 6.1.e del RGPD al ser necesario para el ejercicio de competencias públicas del organismo."

## 7. Cesiones y comunicación entre organismos
Cuando hay integración con otros sistemas:
> "Las comunicaciones entre Administraciones se realizarán conforme a los principios del RGPD, garantizando que cada organismo actúa como Responsable o Encargado del tratamiento según su función en el procedimiento."

Si cedes datos a prestadores cloud:
> "Los proveedores actuarán como Encargados del Tratamiento, formalizando contrato que detalle obligaciones, medidas de seguridad y condiciones de subcontratación."

## 8. Seguridad: RGPD + ENS juntos
La forma correcta de aplicarlo:
> "Las medidas de seguridad se establecerán conforme al Esquema Nacional de Seguridad (RD 311/2022), garantizando integridad, autenticidad, disponibilidad y trazabilidad en cumplimiento del artículo 32 del RGPD."

El tribunal valora mucho esta frase.

## 9. Transferencias internacionales
Si aparece cloud fuera de UE o CDN, menciona:
> "Si existieran transferencias internacionales de datos, se garantizaría un nivel adecuado mediante mecanismos previstos en el RGPD (cláusulas tipo, decisiones de adecuación, etc.)."

Con esto cubres el aspecto legal.

## 10. Cómo meter todo esto en una respuesta real

### Caso típico 1: Aplicación web de la AGE que gestiona expedientes ciudadanos
> "El sistema realizará el tratamiento de datos personales cumpliendo el RGPD y la LOPDGDD. El tratamiento se documentará en el Registro de Actividades, identificando al organismo como Responsable y a los proveedores como Encargados mediante los correspondientes contratos. El tratamiento se fundamenta en el artículo 6.1.e del RGPD por ejercicio de funciones públicas. Se aplicarán los principios de minimización y limitación de conservación, almacenando únicamente los datos necesarios para el trámite y durante el plazo imprescindible. Las medidas de seguridad se implantarán conforme al ENS, garantizando control de acceso, trazabilidad, cifrado y registro de eventos. Se garantizará el ejercicio de los derechos ARSOPL mediante procedimientos habilitados en la sede electrónica del organismo."

### Caso típico 2: Integración con servicios de otra administración
> "Las cesiones de datos a otros organismos se realizarán conforme al RGPD, actuando cada entidad como Responsable o Encargado según su función. El intercambio se documentará en el Registro de Actividades y se implementarán medidas técnicas y organizativas alineadas con el ENS para garantizar confidencialidad, integridad y trazabilidad de la información."

### Caso típico 3: Tratamiento de datos especialmente sensibles
> "Al tratarse de un tratamiento de datos que supone un alto riesgo para los derechos de los interesados, se realizará una Evaluación de Impacto en protección de datos (EIPD) conforme al RGPD, incluyendo análisis de riesgos, medidas compensatorias y verificación por el Delegado de Protección de Datos."

## 11. Frases comodín listas para copiar
* "Se aplicará el RGPD y la LOPDGDD garantizando el tratamiento lícito, leal y transparente de los datos."
* "El tratamiento se fundamenta en el ejercicio de poderes públicos (art. 6.1.e RGPD)."
* "Se documentará el tratamiento en el Registro de Actividades correspondiente."
* "Los proveedores actuarán como Encargados del Tratamiento mediante contrato conforme al art. 28 del RGPD."
* "Si existiesen riesgos elevados, se realizará una Evaluación de Impacto en protección de datos."
* "Las medidas de seguridad se implantarán de acuerdo con el ENS."
* "Se aplicará minimización de datos, conservando únicamente los estrictamente necesarios."
* "Se garantizará el ejercicio de los derechos ARSOPL del interesado a través de la sede electrónica."

---

# PARTE II: Guía de Redacción Avanzada y Casos Específicos

## 1. ¿Cuándo mencionarlo?
En una respuesta de examen suele aparecer cuando:
* El sistema trata datos personales.
* Hay riesgos de privacidad.
* Se diseña o actualiza una aplicación, procedimiento o servicio digital.
* Existe una brecha de seguridad.
* Se evalúan responsabilidades del órgano gestor o del responsable TI.

## 2. Párrafos tipo para usar en el examen

### 2.1. Cumplimiento general RGPD/LOPDGDD
> "El sistema debe garantizar el cumplimiento de lo establecido en el Reglamento (UE) 2016/679 (RGPD) y en la Ley Orgánica 3/2018 (LOPDGDD), aplicando los principios de protección de datos desde el diseño y por defecto, limitación de la finalidad, minimización de datos, exactitud, confidencialidad e integridad."

### 2.2. Base jurídica del tratamiento
> "El tratamiento se fundamenta en el artículo 6 del RGPD, al ser necesario para el cumplimiento de una misión realizada en interés público o en el ejercicio de poderes públicos conferidos a la Administración."

### 2.3. Registro de actividades de tratamiento (obligatorio)
> "El tratamiento debe estar incluido en el Registro de Actividades de Tratamiento exigido por el artículo 30 del RGPD, detallando finalidad, categoría de datos, cesiones, plazos de conservación y medidas de seguridad aplicadas."

### 2.4. Deber de información (art. 13 RGPD – ARSOPLUS)
> "La solución deberá asegurar que se proporciona al ciudadano la información requerida por el artículo 13 del RGPD, incluyendo responsable del tratamiento, finalidad, base jurídica, plazo de conservación y derechos ARSOPLUS (acceso, rectificación, supresión, oposición, portabilidad y limitación)."

### 2.5. Contratos con encargados del tratamiento
> "En caso de intervención de terceros, se formalizará un contrato de encargo de tratamiento conforme al artículo 28 del RGPD, especificando obligaciones de confidencialidad, seguridad, subcontratación y retorno de datos."

### 2.6. Evaluación de Impacto (cuando haya riesgos)
> "Al estar presente un tratamiento susceptible de alto riesgo para los derechos y libertades de las personas, se realizará una Evaluación de Impacto en protección de datos (EIPD), conforme al artículo 35 del RGPD y a las directrices de la AEPD."

### 2.7. Medidas de seguridad
> "Las medidas de seguridad deberán ser adecuadas al riesgo, siguiendo el artículo 32 del RGPD: control de acceso, cifrado, trazabilidad, copias de seguridad, auditorías y pruebas periódicas."

**Frase de cierre rápida:**
> "Estas medidas garantizan la confidencialidad, integridad, disponibilidad y resiliencia del sistema."

### 2.8. Gestión de brechas de seguridad
Si el supuesto plantea fallo, fuga, hackeo, pérdida de USB, etc.:
> "Ante una brecha de seguridad deberá realizarse notificación a la AEPD en un máximo de 72 horas, conforme al artículo 33 del RGPD, incluyendo descripción del incidente, alcance, medidas adoptadas y acciones de mitigación. Si existiera riesgo grave para los afectados, también se les informará (art. 34 RGPD)."

### 2.9. Relación con el ENS
Si quieres unirlo al Esquema Nacional de Seguridad (algo que da muchos puntos):
> "Las medidas de protección de datos se alinearán con las obligaciones del Esquema Nacional de Seguridad, especialmente en lo relativo al control de accesos, análisis de riesgos, registro de actividad y auditoría periódica."

## 3. Un ejemplo real de cómo meterlo en una respuesta

**Caso del examen (ejemplo corto):**
Una aplicación municipal de gestión de multas se va a modernizar y enviará notificaciones electrónicas al ciudadano.

**Cómo meter RGPD + LOPDGDD en un párrafo:**
> "El sistema debe cumplir con el RGPD y la LOPDGDD, aplicando protección de datos desde el diseño y por defecto. El tratamiento se ampara en el artículo 6 del RGPD al ser necesario para el ejercicio de potestades públicas y deberá estar incluido en el Registro de Actividades de Tratamiento. Se garantizará que el ciudadano recibe la información del artículo 13 (responsable, base jurídica, finalidad, conservación y derechos ARSOPLUS). Si participa un proveedor externo, se firmará un contrato de encargo conforme al artículo 28. Las medidas de seguridad deben ser adecuadas al riesgo (art. 32 RGPD) y alineadas con el ENS, incluyendo trazabilidad, control de accesos y auditorías."

Ese párrafo resume prácticamente todos los puntos clave, y da muchísimo nivel en un examen.

**Versión ultra corta (si no hay espacio):**
> "Se garantizará el cumplimiento del RGPD y LOPDGDD, aplicando protección de datos desde el diseño, registro de actividad del tratamiento, deber de información al ciudadano, contratos con encargados, auditoría y medidas de seguridad acordes al riesgo (art. 32), alineadas con el ENS."

## 4. Casos Especiales

### 1) RGPD + LOPDGDD aplicado a un supuesto con brecha de seguridad

**Frases tipo para meter en una respuesta:**

* **Detección y documentación de la brecha:** "La incidencia debe registrarse y documentarse según exige el artículo 33 del RGPD, incluyendo naturaleza de la brecha, sistemas afectados, datos comprometidos, causa raíz y acciones correctoras adoptadas."
* **Notificación a la AEPD (obligatorio):** "La brecha se notificará a la AEPD en un máximo de 72 horas desde su detección, conforme al artículo 33 del RGPD, detallando impacto, alcance y medidas adoptadas para corregir y mitigar el incidente."
* **Notificación a los afectados (si procede):** "Si la brecha entraña un riesgo elevado para los derechos de las personas, se informará también a los afectados sin dilación indebida, aplicando lo establecido en el artículo 34 del RGPD."
* **Intervención del Delegado de Protección de Datos:** "El Delegado de Protección de Datos debe ser informado del incidente y participar en la valoración del impacto, medidas a adoptar, comunicación y seguimiento, de acuerdo con los artículos 37 a 39 del RGPD."
* **Medidas tras la brecha:** "Tras el incidente deben aplicarse medidas correctoras, mejoras de seguridad y, si fuera necesario, actualización de análisis de riesgos, procedimientos internos y Evaluación de Impacto (EIPD)."
* **Enlace directo con el ENS:** "La gestión del incidente debe alinearse con el Esquema Nacional de Seguridad, aplicando los principios de trazabilidad, detección, respuesta, contención y retorno seguro a la operación normal del sistema."

### 2) Cómo relacionar RGPD + LOPDGDD con contratación pública

Puedes meterlo siempre que:
* Se contrate el desarrollo de un sistema.
* Se externalice un servicio.
* Haya subcontratación tecnológica.

**Claves para soltar en el examen:**

* **Encargado del tratamiento:** "Cuando el tratamiento sea realizado por un proveedor externo, deberá formalizarse un contrato de encargo de tratamiento conforme al artículo 28 del RGPD, especificando obligaciones de confidencialidad, seguridad, devolución de datos y supervisión por parte de la Administración."
* **Exigencias dentro del pliego:** "El pliego de prescripciones técnicas debe incluir requisitos de protección de datos y seguridad, entre ellos medidas técnicas adecuadas al riesgo, registro de actividad, segregación de funciones, cifrado y auditorías periódicas."
* **Seguimiento contractual:** "La Administración debe supervisar el cumplimiento del contrato en materia de seguridad y protección de datos, pudiendo requerir evidencias de controles, auditorías, pruebas de seguridad o indicadores definidos contractualmente."
* **Alineación con ENS (muy valorado):** "Las obligaciones del proveedor deberán alinearse con el Esquema Nacional de Seguridad, garantizando controles de acceso, auditoría, análisis periódico de riesgos y continuidad de servicio."
* **Prevención ante filtraciones y sanciones:** "El incumplimiento de estas obligaciones puede implicar responsabilidad administrativa tanto para el encargado como para el responsable del tratamiento, conforme a los artículos 82 y 83 del RGPD."

### 3) Cómo enlazar RGPD con ENS y normativa CCN-STIC en una respuesta

Este bloque da muchísimo nivel porque demuestra visión global.

**Frase general para usar en cualquier supuesto:**
> "Las obligaciones derivadas del RGPD en materia de seguridad del tratamiento (art. 32) se sustancian en la Administración mediante la aplicación del Esquema Nacional de Seguridad y de las guías CCN-STIC que lo desarrollan, garantizando la confidencialidad, integridad, disponibilidad, trazabilidad y autenticidad del sistema."

**Cómo meterlo de forma sistemática:**

1.  **Alineación RGPD → ENS:** "El artículo 32 del RGPD obliga a aplicar medidas de seguridad adecuadas al riesgo. En el ámbito del sector público, estas medidas se concretan a través del Esquema Nacional de Seguridad, que establece requerimientos mínimos de protección, operación y auditoría."
2.  **Mención a ENS (principios básicos):** "Se aplicarán los principios del ENS: seguridad integral, gestión del riesgo, prevención, detección, respuesta, mejora continua y líneas de defensa."
3.  **Uso de guías CCN-STIC:** "La selección de medidas deberá apoyarse en las guías CCN-STIC correspondientes, en especial las relativas a análisis de riesgos, bastionado, gestión de incidentes, auditoría y controles de seguridad sobre sistemas de información."
4.  **Relación con el Registro de Actividades de Tratamiento:** "El Registro de Actividades de Tratamiento debe reflejar las medidas de seguridad implantadas, alineadas con el ENS y justificadas conforme al análisis de riesgo realizado."
5.  **En caso de incidente:** "La gestión de brechas de seguridad se realizará aplicando el artículo 33 del RGPD y, en paralelo, el proceso de gestión de incidentes del ENS y las guías CCN-STIC serie 817, garantizando la detección, contención, erradicación y recuperación controlada del servicio."

**Frase de cierre corta para elevar la nota:**
> "De este modo, el cumplimiento legal del RGPD se materializa mediante la aplicación técnica y operativa del ENS y de las guías CCN-STIC, asegurando un sistema seguro, trazable, auditable y alineado con la normativa estatal."

## 5. Mini-esquema RGPD + LOPDGDD + ENS en 10 líneas para usar en examen

1.  La AGE actúa como **Responsable del Tratamiento** según el artículo 4 del RGPD.
2.  El tratamiento debe basarse en una **base jurídica válida** del artículo 6 RGPD.
3.  Debe existir **Registro de Actividades de Tratamiento** actualizado (art. 30).
4.  Si interviene un proveedor externo, debe firmarse contrato de **Encargado del Tratamiento** (art. 28).
5.  Las medidas de seguridad deben ser adecuadas al riesgo según artículo 32 RGPD.
6.  En la AGE estas medidas se concretan mediante el **Esquema Nacional de Seguridad**.
7.  El ENS exige análisis de riesgos, medidas organizativas y técnicas y auditoría periódica.
8.  La selección de medidas debe apoyarse en **guías CCN-STIC** aplicables.
9.  Si ocurre una brecha, debe notificarse a la AEPD en 72 horas (art. 33 RGPD).
10. Si implica riesgo elevado para las personas, también se informará a los afectados (art. 34).

---

# Ley 39/2015

Con frases reutilizables, claras, cortas, y fáciles de soltar en una respuesta del examen.

## 1. En qué situaciones suele salir la Ley 39/2015 en el supuesto

Normalmente aparece cuando se plantea:

* Un desarrollo de
* Registro electrónico
* Tramitación digital
* Presentación de solicitudes
* Notificaciones electrónicas
* Portafirmas o validación documental
* Procedimiento administrativo completo

Cuando preguntas del tipo:

* “¿Qué debe cumplir una aplicación de tramitación?”
* “¿Qué implicaciones legales tiene procesar solicitudes electrónicas?”
* “¿Cómo se gestiona un procedimiento de forma íntegramente digital?”

O cuando el exame quiere comprobar que sabes

* Qué debe hacer la aplicación
* Qué derechos tiene el ciudadano
* Qué obligaciones tiene la Administración

## 2. Mini-esquema básico para memorizar

> La Ley 39/2015 regula el procedimiento administrativo común y exige que la tramitación sea íntegramente electrónica, garantizando la validez, integridad, autenticidad, confidencialidad y disponibilidad de la información. Establece derechos del ciudadano, requisitos de registro electrónico, notificación, firma, representación, interoperabilidad y cómputo de plazos.

Si solo te diera tiempo a poner esto, ya estás aprobado.

## 3. Frases para meter en casi cualquier respuesta

**Tramitación electrónica obligatoria**
> La Ley 39/2015 establece, en su artículo 14, la obligación de relacionarse electrónicamente con las Administraciones Públicas para determinados colectivos, por lo que el sistema debe permitir una tramitación íntegramente digital del procedimiento.

**Derechos del ciudadano**
> El artículo 53 reconoce el derecho a conocer el estado de tramitación del expediente y acceder a los documentos del mismo, lo que implica que la solución debe ofrecer consultas seguras, trazables y accesibles.

**Registro electrónico**
> El artículo 16 exige un registro electrónico que permita la presentación de solicitudes 24x7, identificación del remitente, acuse de recibo y anotación automática de fecha y hora con sello de tiempo.

**Representación**
> La aplicación debe contemplar la presentación por representante, conforme al artículo 5, acreditando representación mediante apoderamiento y pudiendo verificarse a través del Registro Electrónico de Apoderamientos.

**Firma electrónica**
> La autenticidad e integridad de los documentos debe garantizarse mediante firma electrónica conforme al artículo 10, pudiendo utilizarse certificados cualificados o sistemas admitidos en Cl@ve.

**Notificaciones**
> Las notificaciones electrónicas deben realizarse a través de medios admitidos legalmente según el artículo 41, ofreciendo acreditación de fecha, contenido y acceso efectivo del interesado.

**Cómputo de plazos**
> El sistema debe aplicar el cómputo de plazos del artículo 30, considerando días hábiles, festivos nacionales, autonómicos y locales y el calendario oficial de la sede electrónica.

**Archivo electrónico único**
> El artículo 17 establece la conservación de expedientes en archivo electrónico único, lo que exige almacenamiento seguro, control de acceso y mantenimiento de integridad y trazabilidad.

## 4. “Plantilla de párrafo completo” para soltar en un supuesto

Esta frase puedes soltarla entera y nunca falla:

> El sistema debe permitir una tramitación íntegramente electrónica según la Ley 39/2015, garantizando identificación, firma, presentación telemática de solicitudes, registro electrónico conforme al artículo 16, acceso al estado de tramitación (artículo 53), notificaciones con plena validez jurídica (artículo 41), correcta gestión de representantes (artículo 5), aplicación automática del cómputo de plazos (artículo 30) y conservación segura del expediente en archivo electrónico único (artículo 17).

Ese párrafo solo, en una respuesta, sube nota en casi cualquier caso práctico.

## 5. Cómo enlazar Ley 39/2015 con ENS y ENI

Si quieres aparentar nivel alto, mete esto:

> La aplicación debe cumplir la Ley 39/2015, pero su materialización técnica se alinea con el ENS (seguridad del sistema) y con el ENI y sus NTI (estructura de documentos, metadatos, intercambio y archivo electrónico).

Esto pocas personas lo ponen y marca diferencia.

## 6. Ejemplos

### A) Desarrollo de aplicación para tramitación de subvenciones

El desarrollo de la aplicación debe garantizar una tramitación íntegramente electrónica conforme a la Ley 39/2015. La presentación de solicitudes se registrará mediante el Registro Electrónico (art. 16), con sello de tiempo y acuse de recibo automático. La identificación y firma del solicitante se realizará mediante sistemas admitidos legalmente (art. 10), pudiendo apoyarse en Cl@ve, certificados cualificados o firma en la nube.

El ciudadano tendrá acceso al estado del procedimiento en cualquier momento, dando cumplimiento al artículo 53. La gestión de representantes deberá permitir acreditación y consulta del apoderamiento según el artículo 5. El sistema deberá aplicar el cómputo de plazos (art. 30) y permitir la tramitación y resolución conforme a las fases definidas del procedimiento, incluyendo notificaciones electrónicas válidas conforme al artículo 41. Finalmente, los expedientes deberán conservarse en archivo electrónico único según el artículo 17, garantizando integridad, trazabilidad y conservación a largo plazo.

### B) Registro y presentación de solicitudes desde sede electrónica

El sistema debe implementar un registro electrónico conforme al artículo 16 de la Ley 39/2015, permitiendo la presentación telemática segura de solicitudes durante 24 horas al día y todos los días del año. Debe generar justificante acreditativo de la presentación con fecha, hora y número de registro, aplicando sello de tiempo.

El solicitante debe identificarse con un sistema de firma admitido (art. 10), incluyendo certificados electrónicos o Cl@ve. Si actúa en nombre de otro, deberá acreditarse la representación según el artículo 5. El sistema aplicará automáticamente el calendario de días hábiles y festivos conforme al artículo 30.

Los datos registrados formarán parte del expediente administrativo, que será accesible por el ciudadano durante toda la tramitación acorde al artículo 53. El expediente debe conservarse en archivo electrónico único según el artículo 17.

### C) Implantación de un sistema de notificaciones electrónicas

Las notificaciones electrónicas deben realizarse conforme al artículo 41 de la Ley 39/2015, garantizando la autenticidad del remitente, integridad del contenido y acreditación de la fecha y hora de puesta a disposición y de acceso del interesado. El sistema debe contemplar aviso mediante canales complementarios, sin valor de notificación, y gestionar el acceso efectivo o la expiración por transcurso de 10 días naturales.

La identificación del ciudadano se realizará mediante los sistemas de firma admitidos legalmente (art. 10). Debe registrarse trazabilidad completa del proceso, permitiendo acreditar posteriormente la validez del acto administrativo.

El sistema debe integrarse con las plataformas corporativas, pudiendo realizarse notificaciones a través de servicios como Notifica o Carpeta Ciudadana. La conservación y acceso posterior del documento se garantizará en archivo electrónico único según el artículo 17.

### D) Reingeniería completa del procedimiento administrativo en digital

De acuerdo con la Ley 39/2015, el procedimiento debe rediseñarse para garantizar su tramitación íntegramente electrónica, eliminando la dependencia de papel. La presentación de documentos se realizará por vía electrónica mediante registro conforme al artículo 16 y con plena validez jurídica. La identificación y firma se efectuarán mediante sistemas previstos en el artículo 10.

El sistema debe proporcionar al ciudadano acceso permanente al estado de tramitación y a los documentos del expediente, cumpliendo el artículo 53. La reingeniería debe incluir notificaciones electrónicas regladas conforme al artículo 41, aplicación automatizada del cómputo de plazos (art. 30) y soporte para actuación mediante representante (art. 5).

El expediente administrativo resultante se custodiará en archivo electrónico único según el artículo 17, aplicando medidas de seguridad, control de acceso y trazabilidad. La implementación técnica se alineará con el ENS y el ENI para garantizar seguridad, interoperabilidad y accesibilidad.

### E) Aplicación móvil de una Administración que soporta procedimientos electrónicos

La aplicación móvil debe permitir al ciudadano realizar trámites con validez jurídica conforme a la Ley 39/2015, asegurando identificación y firma electrónica con sistemas admitidos legalmente (art. 10), pudiendo integrarse con Cl@ve o certificados cualificados almacenados en el dispositivo o en la nube.

Las solicitudes transmitidas desde la aplicación deberán generarse en el Registro Electrónico de la Administración (art. 16), con sello de tiempo y acuse de recibo. El usuario debe poder consultar de forma segura el estado del expediente y acceder a los documentos completos durante la tramitación, cumpliendo el artículo 53. Si actúa en representación, deberá acreditarse y verificarse el apoderamiento según el artículo 5.

Las notificaciones deberán ser accesibles desde el dispositivo móvil y cumplir el artículo 41, trazando puesta a disposición, acceso y plazos. El expediente generado se conservará como archivo electrónico único según el artículo 17. El diseño técnico se alineará con el ENS y el ENI para asegurar seguridad, interoperabilidad y usabilidad.

---

# Ley 40/2015

Igual que con la Ley 39/2015:
* Explicación breve
* Frases listas para copiar en examen
* Varios ejemplos completos aplicados a supuestos reales de la AGE.

---

# PARTE I: Guía General y Frases Tipo

## 1. Qué pinta la Ley 40/2015 en el segundo ejercicio
Se utiliza cuando el caso práctico entra en temas como:
* Funcionamiento electrónico de las Administraciones Públicas
* Reutilización de sistemas
* Plataformas e infraestructuras compartidas
* Interoperabilidad entre organismos
* Sedes electrónicas
* Actuación automatizada
* Intercambio de datos entre sistemas

Es una ley perfecta para meter “puntos gratis” cuando se aborda:
* Integración entre ministerios
* Uso de servicios comunes (Cl@ve, Autentica, Notifica, INSIDE, etc.)
* Infraestructuras compartidas del Estado
* Ahorro de costes y no duplicar soluciones

## 2. Mini-esquema para memorizar

> La Ley 40/2015 regula el funcionamiento electrónico del sector público y exige reutilización de sistemas, uso de plataformas e infraestructuras comunes, interoperabilidad, sedes electrónicas con identificación y seguridad, actuación automatizada y funcionamiento coordinado entre Administraciones Públicas.

Con esta frase ya tienes medio punto asegurado en casi cualquier supuesto.

## 3. Frases tipo para usar en respuestas

**Funcionamiento electrónico**
> La Ley 40/2015 establece la obligatoriedad de funcionamiento electrónico de las Administraciones Públicas, garantizando eficiencia, transparencia y reducción de cargas administrativas.

**Reutilización de sistemas (clave para subir nota)**
> Según el artículo 157, deben reutilizarse soluciones e infraestructuras ya existentes en la Administración para evitar duplicidad de esfuerzos y gasto innecesario, priorizando el uso de servicios comunes.

**Plataformas e infraestructuras compartidas**
> El artículo 156 señala que las Administraciones utilizarán preferentemente servicios e infraestructuras compartidas, incluyendo sistemas de identificación, intercambio de datos, archivo, notificación y registro.

**Interoperabilidad**
> La ley requiere que los sistemas garanticen interoperabilidad técnica, semántica y organizativa, alineándose con el ENI y sus Normas Técnicas de Interoperabilidad.

**Sedes electrónicas**
> Las sedes electrónicas deben asegurar disponibilidad, autenticidad, integridad, veracidad y protección de la información gestionada, conforme al artículo 38.

**Actuación automatizada**
> El artículo 41 permite la actuación administrativa automatizada, siempre que el procedimiento identifique el órgano responsable y deje trazabilidad y auditoría de las decisiones.

**Seguridad**
> La Ley 40/2015 establece que la seguridad se implementará aplicando el Esquema Nacional de Seguridad y las guías CCN-STIC asociadas.

## 4. Cómo enlazar Ley 40/2015 con ENS y ENI

Frase para soltar y sumar puntos:

> La seguridad del sistema se implementará conforme al ENS, mientras que la interoperabilidad y el intercambio de datos se ajustarán al ENI y a sus Normas Técnicas, garantizando la coordinación establecida en la Ley 40/2015.

## 5. EJEMPLOS COMPLETOS PARA EXAMEN
Como me pediste, igual que con la Ley 39/2015: 5 casos distintos, listos para copiar y pegar.

### A) Integración de sistemas entre dos Ministerios
La integración entre ambos organismos deberá realizarse conforme a la Ley 40/2015, que exige funcionamiento electrónico de las Administraciones y coordinación en el intercambio de información. La interoperabilidad se garantizará según el artículo 156, utilizando plataformas e infraestructuras compartidas y evitando la duplicación de sistemas.

El intercambio de datos se alineará con el ENI y sus Normas Técnicas de Interoperabilidad para asegurar consistencia, semántica común, metadatos homogéneos y trazabilidad. La seguridad se implementará mediante el ENS, asegurando confidencialidad, integridad, disponibilidad y autenticación en el consumo de servicios. De esta forma, ambos organismos podrán compartir información de forma segura, eficiente y con plena validez administrativa.

### B) Implantación de una nueva plataforma corporativa para toda la AGE
La Ley 40/2015 establece que deben priorizarse infraestructuras y servicios compartidos para reducir costes y garantizar eficiencia. Según el artículo 156, la plataforma corporativa será común para toda la Administración General del Estado, evitando desarrollos duplicados y facilitando reutilización.

La solución debe asegurar interoperabilidad plena con otros sistemas públicos, conforme al ENI. Para garantizar seguridad, se aplicarán las medidas exigidas por el ENS, incluyendo autenticación, trazabilidad, auditoría y gestión de riesgos. La implantación de servicios comunes permite estandarizar procedimientos, simplificar la tramitación y asegurar un funcionamiento coordinado entre organismos.

### C) Diseño de una sede electrónica
El diseño de la sede electrónica debe cumplir con el artículo 38 de la Ley 40/2015, garantizando disponibilidad, veracidad, integridad y seguridad de la información. La identificación de los ciudadanos y empleados públicos se realizará mediante sistemas admitidos legalmente, mientras que la sede deberá ofrecer acceso a expedientes y servicios de forma continuada.

La sede se considerará un punto oficial de relación electrónica con el ciudadano, debiendo disponer de información sobre titularidad, canales de atención, calendario oficial y medios de contacto. La seguridad se implementará conforme al ENS, y la interoperabilidad y presentación documental se ajustarán al ENI y NTI de documentación y metadatos.

### D) Desarrollo de un sistema de notificación entre Administraciones
Conforme a la Ley 40/2015, el sistema debe permitir el funcionamiento electrónico coordinado entre Administraciones, simplificando procesos y evitando duplicidades. El artículo 156 establece el uso de plataformas e infraestructuras compartidas, por lo que el sistema podrá integrarse con servicios comunes como Notifica o SIR.

El intercambio de información se realizará asegurando interoperabilidad organizativa, técnica y semántica conforme al ENI. La seguridad se implementará aplicando el ENS, con identificación, control de acceso, trazabilidad, auditoría y protección de extremo a extremo.

### E) Implantación de actuaciones administrativas automatizadas
El artículo 41 de la Ley 40/2015 permite la actuación administrativa automatizada siempre que el procedimiento identifique el órgano responsable y garantice trazabilidad, auditoría y control. La aplicación deberá registrar todas las operaciones ejecutadas por la automatización, almacenando evidencias y permitiendo auditoría posterior.

La seguridad debe alinearse con el ENS, mientras que los formatos, intercambio de datos y metadatos se ajustarán al ENI. La automatización contribuye a la eficiencia, reducción de plazos y eliminación de cargas, manteniendo plena validez jurídica del procedimiento.

---

# PARTE II: Ley 40/2015 Aplicada a Supuestos

La Ley 40/2015 regula el funcionamiento interno del Sector Público, y en el examen del segundo ejercicio es muy útil cuando nos piden:

* Funcionamiento de sistemas dentro de una Administración
* Colaboración entre Administraciones
* Interoperabilidad
* Sedes electrónicas
* Reutilización de servicios comunes
* Órganos colegiados
* Sistemas de información y seguridad administrativa

## Artículos más útiles para meter en una respuesta

| Artículo | Tema clave | Cuándo citarlo |
| :--- | :--- | :--- |
| **Art. 3** | Principios de actuación del sector público | Introducciones y justificaciones normativas |
| **Art. 13** | Funcionamiento electrónico del Sector Público | Cualquier sistema digital interno |
| **Art. 157** | Funcionamiento de los medios electrónicos | Sedes, aplicaciones, plataformas electrónicas |
| **Art. 156 y 157** | Interoperabilidad y seguridad de los sistemas | Para justificar uso de ENS, ENI, NTI |
| **Art. 140** | Reutilización de sistemas y servicios compartidos | Cuando se eligen servicios comunes como Cl@ve, INSIDE, etc. |
| **Art. 149–153** | Cooperación entre Administraciones | Proyectos entre varios organismos |
| **Art. 129–138** | Órganos colegiados | Comité de seguimiento, gobernanza, cuadros de mando |

Estas son las más “rentables” en un examen.

## Cómo justificar su uso de forma corta (Frases tipo)

**Para justificar uso de servicios comunes**
> De acuerdo con el principio de reutilización de sistemas establecido en el artículo 140 de la Ley 40/2015, se prioriza el uso de plataformas comunes ya disponibles en la AGE, evitando desarrollos duplicados y reduciendo plazos y costes.

**Para justificar seguridad e interoperabilidad**
> En cumplimiento de los artículos 156 y 157 de la Ley 40/2015, el sistema se integra con el Esquema Nacional de Seguridad y el Esquema Nacional de Interoperabilidad, garantizando protección de la información e intercambio de datos entre Administraciones.

**Para justificar sedes electrónicas y funcionamiento en digital**
> Conforme al artículo 13 y 157 de la Ley 40/2015, la tramitación administrativa se realizará íntegramente por medios electrónicos, integrándose en la sede electrónica del organismo y permitiendo la relación telemática con el ciudadano.

**Para proyectos que involucren varias Administraciones**
> De acuerdo con los artículos 149 a 153 de la Ley 40/2015, el proyecto se diseña en un marco de cooperación administrativa, permitiendo el intercambio ágil de información entre organismos y evitando duplicidades en la gestión pública.

**Para gobernanza del proyecto**
> Se establece un comité de seguimiento conforme a lo previsto en los artículos 129 a 138 de la Ley 40/2015 relativo a la organización y funcionamiento de órganos colegiados.

## Ejemplos reales para soltar en el examen

### EJEMPLO 1: Sistema de gestión de expedientes compartido entre dos Ministerios
La solución se desarrollará como un servicio horizontal reutilizable, conforme al artículo 140 de la Ley 40/2015, priorizando el aprovechamiento de sistemas ya disponibles en la AGE para reducir esfuerzos y garantizar sostenibilidad a largo plazo.

El sistema garantizará interoperabilidad en el intercambio de expedientes y datos entre ambos organismos, cumpliendo lo establecido en los artículos 156 y 157 de la Ley 40/2015 en relación con la interoperabilidad y el uso de medios electrónicos dentro del sector público.

### EJEMPLO 2: Creación de un módulo dentro de la sede electrónica
La tramitación se integrará dentro de la sede electrónica corporativa del organismo, tal como establece el artículo 13 y 157 de la Ley 40/2015, permitiendo a ciudadanos y empresas realizar consultas, presentar documentación y hacer seguimiento del estado de su expediente mediante medios electrónicos.

### EJEMPLO 3: Proyecto de nueva aplicación que consume Cl@ve, Notifica, INSIDE, etc.
Siguiendo el principio de reutilización recogido en el artículo 140 de la Ley 40/2015, la solución se apoyará en los servicios comunes ya prestados por la AGE, como Cl@ve para autenticación, INSIDE para gestión documental y Notifica para la práctica de notificaciones electrónicas, evitando desarrollos duplicados y optimizando recursos públicos.

### EJEMPLO 4: Gobernanza del desarrollo de un proyecto
Para asegurar la correcta coordinación del proyecto se constituirá un comité de seguimiento conforme a los artículos 129 a 138 de la Ley 40/2015 sobre órganos colegiados de la Administración, que supervisará evolución, riesgos y cumplimiento de objetivos.


---

# REGLAMENTO DE ACTUACIÓN (RD 203/2021)

El **RD 203/2021** desarrolla las Leyes 39 y 40/2015. Es la norma operativa que define cómo deben funcionar los servicios electrónicos de la AGE.

---

## 1. CONCEPTOS OBLIGATORIOS (DEFINICIONES LEGALES)

### 1.1. Sede Electrónica (Art. 9-12)
* **Qué es:** No es una simple web. Es la dirección electrónica disponible para los ciudadanos a través de redes de telecomunicaciones cuya titularidad corresponde a una AAPP.
* **Responsabilidad:** El titular de la Sede es responsable de la integridad, veracidad y actualización de la información.
* **Requisitos:** Debe garantizar la **disponibilidad**, el acceso seguro (HTTPS) y la identificación del titular.

### 1.2. PAGe (Punto de Acceso General electrónico)
* **Qué es:** Es la "puerta de entrada" única (`administracion.gob.es`).
* **Obligación:** Todas las Sedes Electrónicas de la AGE deben ser accesibles a través del PAGe. Tu sistema debe facilitar la integración o publicación en él.

### 1.3. Carpeta Ciudadana (Área Personal)
* **Qué es:** El servicio que permite al ciudadano consultar el estado de sus expedientes, sus notificaciones y sus datos en poder de la administración.
* **Obligación:** Cualquier nuevo trámite que diseñes **debe** volcar su información en la Carpeta Ciudadana (interoperabilidad).

---

## 2. ACTUACIÓN ADMINISTRATIVA AUTOMATIZADA (AAA) (Art. 40-42)
* **Definición:** Acto producido por un sistema de información adecuadamente programado sin intervención de empleado público.
* **Requisito:** Se debe definir el **órgano responsable** a efectos de impugnación.
* **Firma:** Se realiza mediante **Sello Electrónico de Administración Pública**.

---

## 3. REUTILIZACIÓN Y TRANSFERENCIA (Art. 64)
* **Obligación:** Antes de adquirir o desarrollar una aplicación, se debe consultar el **Directorio General de Aplicaciones (CTT)** para ver si existe una solución reutilizable.
* **Justificación en Supuesto:** "En cumplimiento del Art. 64 del RD 203/2021, antes de iniciar el desarrollo, se consultará el CTT para verificar la existencia de soluciones reutilizables, optando por servicios comunes como GEISER o INSIDE".

---