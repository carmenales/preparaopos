# METODOLOGÍA, GESTIÓN DEL PROYECTO Y PLANIFICACIÓN

## 0. Introducción General del Módulo

Este documento recoge todas las estrategias y herramientas relacionadas con:

* Metodologías (Métrica v3, Agile/Scrum, híbridas)
* Modelo de gobierno
* Gestión del cambio
* Migración
* Planificación (cronograma, hitos, ruta crítica)
* Cuadros de mando e indicadores (KPIs)
* Calidad y Plan de Pruebas
* Análisis estratégico (DAFO, FCE)

Todo lo necesario para contestar preguntas transversales de gestión de proyectos TIC en el segundo ejercicio A2.

---

## 1. PLANTILLAS DE INTRODUCCIÓN AL PROYECTO

Las siguientes plantillas son para iniciar cualquier pregunta que hable de: Proyecto, Despliegue, Migración, Modernización, Nuevo sistema, Sustitución de legacy, Implantación, Planificación, Metodología, Gobierno del proyecto.

### 1.1. Plantilla Maestra (Opción recomendada)

> "Para abordar el supuesto planteado, se propone el diseño y despliegue de un sistema de información alineado con la Estrategia TIC de la AGE. El objetivo es [digitalizar / modernizar] el trámite X, garantizando cumplimiento normativo (Ley 39/2015, Ley 40/2015), interoperabilidad (ENI), seguridad (ENS), accesibilidad (RD 1112/2018) y protección de datos (RGPD).
>
> La metodología adoptada combina Métrica v3 para documentación y control, con enfoques ágiles (Scrum) para la entrega incremental. La solución se desplegará sobre infraestructuras de Nube SARA, priorizando la reutilización de servicios comunes y la eficiencia operativa."

!!! tip "Frase tipo"
    *El proyecto se desarrolla bajo un modelo híbrido, equilibrando control formal y agilidad en la ejecución.*

### 1.2. Plantilla Institucional (Plan de Digitalización AAPP 2021–2025)

> "El proyecto se enmarca dentro del Plan de Digitalización de las AAPP 2021–2025 y las líneas estratégicas de España Digital 2026. La propuesta contribuye al fortalecimiento de los servicios públicos digitales mediante la reutilización de infraestructuras, la automatización y la adopción de modelos cloud soberanos como la Nube SARA."

!!! note "Cuándo usarla"
    Úsala si el enunciado menciona modernización, digitalización, PRTR o Next Generation.

### 1.3. Plantilla de Justificación Económica (Artículo 103 CE)

> "Conforme a los principios de eficacia y eficiencia (Art. 103 CE) y a la Ley Orgánica 2/2012 de Estabilidad Presupuestaria, la solución propuesta prioriza la reutilización de servicios comunes (Art. 157 Ley 40/2015), optimizando recursos y asegurando la sostenibilidad económica del proyecto."

!!! tip "Úsala cuando"
    * Hablan de recortes presupuestarios
    * El supuesto menciona optimización, eficiencia, sostenibilidad

---

## 2. METODOLOGÍA DE GESTIÓN Y DESARROLLO

Este apartado cubre todas las preguntas tipo sobre metodología, organización del desarrollo, roles y justificación de enfoques.

### 2.1. Modelo Híbrido (estándar recomendado TIC A2)

!!! note "Por qué modelo híbrido"
    * **Métrica v3** → da formalidad, rigor documental, control.
    * **Agile/Scrum** → da capacidad de adaptación, prototipado, entregas rápidas.
    
    El Tribunal valora positivamente esta combinación.



**Enfoque recomendado:**

* **Métrica v3 para:**
    * Documentación (ASI, DSI)
    * Control de hitos
    * Especificaciones
    * Criterios de aceptación
    * Relación con proveedores
* **Scrum / Agile para:**
    * Construcción iterativa
    * Backlog de requisitos priorizado
    * Sprints de 2–3 semanas
    * Reuniones: planning, daily, review, retro

!!! tip "Frase corta (para examen)"
    *Modelo híbrido: documentación con Métrica v3, ejecución con Scrum.*

!!! warning "Error típico"
    No digas nunca “solo Agile” ni “solo Métrica v3”. Es incoherente con la AGE.

### 2.2. Roles del Proyecto (para cualquier pregunta de gobierno)

Inclúyelos siempre que te pidan estructura organizativa.

* Dirección del Proyecto (propietario funcional)
* Jefe de Proyecto TIC (propietario técnico)
* Product Owner (si usas Agile)
* Scrum Master
* Equipo de Desarrollo
* Equipo de Seguridad / Delegado de Protección de Datos
* Comité de Dirección
* Comité Técnico de Seguimiento

!!! tip "Comités"
    *La existencia de comités es un criterio de calidad y gobierno en proyectos TIC de la AGE.*

### 2.3. Herramientas de Análisis Estratégico (DAFO y FCE)

Estas herramientas deben aparecer SIEMPRE que el supuesto mencione problemas, riesgos, rendimiento, mejora, modernización o contexto inicial.

!!! note "Frase tipo para introducirlo"
    *Se realiza un análisis DAFO para identificar factores internos/externos y orientar la estrategia del proyecto conforme al Art. 3 de la Ley 40/2015 y al ENS.*

---

## 3. JUSTIFICACIÓN DE ARQUITECTURA
(lógica + física — siempre puntúa mucho)

### 3.1. Arquitectura Lógica (Diagrama de Paquetes)

> *Se adopta una Arquitectura en 3/4 Capas que asegura separación de responsabilidades, mantenibilidad y reutilización, siguiendo principios SOLID y buenas prácticas.*



**Capas típicas:**

1.  **Presentación:** Web responsiva / móviles, Accesibilidad RD 1112/2018, UX (Jakob Nielsen).
2.  **Negocio / Dominio:** Reglas, validaciones, servicios, Integración con servicios comunes.
3.  **Integración:** APIs REST, Cliente PID, Notifica, Cl@ve.
4.  **Datos:** JPA / Hibernate, PostgreSQL / Oracle.

!!! tip "Datos"
    Di siempre: “Modelo de Datos conceptual + lógico (JPA/Hibernate)”.

### 3.2. Arquitectura Física (Despliegue ENS + SARA)

> “El despliegue sigue principios de defensa en profundidad del ENS, segmentación de redes y uso de infraestructuras soberanas como Nube SARA.”



* VLANs, firewalls, DMZ
* Red SARA (lote 1 SUT)
* Seguridad perimetral (Guía CCN 408)
* VPN cifrada (Guía CCN 836)
* Sondas SAT-INET (Lazarus)
* Backup, HA, cluster
* Monitorización 24/7 (SIEM + SOC)

!!! warning "Error típico"
    Nunca menciones “AWS”, “Azure” o cloud privada comercial para un organismo AGE.

---

## 4. PLANIFICACIÓN DEL PROYECTO (CRONOGRAMA + HITOS)

### 4.1. Fases del Proyecto (Métrica v3 + enfoque modernizado)

!!! note "Clave de examen"
    Aunque Métrica v3 es antigua, sigue siendo la referencia formal en la AGE. La combinas con Agile para parecer actual y equilibrado.

**Fases completas:**

1.  **EVS — Estudio de Viabilidad del Sistema (Mes 1):** Coste/beneficio, Análisis legal, Alternativas, Riesgos.
2.  **ASI — Análisis del Sistema de Información (Meses 2–3):** Toma de requisitos, RF / RNF, Casos de uso, Modelo de datos conceptual, Actores y sistemas externos.
3.  **DSI — Diseño del Sistema de Información (Mes 4):** Arquitectura lógica, Arquitectura física, Diagrama de despliegue, Modelo de datos físico, Integraciones.
4.  **CSI — Construcción (Meses 5–10):** Desarrollo en Sprints de 2–3 semanas, Testing continuo, Integración CI/CD, Entrega incremental.
5.  **IAS — Implantación y Aceptación (Mes 11):** UAT, Formación, Carga de datos, Paso a producción, Puesta en marcha del CAU, Monitoreo 24/7 (primeras semanas).

!!! tip "Ruta Crítica"
    “La ruta crítica del proyecto recae sobre: construcción, integraciones externas y pruebas.”

### 4.2. Plantilla de cronograma (texto para copiar en examen)

> “El proyecto tendrá una duración estimada de 12 meses.
>
> La planificación se representa en un cronograma tipo Gantt donde se alinean las fases EVS, ASI, DSI, CSI e IAS.
>
> Los hitos principales son:
> 
> * Hito 1 (Mes 3): Validación del Análisis Funcional (ASI).
> * Hito 2 (Mes 6): MVP o piloto funcional para pruebas controladas.
> * Hito 3 (Mes 10): Integraciones externas completas (PID, Notifica, Cl@ve).
> * Hito 4 (Mes 12): Puesta en producción y cierre del proyecto."



!!! example "Ejemplo en estilo del tribunal"
    “En el mes 6 se publica un MVP funcional que permite el registro, consulta básica del expediente y autenticación mediante Cl@ve.”

### 4.3. Cómo justificar la duración del proyecto

!!! tip "Frase brillante de examen"
    “La duración es coherente con proyectos AGE similares, priorizando la entrega temprana (MVP) y la reducción de riesgos mediante ciclos iterativos.”

### 4.4. Ruta crítica (qué poner si te lo piden)

* Integraciones con servicios comunes
* Migración de datos
* Pruebas de aceptación
* Formación
* Hardening + ENS
* Publicación en producción

!!! warning "Error típico"
    No digas nunca que la ruta crítica es “la parte de interfaz”. El tribunal lo penaliza.

---

## 5. GESTIÓN DEL CAMBIO + MIGRACIÓN

### 5.1. Gestión del cambio (Factor humano)

!!! note "Idea clave"
    La resistencia al cambio es el mayor riesgo real de cualquier proyecto TIC.

Incluye siempre estos conceptos:

* Liderazgo único del cambio
* Comunicación y transparencia
* Formación previa a despliegue
* Apoyo institucional como FCE

!!! tip "Frase tipo"
    *El cambio se realiza con las personas, no contra ellas.* Esta frase da muchos puntos.

### 5.2. Fases de la migración técnica

!!! note "Frase para iniciar"
    *La migración no se realiza en Big Bang, sino de forma gradual y controlada.*



1.  **Fase 1 — Preparación y paralelos:** Formación inicial, Entorno de pruebas, Datos anonimizados, Configuración base, Acuerdos con SGAD si se usan Servicios Comunes (Nube SARA).
2.  **Fase 2 — Piloto:** Pequeño grupo de usuarios, Entorno controlado, Validación de procesos clave, Corrección temprana de errores.
3.  **Fase 3 — Migración y coexistencia:** Migración de datos reales, Funcionamiento dual (convivencia), Seguimiento intensivo, Apagado del sistema antiguo.

!!! warning "Error típico"
    Nunca digas *apagado inmediato tras migración*. Penalizan muchísimo no mencionar convivencia.

### 5.3. Plantilla completa para responder Migración

> “La transición se realizará mediante un modelo gradual en tres fases:
> 
> 1. Preparación y paralelos (formación, entornos de prueba),
> 2. Piloto con usuarios reales,
> 3. Migración completa con coexistencia temporal y apagado progresivo.
> 
> Este enfoque minimiza riesgos, reduce la resistencia al cambio y garantiza continuidad del servicio conforme al ENS.”

---

## 6. CALIDAD DEL SOFTWARE Y PLAN DE PRUEBAS

### 6.1. Estándares de calidad ISO 25000 (SQuaRE)

!!! note "ISO 25000"
    Esta norma es ORO puro en examen. Si la mencionas, sumas puntos.



**Dimensiones que debes citar:**

* Adecuación funcional
* Rendimiento / eficiencia
* Compatibilidad
* Usabilidad
* Fiabilidad
* Seguridad
* Mantenibilidad
* Portabilidad

!!! warning "Accesibilidad"
    No olvides citar accesibilidad (RD 1112/2018) como parte de la calidad global.

### 6.2. Plan de Pruebas (QA)

Incluye TODAS estas pruebas; no quites ninguna.

| Tipo | Qué valida | Herramientas típicas |
| :--- | :--- | :--- |
| **Unitarias** | Código | JUnit |
| **Integración** | Módulos | Jenkins (CI) |
| **Sistema** | RF/RNF | Selenium |
| **Carga** | Rendimiento | JMeter |
| **Seguridad** | Vulnerabilidades | SonarQube / OWASP ZAP |
| **Aceptación (UAT)** | Validación usuario | Manuales |

!!! tip "CI/CD"
    *Las pruebas se integran en el pipeline CI/CD para asegurar calidad continua.*

### 6.3. ANS / SLA (Calidad en producción)

**Indicadores estándar:**

* Disponibilidad: 99,9%
* RTO: < 4 h
* Tiempo respuesta: < 2 s

!!! example "Ejemplo"
    *Las operaciones críticas deben restablecerse en menos de 4 horas según SLA.*

---

## 7. CUADROS DE MANDO E INDICADORES (KPIs)

### 7.1. Justificación normativa (siempre citar esto)

!!! note "Normativa"
    La AGE está obligada a evaluar eficacia y calidad del servicio público. Mencionar esto sube nota automáticamente.

**Justificaciones para copiar:**

* **Ley 39/2015 (Art. 13):** derecho a un servicio eficaz y de calidad.
* **Ley 40/2015 (Art. 3):** obligación de evaluar desempeño y resultados.
* **Ley 40/2015 (Art. 81):** sostenibilidad financiera y control de eficacia.
* **ENS (RD 311/2022 — Art. 27):** auditoría continua y revisión de seguridad.
* **NTI de Reutilización:** trazabilidad e indicadores de uso.

!!! tip "Frase de introducción"
    *Se establece un cuadro de mando integral que permite supervisar disponibilidad, rendimiento, seguridad y satisfacción, garantizando el cumplimiento del Art. 3 de la Ley 40/2015 y el Art. 27 del ENS.*

### 7.2. Tabla de KPIs recomendados (memorizar)



| Indicador | Fórmula | Meta | Justificación |
| :--- | :--- | :--- | :--- |
| **Disponibilidad mensual** | Horas activas / Horas totales | ≥ 99,5% | ENS (continuidad del servicio) |
| **Tiempo de respuesta** | Media(ms) | ≤ 250 ms | Ley 40/2015 (eficacia) |
| **Vulnerabilidades críticas** | Nº detectadas - Nº corregidas | 0 | ENS (gestión de riesgos) |
| **Incidentes de seguridad** | Nº incidentes abiertos | ↓ | CCN-STIC 817 |
| **Satisfacción ciudadana** | Encuestas positivas / Total | ≥ 85% | Ley 39/2015 |
| **% tramitación electrónica** | Solicitudes telemáticas / Total | ↑ | Ley 39/2015 Art. 14 |
| **Auditorías realizadas** | Nº auditorías/año | ≥ 1 | ENS Art. 27 |

!!! warning "Error"
    No pongas “tiempo de carga 30 segundos”. El tribunal te suspendería.

### 7.3. Fuentes de datos para el Cuadro de Mando
* Logs de servidores → disponibilidad y errores
* Base de datos → volumen de trámites
* SIEM / SOC → seguridad
* Analytics (web/app) → uso y experiencia
* Encuestas → satisfacción ciudadana

### 7.4. Herramientas de visualización
* **AGE / MINHAFP:** OBSAE, paneles estandarizados
* **Open Source:** Grafana, Kibana, Pentaho
* **No libres:** PowerBI, Tableau

!!! example "Ejemplo"
    *Para monitorización técnica se utilizará Grafana conectado a Prometheus, y para analítica funcional un cuadro de mando con indicadores obtenidos de BBDD + logs.*

### 7.5. Plantilla para responder “defina un cuadro de mando” (copiar en examen)
> *El sistema contará con un Cuadro de Mando Integral que monitoriza rendimiento, disponibilidad, seguridad, tramitación electrónica y satisfacción del usuario. Estos indicadores se revisan de forma mensual y permiten una mejora continua conforme al ENS (Art. 27), a la Ley 40/2015 (evaluación de desempeño) y al principio de eficacia del servicio público.*

---

## 8. ANÁLISIS ESTRATÉGICO (DAFO y FCE)

### 8.1. Introducción normativa (puedes copiarla literal)
> *Con el objetivo de garantizar la viabilidad del proyecto y su alineación con los principios de eficacia y eficiencia administrativa (Art. 103 CE y Ley Orgánica 2/2012), se realiza un análisis estratégico mediante una matriz DAFO. Esta herramienta responde al Art. 3 de la Ley 40/2015, que exige planificación y evaluación, y al ENS, que requiere conocer riesgos y amenazas del entorno.*

!!! tip "Consejo"
    Si citas ENS + Ley 40 juntos → siempre puntúa.

### 8.2. Análisis DAFO — estructura para examen



[Image of SWOT analysis template for IT project]


**A. Análisis Interno (Organización)**

* **Debilidades (ejemplos típicos):** Falta de política de seguridad formal, Falta de inventario de activos, Ausencia de monitorización proactiva, Sistemas legacy, Poca capacitación TIC.
* **Fortalezas:** Equipo técnico capacitado, Infraestructura consolidada, Dirección comprometida, Integración previa con servicios comunes.

**B. Análisis Externo (Entorno)**

* **Amenazas:** Incremento de ciberataques, Brechas RGPD → impacto reputacional, Actualizaciones normativas constantes (ENS 2022), Presión presupuestaria.
* **Oportunidades:** Fondos europeos (PRTR), Adopción de servicios comunes, Red SARA disponible, Modernización impulsada por España Digital 2026.

!!! tip "Frase para brillar"
    *Las oportunidades permiten impulsar reutilización, reducción de costes y mejora del servicio público.*

### 8.3. Ejemplo DAFO completo (puedes copiar y adaptar)

| Debilidades | Fortalezas |
| :--- | :--- |
| Falta política seguridad ENS | Equipo TIC especializado |
| Sistemas obsoletos | Infraestructura con firewall |
| Sin inventario de activos | Integración con Cl@ve, Registro |

| Amenazas | Oportunidades |
| :--- | :--- |
| Ciberataques (DDoS, ransomware) | Fondos Next Generation |
| Riesgo RGPD | Servicios Comunes |
| Cambios normativos | Colaboración AA.PP. |

### 8.4. Factores Críticos de Éxito (FCE) — lo que el tribunal quiere ver
* Apoyo institucional
* Gestión del cambio eficaz
* Interoperabilidad real
* Alta disponibilidad (Nube SARA)
* Ciberseguridad ENS + CCN-STIC
* Datos de calidad + migración correcta

!!! warning "Ojo"
    No confundas FCE con requisitos o RF/RNF. Los FCE son condiciones imprescindibles para que el proyecto no fracase.

### 8.5. Plantilla DAFO lista para examen
* **Introducción:** “Se realiza un análisis DAFO alineado con la planificación estratégica exigida por la Ley 40/2015 y el análisis de riesgos del ENS.”
* **Desarrollo (3–4 ítems por cuadrante):** Debilidades: X, Y, Z; Amenazas: X, Y, Z; Fortalezas: X, Y, Z; Oportunidades: X, Y, Z.
* **Cierre:** “El análisis permite identificar riesgos clave y orientar decisiones alineadas con ENS, Ley 39/2015 y NTI.”

---

## 9. MODELO DE GOBIERNO DEL PROYECTO



### 9.1. Principios del modelo de gobierno
!!! note "Institucionalidad"
    La AGE exige gobierno formal, comités y roles definidos. No basta con “Scrum”. Hay que mostrar “institucionalidad”.

**Principios clave:**

* Transparencia
* Responsabilidad clara
* Toma de decisiones estructurada
* Supervisión continua (Art. 3 Ley 40/2015)
* Gestión de riesgos y calidad
* Alineación con estándares (ENS, ENI, NTI)

### 9.2. Estructura del modelo de gobierno
La más valorada por el tribunal es esta:

1.  **Alta Dirección (nivel estratégico):** Define visión, objetivos, presupuesto y aprobación final.
2.  **Comité de Dirección del Proyecto:** Se reúne mensualmente. Participan: Dirección del organismo, Jefe Proyecto TIC, Jefe Proyecto Funcional, Seguridad, Jurídico, Representante DPO. Funciones: Validar hitos, Revisar riesgos, Aprobar entregables clave.
3.  **Comité Técnico de Seguimiento (nivel táctico):** Reuniones semanales o quincenales. Participantes: Jefe proyecto TIC, PO (si Agile), Arquitecto, Líder de desarrollo, Responsable de Seguridad ENS. Funciones: Seguimiento del cronograma, Análisis de incidencias, Revisión de calidad, Prioridad del backlog.
4.  **Equipos Operativos (nivel operativo):** Desarrolladores, QA, soporte técnico, responsables ENS/DPD.

!!! tip "Frase tipo"
    *El proyecto se gobierna mediante comités estratégicos y técnicos, asegurando control institucional, trazabilidad y cumplimiento ENS.*

---

## 10. GESTIÓN DE RIESGOS

### 10.1. Justificación normativa
!!! note "Relación"
    Riesgos siempre debe relacionarse con:

    * ENS (análisis de riesgos + categorización)
    * Ley 40/2015 Art. 3 (eficacia y planificación)

### 10.2. Lista de riesgos típicos (memorizables)
* Resistencia al cambio
* Retrasos en integraciones externas (Cl@ve, PID, Notifica)
* Mala calidad de datos en origen
* Subestimación del esfuerzo de pruebas
* Problemas de rendimiento en picos de carga
* Falta de documentación en sistemas legacy
* Dependencia de proveedores externos
* Brechas de seguridad o ataques
* Sobrecostes / ampliación de alcance (scope creep)

### 10.3. Matriz Riesgo → Mitigación (para sacar sobresaliente)

| Riesgo | Mitigación |
| :--- | :--- |
| Resistencia al cambio | Plan de formación + piloto + convivencia |
| Datos de mala calidad | ETL + limpieza previa + pruebas de migración |
| Retraso integraciones | Mock + pruebas tempranas + entorno pre-producción |
| Ataques o brechas ENS | Hardening + pentesting + SIEM/SOC 24/7 |
| Baja disponibilidad | HA + cluster + balanceo |
| Sobrecostes | Gestión del alcance + control en comités |

!!! example "Ejemplo"
    *Para integraciones con Cl@ve/PID/Notifica se realiza un Mock de pruebas para evitar retrasos críticos.*

---

## 11. INTEGRACIÓN VERTICAL DEL PROYECTO
(cómo conectar requisitos → arquitectura → despliegue → pruebas → KPIs)

### 11.1. La cadena de trazabilidad recomendada
1.  **Análisis (ASI):** → RF / RNF → Casos de uso
2.  **Diseño (DSI):** → Arquitectura lógica → Arquitectura física → Integraciones
3.  **Construcción (CSI):** → Desarrollo iterativo → Automatización CI/CD → Pruebas continuas
4.  **Implantación (IAS):** → Migración → Formación → Despliegue → Producción
5.  **Explotación:** → KPIs → SLA → Auditorías ENS → Evolutivos

!!! tip "Coherencia"
    *La trazabilidad vertical garantiza coherencia, control y cumplimiento normativo.*

### 11.2. Plantilla para responder coherencia del proyecto
> *El proyecto mantiene trazabilidad completa entre requisitos (RF/RNF), arquitectura (capas e integraciones), construcción (desarrollo iterativo), pruebas (plan QA), implantación (migración) y explotación (KPIs y ENS), garantizando un ciclo de vida coherente en todas sus fases.*

---

## 12. PLANTILLAS DE REDACCIÓN (versión corta, media y larga)

### 12.1. Plantilla corta (para preguntas de 2–3 minutos)
> *La gestión del proyecto sigue un modelo híbrido (Métrica v3 + Scrum), con gobierno mediante Comités de Dirección y Técnico.*
>
> *La planificación se estructura en las fases EVS, ASI, DSI, CSI e IAS, con un piloto en el mes 6 y puesta en producción en el mes 12.*
>
> *La transición se realiza en piloto + convivencia, garantizando continuidad.*
>
> *La calidad se asegura mediante pruebas unitarias, integración, sistema y carga; y explotación mediante KPIs de disponibilidad, tiempo de respuesta y seguridad.*

### 12.2. Plantilla media
> *El proyecto se gestiona mediante un modelo híbrido que combina la documentación formal de Métrica v3 con la ejecución iterativa mediante Scrum. El gobierno se articula mediante Comités Estratégicos y Técnicos que validan hitos, riesgos y entregables.*
>
> *La planificación incluye un piloto funcional (MVP) y un plan de migración gradual con convivencia. La calidad se garantiza aplicando ISO 25000, pruebas funcionales y técnicas (Selenium, JMeter, SonarQube), y se controla en explotación mediante un Cuadro de Mando conforme a Art. 3 Ley 40/2015 y Art. 27 ENS.*

### 12.3. Plantilla larga (para sacar matrícula)
> *El proyecto se gestiona mediante un modelo híbrido (Métrica v3 + Scrum) que equilibra control institucional y capacidad de adaptación.*
>
> *La gobernanza se estructura en Comités Estratégicos y Técnicos, con roles formalmente definidos (Dirección, Jefe de Proyecto TIC, Product Owner, Delegado de Protección de Datos, Responsable ENS).*
>
> *La planificación cubre las fases EVS, ASI, DSI, CSI e IAS, con un piloto funcional en el mes 6 y ruta crítica centrada en integraciones y pruebas.*
>
> *La migración se realiza en fases (preparación, piloto, convivencia), minimizando riesgos y garantizando continuidad del servicio.*
>
> *La calidad se asegura mediante ISO 25000, ITIL para explotación, un plan de pruebas completo (unitarias, integración, sistema, rendimiento, seguridad), y SLAs exigentes (99,9% disponibilidad, RTO < 4h).*
>
> *En explotación, el cuadro de mando integra indicadores de rendimiento, seguridad, satisfacción y cumplimiento ENS.*
>
> *Este enfoque garantiza un ciclo de vida coherente, seguro, accesible y alineado con los principios de Legalidad, Eficacia y Eficiencia de la Ley 39/2015 y 40/2015.*

---

## 13. CHECKLISTS PROFESIONALES
(lo que debes revisar SIEMPRE antes de cerrar una respuesta de gestión)

### 13.1. Checklist de Metodología
* [x] ¿Has mencionado Métrica v3?
* [x] ¿Has mencionado Scrum/Agile para iteraciones?
* [x] ¿Has citado por lo menos 2 reuniones de Scrum? (Daily, Review, Retro)
* [x] ¿Has incluido gobernanza formal (comités)?
* [x] ¿Has vinculado metodología con control de calidad?
* [x] ¿Has añadido “modelo híbrido” (se puntúa mucho)?

!!! tip "Consejo"
    Con escribir “modelo híbrido: Métrica v3 + Scrum” ya sumas.

### 13.2. Checklist de Planificación
* [x] ¿Has mencionado EVS, ASI, DSI, CSI e IAS?
* [x] ¿Has puesto duración estimada?
* [x] ¿Has incluido piloto/MVP?
* [x] ¿Has citado ruta crítica?
* [x] ¿Has indicado Hito 1, Hito 2…?
* [x] ¿Has mencionado integración con servicios comunes como riesgo?
* [x] ¿Has vinculado planificación con metodología Agile?

### 13.3. Checklist de Migración / Cambio
* [x] ¿Has dicho “no Big Bang”?
* [x] ¿Has mencionado funcionamiento dual / convivencia?
* [x] ¿Has puesto piloto previo?
* [x] ¿Has puesto formación de usuarios?
* [x] ¿Has descrito fases de migración?
* [x] ¿Has dado un cierre “apagado progresivo”?

!!! warning "Aviso"
    Si no mencionas convivencia, el tribunal te baja puntos.

### 13.4. Checklist de Calidad (ISO 25000 + QA)
* [x] ¿Has citado la norma ISO/IEC 25000?
* [x] ¿Has diferenciado RF y RNF?
* [x] ¿Has citado Pruebas unitarias, Integración, Sistema, Carga, Seguridad, UAT?
* [x] ¿Has hablado de CI/CD?
* [x] ¿Has mencionado SLA (99,9% disponibilidad)?

### 13.5. Checklist de KPIs (Cuadro de Mando)
* [x] ¿Has incluido al menos 5 KPIs clásicos?
* [x] ¿Has citado Art. 3 Ley 40/2015 (eficacia)?
* [x] ¿Has citado ENS (Art. 27)?
* [x] ¿Has incluido seguridad y satisfacción ciudadana?
* [x] ¿Has indicado tendencia (↑ / ↓)?

### 13.6. Checklist de Gobierno
* [x] ¿Has creado Comité de Dirección?
* [x] ¿Has creado Comité Técnico?
* [x] ¿Has definido roles?
* [x] ¿Has indicado periodicidad de reuniones?
* [x] ¿Has vinculado gobierno con planificación?

---

## 14. ERRORES QUE SUSPENDEN (IMPORTANTE)

Léelos cada vez que redactes una pregunta de este módulo.

### 14.1. Errores de metodología
!!! danger "No mencionar Métrica v3"
    Error grave: te descuentan.
!!! danger "Decir que solo usarías Agile"
    Inviable en AGE. Proyecto mal gobernado.

### 14.2. Errores de planificación
!!! danger "Poner cronograma sin piloto"
    Se interpreta como falta de iteración y control.
!!! danger "Decir “duración 3 meses” para un sistema complejo"
    No es creíble, te baja nota.

### 14.3. Errores de migración
!!! danger "Big Bang (migración instantánea)"
    ALTAMENTE penalizado.
!!! danger "No mencionar convivencia"
    Suspenso automático.

### 14.4. Errores de calidad
!!! danger "Olvidar pruebas de carga o seguridad"
    Error crítico.
!!! danger "No mencionar ISO 25000 cuando te piden calidad"
    Pérdida de puntos enorme.

### 14.5. Errores de KPIs
!!! danger "No citar Art. 3 Ley 40/2015"
    Pierdes obligatorio de “evaluación del desempeño”.
!!! danger "No incluir indicadores de seguridad ENS"
    Baja técnica asegurada.

---

## 15. FRASES PROHIBIDAS (NUNCA LAS PONGAS)

Estas frases hacen que el tribunal perciba que no conoces la AGE:

* *Usaremos AWS/Azure/Google Cloud porque son más baratas.*
* *Se hará todo en Agile porque es más rápido.*
* *Se apagará el sistema antiguo tras la migración.*
* *No hacen falta pruebas de seguridad.*
* *El sistema tendrá disponibilidad del 100%.*
* *Se eliminarán los trámites presenciales* (no puedes afirmarlo tú)
* *El sistema almacenará DNI/contraseñas en claro.*

!!! warning "Aviso"
    Si pones una de estas frases, literalmente te restan nota.

---

## 16. FRASES QUE HACEN QUE PUNTÚES ALTO

Estas frases te hacen parecer experta real.

* *Se prioriza la reutilización de servicios comunes conforme a la Ley 40/2015 Art. 157.*
* *Modelo híbrido: Métrica v3 + Scrum, entregas iterativas y rigor documental.*
* *Se aplica un plan de migración gradual según ENS, evitando Big Bang.*
* *El ENS exige análisis, prevención, detección, reacción y recuperación.*
* *La accesibilidad se garantiza mediante RD 1112/2018 y WCAG 2.1 AA.*
* *El sistema se desplegará sobre la Nube SARA por soberanía y eficiencia.*
* *Se utilizan KPIs alineados con Art. 3 Ley 40/2015.*
* *La calidad sigue ISO 25000 e integra pruebas de rendimiento y seguridad.*
* *Las integraciones con Cl@ve, PID y Notifica se realizan con pruebas tempranas (Mock).*
* *La trazabilidad vertical garantiza coherencia del ciclo de vida.*

---

## 17. LIBRETO DE RESPUESTAS RÁPIDAS (copiar y pegar)

* **Si te piden metodología:** *Modelo híbrido: Métrica v3 para control y Scrum para entregas iterativas.*
* **Si te piden planificación:** *Planificación en fases EVS–ASI–DSI–CSI–IAS con piloto en mes 6 y producción en mes 12.*
* **Si te piden migración:** *Migración gradual con piloto, convivencia y apagado progresivo.*
* **Si te piden riesgos:** *Riesgos: resistencia al cambio, datos de mala calidad, integraciones externas y seguridad.*
* **Si te piden calidad:** *Calidad conforme ISO 25000 + pruebas unitarias, integración, sistema, carga y seguridad.*
* **Si te piden KPIs:** *KPIs: disponibilidad, tiempo de respuesta, vulnerabilidades, incidentes, satisfacción ciudadana.*
* **Si te piden gobierno:** *Gobierno mediante Comités de Dirección y Técnico para validar hitos y gestionar riesgos.*

---

## 18. CIERRE PROFESIONAL PARA CUALQUIER RESPUESTA
(Utilízalo para terminar cualquier pregunta del examen sin pensar)

### Plantilla de cierre estándar (para casi todo)
> *En conclusión, la solución propuesta garantiza un proyecto técnicamente viable, seguro y alineado con el marco legal de la AGE. La metodología híbrida (Métrica v3 + Scrum) asegura rigor documental y entregas iterativas.*
>
> *La planificación y la gestión del cambio permiten una implantación sin interrupciones.*
>
> *La calidad se garantiza mediante ISO 25000 y un plan completo de pruebas, y la supervisión continua se realiza mediante KPIs alineados con ENS y Ley 40/2015.*
>
> *Todo ello asegura interoperabilidad, accesibilidad, eficiencia y sostenibilidad del servicio público.*

### Versión corta para ahorrar tiempo
> *La propuesta cumple Ley 39/2015, Ley 40/2015, ENS, ENI y RGPD; se gestiona con modelo híbrido Métrica v3 + Scrum, planificación EVS–ASI–DSI–CSI–IAS, migración gradual, calidad ISO 25000 y KPIs conforme Art. 3 Ley 40/2015.*

### Versión ultra-rápida (para preguntas con poco espacio)
> *Modelo híbrido + ENS + ENI + RGPD + Migración gradual + ISO 25000 + KPIs legales.*

---

## 19. RESUMEN VISUAL (LO QUE TIENES QUE RECORDAR)

**Metodología**

* Métrica v3 para documentación
* Scrum para construcción
* Iteraciones cada 2–3 semanas
* Comités: Dirección + Técnico

**Planificación**

* EVS → ASI → DSI → CSI → IAS
* Piloto en mes 6
* Producción mes 12
* Ruta crítica en Integraciones

**Migración**

* Nunca Big Bang
* Piloto → Convivencia → Apagado
* Formación previa
* Migración de datos controlada

**Calidad (ISO 25000)**

* Pruebas unitarias, Integración, Sistema, Carga, Seguridad, UAT

**KPIs**

* Disponibilidad, T. respuesta, Vulnerabilidades, Incidentes, Tasa de tramitación, Satisfacción

**Gobierno**

* Comité Dirección, Comité Técnico, Gestión de riesgos, Informes quincenales