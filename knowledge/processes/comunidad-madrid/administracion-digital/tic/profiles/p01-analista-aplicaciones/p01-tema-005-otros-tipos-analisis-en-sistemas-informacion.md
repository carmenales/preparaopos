---
id: "cm-ad-ia-p01-tema-005-analisis-no-funcional"
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
created_at: "2026-08-08"
last_reviewed: null
ai_generated: true
ai_sources:
  - "gemini"
needs_human_review: true
---

# Tema 5. Otros tipos de análisis en los sistemas de información

## 1. Análisis de Requisitos No Funcionales (RNF)

Mientras que los requisitos funcionales definen **qué** hace el sistema, los Requisitos No Funcionales (RNF) definen **cómo** lo hace. Son atributos de calidad y restricciones impuestas al sistema [cite: 3]. Si no se cumplen, el sistema fracasa aunque la funcionalidad central haga su trabajo. La identificación de estos requisitos forma parte de las tareas clave de la Ingeniería de Requerimientos [cite: 3].

### 1.1. Rendimiento (Performance)
Define las métricas operativas del sistema bajo una carga de trabajo determinada.
**Patrón Lógico - Métricas Clave:**
*   **Tiempo de respuesta:** Lo que tarda el sistema en reaccionar a una petición del usuario (ej. milisegundos en cargar una pantalla o procesar un pago).
*   **Throughput (Rendimiento de procesamiento):** Número de transacciones o peticiones que el sistema puede procesar por unidad de tiempo (ej. 1000 transacciones por segundo).
*   **Escalabilidad:** Capacidad del sistema para manejar más carga añadiendo recursos (Escalabilidad vertical: añadir más RAM/CPU a un servidor; Escalabilidad horizontal: añadir más servidores al clúster).
*   **Consumo de recursos:** Límites en el uso de memoria, procesador y ancho de banda de red.

### 1.2. Seguridad
Garantiza que la información esté protegida frente a accesos no autorizados, modificaciones o destrucción. En la Administración Pública española se enmarca bajo el **Esquema Nacional de Seguridad (ENS - RD 311/2022)**.

**Patrón Lógico - Dimensiones de la Seguridad (Regla mnemotécnica CIDTA):**
1.  **Confidencialidad:** Solo accede a la información quien tiene permiso.
2.  **Integridad:** La información no se altera de forma no autorizada o fraudulenta.
3.  **Disponibilidad:** El sistema funciona y es accesible cuando se necesita.
4.  **Trazabilidad:** Saber quién ha hecho qué, cuándo y desde dónde (mediante registros o logs).
5.  **Autenticidad:** Garantizar que quien accede es realmente quien dice ser (ej. mediante certificado digital).

*Nota Métrica v3:* Métrica Versión 3 cuenta con una **Interfaz de Seguridad (SEG)** cuyo objetivo es incorporar en los sistemas de información mecanismos de seguridad adicionales a lo largo de todos los procesos (desde la Planificación hasta el Mantenimiento) [cite: 3].

### 1.3. Privacidad
Garantiza el tratamiento correcto y legal de los datos personales. Se rige por el **RGPD** (Reglamento General de Protección de Datos europeo) y la **LOPDGDD** (Ley Orgánica 3/2018).

**Patrón Lógico - Conceptos Clave para el Test:**
*   **Privacidad desde el diseño (Privacy by Design):** La protección de datos se integra desde la fase inicial de análisis y diseño arquitectónico, no como un "parche" que se añade al final de la programación.
*   **Privacidad por defecto (Privacy by Default):** El sistema debe venir configurado con la máxima privacidad posible desde el inicio, sin que el usuario tenga que configurar nada (ej. casillas de "Acepto ceder mis datos" siempre desmarcadas al entrar).
*   **Minimización de datos:** El sistema solo debe solicitar y almacenar los datos estrictamente necesarios para cumplir su finalidad.

---

## 2. Ejemplo Real (Sin analogías)

Imagina que estás desarrollando la nueva **Sede Electrónica de la DGT** para que los ciudadanos consulten los puntos de su carnet de conducir.
*   **Requisito Funcional:** El ciudadano introduce su DNI y el sistema le muestra el saldo de puntos.
*   **Análisis de Rendimiento:** La web debe soportar a 50.000 ciudadanos consultando a la vez el día que se publica una nueva ley de tráfico sin que los servidores se caigan (Escalabilidad), y debe devolver el resultado en menos de 2 segundos (Tiempo de respuesta).
*   **Análisis de Seguridad:** Si un atacante intenta interceptar la conexión de red, el tráfico va cifrado y no puede leerlo (Confidencialidad). Si intenta sumar 10 puntos extra a su cuenta, el sistema bloquea la transacción (Integridad) y guarda un registro del intento de ataque (Trazabilidad).
*   **Análisis de Privacidad:** El sistema no le pide al ciudadano información sobre sus enfermedades o afiliación sindical, solo el DNI (Minimización de datos). Además, la opción de "Enviar historial de infracciones a aseguradoras" viene apagada desde el principio (Privacidad por defecto).

---

## 3. Patrones de Examen y "Palabras Chivatas"

| Concepto | Palabra Chivata en el Test |
| :--- | :--- |
| **Requisito Funcional vs No Funcional** | Funcional = "Qué hace el sistema", "Comportamiento". No Funcional = "Cómo lo hace", "Restricción", "Atributo de calidad". |
| **Throughput** | "Número de transacciones por segundo", "Carga de procesamiento", "Tasa de transferencia". |
| **Escalabilidad** | "Adaptarse a mayor demanda", "Añadir recursos sin rediseñar". |
| **Confidencialidad (Seguridad)** | "Acceso no autorizado", "Cifrado", "Ocultación de la información". |
| **Integridad (Seguridad)** | "Modificación no autorizada", "Alteración o manipulación de datos". |
| **Privacidad desde el diseño** | "Fase de creación", "Fase de ingeniería de requisitos", "Integrado en la arquitectura original". |

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
