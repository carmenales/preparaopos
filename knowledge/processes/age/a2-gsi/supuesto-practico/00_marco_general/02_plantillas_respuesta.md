# 02. PLANTILLAS DE RESPUESTA — GUÍA DEFINITIVA (VERSIÓN MÁXIMA)

**Documento unificado:** incluye TODAS las plantillas, frases tipo, versiones completas, cortas y largas, modelos DEV/SYS/HÍBRIDOS, plantillas de análisis, arquitectura, seguridad, RGPD, ENS, ENI, servicios comunes, introducción, cierre, errores típicos y ejemplos completos listos para copiar en examen.

---

# 1. INTRODUCCIÓN UNIVERSAL (SE USA SIEMPRE)

Las siguientes versiones puedes copiarlas tal cual en cualquier respuesta. Se garantiza puntuación en normativa, seguridad, interoperabilidad y protección de datos.

## 1.1. Introducción universal — Versión LARGA (máxima puntuación)

!!! note "Versión Completa (Recomendada)"
    La Administración Pública actúa conforme a los principios de eficacia, eficiencia, servicio al ciudadano y sometimiento pleno a la Ley y al Derecho (Art. 103 CE). La solución se diseña garantizando el cumplimiento de la Ley 39/2015, que regula el procedimiento administrativo común, y de la Ley 40/2015, relativa al funcionamiento electrónico del sector público, asegurando tramitación íntegramente electrónica, interoperabilidad, reutilización de servicios comunes y funcionamiento coordinado entre Administraciones.

    Se aplicará el Esquema Nacional de Seguridad (RD 311/2022), incluyendo análisis de riesgos, medidas del Anexo II, trazabilidad, control de accesos, auditoría y registro de actividad conforme a las guías CCN-STIC series 800, 400 y 500. Asimismo, se garantizará la interoperabilidad mediante el Esquema Nacional de Interoperabilidad (RD 4/2010) y las Normas Técnicas de Interoperabilidad aplicables a documentos electrónicos, expedientes electrónicos, política de firma y servicios web.

    La solución garantiza accesibilidad universal conforme al RD 1112/2018 y criterios WCAG 2.1 AA, y cumplirá el Reglamento General de Protección de Datos (RGPD) y la LOPDGDD aplicando protección de datos desde el diseño, minimización, base jurídica del artículo 6.1.e, registro de actividades y contratos con encargados del tratamiento.

    Se prioriza el uso de servicios comunes  de la AGE, la interoperabilidad real, la protección de datos y el despliegue eficiente en Nube SARA, garantizando sostenibilidad y reutilización conforme a la Ley 40/2015 (Art. 157).

## 1.2. Introducción universal — Versión MEDIA

!!! tip "Versión Media"
    La solución se diseña conforme a la Ley 39/2015 y Ley 40/2015, garantizando tramitación electrónica, interoperabilidad, uso de servicios comunes y cumplimiento del ENS, ENI y RGPD. Se prioriza despliegue en Nube SARA, accesibilidad según RD 1112/2018 y protección de datos desde el diseño.

## 1.3. Introducción universal — Versión CORTA

!!! warning "Versión Corta"
    Cumple Ley 39/2015, Ley 40/2015, ENS, ENI, RGPD y accesibilidad RD 1112/2018. Reutiliza servicios comunes y se despliega en Nube SARA.

## 1.4. Introducción legal + eficiencia + contención del gasto (versión alternativa)

!!! info "Versión Eficiencia"
    La Administración Pública actúa conforme a los principios de eficacia, eficiencia, jerarquía, coordinación y servicio al interés general (Art. 103 CE). En un contexto de responsabilidad fiscal y contención del gasto público (Ley 2/2012), la solución prioriza la reutilización de servicios comunes de la AGE, la simplificación administrativa y el uso eficiente de los recursos tecnológicos y económicos.

    La propuesta garantiza alineación normativa, sostenibilidad presupuestaria y coherencia con las directrices de digitalización del sector público.

## 1.5. Alineación estratégica con planes nacionales (opcional pero suma puntos)

### Alineación con el Plan de Digitalización AAPP 2021–2025
Puedes citar la línea exacta según el tipo de proyecto:

* **Línea 1 – Ciudadanía:** "Se mejora la experiencia de usuario, usabilidad y accesibilidad, alineado con la Línea 1 del Plan de Digitalización AAPP 2021–2025."
* **Línea 2 – Eficiencia y Automatización:** "Se automatizan tareas y flujos, alineado con la Línea 2 del Plan, orientada a eficiencia y RPA."
* **Línea 3 – Datos:** "Se impulsa intercambio de datos y uso de PID, en coherencia con la Línea 3."
* **Línea 4 – Infraestructura Cloud / Teletrabajo:** "Despliegue en Nube SARA y puesto inteligente, alineado con Línea 4."
* **Línea 5 – Ciberseguridad:** "Reforzamiento de medidas ENS y CCN-STIC, alineado con la Línea 5 del Plan."

### Alineación con España Digital 2026
> El proyecto se coloca dentro de las acciones de transformación digital contempladas en España Digital 2026, reforzando interoperabilidad, uso de datos y seguridad.

### Alineación con el Plan de Recuperación (PRTR)
> El proyecto contribuye a los objetivos del PRTR en materia de digitalización, modernización y mejora del servicio público.

---

# 2. CHECKLIST PREVIO (ANTES DE ESCRIBIR EN EL EXAMEN)

**Marco jurídico administrativo**

- [x] Ley 39/2015 — Procedimiento Administrativo Común
- [x] Ley 40/2015 — Régimen Jurídico del Sector Público

**Seguridad**

- [x] ENS (RD 311/2022)
- [x] CCN-STIC 801 (roles y responsabilidades)
- [x] CCN-STIC 804 (implantación)
- [x] CCN-STIC 811 (interconexión ENS)
- [x] CCN-STIC 408 (seguridad perimetral)
- [x] CCN-STIC 836 (VPN)

**Interoperabilidad**

- [x] ENI (RD 4/2010)
- [x] NTI Documento electrónico
- [x] NTI Expediente
- [x] NTI Política de Firma
- [x] NTI Intermediación de Datos
- [x] NTI Servicios Web

**Protección de datos**

- [x] RGPD
- [x] LOPDGDD

**Accesibilidad**

- [x] RD 1112/2018
- [x] WCAG 2.1
- [x] UNE-EN 301549

---

# 3. PLANTILLAS DE ANÁLISIS FUNCIONAL (CON FRASES)

## 3.1. Plantilla completa — ANÁLISIS FUNCIONAL

**Contexto del procedimiento**
> El procedimiento descrito permite la gestión electrónica de XXX, garantizando tramitación íntegramente digital conforme a la Ley 39/2015 y permitiendo la relación telemática con ciudadanos y empresas.

**Actores**
> Los actores principales son: ciudadano, funcionario tramitador, responsable del órgano gestor y sistemas externos (Cl@ve, SIR, Notifica, PID).

**Canales**
> Se habilitarán los canales web, móvil, sede electrónica y Carpeta Ciudadana, garantizando accesibilidad conforme al RD 1112/2018.

**Requisitos funcionales (RF)**
> * RF1: Presentación telemática de solicitudes con registro automático.
> * RF2: Consulta del expediente.
> * RF3: Generación de notificaciones electrónicas.
> * RF4: Integraciones con servicios comunes.

**Requisitos no funcionales (RNF)**
> Rendimiento, disponibilidad 24x7, escalabilidad, accesibilidad, trazabilidad ENS, seguridad por diseño.

**Casos de uso principales**
> * CU1: “Presentar Solicitud” — validación automática, registro y acuse.
> * CU2: “Consultar Estado” — acceso seguro con Cl@ve.

**Integraciones**
> Se integrará con Cl@ve para autenticación, @firma para firma, INSIDE para expediente electrónico, Notifica para notificaciones y PID para consultas.

**Reglas de negocio y validaciones**
> Las validaciones se aplican en servidor según el procedimiento administrativo, con comprobaciones automáticas frente a PID y catálogos DIR3.

**Trazabilidad y auditoría ENS**
> Todas las operaciones quedarán registradas conforme al ENS, garantizando trazabilidad completa.

**Protección de datos (RGPD)**
> Se aplica minimización, base jurídica del artículo 6.1.e y registro de actividad del tratamiento.

## 3.2. Plantilla ANÁLISIS — Versión CORTA
> Actores → RF/RNF → Casos de Uso → Integraciones (Cl@ve, Notifica, INSIDE) → Seguridad ENS → RGPD → Accesibilidad.

---

# 4. PLANTILLAS DE ARQUITECTURA LÓGICA (DEV)

## 4.1. Plantilla completa ARQUITECTURA LÓGICA

!!! tip "Modelo de 4 capas"
    La arquitectura se organiza en 4 capas (Presentación, Negocio, Integración, Datos), garantizando separación de responsabilidades, mantenibilidad, seguridad desde el diseño (OWASP) e interoperabilidad (ENI + NTI).

!!! tip "Módulos / paquetes"
    Los módulos se agrupan en gestión de solicitudes, tramitación, notificaciones, expediente electrónico y servicios comunes.

!!! tip "API REST"
    Las APIs se documentarán con OpenAPI y cumplirán la NTI de Servicios Web, asegurando intercambio interoperable.

!!! tip "Modelo de datos"
    El modelo de datos aplica principios ENI, minimización RGPD y metadatos obligatorios para documentos y expedientes electrónicos.

!!! tip "Servicios comunes"
    Cl@ve, @firma, INSIDE, Notifica, PID, DIR3.

!!! tip "Seguridad OWASP"
    Se aplicarán controles OWASP Top 10: validación, gestión de sesiones, control de acceso, cifrado TLS, logging seguro.

!!! tip "RGPD"
    Minimización, limitación de finalidad y registros de actividad.

## 4.2. Plantilla corta ARQUITECTURA LÓGICA
> 4 capas → paquetes → APIs REST → modelo de datos → ENI + NTI → OWASP → RGPD.

---

# 5. PLANTILLAS DE ARQUITECTURA TÉCNICA (SISTEMAS)

## 5.1. Plantilla completa

!!! tip "Infraestructura: Nube SARA / CPD"
    El sistema se desplegará en la infraestructura Nube SARA garantizando eficiencia, disponibilidad y soberanía del dato.

!!! tip "Topología (VLAN, DMZ, firewalls)"
    Se definen VLAN separadas para presentación, negocio, datos y administración, con firewalls perimetrales y reglas restrictivas.

!!! tip "Acceso seguro"
    VPN IPsec/SSL, MFA y bastionado de servidores siguiendo guías CCN-STIC 817 y 836.

!!! tip "HA y DRP"
    Se emplearán clusters activos/pasivos y replicación síncrona.

!!! tip "Monitorización"
    SIEM, Syslog, métricas de disponibilidad y alertado.

!!! tip "ENS"
    Clasificación del sistema (B/M/A) y aplicación de medidas del Anexo II.

!!! tip "Cifrado"
    TLS 1.2+, cifrado AES-256 en reposo.

## 5.2. Plantilla corta ARQUITECTURA TÉCNICA
> Nube SARA → VLAN + FW → VPN + MFA → HA + DRP → Monitorización → ENS.

---

# 6. PLANTILLAS DE SEGURIDAD (ENS + CCN + RGPD)

## 6.1. Plantilla completa

!!! tip "ENS"
    Se categoriza el sistema según las dimensiones de confidencialidad, integridad y disponibilidad, aplicando las medidas del Anexo II y guías CCN-STIC.

!!! tip "Control de acceso"
    RBAC, MFA, sesiones seguras, principio mínimo privilegio.

!!! tip "Registro de actividad"
    Logs firmados, sincronizados y custodiados según ENS y RGPD art. 32.

!!! tip "Auditoría"
    Auditoría bienal ENS y pruebas de penetración.

!!! tip "Cifrado"
    * En tránsito: TLS 1.2/1.3.
    * En reposo: AES-256 + cifrado de BBDD.

!!! tip "Respuesta a incidentes"
    Según guías CCN-STIC 817: detección, contención, erradicación, recuperación.

!!! tip "Protección de datos"
    RAT, EIPD si alto riesgo, contratos art. 28.

### Guías CCN-STIC recomendadas (para meter según contexto)
* **CCN-STIC 801** — Roles y responsabilidades ENS
* **CCN-STIC 804** — Implantación ENS
* **CCN-STIC 808** — Política de seguridad
* **CCN-STIC 811** — Interconexión segura
* **CCN-STIC 817** — Gestión de incidentes
* **CCN-STIC 825** — Hardening
* **CCN-STIC 836** — Seguridad en VPN
* **CCN-STIC 1400** — Detección temprana (con Sondas/Lazarus)

**Frase tipo:**
> "Se aplicarán las guías CCN-STIC 801, 804, 811 y 836 para garantizar un diseño seguro conforme al ENS y buenas prácticas de ciberseguridad del CCN."

## 6.2. Plantilla corta
> ENS → MFA → Trazabilidad → Auditoría → Cifrado → RGPD → EIPD.

---

# 7. PLANTILLAS DE SERVICIOS COMUNES

## 7.1. Plantilla completa

**Autenticación → Cl@ve**
> La autenticación se realizará mediante Cl@ve, garantizando identificación segura conforme a la Ley 39/2015.

**Firma → @firma/FIRe**
> Las firmas electrónicas se validarán mediante la plataforma @firma, aplicando la NTI de Política de Firma.

**Expediente → INSIDE**
> La gestión de expedientes seguirá la NTI de Expediente Electrónico y se alojará en INSIDE.

**Registro → GEISER**
> Todas las solicitudes generarán asiento registral con GEISER/SIR.

**Notificaciones → Notifica**
> Las notificaciones se practicarán mediante Notifica garantizando evidencia de entrega.

**Intercambio → SIR**
> Intercambio seguro entre Administraciones mediante SIR.

**Datos → PID**
> Las consultas de datos se harán mediante la Plataforma de Intermediación (PID), aplicando el principio “no aportar”.

---

# 8. PLANTILLAS DE CIERRE

## Cierre largo
> La solución propuesta garantiza el cumplimiento de la Ley 39/2015, Ley 40/2015, ENS, ENI, RGPD y RD 203/2021, asegurando interoperabilidad, seguridad, trazabilidad, accesibilidad, eficiencia y plena validez jurídica del procedimiento. Se prioriza la reutilización de servicios comunes y el despliegue en la infraestructura Nube SARA, garantizando sostenibilidad y protección del interés público.

## Cierre corto
> Cumple Ley 39/2015, Ley 40/2015, ENS, ENI y RGPD, y usa servicios comunes.

---

# 9. ERRORES QUE SUSPENDEN (Y SUS CORRECCIONES)

❌ **Haber olvidado ENS**
> **Corrección:** Se aplicarán las medidas de seguridad del ENS (RD 311/2022), incluyendo análisis de riesgos, control de acceso, trazabilidad y auditoría.

❌ **No citar servicios comunes**
> **Corrección:** El sistema reutiliza Cl@ve, @firma, INSIDE, Notifica y SIR.

❌ **Confundir Ley 39 con 40**
> **Solución:** incluida en todas las plantillas.

❌ **Olvidar RGPD**
> **Corrección:** Aplicación de minimización, base jurídica art. 6.1.e y RAT.

❌ **No justificar una decisión**
> **Fórmula universal:** Se elige X porque garantiza Y según Z (normativa).

## CONSEJOS DE EJECUCIÓN Y PRESENTACIÓN

Antes de escribir la primera palabra, ten en cuenta estas reglas de oro para la presentación física del examen:

1.  **Introducción por Pregunta:** Nunca empieces respondiendo "a saco". Contextualiza:
    > *"Pregunta 1. A continuación, se muestra el diagrama de contexto que describe las relaciones del sistema [NOMBRE] con las entidades externas..."*
2.  **Gestión del Espacio:** Redacta cada pregunta en una hoja nueva. Si es posible, deja una carilla en blanco entre preguntas para añadir matices si te sobra tiempo al final.
3.  **Precisión y Justificación:** Si eliges una tecnología, di por qué.

    * *Mal:* "Usaremos Spark."
    * *Bien:* "Para el análisis de datos se propone el uso de tecnología Spark (o similar) debido a su capacidad de procesamiento en memoria, superior a MapReduce."
    * *Truco:* La coletilla *"o solución de mercado similar"* te protege si no estás 100% seguro de la herramienta específica.
5.  **Coherencia Global:** Si en el Caso de Uso pintas al actor "Funcionario Habilitado", debe aparecer en el Diagrama de Secuencia. El tribunal penaliza la falta de consistencia entre diagramas.

---

# 10. EJEMPLOS COMPLETOS (LISTOS PARA COPIAR)

## Ejemplo 1 — Trámite ciudadano (DEV)
*(Incluye análisis, arquitectura, seguridad y cierre — perfecto para preguntas de desarrollo)*

!!! example "Respuesta Desarrollo"
    La solución permite gestionar el procedimiento de XXX mediante tramitación íntegramente electrónica conforme a la Ley 39/2015. Los actores son ciudadano, funcionario y sistemas externos (Cl@ve, Notifica, INSIDE, PID). El sistema permitirá presentación telemática, consulta del expediente, tramitación interna y notificación electrónica según art. 41.

    La arquitectura se basa en 4 capas (presentación, negocio, integración, datos), con APIs REST documentadas mediante OpenAPI según NTI de Servicios Web. El modelo de datos incorpora metadatos obligatorios conforme al ENI. La autenticación se delegará en Cl@ve, la firma se realizará mediante @firma/FIRe y los expedientes se custodiarán en INSIDE.

    Se aplicarán controles OWASP, cifrado TLS, trazabilidad ENS y medidas RGPD (minimización, RAT, contratos art. 28).

    La solución garantiza cumplimiento de Ley 39/2015, Ley 40/2015, ENS, ENI, RGPD y RD 203/2021.

## Ejemplo 2 — Redes, CPD y seguridad (SYS)

!!! example "Respuesta Sistemas"
    El sistema se desplegará en la infraestructura Nube SARA, aplicando segmentación en VLAN de presentación, negocio y datos, protegidas mediante firewalls perimetrales. El acceso remoto se realizará mediante VPN IPsec/SSL con MFA. La plataforma dispondrá de HA mediante cluster activo/pasivo y replicación de base de datos.

    Se aplicarán las medidas del ENS, incluyendo control de accesos, auditoría, trazabilidad y cifrado. Las operaciones quedarán registradas conforme a CCN-STIC 817.

    Se garantizará interoperabilidad mediante ENI y uso de servicios comunes como Notifica, SIR, GEISER y DIR3.

    Solución alineada con Ley 40/2015, ENS, ENI y RGPD.

## Ejemplo 3 — Notificaciones electrónicas

!!! example "Respuesta Notificaciones"
    El sistema permitirá practicar notificaciones electrónicas conforme al artículo 41 de la Ley 39/2015, garantizando fecha y hora de puesta a disposición, acceso del interesado y evidencias completas. Las notificaciones se realizarán mediante Notifica y se integrarán en Carpeta Ciudadana.

    El sistema aplicará ENS, ENI y RGPD, garantizando trazabilidad, auditoría y seguridad.


---

# 11. INTRODUCCIONES ESTRATÉGICAS

Estas introducciones son textos listos para copiar que justifican el proyecto desde un punto de vista estratégico, legal o presupuestario.

## 11.1. Introducción institucional (España Digital + PRTR)

!!! tip "Introcucción Institucional"
    *El proyecto se alinea con la estrategia nacional de transformación digital, enmarcada en el Plan de Digitalización de las AAPP 2021–2025, el Plan de Recuperación, Transformación y Resiliencia (PRTR) y la agenda España Digital 2026.
    La solución garantiza servicios accesibles, seguros y eficientes, fomentando la reutilización de infraestructuras tecnológicas compartidas y servicios comunes.*

## 11.2. Introducción constitucional (Artículo 103 CE)

!!! note "Nota"
    Especialmente útil cuando el enunciado menciona recursos limitados, falta de medios o necesidad de eficiencia.

!!! tip "Introducción constitucional"
    *La Administración Pública actúa conforme a los principios de eficacia, eficiencia, economía y servicio objetivo al interés general (Art. 103 CE).*

    *En un contexto de contención del gasto público (Ley Orgánica 2/2012), la solución se diseña garantizando máxima eficiencia, reutilización de servicios comunes y optimización de recursos.*


## 11.3. Introducción orientada a planes estratégicos
### Líneas del Plan de Digitalización AAPP 2021–2025

| Línea | Cuándo usarla | Frase lista |
|:---|:---|:---|
| **Línea 1 – Ciudadanía** | Apps, UX, identidad digital | *El proyecto impulsa la mejora de la experiencia de usuario, alineado con la Línea 1 del Plan de Digitalización y el nuevo modelo de identidad digital.* |
| **Línea 2 – Eficiencia** | Automatización, RPA, reducción de cargas | *Se promueve la automatización inteligente conforme a la Línea 2 del Plan, aumentando la eficiencia del procedimiento administrativo.*
| **Línea 3 – Datos** | Uso de PID, interoperabilidad | *La solución maximiza el intercambio seguro de datos siguiendo la Línea 3 del Plan, facilitando interoperabilidad técnica y semántica.* |
| **Línea 4 – Infraestructura** | Nube SARA, Puesto Inteligente, teletrabajo | *El despliegue en Nube SARA se enmarca en la Línea 4 del Plan, impulsando infraestructuras digitales eficientes.* |
| **Línea 5 – Seguridad** | Ciberseguridad, ENS | *La solución refuerza la ciberresiliencia siguiendo la Línea 5 del Plan, aplicando ENS y guías CCN-STIC.* |

## 11.4. Plantilla para justificar eficiencia
!!! tip 
    *La solución planteada reduce cargas administrativas, fomenta la digitalización integral del procedimiento y garantiza sostenibilidad presupuestaria mediante la reutilización de servicios comunes, en cumplimiento de la Ley 40/2015 y la Ley de Estabilidad Presupuestaria.*

## 11.5. Plantilla breve para exámenes con poco espacio
!!! tip
    *Proyecto alineado con España Digital 2026, Plan de Digitalización y PRTR; accesible, interoperable y seguro conforme ENS, ENI, RGPD y RD 1112/2018.*