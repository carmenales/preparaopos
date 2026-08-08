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
tags:
  - "analisis-no-funcional"
  - "rendimiento"
  - "seguridad"
  - "privacidad"
  - "metrica-v3"
  - "ens"
  - "rgpd"
  - "iso-25010"
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

Mientras que los requisitos funcionales definen **qué** hace el sistema, los Requisitos No Funcionales (RNF) definen **cómo** lo hace. Son atributos de calidad y restricciones impuestas al sistema [cite: 3]. Si no se cumplen, el sistema fracasa aunque la funcionalidad central haga su trabajo. La identificación de estos requisitos forma parte de las tareas clave de la Ingeniería de Requerimientos [cite: 3].

El estándar de referencia para clasificar y evaluar los RNF es la norma **ISO/IEC 25010** (SQuaRE — *System and Software Quality Requirements and Evaluation*), sucesora de la antigua ISO/IEC 9126. Define **8 características de calidad de producto software**: idoneidad funcional, **eficiencia de desempeño** (rendimiento), compatibilidad, usabilidad, fiabilidad, **seguridad**, mantenibilidad y portabilidad. La privacidad no aparece como característica independiente en la versión 2011 de la norma, sino como subcaracterística de seguridad; en la revisión ISO/IEC 25010:2023 se eleva a característica propia, reflejando su creciente importancia normativa (RGPD).

### 1.1. Rendimiento (Performance)
Define las métricas operativas del sistema bajo una carga de trabajo determinada.
**Patrón Lógico - Métricas Clave:**
*   **Tiempo de respuesta:** Lo que tarda el sistema en reaccionar a una petición del usuario (ej. milisegundos en cargar una pantalla o procesar un pago).
*   **Throughput (Rendimiento de procesamiento):** Número de transacciones o peticiones que el sistema puede procesar por unidad de tiempo (ej. 1000 transacciones por segundo).
*   **Escalabilidad:** Capacidad del sistema para manejar más carga añadiendo recursos (Escalabilidad vertical: añadir más RAM/CPU a un servidor; Escalabilidad horizontal: añadir más servidores al clúster).
*   **Consumo de recursos:** Límites en el uso de memoria, procesador y ancho de banda de red.

Según ISO/IEC 25010, la característica *Performance efficiency* se descompone en tres subcaracterísticas que conviene memorizar literalmente: **Comportamiento temporal** (*time behaviour* — tiempos de respuesta, procesamiento y throughput), **Utilización de recursos** (*resource utilization* — cantidad y tipo de recursos usados) y **Capacidad** (*capacity* — límites máximos que puede soportar un parámetro, ej. número máximo de usuarios concurrentes).

La validación del rendimiento se realiza mediante **pruebas no funcionales de carga**, que conviene distinguir bien porque suelen confundirse en examen:
*   **Pruebas de carga (*load testing*):** comprueban el comportamiento del sistema bajo el volumen de trabajo esperado en condiciones normales o en el máximo previsto.
*   **Pruebas de estrés (*stress testing*):** llevan al sistema por encima de su capacidad máxima para identificar el punto de ruptura y cómo se degrada o recupera.
*   **Pruebas de resistencia (*endurance/soak testing*):** verifican el comportamiento del sistema bajo carga sostenida durante un periodo prolongado, detectando fugas de memoria o degradación progresiva.
*   **Pruebas de picos (*spike testing*):** valoran la reacción del sistema ante incrementos súbitos y muy bruscos de carga.

En el ámbito contractual y de servicios TIC, los compromisos de rendimiento suelen fijarse mediante **Acuerdos de Nivel de Servicio (SLA — *Service Level Agreement*)**, que establecen umbrales concretos (ej. disponibilidad del 99,9%, tiempo de respuesta máximo de 2 segundos) y penalizaciones si no se cumplen.

### 1.2. Seguridad
Garantiza que la información esté protegida frente a accesos no autorizados, modificaciones o destrucción. En la Administración Pública española se enmarca bajo el **Esquema Nacional de Seguridad (ENS - RD 311/2022)**.

**Patrón Lógico - Dimensiones de la Seguridad (Regla mnemotécnica CIDTA):**
1.  **Confidencialidad:** Solo accede a la información quien tiene permiso.
2.  **Integridad:** La información no se altera de forma no autorizada o fraudulenta.
3.  **Disponibilidad:** El sistema funciona y es accesible cuando se necesita.
4.  **Trazabilidad:** Saber quién ha hecho qué, cuándo y desde dónde (mediante registros o logs).
5.  **Autenticidad:** Garantizar que quien accede es realmente quien dice ser (ej. mediante certificado digital).

*Nota Métrica v3:* Métrica Versión 3 cuenta con una **Interfaz de Seguridad (SEG)** cuyo objetivo es incorporar en los sistemas de información mecanismos de seguridad adicionales a lo largo de todos los procesos (desde la Planificación hasta el Mantenimiento) [cite: 3].

El propio **Real Decreto 311/2022, de 3 de mayo**, que deroga y sustituye al anterior RD 3/2010, formaliza literalmente estas cinco dimensiones en su Anexo I, indicando que "se tendrán en cuenta las siguientes dimensiones de la seguridad, que se identificarán por sus correspondientes iniciales en mayúsculas: a) Confidencialidad [C]; b) Integridad [I]; c) Trazabilidad [T]; d) Autenticidad [A]; e) Disponibilidad [D]". Es habitual encontrar en test y manuales el acrónimo alternativo **DICAT**, que ordena las mismas cinco dimensiones empezando por Disponibilidad. Cada dimensión afectada por un incidente se clasifica en un **nivel de seguridad BAJO, MEDIO o ALTO**, y de la combinación de niveles surge la **categoría del sistema** (BÁSICA, MEDIA o ALTA), que determina qué medidas de seguridad son exigibles.

El ENS se estructura en **principios básicos** (seguridad integral, gestión de riesgos, prevención/reacción/recuperación, líneas de defensa, reevaluación periódica y diferenciación de responsabilidades) y en un conjunto de **medidas de seguridad** agrupadas en tres marcos: **marco organizativo**, **marco operacional** y **medidas de protección**, detalladas en su Anexo II. El organismo de referencia técnica que da soporte al ENS es el **CCN (Centro Criptológico Nacional)**, a través de la serie de guías **CCN-STIC**.

A nivel de estándares internacionales de gestión de la seguridad de la información, la referencia es la familia **ISO/IEC 27000**, en particular **ISO/IEC 27001** (Sistema de Gestión de Seguridad de la Información, SGSI) e **ISO/IEC 27002** (catálogo de controles). Para la seguridad específica en aplicaciones web, la referencia técnica más citada es el **OWASP Top 10**, que recopila los riesgos de seguridad más críticos en aplicaciones web (p. ej. control de acceso roto, fallos criptográficos, inyección), y el **OWASP ASVS** (*Application Security Verification Standard*) como marco de verificación de requisitos de seguridad en el análisis y diseño.

En cuanto a mecanismos técnicos, conviene diferenciar los dos grandes tipos de cifrado: **cifrado simétrico** (misma clave para cifrar y descifrar, ej. AES, más rápido, usado para grandes volúmenes de datos) y **cifrado asimétrico** (par de claves pública/privada, ej. RSA, más lento pero permite firma digital y no repudio, base de la autenticidad en la administración electrónica mediante certificados digitales).

### 1.3. Privacidad
Garantiza el tratamiento correcto y legal de los datos personales. Se rige por el **RGPD** (Reglamento (UE) 2016/679, General de Protección de Datos) y la **LOPDGDD** (Ley Orgánica 3/2018, de Protección de Datos Personales y garantía de los derechos digitales).

**Patrón Lógico - Conceptos Clave para el Test:**
*   **Privacidad desde el diseño (Privacy by Design):** La protección de datos se integra desde la fase inicial de análisis y diseño arquitectónico, no como un "parche" que se añade al final de la programación.
*   **Privacidad por defecto (Privacy by Default):** El sistema debe venir configurado con la máxima privacidad posible desde el inicio, sin que el usuario tenga que configurar nada (ej. casillas de "Acepto ceder mis datos" siempre desmarcadas al entrar).
*   **Minimización de datos:** El sistema solo debe solicitar y almacenar los datos estrictamente necesarios para cumplir su finalidad.

Ambos principios están regulados literalmente en el **artículo 25 del RGPD**, titulado "Protección de datos desde el diseño y por defecto". El apartado 1 exige al responsable del tratamiento aplicar, "tanto en el momento de determinar los medios de tratamiento como en el momento del propio tratamiento, medidas técnicas y organizativas apropiadas, como la seudonimización, concebidas para aplicar de forma efectiva los principios de protección de datos". El apartado 2 concreta la privacidad por defecto: el responsable garantizará que, por defecto, "solo sean objeto de tratamiento los datos personales que sean necesarios para cada uno de los fines específicos del tratamiento", aplicándose esta obligación a la cantidad de datos recogidos, la extensión de su tratamiento, su plazo de conservación y su accesibilidad.

Conviene relacionar la privacidad con los **principios generales del tratamiento de datos** del artículo 5 RGPD, muy preguntados de forma aislada: licitud, lealtad y transparencia; limitación de la finalidad; **minimización de datos**; exactitud; limitación del plazo de conservación; integridad y confidencialidad; y responsabilidad proactiva (*accountability*).

Otros conceptos que amplían y suelen aparecer junto a Privacy by Design/Default:
*   **Evaluación de Impacto relativa a la Protección de Datos (EIPD/DPIA):** análisis obligatorio (art. 35 RGPD) cuando un tratamiento pueda entrañar un alto riesgo para los derechos de las personas, típico en sistemas de la Administración con tratamientos masivos o datos sensibles.
*   **Seudonimización vs. anonimización:** la seudonimización sustituye los identificadores directos por un código, pero permite revertir el proceso con información adicional (sigue siendo dato personal); la anonimización elimina la posibilidad de reidentificación de forma irreversible (deja de ser dato personal y de estar sujeto al RGPD).
*   **Derechos ARCO-POL / derechos digitales (LOPDGDD):** acceso, rectificación, cancelación/supresión (derecho al olvido), oposición, portabilidad, limitación del tratamiento, y los derechos digitales específicos de la LOPDGDD (ej. derecho al olvido en búsquedas de internet, derecho a la educación digital).
*   **AEPD (Agencia Española de Protección de Datos):** autoridad de control nacional; publica guías de referencia como la *Guía de Privacidad desde el Diseño*, que recoge estrategias de optimización, configurabilidad y restricción para implementar el artículo 25 RGPD en la práctica.

---

## 2. Ejemplo Real (Sin analogías)

Imagina que estás desarrollando la nueva **Sede Electrónica de la DGT** para que los ciudadanos consulten los puntos de su carnet de conducir.
*   **Requisito Funcional:** El ciudadano introduce su DNI y el sistema le muestra el saldo de puntos.
*   **Análisis de Rendimiento:** La web debe soportar a 50.000 ciudadanos consultando a la vez el día que se publica una nueva ley de tráfico sin que los servidores se caigan (Escalabilidad), y debe devolver el resultado en menos de 2 segundos (Tiempo de respuesta). Antes de publicarse, el equipo ejecuta una prueba de carga simulando esos 50.000 usuarios y una prueba de estrés para averiguar en qué punto exacto se degradaría el servicio.
*   **Análisis de Seguridad:** Si un atacante intenta interceptar la conexión de red, el tráfico va cifrado y no puede leerlo (Confidencialidad, mediante cifrado simétrico TLS). Si intenta sumar 10 puntos extra a su cuenta, el sistema bloquea la transacción (Integridad) y guarda un registro del intento de ataque (Trazabilidad). Al tratarse de un sistema de la Administración General del Estado, se le asigna una categoría ENS (por ejemplo MEDIA) que determina qué medidas del Anexo II del RD 311/2022 son obligatorias.
*   **Análisis de Privacidad:** El sistema no le pide al ciudadano información sobre sus enfermedades o afiliación sindical, solo el DNI (Minimización de datos, art. 5 RGPD). Además, la opción de "Enviar historial de infracciones a aseguradoras" viene apagada desde el principio (Privacidad por defecto, art. 25.2 RGPD), y si en el futuro se plantea cruzar estos datos con otras bases de datos sanitarias, sería obligatorio realizar antes una Evaluación de Impacto (EIPD).

---

## 3. Patrones de Examen y "Palabras Chivatas"

| Concepto | Palabra Chivata en el Test |
| :--- | :--- |
| **Requisito Funcional vs No Funcional** | Funcional = "Qué hace el sistema", "Comportamiento". No Funcional = "Cómo lo hace", "Restricción", "Atributo de calidad". |
| **Throughput** | "Número de transacciones por segundo", "Carga de procesamiento", "Tasa de transferencia". |
| **Escalabilidad** | "Adaptarse a mayor demanda", "Añadir recursos sin rediseñar". |
| **Prueba de carga vs. estrés** | Carga = "volumen esperado/normal"; Estrés = "por encima de la capacidad", "punto de ruptura". |
| **Confidencialidad (Seguridad)** | "Acceso no autorizado", "Cifrado", "Ocultación de la información". |
| **Integridad (Seguridad)** | "Modificación no autorizada", "Alteración o manipulación de datos". |
| **ENS / RD 311/2022** | "Dimensiones CIDTA/DICAT", "Categoría BÁSICA/MEDIA/ALTA", "CCN-STIC". |
| **Privacidad desde el diseño** | "Fase de creación", "Fase de ingeniería de requisitos", "Integrado en la arquitectura original", "Artículo 25.1 RGPD". |
| **Privacidad por defecto** | "Sin acción del usuario", "Configuración inicial más restrictiva", "Artículo 25.2 RGPD". |
| **Seudonimización vs. anonimización** | Seudonimización = "reversible con clave adicional"; Anonimización = "irreversible, deja de ser dato personal". |

### 3.1. Simulacro de Test: Desmontando trampas

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
