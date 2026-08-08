---
id: "cm-ad-tic-p01-tema-005-analisis-no-funcional"
title: "Otros tipos de análisis en los sistemas de información"
type: "apunte"
status: "borrador"
processes:
  - "comunidad-madrid/administracion-digital/tic"
profiles:
  - "p01-analista-aplicaciones"
official_profile: "P01 - Analista de Aplicaciones"
official_topic: "Tema 5. Otros tipos de análisis en los sistemas de información"
source_ids:
  - "A2_Bloque_IV.pdf"
tags:
  - "requisitos-no-funcionales"
  - "iso-25010"
  - "rendimiento"
  - "seguridad"
  - "privacidad"
  - "rgpd"
  - "ens"
  - "benchmark"
created_at: "2026-08-08"
last_reviewed: "2026-08-08"
ai_generated: true
ai_sources:
  - "gemini"
  - "perplexity"
needs_human_review: true
---

# Tema 5. Otros tipos de análisis en los sistemas de información

## 1. Análisis de Requisitos No Funcionales (RNF)

Mientras que los **requisitos funcionales (RF)** definen *qué* debe hacer un sistema de información (las acciones, procesos y comportamientos específicos ante una entrada), los **requisitos no funcionales (RNF)** determinan *cómo* debe hacerlo. Establecen los atributos de calidad, restricciones del entorno, niveles de servicio y propiedades globales de la plataforma.

En los procesos selectivos de la AGE y Comunidades Autónomas, la referencia normativa estándar para la clasificación de las propiedades de calidad de software es la norma **ISO/IEC 25010** (que sustituyó a la ISO/IEC 9126).

[ ISO/IEC 25010 ]
                              │
+-----------------------------+-----------------------------+
│                             │                             │
[Rendimiento]                 [Seguridad]                   [Privacidad]
(Eficiencia, Carga,          (Autenticación, AAA,          (RGPD, LOPDGDD,
Latencia, Benchmarks)        Confidencialidad, ENS)        Privacidad desde el Diseño)


### 1.1. Rendimiento (Performance)
Define las métricas operativas del sistema bajo una carga de trabajo determinada.

**Patrón Lógico - Métricas Clave:**
*   **Tiempo de respuesta:** Lo que tarda el sistema en reaccionar a una petición del usuario (ej. milisegundos en cargar una pantalla o procesar un pago).
*   **Throughput (Rendimiento de procesamiento):** Número de transacciones o peticiones que el sistema puede procesar por unidad de tiempo (ej. 1000 transacciones por segundo).
*   **Escalabilidad:** Capacidad del sistema para manejar más carga añadiendo recursos (Escalabilidad vertical: añadir más RAM/CPU a un servidor; Escalabilidad horizontal: añadir más servidores al clúster).
*   **Consumo de recursos:** Límites en el uso de memoria, procesador y ancho de banda de red.
*   **Variables Físicas y Lógicas (Monitoreo Predictivo SMART):** 
    *   *Variables Físicas:* Temperatura, vibración, humedad, consumo de energía.
    *   *Variables Lógicas:* Atributos SMART de discos duros (*Self-Monitoring, Analysis and Reporting Technology*), tasa de paquetes perdidos en red, etc.

Según ISO/IEC 25010, la característica *Performance efficiency* se descompone en tres subcaracterísticas que conviene memorizar literalmente: **Comportamiento temporal** (*time behaviour* — tiempos de respuesta, procesamiento y throughput), **Utilización de recursos** (*resource utilization* — cantidad y tipo de recursos usados) y **Capacidad** (*capacity* — límites máximos que puede soportar un parámetro, ej. número máximo de usuarios concurrentes).

La validación del rendimiento se realiza mediante **pruebas no funcionales de carga**, que conviene distinguir bien porque suelen confundirse en examen:
*   **Pruebas de carga (*load testing*):** comprueban el comportamiento del sistema bajo el volumen de trabajo esperado en condiciones normales o en el máximo previsto.
*   **Pruebas de estrés (*stress testing*):** llevan al sistema por encima de su capacidad máxima para identificar el punto de ruptura (*break point*) y cómo se degrada o recupera (*graceful degradation*).
*   **Pruebas de resistencia (*endurance/soak testing*):** verifican el comportamiento del sistema bajo carga sostenida durante un periodo prolongado, detectando fugas de memoria (*memory leaks*) o degradación progresiva.
*   **Pruebas de picos (*spike testing*):** valoran la reacción del sistema ante incrementos súbitos y muy bruscos de carga.

#### Herramientas de Benchmark y Pruebas (Referenciadas en el temario oficial):
*   **Apache JMeter:** Aplicación *Open Source* en Java diseñada para medir rendimiento y realizar pruebas de carga en servicios HTTP, HTTPS, SOAP/REST, JDBC, LDAP, FTP, JMS, comandos shell y TCP[cite: 3, 4].
*   **LoadRunner (OpenText):** Solución empresarial para probar aplicaciones midiendo su comportamiento bajo carga masiva[cite: 3, 4].
*   **PassMark:** Herramienta para evaluar y comparar la capacidad de cómputo de microprocesadores (CPU Mark) en servidores (Intel Xeon, AMD Epyc) y clientes[cite: 3, 4].
*   **3DMark:** Benchmark orientado a gráficos 3D y evaluación del rendimiento de tarjetas gráficas (GPU)[cite: 3, 4].
*   **PCMark:** Benchmark que ofrece tests para medir la capacidad general de los equipos, incluyendo rendimiento de batería, almacenamiento y perfiles del sistema[cite: 3, 4].

En el ámbito contractual y de servicios TIC, los compromisos de rendimiento suelen fijarse mediante **Acuerdos de Nivel de Servicio (SLA — *Service Level Agreement*)**, que establecen umbrales concretos (ej. disponibilidad del 99,9%, tiempo de respuesta máximo de 2 segundos) y penalizaciones si no se cumplen[cite: 3, 4].


### 1.2. Seguridad
Garantiza que la información esté protegida frente a accesos no autorizados, modificaciones o destrucción. En la Administración Pública española se enmarca bajo el **Esquema Nacional de Seguridad (ENS - RD 311/2022)**.

**Patrón Lógico - Dimensiones de la Seguridad (Regla mnemotécnica CIDTA / DICAT):**
1.  **Confidencialidad [C]:** Solo accede a la información quien tiene permiso.
2.  **Integridad [I]:** La información no se altera de forma no autorizada o fraudulenta.
3.  **Disponibilidad [D]:** El sistema funciona y es accesible cuando se necesita.
4.  **Trazabilidad [T]:** Saber quién ha hecho qué, cuándo y desde dónde (mediante registros o logs).
5.  **Autenticidad [A]:** Garantizar que quien accede es realmente quien dice ser (ej. mediante certificado digital).

*Nota Métrica v3:* Métrica Versión 3 cuenta con una **Interfaz de Seguridad (SEG)** cuyo objetivo es incorporar en los sistemas de información mecanismos de seguridad adicionales a lo largo de todos los procesos (desde la Planificación hasta el Mantenimiento).

El propio **Real Decreto 311/2022, de 3 de mayo**, que deroga y sustituye al anterior RD 3/2010, formaliza literalmente estas cinco dimensiones en su Anexo I, indicando que "se tendrán en cuenta las siguientes dimensiones de la seguridad, que se identificarán por sus correspondientes iniciales en mayúsculas: a) Confidencialidad [C]; b) Integridad [I]; c) Trazabilidad [T]; d) Autenticidad [A]; e) Disponibilidad [D]". Es habitual encontrar en test y manuales el acrónimo alternativo **DICAT** o **AICAT**, que ordena las mismas cinco dimensiones. Cada dimensión afectada por un incidente se clasifica en un **nivel de seguridad BAJO, MEDIO o ALTO**, y de la combinación de niveles surge la **categoría del sistema** (BÁSICA, MEDIA o ALTA), que determina qué medidas de seguridad son exigibles.

El ENS se estructura en **principios básicos** (seguridad integral, gestión de riesgos, prevención/reacción/recuperación, líneas de defensa, reevaluación periódica y diferenciación de responsabilidades) y en un conjunto de **medidas de seguridad** agrupadas en tres marcos: **marco organizativo**, **marco operacional** y **medidas de protección**, detalladas en su Anexo II. El organismo de referencia técnica que da soporte al ENS es el **CCN (Centro Criptológico Nacional)**, a través de la serie de guías **CCN-STIC**.

A nivel de estándares internacionales de gestión de la seguridad de la información, la referencia es la familia **ISO/IEC 27000**, en particular **ISO/IEC 27001** (Sistema de Gestión de Seguridad de la Información, SGSI) e **ISO/IEC 27002** (catálogo de controles)[cite: 3, 4]. Para la seguridad específica en aplicaciones web, la referencia técnica más citada es el **OWASP Top 10**, que recopila los riesgos de seguridad más críticos en aplicaciones web (p. ej. control de acceso roto, fallos criptográficos, inyección), y el **OWASP ASVS** (*Application Security Verification Standard*) como marco de verificación de requisitos de seguridad en el análisis y diseño.

En cuanto a mecanismos técnicos, conviene diferenciar los dos grandes tipos de cifrado: **cifrado simétrico** (misma clave para cifrar y descifrar, ej. AES, más rápido, usado para grandes volúmenes de datos) y **cifrado asimétrico** (par de claves pública/privada, ej. RSA, más lento pero permite firma digital y no repudio, base de la autenticidad en la administración electrónica mediante certificados digitales).

### 1.3. Privacidad
Garantiza el tratamiento correcto y legal de los datos personales. Se rige por el **RGPD** (Reglamento (UE) 2016/679, General de Protección de Datos) y la **LOPDGDD** (Ley Orgánica 3/2018, de Protección de Datos Personales y garantía de los derechos digitales).

**Patrón Lógico - Conceptos Clave para el Test:**
*   **Privacidad desde el diseño (*Privacy by Design*):** La protección de datos se integra desde la fase inicial de análisis y diseño arquitectónico, no como un "parche" que se añade al final de la programación.
*   **Privacidad por defecto (*Privacy by Default*):** El sistema debe venir configurado con la máxima privacidad posible desde el inicio, sin que el usuario tenga que configurar nada (ej. casillas de "Acepto ceder mis datos" siempre desmarcadas al entrar).
*   **Minimización de datos:** El sistema solo debe solicitar y almacenar los datos estrictamente necesarios para cumplir su finalidad.

Ambos principios están regulados literalmente en el **artículo 25 del RGPD**, titulado "Protección de datos desde el diseño y por defecto". El apartado 1 exige al responsable del tratamiento aplicar, "tanto en el momento de determinar los medios de tratamiento como en el momento del propio tratamiento, medidas técnicas y organizativas apropiadas, como la seudonimización, concebidas para aplicar de forma efectiva los principios de protección de datos". El apartado 2 concreta la privacidad por defecto: el responsable garantizará que, por defecto, "solo sean objeto de tratamiento los datos personales que sean necesarios para cada uno de los fines específicos del tratamiento", aplicándose esta obligación a la cantidad de datos recogidos, la extensión de su tratamiento, su plazo de conservación y su accesibilidad.

Conviene relacionar la privacidad con los **principios generales del tratamiento de datos** del artículo 5 RGPD, muy preguntados de forma aislada: licitud, lealtad y transparencia; limitación de la finalidad; **minimización de datos**; exactitud; limitación del plazo de conservación; integridad y confidencialidad; y responsabilidad proactiva (*accountability*).

Otros conceptos que amplían y suelen aparecer junto a Privacy by Design/Default:
*   **Evaluación de Impacto relativa a la Protección de Datos (EIPD/DPIA):** análisis obligatorio (art. 35 RGPD) cuando un tratamiento pueda entrañar un alto riesgo para los derechos de las personas, típico en sistemas de la Administración con tratamientos masivos o datos sensibles.
*   **Seudonimización vs. anonimización:** la seudonimización sustituye los identificadores directos por un código, pero permite revertir el proceso con información adicional (sigue siendo dato personal); la anonimización elimina la posibilidad de reidentificación de forma irreversible (deja de ser dato personal y de estar sujeto al RGPD).
*   **Derechos ARCO-POL / derechos digitales (LOPDGDD):** acceso, rectificación, cancelación/supresión (derecho al olvido), oposición, portabilidad, limitación del tratamiento, y los derechos digitales específicos de la LOPDGDD (ej. derecho al olvido en búsquedas de internet, derecho a la educación digital).
*   **AEPD (Agencia Española de Protección de Datos):** autoridad de control nacional; publica guías de referencia como la *Guía de Privacidad desde el Diseño*, que recoge estrategias de optimización, configurabilidad y restricción para implementar el artículo 25 RGPD en la práctica.


## 2. Aspectos No Funcionales de Rendimiento y Eficiencia de Desempeño

El rendimiento (o *Performance Efficiency* según ISO/IEC 25010) mide la capacidad del sistema para responder a las solicitudes de los usuarios y procesos dentro de unos límites de tiempo y consumo de recursos adecuados bajo condiciones específicas.

### 2.1. Métricas Clave de Rendimiento y Capacidad

*   **Tiempo de respuesta (*Response Time*):** Tiempo transcurrido desde que un usuario o sistema envía una petición hasta que recibe la respuesta completa.
*   **Tiempo de latencia (*Latency*):** Tiempo que tarda en procesarse el primer byte de respuesta tras la solicitud.
*   **Rendimiento o Capacidad de procesamiento (*Throughput*):** Número de transacciones, peticiones o unidades de trabajo que el sistema procesa por unidad de tiempo (p. ej., peticiones/segundo, TPS).
*   **Utilización de Recursos (*Resource Utilization*):** Porcentaje de uso de CPU, memoria RAM, operaciones de E/S por segundo (IOPS), ancho de banda de red y espacio en disco.
*   **Línea Base (*Baseline*):** Registro estructurado de métricas de rendimiento obtenido en condiciones normales de operación que sirve de punto de comparación objetivo ante cambios o degradaciones del sistema.
*   **Variables Físicas y Lógicas (Monitoreo Predictivo SMART):** 
    *   *Variables Físicas:* Temperatura, vibración, humedad, consumo de energía.
    *   *Variables Lógicas:* Atributos SMART de discos duros (*Self-Monitoring, Analysis and Reporting Technology*), tasa de paquetes perdidos en red, etc.

### 2.2. Pruebas de Carga y Evaluación del Rendimiento (Benchmarks)

Para verificar y certificar los requisitos de rendimiento se utilizan pruebas automatizadas y herramientas de *benchmarking*:

#### Tipos de Pruebas de Rendimiento:
*   **Pruebas de Carga (*Load Testing*):** Verifican el comportamiento del sistema ante la carga de trabajo máxima esperada en producción.
*   **Pruebas de Estrés (*Stress Testing*):** Someten al sistema a cargas superiores al límite máximo planificado para identificar el punto de ruptura (*break point*) y comprobar su recuperación (*graceful degradation*).
*   **Pruebas de Escalabilidad / Pico (*Spike Testing*):** Validan la reacción del sistema ante incrementos súbitos y masivos de peticiones en intervalos breves.
*   **Pruebas de Resistencia (*Soak / Endurance Testing*):** Evalúan el rendimiento de la plataforma bajo una carga constante durante periodos prolongados para detectar fugas de memoria (*memory leaks*) o degradación paulatina.

#### Herramientas de Benchmark y Pruebas (Referenciadas en el temario):
*   **Apache JMeter:** Aplicación *Open Source* en Java diseñada para medir rendimiento y realizar pruebas de carga en servicios HTTP, HTTPS, SOAP/REST, JDBC, LDAP, FTP, JMS, comandos shell y TCP.
*   **LoadRunner (OpenText):** Solución empresarial para probar aplicaciones midiendo su comportamiento bajo carga masiva.
*   **PassMark:** Herramienta para evaluar y comparar la capacidad de cómputo de microprocesadores (CPU Mark) en servidores (Intel Xeon, AMD Epyc) y clientes.
*   **3DMark y PCMark:** Benchmarks orientados a gráficos 3D y evaluación general de capacidades de sistemas.


## 3. Aspectos No Funcionales de Seguridad

La seguridad en los sistemas de información garantiza que los activos informáticos y los datos se protejan contra accesos no autorizados, modificaciones o indisponibilidades.

### 3.1. Servicios Fundamentales de Seguridad (AAA)

1.  **Autenticación (*Authentication*):** Verificación técnica de la identidad de un usuario, proceso o sistema.
    *   *Mecanismos:* Contraseñas, certificados digitales (PKI), OAuth 2.0 / OpenID Connect, Kerberos (basado en tickets de autenticación).
2.  **Autorización (*Authorization*):** Determinación de los derechos de acceso y permisos específicos otorgados a un usuario o proceso autenticado sobre un recurso determinado.
    *   *Mecanismos:* Control de acceso basado en roles (RBAC), control de acceso basado en atributos (ABAC).
3.  **Trazabilidad / Contabilidad (*Accounting / Auditing*):** Registro y almacenamiento de las actividades realizadas por los usuarios y procesos para garantizar la rendición de cuentas y la detección de anomalías.
4.  **No Repudio (*Non-Repudiation*):** Garantía legal y técnica de que el emisor o receptor de una transacción no puede negar haber realizado dicha acción o enviado dicho mensaje.
5.  **Confidencialidad:** Garantía de que la información no sea divulgada ni accesible a personas o sistemas no autorizados.
6.  **Integridad:** Protección de la exactitud y la totalidad de los datos e interfaces frente a alteraciones no autorizadas o accidentes.
7.  **Disponibilidad:** Garantía de que los usuarios autorizados tengan acceso a los datos y recursos cuando lo requieran.

### 3.2. Marco Normativo de Seguridad en la Administración Pública: El Esquema Nacional de Seguridad (ENS)

En el ámbito de la Administración Pública española, los requisitos no funcionales de seguridad se articulan formalmente a través del **Real Decreto 311/2022**, de 3 de mayo, por el que se regula el **Esquema Nacional de Seguridad (ENS)**.

*   **Principios Básicos del ENS:** Seguridad integral, gestión de la seguridad basada en los riesgos, prevención, reorientación y actualización permanente, líneas de defensa, vigilancia continua y reevaluación periódica, diferenciación de responsabilidades.
*   **Dimensiones de Seguridad del ENS (Marco AICAT):**
    *   **A**utenticidad
    *   **I**ntegridad
    *   **C**onfidencialidad
    *   **A**disponibilidad
    *   **T**razabilidad
*   **Categorización de Sistemas:** Los sistemas se clasifican en categorías **Básica, Media o Alta** en función de la valoración de las dimensiones de seguridad en sus servicios e información.


## 4. Aspectos No Funcionales de Privacidad y Protección de Datos

La privacidad en el análisis de sistemas de información comprende las medidas técnicas, organizativas y de diseño orientadas a proteger la información de carácter personal de las personas físicas.

### 4.1. Marco Regulatorio (RGPD y LOPDGDD)

*   **Reglamento (UE) 2016/679 (RGPD):** Marco legal europeo relativo a la protección de las personas físicas en lo que respecta al tratamiento de datos personales y a la libre circulación de estos datos.
*   **Ley Orgánica 3/2018 (LOPDGDD):** Ley Orgánica de Protección de Datos Personales y garantía de los derechos digitales en España.

### 4.2. Principios de Privacidad en el Diseño de Sistemas

1.  **Privacidad desde el Diseño (*Privacy by Design*):** Las garantías de protección de datos deben integrarse técnicamente desde la fase inicial de concepción y arquitectura del sistema de información, no como un parche posterior.
2.  **Privacidad por Defecto (*Privacy by Default*):** El sistema debe aplicar automáticamente la configuración más restrictiva de protección de datos posibles, garantizando que, por defecto, solo se traten los datos personales necesarios para cada fin específico.
3.  **Minimización de Datos:** Los datos solicitados y procesados por el sistema deben ser adecuados, pertinentes y limitados a lo estrictamente necesario en relación con los fines para los que son tratados.
4.  **Seudonimización y Cifrado:**
    *   *Seudonimización:* Tratamiento de datos personales de manera que ya no puedan atribuirse a un interesado sin utilizar información adicional que se mantenga por separado.
    *   *Cifrado:* Cifrado de datos en reposo (*data at rest*), en tránsito (*data in transit*) y en uso (*data in use*).
5.  **Evaluación de Impacto de la Protección de Datos (EIPD / DPIA):** Análisis obligatorio en sistemas que impliquen un alto riesgo para los derechos y libertades de las personas físicas antes de poner en marcha el tratamiento.

## 5. Cuadro Comparativo Sintético: Aspectos No Funcionales

| Dimensión | Enfoque Principal | Métricas / Parámetros Típicos | Estándares y Normas de Referencia |
| :--- | :--- | :--- | :--- |
| **Rendimiento** | Comportamiento del sistema ante la carga de trabajo y uso de recursos. | Tiempo de respuesta, Latencia, Throughput (TPS), % CPU/RAM/IOPS, SMART. | ISO/IEC 25010, Benchmarks (JMeter, LoadRunner, PassMark). |
| **Seguridad** | Protección de la información y servicios contra accesos o fallos indebidos. | Niveles AAA, Cifrado, Vulnerabilidades, MTTR, MTBF. | RD 311/2022 (ENS), ISO/IEC 27001. |
| **Privacidad** | Protección del derecho a la salvaguarda de datos personales de personas físicas. | Minimización de datos, periodo de retención, tasa de seudonimización. | RGPD (UE 2016/679), LOPDGDD 3/2018, ISO/IEC 27701. |


## 6. Resumen

*   **ISO/IEC 25010:** RNF, Calidad de software, Reemplaza a la ISO 9126.
*   **Pruebas de Carga:** "Condiciones normales o máximas esperadas de uso".
*   **Pruebas de Estrés:** "Superar la capacidad máxima", "punto de rotura", "comprobar recuperación".
*   **ENS (RD 311/2022):** "Categorías Básica-Media-Alta", "Dimensiones AICAT".
*   **Privacidad desde el diseño:** "Desde la fase inicial del proyecto/análisis", "no como añadido posterior".
*   **JMeter:** "Pruebas de carga Open Source Java", "Multiprotocolo (HTTP, JDBC, LDAP)".


## 7. Simulacro de Test:

**Pregunta:**
*Durante el análisis de requisitos de un nuevo sistema centralizado para el Ministerio de Sanidad, se documenta la siguiente restricción: "El sistema deberá procesar un mínimo de 500 peticiones concurrentes por segundo utilizando un máximo del 60% de uso de CPU del servidor". ¿A qué categoría de análisis pertenece este requisito?*
a) Análisis Funcional de comportamiento.
b) Análisis de Rendimiento (Requisito No Funcional).
c) Análisis de Privacidad.
d) Análisis de Seguridad.

**Razonamiento Estructurado:**
1.  **Busca la palabra chivata:** El enunciado da datos concretos sobre "500 peticiones concurrentes por segundo" (esto es el throughput) y "máximo del 60% de uso de CPU" (consumo de recursos).
2.  **Aplica tu patrón lógico de descarte:**
    *   ¿Habla de una acción de negocio que realiza el usuario (ej. pedir una cita)? No, define una restricción técnica. Por tanto, no es funcional. **(A) es falsa**.
    *   ¿Menciona el tratamiento de datos de carácter personal o regulaciones como el RGPD? No. **(C) es falsa**.
    *   ¿Se trata de proteger contra accesos o modificaciones no autorizadas (cifrado, certificados)? No. **(D) es falsa**.
    *   Se refiere estrictamente a métricas operativas de estrés y carga del sistema.
3.  **Respuesta correcta:** B.

**Pregunta:**
*Según el Real Decreto 311/2022, por el que se regula el Esquema Nacional de Seguridad, ¿cuáles son las cinco dimensiones de seguridad que se valoran para determinar la categoría de un sistema de información?*
a) Confidencialidad, Integridad, Disponibilidad, Autenticación y Portabilidad.
b) Confidencialidad, Integridad, Trazabilidad, Autenticidad y Disponibilidad.
c) Privacidad, Integridad, Disponibilidad, Escalabilidad y Rendimiento.
d) Confidencialidad, Fiabilidad, Usabilidad, Mantenibilidad y Disponibilidad.

**Razonamiento Estructurado:**
1.  El propio texto del RD 311/2022 (Anexo I) enumera literalmente: Confidencialidad [C], Integridad [I], Trazabilidad [T], Autenticidad [A] y Disponibilidad [D] (regla mnemotécnica CIDTA/DICAT).
2.  (A) confunde Autenticidad con "Autenticación" e incluye Portabilidad, que es un atributo de calidad ISO 25010, no una dimensión ENS. (C) y (D) mezclan conceptos de rendimiento y calidad de software que no son dimensiones de seguridad del ENS.
3.  **Respuesta correcta:** B.

**Pregunta:**
*Una empresa pública sustituye los DNI de los ciudadanos en una base de datos estadística por un código alfanumérico, pero conserva en un fichero separado y protegido la tabla de correspondencia entre DNI y código. ¿Qué técnica de protección de datos ha aplicado?*
a) Anonimización.
b) Seudonimización.
c) Cifrado asimétrico.
d) Minimización de datos.

**Razonamiento Estructurado:**
1.  La clave está en que existe una "tabla de correspondencia" que permite revertir el proceso: eso es exactamente la definición de seudonimización, que sigue considerando el dato como personal a efectos del RGPD porque es reversible con información adicional. Si no existiera esa tabla y fuera imposible reidentificar a la persona, hablaríamos de anonimización (A).
2.  **Respuesta correcta:** B.
