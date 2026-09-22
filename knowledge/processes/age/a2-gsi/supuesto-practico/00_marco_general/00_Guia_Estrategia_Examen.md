# GUÍA ESTRATÉGICA DEL EXAMEN

## 1. Cómo elegir la opción del examen

!!! note "Perfil del examen"
    El examen ofrece dos opciones:

    * **Opción A → Desarrollo (Bloque III)**
    * **Opción B → Sistemas (Bloque IV)**
    
    Pero cada opción contiene **preguntas cruzadas**: de seguridad, datos, arquitectura o normativa.

### 1.1. Opción A — Perfil Desarrollo (Bloque III)
* **Fortalezas:**
    * Actores, Casos de Uso, RF/RNF
    * UML: clases, secuencia, estados
    * Modelo de datos
    * Arquitectura 4 capas
    * Servicios comunes (Cl@ve, @firma, INSIDE)
* **Riesgos:**
    * Redes, CPD, firewalls, segmentación
    * HA/DRP
    * VPN/Teletrabajo

### 1.2. Opción B — Perfil Sistemas (Bloque IV)
* **Fortalezas:**
    * Red SARA, Nube SARA
    * CPD, redes, VLAN, firewalls
    * Monitorización, Logging, SIEM
    * Alta disponibilidad, clusters
    * ENS, CCN-STIC
* **Riesgos:**
    * UML detallado
    * Modelado de datos
    * Diseño orientado al dominio

## 2. Estrategia ante preguntas cruzadas

!!! tip "Regla de oro"
    **Responde desde tu terreno.**
    
    * Si eres **DEV**, orienta Seguridad a OWASP + API + RGPD.
    * Si eres **SYS**, orienta Datos a HA + cifrado + backup + permisos.

### Caso 1: Soy Desarrollo y me preguntan Seguridad
* **Llevar hacia:**
    * OWASP Top 10
    * Autenticación y sesiones
    * HTTPS, TLS 1.2+
    * RGPD: minimización, confidencialidad
    * Logs y trazabilidad ENS
* **Evitar:**
    * Diseñar CPD, VLANs, segmentación física.

### Caso 2: Soy Sistemas y me preguntan Datos
* **Llevar hacia:**
    * Motor BBDD (PostgreSQL/Oracle)
    * HA: réplica, cluster
    * Tuning de rendimiento
    * Backup, retención, archivado
    * Cifrado en reposo y tránsito
    * Auditoría ENS
* **Evitar:**
    * UML complejo o diagrama de clases con atributos detallados.

## 3. Mapa rápido: qué carpeta mental usar según la pregunta

| Tipo pregunta | Perfil DEV | Perfil SYS | Carpeta |
| :--- | :--- | :--- | :--- |
| **Análisis** | Actores, Casos Uso, RF/RNF | Rendimiento/capacidad | /Analisis |
| **Datos** | UML, ENI-NTI | Motor BBDD + Cifrado | /Logica /Tecnica |
| **Arquitectura** | 4 capas | Despliegue: VPN, FW | /Logica /Tecnica |
| **Seguridad** | OWASP, roles | ENS, CCN-STIC | /Seguridad |
| **Servicios comunes** | Cl@ve, INSIDE | SIR/Geiser, Red SARA | /Servicios |
| **Normativa** | Ley 39/40 | ENS, RD 203/2021 | /General |

## 4. Introducción universal (siempre en todas las respuestas)

**Copiar-pegar este bloque tal cual al inicio:**

> La Administración Pública actúa conforme a los principios de eficacia, eficiencia, seguridad y legalidad (Art. 103 CE). La solución se diseña aplicando la Ley 39/2015, la Ley 40/2015, el Esquema Nacional de Seguridad (RD 311/2022) y el Esquema Nacional de Interoperabilidad (RD 4/2010). Se prioriza el uso de servicios comunes y de infraestructuras compartidas, garantizando accesibilidad (RD 1112/2018), protección de datos (RGPD y LOPDGDD) y despliegue en Nube SARA conforme a los principios de eficiencia y sostenibilidad pública.

## 5. Alineación estratégica con planes estatales

!!! note "Planes estratégicos que puedes citar"
    * Plan de Digitalización AAPP 2021–2025
    * España Digital 2026
    * Plan de Recuperación, Transformación y Resiliencia (PRTR)

**Usa la línea correcta según el contexto:**

* **Línea 1** → UX, AppFactory, identidad digital
* **Línea 2** → automatización, eficiencia
* **Línea 3** → datos e interoperabilidad (PID)
* **Línea 4** → Nube, teletrabajo, puesto inteligente
* **Línea 5** → seguridad y ciberresiliencia

## 6. BLOQUE NORMATIVO FUSIONADO
(Contiene TODAS las leyes y guías de tus ficheros originales)

### 6.1. Ley 39/2015 (LPAC)
!!! tip "Frase tipo para examen"
    El sistema permitirá tramitación íntegramente electrónica conforme a la Ley 39/2015, garantizando identificación (Art. 9), firma (Art. 10), registro electrónico (Art. 16), notificaciones (Art. 41), cómputo de plazos (Art. 30), acceso al expediente (Art. 53) y archivo electrónico único (Art. 17).

**Puntos clave:**

* Art. 14 → relación electrónica
* Art. 16 → registro electrónico
* Art. 10 → firma electrónica
* Art. 5 → representación
* Art. 41 → notificaciones
* Art. 53 → derecho a consulta
* Art. 30 → plazos

### 6.2. Ley 40/2015 (LRJSP)
!!! tip "Frase tipo para examen"
    Se prioriza la reutilización de sistemas (Art. 140) y el uso de infraestructuras comunes, garantizando interoperabilidad (Art. 156–157), sedes electrónicas (Art. 38) y actuación automatizada (Art. 41).

### 6.3. RD 203/2021 (Sede Electrónica, PAGe, Carpeta Ciudadana)
!!! note "Definiciones clave"
    * Sede electrónica → Art. 9–12
    * PAGe → punto de acceso general
    * Carpeta Ciudadana → acceso a expedientes
    * AAA (Actuación Automatizada) → Art. 40–42

!!! tip
    Se integrará en la Sede Electrónica conforme al RD 203/2021 garantizando disponibilidad, autenticidad, veracidad y acceso seguro al expediente.

### 6.4. ENI (RD 4/2010) y NTI
!!! note "Principios ENI"
    * Interoperabilidad organizativa
    * Interoperabilidad semántica
    * Interoperabilidad técnica
    * Reutilización
    * Metadatos
    * Formatos abiertos

**NTI más importantes:**

* Documento
* Expediente
* Política de Firma
* Digitalización
* Servicios Web
* Requisitos de Conexión
* Metadatos
* DIR3

!!! tip "Frase tipo"
    El sistema aplicará el ENI garantizando formatos abiertos (PDF/A, XML, ODT), metadatos normalizados y expediente electrónico conforme a NTI de Documento y Expediente.

### 6.5. ENS (RD 311/2022) + Guías CCN-STIC
!!! note "Conceptos clave ENS"
    * Categorización (B–M–A)
    * Principios: prevención, detección, reacción, trazabilidad
    * Auditoría obligatoria
    * Registro de actividad
    * Control de acceso
    * Seguridad por capas

**Guías CCN-STIC recomendables citar:**

* 801 (responsabilidades)
* 804 (implantación)
* 811 (interconexión)
* 408 (perimetral)
* 836 (VPN)

!!! tip "Frase tipo"
    La arquitectura se implementará conforme al ENS aplicando análisis de riesgos, cifrado, control de accesos, registro de actividad y auditoría periódica según guías CCN-STIC.

### 6.6. RGPD + LOPDGDD
!!! note "Puntos clave"
    * Minimización de datos
    * Registro de Actividades de Tratamiento
    * Roles: Responsable / Encargado / DPO
    * Base jurídica 6.1.e
    * EIPD si alto riesgo
    * Seguridad art. 32 RGPD → se materializa con ENS

!!! tip "Frase tipo"
    El tratamiento de datos personales se ajustará al RGPD y LOPDGDD aplicando protección desde el diseño, RAT, contratos con encargados (Art. 28) y medidas técnicas alineadas con el ENS.

## 7. PLANTILLAS DE REFERENCIA
A continuación se muestran plantillas para tenerlas como referencias para poder contestar a las posibles preguntas del supuesto.

### 7.1. Plantilla universal de introducción
1. Cumplimiento legal: Ley 39/2015 + Ley 40/2015
2. Seguridad: ENS + CCN-STIC
3. Interoperabilidad: ENI + NTI aplicables
4. Accesibilidad: RD 1112/2018, WCAG 2.1 AA
5. Protección de datos: RGPD + LOPDGDD
6. Reutilización de servicios comunes (Cl@ve, INSIDE, Notifica…)
7. Infraestructura: despliegue en Nube SARA

### 7.2. Plantilla para Análisis Funcional
1. Contexto del procedimiento
2. Actores (ciudadano, funcionario, sistemas externos)
3. Requisitos funcionales (RF)
4. Requisitos no funcionales (RNF)
5. Casos de uso clave
6. Validaciones y reglas de negocio
7. Integraciones (Cl@ve, Notifica, PID)
8. Seguridad: control acceso + trazabilidad
9. RGPD: minimización + RAT + base jurídica

### 7.3. Plantilla para Arquitectura Lógica (Desarrollo)
1. Arquitectura en 4 capas (Presentación, Negocio, Integración, Datos)
2. Módulos / paquetes
3. API REST (OpenAPI, NTI de Servicios Web)
4. Modelo de datos (conceptual → lógico)
5. Servicios comunes usados
6. Interoperabilidad (ENI + NTI)
7. Seguridad (OWASP + cifrado + sesiones)

### 7.4. Plantilla para Arquitectura Técnica (Sistemas)
1. Infraestructura: Nube SARA / CPD / Híbrido
2. Segmentación: VLANs + firewalls + DMZ
3. Acceso seguro: VPN, MFA, bastionado
4. Disponibilidad: cluster, balanceo, RAID, DRP
5. Almacenamiento: SAN/NAS, cifrado reposo
6. Monitorización: SIEM, logs ENS
7. Seguridad: ENS + CCN-STIC + hardening

## 8. Plantilla de cierre (todas las preguntas)
> La solución se ajusta a la Ley 39/2015, Ley 40/2015, ENI, ENS, RGPD y RD 203/2021, garantizando interoperabilidad, seguridad, accesibilidad y eficiencia mediante el uso de servicios comunes y la infraestructura Nube SARA.