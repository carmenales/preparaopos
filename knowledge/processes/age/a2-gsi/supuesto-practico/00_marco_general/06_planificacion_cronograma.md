# 06. PLANIFICACIÓN DEL PROYECTO (CRONOGRAMA)

La planificación es una de las partes que más puntúa en el examen del supuesto práctico. El tribunal valora tres cosas:
* **Estructura:** Que uses fases formales (Métrica v3).
* **Razonamiento:** Que justifiques ruta crítica, hitos y dependencias.
* **Narrativa:** Que lo escribas como un jefe de proyecto de la AGE.

---

## 1. JUSTIFICACIÓN NORMATIVA Y METODOLÓGICA

!!! note "Por qué es obligatorio planificar"
    * La Ley 40/2015 (Art. 3) exige eficacia, eficiencia y planificación.
    * El ENS (RD 311/2022) exige control y trazabilidad de todo el ciclo de vida.
    * Métrica v3 es la metodología estándar en la AGE y la base para el tribunal.

!!! tip "Frase tipo para el examen"
    “La planificación del proyecto se estructura según las fases de Métrica v3, garantizando trazabilidad, control de riesgos y cumplimiento de la Ley 40/2015 en materia de eficacia y buena administración.”

## 2. FASES DEL PROYECTO (MÉTRICA V3)

!!! note "Las 5 fases que siempre debes memorizar"
    EVS → ASI → DSI → CSI → IAS
    (Si respondes esto, siempre puntúas.)



[Image of Métrica v3 project phases flow chart]


A continuación, la explicación ampliada:

### 2.1. EVS — Estudio de Viabilidad del Sistema
* **Duración orientativa:** 1 mes
* **Objetivos:**
    * Determinar si el proyecto es viable técnica, económica y legalmente.
    * Evaluar alternativas (reutilización de servicios comunes).
    * Estimar presupuesto y recursos.

!!! tip "Frase tipo"
    “La EVS analiza costes/beneficios, riesgos y cumplimiento normativo, determinando si el sistema cumple Ley 39/2015, 40/2015, ENS y ENI.”

### 2.2. ASI — Análisis del Sistema de Información
* **Duración orientativa:** 2–3 meses
* **Resultados clave:**
    * Actores
    * Casos de Uso
    * RF/RNF
    * Modelo Conceptual de Datos
    * Integraciones (Cl@ve, Notifica, PID…)

!!! example "Frase para examen"
    “En la fase ASI se definen los requisitos funcionales y no funcionales, así como la arquitectura lógica preliminar y el modelo conceptual ENI.”

### 2.3. DSI — Diseño del Sistema de Información
* **Duración:** 1 mes
* **Entregables:**
    * Arquitectura lógica (4 capas)
    * Arquitectura técnica (VLAN, VPN, FW)
    * Diagrama de Despliegue
    * Modelo físico de datos

!!! note "Importante"
    Aquí debes justificar ENS (seguridad), ENI (metadatos/expediente) y servicios comunes.

### 2.4. CSI — Construcción del Sistema
* **Duración:** 6 meses (sprints Agile)
* **Componentes:**
    * Programación
    * Integración continua
    * Contenedores o microservicios
    * Pruebas unitarias + integración
    * Repositorio de código

!!! tip "Frase tipo"
    “La construcción se realiza mediante Sprints de 2–3 semanas siguiendo un marco Scrum que garantiza entregas incrementales y control del cambio.”

### 2.5. IAS — Implantación y Aceptación
* **Duración:** 1 mes
* **Incluye:**
    * Migración → plan en convivencia
    * Carga de datos
    * UAT (pruebas funcionales con usuarios)
    * Puesta en producción
    * Revisión post-implantación

!!! example "Cierre de Fase"
    “La fase IAS culmina con la puesta en producción supervisada y la firma del acta de conformidad por el órgano responsable.”

## 3. CRONOGRAMA TIPO (12 MESES)

!!! note "Cronograma estándar que puedes copiar en el examen"
    | Mes | Fase |
    | :--- | :--- |
    | **Mes 1** | EVS |
    | **Mes 2–3** | ASI |
    | **Mes 4** | DSI |
    | **Mes 5–10** | CSI (Sprints 1–10) |
    | **Mes 11** | IAS |
    | **Mes 12** | Estabilización + cierre |

### 3.1. Ruta Crítica

!!! warning "Esto lo olvidan y da puntos extra"
    Identifica la dependencia crítica del proyecto.
    Normalmente es:
    * Integración con Servicios Comunes
    * Disponibilidad de requisitos
    * Migración de datos

!!! tip "Frase tipo"
    “La ruta crítica recae en la integración con PID, Notifica y Cl@ve, ya que determina la validación completa del flujo del procedimiento.”

### 3.2. Hitos del Proyecto (Ejemplo perfecto)
* **Hito 1 (Mes 3):** Aprobación del ASI.
* **Hito 2 (Mes 6):** MVP funcional (Registro + Expediente).
* **Hito 3 (Mes 10):** Integraciones externas completas.
* **Hito 4 (Mes 12):** Producción y cierre.

!!! tip "Estrategia"
    Si siempre pones 4 hitos, te llevas el punto.

## 4. DIAGRAMA GANTT (VERSIÓN PARA EXAMEN SIN DIBUJAR)



!!! example "Frase lista para copiar"
    “El Gantt del proyecto se organiza en bloques de ejecución secuenciales (EVS–ASI–DSI) y bloques iterativos (CSI). Se identifican hitos clave, ruta crítica y dependencias, garantizando una planificación conforme a Métrica v3 y los principios de eficacia de la Ley 40/2015.”

## 5. GESTIÓN DE RIESGOS (EXTRA PARA «MÁXIMA NOTA»)

!!! note "Tres riesgos que siempre puedes poner"
    * Retraso en la obtención de requisitos.
    * Fallos en integraciones externas.
    * Resistencia al cambio del usuario.

!!! tip "Cómo responder"
    “Se realiza seguimiento semanal, matriz de riesgos (probabilidad $\times$ impacto) y medidas preventivas, conforme ENS (gestión de riesgos).”

## 6. PLANTILLA DE RESPUESTA (LISTA PARA COPIAR EN EL EXAMEN)

**Introducción:**
> “La planificación del proyecto se estructura según las fases de Métrica v3, garantizando control, trazabilidad y eficacia conforme a la Ley 40/2015.”

**Desarrollo:**
* EVS (Mes 1)
* ASI (Meses 2–3)
* DSI (Mes 4)
* CSI + Sprints (Meses 5–10)
* IAS + Migración (Mes 11)

**Cierre:**
> “La ruta crítica recae en integraciones y migración. Se establecen hitos claros y un Gantt estructurado, garantizando una implantación segura conforme ENS y ENI.”

## 7. CIERRE PROFESIONAL
> “La planificación propuesta asegura viabilidad técnica, control de riesgos y ejecución eficiente del servicio público, conforme a Métrica v3, ENS y los principios de eficacia de la Ley 40/2015.”