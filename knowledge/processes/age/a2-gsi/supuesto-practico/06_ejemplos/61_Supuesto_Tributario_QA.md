# SUPUESTO PRÁCTICO Q&A: GESTIÓN TRIBUTARIA Y CONTRATACIÓN

Este supuesto muestra cómo responder a un examen estructurado en **preguntas independientes**, incluyendo la justificación de la **contratación pública** (LCSP).

---

## ENUNCIADO GENERAL
**Contexto:** La Dirección General de Gestión Tributaria desea desarrollar una plataforma web y móvil para:

* Presentación telemática de declaraciones.
* Notificaciones electrónicas y pago telemático.
* Integración con: Cl@ve, Registro, Pasarela de Pagos, PID.

**Modelo de ejecución:** Desarrollo por empresa externa, supervisión interna.

---

## PREGUNTA 1: MODELO DE ANÁLISIS FUNCIONAL (CASOS DE USO)

**Enunciado:** *Diseñe un modelo de análisis funcional apoyado en UML que represente las funcionalidades principales.*

### RESPUESTA MODELO

**1. Enfoque**
Se realiza un diagrama de casos de uso de alto nivel para representar a los actores externos, las funcionalidades del sistema y las integraciones con servicios comunes.

**2. Identificación de Actores**

* **Humanos:** Ciudadano (Contribuyente), Funcionario Gestor.
* **Sistemas (Actores de Servicio):** Sistema Cl@ve, Registro Electrónico, Pasarela de Pagos, Plataforma de Intermediación (PID).

**3. Casos de Uso Principales**

* **Autenticación:** `Autenticarse mediante Cl@ve` (Sustancial/Alto).
* **Tramitación:** `Presentar declaración`, `Anexar documentación`.
* **Económico:** `Realizar pago telemático` (Integración con PAGe).
* **Consulta:** `Consultar expediente`, `Recibir notificaciones` (DEHú).
* **Gestión:** `Validar datos tributarios` (vía PID), `Registrar presentación`.

**4. Justificación Normativa**

* **Ley 39/2015 (Art. 9-11):** Uso de Cl@ve para identificación y firma.
* **Ley 39/2015 (Art. 14):** Garantía del derecho a la tramitación electrónica.
* **ENI:** El intercambio estructurado se ajusta a las NTI de interoperabilidad.



---

## PREGUNTA 2: DIAGRAMA DE SECUENCIA (PAGO TELEMÁTICO)

**Enunciado:** *Realice un diagrama de secuencia que represente el flujo de presentación con pago.*

### RESPUESTA MODELO

**1. Flujo de la Secuencia**

1.  **Ciudadano** → `Sistema`: Solicita inicio de trámite.
2.  `Sistema` → **Cl@ve**: Redirección para validación de identidad.
3.  **Ciudadano** → `Sistema`: Cumplimenta declaración.
4.  `Sistema` → **PID**: Validación automática de datos (ej. Deuda pendiente).
5.  `Sistema` → **Pasarela Pagos (PAGe)**: Solicitud de cargo en cuenta/tarjeta.
6.  **PAGe** → `Sistema`: Confirmación (NRC/Justificante pago).
7.  `Sistema` → **Registro Electrónico**: Generación de asiento registral.
8.  `Sistema` → **Ciudadano**: Entrega de Justificante registrado con CSV.

**2. Normativa Aplicada**

* **ENS (Integridad):** Verificación automática de datos para evitar errores.
* **NTI Registro:** Anotación automática del asiento registral.
* **Ley 39/2015 (Art. 53):** Derecho a obtener copia de los documentos presentados.



---

## PREGUNTA 3: MEDIDAS DE SEGURIDAD (ENS)

**Enunciado:** *Defina las medidas de seguridad ENS aplicables, separando lógicas y físicas.*

### RESPUESTA MODELO

**1. Categorización ENS**
Al tratar datos tributarios y personales, el sistema requiere un nivel de protección elevado:

* **Confidencialidad:** ALTA (Datos tributarios).
* **Disponibilidad:** ALTA (Servicio crítico en periodos de campaña).
* **Integridad/Trazabilidad:** MEDIA/ALTA.

**2. Medidas de Seguridad Lógica**

| Medida | Código ENS | Aplicación Práctica |
| :--- | :--- | :--- |
| **Autenticación** | **[op.acc.6]** | Uso de **Cl@ve** (nivel reforzado) y certificados cualificados. |
| **Trazabilidad** | **[op.exp.8]** | Registro de actividad completo para auditorías. |
| **Vulnerabilidades** | **[op.ges.6]** | Gestión de parches y escaneos periódicos. |
| **Desarrollo** | **[mp.sw.1]** | Ciclo de vida seguro (DevSecOps) y análisis de código. |

**3. Medidas de Seguridad Física**

| Medida | Código ENS | Aplicación Práctica |
| :--- | :--- | :--- |
| **Control Acceso** | **[mp.if.1]** | Tarjetas/biometría para acceso al CPD. |
| **Energía** | **[mp.eq.2]** | Alimentación ininterrumpida (SAI + Grupo Electrógeno). |
| **Contingencia** | **[op.cont]** | CPD de respaldo o despliegue en zonas de disponibilidad distintas (Nube SARA). |

---

## PREGUNTA 4: DIAGNÓSTICO ESTRATÉGICO (DAFO)

**Enunciado:** *Realice un diagnóstico DAFO y proponga medidas de mejora normativas.*

### RESPUESTA MODELO

**1. Matriz DAFO**

* **Fortalezas:** Integración con Servicios Comunes (Ley 40/2015) y personal TIC cualificado.
* **Debilidades:** Monitorización reactiva y falta de Cuadro de Mando.
* **Oportunidades:** Fondos europeos (NextGen) y migración a Nube Híbrida.
* **Amenazas:** Ciberataques (DDoS) y riesgo reputacional.

**2. Medidas de Mejora (Propuesta)**

1.  **Gestión:** Implantar Cuadro de Mando TIC (Cumplimiento de Ley 40/2015, Dirección por Objetivos).
2.  **Operación:** Implementar monitorización proactiva (Sondas CCN) según ENS.
3.  **Gobierno:** Formalizar y publicar la Política de Seguridad (Requisito ENS).
4.  **Arquitectura:** Mejorar la escalabilidad horizontal del frontend (Principio de Disponibilidad).

---

## PREGUNTA 5: CONTRATACIÓN Y OBLIGACIONES (LCSP)

**Enunciado:** *Justifique el modelo de contratación y las obligaciones de la empresa adjudicataria.*

### RESPUESTA MODELO

**1. Modalidad de Contratación**
Se propone un **Contrato de Servicios** para el desarrollo y mantenimiento evolutivo.

* *Justificación:* Permite la adaptación a cambios normativos constantes (Tributarios) y el control funcional por parte de la Administración.

**2. Obligaciones de la Adjudicataria**

* **A) Ley de Contratos (LCSP):**

    * Cumplimiento estricto de plazos y calidad (SLA).
    * Prohibición de subcontratación no autorizada.
    * **Propiedad Intelectual:** Entrega del código fuente y documentación a la Administración (para garantizar la independencia tecnológica).

* **B) Protección de Datos (RGPD):**

    * La empresa actúa como **Encargado del Tratamiento** (Art. 28 RGPD).
    * Obligación de confidencialidad, no uso de datos para otros fines y destrucción/devolución al finalizar el contrato.

* **C) Seguridad (ENS):**

    * Obligación de cumplir la Política de Seguridad del organismo.
    * Deber de notificar incidentes de seguridad de forma inmediata (**[op.ges.4]**).
    * Someterse a auditorías de calidad y seguridad.

---

## CONCLUSIÓN DEL SUPUESTO
La solución propuesta es:

1.  **Legal:** Cumple Ley 39/40 y RGPD.
2.  **Segura:** Aplica ENS Nivel Alto.
3.  **Eficiente:** Reutiliza servicios (Cl@ve, PID) y define un modelo de contratación sostenible.